#!/usr/bin/env python3
"""Step 4: returns vs sector-and-size-matched controls (pre-registered design, §0 of the report).
Inputs: OUT/firms/*.json, OUT/sc/<SYM>/chart.json, OUT/firmyears.json, and the hand check of H3 flags
(research_notes/Backtests/india_annual_report_text_outputs/auditor_flags_checked.tsv, column `confirmed` = Y/N).
Writes OUT/results.json and OUT/events.tsv (+ copies to the report outputs dir)."""
import bisect, csv, datetime as dt, glob, json, math, os, random, re, shutil, statistics as stt, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402
D = dt.date


def series(sym):
    ch = K.jload(os.path.join(K.OUT, "sc", sym, "chart.json"), {}) or {}
    ds = {d["metric"]: d["values"] for d in ch.get("datasets", [])}
    px = [(D.fromisoformat(a), float(b)) for a, b, *_ in ds.get("Price", []) if b not in (None, "") and float(b) > 0]
    mcs = {D.fromisoformat(a): float(c) for a, c, *_ in ds.get("Market Cap to Sales", []) if c not in (None, "")}
    sales = [(D.fromisoformat(a), float(b)) for a, b, *_ in ds.get("Sales", []) if b not in (None, "")]
    return px, mcs, sales


class Firm:
    def __init__(self, st):
        self.sym, self.st = st["sym"], st
        lab = st.get("labels") or {}
        self.sector, self.bsector = lab.get("Sector", ""), lab.get("Broad Sector", "")
        self.px, self.mcs, self.sales = series(st["sym"])
        self.d = [x[0] for x in self.px]

    def close_after(self, day, maxgap=21):
        i = bisect.bisect_right(self.d, day)
        if i < len(self.d) and (self.d[i] - day).days <= maxgap:
            return i
        return None

    def idx_on_or_before(self, day):
        i = bisect.bisect_right(self.d, day) - 1
        return i if i >= 0 else None

    def mcap(self, i):
        day = self.d[i]
        m = self.mcs.get(day)
        s = [v for x, v in self.sales if x <= day]
        return m * s[-1] if m and s and s[-1] > 0 else None

    def ret(self, d0, d1):
        """return from the last close <= d0 to the last close <= d1; None if no close within 10 days of d0."""
        i = self.idx_on_or_before(d0)
        if i is None or (d0 - self.d[i]).days > 10:
            return None
        j = self.idx_on_or_before(d1)
        return self.px[j][1] / self.px[i][1] - 1, (d1 - self.d[j]).days > 14


def stats(xs, ids, seed=7):
    if not xs:
        return {"n": 0}
    n = len(xs)
    s = sorted(xs)
    lo, hi = s[int(0.05 * (n - 1))], s[int(math.ceil(0.95 * (n - 1)))]
    w = [min(max(x, lo), hi) for x in xs]
    m = stt.mean(xs)
    sd = stt.stdev(xs) if n > 1 else float("nan")
    by = {}
    for x, f in zip(xs, ids):
        by.setdefault(f, []).append(x)
    keys = list(by)
    rnd = random.Random(seed)
    bs = []
    for _ in range(2000):
        smp = [x for k in (rnd.choice(keys) for _ in keys) for x in by[k]]
        bs.append(stt.mean(smp))
    bs.sort()
    return {"n": n, "firms": len(keys), "mean": m, "median": stt.median(xs), "wmean": stt.mean(w),
            "hit": sum(x > 0 for x in xs) / n, "t": m / (sd / math.sqrt(n)) if n > 1 and sd > 0 else None,
            "ci": [bs[50], bs[1949]], "min": s[0], "max": s[-1]}


