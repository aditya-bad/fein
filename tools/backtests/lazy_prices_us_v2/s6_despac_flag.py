#!/usr/bin/env python3
"""Step 6 (v2: PRE-REGISTERED exclusion, unchanged method from v1): flag firm-years whose PRIOR 10-K was a blank-check (SPAC)
shell -> the "text change" is a business transformation (de-SPAC), not a subtle edit. Writes despac.tsv."""
import csv, gzip, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import p
PAT = re.compile(r"blank check company|special purpose acquisition", re.I)
out = open(p("despac.tsv"), "w"); out.write("acc\tdespac\n"); n = 0
for r in csv.DictReader(open(p("firmyears.tsv")), delimiter="\t"):
    with gzip.open(p("docs", r["prev_acc"] + ".txt.gz"), "rt", encoding="utf-8") as g:
        head = g.read(40000)
    f = int(bool(PAT.search(head))); n += f
    out.write(f"{r['acc']}\t{f}\n")
print("de-SPAC transitions flagged:", n, file=sys.stderr)
