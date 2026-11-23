#!/usr/bin/env python3
"""Step 2b (BSE stream): SHP list + one June-quarter SHP XBRL per calendar year 2017-2025 for every event firm with a
BSE code (pre-registered budget rule). One stream, >= 1.6 s (bse_fetch limiter). Reuses the bt_hf2 cache (same layout:
<cache>/shp/<bse>/list.json, <file>.xml); new files go to $BT_COMB/shp/<bse>/. XML parsed with regex only (untrusted)."""
import datetime as dt, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common3 as C
import bse_fetch as b
import common2 as C2   # hard_filters_v2: qtr_end
b.MIN_GAP = 1.6


def june_shps(lst):
    """{year: entry} = latest-filed SHP (original or revision filed first? -> earliest filing) for quarter ending June."""
    out = {}
    for x in lst or []:
        qe = C2.qtr_end(x.get("qtr")); fd = (x.get("filing_date_time") or "")[:10]
        if not qe or not fd or qe.month != 6 or not 2017 <= qe.year <= 2025: continue
        cur = out.get(qe.year)
        if cur is None or fd < (cur.get("filing_date_time") or "")[:10]: out[qe.year] = x   # first filing = what was public
    return out


def find(code, name):
    for root in (C.HF2, C.OUT):
        p = os.path.join(root, "shp", code, name)
        if os.path.exists(p) or os.path.exists(p + ".fail"): return p
    return None


def needed_years():
    """June-quarter years an event could use: Jan-Jun -> y-1; Jul-Sep -> y-1 and y; Oct-Dec -> y (saves requests)."""
    import csv, collections
    need = collections.defaultdict(set)
    for r in csv.DictReader(open(os.path.join(C.SURV, "events_w.tsv")), delimiter="\t"):
        y, m = int(r["event"][:4]), int(r["event"][5:7])
        need[r["sym"]].update({y - 1} if m <= 6 else ({y - 1, y} if m <= 9 else {y}))
    return need


def main():
    ids = C.id_maps()
    need = needed_years()
    n = 0
    for i, (sym, r) in enumerate(ids.items()):
        code = r.get("bse_code")
        if not code: continue
        lp = find(code, "list.json")
        if not lp:
            lp = os.path.join(C.OUT, "shp", code, "list.json")
            try:
                lst = b.api("SHPQNewFormat/w", scripcode=code, qtrid="", Type="EQ").get("Table", []) or []
            except Exception as e:
                print("ERR list", sym, code, e, flush=True); continue
            C.js(lp, lst); n += 1
        lst = C.jl(lp, [])
        for y, x in sorted(june_shps(lst).items()):
            if y not in need[sym]: continue
            u = x.get("xbrlurl") or ""
            if not u.endswith(".xml"): continue
            nm = os.path.basename(u)
            if find(code, nm): continue
            fp = os.path.join(C.OUT, "shp", code, nm); os.makedirs(os.path.dirname(fp), exist_ok=True)
            try:
                open(fp, "wb").write(b._curl("https://www.bseindia.com" + u))
            except Exception as e:
                open(fp + ".fail", "w").write(str(e)[:200])
            n += 1
        if i % 20 == 0: print(i, sym, "requests", n, flush=True)
    print("bse done, requests", n, flush=True)


if __name__ == "__main__":
    main()
