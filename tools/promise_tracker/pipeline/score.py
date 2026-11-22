#!/usr/bin/env python3
"""Stage 4: auto-score FINANCIAL promises against reported numbers, and link re-dated
promises into supersedes-chains (goalpost moves counted automatically).

    python3 -I score.py SYMBOL --promises promises.jsonl [--seed memdb_seed.json]
                        [--csv numbers.csv] [--no-screener] [--as-of YYYY-MM-DD]
                        [--cache DIR] [--out scored.jsonl]

Input promises (JSONL from the LLM step, see llm_extract_prompt.md) or --seed (a memdb seed
JSON such as the pilot ledgers; flattened automatically). Fields used:
    id, said_on, speaker, quote, category, metric, target(text), target_low, target_high,
    unit, comparator, measure, period, deadline, deadline_precision, chain_key,
    acknowledges_revision, specificity, materiality, volunteered
Numbers: screener.in consolidated (financials.py, cached) and/or --csv (overrides screener).

For each promise adds:
  auto  = {measure, period, period_end, target_used, actual, gap, status, rule, notes, ...}
          status: delivered | partly | missed | pending | awaiting-data | not-auto-scorable
  chain = {chain_key, supersedes, restates, change, goalpost_move, n_goalpost_moves_in_chain}
  auto_status_final = auto status after the chain rule (a quietly lowered or re-dated target
          whose ORIGINAL version was then missed becomes moved-goalpost)

Measures (controlled vocabulary; the LLM fills `measure`, else it is inferred from metric text):
  revenue_growth_yoy_pct, revenue_qoq_pct, revenue_abs_cr, ebitda_margin_pct,
  ebitda_margin_incl_oi_pct, pat_growth_yoy_pct, pat_abs_cr, finance_cost_pct_revenue,
  debtor_days, roce_pct, fcf_cr, dividend_payout_pct, borrowings_cr, capex_cr (derived).
Status thresholds (fixed across companies, pilot lesson #4):
  growth % (pp gap vs target low):  delivered >= -max(0.5, 5% of |target|); partly >= -max(2, 20% of |target|)
  margin / ROCE / finance-cost % (pp): delivered within 0.3 pp; partly within 1.5 pp
  absolute amounts and days (ratio):   delivered >= 95%; partly 80-95% (days/costs mirrored)
  'late' rule: a level target missed at the deadline but met on the next quarter's TTM -> partly
  Beats count as delivered (one-sided), except when the comparator is '<=' (a ceiling).
Fuzzy deadlines: the period is the fiscal period that contains the deadline; 'vague' or missing
deadlines default to the FY two years after the call (later-date rule), flagged in notes.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
import financials as F  # noqa: E402

DERIVED_CAPEX = [False]
# v1.1 (2026-11-22, FEDERALBNK dry run): bank/NBFC measures. Screener's bank page has no NIM, credit
# cost, GNPA, CASA or loan book, so these are scored ONLY from a --csv built from the investor
# presentation / results PDF (one row per number; see financials.py). Field name = measure name
# for ratios; growth measures read the level fields advances / deposits / casa / fee_income.
BANK_TIGHT = {"nim_pct", "credit_cost_pct", "gnpa_pct", "nnpa_pct", "roa_pct", "slippage_pct", "cod_pct",
              "cof_pct", "yield_advances_pct"}                # 5 bps matters: delivered within 0.05 pp, partly 0.15 pp
BANK_WIDE = {"roe_pct", "cost_income_pct", "casa_ratio_pct", "pcr_pct", "cet1_pct", "crar_pct", "cd_ratio_pct"}
BANK_GROWTH = {"loan_growth_yoy_pct": "advances", "deposit_growth_yoy_pct": "deposits",
               "casa_growth_yoy_pct": "casa", "fee_growth_yoy_pct": "fee_income"}
BANK_MEASURES = BANK_TIGHT | BANK_WIDE | set(BANK_GROWTH)
# v1.2 (2026-11-22, IT mid-caps): IT-services measures. Constant-currency (CC) and USD growth, TCV/deal wins,
# utilisation, attrition, headcount and client concentration are company-defined and are scored ONLY from a --csv
# (field name = measure name; FY rows for FY claims, Q rows for quarters; a reported ratio is read, never derived).
# EBIT margin (the band IT companies guide) is derived from screener as (operating profit - depreciation) / sales
# unless the CSV gives ebit_margin_pct (company EBIT, which governs). v1.1 read "EBIT margin 14-16%" as EBITDA
# margin (screener OPM, ~3 pp higher for IT) and "CC growth 10%" as INR revenue growth (FX moves of 2-4 pp).
IT_GROWTH = {"cc_revenue_growth_yoy_pct", "cc_revenue_qoq_pct", "usd_revenue_growth_yoy_pct", "usd_revenue_qoq_pct"}
IT_PP = {"ebit_margin_pct", "utilisation_pct", "attrition_pct", "top5_client_share_pct", "top10_client_share_pct"}
IT_AMOUNT = {"tcv_usd_mn", "headcount"}
IT_CSV_ONLY = IT_GROWTH | IT_AMOUNT | (IT_PP - {"ebit_margin_pct"})
IT_MEASURES = IT_GROWTH | IT_PP | IT_AMOUNT
IT_RX = [   # matched on the METRIC text first (then metric+target); order matters
    (r"\btcv\b|total contract value|deal wins?|large deals?|\bbookings?\b|\bacv\b", "tcv_usd_mn"),
    (r"attrition", "attrition_pct"),
    (r"utili[sz]ation", "utilisation_pct"),
    (r"headcount|head count|employee (count|base)", "headcount"),
    (r"top[\s-]?(5|five) (clients?|accounts?|customers?)", "top5_client_share_pct"),
    (r"top[\s-]?(10|ten) (clients?|accounts?|customers?)", "top10_client_share_pct"),
    (r"\bebit\b(?!da)|ebit (margin|band)|operating (margin )?band", "ebit_margin_pct"),
    (r"(constant[\s-]currency|\bcc\b).*(q-?o-?q|sequential)|(q-?o-?q|sequential).*(constant[\s-]currency|\bcc\b)", "cc_revenue_qoq_pct"),
    (r"constant[\s-]currency|\bcc\b", "cc_revenue_growth_yoy_pct"),
    (r"(\busd\b|dollar|\$|us\$).*(q-?o-?q|sequential)", "usd_revenue_qoq_pct"),
    (r"(\busd\b|dollar|us\$)\s*(revenue|growth|terms)|(revenue|growth)\s*(in )?(\busd\b|dollar|us\$)", "usd_revenue_growth_yoy_pct"),
]
IT_SEGMENT_RX = re.compile(r"vertical|\bbfsi\b|\bbfs\b|insurance|healthcare|hi[\s-]?tech|\bmanufacturing\b|retail|"
                           r"travel|\bgeo|europe|north america|\busa?\b region|\brow\b|segment|service line|\bdirect\b|"
                           r"\bdxc\b|\bhp\b|top client|client [a-z0-9]|account|nagarro|cigniti|organic|ex-|excluding", re.I)


# v1.3 (2026-11-22, US industrials: WTS, AOS, SSD, LECO). US companies (promise id 'promise:US-...', symbol 'US-...' or
# market 'us') get their OWN vocabulary and never fall through to the India/screener measures. All are scored from a --csv
# only (company-reported or SEC XBRL figures; field name = measure name, FY / Q rows as for IT).
US_GROWTH = {"organic_growth_pct", "net_sales_growth_pct", "segment_sales_growth_pct"}
US_PP = {"adj_op_margin_pct", "gaap_op_margin_pct", "adj_ebitda_margin_pct", "segment_margin_pct", "fcf_conversion_pct",
         "cash_return_pct_fcf"}
US_AMOUNT = {"adj_eps_usd", "gaap_eps_usd", "fcf_usd_mn", "capex_usd_mn", "buyback_usd_mn", "cost_savings_usd_mn",
             "price_realisation_usd_mn"}
US_MEASURES = US_GROWTH | US_PP | US_AMOUNT
US_RX = [   # matched on the METRIC text first (then metric+target); order matters
    (r"segment|division|americas|international|europe|apmea|rest of world|north america|boiler|water treatment|water heater|"
     r"automation|harris|china|india|leonard", "_segment"),
    (r"organic", "organic_growth_pct"),
    (r"\beps\b|earnings per share|per share", "_eps"),
    (r"(fcf|free cash flow|cash) conversion|fcf\s*/\s*net income", "fcf_conversion_pct"),
    (r"(returned?|return of|dividends \+ buybacks).*(fcf|free cash flow)|/ ?fcf", "cash_return_pct_fcf"),
    (r"free cash flow|\bfcf\b", "fcf_usd_mn"),
    (r"capex|capital expenditure", "capex_usd_mn"),
    (r"repurchase|buyback", "buyback_usd_mn"),
    (r"savings|cost (programme|program|reduction)|operating expenses", "cost_savings_usd_mn"),
    (r"price[\s/-]*cost|price (actions?|increases?|realis|realiz)", "price_realisation_usd_mn"),
    (r"ebitda", "adj_ebitda_margin_pct"),
    (r"adjusted operating|adj\.? operating|operating income margin|operating margin", "_opm"),
    (r"(net )?sales growth|revenue growth|top[\s-]?line|net sales", "net_sales_growth_pct"),
]


def is_us(p):
    return (str(p.get("id", "")).startswith("promise:US-") or str(p.get("symbol", "")).startswith("US-")
            or str(p.get("market", "")).lower() == "us")


def infer_us_measure(metric, text):
    """US-company KPI. Segment / product-line / country figures -> segment_* (never the group measure).
    Multi-year targets (2030, CAGR, 'average across the cycle') return None (judgment)."""
    full = (metric + " " + text).lower()
    if re.search(r"cagr|20[3-9]\d|across the cycle|\baverage\b.*20\d\d-20\d\d", full):
        return None
    seg = bool(re.search(US_RX[0][0], metric.lower()))
    if seg and "%" not in full and re.search(r"\$|\bmn\b|million", full):
        return None   # segment / acquired-business dollar amounts (e.g. 'Leonard Valve sales ~$70 mn'): judgment
    for src in (metric, text):
        tl = src.lower()
        for rx, m in US_RX[1:]:
            if re.search(rx, tl):
                if m == "_eps":
                    return "adj_eps_usd" if "adjust" in full or "continuing" in full else "gaap_eps_usd"
                if m == "_opm":
                    return "segment_margin_pct" if seg else ("gaap_op_margin_pct" if "gaap" in full else "adj_op_margin_pct")
                if m in ("net_sales_growth_pct", "organic_growth_pct") and seg:
                    return "segment_sales_growth_pct"
                if m == "adj_ebitda_margin_pct" and seg:
                    return "segment_margin_pct"
                return m
    if seg and re.search(r"margin", full):
        return "segment_margin_pct"
    if seg and re.search(r"sales|growth", full):
        return "segment_sales_growth_pct"
    return None


def infer_it_measure(metric, text):
    """IT-services KPI from the metric text (fallback: metric+target). Vertical/geo/client-level growth,
    'organic'/'excluding X' variants and multi-year CAGRs are NOT the company-level measure (judgment)."""
    for src in (metric, text):
        tl = src.lower()
        for rx, m in IT_RX:
            if re.search(rx, tl):
                if m in IT_GROWTH and (IT_SEGMENT_RX.search(metric) or re.search(r"cagr|\d\s*(-|to)\s*\d\s*years|by fy\d\d.*fy\d\d", tl)):
                    return None
                if m == "utilisation_pct" and re.search(r"capacit|plant|engineering|line\b|wheel|tonn|factory|press", tl):
                    return None   # manufacturing capacity utilisation, not billable-staff utilisation
                if m == "ebit_margin_pct" and re.search(r"segment|vertical|nagarro|organic|ex-|excluding|exit rate", metric.lower()):
                    return None
                return m
    return None
LOWER_BETTER = {"finance_cost_pct_revenue", "debtor_days", "borrowings_cr",
                "credit_cost_pct", "gnpa_pct", "nnpa_pct", "slippage_pct", "cod_pct", "cof_pct", "cost_income_pct",
                "attrition_pct", "top5_client_share_pct", "top10_client_share_pct"}
PP_MEASURES = {"ebitda_margin_pct", "ebitda_margin_incl_oi_pct", "finance_cost_pct_revenue", "roce_pct",
               "dividend_payout_pct"}
GROWTH_MEASURES = {"revenue_growth_yoy_pct", "revenue_qoq_pct", "pat_growth_yoy_pct"} | set(BANK_GROWTH) | IT_GROWTH | US_GROWTH
PP_MEASURES |= BANK_WIDE | IT_PP | US_PP
SEGMENT_RX = re.compile(r"segment|division|polymer|engineering|infra|export|aftermarket|small[\s-]ag|large ag|"
                        r"construction|mexico|fabrication|warehouse|order|utili[sz]ation|capacity|share of|mix|epc|"
                        r"substation|pipes|tonne|\busd\b|\$|normali[sz]ed|ex-fx|through[\s-]the[\s-]cycle|cagr|"
                        r"long[\s-]term|5-year|market share|tariff|freight|net working|company definition|nwc|\bshare\b|platform|"
                        r"rais\w+|equity|dilution|funding|acquisition|per quarter|run[\s-]rate shape|shape", re.I)


# ------------------------------------------------------------------ input
def flatten_seed(path):
    out = []
    for r in json.load(open(path)):
        if r.get("type") != "promise":
            continue
        d = dict(r["data"])
        d["id"] = r["id"]
        d["title"] = r.get("title")
        d["manual_status"] = d.get("status")
        v = d.get("volunteered")
        d["volunteered"] = v is True or v == "volunteered"
        out.append(d)
    return out


def _parse_us_target(t):
    head = re.split(r"\(|;|\bvs\b|\bfrom\b", t)[0]
    comp = ">=" if re.search(r">=|>|at least|or more|or higher|\+$", head) else "~"
    m = re.search(r"\$\s*(\d{1,3}\.\d{2})\s*(?:-|to)\s*\$?\s*(\d{1,3}\.\d{2})(?!\s*(?:mn|bn|million|billion))", head)
    if m:
        a_, b_ = float(m.group(1)), float(m.group(2))
        return min(a_, b_), max(a_, b_), "USD/share", "range"
    m = re.search(r"\$\s*(\d{1,3}\.\d{2})(?!\d|\s*(?:mn|bn|million|billion))", head)
    if m:
        v = float(m.group(1)); return v, v, "USD/share", comp
    for rx, lo, hi in ((r"low[\s-]single[\s-]digits?", 1, 3), (r"mid[\s-]single[\s-]digits?", 4, 6),
                       (r"low[\s-]teens", 11, 13), (r"mid[\s-]teens", 14, 16)):
        if re.search(rx, head, re.I):
            return lo, hi, "%", "range"
    return None


def parse_target(text, us=False):
    """'+25% (FY24 base ...)' -> (25, 25, '%', '>='?) ; '0% to -3%' -> (-3, 0, '%', 'range').
    us=True (v1.3) adds per-share ranges ('$3.42 to $3.52' -> USD/share) and the US growth words ('low/mid single digit',
    'low/mid teens'); India/IT parsing (us=False) is unchanged."""
    if not text:
        return None
    if us:
        r = _parse_us_target(str(text).replace("−", "-").replace("–", "-"))
        if r:
            return r
    t = str(text).replace("−", "-").replace("–", "-")
    head = re.split(r"\(|;|\bvs\b|\bfrom\b|\bon\b FY|\bbase\b", t)[0]
    comp = "~"
    if re.search(r"(^|\s)(>|>=|≥|at least|minimum|above|over|in excess|plus|\+$)|\d\s*%?\s*\+|\d\s*(?:mn|bn|million|billion)\s*\+|%\s*plus|comfortably above", head, re.I):
        comp = ">="
    if re.search(r"(^|\s)(<|<=|≤|below|under|at most|max|less than|within)", head, re.I):
        comp = "<="
    bps = re.findall(r"([+-]?\d+(?:\.\d+)?)\s*(?:bps|bp\b|basis points?)", head, re.I)
    if bps and not re.search(r"\d\s*%", head):   # '40-50 bps' -> 0.40-0.50 %  (bank credit cost / NIM)
        mr = re.search(r"(\d+(?:\.\d+)?)\s*(?:bps)?\s*(?:-|to)\s*(\d+(?:\.\d+)?)\s*(?:bps|bp\b|basis)", head, re.I)
        vals = [float(mr.group(1)) / 100, float(mr.group(2)) / 100] if mr else [abs(float(x)) / 100 for x in bps[:1]]
        rng = len(vals) == 2
        lo, hi = (min(vals), max(vals)) if rng else (vals[0], vals[0])
        if re.search(r"\b(up|down|improve|expan|compress|reduc|declin|fall|rise|increase|decrease)\w*", head, re.I):
            return None   # a CHANGE in bps ('NIM up 5 bps') is not a level target: leave to judgment
        return lo, hi, "%", ("range" if rng and comp == "~" else comp)
    # v1.1: '18-20%' / '3.2-3.3%' / '3.2 to 3.3%' (no % on the first number). v1 read the dash as a
    # minus sign and returned (-20, -20). A leading sign is kept only when spaced or explicit (+/-x% to -y%).
    m = re.search(r"(?<![\d.])([+-]?\d+(?:\.\d+)?)\s*%?\s*(?:-|to)\s*([+-]?\d+(?:\.\d+)?)\s*%", head)
    if m and not re.match(r"[+-]", m.group(2)) or (m and re.search(r"\bto\b", m.group(0))):
        a_, b_ = float(m.group(1)), float(m.group(2))
        return min(a_, b_), max(a_, b_), "%", ("range" if comp == "~" else comp)
    pcts = re.findall(r"([+-]?\d+(?:\.\d+)?)\s*%", head)
    if pcts:
        vals = [float(x) for x in pcts[:2]]
        rng = re.search(r"\d\s*%?\s*(?:to|-)\s*[+-]?\d", head) and len(vals) == 2
        lo, hi = (min(vals), max(vals)) if rng else (vals[0], vals[0])
        if rng and comp == "~":
            comp = "range"
        return lo, hi, "%", comp
    m = re.search(r"(?:INR|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)\s*(?:-|to)\s*(?:INR|Rs\.?|₹)?\s*([\d,]+(?:\.\d+)?)\s*cr", head, re.I)
    if m:
        return float(m.group(1).replace(",", "")), float(m.group(2).replace(",", "")), "INR cr", \
            ("range" if comp == "~" else comp)
    m = re.search(r"(?:INR|Rs\.?|₹)\s*~?\s*([\d,]+(?:\.\d+)?)\s*(cr|crore)", head, re.I) or \
        re.search(r"~?\s*([\d,]+(?:\.\d+)?)\s*(cr|crore)", head, re.I)
    if m:
        v = float(m.group(1).replace(",", ""))
        return v, v, "INR cr", comp
    m = re.search(r"([\d,]+(?:\.\d+)?)\s*days", head, re.I)
    if m:
        v = float(m.group(1).replace(",", ""))
        return v, v, "days", comp
    # v1.2 (IT): 'USD 500 mn' / '$1.5 bn' / '$300-350 million' -> USD mn; qualitative growth words
    m = re.search(r"(?:USD|US\$|\$)\s*~?\s*([\d,]+(?:\.\d+)?)\s*(?:(?:-|to)\s*(?:USD|US\$|\$)?\s*([\d,]+(?:\.\d+)?)\s*)?"
                  r"(mn|million|bn|billion)\b", head, re.I)
    if m:
        k = 1000.0 if m.group(3).lower() in ("bn", "billion") else 1.0
        a_ = float(m.group(1).replace(",", "")) * k
        b_ = float(m.group(2).replace(",", "")) * k if m.group(2) else a_
        return min(a_, b_), max(a_, b_), "USD mn", ("range" if m.group(2) and comp == "~" else comp)
    if re.search(r"\bhigh[\s-]single[\s-]digits?\b", head, re.I):
        return 7, 9, "%", "range"
    if re.search(r"\blow[\s-]double[\s-]digits?\b", head, re.I):
        return 10, 12, "%", "range"
    if re.search(r"\bdouble[\s-]digits?\b", head, re.I):
        return 10, 10, "%", ">="
    if re.search(r"\b(mid[\s-]teens?)\b", head, re.I):
        return 14, 16, "%", "range"
    if re.search(r"\bflat\b|in line|~?\s*0\s*%", head, re.I):
        return 0, 0, "%", "~"
    return None


BANK_RX = [   # order matters: specific before generic. Matched on the METRIC text first.
    (r"\bnim\b|net interest margin", "nim_pct"),
    (r"credit cost|\bloan loss provision", "credit_cost_pct"),
    (r"slippage", "slippage_pct"),
    (r"\bgnpa\b|gross npa|gross non[\s-]performing", "gnpa_pct"),
    (r"\bnnpa\b|net npa|net non[\s-]performing", "nnpa_pct"),
    (r"\bpcr\b|provision coverage", "pcr_pct"),
    (r"cost[\s-]to[\s-]income|cost[\s/]income|\bc/i\b", "cost_income_pct"),
    (r"cost of deposits?|\bcod\b", "cod_pct"),
    (r"cost of funds?|\bcof\b", "cof_pct"),
    (r"yield on (advances|loans)", "yield_advances_pct"),
    (r"\bcasa\b.*(growth|grow)", "casa_growth_yoy_pct"),
    (r"\bcasa\b", "casa_ratio_pct"),
    (r"\broa\b|return on (average )?assets", "roa_pct"),
    (r"\broe\b|return on (average )?equity", "roe_pct"),
    (r"\bcet[\s-]?1\b|common equity tier", "cet1_pct"),
    (r"\bcrar\b|capital adequacy", "crar_pct"),
    (r"\bcd ratio\b|credit[\s-]to[\s-]deposit|credit[\s-]deposit", "cd_ratio_pct"),
    (r"(loan|advances?|credit|book) growth|grow (the )?(loan|advances|book)", "loan_growth_yoy_pct"),
    (r"deposit growth|grow (the )?deposits", "deposit_growth_yoy_pct"),
    (r"fee (income )?growth", "fee_growth_yoy_pct"),
]


BANK_SEGMENT_RX = re.compile(r"corporate|\bcib\b|retail|gold|\bsme\b|msme|business banking|\bbub\b|personal|card|\blap\b|"
                             r"housing|home loan|vehicle|cv/ce|micro|mfi|agri|segment|commercial banking|wholesale|nri|\bnr\b|fcnr", re.I)


def infer_bank_measure(metric, text):
    """Segment growth ("corporate book growth") and multi-year CAGRs are NOT the bank-level measure.
    Bank/NBFC KPI from the metric text (fallback: metric+target). Without this, 'net interest
    margin ~3.2%' matched the 'interest + %' finance-cost rule and was scored as interest/revenue."""
    for src in (metric, text):
        tl = src.lower()
        for rx, m in BANK_RX:
            if re.search(rx, tl):
                if m.endswith("growth_yoy_pct") and re.search(r"x of|\dx\b|times|multiple of|gdp|industry|system",
                                                              text.lower()):
                    return None   # relative-to-system growth: judgment item
                if m.endswith("growth_yoy_pct") and (BANK_SEGMENT_RX.search(metric) or
                                                     re.search(r"cagr|\d\s*(-|to)\s*\d\s*years|years\)", text.lower())):
                    return None   # segment growth or multi-year CAGR: judgment / segment CSV
                if m in ("casa_ratio_pct",) and re.search(r"nri|\bnr\b", metric.lower()):
                    return None
                return m
        if src is metric and metric.strip():
            continue
    return None


