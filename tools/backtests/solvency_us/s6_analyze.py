#!/usr/bin/env python3
"""Step 6: outcomes + per-flag statistics with CIK-clustered bootstrap; verdict per the pre-registered rule.
Writes BASE/panel.jsonl, BASE/results.json and prints markdown tables."""
import json, re, sys
from datetime import date, datetime, timezone, timedelta
import numpy as np
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import p, SNAPS

FLAGS = ["S1", "S2", "S3", "S4", "S5", "S1raw", "S0"]
CANDIDATES = ["S1", "S2", "S3", "S4", "S5"]
rng = np.random.default_rng(20261121)


def load_px(t):
    try:
        d = json.load(open(p("prices", t.replace("/", "_") + ".json")))
    except FileNotFoundError:
        return None
    if d.get("missing"):
        return None
    ds = [datetime.fromtimestamp(x, timezone.utc).date() for x in d["t"]]
    sp = [(datetime.fromtimestamp(int(k), timezone.utc).date(), v["numerator"] / v["denominator"]) for k, v in (d.get("splits") or {}).items()] if isinstance(d.get("splits"), dict) else []
    return ds, d["close"], d["adj"], sp


def price_outcome(r, tick):
    T = date.fromisoformat(r["T"]); E = T.replace(year=T.year + 5)
    tried = []
    for t in tick["current"] + tick["instance"]:
        s = load_px(t)
        if not s:
            tried.append((t, "no yahoo")); continue
        ds, cl, adj, sp = s
        idx = [i for i, x in enumerate(ds) if x <= T and adj[i] is not None and cl[i] is not None]
        if not idx or (T - ds[idx[-1]]).days > 7:
            tried.append((t, "no price at T")); continue
        i0 = idx[-1]
        raw0 = cl[i0] * np.prod([f for dd, f in sp if dd > ds[i0]] or [1.0])
        chk = None
        if r.get("shares"):
            chk = raw0 * r["shares"] / r["float"]
            if not (0.4 <= chk <= 8):
                tried.append((t, f"identity fail {chk:.2f}")); continue
        p0 = adj[i0]
        win = [(ds[i], adj[i]) for i in range(i0 + 1, len(ds)) if ds[i] <= E and adj[i] is not None]
        # month-end closes
        me = {}
        for dd, v in win:
            me[(dd.year, dd.month)] = v
        mn = min(me.values()) if me else None
        last = win[-1] if win else None
        full = last is not None and (E - last[0]).days <= 10
        return {"ticker": t, "p0": p0, "mcap_px": raw0 * r["shares"] if r.get("shares") else None, "id_ratio": chk,
                "O_px": int(mn is not None and mn <= 0.2 * p0), "min_ratio": (mn / p0) if mn else None,
                "R5": (last[1] / p0) if full else None, "px_status": "full" if full else "truncated", "tried": tried}
    return {"ticker": None, "O_px": 0, "R5": None, "px_status": "none", "tried": tried, "min_ratio": None}


def boot_stats(rows, f, outcome, B=2000):
    k = [r for r in rows if r[f] is not None]
    if not k:
        return None
    ciks = sorted({r["cik"] for r in k}); ci = {c: i for i, c in enumerate(ciks)}
    g = np.array([ci[r["cik"]] for r in k]); F = np.array([r[f] for r in k]); O = np.array([r[outcome] for r in k])
    W = np.array([1 if (r["R5"] is not None and r["R5"] > 3) else 0 for r in k]); Wk = np.array([r["R5"] is not None for r in k])
    nC = len(ciks)
    # per-cluster sums for fast bootstrap
    def sums(mask):
        return np.bincount(g, weights=mask.astype(float), minlength=nC)
    cN = sums(np.ones_like(F)); cF = sums(F == 1); cO = sums(O == 1); cFO = sums((F == 1) & (O == 1))
    cW = sums((W == 1) & Wk); cFW = sums((F == 1) & (W == 1) & Wk)
    def stat(w):
        n, nf, no, nfo, nw, nfw = (w @ x for x in (cN, cF, cO, cFO, cW, cFW))
        base = no / n if n else np.nan; prec = nfo / nf if nf else np.nan
        unf = (no - nfo) / (n - nf) if n - nf else np.nan
        return np.array([prec, base, prec / base if base else np.nan, prec / unf if unf else np.nan,
                         nfo / no if no else np.nan, nfw / nw if nw else np.nan])
    pt = stat(np.ones(nC))
    bs = np.array([stat(np.bincount(rng.integers(0, nC, nC), minlength=nC).astype(float)) for _ in range(B)])
    lo, hi = np.nanpercentile(bs, 2.5, axis=0), np.nanpercentile(bs, 97.5, axis=0)
    names = ["precision", "base", "lift", "rr", "recall", "win_excl"]
    out = {"n": int(len(k)), "n_flag": int(F.sum()), "n_fail": int(O.sum()), "n_flag_fail": int(((F == 1) & (O == 1)).sum()),
           "n_win": int(((W == 1) & Wk).sum()), "n_flag_win": int(((F == 1) & (W == 1) & Wk).sum())}
    for i, nm in enumerate(names):
        out[nm] = float(pt[i]); out[nm + "_ci"] = [float(lo[i]), float(hi[i])]
    ex = [r["exc_" + f] for r in k if r[f] == 1 and r.get("exc_" + f) is not None]
    out["med_excess_flagged"] = float(np.median(ex)) if ex else None; out["n_excess"] = len(ex)
    return out


