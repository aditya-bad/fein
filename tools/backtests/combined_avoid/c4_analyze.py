#!/usr/bin/env python3
"""Step 3b: pre-registered analysis (combined_avoid_india.md). Quintiles/bootstrap/summaries reuse
india_pead_survivorship/s5_analyze (groups, boot, summ, mean; loaded without running its analysis).
H1: per-quarter mean excess(A) - mean excess(B), quarters with >= 3 events in each, mean across quarters, 5,000-draw
quarter bootstrap (seed 1). H2: pooled P(halve 12m) A / D with a quarter bootstrap of the ratio.
Output: research_notes/Backtests/combined_avoid_outputs/{results.json, tables.md}."""
import collections, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common3 as C

_src = open(os.path.join(C.ROOT, "tools", "backtests", "india_pead_survivorship", "s5_analyze.py")).read()
_g = {"__file__": "s5_head"}
exec(compile(_src.split("\nev = read(")[0].replace("import common as K", ""), "s5_head", "exec"), _g)
groups, summ, boot, mean = _g["groups"], _g["summ"], _g["boot"], _g["mean"]
NUM = ("sue", "r13", "cA13", "r26", "cA26", "mcap_cr", "pledge", "B25", "B50", "S1", "S2", "S4", "S5", "RED", "RED_u0",
       "halve12", "fin", "distress", "icr")


def read():
    rows, hdr = [], None
    for line in open(os.path.join(C.OUT, "events_flags.tsv")):
        p = line.rstrip("\n").split("\t")
        if hdr is None: hdr = p; continue
        r = dict(zip(hdr, p))
        for k in NUM:
            if k in r: r[k] = float(r[k]) if r[k] != "" else None
        rows.append(r)
    return rows


def assign(rows):
    """SUE quintile within fiscal quarter over the whole event set (same cut points as the survivorship check)."""
    for qe, g in groups(rows, "sue", 5, 25).items():
        for r, b in g: r["bin"] = b
    return [r for r in rows if "bin" in r]


def label(r, flag):
    f = r.get(flag)
    if f is None: return None
    bot = r["bin"] <= 1
    return ("A" if f == 1 else "B") if bot else ("C" if f == 1 else "D")


def xs(r, h=13):
    return None if r.get(f"r{h}") is None or r.get(f"cA{h}") is None else r[f"r{h}"] - r[f"cA{h}"]


def by_q(rows, flag, h=13):
    q = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        g = label(r, flag)
        if g: q[r["qe"]][g].append(r)
    return q


def analyse(rows, flag, h=13, minq=3):
    Q = by_q(rows, flag, h)
    res = {"n": {g: sum(len(v[g]) for v in Q.values()) for g in "ABCD"}}
    res["n_unknown"] = sum(1 for r in rows if r.get(flag) is None)
    qm = {g: [] for g in "ABCD"}
    diffs = collections.defaultdict(list)
    for qe, v in Q.items():
        m = {g: mean(xs(r, h) for r in v[g]) if len([r for r in v[g] if xs(r, h) is not None]) >= minq else None
             for g in "ABCD"}
        for g in "ABCD":
            if m[g] is not None: qm[g].append(m[g])
        for a, b in (("A", "B"), ("A", "C"), ("A", "D"), ("B", "D"), ("C", "D")):
            if m[a] is not None and m[b] is not None: diffs[a + "-" + b].append(m[a] - m[b])
        if all(m[g] is not None for g in "ABCD"): diffs["interaction"].append((m["A"] - m["B"]) - (m["C"] - m["D"]))
    res["excess_qmean"] = {g: summ(qm[g]) for g in "ABCD"}
    res["excess_pooled"] = {g: mean(xs(r, h) for v in Q.values() for r in v[g]) for g in "ABCD"}
    res["diff"] = {k: summ(v) for k, v in diffs.items()}
    # halving
    hq = {qe: {g: [r["halve12"] for r in v[g] if r.get("halve12") is not None] for g in "ABCD"} for qe, v in Q.items()}
    rate = lambda qs, g: (sum(sum(hq[q][g]) for q in qs) / max(1, sum(len(hq[q][g]) for q in qs)))
    qs = sorted(hq)
    res["halve"] = {g: {"n": sum(len(hq[q][g]) for q in qs), "k": int(sum(sum(hq[q][g]) for q in qs)),
                        "p": rate(qs, g)} for g in "ABCD"}
    rnd = random.Random(1); bs = {"A/D": [], "A/B": [], "B/D": [], "C/D": []}
    for _ in range(5000):
        s = [rnd.choice(qs) for _ in qs]
        p = {g: rate(s, g) for g in "ABCD"}
        for k in bs:
            a, b = k.split("/")
            if p[b] > 0: bs[k].append(p[a] / p[b])
    for k in bs:
        a, b = k.split("/"); v = sorted(bs[k]); pb = res["halve"][b]["p"]
        res["halve"]["ratio_" + k] = {"ratio": res["halve"][a]["p"] / pb if pb else None,
                                      "lo": v[int(0.025 * len(v))] if v else None, "hi": v[int(0.975 * len(v)) - 1] if v else None}
    return res


