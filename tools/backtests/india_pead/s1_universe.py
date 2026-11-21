#!/usr/bin/env python3
"""Step 1: seeded random sample of NSE main-board equities (EQ/BE series) from the CURRENT
NSE equity list (EQUITY_L.csv -> survivorship: delisted firms are absent; see report §5).
Usage: python3 s1_universe.py OUTDIR   (expects OUTDIR/EQUITY_L.csv, downloaded from
https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv). Writes OUTDIR/sample.txt
(ALL eligible symbols, shuffled with seed 20261121; later steps walk it in order)."""
import csv, datetime as dt, os, random, sys
S = sys.argv[1]
rows = list(csv.reader(open(os.path.join(S, "EQUITY_L.csv"), encoding="utf-8", errors="replace")))
hdr = [h.strip() for h in rows[0]]
syms = []
for r in rows[1:]:
    d = dict(zip(hdr, [x.strip() for x in r]))
    if d.get("SERIES") not in ("EQ", "BE"): continue
    try: lst = dt.datetime.strptime(d["DATE OF LISTING"], "%d-%b-%Y").date()
    except Exception: continue
    if lst > dt.date(2023, 6, 30): continue          # need >= ~2 years of results before 2025
    syms.append(d["SYMBOL"])
syms.sort()
random.Random(20261121).shuffle(syms)
open(os.path.join(S, "sample.txt"), "w").write("\n".join(syms) + "\n")
print(len(syms), "eligible symbols; first 5:", syms[:5])
