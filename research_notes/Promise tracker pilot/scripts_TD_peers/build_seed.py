"""Build memdb promise/analysis records for a T&D peer ledger (same scoring as scripts_SKIPPER/build_seed.py).
usage: python3 -I build_seed.py promises_KEC.py [promises_KPIL.py ...] --out records.json
Prints one summary JSON per ledger."""
import json, sys, os, datetime, importlib.util
AS_OF = datetime.date(2026, 11, 21)
SCORE = {"delivered": 1.0, "partly": 0.5, "missed": -1.0, "moved-goalpost": -1.5, "silently-dropped": -1.5, "withdrawn": -0.5}
CREDIT = {"delivered": 1.0, "partly": 0.5}
SPEC_W = {"precise": 3, "range": 2, "vague": 1}
CAT = {"capacity_commissioning": "capacity", "capex": "capacity", "customer_win": "other", "new_product": "other"}

def load(path):
    s = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def weight(p):
    q_age = (AS_OF - datetime.date.fromisoformat(p["said_on"])).days / 91.3
    return SPEC_W[p["specificity"]] * p.get("materiality", 2) * 0.5 ** (q_age / 8)

def fy(d):
    return "FY25 calls" if d < "2025-05-01" else ("FY26 calls" if d < "2026-05-01" else "FY27 calls")

