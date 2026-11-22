#!/usr/bin/env python3
"""FEIN solvency screen, India (Roadmap stage 2: hard filters). Standard library + system curl.

For each NSE symbol, reads the latest annual (fiscal-year) consolidated numbers from screener.in
and computes the Indian adaptation of the US-tested solvency flags (decision:solvency-flags-graded,
lesson L24). Graded red = S1 or S5. These are "look harder, size smaller" flags, not a short signal
and not protection: in the US test they caught only 8-16% of later failures.

Flags (FY0 = latest fiscal year in the profit-and-loss table; balance sheet at the same date):
  S1raw  net worth < 0 (Equity Capital + Reserves; minority interest is NOT included).
  S1     S1raw, unless payout-driven: FCF(FY0) > 0 AND dividends paid over the last 3 FYs >= |net worth|.
         (The US test exempted buyback-driven negative equity. Indian buybacks are small and screener does
         not split them out of "Other financing items", so only dividends count; the exemption should
         almost never apply. Exempt rows are reported with s1raw=1, s1=0.)
  S2     interest cover EBIT / Interest < 1.5x, EBIT = Operating Profit - Depreciation (excludes screener's
         Other Income, which carries one-off gains; fallback PBT + Interest). Negative EBIT with any interest fires.
         Interest 0 or missing: not fired if borrowings < 5% of total assets, else unknown.
  S2b    India-adjusted variant: interest cover < 2.5x (UNTESTED; reported, not used for the grade).
  S3     short-term funding gap: short-term borrowings > 0 and > cash equivalents + 0.5 x CFO
         (CFO with its sign). Ind AS Schedule III puts current maturities of long-term debt inside
         short-term borrowings, which matches the US "debt current" definition.
  S4     payouts > FCF while debt rose: dividends paid > 0 and > FCF(FY0) and borrowings(FY0) >
         borrowings(FY-1). (Buybacks not separable on screener -> dividends only.)
  S5     >= 2 of S1..S4 fired (unknown = not fired; S5 known if >= 2 components known).
  S5b    same with S2b instead of S2 (UNTESTED variant).
Banks, NBFCs / financial institutions, insurers and margin-funding brokers are excluded
(status=financial_alm): their borrowings are inventory, so these flags do not apply; they need a
separate asset-liability-maturity (ALM) test.

Outputs ($FEIN_DATA/solvency/):
  solvency_<date>.csv, solvency_<date>.md, latest.csv; rows also go to fein.sqlite table `solvency`,
  which detect.py turns into alerts solvency_s1 / solvency_s5 (once per symbol per fiscal year).
Cache: $FEIN_DATA/solvency/cache/<SYM>/ (page + schedule JSON), reused for --max-age-days (default 6).

Usage:
  python3 solvency_screen.py                         # whole universe (~1,550 names, ~4 requests each, ~2.5 h)
  python3 solvency_screen.py --sample 150 --seed 7   # random validation sample
  python3 solvency_screen.py --symbols VEDL,IDEA     # specific names
  python3 solvency_screen.py --selftest              # offline flag checks
Research tool, not SEBI-registered advice.
"""
import argparse, csv, datetime as dt, json, os, random, re, subprocess, sys, time, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "promise_tracker", "pipeline"))
import fein_common as C  # noqa: E402
from fein_common import log  # noqa: E402
try:
    import financials as F  # screener table parser (tools/promise_tracker/pipeline/financials.py)
except ImportError:
    sys.exit("needs tools/promise_tracker/pipeline/financials.py and common.py next to tools/detectors/ "
             "(copy both folders, or the whole repo, onto the Pi)")

F.ROWMAP.update({"total assets": "total_assets", "total liabilities": "total_liabilities",
                 "investments": "investments", "other liabilities": "other_liabilities",
                 "other assets": "other_assets", "free cash flow": "fcf"})

ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
UNIVERSE = os.path.join(ROOT, "research_notes", "Backtests", "india_pead_live", "universe.csv")
OUT = os.path.join(C.DATA, "solvency")
SCREENER = "https://www.screener.in"
GAP = 1.5
ICR, ICR_INDIA, NO_INT_DEBT_SHARE = 1.5, 2.5, 0.05
STALE_DAYS = 550          # FY0 older than ~18 months: company probably not filing (suspended/dead?)
FIN_BROAD = {"banks", "finance", "insurance"}
FIN_INDUSTRY = ("stockbroking", "non banking", "nbfc", "housing finance", "financial institution", "microfinance")
SCHEDULES = [("Borrowings", "balance-sheet"), ("Other Assets", "balance-sheet"),
             ("Cash from Financing Activity", "cash-flow")]
