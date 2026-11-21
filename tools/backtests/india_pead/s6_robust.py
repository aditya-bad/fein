#!/usr/bin/env python3
"""Step 6 (EXPLORATORY, written after the pre-registered run): robustness of the PEAD result.
- quintile ladder Q1..Q5 (63d excess vs size-matched controls), per period
- T-B and top-vs-controls with returns winsorised at 1%/99% (per period), and with per-quarter MEDIANS
- per-quarter test T-B (63d) list; net-of-cost long-only (top vs ctrl minus 0.5% / 1.0%)
- non-overlapping check: every other quarter only (126d horizons overlap adjacent quarters)
- liquidity-style split: entry price < Rs 100 vs >= 100; financials excluded is not possible (no sector field)
Usage: python3 s6_robust.py OUTDIR -> OUTDIR/robust.json"""
import collections, json, math, os, random, statistics as st, sys

S = sys.argv[1]
rows, hdr = [], None
for line in open(os.path.join(S, "events.tsv")):
    p = line.rstrip("\n").split("\t")
    if hdr is None: hdr = p; continue
    r = dict(zip(hdr, p))
    for k in hdr:
        if k not in ("sym", "qe", "event", "entry", "src", "ev_src"):
            r[k] = float(r[k]) if r[k] != "" else None
    r["period"] = "train" if r["event"][:4] <= "2021" else "test"
    rows.append(r)


def boot(v, n=5000, seed=1):
    rnd = random.Random(seed); m = len(v)
    b = sorted(sum(rnd.choice(v) for _ in range(m)) / m for _ in range(n))
    return b[int(.025 * n)], b[int(.975 * n) - 1]


def summ(v):
    v = [x for x in v if x is not None]
    if len(v) < 3: return {"n_q": len(v)}
    m = sum(v) / len(v); sd = st.stdev(v); lo, hi = boot(v)
    return {"n_q": len(v), "mean": m, "t": m / (sd / math.sqrt(len(v))), "lo": lo, "hi": hi}


def quint(rs, key="sue_eps", nb=5):
    by = collections.defaultdict(list)
    for r in rs:
        if r[key] is not None: by[r["qe"]].append(r)
    out = {}
    for qe, g in by.items():
        if len(g) < 25: continue
        g.sort(key=lambda r: r[key]); n = len(g)
        out[qe] = [(r, min(nb - 1, int(i * nb / n))) for i, r in enumerate(g)]
    return out


def agg(xs, how):
    xs = [x for x in xs if x is not None]
    if not xs: return None
    return st.median(xs) if how == "median" else sum(xs) / len(xs)