def build(D):
    T = D.TICKER; aid = f"analysis:{T}:credibility-2026-11"
    recs, scored = [], []
    for p in D.P:
        doc, url = D.CALLS.get(p["said_on"], ("concall transcript", None))
        status = p.get("status", "pending")
        keys = ("said_on", "speaker", "quote", "category", "metric", "target", "deadline", "deadline_precision", "specificity",
                "volunteered", "materiality", "conditionality", "status", "evidence", "delivered_value", "delivery_ratio",
                "explanation_for_miss", "admitted_unprompted", "later_restatements", "check_after")
        data = {k: p[k] for k in keys if p.get(k) is not None}
        data.update(source_doc=doc, source_url=url, prompted=not p["volunteered"], status_as_of=AS_OF.isoformat(),
                    category_group=CAT.get(p["category"], p["category"]))
        if status in SCORE:
            data["score"] = SCORE[status]; data["weight"] = round(weight(p), 3); scored.append((p, data["weight"]))
        body = (f"{p['speaker']} on {p['said_on']} ({doc}): \"{p['quote']}\" Metric: {p['metric']}. Target: {p['target']}. "
                f"Deadline: {p['deadline']}. Specificity: {p['specificity']}; {'volunteered' if p['volunteered'] else 'prompted by analyst'}. "
                f"Status as of {AS_OF}: {status}. Evidence: {p.get('evidence', 'n/a')}"
                + (f" Explanation given: {p['explanation_for_miss']}" if p.get('explanation_for_miss') else ""))
        srcs = [u for u in [url] + p.get("extra_sources", []) if u]
        if status != "unverifiable":
            srcs.append(D.SCREENER)
        recs.append({"type": "promise", "id": f"promise:{T}:{p['said_on']}:{p['slug']}", "title": p["title"], "body": body,
                     "tickers": [T], "tags": ["india", "promise-tracker", "sector-power-td", "governance", "td-peer-calibration", p["category"].replace("_", "-")],
                     "date": p["said_on"], "data": data, "sources": sorted(set(srcs)), "confidence": p.get("confidence", "single-source"),
                     "links": [{"to": f"company:{T}", "rel": "about"}, {"to": aid, "rel": "part_of"}]})
    sw = sum(w for _, w in scored)
    mcs = sum(SCORE[p["status"]] * w for p, w in scored) / sw
    wdr = sum(CREDIT.get(p["status"], 0) * w for p, w in scored) / sw
    sw2 = sum(SPEC_W[p["specificity"]] for p, _ in scored)
    sdr = sum(CREDIT.get(p["status"], 0) * SPEC_W[p["specificity"]] for p, _ in scored) / sw2
    counts = {}
    for p in D.P:
        counts[p.get("status", "pending")] = counts.get(p.get("status", "pending"), 0) + 1
    misses = [p for p, _ in scored if p["status"] in ("missed", "moved-goalpost", "silently-dropped", "partly", "withdrawn")]
    hard = [p for p in misses if p["status"] != "partly"]
    def grp(keyf):
        out = {}
        for p, w in scored:
            o = out.setdefault(keyf(p), {"n": 0, "w": 0.0, "wc": 0.0})
            o["n"] += 1; o["w"] += SPEC_W[p["specificity"]]; o["wc"] += CREDIT.get(p["status"], 0) * SPEC_W[p["specificity"]]
        return {k: {"n": v["n"], "delivery_ratio_pct": round(100 * v["wc"] / v["w"], 1)} for k, v in sorted(out.items())}
    admitted = [p for p in misses if p.get("admitted_unprompted") is True]
    summary = {
        "as_of": AS_OF.isoformat(), "n_promises": len(D.P), "n_scored": len(scored), "status_counts": counts,
        "mcs_schema_scale": round(mcs, 3),
        "mcs_scale_note": "-1.5 (all moved/dropped) .. +1 (all delivered); weights = specificity(3/2/1) x materiality(1-3) x recency decay (half-life 8 qtrs)",
        "weighted_delivery_ratio_pct": round(100 * wdr, 1), "specificity_weighted_delivery_ratio_pct": round(100 * sdr, 1),
        "raw_hit_rate_pct": round(100 * sum(1 for p, _ in scored if p["status"] == "delivered") / len(scored), 1),
        "candour_index_pct": round(100 * len(admitted) / len(misses), 1) if misses else None,
        "candour_index_hard_misses_pct": round(100 * sum(1 for p in hard if p.get("admitted_unprompted") is True) / len(hard), 1) if hard else None,
        "by_category": grp(lambda p: CAT.get(p["category"], p["category"])),
        "by_specificity": grp(lambda p: p["specificity"]),
        "by_materiality": grp(lambda p: {3: "core (3)", 2: "meaningful (2)", 1: "minor (1)"}[p["materiality"]]),
        "by_volunteered": grp(lambda p: "volunteered" if p["volunteered"] else "prompted"),
        "by_fiscal_year_said": grp(lambda p: fy(p["said_on"])),
        "n_shortfalls": len(misses), "n_shortfalls_admitted_unprompted": len(admitted),
        "n_volunteered": sum(1 for p in D.P if p["volunteered"]), "n_prompted": sum(1 for p in D.P if not p["volunteered"]),
    }
    summary.update(getattr(D, "SUMMARY_EXTRA", {}))
    recs.append({"type": "analysis", "id": aid, "title": getattr(D, "ANALYSIS_TITLE", f"{T} - Management Credibility Score (T&D peer calibration, Nov 2026)"),
                 "body": D.ANALYSIS_BODY.format(**summary), "tickers": [T],
                 "tags": ["india", "promise-tracker", "sector-power-td", "governance", "process", "td-peer-calibration"],
                 "date": AS_OF.isoformat(), "data": summary,
                 "sources": sorted({u for _, u in D.CALLS.values()} | {D.SCREENER}), "confidence": "single-source",
                 "links": [{"to": f"company:{T}", "rel": "about"}, {"to": "analysis:SKIPPER:credibility-2026-11", "rel": "compares_to"}]})
    return recs, summary

if __name__ == "__main__":
    args = sys.argv[1:]; out = args[args.index("--out") + 1]; paths = [a for a in args if a.endswith(".py")]
    allrecs, sums = [], {}
    for path in paths:
        r, s = build(load(path)); allrecs += r; sums[r[-1]["tickers"][0]] = s
    json.dump(allrecs, open(out, "w"), indent=1, ensure_ascii=False); json.load(open(out))
    print(json.dumps(sums, indent=1))
