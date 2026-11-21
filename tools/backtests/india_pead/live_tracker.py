#!/usr/bin/env python3
"""LIVE forward test of the Indian PEAD rule (pre-registered in research_notes/Backtests/india_pead_v2.md §Live).
Standard library only (runs on a Raspberry Pi). All state lives in research_notes/Backtests/india_pead_live/:
  universe.csv        sym, shares (latest known), listed  -- control universe (bootstrap, refreshed by `update`)
  eps_history.csv     sym, qe, basis(C|S), eps_raw, event_ts, shares   -- reported EPS per quarter (append/update)
  sue_cutpoints.json  fixed quintile breakpoints of SUE from the 2022-26 backtest (ex-ante provisional quintile)
  predictions.csv     one row per (sym, qe) result: SUE, provisional and final quintile, prediction, outcomes
  scorecard.md        latest scored summary (written by `score`)
Subcommands:
  bootstrap V1DIR V2DIR   build universe/eps_history/cutpoints from the v2 backtest caches (run once, on the laptop)
  update [--days N]       fetch NSE result announcements of the last N days (default 4), pull the new quarterly
                          filings (integrated-filing-results XBRL) of those companies, compute SUE at announcement,
                          and log a prediction once the entry close (first trading day after the filing) exists.
  finalize                after a quarter's filing season closes (quarter-end + 50 days; Mar quarter + 65), assign the
                          FINAL in-quarter SUE quintile (the backtest definition) to every logged row of that quarter.
  score                   fill 21/63-trading-day outcomes vs size-matched controls (universe stocks with mcap x0.5-x2
                          on the entry date) for rows whose windows have closed; write scorecard.md.
Rules = backtest rules: SUE = (EPS_q - EPS_q-4)/sd(<=8 prior seasonal changes, >=4), consolidated if its history
suffices else standalone; entry = close of first NSE trading day strictly after the filing date; Rs 500-50,000 cr.
Only quarters ending on/after --first-qe (default 2026-12-31 = Q3 FY27, filed Jan-Feb 2027) are logged.
Rates: NSE API >= 1.5 s, NSE archive >= 0.5 s, Yahoo >= 1.1 s per call.
Cron (Pi, IST evenings):  15 20 * * 1-5  cd ~/fein && python3 tools/backtests/india_pead/live_tracker.py update
                          30 21 * * 6    cd ~/fein && python3 tools/backtests/india_pead/live_tracker.py finalize && \
                                         python3 tools/backtests/india_pead/live_tracker.py score"""
import argparse, bisect, csv, datetime as dt, glob, gzip, json, math, os, random, statistics as st, sys, time
import urllib.error, urllib.parse, urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
LIVE = os.path.join(ROOT, "research_notes", "Backtests", "india_pead_live")
PXC = os.path.join(LIVE, ".pxcache")          # gitignored price cache
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import v2_fetch as F                           # reuse polite getters + XBRL parser

F.GAP.update({"api": 1.5, "arc": 0.5, "yh": 1.1})
PRED_COLS = ["logged_at", "sym", "qe", "fiscal_q", "basis", "event_ts", "entry_date", "entry_close", "mcap_cr",
             "sue", "n_prev", "ann_ret", "q5_prov", "ann_up", "prediction", "q5_final", "tertile_final",
             "exit21", "r21", "c21", "nc21", "x21", "exit63", "r63", "c63", "nc63", "x63", "status"]


def fiscal_label(qe):
    fy = qe.year + (1 if qe.month > 3 else 0)
    return f"Q{ {6: 1, 9: 2, 12: 3, 3: 4}[qe.month] } FY{fy % 100:02d}"


def rcsv(fn):
    return list(csv.DictReader(open(fn))) if os.path.exists(fn) else []


