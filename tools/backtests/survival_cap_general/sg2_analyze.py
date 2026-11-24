#!/usr/bin/env python3
"""Step 2: pre-registered analysis (research_notes/Backtests/survival_cap_general_india.md), run once.
E: RR of 12-month halving for CARD (pledge > 25% or interest cover < 1.5x) vs not, firm-cluster bootstrap (5,000, seed 1),
quarter bootstrap, Mantel-Haenszel (quarter x mcap tercile); XS52/XS156, FAIL3, WIN3 and winner cost.
P: weighted RRs with stratum-wise bootstrap. Output: survival_cap_general_outputs/{results.json, tables.md}."""
import collections, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "research_notes", "Backtests", "survival_cap_general_outputs")
B, SEED = 5000, 1


def f(x):
    return None if x in ("", None) else float(x)


def read(fn):
    rows, hdr = [], None
    for line in open(fn):
        p = line.rstrip("\n").split("\t")
        if hdr is None: hdr = p; continue
        rows.append(dict(zip(hdr, p)))
    return rows


def card(r, b25="B25", s2="S2", u0=False):
    c = [f(r.get(b25)), f(r.get(s2))]
    if 1 in c: return 1
    if None not in c or u0: return 0
    return None


def red(r):
    c = card(r)
    if c == 1 or f(r.get("S5")) == 1: return 1
    return c


def ci(a):
    a = np.asarray([x for x in a if np.isfinite(x)])
    return [round(float(np.percentile(a, 2.5)), 3), round(float(np.percentile(a, 97.5)), 3)] if len(a) else None


def cluster_stats(rows, flag, out, key):
    """per-cluster sums for flagged/unflagged: n, sum(outcome). Outcome may be binary or continuous."""
    d = collections.defaultdict(lambda: np.zeros(4))
    for r in rows:
        g, y = flag(r), f(r.get(out))
        if g is None or y is None: continue
        v = d[r[key]]
        if g == 1: v[0] += 1; v[1] += y
        else: v[2] += 1; v[3] += y
    return np.array(list(d.values())) if d else np.zeros((0, 4))


def rr_test(rows, flag, out, key="sym", diff=False):
    M = cluster_stats(rows, flag, out, key)
    if len(M) == 0: return None
    n1, s1, n0, s0 = M.sum(0)
    if n1 == 0 or n0 == 0: return None
    p1, p0 = s1 / n1, s0 / n0
    rng = np.random.default_rng(SEED)
    idx = rng.integers(0, len(M), size=(B, len(M)))
    S = M[idx].sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        b1, b0 = S[:, 1] / S[:, 0], S[:, 3] / S[:, 2]
        stat = (b1 - b0) if diff else (b1 / b0)
    res = {"n1": int(n1), "n0": int(n0), "m1": round(p1, 4), "m0": round(p0, 4), "clusters": len(M)}
    if diff: res.update(diff=round(p1 - p0, 4), ci=ci(stat))
    else: res.update(k1=int(s1), k0=int(s0), rr=round(p1 / p0, 3) if p0 else None, ci=ci(stat))
    return res


def mh_rr(rows, flag, out):
    byq = collections.defaultdict(list)
    for r in rows:
        if flag(r) is not None and f(r.get(out)) is not None: byq[r["qe"]].append(r)
    num = den = 0.0
    for q, L in byq.items():
        mc = np.array([float(r["mcap_cr"]) for r in L]); cut = np.percentile(mc, [100 / 3, 200 / 3])
        ter = [0 if m <= cut[0] else 1 if m <= cut[1] else 2 for m in mc]
        for t in range(3):
            S = [r for r, tt in zip(L, ter) if tt == t]
            N = len(S)
            if N == 0: continue
            a = sum(f(r[out]) for r in S if flag(r) == 1); n1 = sum(flag(r) == 1 for r in S)
            c = sum(f(r[out]) for r in S if flag(r) == 0); n0 = N - n1
            num += a * n0 / N; den += c * n1 / N
    return round(num / den, 3) if den else None


def median_by(rows, flag, out):
    g = collections.defaultdict(list)
    for r in rows:
        if flag(r) is not None and f(r.get(out)) is not None: g[flag(r)].append(f(r[out]))
    return {k: round(float(np.median(v)), 4) for k, v in g.items()}


