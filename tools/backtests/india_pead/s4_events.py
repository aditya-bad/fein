#!/usr/bin/env python3
"""Step 4: build PEAD events (pre-registered rules in research_notes/Backtests/india_pead.md).
For every 'ok' symbol in OUTDIR/results: split-adjust EPS (Yahoo split events after the filing date),
compute seasonal-random-walk SUE (EPS primary, revenue secondary), event/entry dates, market cap at entry,
returns at 21/63/126 trading days (close-to-close from the first trading day AFTER the filing date; plus
next-day-open variant), announcement-window return, and size-matched control returns
(all sampled stocks with mcap x0.5-x2 on the entry date, >=5 required).
Usage: python3 s4_events.py OUTDIR   -> OUTDIR/events.tsv, OUTDIR/s4_funnel.json"""
import bisect, collections, datetime as dt, glob, json, math, os, statistics as st, sys

S = sys.argv[1]
H = (21, 63, 126)
D0, D1 = dt.date(2018, 1, 1), dt.date(2025, 12, 31)


def load_px(sym):
    fn = os.path.join(S, "prices", sym + ".json")
    if not os.path.exists(fn): return None
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


def qkey(d):  # quarter index
    return d.year * 4 + (d.month - 1) // 3


funnel = collections.Counter()
data = {}
for fn in sorted(glob.glob(os.path.join(S, "results", "*.json"))):
    j = json.load(open(fn)); sym = j["symbol"]
    funnel["status_" + j["status"]] += 1
    if j["status"] != "ok": continue
    px = load_px(sym)
    if not px: funnel["no_prices"] += 1; continue
    qs = []
    for q in j["quarters"]:
        qe = dt.date.fromisoformat(q["qe"]); ev = dt.datetime.strptime(q["event"], "%Y-%m-%d %H:%M:%S")
        if qe.month not in (3, 6, 9, 12): continue
        qs.append(dict(q, qe=qe, ev=ev))
    # unit sanity for detail rows (lakh) vs xbrl rows (rupee) using implied shares
    xs = [q["pdup"] / q["face"] for q in qs if q.get("src") == "xbrl" and q.get("pdup") and q.get("face")]
    ds = [q["pdup"] * q["unit"] / q["face"] for q in qs if q.get("src") == "detail" and q.get("pdup") and q.get("face")]
    adj = 1.0
    if xs and ds:
        r = st.median(ds) / st.median(xs)
        if not 0.3 < r < 3:
            k = round(math.log10(r)); adj = 10 ** -k; funnel["unit_rescaled"] += 1
    for q in qs:
        u = q.get("unit") or 1.0
        if q.get("src") == "detail": u *= adj
        q["rev_rs"] = q["rev"] * u if q.get("rev") is not None else None
        q["sh"] = q["pdup"] * u / q["face"] if q.get("pdup") and q.get("face") else None
        q["eps_a"] = q["eps"] / split_factor(px["sp"], q["ev"].date()) if q.get("eps") is not None else None
    # robust shares: median of up to 3 most recent known values (catches 10x XBRL typos)
    hist = []
    for q in qs:
        if q["sh"]: hist.append(q["sh"])
        q["sh_r"] = st.median(hist[-3:]) if hist else None
    data[sym] = {"px": px, "q": {qkey(q["qe"]): q for q in qs}}

print("symbols with results+prices:", len(data))
# daily mcap lookup for controls: shares as of date (last filing <= date) x unadjusted close
idx = {}
for sym, v in data.items():
    px = v["px"]; filings = sorted((q["ev"].date(), q["sh_r"]) for q in v["q"].values() if q["sh_r"])
    v["filings"] = filings; v["fd"] = [f[0] for f in filings]
    v["di"] = {d: i for i, d in enumerate(px["d"])}


def mcap(sym, i):
    v = data[sym]; d = v["px"]["d"][i]
    k = bisect.bisect_right(v["fd"], d) - 1
    if k < 0: return None
    sh = v["filings"][k][1]
    return v["px"]["c"][i] * split_factor(v["px"]["sp"], d) * sh / 1e7


for sym, v in data.items():
    v["mc"] = [mcap(sym, i) for i in range(len(v["px"]["d"]))]


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
        lag = (ev - q["qe"]).days
        if lag > 150: funnel["drop_late_filing_or_comparative"] += 1; continue
        s_eps, n_eps = sue(v["q"], k, "eps_a")
        s_rev, _ = sue(v["q"], k, "rev_rs")
        if s_eps is None and s_rev is None: funnel["drop_no_sue"] += 1; continue
        i0 = bisect.bisect_right(d, ev)           # first trading day strictly after filing date
        if i0 >= len(d): funnel["drop_no_entry_px"] += 1; continue
        if i0 < 250: funnel["drop_short_history"] += 1; continue
        if (d[i0] - ev).days > 7: funnel["drop_price_gap"] += 1; continue
        mc = v["mc"][i0]
        if mc is None: funnel["drop_no_shares"] += 1; continue
        if not (500 <= mc <= 50000): funnel["drop_mcap_range"] += 1; continue
        ib = bisect.bisect_left(d, ev) - 1        # last close before filing date
        rec = {"sym": sym, "qe": str(q["qe"]), "event": q["ev"].strftime("%Y-%m-%d %H:%M"), "entry": str(d[i0]),
               "mcap_cr": round(mc, 1), "sue_eps": s_eps, "sue_rev": s_rev, "n_prev": n_eps,
               "ann_ret": px["c"][i0] / px["c"][ib] - 1 if ib >= 0 else None, "src": q.get("src")}
        for h in H:
            j1 = i0 + h
            if j1 >= len(d) or (d[j1] - d[i0]).days > h * 1.7 + 15:
                rec[f"r{h}"] = rec[f"ro{h}"] = rec[f"c{h}"] = None; rec[f"nc{h}"] = 0; continue
            rec[f"r{h}"] = px["c"][j1] / px["c"][i0] - 1
            rec[f"ro{h}"] = px["c"][j1] / px["o"][i0] - 1 if px["o"][i0] else None
            # size-matched controls over identical calendar window
            cr = []
            for s2, v2 in data.items():
                if s2 == sym: continue
                a, b = v2["di"].get(d[i0]), v2["di"].get(d[j1])
                if a is None or b is None or a < 250: continue
                m2 = v2["mc"][a]
                if m2 is None or not (0.5 * mc <= m2 <= 2 * mc): continue
                cr.append(v2["px"]["c"][b] / v2["px"]["c"][a] - 1)
            rec[f"nc{h}"] = len(cr)
            rec[f"c{h}"] = sum(cr) / len(cr) if len(cr) >= 5 else None
        rows.append(rec); funnel["events_kept"] += 1

cols = ["sym", "qe", "event", "entry", "mcap_cr", "sue_eps", "sue_rev", "n_prev", "ann_ret", "src"] + \
       [f"{p}{h}" for h in H for p in ("r", "ro", "c", "nc")]
with open(os.path.join(S, "events.tsv"), "w") as f:
    f.write("\t".join(cols) + "\n")
    for r in rows:
        f.write("\t".join("" if r.get(c) is None else (f"{r[c]:.6g}" if isinstance(r[c], float) else str(r[c]))
                          for c in cols) + "\n")
json.dump(funnel, open(os.path.join(S, "s4_funnel.json"), "w"), indent=1)
print(dict(funnel))
