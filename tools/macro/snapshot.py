#!/usr/bin/env python3
"""FEIN monthly macro snapshot (India + US context). Roadmap stage 5 (valuation context).

Standard library + the system `curl`. Public pages and files only: no logins, no API keys, no CAPTCHA or
anti-bot workarounds, one request at a time with a gap between requests. A source that fails is recorded as
missing, never guessed. Every field carries value, unit, as_of, source URL and, where cheap, a second source.

  python3 tools/macro/snapshot.py                    # snapshot for the current month -> research_notes/Macro/
  python3 tools/macro/snapshot.py --month 2026-11 --memdb   # also store key numbers as memdb metrics (MACRO)
  python3 tools/macro/snapshot.py --out-dir DIR      # write elsewhere (the Pi job writes to $FEIN_DATA/macro)
  python3 tools/macro/snapshot.py --selftest         # offline parser checks on fixtures, no network

Fields that no public machine-readable source gives (CPI on the 2024 base, NSDL FPI flows: NSDL returns an
empty reply to scripted requests) come from tools/macro/manual.json, entered by hand with a source URL, and are
marked "manual". Research, not SEBI-registered advice.
"""
import argparse, csv, datetime as dt, html, io, json, os, re, subprocess, sys, tempfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
GAP = 1.5
_last = [0.0]

URL = {
    "rbi_home": "https://www.rbi.org.in/",
    "fred": "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}",
    "ecb": "https://api.frankfurter.dev/v1/latest?base=USD&symbols=INR,EUR,JPY,GBP,CAD,SEK,CHF",
    "gold": "https://api.gold-api.com/price/XAU",
    "ibja": "https://ibjarates.com/",
    "nse_idx": "https://archives.nseindia.com/content/indices/ind_close_all_{}.csv",
    "ust": ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"
            "{y}/all?type=daily_treasury_yield_curve&field_tdr_date_value={y}&page&_format=csv"),
    "nsdl": "https://www.fpi.nsdl.co.in/web/Reports/Monthly.aspx",
}
TROY_OZ_G = 31.1034768


def fetch(url, timeout=30):
    """GET via curl. Returns text or None (failure is data, not an exception)."""
    wait = GAP - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    try:
        p = subprocess.run(["curl", "-sS", "-L", "-m", str(timeout), "-w", "\n%{http_code}", url],
                           capture_output=True, timeout=timeout + 10)
    except Exception:
        return None
    out = p.stdout.decode("utf-8", "replace")
    body, _, code = out.rpartition("\n")
    return body if p.returncode == 0 and code.strip() == "200" else None


def field(value, unit, as_of, source, note="", second=None, kind="auto"):
    d = {"value": value, "unit": unit, "as_of": as_of, "source": source, "kind": kind}
    if note:
        d["note"] = note
    if second:
        d["second"] = second
    return d


def missing(source, note):
    return {"value": None, "unit": "", "as_of": None, "source": source, "kind": "missing", "note": note}


# ---------------------------------------------------------------- parsers (pure, tested offline)
def html_text(s):
    s = re.sub(r"<script.*?</script>|<style.*?</style>", " ", s, flags=re.S | re.I)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)))


def parse_rbi_home(s, year):
    """RBI home 'Current Rates' box: repo rate, FBIL USD reference rate, G-sec yields by maturity."""
    t = html_text(s)
    out = {}
    m = re.search(r"Policy Repo Rate\s*:\s*([\d.]+)\s*%", t)
    if m:
        out["repo"] = float(m.group(1))
    m = re.search(r"INR / 1 USD\s*:\s*([\d.]+)", t)
    if m:
        out["usdinr"] = float(m.group(1))
    m = re.search(r"As at [^)]*?of ([A-Z][a-z]+ \d{1,2}, \d{4})", t)
    if m:
        out["fx_as_of"] = dt.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()
    m = re.search(r"as on ([A-Z][a-z]+ \d{1,2}, \d{4})", t)
    if m:
        out["mkt_as_of"] = dt.datetime.strptime(m.group(1), "%B %d, %Y").date().isoformat()
    gs = [(int(y), float(v), f"{c}% GS {y}") for c, y, v in re.findall(r"([\d.]+)% GS (\d{4})\s*:\s*([\d.]+)%", t)]
    if gs:
        y, v, name = min(gs, key=lambda g: abs(g[0] - (year + 10)))
        out["gsec10"] = (v, name)
    return out


