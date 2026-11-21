#!/usr/bin/env python3
"""Step 1: download NSE PIT (Reg 7) disclosures 2021-01-01..2025-01-31 in 7-day chunks (cached).
Usage: python3 s1_fetch_pit.py OUTDIR"""
import datetime as dt, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from tools.nse_fetch import api

out = os.path.join(sys.argv[1], "pit")
os.makedirs(out, exist_ok=True)
d, end = dt.date(2020, 12, 1), dt.date(2025, 1, 31)
while d <= end:
    e = min(d + dt.timedelta(days=6), end)
    fn = os.path.join(out, f"{d:%Y%m%d}.json")
    if not os.path.exists(fn):
        for attempt in range(3):
            try:
                j = api("corporates-pit", index="equities",
                        from_date=f"{d:%d-%m-%Y}", to_date=f"{e:%d-%m-%Y}")
                break
            except Exception as ex:
                print("retry", d, ex, flush=True); j = None
        if j is None:
            d = e + dt.timedelta(days=1); continue
        json.dump(j.get("data", []), open(fn, "w"))
        print(d, len(j.get("data", [])), flush=True)
    d = e + dt.timedelta(days=1)
