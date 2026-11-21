#!/usr/bin/env python3
"""Step 3: quarterly STANDALONE results (EPS, revenue, net profit, paid-up capital, face value) and
filing timestamps from NSE, for symbols in sample.txt (in order).

Sources (all www.nseindia.in / nsearchives.nseindia.in, tested 2026-11-21):
  - api/corporates-financial-results?index=equities&symbol=X&period=Quarterly  (filings list to Jan-2025)
  - api/corporates-financial-results-data?...params=..&seq_id=..  (figures; used for pre-2018 'Old' format
    filings and any filing without an XBRL link; amounts in Rs lakh)
  - the filing's XBRL (nsearchives .../corporate/xbrl/*.xml; amounts in Rs)
  - api/integrated-filing-results?index=equities&symbol=X&type=Integrated Filing- Financials  (2025 onwards,
    SEBI 'Integrated Filing' regime; figures from its XBRL)
Pre-filter (saves calls): shares (latest pre-2025 filing) x unadjusted Yahoo close must touch
Rs 400-60,000 cr at some point in 2018-2025, else the symbol is marked 'out_of_range' and skipped.
Usage: python3 s3_results.py OUTDIR [max_symbols]   -> OUTDIR/results/<SYM>.json
Rate: API host >=1.0 s between calls, archive host >=0.5 s; two worker threads (one per host)."""
import concurrent.futures as cf, datetime as dt, gzip, json, os, re, sys, threading, time
import urllib.error, urllib.parse, urllib.request

S = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
OUT = os.path.join(S, "results"); os.makedirs(OUT, exist_ok=True)
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
H = {"User-Agent": UA, "Accept": "application/json, text/plain, */*", "Accept-Language": "en-US,en;q=0.9",
     "Accept-Encoding": "gzip", "Referer": "https://www.nseindia.in/"}
GAP = {"api": 1.0, "arc": 0.5}
last = {"api": 0.0, "arc": 0.0}
locks = {"api": threading.Lock(), "arc": threading.Lock()}


def get(url, host, binary=False):
    for i in range(5):
        with locks[host]:
            w = GAP[host] - (time.time() - last[host])
            if w > 0: time.sleep(w)
            last[host] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=40) as r:
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


def pd(s, fmts=("%d-%b-%Y %H:%M:%S", "%d-%b-%Y %H:%M", "%d-%b-%Y")):
    if not s: return None
    for f in fmts:
        try: return dt.datetime.strptime(s.strip().title() if f.startswith("%d-%b") else s.strip(), f)
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


def parse_xbrl(b, qe):
    t = b.decode("utf-8", "replace")
    ctx = {}
    for m in re.finditer(r"<xbrli:context id=\"([^\"]+)\">(.*?)</xbrli:context>", t, re.S):
        body = m.group(2)
        if "xbrldi:" in body: continue
        sd = re.search(r"<xbrli:startDate>([^<]+)<", body); ed = re.search(r"<xbrli:endDate>([^<]+)<", body)
        if sd and ed: ctx[m.group(1)] = (sd.group(1).strip(), ed.group(1).strip())
    qctx = set()
    for c, (s, e) in ctx.items():
        try:
            s, e = dt.date.fromisoformat(s[:10]), dt.date.fromisoformat(e[:10])
        except Exception: continue
        if e == qe and 80 <= (e - s).days <= 100: qctx.add(c)
    if not qctx and "OneD" not in ctx:   # some 2018-21 NSE files omit the OneD context definition;
        qctx.add("OneD")                 # NSE convention: OneD = current quarter (checked on 2023 files)
    vals = {}
    for m in re.finditer(r"<[\w\-]+:(\w+)\s[^>]*contextRef=\"([^\"]+)\"[^>]*>([^<]*)<", t):
        tag, c, v = m.groups()
        if tag in vals: continue
        if tag in ("PaidUpValueOfEquityShareCapital", "FaceValueOfEquityShareCapital") or c in qctx:
            x = num(v)
            if x is not None: vals[tag] = x
    eps = next((vals[k] for k in EPS_TAGS if k in vals), None)
    rev = next((vals[k] for k in REV_TAGS if k in vals), None)
    return {"eps": eps, "rev": rev, "np": vals.get("ProfitLossForPeriod"),
            "pdup": vals.get("PaidUpValueOfEquityShareCapital"), "face": vals.get("FaceValueOfEquityShareCapital"),
            "unit": 1.0, "nq": len(qctx)}


def parse_detail(d):
    r = (d or {}).get("resultsData2") or {}
    f = lambda *ks: next((num(r[k]) for k in ks if num(r.get(k)) not in (None,)), None)
    eps = f("re_basic_eps_for_cont_dic_opr", "re_bsc_eps_bfr_exi", "re_basic_eps")
    if eps == 0 and f("re_bsc_eps_bfr_exi") not in (None, 0): eps = f("re_bsc_eps_bfr_exi")
    return {"eps": eps, "rev": f("re_net_sale", "re_rev_frm_opr", "re_int_earned", "re_total_inc", "re_gro_inc"),
            "np": f("re_net_profit", "re_con_pro_loss", "re_proloss_ord_act"),
            "pdup": f("re_pdup"), "face": f("re_face_val"), "unit": 1e5, "fmt": d.get("resultFormat") if d else None}


