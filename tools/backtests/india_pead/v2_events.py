#!/usr/bin/env python3
"""PEAD v2, step 2: build events (rules pre-registered in research_notes/Backtests/india_pead_v2.md).
Differences from v1 s4_events.py: full universe (V2DIR/results), consolidated EPS SUE where the consolidated history
suffices (else standalone; never mixed within one SUE), announcement dates from v1 ann/ cache UNION v2 anndays/,
window 2022-01-01 .. 2026-11-21, horizon returns only when the window has closed (else blank = pending).
Controls: equal-weight mean return of all universe stocks with mcap x0.5-x2 on the entry date (>= 5), same window.
Usage: python3 v2_events.py V1DIR V2DIR  -> V2DIR/events_v2.tsv, V2DIR/events_v2_funnel.json"""
import bisect, collections, datetime as dt, glob, json, math, os, statistics as st, sys
import numpy as np

V1, V2 = sys.argv[1], sys.argv[2]
H = (21, 63, 126)
D0, D1 = dt.date(2022, 1, 1), dt.date(2026, 11, 21)
funnel = collections.Counter()


def load_px(sym):
    fn = next((os.path.join(d, "prices", sym + ".json") for d in (V2, V1)
               if os.path.exists(os.path.join(d, "prices", sym + ".json"))), None)
    if not fn: return None
    try:
        r = json.load(open(fn))["chart"]["result"][0]
        q = r["indicators"]["quote"][0]
        sp = sorted((dt.date.fromtimestamp(int(k)), v["numerator"] / v["denominator"])
                    for k, v in (r.get("events", {}).get("splits") or {}).items())
    except Exception:
        return None
    d, o, c = [], [], []
    for t, op, cl in zip(r["timestamp"], q["open"], q["close"]):
        if cl is None or cl <= 0: continue
        dd = dt.date.fromtimestamp(t)
        if d and dd <= d[-1]: continue
        d.append(dd); c.append(cl); o.append(op if op and op > 0 else None)
    if len(d) < 300: return None
    return {"d": d, "o": o, "c": c, "sp": sp}


def split_factor(sp, after):
    f = 1.0
    for sd, ratio in sp:
        if sd > after: f *= ratio
    return f


def qkey(d): return d.year * 4 + (d.month - 1) // 3