def parse_fred(s):
    """FRED fredgraph.csv -> last (date, value) with a numeric value."""
    last = None
    for row in csv.reader(io.StringIO(s)):
        if len(row) == 2 and re.match(r"\d{4}-\d{2}-\d{2}", row[0]):
            try:
                last = (row[0], float(row[1]))
            except ValueError:
                pass
    return last


def dxy_from_rates(r):
    """ICE US Dollar Index formula applied to ECB reference rates (rates quoted per 1 USD)."""
    eurusd, gbpusd = 1 / r["EUR"], 1 / r["GBP"]
    return (50.14348112 * eurusd ** -0.576 * r["JPY"] ** 0.136 * gbpusd ** -0.119 * r["CAD"] ** 0.091
            * r["SEK"] ** 0.042 * r["CHF"] ** 0.036)


def parse_nse_idx(s, name="Nifty 50"):
    """NSE ind_close_all CSV -> dict for one index (old files call Nifty 50 'S&P CNX Nifty'/'CNX Nifty')."""
    aliases = {name.lower()} | ({"s&p cnx nifty", "cnx nifty"} if name == "Nifty 50" else set())
    for row in csv.DictReader(io.StringIO(s)):
        if (row.get("Index Name") or "").strip().lower() in aliases:
            f = lambda k: float(row[k]) if row.get(k) not in (None, "", "-") else None  # noqa: E731
            d = dt.datetime.strptime(row["Index Date"].strip().replace("/", "-"), "%d-%m-%Y").date().isoformat()
            return {"date": d, "close": f("Closing Index Value"), "pe": f("P/E"), "pb": f("P/B"), "dy": f("Div Yield")}
    return None


def parse_ust(s):
    rows = list(csv.DictReader(io.StringIO(s)))
    for r in rows:  # newest first
        if r.get("10 Yr"):
            return dt.datetime.strptime(r["Date"], "%m/%d/%Y").date().isoformat(), float(r["10 Yr"])
    return None


def parse_ibja(s):
    m = re.search(r'id="lblGold999_AM">\s*([\d.]+)', s)
    if not m:
        return None
    dates = [dt.datetime.strptime(d, "%d/%m/%Y").date() for d in re.findall(r"\b(\d{2}/\d{2}/\d{4})\b", s)]
    return float(m.group(1)), (max(dates).isoformat() if dates else None)


# ---------------------------------------------------------------- collection
def latest_nse(today):
    for back in range(0, 8):
        d = today - dt.timedelta(days=back)
        if d.weekday() >= 5:
            continue
        u = URL["nse_idx"].format(d.strftime("%d%m%Y"))
        s = fetch(u)
        if s and "Index Name" in s:
            r = parse_nse_idx(s)
            if r:
                return r, u
    return None, None


