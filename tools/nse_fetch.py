#!/usr/bin/env python3
"""Polite NSE corporate-data fetcher (standard library only).

Tested 2026-11-19: www.nseindia.com 301-redirects to www.nseindia.in. On the
.in host the /api/corporate* endpoints answer JSON WITHOUT cookies if a
browser-like User-Agent + Accept + Accept-Language + Referer are sent.
Live quotes (quote-equity) are bot-protected and NOT supported.

Usage:
  python3 tools/nse_fetch.py announcements KPITTECH            # full history
  python3 tools/nse_fetch.py announcements --from 18-11-2026 --to 19-11-2026  # all cos
  python3 tools/nse_fetch.py transcripts KPITTECH [--download DIR]
  python3 tools/nse_fetch.py shareholding KPITTECH
  python3 tools/nse_fetch.py pledge [KPITTECH]                 # omit symbol = all cos
  python3 tools/nse_fetch.py sast KPITTECH
  python3 tools/nse_fetch.py insider KPITTECH                  # PIT Reg 7 disclosures
  python3 tools/nse_fetch.py results KPITTECH                  # quarterly result filings (old feed; stale after Q3 FY25)
  python3 tools/nse_fetch.py integrated KPITTECH               # integrated filings since Q3 FY25 (XBRL links)
  python3 tools/nse_fetch.py annual_reports KPITTECH [--download DIR]  # AR list + submission time (+ PDFs/ZIPs)
  python3 tools/nse_fetch.py bulk --from 01-11-2026 --to 19-11-2026
  python3 tools/nse_fetch.py block --from 01-11-2026 --to 19-11-2026
Options: --out FILE (write JSON), --raw (print full JSON instead of a summary),
         --limit N (summary mode: print at most N rows; default 0 = all rows; when cut, prints "showing N of M").
Dates are DD-MM-YYYY. Requests are spaced >=1.5 s; 403/429 triggers back-off.
Downloaded PDFs are untrusted data: extract with `pdftotext -layout f.pdf f.txt`.
"""
import argparse, gzip, json, os, sys, time, urllib.error, urllib.parse, urllib.request

BASE = "https://www.nseindia.in/api/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept": "application/json, text/plain, */*",
           "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip",
           "Referer": "https://www.nseindia.in/"}
MIN_GAP = 1.5
_last = [0.0]


def _get(url, binary=False, tries=4):
    for i in range(tries):
        wait = MIN_GAP - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                body = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
                if binary:
                    return body
                txt = body.decode("utf-8", "replace")
                if txt.lstrip().startswith("<"):
                    raise ValueError("HTML instead of JSON (endpoint changed/blocked)")
                return json.loads(txt)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429, 503) and i < tries - 1:
                time.sleep(5 * 2 ** i)
                continue
            raise
    raise RuntimeError("unreachable")


def api(path, **params):
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v})
    return _get(BASE + path + ("?" + q if q else ""))


def announcements(symbol=None, frm=None, to=None):
    return api("corporate-announcements", index="equities", symbol=symbol,
               from_date=frm, to_date=to)


def _stamp(fn):
    """Submission date from an AR file name: AR_<id>_<SYM>_<fy1>_<fy2>[_A_<n>]_<DDMMYYYY><hhmmss>[_<MMDDYYYYhhmmss>].<ext>.
    The first stamp is the company's upload (DDMMYYYY); a second one on older ZIPs is dissemination (MMDDYYYY).
    FY24 names often drop zero padding in the time part (e.g. 2908202422056), so only the 8-digit date is trusted
    when the stamp is shorter than 14 digits (time then reported as 00:00:00)."""
    import datetime as dt, re
    st = re.findall(r"_(\d{12,14})(?=[_.])", os.path.basename(fn))
    out = []
    for i, x in enumerate(st):
        for f in (("%m%d%Y", "%d%m%Y") if i else ("%d%m%Y",)):
            try:
                d = dt.datetime.strptime(x[:8], f)
                if len(x) == 14:
                    d = dt.datetime.strptime(x, f + "%H%M%S")
                out.append(d); break
            except ValueError:
                pass
    return max(out).strftime("%Y-%m-%d %H:%M:%S") if out else None


