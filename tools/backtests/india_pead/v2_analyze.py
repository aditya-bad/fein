#!/usr/bin/env python3
"""PEAD v2, step 3: pre-registered analysis (research_notes/Backtests/india_pead_v2.md) of V2DIR/events_v2.tsv.
FRESH = events dated 2026 of fiscal quarters Dec-25, Mar-26, Jun-26, Sep-26 -> event-level pooled means; t with SE
clustered by entry ISO week (sensitivity: entry month); 95% cluster bootstrap (5,000 draws, seed 1).
RERUN = events dated 2022-2025 -> v1 method: mean of per-fiscal-quarter values, t across quarters, 95% bootstrap over
quarters (5,000).
Quintiles of SUE within each fiscal quarter among ALL its eligible events (>= 25), whatever the window status.
Usage: python3 v2_analyze.py V2DIR [--sue-col sue|sue_S|sue_C]  -> V2DIR/v2_results[_<col>].json + printout"""
import collections, datetime as dt, json, math, os, random, statistics as st, sys
import numpy as np

V2 = sys.argv[1]
COL = sys.argv[sys.argv.index("--sue-col") + 1] if "--sue-col" in sys.argv else "sue"
FRESH_Q = {"2025-12-31", "2026-03-31", "2026-06-30", "2026-09-30"}
H = (21, 63, 126)
NUM = ("mcap_cr", "sue", "sue_C", "sue_S", "ann_ret") + tuple(f"{p}{h}" for h in H for p in ("r", "c", "nc"))
rows, hdr = [], None
for line in open(os.path.join(V2, "events_v2.tsv")):
    p = line.rstrip("\n").split("\t")
    if hdr is None: hdr = p; continue
    r = dict(zip(hdr, p))
    for k in NUM: r[k] = float(r[k]) if r.get(k, "") != "" else None
    y = r["event"][:4]
    r["period"] = "fresh" if (y == "2026" and r["qe"] in FRESH_Q) else ("rerun" if "2022" <= y <= "2025" else "other")
    e = dt.date.fromisoformat(r["entry"]); iw = e.isocalendar()
    r["wk"] = f"{iw[0]}-W{iw[1]:02d}"; r["mo"] = r["entry"][:7]
    for h in H:
        r[f"x{h}"] = r[f"r{h}"] - r[f"c{h}"] if r[f"r{h}"] is not None and r[f"c{h}"] is not None else None
    rows.append(r)

# quintiles within fiscal quarter (all events of that qe with a SUE)
byq = collections.defaultdict(list)
for r in rows:
    r["q5"] = None
    if r[COL] is not None: byq[r["qe"]].append(r)
for qe, g in byq.items():
    if len(g) < 25: continue
    g.sort(key=lambda r: r[COL]); n = len(g)
    for i, r in enumerate(g): r["q5"] = min(4, int(i * 5 / n))
    g2 = sorted(g, key=lambda r: r["mcap_cr"])
    for i, r in enumerate(g2): r["tert"] = min(2, int(i * 3 / n))
# quintiles within (qe, tertile) for H4 (>= 15 events, as v1)
bqt = collections.defaultdict(list)
for r in rows:
    if r.get("tert") is not None: bqt[(r["qe"], r["tert"])].append(r)
for k, g in bqt.items():
    for r in g: r["q5t"] = None
    if len(g) < 15: continue
    g.sort(key=lambda r: r[COL]); n = len(g)
    for i, r in enumerate(g): r["q5t"] = min(4, int(i * 5 / n))

RNG = np.random.default_rng(1)
NB = 5000