def load_prices(sym):
    fn = os.path.join(S, "prices", sym + ".json")
    if not os.path.exists(fn): return None
    j = json.load(open(fn))
    try:
        r = j["chart"]["result"][0]
        ts, cl = r["timestamp"], r["indicators"]["quote"][0]["close"]
        sp = sorted((int(k), v["numerator"] / v["denominator"]) for k, v in (r.get("events", {}).get("splits") or {}).items())
    except Exception:
        return None
    out = []
    for t, c in zip(ts, cl):
        if c is None: continue
        f = 1.0
        for st, ratio in sp:
            if st > t: f *= ratio
        out.append((dt.date.fromtimestamp(t), c * f))   # unadjusted close
    return out


def do_symbol(sym, ex_api, ex_arc):
    fn = os.path.join(OUT, sym + ".json")
    if os.path.exists(fn): return "cached"
    lst = api("corporates-financial-results", index="equities", symbol=sym, period="Quarterly")
    if not isinstance(lst, list):
        json.dump({"symbol": sym, "status": "no_list"}, open(fn, "w")); return "no_list"
    best = {}
    for x in lst:
        if x.get("consolidated") != "Non-Consolidated" or x.get("period") != "Quarterly": continue
        qe = pd(x.get("toDate"))
        if not qe or qe.date() < dt.date(2015, 3, 31): continue
        cands = [d for d in (pd(x.get("broadCastDate")), pd(x.get("filingDate")), xbrl_date(x.get("xbrl"))) if d]
        if not cands: continue
        ev = min(cands)
        if (ev.date() - qe.date()).days < 0: continue
        k = qe.date()
        if k not in best or ev < best[k][0]: best[k] = (ev, x)
    integ = api("integrated-filing-results", index="equities", symbol=sym, type="Integrated Filing- Financials")
    ib = {}
    for x in (integ or {}).get("data", []) if isinstance(integ, dict) else []:
        if x.get("consolidated") != "Standalone" or not x.get("xbrl"): continue
        qe = pd(x.get("qe_Date"))
        if not qe or qe.date() < dt.date(2025, 1, 1) or qe.date() > dt.date(2025, 12, 31): continue
        ev = pd(x.get("broadcast_Date")) or pd(x.get("creation_Date")) or xbrl_date(x["xbrl"])
        if not ev: continue
        k = qe.date()
        if k not in ib or ev < ib[k][0]: ib[k] = (ev, x)
    if not best and not ib:
        json.dump({"symbol": sym, "status": "no_quarters"}, open(fn, "w")); return "no_quarters"
    # --- pre-filter on market cap using the latest pre-2025 filing
    px = load_prices(sym)
    def fetch_one(k, ev, x, kind):
        if kind == "integ" or (x.get("xbrl") or "").endswith(".xml"):
            b = get(x["xbrl"], "arc", binary=True)
            if b:
                r = parse_xbrl(b, k); r["src"] = "xbrl"
                if r["eps"] is not None or kind == "integ": return r
        if kind == "integ": return {"src": "none"}
        d = api("corporates-financial-results-data", index="equities", params=x["params"], seq_id=x["seqNumber"],
                industry=x.get("industry") or "-", frOldNewFlag=x.get("oldNewFlag") or "", ind=x.get("reInd") or "",
                format=x.get("format") or "")
        r = parse_detail(d); r["src"] = "detail"; return r
    rows = {}
    if best:
        k0 = max(best)
        r0 = fetch_one(k0, *best[k0], "old"); rows[k0] = r0
        if px and r0.get("pdup") and r0.get("face"):
            sh = r0["pdup"] * r0["unit"] / r0["face"]
            mc = [c * sh / 1e7 for d, c in px if dt.date(2018, 1, 1) <= d <= dt.date(2025, 12, 31)]
            if mc and (max(mc) < 400 or min(mc) > 60000):
                json.dump({"symbol": sym, "status": "out_of_range", "mcap_cr_min": min(mc), "mcap_cr_max": max(mc)},
                          open(fn, "w"))
                return "out_of_range"
    futs = {}
    for k, (ev, x) in best.items():
        if k in rows: continue
        ex = ex_arc if (x.get("xbrl") or "").endswith(".xml") else ex_api
        futs[k] = ex.submit(fetch_one, k, ev, x, "old")
    for k, (ev, x) in ib.items():
        if k in best: continue
        futs[k] = ex_arc.submit(fetch_one, k, ev, x, "integ")
    for k, f in futs.items():
        try: rows[k] = f.result()
        except Exception as e: rows[k] = {"src": "error", "err": str(e)[:100]}
    q = []
    for k in sorted(rows):
        ev = (best.get(k) or ib.get(k))[0]
        q.append(dict(rows[k], qe=str(k), event=ev.strftime("%Y-%m-%d %H:%M:%S")))
    json.dump({"symbol": sym, "status": "ok", "quarters": q}, open(fn, "w"))
    return "ok"


if __name__ == "__main__":
    syms = open(os.path.join(S, "sample.txt")).read().split()[:N]
    ex_api, ex_arc = cf.ThreadPoolExecutor(1), cf.ThreadPoolExecutor(1)
    for i, s in enumerate(syms):
        t0 = time.time()
        try: st = do_symbol(s, ex_api, ex_arc)
        except Exception as e: st = "error " + str(e)[:80]
        print(i, s, st, f"{time.time() - t0:.0f}s", flush=True)