def verdicts(R):
    d = R["diff"].get("A-B", {})
    if d.get("mean") is not None and d["hi"] < 0:
        h1 = "SUPPORTED" if d["mean"] <= -0.02 else "WEAKER THAN HYPOTHESISED (real but < 2 pp)"
    else: h1 = "NOT SUPPORTED"
    r = R["halve"]["ratio_A/D"]
    if r["ratio"] is not None and r["lo"] is not None and r["lo"] > 1:
        h2 = "SUPPORTED" if r["ratio"] >= 2 else "WEAKER THAN HYPOTHESISED (ratio < 2)"
    else: h2 = "NOT SUPPORTED"
    return {"H1": h1, "H2": h2}


def main():
    rows = assign(read())
    R = {"n_events": len(rows)}
    variants = {"primary": (rows, "RED"), "unknown_as_unflagged": (rows, "RED_u0"), "B25_only": (rows, "B25"),
                "B50_only": (rows, "B50"), "S2_only": (rows, "S2"), "S5_only": (rows, "S5"),
                "LIVE_only": ([r for r in rows if r["u"] == "L"], "RED"),
                "no_financials": ([r for r in rows if r.get("fin") != 1], "RED"),
                "2018_21": ([r for r in rows if r["event"][:4] <= "2021"], "RED"),
                "2022_25": ([r for r in rows if r["event"][:4] >= "2022"], "RED")}
    for k, (rs, fl) in variants.items():
        R[k] = analyse(rs, fl)
        R[k]["verdicts"] = verdicts(R[k])
    R["w26_primary"] = analyse(rows, "RED", h=26); R["w26_primary"]["verdicts"] = verdicts(R["w26_primary"])
    os.makedirs(C.REPORT_OUT, exist_ok=True)
    C.js(os.path.join(C.REPORT_OUT, "results.json"), R)
    pc = lambda s: "–" if not s or s.get("mean") is None else (
        f"{100*s['mean']:+.2f}% [{100*s['lo']:+.2f}, {100*s['hi']:+.2f}] t {s['t']:.2f} (q={s['n_q']})" if s.get("t") is not None
        else f"{100*s['mean']:+.2f}%")
    fp = lambda v: "–" if v is None else f"{100*v:+.2f}%"
    fx = lambda v: "–" if v is None else f"{v:.2f}x"
    L = ["# Combined avoid test — tables (auto-generated by c4_analyze.py)", ""]
    for k in list(variants) + ["w26_primary"]:
        x = R[k]
        L += [f"## {k}", "", f"verdicts: {x['verdicts']}; unknown-flag events excluded: {x['n_unknown']}", "",
              "| group | n | excess (mean of quarterly means) | pooled excess | P(halve 12m) (k/n) |", "|---|---|---|---|---|"]
        for g in "ABCD":
            hv = x["halve"][g]
            warn = " ⚠ n<50" if x["n"][g] < 50 else ""
            pe = x["excess_pooled"][g]
            L.append(f"| {g}{warn} | {x['n'][g]} | {pc(x['excess_qmean'][g])} | {fp(pe)} | "
                     f"{100*hv['p']:.1f}% ({hv['k']}/{hv['n']}) |")
        L += ["", "| contrast | per-quarter difference |", "|---|---|"]
        for d in ("A-B", "A-C", "A-D", "B-D", "C-D", "interaction"):
            L.append(f"| {d} | {pc(x['diff'].get(d))} |")
        for rk in ("A/D", "A/B", "B/D", "C/D"):
            r = x["halve"]["ratio_" + rk]
            L.append(f"| halving ratio {rk} | {fx(r['ratio'])} [{fx(r['lo'])}, {fx(r['hi'])}] |")
        L.append("")
    open(os.path.join(C.REPORT_OUT, "tables.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
