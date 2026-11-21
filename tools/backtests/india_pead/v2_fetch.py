#!/usr/bin/env python3
"""PEAD v2, step 1: full-universe quarterly results with CONSOLIDATED EPS where filed (FY2020+), plus standalone
fallback, plus Yahoo prices for symbols not already cached by v1. Pre-registration: research_notes/Backtests/india_pead_v2.md.

Universe: current NSE EQUITY_L.csv (EQ/BE) listed <= 2023-12-31, in v1's seeded order (seed 20261121, symbols listed
<= 2023-06-30), then the Jul-Dec 2023 listings alphabetically.
Per symbol:
  lists: api/corporates-financial-results (to ~Jan-2025) + api/integrated-filing-results (Dec-2024 ->), both bases;
  earliest filing per (quarter-end, basis); basis C = Consolidated, S = Non-Consolidated/Standalone.
  pre-filter: shares (latest filing) x unadjusted close must touch Rs 400-60,000 cr in 2021-2026, else 'out_of_range'.
  XBRL per quarter: C where filed; S where C not filed, or for every quarter if C coverage in the window is partial.
  v1 standalone rows (V1/results/SYM.json) are reused and never re-fetched.
Passes: A = quarters ended 2022-12-31 .. 2026-09-30 (fresh test); B = 2019-06-30 .. 2022-09-30 (2022-25 re-run).
Rates: NSE API host >= 1.0 s; NSE archive host >= 0.3 s (one thread); Yahoo >= 1.1 s. Resumable (per-symbol JSON).
Usage: python3 v2_fetch.py V1DIR V2DIR --pass A|B [--limit N] [--start I]  (two processes on two slices is fine)"""
import argparse, concurrent.futures as cf, csv, datetime as dt, gzip, json, os, random, re, sys, threading, time
import urllib.error, urllib.parse, urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
H = {"User-Agent": UA, "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9",
     "Accept-Encoding": "gzip", "Referer": "https://www.nseindia.in/"}
GAP = {"api": 1.0, "arc": 0.3, "yh": 1.1}
last = {k: 0.0 for k in GAP}
locks = {k: threading.Lock() for k in GAP}
PASS_RANGE = {"A": (dt.date(2022, 12, 31), dt.date(2026, 9, 30)), "B": (dt.date(2019, 6, 30), dt.date(2022, 9, 30))}


def get(url, host, binary=False, headers=None):
    for i in range(5):
        with locks[host]:
            w = GAP[host] - (time.time() - last[host])
            if w > 0: time.sleep(w)
            last[host] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers or H), timeout=40) as r:
                b = r.read()
                if r.headers.get("Content-Encoding") == "gzip": b = gzip.decompress(b)
            if binary: return b
            t = b.decode("utf-8", "replace")
            if t.lstrip().startswith("<"): raise ValueError("html")
            return json.loads(t)
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(5 * 2 ** i)
        except Exception:
            time.sleep(3 * 2 ** i)
    return None


def api(path, **kw):
    return get("https://www.nseindia.in/api/" + path + "?" + urllib.parse.urlencode(kw), "api")


def pdt(s):
    if not s: return None
    for f in ("%d-%b-%Y %H:%M:%S", "%d-%b-%Y %H:%M", "%d-%b-%Y"):
        try: return dt.datetime.strptime(s.strip().title(), f)
        except Exception: pass
    return None


def xbrl_date(url):
    m = re.search(r"_(\d{8})(\d{6})(?:_WEB)?\.xml$", url or "")
    if not m: return None
    try: return dt.datetime.strptime(m.group(1), "%d%m%Y")
    except Exception: return None


def num(x):
    try: return float(str(x).replace(",", ""))
    except Exception: return None


EPS_TAGS = ["BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations",
            "BasicEarningsLossPerShareFromContinuingOperations", "BasicEarningsLossPerShare",
            "BasicEarningsPerShareAfterExtraordinaryItems", "BasicEarningsPerShareBeforeExtraordinaryItems"]
