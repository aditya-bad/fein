"""Assemble memdb/seeds/2026-11-21_promises_TD_peers.json: KEC + KPIL promise/analysis records + one sector base-rate insight.
usage: python3 -I make_seed.py <skipper_summary.json> <out.json>
(skipper_summary.json = stdout of scripts_SKIPPER/build_seed.py; it is only read for the comparison numbers.)"""
import json, sys, os, statistics as st, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("tdb", os.path.join(HERE, "build_seed.py")); B = importlib.util.module_from_spec(sp); sp.loader.exec_module(B)
recs, sums = [], {}
for f in ("promises_KEC.py", "promises_KPIL.py"):
    r, s = B.build(B.load(os.path.join(HERE, f))); recs += r; sums[r[-1]["tickers"][0]] = s
sums["SKIPPER"] = json.load(open(sys.argv[1]))
MAP = {"order_book": "order_inflow"}
CATS = ["revenue_growth", "margin", "order_inflow", "debt_reduction", "working_capital", "capacity", "other"]
cat = {}
for t, s in sums.items():
    d = {}
    for c, v in s["by_category"].items():
        o = d.setdefault(MAP.get(c, c), [0, 0.0]); o[0] += v["n"]; o[1] += v["n"] * v["delivery_ratio_pct"]
    cat[t] = {c: (n, round(x / n, 1)) for c, (n, x) in d.items()}
adj = {}
for t in cat:
    tot = sum(cat[t].get(c, (0, 0))[0] for c in CATS); a = 0.0; rows = {}
    for c in CATS:
        if c not in cat[t]: continue
        ref = st.median([cat[o][c][1] for o in cat if o != t and c in cat[o]])
        rows[c] = round(cat[t][c][1] - ref, 1); a += cat[t][c][0] / tot * (cat[t][c][1] - ref)
    adj[t] = {"sector_adjusted_pts": round(a, 1), "by_category_vs_peer_median": rows}
head = {t: sums[t]["weighted_delivery_ratio_pct"] for t in sums}
data = {
    "as_of": "2026-11-21", "companies": ["SKIPPER", "KEC", "KPIL"],
    "weighted_delivery_ratio_pct": head,
    "specificity_weighted_delivery_ratio_pct": {t: sums[t]["specificity_weighted_delivery_ratio_pct"] for t in sums},
    "raw_hit_rate_pct": {t: sums[t]["raw_hit_rate_pct"] for t in sums},
    "mcs_schema_scale": {t: sums[t]["mcs_schema_scale"] for t in sums},
    "candour_index_pct": {t: sums[t]["candour_index_pct"] for t in sums},
    "n_scored": {t: sums[t]["n_scored"] for t in sums},
    "peer_median_weighted_delivery_pct": st.median(head.values()),
    "category_delivery_pct": {t: {c: cat[t][c][1] for c in CATS if c in cat[t]} for t in cat},
    "category_peer_median_pct": {c: st.median([cat[t][c][1] for t in cat if c in cat[t]]) for c in CATS},
    "sector_adjusted_credibility": adj,
    "metric_definition": "SAC = sum over categories c of (n_c / N) x (company delivery% in c - median delivery% in c of the OTHER peers); delivery% = specificity-weighted credit (delivered 1, partly 0.5). Positive = more credible than peers on the same kinds of promise.",
    "skipper_sensitivity": "Scoring Skipper's FY25 finance-cost miss (4.63% vs <4.5%) as partly under the ceiling rule moves its weighted delivery from 41.3% to 42.2%.",
    "caveats": "Three companies only; windows differ (Skipper Jul-24 to Oct-26, 10 calls; KEC Feb-25 to Nov-26, 8 calls; KPIL Feb-25 to Aug-26, 7 calls + Nov-26 deck). Skipper was read in full; KEC/KPIL read as full opening remarks + keyword-filtered management answers, so vague promises may be under-counted for the peers.",
}
body = (f"Same-method promise scores for three power T&D / EPC companies (Nov-2026): KPIL {head['KPIL']}% weighted delivery, SKIPPER {head['SKIPPER']}%, KEC {head['KEC']}%; "
        f"peer median {data['peer_median_weighted_delivery_pct']}%. Skipper's ~41% is therefore mid-pack, not low: about 7 points below the mean of the other two and slightly below on a sector-adjusted basis "
        f"({adj['SKIPPER']['sector_adjusted_pts']} pts; KEC {adj['KEC']['sector_adjusted_pts']}, KPIL {adj['KPIL']['sector_adjusted_pts']}). "
        "Sector-wide patterns: (1) FY26 domestic T&D order inflow fell short at all three (Skipper 87-95% of guide, citing CEA holding back bids, ROW and transformer shortages; KPIL India T&D ~7,000 -> 4,500 cr as awards slipped; KEC India T&D ~-11% vs +20% guided, worsened by a company-specific 15-month gap in PGCIL awards after a bribery inquiry raised by analysts); group-level inflow misses were partial (84-100%), not collapses. "
        "(2) Dates slip 1-2 quarters everywhere (capacity, plants, asset sales, receivable recoveries). (3) JJM water receivables broke every recovery promise made at KEC and KPIL. (4) Capex/commissioning is the weakest category for the sector (median ~36%). "
        "Company-specific: margins, debt and NWC (KEC near zero, KPIL ~100%), and group revenue (16% vs 80%). Volunteered opening-remark guidance delivered far better than Q&A numbers at KEC (48% vs 22%) and KPIL (91% vs 58%) but not at Skipper (39% vs 42%). "
        "Use: judge a T&D company's credibility relative to this peer table by category; a raw delivery ratio without a base rate misleads. n=3, so treat as provisional. Research, not advice.")
recs.append({"type": "insight", "id": "insight:td-epc-promise-credibility-base-rate",
             "title": "Base rate for management promise delivery in Indian power T&D / EPC (Skipper vs KEC vs KPIL, Nov 2026)",
             "body": body, "tickers": ["SKIPPER", "KEC", "KPIL"],
             "tags": ["india", "promise-tracker", "sector-power-td", "governance", "base-rate", "process", "td-peer-calibration"],
             "date": "2026-11-21", "data": data,
             "sources": sorted({u for r in recs if r["type"] == "analysis" for u in r["sources"]} | {"https://www.screener.in/company/SKIPPER/consolidated/"}),
             "confidence": "single-source",
             "links": [{"to": "analysis:SKIPPER:credibility-2026-11", "rel": "about"}, {"to": "analysis:KEC:credibility-2026-11", "rel": "about"},
                       {"to": "analysis:KPIL:credibility-2026-11", "rel": "about"}, {"to": "theme:sector-capital-goods-epc-td", "rel": "part_of"}]})
json.dump(recs, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
json.load(open(sys.argv[2]))
print(len(recs), "records;", json.dumps({"head": head, "adj": {t: adj[t]["sector_adjusted_pts"] for t in adj}}))
