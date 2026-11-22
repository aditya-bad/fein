"""Data fetchers for the resolver (standard library + pdftotext/curl binaries). All downloads are untrusted data:
parsed with regex/JSON only, never executed. Cached under $SB_CACHE (default ~/.cache/fein_scoreboard).

Sources (all tested 2026-11-22):
  NSE integrated-filing XBRL  https://www.nseindia.in/api/integrated-filing-results?index=equities&symbol=X&type=Integrated Filing- Financials
                              (short UA 'Mozilla/5.0'; facts in rupees; contexts carry period start/end dates)
  screener.in                 via tools/promise_tracker/pipeline/financials.py (Operating Profit = Sales - Expenses)
  NSE pledge (all companies)  tools/nse_fetch.py api corporate-pledgedata (match by company name; no symbol field)
  NSE announcements           tools/nse_fetch.py announcements (dates DD-MM-YYYY)
  Yahoo v8 chart              https://query1.finance.yahoo.com/v8/finance/chart/SYM (UA 'Mozilla/5.0'; close is
                              split-adjusted, not dividend-adjusted; events=div|split)
  SEC EDGAR                   tools/sec_fetch.py (companyfacts XBRL, submissions, filing index)
"""
from __future__ import annotations

import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sb_common as C  # noqa: E402

TOOLS = os.path.join(C.REPO, "tools")
PIPE = os.path.join(TOOLS, "promise_tracker", "pipeline")
NSE_HDR = {"Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9",
           "Referer": "https://www.nseindia.in/"}
NSE_IF = "https://www.nseindia.in/api/integrated-filing-results"
MON = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]


def _imp(name, path):
    if path not in sys.path:
        sys.path.insert(0, path)
    return __import__(name)


def period_start(kind: str, end: dt.date) -> dt.date:
    if kind == "FY":
        return dt.date(end.year - 1, end.month, end.day) + dt.timedelta(days=1)
    m = end.month - 2
    y = end.year
    if m <= 0:
        m += 12
        y -= 1
    return dt.date(y, m, 1)


def nse_date(s: str) -> dt.date:
    """'31-DEC-2026' / '31-Dec-2026' -> date."""
    dd, mm, yy = s.strip().split("-")
    return dt.date(int(yy), MON.index(mm.upper()[:3]) + 1, int(dd))