def infer_measure(p):
    if p.get("measure"):
        return p["measure"], "given"
    text = " ".join(str(p.get(k) or "") for k in ("metric", "target"))
    metric = str(p.get("metric") or "")
    if is_us(p):   # v1.3: US companies never fall through to the India / screener measures
        um = infer_us_measure(metric, text)
        return (um, "inferred (US)") if um else (None, "US company: no recognised US measure (judgment)")
    bm = infer_bank_measure(metric, text)
    if bm:
        return bm, "inferred (bank)"
    im = infer_it_measure(metric, text)
    if im:
        return im, "inferred (IT services)"
    if re.search(r"constant[\s-]currency|\bcc\b|\busd\b|dollar|us\$|\bebit\b(?!da)", text.lower()):
        return None, "IT variant (vertical/geo/client, organic/ex-acquisition, CAGR or segment EBIT): judgment"
    if SEGMENT_RX.search(metric) or SEGMENT_RX.search(str(p.get("target") or "")[:40]):
        return None, "segment/non-financial or company-defined metric"
    tl = text.lower()
    if re.search(r"finance cost|interest", tl) and "%" in tl:
        return "finance_cost_pct_revenue", "inferred"
    if re.search(r"debtor|receivable", tl) and "days" in tl:
        return "debtor_days", "inferred"
    if re.search(r"\broce\b", tl):
        return "roce_pct", "inferred"
    if re.search(r"free cash flow|\bfcf\b", tl):
        return "fcf_cr", "inferred"
    if re.search(r"capex|capital expenditure", tl):
        return ("capex_pct_revenue" if re.search(r"% of (revenue|top ?line|sales)|/revenue", tl) else "capex_cr"), "inferred"
    if re.search(r"dividend", tl) and "%" in tl:
        return "dividend_payout_pct", "inferred"
    if re.search(r"ebitda|operating margin|\bopm\b|margin", tl) and re.search(r"\d\s*%", tl):
        if re.search(r"gross|pat margin|net margin", tl):
            return None, "gross/net margin not auto-scored"
        if re.search(r"incl\.? other income|including other income", tl):
            return "ebitda_margin_incl_oi_pct", "inferred"
        return "ebitda_margin_pct", "inferred"
    if re.search(r"\bpat\b|net profit|profit after tax", tl):
        return ("pat_growth_yoy_pct" if "%" in tl else "pat_abs_cr"), "inferred"
    if re.search(r"revenue|sales|top[\s-]?line|turnover", tl):
        if re.search(r"qoq|sequential|in line with q|vs q\d", tl):
            return "revenue_qoq_pct", "inferred"
        if re.search(r"\bq[1-4]\s?fy|quarterly", tl) and re.search(r"cr\b|crore", tl) and "%" not in tl.split("(")[0]:
            return "revenue_abs_cr", "inferred"
        if re.search(r"growth|yoy|\d\s*%", tl):
            return "revenue_growth_yoy_pct", "inferred"
        if re.search(r"cr\b|crore", tl):
            return "revenue_abs_cr", "inferred"
    return None, "no financial measure recognised"


