#!/usr/bin/env python3
"""Step 6: survivorship audit of events dropped because Yahoo has no price history.
For each missing event issuer, read SEC submissions and classify the exit:
  acquired   = filed DEFM14A / PREM14A / SC TO-T / SC 14D9 / S-4 (as target) after the event
  bankrupt   = 8-K item 1.03 after the event
  deregistered = Form 15-12B/15-12G or 25-NSE without merger forms
Usage: python3 s6_missing_audit.py OUTDIR   (reads results.json, writes missing_audit.json)
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import sec_fetch as S

out = sys.argv[1]
d = json.load(open(os.path.join(out, "results.json")))
miss = [r for r in d["rows"] if r.get("status") == "missing" and r.get("grp") != "bio"]
res = []
for r in miss:
    try:
        _, rows = S.submissions(int(r["issuer_cik"]), all_pages=False)
    except Exception as e:
        res.append({"cik": r["issuer_cik"], "ticker": r["ticker"], "cls": "err"}); continue
    after = [x for x in rows if x["filingDate"] >= r["event_date"]]
    forms = {x["form"] for x in after}
    items = ",".join(x.get("items", "") for x in after if x["form"] == "8-K")
    if forms & {"DEFM14A", "PREM14A", "SC TO-T", "SC 14D9", "DEFM14C", "SC 13E3"}:
        cls = "acquired"
    elif "1.03" in items:
        cls = "bankrupt"
    elif forms & {"15-12B", "15-12G", "25-NSE", "15-15D", "25"}:
        cls = "deregistered_other"
    else:
        cls = "still_filing(ticker/class issue)"
    last = max((x["filingDate"] for x in after), default="")
    res.append({"cik": r["issuer_cik"], "ticker": r["ticker"], "event_date": r["event_date"], "cls": cls,
                "last_filing": last, "grp": r.get("grp")})
json.dump(res, open(os.path.join(out, "missing_audit.json"), "w"), indent=1)
from collections import Counter
print(len(res), Counter(x["cls"] for x in res))
