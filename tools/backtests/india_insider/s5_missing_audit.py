#!/usr/bin/env python3
"""Step 5: survivorship audit. For events (and the control universe) with no Yahoo history, pull NSE announcements
and classify by keywords (merger/amalgamation/scheme, delisting, insolvency/IBC, symbol change).
Usage: python3 s5_missing_audit.py OUTDIR"""
import csv, json, os, re, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from tools.nse_fetch import api
S = sys.argv[1]; P = os.path.join(S, "prices")
def missing(sym):
    fn = os.path.join(P, sym.replace("/", "_") + ".json")
    if not os.path.exists(fn): return None
    j = json.load(open(fn))
    try: return not j["chart"]["result"][0]["timestamp"]
    except Exception: return True
ev = list(csv.DictReader(open(os.path.join(S, "events.tsv")), delimiter="\t"))
uni = open(os.path.join(S, "universe.txt")).read().split()
miss_ev = sorted({e["sym"] for e in ev if missing(e["sym"])})
miss_uni = [s for s in uni if missing(s)]
print("event symbols missing on Yahoo:", len(miss_ev), "| universe missing:", len(miss_uni), "of", len(uni))
PAT = [("merged", r"amalgamat|merger|scheme of arrangement|demerg"), ("delisted", r"delist"),
       ("insolvency", r"insolvency|\bIBC\b|CIRP|liquidat|resolution professional"),
       ("renamed", r"change (in|of) (the )?name|symbol change|change in symbol")]
out = {}
for s in miss_ev:
    try: a = api("corporate-announcements", index="equities", symbol=s)
    except Exception as ex: out[s] = {"error": str(ex)}; continue
    subj = [(x.get("an_dt", ""), (x.get("desc") or "") + " " + (x.get("attchmntText") or "")) for x in (a if isinstance(a, list) else [])]
    tags = sorted({k for k, p in PAT for _, t in subj if re.search(p, t, re.I)})
    out[s] = {"n_ann": len(subj), "last": subj[0][0] if subj else None, "tags": tags}
    print(s, out[s], flush=True)
json.dump({"events_missing": out, "universe_missing": miss_uni}, open(os.path.join(S, "missing_audit.json"), "w"), indent=1)
