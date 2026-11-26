#!/usr/bin/env python3
"""Cohort-2 frame + seeded shuffle (prereg.md s1). Run from repo root:
   python3 -I "research_notes/Promise tracker pilot/forward_test_2026-11-c2/draw.py"
Writes selection_order.json next to this file. Research, not SEBI-registered advice."""
import csv, io, json, os, random, subprocess

ROOT = os.getcwd()
HERE = os.path.join(ROOT, "research_notes", "Promise tracker pilot", "forward_test_2026-11-c2")
PEAD = os.path.join(ROOT, "research_notes", "Backtests", "india_pead_live")
SECTORS = ["Information Technology", "Consumer Durables", "Automobile and Auto Components"]
EXCL = set("""SUNFLAG AUTOAXLES INDRAMEDCO UTKARSHBNK HARSHA SHK UTTAMSUGAR CUMMINSIND VMM FEDERALBNK FIVE VIYASH
JASH KIRLOSBROS RISHABH ANUP NEOGEN GALAXYSURF YASHO TATVA KRSNAA ORCHPHARMA SYNGENE SHILPAMED
KPIL SKIPPER KEC UNIPARTS SANSERA SONACOMS HAPPYFORGE ENDURANCE PERSISTENT COFORGE MPHASIS KPITTECH GULFPETRO REPRO""".split())

def bhav():
    for d in ("26112026", "25112026", "24112026"):
        url = f"https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{d}.csv"
        r = subprocess.run(["curl", "-s", "-f", "-A", "Mozilla/5.0", url], capture_output=True)
        if r.returncode == 0 and r.stdout.count(b"\n") > 500:
            rows = list(csv.DictReader(io.StringIO(r.stdout.decode())))
            rows = [{k.strip(): (v or "").strip() for k, v in x.items()} for x in rows]
            return d, rows
        print("bhavcopy", d, "->", r.returncode)
    raise SystemExit("no bhavcopy")

def main():
    d, rows = bhav()
    close = {x["SYMBOL"]: float(x["CLOSE_PRICE"]) for x in rows if x["SERIES"] in ("EQ", "BE", "BZ")}
    date1 = sorted({x["DATE1"] for x in rows})
    imap = {r["symbol"]: r for r in csv.DictReader(open(os.path.join(PEAD, "industry_map.csv")))}
    uni = list(csv.DictReader(open(os.path.join(PEAD, "universe.csv"))))
    unpriced = 0; inband = []; missing = 0
    for u in uni:
        s = u["sym"]
        if s not in close: unpriced += 1; continue
        mc = int(u["shares"]) * close[s] / 1e7
        if 1000 <= mc <= 20000:
            if s not in imap: missing += 1; continue
            inband.append((s, round(mc, 1)))
    rng = random.Random(20261211)
    order, excl_present = {}, {}
    for sec in SECTORS:
        el = sorted([(s, m) for s, m in inband if imap[s]["sector"] == sec])
        excl_present[sec] = [s for s, _ in el if s in EXCL]
        el = [(s, m) for s, m in el if s not in EXCL]
        rng.shuffle(el)
        order[sec] = [[s, m, imap[s]["industry"], imap[s]["basic_industry"]] for s, m in el]
    out = {"file": d, "frame_close": date1, "universe": len(uni), "unpriced": unpriced, "in_band": len(inband),
           "in_band_missing_map": missing, "excluded_present": excl_present, "order": order}
    json.dump(out, open(os.path.join(HERE, "selection_order.json"), "w"), indent=1)
    print(d, date1, "universe", len(uni), "unpriced", unpriced, "in band", len(inband), "missing", missing)
    for sec in SECTORS:
        print(sec, len(order[sec]), "excluded present:", excl_present[sec])
        for r in order[sec][:12]: print("   ", r)

if __name__ == "__main__":
    main()