REV_TAGS = ["RevenueFromOperations", "InterestEarned", "Income"]


def parse_xbrl(b, qe):   # identical logic to v1 s3_results.parse_xbrl
    t = b.decode("utf-8", "replace")
    ctx = {}
    for m in re.finditer(r"<xbrli:context id=\"([^\"]+)\">(.*?)</xbrli:context>", t, re.S):
        body = m.group(2)
        if "xbrldi:" in body: continue
        sd = re.search(r"<xbrli:startDate>([^<]+)<", body); ed = re.search(r"<xbrli:endDate>([^<]+)<", body)
        if sd and ed: ctx[m.group(1)] = (sd.group(1).strip(), ed.group(1).strip())
    qctx = set()
    for c, (s, e) in ctx.items():
        try: s, e = dt.date.fromisoformat(s[:10]), dt.date.fromisoformat(e[:10])
        except Exception: continue
        if e == qe and 80 <= (e - s).days <= 100: qctx.add(c)
    if not qctx and "OneD" not in ctx: qctx.add("OneD")
    vals = {}
    for m in re.finditer(r"<[\w\-]+:(\w+)\s[^>]*contextRef=\"([^\"]+)\"[^>]*>([^<]*)<", t):
        tag, c, v = m.groups()
        if tag in vals: continue
        if tag in ("PaidUpValueOfEquityShareCapital", "FaceValueOfEquityShareCapital") or c in qctx:
            x = num(v)
            if x is not None: vals[tag] = x
    return {"eps": next((vals[k] for k in EPS_TAGS if k in vals), None),
            "rev": next((vals[k] for k in REV_TAGS if k in vals), None), "np": vals.get("ProfitLossForPeriod"),
            "pdup": vals.get("PaidUpValueOfEquityShareCapital"), "face": vals.get("FaceValueOfEquityShareCapital"),
            "unit": 1.0, "nq": len(qctx)}


def parse_detail(d):
    r = (d or {}).get("resultsData2") or {}
    f = lambda *ks: next((num(r[k]) for k in ks if num(r.get(k)) is not None), None)
    eps = f("re_basic_eps_for_cont_dic_opr", "re_bsc_eps_bfr_exi", "re_basic_eps")
    if eps == 0 and f("re_bsc_eps_bfr_exi") not in (None, 0): eps = f("re_bsc_eps_bfr_exi")
    return {"eps": eps, "rev": f("re_net_sale", "re_rev_frm_opr", "re_int_earned", "re_total_inc", "re_gro_inc"),
            "np": f("re_net_profit", "re_con_pro_loss", "re_proloss_ord_act"),
            "pdup": f("re_pdup"), "face": f("re_face_val"), "unit": 1e5}


def universe(v1):
    rows = list(csv.reader(open(os.path.join(v1, "EQUITY_L.csv"), encoding="utf-8", errors="replace")))
    hdr = [h.strip() for h in rows[0]]
    a, b = [], []
    for r in rows[1:]:
        d = dict(zip(hdr, [x.strip() for x in r]))
        if d.get("SERIES") not in ("EQ", "BE"): continue
        try: lst = dt.datetime.strptime(d["DATE OF LISTING"], "%d-%b-%Y").date()
        except Exception: continue
        if lst <= dt.date(2023, 6, 30): a.append(d["SYMBOL"])
        elif lst <= dt.date(2023, 12, 31): b.append(d["SYMBOL"])
    a.sort(); random.Random(20261121).shuffle(a)
    return a + sorted(b)


def price_path(v1, v2, sym):
    for d in (v2, v1):
        fn = os.path.join(d, "prices", sym + ".json")
        if os.path.exists(fn): return fn
    return None


