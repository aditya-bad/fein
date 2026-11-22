#!/usr/bin/env python3
"""Step 5 (v2): pre-registered analysis — research_notes/Backtests/lazy_prices_us_v2.md section 0.

Exclusions BEFORE quintiles: primary docs < 50k chars; first 10-K after de-SPAC (despac.tsv from s6).
Quintiles of each measure within filing-year group (2024; 2025 H1) over all firm-years with a score.
H1 = jac_full Q1 (bottom, changers); H2 = jac_1a Q5 (top, stale risk factors). Decision horizon 12m.
Primary controls: same filing-year group, not the event's quintile, other CIK, mcap on the event's entry date
within x0.5-x2.0; Tier A same 2-digit SIC (>=3 -> 5 nearest in log mcap), else Tier B same 1-digit SIC, else dropped.
Secondary controls (v1 style): 5 seeded random size-only controls, x0.6-x1.67.
Stats: mean, median, winsorised mean, hit, naive t, 95% bootstrap CI resampling filing months.
Usage: python3 s5_analyze.py [--exclude-bio]   (ex-bio is a pre-registered SECONDARY cut)
Output: results_v2[_exbio].json / .txt
"""
import bisect, csv, json, math, os, random, sys
from collections import defaultdict
from datetime import datetime, timezone, date
sys.path.insert(0, os.path.dirname(__file__))
from common import p

H = {"3m": 63, "6m": 126, "12m": 252}
MEASURES = ["jac_full", "jac_1a", "cos_full", "cos_1a", "jac_7", "cos_7"]
YEARS = ("2024", "2025")
LAST_OK = "2026-11-13"
COST = 0.005
MINLEN = 50000
BIO = {"2834", "2835", "2836", "8731"}


def load_px(t):
    f = p("prices", t.replace("/", "_") + ".json")
    if not t or not os.path.exists(f): return None
    d = json.load(open(f))
    if d.get("missing"): return None
    ds, adj, cl = [], [], []
    for ts, a, c in zip(d["t"], d["adj"], d["close"]):
        if a is None or c is None or a <= 0: continue
        ds.append(datetime.fromtimestamp(ts, timezone.utc).date().isoformat()); adj.append(a); cl.append(c)
    if not ds: return None
    spl = sorted((datetime.fromtimestamp(int(k), timezone.utc).date().isoformat(), v["numerator"] / v["denominator"])
                 for k, v in (d.get("splits") or {}).items())
    return {"d": ds, "adj": adj, "close": cl, "splits": spl}


def unadj(px, i):
    f = 1.0
    for sd, r in px["splits"]:
        if sd > px["d"][i]: f *= r
    return px["close"][i] * f


def entry(px, d):
    i = bisect.bisect_right(px["d"], d)
    if i >= len(px["d"]): return None
    if (datetime.fromisoformat(px["d"][i]) - datetime.fromisoformat(d)).days > 10: return None
    return i


def rets(px, i0):
    out = {}
    for k, h in H.items():
        j = i0 + h
        if j < len(px["d"]): out[k] = px["adj"][j] / px["adj"][i0] - 1
        elif px["d"][-1] < LAST_OK: out[k] = px["adj"][-1] / px["adj"][i0] - 1
        else: out[k] = None
    return out


