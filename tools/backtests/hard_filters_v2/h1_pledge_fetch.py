#!/usr/bin/env python3
"""Step 1: promoter pledge at T from BSE shareholding-pattern XBRL (point-in-time), for every panel company.
One stream, >= 1.6 s between requests (bse_fetch rate limiter). Cache: $BT_HF2/shp/<bse>/list.json, <file>.xml.
For each (company, snapshot): latest SHP filed before T whose quarter ends within 12 months before T; plus the
one filed ~12 months earlier (for the exploratory B_rise). Output of this step: cache only; h2 parses it.
Downloaded XML is untrusted data: parsed with regex only."""
import datetime as dt, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common2 as C
import bse_fetch as b

b.MIN_GAP = 1.6


def pick(lst, T):
    ok = []
    for x in lst:
        fd = (x.get("filing_date_time") or "")[:10]
        qe = C.qtr_end(x.get("qtr"))
        if not fd or not qe:
            continue
        fd = dt.date.fromisoformat(fd)
        if fd < T and qe >= T - dt.timedelta(days=366):
            ok.append((fd, x))
    return max(ok, key=lambda z: z[0])[1] if ok else None


def targets(lst, T):
    out = {}
    x = pick(lst, T)
    if x:
        out["at_T"] = x
    y = pick(lst, T - dt.timedelta(days=365))
    if y and (not x or y["xbrlurl"] != x["xbrlurl"]):
        out["prior"] = y
    return out


def main():
    frame = {r["key"]: r for r in C.K.read_csv(os.path.join(C.K.CACHE, "frame.csv"))}
    panel = C.K.read_csv(C.PANEL)
    snaps = {}
    for r in panel:
        snaps.setdefault(r["key"], set()).add(r["snap"])
    n = 0
    for i, (k, ss) in enumerate(sorted(snaps.items()), 1):
        code = frame[k]["bse_code"]
        if not code:
            continue
        d = os.path.join(C.CACHE2, "shp", code)
        os.makedirs(d, exist_ok=True)
        lp = os.path.join(d, "list.json")
        if not os.path.exists(lp):
            try:
                lst = b.api("SHPQNewFormat/w", scripcode=code, qtrid="", Type="EQ").get("Table", []) or []
            except Exception as e:
                print("ERR list", code, e, flush=True)
                continue
            C.K.jsave(lp, lst)
            n += 1
        lst = C.K.jload(lp, [])
        for sn in sorted(ss):
            for role, x in targets(lst, C.K.SNAPS[sn]).items():
                u = x.get("xbrlurl") or ""
                if not u.endswith(".xml"):
                    continue
                fp = os.path.join(d, os.path.basename(u))
                if os.path.exists(fp) or os.path.exists(fp + ".fail"):
                    continue
                try:
                    body = b._curl("https://www.bseindia.com" + u)
                    open(fp, "wb").write(body)
                except Exception as e:
                    open(fp + ".fail", "w").write(str(e)[:200])
                n += 1
        if i % 25 == 0:
            print(f"{i}/{len(snaps)} companies, requests {n}", flush=True)
    print("done, requests", n, flush=True)


if __name__ == "__main__":
    main()