def resolve_period(p, measure):
    """-> (kind, end_date, label, notes)"""
    notes = []
    per = (p.get("period") or "").upper().replace(" ", "").replace("'", "")
    m = re.match(r"Q([1-4])FY(\d{2,4})$", per)
    if m:
        d = C.quarter_end(m.group(1), m.group(2))
        return "Q", d, per, notes
    m = re.match(r"H([12])FY(\d{2,4})$", per)
    if m:
        d = C.quarter_end(2 if m.group(1) == "1" else 4, m.group(2))
        return "H", d, per, notes
    m = re.match(r"FY(\d{2,4})$", per)
    if m:
        return "FY", C.fy_end(m.group(1)), per, notes
    said = dt.date.fromisoformat(p["said_on"])
    dl = None
    try:
        dl = dt.date.fromisoformat(str(p.get("deadline"))[:10])
    except ValueError:
        pass
    if dl is None:
        dl = C.fy_end(C.fy_of(said) + 2)
        notes.append("no parseable deadline: FY+2 assumed (later-date rule)")
    prec = (p.get("deadline_precision") or "").lower()
    text = " ".join(str(p.get(k) or "") for k in ("metric", "target", "title"))
    if measure == "revenue_qoq_pct" or prec in ("quarter",) and measure in ("revenue_abs_cr", "revenue_qoq_pct") \
            or re.search(r"\bQ[1-4]\s?FY|\bquarter(ly)?\b|/qtr", text, re.I) and measure in ("revenue_abs_cr", "revenue_qoq_pct"):
        qe = C.quarter_end_of(dl)
        q, fy = C.fq_of(qe)
        return "Q", qe, C.qlabel(q, fy), notes
    if prec == "half-year" and measure in ("revenue_growth_yoy_pct", "revenue_abs_cr", "ebitda_margin_pct"):
        qe = C.quarter_end_of(dl)
        if qe.month not in (9, 3):
            qe = C.quarter_end_of(qe + dt.timedelta(days=92))
        q, fy = C.fq_of(qe)
        return "H", qe, f"H{1 if q == 2 else 2}FY{fy % 100:02d}", notes
    if prec == "vague":
        notes.append("vague deadline: scored on the FY containing the stated/assumed deadline")
    fy = C.fy_of(dl)
    if measure in ("capex_cr", "capex_pct_revenue") and (dl - said).days > 300 and C.fy_end(fy) != dl and dl.month != 3:
        notes.append("12-month window mapped to FY")
    return "FY", C.fy_end(fy), f"FY{fy % 100:02d}", notes