def verdict(s):
    if s is None or s["n_flag"] == 0:
        return "no data"
    graded = s["lift"] >= 2 and s["lift_ci"][0] > 1 and s["win_excl"] < 0.10
    if graded and s["lift"] >= 4:
        return "HARD"
    if graded:
        return "GRADED RED"
    why = []
    if s["lift"] < 2: why.append(f"lift {s['lift']:.2f} < 2")
    if s["lift_ci"][0] <= 1: why.append("lift CI touches 1")
    if s["win_excl"] >= 0.10: why.append(f"excludes {s['win_excl']:.0%} of >3x winners")
    return "QUESTION (" + "; ".join(why) + ")"


def main():
    U = [json.loads(l) for l in open(p("universe.jsonl"))]
    ev = {(e["cik"], e["T"]): e for e in map(json.loads, open(p("events.jsonl")))}
    tick = {int(k): v for k, v in json.load(open(p("tickers.json"))).items()}
    c301 = json.load(open(p("item301_class.json")))
    GOV = re.compile(r"audit committee|independent director|annual meeting|compensation committee|board", re.I)
    panel = []
    for r in U:
        r.update(ev[(r["cik"], r["T"])]); r.update(price_outcome(r, tick[r["cik"]]))
        # Deviation (documented in report): as-registered O_delist was dominated by voluntary exchange transfers.
        # Revised: a substantive listing-rule failure notice (text-classified; governance-composition notices excluded)
        # followed by a Form 25/15 in the window, no merger evidence.
        k3 = c301.get(f"{r['cik']}|{r['T']}")
        subst = [d for d in (k3 or {}).get("docs", []) if d["cause"] and not d["transfer"] and not GOV.search(d["snip"])]
        r["O_delist_asreg"] = r["O_delist"]
        r["O_delist"] = int(bool(subst) and r["delist_date"] is not None and r["delist_date"] >= subst[0]["date"])
        r["O_fail_asreg"] = int(r["O_bk"] or r["O_delist_asreg"] or r["O_px"])
        r["O_fail"] = int(r["O_bk"] or r["O_delist"] or r["O_px"]); r["O_strict"] = int(r["O_bk"] or r["O_delist"])
        r["sens_ok"] = r["px_status"] == "full" or r["O_strict"] == 1 or r["O_px"] == 1
        panel.append(r)
    # size quintile by float within snapshot; size-matched excess per flag
    for Ts in SNAPS:
        rs = [r for r in panel if r["T"] == Ts]
        qs = np.quantile([r["float"] for r in rs], [0.2, 0.4, 0.6, 0.8])
        for r in rs:
            r["sizeq"] = int(np.searchsorted(qs, r["float"]))
        for f in FLAGS:
            for q in range(5):
                ctrl = [r["R5"] for r in rs if r["sizeq"] == q and r[f] == 0 and r["R5"] is not None]
                med = float(np.median(ctrl)) if ctrl else None
                for r in rs:
                    if r["sizeq"] == q:
                        r["exc_" + f] = (r["R5"] - med) if (r["R5"] is not None and med is not None) else None
    with open(p("panel.jsonl"), "w") as fo:
        for r in panel:
            fo.write(json.dumps(r, default=str) + "\n")
    res = {}
    sets = {"pooled": panel, **{Ts: [r for r in panel if r["T"] == Ts] for Ts in SNAPS}}
    for nm, rs in sets.items():
        for oc in (["O_fail", "O_strict", "O_fail_asreg"] if nm == "pooled" else ["O_fail", "O_strict"]):
            for f in FLAGS:
                res[f"{nm}|{oc}|{f}"] = boot_stats(rs, f, oc, B=2000 if nm == "pooled" else 1000)
    sens = [r for r in panel if r["sens_ok"]]
    for f in FLAGS:
        res[f"sens_priced|O_fail|{f}"] = boot_stats(sens, f, "O_fail", B=1000)
    for f in CANDIDATES:
        res["verdict|" + f] = verdict(res[f"pooled|O_fail|{f}"])
    json.dump(res, open(p("results.json"), "w"), indent=1)
    # print tables
    def row(f, s):
        if not s: return f"| {f} | – |"
        c = lambda k: f"{s[k]:.2f} [{s[k+'_ci'][0]:.2f}, {s[k+'_ci'][1]:.2f}]"
        pc = lambda k: f"{s[k]:.1%} [{s[k+'_ci'][0]:.1%}, {s[k+'_ci'][1]:.1%}]"
        me = f"{s['med_excess_flagged']:+.2f}" if s["med_excess_flagged"] is not None else "–"
        return (f"| {f} | {s['n']} / {s['n_flag']} ({s['n_flag']/s['n']:.0%}) | {s['n_flag_fail']} / {s['n_fail']} | {pc('precision')} | "
                f"{s['base']:.1%} | {c('lift')} | {s['rr']:.2f} | {pc('recall')} | {s['n_flag_win']} / {s['n_win']} = {pc('win_excl')} | {me} |")
    hdr = ("| Flag | known / fired | fired&fail / all fail | precision | base | lift [95% CI] | RR vs unflagged | recall | >3x winners excluded | median size-matched excess R5 (flagged) |\n"
           "|---|---|---|---|---|---|---|---|---|---|")
    for nm in list(sets) + ["sens_priced"]:
        for oc in ((["O_fail", "O_strict", "O_fail_asreg"] if nm == "pooled" else ["O_fail", "O_strict"]) if nm in sets else ["O_fail"]):
            print(f"\n### {nm} — {oc}\n" + hdr)
            for f in FLAGS:
                print(row(f, res.get(f"{nm}|{oc}|{f}")))
    print("\nVERDICTS:", {f: res["verdict|" + f] for f in CANDIDATES})


if __name__ == "__main__":
    main()
