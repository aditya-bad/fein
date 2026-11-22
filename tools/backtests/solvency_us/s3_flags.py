#!/usr/bin/env python3
"""Step 3: point-in-time universe + solvency flags at each snapshot T (no outcome data used).
Output: BASE/universe.jsonl (one row per firm x snapshot) and a funnel printout."""
import glob, json, sys
from datetime import date, timedelta
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from common import p, SNAPS

D = lambda s: date.fromisoformat(s)
KFORMS = ("10-K", "10-KT", "10-K405")
CH = {  # concept -> tag fallbacks
 "E": ["StockholdersEquity", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
 "OI": ["OperatingIncomeLoss"],
 "PTI": ["IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest",
         "IncomeLossFromContinuingOperationsBeforeIncomeTaxesMinorityInterestAndIncomeLossFromEquityMethodInvestments",
         "IncomeLossFromContinuingOperationsBeforeIncomeTaxesDomestic"],
 "I": ["InterestExpense", "InterestExpenseDebt", "InterestAndDebtExpense", "InterestPaidNet", "InterestPaid"],
 "C": ["CashAndCashEquivalentsAtCarryingValue", "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", "Cash"],
 "CFO": ["NetCashProvidedByUsedInOperatingActivities", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
 "CAPEX": ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets"],
 "DIV": ["PaymentsOfDividends", "PaymentsOfDividendsCommonStock"],
 "BB": ["PaymentsForRepurchaseOfCommonStock", "PaymentsForRepurchaseOfEquity"],
 "TS": ["TreasuryStockValue"], "A": ["Assets"],
 "REV": ["Revenues", "SalesRevenueNet", "RevenueFromContractWithCustomerExcludingAssessedTax"],
}
FLOW = {"OI", "PTI", "I", "CFO", "CAPEX", "DIV", "BB", "REV"}


class Firm:
    def __init__(self, d, T):
        self.f = d["facts"]; self.T = T

    def tagval(self, tag, end, flow, accn):
        rows = self.f.get(tag)
        if not rows:
            return None
        best = None
        for st, en, v, ac, form, filed, fp in rows:
            if filed is None or D(filed) > self.T:
                continue
            if abs((D(en) - end).days) > 7:
                continue
            if flow:
                if not st or not (330 <= (D(en) - D(st)).days <= 400):
                    continue
            elif st:
                continue
            key = (ac == accn, filed)  # prefer the T-filing itself, else the latest filed <= T
            if best is None or key > best[0]:
                best = (key, v)
        return None if best is None else best[1]

    def get(self, concept, end, accn):
        for t in CH[concept]:
            v = self.tagval(t, end, concept in FLOW, accn)
            if v is not None:
                return v, t
        return None, None

    def raw(self, tag, end, accn, flow=False):
        return self.tagval(tag, end, flow, accn)


def debt(F, end, accn):
    r = lambda t: F.raw(t, end, accn)
    dc = r("DebtCurrent")
    if dc is not None:
        std = dc
    else:
        ltdc = max([x for x in (r("LongTermDebtCurrent"), r("LongTermDebtAndCapitalLeaseObligationsCurrent")) if x is not None], default=0)
        stb = r("ShortTermBorrowings")
        if stb is None:
            stb = sum(x for x in (r("CommercialPaper"), r("LinesOfCreditCurrent"), r("ShortTermBankLoansAndNotesPayable")) if x is not None)
        std = ltdc + stb
    nc = r("LongTermDebtNoncurrent")
    if nc is None:
        nc = r("LongTermDebtAndCapitalLeaseObligations")
    if nc is None:
        ltd = r("LongTermDebt")
        if ltd is not None:
            cur = r("LongTermDebtCurrent") or r("LongTermDebtAndCapitalLeaseObligationsCurrent") or 0
            nc = max(ltd - cur, 0)
    tagged = any(r(t) is not None for t in ("DebtCurrent", "LongTermDebtCurrent", "LongTermDebtAndCapitalLeaseObligationsCurrent",
                 "ShortTermBorrowings", "CommercialPaper", "LinesOfCreditCurrent", "ShortTermBankLoansAndNotesPayable",
                 "LongTermDebtNoncurrent", "LongTermDebtAndCapitalLeaseObligations", "LongTermDebt"))
    return std, std + (nc or 0), tagged


def snapshot(d, Ts):
    T = D(Ts)
    ks = [x for x in d["filings"] if x[0] in KFORMS and x[1] and T - timedelta(days=457) <= D(x[1]) <= T]
    if not ks:
        return None, "no 10-K filed in 15m before T"
    k = max(ks, key=lambda x: x[1])
    form, filed, rep, items, accn, doc = k
    F = Firm(d, T)
    # fiscal year end: reportDate, else latest instant end in that accession
    if rep:
        fy0 = D(rep)
    else:
        ends = [D(r[1]) for rows in d["facts"].values() for r in rows if r[3] == accn and not r[0]]
        if not ends:
            return None, "T-10-K has no XBRL facts"
        fy0 = max(ends)
    fl = [r for r in d["facts"].get("EntityPublicFloat", []) if r[3] == accn]
    if not fl:
        return None, "no public float on T-10-K"
    flt = max(fl, key=lambda r: r[1])[2]
    fy1 = fy0 - timedelta(days=365); fy2 = fy0 - timedelta(days=730)
    v = {}
    for c in CH:
        v[c], v[c + "_tag"] = F.get(c, fy0, accn)
    A = v["A"]
    if A is None or A <= 0:
        return None, "no total assets"
    if not (0.001 <= flt / A <= 1000):
        return None, "float/assets scaling check"
    row = {"cik": d["cik"], "name": d["name"], "sic": d["sic"], "T": Ts, "accn": accn, "filed": filed, "fy0": fy0.isoformat(),
           "float": flt, "assets": A}
    if not (3e8 <= flt <= 2e10):
        return None, "float outside $300M-$20B"
    std0, td0, tagged0 = debt(F, fy0, accn)
    std1, td1, tagged1 = debt(F, fy1, accn)
    div1, _ = F.get("DIV", fy1, accn); bb1, _ = F.get("BB", fy1, accn)
    div2, _ = F.get("DIV", fy2, accn); bb2, _ = F.get("BB", fy2, accn)
    cfo1, _ = F.get("CFO", fy1, accn); cap1, _ = F.get("CAPEX", fy1, accn)
    sh = [r for r in d["facts"].get("EntityCommonStockSharesOutstanding", []) if r[5] and D(r[5]) <= T]
    shares = None
    if sh:
        lastf = max(sh, key=lambda r: (r[5], r[1]))
        shares = sum(r[2] for r in sh if r[3] == lastf[3] and r[1] == lastf[1])
        row["shares_asof"] = lastf[1]
    E, OI, PTI, I, C, CFO = v["E"], v["OI"], v["PTI"], v["I"], v["C"], v["CFO"]
    CAPEX = v["CAPEX"] if v["CAPEX"] is not None else 0
    DIV = v["DIV"] or 0; BB = v["BB"] or 0; TS = v["TS"] or 0
    EBIT = OI if OI is not None else (PTI + (I or 0) if PTI is not None else None)
    FCF = CFO - CAPEX if CFO is not None else None
    big = lambda x: x is not None and abs(x) > 5 * A
    bad = {k for k, x in (("E", E), ("STD", std0), ("TD", td0), ("C", C), ("CFO", CFO), ("PAY", DIV + BB), ("I", I), ("EBIT", EBIT)) if big(x)}
    row.update(E=E, EBIT=EBIT, EBIT_src="OI" if OI is not None else ("PTI+I" if EBIT is not None else None), I=I, I_tag=v["I_tag"],
               STD=std0, TD=td0, TD1=td1, debt_tagged=tagged0, C=C, CFO=CFO, CAPEX=CAPEX, capex_missing=v["CAPEX"] is None,
               FCF=FCF, DIV=DIV, BB=BB, TS=TS, shares=shares, REV=v["REV"], scale_flags=sorted(bad))
    # S1
    if E is None or "E" in bad:
        s1 = s1raw = None
    else:
        s1raw = int(E < 0)
        pay3 = sum(x or 0 for x in (DIV, BB, div1, bb1, div2, bb2))
        exempt = E < 0 and FCF is not None and FCF > 0 and (TS + pay3) >= abs(E)
        s1 = int(E < 0 and not exempt)
        row["S1_exempt"] = int(bool(exempt)); row["pay3"] = pay3
    # S2
    if EBIT is None or "EBIT" in bad or "I" in bad:
        s2 = None
    elif I is not None and I > 0:
        s2 = int(EBIT / I < 1.5)
    else:
        s2 = 0 if td0 < 0.05 * A else None
    # S3
    if "STD" in bad:
        s3 = None
    elif std0 <= 0:
        s3 = 0
    elif C is None or CFO is None or "C" in bad or "CFO" in bad:
        s3 = None
    else:
        s3 = int(std0 > C + 0.5 * CFO)
    # S4
    if FCF is None or "CFO" in bad or "TD" in bad or "PAY" in bad:
        s4 = None
    else:
        s4 = int((DIV + BB) > 0 and (DIV + BB) > FCF and td0 > td1)
    s0 = None if EBIT is None or "EBIT" in bad else int(EBIT < 0)
    comps = [s1, s2, s3, s4]
    known = [x for x in comps if x is not None]
    s5 = int(sum(known) >= 2) if len(known) >= 2 else None
    row.update(S0=s0, S1=s1, S1raw=s1raw, S2=s2, S3=s3, S4=s4, S5=s5, nflags=sum(known))
    return row, "ok"


def main():
    files = glob.glob(p("firms", "*.json"))
    out = open(p("universe.jsonl"), "w")
    funnel = {}
    for fp in files:
        d = json.load(open(fp))
        if d.get("missing"):
            for Ts in SNAPS: funnel.setdefault(Ts, {}).setdefault("no submissions", 0); funnel[Ts]["no submissions"] += 1
            continue
        for Ts in SNAPS:
            if d.get("sic_excluded"):
                why = "excluded SIC (fin/REIT/utility/none)"; row = None
            else:
                row, why = snapshot(d, Ts)
            funnel.setdefault(Ts, {}).setdefault(why, 0); funnel[Ts][why] += 1
            if row:
                out.write(json.dumps(row) + "\n")
    out.close()
    json.dump(funnel, open(p("funnel.json"), "w"), indent=1)
    for Ts, f in funnel.items():
        print(Ts, json.dumps(f))


if __name__ == "__main__":
    main()