# ------------------------------------------------------------------ actuals
def _prev_q(d):
    return C.quarter_end_of(d - dt.timedelta(days=92))


def _sum_q(fin, end, n, field):
    ds, d = [], end
    for _ in range(n):
        ds.append(d)
        d = _prev_q(d)
    vals = [fin["Q"].get(x, {}).get(field) for x in ds]
    return None if any(v is None for v in vals) else sum(vals)


def period_value(fin, kind, end, field):
    if kind == "Q":
        return fin["Q"].get(end, {}).get(field)
    if kind == "H":
        return _sum_q(fin, end, 2, field)
    if kind == "TTM":
        return _sum_q(fin, end, 4, field)
    v = fin["FY"].get(end, {}).get(field)
    if v is None and field in ("sales", "op_profit", "other_income", "interest", "net_profit", "pbt", "depreciation"):
        v = _sum_q(fin, end, 4, field)
    return v


def year_ago(d):
    return dt.date(d.year - 1, d.month, d.day if not (d.month == 2 and d.day == 29) else 28)


def bank_actual(fin, measure, kind, end):
    """Bank KPIs from the --csv. Ratios: the FY row if given, else the mean of the four quarterly
    (annualised) values; Q -> the quarter row. Growth: level field at period end vs a year earlier
    (Q rows first, then BS rows)."""
    if measure in BANK_GROWTH:
        fld = BANK_GROWTH[measure]
        def lvl(d):
            for k in ("Q", "BS", "FY"):
                v = fin.get(k, {}).get(d, {}).get(fld)
                if v is not None:
                    return v
            return None
        if fld == "fee_income" and kind == "FY":
            a, b = _sum_q(fin, end, 4, fld), _sum_q(fin, year_ago(end), 4, fld)
        else:
            a, b = lvl(end), lvl(year_ago(end))
        return (100 * (a / b - 1), f"{fld} {a:g} vs {b:g} (CSV)") if a and b else (None, f"{fld} missing in CSV")
    if kind == "Q":
        v = fin.get("Q", {}).get(end, {}).get(measure)
        return (v, f"{measure} Q (CSV)") if v is not None else (None, f"{measure} missing in CSV")
    v = fin.get("FY", {}).get(end, {}).get(measure)
    if v is not None:
        return v, f"{measure} FY (CSV)"
    if kind in ("FY", "H", "TTM"):
        n = 2 if kind == "H" else 4
        ds, d = [], end
        for _ in range(n):
            ds.append(d)
            d = _prev_q(d)
        vals = [fin.get("Q", {}).get(x, {}).get(measure) for x in ds]
        if all(x is not None for x in vals):
            return sum(vals) / n, f"mean of {n} quarterly {measure} (CSV; approximates the period ratio)"
    return None, f"{measure} missing in CSV"


