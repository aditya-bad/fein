#!/usr/bin/env python3
"""Pre-registered split test (research_notes/Backtests/survival_cap_split_india.md), run once.
Groups: G0 (no pledge>25%, ICR>=1.5), Gp pledge-only, Gi ICR-only, Gb both, B50, B50-only; each vs G0.
E: firm-cluster bootstrap (reuses survival_cap_general/sg2_analyze.rr_test). P: weighted, firm-cluster bootstrap within
stratum. Inputs: survival_cap_general_outputs/{events_out,panel_out}.tsv. Output: survival_cap_split_outputs/results.json."""
import collections, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "survival_cap_general"))
from sg2_analyze import read, f, ci, rr_test, ROOT, B, SEED  # noqa: E402
SRC = os.path.join(ROOT, "research_notes", "Backtests", "survival_cap_general_outputs")
OUT = os.path.join(ROOT, "research_notes", "Backtests", "survival_cap_split_outputs")
MIN_E_N, MIN_E_FIRMS, MIN_P_N = 30, 15, 20


def grp(r, s2="S2", u0=False):
    b, s, b50 = f(r.get("B25")), f(r.get(s2)), f(r.get("B50"))
    if u0: b, s, b50 = b or 0, s or 0, b50 or 0
    if b is None or s is None: return None
    return {"G0": b == 0 and s == 0, "Gp": b == 1 and s == 0, "Gi": b == 0 and s == 1, "Gb": b == 1 and s == 1,
            "B50": b50 == 1, "B50only": b50 == 1 and s == 0}


def vs(name, s2="S2", u0=False, ref="G0"):
    def fn(r):
        g = grp(r, s2, u0)
        if g is None: return None
        return 1 if g[name] else 0 if g[ref] else None
    return fn


GROUPS = ["Gp", "Gi", "Gb", "B50", "B50only"]


def firms(rows, flag, out):
    return len({r["sym"] for r in rows if flag(r) == 1 and f(r.get(out)) is not None})


def e_group(rows, name, **kw):
    fl = vs(name, **kw)
    d = {o: rr_test(rows, fl, o) for o in ("halve12", "fail3", "win3")}
    for o in ("xs52", "xs156"): d[o] = rr_test(rows, fl, o, diff=True)
    med = collections.defaultdict(list)
    for r in rows:
        g, y = fl(r), f(r.get("xs156"))
        if g is not None and y is not None: med[g].append(y)
    d["xs156_median"] = {k: round(float(np.median(v)), 4) for k, v in med.items()}
    d["firms_flag_h12"] = firms(rows, fl, "halve12"); d["firms_flag_win3"] = firms(rows, fl, "win3")
    return d


def p_test(rows, flag, out, diff=False):
    """weighted rates; bootstrap resamples firms (key) within stratum."""
    S = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in rows:
        g, y = flag(r), f(r.get(out))
        if g is None or y is None: continue
        S[r["stratum"]][r["key"]].append((float(r["weight"]), g, y))
    def stat(L):
        w1 = sum(w for w, g, _ in L if g == 1); w0 = sum(w for w, g, _ in L if g == 0)
        if w1 == 0 or w0 == 0: return np.nan, np.nan, np.nan
        m1 = sum(w * y for w, g, y in L if g == 1) / w1; m0 = sum(w * y for w, g, y in L if g == 0) / w0
        return m1, m0, (m1 - m0) if diff else (m1 / m0 if m0 else np.nan)
    allL = [x for st in S.values() for L in st.values() for x in L]
    m1, m0, s = stat(allL)
    rng = np.random.default_rng(SEED); bs = []
    cl = {k: list(v.values()) for k, v in S.items()}
    for _ in range(B):
        L = []
        for v in cl.values():
            for i in rng.integers(0, len(v), len(v)): L += v[i]
        bs.append(stat(L)[2])
    return {"n1": sum(g == 1 for _, g, _ in allL), "n0": sum(g == 0 for _, g, _ in allL),
            "firms1": len({k for st in S.values() for k, L in st.items() if any(g == 1 for _, g, _ in L)}),
            "m1_w": round(m1, 4), "m0_w": round(m0, 4), ("diff" if diff else "rr"): round(s, 3), "ci": ci(bs)}


def p_group(rows, name, **kw):
    fl = vs(name, s2="s2", **kw)
    d = {o: p_test(rows, fl, o) for o in ("h12", "o_fail", "o_strict", "winner")}
    for o in ("xs52", "xs156"): d[o] = p_test(rows, fl, o, diff=True)
    return d


def ok_e(d, out):
    x = d[out]
    return x is not None and x["n1"] >= MIN_E_N and d["firms_flag_" + ("h12" if out == "halve12" else "win3")] >= MIN_E_FIRMS


