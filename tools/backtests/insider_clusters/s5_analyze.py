#!/usr/bin/env python3
"""Step 5: event returns vs IWM/SPY and vs size-matched random controls; stats + subsamples.

Entry: adjusted close on the first trading day STRICTLY AFTER the event (filing) date.
Horizons: 21/63/126/252 trading days after entry (~1/3/6/12 months).
If a series ends before the horizon (delisting), the last available price is used and the
event is counted in 'truncated' (exit at last trade - optimistic for bankruptcies).
Controls: for each event, up to 5 firms drawn at random (seeded) from the point-in-time
universe (issuers with any Form 4 that quarter), same SIC exclusions, market cap within
x0.6-x1.67 of the event firm's at the event date, not an event firm within +-365 days, with
prices on the entry date. Excess vs control = event return - mean(control returns).
Stats: mean, median, hit rate, naive t, 95% bootstrap CI clustered by event MONTH (events in the
same month share market shocks), 2000 resamples.
Usage: python3 s5_analyze.py OUTDIR [--mcap-lo 300 --mcap-hi 10000]
"""
import bisect, csv, json, math, os, random, sys, argparse
from collections import defaultdict
from datetime import date, datetime, timezone

H = {"1m": 21, "3m": 63, "6m": 126, "12m": 252}
SPAC = {"6770"}
FUND = {"6722", "6726", "6799"}
BIO = {"2834", "2835", "2836", "8731"}
BANK = {str(x) for x in range(6020, 6037)} | {"6035", "6036", "6120", "6111"}


def load_px(pdir, t):
    p = os.path.join(pdir, t.replace("/", "_") + ".json")
    if not os.path.exists(p): return None
    d = json.load(open(p))
    if d.get("missing"): return {"missing": True}
    ds, adj, cl = [], [], []
    for ts, a, c in zip(d["t"], d["adj"], d["close"]):
        if a is None or c is None or a <= 0: continue
        ds.append(datetime.fromtimestamp(ts, timezone.utc).date().isoformat()); adj.append(a); cl.append(c)
    if not ds: return {"missing": True}
    spl = sorted((datetime.fromtimestamp(int(k), timezone.utc).date().isoformat(), v["numerator"] / v["denominator"])
                 for k, v in (d.get("splits") or {}).items())
    return {"d": ds, "adj": adj, "close": cl, "splits": spl, "type": d.get("type")}


def unadj_close(px, i):
    f = 1.0
    for sd, r in px["splits"]:
        if sd > px["d"][i]: f *= r
    return px["close"][i] * f


def entry_idx(px, d):
    i = bisect.bisect_right(px["d"], d)
    return i if i < len(px["d"]) else None


def rets(px, i0, last_ok="2026-11-13"):
    out, trunc = {}, False
    for k, h in H.items():
        j = i0 + h
        if j < len(px["d"]):
            out[k] = px["adj"][j] / px["adj"][i0] - 1
        elif px["d"][-1] < last_ok:      # series stopped (delisted) -> last price
            out[k] = px["adj"][-1] / px["adj"][i0] - 1; trunc = True
        else:
            out[k] = None
    return out, trunc


