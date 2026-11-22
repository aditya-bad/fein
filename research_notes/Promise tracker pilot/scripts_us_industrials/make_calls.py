"""Credibility-generated paper calls (US industrials, 2026-11-22; first US sector). Copied from scripts_it_peers/make_calls.py;
the rule is unchanged. The probability of every call is set ONLY by the pre-stated rule in us_summary.json ('adjustment_rule');
nothing here is a judgment probability.
  P(base) = p0 = leave-one-out peer strict delivery rate for the promise category
  P(ours) = clip(p0 + N/(N+20) * SAC/100, 0.05, 0.95)
Resolution: SEC XBRL (sec_fact, structured: revenue_growth_pct, op_margin_pct, capex) where the guided number is GAAP; 8-K Item
2.02 Exhibit 99 doc_scan (assisted) where it is company-adjusted (adjusted EPS, adjusted operating margin, organic growth).
usage: python3 -I make_calls.py <repo_root>   -> memdb/seeds/2026-11-22_paper_calls_credibility_us.json + merges tools/scoreboard/specs.json"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = sys.argv[1]
S = json.load(open(os.path.join(HERE, "us_summary.json")))
MADE = "2026-11-22"
SEC = "https://data.sec.gov/api/xbrl/companyfacts/CIK{}.json"
CIK = {"US-WTS": "0000795403", "US-AOS": "0000091142", "US-SSD": "0000920371", "US-LECO": "0000059527"}

def prob(T, c):
    b = S["base_rates_leave_one_out"][T][c]; p0 = b["p0_pct"] / 100; sac = S["sac"][T]
    p = min(0.95, max(0.05, p0 + sac["shrink_weight"] * sac["sac_pts"] / 100))
    return round(p, 2), round(p0, 2), b

def sec_spec(metric, op, thr, check_from, hi=None, rnd=1, note=""):
    s = {"type": "a", "auto": "structured", "kind": "sec_fact", "metric": metric, "period": "FY", "fy_end": "2026-12-31",
         "op": op, "threshold": thr, "check_from": check_from}
    if hi is not None: s["threshold_hi"] = hi
    if rnd is not None: s["round"] = rnd
    if note: s["note"] = note
    return s

def k8_spec(tk, phrases, op, thr, check_from, note, frm="2027-01-15"):
    return {"type": "a", "auto": "assisted", "kind": "doc_scan", "source": "sec", "ticker": tk, "forms": ["8-K"], "items": ["2.02"],
            "from": frm, "phrases": phrases, "op": op, "threshold": thr, "note": note, "check_from": check_from}

C = []  # (ticker, slug, category, promise_id, title, evidence, rule, source, resolve_by, spec)
def call(**k): C.append(k)

# ---------------- US-WTS (Watts Water; guidance raised at every call - the rule ignores in-year progress by design)
call(T="US-WTS", slug="fy26-reported-sales-growth-17pct-plus-cred", cat="revenue_growth", promise="promise:US-WTS:2026-11-05:fy26-reported-growth-17-18pct",
     title="Watts Water FY2026 reported net sales growth is >=17.0%",
     evidence="Q3-2026 call (05-Nov-2026): FY2026 reported sales growth guide 17-18% incl. ~$128-131 mn acquisition sales (raised from 8-12% in Feb, 14-17% in Aug). FY2025 net sales $2,438.5 mn (XBRL). 9M-2026 reported growth ~+20%.",
     rule="YES if FY2026 net sales / FY2025 net sales - 1 >= 17.0%, to one decimal, both from the FY2026 Form 10-K XBRL (revenue, as first reported; prior year = the comparative in the same filing).",
     source="SEC EDGAR XBRL companyfacts (FY2026 10-K)", by="2027-03-15",
     spec=sec_spec("revenue_growth_pct", ">=", 17.0, "2027-02-15"))
call(T="US-WTS", slug="fy26-adj-op-margin-20-3pct-plus-cred", cat="margin", promise="promise:US-WTS:2026-11-05:fy26-adj-op-margin-20-3-20-4",
     title="Watts Water FY2026 adjusted operating margin (company-reported) is >=20.3%",
     evidence="Q3-2026 call: FY2026 adjusted operating margin 20.3-20.4% (+70 to +80 bp; Aug guide 19.8-20.4%). FY2025 19.6%. Q1-Q3 2026 20.1% / 21.0% / 20.9%.",
     rule="YES if the FY2026 adjusted operating margin in Watts's Q4-2026 results release (8-K Item 2.02, Ex 99.1) is >= 20.3%, to one decimal. GAAP operating margin is NOT used.",
     source="Watts Q4-2026 8-K Ex 99.1 press release (SEC EDGAR)", by="2027-03-15",
     spec=k8_spec("WTS", [r"Full Year 2026 Highlights[\s\S]{0,500}?adjusted operating margin of (\d{2}\.\d) ?%", r"(?:full[- ]year|for the year)[^.]{0,120}?adjusted operating margin[^.]{0,40}?(\d{2}\.\d) ?%"],
                  ">=", 20.3, "2027-02-08", "assisted: company FY2026 adjusted operating margin >= 20.3% (first capture = full-year highlight bullet in the FY2025 release format)"))
call(T="US-WTS", slug="fy26-organic-growth-11pct-plus-cred", cat="revenue_growth", promise="promise:US-WTS:2026-11-05:fy26-organic-11-12pct",
     title="Watts Water FY2026 organic sales growth (company-reported) is >=11.0%",
     evidence="Q3-2026 call: 'We now anticipate organic sales growth of 11% to 12%' (Feb guide 2-6%, Aug 8-11%). Q1/Q2/Q3-2026 organic +12% / +12.2% / +12%; Q4 guide +9-12%. FY2025 +5%.",
     rule="YES if the FY2026 organic sales growth Watts reports in its Q4-2026 results release is >= 11.0% (company definition; whole-percent figures count as stated, e.g. '11%' = YES).",
     source="Watts Q4-2026 8-K Ex 99.1 press release (SEC EDGAR)", by="2027-03-15",
     spec=k8_spec("WTS", [r"Full Year 2026 Highlights[\s\S]{0,300}?and (\d{1,2}(?:\.\d)?) ?% organically", r"(?:full[- ]year|for the year)[^.]{0,120}?organic(?:ally| sales)[^.]{0,60}?(\d{1,2}(?:\.\d)?) ?%"],
                  ">=", 11.0, "2027-02-08", "assisted: company FY2026 organic growth >= 11.0%"))
# ---------------- US-AOS (A. O. Smith; China moved to discontinued operations in Q4-2026)
call(T="US-AOS", slug="fy26-adj-eps-ex-china-3-42-plus-cred", cat="other", promise="promise:US-AOS:2026-10-29:fy26-adj-eps-3-42-3-52-ex-china",
     title="A. O. Smith FY2026 adjusted EPS excluding China (continuing operations) is >=$3.42",
     evidence="Q3-2026 call / release (29-Oct-2026): 'Adjusted EPS, excluding China, of between $3.42 and $3.52' (the fourth FY2026 guide: $3.85-4.15 Jan, $3.70-4.00 Apr, $3.70-3.85 Jul, all incl. China). Excludes water-treatment restructuring.",
     rule="YES if A. O. Smith's FY2026 adjusted EPS from continuing operations (China excluded, as defined in its Q4-2026 release) is >= $3.42. If the company reports only a figure that includes China, the call goes to review (void if no ex-China figure is published by 2027-03-31).",
     source="A. O. Smith Q4-2026 8-K Ex 99.1 press release (SEC EDGAR)", by="2027-03-31",
     spec=k8_spec("AOS", [r"Adjusted earnings per share[^$\n]{0,40}\$(\d\.\d{2})", r"adjusted EPS[^.]{0,80}?\$(\d\.\d{2})"],
                  ">=", 3.42, "2027-01-26", "assisted: FY2026 adjusted EPS ex-China >= $3.42 (first capture = full-year table row in the Jan-2026 release format; CHECK it is continuing ops)"))
call(T="US-AOS", slug="fy26-sales-growth-ex-china-3-5pct-plus-cred", cat="revenue_growth", promise="promise:US-AOS:2026-10-29:fy26-sales-growth-4pct-ex-china",
     title="A. O. Smith FY2026 net sales growth, continuing operations (China excluded), is >=3.5% ('approximately 4%')",
     evidence="Q3-2026 release: 'Net sales growth, excluding China, of approximately 4%'; table: 2025 ex-China $3,155 mn, 2026 outlook $3,270-3,290 mn (+3.6% to +4.3%). Includes Leonard Valve (~$55 mn).",
     rule="YES if FY2026 net sales / FY2025 net sales - 1 >= 3.5% (one decimal), both from the FY2026 Form 10-K XBRL with China in discontinued operations (prior year = recast comparative in the same filing). If the 10-K comparative differs from ~$3,155 mn by more than 2% (China not excluded), the call goes to review and is resolved on the company's ex-China net sales.",
     source="SEC EDGAR XBRL companyfacts (FY2026 10-K)", by="2027-03-31",
     spec=sec_spec("revenue_growth_pct", ">=", 3.5, "2027-02-10", note="continuing operations; check the FY2025 comparative is ~3,155 mn (ex-China)"))
call(T="US-AOS", slug="china-sale-closes-by-jun27-cred", cat="other", promise="promise:US-AOS:2026-10-29:china-sale-close-h1-2027",
     title="A. O. Smith completes the sale of 81% of its China business to CPE by 30-Jun-2027",
     evidence="Q3-2026 call: 'We plan to close in the first half of 2027 subject to regulatory approvals and customary closing conditions' ($400 mn valuation for 81%; agreement 27-Oct-2026).",
     rule="YES if A. O. Smith announces (8-K Item 2.01 / press release / 10-Q) that the sale of the majority interest in its China business closed on or before 30-Jun-2027. NO if not closed by then (terminated or still pending).",
     source="A. O. Smith 8-K filings (SEC EDGAR); Q2-2027 results release", by="2027-07-31",
     spec={"type": "c", "auto": "assisted", "kind": "doc_scan", "source": "sec", "ticker": "AOS", "forms": ["8-K"], "from": MADE,
           "deadline": "2027-06-30", "phrases": [r"(?:completed|closed|completion of)[^.]{0,120}(?:China|CPE)", r"(?:China|CPE)[^.]{0,120}(?:has|have) (?:been )?(?:completed|closed)"],
           "note": "assisted: China divestiture closing on/before 30-Jun-2027", "check_from": "2027-01-15"})
# ---------------- US-SSD (Simpson; guides GAAP operating margin -> structured from XBRL)
call(T="US-SSD", slug="fy26-op-margin-20pct-plus-cred", cat="margin", promise="promise:US-SSD:2026-10-26:fy26-op-margin-20-0-20-5",
     title="Simpson FY2026 GAAP consolidated operating margin is >=20.0%",
     evidence="Q3-2026 call (26-Oct-2026): FY2026 operating margin 20.0-20.5% incl. an ~$11 mn Q4 land-sale gain (Feb guide 19.5-20.5%, Jul 19.7-20.5%). FY2025 19.6% (XBRL 458.1/2,330).",
     rule="YES if FY2026 OperatingIncomeLoss / revenue >= 20.0%, to one decimal, both from the FY2026 Form 10-K XBRL (as first reported).",
     source="SEC EDGAR XBRL companyfacts (FY2026 10-K)", by="2027-03-15",
     spec=sec_spec("op_margin_pct", ">=", 20.0, "2027-02-15"))
call(T="US-SSD", slug="fy26-capex-80-90mn-cred", cat="capacity", promise="promise:US-SSD:2026-10-26:fy26-capex-80-90mn",
     title="Simpson FY2026 capital expenditures are within $80-90 mn",
     evidence="Q2-2026 release and Q3-2026 call: capex $80-90 mn (Feb guide $75-85 mn). FY2025 $161.0 mn (Gallatin/Columbus build-out), outside its last range by 0.6%.",
     rule="YES if FY2026 PaymentsToAcquirePropertyPlantAndEquipment in the FY2026 Form 10-K XBRL is >= $80.0 mn and <= $90.0 mn.",
     source="SEC EDGAR XBRL companyfacts (FY2026 10-K)", by="2027-03-15",
     spec=sec_spec("capex", "between", 80.0e6, "2027-02-15", hi=90.0e6, rnd=None))
# ---------------- US-LECO (Lincoln Electric; guides in words: 'low teens percent')
call(T="US-LECO", slug="fy26-sales-growth-11pct-plus-cred", cat="revenue_growth", promise="promise:US-LECO:2026-10-27:fy26-sales-growth-low-teens",
     title="Lincoln Electric FY2026 net sales growth is >=11.0% ('low teens percent')",
     evidence="Q3-2026 call (27-Oct-2026): 'We now expect net sales growth to be in the low teens percent range for the full year' (Feb: mid single digit; Apr: high single digit). FY2025 net sales $4,233 mn. Q1/Q3-2026 +12% / +15.1%.",
     rule="YES if FY2026 net sales / FY2025 net sales - 1 >= 11.0%, to one decimal, from the FY2026 Form 10-K XBRL (as first reported; prior year = comparative in the same filing).",
     source="SEC EDGAR XBRL companyfacts (FY2026 10-K)", by="2027-03-15",
     spec=sec_spec("revenue_growth_pct", ">=", 11.0, "2027-02-20"))
call(T="US-LECO", slug="fy26-capex-140-150mn-cred", cat="capacity", promise="promise:US-LECO:2026-10-27:fy26-capex-140-150mn",
     title="Lincoln Electric FY2026 capital expenditures are within $140-150 mn",
     evidence="Q3-2026 call: capex $140-150 mn, raised from the Feb-2026 $110-130 mn. FY2025 $127.0 mn (XBRL). Q3-2026 capex $41.2 mn.",
     rule="YES if FY2026 capital expenditures in the FY2026 Form 10-K XBRL (PaymentsToAcquirePropertyPlantAndEquipment, else PaymentsToAcquireProductiveAssets) are >= $140.0 mn and <= $150.0 mn.",
     source="SEC EDGAR XBRL companyfacts (FY2026 10-K)", by="2027-03-15",
     spec=sec_spec("capex", "between", 140.0e6, "2027-02-20", hi=150.0e6, rnd=None))
call(T="US-LECO", slug="fy26-adj-op-margin-above-17-6-cred", cat="margin", promise="promise:US-LECO:2026-02-12:fy26-modest-margin-improvement",
     title="Lincoln Electric FY2026 adjusted operating income margin (company-reported) is >=17.7% (above FY2025's 17.6%)",
     evidence="Q4-2025 call (12-Feb-2026): 'a modest improvement in our operating margin for the full year'; reiterated Apr-2026. FY2025 adjusted operating income margin 17.6% (Q4-2025 release). Q1-2026 16.9%, Q3-2026 18.0%.",
     rule="YES if the FY2026 adjusted operating income margin in Lincoln's Q4-2026 results release (8-K Item 2.02, Ex 99.1) is >= 17.7%, to one decimal. GAAP operating margin is NOT used.",
     source="Lincoln Electric Q4-2026 8-K Ex 99.1 press release (SEC EDGAR)", by="2027-03-15",
     spec=k8_spec("LECO", [r"Full Year 2026 Highlights[\s\S]{0,500}?Adjusted operating income margin of (\d{2}\.\d) ?%"],
                  ">=", 17.7, "2027-02-10", "assisted: company FY2026 adjusted operating income margin >= 17.7% (Q4 release 'Full Year 2026 Highlights' bullet)"))

recs, specs = [], {}
for k in C:
    T = k["T"]; p, p0, b = prob(T, k["cat"]); sac = S["sac"][T]
    cid = f"thesis:paper-call:{T}:{k['slug']}"
    adj = f"p0 = {p0:.2f} (leave-one-out peer strict delivery rate, category '{k['cat']}'" + (", all-category fallback" if b.get("fallback_all") else "") + f", n={b['n']}); SAC {sac['sac_pts']:+} pts x weight {sac['shrink_weight']} (N={sac['n_scored']}) -> p = {p:.2f}"
    body = (f"Credibility-generated forward test (NOT a recommendation; not buy/sell). Probability {p:.2f} (naive sector base rate {p0:.2f}) that: {k['title'][len(T)+1:] if False else k['title']}. "
            f"Probability set only by the pre-stated rule (research_notes/Promise tracker pilot/US_INDUSTRIALS_peer_comparison.md section 5 = AUTO_COMPONENTS_peer_comparison.md section 5, unchanged): {adj}. "
            f"Evidence: {k['evidence']} Resolution: {k['rule']} Source: {k['source']}. Resolve by {k['by']}; score with Brier vs the base rate, to test whether the credibility adjustment adds skill.")
    recs.append({"type": "thesis", "id": cid, "title": "Paper call: " + k["title"], "body": body, "tickers": [T],
                 "tags": ["paper-call", "method-test", "credibility-generated", "promise-tracker", "us", "sector-us-industrials", "industrials", f"cat-{k['cat'].replace('_','-')}"],
                 "date": MADE, "status": "open",
                 "data": {"probability": p, "base_rate_probability": p0, "method": "promise-tracker credibility (sector-adjusted, rule-generated)",
                          "made_on": MADE, "resolve_by": k["by"], "resolution_rule": k["rule"], "resolution_source": k["source"],
                          "base_rate_reasoning": f"Naive forecaster = sector delivery rate for '{k['cat']}' promises among the other US industrials peers (strict: delivered only, specificity-weighted; n={b['n']}" + (", too few in category so all-category peer rate used" if b.get("fallback_all") else "") + "). No company-specific information.",
                          "adjustment_rule": S["adjustment_rule"], "adjustment_applied": adj,
                          "sector_adjusted_score": sac["sac_pts"], "sac_shrink_weight": sac["shrink_weight"], "sac_n_scored": sac["n_scored"],
                          "promise_category": k["cat"], "promise_id": k["promise"], "peer_set": S["companies"],
                          "outcome": None, "brier": None},
                 "sources": [SEC.format(CIK[T])],
                 "confidence": "single-source",
                 "links": [{"to": k["promise"], "rel": "tests"}, {"to": f"analysis:{T}:credibility-2026-11", "rel": "derived_from"},
                           {"to": "insight:us-industrials-promise-credibility-base-rate", "rel": "derived_from"}]})
    sp_ = dict(k["spec"])
    if sp_.get("kind") == "doc_scan" and "deadline" in sp_:   # the confirming document (next results call) arrives after the event date
        sp_["event_deadline"] = sp_["deadline"]; sp_["deadline"] = k["by"]
    specs[cid] = sp_
# transcript urls as sources
import importlib.util
for r in recs:
    T = r["tickers"][0]
    sp = importlib.util.spec_from_file_location("L", os.path.join(HERE, f"promises_{T}.py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    d = r["data"]["promise_id"].split(":")[2]
    if d in m.CALLS: r["sources"].insert(0, m.CALLS[d][1])
out = os.path.join(ROOT, "memdb/seeds/2026-11-22_paper_calls_credibility_us.json")
json.dump(recs, open(out, "w"), indent=1, ensure_ascii=False); json.load(open(out))
# append to specs.json keeping its one-entry-per-line layout (idempotent: entries already present are replaced in place)
sp_path = os.path.join(ROOT, "tools/scoreboard/specs.json"); txt = open(sp_path, encoding="utf-8").read(); have = json.loads(txt)
lines = txt.rstrip().rstrip("}").rstrip().split("\n")
lines = [l for l in lines if not any(l.lstrip().startswith(json.dumps(cid) + ":") for cid in specs)]
if lines[-1].endswith(","): lines[-1] = lines[-1][:-1]
lines[-1] += ","
new = [f" {json.dumps(cid)}: {json.dumps(v, ensure_ascii=False)}," for cid, v in specs.items()]
new[-1] = new[-1][:-1]
open(sp_path, "w", encoding="utf-8").write("\n".join(lines + new) + "\n}\n")
chk = json.load(open(sp_path, encoding="utf-8")); assert all(k in chk for k in have) and all(k in chk for k in specs)
for r in recs: print(f"{r['tickers'][0]:8} {r['data']['promise_category']:15} p={r['data']['probability']:.2f} base={r['data']['base_rate_probability']:.2f} {r['data']['resolve_by']} {r['id']}")
