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
    <ar_root>/<SYMBOL>/txt/AR_FY26.txt       pdftotext -layout output (ZIPs: most likely AR PDF inside, or its numbered parts)
    <ar_root>/<SYMBOL>/manifest.json         one row per document: file, url, filed, call_date (= submission
                                             date), quarter ("ARFY26"), fy, kind, words, skip
<ar_root> = --cache if given, else $PT_CACHE/ar, else ~/.cache/fein_promise_tracker/ar.
PDFs and ZIPs are untrusted data. They are written to <SYMBOL>/pdf/, converted, and DELETED (unless
--keep-pdf); ZIP members are read in memory and only *.pdf members are used (no path is taken from the archive).
File type is detected by magic bytes; a corrupt ZIP/PDF skips that year with a WARNING instead of crashing.

Optional extra documents from the NSE announcement list (each counts as its own dated "call", kind shown in
the manifest): --presentations (investor presentations), --outcomes ("Outcome of Board Meeting" PDFs, which
are mostly results; use with --since). Both are off by default.
"""
import argparse
import datetime as dt
import io
import os
import re
import subprocess
import sys
import urllib.parse
import zipfile
import zlib

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


ZIP_MAX_MEMBER = 400 * 2 ** 20
_LIKELY = re.compile(r"annual|integrated|\bar\b|\bar[\s_-]*20\d\d|report", re.I)
_UNLIKELY = re.compile(r"notice|agm|brsr|business\s*responsib|cover|letter|intimation|proxy|attendance|e-?voting", re.I)
_PART = re.compile(r"part[\s_-]*\d+|vol(ume)?[\s_-]*\d+", re.I)


def pick_zip_members(infos):
    """Choose which ZIP members hold the annual report. `infos` = zipfile.ZipInfo list (or objects with
    .filename / .file_size / .is_dir()). Rule: the most likely PDF (name looks like an annual report and not like
    a notice/BRSR/cover letter), ties broken by size (largest). If that file is one of several numbered parts
    ("Part 1", "Vol 2"), all numbered parts are returned in name order. Returns [] if there is no usable PDF."""
    pdfs = [i for i in infos if not i.is_dir() and i.filename.lower().endswith(".pdf")
            and "__macosx" not in i.filename.lower() and 0 < i.file_size <= ZIP_MAX_MEMBER]
    if not pdfs:
        return []

    def score(i):
        b = os.path.basename(i.filename)
        return (bool(_LIKELY.search(b)) - bool(_UNLIKELY.search(b)), i.file_size)
    best = max(pdfs, key=score)
    if _PART.search(os.path.basename(best.filename)):
        parts = [i for i in pdfs if _PART.search(os.path.basename(i.filename))
                 and not _UNLIKELY.search(os.path.basename(i.filename))]
        if len(parts) > 1:
            return sorted(i.filename for i in parts)
    return [best.filename]


def extract(data, url, pdir, stem, keep=False):
    """PDF or ZIP bytes -> (text, n_pdfs). The type is detected by magic bytes, not by the URL extension (NSE
    sometimes lists an AR as .zip, or a .pdf link serves a ZIP). ZIP: the most likely annual-report PDF (or all its
    numbered parts) is used; see pick_zip_members. Raises ValueError for anything unusable, including corrupt or
    encrypted ZIPs and PDFs pdftotext cannot read, so the caller can skip that year with a warning."""
    if keep:
        with open(os.path.join(pdir, stem + os.path.splitext(urllib.parse.urlparse(url).path)[1]), "wb") as f:
            f.write(data)
    head = data[:1024]
    try:
        if head.lstrip().startswith(b"%PDF") or b"%PDF-" in head:
            return pdf_bytes_to_text(data, pdir, stem), 1
        if data.startswith(b"PK"):
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                names = pick_zip_members(z.infolist())
                if not names:
                    raise ValueError("ZIP holds no usable PDF (members: %s)"
                                     % ", ".join(n for n in z.namelist()[:8]))
                parts = []
                for i, n in enumerate(names):
                    blob = z.read(n)
                    if b"%PDF" not in blob[:1024]:
                        print(f"  warning: ZIP member {os.path.basename(n)!r} is not a PDF; ignored")
                        continue
                    parts.append(pdf_bytes_to_text(blob, pdir, f"{stem}_part{i:02d}"))
                if not parts:
                    raise ValueError("ZIP members named .pdf are not PDFs")
            return "\n\f\n".join(parts), len(parts)
    except (zipfile.BadZipFile, zlib.error, EOFError, NotImplementedError, RuntimeError, OSError) as e:
        raise ValueError(f"corrupt or unreadable archive/PDF ({type(e).__name__}: {e})") from e
    except subprocess.CalledProcessError as e:
        raise ValueError(f"pdftotext failed (exit {e.returncode})") from e
    except subprocess.TimeoutExpired as e:
        raise ValueError("pdftotext timed out") from e
    raise ValueError("neither PDF nor ZIP (first bytes %r)" % data[:8])


def add_doc(manifest, sym, root, key, url, filed, kind, label, fy, keep=False):
    tdir, pdir = C.sym_dir(root, sym, "txt"), C.sym_dir(root, sym, "pdf")
    txt = os.path.join(tdir, key + ".txt")
    nparts = None
    if not os.path.exists(txt) or os.path.getsize(txt) == 0:
        try:
            data = FE.http_get(url)
            text, nparts = extract(data, url, pdir, key, keep)
        except ValueError as e:
            print(f"  WARNING: skipping {key} ({label}): {e}", file=sys.stderr)
            return
        except Exception as e:  # network errors etc.: one bad year must not stop the run
            print(f"  WARNING: skipping {key} ({label}): download failed ({type(e).__name__}: {e})", file=sys.stderr)
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
