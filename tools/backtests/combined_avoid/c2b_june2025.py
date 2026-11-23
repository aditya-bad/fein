#!/usr/bin/env python3
"""Step 2c (BSE stream, after c2 finished; logged deviation D1): June-2025 SHPs are listed with an HTML link but
still name their XBRL file (XbrlFile). Probe /XBRL1/<XbrlFile> once; if BSE serves XBRL there, fetch it for every firm
whose events need the June-2025 SHP. One stream, >= 1.6 s. Saves to $BT_COMB/shp/<bse>/<XbrlFile>."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common3 as C
import bse_fetch as b
from c2_fetch_bse import june_shps, find, needed_years
b.MIN_GAP = 1.6


def main():
    ids, need = C.id_maps(), needed_years()
    todo = []
    for sym, r in ids.items():
        code = r.get("bse_code")
        if not code or 2025 not in need[sym]: continue
        lp = find(code, "list.json")
        x = june_shps(C.jl(lp, []) if lp else []).get(2025)
        if not x or (x.get("xbrlurl") or "").endswith(".xml") or not (x.get("XbrlFile") or "").endswith(".xml"): continue
        if not find(code, x["XbrlFile"]): todo.append((code, x["XbrlFile"]))
    print("to fetch", len(todo), flush=True)
    for i, (code, nm) in enumerate(todo):
        fp = os.path.join(C.OUT, "shp", code, nm); os.makedirs(os.path.dirname(fp), exist_ok=True)
        try:
            body = b._curl("https://www.bseindia.com/XBRL1/" + nm)
            open(fp, "wb").write(body)
            ok = b"in-bse-shp" in body[:5000] or b"<in-bse-shp:" in body
        except Exception as e:
            open(fp + ".fail", "w").write(str(e)[:200]); ok = False
        if i == 0:
            print("probe", nm, "xbrl" if ok else "NOT xbrl", flush=True)
            if not ok: print("stop: June-2025 XBRL not served at /XBRL1/"); return
        if i % 25 == 0: print(i, flush=True)
    print("june2025 done", flush=True)


if __name__ == "__main__":
    main()