def cl_mean(recs, field, cl="wk", shift=0.0):
    recs = [r for r in recs if r[field] is not None]
    if len(recs) < 10: return {"n": len(recs)}
    x = np.array([r[field] for r in recs]) - shift
    m = float(x.mean())
    cid = {}; g = np.array([cid.setdefault(r[cl], len(cid)) for r in recs]); G = len(cid)
    S = np.bincount(g, weights=x, minlength=G); N = np.bincount(g, minlength=G).astype(float)
    e = np.bincount(g, weights=x - m, minlength=G)
    se = math.sqrt(G / (G - 1) * float((e ** 2).sum())) / len(x) if G > 1 else float("nan")
    idx = RNG.integers(G, size=(NB, G))
    bs = np.sort(S[idx].sum(1) / N[idx].sum(1))
    return {"n": len(x), "G": G, "mean": m, "t": m / se if se > 0 else None,
            "lo": float(bs[int(.025 * NB)]), "hi": float(bs[int(.975 * NB) - 1]),
            "median": float(np.median(x)), "hit": float((x > 0).mean())}


def cl_diff(A, B, field, cl="wk"):
    A = [r for r in A if r[field] is not None]; B = [r for r in B if r[field] is not None]
    if len(A) < 10 or len(B) < 10: return {"nA": len(A), "nB": len(B)}
    cid = {}
    ga = np.array([cid.setdefault(r[cl], len(cid)) for r in A]); gb = np.array([cid.setdefault(r[cl], len(cid)) for r in B])
    G = len(cid)
    xa = np.array([r[field] for r in A]); xb = np.array([r[field] for r in B])
    ma, mb = xa.mean(), xb.mean(); d = float(ma - mb)
    psi = np.bincount(ga, weights=(xa - ma) / len(xa), minlength=G) - np.bincount(gb, weights=(xb - mb) / len(xb), minlength=G)
    se = math.sqrt(G / (G - 1) * float((psi ** 2).sum()))
    SA = np.bincount(ga, weights=xa, minlength=G); NA = np.bincount(ga, minlength=G).astype(float)
    SB = np.bincount(gb, weights=xb, minlength=G); NB_ = np.bincount(gb, minlength=G).astype(float)
    idx = RNG.integers(G, size=(NB, G))
    with np.errstate(invalid="ignore", divide="ignore"):
        bs = SA[idx].sum(1) / NA[idx].sum(1) - SB[idx].sum(1) / NB_[idx].sum(1)
    bs = np.sort(bs[np.isfinite(bs)]); k = len(bs)
    return {"nA": len(xa), "nB": len(xb), "G": G, "mean": d, "t": d / se if se > 0 else None,
            "lo": float(bs[int(.025 * k)]), "hi": float(bs[int(.975 * k) - 1])}


def q_summ(vals, seed=1):
    v = [x for x in vals if x is not None]
    if len(v) < 3: return {"n_q": len(v)}
    m = sum(v) / len(v); sd = st.stdev(v)
    rnd = random.Random(seed)
    b = sorted(sum(rnd.choice(v) for _ in range(len(v))) / len(v) for _ in range(5000))
    return {"n_q": len(v), "mean": m, "t": m / (sd / math.sqrt(len(v))) if sd > 0 else None, "lo": b[125], "hi": b[4874]}


def mean(x):
    x = [v for v in x if v is not None]
    return sum(x) / len(x) if x else None


OUT = {"sue_col": COL, "counts": collections.Counter(r["period"] for r in rows)}
# ---------------- FRESH
F = [r for r in rows if r["period"] == "fresh" and r["q5"] is not None]
top = [r for r in F if r["q5"] == 4]; bot = [r for r in F if r["q5"] == 0]
fr = {"n_events": len(F), "n_syms": len({r["sym"] for r in F}),
      "by_quarter_counts": {q: {"n": sum(r["qe"] == q for r in F), "n_top": sum(r["qe"] == q for r in top),
                                **{f"closed{h}": sum(r["qe"] == q and r[f"x{h}"] is not None for r in F) for h in H}}
                            for q in sorted(FRESH_Q)},
      "basis_C_share": mean([1.0 if r["basis"] == "C" else 0.0 for r in F])}
