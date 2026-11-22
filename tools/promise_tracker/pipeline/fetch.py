#!/usr/bin/env python3
"""Stage 1: fetch earnings-call transcripts for one NSE symbol.

    python3 -I fetch.py SKIPPER --since 2024-07-01 [--until 2026-11-30] [--cache DIR] [--refresh]

* Lists the symbol's NSE corporate announcements (one call, full history), keeps
  transcript filings (attachment text or file name contains "ranscript", which also
  catches typos like "Trancript"; .zip archives are skipped).
* Downloads ONLY the PDFs whose filing date is inside [--since, --until]
  (nse_fetch.py --download ignores dates; that was pilot lesson #1).
* Converts each PDF with `pdftotext -layout`, finds the date the call was held
  (from the cover letter / title page), and writes manifest.json.
* Everything is cached; re-runs only fetch what is missing. --refresh re-pulls the
  announcement list (do this each quarter).

NSE notes (2026-11): the API lives on www.nseindia.in; a SHORT User-Agent
('Mozilla/5.0') plus Accept/Accept-Language/Referer works without cookies; the
long Chrome UA string has been getting stream resets. Requests are spaced >= 1.5 s
with exponential back-off on 403/429/503. PDFs are untrusted data.
"""
import argparse
import datetime as dt
import gzip
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

