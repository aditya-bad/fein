#!/usr/bin/env python3
"""Step 1: candidate CIKs from dei:EntityPublicFloat frames (all filers, dead ones included)."""
import json, sys
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import sec_get, p

cands = {}
for y in range(2013, 2020):
    for q in range(1, 5):
        fr = f"CY{y}Q{q}I"
        d = sec_get(f"https://data.sec.gov/api/xbrl/frames/dei/EntityPublicFloat/USD/{fr}.json", p("frames", f"float_{fr}.json"))
        if not d:
            continue
        n = 0
        for r in d["data"]:
            if 1e8 <= r["val"] <= 4e10:
                cands.setdefault(r["cik"], r["entityName"]); n += 1
        print(fr, len(d["data"]), "in loose band", n)
json.dump(cands, open(p("candidates.json"), "w"))
print("candidates", len(cands))