def ensure_prices(v1, v2, sym):
    if price_path(v1, v2, sym): return
    u = ("https://query1.finance.yahoo.com/v8/finance/chart/" + urllib.parse.quote(sym + ".NS") +
         "?period1=1420070400&period2=1795000000&interval=1d&events=split")
    j = get(u, "yh", headers={"User-Agent": "Mozilla/5.0"})
    os.makedirs(os.path.join(v2, "prices"), exist_ok=True)
    json.dump(j if j is not None else {"missing": True}, open(os.path.join(v2, "prices", sym + ".json"), "w"))


def unadj_close(fn):
    try:
        r = json.load(open(fn))["chart"]["result"][0]
        ts, cl = r["timestamp"], r["indicators"]["quote"][0]["close"]
        sp = sorted((int(k), v["numerator"] / v["denominator"]) for k, v in (r.get("events", {}).get("splits") or {}).items())
    except Exception:
        return []
    out = []
    for t, c in zip(ts, cl):
        if c is None: continue
        f = 1.0
        for s, ratio in sp:
            if s > t: f *= ratio
        out.append((dt.date.fromtimestamp(t), c * f))
    return out


def lists(sym):
    """{(qe_iso, basis): {event, xbrl, x(old-feed row or None)}} earliest timestamp per key."""
    best = {}
    def put(k, ev, xb, x):
        if k not in best or ev < dt.datetime.fromisoformat(best[k]["event"]):
            best[k] = {"event": ev.isoformat(sep=" "), "xbrl": xb, "x": x}
    old = api("corporates-financial-results", index="equities", symbol=sym, period="Quarterly")
    for x in old if isinstance(old, list) else []:
        if x.get("period") != "Quarterly": continue
        b = {"Consolidated": "C", "Non-Consolidated": "S"}.get(x.get("consolidated"))
        qe = pdt(x.get("toDate"))
        if not b or not qe or qe.date() < dt.date(2019, 6, 30): continue
        cands = [d for d in (pdt(x.get("broadCastDate")), pdt(x.get("filingDate")), xbrl_date(x.get("xbrl"))) if d]
        if not cands or min(cands).date() < qe.date(): continue
        keep = {k: x.get(k) for k in ("params", "seqNumber", "industry", "oldNewFlag", "reInd", "format")}
        put((str(qe.date()), b), min(cands), x.get("xbrl"), keep)
    integ = api("integrated-filing-results", index="equities", symbol=sym, type="Integrated Filing- Financials")
    for x in (integ or {}).get("data", []) if isinstance(integ, dict) else []:
        b = {"Consolidated": "C", "Standalone": "S"}.get(x.get("consolidated"))
        qe = pdt(x.get("qe_Date"))
        if not b or not qe or not x.get("xbrl") or qe.date() < dt.date(2024, 6, 30): continue
        cands = [d for d in (pdt(x.get("broadcast_Date")), pdt(x.get("creation_Date")), xbrl_date(x["xbrl"])) if d]
        if not cands or min(cands).date() < qe.date(): continue
        put((str(qe.date()), b), min(cands), x["xbrl"], None)
    return best, (isinstance(old, list), isinstance(integ, dict))


