#!/usr/bin/env python3
"""Step 2: the MISSING universe (pre-registered): NSE quarterly filers 2018-01..2025-03 (s1) not in v1's frame.
  dead   = symbol AND ISIN absent from today's EQUITY_L.csv and today's NSE SME list
  offser = in EQUITY_L but not EQ/BE series (v1 excluded these too)
Shuffle (seed 20261122) and take the first round(f*N), f = 700/1791 (v1's sampling fraction).
Distress tag from research_notes/Universe/india_dead_companies_2026-11-22.csv (IBBI / NSE forced or liquidation
delisting / NSE or BSE suspension), matched by NSE symbol or ISIN. No prices or returns are touched.
Usage: python3 s2_missing.py  -> $OUT/missing.csv, $OUT/missing_meta.json"""
import collections, csv, datetime as dt, glob, json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K

eq = list(csv.DictReader(open(os.path.join(K.V1, "EQUITY_L.csv"), encoding="utf-8", errors="replace")))
eq = [{k.strip(): (v or "").strip() for k, v in r.items()} for r in eq]
eq_sym = {r["SYMBOL"]: r for r in eq}
eq_isin = {r.get("ISIN NUMBER"): r for r in eq if r.get("ISIN NUMBER")}
sme_sym, sme_isin = set(), set()
smef = os.path.join(K.OUT, "SME_EQUITY_L.csv")
if os.path.exists(smef):
    for r in csv.DictReader(open(smef, encoding="utf-8", errors="replace")):
        r = {k.strip(): (v or "").strip() for k, v in r.items()}
        sme_sym.add(r.get("SYMBOL")); sme_isin.add(r.get("ISIN_NUMBER") or r.get("ISIN NUMBER"))
frame = set(open(os.path.join(K.V1, "sample.txt")).read().split())      # all 1,791 v1-frame symbols

fil = collections.defaultdict(lambda: {"isin": set(), "name": "", "n": 0, "first": None, "last": None})
nwin, nfail = 0, 0
for fn in sorted(glob.glob(os.path.join(K.OUT, "filers", "*.json"))):
    j = json.load(open(fn)); nwin += 1
    if j["rows"] is None: nfail += 1; continue
    for x in j["rows"]:
        if x.get("period") != "Quarterly" or not x.get("symbol"): continue
        f = fil[x["symbol"]]; f["n"] += 1; f["name"] = x.get("companyName") or f["name"]
        if x.get("isin"): f["isin"].add(x["isin"])
        try: qe = dt.datetime.strptime(x["toDate"], "%d-%b-%Y").date()
        except Exception: continue
        f["first"] = min(f["first"] or qe, qe); f["last"] = max(f["last"] or qe, qe)

dist = collections.defaultdict(set)
for r in csv.DictReader(open(os.path.join(K.ROOT, "research_notes", "Universe", "india_dead_companies_2026-11-22.csv"))):
    tag = r["source"] if r["source"] != "nse_delisted" else "nse_delisted:" + (r["event"] or "")
    for k in (r.get("nse_symbol"), r.get("isin")):
        if k: dist[k].add(tag)
bse_of = {}
for r in csv.DictReader(open(os.path.join(K.ROOT, "research_notes", "Universe", "india_dead_companies_2026-11-22.csv"))):
    for k in (r.get("nse_symbol"), r.get("isin")):
        if k and r.get("bse_code"): bse_of.setdefault(k, r["bse_code"])
for r in csv.DictReader(open(os.path.join(K.SOLV, "frame.csv"))):
    for k in (r.get("nse_symbol"), r.get("isin")):
        if k and r.get("bse_code"): bse_of.setdefault(k, r["bse_code"])

DISTRESS = ("ibbi", "nse_delisted:delisted_compulsory", "nse_delisted:delisted_delisting_liquidation", "nse_suspended", "bse_suspended")
rows, cnt = [], collections.Counter()
for s, f in sorted(fil.items()):
    if s in frame: cnt["in_v1_frame"] += 1; continue
    live = eq_sym.get(s) or next((eq_isin[i] for i in f["isin"] if i in eq_isin), None)
    if s in sme_sym or f["isin"] & sme_isin: cnt["sme_listed_now"] += 1; continue
    if live:
        if live.get("SERIES") in ("EQ", "BE"):
            cnt["eq_listed_after_2023-06_or_renamed"] += 1; continue   # in EQUITY_L EQ/BE but not in v1 frame
        cls = "offser"
    else:
        cls = "dead"
    tags = set().union(*(dist.get(k, set()) for k in [s] + sorted(f["isin"])))
    tags = {t.lower() for t in tags}
    distress = any(t.startswith(d) for t in tags for d in DISTRESS)
    isin = sorted(f["isin"])[0] if f["isin"] else ""
    rows.append({"symbol": s, "isin": isin, "name": f["name"], "cls": cls, "n_filings": f["n"],
                 "first_qe": f["first"], "last_qe": f["last"], "distress": int(distress), "tags": "|".join(sorted(tags)),
                 "bse_code": bse_of.get(s) or bse_of.get(isin, "")})
    cnt[cls] += 1
rows.sort(key=lambda r: r["symbol"]); random.Random(20261122).shuffle(rows)
f_rate = 700 / 1791
n_take = round(f_rate * len(rows))
for i, r in enumerate(rows): r["order"] = i; r["sampled"] = int(i < n_take)
with open(os.path.join(K.OUT, "missing.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
meta = {"windows": nwin, "windows_failed": nfail, "filer_symbols": len(fil), "counts": cnt, "missing": len(rows),
        "f": f_rate, "sampled": n_take,
        "sampled_by_cls": collections.Counter(r["cls"] for r in rows[:n_take]),
        "sampled_distress": sum(r["distress"] for r in rows[:n_take])}
json.dump(meta, open(os.path.join(K.OUT, "missing_meta.json"), "w"), indent=1, default=str)
print(json.dumps(meta, indent=1, default=str))
