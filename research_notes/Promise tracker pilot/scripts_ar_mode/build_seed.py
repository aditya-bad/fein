"""Build memdb/seeds/2026-11-23_promises_ar_mode.json from the AR-mode pipeline seeds (ar_run.py output) plus
the hand reads (AR_mode_validation.md). Only records a human confirmed as company forward statements are kept;
hand-verified statuses go in `human_status` (report.py's hybrid rule lets them win). Run:
    python3 build_seed.py <AR cache root> <output json>
"""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, "/home/user/fein/tools/promise_tracker/pipeline")
import common as C  # noqa: E402
import report as RP  # noqa: E402

ARC, OUT = sys.argv[1], sys.argv[2]
AS_OF = dt.date(2026, 11, 23)
TAGS = ["india", "promise-tracker", "governance", "ar-mode", "no-concall"]

# pipeline promises a human confirmed (quote substring -> hand note / status)
KEEP = {
    "SUNFLAG": {
        "expansion at Blooming Mill": {"human_status": "partly", "hand": "AR FY23: 'during the year commissioned its Blooming mill' (by 31-Mar-2023) vs cold trial promised Q2 FY23; exact date not disclosed. AR FY24 and FY25 repeat the same 'commissioned during the year' sentence (stale text)."},
        "looking forward to acquire coal and iron ore mines": {"human_status": "delivered", "hand": "Surajpura phosphorite LOI 13-Feb-2026; Tambia South coal successful bidder 07-May-2026 (AR FY26). Restated in AR FY23, FY24, FY25."},
        "acquire coal, iron ore and other mines": {"human_status": "delivered", "hand": "Same evidence as the FY23/FY24 statements."},
        "Renew Green Energy": {"human_status": "delivered", "hand": "Status right, evidence sentence wrong: the pipeline matched the Sunsure SPV text; the real evidence is AR FY26 BRSR P6 (137.75 m kWh renewable power bought, 3x FY25, from the ReNew JV)."},
        "management remains confident": {"hand": "Vague; not scorable."},
        "EC and Stage I clearances are likely": {"hand": "The only dated mine promise (hand ledger section 5.4). Deadline end-Sep-2026 passed; no AR since; check NSE filings/Parivesh. Live call 4 (EC by 2027-09-30, P=0.35)."},
    },
    "GULFPETRO": {
        "has plans to venture into new territories": {"hand": "Vague; restated in AR FY25 (next record)."},
        "plans to venture into new territories": {"hand": "Vague restatement."},
        "These partnerships are expected to strengthen our market presence": {"hand": "Vague (Repsol distribution/export)."},
        "well-prepared plant is equipped to support its growth agenda": {"hand": "Capacity-sufficiency claim for 5 years; not checkable from ARs."},
        "going to be one of the key beneficiaries": {"hand": "Vague; hand item G7."},
        "aims to significantly enhance market coverage": {"hand": "Vague; hand item G5."},
        "We will continue to pursue growth that is sustainable": {"hand": "Boilerplate aspiration."},
        "significant milestones in the Company's diversification strategy": {"hand": "Vague (bitumen / infrastructure)."},
    },
    "REPRO": {
        "business acquisition is not expected to be impacted": {"hand": "COVID-era expectation; vague."},
        "aims to continue its growth trajectory": {"hand": "Vague."},
        "expecting to implement it soon": {"hand": "Solar project 'soon' (AR FY23); AR FY25 energy annexure still says 'Solar Project: Under review'. Hand view: missed/slipping, but 'soon' has no date."},
        "recertification of ISO14001-2015 at Surat facility in June 2023": {"hand": "Stale at filing: the June-2023 date had passed when the July-2023 report was filed."},
        "further expand its presence in the global market": {"hand": "Vague."},
        "aims to drive the future direction of the industry": {"hand": "Vague."},
        "new Bindwel planned to be installed": {"human_status": "partly", "hand": "Planned for April 2025 but still 'planned' in the July-2025 report (stale at filing); AR FY26 (filed 26-Oct-2026) reports the Bindwel binding capacity installed and commissioned during FY26. Late, delivered."},
        "guided by several key strategic priorities": {"hand": "Vague; hand item R4."},
        "expected to lead to greater financial resilience": {"hand": "Vague."},
        "expects to receive the renewed certification by the end of May 2026": {"hand": "Stale at filing (report filed 26-Oct-2026)."},
        "Rewari manufacturing facility is scheduled to undergo assessment": {"hand": "Checkable next year (Disney FAMA assessment)."},
        "optimising customer and channel acquisition frameworks": {"hand": "Vague."},
        "transforming online book buying": {"hand": "Vague."},
    },
}

