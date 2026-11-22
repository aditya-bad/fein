#!/usr/bin/env python3
"""Step 4: weighted flag-vs-outcome statistics with stratified, company-clustered bootstrap CIs (2,000 draws),
pre-registered verdicts, survivorship audit. Output: solvency_india_outputs/results.json, tables.md."""
import collections, json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

FLAGS = [("s1", "S1 net worth < 0 (adj.)", "candidate"), ("s1raw", "S1raw net worth < 0", "secondary"),
         ("s2", "S2 interest cover < 1.5x", "candidate"), ("s2b", "S2b interest cover < 2.5x", "candidate"),
         ("s4", "S4 dividends > FCF while debt rose", "candidate"), ("s5", "S5-India >= 2 of S1,S2,S4", "candidate"),
         ("s5b", "S5b-India >= 2 of S1,S2b,S4", "exploratory"), ("s3", "S3 US funding gap", "reported only"),
         ("s3_india", "S3-India STD > cash+inv+0.5 CFO", "exploratory"), ("s5_us", "S5-US >= 2 of S1-S4", "exploratory"),
         ("s0", "S0 EBIT < 0 (reference)", "reference")]
B = 2000


def num(v):
    if v in ("", None):
        return np.nan
    return float(v)


def load():
    rows = K.read_csv(os.path.join(K.OUTDIR, "panel.csv"))
    return rows


def stats(rows, flag, out, boot=True, seed=7):
    sel = [r for r in rows if r.get(flag) not in ("", None)]
    if not sel:
        return None
    w = np.array([float(r["weight"]) for r in sel])
    f = np.array([num(r[flag]) for r in sel])
    o = np.array([num(r[out]) for r in sel])
    win = np.array([num(r["winner"]) for r in sel])
    keys = [r["key"] for r in sel]
    strata = [r["stratum"] for r in sel]

    def calc(m):
        ww = w * m
        tot, fo = ww.sum(), (ww * o).sum()
        nf = (ww * f).sum()
        if tot == 0 or fo == 0 or nf == 0:
            return dict(base=np.nan, prec=np.nan, lift=np.nan, recall=np.nan, rr=np.nan, wexcl=np.nan)
        base = fo / tot
        prec = (ww * f * o).sum() / nf
        un = ((ww * (1 - f)).sum())
        p_un = (ww * (1 - f) * o).sum() / un if un else np.nan
        wk = ~np.isnan(win)
        wins = (ww[wk] * win[wk]).sum()
        return dict(base=base, prec=prec, lift=prec / base, recall=(ww * f * o).sum() / fo,
                    rr=prec / p_un if p_un else np.nan,
                    wexcl=(ww[wk] * win[wk] * f[wk]).sum() / wins if wins else np.nan)
    pt = calc(np.ones(len(sel)))
    res = {"n_known": len(sel), "n_fired": int(np.nansum(f)), "n_fail": int(np.nansum(o)),
           "n_fired_fail": int(np.nansum(f * o)), "n_winners": int(np.nansum(win)),
           "n_fired_winners": int(np.nansum(np.nan_to_num(win) * f)),
           "w_fired_share": float((w * f).sum() / w.sum())}
    res.update({k: float(v) for k, v in pt.items()})
    if boot:
        rng = np.random.default_rng(seed)
        comp = sorted(set(keys))
        cidx = {c: i for i, c in enumerate(comp)}
        rc = np.array([cidx[k] for k in keys])
        cstr = {}
        for k, s in zip(keys, strata):
            cstr[k] = s
        groups = collections.defaultdict(list)
        for c in comp:
            groups[cstr[c]].append(cidx[c])
        draws = collections.defaultdict(list)
        for _ in range(B):
            mult = np.zeros(len(comp))
            for s, g in groups.items():
                pick = rng.integers(0, len(g), len(g))
                np.add.at(mult, np.array(g)[pick], 1)
            m = mult[rc]
            for k, v in calc(m).items():
                draws[k].append(v)
        for k in ("lift", "prec", "recall", "wexcl", "base"):
            arr = np.array(draws[k], dtype=float)
            arr = arr[~np.isnan(arr)]
            res[k + "_ci"] = [float(np.percentile(arr, 2.5)), float(np.percentile(arr, 97.5))] if len(arr) > 50 else None
    return res