def collect(today, manual):
    F = {}
    rbi = fetch(URL["rbi_home"])
    r = parse_rbi_home(rbi, today.year) if rbi else {}
    fred = {k: (parse_fred(fetch(URL["fred"].format(k)) or "") or None)
            for k in ("INDIRLTLT01STM", "DEXINUS", "DCOILBRENTEU", "DTWEXBGS", "DGS10")}
    fu = lambda k: URL["fred"].format(k).replace("graph/fredgraph.csv?id=", "series/")  # noqa: E731

    F["rbi_repo_rate"] = (field(r["repo"], "%", r.get("fx_as_of") or today.isoformat(), URL["rbi_home"],
                                "RBI home page 'Current Rates' box; date is the page's rates date")
                          if "repo" in r else missing(URL["rbi_home"], "RBI page not parsed"))
    if "gsec10" in r:
        v, name = r["gsec10"]
        sec = {"value": fred["INDIRLTLT01STM"][1], "as_of": fred["INDIRLTLT01STM"][0], "source": fu("INDIRLTLT01STM"),
               "note": "OECD MEI via FRED, monthly average"} if fred["INDIRLTLT01STM"] else None
        F["india_10y_gsec"] = field(v, "%", r.get("mkt_as_of"), URL["rbi_home"],
                                    f"{name} (security nearest 10-yr maturity on RBI's list)", sec)
    elif fred["INDIRLTLT01STM"]:
        F["india_10y_gsec"] = field(fred["INDIRLTLT01STM"][1], "%", fred["INDIRLTLT01STM"][0], fu("INDIRLTLT01STM"),
                                    "monthly average; RBI page unavailable")
    else:
        F["india_10y_gsec"] = missing(URL["rbi_home"], "no source answered")

    ecb_s = fetch(URL["ecb"])
    ecb = json.loads(ecb_s) if ecb_s else None
    secs = []
    if fred["DEXINUS"]:
        secs.append({"value": fred["DEXINUS"][1], "as_of": fred["DEXINUS"][0], "source": fu("DEXINUS"), "note": "Fed H.10 noon NY"})
    if ecb:
        secs.append({"value": ecb["rates"]["INR"], "as_of": ecb["date"], "source": URL["ecb"], "note": "ECB reference via Frankfurter"})
    if "usdinr" in r:
        F["usd_inr"] = field(r["usdinr"], "INR per USD", r.get("fx_as_of"), URL["rbi_home"], "FBIL reference rate", secs or None)
    elif secs:
        F["usd_inr"] = field(secs[0]["value"], "INR per USD", secs[0]["as_of"], secs[0]["source"], secs[0]["note"], secs[1:] or None)
    else:
        F["usd_inr"] = missing(URL["rbi_home"], "no source answered")

    F["brent_usd"] = (field(fred["DCOILBRENTEU"][1], "USD/bbl", fred["DCOILBRENTEU"][0], fu("DCOILBRENTEU"), "EIA Europe Brent spot via FRED")
                      if fred["DCOILBRENTEU"] else missing(fu("DCOILBRENTEU"), "FRED did not answer"))
    if ecb:
        sec = ({"value": fred["DTWEXBGS"][1], "as_of": fred["DTWEXBGS"][0], "source": fu("DTWEXBGS"),
                "note": "Fed broad trade-weighted dollar (Jan-2006=100): a different index, direction check only"}
               if fred["DTWEXBGS"] else None)
        F["dxy"] = field(round(dxy_from_rates(ecb["rates"]), 2), "index", ecb["date"], URL["ecb"],
                         "computed: ICE DXY formula on ECB reference rates (approximation, not ICE's print)", sec)
    else:
        F["dxy"] = missing(URL["ecb"], "ECB rates unavailable")

    g = fetch(URL["gold"])
    g = json.loads(g) if g else None
    ib = fetch(URL["ibja"])
    ib = parse_ibja(ib) if ib else None
    if g:
        F["gold_usd_oz"] = field(round(g["price"], 2), "USD/troy oz", g["updatedAt"][:10], URL["gold"], "spot, gold-api.com")
        fx = F["usd_inr"]["value"]
        if fx:
            sec = ({"value": ib[0], "as_of": ib[1], "source": URL["ibja"],
                    "note": "IBJA 999 AM rate: domestic, includes import duty, excludes GST"} if ib else None)
            F["gold_inr_10g"] = field(round(g["price"] * fx / TROY_OZ_G * 10), "INR per 10 g", g["updatedAt"][:10],
                                      URL["gold"], "computed: USD spot x USD/INR / 31.1035 x 10 (no duty)", sec)
    else:
        F["gold_usd_oz"] = missing(URL["gold"], "gold-api.com did not answer")
        F["gold_inr_10g"] = (field(ib[0], "INR per 10 g", ib[1], URL["ibja"], "IBJA 999 AM, includes duty") if ib
                             else missing(URL["ibja"], "no source answered"))

    n, nu = latest_nse(today)
    if n:
        F["nifty50_close"] = field(n["close"], "index", n["date"], nu, "NSE daily index file")
        F["nifty50_pe"] = field(n["pe"], "x", n["date"], nu, "trailing P/E, consolidated earnings basis since 31-Mar-2021")
        F["nifty50_pb"] = field(n["pb"], "x", n["date"], nu)
        F["nifty50_div_yield"] = field(n["dy"], "%", n["date"], nu)
        if n["pe"] and F["india_10y_gsec"]["value"] is not None:
            ey = 100 / n["pe"]
            F["nifty50_earnings_yield"] = field(round(ey, 3), "%", n["date"], nu, "100 / trailing P/E")
            F["nifty_ey_minus_gsec10"] = field(round(ey - F["india_10y_gsec"]["value"], 3), "pp", n["date"], nu,
                                               "earnings yield minus India 10-yr G-sec; see research_notes/Macro/ey_gsec_gap_test.md")
    else:
        F["nifty50_close"] = missing(URL["nse_idx"], "no NSE index file in the last 8 days")

    u = fetch(URL["ust"].format(y=today.year))
    u = parse_ust(u) if u else None
    sec = {"value": fred["DGS10"][1], "as_of": fred["DGS10"][0], "source": fu("DGS10")} if fred["DGS10"] else None
    F["us_10y"] = (field(u[1], "%", u[0], URL["ust"].format(y=today.year), "US Treasury par yield curve", sec) if u
                   else field(sec["value"], "%", sec["as_of"], sec["source"]) if sec else missing(URL["ust"], "no source answered"))

    nsdl = fetch(URL["nsdl"])
    F["fpi_net_equity_month"] = missing(URL["nsdl"], "NSDL FPI site gave no usable reply to a scripted request" if not nsdl
                                        else "NSDL page fetched but not parsed (add a parser)")
    for k, v in (manual or {}).items():   # hand-entered values for fields with no machine-readable source
        if k.startswith("_"):
            continue
        if F.get(k, {}).get("value") is None:
            F[k] = dict(v, kind="manual")
    return F


