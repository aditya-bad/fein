#!/usr/bin/env python3
"""Cached industry map for the PEAD live universe (roadmap stage 1: universe; unlocks sector frames, L40).

    python3 tools/universe/industry_map.py                 # build / resume
    python3 tools/universe/industry_map.py --retry-misses  # also re-try symbols that missed last time
    python3 tools/universe/industry_map.py --limit 20      # first 20 pending symbols only (smoke run)
    python3 tools/universe/industry_map.py --selftest      # offline parser/resume tests, no network

Input : research_notes/Backtests/india_pead_live/universe.csv (column `sym`)
Output: research_notes/Backtests/india_pead_live/industry_map.csv
        symbol, industry, sector, source, as_of  (+ macro, basic_industry, isin, bse_code for convenience)

All three sources use the same NSE/BSE 4-level classification (macro > sector > industry > basic industry):
  1. nse   : www.nseindia.in/api/quote-equity industryInfo {macro, sector, industry, basicIndustry}.
             Bot-protected (Akamai 403, tested 2026-11-19 and 2026-11-24). One probe per run; if it is refused
             the run stops asking NSE (no hammering) and falls through to BSE.
  2. bse   : api.bseindia.com ComHeadernew (Sector = macro, IndustryNew = sector, IGroup = industry,
             ISubGroup = basic industry). NSE symbol -> BSE code via the BSE scrip list (ISIN from NSE EQUITY_L.csv,
             then BSE scrip_id). Goes through tools/detectors/fein_common.bse_api (curl --http2).
  3. screener : screener.in/company/<SYM>/ breadcrumb (title="Broad Sector" / "Sector" / "Broad Industry" /
             "Industry"). Last resort.
Rows with no hit are written with source "miss" so coverage is visible; --retry-misses tries them again.

Resume: the output CSV is the state. It is rewritten (atomically) every 25 symbols, and symbols already mapped are
skipped. Requests are >= 1.5 s apart per host (fein_common pacing for BSE, own pacing for NSE/screener).
Research data, not SEBI-registered advice.
"""
import argparse
import csv
import datetime as dt
import gzip
import html
import io
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
LIVE = os.path.join(ROOT, "research_notes", "Backtests", "india_pead_live")
UNIVERSE = os.path.join(LIVE, "universe.csv")
OUT = os.path.join(LIVE, "industry_map.csv")
FIELDS = ["symbol", "industry", "sector", "source", "as_of", "macro", "basic_industry", "isin", "bse_code"]
SAVE_EVERY = 25
MIN_GAP = 1.5
UA = "Mozilla/5.0"
NSE_QUOTE = "https://www.nseindia.in/api/quote-equity?symbol="
NSE_HDRS = {"User-Agent": UA, "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip", "Referer": "https://www.nseindia.in/"}
EQUITY_L = "https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv"
SCREENER = "https://www.screener.in/company/%s/"
_last = {}


def _log(*a):
    print(*a, flush=True)


def _pace(host):
    wait = MIN_GAP - (time.time() - _last.get(host, 0.0))
    if wait > 0:
        time.sleep(wait)
    _last[host] = time.time()


