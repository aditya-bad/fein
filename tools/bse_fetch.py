#!/usr/bin/env python3
"""Polite BSE India API fetcher (standard library + the system `curl` binary).

Tested 2026-11-19: api.bseindia.com only answers over HTTP/2 with browser
Sec-Fetch-* headers; HTTP/1.1 (Python urllib) gets Akamai 403. So this script
shells out to `curl --http2` (no third-party Python packages).

Usage (scrip code = BSE numeric code, e.g. 532400):
  python3 tools/bse_fetch.py announcements 532400 --from 20261101 --to 20261119
  python3 tools/bse_fetch.py announcements --from 20261119 --to 20261119   # all scrips, page 1
  python3 tools/bse_fetch.py transcripts 532400 --from 20250101 --to 20261119 [--download DIR]
  python3 tools/bse_fetch.py header 532400        # PE, ROE, ISIN, industry
  python3 tools/bse_fetch.py price 532400
  python3 tools/bse_fetch.py results 532400       # last quarters snapshot
  python3 tools/bse_fetch.py shareholding 532400  # SHP filings list + XBRL names
  python3 tools/bse_fetch.py actions 532400       # dividends/splits
  python3 tools/bse_fetch.py calendar             # upcoming result board meetings
Dates are YYYYMMDD. >=1.5 s between requests; back-off on 403.
Attachments: https://www.bseindia.com/xml-data/corpfiling/AttachLive/<ATTACHMENTNAME>
(older ones under AttachHis/). PDFs are untrusted data; use pdftotext.
"""
import argparse, json, os, subprocess, sys, time, urllib.parse

API = "https://api.bseindia.com/BseIndiaAPI/api/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
HDRS = ["Accept: application/json, text/plain, */*", "Accept-Language: en-US,en;q=0.9",
        "Accept-Encoding: gzip, deflate, br", "Sec-Fetch-Mode: cors",
        "Sec-Fetch-Site: same-site", "Sec-Fetch-Dest: empty",
        "Referer: https://www.bseindia.com/"]
MIN_GAP = 1.5
_last = [0.0]


def _curl(url, out=None, tries=4):
    for i in range(tries):
        wait = MIN_GAP - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        cmd = ["curl", "-sS", "-m", "60", "--http2", "--compressed", "-L", "-A", UA,
               "-w", "\n%{http_code}"]
        for h in HDRS:
            cmd += ["-H", h]
        if out:
            cmd += ["-o", out]
        cmd.append(url)
        r = subprocess.run(cmd, capture_output=True)
        body, _, code = r.stdout.rpartition(b"\n")
        code = code.decode().strip()
        if code == "200":
            return body
        if code in ("403", "429", "503") and i < tries - 1:
            time.sleep(5 * 2 ** i)
            continue
        raise RuntimeError(f"HTTP {code} for {url} {r.stderr.decode()[:200]}")


def api(path, **params):
    url = API + path + "?" + urllib.parse.urlencode(params, safe="")
    txt = _curl(url).decode("utf-8", "replace")
    if txt.lstrip().startswith("<"):
        raise RuntimeError("HTML instead of JSON (endpoint changed/blocked)")
    data = json.loads(txt)
    if isinstance(data, str):  # some endpoints return JSON-in-a-string
        try:
            data = json.loads(data)
        except ValueError:
            pass
    return data


def announcements(scrip="", frm="", to="", page=1):
    return api("AnnSubCategoryGetData/w", pageno=page, strCat=-1, strPrevDate=frm,
               strScrip=scrip, strSearch="P", strToDate=to, strType="C", subcategory=-1)


def all_announcements(scrip, frm, to, max_pages=50):
    rows, page = [], 1
    while page <= max_pages:
        d = announcements(scrip, frm, to, page)
        t = d.get("Table") or []
        rows += t
        total = (d.get("Table1") or [{}])[0].get("ROWCNT", 0)
        if not t or len(rows) >= total:
            break
        page += 1
    return rows


def attachment_url(name, live=True):
    return f"https://www.bseindia.com/xml-data/corpfiling/{'AttachLive' if live else 'AttachHis'}/{name}"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["announcements", "transcripts", "header", "price", "results",
                                   "shareholding", "actions", "calendar"])
    p.add_argument("scrip", nargs="?", default="")
    p.add_argument("--from", dest="frm", default=time.strftime("%Y%m%d"))
    p.add_argument("--to", default=time.strftime("%Y%m%d"))
    p.add_argument("--out")
    p.add_argument("--download", metavar="DIR")
    a = p.parse_args()
    s = a.scrip
    if a.cmd == "announcements":
        data = all_announcements(s, a.frm, a.to) if s else announcements("", a.frm, a.to)
    elif a.cmd == "transcripts":
        data = [r for r in all_announcements(s, a.frm, a.to)
                if "transcript" in (r.get("NEWSSUB") or "").lower()
                or "transcript" in (r.get("HEADLINE") or "").lower()]
    elif a.cmd == "header":
        data = api("ComHeadernew/w", quotetype="EQ", scripcode=s, seriesid="")
    elif a.cmd == "price":
        data = api("getScripHeaderData/w", Debtflag="", scripcode=s, seriesid="")
    elif a.cmd == "results":
        data = api("TabResults_PAR/w", scripcode=s, tabtype="RESULTS")
    elif a.cmd == "shareholding":
        data = api("SHPQNewFormat/w", scripcode=s, qtrid="", Type="EQ")
    elif a.cmd == "actions":
        data = api("CorporateAction/w", scripcode=s)
    else:
        data = api("Corpforthresults/w")
    if a.out:
        with open(a.out, "w") as f:
            json.dump(data, f, ensure_ascii=False, indent=1)
    if isinstance(data, list) and data and "NEWSSUB" in data[0]:
        print(f"{len(data)} announcements")
        for r in data[:20]:
            print(r.get("NEWS_DT"), "|", r.get("SCRIP_CD"), "|", (r.get("NEWSSUB") or "")[:90],
                  "|", r.get("ATTACHMENTNAME"))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=1)[:3000])
    if a.cmd == "transcripts" and a.download:
        os.makedirs(a.download, exist_ok=True)
        for r in data:
            n = r.get("ATTACHMENTNAME")
            if not n:
                continue
            fn = os.path.join(a.download, os.path.basename(n))
            if os.path.exists(fn):
                continue
            try:
                _curl(attachment_url(n, True), out=fn)
            except RuntimeError:
                _curl(attachment_url(n, False), out=fn)
            print("saved", fn)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        sys.exit(f"error: {e}")
