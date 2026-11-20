"""Build memdb seed JSON for the SKIPPER promise-tracker pilot.
usage: python3 -I build_seed.py <out.json> [--stage N]"""
import json, sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import promises_data as D

AS_OF = datetime.date(2026, 11, 19)
SCORE = {"delivered": 1.0, "partly": 0.5, "missed": -1.0, "moved-goalpost": -1.5,
         "silently-dropped": -1.5, "withdrawn": -0.5}
CREDIT = {"delivered": 1.0, "partly": 0.5}  # for plain weighted delivery ratio
SPEC_W = {"precise": 3, "range": 2, "vague": 1}


def call_meta(said_on):
    return D.CALLS.get(said_on, ("concall transcript", None))


def weight(p):
    d = datetime.date.fromisoformat(p["said_on"])
    q_age = (AS_OF - d).days / 91.3
    decay = 0.5 ** (q_age / 8)
    return SPEC_W[p["specificity"]] * p.get("materiality", 2) * decay


def main():
    out = sys.argv[1]
    recs, scored = [], []
    for p in D.P:
        if p.get("status") == "not-a-promise":
            continue
        doc, url = call_meta(p["said_on"])
        status = p.get("status", "pending")
        data = {k: p.get(k) for k in ("said_on", "speaker", "quote", "category", "metric", "target",
                                       "deadline", "deadline_precision", "specificity", "volunteered",
                                       "materiality", "conditionality", "status", "evidence", "delivered_value",
                                       "delivery_ratio", "explanation_for_miss", "admitted_unprompted",
                                       "later_restatements", "check_after")}
        data = {k: v for k, v in data.items() if v is not None}
        data["source_doc"] = doc
        data["source_url"] = url
        data["prompted"] = not p["volunteered"]
        data["status_as_of"] = AS_OF.isoformat()
        if status in SCORE:
            data["score"] = SCORE[status]
            data["weight"] = round(weight(p), 3)
            scored.append((p, data["weight"]))
        body = (f"{p['speaker']} on {p['said_on']} ({doc}): \"{p['quote']}\" "
                f"Metric: {p['metric']}. Target: {p['target']}. Deadline: {p['deadline']}. "
                f"Specificity: {p['specificity']}; {'volunteered' if p['volunteered'] else 'prompted by analyst'}. "
                f"Status as of {AS_OF}: {status}. Evidence: {p.get('evidence', 'n/a')}"
                + (f" Explanation given: {p['explanation_for_miss']}" if p.get('explanation_for_miss') else ""))
        srcs = [u for u in [url] + p.get("extra_sources", []) if u]
        if status in SCORE or status == "pending":
            srcs.append("https://www.screener.in/company/SKIPPER/consolidated/")
        recs.append({
            "type": "promise", "id": f"promise:SKIPPER:{p['said_on']}:{p['slug']}",
            "title": p["title"], "body": body, "tickers": ["SKIPPER"],
            "tags": ["india", "promise-tracker", "sector-power-td", "governance", p["category"].replace("_", "-")],
            "date": p["said_on"], "data": data, "sources": sorted(set(srcs)),
            "confidence": p.get("confidence", "single-source"),
            "links": [{"to": "company:SKIPPER", "rel": "about"},
                      {"to": "analysis:SKIPPER:credibility-2026-11", "rel": "part_of"}],
        })
    # ---- score
    sw = sum(w for _, w in scored)
    mcs = sum(SCORE[p["status"]] * w for p, w in scored) / sw if sw else None
    wdr = sum(CREDIT.get(p["status"], 0) * w for p, w in scored) / sw if sw else None
    # plain specificity-only weighted delivery ratio (no materiality, no decay)
    sw2 = sum(SPEC_W[p["specificity"]] for p, _ in scored)
    sdr = sum(CREDIT.get(p["status"], 0) * SPEC_W[p["specificity"]] for p, _ in scored) / sw2 if sw2 else None
    counts = {}
    for p in [q for q in D.P if q.get("status") != "not-a-promise"]:
        counts[p.get("status", "pending")] = counts.get(p.get("status", "pending"), 0) + 1
    misses = [p for p, _ in scored if p["status"] in ("missed", "moved-goalpost", "silently-dropped", "partly", "withdrawn")]
    hard = [p for p in misses if p["status"] != "partly"]
    def grp(keyf):
        out = {}
        for p, w in scored:
            k = keyf(p)
            o = out.setdefault(k, {"n": 0, "credit": 0.0, "w": 0.0, "wc": 0.0})
            o["n"] += 1; o["credit"] += CREDIT.get(p["status"], 0)
            o["w"] += SPEC_W[p["specificity"]]; o["wc"] += CREDIT.get(p["status"], 0) * SPEC_W[p["specificity"]]
        return {k: {"n": v["n"], "delivery_ratio_pct": round(100 * v["wc"] / v["w"], 1)} for k, v in sorted(out.items())}
    admitted = [p for p in misses if p.get("admitted_unprompted") is True]
    summary = {
        "as_of": AS_OF.isoformat(), "n_promises": sum(1 for q in D.P if q.get("status") != "not-a-promise"), "n_scored": len(scored), "status_counts": counts,
        "mcs_schema_scale": round(mcs, 3) if mcs is not None else None,
        "mcs_scale_note": "-1.5 (all moved/dropped) .. +1 (all delivered); weights = specificity(3/2/1) x materiality(1-3) x recency decay (half-life 8 qtrs)",
        "weighted_delivery_ratio_pct": round(100 * wdr, 1) if wdr is not None else None,
        "specificity_weighted_delivery_ratio_pct": round(100 * sdr, 1) if sdr is not None else None,
        "raw_hit_rate_pct": round(100 * sum(1 for p, _ in scored if p["status"] == "delivered") / len(scored), 1) if scored else None,
        "candour_index_pct": round(100 * len(admitted) / len(misses), 1) if misses else None,
        "candour_index_hard_misses_pct": round(100 * sum(1 for p in hard if p.get("admitted_unprompted") is True) / len(hard), 1) if hard else None,
        "by_category": grp(lambda p: {"capacity_commissioning": "capacity", "capex": "capacity"}.get(p["category"], p["category"])),
        "by_specificity": grp(lambda p: p["specificity"]),
        "by_materiality": grp(lambda p: {3: "core (3)", 2: "meaningful (2)", 1: "minor (1)"}[p["materiality"]]),
        "by_volunteered": grp(lambda p: "volunteered" if p["volunteered"] else "prompted"),
        "by_fiscal_year_said": grp(lambda p: "FY25 calls" if p["said_on"] < "2025-05-01" else ("FY26 calls" if p["said_on"] < "2026-05-01" else "FY27 calls")),
        "n_shortfalls": len(misses), "n_shortfalls_admitted_unprompted": len(admitted),
    }
    summary.update(getattr(D, "SUMMARY_EXTRA", {}))
    recs.append({
        "type": "analysis", "id": "analysis:SKIPPER:credibility-2026-11",
        "title": "Skipper Ltd - Management Credibility Score (promise tracker pilot, Nov 2026)",
        "body": getattr(D, "ANALYSIS_BODY", "stage build - body pending").format(**summary),
        "tickers": ["SKIPPER"], "tags": ["india", "promise-tracker", "sector-power-td", "governance", "process"],
        "date": AS_OF.isoformat(), "data": summary,
        "sources": sorted({call_meta(k)[1] for k in D.CALLS} | {"https://www.screener.in/company/SKIPPER/consolidated/"}),
        "confidence": "single-source",
        "links": [{"to": "company:SKIPPER", "rel": "about"}, {"to": "analysis:SKIPPER:2026-11-19", "rel": "about"}],
    })
    json.dump(recs, open(out, "w"), indent=1, ensure_ascii=False)
    json.load(open(out))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
