#!/usr/bin/env python3
"""Pre-registered allocation test (research_notes/Allocation/allocation_test_india.md).

India, rupees, month-end. Equity / gold / 10-yr gilt / cash; strategies 100% equity, 70/20/10 yearly, 70/20/10 +-5pp bands,
P/E-tercile tilt, new-money-to-underweight SIP, 50/50 equity/gold. Standard library + curl. Public sources only.

  python3 tools/allocation/backtest.py --fetch   # download raw data to research_notes/Allocation/data/ (as_of stamped)
  python3 tools/allocation/backtest.py           # compute from saved data -> data/results.json + data/monthly.csv
"""
import argparse, csv, datetime as dt, json, math, os, re, subprocess, sys, zipfile

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DATA = os.path.join(REPO, "research_notes", "Allocation", "data")
PE_CSV = os.path.join(REPO, "research_notes", "Macro", "ey_gap_test_outputs", "monthly.csv")
END = "2026-10"   # last complete month

YH = "https://query1.finance.yahoo.com/v8/finance/chart/{}?period1=900000000&period2=1795000000&interval=1d"
SRC = {
    "yahoo_sensex.json": YH.format("%5EBSESN"),
    "yahoo_nifty.json": YH.format("%5ENSEI"),
    "yahoo_gold_usd.json": YH.format("GC%3DF"),
    "yahoo_usdinr.json": YH.format("INR%3DX"),
    "yahoo_goldbees.json": YH.format("GOLDBEES.NS"),
    "fred_EXINUS.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=EXINUS",
    "fred_INDIRLTLT01STM.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDIRLTLT01STM",
    "fred_INDIR3TIB01STM.csv": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=INDIR3TIB01STM",
    "mf_100822_uti_nifty50_index.json": "https://api.mfapi.in/mf/100822",
    "mf_101281_hdfc_sensex_index.json": "https://api.mfapi.in/mf/101281",
    "mf_101002_sbi_10y_cm_gilt.json": "https://api.mfapi.in/mf/101002",
    "mf_100851_nippon_liquid.json": "https://api.mfapi.in/mf/100851",
    "mf_105085_gold_bees.json": "https://api.mfapi.in/mf/105085",
    "wb_cmo_monthly.xlsx": ("https://thedocs.worldbank.org/en/doc/5d903e848db1d1b83e0ec8f744e55570-0350012021/related/"
                            "CMO-Historical-Data-Monthly.xlsx"),
}


def fetch_all():
    os.makedirs(DATA, exist_ok=True)
    meta = {}
    for fn, url in SRC.items():
        path = os.path.join(DATA, fn)
        ua = ["-A", "Mozilla/5.0"] if "yahoo" in url else []   # Yahoo needs a browser UA; FRED rejects it
        p = subprocess.run(["curl", "-sS", "-L", "-m", "90", *ua, "-o", path, "-w", "%{http_code}", url],
                           capture_output=True, text=True)
        meta[fn] = {"url": url, "http": p.stdout.strip(), "as_of": dt.date.today().isoformat()}
        print(fn, p.stdout.strip(), file=sys.stderr)
    # the World Bank workbook is large: keep only the gold column as CSV
    xl = os.path.join(DATA, "wb_cmo_monthly.xlsx")
    if os.path.exists(xl):
        rows = wb_gold(xl)
        with open(os.path.join(DATA, "wb_gold_usd_monthly_avg.csv"), "w") as f:
            f.write("month,gold_usd_oz_lbma_pm_monthly_avg\n" + "".join(f"{k},{v}\n" for k, v in sorted(rows.items())))
        os.remove(xl)
        meta["wb_gold_usd_monthly_avg.csv"] = dict(meta.pop("wb_cmo_monthly.xlsx"), note="gold column extracted")
    json.dump(meta, open(os.path.join(DATA, "sources.json"), "w"), indent=1)