# hand-read items the pipeline missed (one report each; AR_mode_validation.md section 3)
MISSED = {
    "GULFPETRO": ("2025-08-22", "ARFY25", [
        ("pcmo-launch-new-products", "the company is actively expanding its presence in the passenger car motor oil (PCMO) segment by aggressively launching new products to capitalize on the burgeoning opportunities in this market.",
         "new_product", "PCMO segment presence / new launches", "pending", "Vague. The identical sentence is repeated in AR FY26 (copied text).", "vague", 1),
        ("repsol-bangladesh-nepal", "The company is also exploring opportunities to expand this alliance into Bangladesh and Nepal through the appointment of exclusive distributors, anticipating substantial growth in these territories.",
         "customer_win", "Repsol alliance: exclusive distributors in Bangladesh and Nepal", "pending", "Not mentioned in AR FY26 (suggested: silently dropped?).", "vague", 2),
        ("lubricants-beyond-india", "In parallel, we are also exploring opportunities beyond Indian borders in the lubricants segment, seeking to expand our international footprint",
         "other", "International lubricant opportunities", "pending", "Not mentioned in AR FY26.", "vague", 1),
        ("amron-50pc-jv", "The Company has entered into a Share Purchase Agreement on June 07, 2025, to acquire 50% stake in Amron Oil Resources Private Limited (the Target Company) to form it as its JV Company in association with West Coast Oils LLP.",
         "m&a", "Acquire 50% of Amron Oil Resources (JV with West Coast Oils)", "delivered", "AR FY26: 50% stake acquired in June 2025; the JV commenced operations during FY 2025-26.", "precise", 2),
    ]),
    "REPRO": ("2025-07-22", "ARFY25", [
        ("content-monetisation-share-of-turnover", "It will continue to play an increasingly significant role in our overall turnover.",
         "revenue_growth", "Content monetisation share of turnover", "pending", "Vague; segment split not disclosed in the AR.", "vague", 2),
        ("content-monetisation-key-driver", "Moving forward, content monetisation will remain the key driver of growth, powered by technology, talent, and innovative ways of connecting books to readers.",
         "revenue_growth", "Content monetisation as growth driver", "pending", "Restated in AR FY26 ('the focus is on content monetisation').", "vague", 1),
        ("expand-sales-marketing-teams", "Hence expanding sales and marketing teams across different segments aim will be key in driving growth in the global and Indian book publishing markets.",
         "people", "Sales and marketing team expansion", "pending", "Vague.", "vague", 1),
        ("top5-online-book-seller", "The Company aims to position itself as the topnotch seller of Books online. ... Visibility of the e-commerce platform in the ranking of top 5 sellers for books online.",
         "other", "Rank among top-5 online book sellers (BRSR target)", "pending", "Not reported in AR FY26 BRSR.", "range", 2),
        ("data-analytics-phase1", "Phase-1 of data analytic platform in activation.",
         "new_product", "Phase 1 of the data analytics platform", "delivered", "AR FY26 BRSR: 'The first phase of its data analytics platform was operationalised'.", "range", 1),
        ("plant-assessment-corrective-actions", "The assessments for the plant locations are still on-going and corrective actions are in process at different stages. It is expected to be completed in the next year.",
         "other", "Plant assessment corrective actions (BRSR)", "pending", "Not checked.", "vague", 1),
    ]),
}


