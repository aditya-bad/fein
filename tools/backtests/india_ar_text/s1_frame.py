#!/usr/bin/env python3
"""Step 1: company frame = every NSE symbol with >= 1 corporate announcement 2023-06-01..2023-09-30 (all-company
daily feed), shuffled with seed 2026112203 -> OUT/frame.txt. Survivorship-free for firms listed in mid-2023.
~122 requests at >= 1.5 s. Resumable (OUT/anndays/<date>.json holds the symbol list per day)."""
import datetime as dt, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K  # noqa: E402
A = os.path.join(K.OUT, "anndays"); os.makedirs(A, exist_ok=True)
d, end = dt.date(2023, 6, 1), dt.date(2023, 9, 30)
while d <= end:
    fn = os.path.join(A, d.isoformat() + ".json")
    if not os.path.exists(fn):
        s = d.strftime("%d-%m-%Y")
        try:
            rows = K.N.announcements(None, s, s)
        except Exception as e:
            print("fail", d, e, flush=True); rows = None
        if rows is not None:
            K.jdump({"n": len(rows), "syms": sorted({r.get("symbol") for r in rows if r.get("symbol")})}, fn)
    d += dt.timedelta(days=1)
syms, days = set(), 0
for f in sorted(os.listdir(A)):
    j = K.jload(os.path.join(A, f), {})
    syms |= set(j.get("syms", [])); days += 1
fr = sorted(syms)
random.Random(2026112203).shuffle(fr)
open(os.path.join(K.OUT, "frame.txt"), "w").write("\n".join(fr) + "\n")
print(days, "days,", len(fr), "symbols; first 5:", fr[:5])
