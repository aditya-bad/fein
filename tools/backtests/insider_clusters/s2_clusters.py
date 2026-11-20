#!/usr/bin/env python3
"""Step 2: turn purchase rows into cluster events (no look-ahead).

Rule tested (see strategy record):
  - Form 4 / 4-A, TRANS_CODE 'P' (open-market or private purchase), acquired.
  - NOT flagged 10b5-1 (checkbox AFF10B5ONE, from 2023-04, or any footnote mentioning 10b5-1).
  - Reporting owner is a Director or Officer (pure 10%-owners / 'Other' excluded).
  - Common stock only (preferred, notes, warrants, units, depositary excluded); price >= $1.
  - Cluster: >= 2 DISTINCT insiders whose purchases have trade dates within 30 days of each
    other. The event is dated on the FILING date on which the 2nd insider's purchase became
    public (so the signal is knowable). Entry happens the next trading day.
  - One event per issuer per 365 days (avoids overlapping 12-month windows within a firm).
  - Signal dates 2021-01-01 .. 2024-12-31.
Usage: python3 s2_clusters.py OUTDIR      (reads OUTDIR/purchases.tsv, writes OUTDIR/events_raw.tsv)
"""
import csv, os, re, sys
from collections import defaultdict
from datetime import date, timedelta

BAD_SEC = re.compile(r"prefer|warrant|unit|note|debenture|depositary|right|option|bond|ADS\b", re.I)


def main(out):
    rows = list(csv.DictReader(open(os.path.join(out, "purchases.tsv")), delimiter="\t"))
    keep = []
    drop = defaultdict(int)
    for r in rows:
        if r["plan_flag"] == "1" or r["plan_footnote"] == "1": drop["10b5-1"] += 1; continue
        rel = r["relationship"]
        if "Director" not in rel and "Officer" not in rel: drop["not_dir_officer"] += 1; continue
        if BAD_SEC.search(r["security"]): drop["not_common"] += 1; continue
        if float(r["price"]) < 1 or float(r["shares"]) <= 0: drop["price<1_or_0sh"] += 1; continue
        t = r["ticker"]
        if t in ("NONE", "NA", "NULL") or not re.fullmatch(r"[A-Z]{1,5}([.-][A-Z])?", t or ""): drop["bad_ticker"] += 1; continue
        if not r["trans_date"] or not r["filing_date"]: drop["no_date"] += 1; continue
        keep.append(r)
    print(f"purchase rows {len(rows)} -> kept {len(keep)}; dropped {dict(drop)}", file=sys.stderr)
    by = defaultdict(list)
    for r in keep:
        by[r["issuer_cik"]].append(r)
    events = []
    for cik, lst in by.items():
        lst.sort(key=lambda r: (r["filing_date"], r["trans_date"]))
        fdates = sorted({r["filing_date"] for r in lst})
        last_ev = None
        for d in fdates:
            if not ("2021-01-01" <= d <= "2024-12-31"):
                continue
            if last_ev and date.fromisoformat(d) < last_ev + timedelta(days=365):
                continue
            dd = date.fromisoformat(d)
            known = [r for r in lst if r["filing_date"] <= d and
                     date.fromisoformat(r["trans_date"]) >= dd - timedelta(days=45)]
            # need two distinct owners with trade dates within 30 days, one of them filed today
            today = [r for r in known if r["filing_date"] == d]
            hit = None
            for t in today:
                td = date.fromisoformat(t["trans_date"])
                grp = [r for r in known if abs((date.fromisoformat(r["trans_date"]) - td).days) <= 30]
                owners = {r["owner_cik"] for r in grp}
                if len(owners) >= 2:
                    hit = grp; break
            if hit:
                last_ev = dd
                owners = {r["owner_cik"] for r in hit}
                val = sum(float(r["value"]) for r in hit)
                sh = sum(float(r["shares"]) for r in hit)
                roles = ";".join(sorted({("CEO" if re.search(r"\bCEO\b|Chief Executive", r["title"], re.I) else
                                         "CFO" if re.search(r"\bCFO\b|Chief Financial", r["title"], re.I) else
                                         "Off" if "Officer" in r["relationship"] else "Dir") for r in hit}))
                events.append({"issuer_cik": cik, "ticker": hit[-1]["ticker"], "issuer_name": hit[-1]["issuer_name"],
                               "event_date": d, "first_trade": min(r["trans_date"] for r in hit),
                               "n_insiders": len(owners), "n_tx": len(hit), "buy_value": round(val),
                               "vwap": round(val / sh, 4), "roles": roles})
    events.sort(key=lambda e: e["event_date"])
    with open(os.path.join(out, "events_raw.tsv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(events[0]), delimiter="\t"); w.writeheader(); w.writerows(events)
    print(f"{len(events)} cluster events, {len({e['issuer_cik'] for e in events})} issuers", file=sys.stderr)
    from collections import Counter
    print(Counter(e["event_date"][:4] for e in events), Counter(min(e["n_insiders"], 5) for e in events), file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