def slim(rec, sym, note):
    d = rec["data"]
    for k in ("evidence_trail", "context", "auto", "candidate_id"):
        d.pop(k, None)
    ch = d.get("chain") or {}
    d["chain"] = {k: ch.get(k) for k in ("chain_key", "supersedes", "restates", "change", "goalpost_move")}
    d["hand_review"] = note["hand"]
    d["review"] = "AR mode (ar_run.py) auto-extracted; confirmed as a company forward statement by a hand read on 2026-11-23"
    if note.get("human_status"):
        d["human_status"] = note["human_status"]
        d["status"] = note["human_status"]
        d["status_source"] = "human"
        if d["status"] in RP.SCORE:
            d["score"] = RP.SCORE[d["status"]]
            d["weight"] = round(RP.weight(d, AS_OF), 3)
    rec["tags"] = sorted(set(rec["tags"] + TAGS))
    rec["confidence"] = "single-source"
    rec["body"] = rec["body"][:1500] + f" Hand review: {note['hand']}"
    return rec


out = []
for sym, keep in KEEP.items():
    seed = json.load(open(os.path.join(ARC, sym, "out", f"{sym}_seed.json")))
    man = {m["call_date"]: m for m in C.load_json(os.path.join(ARC, sym, "manifest.json"))}
    used = set()
    for r in seed:
        if r["type"] != "promise":
            continue
        q = r["data"].get("quote") or ""
        hit = next((k for k in keep if k in q), None)
        if hit:
            out.append(slim(r, sym, keep[hit]))
            used.add(hit)
    missing = set(keep) - used
    if missing:
        raise SystemExit(f"{sym}: KEEP keys not found in pipeline seed: {missing}")
    if sym in MISSED:
        said, q_label, items = MISSED[sym]
        for slug, quote, cat, metric, status, ev, spec, mat in items:
            d = {"said_on": said, "speaker": f"{q_label} annual report (hand read)", "quote": quote, "category": cat,
                 "metric": metric, "target": metric, "deadline": C.fy_end(C.fy_of(dt.date.fromisoformat(said)) + 2).isoformat(),
                 "deadline_precision": "vague", "specificity": spec, "materiality": mat, "volunteered": True,
                 "status": status, "status_source": "human", "human_status": status, "evidence": ev,
                 "source_doc": f"{q_label} annual report", "source_url": man[said]["url"], "mode": "annual_report",
                 "review": "hand read 2026-11-23; missed by the AR-mode pipeline (recall miss)", "status_as_of": AS_OF.isoformat()}
            if status in RP.SCORE:
                d["score"] = RP.SCORE[status]
                d["weight"] = round(RP.weight(d, AS_OF), 3)
            out.append({"type": "promise", "id": f"promise:{sym}:{said}:{slug}", "title": f"{metric}"[:140],
                        "body": f"{q_label} annual report (filed {said}), hand read: \"{quote}\" Status as of {AS_OF}: {status}. {ev} "
                                f"Missed by the AR-mode pipeline. Research, not advice.",
                        "tickers": [sym], "tags": sorted(set(TAGS + [cat.replace('_', '-')])), "date": said, "data": d,
                        "sources": [man[said]["url"]], "confidence": "single-source",
                        "links": [{"to": f"company:{sym}", "rel": "about"},
                                  {"to": f"analysis:{sym}:credibility-ar-2026-11", "rel": "part_of"}]})
    # analysis record (hand-adjusted statuses), recomputed with report.py's formula
    rows = [dict(r["data"], id=r["id"]) for r in out if r["tickers"] == [sym] and r["type"] == "promise"]
    s = RP.build(rows, sym, AS_OF, "hybrid")
    s = {k: v for k, v in s.items() if not k.startswith("by_") or k in ("by_category",)}
    for r in out:
        if r["tickers"] == [sym]:
            r["links"] = [lk if lk["rel"] != "part_of" else {"to": f"analysis:{sym}:credibility-ar-2026-11", "rel": "part_of"}
                          for lk in r["links"]]
    out.append({"type": "analysis", "id": f"analysis:{sym}:credibility-ar-2026-11",
                "title": f"{sym}: management credibility from annual reports (AR mode, 2026-11-23)",
                "body": (f"AR-mode promise tracker (no earnings calls): last 5 annual reports, hand-confirmed records only. "
                         f"{s['n']} promises, {s['n_scored']} scored; MCS {s.get('mcs')} (scale -1.5..+1), weighted delivery "
                         f"{s.get('weighted_delivery_ratio_pct')}%, hit rate {s.get('hit_rate_pct')}%. Most annual-report "
                         f"statements are vague (no date, no number), so n is tiny and the score is NOT comparable with "
                         f"concall MCS. See research_notes/Promise tracker pilot/AR_mode_validation.md. Research, not advice."),
                "tickers": [sym], "tags": sorted(set(TAGS + ["process"])), "date": AS_OF.isoformat(),
                "data": dict(s, as_of=AS_OF.isoformat(), mode="annual_report", comparable_with_concall=False),
                "sources": [m["url"] for m in man.values()], "confidence": "single-source",
                "links": [{"to": f"company:{sym}", "rel": "about"}]})

