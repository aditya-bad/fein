#!/usr/bin/env python3
"""Step 5: pre-registered PEAD analysis on OUTDIR/events.tsv.
Unit of inference = fiscal-quarter cross-section (qe). Quintiles of SUE within each cross-section
(>= 25 events; deciles need >= 50). T-B = mean(top) - mean(bottom) per quarter. Excess vs size-matched
controls = r - c. Mean across quarters, naive t across quarters, 95% bootstrap CI resampling quarters (5,000).
Periods by event date: train 2018-2021, test 2022-2025.
Usage: python3 s5_analyze.py OUTDIR  -> OUTDIR/results.json, prints tables."""
import collections, json, math, os, random, statistics as st, sys

S = sys.argv[1]
rows = []
hdr = None
for line in open(os.path.join(S, "events.tsv")):
    p = line.rstrip("\n").split("\t")
    if hdr is None: hdr = p; continue
    r = dict(zip(hdr, p))
    for k in hdr:
        if k in ("sym", "qe", "event", "entry", "src", "ev_src"): continue
        r[k] = float(r[k]) if r[k] != "" else None
    r["period"] = "train" if r["event"][:4] <= "2021" else "test"
    rows.append(r)
H = (21, 63, 126)
OUT = {}


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
    """per cross-section qe: assign bucket 0..nb-1 by rank of key."""
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


def analyse(rs, key="sue_eps", nb=5, minn=25, ret="r"):
    G = groups(rs, key, nb, minn)
    res = {"n_events": sum(len(g) for g in G.values()), "n_quarters": len(G)}
    for h in H:
        tb, tc, bc, mc, ann = [], [], [], [], []
        for qe, g in G.items():
            top = [r for r, b in g if b == nb - 1]; bot = [r for r, b in g if b == 0]
            mt, mb = mean(r[f"{ret}{h}"] for r in top), mean(r[f"{ret}{h}"] for r in bot)
            if mt is not None and mb is not None: tb.append(mt - mb)
            xt = mean(r[f"{ret}{h}"] - r[f"c{h}"] for r in top if r[f"{ret}{h}"] is not None and r[f"c{h}"] is not None)
            xb = mean(r[f"{ret}{h}"] - r[f"c{h}"] for r in bot if r[f"{ret}{h}"] is not None and r[f"c{h}"] is not None)
            if xt is not None: tc.append(xt)
            if xb is not None: bc.append(xb)
            xa = mean(r[f"{ret}{h}"] - r[f"c{h}"] for r, b in g if r[f"{ret}{h}"] is not None and r[f"c{h}"] is not None)
            if xa is not None: mc.append(xa)
        res[f"h{h}"] = {"TB": summ(tb), "top_vs_ctrl": summ(tc), "bot_vs_ctrl": summ(bc), "all_vs_ctrl": summ(mc)}
    # announcement reaction (sanity: SUE should be priced on day 0/1)
    ta, ba = [], []
    for qe, g in G.items():
        a = mean(r["ann_ret"] for r, b in g if b == nb - 1); c = mean(r["ann_ret"] for r, b in g if b == 0)
        if a is not None and c is not None: ta.append(a - c)
    res["ann_TB"] = summ(ta)
    return res


def by_tertile(rs, key="sue_eps"):
    """mcap tertile within each qe (cut among that quarter's eligible events), then SUE quintiles within tertile."""
    by = collections.defaultdict(list)
    for r in rs:
        if r.get(key) is not None: by[r["qe"]].append(r)
    tert = {0: [], 1: [], 2: []}
    for qe, g in by.items():
        g = sorted(g, key=lambda r: r["mcap_cr"]); n = len(g)
        for i, r in enumerate(g): tert[min(2, int(i * 3 / n))].append(r)
    out = {}
    per_q = {}
    for t, rr in tert.items():
        G = groups(rr, key, 5, 15)
        out[t] = {}
        for h in H:
            tb = {}
            for qe, g in G.items():
                mt = mean(r[f"r{h}"] for r, b in g if b == 4); mb = mean(r[f"r{h}"] for r, b in g if b == 0)
                if mt is not None and mb is not None: tb[qe] = mt - mb
            out[t][f"h{h}"] = summ(list(tb.values()))
            per_q[(t, h)] = tb
        out[t]["mcap_median"] = st.median(r["mcap_cr"] for r in rr) if rr else None
    for h in H:
        common = set(per_q[(0, h)]) & set(per_q[(2, h)])
        out[f"small_minus_large_h{h}"] = summ([per_q[(0, h)][q] - per_q[(2, h)][q] for q in common])
    return out


