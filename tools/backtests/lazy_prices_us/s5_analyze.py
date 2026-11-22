#!/usr/bin/env python3
"""Step 5: pre-registered analysis (see research_notes/Backtests/lazy_prices_us.md section 0).

Quintiles of each similarity measure are formed within filing year over ALL firm-years with a score
(before looking at price availability). Events = bottom quintile (changers, Q1) and top quintile
(non-changers, Q5) with usable prices. Each event gets 5 seeded random size-matched controls from the
same filing year, outside the event's quintile, mcap on the event's entry date within x0.6-x1.67.
Returns: adjusted close, entry = first trading day after filing date, 63/126/252 trading days;
a series that stops inside the window uses its last price (delisted).
Stats: mean, median, winsorised mean, hit rate, naive t, 95% bootstrap CI resampling filing months.
Output: results.json, results.txt
"""
import bisect, csv, json, math, os, random, sys
from collections import defaultdict
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(__file__))
from common import p

H = {"3m": 63, "6m": 126, "12m": 252}
MEASURES = ["cos_full", "jac_full", "cos_1a", "jac_1a", "cos_7", "jac_7"]
LAST_OK = "2026-11-13"
COST = 0.005


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
    if (datetime.fromisoformat(px["d"][i]) - datetime.fromisoformat(d)).days > 10: return None  # gap: not trading
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
    # month-clustered t: mean of monthly means / se across months (weighted by n)
    return {"n": n, "mean": mean, "mean_ci": [bm[lo], bm[hi]], "median": med, "median_ci": [bmed[lo], bmed[hi]],
            "hit": sum(1 for a in v if a > 0) / n, "t_naive": t,
            "wmean": sum(min(max(a, a1), a99) for a in v) / n, "months": len(keys)}


def spread(a_vals, a_m, b_vals, b_m, B=2000, seed=11):
    """mean(a) - mean(b), bootstrap resampling filing months jointly."""
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
    return {"diff": pt, "ci": [out[int(0.025 * len(out))], out[int(0.975 * len(out)) - 1]]}