out.append({"type": "insight", "id": "insight:promise-tracker-ar-mode-validation-2026-11",
            "title": "Promise tracker AR mode (no-concall companies): what annual reports can and cannot score (Nov 2026)",
            "body": ("Validated on SUNFLAG plus two seeded-random no-concall NSE small caps (GULFPETRO, REPRO). Annual reports "
                     "carry few checkable promises: hand reads found 7 (GULFPETRO FY25) and 8 (REPRO FY25) forward statements, "
                     "almost all undated; the pipeline recovered 3/7 and 2/8 at the promise stage (zone 5/7, 3/8). Auto-scored "
                     "n was 5 (SUNFLAG), 0, 0. The most useful AR-mode outputs are not the MCS but (1) the asset status tracker "
                     "(SUNFLAG: 17/17 hand-ledger mine-status cells reproduced; the unchanged Belgaon 5.391 MT reserve flagged) "
                     "and (2) disclosure-quality flags: stale forward dates at filing (REPRO x3), 'done during the year' text "
                     "repeated across years (SUNFLAG Blooming mill), identical sentences copied year to year. Treat AR-mode "
                     "MCS as non-comparable with concall MCS. Research, not advice."),
            "tickers": ["SUNFLAG", "GULFPETRO", "REPRO"], "tags": sorted(set(TAGS + ["process", "lesson"])),
            "date": AS_OF.isoformat(),
            "data": {"as_of": AS_OF.isoformat(), "recall_promise_stage": {"GULFPETRO": "3/7", "REPRO": "2/8"},
                     "recall_zone": {"GULFPETRO": "5/7", "REPRO": "3/8"}, "sunflag_ledger_cells": "17/17",
                     "precision_promise_stage": "28/48 (58%) hand-confirmed company forward statements"},
            "sources": ["research_notes/Promise tracker pilot/AR_mode_validation.md"], "confidence": "single-source",
            "links": [{"to": "company:SUNFLAG", "rel": "about"}, {"to": "company:GULFPETRO", "rel": "about"},
                      {"to": "company:REPRO", "rel": "about"}]})
json.dump(out, open(OUT, "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(OUT, len(out), Counter(r["type"] for r in out))
for r in out:
    if r["type"] == "analysis":
        print(r["id"], {k: r["data"].get(k) for k in ("n", "n_scored", "mcs", "weighted_delivery_ratio_pct", "hit_rate_pct", "status_counts")})