def it_actual(fin, measure, kind, end):
    """IT KPIs (v1.2). Company-reported ratios/amounts come from the --csv only: the FY row for FY/H claims
    (CC growth, attrition and utilisation are not averages of quarters), the Q row for quarters. For tcv_usd_mn
    over an FY/H the quarterly rows are summed. ebit_margin_pct falls back to screener (op profit - depreciation)/sales."""
    row = "Q" if kind == "Q" else "FY"
    v = fin.get(row, {}).get(end, {}).get(measure)
    if v is not None:
        return v, f"{measure} {row} (CSV, company-reported)"
    if measure in ("tcv_usd_mn",) and kind in ("FY", "H", "TTM"):
        t = _sum_q(fin, end, 2 if kind == "H" else 4, measure) if fin.get("Q") else None
        if t is not None:
            return t, f"sum of quarterly {measure} (CSV)"
    if measure == "ebit_margin_pct":
        s_, o, d = (period_value(fin, kind, end, f) for f in ("sales", "op_profit", "depreciation"))
        if s_ and o is not None and d is not None:
            return 100 * (o - d) / s_, f"(op {o:g} - dep {d:g}) / sales {s_:g} (screener-derived EBIT; company EBIT may differ)"
        return None, "sales/op_profit/depreciation missing"
    return None, f"{measure} missing in CSV (company-defined IT/US KPI: not on screener)"