def main():
    allst = [K.jload(f) for f in glob.glob(os.path.join(K.OUT, "firms", "*.json"))]
    pool = {s["sym"]: Firm(s) for s in allst if s.get("elig") and s.get("el_rank", 10 ** 9) <= 350}
    fy = K.jload(os.path.join(K.OUT, "firmyears.json"), [])
    chk = {}
    cp = os.path.join(K.REPORT_OUT, "auditor_flags_checked.tsv")
    if os.path.exists(cp):
        for r in csv.DictReader(open(cp), delimiter="\t"):
            if r.get("confirmed", "").strip().upper() == "Y":
                chk.setdefault((r["sym"], r["pair"]), set()).add(r["cat"])
    # quintiles within pair-year
    for meas in ("jac_mda", "jac_aud"):
        for p in ("P1", "P2"):
            g = sorted([r for r in fy if r["pair"] == p and r.get(meas) is not None], key=lambda r: r[meas])
            for k, r in enumerate(g):
                r["q_" + meas] = 1 + int(5 * k / len(g))
    for r in fy:
        r["h3"] = bool(chk.get((r["sym"], r["pair"])))
        r["h3_cats"] = sorted(chk.get((r["sym"], r["pair"]), []))
    # events: entry, returns, controls
    ev = []
    for r in fy:
        f = pool.get(r["sym"])
        if not f:
            continue
        sub = D.fromisoformat(r["submitted"][:10])
        i = f.close_after(sub)
        if i is None:
            r["drop"] = "no_close_21d"; continue
        e0 = f.d[i]
        m0 = f.mcap(i)
        out = dict(r, entry=e0.isoformat(), mcap_entry=m0)
        for h, days in (("6", 182), ("12", 365)):
            x = f.ret(e0, e0 + dt.timedelta(days=days))
            out["r" + h], out["ended" + h] = (x if x else (None, None))
        ev.append(out)
    fyset = {(r["sym"], r["pair"]): r for r in fy}

    def controls(e, meas, tier_log):
        f = pool[e["sym"]]
        e0 = D.fromisoformat(e["entry"])
        m0 = e["mcap_entry"]
        if not m0:
            return None, "no_mcap"
        cands = []
        for s, g in pool.items():
            if s == e["sym"]:
                continue
            o = fyset.get((s, e["pair"]))
            if o is not None:
                if meas == "h3":
                    if o.get("h3"):
                        continue
                elif o.get("q_" + meas) is not None and o.get("q_" + meas) == e.get("q_" + meas):
                    continue
            i = g.idx_on_or_before(e0)
            if i is None or (e0 - g.d[i]).days > 10:
                continue
            mc = g.mcap(i)
            if not mc:
                continue
            cands.append((g, mc))
        for tier, key, lo, hi in (("A", "sector", 1 / 3, 3), ("B", "bsector", 1 / 3, 3), ("C", None, 0.5, 2)):
            c = [(g, mc) for g, mc in cands if lo * m0 <= mc <= hi * m0 and
                 (key is None or (getattr(g, key) and getattr(g, key) == getattr(f, key)))]
            if len(c) >= 3 or tier == "C":
                c.sort(key=lambda x: abs(math.log(x[1] / m0)))
                return [g for g, _ in c[:5]], tier
        return None, "none"

    res = {"pool_firms": len(pool), "firmyears": len(fy), "events_priced": len(ev)}
    rows_out = []
    for meas, sel in (("jac_mda", lambda e: e.get("q_jac_mda") == 1), ("jac_aud", lambda e: e.get("q_jac_aud") == 1),
                      ("h3", lambda e: e.get("h3")),
                      ("jac_mda_Q5", lambda e: e.get("q_jac_mda") == 5), ("jac_aud_Q5", lambda e: e.get("q_jac_aud") == 5),
                      ("all_mda", lambda e: e.get("q_jac_mda") is not None),
                      ("all_aud", lambda e: e.get("q_jac_aud") is not None)):
        cm = {"jac_mda_Q5": "jac_mda", "jac_aud_Q5": "jac_aud", "all_mda": "all", "all_aud": "all"}.get(meas, meas)
        for h in ("12", "6"):
            xs, ids, raw, tiers, perpair = [], [], [], {}, {"P1": [], "P2": []}
            for e in ev:
                if not sel(e) or e.get("r" + h) is None:
                    continue
                c, tier = controls(e, cm if cm != "all" else "__none__", tiers)
                tiers[tier] = tiers.get(tier, 0) + 1
                if not c:
                    continue
                e0 = D.fromisoformat(e["entry"]); e1 = e0 + dt.timedelta(days=int(h) * 365 // 12 if h == "6" else 365)
                e1 = e0 + dt.timedelta(days=182 if h == "6" else 365)
                cr = [g.ret(e0, e1) for g in c]
                cr = [x[0] for x in cr if x]
                if not cr:
                    continue
                x = e["r" + h] - stt.mean(cr)
                xs.append(x); ids.append(e["sym"]); raw.append(e["r" + h]); perpair[e["pair"]].append(x)
                if h == "12" and meas in ("jac_mda", "jac_aud", "h3"):
                    rows_out.append([meas, e["sym"], e["pair"], e["entry"], round(e["mcap_entry"] or 0), e.get("sector", ""),
                                     round(e.get(cm) or 0, 4) if cm.startswith("jac") else ";".join(e.get("h3_cats", [])),
                                     round(e["r12"], 4), round(stt.mean(cr), 4), round(x, 4), tier, e.get("ended12")])
            res[f"{meas}_{h}m"] = dict(stats(xs, ids), tiers=tiers, raw_mean=stt.mean(raw) if raw else None,
                                      per_pair={p: (stt.mean(v) if v else None, len(v)) for p, v in perpair.items()})
    os.makedirs(K.REPORT_OUT, exist_ok=True)
    K.jdump(res, os.path.join(K.OUT, "results.json"))
    with open(os.path.join(K.OUT, "events.tsv"), "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["test", "sym", "pair", "entry", "mcap_cr", "sector", "score_or_cats", "r12", "ctrl12", "x12", "tier", "ended_early"])
        w.writerows(rows_out)
    for fn in ("results.json", "events.tsv", "s3_funnel.json", "auditor_flags.tsv"):
        if os.path.exists(os.path.join(K.OUT, fn)):
            shutil.copy(os.path.join(K.OUT, fn), os.path.join(K.REPORT_OUT, fn))
    for k, v in res.items():
        if isinstance(v, dict) and "n" in v:
            if v["n"]:
                print(f"{k:16s} n={v['n']:3d} mean={v['mean']*100:+6.1f}% med={v['median']*100:+6.1f}% w={v['wmean']*100:+6.1f}% "
                      f"hit={v['hit']*100:4.0f}% t={v['t'] if v['t'] is None else round(v['t'],2)} CI=[{v['ci'][0]*100:+.1f},{v['ci'][1]*100:+.1f}] "
                      f"tiers={v['tiers']} pp={ {p: (round(a*100,1) if a is not None else None, n) for p,(a,n) in v['per_pair'].items()} }")
            else:
                print(k, "n=0")
        else:
            print(k, v)


if __name__ == "__main__":
    main()