def _get(url, host, headers=None, tries=3):
    """urllib GET with pacing; returns text. 403/429/503 back off; a 403 on the last try raises HTTPError."""
    for i in range(tries):
        _pace(host)
        req = urllib.request.Request(url, headers=headers or {"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                body = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
                return body.decode("utf-8-sig", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code in (403, 429, 503) and i < tries - 1:
                time.sleep(5 * 2 ** i)
                continue
            raise
        except (urllib.error.URLError, TimeoutError, OSError):
            if i < tries - 1:
                time.sleep(5 * 2 ** i)
                continue
            raise
    return None


# ----------------------------------------------------------------------------- parsers (pure, self-tested)

def _clean(x):
    x = html.unescape((x or "").strip())
    return "" if x in ("-", "NA", "N.A.", "null", "None") else x


def parse_nse_quote(js):
    """quote-equity JSON -> dict(macro, sector, industry, basic_industry, isin) or None."""
    if not isinstance(js, dict):
        return None
    ii = js.get("industryInfo") or {}
    out = {"macro": _clean(ii.get("macro")), "sector": _clean(ii.get("sector")),
           "industry": _clean(ii.get("industry")), "basic_industry": _clean(ii.get("basicIndustry")),
           "isin": _clean((js.get("info") or {}).get("isin"))}
    return out if (out["industry"] or out["basic_industry"]) else None


def parse_bse_header(js):
    """BSE ComHeadernew JSON -> dict or None. Old scrips only have `Industry` (= basic industry)."""
    if not isinstance(js, dict):
        return None
    out = {"macro": _clean(js.get("Sector")), "sector": _clean(js.get("IndustryNew")),
           "industry": _clean(js.get("IGroup")), "basic_industry": _clean(js.get("ISubGroup") or js.get("Industry")),
           "isin": _clean(js.get("ISIN"))}
    if not out["industry"] and out["basic_industry"]:
        out["industry"] = out["basic_industry"]
    return out if out["industry"] else None


_SCR = {k: re.compile(r'title="%s">([^<]+)</a>' % t) for k, t in
        (("macro", "Broad Sector"), ("sector", "Sector"), ("industry", "Broad Industry"),
         ("basic_industry", "Industry"))}


def parse_screener(page):
    if not page:
        return None
    out = {k: (_clean(rx.search(page).group(1)) if rx.search(page) else "") for k, rx in _SCR.items()}
    out["isin"] = ""
    return out if out["industry"] else None


def read_existing(path):
    if not os.path.exists(path):
        return {}
    with open(path, newline="") as f:
        return {r["symbol"]: r for r in csv.DictReader(f)}


def pending(symbols, existing, retry_misses):
    return [s for s in symbols if s not in existing or (retry_misses and existing[s].get("source") == "miss")]


def write_rows(path, rows):
    """Atomic rewrite, rows sorted by symbol."""
    d = os.path.dirname(path) or "."
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for k in sorted(rows):
            w.writerow({x: rows[k].get(x, "") for x in FIELDS})
    os.replace(tmp, path)


def coverage(rows, symbols):
    hit = [s for s in symbols if s in rows and rows[s].get("source") not in ("miss", "", None)]
    by = {}
    for s in hit:
        by[rows[s]["source"]] = by.get(rows[s]["source"], 0) + 1
    return len(hit), len(symbols), by


# ----------------------------------------------------------------------------- sources

class Sources:
    def __init__(self, log=_log):
        self.log = log
        self.nse_ok = None          # None = not probed, False = blocked this run
        self.bse_codes = None       # NSE symbol -> BSE code
        self.isin_by_sym = {}
        self.bse_ok = True
        self.scr_ok = True

    def nse(self, sym):
        if self.nse_ok is False:
            return None
        try:
            txt = _get(NSE_QUOTE + urllib.request.quote(sym), "nse", NSE_HDRS, tries=1 if self.nse_ok is None else 2)
            js = json.loads(txt) if txt and not txt.lstrip().startswith("<") else None
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError, OSError) as e:
            if self.nse_ok is None:
                self.log(f"NSE quote-equity refused ({e}); not asking NSE again this run (bot-protected), using BSE")
                self.nse_ok = False
            return None
        self.nse_ok = True
        return parse_nse_quote(js)

    def _load_bse_codes(self):
        sys.path.insert(0, os.path.join(ROOT, "tools", "detectors"))
        import fein_common as F
        self._F = F
        self.bse_codes, by_isin = {}, {}
        for status in ("Active", "Suspended", "Delisted"):
            try:
                rows, _ = F.bse_api("ListofScripData/w", Group="", Scripcode="", industry="", segment="Equity",
                                    status=status)
            except Exception as e:  # one list failing is not fatal
                self.log(f"BSE scrip list ({status}) failed: {e}")
                continue
            for r in rows or []:
                code, sid, isin = r.get("SCRIP_CD"), (r.get("scrip_id") or "").upper(), r.get("ISIN_NUMBER") or ""
                if sid and sid not in self.bse_codes:
                    self.bse_codes[sid] = code
                if isin and isin not in by_isin:
                    by_isin[isin] = code
        try:
            txt = _get(EQUITY_L, "nsearch", {"User-Agent": UA})
            for r in csv.DictReader(io.StringIO(txt or "")):
                r = {k.strip(): (v or "").strip() for k, v in r.items() if k}
                self.isin_by_sym[r.get("SYMBOL", "").upper()] = r.get("ISIN NUMBER", "")
        except Exception as e:
            self.log(f"NSE EQUITY_L.csv failed ({e}); BSE mapping by scrip_id only")
        self.by_isin = by_isin
        self.log(f"BSE scrip list: {len(self.bse_codes)} scrip_ids, {len(by_isin)} ISINs; NSE ISINs {len(self.isin_by_sym)}")

    def bse(self, sym):
        if not self.bse_ok:
            return None, ""
        if self.bse_codes is None:
            self._load_bse_codes()
        # ISIN first (a delisted BSE scrip_id can equal an unrelated live NSE symbol), then scrip_id
        code = self.by_isin.get(self.isin_by_sym.get(sym, ""), "") or self.bse_codes.get(sym, "")
        if not code:
            return None, ""
        try:
            js, _ = self._F.bse_api("ComHeadernew/w", tries=2, quotetype="EQ", scripcode=code, seriesid="")
        except Exception as e:
            self.log(f"  BSE header {sym}/{code} failed: {e}")
            return None, code
        return parse_bse_header(js), code

    def screener(self, sym):
        if not self.scr_ok:
            return None
        try:
            page = _get(SCREENER % urllib.request.quote(sym), "screener", {"User-Agent": UA}, tries=2)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                self.log(f"screener refused ({e.code}); not asking screener again this run")
                self.scr_ok = False
            return None
        except Exception:
            return None
        return parse_screener(page)


def map_symbol(sym, src, today):
    row = {"symbol": sym, "as_of": today, "isin": src.isin_by_sym.get(sym, ""), "bse_code": ""}
    hit = src.nse(sym)
    source = "nse_quote_equity" if hit else ""
    if not hit:
        hit, code = src.bse(sym)
        row["bse_code"] = code
        source = "bse_comheader" if hit else ""
    if not hit:
        hit = src.screener(sym)
        source = "screener" if hit else ""
    if hit:
        row.update({k: v for k, v in hit.items() if v or k != "isin"})
        row["source"] = source
    else:
        row.update({"industry": "", "sector": "", "macro": "", "basic_industry": "", "source": "miss"})
    return row


def build(universe=UNIVERSE, out=OUT, retry_misses=False, limit=None, src=None, log=_log, today=None):
    with open(universe, newline="") as f:
        symbols = [r["sym"].strip().upper() for r in csv.DictReader(f) if r.get("sym", "").strip()]
    rows = read_existing(out)
    todo = pending(symbols, rows, retry_misses)
    if limit:
        todo = todo[:limit]
    log(f"universe {len(symbols)} symbols; {len(rows)} already in map; {len(todo)} to fetch")
    src = src or Sources(log)
    today = today or dt.date.today().isoformat()
    for i, s in enumerate(todo, 1):
        rows[s] = map_symbol(s, src, today)
        if i % SAVE_EVERY == 0 or i == len(todo):
            write_rows(out, rows)
            n, tot, by = coverage(rows, symbols)
            log(f"  {i}/{len(todo)} done; coverage {n}/{tot} = {100 * n / tot:.1f}% {by}")
    if not todo:
        write_rows(out, rows) if rows else None
    n, tot, by = coverage(rows, symbols)
    log(f"coverage: {n}/{tot} = {100 * n / max(tot, 1):.1f}% by source {by}; misses {tot - n} -> {out}")
    return n, tot, by


# ----------------------------------------------------------------------------- self-test (offline)

def selftest():
    nse_js = {"info": {"isin": "INE117A01022"}, "industryInfo": {"macro": "Industrials", "sector": "Capital Goods",
                                                                  "industry": "Electrical Equipment",
                                                                  "basicIndustry": "Heavy Electrical Equipment"}}
    a = parse_nse_quote(nse_js)
    assert a["industry"] == "Electrical Equipment" and a["sector"] == "Capital Goods", a
    assert parse_nse_quote({"industryInfo": {}}) is None and parse_nse_quote("x") is None
    b = parse_bse_header({"Sector": "Industrials", "IndustryNew": "Capital Goods", "IGroup": "Electrical Equipment",
                          "ISubGroup": "Heavy Electrical Equipment", "ISIN": "INE117A01022"})
    assert b["industry"] == "Electrical Equipment" and b["macro"] == "Industrials", b
    old = parse_bse_header({"Industry": "Textiles", "IGroup": "", "ISubGroup": ""})
    assert old["industry"] == "Textiles", old
    assert parse_bse_header({"Industry": "-"}) is None
    page = ('<a href="/market/IN03/" title="Broad Sector">Industrials</a> <a title="Sector">Capital Goods</a>'
            '<a title="Broad Industry">Electrical Equipment</a><a title="Industry">Heavy Electrical &amp; Co</a>')
    c = parse_screener(page)
    assert c["industry"] == "Electrical Equipment" and c["basic_industry"] == "Heavy Electrical & Co", c
    assert parse_screener("<html></html>") is None

    class Fake:
        isin_by_sym = {}
        calls = []

        def nse(self, s):
            self.calls.append(("nse", s))
            return None

        def bse(self, s):
            self.calls.append(("bse", s))
            return (dict(b) if s == "AAA" else None), ("500002" if s == "AAA" else "")

        def screener(self, s):
            self.calls.append(("scr", s))
            return dict(c) if s == "BBB" else None

    with tempfile.TemporaryDirectory() as d:
        uni, out = os.path.join(d, "u.csv"), os.path.join(d, "m.csv")
        with open(uni, "w") as f:
            f.write("sym,shares\nAAA,1\nBBB,2\nCCC,3\n")
        q = lambda *_: None  # noqa: E731
        n, tot, by = build(uni, out, src=Fake(), log=q, today="2026-11-24")
        assert (n, tot) == (2, 3) and by == {"bse_comheader": 1, "screener": 1}, (n, tot, by)
        rows = read_existing(out)
        assert rows["AAA"]["source"] == "bse_comheader" and rows["AAA"]["bse_code"] == "500002"
        assert rows["CCC"]["source"] == "miss" and rows["BBB"]["sector"] == "Capital Goods"
        assert list(csv.reader(open(out)))[0][:5] == ["symbol", "industry", "sector", "source", "as_of"]
        f2 = Fake(); f2.calls = []
        build(uni, out, src=f2, log=q)                     # resume: nothing to do
        assert f2.calls == [], f2.calls
        f3 = Fake(); f3.calls = []
        build(uni, out, src=f3, log=q, retry_misses=True)  # only the miss is retried
        assert {s for _, s in f3.calls} == {"CCC"}, f3.calls
    print("selftest: OK (parsers, fallback order, coverage, resume, retry-misses)")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--universe", default=UNIVERSE)
    p.add_argument("--out", default=OUT)
    p.add_argument("--retry-misses", action="store_true")
    p.add_argument("--limit", type=int)
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args(argv)
    if a.selftest:
        return selftest()
    build(a.universe, a.out, a.retry_misses, a.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
