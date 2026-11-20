#!/usr/bin/env python3
"""Step 4: daily prices from Yahoo v8 chart API (adjusted close + split events).

Polite: >= 1.1 s between calls, cached per ticker as JSON (a missing/delisted ticker is cached
as {"missing": true} so the survivorship count is reproducible).
Usage: python3 s4_prices.py OUTDIR TICKER [TICKER ...]   or   --file tickers.txt
"""
import json, os, sys, time, urllib.request, urllib.error

P1, P2 = 1606780800, 1795132800  # 2020-12-01 .. 2026-11-20
_last = [0.0]


def fetch(t, pdir):
    p = os.path.join(pdir, t.replace("/", "_") + ".json")
    if os.path.exists(p):
        return json.load(open(p))
    yt = t.replace(".", "-")
    url = (f"https://query1.finance.yahoo.com/v8/finance/chart/{yt}?period1={P1}&period2={P2}"
           f"&interval=1d&events=split")
    for i in range(4):
        w = 1.1 - (time.time() - _last[0])
        if w > 0: time.sleep(w)
        _last[0] = time.time()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research script)"})
            with urllib.request.urlopen(req, timeout=40) as r:
                d = json.load(r)["chart"]["result"][0]
            ts = d.get("timestamp") or []
            if not ts:
                res = {"missing": True, "why": "no data"}; break
            q = d["indicators"]["quote"][0]
            res = {"ticker": t, "t": ts, "close": q.get("close"), "adj": d["indicators"]["adjclose"][0]["adjclose"],
                   "vol": q.get("volume"), "splits": (d.get("events") or {}).get("splits", {}),
                   "type": d["meta"].get("instrumentType"), "exch": d["meta"].get("exchangeName")}
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                res = {"missing": True, "why": "404"}; break
            if e.code == 429:
                time.sleep(30 * (i + 1)); continue
            res = {"missing": True, "why": f"http {e.code}"}
        except Exception as e:
            res = {"missing": True, "why": str(e)[:80]}; time.sleep(3)
    json.dump(res, open(p, "w"))
    return res


def main():
    out = sys.argv[1]; args = sys.argv[2:]
    if args and args[0] == "--file":
        args = [l.strip() for l in open(args[1]) if l.strip()]
    pdir = os.path.join(out, "prices"); os.makedirs(pdir, exist_ok=True)
    miss = 0
    for i, t in enumerate(args):
        r = fetch(t, pdir)
        miss += bool(r.get("missing"))
        if i % 100 == 0:
            print(f"{i}/{len(args)} missing so far {miss}", file=sys.stderr, flush=True)
    print(f"done {len(args)}, missing {miss}", file=sys.stderr)


if __name__ == "__main__":
    main()
