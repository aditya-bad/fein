#!/usr/bin/env python3
"""Step 4: EDGAR outcome events per (firm, snapshot) from the cached submissions (all pages).
O_bk = 8-K item 1.03; O_delist = 8-K 3.01 + Form 25/15 + no merger evidence; fate audit for missing prices."""
import json, sys
from datetime import date
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import p

MERGER_FORMS = {"DEFM14A", "DEFM14C", "PREM14A", "PREM14C", "SC 14D9", "SC TO-T", "SC 13E3", "425", "SC 14D9/A", "SC TO-T/A"}
DELIST_FORMS = {"25", "25-NSE", "15-12B", "15-12G", "15-15D", "15F-12B"}


def plus5(Ts):
    T = date.fromisoformat(Ts); return T, T.replace(year=T.year + 5)


def main():
    rows = [json.loads(l) for l in open(p("universe.jsonl"))]
    out = open(p("events.jsonl"), "w")
    cache = {}
    for r in rows:
        cik = r["cik"]
        if cik not in cache:
            cache[cik] = json.load(open(p("firms", f"{cik}.json")))["filings"]
        T, E = plus5(r["T"])
        fl = [x for x in cache[cik] if x[1] and T < date.fromisoformat(x[1]) <= E]
        items8k = [(x[1], x[3]) for x in fl if x[0] in ("8-K", "8-K/A")]
        has = lambda code: sorted(d for d, it in items8k if code in (it or "").split(","))
        bk = has("1.03"); i301 = has("3.01"); i501 = has("5.01")
        merger = sorted(x[1] for x in fl if x[0] in MERGER_FORMS) + i501
        dl = sorted(x[1] for x in fl if x[0] in DELIST_FORMS)
        periodic_after = sorted(x[1] for x in cache[cik] if x[0] in ("10-K", "10-Q", "10-KT") and x[1] and date.fromisoformat(x[1]) > T)
        last_periodic = periodic_after[-1] if periodic_after else None
        o_bk = int(bool(bk))
        o_del = int(bool(i301) and bool(dl) and not merger)
        # fate (for the missing-price audit)
        if o_bk: fate = "bankrupt"
        elif o_del: fate = "delisted-for-cause"
        elif merger and dl: fate = "acquired/merged"
        elif merger: fate = "merger-evidence-still-filing" if last_periodic and last_periodic > E.isoformat() else "acquired/merged"
        elif last_periodic is None or date.fromisoformat(last_periodic) < E.replace(year=E.year - 1):
            fate = "stopped-filing"
        else: fate = "alive"
        out.write(json.dumps({"cik": cik, "T": r["T"], "O_bk": o_bk, "bk_date": bk[0] if bk else None, "O_delist": o_del,
                              "delist_date": dl[0] if dl else None, "i301": i301[:1], "merger_date": merger[0] if merger else None,
                              "last_periodic": last_periodic, "fate": fate}) + "\n")
    out.close()


if __name__ == "__main__":
    main()
