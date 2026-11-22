#!/usr/bin/env python3
"""Step 1: every NSE quarterly-result filing 2018-01-01 .. 2025-03-31 from the all-company feed
(api/corporates-financial-results, 7-day windows), to find NSE filers that are NOT in today's equity list
(dead / delisted / merged). NSE maps renamed live firms to their current symbol, so a filer symbol missing from
EQUITY_L (by symbol and ISIN) is a firm that left the exchange. No price or outcome is fetched here.
Usage: python3 s1_filers.py   -> $OUT/filers/<from>.json, $OUT/filers_all.json"""
import datetime as dt, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K
import v2_fetch as V
K.single_stream(V)
D = os.path.join(K.OUT, "filers"); os.makedirs(D, exist_ok=True)
a, end = dt.date(2018, 1, 1), dt.date(2025, 3, 31)
keep = ("symbol", "isin", "companyName", "toDate", "consolidated", "broadCastDate", "period")
while a <= end:
    b = min(a + dt.timedelta(days=6), end)
    fn = os.path.join(D, a.isoformat() + ".json")
    if not os.path.exists(fn):
        d = V.api("corporates-financial-results", index="equities", period="Quarterly",
                  from_date=a.strftime("%d-%m-%Y"), to_date=b.strftime("%d-%m-%Y"))
        rows = [{k: x.get(k) for k in keep} for x in d] if isinstance(d, list) else None
        json.dump({"from": str(a), "to": str(b), "rows": rows}, open(fn, "w"))
        print(a, None if rows is None else len(rows), flush=True)
    a = b + dt.timedelta(days=1)
print("done")
