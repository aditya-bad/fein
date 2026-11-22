#!/usr/bin/env python3
"""Step 5: pre-registered analysis (india_pead_survivorship.md). Inference as v1 s5_analyze.py (functions boot/summ/
groups copied unchanged): fiscal-quarter cross-sections, SUE quintiles within quarter (>= 25 events), mean of quarterly
portfolio means, t across quarters, 95% bootstrap over quarters (5,000, seed 1). Bias = ALL - LIVE per quarter (paired).
Usage: python3 s5_analyze.py -> $REPORT_OUT/results.json, tables.md"""
import collections, json, math, os, random, statistics as st, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

TXT = ("sym", "u", "cls", "qe", "event", "entry", "ev_src", "src")


def read(fn):
    rows, hdr = [], None
    for line in open(fn):
        p = line.rstrip("\n").split("\t")
        if hdr is None: hdr = p; continue
        r = dict(zip(hdr, p))
        for k in hdr:
            if k not in TXT: r[k] = float(r[k]) if r[k] != "" else None
        rows.append(r)
    return rows


def boot(vals, n=5000, seed=1):
    rnd = random.Random(seed); m = len(vals)
    if m < 3: return (None, None)
    bs = sorted(sum(rnd.choice(vals) for _ in range(m)) / m for _ in range(n))
    return (bs[int(0.025 * n)], bs[int(0.975 * n) - 1])


def summ(vals):
    vals = [v for v in vals if v is not None]
    if len(vals) < 3: return {"n_q": len(vals)}
    m = sum(vals) / len(vals); sd = st.stdev(vals)
    lo, hi = boot(vals)
    return {"n_q": len(vals), "mean": m, "t": m / (sd / math.sqrt(len(vals))) if sd > 0 else None, "lo": lo, "hi": hi}


def groups(rs, key, nb, minn):
    by = collections.defaultdict(list)
    for r in rs:
        if r.get(key) is not None: by[r["qe"]].append(r)
    out = {}
    for qe, g in by.items():
        if len(g) < minn: continue
        g = sorted(g, key=lambda r: r[key])
        n = len(g)
        out[qe] = [(r, min(nb - 1, int(i * nb / n))) for i, r in enumerate(g)]
    return out


def mean(x):
    x = [v for v in x if v is not None]
    return sum(x) / len(x) if x else None


def per_quarter(rs, rk, ck, period=None):
    """{qe: {'bot','top','tb','all', 'n', 'n_bot'}} using returns rk+h and controls ck+h."""
    if period == "train": rs = [r for r in rs if r["event"][:4] <= "2021"]
    if period == "test": rs = [r for r in rs if r["event"][:4] >= "2022"]
    G = groups(rs, "sue", 5, 25)
    out = {}
    for qe, g in G.items():
        x = lambda b: mean(r[rk] - r[ck] for r, bb in g if bb == b and r.get(rk) is not None and r.get(ck) is not None)
        raw = lambda b: mean(r[rk] for r, bb in g if bb == b and r.get(rk) is not None)
        t, bo = raw(4), raw(0)
        out[qe] = {"bot": x(0), "q2": x(1), "q3": x(2), "q4": x(3), "top": x(4),
                   "tb": (t - bo) if t is not None and bo is not None else None,
                   "all": mean(r[rk] - r[ck] for r, _ in g if r.get(rk) is not None and r.get(ck) is not None),
                   "n": len(g), "n_missing": sum(r.get("u") == "M" for r, _ in g),
                   "n_missing_bot": sum(r.get("u") == "M" for r, b in g if b == 0),
                   "n_missing_top": sum(r.get("u") == "M" for r, b in g if b == 4)}
    return out


def table(pq):
    res = {k: summ([v[k] for v in pq.values()]) for k in ("bot", "q2", "q3", "q4", "top", "tb", "all")}
    res["top_net1"] = summ([v["top"] - 0.01 for v in pq.values() if v["top"] is not None])
    res["n_events"] = sum(v["n"] for v in pq.values()); res["n_quarters"] = len(pq)
    res["n_missing"] = sum(v["n_missing"] for v in pq.values())
    res["n_missing_bot"] = sum(v["n_missing_bot"] for v in pq.values())
    res["n_missing_top"] = sum(v["n_missing_top"] for v in pq.values())
    return res


def paired(pa, pl, k):
    return summ([pa[q][k] - pl[q][k] for q in pa if q in pl and pa[q][k] is not None and pl[q][k] is not None])


