#!/usr/bin/env python3
"""Resolve paper calls whose data now exists; queue the rest for a human. Never resolves early on partial data.

    python3 tools/scoreboard/resolve.py                  # nightly: fetch, decide, write seed + review queue
    python3 tools/scoreboard/resolve.py --dry-run        # decide and print; write nothing (except --report)
    python3 tools/scoreboard/resolve.py --dry-run --report research_notes/Scoreboard/dry_run.md --probe-past
    python3 tools/scoreboard/resolve.py --only BAJFINANCE --today 2027-05-20     # one call, replay a date
    python3 tools/scoreboard/resolve.py --offline        # no network: only human decisions + not-due checks

States per call:
  not_due        today < check_from (no network used)
  waiting_data   in the window but the data is not there yet / only one source so far (normal)
  review         a human must decide (type d, assisted proposals, sources disagree, near-threshold, overdue)
  resolved       outcome 1/0 decided from structured data, or a human decision in review_decisions.jsonl
Rules that keep it honest:
  * a number is only used when the filing for EXACTLY that period/basis exists (XBRL context dates must match);
  * India numbers need two sources (NSE XBRL + screener) on the same side of the threshold; a single source is
    used only at/after resolve_by and only if it is further than `guard` from the threshold;
  * prices: last close <= end date, read only after the end date has passed (and a later bar exists or 4 days passed);
  * events: YES only on a structured signal (8-K Item 1.03, Yahoo dividend >= amount); every NO and every
    text-derived number is a *proposal* that a human confirms;
  * type d always goes to the review queue.
Outputs (normal run): memdb/seeds/<today>_scoreboard_resolutions.json (only when something resolved; apply with
tools/scoreboard/apply.sh), research_notes/Scoreboard/review_queue.md + .jsonl, resolver_status.md,
tools/scoreboard/state/resolver_log.jsonl. Human decisions: research_notes/Scoreboard/review_decisions.jsonl,
one JSON object per line: {"id": "...", "outcome": 1|0|"void", "value": ..., "source": "URL", "source_date":
"YYYY-MM-DD", "note": "...", "decided_by": "user"}.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sb_common as C  # noqa: E402

DECISIONS = os.path.join(C.OUT_DIR, "review_decisions.jsonl")
PCT_TOL = 0.3      # two sources "agree" on a % metric if within 0.3 pp
AMT_TOL = 0.01     # ... on an amount if within 1%
MAX_DOCS = 25
WORDNUM = {w: i for i, w in enumerate("zero one two three four five six seven eight nine ten eleven twelve thirteen "
                                      "fourteen fifteen sixteen seventeen eighteen nineteen twenty".split())}


# ----------------------------------------------------------------- comparisons
def rnd(v, spec):
    return round(v, spec["round"]) if spec.get("round") is not None and v is not None else v


def compare(v, spec) -> int:
    t, op = spec["threshold"], spec["op"]
    v = rnd(v, spec)
    if op == ">=":
        return int(v >= t)
    if op == ">":
        return int(v > t)
    if op == "<=":
        return int(v <= t)
    if op == "<":
        return int(v < t)
    if op == "between":
        return int(t <= v <= spec["threshold_hi"])
    raise ValueError(f"unknown op {op}")


def distance(v, spec) -> float:
    v = rnd(v, spec)
    if spec["op"] == "between":
        return min(abs(v - spec["threshold"]), abs(v - spec["threshold_hi"]))
    return abs(v - spec["threshold"])


def is_pct(metric):
    return metric.endswith("_pct")


def ev(value, source, date, note="", name=""):
    return {"value": None if value is None else round(value, 4), "source": source, "date": date,
            "source_name": name, "note": note}


def result(state, reason="", outcome=None, value=None, evidence=None, proposal=None, confidence=None):
    return {"state": state, "reason": reason, "outcome": outcome, "value": value, "evidence": evidence or [],
            "proposal": proposal, "confidence": confidence}


def missing(call, today, what):
    if today > C.d(call["resolve_by"]):
        return result("review", f"OVERDUE: resolve_by {call['resolve_by']} passed and {what}; decide or void by hand")
    return result("waiting_data", what)


# ----------------------------------------------------------------- type a: India financials
def india_metric(src, symbol, basis, kind, end, metric, first_reported):
    """-> list of (source_name, value, evidence[]) for the metric, one per source that has the period."""
    out = []
    growth = metric.endswith("_growth_pct")
    base_field = {"sales_growth_pct": "sales_cr", "op_profit_growth_pct": "op_profit_cr"}.get(
        metric, metric[:-len("_growth_pct")] + "_cr" if growth else metric)   # e.g. nii_growth_pct -> nii_cr
    prior_end = dt.date(end.year - 1, end.month, end.day)
    for name in ("xbrl", "screener"):
        try:
            if name == "xbrl":
                cur = src.india_xbrl(symbol, basis, kind, end, first_reported)
                pri = src.india_xbrl(symbol, basis, kind, prior_end, first_reported) if growth else None
            else:
                cur = src.screener_values(symbol, basis, kind, end)
                pri = src.screener_values(symbol, basis, kind, prior_end) if growth else None
        except Exception as e:  # one source failing must not kill the other
            src.log(f"  {name} {symbol}: {type(e).__name__}: {e}")
            continue
        if not cur or cur.get(base_field) is None:
            continue
        evs = [ev(cur[base_field], cur["source"], cur.get("date"), f"{basis} {kind} ending {end}", cur["source_name"])]
        if growth:
            if not pri or not pri.get(base_field):
                continue
            v = 100 * (cur[base_field] / pri[base_field] - 1)
            evs.append(ev(pri[base_field], pri["source"], pri.get("date"), f"{basis} {kind} ending {prior_end}",
                          pri["source_name"]))
        else:
            v = cur[base_field]
        out.append((cur["source_name"], v, evs))
    return out


def eval_india_fin(call, spec, src, today):
    end = C.d(spec["end"])
    vals = india_metric(src, call["symbol"], spec["basis"], spec["period"], end, spec["metric"],
                        spec.get("first_reported", True))
    if not vals and spec.get("basis_fallback"):
        vals = india_metric(src, call["symbol"], spec["basis_fallback"], spec["period"], end, spec["metric"],
                            spec.get("first_reported", True))
    if not vals:
        return missing(call, today, f"no filing yet for {spec['basis']} {spec['period']} ending {end}")
    evidence = [e for _, _, es in vals for e in es]
    sides = {compare(v, spec) for _, v, _ in vals}
    guard = spec.get("guard", 0)
    near = any(distance(v, spec) <= guard for _, v, _ in vals)
    shown = "; ".join(f"{n}={rnd(v, spec) if spec.get('round') is not None else round(v, 2)}" for n, v, _ in vals)
    prop = {"outcome": compare(vals[0][1], spec), "value": round(vals[0][1], 4), "basis": vals[0][0]}
    if len(vals) >= 2:
        a, b = vals[0][1], vals[1][1]
        tol = PCT_TOL if is_pct(spec["metric"]) else AMT_TOL * max(abs(a), abs(b))
        if len(sides) > 1:
            return result("review", f"sources disagree on the outcome ({shown})", evidence=evidence, proposal=prop)
        if near and (spec.get("company_reported_governs") or abs(a - b) > tol):
            why = "company-reported figure governs" if spec.get("company_reported_governs") else "sources differ"
            return result("review", f"within guard {guard} of threshold and {why} ({shown})", evidence=evidence,
                          proposal=prop)
        o = sides.pop()
        return result("resolved", f"two sources agree ({shown})", o, round(a, 4), evidence, confidence="verified")
    # one source only
    if today < C.d(call["resolve_by"]):
        return result("waiting_data", f"one source so far ({shown}); waiting for the second until resolve_by",
                      evidence=evidence)
    if near or spec.get("company_reported_governs"):
        return result("review", f"single source at resolve_by and near threshold/company-governed ({shown})",
                      evidence=evidence, proposal=prop)
    o = sides.pop()
    return result("resolved", f"single source at resolve_by, beyond guard ({shown})", o, round(vals[0][1], 4),
                  evidence, confidence="single-source")


# ----------------------------------------------------------------- type a: NSE pledge
def eval_nse_pledge(call, spec, src, today):
    rows = src.nse_pledge_all()
    mine = [r for r in rows if (r.get("comName") or "").strip().lower() == spec["company_name"].lower()]
    url = "https://www.nseindia.in/api/corporate-pledgedata?index=equities"
    hit = [r for r in mine if (r.get("shp") or "").strip().lower() == spec["shp"].lower()]
    if hit:
        v = float(hit[0][spec["field"]])
        return result("resolved", f"{spec['field']}={v} for SHP {spec['shp']}", compare(v, spec), v,
                      [ev(v, url, hit[0].get("broadcastDt"), f"SHP {spec['shp']}", "NSE pledge data")],
                      confidence="verified")
    want = dt.datetime.strptime(spec["shp"], "%d-%b-%Y").date()
    later = [r["shp"] for r in mine if r.get("shp") and dt.datetime.strptime(r["shp"], "%d-%b-%Y").date() > want]
    if later:
        return result("review", f"NSE now shows SHP {later[0]} but never showed {spec['shp']}; check the SHP archive")
    return missing(call, today, f"NSE pledge data still shows {mine[0].get('shp') if mine else 'no row'}")


# ----------------------------------------------------------------- type a: SEC XBRL
SEC_TAGS = {
    "revenue": [("us-gaap", t, "USD") for t in ("RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                                                "SalesRevenueNet", "RevenueFromContractWithCustomerIncludingAssessedTax")],
    "nii": [("us-gaap", "InterestIncomeExpenseNet", "USD")],
    "eps_diluted": [("us-gaap", "EarningsPerShareDiluted", "USD/shares")],
    # 2026-11-22 (US industrials credibility calls): GAAP operating income and capex, plus op_margin_pct below
    "operating_income": [("us-gaap", "OperatingIncomeLoss", "USD")],
    "capex": [("us-gaap", t, "USD") for t in ("PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets")],
}
# ratio metrics (percent) built from two SEC_TAGS metrics for the same period, each fetched as first reported
SEC_RATIOS = {"op_margin_pct": ("operating_income", "revenue")}


def _dur(p):
    return (C.d(p["end"]) - C.d(p["start"])).days


def sec_value(facts, metric, period, fy_end):
    """-> (value, evidence list) from 10-K/10-Q XBRL, or None if the fiscal year's 10-K is not filed yet.
    period: FY | Q4 (FY minus 9-month YTD unless a 3-month Q4 fact is tagged) | FY_growth (pct).
    op_margin_pct = 100 x operating_income / revenue (both from the same rules; None unless both exist)."""
    if metric in SEC_RATIOS:
        num, den = SEC_RATIOS[metric]
        a, b = sec_value(facts, num, period, fy_end), sec_value(facts, den, period, fy_end)
        if not a or not b or not b[0]:
            return None
        return 100 * a[0] / b[0], a[1] + b[1]
    fy_end = C.d(fy_end)
    base = metric.replace("_growth_pct", "")
    for tax, tag, unit in SEC_TAGS[base]:
        try:
            pts = facts["facts"][tax][tag]["units"][unit]
        except KeyError:
            continue
        dur = [p for p in pts if "start" in p and p.get("form", "")[:4] in ("10-K", "10-Q")]
        annual = [p for p in dur if p["form"].startswith("10-K") and 350 <= _dur(p) <= 380
                  and abs((C.d(p["end"]) - fy_end).days) <= 10]
        # the 10-K for THIS fiscal year: filed after the year end
        annual = [p for p in annual if C.d(p["filed"]) > C.d(p["end"])]
        if not annual:
            continue
        a = sorted(annual, key=lambda p: p["filed"])[0]          # as first reported
        url = f"https://www.sec.gov/Archives/edgar/data/{facts.get('cik')}/{a['accn'].replace('-', '')}/"
        e_a = ev(a["val"], url, a["filed"], f"{tag} {a['start']}..{a['end']} ({a['form']} {a['accn']})", "SEC XBRL")
        if metric.endswith("_growth_pct"):
            prev_end = C.d(a["start"]) - dt.timedelta(days=1)
            prev = [p for p in dur if 350 <= _dur(p) <= 380 and abs((C.d(p["end"]) - prev_end).days) <= 10]
            same = [p for p in prev if p.get("accn") == a["accn"]] or sorted(prev, key=lambda p: p["filed"])[-1:]
            if not same:
                return None
            pv = same[0]
            e_p = ev(pv["val"], url, pv["filed"], f"{tag} {pv['start']}..{pv['end']} (comparative)", "SEC XBRL")
            return 100 * (a["val"] / pv["val"] - 1), [e_a, e_p]
        if period == "FY":
            return a["val"], [e_a]
        # Q4
        q4 = [p for p in dur if 80 <= _dur(p) <= 100 and p["end"] == a["end"] and p.get("accn") == a["accn"]]
        if q4:
            return q4[0]["val"], [ev(q4[0]["val"], url, q4[0]["filed"], f"{tag} 3-month {q4[0]['start']}..{q4[0]['end']}",
                                     "SEC XBRL")]
        nine = [p for p in dur if p["form"].startswith("10-Q") and 250 <= _dur(p) <= 290
                and abs((C.d(p["start"]) - C.d(a["start"])).days) <= 3]
        if not nine:
            return None
        n = sorted(nine, key=lambda p: p["filed"])[0]
        url9 = f"https://www.sec.gov/Archives/edgar/data/{facts.get('cik')}/{n['accn'].replace('-', '')}/"
        return a["val"] - n["val"], [e_a, ev(n["val"], url9, n["filed"], f"{tag} 9-month YTD {n['start']}..{n['end']} "
                                            f"({n['accn']}); Q4 = FY - 9M", "SEC XBRL")]
    return None


def eval_sec_fact(call, spec, src, today):
    facts = src.sec_facts(call["symbol"])
    got = sec_value(facts, spec["metric"], spec["period"], spec["fy_end"])
    if not got:
        return missing(call, today, f"10-K XBRL for fiscal year ending ~{spec['fy_end']} not filed yet")
    v, evidence = got
    return result("resolved", f"{spec['metric']}={rnd(v, spec)} (SEC XBRL)", compare(v, spec), v, evidence,
                  confidence="verified")


# ----------------------------------------------------------------- type b: relative return
def eval_price_relative(call, spec, src, today):
    start, end = C.d(spec["start"]), C.d(spec["end"])
    if today <= end:
        return result("not_due", f"window ends {end}")
    out = {}
    for key in ("symbol", "bench"):
        y = src.yahoo(spec[key], start, end + dt.timedelta(days=6))
        bars = y["bars"]
        s = [c for t, c in bars if t == start]
        e = [(t, c) for t, c in bars if t <= end]
        after = [t for t, _ in bars if t > end]
        if not s or not e:
            return missing(call, today, f"Yahoo has no close for {spec[key]} on {start} or before {end}")
        if (end - e[-1][0]).days > 6:   # stale series (feed gap / replayed date): never score on an old close
            return missing(call, today, f"latest {spec[key]} close is {e[-1][0]}, not near {end}")
        if not after and today < end + dt.timedelta(days=4):
            return result("waiting_data", f"waiting for a bar after {end} to make the {spec[key]} close final")
        out[key] = (s[0], e[-1], y)
    (s0, (t1, c1), ys), (b0, (u1, d1), yb) = out["symbol"], out["bench"]
    r_s, r_b = c1 / s0, d1 / b0
    evidence = [ev(s0, ys["url"], start.isoformat(), f"{spec['symbol']} close {start} (Yahoo, split-adjusted)", "Yahoo v8"),
                ev(c1, ys["url"], t1.isoformat(), f"{spec['symbol']} close {t1}", "Yahoo v8"),
                ev(b0, yb["url"], start.isoformat(), f"{spec['bench']} close {start}", "Yahoo v8"),
                ev(d1, yb["url"], u1.isoformat(), f"{spec['bench']} close {u1}", "Yahoo v8")]
    if (not ys["splits"] and abs(s0 / spec["base_px"] - 1) > 0.005) or abs(b0 / spec["bench_px"] - 1) > 0.005:
        return result("review", f"Yahoo start closes ({s0}, {b0}) differ >0.5% from the rule's ({spec['base_px']}, "
                      f"{spec['bench_px']}) with no split", evidence=evidence,
                      proposal={"outcome": int(r_s > r_b), "value": r_s / r_b - 1})
    note = f"; splits in window: {ys['splits']}" if ys["splits"] else ""
    return result("resolved", f"stock x{r_s:.4f} vs bench x{r_b:.4f}{note}", int(r_s > r_b), round(r_s / r_b - 1, 6),
                  evidence, confidence="verified")


# ----------------------------------------------------------------- type c: structured events
def eval_price_level(call, spec, src, today):
    """Absolute price-level calls on a Yahoo symbol (e.g. GC=F gold).
    mode "close_on": the last close on/before `end` is `op` `level` (resolves after `end` once a later bar exists).
    mode "touch":    any daily close in [start, end] is `op` `level` -> YES as soon as it happens; NO after `end`."""
    start, end = C.d(spec["start"]), C.d(spec["end"])
    op, level, mode = spec["op"], float(spec["level"]), spec["mode"]
    hit = (lambda c: c >= level) if op == ">=" else (lambda c: c <= level) if op == "<=" else \
          (lambda c: c > level) if op == ">" else (lambda c: c < level)
    upto = min(today, end + dt.timedelta(days=6))
    y = src.yahoo(spec["symbol"], start, upto, events="split")
    bars = [(t, c) for t, c in y["bars"] if start <= t]
    if mode == "touch":
        inwin = [(t, c) for t, c in bars if t <= end]
        first = next(((t, c) for t, c in inwin if hit(c)), None)
        if first:
            return result("resolved", f"{spec['symbol']} closed {first[1]:.2f} on {first[0]} ({op} {level})", 1, first[1],
                          evidence=[ev(first[1], y["url"], first[0].isoformat(), f"{spec['symbol']} close", "Yahoo v8")])
        if today <= end:
            return result("not_due", f"not touched yet; window ends {end}")
        if not inwin or (end - inwin[-1][0]).days > 6:
            return missing(call, today, f"Yahoo series for {spec['symbol']} incomplete up to {end}")
        return result("resolved", f"no close {op} {level} between {start} and {end}", 0, min(c for _, c in inwin) if op in ("<=", "<") else max(c for _, c in inwin))
    if today <= end:
        return result("not_due", f"window ends {end}")
    e = [(t, c) for t, c in bars if t <= end]
    after = [t for t, _ in bars if t > end]
    if not e or (end - e[-1][0]).days > 6:
        return missing(call, today, f"no {spec['symbol']} close near {end}")
    if not after and today < end + dt.timedelta(days=4):
        return result("waiting_data", f"waiting for a bar after {end}")
    t1, c1 = e[-1]
    return result("resolved", f"{spec['symbol']} close {c1:.2f} on {t1} vs {op} {level}", int(hit(c1)), c1,
                  evidence=[ev(c1, y["url"], t1.isoformat(), f"{spec['symbol']} close {t1}", "Yahoo v8")])


def eval_sec_8k_item(call, spec, src, today):
    frm, dl = C.d(spec["from"]), C.d(spec["deadline"])
    hits, late = [], []
    for cik in spec["ciks"]:
        for r in src.sec_filings(cik):
            if not r.get("form", "").startswith("8-K"):
                continue
            items = set((r.get("items") or "").split(","))
            if not items & set(spec["items"]):
                continue
            fd = C.d(r["filingDate"])
            url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{r['accessionNumber'].replace('-', '')}/{r.get('primaryDocument', '')}"
            if frm <= fd <= dl:
                hits.append(ev(None, url, r["filingDate"], f"8-K items {r.get('items')}", "SEC EDGAR"))
            elif dl < fd <= dl + dt.timedelta(days=7):
                late.append(ev(None, url, r["filingDate"], f"8-K items {r.get('items')} (filed after deadline)", "SEC EDGAR"))
    if hits:
        return result("resolved", f"8-K Item {'/'.join(spec['items'])} filed {hits[0]['date']}", 1, None, hits,
                      confidence="verified")
    if late:
        return result("review", "qualifying 8-K filed just after the deadline: check the petition date", evidence=late,
                      proposal={"outcome": None})
    if today > dl + dt.timedelta(days=5):
        return result("review", f"no 8-K Item {'/'.join(spec['items'])} by {dl}: confirm NO (check docket/claims agent)",
                      proposal={"outcome": 0})
    return result("waiting_data", f"no 8-K Item {'/'.join(spec['items'])} yet (window to {dl})")


def eval_yahoo_dividend(call, spec, src, today):
    frm, dl = C.d(spec["from"]), C.d(spec["deadline"])
    y = src.yahoo(spec["symbol"], frm, min(today, dl + dt.timedelta(days=75)), events="div")
    hits = [(t, a) for t, a in y["divs"] if frm <= t <= dl and a is not None and a >= spec["min_amount"] - 1e-9]
    if hits:
        t, a = hits[0]
        return result("resolved", f"dividend {a} ex {t} >= {spec['min_amount']} (declared before its ex-date)", 1, a,
                      [ev(a, y["url"], t.isoformat(), "Yahoo dividend event (ex-date)", "Yahoo v8")],
                      confidence="verified")
    if today > dl + dt.timedelta(days=75):
        later = [(t, a) for t, a in y["divs"] if t > dl and a >= spec["min_amount"] - 1e-9]
        why = (f"dividend {later[0][1]} ex {later[0][0]} after deadline: was it DECLARED by {dl}?" if later
               else f"no dividend >= {spec['min_amount']} through {dl}+75d")
        return result("review", why, proposal={"outcome": None if later else 0},
                      evidence=[ev(a, y["url"], t.isoformat(), "Yahoo dividend", "Yahoo v8") for t, a in later])
    last = y["divs"][-1] if y["divs"] else None
    return result("waiting_data", f"latest dividend seen {last}; need >= {spec['min_amount']}")


# ----------------------------------------------------------------- assisted: document scan
def _snips(text, phrases, k=3):
    out, nums = [], []
    flat = re.sub(r"[ \t\xa0]+", " ", text)
    for rx in phrases:
        for m in list(re.finditer(rx, flat, re.I))[:k]:
            a, b = max(0, m.start() - 120), min(len(flat), m.end() + 120)
            out.append(re.sub(r"\s+", " ", flat[a:b]).strip())
            g = [x for x in m.groups() if x] if m.groups() else []
            vals = []
            for x in g:
                try:
                    vals.append(float(x.replace(",", "")))
                except ValueError:
                    if x.lower() in WORDNUM:          # "increased four percent"
                        vals.append(float(WORDNUM[x.lower()]))
            if vals:
                nums.append(sum(vals) / len(vals))
    return out, nums


def gather_docs(spec, src, today):
    frm = C.d(spec.get("from") or spec.get("check_from"))
    docs = []
    if spec["source"] == "nse":
        for sym in [spec["symbol"]] + spec.get("extra_symbols", []):
            rows = src.nse_announcements(sym, frm, today)
            for r in rows:
                blob = " ".join(str(r.get(k) or "") for k in ("desc", "attchmntText", "attchmntFile"))
                if spec.get("subject") and not re.search(spec["subject"], blob, re.I):
                    continue
                if r.get("attchmntFile"):
                    docs.append({"url": r["attchmntFile"], "date": (r.get("sort_date") or r.get("an_dt") or "")[:10],
                                 "title": (r.get("desc") or "") + ": " + (r.get("attchmntText") or "")[:140]})
    else:
        for tk in [spec["ticker"]] + spec.get("extra_tickers", []):
            cik = src.sec_cik(tk)
            keep = []
            for r in src.sec_filings(cik):
                if r.get("form") not in spec.get("forms", ["8-K"]):
                    continue
                if not (frm <= C.d(r["filingDate"]) <= today):
                    continue
                if spec.get("items") and r.get("form", "").startswith("8-K") and \
                        not set((r.get("items") or "").split(",")) & set(spec["items"]):
                    continue
                keep.append(r)
            for r in sorted(keep, key=lambda r: r["filingDate"], reverse=True)[:12]:
                # exhibit names are arbitrary (e.g. livef8k3q26991.htm): keep every document except EDGAR's
                # index/XBRL viewer files; primary document first, at most 6 per filing
                names = [n for n, _ in src.sec_filing_docs(cik, r["accessionNumber"])]
                urls = dict(src.sec_filing_docs(cik, r["accessionNumber"]))
                keep_n = [n for n in names if n.lower().endswith((".htm", ".html", ".pdf"))
                          and not re.search(r"index|^R\d+\.htm$|FilingSummary", n, re.I)]
                keep_n.sort(key=lambda n: n != r.get("primaryDocument"))
                for name in keep_n[:6]:
                    docs.append({"url": urls[name], "date": r["filingDate"],
                                 "title": f"{tk} {r['form']} items={r.get('items') or '-'} {name}"})
    docs.sort(key=lambda x: x["date"], reverse=True)
    return docs[:MAX_DOCS]


def eval_doc_scan(call, spec, src, today):
    docs = gather_docs(spec, src, today)
    hits, nums = [], []
    for dct in docs:
        try:
            text = src.doc_text(dct["url"])
        except Exception as e:
            hits.append(ev(None, dct["url"], dct["date"], f"could not read: {e}", dct["title"]))
            continue
        sn, nn = _snips(text, spec.get("phrases", []))
        if sn:
            hits.append({**ev(None, dct["url"], dct["date"], " | ".join(sn[:3])[:900], dct["title"]),
                         "numbers": [round(x, 4) for x in nn[:6]]})
            nums += [(dct["date"], x) for x in nn]
    dl = C.d(spec.get("deadline") or call["resolve_by"])
    proposal = None
    if nums and "threshold" in spec:
        v = nums[0][1]
        proposal = {"outcome": compare(v, spec), "value": v,
                    "basis": "first number captured in the newest matching document - CHECK IT"}
    elif spec["type"] == "c" and "threshold" not in spec and hits:
        proposal = {"outcome": 1, "basis": "matching text found - confirm it meets the rule exactly"}
    if spec["type"] == "c" and today > dl and not [h for h in hits if C.d(h["date"][:10]) <= dl]:
        proposal = {"outcome": 0, "basis": f"no matching document on/before deadline {dl} - confirm NO"}
    tag = "judgment call" if spec["type"] == "d" else "assisted (human confirms)"
    if hits or today > dl or today >= C.d(call["resolve_by"]):
        return result("review", f"{tag}: {len(hits)} matching docs of {len(docs)} scanned", evidence=hits,
                      proposal=proposal)
    return result("waiting_data", f"{tag}: {len(docs)} docs scanned since {spec.get('from')}, no match yet")


EVAL = {"india_fin": eval_india_fin, "nse_pledge": eval_nse_pledge, "sec_fact": eval_sec_fact,
        "price_relative": eval_price_relative, "sec_8k_item": eval_sec_8k_item,
        "yahoo_dividend": eval_yahoo_dividend, "doc_scan": eval_doc_scan,
        "price_level": eval_price_level}


def evaluate(call, spec, src, today, offline=False):
    if call["status"] != "open":
        return result("skipped", f"status {call['status']}")
    if not spec:
        return result("review", "NO SPEC: add one to tools/scoreboard/specs.json (type " +
                      __import__("calls").classify(call["resolution_rule"], "", call["title"])[0] + ")")
    if today < C.d(spec.get("check_from") or call["resolve_by"]):
        return result("not_due", f"check from {spec.get('check_from')} (resolve by {call['resolve_by']})")
    if offline:
        return result("waiting_data", "offline run: data not checked")
    try:
        return EVAL[spec["kind"]](call, spec, src, today)
    except Exception as e:
        return result("waiting_data", f"fetch error (will retry): {type(e).__name__}: {e}"[:300])


# ----------------------------------------------------------------- human decisions + seeds
def load_decisions(path=DECISIONS):
    out = {}
    if not os.path.exists(path):
        return out
    for i, line in enumerate(C.read_text(path).splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            dcs = json.loads(line)
        except ValueError:
            print(f"review_decisions.jsonl line {i}: not JSON, ignored", file=sys.stderr)
            continue
        if dcs.get("outcome") not in (0, 1, "void"):
            print(f"review_decisions.jsonl line {i}: outcome must be 1, 0 or \"void\"", file=sys.stderr)
            continue
        if dcs["outcome"] in (0, 1) and not dcs.get("source"):
            print(f"review_decisions.jsonl line {i}: a 1/0 decision needs a source URL", file=sys.stderr)
            continue
        out[dcs["id"]] = dcs
    return out


def decision_result(dcs):
    e = [ev(dcs.get("value") if isinstance(dcs.get("value"), (int, float)) else None, dcs.get("source", ""),
            dcs.get("source_date", ""), dcs.get("note", ""), "human decision")]
    if dcs["outcome"] == "void":
        return result("void", dcs.get("note") or "void by human decision", None, dcs.get("value"), e)
    return result("resolved", "human decision: " + (dcs.get("note") or ""), dcs["outcome"], dcs.get("value"), e,
                  confidence=dcs.get("confidence", "verified"))


def seed_record(call, spec, res, today, by):
    data = {"resolved_on": today.isoformat(), "resolved_by": by, "evidence": res["evidence"],
            "resolution_type": (spec or {}).get("type"), "resolution_kind": (spec or {}).get("kind"),
            "resolution_reason": res["reason"], "resolution_value": res["value"],
            "resolution_confidence": res.get("confidence")}
    rec = {"type": "thesis", "id": call["id"], "title": "Paper call: " + call["title"],
           "sources": sorted({e["source"] for e in res["evidence"] if str(e.get("source", "")).startswith("http")})}
    if res["state"] == "void":
        rec.update(status="void", tags=["void"])
        data.update(void_reason=res["reason"])
    else:
        o = int(res["outcome"])
        rec.update(status="resolved", tags=["resolved"])
        data.update(outcome=o, **C.score_fields(call["probability"], call["base_rate_probability"], o))
    rec["data"] = data
    return rec


def write_seed(records, today, seeds_dir=C.SEEDS_DIR):
    path = os.path.join(seeds_dir, f"{today.isoformat()}_scoreboard_resolutions.json")
    old = C.read_json(path) if os.path.exists(path) else []
    have = {r["id"] for r in old}
    allr = old + [r for r in records if r["id"] not in have]
    C.write_json(path, allr)
    return path


# ----------------------------------------------------------------- reports
def queue_md(items, today):
    out = [f"# Review queue ({today})", "",
           "Calls a human must decide. For each, read the evidence, apply the WRITTEN rule strictly, then append one "
           "line to `research_notes/Scoreboard/review_decisions.jsonl`, e.g.", "",
           '`{"id": "thesis:paper-call:X:y", "outcome": 1, "value": 24.3, "source": "https://...", '
           '"source_date": "2027-02-05", "note": "Q3 press release p2", "decided_by": "user"}`', "",
           "Use `\"outcome\": \"void\"` only when the source no longer publishes the metric (scoring protocol). "
           "The next resolver run turns decisions into a memdb seed.", ""]
    if not items:
        out.append("_Queue empty._")
    for c, sp, r in items:
        out += [f"## `{c['id']}`", f"- **Type** {(sp or {}).get('type', '?')} / {(sp or {}).get('auto', 'no spec')} · "
                f"P(ours) {c['probability']} · P(base) {c['base_rate_probability']} · resolve by {c['resolve_by']}",
                f"- **Rule:** {c['resolution_rule']}", f"- **Why here:** {r['reason']}"]
        if (sp or {}).get("note"):
            out.append(f"- **Spec note:** {sp['note']}")
        if r.get("proposal"):
            out.append(f"- **Resolver proposal:** `{json.dumps(r['proposal'], ensure_ascii=False)}`")
        for e in r["evidence"][:8]:
            out.append(f"  - {e.get('date') or ''} [{e.get('source_name') or 'source'}]({e.get('source')}) "
                       f"{('value ' + str(e['value'])) if e.get('value') is not None else ''} {e.get('note') or ''}"[:1200])
        out.append("")
    return "\n".join(out) + "\n"


def status_md(rows, today):
    from collections import Counter
    cnt = Counter(r["state"] for _, _, r in rows)
    out = [f"# Resolver status ({today})", "", "Counts: " + ", ".join(f"{k} {v}" for k, v in sorted(cnt.items())), "",
           "| Call | Type | State | Check from | Resolve by | Reason |", "|---|---|---|---|---|---|"]
    for c, sp, r in sorted(rows, key=lambda x: ((x[1] or {}).get("check_from", ""), x[0]["id"])):
        out.append(f"| `{c['id'].replace('thesis:paper-call:', '')}` | {(sp or {}).get('type', '?')}/"
                   f"{(sp or {}).get('auto', '-')} | {r['state']} | {(sp or {}).get('check_from', '-')} | "
                   f"{c['resolve_by']} | {r['reason'].replace('|', '/')[:160]} |")
    return "\n".join(out) + "\n"


# ----------------------------------------------------------------- probe past periods (plumbing check)
def probe_past(calls, specs, src):
    """Run the structured type-a fetchers on the latest COMPLETED period (Q2 FY27 / FY26 / prior FY) to prove the
    data path works today. Prints values only; never decides a call."""
    lines = ["| Call | Probe period | Values by source |", "|---|---|---|"]
    for c in calls:
        sp = specs.get(c["id"]) or {}
        try:
            if sp.get("kind") == "india_fin":
                end = dt.date(2026, 9, 30) if sp["period"] == "Q" else dt.date(2026, 3, 31)
                vals = india_metric(src, c["symbol"], sp["basis"], sp["period"], end, sp["metric"], True)
                if not vals and sp.get("basis_fallback"):
                    vals = india_metric(src, c["symbol"], sp["basis_fallback"], sp["period"], end, sp["metric"], True)
                txt = "; ".join(f"{n} {sp['metric']}={v:.2f}" for n, v, _ in vals) or "NO DATA"
            elif sp.get("kind") == "sec_fact":
                fe = C.d(sp["fy_end"])
                fe = dt.date(fe.year - 1, fe.month, min(fe.day, 28))
                got = sec_value(src.sec_facts(c["symbol"]), sp["metric"], sp["period"], fe.isoformat())
                end = fe
                txt = f"SEC XBRL {sp['metric']}={got[0]:,.4g} ({got[1][0]['note']})" if got else "NO DATA"
            elif sp.get("kind") == "nse_pledge":
                rows = [r for r in src.nse_pledge_all() if (r.get("comName") or "").lower() == sp["company_name"].lower()]
                end = rows[0]["shp"] if rows else "-"
                txt = f"percTotShares={rows[0]['percTotShares'].strip()} (rule baseline 57.93)" if rows else "NO DATA"
            else:
                continue
        except Exception as e:
            end, txt = "-", f"ERROR {type(e).__name__}: {e}"[:200]
        lines.append(f"| `{c['id'].replace('thesis:paper-call:', '')}` | {end} | {txt} |")
        print(lines[-1])
    return "\n".join(lines) + "\n"


# ----------------------------------------------------------------- main
def run(calls, specs, src, today, decisions, offline=False, only=None, emitted=frozenset()):
    rows = []
    for c in calls:
        if only and only.upper() not in c["id"].upper():
            continue
        sp = specs.get(c["id"])
        if c["id"] in emitted:
            rows.append((c, sp, result("skipped", "already in a resolution seed (apply it)")))
            continue
        if c["status"] == "open" and c["id"] in decisions:
            rows.append((c, sp, decision_result(decisions[c["id"]])))
            continue
        r = evaluate(c, sp, src, today, offline)
        rows.append((c, sp, r))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="decide and print, write no seed/queue/status")
    ap.add_argument("--offline", action="store_true", help="no network")
    ap.add_argument("--today", help="replay as of YYYY-MM-DD (default: today IST)")
    ap.add_argument("--only", help="substring of call ids to run")
    ap.add_argument("--report", help="write a markdown run report here (works with --dry-run)")
    ap.add_argument("--probe-past", action="store_true", help="also fetch last completed period (plumbing check)")
    a = ap.parse_args(argv)
    today = C.d(a.today) if a.today else C.today()
    calls = C.load_calls(include_closed=True)
    specs = C.load_specs()
    import sources
    src = sources.Live(log=lambda m: print(m, file=sys.stderr))
    decisions = load_decisions()
    emitted = C.pending_seed_ids()
    rows = run(calls, specs, src, today, decisions, a.offline, a.only, emitted)

    resolved = [(c, sp, r) for c, sp, r in rows if r["state"] in ("resolved", "void")]
    queue = [(c, sp, r) for c, sp, r in rows if r["state"] == "review"]
    for c, sp, r in rows:
        if r["state"] not in ("not_due", "skipped"):
            print(f"{r['state']:13} {c['id']}: {r['reason'][:200]}")
    from collections import Counter
    print("states:", dict(Counter(r["state"] for _, _, r in rows)))

    if a.report:
        nd = sorted((sp or {}).get("check_from", "") for c, sp, r in rows if r["state"] == "not_due")
        rep = [f"# Resolver run {today} ({'dry run' if a.dry_run else 'live'})", "", status_md(rows, today)]
        rep += ["", queue_md(queue, today)]
        if a.probe_past:
            rep += ["", "## Plumbing probe: structured sources on the latest completed period", "",
                    "Values only; nothing is decided. Shows the data path works before the real periods arrive.", "",
                    probe_past([c for c, _, _ in rows if c["status"] == "open"], specs, src)]
        C.write_text(a.report, "\n".join(rep))
        print("report ->", a.report)
    if a.dry_run:
        print(f"dry run: {len(resolved)} would resolve, {len(queue)} would queue; nothing written")
        return rows

    by_auto = f"auto:{C.VERSION}"
    recs = [seed_record(c, sp, r, today, "human:" + decisions[c["id"]].get("decided_by", "user")
                        if c["id"] in decisions else by_auto) for c, sp, r in resolved]
    if recs:
        print(f"{len(recs)} resolutions -> {write_seed(recs, today)} (run tools/scoreboard/apply.sh)")
    C.write_text(os.path.join(C.OUT_DIR, "review_queue.md"), queue_md(queue, today))
    C.write_text(os.path.join(C.OUT_DIR, "review_queue.jsonl"), "".join(
        json.dumps({"id": c["id"], "reason": r["reason"], "proposal": r["proposal"], "evidence": r["evidence"]},
                   ensure_ascii=False) + "\n" for c, sp, r in queue))
    C.write_text(os.path.join(C.OUT_DIR, "resolver_status.md"), status_md(rows, today))
    os.makedirs(C.STATE_DIR, exist_ok=True)
    with open(os.path.join(C.STATE_DIR, "resolver_log.jsonl"), "a", encoding="utf-8") as f:
        for c, sp, r in rows:
            if r["state"] not in ("not_due", "skipped"):
                f.write(json.dumps({"run": today.isoformat(), "id": c["id"], **r}, ensure_ascii=False, default=str) + "\n")
    return rows


if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
