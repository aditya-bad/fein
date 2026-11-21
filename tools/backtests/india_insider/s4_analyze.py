#!/usr/bin/env python3
"""Step 4: returns of pre-registered events vs 5 size-matched random NSE controls (+ NIFTY 500 context).

Market cap (Rs cr): events = implied total shares (afterAcqSharesNo / afterAcqSharesPer) x insider VWAP.
Controls at date t = implied shares from the PIT row nearest in time (|gap| <= 365 d) x k x Yahoo close(t), where
k = unadjusted PIT market-trade price / Yahoo close near the share row's date (Yahoo's split event list is incomplete
for Indian bonuses, e.g. 360ONE 2023 shows 2:1 while prices are adjusted 4:1, so split events are NOT used).
Identity check for events: VWAP / k / Yahoo close on event date within x0.6-x1.67.
Entry = adjusted close on first trading day STRICTLY after the broadcast date; horizons 63/126/252 trading days.
If a series ends early (delisted/merged) the last price is used ('truncated').
Controls: 5 random (seed 11) from all PIT-filing NSE symbols with prices, mcap x0.5-x2 of event firm, listed >= 180 d
before event, no own qualifying event within +-365 d, price on entry day. Excess = event - mean(controls).
Stats: mean, 1/99 winsorised mean, median, hit, naive t, 95% bootstrap CI resampling event-months (2000).
Usage: python3 s4_analyze.py OUTDIR [--seed N] [--no-ctl-jump-screen] [--tag NAME]   (sensitivity runs write results_<tag>.*)"""
import bisect, csv, json, math, os, random, sys
from collections import defaultdict
from datetime import date, datetime, timezone, timedelta

S = sys.argv[1]; P = os.path.join(S, "prices")
SEED = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 11
CTL_JUMP = "--no-ctl-jump-screen" not in sys.argv
TAG = ("_" + sys.argv[sys.argv.index("--tag") + 1]) if "--tag" in sys.argv else ""
H = {"3m": 63, "6m": 126, "12m": 252}
LAST_OK = "2026-11-10"
_cache = {}
def load(sym):
    if sym in _cache: return _cache[sym]
    fn = os.path.join(P, sym.replace("/", "_") + ".json"); out = None
    if os.path.exists(fn):
        j = json.load(open(fn)); out = {"missing": True}
        try:
            r = j["chart"]["result"][0]
            ts = r["timestamp"]; cl = r["indicators"]["quote"][0]["close"]; ad = r["indicators"]["adjclose"][0]["adjclose"]
            ds, A, C = [], [], []
            for t, c, a in zip(ts, cl, ad):
                if c is None or a is None or c <= 0 or a <= 0: continue
                d = (datetime.fromtimestamp(t, timezone.utc) + timedelta(hours=5, minutes=30)).date().isoformat()
                if ds and ds[-1] == d: continue
                ds.append(d); A.append(a); C.append(c)
            spl = sorted(((datetime.fromtimestamp(int(v["date"]), timezone.utc) + timedelta(hours=5, minutes=30)).date().isoformat(),
                          v["numerator"] / v["denominator"]) for v in (r.get("events", {}).get("splits") or {}).values())
            if len(ds) > 20: out = {"d": ds, "adj": A, "close": C, "splits": spl}
        except Exception:
            pass
    _cache[sym] = out; return out


shares = defaultdict(list)
for line in open(os.path.join(S, "shares.tsv")):
    s, d, n = line.split("\t"); shares[s].append((d, float(n)))