def stats(vals, months, B=2000, seed=7):
    xs = [(v, m) for v, m in zip(vals, months) if v is not None]
    n = len(xs)
    if n < 5: return {"n": n}
    v = [a for a, _ in xs]
    mean = sum(v) / n; s = sorted(v); med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    sd = math.sqrt(sum((a - mean) ** 2 for a in v) / (n - 1)); t = mean / (sd / math.sqrt(n)) if sd else 0
    byM = defaultdict(list)
    for a, m in xs: byM[m].append(a)
    keys = sorted(byM); rnd = random.Random(seed); bm, bmed = [], []
    for _ in range(B):
        smp = []
        for _ in keys: smp += byM[rnd.choice(keys)]
        bm.append(sum(smp) / len(smp)); ss = sorted(smp); bmed.append(ss[len(ss) // 2])
    bm.sort(); bmed.sort(); lo, hi = int(0.025 * B), int(0.975 * B) - 1
    a1, a99 = s[int(0.01 * (n - 1))], s[int(0.99 * (n - 1))]
    return {"n": n, "mean": mean, "mean_ci": [bm[lo], bm[hi]], "median": med, "median_ci": [bmed[lo], bmed[hi]],
            "hit": sum(1 for a in v if a > 0) / n, "t_naive": t,
            "wmean": sum(min(max(a, a1), a99) for a in v) / n, "months": len(keys),
            "month_n": {k: len(byM[k]) for k in keys}}


def spread(a_vals, a_m, b_vals, b_m, B=2000, seed=11):
    A, Bv = defaultdict(list), defaultdict(list)
    for v, m in zip(a_vals, a_m):
        if v is not None: A[m].append(v)
    for v, m in zip(b_vals, b_m):
        if v is not None: Bv[m].append(v)
    keys = sorted(set(A) | set(Bv)); rnd = random.Random(seed); out = []
    def d(ks):
        a = [x for k in ks for x in A.get(k, [])]; b = [x for k in ks for x in Bv.get(k, [])]
        return (sum(a) / len(a) - sum(b) / len(b)) if a and b else None
    pt = d(keys)
    for _ in range(B):
        r = d([rnd.choice(keys) for _ in keys])
        if r is not None: out.append(r)
    out.sort()
    return {"diff": pt, "ci": [out[int(0.025 * len(out))], out[int(0.975 * len(out)) - 1]]} if out else {"diff": pt}


def verdict(s):
    if "mean" not in s: return "NO DATA"
    edge = s["t_naive"] <= -3 or s["mean_ci"][1] < -COST
    return "PROVEN AVOID FLAG" if edge else ("NOT PROVEN" if s["mean"] < 0 else "REJECTED / NO SIGN")


def surv_kind(firm, fd, days=None):
    ev = [s for s in firm.get("surv", []) if s["fd"] > fd and
          (days is None or (date.fromisoformat(s["fd"]) - date.fromisoformat(fd)).days <= days)]
    if any(s["form"] == "8-K" for s in ev): return "bankrupt"
    if any(s["form"] in ("DEFM14A", "PREM14A", "SC TO-T", "SC 14D9", "DEFM14C", "S-4") for s in ev): return "merger"
    if any(s["form"].startswith(("15", "25")) for s in ev): return "delist"
    return "unexplained"


def main():
    allrows = [r for r in csv.DictReader(open(p("sims.tsv")), delimiter="\t") if r["status"] == "ok"]
    rows = [r for r in allrows if int(r["len"]) >= MINLEN and int(r["prev_len"]) >= MINLEN]
    n_short = len(allrows) - len(rows)
    ds = {r["acc"] for r in csv.DictReader(open(p("despac.tsv")), delimiter="\t") if r["despac"] == "1"}
    n_spac = sum(r["acc"] in ds for r in rows)
    rows = [r for r in rows if r["acc"] not in ds]
    EXBIO = "--exclude-bio" in sys.argv
    if EXBIO:
        rows = [r for r in rows if r["sic"] not in BIO]
    tag = "_exbio" if EXBIO else ""
    old = {}
    if os.path.exists(p("old_tickers.tsv")):
        old = {r["acc"]: r["symbol"] for r in csv.DictReader(open(p("old_tickers.tsv")), delimiter="\t") if r["symbol"]}
    for r in rows:
        r["recovered"] = ""
        if not r["ticker"] and r["acc"] in old:
            r["ticker"] = old[r["acc"]]; r["recovered"] = "1"
        r["grp"] = r["fd"][:4]
    pxc = {}
    def px(t):
        if t not in pxc: pxc[t] = load_px(t)
        return pxc[t]
    iwm = load_px("IWM")
    for r in rows:
        r["month"] = r["fd"][:7]; r["px"] = None
        P = px(r["ticker"])
        if not P: r["pxwhy"] = "no_ticker" if not r["ticker"] else "no_series"; continue
        i0 = entry(P, r["fd"])
        if i0 is None: r["pxwhy"] = "no_entry"; continue
        sh = float(r["shares"]) if r["shares"] else None
        fl = float(r["float"])
        mc = sh * unadj(P, i0) if sh else fl
        if sh and not 0.2 <= mc / fl <= 30: r["pxwhy"] = "mcap_mismatch"; continue
        r["px"] = P; r["i0"] = i0; r["mcap"] = mc; r["ret"] = rets(P, i0); r["pxwhy"] = "ok"
        j = entry(iwm, r["fd"]); r["iwm"] = rets(iwm, j) if j is not None else {}
    res = {"n_scored_all": len(allrows), "n_short_excluded": n_short, "n_despac_excluded": n_spac,
           "n_firmyears": len(rows), "by_group": {y: sum(r["grp"] == y for r in rows) for y in YEARS},
           "pxwhy": {}, "measures": {}}
    for r in rows:
        k_ = r["pxwhy"] + ("(recovered ticker)" if r["recovered"] else "")
        res["pxwhy"][k_] = res["pxwhy"].get(k_, 0) + 1
    usable = [r for r in rows if r["px"]]
    firms = {json.loads(l)["cik"].lstrip("0"): json.loads(l) for l in open(p("firms.jsonl"))}
    mcap_cache = {}
    def cmcap(c, fd):
        key = (c["acc"], fd)
        if key not in mcap_cache:
            j = entry(c["px"], fd)
            if j is None: mcap_cache[key] = None
            else:
                sh = float(c["shares"]) if c["shares"] else None
                mcap_cache[key] = (j, sh * unadj(c["px"], j) if sh else float(c["float"]))
        return mcap_cache[key]
    for meas in MEASURES:
        q = {}
        for y in YEARS:
            xs = sorted((float(r[meas]), r["acc"]) for r in rows if r["grp"] == y and r[meas])
            n = len(xs)
            for k, (v, acc) in enumerate(xs): q[acc] = 1 + (5 * k) // n
        for r in rows: r["q_" + meas] = q.get(r["acc"])
        M = {"quintile_n": {g: sum(1 for r in rows if r["q_" + meas] == g) for g in range(1, 6)}, "groups": {}}
        rnd = random.Random(20261122)
        bygrp = defaultdict(list)
        for r in usable:
            if r["q_" + meas]: bygrp[r["grp"]].append(r)
        for g in (1, 5):
            ev = [r for r in usable if r["q_" + meas] == g]
            out = {k: {"sec": [], "size": [], "iwm": [], "raw": [], "ctlraw": [], "m": []} for k in H}
            tiers = defaultdict(int); nsz = []
            for e in ev:
                pool = [c for c in bygrp[e["grp"]] if c["q_" + meas] != g and c["cik"] != e["cik"]]
                band, size_c = [], []
                for c in pool:
                    x = cmcap(c, e["fd"])
                    if x is None: continue
                    j, cm = x; ratio = cm / e["mcap"]
                    if 0.5 <= ratio <= 2.0: band.append((abs(math.log(ratio)), c, j))
                    if 0.6 <= ratio <= 1.67: size_c.append((c, j))
                A = sorted([b for b in band if b[1]["sic"][:2] == e["sic"][:2]], key=lambda b: (b[0], b[1]["acc"]))
                if len(A) >= 3: ctl = A[:5]; tiers["A_2digit"] += 1
                else:
                    Bt = sorted([b for b in band if b[1]["sic"][:1] == e["sic"][:1]], key=lambda b: (b[0], b[1]["acc"]))
                    if len(Bt) >= 3: ctl = Bt[:5]; tiers["B_1digit"] += 1
                    else: ctl = []; tiers["none"] += 1
                size_c.sort(key=lambda x: x[0]["acc"]); rnd.shuffle(size_c); sz = size_c[:5]; nsz.append(len(sz))
                cr = [rets(c["px"], j) for _, c, j in ctl]
                sr = [rets(c["px"], j) for c, j in sz]
                for k in H:
                    v = e["ret"][k]
                    cv = [x[k] for x in cr if x[k] is not None]
                    sv = [x[k] for x in sr if x[k] is not None]
                    out[k]["raw"].append(v); out[k]["m"].append(e["month"])
                    out[k]["sec"].append(v - sum(cv) / len(cv) if v is not None and cv else None)
                    out[k]["ctlraw"].append(sum(cv) / len(cv) if v is not None and cv else None)
                    out[k]["size"].append(v - sum(sv) / len(sv) if v is not None and sv else None)
                    iv = e["iwm"].get(k)
                    out[k]["iwm"].append(v - iv if v is not None and iv is not None else None)
            G = {"n_events": len(ev), "tiers": dict(tiers), "size_ctl_full5": sum(1 for x in nsz if x == 5)}
            for k in H:
                G[k] = {"vs_sector_size": stats(out[k]["sec"], out[k]["m"]), "vs_size_only": stats(out[k]["size"], out[k]["m"]),
                        "vs_iwm": stats(out[k]["iwm"], out[k]["m"]), "raw": stats(out[k]["raw"], out[k]["m"])}
            s12 = out["12m"]
            G["by_group_12m"] = {y: stats([s12["sec"][i] for i, m in enumerate(s12["m"]) if m.startswith(y)],
                                          [m for m in s12["m"] if m.startswith(y)]) for y in YEARS}
            # biotech share among events
            G["bio_share"] = sum(1 for r in ev if r["sic"] in BIO) / len(ev) if ev else None
            cr12 = [x for x in s12["ctlraw"] if x is not None]
            G["ctl_raw_mean_12m"] = sum(cr12) / len(cr12) if cr12 else None
            G["_series"] = out
            M["groups"][g] = G
        for k in H:
            a, b = M["groups"][1]["_series"][k], M["groups"][5]["_series"][k]
            M[f"spread_raw_{k}"] = spread(a["raw"], a["m"], b["raw"], b["m"])
            M[f"spread_sec_{k}"] = spread(a["sec"], a["m"], b["sec"], b["m"])
        # survivorship audit + bound
        aud = defaultdict(lambda: defaultdict(int))
        imp_all = []  # imputed raw for every missing scored firm-year (universe)
        n_scored = 0
        miss_by_q = defaultdict(list)
        for r in rows:
            qq = r["q_" + meas]
            if not qq: continue
            n_scored += 1
            f = firms.get(r["cik"].lstrip("0"), {})
            if r["pxwhy"] == "ok":
                if r["i0"] + 252 < len(r["px"]["d"]): continue
                aud[f"Q{qq}"]["series_ends_in_window:" + surv_kind(f, r["fd"])] += 1
                continue
            kind = surv_kind(f, r["fd"]); kind365 = surv_kind(f, r["fd"], 365)
            aud[f"Q{qq}"][f"{r['pxwhy']}:{kind}"] += 1
            aud[f"Q{qq}"]["_missing"] += 1
            miss_by_q[qq].append(kind365); imp_all.append(kind365)
        aud = {k: dict(v) for k, v in aud.items()}
        M["survivorship"] = aud
        def bound(g, imp):
            G = M["groups"][g]; s = G["12m"]["vs_sector_size"]
            if "mean" not in s or G["ctl_raw_mean_12m"] is None: return None
            ctl = G["ctl_raw_mean_12m"]
            qn = M["quintile_n"][g]; mg = len(miss_by_q[g]) / qn if qn else 0
            img = sum(imp[k] for k in miss_by_q[g]) / len(miss_by_q[g]) if miss_by_q[g] else 0
            mu = len(imp_all) / n_scored if n_scored else 0
            imu = sum(imp[k] for k in imp_all) / len(imp_all) if imp_all else 0
            ev_full = (1 - mg) * (s["mean"] + ctl) + mg * img
            ctl_full = (1 - mu) * ctl + mu * imu
            return {"bound": ev_full - ctl_full, "miss_share_group": mg, "miss_share_univ": mu,
                    "kinds_group": {k: miss_by_q[g].count(k) for k in set(miss_by_q[g])}}
        base = {"bankrupt": -0.8, "merger": 0.25, "delist": 0.0, "unexplained": 0.0}
        M["surv_bound"] = {g: {"pre-registered (bk -80%, merger +25%, other 0)": bound(g, base),
                               "bankrupt at 0": bound(g, dict(base, bankrupt=0.0))} for g in (1, 5)}
        for g in (1, 5): del M["groups"][g]["_series"]
        res["measures"][meas] = M
    h1 = res["measures"]["jac_full"]["groups"][1]["12m"]["vs_sector_size"]
    h2 = res["measures"]["jac_1a"]["groups"][5]["12m"]["vs_sector_size"]
    res["H1"] = {"stat": h1, "verdict": verdict(h1), "avoid_benefit_after_cost": -h1["mean"] - COST if "mean" in h1 else None}
    res["H2"] = {"stat": h2, "verdict": verdict(h2), "avoid_benefit_after_cost": -h2["mean"] - COST if "mean" in h2 else None}
    json.dump(res, open(p(f"results_v2{tag}.json"), "w"), indent=1, default=str)
    L = [f"scored {len(allrows)}; short excl {n_short}; de-SPAC excl {n_spac}; analysed {len(rows)} {res['by_group']}",
         f"price status {res['pxwhy']}"]
    def fmt(s):
        if "mean" not in s: return f"n={s.get('n')}"
        return (f"n={s['n']:4d} mean {s['mean']*100:+6.2f}% [{s['mean_ci'][0]*100:+6.2f},{s['mean_ci'][1]*100:+6.2f}] "
                f"med {s['median']*100:+6.2f}% w {s['wmean']*100:+6.2f}% hit {s['hit']*100:4.1f}% t {s['t_naive']:+5.2f} months {s['months']}")
    for meas in MEASURES:
        M = res["measures"][meas]
        L.append(f"\n=== {meas} === quintile n {M['quintile_n']}")
        for g in (1, 5):
            G = M["groups"][g]
            L.append(f" Q{g} events {G['n_events']} tiers {G['tiers']} bio share {G['bio_share']:.2f} ctl raw 12m {G['ctl_raw_mean_12m']}")
            for k in H:
                L.append(f"  {k} vs sector-size {fmt(G[k]['vs_sector_size'])}")
            L.append(f"  12m vs size-only  {fmt(G['12m']['vs_size_only'])}")
            L.append(f"  12m vs IWM        {fmt(G['12m']['vs_iwm'])}")
            L.append(f"  12m raw           {fmt(G['12m']['raw'])}")
            for y, s in G["by_group_12m"].items(): L.append(f"  12m sector-size {y}: {fmt(s)}")
            b = M["surv_bound"][g]
            L.append(f"  surv bound: {json.dumps(b, default=str)}")
        for k in H:
            s1, s2 = M[f"spread_raw_{k}"], M[f"spread_sec_{k}"]
            L.append(f"  Q1-Q5 {k}: raw {s1['diff']*100:+.2f}% [{s1['ci'][0]*100:+.2f},{s1['ci'][1]*100:+.2f}]  "
                     f"sector-size excess {s2['diff']*100:+.2f}% [{s2['ci'][0]*100:+.2f},{s2['ci'][1]*100:+.2f}]")
        L.append(f"  survivorship: {json.dumps(M['survivorship'])}")
    for h in ("H1", "H2"):
        L.append(f"\n{h}: {res[h]['verdict']}  {fmt(res[h]['stat'])}  avoid benefit after cost "
                 f"{res[h]['avoid_benefit_after_cost']*100:+.2f}%")
    open(p(f"results_v2{tag}.txt"), "w").write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