OUT = {}
for per in ("train", "test"):
    rs = [r for r in rows if r["period"] == per]
    # winsorise per period
    lim = {}
    for h in (21, 63, 126):
        v = sorted(r[f"r{h}"] for r in rs if r[f"r{h}"] is not None)
        lim[h] = (v[int(.01 * len(v))], v[int(.99 * len(v)) - 1])
    G = quint(rs); o = {}
    # ladder
    lad = {}
    for b in range(5):
        lad[f"Q{b+1}"] = summ([agg([r["r63"] - r["c63"] for r, bb in g if bb == b and r["c63"] is not None], "mean")
                              for g in G.values()])
    o["ladder_x63"] = lad
    for how in ("mean", "median", "wins"):
        d = {}
        for h in (21, 63, 126):
            lo, hi = lim[h]
            f = (lambda x: min(hi, max(lo, x))) if how == "wins" else (lambda x: x)
            a = "median" if how == "median" else "mean"
            tb, tc = [], []
            for g in G.values():
                t = agg([f(r[f"r{h}"]) for r, b in g if b == 4 and r[f"r{h}"] is not None], a)
                bo = agg([f(r[f"r{h}"]) for r, b in g if b == 0 and r[f"r{h}"] is not None], a)
                if t is not None and bo is not None: tb.append(t - bo)
                x = agg([f(r[f"r{h}"]) - r[f"c{h}"] for r, b in g if b == 4 and r[f"r{h}"] is not None and r[f"c{h}"] is not None], a)
                if x is not None: tc.append(x)
            d[f"h{h}"] = {"TB": summ(tb), "top_vs_ctrl": summ(tc),
                          "top_vs_ctrl_net0.5": summ([x - .005 for x in tc]),
                          "top_vs_ctrl_net1.0": summ([x - .01 for x in tc])}
        o[how] = d
    # per-quarter list (63d)
    pq = {}
    for qe, g in sorted(G.items()):
        t = agg([r["r63"] for r, b in g if b == 4], "mean"); bo = agg([r["r63"] for r, b in g if b == 0], "mean")
        x = agg([r["r63"] - r["c63"] for r, b in g if b == 4 and r["c63"] is not None], "mean")
        pq[qe] = {"n": len(g), "n_top": sum(1 for _, b in g if b == 4), "TB63": t - bo, "top_x63": x}
    o["per_quarter"] = pq
    qs = sorted(pq); o["alt_quarters_TB126"] = {
        "even": summ([agg([r["r126"] for r, b in G[q] if b == 4], "mean") - agg([r["r126"] for r, b in G[q] if b == 0], "mean") for q in qs[0::2]]),
        "odd": summ([agg([r["r126"] for r, b in G[q] if b == 4], "mean") - agg([r["r126"] for r, b in G[q] if b == 0], "mean") for q in qs[1::2]])}
    # price-level split (exploratory proxy for liquidity/penny-ness): entry close from mcap not available -> use mcap < 1000 cr
    for lbl, cond in (("mcap_lt_1000", lambda r: r["mcap_cr"] < 1000), ("mcap_ge_1000", lambda r: r["mcap_cr"] >= 1000)):
        G2 = quint([r for r in rs if cond(r)])
        o[lbl] = {"n_q": len(G2), "top_vs_ctrl63": summ([agg([r["r63"] - r["c63"] for r, b in g if b == 4 and r["c63"] is not None], "mean") for g in G2.values()]),
                  "TB63": summ([agg([r["r63"] for r, b in g if b == 4], "mean") - agg([r["r63"] for r, b in g if b == 0], "mean") for g in G2.values()])}
    # top quintile also has positive announcement reaction? split top by ann_ret sign (exploratory)
    for lbl, cond in (("top_ann_up", lambda r: r["ann_ret"] > 0), ("top_ann_down", lambda r: r["ann_ret"] <= 0)):
        o[lbl] = summ([agg([r["r63"] - r["c63"] for r, b in g if b == 4 and cond(r) and r["c63"] is not None], "mean") for g in G.values()])
    OUT[per] = o
json.dump(OUT, open(os.path.join(S, "robust.json"), "w"), indent=1)


def fmt(s):
    if "mean" not in s: return f"nq={s.get('n_q')}"
    return f"{s['mean']*100:+.2f}% [{s['lo']*100:+.2f}, {s['hi']*100:+.2f}] t={s['t']:.2f} nq={s['n_q']}"


for per, o in OUT.items():
    print(f"\n===== {per}")
    for k, v in o["ladder_x63"].items(): print(" ladder", k, fmt(v))
    for how in ("mean", "median", "wins"):
        for h in (21, 63, 126):
            for k, v in o[how][f"h{h}"].items(): print(f" {how:6s} h{h} {k:18s}", fmt(v))
    print(" alt quarters 126:", {k: fmt(v) for k, v in o["alt_quarters_TB126"].items()})
    for k in ("mcap_lt_1000", "mcap_ge_1000"): print(" ", k, "TB63", fmt(o[k]["TB63"]), "| top_x63", fmt(o[k]["top_vs_ctrl63"]))
    for k in ("top_ann_up", "top_ann_down"): print(" ", k, fmt(o[k]))
    print(" per-quarter:", {q: (v["n"], v["n_top"], round(v["TB63"] * 100, 1), round(v["top_x63"] * 100, 1)) for q, v in o["per_quarter"].items()})