def fetch_one(qe, rec):
    xb = rec.get("xbrl") or ""
    if xb.endswith(".xml"):
        b = get(xb, "arc", binary=True)
        if b:
            r = parse_xbrl(b, dt.date.fromisoformat(qe)); r["src"] = "xbrl"
            if r["eps"] is not None or rec.get("x") is None: return r
    x = rec.get("x")
    if not x: return {"src": "none"}
    d = api("corporates-financial-results-data", index="equities", params=x["params"], seq_id=x["seqNumber"],
            industry=x.get("industry") or "-", frOldNewFlag=x.get("oldNewFlag") or "", ind=x.get("reInd") or "",
            format=x.get("format") or "")
    r = parse_detail(d); r["src"] = "detail"; return r


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("v1"); ap.add_argument("v2")
    ap.add_argument("--pass", dest="p", required=True, choices=["A", "B"]); ap.add_argument("--limit", type=int, default=10 ** 9)
    ap.add_argument("--start", type=int, default=0)
    a = ap.parse_args()
    R = os.path.join(a.v2, "results"); L = os.path.join(a.v2, "lists"); os.makedirs(R, exist_ok=True); os.makedirs(L, exist_ok=True)
    lo, hi = PASS_RANGE[a.p]
    syms = universe(a.v1)[:a.limit]
    ex = cf.ThreadPoolExecutor(2)   # both workers share the archive/api rate locks
    for i, sym in enumerate(syms):
        if i < a.start: continue
        t0 = time.time()
        fn = os.path.join(R, sym + ".json")
        j = json.load(open(fn)) if os.path.exists(fn) else {"symbol": sym, "passes": [], "q": {}}
        if a.p in j["passes"] or j.get("status") in ("out_of_range", "no_quarters", "no_prices"):
            continue
        lf = os.path.join(L, sym + ".json")
        if os.path.exists(lf):
            best = {tuple(k.split("|")): v for k, v in json.load(open(lf)).items()}
        else:
            best, ok = lists(sym)
            if not any(ok):
                print(i, sym, "list_fail", flush=True); continue
            json.dump({"|".join(k): v for k, v in best.items()}, open(lf, "w"))
        if not best:
            j["status"] = "no_quarters"; json.dump(j, open(fn, "w")); print(i, sym, "no_quarters", flush=True); continue
        ensure_prices(a.v1, a.v2, sym)
        # v1 standalone cache
        v1r = {}
        v1f = os.path.join(a.v1, "results", sym + ".json")
        if os.path.exists(v1f):
            jj = json.load(open(v1f))
            for q in jj.get("quarters", []) if jj.get("status") == "ok" else []:
                if q.get("eps") is not None: v1r[q["qe"]] = q
        if "status" not in j:   # pre-filter once
            k0 = max(best, key=lambda k: k[0])
            r0 = fetch_one(k0[0], best[k0]); j["q"]["|".join(k0)] = dict(r0, event=best[k0]["event"])
            px = unadj_close(price_path(a.v1, a.v2, sym)) if price_path(a.v1, a.v2, sym) else []
            if not px:
                j["status"] = "no_prices"; json.dump(j, open(fn, "w")); print(i, sym, "no_prices", flush=True); continue
            if r0.get("pdup") and r0.get("face"):
                sh = r0["pdup"] * r0["unit"] / r0["face"]
                mc = [c * sh / 1e7 for d, c in px if dt.date(2021, 1, 1) <= d]
                if mc and (max(mc) < 400 or min(mc) > 60000):
                    j.update(status="out_of_range", mcap_cr_min=min(mc), mcap_cr_max=max(mc))
                    json.dump(j, open(fn, "w")); print(i, sym, "out_of_range", flush=True); continue
            j["status"] = "ok"
        qes = sorted({k[0] for k in best if lo <= dt.date.fromisoformat(k[0]) <= hi})
        hasC = [q for q in qes if (q, "C") in best]
        partialC = 0 < len(hasC) < len(qes)
        todo = []
        for q in qes:
            if (q, "C") in best: todo.append((q, "C"))
            if (q, "S") in best and ((q, "C") not in best or partialC) and q not in v1r: todo.append((q, "S"))
        futs = {k: ex.submit(fetch_one, k[0], best[k]) for k in todo if "|".join(k) not in j["q"]}
        for k, f in futs.items():
            try: r = f.result()
            except Exception as e: r = {"src": "error", "err": str(e)[:80]}
            j["q"]["|".join(k)] = dict(r, event=best[k]["event"])
        for q, r in v1r.items():   # reuse v1 standalone rows (any period)
            kk = q + "|S"
            if kk not in j["q"]: j["q"][kk] = dict(r, src=(r.get("src") or "") + "_v1")
        j["passes"].append(a.p)
        json.dump(j, open(fn, "w"))
        print(i, sym, a.p, len(futs), f"{time.time() - t0:.0f}s", flush=True)
    print("done pass", a.p)


if __name__ == "__main__":
    main()