def wcsv(fn, rows, cols):
    tmp = fn + ".tmp"
    with open(tmp, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(rows)
    os.replace(tmp, fn)


# ---------------------------------------------------------------- prices
def prices(sym, max_age_days=1):
    os.makedirs(PXC, exist_ok=True)
    fn = os.path.join(PXC, sym + ".json")
    if not os.path.exists(fn) or time.time() - os.path.getmtime(fn) > max_age_days * 86400:
        u = ("https://query1.finance.yahoo.com/v8/finance/chart/" + urllib.parse.quote(sym + ".NS") +
             "?range=3y&interval=1d&events=split")
        j = F.get(u, "yh", headers={"User-Agent": "Mozilla/5.0"})
        if j is None: return None
        json.dump(j, open(fn, "w"))
    try:
        r = json.load(open(fn))["chart"]["result"][0]
        ts, cl = r["timestamp"], r["indicators"]["quote"][0]["close"]
        sp = sorted((dt.date.fromtimestamp(int(k)), v["numerator"] / v["denominator"])
                    for k, v in (r.get("events", {}).get("splits") or {}).items())
    except Exception:
        return None
    d, c = [], []
    for t, x in zip(ts, cl):
        if x is None or x <= 0: continue
        dd = (dt.datetime.utcfromtimestamp(t) + dt.timedelta(hours=5, minutes=30)).date()
        if d and dd <= d[-1]: continue
        d.append(dd); c.append(x)
    return {"d": d, "c": c, "sp": sp}


def split_factor(sp, after):
    f = 1.0
    for sd, ratio in sp:
        if sd > after: f *= ratio
    return f


# ---------------------------------------------------------------- SUE
def qkey(d): return d.year * 4 + (d.month - 1) // 3


def sue_for(hist, sym, qe, sp):
    """hist rows for sym -> (sue, n_prev, basis) at quarter qe, consolidated first, never mixing bases."""
    for b in ("C", "S"):
        q = {}
        for r in hist:
            if r["basis"] != b or r["eps_raw"] in ("", None): continue
            q[qkey(dt.date.fromisoformat(r["qe"]))] = float(r["eps_raw"]) / split_factor(sp, dt.datetime.fromisoformat(r["event_ts"]).date())
        k = qkey(qe)
        chg = lambda kk: (q[kk] - q[kk - 4]) if kk in q and kk - 4 in q else None
        d0 = chg(k)
        if d0 is None: continue
        prev = [x for x in (chg(k - i) for i in range(1, 9)) if x is not None]
        if len(prev) < 4: continue
        sd = st.stdev(prev)
        if sd <= 0: continue
        return d0 / sd, len(prev), b
    return None, 0, None


def quintile(s, cuts):
    return 1 + sum(s > c for c in cuts)   # 1 = biggest miss ... 5 = biggest beat


# ---------------------------------------------------------------- bootstrap
def bootstrap(v1, v2):
    os.makedirs(LIVE, exist_ok=True)
    hist, uni = [], []
    for fn in sorted(glob.glob(os.path.join(v2, "results", "*.json"))):
        j = json.load(open(fn))
        if j.get("status") != "ok": continue
        shs = []
        for k in sorted(j["q"]):
            qe, b = k.split("|"); r = j["q"][k]
            sh = r["pdup"] * (r.get("unit") or 1) / r["face"] if r.get("pdup") and r.get("face") else None
            if sh: shs.append(sh)
            if r.get("eps") is None or not r.get("event"): continue
            hist.append({"sym": j["symbol"], "qe": qe, "basis": b, "eps_raw": r["eps"],
                         "event_ts": r["event"].replace("T", " ")[:19], "shares": round(sh) if sh else ""})
        if shs: uni.append({"sym": j["symbol"], "shares": round(st.median(shs[-3:]))})   # median of last 3: guards 10x typos
    wcsv(os.path.join(LIVE, "eps_history.csv"), hist, ["sym", "qe", "basis", "eps_raw", "event_ts", "shares"])
    wcsv(os.path.join(LIVE, "universe.csv"), uni, ["sym", "shares"])
    ev = os.path.join(v2, "events_v2.tsv")
    s = sorted(float(r["sue"]) for r in csv.DictReader(open(ev), delimiter="\t") if r["sue"])
    cuts = [s[int(len(s) * p)] for p in (.2, .4, .6, .8)]
    json.dump({"cuts": cuts, "n": len(s), "source": "events_v2.tsv 2022-01..2026-11 pooled SUE (primary basis)",
               "made": str(dt.date.today())}, open(os.path.join(LIVE, "sue_cutpoints.json"), "w"), indent=1)
    if not os.path.exists(os.path.join(LIVE, "predictions.csv")):
        wcsv(os.path.join(LIVE, "predictions.csv"), [], PRED_COLS)
    print(f"bootstrap: {len(hist)} EPS rows, {len(uni)} universe symbols, cuts {cuts}")


# ---------------------------------------------------------------- update
def results_announcements(days):
    out = {}
    for i in range(days):
        d = dt.date.today() - dt.timedelta(days=i)
        s = d.strftime("%d-%m-%Y")
        rows = F.api("corporate-announcements", index="equities", from_date=s, to_date=s) or []
        for x in rows if isinstance(rows, list) else []:
            ds, t = x.get("desc") or "", (x.get("attchmntText") or "").lower()
            if ds in ("Financial Result Updates", "Outcome of Board Meeting") or "financial result" in t:
                if ds == "Outcome of Board Meeting" and "result" not in t: continue
                try: ts = dt.datetime.strptime(x.get("an_dt"), "%d-%b-%Y %H:%M:%S")
                except Exception: continue
                sym = x.get("symbol")
                if sym and (sym not in out or ts < out[sym]): out[sym] = ts
    return out


def update(days, first_qe):
    hf = os.path.join(LIVE, "eps_history.csv"); pf = os.path.join(LIVE, "predictions.csv")
    hist = rcsv(hf); preds = rcsv(pf); uni = {r["sym"]: r for r in rcsv(os.path.join(LIVE, "universe.csv"))}
    cuts = json.load(open(os.path.join(LIVE, "sue_cutpoints.json")))["cuts"]
    have = {(r["sym"], r["qe"]) for r in preds}
    hk = {(r["sym"], r["qe"], r["basis"]) for r in hist}
    ann = results_announcements(days)
    print(len(ann), "companies announced results in the last", days, "days")
    # retry companies whose filing is known but whose entry close was not yet available on an earlier run
    recent = dt.datetime.now() - dt.timedelta(days=20)
    for r in hist:
        if (r["qe"] >= str(first_qe) and (r["sym"], r["qe"]) not in have and r["sym"] not in ann
                and dt.datetime.fromisoformat(r["event_ts"]) > recent):
            ann[r["sym"]] = dt.datetime.fromisoformat(r["event_ts"])
    for sym, ts in sorted(ann.items()):
        integ = F.api("integrated-filing-results", index="equities", symbol=sym, type="Integrated Filing- Financials")
        new = []
        for x in (integ or {}).get("data", []) if isinstance(integ, dict) else []:
            b = {"Consolidated": "C", "Standalone": "S"}.get(x.get("consolidated")); qe = F.pdt(x.get("qe_Date"))
            if not b or not qe or not x.get("xbrl") or qe.date() < first_qe - dt.timedelta(days=800): continue
            if (sym, str(qe.date()), b) in hk: continue
            cands = [d for d in (F.pdt(x.get("broadcast_Date")), F.pdt(x.get("creation_Date")), F.xbrl_date(x["xbrl"])) if d]
            r = F.fetch_one(str(qe.date()), {"xbrl": x["xbrl"], "x": None})
            sh = r["pdup"] / r["face"] if r.get("pdup") and r.get("face") else ""
            row = {"sym": sym, "qe": str(qe.date()), "basis": b, "eps_raw": r.get("eps") if r.get("eps") is not None else "",
                   "event_ts": min(cands).strftime("%Y-%m-%d %H:%M:%S"), "shares": round(sh) if sh else ""}
            hist.append(row); hk.add((sym, row["qe"], b)); new.append(row)
            if sh: uni.setdefault(sym, {"sym": sym})["shares"] = round(sh)
        for qe_s in sorted({r["qe"] for r in hist if r["sym"] == sym and r["qe"] >= str(first_qe)}):
            qe = dt.date.fromisoformat(qe_s)
            if qe < first_qe or (sym, qe_s) in have: continue
            px = prices(sym)
            if not px: continue
            mine = [r for r in hist if r["sym"] == sym]
            fe = min(dt.datetime.fromisoformat(r["event_ts"]) for r in mine if r["qe"] == qe_s)
            ev = ts if qe < ts.date() <= fe.date() else fe            # earliest announcement, v1 D8 rule
            s, n, b = sue_for(mine, sym, qe, px["sp"])
            i0 = bisect.bisect_right(px["d"], ev.date())
            if s is None or i0 >= len(px["d"]) or i0 < 250: continue   # entry close not yet available -> retry later
            sh = float(uni.get(sym, {}).get("shares") or 0)
            mc = px["c"][i0] * split_factor(px["sp"], px["d"][i0]) * sh / 1e7 if sh else None
            if mc is None or not 500 <= mc <= 50000: continue
            ib = bisect.bisect_left(px["d"], ev.date()) - 1
            ar = px["c"][i0] / px["c"][ib] - 1 if ib >= 0 else None
            q5 = quintile(s, cuts)
            pred = {5: "TOP: will beat size-matched controls over 63 trading days",
                    1: "BOTTOM: will lag size-matched controls over 63 trading days"}.get(q5, "middle: no call")
            preds.append({"logged_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M"), "sym": sym, "qe": qe_s,
                          "fiscal_q": fiscal_label(qe), "basis": b, "event_ts": ev.strftime("%Y-%m-%d %H:%M"),
                          "entry_date": str(px["d"][i0]), "entry_close": round(px["c"][i0], 2), "mcap_cr": round(mc, 1),
                          "sue": round(s, 4), "n_prev": n, "ann_ret": round(ar, 5) if ar is not None else "",
                          "q5_prov": q5, "ann_up": int(ar is not None and ar > 0), "prediction": pred, "status": "open"})
            have.add((sym, qe_s)); print("logged", sym, qe_s, "SUE", round(s, 2), "Q", q5)
    wcsv(hf, hist, ["sym", "qe", "basis", "eps_raw", "event_ts", "shares"])
    wcsv(os.path.join(LIVE, "universe.csv"), list(uni.values()), ["sym", "shares"])
    wcsv(pf, preds, PRED_COLS)


