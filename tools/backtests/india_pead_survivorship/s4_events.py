#!/usr/bin/env python3
"""Step 4: weekly-close PEAD events for LIVE (v1 sample) and MISSING (sampled dead/off-series firms), same rules.
SUE, standalone EPS, D8 event dates, unit/shares logic: copied from v1 s4_events.py. Changes (pre-registered):
weekly closes (Friday-labelled) for everyone; entry = first weekly close strictly after the event date (<= 10 days);
exit = last weekly close dated <= entry + h weeks + 3 days (a delisted firm's return runs to its last traded close);
controls = universe firms with a close on the entry Friday, mcap x0.5-x2, >= 5, same exit rule, computed separately
within ALL and within LIVE. Usage: python3 s4_events.py -> $OUT/events_w.tsv, $OUT/s4_funnel.json"""
import bisect, collections, csv, datetime as dt, glob, json, math, os, statistics as st, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

HW = (4, 13, 26)
D0, D1 = dt.date(2018, 1, 1), dt.date(2025, 12, 31)
funnel = collections.Counter()
miss = {r["symbol"]: r for r in csv.DictReader(open(os.path.join(K.OUT, "missing.csv"))) if r["sampled"] == "1"}


def fri(d): return d + dt.timedelta(days=4 - d.weekday()) if d.weekday() <= 4 else d - dt.timedelta(days=d.weekday() - 4)


def split_factor(sp, after):
    f = 1.0
    for sd, ratio in sp:
        if sd > after: f *= ratio
    return f


def load_px(root, sym, weekly_src):
    fn = os.path.join(root, "prices", sym + ".json")
    if not os.path.exists(fn): return None
    try:
        r = json.load(open(fn))["chart"]["result"][0]
        q = r["indicators"]["quote"][0]
        sp = sorted((dt.date.fromtimestamp(int(k)), v["numerator"] / v["denominator"])
                    for k, v in (r.get("events", {}).get("splits") or {}).items())
    except Exception:
        return None
    wk = {}
    for t, cl in zip(r["timestamp"], q["close"]):
        if cl is None or cl <= 0: continue
        dd = dt.date.fromtimestamp(t)
        f = fri(dd)
        if f not in wk or dd >= wk[f][0]: wk[f] = (dd, cl)      # last close of the Mon-Fri week
    d = sorted(wk)
    c = [wk[x][1] for x in d]
    sf = [split_factor(sp, wk[x][0]) for x in d]                 # adjusted -> unadjusted factor at that close
    if len(d) < 60: return None
    return {"d": d, "c": c, "sf": sf}


def qkey(d): return d.year * 4 + (d.month - 1) // 3


