#!/usr/bin/env python3
"""Stage 5: credibility report + memdb seed JSON.

    python3 -I report.py SYMBOL --scored scored.jsonl [--as-of YYYY-MM-DD] [--status-source hybrid]
                         [--cache DIR] [--candour-auto] [--seed-out seed.json] [--md-out report.md]
                         [--json-out summary.json] [--company-tags sector-x,...]

Status used per promise (--status-source):
  hybrid (default): human_status > auto_status_final (when the numbers or a chain resolved it)
                    > status (LLM/manual) > pending
  auto:   auto_status_final only (non-auto promises count as pending)
  manual: status field only (reproduces a pilot ledger)
Formula (identical to both pilots):
  score   delivered +1, partly +0.5, missed -1, moved-goalpost -1.5, silently-dropped -1.5, withdrawn -0.5
  weight  specificity (precise 3 / range 2 / vague 1) x materiality (1-3) x 0.5 ** (quarters since said / 8)
  MCS     sum(w*score)/sum(w) over scored promises; scale -1.5 .. +1
  weighted delivery ratio = sum(w*credit)/sum(w), credit delivered 1, partly 0.5, else 0
  hit rate = delivered / scored;  candour index = shortfalls admitted unprompted / shortfalls
             (shortfall = partly, missed, moved-goalpost, silently-dropped, withdrawn)
--candour-auto: for shortfalls with no admitted_unprompted value, look in the management
  OPENING/CLOSING remarks of the first call after the deadline for a sentence that names the
  metric and a shortfall word (lower than expected, delay, miss, below, short of...). Heuristic;
  flagged as auto in the output.
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

SCORE = {"delivered": 1.0, "partly": 0.5, "missed": -1.0, "moved-goalpost": -1.5, "silently-dropped": -1.5,
         "withdrawn": -0.5}
CREDIT = {"delivered": 1.0, "partly": 0.5}
SPEC_W = {"precise": 3, "range": 2, "vague": 1}
SHORTFALL = {"partly", "missed", "moved-goalpost", "silently-dropped", "withdrawn"}
ALIASES = {"partially_delivered": "partly", "moved_goalpost": "moved-goalpost", "silent_drop": "silently-dropped",
           "silently_dropped": "silently-dropped", "open": "pending"}
EXEC_CATS = {"capacity_commissioning", "customer_win", "m&a", "new_product", "approval_regulatory"}
SHORT_WORDS = re.compile(r"lower than (expected|anticipated|guided)|below (our )?(expect|guid|target)|short of|"
                         r"\bmiss(ed)?\b|delay\w*|slipp\w*|could not|couldn't|did not (meet|achieve|reach)|"
                         r"unfortunately|disappoint\w*|not (been )?able to|fell short|shortfall|revis\w+ (down|our)|"
                         r"lower(ed)? (our )?guidance|cut (our )?guidance|not as (high|strong)|softer than", re.I)


def norm_status(s):
    s = (s or "pending").strip().lower()
    return ALIASES.get(s, s)


def pick_status(p, source):
    if source == "manual":
        return norm_status(p.get("manual_status") or p.get("status")), "manual"
    if p.get("human_status"):
        return norm_status(p["human_status"]), "human"
    auto = p.get("auto_status_final") or (p.get("auto") or {}).get("status")
    if auto in SCORE:
        return auto, "auto"
    if source == "auto":
        return "pending", "auto"
    return norm_status(p.get("status")), "llm/manual" if p.get("status") else "none"


def spec_of(p):
    s = p.get("specificity")
    if isinstance(s, str) and s in SPEC_W:
        return SPEC_W[s], s
    if isinstance(s, (int, float)):
        v = max(1, min(3, int(s)))
        return v, {3: "precise", 2: "range", 1: "vague"}[v]
    v = int(p.get("specificity_score") or 2)
    return v, {3: "precise", 2: "range", 1: "vague"}.get(v, "range")


def weight(p, as_of):
    q = (as_of - dt.date.fromisoformat(p["said_on"])).days / 91.3
    return spec_of(p)[0] * int(p.get("materiality") or 2) * 0.5 ** (q / 8)


def summarize(rows, as_of):
    sc = [r for r in rows if r["_status"] in SCORE]
    W = sum(r["_w"] for r in sc)
    out = {"n": len(rows), "n_scored": len(sc)}
    if W:
        out["mcs"] = round(sum(r["_w"] * SCORE[r["_status"]] for r in sc) / W, 3)
        out["weighted_delivery_ratio_pct"] = round(100 * sum(r["_w"] * CREDIT.get(r["_status"], 0) for r in sc) / W, 1)
        out["hit_rate_pct"] = round(100 * sum(r["_status"] == "delivered" for r in sc) / len(sc), 1)
    return out


def load_turns(root, sym):
    out = {}
    for f in glob.glob(os.path.join(root, sym, "turns", "*.json")):
        d = C.load_json(f)
        out[d["call_date"]] = d
    return dict(sorted(out.items()))


def candour_auto(p, turns_by_date):
    """True/False/None: did management raise the shortfall unprompted at the first call after the deadline?"""
    try:
        dl = dt.date.fromisoformat(str(p.get("deadline"))[:10])
    except ValueError:
        dl = dt.date.fromisoformat(p["said_on"]) + dt.timedelta(days=365)
    after = [d for d in turns_by_date if dt.date.fromisoformat(d) > dl]
    if not after:
        return None, "no later call"
    doc = turns_by_date[after[0]]
    words = [w for w in re.findall(r"[a-z]{4,}", (str(p.get("metric") or "") + " " + str(p.get("category") or "")).lower())
             if w not in {"consolidated", "growth", "revenue", "segment", "other", "year", "from", "with", "fiscal"}]
    words = words or re.findall(r"[a-z]{5,}", str(p.get("metric") or "").lower())
    for t in doc["turns"]:
        if t["role"] != "management" or t["section"] not in ("opening", "closing"):
            continue
        for s in re.split(r"(?<=[\.\?!])\s+", t["text"]):
            if SHORT_WORDS.search(s) and any(w in s.lower() for w in words[:6]):
                return True, f"{after[0]} opening: {s[:200]}"
    return False, f"not in {after[0]} opening/closing remarks"


def build(rows, sym, as_of, source):
    for r in rows:
        r["_status"], r["_status_src"] = pick_status(r, source)
        r["_w"] = weight(r, as_of)
    head = summarize(rows, as_of)
    counts = Counter(r["_status"] for r in rows)
    shortfalls = [r for r in rows if r["_status"] in SHORTFALL]
    adm = [r for r in shortfalls if r.get("_admitted") is True]
    known = [r for r in shortfalls if r.get("_admitted") is not None]
    head.update({
        "status_counts": dict(counts),
        "candour_index_pct": round(100 * len(adm) / len(shortfalls), 1) if shortfalls else None,
        "candour_known_n": len(known), "n_shortfalls": len(shortfalls),
        "goalpost_moves_counted": sum(1 for r in rows if (r.get("chain") or {}).get("goalpost_move")),
        "restatements": sum(1 for r in rows if (r.get("chain") or {}).get("restates")),
        "status_sources": dict(Counter(r["_status_src"] for r in rows if r["_status"] in SCORE)),
        "avg_delivery_ratio_auto": None,
    })
    drs = []
    for r in rows:
        au = r.get("auto") or {}
        if au.get("actual") is not None and au.get("target_used") and au.get("measure") and not au["measure"].endswith("qoq_pct"):
            t = au["target_used"][0]
            if t and t > 0 and not au["measure"] in ("finance_cost_pct_revenue", "debtor_days"):
                drs.append(au["actual"] / t)
    if drs:
        head["avg_delivery_ratio_auto"] = round(sum(drs) / len(drs), 2)
        head["avg_delivery_ratio_auto_n"] = len(drs)

    def grp(keyf):
        g = defaultdict(list)
        for r in rows:
            g[keyf(r)].append(r)
        return {k: summarize(v, as_of) for k, v in sorted(g.items(), key=lambda kv: str(kv[0]))}
    head["by_category"] = grp(lambda r: {"capex": "capacity/capex", "capacity_commissioning": "capacity/capex"}.get(
        r.get("category"), r.get("category") or "other"))
    head["by_driver"] = grp(lambda r: "execution/strategic" if r.get("category") in EXEC_CATS else "cycle/financial")
    head["by_specificity"] = grp(lambda r: spec_of(r)[1])
    head["by_volunteered"] = grp(lambda r: "volunteered" if r.get("volunteered") in (True, "volunteered") else "prompted")
    head["by_materiality"] = grp(lambda r: f"materiality {r.get('materiality') or 2}")
    head["by_fiscal_year_said"] = grp(lambda r: f"FY{C.fy_of(dt.date.fromisoformat(r['said_on'])) % 100:02d} calls")
    head["by_speaker"] = grp(lambda r: re.sub(r"\s*\(.*", "", str(r.get("speaker") or "?")))
    head.update(symbol=sym, as_of=as_of.isoformat(), status_source=source,
                formula="score: delivered +1, partly +0.5, missed -1, moved-goalpost -1.5, silently-dropped -1.5, "
                        "withdrawn -0.5; weight = specificity(3/2/1) x materiality(1-3) x 0.5^(quarters/8)")
    return head


def grade(mcs):
    if mcs is None:
        return "n/a"
    for cut, g in ((0.6, "A"), (0.4, "B+"), (0.2, "B"), (0.0, "C+"), (-0.2, "C-"), (-0.5, "D")):
        if mcs >= cut:
            return g
    return "F"


def seed_records(rows, sym, as_of, summary, tags):
    recs = []
    aid = f"analysis:{sym}:credibility-{as_of.strftime('%Y-%m')}"
    for r in rows:
        pid = r["id"] if str(r.get("id", "")).startswith("promise:") else \
            f"promise:{sym}:{r['said_on']}:{C.slugify(r.get('slug') or r.get('title') or r.get('metric') or 'x')}"
        data = {k: v for k, v in r.items() if not k.startswith("_") and k not in ("id", "title", "body")}
        data["status"] = r["_status"]
        data["status_source"] = r["_status_src"]
        data["status_as_of"] = as_of.isoformat()
        if r["_status"] in SCORE:
            data["score"] = SCORE[r["_status"]]
            data["weight"] = round(r["_w"], 3)
        ch = r.get("chain") or {}
        if ch.get("supersedes"):
            data["supersedes"] = ch["supersedes"]
        if ch.get("restates"):
            data["restates"] = ch["restates"]
        au = r.get("auto") or {}
        ev = r.get("evidence") or (f"auto: {au.get('measure')} {au.get('period')} actual {au.get('actual')} vs target "
                                   f"{au.get('target_used')} ({au.get('actual_detail')}); {au.get('rule')}"
                                   if au.get("actual") is not None else "")
        body = (f"{r.get('speaker')} on {r['said_on']} ({'volunteered' if r.get('volunteered') in (True, 'volunteered') else 'prompted'}): "
                f"\"{r.get('quote')}\" Metric: {r.get('metric')}. Target: {r.get('target') or au.get('target_used')}. "
                f"Deadline: {r.get('deadline')} ({r.get('deadline_precision')}). Status as of {as_of}: {r['_status']} "
                f"[{r['_status_src']}]. {ev}")
        links = [{"to": f"company:{sym}", "rel": "about"}, {"to": aid, "rel": "part_of"}]
        if ch.get("supersedes"):
            links.append({"to": ch["supersedes"], "rel": "supersedes"})
        if ch.get("restates"):
            links.append({"to": ch["restates"], "rel": "restates"})
        srcs = [u for u in [r.get("source_url")] if u]
        if au.get("actual") is not None:
            srcs.append(f"https://www.screener.in/company/{sym}/consolidated/")
        recs.append({"type": "promise", "id": pid, "title": r.get("title") or f"{r.get('metric')}: {r.get('target')}",
                     "body": body[:2000], "tickers": [sym],
                     "tags": ["india", "promise-tracker", "governance"] + tags + [str(r.get("category") or "other").replace("_", "-")],
                     "date": r["said_on"], "data": data, "sources": sorted(set(srcs)),
                     "confidence": r.get("confidence") or "single-source", "links": links})
    s = summary
    body = (f"Promise-tracker pipeline run for {sym} as of {as_of}: {s['n']} promises, {s['n_scored']} scored. "
            f"MCS {s.get('mcs')} (scale -1.5..+1; grade {grade(s.get('mcs'))}), weighted delivery ratio "
            f"{s.get('weighted_delivery_ratio_pct')}%, hit rate {s.get('hit_rate_pct')}%, candour index "
            f"{s.get('candour_index_pct')}% of {s['n_shortfalls']} shortfalls. Goalpost moves counted from "
            f"supersedes-chains: {s['goalpost_moves_counted']}. Status sources: {s['status_sources']}. "
            f"Auto-scored items use screener.in consolidated numbers; segment, order-book and timeline promises "
            f"need an LLM/human status. Research, not advice.")
    recs.append({"type": "analysis", "id": aid, "title": f"{sym}: management credibility score ({as_of})",
                 "body": body, "tickers": [sym], "tags": ["india", "promise-tracker", "governance", "process"] + tags,
                 "date": as_of.isoformat(), "data": s,
                 "sources": [f"https://www.screener.in/company/{sym}/consolidated/"],
                 "confidence": "single-source", "links": [{"to": f"company:{sym}", "rel": "about"}]})
    return recs


def markdown(s, rows):
    L = [f"# {s['symbol']} — management credibility ({s['as_of']})", "",
         "*Research, not SEBI-registered advice.*", "",
         "| Measure | Value |", "|---|---|",
         f"| Promises / scored | {s['n']} / {s['n_scored']} |",
         f"| Status counts | {', '.join(f'{k} {v}' for k, v in sorted(s['status_counts'].items()))} |",
         f"| **MCS** (−1.5..+1) | **{s.get('mcs')}** (grade {grade(s.get('mcs'))}) |",
         f"| Weighted delivery ratio | {s.get('weighted_delivery_ratio_pct')}% |",
         f"| Hit rate | {s.get('hit_rate_pct')}% |",
         f"| Candour index | {s.get('candour_index_pct')}% of {s['n_shortfalls']} shortfalls ({s['candour_known_n']} known) |",
         f"| Goalpost moves (chains) / restatements | {s['goalpost_moves_counted']} / {s['restatements']} |",
         f"| Status sources | {s['status_sources']} |", ""]
    for key, title in (("by_category", "Category"), ("by_driver", "Driver"), ("by_specificity", "Specificity"),
                       ("by_volunteered", "Volunteered vs prompted"), ("by_fiscal_year_said", "When said"),
                       ("by_speaker", "Speaker")):
        L += [f"## By {title.lower()}", "", f"| {title} | n | scored | MCS | weighted delivery | hit rate |",
              "|---|---|---|---|---|---|"]
        for k, v in s[key].items():
            L.append(f"| {k} | {v['n']} | {v['n_scored']} | {v.get('mcs', '')} | {v.get('weighted_delivery_ratio_pct', '')} | {v.get('hit_rate_pct', '')} |")
        L.append("")
    L += ["## Ledger", "", "| Said | Speaker | Metric | Target | Deadline | Status (source) | Chain |", "|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: r["said_on"]):
        ch = r.get("chain") or {}
        cs = ("goalpost move; " if ch.get("goalpost_move") else "") + (f"supersedes {ch['supersedes'].split(':')[-1]}" if ch.get("supersedes") else "") \
            + (f"restates {ch['restates'].split(':')[-1]}" if ch.get("restates") else "")
        L.append(f"| {r['said_on']} | {re.sub(r' *\\(.*', '', str(r.get('speaker')))} | {str(r.get('metric'))[:50]} | "
                 f"{str(r.get('target'))[:40]} | {str(r.get('deadline'))[:10]} | {r['_status']} ({r['_status_src']}) | {cs} |")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--scored", required=True)
    ap.add_argument("--as-of")
    ap.add_argument("--status-source", default="hybrid", choices=["hybrid", "auto", "manual"])
    ap.add_argument("--cache")
    ap.add_argument("--candour-auto", action="store_true")
    ap.add_argument("--seed-out")
    ap.add_argument("--md-out")
    ap.add_argument("--json-out")
    ap.add_argument("--company-tags", default="")
    a = ap.parse_args(argv)
    sym = a.symbol.upper()
    as_of = dt.date.fromisoformat(a.as_of) if a.as_of else dt.date.today()
    rows = C.read_jsonl(a.scored)
    turns = load_turns(C.cache_root(a.cache), sym) if a.candour_auto else {}
    for r in rows:
        r["_admitted"] = r.get("admitted_unprompted")
    s = build(rows, sym, as_of, a.status_source)
    if a.candour_auto:
        agree = []
        for r in rows:
            if r["_status"] in SHORTFALL:
                v, why = candour_auto(r, turns)
                r["admitted_unprompted_auto"] = v
                r["admitted_unprompted_auto_evidence"] = why
                if r.get("admitted_unprompted") is not None and v is not None:
                    agree.append(bool(r["admitted_unprompted"]) == v)
                if r["_admitted"] is None:
                    r["_admitted"] = v
        s = build(rows, sym, as_of, a.status_source)
        s["candour_auto_agreement_with_given"] = f"{sum(agree)}/{len(agree)}" if agree else None
        s["candour_index_auto_only_pct"] = round(100 * sum(1 for r in rows if r["_status"] in SHORTFALL and
                                                            r.get("admitted_unprompted_auto")) /
                                                 max(1, s["n_shortfalls"]), 1)
    s["grade"] = grade(s.get("mcs"))
    print(json.dumps({k: v for k, v in s.items() if not k.startswith("by_")}, indent=1, ensure_ascii=False))
    for k in ("by_driver", "by_category", "by_volunteered"):
        print(k, json.dumps({x: (y.get("mcs"), y["n_scored"]) for x, y in s[k].items()}))
    tags = [t for t in a.company_tags.split(",") if t]
    if a.seed_out:
        recs = seed_records(rows, sym, as_of, s, tags)
        C.save_json(a.seed_out, recs)
        json.load(open(a.seed_out))
        print("seed:", a.seed_out, len(recs), "records")
    if a.md_out:
        open(a.md_out, "w").write(markdown(s, rows))
        print("markdown:", a.md_out)
    if a.json_out:
        C.save_json(a.json_out, s)


if __name__ == "__main__":
    main()