# ---------------------------------------------------------------- finalize
def finalize():
    pf = os.path.join(LIVE, "predictions.csv"); preds = rcsv(pf)
    for qe_s in sorted({r["qe"] for r in preds}):
        qe = dt.date.fromisoformat(qe_s)
        if dt.date.today() < qe + dt.timedelta(days=65 if qe.month == 3 else 50): continue
        g = sorted([r for r in preds if r["qe"] == qe_s], key=lambda r: float(r["sue"]))
        if len(g) < 25: continue
        for i, r in enumerate(g): r["q5_final"] = 1 + min(4, int(i * 5 / len(g)))
        g2 = sorted(g, key=lambda r: float(r["mcap_cr"]))
        for i, r in enumerate(g2): r["tertile_final"] = 1 + min(2, int(i * 3 / len(g2)))
    wcsv(pf, preds, PRED_COLS); print("finalized")


# ---------------------------------------------------------------- score
def score():
    pf = os.path.join(LIVE, "predictions.csv"); preds = rcsv(pf)
    open_rows = [r for r in preds if r["status"] != "closed"]
    if not open_rows: print("nothing to score"); return
    uni = rcsv(os.path.join(LIVE, "universe.csv"))
    P = {}
    for u in uni:                        # ~1 Yahoo call per universe stock per run (cached 3 days)
        if not u.get("shares"): continue
        px = prices(u["sym"], max_age_days=3)
        if px and len(px["d"]) > 250: P[u["sym"]] = (px, float(u["shares"]), {d: i for i, d in enumerate(px["d"])})
    for r in open_rows:
        if r["sym"] not in P: continue
        px, _, di = P[r["sym"]]; e = dt.date.fromisoformat(r["entry_date"]); i0 = di.get(e)
        if i0 is None: continue
        done = True
        for h in (21, 63):
            if r.get(f"x{h}"): continue
            j1 = i0 + h
            if j1 >= len(px["d"]): done = False; continue
            a, b = px["d"][i0], px["d"][j1]; mc = float(r["mcap_cr"]); cr = []
            for s2, (p2, sh2, d2) in P.items():
                if s2 == r["sym"] or a not in d2 or b not in d2 or d2[a] < 250: continue
                m2 = p2["c"][d2[a]] * split_factor(p2["sp"], a) * sh2 / 1e7
                if 0.5 * mc <= m2 <= 2 * mc: cr.append(p2["c"][d2[b]] / p2["c"][d2[a]] - 1)
            rr = px["c"][j1] / px["c"][i0] - 1
            r.update({f"exit{h}": str(b), f"r{h}": round(rr, 5), f"nc{h}": len(cr)})
            if len(cr) >= 5:
                c = sum(cr) / len(cr); r[f"c{h}"] = round(c, 5); r[f"x{h}"] = round(rr - c, 5)
        r["status"] = "closed" if done and r.get("x63") else ("partial" if r.get("x21") else "open")
    wcsv(pf, preds, PRED_COLS)
    write_scorecard(preds)