def winner_cost(rows, flag):
    k = [r for r in rows if flag(r) is not None]
    sh = lambda S: round(sum(flag(r) == 1 for r in S) / len(S), 4) if S else None
    W = [r for r in k if f(r["win3"]) == 1]
    firms = collections.defaultdict(list)
    for r in W: firms[r["sym"]].append(flag(r))
    return {"share_all_events_flagged": sh(k), "share_win3_flagged": sh(W), "n_win3": len(W),
            "share_halve12_flagged": sh([r for r in k if f(r["halve12"]) == 1]),
            "share_fail3_flagged": sh([r for r in k if f(r["fail3"]) == 1]),
            "n_fail3": sum(f(r["fail3"]) == 1 for r in k),
            "win3_firms": len(firms), "win3_firms_all_flagged": sum(all(v == 1 for v in L) for L in firms.values()),
            "win3_firms_any_flagged": sum(any(v == 1 for v in L) for L in firms.values()),
            "p_win3_flag": rr_test(rows, flag, "win3")}


def e_block(rows, flag, key="sym"):
    return {"H12": rr_test(rows, flag, "halve12", key), "FAIL3": rr_test(rows, flag, "fail3", key),
            "WIN3": rr_test(rows, flag, "win3", key), "XS52": rr_test(rows, flag, "xs52", key, diff=True),
            "XS156": rr_test(rows, flag, "xs156", key, diff=True)}


# ---------------- sample P ----------------
def p_test(rows, flag, out, diff=False):
    S = collections.defaultdict(list)
    for r in rows:
        g, y = flag(r), f(r.get(out))
        if g is None or y is None: continue
        S[r["stratum"]].append((float(r["weight"]), g, y))
    def stat(L):
        w1 = sum(w for w, g, _ in L if g == 1); w0 = sum(w for w, g, _ in L if g == 0)
        if w1 == 0 or w0 == 0: return np.nan, np.nan, np.nan
        m1 = sum(w * y for w, g, y in L if g == 1) / w1; m0 = sum(w * y for w, g, y in L if g == 0) / w0
        return m1, m0, (m1 - m0) if diff else (m1 / m0 if m0 else np.nan)
    allL = [x for L in S.values() for x in L]
    m1, m0, st = stat(allL)
    rng = np.random.default_rng(SEED); bs = []
    arr = {k: L for k, L in S.items()}
    for _ in range(B):
        L = []
        for k, v in arr.items():
            L += [v[i] for i in rng.integers(0, len(v), len(v))]
        bs.append(stat(L)[2])
    return {"n1": sum(g == 1 for _, g, _ in allL), "n0": sum(g == 0 for _, g, _ in allL),
            "k1": int(sum(y for _, g, y in allL if g == 1)) if not diff else None,
            "m1_w": round(m1, 4), "m0_w": round(m0, 4), ("diff" if diff else "rr"): round(st, 3), "ci": ci(bs)}


def p_winner_cost(rows, flag):
    k = [r for r in rows if flag(r) is not None]
    wsh = lambda S: round(sum(float(r["weight"]) for r in S if flag(r) == 1) / sum(float(r["weight"]) for r in S), 4) if S else None
    return {"w_share_all_flagged": wsh(k), "w_share_winners_flagged": wsh([r for r in k if f(r["winner"]) == 1]),
            "n_winners": sum(f(r["winner"]) == 1 for r in k),
            "w_share_fail_flagged": wsh([r for r in k if f(r["o_fail"]) == 1]),
            "w_share_h12_flagged": wsh([r for r in k if f(r["h12"]) == 1])}