def load_universe(root, syms, tag):
    data = {}
    for sym in syms:
        fn = os.path.join(root, "results", sym + ".json")
        if not os.path.exists(fn): funnel[tag + "_no_results_file"] += 1; continue
        j = json.load(open(fn))
        funnel[tag + "_status_" + j["status"]] += 1
        if j["status"] != "ok": continue
        px = load_px(root, sym, tag == "M")
        if not px: funnel[tag + "_no_prices"] += 1; continue
        ann = []
        af = os.path.join(root, "ann", sym + ".json")
        if os.path.exists(af):
            for t, _ in json.load(open(af)):
                try: ann.append(dt.datetime.strptime(t, "%d-%b-%Y %H:%M:%S"))
                except Exception: pass
        else: funnel[tag + "_no_ann_file"] += 1
        ann.sort()
        qs = []
        for q in j["quarters"]:
            qe = dt.date.fromisoformat(q["qe"]); ev = dt.datetime.strptime(q["event"], "%Y-%m-%d %H:%M:%S")
            if qe.month not in (3, 6, 9, 12): continue
            c = [t for t in ann if qe < t.date() <= ev.date()]
            if c: q["ev_src"] = "ann" if c[0].date() < ev.date() else "ann_same"; ev = c[0]
            else: q["ev_src"] = "feed"
            qs.append(dict(q, qe=qe, ev=ev))
        xs = [q["pdup"] / q["face"] for q in qs if q.get("src") == "xbrl" and q.get("pdup") and q.get("face")]
        ds = [q["pdup"] * q["unit"] / q["face"] for q in qs if q.get("src") == "detail" and q.get("pdup") and q.get("face")]
        adj = 1.0
        if xs and ds:
            rr = st.median(ds) / st.median(xs)
            if not 0.3 < rr < 3: adj = 10 ** -round(math.log10(rr)); funnel[tag + "_unit_rescaled"] += 1
        # EPS split adjustment (v1 D2): LIVE uses Yahoo splits; MISSING has none (stated bias)
        for q in qs:
            u = (q.get("unit") or 1.0) * (adj if q.get("src") == "detail" else 1.0)
            q["sh"] = q["pdup"] * u / q["face"] if q.get("pdup") and q.get("face") else None
            q["eps_a"] = q["eps"] / sf_at(px, q["ev"].date()) if q.get("eps") is not None else None
        hist = []
        for q in qs:
            if q["sh"]: hist.append(q["sh"])
            q["sh_r"] = st.median(hist[-3:]) if hist else None
        filings = sorted((q["ev"].date(), q["sh_r"]) for q in qs if q["sh_r"])
        fd = [f[0] for f in filings]
        mc = []
        for i, d in enumerate(px["d"]):
            k = bisect.bisect_right(fd, d) - 1
            mc.append(px["c"][i] * px["sf"][i] * filings[k][1] / 1e7 if k >= 0 else np.nan)
        px["mc"] = mc; px["di"] = {d: i for i, d in enumerate(px["d"])}
        data[sym] = {"px": px, "q": {qkey(q["qe"]): q for q in qs}, "u": tag}
    return data


def sf_at(px, d):
    """split factor (Yahoo) for EPS reported at d: ratio of unadjusted/adjusted at d vs today (= product of later splits)."""
    i = bisect.bisect_right(px["d"], fri(d)) - 1
    return px["sf"][max(i, 0)]


def sue(qd, k, field="eps_a"):
    def chg(kk):
        a, b = qd.get(kk), qd.get(kk - 4)
        if not a or not b or a.get(field) is None or b.get(field) is None: return None
        return a[field] - b[field]
    d0 = chg(k)
    if d0 is None: return None, 0
    prev = [x for x in (chg(k - i) for i in range(1, 9)) if x is not None]
    if len(prev) < 4: return None, len(prev)
    sd = st.stdev(prev)
    if sd <= 0: return None, len(prev)
    return d0 / sd, len(prev)


def exit_idx(px, i0, h):
    tgt = px["d"][i0] + dt.timedelta(days=7 * h + 3)
    j = bisect.bisect_right(px["d"], tgt) - 1
    return j, px["d"][j] < px["d"][i0] + dt.timedelta(days=7 * h - 3)   # (index, ended early)


live_syms = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(K.V1, "results", "*.json")))
data = load_universe(K.V1, live_syms, "L")
data.update(load_universe(K.OUT, sorted(miss), "M"))
print("symbols: live", sum(v["u"] == "L" for v in data.values()), "missing", sum(v["u"] == "M" for v in data.values()), flush=True)

