#!/usr/bin/env python3
"""AR mode, stage 1: fetch the last N annual reports of an NSE symbol, extract text, delete the PDFs.

    python3 -I ar_fetch.py SUNFLAG [--n 5] [--cache DIR] [--refresh]
                           [--presentations] [--outcomes] [--since YYYY-MM-DD] [--keep-pdf]

For companies that hold NO earnings calls (many Indian small caps; SUNFLAG had none, see
research_notes/Deep dives/SUNFLAG_live.md section 10), the annual report is the only regular forward-looking
document. In AR mode each annual report is treated as one "call", dated at its NSE SUBMISSION date
(broadcast time, else the time stamp in the file name; nse_fetch.annual_reports). The next year's report is
the evidence for the previous one's promises.

Cache layout (an AR-mode cache root is separate from the concall cache, so the two never mix):
    <ar_root>/<SYMBOL>/ar_list.json          NSE api/annual-reports rows (+ submitted)
    <ar_root>/<SYMBOL>/txt/AR_FY26.txt       pdftotext -layout output (ZIPs: all PDFs inside, name order)
    <ar_root>/<SYMBOL>/manifest.json         one row per document: file, url, filed, call_date (= submission
                                             date), quarter ("ARFY26"), fy, kind, words, skip
<ar_root> = --cache if given, else $PT_CACHE/ar, else ~/.cache/fein_promise_tracker/ar.
PDFs and ZIPs are untrusted data. They are written to <SYMBOL>/pdf/, converted, and DELETED (unless
--keep-pdf); ZIP members are read in memory and only *.pdf members are used (no path is taken from the archive).

Optional extra documents from the NSE announcement list (each counts as its own dated "call", kind shown in
the manifest): --presentations (investor presentations), --outcomes ("Outcome of Board Meeting" PDFs, which
are mostly results; use with --since). Both are off by default.
"""
import argparse
import datetime as dt
import io
import os
import re
import sys
import urllib.parse
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))   # tools/ for nse_fetch
import common as C  # noqa: E402
import fetch as FE  # noqa: E402

MIN_WORDS = 8000   # a full annual report has 60k-200k words; fewer means scanned/partial


def ar_root(cache=None):
    if cache:
        os.makedirs(cache, exist_ok=True)
        return cache
    base = os.environ.get("PT_CACHE") or os.path.expanduser("~/.cache/fein_promise_tracker")
    d = os.path.join(base, "ar")
    os.makedirs(d, exist_ok=True)
    return d


def list_ars(sym, root, refresh=False):
    path = os.path.join(C.sym_dir(root, sym), "ar_list.json")
    if not refresh and os.path.exists(path):
        return C.load_json(path)
    import nse_fetch   # tools/nse_fetch.py (standard library)
    rows = nse_fetch.annual_reports(sym)
    C.save_json(path, rows)
    return rows


def pick_latest(rows, n):
    """One row per fiscal year (fromYr-toYr): the latest submission wins (a 'Revised' upload replaces 'New')."""
    by = {}
    for r in rows:
        if not r.get("fileName") or not r.get("toYr"):
            continue
        k = int(r["toYr"])
        if k not in by or (r.get("submitted") or "") > (by[k].get("submitted") or ""):
            by[k] = r
    return [by[k] for k in sorted(by)[-n:]]


def pdf_bytes_to_text(data, pdir, stem):
    """Write PDF bytes, run pdftotext -layout, delete the PDF. Returns text."""
    pdf = os.path.join(pdir, stem + ".pdf")
    txt = os.path.join(pdir, stem + ".txt")
    with open(pdf, "wb") as f:
        f.write(data)
    try:
        FE.pdf_to_text(pdf, txt)
        return open(txt, errors="replace").read()
    finally:
        for x in (pdf, txt):
            if os.path.exists(x):
                os.remove(x)


def extract(data, url, pdir, stem, keep=False):
    """PDF or ZIP bytes -> text (ZIP: every .pdf member in name order, joined)."""
    if keep:
        with open(os.path.join(pdir, stem + os.path.splitext(urllib.parse.urlparse(url).path)[1]), "wb") as f:
            f.write(data)
    if data.startswith(b"%PDF"):
        return pdf_bytes_to_text(data, pdir, stem), 1
    if data.startswith(b"PK"):
        parts = []
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = sorted(n for n in z.namelist() if n.lower().endswith(".pdf"))
            for i, n in enumerate(names):
                if z.getinfo(n).file_size > 400 * 2 ** 20:
                    continue
                parts.append(pdf_bytes_to_text(z.read(n), pdir, f"{stem}_part{i:02d}"))
        return "\n\f\n".join(parts), len(parts)
    raise ValueError("neither PDF nor ZIP")