def pts(s):
    for f in ("%d-%b-%Y %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try: return dt.datetime.strptime(s, f)
        except Exception: pass
    return None


# announcements: per symbol list of datetimes
ann = collections.defaultdict(list)
for f in glob.glob(os.path.join(V1, "ann", "*.json")):
    sym = os.path.basename(f)[:-5]
    for t, _ in json.load(open(f)):
        x = pts(t or "")
        if x: ann[sym].append(x)
for f in glob.glob(os.path.join(V2, "anndays", "*.json")):
    for sym, t, _ in json.load(open(f))["rows"]:
        x = pts(t or "")
        if x and sym: ann[sym].append(x)
for k in ann: ann[k] = sorted(set(ann[k]))

data = {}
for fn in sorted(glob.glob(os.path.join(V2, "results", "*.json"))):
    j = json.load(open(fn)); sym = j["symbol"]
    funnel["status_" + str(j.get("status"))] += 1
    if j.get("status") != "ok": continue
    if "A" not in j.get("passes", []): funnel["passA_missing"] += 1; continue
    px = load_px(sym)
    if not px: funnel["no_prices"] += 1; continue
    byq = collections.defaultdict(dict)   # qe -> basis -> row
    for k, r in j["q"].items():
        qe, b = k.split("|"); qe = dt.date.fromisoformat(qe)
        if qe.month not in (3, 6, 9, 12): continue
        byq[qe][b] = r
    xs = [r["pdup"] / r["face"] for q in byq.values() for r in q.values() if r.get("src", "").startswith("xbrl") and r.get("pdup") and r.get("face")]
    ds = [r["pdup"] * r["unit"] / r["face"] for q in byq.values() for r in q.values() if r.get("src", "").startswith("detail") and r.get("pdup") and r.get("face")]
    adj = 1.0
    if xs and ds:
        rr = st.median(ds) / st.median(xs)
        if not 0.3 < rr < 3: adj = 10 ** -round(math.log10(rr)); funnel["unit_rescaled"] += 1
    qs = []
    for qe in sorted(byq):
        rows = byq[qe]
        evs = [pts(r["event"]) for r in rows.values() if r.get("event")]
        evs = [e for e in evs if e]
        if not evs: continue
        ev = min(evs)
        c = [t for t in ann.get(sym, []) if qe < t.date() <= ev.date()]
        ev_src = ("ann" if c[0].date() < ev.date() else "ann_same") if c else "feed"
        if c: ev = c[0]
        q = {"qe": qe, "ev": ev, "ev_src": ev_src}
        for b, r in rows.items():
            u = (r.get("unit") or 1.0) * (adj if r.get("src", "").startswith("detail") else 1.0)
            if r.get("eps") is not None:
                q["eps_" + b] = r["eps"] / split_factor(px["sp"], ev.date())
            if r.get("pdup") and r.get("face") and "sh" not in q: q["sh"] = r["pdup"] * u / r["face"]
        qs.append(q)
    hist = []
    for q in qs:
        if q.get("sh"): hist.append(q["sh"])
        q["sh_r"] = st.median(hist[-3:]) if hist else None
    data[sym] = {"px": px, "q": {qkey(q["qe"]): q for q in qs}}
print("symbols with results+prices:", len(data), flush=True)

for sym, v in data.items():
    px = v["px"]
    filings = sorted((q["ev"].date(), q["sh_r"]) for q in v["q"].values() if q["sh_r"])
    fd = [f[0] for f in filings]
    mc = []
    for i, d in enumerate(px["d"]):
        k = bisect.bisect_right(fd, d) - 1
        mc.append(px["c"][i] * split_factor(px["sp"], d) * filings[k][1] / 1e7 if k >= 0 else np.nan)
    v["mc"] = mc; v["di"] = {d: i for i, d in enumerate(px["d"])}


def sue(qd, k, field):
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


rows = []
for sym, v in data.items():
    px = v["px"]; d = px["d"]
    for k, q in v["q"].items():
        ev = q["ev"].date()
        if not (D0 <= ev <= D1): continue
        funnel["ev_in_window"] += 1
        if (ev - q["qe"]).days > 150: funnel["drop_late_filing"] += 1; continue
        sC, nC = sue(v["q"], k, "eps_C"); sS, nS = sue(v["q"], k, "eps_S")
        s, basis = (sC, "C") if sC is not None else ((sS, "S") if sS is not None else (None, None))
        if s is None: funnel["drop_no_sue"] += 1; continue
        i0 = bisect.bisect_right(d, ev)
        if i0 >= len(d): funnel["drop_no_entry_px_yet"] += 1; continue
        if i0 < 250: funnel["drop_short_history"] += 1; continue
        if (d[i0] - ev).days > 7: funnel["drop_price_gap"] += 1; continue
        mc = v["mc"][i0]
        if not mc == mc: funnel["drop_no_shares"] += 1; continue
        if not (500 <= mc <= 50000): funnel["drop_mcap_range"] += 1; continue
        ib = bisect.bisect_left(d, ev) - 1
        rec = {"sym": sym, "qe": str(q["qe"]), "event": q["ev"].strftime("%Y-%m-%d %H:%M"), "entry": str(d[i0]),
               "mcap_cr": round(mc, 1), "sue": s, "basis": basis, "sue_C": sC, "sue_S": sS,
               "ann_ret": px["c"][i0] / px["c"][ib] - 1 if ib >= 0 else None, "ev_src": q["ev_src"],
               "_i0": i0}
        rows.append(rec); funnel["events_kept"] += 1
print("events:", len(rows), flush=True)

# controls, grouped by (entry date, end date)
syms = list(data)
need = collections.defaultdict(list)
for r in rows:
    v = data[r["sym"]]; d = v["px"]["d"]; i0 = r.pop("_i0")
    for h in H:
        j1 = i0 + h
        if j1 >= len(d) or (d[j1] - d[i0]).days > h * 1.7 + 15:
            r[f"r{h}"] = r[f"c{h}"] = None; r[f"nc{h}"] = 0; continue
        r[f"r{h}"] = v["px"]["c"][j1] / v["px"]["c"][i0] - 1
        need[(d[i0], d[j1])].append((r, h))
for n, ((a, b), lst) in enumerate(need.items()):
    m, ret, who = [], [], []
    for s2 in syms:
        v2 = data[s2]; ia, ibb = v2["di"].get(a), v2["di"].get(b)
        if ia is None or ibb is None or ia < 250: continue
        mm = v2["mc"][ia]
        if not mm == mm: continue
        m.append(mm); ret.append(v2["px"]["c"][ibb] / v2["px"]["c"][ia] - 1); who.append(s2)
    m, ret, who = np.array(m), np.array(ret), np.array(who)
    for r, h in lst:
        sel = (m >= 0.5 * r["mcap_cr"]) & (m <= 2 * r["mcap_cr"]) & (who != r["sym"])
        r[f"nc{h}"] = int(sel.sum())
        r[f"c{h}"] = float(ret[sel].mean()) if sel.sum() >= 5 else None

cols = ["sym", "qe", "event", "entry", "mcap_cr", "sue", "basis", "sue_C", "sue_S", "ann_ret", "ev_src"] + \
       [f"{p}{h}" for h in H for p in ("r", "c", "nc")]
with open(os.path.join(V2, "events_v2.tsv"), "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in rows:
        f.write("\t".join("" if r.get(c) is None else (f"{r[c]:.6g}" if isinstance(r[c], float) else str(r[c]))
                          for c in cols) + "\n")
json.dump(funnel, open(os.path.join(V2, "events_v2_funnel.json"), "w"), indent=1)
print(dict(funnel))
