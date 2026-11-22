#!/usr/bin/env python3
"""Export paper calls from memdb into a normalised CSV, classify each resolution rule, write the calendar.

    python3 tools/scoreboard/calls.py                 # open calls -> research_notes/Scoreboard/calls.csv
    python3 tools/scoreboard/calls.py --all           # include resolved/void calls
    python3 tools/scoreboard/calls.py --print         # also print the table

Resolution TYPE (machine-checkability):
  a  reported number vs threshold (revenue, margin, NIM, EPS, order inflow...) - NSE XBRL/screener, SEC XBRL/8-K
  b  price / relative return vs a benchmark - Yahoo v8 chart closes
  c  corporate event (rating action, 8-K 1.03 bankruptcy, commissioning, deal closing, guidance raised/cut)
  d  needs human judgment (company-defined basis, "as the company counts it", "most popular plan")
Automation level: structured (resolver decides from structured data), assisted (resolver gathers documents and
proposes; a human confirms), human (judgment queue).

The TYPE in the CSV comes from tools/scoreboard/specs.json when the call has a spec (curated), else from the
text heuristic below (type_auto). Both are kept so disagreements are visible. Calls with no spec are listed as
"needs spec" and go to the review queue: add a spec before their check date.
Outputs: research_notes/Scoreboard/calls.csv, calendar.md, calendar.ics. Stage 7 (scorekeeping).
"""
from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sb_common as C  # noqa: E402

FIELDS = ["id", "ticker", "market", "method", "probability", "base_rate_probability", "made_on", "resolve_by",
          "check_from", "type", "type_auto", "automation", "spec_kind", "metric_type", "sector", "batch", "status",
          "resolution_rule", "resolution_source"]

# ---------------------------------------------------------------- heuristic classifier
JUDGMENT = [r"as (?:\w+ ){0,3}(?:itself )?counts it", r"most popular", r"same basis as the guidance",
            r"incl\. NGEL and JVs", r"as the company counts"]
PRICE = [r"close on [^÷]*÷", r"close [^÷]*÷", r"price return", r"beats? (?:the )?(?:SPY|Nifty|S&P)"]
EVENT = [("bankruptcy", r"chapter 11|bankrupt|insolvency|petition under"),
         ("rating", r"\b(?:downgrade|upgrade|rating action|credit rating)\b"),
         ("icfr", r"internal control over financial reporting|material weakness|\bICFR\b"),
         ("dividend", r"\bdividend\b"),
         ("buyback", r"repurchase|buy-?back"),
         ("regulatory", r"final order|approv(?:es|ing|al)\b.*(?:commission|merger|regulator)"),
         ("deal", r"\b(?:completion|closing|closes|completed)\b.*(?:acquisition|offer|deal)|binding|definitive agreement"),
         ("commissioning", r"commission(?:ed|ing)|commenced (?:commercial )?production|back online|production starts?"),
         ("tariff", r"tariff (?:increase|hike)|tariffs? under which"),
         ("guidance", r"guidance|outlook|\bguide\b")]
METRICS = [("opm", r"operating (?:profit )?margin|operating profit ÷ sales|opm|ebitda margin"),
           ("nim", r"net interest margin|\bnim\b"), ("nii", r"net interest income|\bnii\b"),
           ("gnpa", r"gross npa|gnpa"), ("credit_cost", r"credit cost"), ("combined_ratio", r"combined ratio"),
           ("aum", r"\baum\b"), ("vnb", r"\bvnb\b|value of new business"), ("bookings", r"booking"),
           ("order_inflow", r"order (?:inflow|intake)|inflow"), ("capacity", r"capacity|\bgw\b|\bmw\b"),
           ("volume", r"volume|total sales \("), ("comps", r"comparable sales|comps"),
           ("organic_growth", r"organic"), ("pledge", r"pledge|encumber"),
           ("procedure_growth", r"procedure"), ("eps", r"\beps\b|per share"),
           ("ebitda", r"ebitda"), ("op_profit", r"operating profit"),
           ("revenue", r"revenue|sales"), ("price", r"close")]


