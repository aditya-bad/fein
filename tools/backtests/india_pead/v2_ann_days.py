#!/usr/bin/env python3
"""PEAD v2: results-announcement timestamps for ALL companies, one calendar day per call (NSE corporate-announcements,
no symbol). Keeps rows with subject 'Financial Result Updates', or 'Outcome of Board Meeting' whose text mentions results
(same filter as v1 s3b_announce.py). Used for event dating (v1 deviation D8) for symbols without a v1 ann/ cache.
Order: newest day first (2026 fresh period first). Rate >= 1.5 s/call. Resumable.
Usage: python3 v2_ann_days.py V2DIR FROM_YYYY-MM-DD TO_YYYY-MM-DD   -> V2DIR/anndays/<date>.json [[sym, an_dt, desc], ...]"""
import datetime as dt, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import nse_fetch as n

V2, d0, d1 = sys.argv[1], dt.date.fromisoformat(sys.argv[2]), dt.date.fromisoformat(sys.argv[3])
A = os.path.join(V2, "anndays"); os.makedirs(A, exist_ok=True)
n.MIN_GAP = 1.5
d = d1
while d >= d0:
    fn = os.path.join(A, str(d) + ".json")
    if not os.path.exists(fn):
        s = d.strftime("%d-%m-%Y")
        try:
            rows = n.announcements(None, s, s)
        except Exception as e:
            print(d, "error", e, flush=True); d -= dt.timedelta(days=1); continue
        keep = []
        for x in rows or []:
            ds, t = x.get("desc") or "", (x.get("attchmntText") or "").lower()
            if ds in ("Financial Result Updates", "Outcome of Board Meeting") or "financial result" in t:
                if ds == "Outcome of Board Meeting" and "result" not in t: continue
                keep.append([x.get("symbol"), x.get("an_dt"), ds])
        json.dump({"n_all": len(rows or []), "rows": keep}, open(fn, "w"))
        print(d, len(rows or []), len(keep), flush=True)
    d -= dt.timedelta(days=1)
print("done")