def main():
    E = read(os.path.join(SRC, "events_out.tsv")); P = read(os.path.join(SRC, "panel_out.tsv"))
    NF = [r for r in E if r["fin"] == "0"]
    yr = lambda r: int(r["entry"][:4])
    early, late = [r for r in NF if yr(r) <= 2021], [r for r in NF if yr(r) >= 2022]
    R = {"counts": {}, "E": {}, "E_2018_21": {}, "E_2022_25": {}, "P": {}, "sens": {}}
    for nm, rows, s2 in (("E", NF, "S2"), ("P", P, "s2")):
        c = collections.Counter()
        for r in rows:
            g = grp(r, s2)
            c["unknown" if g is None else next(k for k in ("G0", "Gp", "Gi", "Gb") if g[k])] += 1
        R["counts"][nm] = dict(c)
    for g in GROUPS:
        R["E"][g] = e_group(NF, g); R["E_2018_21"][g] = e_group(early, g); R["E_2022_25"][g] = e_group(late, g)
        R["P"][g] = p_group(P, g)
    # Gp vs Gi directly
    R["E"]["Gp_vs_Gi"] = {"win3": rr_test(NF, vs("Gp", ref="Gi"), "win3"),
                          "halve12": rr_test(NF, vs("Gp", ref="Gi"), "halve12"),
                          "xs156": rr_test(NF, vs("Gp", ref="Gi"), "xs156", diff=True)}
    R["P"]["Gp_vs_Gi"] = {"winner": p_test(P, vs("Gp", s2="s2", ref="Gi"), "winner"),
                          "h12": p_test(P, vs("Gp", s2="s2", ref="Gi"), "h12"),
                          "xs156": p_test(P, vs("Gp", s2="s2", ref="Gi"), "xs156", True)}
    # sensitivities (do not decide)
    for g in ("Gp", "Gi", "B50"):
        R["sens"][g] = {"all_incl_fin_H12_WIN3": [rr_test(E, vs(g), o) for o in ("halve12", "win3")],
                        "live_only_H12_WIN3": [rr_test([r for r in NF if r["u"] == "L"], vs(g), o) for o in ("halve12", "win3")],
                        "unknown_as_0_H12_WIN3": [rr_test(NF, vs(g, u0=True), o) for o in ("halve12", "win3")],
                        "quarter_boot_H12_WIN3": [rr_test(NF, vs(g), o, "qe") for o in ("halve12", "win3")]}
    # ---- verdict (pre-registered Rule T and Rule L) ----
    def T(g):
        e, p, e1, e2 = R["E"][g], R["P"][g], R["E_2018_21"][g], R["E_2022_25"][g]
        t1 = (ok_e(e, "win3") and ok_e(e, "halve12") and e["win3"]["rr"] <= 1.0 and e["win3"]["ci"][1] < 1.2
              and e["halve12"]["rr"] >= 2.0 and e["halve12"]["ci"][0] > 1.3)
        p_ok = p["winner"]["n1"] >= MIN_P_N
        t2 = (p_ok and p["winner"]["rr"] <= 1.0 and p["winner"]["ci"][1] < 1.2 and p["h12"]["rr"] >= 2.0 and p["h12"]["ci"][0] > 1.0)
        t2_points = p_ok and p["winner"]["rr"] <= 1.0 and p["h12"]["rr"] >= 2.0
        t3 = all(ok_e(x, "win3") and ok_e(x, "halve12") and x["win3"]["rr"] <= 1.0 and x["halve12"]["rr"] >= 2.0 for x in (e1, e2))
        t4 = e["xs156"]["diff"] <= 0 and p["xs156"]["diff"] <= 0
        return {"T1": t1, "T2": t2, "T2_points_only": t2_points, "T3": t3, "T4": t4,
                "pass": t1 and t2 and t3 and t4, "provisional": t1 and t3 and t4 and (not t2) and t2_points}
    V = {g: T(g) for g in ("Gp", "B50", "Gb")}
    if V["Gp"]["pass"] and R["E"]["Gb"]["win3"]["rr"] <= 1.0: tight = "ADOPT: pledge > 25% -> 0 new money"
    elif V["B50"]["pass"]: tight = "ADOPT: pledge > 50% -> 0 new money"
    elif V["Gb"]["pass"]: tight = "ADOPT: pledge > 25% and ICR < 1.5x -> 0 new money"
    elif any(V[g]["provisional"] for g in V): tight = "PROVISIONAL (" + ",".join(g for g in V if V[g]["provisional"]) + ")"
    else: tight = "NOT ADOPTED"
    gi, pgi = R["E"]["Gi"], R["P"]["Gi"]
    loosen = gi["halve12"]["ci"][1] < 1.5 and gi["fail3"]["ci"][1] < 2.0 and pgi["o_fail"]["ci"][1] < 1.5
    R["verdict"] = {"rule_T": V, "tighten": tight, "rule_L_loosen_ICR_only": loosen}
    os.makedirs(OUT, exist_ok=True)
    json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=lambda x: x.item())
    print(json.dumps(R["counts"])); print(json.dumps(R["verdict"], indent=1, default=lambda x: x.item()))


if __name__ == "__main__":
    main()