for h in H:
    x = f"x{h}"; R = f"r{h}"
    up = [r for r in top if r["ann_ret"] is not None and r["ann_ret"] > 0]
    dn = [r for r in top if r["ann_ret"] is not None and r["ann_ret"] <= 0]
    fr[f"h{h}"] = {
        "top": cl_mean(top, x), "top_net0.5": cl_mean(top, x, shift=.005), "top_net1.0": cl_mean(top, x, shift=.01),
        "top_net1.0_month": cl_mean(top, x, "mo", .01),
        "bot": cl_mean(bot, x), "bot_month": cl_mean(bot, x, "mo"), "all": cl_mean(F, x),
        "TB_raw": cl_diff(top, bot, R),
        "H2_D_up_minus_down": cl_diff(up, dn, x), "H2_D_month": cl_diff(up, dn, x, "mo"),
        "top_up_net1.0": cl_mean(up, x, shift=.01), "top_down": cl_mean(dn, x),
        "ladder": {f"Q{b + 1}": cl_mean([r for r in F if r["q5"] == b], x) for b in range(5)},
        "by_quarter": {q: {"top": cl_mean([r for r in top if r["qe"] == q], x),
                           "bot": cl_mean([r for r in bot if r["qe"] == q], x),
                           "TB": cl_diff([r for r in top if r["qe"] == q], [r for r in bot if r["qe"] == q], R)}
                       for q in sorted(FRESH_Q)},
        "H4_tertiles": {t: {"top": cl_mean([r for r in F if r.get("tert") == t and r.get("q5t") == 4], x),
                            "TB": cl_diff([r for r in F if r.get("tert") == t and r.get("q5t") == 4],
                                          [r for r in F if r.get("tert") == t and r.get("q5t") == 0], R),
                            "mcap_median": st.median([r["mcap_cr"] for r in F if r.get("tert") == t] or [0])}
                        for t in (0, 1, 2)},
        "consolidated_only": {"top": cl_mean([r for r in top if r["basis"] == "C"], x),
                              "bot": cl_mean([r for r in bot if r["basis"] == "C"], x)},
    }
OUT["fresh"] = fr

# ---------------- RERUN (quarter-level, v1 method)
Rr = [r for r in rows if r["period"] == "rerun" and r["q5"] is not None]
QS = sorted({r["qe"] for r in Rr})
rr = {"n_events": len(Rr), "n_syms": len({r["sym"] for r in Rr}), "n_quarters": len(QS),
      "basis_C_share": mean([1.0 if r["basis"] == "C" else 0.0 for r in Rr])}
for h in H:
    x = f"x{h}"; R = f"r{h}"
    tq, bq, aq, tbq, dq, upq, tert = [], [], [], [], [], [], {0: ([], []), 1: ([], []), 2: ([], [])}
    perq = {}
    for q in QS:
        g = [r for r in Rr if r["qe"] == q]
        t_ = [r for r in g if r["q5"] == 4]; b_ = [r for r in g if r["q5"] == 0]
        mt, mb = mean(r[x] for r in t_), mean(r[x] for r in b_)
        tq.append(mt); bq.append(mb); aq.append(mean(r[x] for r in g))
        rt, rb = mean(r[R] for r in t_), mean(r[R] for r in b_)
        tbq.append(rt - rb if rt is not None and rb is not None else None)
        u = mean(r[x] for r in t_ if r["ann_ret"] is not None and r["ann_ret"] > 0)
        dn = mean(r[x] for r in t_ if r["ann_ret"] is not None and r["ann_ret"] <= 0)
        dq.append(u - dn if u is not None and dn is not None else None); upq.append(u)
        for t in (0, 1, 2):
            gt = [r for r in g if r.get("tert") == t]
            a1 = mean(r[x] for r in gt if r.get("q5t") == 4)
            a2, a3 = mean(r[R] for r in gt if r.get("q5t") == 4), mean(r[R] for r in gt if r.get("q5t") == 0)
            tert[t][0].append(a1); tert[t][1].append(a2 - a3 if a2 is not None and a3 is not None else None)
        perq[q] = {"n": len(g), "top_x": mt, "bot_x": mb, "TB": tbq[-1]}
    rr[f"h{h}"] = {"top": q_summ(tq), "top_net0.5": q_summ([v - .005 for v in tq if v is not None]),
                   "top_net1.0": q_summ([v - .01 for v in tq if v is not None]), "bot": q_summ(bq), "all": q_summ(aq),
                   "TB_raw": q_summ(tbq), "H2_D_up_minus_down": q_summ(dq),
                   "top_up_net1.0": q_summ([v - .01 for v in upq if v is not None]),
                   "H4_tertiles": {t: {"top": q_summ(tert[t][0]), "TB": q_summ(tert[t][1])} for t in (0, 1, 2)},
                   "per_quarter": perq,
                   "event_level_top_net1.0_week": cl_mean([r for r in Rr if r["q5"] == 4], x, shift=.01)}
    yy = {}
    for y in ("2022", "2023", "2024", "2025"):
        g = [r for r in Rr if r["event"][:4] == y]
        yy[y] = {"top": cl_mean([r for r in g if r["q5"] == 4], x), "bot": cl_mean([r for r in g if r["q5"] == 0], x)}
    rr[f"h{h}"]["by_year_event_level"] = yy
