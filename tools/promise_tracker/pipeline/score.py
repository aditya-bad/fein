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
LOWER_BETTER = {"finance_cost_pct_revenue", "debtor_days", "borrowings_cr"}
PP_MEASURES = {"ebitda_margin_pct", "ebitda_margin_incl_oi_pct", "finance_cost_pct_revenue", "roce_pct",
               "dividend_payout_pct"}
GROWTH_MEASURES = {"revenue_growth_yoy_pct", "revenue_qoq_pct", "pat_growth_yoy_pct"}
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


def parse_target(text):
    """'+25% (FY24 base ...)' -> (25, 25, '%', '>='?) ; '0% to -3%' -> (-3, 0, '%', 'range')."""
    if not text:
        return None
    t = str(text).replace("−", "-").replace("–", "-")
    head = re.split(r"\(|;|\bvs\b|\bfrom\b|\bon\b FY|\bbase\b", t)[0]
    comp = "~"
    if re.search(r"(^|\s)(>|>=|≥|at least|minimum|above|over|in excess|plus|\+$)|\d\s*%?\s*\+|%\s*plus|comfortably above", head, re.I):
        comp = ">="
    if re.search(r"(^|\s)(<|<=|≤|below|under|at most|max|less than|within)", head, re.I):
        comp = "<="
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
    if re.search(r"\b(mid[\s-]teens?)\b", head, re.I):
        return 14, 16, "%", "range"
    if re.search(r"\bflat\b|in line|~?\s*0\s*%", head, re.I):
        return 0, 0, "%", "~"
    return None


def infer_measure(p):
    if p.get("measure"):
        return p["measure"], "given"
    text = " ".join(str(p.get(k) or "") for k in ("metric", "target"))
    metric = str(p.get("metric") or "")
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
        if not DERIVED_CAPEX[0]:
            return None, "capex: screener has no capex line (use --derived-capex or a CSV)"
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


def actual_for(fin, measure, kind, end):
    """-> (value, detail) or (None, reason)"""
    pv = lambda f, k=kind, e=end: period_value(fin, k, e, f)  # noqa: E731
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
    parsed = parse_target(p.get("target")) if p.get("target") else None
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
    lo = hi if lo is None else lo
    hi = lo if hi is None else hi
    kind, end, label, notes = resolve_period(p, measure)
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
                elif change in ("lowered", "deadline_pushed", "lowered+deadline_pushed") \
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
        t = parse_target(p["target"])
        if t:
            lo, hi = t[0], t[1]
    return [lo, hi] if lo is not None else None


def compare(a, b):
    ta, tb = _tgt(a), _tgt(b)
    da, db = str(a.get("deadline"))[:10], str(b.get("deadline"))[:10]
    lower_better = (a.get("auto", {}).get("measure") in LOWER_BETTER)
    out = []
    if ta and tb and ta[0] is not None and tb[0] is not None:
        la, lb = ta[0], tb[0]
        tol = max(0.5, 0.03 * abs(la))
        if (lb < la - tol and not lower_better) or (lb > la + tol and lower_better):
            out.append("lowered")
        elif (lb > la + tol and not lower_better) or (lb < la - tol and lower_better):
            out.append("raised")
    try:
        dda, ddb = dt.date.fromisoformat(da), dt.date.fromisoformat(db)
        if (ddb - dda).days > 45:
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
    if p.get("superseded_by_goalpost") and st != "delivered":
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
