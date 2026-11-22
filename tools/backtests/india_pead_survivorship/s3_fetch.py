#!/usr/bin/env python3
"""Step 3: data for the sampled MISSING firms (pre-registered in india_pead_survivorship.md).
  --stage screener : company id (reuse the solvency cache bt_solv_in when the firm is there; else /company/<NSE sym>/,
                     then /company/<BSE code>/), then the weekly chart Price-Market Cap to Sales-Sales (same query as
                     solvency_india/s2_fetch.py). Writes $OUT/prices/<SYM>.json in v1's Yahoo-like layout (weekly
                     closes; no split events) so v1's s3_results pre-filter can read it. One screener stream, >= 1.5 s.
  --stage nse      : v1 s3_results.do_symbol (standalone quarterly EPS + filing dates, unchanged) for symbols that have
                     a price series, then v1 s3b_announce logic (results announcements). One NSE stream, >= 1.5 s.
                     Waits for the screener stage, in list order.
Status: $OUT/status_<stage>.json. Resumable."""
import argparse, csv, datetime as dt, json, os, re, sys, time, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

ap = argparse.ArgumentParser(); ap.add_argument("--stage", required=True, choices=["screener", "nse"])
ap.add_argument("--limit", type=int); a = ap.parse_args()
miss = [r for r in csv.DictReader(open(os.path.join(K.OUT, "missing.csv"))) if r["sampled"] == "1"][: a.limit]
stp = lambda s: os.path.join(K.OUT, f"status_{s}.json")
def jl(p, d):
    try: return json.load(open(p))
    except Exception: return d
def js(p, o):
    json.dump(o, open(p + ".tmp", "w")); os.replace(p + ".tmp", p)

if a.stage == "screener":
    sys.path.insert(0, os.path.join(K.ROOT, "tools", "detectors"))
    import solvency_screen as SS
    SS.GAP = 1.55
    # solvency cache: nse symbol / isin / bse code -> (slug, cid)
    st_s = jl(os.path.join(K.SOLV, "fetch_status.json"), {})
    known = {}
    for r in csv.DictReader(open(os.path.join(K.SOLV, "frame.csv"))):
        s = st_s.get(r["key"], {})
        if s.get("page") == "ok" and s.get("cid"):
            for k in (r["nse_symbol"], r["isin"], r["bse_code"]):
                if k: known.setdefault(k, (s["slug"], s["cid"]))
    st = jl(stp("screener"), {})
    for i, r in enumerate(miss):
        sym = r["symbol"]
        if sym in st: continue
        rec = {}
        try:
            hit = known.get(sym) or known.get(r["isin"]) or known.get(r["bse_code"])
            if hit:
                slug, cid = hit; rec["src"] = "solv_cache"; d = os.path.join(K.SOLV, "sc", slug)
            else:
                slug = cid = None
                for cand in [sym] + ([r["bse_code"]] if r["bse_code"] else []):
                    d = os.path.join(K.OUT, "sc", cand)
                    pg = SS.cached(os.path.join(d, "page.html"), 1e6,
                                   lambda: SS.curl(f"https://www.screener.in/company/{urllib.parse.quote(cand)}/"))
                    m = re.search(r'data-company-id="(\d+)"', pg or "")
                    if m: slug, cid = cand, m.group(1); break
                rec["src"] = "fetched" if cid else "no_page"
            if cid:
                q = "Price-Market+Cap+to+Sales-Sales"
                txt = SS.cached(os.path.join(d, "chart.json"), 1e6,
                                lambda: SS.curl(f"https://www.screener.in/api/company/{cid}/chart/?q={q}&days=10000"))
                ch = json.loads(txt) if txt else {}
                px = [(x[0], float(x[1])) for ds in ch.get("datasets", []) if ds.get("metric") == "Price"
                      for x in ds["values"] if x[1] not in (None, "")]
                rec.update(slug=slug, cid=cid, n_px=len(px), px_first=px[0][0] if px else None,
                           px_last=px[-1][0] if px else None)
                if px:
                    ts = [int(dt.datetime.combine(dt.date.fromisoformat(d0), dt.time(12)).timestamp()) for d0, _ in px]
                    os.makedirs(os.path.join(K.OUT, "prices"), exist_ok=True)
                    json.dump({"chart": {"result": [{"timestamp": ts, "indicators": {"quote": [{"close": [p for _, p in px]}]},
                                                    "events": {}}]}, "source": "screener_weekly", "chart_path": d},
                              open(os.path.join(K.OUT, "prices", sym + ".json"), "w"))
        except Exception as e:
            rec["error"] = str(e)[:200]
        st[sym] = rec; js(stp("screener"), st)
        print(i, sym, rec.get("src"), rec.get("n_px"), rec.get("px_last"), flush=True)
    print("screener done")
else:
    sys.argv = [sys.argv[0], K.OUT]
    import s3_results as R          # v1 code, unchanged (reads S = $OUT, writes $OUT/results)
    import nse_fetch as N
    K.single_stream(R); N.MIN_GAP = K.GAP
    import concurrent.futures as cf
    ex = cf.ThreadPoolExecutor(1)    # one worker for both hosts -> one stream
    os.makedirs(os.path.join(K.OUT, "ann"), exist_ok=True)
    st = jl(stp("nse"), {})
    for i, r in enumerate(miss):
        sym = r["symbol"]
        while True:
            ss = jl(stp("screener"), {})
            if sym in ss: break
            time.sleep(20)
        if sym in st: continue
        if not ss[sym].get("n_px"):
            st[sym] = "no_prices"; js(stp("nse"), st); continue
        t0 = time.time()
        try: res = R.do_symbol(sym, ex, ex)
        except Exception as e: res = "error " + str(e)[:80]
        if res in ("ok", "cached"):
            out = os.path.join(K.OUT, "ann", sym + ".json")
            if not os.path.exists(out):
                try:
                    time.sleep(K.GAP)
                    rows = N.announcements(sym, "01-01-2015", "31-03-2026"); keep = []
                    for x in rows or []:
                        d, t = x.get("desc") or "", (x.get("attchmntText") or "").lower()
                        if d in ("Financial Result Updates", "Outcome of Board Meeting") or "financial result" in t:
                            if d == "Outcome of Board Meeting" and "result" not in t: continue
                            keep.append([x.get("an_dt"), d])
                    json.dump(keep, open(out, "w"))
                except Exception as e:
                    res += " ann_err " + str(e)[:60]
        st[sym] = res; js(stp("nse"), st)
        print(i, sym, res, f"{time.time()-t0:.0f}s", flush=True)
    print("nse done")
