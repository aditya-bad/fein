#!/usr/bin/env python3
"""Polite BSE India API fetcher (standard library + the system `curl` binary).

Tested 2026-11-19: api.bseindia.com only answers over HTTP/2 with browser
Sec-Fetch-* headers; HTTP/1.1 (Python urllib) gets Akamai 403. So this script
shells out to `curl --http2` (no third-party Python packages).

Usage (scrip code = BSE numeric code, e.g. 532400):
  python3 tools/bse_fetch.py announcements 532400 --from 20261101 --to 20261119
  python3 tools/bse_fetch.py announcements --from 20261119 --to 20261119   # all scrips (one window per day)
  python3 tools/bse_fetch.py transcripts 532400 --from 20250101 --to 20261119 [--download DIR]
  python3 tools/bse_fetch.py header 532400        # PE, ROE, ISIN, industry
  python3 tools/bse_fetch.py price 532400
  python3 tools/bse_fetch.py results 532400       # last quarters snapshot
  python3 tools/bse_fetch.py shareholding 532400  # SHP filings list + XBRL names
  python3 tools/bse_fetch.py actions 532400       # dividends/splits
  python3 tools/bse_fetch.py calendar             # upcoming result board meetings
  python3 tools/bse_fetch.py selftest [--live]   # offline windowing/pagination checks (+1 real call)
Dates are YYYYMMDD; any range length (split into <=1-year windows, 50 rows/page; a >1-year window is HTTP 400).
>=1.5 s between requests; back-off on 403.
Attachments: https://www.bseindia.com/xml-data/corpfiling/AttachLive/<ATTACHMENTNAME>
(older ones under AttachHis/). PDFs are untrusted data; use pdftotext.
"""
import argparse, datetime, json, os, subprocess, sys, time, urllib.parse

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
        if code == "400":
            raise HTTPError400(f"HTTP 400 for {url}")
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


class HTTPError400(RuntimeError):
    pass


def _ymd(d):
    return d.strftime("%Y%m%d")


def _date(s):
    return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:8]))


def _minus_year(d):
    try:
        return d.replace(year=d.year - 1)
    except ValueError:          # 29-Feb
        return d.replace(year=d.year - 1, day=28)


def windows(frm, to, scrip=True):
    """Split [frm, to] (YYYYMMDD) into windows the API accepts (tested 2026-11-25):
    - with a scrip code, strPrevDate must be >= strToDate minus one calendar year, else HTTP 400 on every page
      (20251125-20261125 OK, 20251124-20261125 400; 20231231-20241231 OK);
    - without a scrip code, a multi-day range silently returns no rows (Table1 null), so one window per day.
    Returned newest first (the API sorts newest first)."""
    a, b = _date(frm), _date(to)
    out = []
    while b >= a:
        lo = max(a, _minus_year(b) + datetime.timedelta(days=1)) if scrip else b
        out.append((_ymd(lo), _ymd(b)))
        b = lo - datetime.timedelta(days=1)
    return out


def _pages(scrip, frm, to, max_pages, fetch):
    rows, page = [], 1
    while page <= max_pages:
        d = fetch(scrip, frm, to, page)
        t = d.get("Table") or []
        rows += t
        total = (d.get("Table1") or [{}])[0].get("ROWCNT", 0)
        if not t or len(rows) >= total:
            break
        page += 1
    return rows


def all_announcements(scrip, frm, to, max_pages=200, fetch=None):
    """Every announcement in [frm, to], any range length: windows (see `windows`) x pages (50 rows/page).
    A window that still gets HTTP 400 is halved until it is one day. Rows de-duplicated by NEWSID."""
    fetch = fetch or announcements
    rows, seen = [], set()
    todo = windows(frm, to, bool(scrip))
    while todo:
        lo, hi = todo.pop(0)
        try:
            got = _pages(scrip, lo, hi, max_pages, fetch)
        except HTTPError400:
            a, b = _date(lo), _date(hi)
            if a >= b:
                raise
            mid = a + (b - a) // 2
            todo[:0] = [(_ymd(mid + datetime.timedelta(days=1)), hi), (lo, _ymd(mid))]
            continue
        for r in got:
            k = r.get("NEWSID") or (r.get("NEWS_DT"), r.get("SCRIP_CD"), r.get("NEWSSUB"), r.get("ATTACHMENTNAME"))
            if k not in seen:
                seen.add(k)
                rows.append(r)
    return rows


def selftest(live=False):
    """Offline checks of windowing/pagination with a fake API (mimics the 400 rule); --live adds one real call."""
    assert windows("20251125", "20261125") == [("20251126", "20261125"), ("20251125", "20251125")]
    w = windows("20230701", "20261125")
    assert w[0] == ("20251126", "20261125") and w[-1][0] == "20230701" and len(w) == 4, w
    assert all(_date(lo) > _minus_year(_date(hi)) for lo, hi in w)
    assert windows("20261118", "20261119", scrip=False) == [("20261119", "20261119"), ("20261118", "20261118")]
    n_by_day = {}
    day = _date("20230701")
    while day <= _date("20261125"):
        n_by_day[_ymd(day)] = 1 if day.day % 3 == 0 else 0   # ~120 rows a year, 3 pages a window
        day += datetime.timedelta(days=1)
    calls = []

    def fake(scrip, frm, to, page, page_size=50):
        calls.append((frm, to, page))
        if _date(frm) < _minus_year(_date(to)):
            raise HTTPError400("HTTP 400 (window > 1 year)")
        ids = [f"{k}-{scrip}" for k, v in sorted(n_by_day.items(), reverse=True) if frm <= k <= to and v]
        return {"Table": [{"NEWSID": i} for i in ids[(page - 1) * page_size:page * page_size]],
                "Table1": [{"ROWCNT": len(ids)}]}
    got = all_announcements("543942", "20230701", "20261125", fetch=fake)
    assert len(got) == sum(n_by_day.values()) == len({r["NEWSID"] for r in got}), len(got)
    assert max(p for _, _, p in calls) >= 2                     # pagination exercised (>50 rows per window)
    calls.clear()                                               # a window the API still rejects gets halved
    got2 = all_announcements("543942", "20250101", "20261125",
                             fetch=lambda s, f, t, p: (_ for _ in ()).throw(HTTPError400("x"))
                             if (_date(t) - _date(f)).days > 100 else fake(s, f, t, p))
    assert len(got2) == sum(v for k, v in n_by_day.items() if "20250101" <= k <= "20261125"), len(got2)
    print("selftest offline: OK")
    if live:
        rows = all_announcements("543942", "20251101", "20261125")
        print(f"selftest live: UTKARSHBNK 20251101-20261125 -> {len(rows)} rows (one call >1y would be HTTP 400)")
        assert len(rows) > 50, "pagination returned <= 1 page"


def attachment_url(name, live=True):
    return f"https://www.bseindia.com/xml-data/corpfiling/{'AttachLive' if live else 'AttachHis'}/{name}"


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("cmd", choices=["announcements", "transcripts", "header", "price", "results",
                                   "shareholding", "actions", "calendar", "selftest"])
    p.add_argument("--live", action="store_true", help="selftest: also make one real paginated call")
    p.add_argument("scrip", nargs="?", default="")
    p.add_argument("--from", dest="frm", default=time.strftime("%Y%m%d"))
    p.add_argument("--to", default=time.strftime("%Y%m%d"))
    p.add_argument("--out")
    p.add_argument("--download", metavar="DIR")
    a = p.parse_args()
    s = a.scrip
    if a.cmd == "selftest":
        return selftest(a.live)
    if a.cmd == "announcements":
        data = all_announcements(s, a.frm, a.to)
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