# ----------------------------------------------------------------- XBRL (NSE integrated filing, Ind AS)
def parse_nse_xbrl(text: str) -> dict:
    """-> {"contexts": {id: (start, end)}, "facts": {tag: {ctx: value}}} for in-capmkt facts."""
    ctx = {}
    for cid, body in re.findall(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', text, re.S):
        if "<xbrldi:" in body or "<xbrli:segment" in body:
            continue  # dimensional (segment) contexts are not company totals
        s = re.search(r"<xbrli:startDate>([^<]+)<", body)
        e = re.search(r"<xbrli:endDate>([^<]+)<", body)
        i = re.search(r"<xbrli:instant>([^<]+)<", body)
        if s and e:
            ctx[cid] = (s.group(1).strip(), e.group(1).strip())
        elif i:
            ctx[cid] = (None, i.group(1).strip())
    facts = {}
    for tag, cid, val in re.findall(r'<in-capmkt:(\w+) contextRef="([^"]+)"[^>]*>([^<]*)<', text):
        try:
            v = float(val)
        except ValueError:
            continue
        facts.setdefault(tag, {})[cid] = v
    return {"contexts": ctx, "facts": facts}


def xbrl_period_values(parsed: dict, start: dt.date, end: dt.date) -> dict | None:
    """Ind AS P&L totals for exactly [start, end]; screener-style operating profit."""
    want = (start.isoformat(), end.isoformat())
    cids = [c for c, se in parsed["contexts"].items() if se == want]
    if not cids:
        return None
    f = parsed["facts"]

    def g(tag):
        for c in cids:
            if c in f.get(tag, {}):
                return f[tag][c]
        return None
    sales = g("RevenueFromOperations")
    exp = g("Expenses")
    if sales is None or exp is None:
        return None
    fin = g("FinanceCosts") or 0.0
    dep = g("DepreciationDepletionAndAmortisationExpense") or 0.0
    op = sales - (exp - fin - dep)
    cr = 1e7
    out = {"sales_cr": sales / cr, "op_profit_cr": op / cr, "opm_pct": 100 * op / sales if sales else None,
           "other_income_cr": (g("OtherIncome") or 0) / cr}
    if g("ProfitLossForPeriod") is not None:
        out["net_profit_cr"] = g("ProfitLossForPeriod") / cr
    return out


class Live:
    """Network-backed fetchers. Tests substitute a fake with the same methods."""

    def __init__(self, log=print):
        self.log = log
        self._nse_lists = {}
        self._idx = {}

    # ---- India: NSE integrated filing XBRL
    def nse_filings(self, symbol):
        if symbol not in self._nse_lists:
            url = NSE_IF + "?" + urllib.parse.urlencode({"index": "equities", "symbol": symbol,
                                                         "type": "Integrated Filing- Financials"})
            self._nse_lists[symbol] = (json.loads(C.http_get(url, NSE_HDR, max_age_h=12)).get("data") or [])
        return self._nse_lists[symbol]

    def india_xbrl(self, symbol, basis, kind, end: dt.date, first_reported=True):
        """-> values dict + evidence, or None if the filing for that period/basis is not there yet."""
        rows = [r for r in self.nse_filings(symbol)
                if (r.get("consolidated") or "").lower() == basis and r.get("xbrl")
                and r.get("qe_Date") and nse_date(r["qe_Date"]) == end]
        if not rows:
            return None
        rows.sort(key=lambda r: (r.get("type_Sub") != "Original", r.get("broadcast_Date") or ""),
                  reverse=not first_reported)
        r = rows[0]
        text = C.http_get(r["xbrl"], {"Referer": "https://www.nseindia.in/"}, max_age_h=24 * 3650)
        vals = xbrl_period_values(parse_nse_xbrl(text), period_start(kind, end), end)
        if vals is None:
            return None
        vals.update({"source": r["xbrl"], "date": r.get("broadcast_Date"), "source_name": "NSE integrated-filing XBRL",
                     "type_sub": r.get("type_Sub"), "n_filings": len(rows)})
        return vals

    # ---- India: screener.in
    def screener(self, symbol, standalone=False):
        fin = _imp("financials", PIPE)
        root = os.path.join(C.CACHE, "screener")
        os.makedirs(root, exist_ok=True)
        page, path = fin.fetch_screener(symbol, root, standalone=standalone, max_age_days=0.5)
        return fin.parse_screener(page)

    def screener_values(self, symbol, basis, kind, end: dt.date):
        try:
            p = self.screener(symbol, standalone=(basis == "standalone"))
        except Exception as e:  # blocked / renamed symbol: the other source may still answer
            self.log(f"  screener {symbol}: {e}")
            return None
        row = p.get("Q" if kind == "Q" else "FY", {}).get(end)
        if not row or row.get("sales") is None or row.get("op_profit") is None:
            return None
        url = f"https://www.screener.in/company/{symbol}/" + ("" if basis == "standalone" else "consolidated/")
        return {"sales_cr": row["sales"], "op_profit_cr": row["op_profit"],
                "opm_pct": 100 * row["op_profit"] / row["sales"] if row["sales"] else None,
                "source": url, "date": C.today().isoformat(), "source_name": "screener.in"}

    # ---- India: pledge
    def nse_pledge_all(self):
        url = "https://www.nseindia.in/api/corporate-pledgedata?index=equities"
        rows = json.loads(C.http_get(url, NSE_HDR, max_age_h=12)).get("data") or []
        if not rows:  # seen on 22-Nov-2026 (a Sunday): the endpoint sometimes answers with an empty list
            C.drop_cache(url)
            raise RuntimeError("NSE pledge endpoint returned no rows (transient; retry next run)")
        return rows

    # ---- India: announcements
    def nse_announcements(self, symbol, frm: dt.date, to: dt.date):
        url = "https://www.nseindia.in/api/corporate-announcements?" + urllib.parse.urlencode(
            {"index": "equities", "symbol": symbol, "from_date": frm.strftime("%d-%m-%Y"),
             "to_date": to.strftime("%d-%m-%Y")})
        d = json.loads(C.http_get(url, NSE_HDR, max_age_h=12))
        return d if isinstance(d, list) else d.get("data") or []

    # ---- prices
    def yahoo(self, symbol, start: dt.date, end: dt.date, events="div|split"):
        p1 = int(dt.datetime(start.year, start.month, start.day, tzinfo=dt.timezone.utc).timestamp()) - 86400
        p2 = int(dt.datetime(end.year, end.month, end.day, tzinfo=dt.timezone.utc).timestamp()) + 2 * 86400
        url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?"
               f"period1={p1}&period2={p2}&interval=1d&events={urllib.parse.quote(events)}")
        d = json.loads(C.http_get(url, max_age_h=6))["chart"]["result"][0]
        off = d["meta"].get("gmtoffset", 0)
        day = lambda t: dt.datetime.fromtimestamp(t + off, dt.timezone.utc).date()  # noqa: E731
        closes = d["indicators"]["quote"][0].get("close") or []
        bars = [(day(t), c) for t, c in zip(d.get("timestamp") or [], closes) if c is not None]
        ev = d.get("events") or {}
        splits = [(day(int(k)), v.get("numerator"), v.get("denominator")) for k, v in (ev.get("splits") or {}).items()]
        divs = sorted((day(int(k)), v.get("amount")) for k, v in (ev.get("dividends") or {}).items())
        return {"bars": bars, "splits": splits, "divs": divs, "url": url}

    # ---- SEC
    def _sec(self):
        return _imp("sec_fetch", TOOLS)

    def sec_cik(self, ticker):
        return self._sec().resolve(ticker)[0]

    def sec_facts(self, ticker):
        return self._sec().company_facts(self.sec_cik(ticker))

    def sec_filings(self, cik):
        return self._sec().submissions(cik)[1]

    def sec_filing_docs(self, cik, accession):
        key = (cik, accession)
        if key not in self._idx:
            s = self._sec()
            self._idx[key] = [(it["name"], s.archive_url(cik, accession, it["name"])) for it in s.filing_index(cik, accession)]
        return self._idx[key]

    # ---- documents
    def doc_text(self, url):
        """PDF/HTML -> plain text, cached for good (documents do not change)."""
        os.makedirs(os.path.join(C.CACHE, "docs"), exist_ok=True)
        key = C.hashlib.sha1(url.encode()).hexdigest()
        txt = os.path.join(C.CACHE, "docs", key + ".txt")
        if os.path.exists(txt):
            return C.read_text(txt)
        hdr = {"Referer": "https://www.nseindia.in/"} if "nseindia" in url else \
            {"User-Agent": self._sec().UA} if "sec.gov" in url else {}
        b = C.http_get(url, hdr, binary=True, max_age_h=24 * 3650)
        if b[:5] == b"%PDF-":
            pdf = txt[:-4] + ".pdf"
            C.write_bytes(pdf, b)
            if not shutil.which("pdftotext"):
                raise RuntimeError("pdftotext (poppler-utils) not installed")
            subprocess.run(["pdftotext", "-layout", pdf, txt], check=True, timeout=180)
            os.remove(pdf)
            return C.read_text(txt)
        s = self._sec().html_to_text(b.decode("utf-8", "replace"))
        C.write_text(txt, s)
        return s
