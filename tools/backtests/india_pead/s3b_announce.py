#!/usr/bin/env python3
"""Step 3b: exchange-announcement timestamps of results, to refine event dates (deviation D8).
A spot-check of 8 events showed the results-feed dates are often one day LATE (XBRL/filing stamps of
late-evening filings) and occasionally a revision weeks later. For each 'ok' symbol, fetch NSE
corporate-announcements 2015-01-01 -> 2026-03-31 (one call) and keep rows whose subject is
'Financial Result Updates' / 'Outcome of Board Meeting' (or whose text mentions financial results).
s4 then sets event = earliest such announcement in [quarter-end + 1 day, results-feed date].
Usage: python3 s3b_announce.py OUTDIR   -> OUTDIR/ann/<SYM>.json (list of [timestamp, desc])"""
import glob, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import nse_fetch as n

S = sys.argv[1]
A = os.path.join(S, "ann"); os.makedirs(A, exist_ok=True)
n.MIN_GAP = 1.0
for fn in sorted(glob.glob(os.path.join(S, "results", "*.json"))):
    j = json.load(open(fn))
    if j.get("status") != "ok": continue
    out = os.path.join(A, j["symbol"] + ".json")
    if os.path.exists(out): continue
    try:
        rows = n.announcements(j["symbol"], "01-01-2015", "31-03-2026")
    except Exception as e:
        print(j["symbol"], "error", e); continue
    keep = []
    for x in rows or []:
        d, t = x.get("desc") or "", (x.get("attchmntText") or "").lower()
        if d in ("Financial Result Updates", "Outcome of Board Meeting") or "financial result" in t:
            if d == "Outcome of Board Meeting" and "result" not in t: continue
            keep.append([x.get("an_dt"), d])
    json.dump(keep, open(out, "w"))
    print(j["symbol"], len(keep), flush=True)