def actual_for(fin, measure, kind, end):
    """-> (value, detail) or (None, reason)"""
    pv = lambda f, k=kind, e=end: period_value(fin, k, e, f)  # noqa: E731
    if measure in BANK_MEASURES:
        return bank_actual(fin, measure, kind, end)
    if measure in IT_MEASURES or measure in US_MEASURES:   # US (v1.3): CSV only, same lookup as the IT KPIs
        return it_actual(fin, measure, kind, end)
    try:
        if measure == "revenue_growth_yoy_pct":
            a, b = pv("sales"), pv("sales", kind, year_ago(end))
            return (100 * (a / b - 1), f"sales {a:g} vs {b:g}") if a and b else (None, "sales missing")
        if measure == "revenue_qoq_pct":
            a, b = pv("sales", "Q"), pv("sales", "Q", _prev_q(end))
            return (100 * (a / b - 1), f"sales {a:g} vs prior qtr {b:g}") if a and b else (None, "sales missing")
        if measure == "revenue_abs_cr":
            a = pv("sales")
            return (a, f"sales {a:g}") if a else (None, "sales missing")
        if measure in ("ebitda_margin_pct", "ebitda_margin_incl_oi_pct"):
            s, o = pv("sales"), pv("op_profit")
            if not s or o is None:
                return None, "sales/op_profit missing"
            oi = (pv("other_income") or 0) if measure == "ebitda_margin_incl_oi_pct" else 0
            return 100 * (o + oi) / s, f"(op {o:g}{' + oi %g' % oi if oi else ''}) / sales {s:g}"
        if measure == "pat_growth_yoy_pct":
            a, b = pv("net_profit"), pv("net_profit", kind, year_ago(end))
            return (100 * (a / b - 1), f"PAT {a:g} vs {b:g}") if a and b and b > 0 else (None, "PAT missing/neg base")
        if measure == "pat_abs_cr":
            a = pv("net_profit")
            return (a, f"PAT {a:g}") if a is not None else (None, "PAT missing")
        if measure == "finance_cost_pct_revenue":
            i, s = pv("interest"), pv("sales")
            return (100 * i / s, f"interest {i:g} / sales {s:g}") if i is not None and s else (None, "missing")
        if measure in ("debtor_days", "roce_pct", "fcf_cr", "dividend_payout_pct"):
            if kind != "FY":
                return None, f"{measure} only reported annually"
            fld = {"fcf_cr": "fcf"}.get(measure, measure)
            v = fin["FY"].get(end, {}).get(fld)
            return (v, f"screener {fld}") if v is not None else (None, f"{fld} missing")
        if measure == "borrowings_cr":
            v = fin["BS"].get(end, {}).get("borrowings")
            return (v, "screener borrowings") if v is not None else (None, "borrowings missing")
        if measure in ("capex_cr", "capex_pct_revenue"):
            if kind != "FY":
                return None, "capex derived only annually"
            given = fin["FY"].get(end, {}).get("capex")
            if given is not None:
                if measure == "capex_pct_revenue":
                    return 100 * given / pv("sales"), f"capex {given:g} (CSV) / sales"
                return given, "capex from CSV"
            b1, b0 = fin["BS"].get(end, {}), fin["BS"].get(year_ago(end), {})
            dep = fin["FY"].get(end, {}).get("depreciation")
            try:
                cap = (b1["fixed_assets"] + b1["cwip"]) - (b0["fixed_assets"] + b0["cwip"]) + dep
            except (KeyError, TypeError):
                return None, "balance sheet missing"
            if measure == "capex_pct_revenue":
                s = pv("sales")
                return 100 * cap / s, f"derived capex {cap:.0f} / sales {s:g} (dNet block+dCWIP+dep; includes acquisitions/leases)"
            return cap, "derived capex = dNet block + dCWIP + depreciation (includes leases/revaluation)"
    except (TypeError, ZeroDivisionError):
        return None, "arithmetic on missing data"
    return None, "measure not supported"


def judge(measure, actual, lo, hi, comp):
    """-> (status, gap, rule)"""
    lower_better = measure in LOWER_BETTER or comp == "<="
    tgt = (hi if hi is not None else lo) if lower_better else lo
    if comp in (">=", "<=") and tgt:
        # an explicit floor ('25% plus', 'at least') or ceiling ('below 4.5%'): strict, 2.5% relative band
        rel = (actual - tgt) / abs(tgt) * (-1 if lower_better else 1)
        st = "delivered" if rel >= -0.001 else "partly" if rel >= -0.025 else "missed"
        return st, round(rel, 3), "explicit floor/ceiling: delivered if met, partly within 2.5% relative"
    if measure in BANK_TIGHT and comp not in (">=", "<="):
        gap = actual - tgt if not lower_better else tgt - actual
        if comp == "range" and lo is not None and hi is not None and lo <= actual <= hi:
            gap = 0.0
        st = "delivered" if gap >= -0.05 else "partly" if gap >= -0.15 else "missed"
        return st, round(gap, 3), "bank ratio pp: delivered within 0.05pp (5 bps), partly within 0.15pp"
    if measure in GROWTH_MEASURES:
        gap = actual - tgt if not lower_better else tgt - actual
        td, tp = max(0.5, 0.05 * abs(tgt)), max(2.0, 0.20 * abs(tgt))
        st = "delivered" if gap >= -td else "partly" if gap >= -tp else "missed"
        return st, round(gap, 2), f"growth pp: delivered>=-{td:g}, partly>=-{tp:g}"
    if measure in PP_MEASURES or measure == "capex_pct_revenue":
        gap = actual - tgt if not lower_better else tgt - actual
        st = "delivered" if gap >= -0.3 else "partly" if gap >= -1.5 else "missed"
        return st, round(gap, 2), "level pp: delivered within 0.3pp, partly within 1.5pp"
    if not tgt:
        return None, None, "zero target"
    ratio = actual / tgt if not lower_better else tgt / actual if actual else 0
    st = "delivered" if ratio >= 0.95 else "partly" if ratio >= 0.80 else "missed"
    return st, round(ratio, 3), "ratio: delivered>=0.95, partly>=0.80"


