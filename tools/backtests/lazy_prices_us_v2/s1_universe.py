#!/usr/bin/env python3
"""Step 1 (v2): universe + seeded sample (pre-registered, research_notes/Backtests/lazy_prices_us_v2.md s0).

1. dei EntityPublicFloat frames CY2022Q4I..CY2025Q1I -> candidate CIKs with any float in $300M-$10B.
2. dei EntityCommonStockSharesOutstanding frames CY2023Q4I..CY2025Q3I (cover-page shares, for market cap).
3. Shuffle candidate CIKs (seed 2026112202); fetch EDGAR submissions for each in that order (cached),
   keep a compact record (SIC, tickers, 10-K list with primary documents, survivorship events).
4. Firm-year eligible if: 10-K (not /A) filed 2024-01-01..2025-06-30, prior 10-K filed 270-460 days earlier,
   float (end date 120-400 days before filing) in $300M-$10B, SIC not 6000-6799 / 4900-4999.
   Stop once total eligible firm-years >= TARGET (2000).
Outputs: firms.jsonl (compact submissions), firmyears.tsv, s1_log.json
"""
import datetime as dt, json, os, random, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import p, sec_json, excluded_sic

TARGET = int(os.environ.get("TARGET", "2000"))
FLOAT_FRAMES = [f"CY{y}Q{q}I" for y in range(2022, 2026) for q in range(1, 5)][3:-3]   # 2022Q4..2025Q1
SHARE_FRAMES = [f"CY{y}Q{q}I" for y in range(2023, 2026) for q in range(1, 5)][3:-1]   # 2023Q4..2025Q3
SURV_FORMS = {"25-NSE", "25", "15-12B", "15-12G", "15-15D", "DEFM14A", "PREM14A", "SC TO-T", "SC 14D9", "S-4", "DEFM14C"}


def D(s):
    return dt.date.fromisoformat(s[:10])


def compact(sub):
    out = {"cik": sub["cik"], "name": sub.get("name"), "sic": sub.get("sic"), "tickers": sub.get("tickers"),
           "exchanges": sub.get("exchanges"), "tenk": [], "surv": []}
    blocks = [sub["filings"]["recent"]] + sub.get("_extra", [])
    for b in blocks:
        for i, form in enumerate(b["form"]):
            fd = b["filingDate"][i]
            if form == "10-K":
                out["tenk"].append({"acc": b["accessionNumber"][i], "fd": fd, "acc_dt": b["acceptanceDateTime"][i],
                                    "doc": b["primaryDocument"][i], "rd": b["reportDate"][i]})
            elif fd >= "2021-01-01" and (form in SURV_FORMS or (form == "8-K" and "1.03" in (b.get("items", [""] * 99999)[i] or ""))):
                out["surv"].append({"form": form, "fd": fd, "items": b.get("items", [""] * 99999)[i]})
    out["tenk"].sort(key=lambda r: r["fd"])
    return out


def main():
    floats = {}  # cik -> list of (end, val)
    for fr in FLOAT_FRAMES:
        d = sec_json(f"https://data.sec.gov/api/xbrl/frames/dei/EntityPublicFloat/USD/{fr}.json", p("frames", f"float_{fr}.json"))
        for r in (d or {}).get("data", []):
            floats.setdefault(r["cik"], []).append((r["end"], r["val"]))
    shares = {}
    for fr in SHARE_FRAMES:
        d = sec_json(f"https://data.sec.gov/api/xbrl/frames/dei/EntityCommonStockSharesOutstanding/shares/{fr}.json",
                     p("frames", f"shares_{fr}.json"))
        for r in (d or {}).get("data", []):
            shares.setdefault(r["cik"], []).append((r["end"], r["val"], r["accn"]))
    json.dump({str(k): v for k, v in shares.items()}, open(p("shares.json"), "w"))
    json.dump({str(k): v for k, v in floats.items()}, open(p("floats.json"), "w"))
    cands = sorted(c for c, v in floats.items() if any(3e8 <= x <= 1e10 for _, x in v))
    random.Random(2026112202).shuffle(cands)
    print(f"candidate CIKs with any float in range: {len(cands)}", file=sys.stderr)
    counts = {2024: 0, 2025: 0}
    log = {"candidates": len(cands), "processed": 0, "excl_sic": 0, "no_sub": 0, "order": []}
    fy_rows = []
    fo = open(p("firms.jsonl"), "w")
    for k, cik in enumerate(cands):
        if sum(counts.values()) >= TARGET:
            break
        log["processed"] += 1; log["order"].append(cik)
        sub = sec_json(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", p("subs", f"{cik}.json"))
        if not sub:
            log["no_sub"] += 1; continue
        if sub["filings"]["recent"]["filingDate"] and min(sub["filings"]["recent"]["filingDate"]) > "2022-06-01" and "_extra" not in sub:
            ex = []
            for f in sub["filings"].get("files", []):
                if f.get("filingTo", "") >= "2022-06-01":
                    e = sec_json(f"https://data.sec.gov/submissions/{f['name']}")
                    if e: ex.append(e)
            sub["_extra"] = ex
            json.dump(sub, open(p("subs", f"{cik}.json"), "w"))
        c = compact(sub)
        fo.write(json.dumps(c) + "\n")
        if excluded_sic(c["sic"]):
            log["excl_sic"] += 1; continue
        tk = c["tenk"]
        for i in range(1, len(tk)):
            cur, pr = tk[i], tk[i - 1]
            y = int(cur["fd"][:4])
            if y not in counts or cur["fd"] > "2025-06-30":
                continue
            gap = (D(cur["fd"]) - D(pr["fd"])).days
            if not 270 <= gap <= 460:
                continue
            fl = [(e, v) for e, v in floats.get(cik, []) if 120 <= (D(cur["fd"]) - D(e)).days <= 400]
            if not fl:
                continue
            e, v = max(fl)
            if not 3e8 <= v <= 1e10:
                continue
            sh = [(se, sv) for se, sv, sa in shares.get(cik, []) if sa == cur["acc"]] or \
                 [(se, sv) for se, sv, sa in shares.get(cik, []) if -30 <= (D(cur["fd"]) - D(se)).days <= 120]
            shv = max(sh)[1] if sh else ""
            counts[y] += 1
            fy_rows.append([cik, y, cur["fd"], cur["acc_dt"], cur["acc"], cur["doc"], pr["fd"], pr["acc"], pr["doc"],
                            e, v, shv, c["sic"], (c["tickers"] or [""])[0]])
        if k % 200 == 0:
            print(k, counts, file=sys.stderr, flush=True)
    fo.close()
    with open(p("firmyears.tsv"), "w") as f:
        f.write("cik\tyear\tfd\tacc_dt\tacc\tdoc\tprev_fd\tprev_acc\tprev_doc\tfloat_end\tfloat\tshares\tsic\tticker\n")
        for r in fy_rows:
            f.write("\t".join(map(str, r)) + "\n")
    log["counts"] = counts
    json.dump(log, open(p("s1_log.json"), "w"))
    print("done", counts, log["processed"], file=sys.stderr)


if __name__ == "__main__":
    main()