def add_doc(manifest, sym, root, key, url, filed, kind, label, fy, keep=False):
    tdir, pdir = C.sym_dir(root, sym, "txt"), C.sym_dir(root, sym, "pdf")
    txt = os.path.join(tdir, key + ".txt")
    nparts = None
    if not os.path.exists(txt) or os.path.getsize(txt) == 0:
        data = FE.http_get(url)
        try:
            text, nparts = extract(data, url, pdir, key, keep)
        except ValueError as e:
            print(f"  skip {key}: {e}")
            return
        with open(txt, "w") as f:
            f.write(text)
        print(f"  downloaded {key} {len(data) // 1024} KB -> {len(text.split())} words (PDF deleted)")
    text = open(txt, errors="replace").read()
    words = len(text.split())
    min_w = MIN_WORDS if kind == "annual_report" else 300
    manifest[key] = {"file": key, "url": url, "filed": filed.isoformat(), "call_date": filed.isoformat(),
                     "call_date_source": "nse submission date", "quarter": label, "fy": fy, "kind": kind,
                     "txt": txt, "words": words, "parts": nparts, "scanned_suspect": words < min_w,
                     "cover_letter_only": False, "source": "nse", "skip": words < min_w}
    flag = "  <-- few words: scanned PDF? needs OCR (skipped)" if words < min_w else ""
    print(f"  {label} submitted {filed} {words} words {key}{flag}")


EXTRA_RX = {"presentation": re.compile(r"investor\s+presentation|analyst\s+presentation|corporate\s+presentation", re.I),
            "board_outcome": re.compile(r"outcome\s+of\s+(the\s+)?board\s+meeting", re.I)}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol")
    p.add_argument("--n", type=int, default=5, help="number of latest annual reports (default 5)")
    p.add_argument("--cache", help="AR-mode cache root (default $PT_CACHE/ar)")
    p.add_argument("--refresh", action="store_true", help="re-pull the NSE annual-report and announcement lists")
    p.add_argument("--presentations", action="store_true", help="also investor presentations from announcements")
    p.add_argument("--outcomes", action="store_true", help="also 'Outcome of Board Meeting' PDFs")
    p.add_argument("--since", help="YYYY-MM-DD lower bound for --presentations/--outcomes (default: oldest AR's FY start)")
    p.add_argument("--keep-pdf", action="store_true", help="keep the downloaded PDF/ZIP files (default: delete)")
    a = p.parse_args(argv)
    sym = a.symbol.upper()
    root = ar_root(a.cache)
    rows = list_ars(sym, root, a.refresh)
    sel = pick_latest(rows, a.n)
    print(f"{sym}: {len(rows)} annual-report rows on NSE; using the latest {len(sel)}")
    mpath = os.path.join(C.sym_dir(root, sym), "manifest.json")
    manifest = {m["file"]: m for m in (C.load_json(mpath, []) or [])}
    for r in sel:
        fy = int(r["toYr"])
        sub = r.get("submitted")
        if not sub:
            print("  no submission date; skipped", r.get("fileName"))
            continue
        filed = dt.date.fromisoformat(sub[:10])
        add_doc(manifest, sym, root, f"AR_FY{fy % 100:02d}", r["fileName"], filed, "annual_report",
                f"ARFY{fy % 100:02d}", fy, a.keep_pdf)
    if a.presentations or a.outcomes:
        since = dt.date.fromisoformat(a.since) if a.since else dt.date(int(sel[0]["fromYr"]), 4, 1)
        ann = FE.list_announcements(sym, root, a.refresh)
        for r in sorted(ann, key=lambda r: C.parse_nse_date(r["an_dt"])):
            d = C.parse_nse_date(r["an_dt"])
            url = r.get("attchmntFile") or ""
            blob = (r.get("attchmntText") or "") + " " + (r.get("desc") or "")
            if d < since or not url.lower().endswith(".pdf"):
                continue
            for kind, on in (("presentation", a.presentations), ("board_outcome", a.outcomes)):
                if on and EXTRA_RX[kind].search(blob):
                    key = f"{'IP' if kind == 'presentation' else 'BM'}_{d.isoformat()}_" + \
                          C.slugify(os.path.basename(urllib.parse.urlparse(url).path)[:-4], 30)
                    add_doc(manifest, sym, root, key, url, d, kind, f"{'IP' if kind == 'presentation' else 'BM'}{d:%Y%m%d}",
                            C.fy_of(d), a.keep_pdf)
                    break
    out = sorted(manifest.values(), key=lambda m: m["call_date"])
    C.save_json(mpath, out)
    print("manifest:", mpath, len(out), "documents")


if __name__ == "__main__":
    main()
