#!/usr/bin/env python3
"""Bank/NBFC KPI CSV for score.py --csv (added 2026-11-22 after the FEDERALBNK dry run).

    python3 -I bank_kpis.py SYMBOL [--cache DIR] [--manual kpis_manual.csv] [--out SYMBOL_bank.csv]

Why: screener.in's bank page has no NIM, credit cost, CASA, GNPA history or loan book, so v1 of the
promise tracker could not score any bank guidance. Two sources, in this order of trust:
  1. NSE "integrated filing" XBRL (SEBI IntegratedFinance_Banking taxonomy, from Q3 FY25 onwards),
     fetched with the short UA. Gives, per quarter (standalone): advances, deposits, NII, other income,
     operating expenses, employee cost, provisions (other than tax), PAT, GNPA %, NNPA %, CET1 %,
     RoA (quarterly, annualised here x4), basic and diluted EPS.
  2. A hand-filled CSV of the bank's OWN KPI definitions from the investor presentation
     (nim_pct, credit_cost_pct, casa_ratio_pct, cod_pct, pcr_pct, slippage_pct, cost_income_pct, ...).
     Same format as financials.py: period_end,period_type,field,value. It overrides (1).
Derived from XBRL (named so they are never confused with company-defined KPIs):
  cost_income_xbrl_pct = opex / (NII + other income)      (company C/I may exclude one-offs)
  prov_to_adv_pct      = 4 x provisions / advances          (includes investment + standard-asset
                                                             provisions: NOT the company's "credit cost")
Every value is source-tagged in the `source` column. Untrusted data: XBRL is parsed with regex only.
"""
import argparse
import csv
import datetime as dt
import gzip
import os
import re
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

API = "https://www.nseindia.in/api/integrated-filing-results"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json, text/plain, */*",
           "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip", "Referer": "https://www.nseindia.in/"}
FACTS = {"Advances": "advances", "Deposits": "deposits", "InterestEarned": "interest_earned",
         "InterestExpended": "interest_expended", "OtherIncome": "other_income", "OperatingExpenses": "opex",
         "EmployeesCost": "employee_cost", "ProvisionsOtherThanTaxAndContingencies": "provisions",
         "ProfitLossForThePeriod": "net_profit", "PercentageOfGrossNpa": "gnpa_pct", "PercentageOfNpa": "nnpa_pct",
         "CET1Ratio": "cet1_pct", "ReturnOnAssets": "roa_q", "BasicEarningsPerShareAfterExtraordinaryItems": "eps",
         "DilutedEarningsPerShareAfterExtraordinaryItems": "eps_diluted"}
PCT = {"gnpa_pct", "nnpa_pct", "cet1_pct"}
_last = [0.0]


def get(url, binary=False):
    wait = 1.5 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=60) as r:
        b = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            b = gzip.decompress(b)
    return b if binary else __import__("json").loads(b.decode("utf-8", "replace"))


def parse_xbrl(text):
    """-> {field: value} for the current-quarter (OneD duration / OneI instant) contexts."""
    unit = 1e7  # rupees -> crore
    out = {}
    for tag, ctx, val in re.findall(r"<in-capmkt:(\w+) contextRef=\"([^\"]+)\"[^>]*>([^<]+)<", text):
        if tag not in FACTS or ctx not in ("OneD", "OneI"):
            continue
        f = FACTS[tag]
        try:
            v = float(val)
        except ValueError:
            continue
        if f in PCT:
            v *= 100
        elif f == "roa_q":
            f, v = "roa_pct", v * 400          # quarterly, not annualised in XBRL
        elif f not in ("eps", "eps_diluted"):
            v /= unit
        out.setdefault(f, v)
    if out.get("interest_earned") is not None and out.get("interest_expended") is not None:
        out["nii"] = out["interest_earned"] - out["interest_expended"]
        den = out["nii"] + (out.get("other_income") or 0)
        if out.get("opex") and den:
            out["cost_income_xbrl_pct"] = 100 * out["opex"] / den
    if out.get("provisions") is not None and out.get("advances"):
        out["prov_to_adv_pct"] = 400 * out["provisions"] / out["advances"]
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol")
    p.add_argument("--cache")
    p.add_argument("--manual", help="presentation KPIs CSV (period_end,period_type,field,value[,source])")
    p.add_argument("--basis", default="Standalone", choices=["Standalone", "Consolidated"])
    p.add_argument("--out")
    a = p.parse_args(argv)
    sym = a.symbol.upper()
    root = C.cache_root(a.cache)
    xdir = C.sym_dir(root, sym, "xbrl")
    d = get(API + "?" + urllib.parse.urlencode({"index": "equities", "symbol": sym,
                                                 "type": "Integrated Filing- Financials"}))
    rows = []
    for x in (d.get("data") or []):
        if x.get("consolidated") != a.basis or not x.get("xbrl"):
            continue
        qe = dt.datetime.strptime(x["qe_Date"], "%d-%b-%Y").date()
        fn = os.path.join(xdir, f"{qe}_{a.basis[0]}.xml")
        if not os.path.exists(fn):
            open(fn, "wb").write(get(x["xbrl"], binary=True))
        facts = parse_xbrl(open(fn, errors="replace").read())
        for f, v in sorted(facts.items()):
            rows.append({"period_end": qe.isoformat(), "period_type": "Q", "field": f, "value": round(v, 4),
                         "source": "NSE integrated-filing XBRL " + os.path.basename(x["xbrl"])})
            if f in ("advances", "deposits"):
                rows.append({"period_end": qe.isoformat(), "period_type": "BS", "field": f, "value": round(v, 2),
                             "source": "NSE integrated-filing XBRL"})
    if a.manual:
        man = list(csv.DictReader(open(a.manual)))
        keys = {(r["period_end"], r["period_type"], r["field"]) for r in man}
        rows = [r for r in rows if (r["period_end"], r["period_type"], r["field"]) not in keys]
        rows += [{"period_end": r["period_end"], "period_type": r["period_type"], "field": r["field"],
                  "value": r["value"], "source": r.get("source") or "manual"} for r in man]
    rows.sort(key=lambda r: (r["period_end"], r["period_type"], r["field"]))
    out = a.out or os.path.join(C.sym_dir(root, sym), f"{sym}_bank.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["period_end", "period_type", "field", "value", "source"])
        w.writeheader()
        w.writerows(rows)
    qs = sorted({r["period_end"] for r in rows if r["period_type"] == "Q"})
    print(f"{sym}: {len(rows)} rows, quarters {qs[0] if qs else '-'} .. {qs[-1] if qs else '-'} -> {out}")


if __name__ == "__main__":
    main()
