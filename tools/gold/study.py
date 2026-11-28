#!/usr/bin/env python3
"""Gold study: drawdown base rates (Q1), run-up (Q2), Fed/real-yield regime (Q3), INR cushion (Q4), forecast track
record (Q5), today's state, analog-based scenario probabilities and call probabilities, L52 allocation tie.
Method is pre-registered in research_notes/Gold/gold_study_2026-11/prereg.md. Stdlib only.

    python3 tools/gold/study.py [--data DIR] [--out DIR]     # writes results.json + tables.md into --out
Reads files written by tools/gold/fetch.py. Reusable monthly: re-run fetch.py into a new dated folder, then this.
"""
import argparse, collections, csv, datetime as dt, json, math, os, re, statistics as st

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DEF = os.path.join(REPO, "research_notes", "Gold", "gold_study_2026-11")
ALLOC = os.path.join(REPO, "research_notes", "Allocation", "data", "monthly.csv")
OZ_G = 31.1034768
BUCKETS = [("best", 0.25, 9), ("base", -0.05, 0.25), ("bad", -0.25, -0.05), ("worst", -9, -0.25)]
K_SHRINK, FLOOR = 3, 0.05

# LBMA Annual Precious Metals Forecast Survey (lbma.org.uk pages, read 2026-11-28): consensus average-price forecast
# for the year, published each January. Actual = World Bank/datahub annual average (computed below).
LBMA = {2020: 1558.8, 2022: 1801.9, 2023: 1859.0, 2024: 2058.96, 2025: 2735.33, 2026: 4741.97}


# ------------------------------------------------------------------ loaders
def fred(path):
    out = {}
    for r in csv.reader(open(path)):
        if len(r) >= 2 and re.match(r"\d{4}-\d\d-\d\d", r[0]):
            try:
                out[r[0]] = float(r[1])
            except ValueError:
                pass
    return out


def monthly_mean(daily):
    g = collections.defaultdict(list)
    for d, v in daily.items():
        g[d[:7]].append(v)
    return {k: sum(v) / len(v) for k, v in g.items()}


def fred_m(path):  # monthly FRED series (first-of-month dates) -> {YYYY-MM: v}
    return {k[:7]: v for k, v in fred(path).items()}


def simple_csv(path, col=1):
    out = {}
    for r in list(csv.reader(open(path)))[1:]:
        try:
            out[r[0][:7]] = float(r[col])
        except (ValueError, IndexError):
            pass
    return out