def metric_type(text: str) -> str:
    t = text.lower()
    for name, rx in METRICS:
        if re.search(rx, t):
            return name
    return "other"


def classify(rule: str, source: str = "", title: str = "") -> tuple[str, str]:
    """-> (TYPE a|b|c|d, subtype). Heuristic for calls without a curated spec."""
    text = " ".join([rule or "", title or ""])
    low = text.lower()
    for rx in JUDGMENT:
        if re.search(rx, low):
            return "d", "judgment:" + metric_type(text)
    for rx in PRICE:
        if re.search(rx, text, re.I):
            return "b", "relative-return"
    for name, rx in EVENT:
        if re.search(rx, low):
            # "guidance" words also appear in numeric rules ("midpoint of its guide"): an explicit
            # threshold on a REPORTED number stays type a
            if name == "guidance" and re.search(r"\breported\b|\bas reported\b", low) and \
                    not re.search(r"guidance (?:announced|range|in)|initial|outlook (?:first )?issued|raises", low):
                break
            return "c", name
    if re.search(r"[≥≤<>]|at least|or more|or better|within|(?:greater|less|higher|lower) than", text, re.I):
        return "a", metric_type(text)
    return "d", "unparsed"


def spec_metric(spec: dict, call: dict) -> str:
    if spec.get("metric"):
        return {"opm_pct": "opm", "op_profit_cr": "op_profit", "sales_cr": "revenue",
                "sales_growth_pct": "revenue_growth", "op_profit_growth_pct": "ebitda_growth",
                "revenue_growth_pct": "revenue_growth", "eps_diluted": "eps"}.get(spec["metric"], spec["metric"])
    if spec.get("kind") == "price_relative":
        return "relative_return"
    if spec.get("kind") == "nse_pledge":
        return "pledge"
    return metric_type(call["resolution_rule"] + " " + call["title"])


def build_rows(calls, specs):
    rows = []
    for c in calls:
        sp = specs.get(c["id"])
        ta, sub = classify(c["resolution_rule"], c["resolution_source"], c["title"])
        rows.append({
            "id": c["id"], "ticker": c["ticker"], "market": c["market"], "method": c["method"],
            "probability": c["probability"],
            "base_rate_probability": "" if c["base_rate_probability"] is None else c["base_rate_probability"],
            "made_on": c["made_on"], "resolve_by": c["resolve_by"],
            "check_from": (sp or {}).get("check_from", ""),
            "type": sp["type"] if sp else ta, "type_auto": f"{ta}:{sub}",
            "automation": sp.get("auto", "") if sp else "needs-spec",
            "spec_kind": sp.get("kind", "") if sp else "", "metric_type": spec_metric(sp, c) if sp else sub,
            "sector": c["sector"], "batch": c["batch"], "status": c["status"],
            "resolution_rule": c["resolution_rule"], "resolution_source": c["resolution_source"],
        })
    rows.sort(key=lambda r: (r["resolve_by"] or "9999", r["id"]))
    return rows