API = "https://www.nseindia.in/api/corporate-announcements"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json, text/plain, */*",
           "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip",
           "Referer": "https://www.nseindia.in/"}
MIN_GAP = 1.5
_last = [0.0]


def http_get(url, tries=4):
    for i in range(tries):
        wait = MIN_GAP - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=60) as r:
                body = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
                return body
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 503) and i < tries - 1:
                time.sleep(5 * 2 ** i)
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if i < tries - 1:
                time.sleep(5 * 2 ** i)
                continue
            raise
    raise RuntimeError("unreachable")


def list_announcements(symbol, root, refresh=False, max_age_h=24):
    path = os.path.join(C.sym_dir(root, symbol), "announcements.json")
    if not refresh and os.path.exists(path) and time.time() - os.path.getmtime(path) < max_age_h * 3600:
        return C.load_json(path)
    import json
    body = http_get(API + "?" + urllib.parse.urlencode({"index": "equities", "symbol": symbol}))
    txt = body.decode("utf-8", "replace")
    if txt.lstrip().startswith("<"):
        raise RuntimeError("NSE returned HTML instead of JSON (blocked or endpoint moved)")
    rows = json.loads(txt)
    rows = rows.get("data", rows) if isinstance(rows, dict) else rows
    C.save_json(path, rows)
    return rows


def is_transcript(r):
    blob = ((r.get("attchmntText") or "") + " " + (r.get("attchmntFile") or "")).lower()
    url = (r.get("attchmntFile") or "").lower()
    return ("ranscript" in blob or "trancript" in blob) and url.endswith(".pdf")


def pdf_to_text(pdf, txt):
    if not shutil.which("pdftotext"):
        raise SystemExit("pdftotext not found (apt install poppler-utils)")
    subprocess.run(["pdftotext", "-layout", pdf, txt], check=True, timeout=180)


def detect_call_date(text, filed):
    """Earliest date in the first ~6k chars that lies within 35 days before filing."""
    head = text[:6000]
    found = [(pos, d) for pos, d in C.find_dates(head) if filed - dt.timedelta(days=35) <= d <= filed]
    # a date right after "held on" / "conducted on" is the call date
    for pos, d in found:
        if re.search(r"(held|conducted|organi[sz]ed|scheduled)\s+(on\s+)?(\w+day,?\s+)?(the\s+)?$",
                     head[max(0, pos - 60):pos], re.I):
            return d, "text(held on)"
    # otherwise the earliest date that is not a quarter-end ("quarter ended 31st December")
    qends = {(3, 31), (6, 30), (9, 30), (12, 31)}
    cands = [d for _, d in found if (d.month, d.day) not in qends] or [d for _, d in found]
    if cands:
        return min(cands), "text"
    return filed - dt.timedelta(days=5), "assumed(filing-5d)"


COVER_RX = re.compile(r"(has been |is being |been )?(made )?available on (the |our )?(Bank[’']?s?|Company[’']?s?|our)?\s*website|"
                      r"uploaded on (the |our )?(Bank[’']?s?|Company[’']?s?)?\s*website|placed on (the )?website", re.I)


def add_call(manifest, fn, url, filed, pdf, txt, text, source="nse"):
    call_date, how = detect_call_date(text, filed)
    q, fy = C.reported_quarter_for_call(call_date, text)
    words = len(text.split())
    # v1.1 (FEDERALBNK dry run): many banks file only a cover letter on NSE that says the transcript
    # "has been made available on the Bank's website". That is NOT a scanned PDF; OCR will not help.
    cover = words < 1500 and bool(COVER_RX.search(re.sub(r"\s+", " ", text)))   # -layout pads words with spaces
    manifest[fn] = {"file": fn, "url": url, "filed": filed.isoformat(), "call_date": call_date.isoformat(),
                    "call_date_source": how, "quarter": C.qlabel(q, fy), "pdf": pdf, "txt": txt,
                    "words": words, "scanned_suspect": words < 1500 and not cover,
                    "cover_letter_only": cover, "source": source,
                    "skip": words < 1500}
    flag = ("  <-- COVER LETTER ONLY: transcript is on the company website; download it and pass "
            "--local PDF@FILED (skipped)") if cover else ("  <-- few words: scanned PDF? needs OCR (skipped)"
                                                          if words < 1500 else "")
    print(f"  {C.qlabel(q, fy)} call {call_date} ({how}) filed {filed} {words} words {fn}{flag}")


def add_local(manifest, spec, pdir, tdir):
    """--local PATH@YYYY-MM-DD : a transcript PDF fetched from the company website (untrusted data).
    The date is the filing/publication date used to bound the call-date search."""
    path, _, d = spec.rpartition("@")
    if not path:
        raise SystemExit("--local needs PATH@YYYY-MM-DD")
    filed = dt.date.fromisoformat(d)
    fn = "local_" + os.path.basename(path)
    pdf = os.path.join(pdir, fn)
    if not os.path.exists(pdf):
        shutil.copyfile(path, pdf)
    txt = os.path.join(tdir, fn[:-4] + ".txt")
    if not os.path.exists(txt):
        pdf_to_text(pdf, txt)
    add_call(manifest, fn, "local:" + os.path.abspath(path), filed, pdf, txt,
             open(txt, errors="replace").read(), source="local")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol")
    p.add_argument("--since", required=True, help="YYYY-MM-DD (filing date, inclusive)")
    p.add_argument("--until", help="YYYY-MM-DD (filing date, inclusive; default today)")
    p.add_argument("--cache")
    p.add_argument("--refresh", action="store_true", help="re-pull the announcement list")
    p.add_argument("--local", action="append", metavar="PDF@YYYY-MM-DD",
                   help="add a transcript PDF from the company website (repeatable); replaces an NSE cover letter")
    a = p.parse_args(argv)
    sym = a.symbol.upper()
    root = C.cache_root(a.cache)
    since = dt.date.fromisoformat(a.since)
    until = dt.date.fromisoformat(a.until) if a.until else dt.date.today()

    rows = list_announcements(sym, root, a.refresh)
    tr = [r for r in rows if is_transcript(r)]
    sel = [r for r in tr if since <= C.parse_nse_date(r["an_dt"]) <= until]
    print(f"{sym}: {len(rows)} announcements, {len(tr)} transcript PDFs, {len(sel)} in {since}..{until}")

    pdir, tdir = C.sym_dir(root, sym, "pdf"), C.sym_dir(root, sym, "txt")
    mpath = os.path.join(C.sym_dir(root, sym), "manifest.json")
    manifest = {m["file"]: m for m in (C.load_json(mpath, []) or [])}
    for r in sorted(sel, key=lambda r: C.parse_nse_date(r["an_dt"])):
        url = r["attchmntFile"]
        fn = os.path.basename(urllib.parse.urlparse(url).path)
        pdf = os.path.join(pdir, fn)
        txt = os.path.join(tdir, fn[:-4] + ".txt")
        if not os.path.exists(pdf) or os.path.getsize(pdf) == 0:
            data = http_get(url)
            if not data.startswith(b"%PDF"):
                print("  skip (not a PDF):", fn)
                continue
            with open(pdf, "wb") as f:
                f.write(data)
            print("  downloaded", fn, f"{len(data) // 1024} KB")
        if not os.path.exists(txt):
            pdf_to_text(pdf, txt)
        text = open(txt, errors="replace").read()
        filed = C.parse_nse_date(r["an_dt"])
        add_call(manifest, fn, url, filed, pdf, txt, text)
    for spec in a.local or []:
        add_local(manifest, spec, pdir, tdir)
    # a local/website copy of a call replaces an NSE cover letter for the same quarter
    good = {m["quarter"] for m in manifest.values() if not m.get("skip")}
    for m in manifest.values():
        if m.get("cover_letter_only") and m["quarter"] in good - {None}:
            m["replaced_by_local"] = True
    out = sorted(manifest.values(), key=lambda m: m["call_date"])
    for m in out:   # entries written by v1 lack the flags
        m.setdefault("skip", m.get("words", 9999) < 1500)
    C.save_json(mpath, out)
    print("manifest:", mpath, len(out), "calls")


if __name__ == "__main__":
    main()
