#!/usr/bin/env python3
"""Step 4 (POST-HOC, exploratory, not pre-registered): does pledge add information beyond the solvency flags
(S2 interest cover < 1.5x, S5-India) and beyond loss-makers (S0)? Lift of B25/B50 within rows where the solvency
flag is NOT fired. Output: hard_filters_india_v2_outputs/posthoc.json"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common2 as C
sys.path.insert(0, os.path.join(C.ROOT, "tools", "backtests", "solvency_india"))
import s4_analyze as S4

rows = C.K.read_csv(os.path.join(C.OUT, "panel_v2.csv"))
out = {}
for cond in ("s2", "s5", "s0", "s1"):
    sub = [r for r in rows if r.get(cond) == "0"]
    for k in ("B25", "B50"):
        r = S4.stats(sub, k, "o_fail")
        out[f"{k}|{cond}=0"] = {x: r[x] for x in ("n_known", "n_fired", "n_fired_fail", "lift", "lift_ci", "wexcl", "prec", "base")}
# overlap: share of pledge-flagged rows also flagged by S2 / S5
for k in ("B25", "B50"):
    fl = [r for r in rows if r.get(k) == "1"]
    out[f"overlap_{k}"] = {c: sum(r[c] == "1" for r in fl) / len(fl) for c in ("s2", "s5", "s0", "s1")}
    out[f"overlap_{k}"]["n"] = len(fl)
C.K.jsave(os.path.join(C.OUT, "posthoc.json"), out)
for k, v in out.items():
    print(k, {a: (round(b, 3) if isinstance(b, float) else b) for a, b in v.items()})
