#!/usr/bin/env python3
"""Step 3: Yahoo v8 daily prices (split events included) for every symbol in universe.txt + ^CRSLDX.
>=1.1 s between calls, cached. Usage: python3 s3_prices.py OUTDIR [symbols_file]"""
import json, os, sys, time, urllib.parse, urllib.request
S = sys.argv[1]
syms = open(sys.argv[2] if len(sys.argv) > 2 else os.path.join(S, "universe.txt")).read().split()
P = os.path.join(S, "prices"); os.makedirs(P, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0"}  # long browser UA strings got HTTP 429 (2026-11-21)
def fetch(t):
    u = ("https://query1.finance.yahoo.com/v8/finance/chart/" + urllib.parse.quote(t) +
         "?period1=1546300800&period2=1795000000&interval=1d&events=split")
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 404: return {"missing": True}
            time.sleep(5 * 2 ** i)
        except Exception:
            time.sleep(5 * 2 ** i)
    return None
for s in ["^CRSLDX"] + syms:
    fn = os.path.join(P, s.replace("/", "_") + ".json")
    if os.path.exists(fn): continue
    t0 = time.time()
    j = fetch(s if s.startswith("^") else s + ".NS")
    if j is not None:
        json.dump(j, open(fn, "w"))
    time.sleep(max(0, 1.1 - (time.time() - t0)))
print("done")
