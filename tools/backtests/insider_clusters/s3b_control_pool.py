#!/usr/bin/env python3
"""Step 3b: random control pool from the point-in-time universe.

Universe = issuers with any Form 4 filed 2021q1-2024q4 (ticker as last filed in that period)
that have a dei shares-outstanding frame and are not SPACs/funds by SIC. A seeded random sample
of N is drawn, nothing else (an earlier draft added event issuers;
removed because it tilts the control toward insider-buying firms). Ticker reuse is guarded downstream: a reused ticker's Yahoo series
starts after the old issuer left, so it fails the 'price on entry date' test.
Writes OUTDIR/control_pool.tsv (cik<TAB>ticker) and OUTDIR/ctl_tickers_to_fetch.txt.
Usage: python3 s3b_control_pool.py OUTDIR [N=1500]
"""
import csv, json, os, random, re, sys

out = sys.argv[1]; N = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
uni = json.load(open(os.path.join(out, "universe_tickers.json")))
sic = json.load(open(os.path.join(out, "sic.json")))
fr = set()
for fn in os.listdir(os.path.join(out, "frames")):
    for r in json.load(open(os.path.join(out, "frames", fn)))["data"]:
        fr.add(str(r["cik"]))
cand = []
for cik, qs in uni.items():
    qq = sorted(q for q in qs if "2021q1" <= q <= "2024q4")
    if not qq or cik not in fr: continue
    if sic.get(cik, {}).get("sic", "") in {"6770", "6722", "6726", "6799"}: continue
    t = qs[qq[-1]]
    if re.fullmatch(r"[A-Z]{1,5}([.-][A-Z])?", t): cand.append((cik, t))
rnd = random.Random(2026); rnd.shuffle(cand)
pool = cand[:N]
# NOTE: event issuers are NOT added (a pool tilted to firms that had insider clusters at other
# times would not be a random control); they appear only if drawn at random.
with open(os.path.join(out, "control_pool.tsv"), "w") as f:
    f.write("\n".join(f"{c}\t{t}" for c, t in pool))
with open(os.path.join(out, "ctl_tickers_to_fetch.txt"), "w") as f:
    f.write("\n".join(t for _, t in cand[:N]))
print(f"universe candidates {len(cand)}; pool {len(pool)} (random draw)", file=sys.stderr)
