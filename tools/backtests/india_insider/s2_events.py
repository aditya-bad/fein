#!/usr/bin/env python3
"""Step 2: parse PIT rows -> qualifying open-market buys -> events (pre-registered rule) + share estimates.
Usage: python3 s2_events.py OUTDIR
Writes: buys.tsv, events.tsv, shares.tsv (implied total shares per symbol per PIT row),
        tradepx.tsv (unadjusted single-day trade prices), universe.txt"""
import collections, datetime as dt, glob, json, os, sys

S = sys.argv[1]
def pdate(s):
    for f in ("%d-%b-%Y %H:%M", "%d-%b-%Y"):
        try: return dt.datetime.strptime(s.strip(), f).date()
        except Exception: pass
    return None
def num(x):
    try: return float(str(x).replace(",", ""))
    except Exception: return None

PROM = {"Promoters", "Promoter Group"}
KMP = {"Director", "Key Managerial Personnel"}
rows, seen = [], set()
for f in sorted(glob.glob(os.path.join(S, "pit", "*.json"))):
    for r in json.load(open(f)):
        k = (r.get("symbol"), r.get("acqName"), r.get("acqfromDt"), r.get("acqtoDt"),
             r.get("secAcq"), r.get("acqMode"), r.get("tdpTransactionType"))
        if k in seen: continue
        seen.add(k); rows.append(r)
print("unique rows", len(rows))

# implied total shares from any equity row with after-holding >= 1%
sh = open(os.path.join(S, "shares.tsv"), "w")
universe = set()
for r in rows:
    if r.get("secType") != "Equity Shares" or not r.get("symbol"): continue
    universe.add(r["symbol"])
    n, p, d = num(r.get("afterAcqSharesNo")), num(r.get("afterAcqSharesPer")), pdate(r.get("date") or "")
    if n and p and p >= 1.0 and d:
        sh.write(f"{r['symbol']}\t{d}\t{n / p * 100:.0f}\n")
sh.close()
# unadjusted trade prices (single-day market trades) -> used to map share counts onto Yahoo's adjusted basis
tp = open(os.path.join(S, "tradepx.tsv"), "w")
for r in rows:
    if r.get("acqMode") not in ("Market Sale", "Market Purchase") or r.get("secType") != "Equity Shares": continue
    if r.get("acqfromDt") != r.get("acqtoDt"): continue
    q, v, d = num(r.get("secAcq")), num(r.get("secVal")), pdate(r.get("acqtoDt") or "")
    if q and v and q >= 10 and v > 0 and d:
        tp.write(f"{r['symbol']}\t{d}\t{v / q:.4f}\n")
tp.close()
open(os.path.join(S, "universe.txt"), "w").write("\n".join(sorted(universe)))

buys, drop = [], collections.Counter()
for r in rows:
    if r.get("acqMode") != "Market Purchase": drop["mode:" + str(r.get("acqMode"))] += 1; continue
    if r.get("tdpTransactionType") != "Buy": drop["type"] += 1; continue
    if r.get("secType") != "Equity Shares": drop["sec"] += 1; continue
    cat = r.get("personCategory")
    if cat in PROM: cls = "promoter"
    elif cat in KMP: cls = "kmp"
    else: drop["cat:" + str(cat)] += 1; continue
    q, v, d = num(r.get("secAcq")), num(r.get("secVal")), pdate(r.get("date") or "")
    if not q or not v or q <= 0 or v <= 0 or not d: drop["zero"] += 1; continue
    nb, pb = num(r.get("afterAcqSharesNo")), num(r.get("afterAcqSharesPer"))
    tot = nb / pb * 100 if nb and pb and pb >= 1.0 else None
    buys.append(dict(sym=r["symbol"], d=d, cls=cls, q=q, v=v, px=v / q, tot=tot,
                     name=r.get("acqName"), tdate=pdate(r.get("acqtoDt") or "")))
print("drops", drop.most_common(12)); print("qualifying buys", len(buys))

with open(os.path.join(S, "buys.tsv"), "w") as f:
    f.write("sym\tbroadcast\ttrade_to\tcls\tqty\tvalue\tpx\tname\n")
    for b in sorted(buys, key=lambda b: (b["sym"], b["d"])):
        f.write(f"{b['sym']}\t{b['d']}\t{b['tdate']}\t{b['cls']}\t{b['q']:.0f}\t{b['v']:.0f}\t{b['px']:.2f}\t{b['name']}\n")

# events: rolling 30-day window from each start buy; fire when >= Rs 1 cr or >= 0.25% of equity
by = collections.defaultdict(list)
for b in buys: by[b["sym"]].append(b)
events = []
for sym, bl in by.items():
    bl.sort(key=lambda b: b["d"]); last = None
    for i, b0 in enumerate(bl):
        if last and (b0["d"] - last).days < 365: continue
        v = q = 0; cls = set(); tot = None; names = set()
        for b in bl[i:]:
            if (b["d"] - b0["d"]).days > 30: break
            v += b["v"]; q += b["q"]; cls.add(b["cls"]); names.add(b["name"]); tot = b["tot"] or tot
            pct = q / tot * 100 if tot else None
            if v >= 1e7 or (pct is not None and pct >= 0.25):
                if dt.date(2021, 1, 1) <= b["d"] <= dt.date(2024, 12, 31):
                    if last and (b["d"] - last).days < 365: break
                    events.append(dict(sym=sym, d=b["d"], start=b0["d"], v=v, q=q, pct=pct,
                                       cls="mixed" if len(cls) > 1 else cls.pop(), n=len(names),
                                       px=v / q, tot=tot))
                    last = b["d"]
                break
print("events", len(events))
with open(os.path.join(S, "events.tsv"), "w") as f:
    f.write("sym\tevent_date\tstart\tvalue_cr\tqty\tpct_equity\tcls\tn_buyers\tvwap\timplied_shares\n")
    for e in sorted(events, key=lambda e: e["d"]):
        f.write(f"{e['sym']}\t{e['d']}\t{e['start']}\t{e['v']/1e7:.3f}\t{e['q']:.0f}\t"
                f"{'' if e['pct'] is None else round(e['pct'],3)}\t{e['cls']}\t{e['n']}\t{e['px']:.2f}\t{e['tot'] or ''}\n")