def yahoo_daily(path):
    r = json.load(open(path))["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    out = {}
    for i, t in enumerate(r["timestamp"]):
        c = q["close"][i]
        if c:
            out[dt.datetime.fromtimestamp(t, dt.timezone.utc).date().isoformat()] = (c, q["high"][i], q["low"][i])
    return out, r["meta"]


def months(a, b):
    y, m = int(a[:4]), int(a[5:])
    out = []
    while f"{y:04d}-{m:02d}" <= b:
        out.append(f"{y:04d}-{m:02d}")
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def add_m(k, n):
    y, m = int(k[:4]), int(k[5:]) - 1 + n
    return f"{y + m // 12:04d}-{m % 12 + 1:02d}"


def mdiff(a, b):
    return (int(b[:4]) - int(a[:4])) * 12 + int(b[5:]) - int(a[5:])


# ------------------------------------------------------------------ core analytics
def episodes(P, ms, thr=0.20):
    """Drawdowns from running ATH that reach >= thr before a new ATH. Returns list of dicts."""
    out, ath, athm, low, lowm, hit = [], None, None, None, None, False
    for k in ms:
        p = P[k]
        if ath is None or p >= ath:
            if hit:
                out.append(dict(peak=athm, peak_px=ath, trough=lowm, trough_px=low, recovered=k))
            ath, athm, low, lowm, hit = p, k, p, k, False
            continue
        if p < low:
            low, lowm = p, k
        if p <= ath * (1 - thr):
            hit = True
    if hit:
        out.append(dict(peak=athm, peak_px=ath, trough=lowm, trough_px=low, recovered=None))
    for e in out:
        e["depth"] = e["trough_px"] / e["peak_px"] - 1
        e["m_to_trough"] = mdiff(e["peak"], e["trough"])
        e["m_to_recover"] = mdiff(e["peak"], e["recovered"]) if e["recovered"] else None
        e["open_months_so_far"] = None if e["recovered"] else mdiff(e["peak"], ms[-1])
        pre = [k for k in ms if 0 < mdiff(k, e["peak"]) <= 36]
        if pre:
            mk = min(pre, key=lambda k: P[k])
            e["runup_x"] = e["peak_px"] / P[mk]
            e["runup_from"] = mk
            e["runup_months"] = mdiff(mk, e["peak"])
    return out


def regime(FF, k):
    a, b = FF.get(k), FF.get(add_m(k, -6))
    if a is None or b is None:
        return None
    d = a - b
    return "hiking" if d > 0.25 else "cutting" if d < -0.25 else "hold"


def bucket(r):
    for name, lo, hi in BUCKETS:
        if lo < r <= hi or (name == "best" and r > lo):
            return name
    return "worst"


def shrink(fx, nx, fa):
    return (nx * fx + K_SHRINK * fa) / (nx + K_SHRINK)


def finalize(p):
    p = {k: max(v, FLOOR) for k, v in p.items()}
    s = sum(p.values())
    return {k: v / s for k, v in p.items()}


def freq(rows, key):
    c = collections.Counter(bucket(r[key]) for r in rows if r.get(key) is not None)
    n = sum(c.values())
    return {b[0]: (c[b[0]] / n if n else 0.0) for b in BUCKETS}, n


def blend_probs(sets, key):
    fa, na = freq(sets["a"], key)
    parts = []
    for s in ("b", "c"):
        rows = [r for r in sets[s] if r.get(key) is not None]
        ne = len({r["ep"] for r in rows})
        if ne >= 2:
            fx, _ = freq(rows, key)
            parts.append({b: shrink(fx[b], ne, fa[b]) for b in fa})
    raw = {b: sum(p[b] for p in parts) / len(parts) for b in fa} if parts else fa
    return finalize(raw), {"a": fa, "n_months_a": na, "parts_used": len(parts)}


def event_prob(sets, fn):
    """fn(row) -> True/False/None. Same blend as scenarios (shrink b,c to a; >=2 episodes)."""
    def f(rows):
        v = [fn(r) for r in rows]
        v = [x for x in v if x is not None]
        return (sum(v) / len(v) if v else None), len({r["ep"] for r, x in zip(rows, [fn(r) for r in rows]) if x is not None})
    fa, _ = f(sets["a"])
    parts = []
    for s in ("b", "c"):
        fx, ne = f(sets[s])
        if fx is not None and ne >= 2:
            parts.append(shrink(fx, ne, fa))
    p = sum(parts) / len(parts) if parts else fa
    return max(min(p, 1 - FLOOR), FLOOR), {"a": fa, "parts": parts}


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=os.path.join(DEF, "data"))
    ap.add_argument("--out", default=DEF)
    a = ap.parse_args()
    D = lambda f: os.path.join(a.data, f)
    R = {"generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")}

    # gold monthly history: WB (to its last month) then datahub (WB/LBMA mirror) for later months
    wb = simple_csv(D("wb_gold_usd_monthly_avg.csv"))
    dh = simple_csv(D("datahub_gold_monthly.csv"))
    gd, gmeta = yahoo_daily(D("yahoo_gcf_1d.json"))
    yavg = monthly_mean({d: v[0] for d, v in gd.items()})
    last_full = max(dh)
    G = {k: wb[k] for k in wb}
    for k in dh:
        if k not in G and k >= "1968-04":
            G[k] = dh[k]
    ov = [abs(dh[k] / wb[k] - 1) for k in wb if k in dh and k >= "1968-04"]
    yo = [yavg[k] / G[k] - 1 for k in G if k in yavg and k >= "2001-01" and k <= last_full]
    R["source_check"] = {
        "wb_last": max(wb), "datahub_last": last_full,
        "wb_vs_datahub_max_abs_diff_pct": round(100 * max(ov), 3), "n_overlap": len(ov),
        "yahoo_gcf_monthly_avg_vs_hist_median_pct": round(100 * st.median(yo), 2),
        "yahoo_vs_hist_p5_p95_pct": [round(100 * sorted(yo)[int(0.05 * len(yo))], 2),
                                     round(100 * sorted(yo)[int(0.95 * len(yo))], 2)],
        "n_yahoo_overlap": len(yo)}
    ms68 = months("1968-04", last_full)
    ms75 = months("1975-01", last_full)

    # macro monthly
    CPI = fred_m(D("fred_CPIAUCSL.csv"))
    FF = fred_m(D("fred_FEDFUNDS.csv"))
    GS10 = fred_m(D("fred_GS10.csv"))
    FII = fred_m(D("fred_FII10.csv"))
    INR = fred_m(D("fred_EXINUS.csv"))
    RY = {}
    for k in GS10:
        if k in FII:
            RY[k] = FII[k]
        elif k in CPI and add_m(k, -12) in CPI:
            RY[k] = GS10[k] - 100 * (CPI[k] / CPI[add_m(k, -12)] - 1)
    GI = {k: G[k] * INR[k] for k in G if k in INR}
    real = {k: G[k] / CPI[k] * CPI[last_full] for k in G if k in CPI}

    # ---------------- Q1 / Q2 / Q3 / Q4 per episode
    def annotate(E, P):
        for e in E:
            e["regime_at_peak"] = regime(FF, e["peak"])
            fall = months(e["peak"], e["trough"])
            rg = collections.Counter(regime(FF, k) for k in fall)
            e["regime_during_fall"] = dict(rg)
            e["ry_at_peak"] = RY.get(e["peak"]); e["ry_at_trough"] = RY.get(e["trough"])
            e["ry_change_fall_pp"] = (RY[e["trough"]] - RY[e["peak"]]) if e["peak"] in RY and e["trough"] in RY else None
            e["ff_at_peak"] = FF.get(e["peak"]); e["ff_at_trough"] = FF.get(e["trough"])
            e["regime_at_trough"] = regime(FF, e["trough"])
            t12 = add_m(e["trough"], 12)
            e["ry_change_trough_plus12_pp"] = (RY[t12] - RY[e["trough"]]) if t12 in RY and e["trough"] in RY else None
            if e["peak"] in INR and e["trough"] in INR:
                e["inr_ret_same_window"] = GI[e["trough"]] / GI[e["peak"]] - 1
                e["usdinr_change"] = INR[e["trough"]] / INR[e["peak"]] - 1
                e["cushion_pp"] = 100 * (e["inr_ret_same_window"] - e["depth"])
            if e["peak"] in real:
                rt = [k for k in months(e["peak"], last_full) if k in real]
                rec = next((k for k in rt[1:] if real[k] >= real[e["peak"]]), None)
                e["real_m_to_recover"] = mdiff(e["peak"], rec) if rec else None
                e["real_depth"] = min(real[k] for k in rt[:max(1, mdiff(e["peak"], e["recovered"] or last_full))]) / real[e["peak"]] - 1
        return E

    E20 = annotate(episodes(G, ms68, 0.20), G)
    E15 = annotate(episodes(G, ms68, 0.15), G)
    EI20 = episodes(GI, [k for k in ms75 if k in GI], 0.20)
    EI15 = episodes(GI, [k for k in ms75 if k in GI], 0.15)
    R["episodes_usd_20"] = E20; R["episodes_usd_15"] = E15
    R["episodes_inr_20"] = EI20; R["episodes_inr_15"] = EI15

    # Q3 broad: 12m gold return vs 12m change in real yield; by regime
    q3 = []
    for k in ms75:
        k12 = add_m(k, 12)
        if k12 in G and k in RY and k12 in RY:
            q3.append((G[k12] / G[k] - 1, RY[k12] - RY[k], regime(FF, k), RY[k], k))
    def corr(x, y):
        mx, my = st.mean(x), st.mean(y)
        sx = math.sqrt(sum((i - mx) ** 2 for i in x)); sy = math.sqrt(sum((j - my) ** 2 for j in y))
        return sum((i - mx) * (j - my) for i, j in zip(x, y)) / (sx * sy)
    R["q3"] = {
        "corr_12m_gold_vs_12m_dRY_1975_2002_proxy": round(corr([r[0] for r in q3 if r[4] < "2003-01"], [r[1] for r in q3 if r[4] < "2003-01"]), 2),
        "corr_12m_gold_vs_12m_dRY_2003_on_tips": round(corr([r[0] for r in q3 if r[4] >= "2003-01"], [r[1] for r in q3 if r[4] >= "2003-01"]), 2),
        "fwd12_by_regime": {g: {"n_months": len(v), "median_pct": round(100 * st.median(v), 1),
                                "p_neg": round(sum(x < 0 for x in v) / len(v), 2)}
                            for g in ("hiking", "hold", "cutting")
                            for v in [[r[0] for r in q3 if r[2] == g]] if v},
        "fwd12_by_ry_level": {lab: {"n_months": len(v), "median_pct": round(100 * st.median(v), 1),
                                    "p_neg": round(sum(x < 0 for x in v) / len(v), 2)}
                              for lab, lo, hi in (("ry<0", -99, 0), ("0-2", 0, 2), ("ry>=2", 2, 99))
                              for v in [[r[0] for r in q3 if lo <= r[3] < hi]] if v},
    }
    # Q4 broad: in months where USD gold 12m return < 0, how often did INR gold do better, by how much
    q4 = [(G[add_m(k, 12)] / G[k] - 1, GI[add_m(k, 12)] / GI[k] - 1) for k in ms75
          if add_m(k, 12) in GI and k in GI]
    neg = [(u, i) for u, i in q4 if u < 0]
    R["q4"] = {"n_12m_windows_usd_negative": len(neg),
               "share_inr_better": round(sum(i > u for u, i in neg) / len(neg), 2),
               "median_cushion_pp": round(100 * st.median(i - u for u, i in neg), 1),
               "share_inr_also_negative": round(sum(i < 0 for u, i in neg) / len(neg), 2),
               "usdinr_cagr_1975_to_last_pct": round(100 * ((INR[last_full] / INR["1975-01"]) ** (12 / mdiff("1975-01", last_full)) - 1), 2)}

    # Q5 LBMA consensus vs actual vs random walk (prior-December average)
    ann = {}
    for y in LBMA:
        ks = [k for k in G if k.startswith(str(y))]
        if ks:
            ann[y] = (sum(G[k] for k in ks) / len(ks), len(ks))
    q5 = []
    for y, f in LBMA.items():
        if y in ann:
            act, n = ann[y]
            rw = G[f"{y - 1}-12"]
            q5.append({"year": y, "consensus": f, "actual_avg": round(act, 2), "months": n, "random_walk_dec": rw,
                       "consensus_err_pct": round(100 * (f / act - 1), 1), "rw_err_pct": round(100 * (rw / act - 1), 1),
                       "consensus_better": abs(f / act - 1) < abs(rw / act - 1)})
    R["q5_lbma"] = q5
    full = [r for r in q5 if r["months"] == 12]
    R["q5_summary"] = {"n_full_years": len(full),
                       "consensus_mape": round(st.mean(abs(r["consensus_err_pct"]) for r in full), 1),
                       "rw_mape": round(st.mean(abs(r["rw_err_pct"]) for r in full), 1),
                       "consensus_better_years": sum(r["consensus_better"] for r in full)}

    # ---------------- today's state
    dk = sorted(gd)
    last_d = dk[-1]
    px = gd[last_d][0]
    ath_close_d = max(dk, key=lambda d: gd[d][0]); ath_high_d = max(dk, key=lambda d: gd[d][1] or 0)
    def back(days):
        tgt = (dt.date.fromisoformat(last_d) - dt.timedelta(days=days)).isoformat()
        d = max(x for x in dk if x <= tgt)
        return d, gd[d][0], px / gd[d][0] - 1
    spot = json.load(open(D("goldapi_xau.json")))
    ath_m = max(G, key=G.get)
    inr_d, _ = yahoo_daily(D("yahoo_inr_1d.json"))
    inr_last = max(inr_d)
    usdinr = inr_d[inr_last][0]
    gi_10g = px * usdinr / OZ_G * 10
    R["today"] = {
        "gcf_last_date": last_d, "gcf_last_close": round(px, 1),
        "spot_goldapi": spot.get("price"), "spot_goldapi_at": spot.get("updatedAt"),
        "ath_close": round(gd[ath_close_d][0], 1), "ath_close_date": ath_close_d,
        "ath_intraday": round(gd[ath_high_d][1], 1), "ath_intraday_date": ath_high_d,
        "pct_below_ath_close": round(100 * (px / gd[ath_close_d][0] - 1), 1),
        "pct_below_ath_intraday": round(100 * (px / gd[ath_high_d][1] - 1), 1),
        "recent_low_close": min((gd[d][0], d) for d in dk if d >= "2026-02-01"),
        "ath_monthly_avg": [ath_m, G[ath_m]], "pct_below_ath_monthly_avg": round(100 * (px / G[ath_m] - 1), 1),
        "chg_1m": back(30), "chg_3m": back(91), "chg_1y": back(365),
        "usdinr_yahoo": [inr_last, round(usdinr, 3)],
        "gold_inr_10g_no_duty": round(gi_10g),
        "regime_last_ff_month": [max(FF), regime(FF, max(FF))], "ff_6m_change": round(FF[max(FF)] - FF[add_m(max(FF), -6)], 2),
        "ry_last_month": [max(FII), FII[max(FII)]],
    }
    # IBJA
    try:
        s = re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", open(D("ibja_home.html"), errors="ignore").read()))
        m = re.findall(r"(\d\d/\d\d/\d{4}) (\d{6}) \d{6} \d{6}", s)
        if m:
            R["today"]["ibja_999_rows"] = m[:8]
    except OSError:
        pass

    # ---------------- analogs (pre-registered): months 1975+ with 25-45% below running ATH
    ath, athm, rows = 0, None, []
    epi = {e["peak"]: e for e in E20}
    for k in ms68:
        if G[k] >= ath:
            ath, athm = G[k], k
        if k < "1975-01":
            continue
        dd = G[k] / ath - 1
        if -0.45 <= dd <= -0.25:
            e = epi.get(athm, {})
            r = {"m": k, "ep": athm, "dd": dd, "runup_big": bool(e.get("runup_x", 0) >= 2.5 and e.get("runup_months", 99) <= 36),
                 "reg": regime(FF, k), "ry": RY.get(k)}
            for h in (7, 12, 13, 24, 25):
                kh = add_m(k, h)
                if kh in G:
                    path = [G[add_m(k, i)] for i in range(1, h + 1)]
                    r[f"f{h}"] = G[kh] / G[k] - 1
                    r[f"min{h}"] = min(path) / G[k] - 1
                    r[f"max{h}"] = max(path) / G[k] - 1
            rows.append(r)
    sets = {"a": rows, "b": [r for r in rows if r["runup_big"]],
            "c": [r for r in rows if r["reg"] == "hiking" or (r["ry"] is not None and r["ry"] >= 2)]}
    R["analogs"] = {s: {"n_months": len(v), "episodes": sorted({r["ep"] for r in v}),
                        "n_months_with_f24": sum("f24" in r for r in v)} for s, v in sets.items()}
    per_ep = {}
    for s, v in sets.items():
        for h in ("f12", "f24"):
            for ep in sorted({r["ep"] for r in v}):
                x = [r[h] for r in v if r["ep"] == ep and h in r]
                if x:
                    per_ep.setdefault(s, {}).setdefault(h, {})[ep] = {"n": len(x), "median_pct": round(100 * st.median(x), 1),
                                                                     "p_pos": round(sum(i > 0 for i in x) / len(x), 2)}
    R["analogs_per_episode"] = per_ep
    sc = {}
    for h in ("f12", "f24"):
        p, info = blend_probs(sets, h)
        meds = {}
        for name, lo, hi in BUCKETS:
            x = [r[h] for r in rows if h in r and bucket(r[h]) == name]
            meds[name] = st.median(x) if x else (lo + hi) / 2 if abs(hi) < 5 else (lo + 0.1 if name == "best" else hi - 0.1)
        sc[h] = {b: {"p": round(p[b], 3), "median_ret_pct": round(100 * meds[b], 1), "price": round(px * (1 + meds[b]))}
                 for b in p}
        sc[h]["_info"] = {k: (v if not isinstance(v, dict) else {i: round(j, 3) for i, j in v.items()}) for k, v in info.items()}
        for s in ("b", "c"):
            fx, n = freq([r for r in sets[s] if h in r], h)
            sc[h]["_info"][f"freq_{s}"] = {i: round(j, 3) for i, j in fx.items()}
            sc[h]["_info"][f"n_months_{s}"] = n
            sc[h]["_info"][f"n_ep_{s}"] = len({r["ep"] for r in sets[s] if h in r})
    R["scenarios"] = sc
    # sensitivity (NOT pre-registered; added 2026-11-28 after seeing month-pooled results): each episode weighted
    # equally instead of each month (the 1980-2006 episode supplies ~2/3 of analog months)
    def ew(rows, fn):
        g = collections.defaultdict(list)
        for r in rows:
            v = fn(r)
            if v is not None:
                g[r["ep"]].append(v)
        return {ep: sum(v) / len(v) for ep, v in g.items()}
    R["sensitivity_episode_weighted"] = {}
    for h in ("f12", "f24"):
        out = {}
        for name, lo, hi in BUCKETS:
            e = ew(rows, lambda r: (bucket(r[h]) == name) if h in r else None)
            out[name] = {"by_episode": {k: round(v, 2) for k, v in e.items()}, "mean": round(sum(e.values()) / len(e), 3)}
        R["sensitivity_episode_weighted"][h] = out

    # daily-vs-monthly-average gap (sensitivity for touch events)
    gaps_lo, gaps_hi = [], []
    for k in sorted(yavg):
        cl = [gd[d][0] for d in dk if d.startswith(k)]
        if len(cl) > 10 and k < last_full[:7]:
            gaps_lo.append(min(cl) / yavg[k] - 1); gaps_hi.append(max(cl) / yavg[k] - 1)
    glo, ghi = st.median(gaps_lo), st.median(gaps_hi)
    R["daily_vs_monthly_gap"] = {"median_min_close_vs_avg_pct": round(100 * glo, 2), "median_max_close_vs_avg_pct": round(100 * ghi, 2)}

    calls = {
        "gold-close-4000-plus-2027-06-30": ("f7", lambda r, adj=0: (r["f7"] >= 4000 / px - 1) if "f7" in r else None),
        "gold-touch-3200-or-less-by-2027-06-30": ("min7", lambda r, adj=0: (r["min7"] + adj * glo <= 3200 / px - 1) if "min7" in r else None),
        "gold-touch-3070-or-less-by-2027-12-31": ("min13", lambda r, adj=0: (r["min13"] + adj * glo <= 3070 / px - 1) if "min13" in r else None),
        "gold-close-4500-plus-2027-12-31": ("f13", lambda r, adj=0: (r["f13"] >= 4500 / px - 1) if "f13" in r else None),
        "gold-new-record-by-2028-12-31": ("max25", lambda r, adj=0: (r["max25"] + adj * ghi >= 5318 / px - 1) if "max25" in r else None),
    }
    old = {"gold-close-4000-plus-2027-06-30": 0.35, "gold-touch-3200-or-less-by-2027-06-30": 0.35,
           "gold-touch-3070-or-less-by-2027-12-31": 0.25, "gold-close-4500-plus-2027-12-31": 0.30,
           "gold-new-record-by-2028-12-31": 0.20}
    R["calls"] = {}
    for cid, (_, fn) in calls.items():
        p0, i0 = event_prob(sets, lambda r: fn(r, 0))
        p1, _ = event_prob(sets, lambda r: fn(r, 1))
        ewp = ew(rows, lambda r: fn(r, 0))
        R.setdefault("calls_episode_weighted", {})[cid] = {"by_episode": {k: round(v, 2) for k, v in ewp.items()},
                                                          "mean": round(sum(ewp.values()) / len(ewp), 3)}
        R["calls"][cid] = {"old_p": old[cid], "study_p": round(p0, 3), "study_p_daily_adj": round(p1, 3),
                           "unconditional_a": round(i0["a"], 3) if i0["a"] is not None else None,
                           "parts": [round(x, 3) for x in i0["parts"]],
                           "differs_by_0.10": abs(p0 - old[cid]) >= 0.10}

    # ---------------- L52 allocation tie (INR, real fund data from the allocation test)
    if os.path.exists(ALLOC):
        A = {r["month"]: r for r in csv.DictReader(open(ALLOC))}
        am = sorted(A)
        g = {k: float(A[k]["gold_inr_oz"]) for k in am}
        ei = episodes(g, am, 0.15)
        tie = {"inr_gold_episodes_2006_2026_15pct": [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in e.items()} for e in ei]}
        # 70/20/10 Jan reset through the worst INR gold episode: track gold sleeve, how much the resets bought
        w = {"equity": 0.7, "gold": 0.2, "bond": 0.1}
        col = {"equity": "equity_nav", "gold": "gold_inr_oz", "bond": "bond_nav"}
        val = {x: 1e6 * w[x] for x in w}; buys = []; path = [1e6]
        for i, k in enumerate(am[1:], 1):
            for x in w:
                val[x] *= float(A[k][col[x]]) / float(A[am[i - 1]][col[x]])
            V = sum(val.values())
            if k[5:] == "01":
                buys.append((k, round(V * w["gold"] - val["gold"]), round(100 * (V * w["gold"] - val["gold"]) / V, 2),
                             round(100 * val["gold"] / V, 1)))
                val = {x: V * w[x] for x in w}
            path.append(sum(val.values()))
        tie["jan_resets_gold_buy"] = [b for b in buys if b[0] >= "2012-01" and b[0] <= "2017-01"] + [b for b in buys if b[0] >= "2025-01"]
        if ei:
            worst = min(ei, key=lambda e: e["depth"])
            s, t = am.index(worst["peak"]), am.index(worst["trough"])
            tie["worst_inr_gold_episode"] = {"peak": worst["peak"], "trough": worst["trough"], "gold_depth_pct": round(100 * worst["depth"], 1),
                                             "portfolio_ret_same_window_pct": round(100 * (path[t] / path[s] - 1), 1),
                                             "equity_ret_same_window_pct": round(100 * (float(A[worst["trough"]]["equity_nav"]) / float(A[worst["peak"]]["equity_nav"]) - 1), 1)}
        # stress from target weights: gold falls further X% with equity/bonds flat; what January reset buys
        tie["stress"] = [{"gold_fall_pct": f, "portfolio_hit_pct": round(-0.2 * f, 1),
                          "jan_reset_buys_pct_of_portfolio": round(100 * (0.2 - 0.2 * (1 - f / 100) / (1 - 0.2 * f / 100)), 2)}
                         for f in (16, 25, 40, 50)]
        R["allocation_tie"] = tie

    os.makedirs(a.out, exist_ok=True)
    json.dump(R, open(os.path.join(a.out, "results.json"), "w"), indent=1, default=str)
    print(json.dumps(R, indent=1, default=str))


if __name__ == "__main__":
    main()