def wb_gold(path):
    z = zipfile.ZipFile(path)
    st = [re.sub("<[^>]+>", "", x) for x in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode(), re.S)]
    s = z.read("xl/worksheets/sheet2.xml").decode()
    col, out = None, {}
    for row in re.findall(r"<row [^>]*>(.*?)</row>", s, re.S):
        cells = re.findall(r'<c r="([A-Z]+)\d+"([^>]*)>(?:<v>([^<]*)</v>)?', row)
        if col is None:
            for c, attr, v in cells:
                if 't="s"' in attr and v and st[int(v)] == "Gold":
                    col = c
            continue
        d = {c: (st[int(v)] if 't="s"' in a and v else v) for c, a, v in cells}
        m = re.match(r"(\d{4})M(\d\d)", d.get("A", "") or "")
        if m and d.get(col):
            try:
                out[f"{m.group(1)}-{m.group(2)}"] = float(d[col])
            except ValueError:
                pass
    return out


# ---------------------------------------------------------------- loaders -> {YYYY-MM: month-end value}
def load_yahoo(fn):
    j = json.load(open(os.path.join(DATA, fn)))["chart"]["result"][0]
    out = {}
    for t, c in zip(j["timestamp"], j["indicators"]["quote"][0]["close"]):
        if c is None:
            continue
        k = (dt.datetime.fromtimestamp(t, dt.timezone.utc) + dt.timedelta(hours=6)).strftime("%Y-%m")  # IST bars stamp 18:30 UTC
        if k <= END:
            out[k] = c
    return out


def load_fred(fn):
    out = {}
    for row in csv.reader(open(os.path.join(DATA, fn))):
        if len(row) == 2 and row[0][:2] in ("19", "20"):
            try:
                out[row[0][:7]] = float(row[1])
            except ValueError:
                pass
    return out


def load_mf(fn, split_fix=False):
    d = json.load(open(os.path.join(DATA, fn)))["data"]
    pts = sorted((dt.datetime.strptime(x["date"], "%d-%m-%Y").date(), float(x["nav"])) for x in d if float(x["nav"]) > 0)
    if split_fix:   # face-value changes show up as one-day jumps > 20%: chain them out
        adj, f, prev = [], 1.0, None
        for day, v in pts:
            if prev and (v / prev > 1.2 or v / prev < 0.8):
                f *= prev / v
            adj.append((day, v * f)); prev = v
        pts = adj
    out = {}
    for day, v in pts:
        k = day.strftime("%Y-%m")
        if k <= END:
            out[k] = v   # last NAV of the month wins
    return out


def load_csv(fn, col):
    return {r["month"]: float(r[col]) for r in csv.DictReader(open(os.path.join(DATA, fn)))}