def main():
    rows = [r for r in csv.DictReader(open(p("sims.tsv")), delimiter="\t") if r["status"] == "ok"]
    pxc = {}
    def px(t):
        if t not in pxc: pxc[t] = load_px(t)
        return pxc[t]
    iwm = load_px("IWM")
    # usable price info per firm-year
    for r in rows:
        r["month"] = r["fd"][:7]; r["px"] = None
        P = px(r["ticker"])
        if not P: r["pxwhy"] = "no_series"; continue
        i0 = entry(P, r["fd"])
        if i0 is None: r["pxwhy"] = "no_entry"; continue
        sh = float(r["shares"]) if r["shares"] else None
        fl = float(r["float"])
        mc = sh * unadj(P, i0) if sh else fl
        if sh and not 0.2 <= mc / fl <= 30: r["pxwhy"] = "mcap_mismatch"; continue
        r["px"] = P; r["i0"] = i0; r["mcap"] = mc; r["ret"] = rets(P, i0); r["pxwhy"] = "ok"
        j = entry(iwm, r["fd"]); r["iwm"] = rets(iwm, j) if j is not None else {}
    res = {"n_firmyears_ok": len(rows), "by_year": {}, "pxwhy": {}, "measures": {}}
    for r in rows:
        res["pxwhy"][r["pxwhy"]] = res["pxwhy"].get(r["pxwhy"], 0) + 1
    for y in ("2021", "2022", "2023"):
        res["by_year"][y] = sum(r["year"] == y for r in rows)
    usable = [r for r in rows if r["px"]]
    for meas in MEASURES:
        q = {}
        for y in ("2021", "2022", "2023"):
            xs = sorted((float(r[meas]), r["acc"]) for r in rows if r["year"] == y and r[meas])
            n = len(xs)
            for k, (v, acc) in enumerate(xs): q[acc] = 1 + (5 * k) // n
        for r in rows: r["q_" + meas] = q.get(r["acc"])
        M = {"quintile_n": {}, "groups": {}}
        rnd = random.Random(20261122)
        byyear = defaultdict(list)
        for r in usable:
            if r["q_" + meas]: byyear[r["year"]].append(r)
        for g in (1, 5):
            ev = [r for r in usable if r["q_" + meas] == g]
            out = {k: {"raw": [], "exc": [], "iwm": [], "m": []} for k in H}
            nctl = []
            for e in ev:
                pool = [c for c in byyear[e["year"]] if c["q_" + meas] != g and c["cik"] != e["cik"]]
                cands = []
                for c in pool:
                    j = entry(c["px"], e["fd"])
                    if j is None: continue
                    sh = float(c["shares"]) if c["shares"] else None
                    cm = sh * unadj(c["px"], j) if sh else float(c["float"])
                    if 0.6 <= cm / e["mcap"] <= 1.67: cands.append((c, j))
                rnd.shuffle(cands); ctl = cands[:5]; nctl.append(len(ctl))
                cr = [rets(c["px"], j) for c, j in ctl]
                for k in H:
                    v = e["ret"][k]
                    cv = [x[k] for x in cr if x[k] is not None]
                    out[k]["raw"].append(v); out[k]["m"].append(e["month"])
                    out[k]["exc"].append(v - sum(cv) / len(cv) if v is not None and cv else None)
                    iv = e["iwm"].get(k)
                    out[k]["iwm"].append(v - iv if v is not None and iv is not None else None)
            G = {"n_events": len(ev), "ctl_full5": sum(1 for x in nctl if x == 5), "ctl_none": sum(1 for x in nctl if x == 0)}
            for k in H:
                G[k] = {"vs_controls": stats(out[k]["exc"], out[k]["m"]), "vs_iwm": stats(out[k]["iwm"], out[k]["m"]),
                        "raw": stats(out[k]["raw"], out[k]["m"])}
            G["_series"] = out
            M["groups"][g] = G
        for k in H:
            a, b = M["groups"][1]["_series"][k], M["groups"][5]["_series"][k]
            M[f"spread_raw_{k}"] = spread(a["raw"], a["m"], b["raw"], b["m"])
            M[f"spread_exc_{k}"] = spread(a["exc"], a["m"], b["exc"], b["m"])
        # per-year, primary horizon
        M["by_year_12m"] = {}
        for y in ("2021", "2022", "2023"):
            s = M["groups"][1]["_series"]["12m"]
            idx = [i for i, m in enumerate(s["m"]) if m.startswith(y)]
            M["by_year_12m"][y] = stats([s["exc"][i] for i in idx], [s["m"][i] for i in idx])
        for g in (1, 5): del M["groups"][g]["_series"]
        res["measures"][meas] = M
    # decision on primary
    P = res["measures"]["cos_full"]["groups"][1]["12m"]["vs_controls"]
    edge = P.get("t_naive", 0) <= -3 or P.get("mean_ci", [0, 0])[1] < -COST
    res["primary"] = {"stat": P, "avoid_benefit_after_cost": -P["mean"] - COST,
                      "verdict": "EDGE" if edge else ("NOT PROVEN" if P["mean"] < 0 else "REJECTED/NO SIGN")}
    # survivorship tallies by primary quintile
    firms = {json.loads(l)["cik"].lstrip("0"): json.loads(l) for l in open(p("firms.jsonl"))}
    aud = defaultdict(lambda: defaultdict(int))
    for r in rows:
        qq = r.get("q_cos_full")
        if not qq: continue
        status = r["pxwhy"]
        if status == "ok":
            P_ = r["px"]; end_i = r["i0"] + 252
            if end_i < len(P_["d"]): continue
            status = "series_ends_in_window"
        f = firms.get(r["cik"].lstrip("0"), {})
        ev = [s for s in f.get("surv", []) if s["fd"] > r["fd"]]
        kind = "bankrupt(8-K 1.03)" if any(s["form"] == "8-K" for s in ev) else \
               "merger/tender" if any(s["form"] in ("DEFM14A", "PREM14A", "SC TO-T", "SC 14D9", "DEFM14C", "S-4") for s in ev) else \
               "delist/dereg" if any(s["form"].startswith(("15", "25")) for s in ev) else "unexplained"
        aud[f"Q{qq}"][f"{status}:{kind}"] += 1
        aud["all"][status] += 1
    res["survivorship"] = {k: dict(v) for k, v in aud.items()}
    json.dump(res, open(p("results.json"), "w"), indent=1, default=str)
    # text summary
    L = [f"firm-years with both docs: {len(rows)}  by year {res['by_year']}  price status {res['pxwhy']}"]
    def fmt(s):
        if "mean" not in s: return f"n={s.get('n')}"
        return (f"n={s['n']:4d} mean {s['mean']*100:+6.2f}% [{s['mean_ci'][0]*100:+6.2f},{s['mean_ci'][1]*100:+6.2f}] "
                f"med {s['median']*100:+6.2f}% w {s['wmean']*100:+6.2f}% hit {s['hit']*100:4.1f}% t {s['t_naive']:+5.2f}")
    for meas in MEASURES:
        M = res["measures"][meas]
        L.append(f"\n=== {meas} ===")
        for g in (1, 5):
            G = M["groups"][g]
            L.append(f" Q{g} events {G['n_events']} (5 controls: {G['ctl_full5']}, none: {G['ctl_none']})")
            for k in H:
                L.append(f"  {k} vs ctl {fmt(G[k]['vs_controls'])}")
                L.append(f"  {k} vs IWM {fmt(G[k]['vs_iwm'])}")
        for k in H:
            s1, s2 = M[f"spread_raw_{k}"], M[f"spread_exc_{k}"]
            L.append(f"  Q1-Q5 {k}: raw {s1['diff']*100:+.2f}% [{s1['ci'][0]*100:+.2f},{s1['ci'][1]*100:+.2f}]  "
                     f"excess {s2['diff']*100:+.2f}% [{s2['ci'][0]*100:+.2f},{s2['ci'][1]*100:+.2f}]")
        for y, s in M["by_year_12m"].items(): L.append(f"  Q1 12m vs ctl {y}: {fmt(s)}")
    L.append(f"\nPRIMARY: {res['primary']['verdict']}  avoid benefit after cost {res['primary']['avoid_benefit_after_cost']*100:+.2f}%")
    L.append(f"survivorship: {json.dumps(res['survivorship'], indent=1)}")
    open(p("results.txt"), "w").write("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