_last = [0.0]


# ---------- fetching ----------
def curl(url, tries=4):
    err = None
    for i in range(tries):
        wait = GAP - (time.time() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.time()
        try:
            r = subprocess.run(["curl", "-sS", "-L", "--compressed", "-A", "Mozilla/5.0", "--max-time", "60",
                                "-w", "\n%{http_code}", url], capture_output=True, timeout=90)
            body, _, code = r.stdout.rpartition(b"\n")
            code = code.decode().strip()
            if code == "200":
                return body.decode("utf-8", "replace")
            if code == "404":
                return None
            err = f"HTTP {code}"
        except (subprocess.TimeoutExpired, OSError) as e:
            err = str(e)
        if i < tries - 1:
            back = 10 * 2 ** i if err == "HTTP 429" else 5 * 2 ** i
            log.warning("screener %s: %s; retry in %ss", url[:100], err, back)
            time.sleep(back)
    raise RuntimeError(f"screener fetch failed: {url} ({err})")


def cached(path, max_age, fetch):
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < max_age * 86400:
        return open(path, errors="replace").read()
    body = fetch()
    if body is not None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(body)
    return body


def labels(page):
    out = {}
    for t, v in re.findall(r'title="(Broad Sector|Sector|Broad Industry|Industry)">([^<]*)<', page):
        out[t] = re.sub(r"&amp;", "&", v).strip()
    return out


def company_name(page):
    m = re.search(r"<h1[^>]*>.*?overflow-wrap-anywhere\">([^<]+)<", page, re.S) or re.search(r"<h1[^>]*>\s*([^<]+?)\s*</h1>", page)
    return m.group(1).strip().replace("&amp;", "&") if m else ""


def fy0_basis(page):
    """'standalone' if screener marks the latest annual column '(S)' (no consolidated accounts), else 'consolidated'."""
    i = page.find('id="profit-loss"')
    heads = [re.sub(r"\s+", " ", h).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", page[i:page.find("</table>", i)], re.S)]
    heads = [h for h in heads if h and not h.upper().startswith("TTM")]
    return "standalone" if heads and "(S)" in heads[-1] else "consolidated"


def fetch_company(sym, max_age, cache):
    d = os.path.join(cache, sym)
    url = f"{SCREENER}/company/{urllib.parse.quote(sym)}/consolidated/"
    page = cached(os.path.join(d, "page.html"), max_age, lambda: curl(url))
    if not page or 'id="profit-loss"' not in page:
        return None, url, None, None
    m = re.search(r'data-company-id="(\d+)"', page)
    return page, url, (m.group(1) if m else None), d


def fetch_schedules(cid, d, max_age):
    out = {}
    for parent, sec in SCHEDULES:
        q = urllib.parse.urlencode({"parent": parent, "section": sec, "consolidated": "true"})
        u = f"{SCREENER}/api/company/{cid}/schedules/?{q}"
        txt = cached(os.path.join(d, re.sub(r"\W+", "_", parent).lower() + ".json"), max_age, lambda: curl(u))
        try:
            out[parent] = json.loads(txt) if txt else {}
        except ValueError:
            out[parent] = {}
    return out


def sched_value(sched, parent, key, date):
    row = (sched.get(parent) or {}).get(key) or {}
    for h, v in row.items():
        if F._date(h) == date:
            return F._num(v) if isinstance(v, str) else None
    return None


# ---------- flags ----------
def is_financial(lab, page):
    bi = lab.get("Broad Industry", "").lower()
    ind = lab.get("Industry", "").lower()
    if bi in FIN_BROAD or any(k in ind for k in FIN_INDUSTRY):
        return True
    # screener's bank/NBFC template ("Revenue"/"Financing Profit") as a fallback when labels are missing
    return not lab and "Financing Profit" in page


def inputs(fin, sched):
    """Pick FY0 / FY-1 and the inputs. Returns dict (None where missing)."""
    fys = sorted(fin["FY"])
    if not fys:
        return None
    fy0 = fys[-1]
    bs_dates = sorted(d for d in fin["BS"] if d.month == fy0.month and d <= fy0)
    if not bs_dates or bs_dates[-1] != fy0:
        return None
    bs0 = fin["BS"][fy0]
    bs1 = fin["BS"][bs_dates[-2]] if len(bs_dates) > 1 else {}
    pl = fin["FY"][fy0]
    g = lambda k, r=pl: r.get(k)
    eq = (bs0.get("equity_capital") or 0) + bs0["reserves"] if bs0.get("reserves") is not None else None
    interest, pbt = g("interest"), g("pbt")
    divs = [sched_value(sched, "Cash from Financing Activity", "Dividends paid", d) for d in fys[-3:]]
    d0 = sched_value(sched, "Cash from Financing Activity", "Dividends paid", fy0)
    return {
        "fy0": fy0, "net_worth": eq,
        # EBIT = Operating Profit - Depreciation (closest to US OperatingIncomeLoss). Screener's "Other
        # Income" carries exceptional items (e.g. Vodafone Idea FY26 +Rs 59,292 cr), so PBT + interest is
        # only the fallback.
        "ebit": (g("op_profit") - (g("depreciation") or 0)) if g("op_profit") is not None
        else ((pbt + (interest or 0)) if pbt is not None else None), "interest": interest,
        "std": sched_value(sched, "Borrowings", "Short term Borrowings", fy0),
        "cash": sched_value(sched, "Other Assets", "Cash Equivalents", fy0),
        "cfo": g("cfo"), "fcf": g("fcf"),
        "dividends": abs(d0) if d0 is not None else (0.0 if sched.get("Cash from Financing Activity") else None),
        "div3": sum(abs(x) for x in divs if x is not None),
        "debt0": bs0.get("borrowings"), "debt1": bs1.get("borrowings"), "assets": bs0.get("total_assets"),
    }


def flags(x):
    """x = inputs(). Returns dict of flag -> 1/0/None (None = unknown)."""
    f = {}
    E = x["net_worth"]
    f["s1raw"] = None if E is None else int(E < 0)
    exempt = bool(f["s1raw"]) and (x["fcf"] or 0) > 0 and x["div3"] >= abs(E)
    f["s1"] = None if E is None else int(E < 0 and not exempt)
    f["s1_exempt"] = int(exempt)
    I, ebit = x["interest"], x["ebit"]
    if I and I > 0 and ebit is not None:
        f["icr"] = ebit / I
        f["s2"], f["s2b"] = int(f["icr"] < ICR), int(f["icr"] < ICR_INDIA)
    else:
        f["icr"] = None
        low_debt = x["debt0"] is not None and x["assets"] and x["debt0"] < NO_INT_DEBT_SHARE * x["assets"]
        f["s2"] = f["s2b"] = 0 if (low_debt or (x["debt0"] == 0)) else None
    std, cash, cfo = x["std"], x["cash"], x["cfo"]
    if std is None:
        f["s3"] = 0 if x["debt0"] == 0 else None
    elif cash is None or cfo is None:
        f["s3"] = 0 if std <= 0 else None
    else:
        f["s3"] = int(std > 0 and std > cash + 0.5 * cfo)
    D, fcf = x["dividends"], x["fcf"]
    if D is None or fcf is None or x["debt0"] is None or x["debt1"] is None:
        f["s4"] = 0 if D == 0 else None
    else:
        f["s4"] = int(D > 0 and D > fcf and x["debt0"] > x["debt1"])
    for out, s2 in (("s5", "s2"), ("s5b", "s2b")):
        comps = [f["s1"], f[s2], f["s3"], f["s4"]]
        known, fired = sum(c is not None for c in comps), sum(c == 1 for c in comps)
        f[out] = int(fired >= 2) if (fired >= 2 or known >= 2) else None
    f["n_flags"] = sum(f[k] == 1 for k in ("s1", "s2", "s3", "s4"))
    return f


def describe(x, f):
    parts = []
    n = lambda v: "n/a" if v is None else f"{v:,.0f}"
    if f["s1raw"]:
        parts.append(f"net worth Rs {n(x['net_worth'])} cr" + (" (payout-driven, exempt)" if f["s1_exempt"] else ""))
    if f["s2b"]:
        parts.append(f"interest cover {f['icr']:.2f}x (EBIT {n(x['ebit'])} / interest {n(x['interest'])})")
    if f["s3"]:
        parts.append(f"short-term borrowings {n(x['std'])} > cash {n(x['cash'])} + 0.5 x CFO {n(x['cfo'])}")
    if f["s4"]:
        parts.append(f"dividends {n(x['dividends'])} > FCF {n(x['fcf'])} while debt {n(x['debt1'])} -> {n(x['debt0'])}")
    return "; ".join(parts) + f" (FY {x['fy0']:%b %Y}, Rs cr)"


def screen_one(sym, max_age, cache):
    row = {"symbol": sym, "status": "", "grade": ""}
    page, url, cid, d = fetch_company(sym, max_age, cache)
    row["url"] = url
    if page is None:
        row["status"] = "no_page"
        return row
    lab = labels(page)
    row["name"] = company_name(page)
    row["industry"] = " / ".join(v for k, v in lab.items() if k in ("Broad Industry", "Industry"))
    fin = F.parse_screener(page)
    row["basis"] = fy0_basis(page)
    if is_financial(lab, page):
        row["status"] = "financial_alm"
        return row
    sched = fetch_schedules(cid, d, max_age) if cid else {}
    x = inputs(fin, sched)
    if x is None:
        row["status"] = "no_annual_data"
        return row
    f = flags(x)
    row.update({k: x[k] for k in ("net_worth", "ebit", "interest", "std", "cash", "cfo", "fcf", "dividends", "debt0", "debt1")})
    row.update({k: f[k] for k in ("icr", "s1raw", "s1", "s2", "s2b", "s3", "s4", "s5", "s5b", "n_flags")})
    row["fy0"] = x["fy0"].isoformat()
    stale = (dt.date.today() - x["fy0"]).days > STALE_DAYS
    row["status"] = "stale_fy" if stale else "ok"
    row["grade"] = "red" if (f["s1"] or f["s5"]) else ""
    row["details"] = describe(x, f) if (f["s1raw"] or f["n_flags"] or f["s2b"]) else ""
    return row


# ---------- outputs ----------
COLS = ["symbol", "name", "industry", "basis", "status", "fy0", "grade", "n_flags", "s1raw", "s1", "s2", "s2b", "s3", "s4",
        "s5", "s5b", "net_worth", "ebit", "interest", "icr", "std", "cash", "cfo", "fcf", "dividends", "debt0", "debt1",
        "details", "url"]


def fmt(v):
    if isinstance(v, float):
        return f"{v:.2f}"
    return "" if v is None else v


def write(rows, day, note):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"solvency_{day}.csv")
    for p in (path, os.path.join(OUT, "latest.csv")):
        with open(p, "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(COLS)
            for r in rows:
                w.writerow([fmt(r.get(c)) for c in COLS])
    st = {}
    for r in rows:
        st[r["status"]] = st.get(r["status"], 0) + 1
    ok = [r for r in rows if r["status"] in ("ok", "stale_fy")]

    def cnt(k):
        known = [r for r in ok if r.get(k) is not None]
        return f"{sum(r[k] == 1 for r in known)} / {len(known)}"
    md = [f"# FEIN solvency screen {day}", "",
          f"{note}. Universe screened: {len(rows)}. Status: " + ", ".join(f"{k} {v}" for k, v in sorted(st.items())) + ".",
          "Graded red = S1 or S5 (decision:solvency-flags-graded). Look harder and size smaller; not a short signal. "
          "Research, not SEBI-registered advice.", "",
          "| flag | fired / known |", "|---|---|"]
    for k, lab in (("s1raw", "S1raw net worth < 0"), ("s1", "S1 (after payout exemption)"), ("s2", "S2 interest cover < 1.5x"),
                   ("s2b", "S2b interest cover < 2.5x (India variant, untested)"), ("s3", "S3 short-term funding gap"),
                   ("s4", "S4 dividends > FCF while debt rose"), ("s5", "S5 >= 2 of S1-S4"), ("s5b", "S5b >= 2 using S2b (untested)")):
        md.append(f"| {lab} | {cnt(k)} |")
    red = sorted((r for r in ok if r["grade"] == "red"), key=lambda r: (-(r["n_flags"] or 0), r["symbol"]))
    md += ["", f"## Graded red ({len(red)})", "", "| symbol | name | flags | details |", "|---|---|---|---|"]
    for r in red:
        fl = ",".join(k.upper() for k in ("s1", "s2", "s3", "s4") if r.get(k) == 1)
        md.append(f"| {r['symbol']} | {r.get('name', '')} | {fl} | {r['details']} |")
    s5b_only = [r for r in ok if r.get("s5b") == 1 and r["grade"] != "red"]
    md += ["", f"## India variant only: S5b fires, S5 does not ({len(s5b_only)}; untested, for information)", ""]
    md += [f"- {r['symbol']}: {r['details']}" for r in s5b_only]
    fin = [r["symbol"] for r in rows if r["status"] == "financial_alm"]
    md += ["", f"## Financials excluded - need an ALM test ({len(fin)})", "", ", ".join(fin) or "none"]
    stale = [f"{r['symbol']} (FY {r['fy0']})" for r in rows if r["status"] == "stale_fy"]
    md += ["", f"## Stale annual data, FY0 older than {STALE_DAYS} days ({len(stale)})", "", ", ".join(stale) or "none"]
    bad = [f"{r['symbol']} ({r['status']})" for r in rows if r["status"] in ("no_page", "no_annual_data", "error")]
    md += ["", f"## Not screened ({len(bad)})", "", ", ".join(bad) or "none"]
    with open(os.path.join(OUT, f"solvency_{day}.md"), "w") as fh:
        fh.write("\n".join(md) + "\n")
    return path


def to_db(rows, day):
    con = C.db()
    db_rows = [dict({c: r.get(c) for c in COLS}, snapshot_date=day) for r in rows]
    C.upsert(con, "solvency", db_rows)
    con.commit()


# ---------- selftest ----------
def selftest():
    D = dt.date(2026, 3, 31)
    base = {"fy0": D, "net_worth": 100.0, "ebit": 50.0, "interest": 10.0, "std": 10.0, "cash": 20.0, "cfo": 30.0,
            "fcf": 10.0, "dividends": 5.0, "div3": 15.0, "debt0": 100.0, "debt1": 90.0, "assets": 500.0}
    cases = [
        ("clean", {}, {"s1": 0, "s2": 0, "s3": 0, "s4": 0, "s5": 0}),
        ("negative net worth, loss-making", {"net_worth": -50.0, "ebit": -5.0, "fcf": -3.0},
         {"s1raw": 1, "s1": 1, "s2": 1, "s5": 1}),
        ("payout-driven negative equity exempt", {"net_worth": -10.0, "fcf": 40.0, "div3": 30.0}, {"s1raw": 1, "s1": 0}),
        ("icr 2.0: India variant only", {"ebit": 20.0}, {"s2": 0, "s2b": 1, "s5": 0}),
        ("funding gap + payouts beyond FCF", {"std": 80.0, "cfo": 10.0, "dividends": 20.0}, {"s3": 1, "s4": 1, "s5": 1}),
        ("debt-free, no interest", {"interest": 0.0, "debt0": 0.0, "debt1": 0.0, "std": 0.0}, {"s2": 0, "s3": 0, "s4": 0}),
        ("indebted, interest missing -> unknown", {"interest": None, "debt0": 300.0}, {"s2": None}),
    ]
    ok = True
    for name, upd, exp in cases:
        got = flags(dict(base, **upd))
        good = all(got[k] == v for k, v in exp.items())
        ok &= good
        print(f"  {'PASS' if good else 'FAIL'} {name}: {({k: got[k] for k in exp})}")
    print("selftest:", "ALL PASS" if ok else "FAILURES above")
    return 0 if ok else 1


def load_universe(path):
    with open(path) as fh:
        return [r["sym"].strip().upper() for r in csv.DictReader(fh) if r.get("sym")]


def main():
    global GAP
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--symbols", help="comma-separated NSE symbols (default: universe file)")
    p.add_argument("--universe", default=UNIVERSE, help="CSV with a 'sym' column")
    p.add_argument("--sample", type=int, help="random sample of N symbols from the universe")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--limit", type=int)
    p.add_argument("--max-age-days", type=float, default=6)
    p.add_argument("--gap", type=float, default=GAP, help="seconds between requests (>= 1.5)")
    p.add_argument("--no-db", action="store_true", help="do not write fein.sqlite (no detect.py alerts)")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    GAP = max(1.5, a.gap)
    C.setup_logging("solvency")
    lock = C.single_instance("solvency")
    if lock is None:
        log.error("another solvency_screen.py is running")
        return 1
    syms = [s.strip().upper() for s in a.symbols.split(",")] if a.symbols else load_universe(a.universe)
    note = f"Symbols from {'--symbols' if a.symbols else os.path.relpath(a.universe, ROOT)}"
    if a.sample:
        syms = sorted(random.Random(a.seed).sample(syms, min(a.sample, len(syms))))
        note += f", random sample of {len(syms)} (seed {a.seed})"
    if a.limit:
        syms = syms[:a.limit]
    cache = os.path.join(OUT, "cache")
    rows, t0 = [], time.time()
    for i, s in enumerate(syms, 1):
        try:
            r = screen_one(s, a.max_age_days, cache)
        except Exception as e:
            log.warning("%s: %s", s, e)
            r = {"symbol": s, "status": "error", "details": str(e)[:200]}
        rows.append(r)
        if r.get("grade") == "red":
            log.info("RED %s %s", s, r.get("details"))
        if i % 25 == 0:
            log.info("%d/%d done, %.0f s", i, len(syms), time.time() - t0)
    day = C.today_ist().isoformat()
    path = write(rows, day, note)
    if not a.no_db:
        to_db(rows, day)
    st = {}
    for r in rows:
        st[r["status"]] = st.get(r["status"], 0) + 1
    log.info("solvency screen: %d symbols, %s, red %d, %.0f s -> %s", len(rows), st,
             sum(r.get("grade") == "red" for r in rows), time.time() - t0, path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