def score_one(p, fin, as_of):
    measure, why = infer_measure(p)
    au = {"measure": measure, "measure_basis": why}
    if not measure:
        au["status"] = "not-auto-scorable"
        return au
    lo, hi = p.get("target_low"), p.get("target_high")
    unit, comp = p.get("unit"), p.get("comparator")
    parsed = parse_target(p.get("target"), us=is_us(p)) if p.get("target") else None
    if lo is None and hi is None and parsed:
        lo, hi, unit, comp = parsed
    elif parsed and not comp:
        comp = parsed[3]
    if lo is None and hi is None:
        au.update(status="not-auto-scorable", measure_basis=why + "; no numeric target")
        return au
    if measure.endswith("_pct") and unit and "%" not in str(unit):
        au.update(status="not-auto-scorable", measure_basis=why + f"; unit {unit} vs % measure")
        return au
    if measure.endswith("_cr") and unit and "%" in str(unit):
        if measure == "capex_cr":
            measure = au["measure"] = "capex_pct_revenue"
        elif measure == "revenue_abs_cr":
            measure = au["measure"] = "revenue_growth_yoy_pct"
        else:
            au.update(status="not-auto-scorable", measure_basis=why + "; % target on amount measure")
            return au
    has_capex = bool(fin) and any("capex" in r for r in fin.get("FY", {}).values())
    if measure in ("capex_cr", "capex_pct_revenue") and not DERIVED_CAPEX[0] and not has_capex:
        au.update(status="not-auto-scorable", measure_basis="capex: screener has no capex line (use --derived-capex or a CSV)")
        return au
    lo = hi if lo is None else lo
    hi = lo if hi is None else hi
    kind, end, label, notes = resolve_period(p, measure)
    per_q = measure == "revenue_abs_cr" and kind in ("H", "FY") and re.search(
        r"per quarter|/qtr|quarterly|run[\s-]?rate|a quarter", " ".join(str(p.get(k) or "") for k in ("metric", "target", "title")), re.I)
    au.update(period=label, period_end=end.isoformat(), target_used=[lo, hi], comparator=comp or "~", notes=notes)
    if end > as_of:
        au["status"] = "pending"
        # tracking: latest TTM / YTD reading where cheap
        if fin and fin.get("as_of") and measure in ("ebitda_margin_pct", "finance_cost_pct_revenue"):
            v, det = actual_for(fin, measure, "TTM", fin["as_of"])
            if v is not None:
                au["tracking"] = f"TTM to {fin['as_of']}: {v:.2f} ({det})"
        return au
    if not fin or not fin.get("as_of") or end > fin["as_of"]:
        au["status"] = "awaiting-data"
        return au
    v, det = actual_for(fin, measure, kind, end)
    if v is not None and per_q:
        nq = 2 if kind == "H" else 4
        v, det = v / nq, det + f" / {nq} quarters (per-quarter target)"
    if v is None:
        au.update(status="not-auto-scorable", measure_basis=why + f"; {det}")
        return au
    st, gap, rule = judge(measure, v, lo, hi, comp)
    au.update(actual=round(v, 2), actual_detail=det, gap=gap, rule=rule, status=st)
    if comp == "<=" and measure not in LOWER_BETTER and v > hi * 1.05 + 0.5:
        au["notes"].append("ceiling exceeded (comparator <=)")
    if measure in ("ebitda_margin_pct",) and re.search(r"incl|reported ebitda", str(p.get("metric")), re.I):
        au["notes"].append("company EBITDA may include other income; screener OPM excludes it")
    # late rule for level measures
    if st in ("missed", "partly") and (measure in PP_MEASURES or measure.endswith("_cr")) and kind in ("FY", "Q"):
        nq = C.quarter_end_of(end + dt.timedelta(days=5))
        if nq <= fin["as_of"] and nq <= as_of:
            v2, det2 = actual_for(fin, measure, "TTM" if kind == "FY" else "Q", nq)
            if v2 is not None and judge(measure, v2, lo, hi, comp)[0] == "delivered":
                au.update(status="partly", rule=rule + "; late rule: met one quarter later",
                          late_value=round(v2, 2))
    if measure == "capex_cr" or measure == "capex_pct_revenue":
        au["notes"].append("capex is DERIVED from balance sheet; check the cash-flow statement before relying on it")
        au["confidence"] = "low"
    return au


# ------------------------------------------------------------------ chains
STOP = {"of", "the", "a", "an", "and", "in", "to", "for", "by", "on", "vs", "yoy", "fy", "cr", "inr", "k", "t"}


def metric_tokens(p):
    s = re.sub(r"\(.*?\)", " ", str(p.get("metric") or "")).lower()
    return {w for w in re.findall(r"[a-z0-9\+]+", s) if w not in STOP and not re.fullmatch(r"fy\d+|q\d|h\d", w)}


def chain_key(p, au):
    if p.get("chain_key"):
        return p["chain_key"], "given"
    if au.get("measure") and au.get("period"):
        return f"{au['measure']}:{au['period']}", "measure+period"
    return None, None


ORDINALS = {"first", "second", "third", "fourth", "next", "another", "new", "further", "phase", "2nd", "3rd"}
FLOW_CATS = {"revenue_growth", "margin", "capex", "order_inflow", "order_book", "working_capital", "debt_reduction",
             "dividend_payout", "profit", "cash_flow", "returns"}


def _flow_period(p):
    """Per-period flows (revenue, inflow, margin...) chain only within one fiscal year: a new year's
    target is a new promise, not a re-date. Milestones (commissioning, launches, deals) chain across dates."""
    if p.get("category") not in FLOW_CATS:
        return None
    try:
        return f"FY{C.fy_of(dt.date.fromisoformat(str(p.get('deadline'))[:10])) % 100:02d}"
    except ValueError:
        return "vague"


def link_chains(promises):
    """Mutates promises: adds p['chain']. Same key -> earlier open promise is superseded/restated."""
    keyed = defaultdict(list)
    loose = []
    for p in promises:
        k, how = chain_key(p, p.get("auto", {}))
        if k:
            keyed[k].append(p)
        else:
            loose.append(p)
    # non-financial without key: cluster by category + metric-token Jaccard
    clusters = []
    for p in sorted(loose, key=lambda x: x["said_on"]):
        tk = metric_tokens(p)
        per = _flow_period(p)
        best = None
        for c in clusters:
            if c["cat"] != p.get("category") or c["per"] != per:
                continue
            if (tk & ORDINALS) != (c["tok"] & ORDINALS):
                continue  # 'second 75k block' is not the first one
            j = len(tk & c["tok"]) / max(1, len(tk | c["tok"]))
            if j >= 0.6 and (best is None or j > best[0]):
                best = (j, c)
        if best:
            best[1]["items"].append(p)
            best[1]["tok"] |= tk
        else:
            clusters.append({"cat": p.get("category"), "per": per, "tok": set(tk), "items": [p]})
    for i, c in enumerate(clusters):
        if len(c["items"]) > 1:
            keyed[f"{c['cat']}:{c['per'] or ''}:~{'-'.join(sorted(c['tok']))[:40]}"] = c["items"]
    for k, items in keyed.items():
        items.sort(key=lambda x: (x["said_on"], x["id"]))
        moves = 0
        for i, p in enumerate(items):
            ch = {"chain_key": k, "supersedes": None, "restates": None, "change": None, "goalpost_move": False}
            # most recent earlier promise in the chain still open when this one was made
            # the most recent earlier statement in the chain: still open at this date, or past its
            # deadline but never resolved by numbers (a silent re-date of e.g. a commissioning date)
            prev = None
            for q in reversed(items[:i]):
                if q["said_on"] >= p["said_on"]:
                    continue
                resolved = q.get("auto", {}).get("status") in ("delivered", "partly", "missed")
                if _open_at(q, p["said_on"]) or not resolved:
                    prev = q
                    break
            if prev:
                ch["supersedes"] = prev["id"]
                change = compare(prev, p)
                ch["change"] = change
                if change == "same":
                    ch["restates"], ch["supersedes"] = prev["id"], None
                elif any(x in change.split("+") for x in ("lowered", "deadline_pushed", "deadline_dropped")) \
                        and not p.get("acknowledges_revision"):
                    ch["goalpost_move"] = True
                    moves += 1
                    # every earlier promise in the chain still open at this date, with a higher target /
                    # earlier deadline, was quietly moved too (counted once per new statement)
                    for q in items[:i]:
                        if q is prev or (_open_at(q, p["said_on"]) and compare(q, p) != "same"
                                         and not compare(q, p).startswith(("raised", "deadline_pulled"))):
                            q.setdefault("superseded_by_goalpost", []).append(p["id"])
                elif change in ("lowered", "deadline_pushed", "lowered+deadline_pushed"):
                    prev.setdefault("withdrawn_by", []).append(p["id"])
            p["chain"] = ch
        for p in items:
            p["chain"]["n_goalpost_moves_in_chain"] = moves
            p["chain"]["chain_len"] = len(items)
    for p in promises:
        p.setdefault("chain", {"chain_key": None, "supersedes": None, "restates": None, "change": None,
                               "goalpost_move": False, "n_goalpost_moves_in_chain": 0, "chain_len": 1})