def write_csv(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def summary(rows) -> dict:
    by_type = collections.Counter(r["type"] for r in rows)
    by_auto = collections.Counter((r["type"], r["automation"]) for r in rows)
    mism = [r for r in rows if r["type_auto"].split(":")[0] != r["type"]]
    return {"n": len(rows), "by_type": dict(by_type), "by_type_auto": {f"{t}/{a}": n for (t, a), n in by_auto.items()},
            "heuristic_disagreements": [(r["id"], r["type"], r["type_auto"]) for r in mism],
            "needs_spec": [r["id"] for r in rows if r["automation"] == "needs-spec"]}


TYPE_NAMES = {"a": "reported number vs threshold", "b": "price / relative return",
              "c": "corporate event / guidance", "d": "human judgment"}


def calendar_md(rows, asof) -> str:
    out = [f"# Paper-call calendar (generated {asof} by tools/scoreboard/calls.py)", "",
           "Every open call's resolve-by date. `check from` = first day the nightly resolver looks for data "
           "(results/filings can arrive before the resolve-by date; events can happen any time in their window). "
           "Not recommendations.", "",
           "| Resolve by | Check from | Call id | Type | Automation | P(ours) | P(base) |", "|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['resolve_by']} | {r['check_from'] or '-'} | `{r['id']}` | {r['type']} | {r['automation']} | "
                   f"{r['probability']} | {r['base_rate_probability'] or '-'} |")
    months = collections.Counter((r["resolve_by"] or "")[:7] for r in rows)
    out += ["", "## Due per month", "", "| Month | Calls due |", "|---|---|"]
    out += [f"| {m} | {n} |" for m, n in sorted(months.items())]
    return "\n".join(out) + "\n"


def calendar_ics(rows, asof) -> str:
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//fein//paper-call scoreboard//EN", "CALSCALE:GREGORIAN"]
    for r in rows:
        if not r["resolve_by"]:
            continue
        day = r["resolve_by"].replace("-", "")
        nxt = (dt.date.fromisoformat(r["resolve_by"]) + dt.timedelta(days=1)).strftime("%Y%m%d")
        summ = f"Resolve paper call {r['ticker']} ({r['type']}/{r['automation']})"
        desc = (r["id"] + " | " + r["resolution_rule"])[:600].replace("\\", "\\\\").replace(",", "\\,") \
            .replace(";", "\\;").replace("\n", " ")
        lines += ["BEGIN:VEVENT", f"UID:{C.slug_uid(r['id'])}@fein-scoreboard", f"DTSTAMP:{stamp}",
                  f"DTSTART;VALUE=DATE:{day}", f"DTEND;VALUE=DATE:{nxt}", f"SUMMARY:{summ}",
                  f"DESCRIPTION:{desc}", "END:VEVENT"]
    lines.append("END:VCALENDAR")
    # RFC 5545 line folding at 75 octets
    out = []
    for ln in lines:
        b = ln.encode("utf-8")
        while len(b) > 75:
            cut = 75
            while (b[cut] & 0xC0) == 0x80:
                cut -= 1
            out.append(b[:cut].decode("utf-8"))
            b = b" " + b[cut:]
        out.append(b.decode("utf-8"))
    return "\r\n".join(out) + "\r\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true", help="include resolved/void calls")
    ap.add_argument("--out", default=os.path.join(C.OUT_DIR, "calls.csv"))
    ap.add_argument("--print", action="store_true")
    a = ap.parse_args(argv)
    calls = C.load_calls(include_closed=a.all)
    if not a.all:
        calls = [c for c in calls if c["status"] == "open"]
    specs = C.load_specs()
    rows = build_rows(calls, specs)
    write_csv(rows, a.out)
    asof = C.today().isoformat()
    open_rows = [r for r in rows if r["status"] == "open"]
    C.write_text(os.path.join(C.OUT_DIR, "calendar.md"), calendar_md(open_rows, asof))
    C.write_text(os.path.join(C.OUT_DIR, "calendar.ics"), calendar_ics(open_rows, asof))
    s = summary(rows)
    print(f"{s['n']} calls -> {a.out}")
    for t in "abcd":
        print(f"  type {t} ({TYPE_NAMES[t]}): {s['by_type'].get(t, 0)}")
    print("  by type/automation:", ", ".join(f"{k}={v}" for k, v in sorted(s["by_type_auto"].items())))
    if s["needs_spec"]:
        print(f"  NEEDS SPEC ({len(s['needs_spec'])}):", ", ".join(s["needs_spec"]))
    print(f"  heuristic vs curated type disagreements: {len(s['heuristic_disagreements'])}")
    for i, t, ta in s["heuristic_disagreements"]:
        print(f"    {i}: spec={t} heuristic={ta}")
    if a.print:
        for r in rows:
            print(f"{r['resolve_by']}  {r['check_from'] or '-':10}  {r['type']}/{r['automation']:10} {r['id']}")
    return rows


if __name__ == "__main__":
    main()