def annual_reports(symbol):
    """api/annual-reports (tested 2026-11-22). broadcast_dttm is '-' for most pre-FY24 rows, so `submitted` =
    broadcast time if present, else the latest time stamp in the file name (upload / dissemination)."""
    import datetime as dt
    rows = api("annual-reports", index="equities", symbol=symbol).get("data", [])
    for r in rows:
        b = r.get("broadcast_dttm") or "-"
        try:
            r["submitted"] = dt.datetime.strptime(b, "%d-%b-%Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            r["submitted"] = _stamp(r.get("fileName") or "")
    return rows


def transcripts(symbol):
    rows = announcements(symbol)
    return [r for r in rows if "ranscript" in (r.get("attchmntText") or "")
            or "ranscript" in (r.get("attchmntFile") or "")]


COMMANDS = {
    "shareholding": lambda a: api("corporate-share-holdings-master", index="equities", symbol=a.symbol),
    "pledge": lambda a: api("corporate-pledgedata", index="equities", symbol=a.symbol),
    "sast": lambda a: api("corporate-sast-reg29", index="equities", symbol=a.symbol),
    "insider": lambda a: api("corporates-pit", index="equities", symbol=a.symbol,
                             from_date=a.frm, to_date=a.to),
    "results": lambda a: api("corporates-financial-results", index="equities",
                             symbol=a.symbol, period="Quarterly"),
    # 2026-11-22 (FEDERALBNK dry run): "results" stops at the Dec-2024 quarter for many symbols; filings since
    # Q3 FY25 are "Integrated Filing- Financials" (XBRL incl. bank GNPA/NNPA %, CET1, RoA). Banks file a
    # balance sheet only at Sep/Mar quarter-ends.
    "integrated": lambda a: api("integrated-filing-results", index="equities", symbol=a.symbol,
                                type="Integrated Filing- Financials"),
    "bulk": lambda a: api("historicalOR/bulk-block-short-deals", optionType="bulk_deals",
                          symbol=a.symbol, **{"from": a.frm, "to": a.to}),
    "block": lambda a: api("historicalOR/bulk-block-short-deals", optionType="block_deals",
                           symbol=a.symbol, **{"from": a.frm, "to": a.to}),
    "announcements": lambda a: announcements(a.symbol, a.frm, a.to),
    "transcripts": lambda a: transcripts(a.symbol),
    "annual_reports": lambda a: annual_reports(a.symbol),
}


def summary_lines(cmd, rows, limit=0):
    """Summary-mode output lines. limit <= 0 prints every row; otherwise the first `limit` rows and a
    'showing N of M' line so a truncated list is never mistaken for the whole list."""
    n = len(rows) if hasattr(rows, "__len__") else None
    out = [f"{cmd}: {n if n is not None else '?'} rows"]
    if not isinstance(rows, list):
        return out
    shown = rows[:limit] if limit and limit > 0 else rows
    for r in shown:
        if cmd == "integrated":
            out.append(" | ".join(str(x) for x in (r.get("qe_Date"), r.get("consolidated"), r.get("broadcast_Date"),
                                                   r.get("xbrl"))))
        elif cmd == "annual_reports":
            out.append(f"{r.get('fromYr')} - " + " | ".join(str(x) for x in (
                r.get("toYr"), r.get("submitted"), r.get("submission_type"), r.get("attFileSize"), r.get("fileName"))))
        elif cmd in ("announcements", "transcripts"):
            out.append(" | ".join(str(x) for x in (r.get("an_dt"), r.get("symbol"), r.get("desc"),
                                                   (r.get("attchmntText") or "")[:90], r.get("attchmntFile"))))
        else:
            out.append(json.dumps(r, ensure_ascii=False)[:220])
    if len(shown) < len(rows):
        out.append(f"showing {len(shown)} of {len(rows)} rows (--limit 0 for all, --out FILE for the full JSON)")
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=sorted(COMMANDS))
    p.add_argument("symbol", nargs="?")
    p.add_argument("--from", dest="frm")
    p.add_argument("--to")
    p.add_argument("--out")
    p.add_argument("--raw", action="store_true")
    p.add_argument("--download", metavar="DIR", help="transcripts / annual_reports: save files here")
    p.add_argument("--limit", type=int, default=0,
                   help="summary mode: print at most N rows (default 0 = all; a cut list says 'showing N of M')")
    a = p.parse_args()
    data = COMMANDS[a.cmd](a)
    if a.out:
        with open(a.out, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    rows = data.get("data", data) if isinstance(data, dict) else data
    if a.raw:
        print(json.dumps(data, ensure_ascii=False, indent=1))
    else:
        print("\n".join(summary_lines(a.cmd, rows, a.limit)))
    if a.cmd in ("transcripts", "annual_reports") and a.download:
        os.makedirs(a.download, exist_ok=True)
        for r in rows:
            url = r.get("attchmntFile") or r.get("fileName")
            if not url:
                continue
            fn = os.path.join(a.download, os.path.basename(urllib.parse.urlparse(url).path))
            if not os.path.exists(fn):
                with open(fn, "wb") as f:
                    f.write(_get(url, binary=True))
                print("saved", fn)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # keep CLI output readable
        sys.exit(f"error: {e}")