def cl_stats(rows, field, shift=0.0):
    x = [(float(r[field]) - shift, dt.date.fromisoformat(r["entry_date"]).isocalendar()[:2]) for r in rows if r.get(field)]
    if len(x) < 10: return f"n={len(x)} (too few)"
    m = sum(v for v, _ in x) / len(x); g = {}
    for v, w in x: g[w] = g.get(w, 0.0) + (v - m)
    G = len(g); se = math.sqrt(G / (G - 1) * sum(e * e for e in g.values())) / len(x) if G > 1 else 0
    return f"{m * 100:+.2f}% (week-clustered t {m / se:.2f}, n={len(x)}, weeks={G})" if se else f"{m * 100:+.2f}% n={len(x)}"


def write_scorecard(preds):
    L = [f"# PEAD live scorecard (updated {dt.date.today()})", "",
         "Pre-registered in research_notes/Backtests/india_pead_v2.md (§Live forward test). Excess = stock − size-matched "
         "controls. Primary call: final top quintile, 63d, net of 1% must be > 0 with week-clustered t > 3 or CI ≠ 0.", ""]
    for qcol in ("q5_final", "q5_prov"):
        L.append(f"## By {qcol}")
        for h in (21, 63):
            for q, lbl in ((5, "top"), (1, "bottom")):
                g = [r for r in preds if r.get(qcol) and int(r[qcol]) == q]
                L.append(f"- {h}d {lbl}: {cl_stats(g, f'x{h}')}" + (f"; net of 1%: {cl_stats(g, f'x{h}', .01)}" if q == 5 else ""))
            up = [r for r in preds if r.get(qcol) and int(r[qcol]) == 5 and r.get("ann_up") == "1"]
            L.append(f"- {h}d top with up announcement reaction (H2 filter): {cl_stats(up, f'x{h}')}")
        L.append("")
    L.append("## By fiscal quarter (final top / bottom, 63d)")
    for fq in sorted({r["fiscal_q"] for r in preds}):
        g = [r for r in preds if r["fiscal_q"] == fq]
        L.append(f"- {fq}: logged {len(g)}; top {cl_stats([r for r in g if r.get('q5_final') == '5'], 'x63')}; "
                 f"bottom {cl_stats([r for r in g if r.get('q5_final') == '1'], 'x63')}")
    open(os.path.join(LIVE, "scorecard.md"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("bootstrap"); b.add_argument("v1"); b.add_argument("v2")
    u = sp.add_parser("update"); u.add_argument("--days", type=int, default=4)
    u.add_argument("--first-qe", default="2026-12-31")
    sp.add_parser("finalize"); sp.add_parser("score")
    a = ap.parse_args()
    if a.cmd == "bootstrap": bootstrap(a.v1, a.v2)
    elif a.cmd == "update": update(a.days, dt.date.fromisoformat(a.first_qe))
    elif a.cmd == "finalize": finalize()
    else: score()