# ---------------------------------------------------------------- output
LABEL = [("rbi_repo_rate", "RBI policy repo rate"), ("india_10y_gsec", "India 10-yr G-sec yield"),
         ("india_cpi_yoy", "India CPI inflation (y/y)"), ("usd_inr", "USD/INR"), ("brent_usd", "Brent crude"),
         ("dxy", "US dollar index (DXY)"), ("gold_usd_oz", "Gold (USD)"), ("gold_inr_10g", "Gold (INR)"),
         ("nifty50_close", "Nifty 50"), ("nifty50_pe", "Nifty 50 trailing P/E"), ("nifty50_pb", "Nifty 50 P/B"),
         ("nifty50_div_yield", "Nifty 50 dividend yield"), ("nifty50_earnings_yield", "Nifty 50 earnings yield"),
         ("nifty_ey_minus_gsec10", "Earnings yield minus 10-yr G-sec"), ("us_10y", "US 10-yr Treasury"),
         ("fpi_net_equity_month", "FPI net equity flows (month to date)")]


def to_md(snap):
    L = [f"# Macro snapshot {snap['month']} (generated {snap['generated']})", "",
         "Stage 5 (valuation context). Every value has a date and a source; `second` = an independent cross-check.",
         "`manual` = entered by hand from the cited page (no machine-readable public source). Research, not advice.", "",
         "| Field | Value | Unit | As of | Source | Second source | Note |", "|---|---|---|---|---|---|---|"]
    F = snap["fields"]
    for k, lab in LABEL + [(k, k) for k in F if k not in dict(LABEL)]:
        if k not in F:
            continue
        f = F[k]
        s = f.get("second")
        s = s if isinstance(s, list) else [s] if s else []
        sec = "; ".join(f"{x['value']} ({x.get('as_of')}, [src]({x['source']}){', ' + x['note'] if x.get('note') else ''})" for x in s)
        val = "n/a" if f["value"] is None else f["value"]
        L.append(f"| {lab} | {val} | {f.get('unit', '')} | {f.get('as_of') or ''} | [{f['kind']}]({f['source']}) | {sec} | {f.get('note', '')} |")
    L += ["", "Gaps and caveats:",
          "- DXY is computed from ECB reference rates with ICE's weights; it can differ from ICE's print by a few tenths.",
          "- Gold INR (computed) excludes import duty; the IBJA domestic rate includes it. If the gap is far from the duty rate, treat both as unverified.",
          "- India 10-yr: RBI lists securities by maturity; the one nearest a 10-yr maturity is used. FRED is a monthly average.",
          "- Nifty P/E is on consolidated earnings since 31-Mar-2021 (standalone before), so long histories have a break."]
    return "\n".join(L) + "\n"


def store_memdb(snap):
    n = 0
    for k, f in snap["fields"].items():
        if isinstance(f.get("value"), (int, float)):
            cmd = [sys.executable, "-m", "memdb", "metric", "add", "MACRO", snap["month"], k, str(f["value"]),
                   "--unit", f.get("unit") or "-", "--source", f["source"], "--as-of", f.get("as_of") or snap["generated"]]
            if subprocess.run(cmd, cwd=REPO, capture_output=True).returncode == 0:
                n += 1
    return n