def stats(vals, months, B=2000, seed=7):
    xs = [(v, m) for v, m in zip(vals, months) if v is not None]
    n = len(xs)
    if n < 5: return {"n": n}
    v = [a for a, _ in xs]
    mean = sum(v) / n; s = sorted(v); med = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    sd = math.sqrt(sum((a - mean) ** 2 for a in v) / (n - 1)); t = mean / (sd / math.sqrt(n)) if sd else 0
    byM = defaultdict(list)
    for a, m in xs: byM[m].append(a)
    keys = list(byM); rnd = random.Random(seed); bm, bmed, bhit = [], [], []
    for _ in range(B):
        smp = []
        for _ in keys: smp += byM[rnd.choice(keys)]
        bm.append(sum(smp) / len(smp)); ss = sorted(smp); bmed.append(ss[len(ss) // 2])
        bhit.append(sum(1 for a in smp if a > 0) / len(smp))
    bm.sort(); bmed.sort(); bhit.sort()
    lo, hi = int(0.025 * B), int(0.975 * B) - 1
    # winsorised mean (1%/99%)
    a1, a99 = s[int(0.01 * (n - 1))], s[int(0.99 * (n - 1))]
    wm = sum(min(max(a, a1), a99) for a in v) / n
    return {"n": n, "mean": mean, "mean_ci": (bm[lo], bm[hi]), "median": med, "median_ci": (bmed[lo], bmed[hi]),
            "hit": sum(1 for a in v if a > 0) / n, "hit_ci": (bhit[lo], bhit[hi]), "t_naive": t, "wmean": wm,
            "months": len(keys)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("out")
    ap.add_argument("--mcap-lo", type=float, default=300); ap.add_argument("--mcap-hi", type=float, default=10000)
    ap.add_argument("--nctl", type=int, default=5)
    a = ap.parse_args(); out = a.out; pdir = os.path.join(out, "prices")
    ev = list(csv.DictReader(open(os.path.join(out, "events_sized.tsv")), delimiter="\t"))
    sic = json.load(open(os.path.join(out, "sic.json")))
    bench = {b: load_px(pdir, b) for b in ("IWM", "SPY")}
    bidx = {b: {d: i for i, d in enumerate(px["d"])} for b, px in bench.items()}
    rp = os.path.join(out, "renamed_tickers.json")
    renamed = json.load(open(rp)) if os.path.exists(rp) else {}
    funnel = defaultdict(int); funnel["cluster_events_2021_2024"] = len(ev)
    res = []
    for e in ev:
        if not e["mcap_m"]: funnel["no_shares_frame"] += 1; continue
        mc = float(e["mcap_m"])
        if not (a.mcap_lo <= mc <= a.mcap_hi): funnel["outside_mcap"] += 1; continue
        s = e["sic"]
        grp = "spac" if s in SPAC else "fund" if s in FUND else "bio" if s in BIO else "bank" if s in BANK else "other"
        if grp in ("spac", "fund"): funnel["spac_or_fund"] += 1; continue
        px = load_px(pdir, e["ticker"])
        if px and px.get("missing") and e["issuer_cik"] in renamed:   # ticker changed later: use current one
            px2 = load_px(pdir, renamed[e["issuer_cik"]][1])
            if px2 and not px2.get("missing"):
                px = px2; funnel["recovered_via_current_ticker"] += 1
        if px is None: funnel["price_not_fetched"] += 1; continue
        if px.get("missing"): funnel["yahoo_missing(delisted/renamed)"] += 1; e["_miss"] = 1; res.append(dict(e, grp=grp, status="missing")); continue
        if e["ticker"] in ("NONE", "NA"): funnel["no_ticker"] += 1; continue
        if px["d"][0] > "2020-12-05" and (date.fromisoformat(e["event_date"]) - date.fromisoformat(px["d"][0])).days < 180:
            funnel["recent_listing(<180d: IPO/de-SPAC)"] += 1; continue
        i0 = entry_idx(px, e["event_date"])
        if i0 is None or (date.fromisoformat(px["d"][i0]) - date.fromisoformat(e["event_date"])).days > 7:
            funnel["no_price_at_entry"] += 1; res.append(dict(e, grp=grp, status="missing")); continue
        # identity check: Yahoo unadjusted close near entry vs insider VWAP
        ratio = unadj_close(px, i0) / float(e["vwap"])
        if not (0.6 <= ratio <= 1.67):
            funnel["price_mismatch(ticker_reuse?)"] += 1; res.append(dict(e, grp=grp, status="mismatch", ratio=ratio)); continue
        r, tr = rets(px, i0)
        bd = px["d"][i0]
        row = dict(e, grp=grp, status="ok", entry=bd, ratio=round(ratio, 3), trunc=int(tr))
        for b, bx in bench.items():
            j0 = bidx[b].get(bd)
            if j0 is None: continue
            for k in H:
                if r[k] is None: continue
                # benchmark over the same calendar window as the stock
                jd = px["d"][min(i0 + H[k], len(px["d"]) - 1)]
                j1 = bisect.bisect_right(bx["d"], jd) - 1
                row[f"x_{b}_{k}"] = r[k] - (bx["adj"][j1] / bx["adj"][j0] - 1)
        for k in H: row[f"r_{k}"] = r[k]
        res.append(row); funnel["usable"] += 1
    # ---- controls
    uni = json.load(open(os.path.join(out, "universe_tickers.json")))
    import s3_size_sector as S3
    sh = S3.frames(out)
    evdates = defaultdict(list)
    for e in ev: evdates[e["issuer_cik"]].append(date.fromisoformat(e["event_date"]))
    pool = [l.strip().split("\t") for l in open(os.path.join(out, "control_pool.tsv")) if l.strip()]
    poolpx = {}
    for cik, t in pool:
        px = load_px(pdir, t)
        if px and not px.get("missing"): poolpx[(cik, t)] = px
    rnd = random.Random(11)
    for row in res:
        if row.get("status") != "ok": continue
        d = row["event_date"]; dd = date.fromisoformat(d); mc = float(row["mcap_m"])
        cands = []
        for (cik, t), px in poolpx.items():
            if cik == row["issuer_cik"]: continue
            if any(abs((dd - x).days) <= 365 for x in evdates.get(cik, [])): continue
            if px["d"][0] > "2020-12-05" and (dd - date.fromisoformat(px["d"][0])).days < 180: continue
            i0 = entry_idx(px, d)
            if i0 is None or px["d"][i0] != row["entry"]: continue
            s_ = S3.shares_at(sh, cik, d)
            if not s_: continue
            cm = s_ * unadj_close(px, i0) / 1e6
            if not (a.mcap_lo <= cm <= a.mcap_hi) or not (mc / 1.67 <= cm <= mc * 1.67): continue
            cg = sic.get(cik, {}).get("sic", "")
            if (cg in BIO) != (row["grp"] == "bio"): continue
            cands.append((cik, t, px, i0))
        rnd.shuffle(cands); ch = cands[:a.nctl]
        row["n_ctl"] = len(ch)
        for k in H:
            vals = []
            for cik, t, px, i0 in ch:
                r, _ = rets(px, i0)
                if r[k] is not None: vals.append(r[k])
            if vals and row.get(f"r_{k}") is not None:
                row[f"c_{k}"] = sum(vals) / len(vals)
                row[f"x_ctl_{k}"] = row[f"r_{k}"] - row[f"c_{k}"]
                jd = row["entry"]
                if f"x_IWM_{k}" in row:  # control's own excess vs IWM
                    row[f"cx_IWM_{k}"] = row[f"c_{k}"] - (row[f"r_{k}"] - row[f"x_IWM_{k}"])
    json.dump({"funnel": funnel, "rows": res}, open(os.path.join(out, "results.json"), "w"), default=str)
    print(json.dumps(funnel, indent=1))
    ok = [r for r in res if r.get("status") == "ok"]

    def table(rows, label):
        print(f"\n=== {label}: {len(rows)} events")
        for meas in ("x_IWM", "x_SPY", "x_ctl", "cx_IWM", "r"):
            for k in H:
                st = stats([r.get(f"{meas}_{k}") for r in rows], [r["event_date"][:7] for r in rows])
                if st.get("n", 0) < 5: continue
                print(f"{meas:7} {k:4} n={st['n']:4} mean={st['mean']*100:6.1f}% [{st['mean_ci'][0]*100:5.1f},{st['mean_ci'][1]*100:5.1f}] "
                      f"wmean={st['wmean']*100:5.1f}% med={st['median']*100:6.1f}% [{st['median_ci'][0]*100:5.1f},{st['median_ci'][1]*100:5.1f}] "
                      f"hit={st['hit']*100:4.1f}% [{st['hit_ci'][0]*100:4.1f},{st['hit_ci'][1]*100:4.1f}] t={st['t_naive']:.2f}")
    main_rows = [r for r in ok if r["grp"] != "bio"]
    table(main_rows, "MAIN (ex-biotech, ex-SPAC/fund)")
    table([r for r in ok if r["grp"] == "bio"], "BIOTECH/PHARMA (separate)")
    table([r for r in main_rows if r["grp"] == "bank"], "subset: banks/thrifts")
    table([r for r in main_rows if r["grp"] != "bank"], "subset: non-banks")
    table([r for r in main_rows if int(r["n_insiders"]) >= 3], "subset: >=3 insiders")
    table([r for r in main_rows if "CEO" in r["roles"] or "CFO" in r["roles"]], "subset: CEO or CFO bought")
    table([r for r in main_rows if float(r["buy_value"]) >= 250000], "subset: cluster buy >= $250k")
    table([r for r in main_rows if float(r["mcap_m"]) < 1000], "subset: mcap 300M-1B")
    table([r for r in main_rows if float(r["mcap_m"]) >= 1000], "subset: mcap 1B-10B")
    for y in ("2021", "2022", "2023", "2024"):
        table([r for r in main_rows if r["event_date"].startswith(y)], f"year {y}")


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
