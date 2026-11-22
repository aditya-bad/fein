#!/usr/bin/env python3
"""Step 2: per candidate CIK, fetch SEC submissions (all pages) and companyfacts; keep only needed tags.
Raw companyfacts is not cached (3-10 MB each); the reduced file keeps every fact version with accn/filed/form.
Usage: s2_fetch.py [--workers 3]"""
import json, os, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, __file__.rsplit("/", 1)[0])
import common
from common import sec_get, p

TAGS = {
 "us-gaap": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest",
  "OperatingIncomeLoss", "IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
  "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
  "IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic", "InterestExpense", "InterestExpenseDebt",
  "InterestAndDebtExpense", "InterestPaidNet", "InterestPaid", "DebtCurrent", "LongTermDebtCurrent",
  "LongTermDebtAndCapitalLeaseObligationsCurrent", "ShortTermBorrowings", "CommercialPaper", "LinesOfCreditCurrent",
  "ShortTermBankLoansAndNotesPayable", "LongTermDebtNoncurrent", "LongTermDebtAndCapitalLeaseObligations", "LongTermDebt",
  "CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", "Cash",
  "NetCashProvidedByUsedInOperatingActivities", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
  "PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets", "PaymentsOfDividends",
  "PaymentsOfDividendsCommonStock", "PaymentsForRepurchaseOfCommonStock", "PaymentsForRepurchaseOfEquity",
  "TreasuryStockValue", "Assets", "Liabilities", "Revenues", "SalesRevenueNet",
  "RevenueFromContractWithCustomerExcludingAssessedTax", "NetIncomeLoss"],
 "dei": ["EntityPublicFloat", "EntityCommonStockSharesOutstanding"],
}
_lock = threading.Lock()


def reduce_facts(cf):
    out = {}
    if not cf:
        return out
    for tax, tags in TAGS.items():
        f = cf.get("facts", {}).get(tax, {})
        for t in tags:
            if t not in f:
                continue
            for unit, rows in f[t]["units"].items():
                if unit not in ("USD", "shares"):
                    continue
                out[t] = [[r.get("start"), r["end"], r["val"], r["accn"], r.get("form"), r.get("filed"), r.get("fp")]
                          for r in rows]
    return out


def subs(cik):
    d = sec_get(f"https://data.sec.gov/submissions/CIK{int(cik):010d}.json")
    if not d:
        return None
    def rows(r):
        keys = ["form", "filingDate", "reportDate", "items", "accessionNumber", "primaryDocument"]
        return [[r[k][i] if k in r else "" for k in keys] for i in range(len(r["form"]))]
    fl = rows(d["filings"]["recent"])
    for f in d["filings"].get("files", []):
        o = sec_get("https://data.sec.gov/submissions/" + f["name"])
        if o:
            fl += rows(o)
    return {"cik": int(cik), "name": d.get("name"), "sic": d.get("sic"), "sicDescription": d.get("sicDescription"),
            "tickers": d.get("tickers"), "exchanges": d.get("exchanges"), "category": d.get("category"),
            "stateOfIncorporation": d.get("stateOfIncorporation"), "formerNames": d.get("formerNames"), "filings": fl}


def one(cik):
    fp = p("firms", f"{int(cik)}.json")
    if os.path.exists(fp):
        return "cached"
    s = subs(cik)
    if s is None:
        res = {"cik": int(cik), "missing": True}
    else:
        sic = s.get("sic") or ""
        try:
            sic_i = int(sic)
        except ValueError:
            sic_i = -1
        excluded = (6000 <= sic_i <= 6799) or (4900 <= sic_i <= 4949) or sic_i in (4961, 4991) or sic_i < 0
        s["facts"] = {} if excluded else reduce_facts(sec_get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{int(cik):010d}.json"))
        s["sic_excluded"] = excluded
        res = s
    tmp = fp + ".tmp"
    with open(tmp, "w") as f:
        json.dump(res, f)
    os.replace(tmp, fp)
    return "ok"


def main():
    os.makedirs(p("firms"), exist_ok=True)
    cands = list(json.load(open(p("candidates.json"))).keys())
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 1
    t0 = time.time(); done = 0
    with ThreadPoolExecutor(workers) as ex:
        for r in ex.map(one, cands):
            done += 1
            if done % 200 == 0:
                print(f"{done}/{len(cands)} {time.time()-t0:.0f}s", flush=True)
    print("done", done)


if __name__ == "__main__":
    main()