def main():
    E = read(os.path.join(OUT, "events_out.tsv"))
    P = read(os.path.join(OUT, "panel_out.tsv"))
    NF = [r for r in E if r["fin"] == "0"]
    R = {"E": {}, "P": {}}
    R["E"]["primary_nonfin_CARD"] = e_block(NF, card)
    R["E"]["primary_quarter_boot_H12"] = rr_test(NF, card, "halve12", "qe")
    R["E"]["primary_MH_H12"] = mh_rr(NF, card, "halve12")
    R["E"]["unknown_CARD"] = sum(card(r) is None for r in NF)
    R["E"]["median_xs"] = {h: median_by(NF, card, h) for h in ("xs52", "xs156")}
    R["E"]["winner_cost_CARD"] = winner_cost(NF, card)
    comps = {"B25": lambda r: None if f(r["B25"]) is None else int(f(r["B25"])),
             "B50": lambda r: None if f(r["B50"]) is None else int(f(r["B50"])),
             "S2": lambda r: None if f(r["S2"]) is None else int(f(r["S2"])),
             "S1": lambda r: None if f(r["S1"]) is None else int(f(r["S1"])),
             "S5": lambda r: None if f(r["S5"]) is None else int(f(r["S5"]))}
    R["E"]["components"] = {k: {"H12": rr_test(NF, fn, "halve12"), "FAIL3": rr_test(NF, fn, "fail3"),
                                "XS156": rr_test(NF, fn, "xs156", diff=True), "winner_cost": winner_cost(NF, fn)}
                            for k, fn in comps.items()}
    def s15(r):
        if card(r) != 0: return None
        if f(r["S1"]) == 1 or f(r["S5"]) == 1: return 1
        return 0 if f(r["S1"]) == 0 else None
    R["E"]["S1S5_incremental"] = {"H12": rr_test(NF, s15, "halve12"), "FAIL3": rr_test(NF, s15, "fail3"),
                                  "XS156": rr_test(NF, s15, "xs156", diff=True)}
    yr = lambda r: int(r["entry"][:4])
    R["E"]["sens"] = {
        "all_events_incl_fin": e_block(E, card),
        "RED_incl_S5": e_block(NF, red),
        "unknown_as_0": e_block(NF, lambda r: card(r, u0=True)),
        "live_only": e_block([r for r in NF if r["u"] == "L"], card),
        "2018_21": e_block([r for r in NF if yr(r) <= 2021], card),
        "2022_25": e_block([r for r in NF if yr(r) >= 2022], card),
        "B50_only_vs_rest": e_block(NF, comps["B50"]),
    }
    # P
    pcard = lambda r: card(r, "B25", "s2")
    for nm, fn in (("CARD", pcard), ("B25", lambda r: None if f(r["B25"]) is None else int(f(r["B25"]))),
                   ("B50", lambda r: None if f(r["B50"]) is None else int(f(r["B50"]))),
                   ("S2", lambda r: None if f(r["s2"]) is None else int(f(r["s2"]))),
                   ("S1", lambda r: None if f(r["s1"]) is None else int(f(r["s1"]))),
                   ("S5", lambda r: None if f(r["s5"]) is None else int(f(r["s5"]))),
                   ("CARD_u0", lambda r: card(r, "B25", "s2", u0=True))):
        R["P"][nm] = {"H12": p_test(P, fn, "h12"), "O_fail": p_test(P, fn, "o_fail"),
                      "O_strict": p_test(P, fn, "o_strict"), "WIN5": p_test(P, fn, "winner"),
                      "XS52": p_test(P, fn, "xs52", True), "XS156": p_test(P, fn, "xs156", True),
                      "winner_cost": p_winner_cost(P, fn), "unknown": sum(fn(r) is None for r in P)}
    # verdict
    h = R["E"]["primary_nonfin_CARD"]["H12"]
    P1 = h["rr"] >= 2.0 and h["ci"][0] > 1.3
    ph, pf = R["P"]["CARD"]["H12"], R["P"]["CARD"]["O_fail"]
    P2 = any(x["rr"] >= 1.5 and x["ci"][0] > 1.0 for x in (ph, pf))
    # return-cost override as pre-registered: flagged firms' 3y mean excess positive with firm-cluster CI lb > 0
    m_fl = R["E"]["primary_nonfin_CARD"]["XS156"]["m1"]
    M = cluster_stats([r for r in NF if card(r) == 1], lambda r: 1, "xs156", "sym")
    rng = np.random.default_rng(SEED); idx = rng.integers(0, len(M), size=(B, len(M))); S = M[idx].sum(1)
    ci_fl = ci(S[:, 1] / S[:, 0])
    override = m_fl > 0 and ci_fl[0] > 0
    s = R["E"]["S1S5_incremental"]["H12"]
    R["verdict"] = {"P1": P1, "P2": P2, "return_cost_override": override,
                    "flagged_xs156_mean": round(m_fl, 4), "flagged_xs156_ci": ci_fl,
                    "S1S5_joins": bool(s and s["rr"] and s["rr"] >= 2.0 and s["ci"][0] > 1.3),
                    "decision": ("ADOPT" if P1 and P2 and not override else "PROVISIONAL" if P1 else "NOT ADOPTED")}
    json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=float)
    print(json.dumps(R["verdict"], indent=1))
    print(json.dumps(R["E"]["primary_nonfin_CARD"], indent=0)[:3000])


if __name__ == "__main__":
    main()