def verdict(r):
    if r is None or np.isnan(r["lift"]):
        return "no data"
    ci = r.get("lift_ci")
    red = r["lift"] >= 2 and ci and ci[0] > 1 and (np.isnan(r["wexcl"]) or r["wexcl"] < 0.10)
    if red and r["lift"] >= 4:
        return "HARD"
    return "GRADED RED" if red else "question"


def pct(x):
    return "n/a" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{100 * x:.1f}%"


def f2(x):
    return "n/a" if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.2f}"


def ci(c, p=False):
    if not c:
        return "n/a"
    return f"[{pct(c[0])}, {pct(c[1])}]" if p else f"[{c[0]:.2f}, {c[1]:.2f}]"


def table(rows, out, title, boot=True):
    md = [f"### {title}", "", "| flag | role | known | fired | fired & failed | wtd fired share | precision | base rate | "
          "lift [95% CI] | recall | winners excluded | verdict |", "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    res = {}
    for k, lab, role in FLAGS:
        r = stats(rows, k, out, boot)
        res[k] = r
        if r is None:
            continue
        v = verdict(r) if role == "candidate" else f"({verdict(r)})"
        md.append(f"| {lab} | {role} | {r['n_known']} | {r['n_fired']} | {r['n_fired_fail']} | {pct(r['w_fired_share'])} | "
                  f"{pct(r['prec'])} | {pct(r['base'])} | {f2(r['lift'])} {ci(r.get('lift_ci'))} | {pct(r['recall'])} | "
                  f"{pct(r['wexcl'])} ({r['n_fired_winners']}/{r['n_winners']}) | {v} |")
    return md, res


def main():
    rows = load()
    out = {"n_rows": len(rows)}
    md = ["# Indian solvency back-test — tables (generated by s4_analyze.py)", "",
          "Weighted by stratum (D census, X and L samples). Counts are unweighted rows; rates are weighted. "
          "CIs: 2,000 stratified bootstrap draws by company. Research, not SEBI-registered advice.", ""]
    # composition
    comp = collections.Counter((r["snap"], r["stratum"]) for r in rows)
    md += ["## Panel composition (rows)", "", "| snapshot | D | X | L | total | O_fail | O_strict | O_cirp | winners |",
           "|---|---|---|---|---|---|---|---|---|"]
    for sn in list(K.SNAPS) + ["pooled"]:
        rr = rows if sn == "pooled" else [r for r in rows if r["snap"] == sn]
        md.append(f"| {sn} | " + " | ".join(str(sum(r['stratum'] == s for r in rr)) for s in "DXL") +
                  f" | {len(rr)} | {sum(r['o_fail'] == '1' for r in rr)} | {sum(r['o_strict'] == '1' for r in rr)} | "
                  f"{sum(r['o_cirp'] == '1' for r in rr)} | {sum(r['winner'] == '1' for r in rr)} |")
    md.append("")
    m, res = table(rows, "o_fail", "Pooled — primary O_fail (liquidation ∨ compulsory exit ∨ price ≤ 0.2×)")
    md += m + [""]
    out["pooled_o_fail"] = res
    out["verdicts"] = {k: verdict(res[k]) for k, _, role in FLAGS if role == "candidate"}
    m, res = table(rows, "o_strict", "Pooled — O_strict (liquidation ∨ compulsory exit; no price)")
    md += m + [""]
    out["pooled_o_strict"] = res
    for sn in K.SNAPS:
        m, res = table([r for r in rows if r["snap"] == sn], "o_fail", f"{sn} only — O_fail")
        md += m + [""]
        out[sn + "_o_fail"] = res
    m, res = table([r for r in rows if r["size_ambiguous"] == "0"], "o_fail",
                   "Sensitivity — drop size-ambiguous rows")
    md += m + [""]
    out["no_ambiguous_o_fail"] = res
    m, res = table([r for r in rows if r["stratum"] == "L"], "o_fail",
                   "Sensitivity — live stratum L only (unweighted within stratum; survivor-tilted)")
    md += m + [""]
    out["L_only_o_fail"] = res
    # CIRP admissions
    adm = [r for r in rows if r["o_cirp"] == "1"]
    md += ["## CIRP admissions in the window (not counted as failure)", "",
           f"{len(adm)} rows admitted; of these {sum(r['o_fail'] == '1' for r in adm)} also failed (O_fail), "
           f"{sum(r['o_liq'] == '1' for r in adm)} liquidated.", "",
           "| flag | admitted rows flagged / known | admission rate flagged | admission rate unflagged (weighted) |",
           "|---|---|---|---|"]
    out["cirp"] = {}
    for k, lab, _ in FLAGS:
        kn = [r for r in rows if r.get(k) not in ("", None)]
        fl = [r for r in kn if r[k] == "1"]
        un = [r for r in kn if r[k] == "0"]
        wr = lambda g: sum(float(r["weight"]) * (r["o_cirp"] == "1") for r in g) / max(sum(float(r["weight"]) for r in g), 1e-9)
        a1 = sum(r["o_cirp"] == "1" for r in fl)
        a_all = sum(r["o_cirp"] == "1" for r in kn)
        md.append(f"| {lab} | {a1} / {a_all} | {pct(wr(fl))} | {pct(wr(un))} |")
        out["cirp"][k] = {"admitted_flagged": a1, "admitted_known": a_all, "rate_flagged": wr(fl), "rate_unflagged": wr(un)}
    md.append("")
    # failure components
    comp_ct = {c: sum(r[c] == "1" for r in rows) for c in ("o_liq", "o_cdel", "o_px", "o_fail", "o_strict", "o_cirp",
                                                           "stopped_in_window", "liq_undated", "size_ambiguous")}
    out["components"] = comp_ct
    md += ["## Outcome components (rows)", "", ", ".join(f"{k} {v}" for k, v in comp_ct.items()), ""]
    # failures by stratum
    md += ["## Failures by stratum (rows)", "", "| stratum | rows | O_fail | O_strict | weight |", "|---|---|---|---|---|"]
    for s in "DXL":
        g = [r for r in rows if r["stratum"] == s]
        if g:
            md.append(f"| {s} | {len(g)} | {sum(r['o_fail'] == '1' for r in g)} | {sum(r['o_strict'] == '1' for r in g)} | {g[0]['weight']} |")
    md.append("")
    # flagged failures list (S1 or S5)
    md += ["## Failures caught by S1 or S5-India (first 40)", "", "| snapshot | company | flags | outcome |", "|---|---|---|---|"]
    n = 0
    for r in sorted(rows, key=lambda r: (r["snap"], r["name"])):
        if r["o_fail"] == "1" and (r["s1"] == "1" or r["s5"] == "1") and n < 40:
            fl = ",".join(k.upper() for k in ("s1", "s2", "s3", "s4") if r[k] == "1")
            oc = ",".join(k for k in ("o_liq", "o_cdel", "o_px") if r[k] == "1")
            md.append(f"| {r['snap']} | {r['name']} ({r['slug']}) | {fl} | {oc}; min {r['min_ratio']} |")
            n += 1
    md.append("")
    K.jsave(os.path.join(K.OUTDIR, "results.json"), out)
    with open(os.path.join(K.OUTDIR, "tables.md"), "w") as fh:
        fh.write("\n".join(md) + "\n")
    print("\n".join(md[:60]))
    print(json.dumps(out["verdicts"]))


if __name__ == "__main__":
    main()