OUT["rerun"] = rr
suffix = "" if COL == "sue" else "_" + COL
json.dump(OUT, open(os.path.join(V2, f"v2_results{suffix}.json"), "w"), indent=1, default=str)


def f(s, k="mean"):
    if not isinstance(s, dict) or s.get(k) is None: return f"n/a {s}"
    t = s.get("t"); n = s.get("n", s.get("n_q", s.get("nA")))
    return (f"{s['mean'] * 100:+.2f}% [{s['lo'] * 100:+.2f}, {s['hi'] * 100:+.2f}] t={t:.2f} n={n}"
            + (f" G={s['G']}" if "G" in s else ""))


print("SUE column:", COL, "| counts:", dict(OUT["counts"]))
print(f"\n===== FRESH 2026  events={fr['n_events']} syms={fr['n_syms']} basisC={fr['basis_C_share']:.2f}")
print(" quarter counts:", fr["by_quarter_counts"])
for h in H:
    o = fr[f"h{h}"]; print(f"-- h{h}")
    for k in ("top", "top_net1.0", "top_net1.0_month", "bot", "bot_month", "all", "TB_raw", "H2_D_up_minus_down",
              "H2_D_month", "top_up_net1.0", "top_down"):
        print(f"   {k:20s}", f(o[k]))
    for k, v in o["ladder"].items(): print("   ladder", k, f(v))
    for q, v in o["by_quarter"].items(): print("   q", q, "top", f(v["top"]), "| bot", f(v["bot"]))
    for t, v in o["H4_tertiles"].items(): print(f"   tert{t} (med {v['mcap_median']:.0f} cr) top", f(v["top"]), "| TB", f(v["TB"]))
    print("   cons-only top", f(o["consolidated_only"]["top"]), "| bot", f(o["consolidated_only"]["bot"]))
print(f"\n===== RERUN 2022-25  events={rr['n_events']} syms={rr['n_syms']} quarters={rr['n_quarters']} basisC={rr['basis_C_share']:.2f}")
for h in H:
    o = rr[f"h{h}"]; print(f"-- h{h}")
    for k in ("top", "top_net1.0", "bot", "all", "TB_raw", "H2_D_up_minus_down", "top_up_net1.0", "event_level_top_net1.0_week"):
        print(f"   {k:20s}", f(o[k]))
    for t, v in o["H4_tertiles"].items(): print(f"   tert{t} top", f(v["top"]), "| TB", f(v["TB"]))
    for y, v in o["by_year_event_level"].items(): print("   year", y, "top", f(v["top"]), "| bot", f(v["bot"]))