ev = read(os.path.join(K.OUT, "events_w.tsv"))
live = [r for r in ev if r["u"] == "L"]
R = {}
for h in (4, 13, 26):
    for per in ("full", "train", "test"):
        p = None if per == "full" else per
        pA = per_quarter(ev, f"r{h}", f"cA{h}", p)
        pL = per_quarter(live, f"r{h}", f"cL{h}", p)
        pP = per_quarter(ev, f"rP{h}", f"cP{h}", p)                     # S1 delisting penalty
        evS = [r for r in ev if not r.get(f"early{h}")]
        pS = per_quarter(evS, f"r{h}", f"cS{h}", p)                     # S2 survivors-style
        evD = [r for r in ev if r["cls"] != "offser"]
        pD = per_quarter(evD, f"r{h}", f"cA{h}", p)                     # S3 without off-series firms
        key = f"w{h}_{per}"
        R[key] = {"ALL": table(pA), "LIVE": table(pL), "S1_penalty": table(pP), "S2_survivors_style": table(pS),
                  "S3_no_offseries": table(pD),
                  "bias_ALL_minus_LIVE": {k: paired(pA, pL, k) for k in ("bot", "top", "tb", "all")},
                  "bias_S1_minus_LIVE": {k: paired(pP, pL, k) for k in ("bot", "top", "tb")},
                  "ALL_minus_S2": {k: paired(pA, pS, k) for k in ("bot", "top", "tb")}}
# calibration: v1 published daily events (63d) with the same functions, full/train/test
v1 = read(os.path.join(K.V1, "events.tsv"))
for r in v1: r["sue"] = r["sue_eps"]
for per in ("full", "train", "test"):
    R[f"v1_daily63_{per}"] = table(per_quarter(v1, "r63", "c63", None if per == "full" else per))
# descriptive: MISSING events by quintile (event level, ALL universe, 13w)
G = groups(ev, "sue", 5, 25)
desc = collections.defaultdict(lambda: {"n": 0, "x": [], "early": 0, "distress": 0})
for qe, g in G.items():
    for r, b in g:
        if r["u"] != "M" or r.get("r13") is None or r.get("cA13") is None: continue
        d = desc[f"Q{b+1}"]; d["n"] += 1; d["x"].append(r["r13"] - r["cA13"]); d["early"] += int(r.get("early13") or 0)
        d["distress"] += int(r["distress"] or 0)
R["missing_by_quintile_w13"] = {k: {"n": v["n"], "mean_excess": mean(v["x"]),
                                    "median_excess": st.median(v["x"]) if v["x"] else None,
                                    "ended_in_window": v["early"], "distress_listed": v["distress"]}
                                for k, v in sorted(desc.items())}
os.makedirs(K.REPORT_OUT, exist_ok=True)
json.dump(R, open(os.path.join(K.REPORT_OUT, "results.json"), "w"), indent=1)

f = lambda s: "–" if not s or s.get("mean") is None else \
    f"{100*s['mean']:+.2f}% [{100*s['lo']:+.2f}, {100*s['hi']:+.2f}] t {s['t']:.2f}" if s.get("t") is not None else f"{100*s['mean']:+.2f}%"
L = ["# PEAD survivorship check — tables (auto-generated by s5_analyze.py)", ""]
for key in [k for k in R if k.startswith("w")]:
    L += [f"## {key} (weeks_period)", "", "| universe | events (missing) | quarters | bottom vs ctrl | top vs ctrl | top net 1% | T−B raw | all vs ctrl |", "|---|---|---|---|---|---|---|---|"]
    for u in ("ALL", "LIVE", "S1_penalty", "S2_survivors_style", "S3_no_offseries"):
        t = R[key][u]
        L.append(f"| {u} | {t['n_events']} ({t['n_missing']}; bot {t['n_missing_bot']}, top {t['n_missing_top']}) | {t['n_quarters']} | {f(t['bot'])} | {f(t['top'])} | {f(t['top_net1'])} | {f(t['tb'])} | {f(t['all'])} |")
    for b in ("bias_ALL_minus_LIVE", "bias_S1_minus_LIVE", "ALL_minus_S2"):
        L.append(f"| {b} | | | {f(R[key][b]['bot'])} | {f(R[key][b]['top'])} | | {f(R[key][b]['tb'])} | {f(R[key][b].get('all'))} |")
    L.append("")
L += ["## v1 published daily events, 63 trading days (calibration)", "", "| period | events | bottom | top | top net 1% | T−B |", "|---|---|---|---|---|---|"]
for per in ("full", "train", "test"):
    t = R[f"v1_daily63_{per}"]
    L.append(f"| {per} | {t['n_events']} | {f(t['bot'])} | {f(t['top'])} | {f(t['top_net1'])} | {f(t['tb'])} |")
L += ["", "## MISSING events by quintile (ALL, 13 weeks, event level)", "", "| quintile | n | mean excess | median | ended in window | distress-listed |", "|---|---|---|---|---|---|"]
for k, v in R["missing_by_quintile_w13"].items():
    L.append(f"| {k} | {v['n']} | {100*v['mean_excess']:+.2f}% | {100*v['median_excess']:+.2f}% | {v['ended_in_window']} | {v['distress_listed']} |")
open(os.path.join(K.REPORT_OUT, "tables.md"), "w").write("\n".join(L) + "\n")
print("\n".join(L))