def months(a, b):
    y, m = int(a[:4]), int(a[5:])
    out = []
    while f"{y}-{m:02d}" <= b:
        out.append(f"{y}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def rets(levels, ms):
    return {ms[i]: levels[ms[i]] / levels[ms[i - 1]] - 1 for i in range(1, len(ms))}


def cagr(a, b, n_months):
    return (b / a) ** (12 / n_months) - 1


# ---------------------------------------------------------------- series
def build():
    sensex, nifty = load_yahoo("yahoo_sensex.json"), load_yahoo("yahoo_nifty.json")
    gc, inr = load_yahoo("yahoo_gold_usd.json"), load_yahoo("yahoo_usdinr.json")
    wbg, exinus = load_csv("wb_gold_usd_monthly_avg.csv", "gold_usd_oz_lbma_pm_monthly_avg"), load_fred("fred_EXINUS.csv")
    y10, tb = load_fred("fred_INDIRLTLT01STM.csv"), load_fred("fred_INDIR3TIB01STM.csv")
    uti, hdfcsx = load_mf("mf_100822_uti_nifty50_index.json"), load_mf("mf_101281_hdfc_sensex_index.json")
    gilt, liquid = load_mf("mf_101002_sbi_10y_cm_gilt.json"), load_mf("mf_100851_nippon_liquid.json", split_fix=True)
    goldbees_mf = load_mf("mf_105085_gold_bees.json")
    try:
        goldbees_y = load_yahoo("yahoo_goldbees.json")
    except Exception:
        goldbees_y = {}
    pe = {r["month"]: (float(r["pe"]), float(r["dy"])) for r in csv.DictReader(open(PE_CSV))}

    start = max(min(uti), min(gilt), min(k for k in inr), min(gc))
    start = months(start, END)[1] if start not in uti else start
    ms = [k for k in months(start, END)]
    miss = [k for k in ms if not all(k in s for s in (uti, gilt, gc, inr))]
    ms = [k for k in ms if k not in miss]

    gold_inr = {k: gc[k] * inr[k] for k in ms}
    gold_inr_wb = {k: wbg[k] * exinus[k] for k in ms if k in wbg and k in exinus}
    # bond total-return approximation from yields (D=7, C=60), from first FRED month
    yb, lvl = {}, None
    for k in months(min(y10), END):
        if k not in y10:
            continue
        if lvl is None:
            lvl, prev = 100.0, y10[k]
        else:
            dy_ = (y10[k] - prev) / 100
            lvl *= 1 + prev / 1200 - 7 * dy_ + 0.5 * 60 * dy_ ** 2
            prev = y10[k]
        yb[k] = lvl
    # Sensex/Nifty price + dividend yield (NSE DY 2012-02+, else 1.3% assumed)
    def pr_tr(px):
        lv, out, keys = 100.0, {}, sorted(px)
        for i, k in enumerate(keys):
            if i:
                dyv = pe.get(keys[i - 1], (None, 1.3))[1]
                lv *= px[k] / px[keys[i - 1]] * (1 + dyv / 1200)
            out[k] = lv
        return out
    return dict(ms=ms, missing=miss, equity=uti, gold=gold_inr, bond=gilt, cash=liquid, tbill=tb,
                checks=dict(sensex_tr=pr_tr(sensex), nifty_tr=pr_tr(nifty), hdfc_sensex_fund=hdfcsx, gold_inr_wb=gold_inr_wb,
                            goldbees_mf=goldbees_mf, goldbees_y=goldbees_y, bond_yield_approx=yb, sensex=sensex,
                            usdinr_y=inr, usdinr_fred=exinus, gold_usd=gc, gold_usd_wb=wbg),
                pe=pe)


# ---------------------------------------------------------------- simulation
GOLD_COST = 0.005 / 12   # ETF/fund expense; equity and gilt series are fund NAVs (already net of expense)
TRADE_COST = 0.001


def eq_ltcg(k):
    return 0.10 if k < "2024-07" else 0.125


def sim(S, ms, rule, tilt=None):
    """Lump sum Rs 10 lakh. rule: 'none'|'jan'|'band'. Returns monthly wealth list and stats on tax/turnover."""
    A = ("equity", "gold", "bond")
    R = {a: rets(S[a], ms) for a in A}
    fixed = TARGET[0]

    def target(k):
        return tilt(k) if tilt else fixed

    w0 = target(ms[0])
    val = {a: 1e6 * w0[a] for a in A}
    basis = dict(val)
    path, taxes, turnover = [1e6], 0.0, 0.0
    for k in ms[1:]:
        for a in A:
            val[a] *= 1 + R[a][k] - (GOLD_COST if a == "gold" else 0)
        V = sum(val.values())
        t = target(k)
        do = False
        if rule == "jan" and k[5:] == "01":
            do = True
        elif rule == "band" and any(abs(val[a] / V - t[a]) > 0.05 for a in A if t[a] > 0 or val[a] > 0):
            do = True
        if do:
            tax = 0.0
            for a in A:
                sell = val[a] - V * t[a]
                if sell > 0 and val[a] > 0:
                    gain = sell * (1 - basis[a] / val[a])
                    rate = eq_ltcg(k) if a == "equity" else 0.20
                    tax += max(gain, 0) * rate
                    basis[a] *= 1 - sell / val[a]
            trade = sum(abs(val[a] - V * t[a]) for a in A) / 2
            V2 = V - tax - TRADE_COST * trade * 2
            for a in A:
                new = V2 * t[a]
                if new > val[a]:
                    basis[a] += new - val[a]
                val[a] = new
            taxes += tax; turnover += trade
        path.append(sum(val.values()))
    return path, {"taxes_paid": round(taxes), "turnover": round(turnover)}


def sip(S, ms, mode):
    """Rs 10,000 at each month-end. mode: 'equity'|'split_jan'|'underweight'. Returns (values, cashflows)."""
    A = ("equity", "gold", "bond")
    R = {a: rets(S[a], ms) for a in A}
    t = TARGET[0]
    val = {a: 0.0 for a in A}
    basis = dict(val)
    vals, taxes = [], 0.0
    for i, k in enumerate(ms):
        if i:
            for a in A:
                val[a] *= 1 + R[a][k] - (GOLD_COST if a == "gold" else 0)
        c = 10000.0
        if mode == "equity":
            val["equity"] += c
        elif mode == "split_jan":
            for a in A:
                val[a] += c * t[a]; basis[a] += c * t[a]
            V = sum(val.values())
            if k[5:] == "01" and i > 0:
                tax = 0.0
                for a in A:
                    sell = val[a] - V * t[a]
                    if sell > 0:
                        gain = sell * (1 - basis[a] / val[a])
                        tax += max(gain, 0) * (eq_ltcg(k) if a == "equity" else 0.20)
                        basis[a] *= 1 - sell / val[a]
                trade = sum(abs(val[a] - V * t[a]) for a in A) / 2
                V2 = V - tax - TRADE_COST * trade * 2
                for a in A:
                    new = V2 * t[a]
                    if new > val[a]:
                        basis[a] += new - val[a]
                    val[a] = new
                taxes += tax
        else:
            V = sum(val.values()) + c
            a = max(A, key=lambda x: t[x] - (val[x] / V if V else 0))
            val[a] += c
        vals.append(sum(val.values()))
    tot = sum(val.values())
    return vals, taxes, {a: round(val[a] / tot, 3) for a in A}


def xirr_monthly(vals):
    """Monthly contributions of 10,000 at t=0..n-1; terminal value vals[-1] at t=n-1."""
    n = len(vals)
    lo, hi = -0.5, 1.0
    for _ in range(200):
        r = (lo + hi) / 2
        m = (1 + r) ** (1 / 12)
        fv = sum(10000 * m ** (n - 1 - i) for i in range(n))
        lo, hi = (r, hi) if fv < vals[-1] else (lo, r)
    return r


# ---------------------------------------------------------------- metrics
def metrics(path, ms, ref=None):
    n = len(path) - 1
    peak, pk_i, mdd, dd_info, under, longest, cur_start = path[0], 0, 0.0, None, 0, 0, None
    for i, v in enumerate(path):
        if v >= peak:
            peak, pk_i = v, i
            under = 0
        else:
            under += 1
            longest = max(longest, under)
            dd = v / peak - 1
            if dd < mdd:
                mdd, dd_info = dd, (pk_i, i, peak, v)
    rec = None
    if dd_info:
        pk_i, tr_i, pv, tv = dd_info
        for j in range(tr_i, len(path)):
            if path[j] >= pv:
                rec = j; break
    r = [path[i] / path[i - 1] - 1 for i in range(1, len(path))]
    mu = sum(r) / len(r)
    vol = math.sqrt(sum((x - mu) ** 2 for x in r) / (len(r) - 1) * 12)
    roll = [cagr(path[i], path[i + 60], 60) for i in range(len(path) - 60)]
    out = {"cagr": cagr(path[0], path[-1], n), "end_value": path[-1], "vol": vol, "max_dd": mdd,
           "dd_peak": ms[dd_info[0]], "dd_trough": ms[dd_info[1]], "dd_rupees_peak": dd_info[2], "dd_rupees_trough": dd_info[3],
           "dd_rupees": dd_info[2] - dd_info[3],
           "recovered": ms[rec] if rec is not None else None,
           "months_peak_to_recovery": (rec - dd_info[0]) if rec is not None else None,
           "months_trough_to_recovery": (rec - dd_info[1]) if rec is not None else None,
           "longest_underwater_months": longest, "worst_5y_cagr": min(roll), "best_5y_cagr": max(roll),
           "n_5y_windows": len(roll)}
    if ref is not None:
        rr = [cagr(ref[i], ref[i + 60], 60) for i in range(len(ref) - 60)]
        out["pct_5y_beat_equity"] = sum(a > b for a, b in zip(roll, rr)) / len(roll)
    return out


TARGET = [{"equity": 0.70, "gold": 0.20, "bond": 0.10}]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fetch", action="store_true")
    a = ap.parse_args()
    if a.fetch:
        fetch_all()
    S = build()
    ms = S["ms"]
    res = {"window": [ms[0], ms[-1]], "n_months": len(ms) - 1, "missing_months": S["missing"], "strategies": {}}
    runs = {}
    TARGET[0] = {"equity": 1.0, "gold": 0.0, "bond": 0.0}
    runs["1_equity_100"] = sim(S, ms, "none")
    TARGET[0] = {"equity": 0.5, "gold": 0.5, "bond": 0.0}
    runs["6_5050_eq_gold_yearly"] = sim(S, ms, "jan")
    TARGET[0] = {"equity": 0.7, "gold": 0.2, "bond": 0.1}
    runs["2_702010_yearly"] = sim(S, ms, "jan")
    runs["3_702010_bands5"] = sim(S, ms, "band")
    eq = runs["1_equity_100"][0]
    for name, (p, extra) in runs.items():
        res["strategies"][name] = dict(metrics(p, ms, eq), **extra)

    # valuation tilt window: P/E months; expanding terciles need >= 24 months history -> start 2014-01
    pe = S["pe"]
    tw = [k for k in ms if "2014-01" <= k]
    def tilt(k):
        hist = sorted(v[0] for kk, v in pe.items() if kk < k)
        cur = pe.get(k, pe.get(max(kk for kk in pe if kk <= k)))[0]
        lo, hi = hist[len(hist) // 3], hist[2 * len(hist) // 3]
        e = 0.8 if cur <= lo else (0.6 if cur > hi else 0.7)
        return {"equity": e, "gold": (1 - e) * 2 / 3, "bond": (1 - e) / 3}
    tilt_path, tex = sim(S, tw, "jan", tilt=tilt)
    TARGET[0] = {"equity": 1.0, "gold": 0.0, "bond": 0.0}
    eq_t, _ = sim(S, tw, "none")
    TARGET[0] = {"equity": 0.7, "gold": 0.2, "bond": 0.1}
    fx_t, fex = sim(S, tw, "jan")
    tilt_log = {k: tilt(k)["equity"] for k in tw if k[5:] == "01"}
    res["tilt_window"] = {"window": [tw[0], tw[-1]], "equity_weight_by_january": tilt_log,
                          "4_pe_tilt": dict(metrics(tilt_path, tw, eq_t), **tex),
                          "1_equity_100": metrics(eq_t, tw, eq_t),
                          "2_702010_yearly": dict(metrics(fx_t, tw, eq_t), **fex)}

    # POST-HOC sensitivities (not pre-registered; labelled as such in the md)
    sens = {}
    def run3(S2, ms2):
        out = {}
        for nm, tg, rl in (("1_equity_100", (1, 0, 0), "none"), ("2_702010_yearly", (.7, .2, .1), "jan"),
                           ("6_5050_eq_gold_yearly", (.5, .5, 0), "jan")):
            TARGET[0] = dict(zip(("equity", "gold", "bond"), tg))
            out[nm] = sim(S2, ms2, rl)[0]
        TARGET[0] = {"equity": 0.7, "gold": 0.2, "bond": 0.1}
        return {nm: {x: round(v, 4) for x, v in metrics(p, ms2, out["1_equity_100"]).items()
                     if x in ("cagr", "max_dd", "worst_5y_cagr", "pct_5y_beat_equity", "longest_underwater_months")}
                for nm, p in out.items()}
    gc = cagr(S["gold"][ms[0]], S["gold"][ms[-1]], len(ms) - 1)
    drag = (1 + gc) ** (1 / 12) / (1.07) ** (1 / 12) - 1
    g2, lv = {}, None
    for i, k in enumerate(ms):
        g2[k] = S["gold"][k] if i == 0 else g2[ms[i - 1]] * (S["gold"][k] / S["gold"][ms[i - 1]]) / (1 + drag)
    sens["gold_cut_to_7pct_cagr"] = run3(dict(S, gold=g2), ms)
    sens["equity_sensex_price_plus_dy"] = run3(dict(S, equity=S["checks"]["sensex_tr"]), ms)
    sens["start_2009_04_after_crash"] = run3(S, [k for k in ms if k >= "2009-04"])
    avg_e = sum(tilt(k)["equity"] for k in tw if k[5:] == "01") / len([k for k in tw if k[5:] == "01"])
    TARGET[0] = {"equity": avg_e, "gold": (1 - avg_e) * 2 / 3, "bond": (1 - avg_e) / 3}
    ctl, _ = sim(S, tw, "jan")
    TARGET[0] = {"equity": 0.7, "gold": 0.2, "bond": 0.1}
    sens["tilt_control_fixed_avg_equity"] = dict(equity_weight=round(avg_e, 3), **{x: round(v, 4) for x, v in
                                                 metrics(ctl, tw, eq_t).items() if x in ("cagr", "max_dd", "worst_5y_cagr")})
    res["post_hoc_sensitivity"] = sens

    # SIPs
    sips = {}
    for mode in ("equity", "split_jan", "underweight"):
        v, tx, fw = sip(S, ms, mode)
        peak, mdd, dd_r = 0, 0, 0
        for x in v:
            peak = max(peak, x)
            mdd, dd_r = min(mdd, x / peak - 1), max(dd_r, peak - x)
        sips[mode] = {"xirr": xirr_monthly(v), "invested": 10000 * len(v), "end_value": v[-1], "max_fall_pct": mdd,
                      "max_fall_rupees": dd_r, "taxes_paid": round(tx), "final_weights": fw}
    res["sip"] = sips

    # cross-checks (overlapping windows)
    C = S["checks"]
    def cg(series, a, b):
        if a in series and b in series:
            return cagr(series[a], series[b], len(months(a, b)) - 1)
    chk = {}
    chk["equity_uti_nifty_fund_cagr"] = cg(S["equity"], ms[0], ms[-1])
    chk["equity_hdfc_sensex_fund_cagr"] = cg(C["hdfc_sensex_fund"], ms[0], ms[-1])
    chk["equity_sensex_price_plus_dy_cagr"] = cg(C["sensex_tr"], ms[0], ms[-1])
    chk["equity_sensex_price_only_cagr"] = cg(C["sensex"], ms[0], ms[-1])
    chk["equity_nifty_price_plus_dy_2012_02"] = cg(C["nifty_tr"], "2012-02", ms[-1])
    chk["equity_uti_fund_2012_02"] = cg(S["equity"], "2012-02", ms[-1])
    chk["gold_inr_yahoo_cagr"] = cg(S["gold"], ms[0], ms[-1])
    wb_end = max(C["gold_inr_wb"])
    chk["gold_wb_window"] = [ms[0], wb_end]
    chk["gold_inr_wb_x_fred_cagr"] = cg(C["gold_inr_wb"], ms[0], wb_end)
    chk["gold_inr_yahoo_same_wb_window"] = cg(S["gold"], ms[0], wb_end)
    chk["gold_usd_yahoo_cagr"] = cg(C["gold_usd"], ms[0], ms[-1])
    chk["usdinr_cagr"] = cg(C["usdinr_y"], ms[0], ms[-1])
    gb = C["goldbees_y"] or C["goldbees_mf"]
    gb0 = max(min(gb), ms[0]); gb1 = min(max(gb), ms[-1])
    chk["goldbees_window"] = [gb0, gb1]
    chk["goldbees_cagr"] = cg(gb, gb0, gb1)
    chk["gold_inr_yahoo_same_window"] = cg(S["gold"], gb0, gb1)
    chk["bond_sbi_cm_gilt_fund_cagr"] = cg(S["bond"], ms[0], ms[-1])
    chk["bond_yield_approx_2011_12"] = cg(C["bond_yield_approx"], "2011-12", ms[-1])
    chk["bond_sbi_fund_2011_12"] = cg(S["bond"], "2011-12", ms[-1])
    chk["cash_liquid_fund_cagr"] = cg(S["cash"], ms[0], ms[-1])
    tb = [v for k, v in sorted(S["tbill"].items()) if "2011-12" <= k <= ms[-1]]
    lv = 1.0
    for v in tb[:-1]:
        lv *= 1 + v / 1200
    chk["cash_tbill_accrued_2011_12"] = lv ** (12 / (len(tb) - 1)) - 1
    chk["cash_liquid_fund_2011_12"] = cg(S["cash"], "2011-12", ms[-1])
    gold_pairs = [(k, S["gold"][k], C["gold_inr_wb"].get(k)) for k in ms if k in C["gold_inr_wb"]]
    chk["gold_level_diff_pct_median"] = sorted(abs(a / b - 1) for _, a, b in gold_pairs)[len(gold_pairs) // 2]
    chk["end_levels"] = {"gold_usd_yahoo": C["gold_usd"][ms[-1]], "gold_usd_wb_avg": C["gold_usd_wb"].get(ms[-1]),
                         "usdinr_yahoo": C["usdinr_y"][ms[-1]], "usdinr_fred_avg": C["usdinr_fred"].get(ms[-1]),
                         "gold_inr_10g_yahoo": S["gold"][ms[-1]] / 31.1034768 * 10}
    # annual asset returns + correlations
    yrs = sorted({k[:4] for k in ms if k[5:] == "12"})
    ann = {}
    for y in yrs:
        a0 = f"{int(y)-1}-12"
        if a0 in S["equity"] and a0 >= ms[0]:
            ann[y] = {x: S[x][f"{y}-12"] / S[x][a0] - 1 for x in ("equity", "gold", "bond")}
    chk["annual_returns"] = ann
    def corr(x, y):
        mx, my = sum(x) / len(x), sum(y) / len(y)
        return sum((a - mx) * (b - my) for a, b in zip(x, y)) / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))
    R = {x: rets(S[x], ms) for x in ("equity", "gold", "bond")}
    chk["monthly_corr"] = {"eq_gold": corr(list(R["equity"].values()), list(R["gold"].values())),
                           "eq_bond": corr(list(R["equity"].values()), list(R["bond"].values())),
                           "gold_bond": corr(list(R["gold"].values()), list(R["bond"].values()))}
    res["checks"] = chk
    res["costs"] = {"gold_cost_pa": 0.005, "trade_cost": TRADE_COST, "eq_ltcg": "10% to 2024-06, 12.5% after, no exemption",
                    "gold_bond_tax": 0.20, "equity_series": "UTI Nifty 50 Index Fund regular-plan NAV (net of expense)",
                    "bond_series": "SBI 10-yr Constant Maturity Gilt Fund regular-plan NAV (net of expense)",
                    "gold_series": "Yahoo GC=F x Yahoo INR=X month-end, minus 0.5%/yr"}
    json.dump(res, open(os.path.join(DATA, "results.json"), "w"), indent=1, default=float)
    with open(os.path.join(DATA, "monthly.csv"), "w") as f:
        f.write("month,equity_nav,gold_inr_oz,bond_nav,w_eq100,w_702010_yearly,w_702010_bands,w_5050\n")
        for i, k in enumerate(ms):
            f.write(f"{k},{S['equity'][k]:.4f},{S['gold'][k]:.2f},{S['bond'][k]:.4f},"
                    + ",".join(f"{runs[n][0][i]:.0f}" for n in ("1_equity_100", "2_702010_yearly", "3_702010_bands5", "6_5050_eq_gold_yearly")) + "\n")
    print(json.dumps({k: res[k] for k in ("window", "n_months", "missing_months")}))
    for n, m in res["strategies"].items():
        print(f"{n:24s} CAGR {m['cagr']:.2%} end {m['end_value']/1e5:.1f}L maxDD {m['max_dd']:.1%} (-{m['dd_rupees']/1e5:.1f}L "
              f"{m['dd_peak']}->{m['dd_trough']}, rec {m['recovered']} pk2rec {m['months_peak_to_recovery']}m) worst5y "
              f"{m['worst_5y_cagr']:.2%} beat {m.get('pct_5y_beat_equity',0):.0%} underwater {m['longest_underwater_months']}m "
              f"vol {m['vol']:.1%} tax {m.get('taxes_paid',0)/1e5:.2f}L")
    tw_ = res["tilt_window"]
    print("tilt window", tw_["window"], tw_["equity_weight_by_january"])
    for n in ("1_equity_100", "2_702010_yearly", "4_pe_tilt"):
        m = tw_[n]
        print(f"  {n:20s} CAGR {m['cagr']:.2%} maxDD {m['max_dd']:.1%} worst5y {m['worst_5y_cagr']:.2%} "
              f"beat {m.get('pct_5y_beat_equity',0):.0%} underwater {m['longest_underwater_months']}m")
    for n, m in sips.items():
        print(f"SIP {n:12s} XIRR {m['xirr']:.2%} invested {m['invested']/1e5:.1f}L end {m['end_value']/1e5:.1f}L "
              f"maxfall {m['max_fall_pct']:.1%} (-{m['max_fall_rupees']/1e5:.1f}L) tax {m['taxes_paid']/1e5:.2f}L")
    print(json.dumps({k: v for k, v in chk.items() if k != "annual_returns"}, default=float))
    print(json.dumps(sens, indent=0))
    print({n: m["final_weights"] for n, m in sips.items()})


if __name__ == "__main__":
    main()