rows = []
for sym, v in data.items():
    px = v["px"]; d = px["d"]
    for k, q in v["q"].items():
        ev = q["ev"].date()
        if not (D0 <= ev <= D1): continue
        funnel[v["u"] + "_ev_in_window"] += 1
        if (ev - q["qe"]).days > 150: funnel[v["u"] + "_drop_late_filing"] += 1; continue
        s, n = sue(v["q"], k)
        if s is None: funnel[v["u"] + "_drop_no_sue"] += 1; continue
        i0 = bisect.bisect_right(d, ev)
        if i0 >= len(d): funnel[v["u"] + "_drop_no_entry_px"] += 1; continue
        if (d[i0] - ev).days > 10: funnel[v["u"] + "_drop_price_gap"] += 1; continue
        if i0 < 50: funnel[v["u"] + "_drop_short_history"] += 1; continue
        mc = px["mc"][i0]
        if not mc == mc: funnel[v["u"] + "_drop_no_shares"] += 1; continue
        if not (500 <= mc <= 50000): funnel[v["u"] + "_drop_mcap_range"] += 1; continue
        m = miss.get(sym, {})
        rec = {"sym": sym, "u": v["u"], "cls": m.get("cls", "live"), "distress": int(m.get("distress", 0) or 0),
               "qe": str(q["qe"]), "event": q["ev"].strftime("%Y-%m-%d %H:%M"), "entry": str(d[i0]),
               "mcap_cr": round(mc, 1), "sue": s, "n_prev": n, "ev_src": q["ev_src"], "_i0": i0}
        ok = True
        for h in HW:
            j, early = exit_idx(px, i0, h)
            if j <= i0: rec[f"r{h}"] = None; ok = ok and h != 13; continue
            rec[f"r{h}"] = px["c"][j] / px["c"][i0] - 1; rec[f"early{h}"] = int(early)
        if rec.get("r13") is None: funnel[v["u"] + "_drop_no_close_after_entry"] += 1; continue
        rows.append(rec); funnel[v["u"] + "_events_kept"] += 1
print("events:", len(rows), flush=True)

# controls per (entry Friday, horizon) within ALL and within LIVE; variants for sensitivities
syms = list(data)
need = collections.defaultdict(list)
for r in rows: need[r["entry"]].append(r)
for n_, (ent, lst) in enumerate(sorted(need.items())):
    a = dt.date.fromisoformat(ent)
    for h in HW:
        m, ret, early, isL, pen, who = [], [], [], [], [], []
        for s2 in syms:
            v2 = data[s2]; px2 = v2["px"]; ia = px2["di"].get(a)
            if ia is None or ia < 50: continue
            mm = px2["mc"][ia]
            if not mm == mm: continue
            j, e = exit_idx(px2, ia, h)
            if j <= ia: continue
            rr = px2["c"][j] / px2["c"][ia] - 1
            dist = v2["u"] == "M" and miss[s2]["distress"] == "1"
            m.append(mm); ret.append(rr); early.append(e); isL.append(v2["u"] == "L"); who.append(s2)
            pen.append((1 + rr) * 0.7 - 1 if (e and dist) else rr)
        m, ret, early, isL, pen, who = map(np.array, (m, ret, early, isL, pen, who))
        for r in lst:
            if r.get(f"r{h}") is None: continue
            base = (m >= 0.5 * r["mcap_cr"]) & (m <= 2 * r["mcap_cr"]) & (who != r["sym"])
            for name, sel, vals in (("cA", base, ret), ("cL", base & isL, ret), ("cP", base, pen),
                                    ("cS", base & ~early, ret)):
                r[f"{name}{h}"] = float(vals[sel].mean()) if sel.sum() >= 5 else None
                if name in ("cA", "cL"): r[f"n{name}{h}"] = int(sel.sum())
            e = r.get(f"early{h}", 0)
            r[f"rP{h}"] = (1 + r[f"r{h}"]) * 0.7 - 1 if (e and r["distress"]) else r[f"r{h}"]
    if n_ % 100 == 0: print("controls", n_, len(need), flush=True)

cols = ["sym", "u", "cls", "distress", "qe", "event", "entry", "mcap_cr", "sue", "n_prev", "ev_src"] + \
       [f"{p}{h}" for h in HW for p in ("r", "early", "rP", "cA", "ncA", "cL", "ncL", "cP", "cS")]
with open(os.path.join(K.OUT, "events_w.tsv"), "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in rows:
        f.write("\t".join("" if r.get(c) is None else (f"{r[c]:.6g}" if isinstance(r[c], float) else str(r[c]))
                          for c in cols) + "\n")
json.dump(funnel, open(os.path.join(K.OUT, "s4_funnel.json"), "w"), indent=1)
print(dict(funnel))