def _open_at(q, date):
    try:
        return q["said_on"] < date and dt.date.fromisoformat(str(q.get("deadline"))[:10]) >= dt.date.fromisoformat(date)
    except ValueError:
        return q["said_on"] < date


def _tgt(p):
    au = p.get("auto", {})
    if au.get("target_used"):
        return au["target_used"]
    lo, hi = p.get("target_low"), p.get("target_high")
    if lo is None and p.get("target"):
        t = parse_target(p["target"], us=is_us(p))
        if t:
            lo, hi = t[0], t[1]
    return [lo, hi] if lo is not None else None


def compare(a, b):
    ta, tb = _tgt(a), _tgt(b)
    da, db = str(a.get("deadline"))[:10], str(b.get("deadline"))[:10]
    meas = a.get("auto", {}).get("measure")
    lower_better = meas in LOWER_BETTER
    out = []
    # v1.1 (FEDERALBNK): for lower-is-better measures the binding number is the CEILING (cost-to-income
    # 52.5-53.5 -> 53-55 -> 53-56 is a lowered bar); v1 compared the floors and saw "same".
    ia = 1 if lower_better and ta and len(ta) > 1 and ta[1] is not None and tb and len(tb) > 1 and tb[1] is not None else 0
    if ta and tb and ta[ia] is not None and tb[ia] is not None:
        la, lb = ta[ia], tb[ia]
        tol = 0.02 if meas in BANK_TIGHT else 0.25 if meas in BANK_WIDE else max(0.5, 0.03 * abs(la))   # bank ratios: bps / 25 bps
        if (lb < la - tol and not lower_better) or (lb > la + tol and lower_better):
            out.append("lowered")
        elif (lb > la + tol and not lower_better) or (lb < la - tol and lower_better):
            out.append("raised")
    vague = "vague" in (str(a.get("deadline_precision")), str(b.get("deadline_precision")))
    if str(b.get("deadline_precision")) == "vague" and str(a.get("deadline_precision")) not in ("vague", "None", ""):
        out.append("deadline_dropped")   # v1.1: "36% in 3 years" -> "36% at some point" is a goalpost move
    if b.get("restates_earlier") and "lowered" not in out:
        return "same"  # speaker says 'maintained'; only a lower number overrides that
    try:
        dda, ddb = dt.date.fromisoformat(da), dt.date.fromisoformat(db)
        if vague:
            pass  # an open-ended aspiration restated later is not a re-date
        elif (ddb - dda).days > 45:
            out.append("deadline_pushed")
        elif (dda - ddb).days > 45:
            out.append("deadline_pulled")
    except ValueError:
        pass
    return "+".join(out) if out else "same"


def apply_chain_rule(p):
    """Pilot rule: a target revised before its deadline WITHOUT being called a revision is a
    moved goalpost, unless the original target was met anyway; an acknowledged cut = withdrawn."""
    st = p.get("auto", {}).get("status")
    final, basis = st, "numbers"
    if p.get("superseded_by_goalpost") and st in ("pending", "awaiting-data"):
        # v1.1 (FEDERALBNK): the original target is not due yet, so "not met" is unknown. Keep it pending,
        # flag the quiet revision, and resolve it at the ORIGINAL deadline against the ORIGINAL target.
        final, basis = st, "goalpost moved before deadline (provisional flag) by " + ", ".join(p["superseded_by_goalpost"][:3])
        p["goalpost_flag"] = True
    elif p.get("superseded_by_goalpost") and st != "delivered":
        final, basis = "moved-goalpost", "chain: quietly lowered/re-dated by " + ", ".join(p["superseded_by_goalpost"][:3])
    elif p.get("withdrawn_by") and st != "delivered":
        final, basis = "withdrawn", "chain: acknowledged revision " + ", ".join(p["withdrawn_by"][:3])
    p["auto_status_final"] = final
    p["auto_status_basis"] = basis


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--promises", help="JSONL from the LLM step")
    ap.add_argument("--seed", help="memdb seed JSON (pilot ledger) instead of --promises")
    ap.add_argument("--csv")
    ap.add_argument("--no-screener", action="store_true")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--as-of")
    ap.add_argument("--cache")
    ap.add_argument("--out")
    ap.add_argument("--derived-capex", action="store_true",
                    help="score capex promises from dNet block+dCWIP+depreciation (rough)")
    a = ap.parse_args(argv)
    DERIVED_CAPEX[0] = a.derived_capex
    sym = a.symbol.upper()
    root = C.cache_root(a.cache)
    as_of = dt.date.fromisoformat(a.as_of) if a.as_of else dt.date.today()
    if a.seed:
        promises = flatten_seed(a.seed)
    elif a.promises:
        promises = C.read_jsonl(a.promises)
    else:
        ap.error("--promises or --seed required")
    fin = None
    if not a.no_screener:
        page, _ = F.fetch_screener(sym, root, a.refresh)
        fin = F.parse_screener(page)
    if a.csv:
        fin = F.merge(fin or {"Q": {}, "FY": {}, "BS": {}, "TTM": {}}, F.load_csv(a.csv))
    for p in promises:
        p["auto"] = score_one(p, fin, as_of)
    link_chains(promises)
    for p in promises:
        apply_chain_rule(p)
    # 'stopped mentioning' suggestion (pilot lesson 5: >= 4 later calls without a restatement)
    man = C.load_json(os.path.join(C.sym_dir(root, sym), "manifest.json"), []) or []
    call_dates = sorted({m["call_date"] for m in man} | {p["said_on"] for p in promises})
    later_by_chain = defaultdict(list)
    for p in promises:
        later_by_chain[p["chain"]["chain_key"] or p["id"]].append(p["said_on"])
    for p in promises:
        if p["auto_status_final"] in ("delivered", "partly", "missed", "moved-goalpost", "withdrawn"):
            continue
        if (p.get("status") or "pending") != "pending" or int(p.get("materiality") or 2) < 2:
            continue  # already judged by a human/LLM, or minor
        last = max(later_by_chain[p["chain"]["chain_key"] or p["id"]])
        n_after = sum(1 for d in call_dates if d > last)
        if n_after >= 4:
            p["suggested_status"] = "silently-dropped?"
            p["suggestion_basis"] = f"not restated in the {n_after} calls after {last} (check: maybe hit, or immaterial)"
    out = a.out or os.path.join(C.sym_dir(root, sym), "scored.jsonl")
    C.write_jsonl(out, promises)
    from collections import Counter
    c = Counter(p["auto_status_final"] for p in promises)
    print(f"{sym}: {len(promises)} promises; auto statuses {dict(c)}; numbers as of {fin and fin.get('as_of')}")
    ch = [p for p in promises if p["chain"]["goalpost_move"]]
    print(f"goalpost moves detected: {len(ch)}; restatements: {sum(1 for p in promises if p['chain']['restates'])}")
    print("wrote", out)


if __name__ == "__main__":
    main()