for s in shares: shares[s].sort()
def shares_at(sym, d):
    L = shares.get(sym)
    if not L: return None
    ds = [x[0] for x in L]; i = bisect.bisect_left(ds, d)
    cands = [L[j] for j in (i - 1, i) if 0 <= j < len(L)]
    best = min(cands, key=lambda x: abs((date.fromisoformat(x[0]) - date.fromisoformat(d)).days))
    if abs((date.fromisoformat(best[0]) - date.fromisoformat(d)).days) > 365: return None
    near = sorted(n for dd, n in L if abs((date.fromisoformat(dd) - date.fromisoformat(best[0])).days) <= 30)
    return best[0], near[len(near) // 2]

tradepx = defaultdict(list)
for line in open(os.path.join(S, "tradepx.tsv")):
    s_, d_, p_ = line.split("\t"); tradepx[s_].append((d_, float(p_)))
for s_ in tradepx: tradepx[s_].sort()

def close_on(px, d, tol=5):
    i = bisect.bisect_right(px["d"], d) - 1
    if i < 0 or (date.fromisoformat(d) - date.fromisoformat(px["d"][i])).days > tol: return None
    return px["close"][i]

def basis_k(sym, px, d, win=10):
    """unadjusted/Yahoo-adjusted price ratio near date d (median over PIT market trades within +-win days)."""
    L = tradepx.get(sym) or []
    ks = []
    for dd, p in L:
        if abs((date.fromisoformat(dd) - date.fromisoformat(d)).days) <= win:
            c = close_on(px, dd, 3)
            if c and 0.05 < p / c < 50: ks.append(p / c)
    if not ks: return None
    ks.sort(); return ks[len(ks) // 2]

def mcap(sym, d, px=None, sh=None):
    """Rs cr at date d = shares(row date r) x k(r) x Yahoo close(d); corporate actions between r and d cancel
    because k maps the row-date share basis onto Yahoo's (fully adjusted) price basis."""
    px = px or load(sym)
    if not px or px.get("missing"): return None
    c = close_on(px, d, 10)
    if c is None: return None
    sh = sh or shares_at(sym, d)
    if not sh: return None
    rowd, n = sh
    k = basis_k(sym, px, rowd) or basis_k(sym, px, rowd, 45)
    if k is None or not (0.05 < k < 50): return None
    return n * k * c / 1e7

def entry(px, d):
    i = bisect.bisect_right(px["d"], d)
    return i if i < len(px["d"]) else None

def rets(px, i0):
    out, tr = {}, False
    for k, h in H.items():
        j = i0 + h
        if j < len(px["d"]): out[k] = px["adj"][j] / px["adj"][i0] - 1
        elif px["d"][-1] < LAST_OK: out[k] = px["adj"][-1] / px["adj"][i0] - 1; tr = True
        else: out[k] = None
    return out, tr

def win_ret(px, d0, d1):   # return between dates (same calendar window as event) for benchmark
    i = bisect.bisect_left(px["d"], d0); j = bisect.bisect_left(px["d"], d1)
    if i >= len(px["d"]) or j >= len(px["d"]): return None
    return px["adj"][j] / px["adj"][i] - 1

def stats(vals, months, B=2000, seed=7):
    xs = [(v, m) for v, m in zip(vals, months) if v is not None]; n = len(xs)
    if n < 5: return {"n": n}
    v = [a for a, _ in xs]; mean = sum(v) / n; s = sorted(v)
    med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    sd = math.sqrt(sum((a - mean) ** 2 for a in v) / (n - 1)); t = mean / (sd / math.sqrt(n)) if sd else 0
    byM = defaultdict(list)
    for a, m in xs: byM[m].append(a)
    keys = list(byM); rnd = random.Random(seed); bm, bmed = [], []
    for _ in range(B):
        smp = []
        for _ in keys: smp += byM[rnd.choice(keys)]
        bm.append(sum(smp) / len(smp)); ss = sorted(smp); bmed.append(ss[len(ss) // 2])
    bm.sort(); bmed.sort(); lo, hi = int(0.025 * B), int(0.975 * B) - 1
    a1, a99 = s[int(0.01 * (n - 1))], s[int(0.99 * (n - 1))]
    wm = sum(min(max(a, a1), a99) for a in v) / n
    return {"n": n, "mean": mean, "ci": (bm[lo], bm[hi]), "median": med, "med_ci": (bmed[lo], bmed[hi]),
            "hit": sum(1 for a in v if a > 0) / n, "t": t, "wmean": wm, "months": len(keys)}

ev = list(csv.DictReader(open(os.path.join(S, "events.tsv")), delimiter="\t"))
evdates = defaultdict(list)
for e in ev: evdates[e["sym"]].append(date.fromisoformat(e["event_date"]))
universe = open(os.path.join(S, "universe.txt")).read().split()
bench = load("^CRSLDX")
funnel = defaultdict(int); funnel["events_2021_2024"] = len(ev)
rows, missing = [], []
rnd = random.Random(SEED)
for e in ev:
    sym, d = e["sym"], e["event_date"]
    px = load(sym)
    sh = (d, float(e["implied_shares"])) if e["implied_shares"] else shares_at(sym, d)
    if px is None: funnel["price_not_fetched"] += 1; continue
    if px.get("missing"):
        mc_est = sh[1] * float(e["vwap"]) / 1e7 if sh else None
        if mc_est is not None and 500 <= mc_est <= 20000:
            funnel["in_band_but_no_yahoo_history"] += 1; missing.append(dict(e, mcap_est=round(mc_est)))
        else: funnel["no_yahoo_history_out_of_band_or_unknown"] += 1
        continue
    if not sh: funnel["no_share_count"] += 1; continue
    if close_on(px, d, 10) is None: funnel["no_price_on_event_date"] += 1; continue
    mc = sh[1] * float(e["vwap"]) / 1e7 if e["implied_shares"] else mcap(sym, d, px, sh)
    if mc is None: funnel["no_mcap_estimate"] += 1; continue
    # identity check: event VWAP re-expressed on Yahoo basis must be within x0.6-x1.67 of Yahoo close on event date
    k = basis_k(sym, px, d, 30)
    if k is None: funnel["no_basis_check(kept)"] += 1
    else:
        ratio = float(e["vwap"]) / k / close_on(px, d, 10)
        if not (0.6 <= ratio <= 1.67): funnel["price_identity_fail"] += 1; continue
    # bad-data flag: daily adjusted move beyond -50%/+100% inside the 12m window (unadjusted bonus etc.)
    i0_ = entry(px, d) or 0
    jump = any(not (0.5 < px["adj"][j] / px["adj"][j - 1] < 2.0) for j in range(i0_ + 1, min(i0_ + 253, len(px["d"]))))
    if not (500 <= mc <= 20000): funnel["outside_mcap_500_20000cr"] += 1; continue
    if (date.fromisoformat(d) - date.fromisoformat(px["d"][0])).days < 180: funnel["listed_lt_180d"] += 1; continue
    i0 = entry(px, d)
    if i0 is None: funnel["no_entry"] += 1; continue
    r, tr = rets(px, i0)
    # controls
    cands = universe[:]; rnd.shuffle(cands); ctl = []
    for c in cands:
        if c == sym: continue
        if any(abs((x - date.fromisoformat(d)).days) <= 365 for x in evdates.get(c, [])): continue
        cp = load(c)
        if not cp or cp.get("missing"): continue
        if (date.fromisoformat(d) - date.fromisoformat(cp["d"][0])).days < 180: continue
        cm = mcap(c, d, cp)
        if cm is None or not (0.5 * mc <= cm <= 2 * mc): continue
        j0 = entry(cp, d)
        if j0 is None or cp["d"][j0] != px["d"][i0]: continue
        cjump = any(not (0.5 < cp["adj"][j] / cp["adj"][j - 1] < 2.0) for j in range(j0 + 1, min(j0 + 253, len(cp["d"]))))
        if cjump and CTL_JUMP: continue
        cr, _ = rets(cp, j0); ctl.append((c, cr))
        if len(ctl) == 5: break
    if len(ctl) < 3: funnel["lt3_controls"] += 1; continue
    exc, bex = {}, {}
    for k in H:
        cv = [cr[k] for _, cr in ctl if cr[k] is not None]
        exc[k] = r[k] - sum(cv) / len(cv) if r[k] is not None and cv else None
        if r[k] is not None and bench and not bench.get("missing"):
            j = min(i0 + H[k], len(px["d"]) - 1)
            b = win_ret(bench, px["d"][i0], px["d"][j]); bex[k] = r[k] - b if b is not None else None
        else: bex[k] = None
    cex = {}
    for k in H:
        cv = [cr[k] for _, cr in ctl if cr[k] is not None]
        if cv and bench and r[k] is not None:
            j = min(i0 + H[k], len(px["d"]) - 1); b = win_ret(bench, px["d"][i0], px["d"][j])
            cex[k] = sum(cv) / len(cv) - b if b is not None else None
        else: cex[k] = None
    funnel["usable"] += 1; funnel["truncated(delisted_after_event)"] += tr
    rows.append(dict(sym=sym, d=d, month=d[:7], mc=mc, cls=e["cls"], v=float(e["value_cr"]),
                     pct=float(e["pct_equity"]) if e["pct_equity"] else None, n=int(e["n_buyers"]),
                     r=r, exc=exc, bex=bex, cex=cex, nctl=len(ctl), ctl=[c for c, _ in ctl], trunc=tr, jump=jump))
    funnel["flag_price_jump"] += jump

def grp(name, sel):
    out = {"name": name}
    for k in H:
        out[k] = stats([x["exc"][k] for x in sel], [x["month"] for x in sel])
    return out
G = [grp("ALL", rows),
     grp("promoter-only", [x for x in rows if x["cls"] == "promoter"]),
     grp("KMP-only", [x for x in rows if x["cls"] == "kmp"]),
     grp("mixed", [x for x in rows if x["cls"] == "mixed"]),
     grp("small 500-2000cr", [x for x in rows if x["mc"] < 2000]),
     grp("large 2000-20000cr", [x for x in rows if x["mc"] >= 2000]),
     # exploratory
     grp("X: buy >= Rs 5 cr", [x for x in rows if x["v"] >= 5]),
     grp("X: buy >= 1% equity", [x for x in rows if x["pct"] and x["pct"] >= 1]),
     grp("ALL ex price-jump flags", [x for x in rows if not x["jump"]]),
     grp("X: >=2 buyers", [x for x in rows if x["n"] >= 2])] + \
    [grp(f"X: year {y}", [x for x in rows if x["d"].startswith(y)]) for y in ("2021", "2022", "2023", "2024")]
BEN = {"event vs NIFTY500": {k: stats([x["bex"][k] for x in rows], [x["month"] for x in rows]) for k in H},
       "controls vs NIFTY500": {k: stats([x["cex"][k] for x in rows], [x["month"] for x in rows]) for k in H},
       "raw event return": {k: stats([x["r"][k] for x in rows], [x["month"] for x in rows]) for k in H}}
json.dump({"funnel": funnel, "groups": G, "bench": BEN, "missing": missing, "rows": rows},
          open(os.path.join(S, "results%s.json" % TAG), "w"), indent=1, default=str)
def f(s, k="mean"):
    if s.get("n", 0) < 5: return f"n={s.get('n')}"
    return (f"n={s['n']:4d} mean {s['mean']*100:+6.1f}% [{s['ci'][0]*100:+.1f},{s['ci'][1]*100:+.1f}] "
            f"wmean {s['wmean']*100:+6.1f}% med {s['median']*100:+6.1f}% [{s['med_ci'][0]*100:+.1f},{s['med_ci'][1]*100:+.1f}] "
            f"hit {s['hit']*100:4.1f}% t {s['t']:+.2f}")
with open(os.path.join(S, "results%s.txt" % TAG), "w") as o:
    o.write("FUNNEL " + json.dumps(funnel) + "\n")
    for g in G:
        for k in H: o.write(f"{g['name']:22s} {k:3s} {f(g[k])}\n")
    for b, d in BEN.items():
        for k in H: o.write(f"{b:22s} {k:3s} {f(d[k])}\n")
    mcs = sorted(x["mc"] for x in rows); vs = sorted(x["v"] for x in rows)
    if rows: o.write(f"median mcap {mcs[len(mcs)//2]:.0f} cr; median buy {vs[len(vs)//2]:.2f} cr; "
                     f"controls/event {sum(x['nctl'] for x in rows)/len(rows):.2f}\n")
    o.write(f"missing in-band events: {len(missing)}\n")
print(open(os.path.join(S, "results%s.txt" % TAG)).read())
