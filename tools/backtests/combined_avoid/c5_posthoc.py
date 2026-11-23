#!/usr/bin/env python3
"""Post-hoc (exploratory, written after reading the primary tables): does the miss add halving risk on top of the red
flag? Pooled P(halve 12m) A / C with the same quarter bootstrap (5,000, seed 1); primary RED and B50."""
import collections, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import c4_analyze as A
import common3 as C
rows = A.assign(A.read()); out = {}
for flag in ("RED", "B50", "B25"):
    Q = A.by_q(rows, flag)
    hq = {q: {g: [r["halve12"] for r in v[g] if r.get("halve12") is not None] for g in "AC"} for q, v in Q.items()}
    rate = lambda qs, g: sum(sum(hq[q][g]) for q in qs) / max(1, sum(len(hq[q][g]) for q in qs))
    qs = sorted(hq); rnd = random.Random(1); bs = []
    for _ in range(5000):
        s = [rnd.choice(qs) for _ in qs]
        if rate(s, "C") > 0: bs.append(rate(s, "A") / rate(s, "C"))
    bs.sort()
    out[flag] = {"A_over_C": rate(qs, "A") / rate(qs, "C"), "lo": bs[int(.025 * len(bs))], "hi": bs[int(.975 * len(bs)) - 1]}
print(json.dumps(out, indent=1))
C.js(os.path.join(C.REPORT_OUT, "posthoc_A_over_C.json"), out)