def pooled(rs, key="sue_eps"):
    """event-level context: pooled top/bottom quintile means."""
    G = groups(rs, key, 5, 25); o = {}
    for h in H:
        t = [r[f"r{h}"] - r[f"c{h}"] for g in G.values() for r, b in g if b == 4 and r[f"r{h}"] is not None and r[f"c{h}"] is not None]
        b = [r[f"r{h}"] - r[f"c{h}"] for g in G.values() for r, b2 in g if b2 == 0 and r[f"r{h}"] is not None and r[f"c{h}"] is not None]
        o[f"h{h}"] = {"top_n": len(t), "top_mean_x": mean(t), "top_median_x": st.median(t) if t else None,
                      "top_hit": sum(x > 0 for x in t) / len(t) if t else None,
                      "bot_n": len(b), "bot_mean_x": mean(b), "bot_median_x": st.median(b) if b else None}
    return o


for per in ("train", "test", "all"):
    rs = [r for r in rows if per == "all" or r["period"] == per]
    OUT[per] = {
        "n_events": len(rs), "n_syms": len({r["sym"] for r in rs}),
        "primary_eps_quintile": analyse(rs),
        "eps_decile": analyse(rs, nb=10, minn=50),
        "rev_quintile": analyse(rs, key="sue_rev"),
        "eps_quintile_open_entry": analyse(rs, ret="ro"),
        "tertiles_eps": by_tertile(rs),
        "pooled_eps": pooled(rs),
    }
# year-by-year (exploratory)
yy = {}
for y in range(2018, 2026):
    rs = [r for r in rows if r["event"][:4] == str(y)]
    a = analyse(rs)
    yy[y] = {"n": a["n_events"], "TB63": a["h63"]["TB"].get("mean"), "top_ctrl63": a["h63"]["top_vs_ctrl"].get("mean")}
OUT["by_year"] = yy
# both-beat (exploratory): EPS and revenue SUE both in top quintile
json.dump(OUT, open(os.path.join(S, "results.json"), "w"), indent=1, default=str)


def f(x, pct=True):
    if x is None: return "  n/a"
    return f"{x * 100:+.2f}%" if pct else f"{x:.2f}"


def line(lbl, s):
    if "mean" not in s: return f"{lbl:34s} nq={s.get('n_q')}"
    return f"{lbl:34s} {f(s['mean'])} [{f(s['lo'])}, {f(s['hi'])}] t={f(s['t'], False)} nq={s['n_q']}"


for per in ("train", "test"):
    o = OUT[per]; print(f"\n===== {per.upper()}  events={o['n_events']} syms={o['n_syms']}")
    for name in ("primary_eps_quintile", "eps_decile", "rev_quintile", "eps_quintile_open_entry"):
        a = o[name]; print(f"-- {name}: events={a['n_events']} quarters={a['n_quarters']}")
        print(line("  announcement T-B (day0->entry)", a["ann_TB"]))
        for h in H:
            for k in ("TB", "top_vs_ctrl", "bot_vs_ctrl", "all_vs_ctrl"):
                print(line(f"  h{h} {k}", a[f"h{h}"][k]))
    t = o["tertiles_eps"]
    for k in (0, 1, 2):
        print(f"-- tertile {k} (median mcap {t[k]['mcap_median']:.0f} cr)")
        for h in H: print(line(f"  h{h} TB", t[k][f"h{h}"]))
    for h in H: print(line(f"  small-minus-large h{h}", t[f"small_minus_large_h{h}"]))
    print("-- pooled event-level (vs controls):", json.dumps({h: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items()} for h, d in o["pooled_eps"].items()}))
print("\nby year:", json.dumps(yy))