# ---------------------------------------------------------------- selftest (offline)
def selftest():
    checks = []
    rbi = ('<div>Policy Repo Rate : 5.50% Standing Deposit Facility Rate : 5.25%</div> INR / 1 USD : 92.4895 '
           '(As at 1.00pm of November 25, 2026) Money Market * as on November 25, 2026 6.20% GS 2029 : 6.8476% # '
           '6.53% GS 2031 : 7.0506% # 6.94% GS 2036 : 7.1641% # 7.06% GS 2041 : 7.3641%')
    r = parse_rbi_home(rbi, 2026)
    checks += [("rbi repo", r.get("repo") == 5.5), ("rbi fx", r.get("usdinr") == 92.4895),
               ("rbi date", r.get("fx_as_of") == "2026-11-25"), ("rbi gsec10 picks GS 2036", r.get("gsec10", (0, ""))[1].endswith("GS 2036")),
               ("rbi gsec value", r.get("gsec10", (0,))[0] == 7.1641)]
    checks.append(("fred last numeric", parse_fred("observation_date,X\n2026-09-01,7.06\n2026-10-01,7.38\n2026-11-01,.\n") == ("2026-10-01", 7.38)))
    usd = {"EUR": 1 / 1.08, "JPY": 150.0, "GBP": 1 / 1.27, "CAD": 1.36, "SEK": 10.5, "CHF": 0.88}
    checks.append(("dxy formula in plausible range", 95 < dxy_from_rates(usd) < 110))
    nse = ("Index Name,Index Date,Open Index Value,High Index Value,Low Index Value,Closing Index Value,Points Change,"
           "Change(%),Volume,Turnover (Rs. Cr.),P/E,P/B,Div Yield\n"
           "S&P CNX Nifty,31-12-2012,5901.2,5919,5897.15,5905.1,-3.25,-.06,64809641,3021.71,18.68,3.13,1.4\n"
           "Nifty 10 yr Benchmark G-Sec,25-11-2026,1,1,1,1,1,1,-,-,-,-,-\n")
    n = parse_nse_idx(nse)
    checks.append(("nse old alias", n and n["pe"] == 18.68 and n["date"] == "2012-12-31"))
    checks.append(("nse dash -> None", parse_nse_idx(nse, "Nifty 10 yr Benchmark G-Sec")["pe"] is None))
    checks.append(("ust", parse_ust('Date,"1 Mo","10 Yr"\n11/25/2026,4.27,4.85\n11/24/2026,4.21,4.91\n') == ("2026-11-25", 4.85)))
    checks.append(("ibja", parse_ibja('<td>25/11/2026</td><span id="lblGold999_AM">122982</span> 24/11/2026') == (122982.0, "2026-11-25")))
    snap = {"month": "2026-11", "generated": "2026-11-26", "fields": {
        "nifty50_pe": field(21.03, "x", "2026-11-25", "u"), "fpi_net_equity_month": missing("u", "x")}}
    md = to_md(snap)
    checks.append(("md renders n/a", "| n/a |" in md and "21.03" in md))
    tmp = tempfile.mkdtemp(prefix="fein-macro-selftest-")
    with open(os.path.join(tmp, "s.json"), "w") as fh:
        json.dump(snap, fh)
    checks.append(("json roundtrip", json.load(open(os.path.join(tmp, "s.json")))["month"] == "2026-11"))
    bad = [c for c, ok in checks if not ok]
    for c, ok in checks:
        print(("ok   " if ok else "FAIL ") + c)
    print(f"selftest: {len(checks) - len(bad)}/{len(checks)} passed")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--month", help="YYYY-MM label (default: current month)")
    ap.add_argument("--out-dir", default=os.path.join(REPO, "research_notes", "Macro"))
    ap.add_argument("--manual", default=os.path.join(HERE, "manual.json"))
    ap.add_argument("--memdb", action="store_true", help="store numeric fields as memdb metrics (ticker MACRO)")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    today = dt.date.today()
    month = a.month or today.strftime("%Y-%m")
    manual = {}
    if os.path.exists(a.manual):
        manual = json.load(open(a.manual)).get(month, {})
    snap = {"month": month, "generated": today.isoformat(), "fields": collect(today, manual)}
    os.makedirs(a.out_dir, exist_ok=True)
    base = os.path.join(a.out_dir, f"snapshot_{month}")
    with open(base + ".json", "w") as fh:
        json.dump(snap, fh, indent=1)
    with open(base + ".md", "w") as fh:
        fh.write(to_md(snap))
    got = sum(1 for f in snap["fields"].values() if f.get("value") is not None)
    print(f"wrote {base}.md/.json: {got}/{len(snap['fields'])} fields with values")
    if a.memdb:
        print(f"memdb: {store_memdb(snap)} metrics stored under MACRO {month}")
    return 0 if got >= len(snap["fields"]) // 2 else 1


if __name__ == "__main__":
    sys.exit(main())
