"""Credibility-generated paper calls (auto components, 2026-11-22). The probability of every call is set ONLY by the
pre-stated rule in auto_summary.json ('adjustment_rule'); nothing here is a judgment probability.
  P(base) = p0 = leave-one-out peer strict delivery rate for the promise category
  P(ours) = clip(p0 + N/(N+20) * SAC/100, 0.05, 0.95)
usage: python3 -I make_calls.py <repo_root>   -> memdb/seeds/2026-11-22_paper_calls_credibility.json + merges tools/scoreboard/specs.json"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = sys.argv[1]
S = json.load(open(os.path.join(HERE, "auto_summary.json")))
MADE = "2026-11-22"
SCR = "https://www.screener.in/company/{}/consolidated/"

def prob(T, c):
    b = S["base_rates_leave_one_out"][T][c]; p0 = b["p0_pct"] / 100; sac = S["sac"][T]
    p = min(0.95, max(0.05, p0 + sac["shrink_weight"] * sac["sac_pts"] / 100))
    return round(p, 2), round(p0, 2), b

def fy_spec(metric, op, thr, guard, note=""):
    return {"type": "a", "auto": "structured", "kind": "india_fin", "metric": metric, "basis": "consolidated", "period": "FY",
            "end": "2027-03-31", "op": op, "threshold": thr, "round": 1, "guard": guard, "check_from": "2027-04-15",
            **({"note": note} if note else {})}

def doc_spec(sym, deadline, subject, phrases, note, check_from):
    return {"type": "c", "auto": "assisted", "kind": "doc_scan", "source": "nse", "symbol": sym, "from": MADE, "deadline": deadline,
            "subject": subject, "phrases": phrases, "note": note, "check_from": check_from}

C = []  # (ticker, slug, category, promise_id, title, evidence, rule, source, resolve_by, spec, sector_tag)
def call(**k): C.append(k)

# ---------------- UNIPARTS
call(T="UNIPARTS", slug="fy27-revenue-growth-24pct-cred", cat="revenue_growth", promise="promise:UNIPARTS:2026-11-05:fy27-revenue-24pct",
     title="Uniparts FY27 consolidated revenue growth is >=24.0% (latest guide ~INR 1,450 cr)",
     evidence="Q2FY27 call (05-Nov-2026): FY27 revenue ~INR 1,450 cr = +24% on INR 1,170 cr, raised from 'mid-teens' (Feb-26), 'in line with FY26 ~20-21%' (May-26), '~+23%' (Aug-26). Screener: FY26 1,171 cr; H1FY27 726 cr (+31.9%); needs H2 >= ~726 cr (+17% YoY).",
     rule="YES if FY27 consolidated revenue from operations / FY26 consolidated revenue from operations - 1 >= 24.0% (NSE XBRL and screener consolidated annual figures, to one decimal).",
     source="NSE integrated-filing XBRL (Q4 FY27 results) + screener.in consolidated P&L", by="2027-05-31",
     spec=fy_spec("sales_growth_pct", ">=", 24.0, 0.5))
call(T="UNIPARTS", slug="fy27-opm-above-20pct-cred", cat="margin", promise="promise:UNIPARTS:2026-05-26:fy27-ebitda-above-20",
     title="Uniparts FY27 consolidated operating margin is >20.0%",
     evidence="Q4FY26 call (26-May-2026): FY27 EBITDA 'above 20%'; Feb-26: '~20% through the cycle'. Screener OPM FY26 21.1% (247/1,171), H1FY27 22.7%, Q2FY27 21.9% (freight/tariff pressure flagged Nov-26).",
     rule="YES if FY27 consolidated Operating Profit / Sales (screener; NSE XBRL as second source) is > 20.0%, to one decimal.",
     source="screener.in consolidated P&L + NSE XBRL", by="2027-05-31",
     spec=fy_spec("opm_pct", ">", 20.0, 0.3))
# ---------------- SONACOMS
call(T="SONACOMS", slug="fy27-opm-23pct-plus-cred", cat="margin", promise="promise:SONACOMS:2026-04-30:fy27-margin-23-25-band",
     title="Sona BLW FY27 consolidated operating margin is >=23.0% (floor of its 23-25% band)",
     evidence="Q4FY26 call (30-Apr-2026): 'now it is 23 to 25% ... we should be able to continue being in that band'; Q2FY27 (26-Oct-2026) CFO: 'around 23%'. Company EBITDA margin FY26 24.7%, H1FY27 ~23%. Screener OPM FY26 24.3%, Q1/Q2 FY27 22.5%/22.5%; XBRL read ~0.5 pp higher than screener on Q2 (scoreboard known limit).",
     rule="YES if FY27 consolidated Operating Profit / Sales is >= 23.0% on both NSE XBRL and screener.in (to one decimal); if they straddle 23.0% the call goes to review and the company-reported FY27 EBITDA margin decides.",
     source="NSE XBRL + screener.in consolidated; Sona Q4 FY27 press release", by="2027-05-31",
     spec=fy_spec("opm_pct", ">=", 23.0, 0.3, "screener and XBRL differ ~0.5pp for Sona; straddle -> review, company EBITDA margin decides"))
call(T="SONACOMS", slug="jv1-denso-closed-by-jan27-cred", cat="other", promise="promise:SONACOMS:2026-10-26:jv1-denso-carveout-close-dec26",
     title="Sona BLW completes the JV1 (2W/3W carve-out with Denso) transaction by 31-Jan-2027",
     evidence="Q2FY27 call (26-Oct-2026), CFO: 'targeting to close this JV 1 ... by end of December ... possibility it may spill over to January'. JV announced 22-Jul-2026.",
     rule="YES if an NSE filing or the Q3 FY27 results/call states the JV1 transaction (business transfer / JV formation with Denso) was completed on or before 31-Jan-2027. Signed-but-not-closed, or completion after 31-Jan-2027 = NO.",
     source="NSE announcements (SONACOMS); Q3 FY27 earnings call transcript", by="2027-02-28",
     spec=doc_spec("SONACOMS", "2027-01-31", "Denso|joint venture|JV|completion|business transfer", ["(JV ?1|joint venture)[^.\\n]{0,200}(complet|consummat|closed|effective)"],
                   "event: JV1 completion on or before 31-Jan-2027; signing alone = NO", "2027-01-01"))
call(T="SONACOMS", slug="jv2-closed-by-jun27-cred", cat="other", promise="promise:SONACOMS:2026-10-26:jv2-close-h1-cy27",
     title="Sona BLW closes JV2 (high-voltage e-powertrain JV with Denso) by 30-Jun-2027",
     evidence="Q2FY27 call (26-Oct-2026): 'JV2 has not yet formed up but we are targeting to close and have it sometime in the 1st half of calendar year 2027.'",
     rule="YES if an NSE filing or company communication states JV2 was formed/closed (definitive agreements executed and transaction completed) on or before 30-Jun-2027.",
     source="NSE announcements (SONACOMS); Q4 FY27 / Q1 FY28 call", by="2027-07-31",
     spec=doc_spec("SONACOMS", "2027-06-30", "Denso|joint venture|JV|completion", ["(JV ?2|joint venture)[^.\\n]{0,200}(complet|consummat|closed|formed|incorporat)"],
                   "event: JV2 completion on or before 30-Jun-2027", "2027-03-01"))
# ---------------- SANSERA
call(T="SANSERA", slug="fy27-revenue-growth-17pct-plus-cred", cat="revenue_growth", promise="promise:SANSERA:2026-08-13:fy27-high-teens-growth",
     title="Sansera FY27 consolidated revenue growth is >=17.0% (low end of 'high-teens' guide)",
     evidence="Q1FY27 call (13-Aug-2026): 'we expect to end FY27 with high-teens top-line growth'; Q&A 'high-teens to 20%'; Feb-26 'about 20%'. Screener: FY26 3,498 cr; H1FY27 2,112 cr (+33%); needs H2 >= ~1,981 cr (+3.9% YoY). ADS FY27 guide INR 550-600 cr.",
     rule="YES if FY27 consolidated revenue from operations / FY26 - 1 >= 17.0% (NSE XBRL + screener consolidated, one decimal).",
     source="NSE XBRL + screener.in consolidated", by="2027-05-31", spec=fy_spec("sales_growth_pct", ">=", 17.0, 0.5))
call(T="SANSERA", slug="fy27-opm-above-fy26-cred", cat="margin", promise="promise:SANSERA:2026-02-10:fy27-margin-better-than-fy26",
     title="Sansera FY27 consolidated operating margin is >18.4% (better than FY26)",
     evidence="Q3FY26 call (10-Feb-2026): 'our margin profile will continue to be better than the current year'; Q1FY27: 'inch towards 19%'. FY26 screener OPM 18.4% (company EBITDA 18.1%); H1FY27 screener 19.2%, company 19.3%.",
     rule="YES if FY27 consolidated Operating Profit / Sales (screener; NSE XBRL second source) is > 18.4%, to one decimal.",
     source="screener.in + NSE XBRL consolidated", by="2027-05-31", spec=fy_spec("opm_pct", ">", 18.4, 0.3))
call(T="SANSERA", slug="nichidai-jv-production-by-mar27-cred", cat="capacity", promise="promise:SANSERA:2026-11-06:nichidai-jv-production-end-h2fy27",
     title="Sansera-Nichidai JV starts commercial production by 31-Mar-2027",
     evidence="Q2FY27 call (06-Nov-2026), opening remarks: 'commercial production at the Sansera-Nichidai JV is expected to commence towards the end of H2 FY 2027.' Sansera's ADS hangar slipped Jun-Jul -> Oct-2026 without explanation.",
     rule="YES if the Q4 FY27 results release/presentation/call (or an NSE filing) states that the JV's commercial production began on or before 31-Mar-2027. 'Trial/sample production' only = NO.",
     source="Sansera Q4 FY27 earnings call transcript / presentation (NSE)", by="2027-06-15",
     spec=doc_spec("SANSERA", "2027-03-31", "transcript|presentation|Nichidai|joint venture", ["Nichidai[^.\\n]{0,200}(commercial production|commenced|started|SOP)"],
                   "event: commercial production (not trial) by 31-Mar-2027", "2027-04-15"))
call(T="SANSERA", slug="defence-facility-operational-by-mar27-cred", cat="capacity", promise="promise:SANSERA:2026-11-06:defence-facility-ops-end-q3fy27",
     title="Sansera's dedicated defence facility is operational by 31-Mar-2027",
     evidence="Q2FY27 call (06-Nov-2026): 'our dedicated facility is expected to begin operations towards the end of Q3 FY 2027'; Q&A 'towards the end of the third quarter or from the fourth quarter'.",
     rule="YES if a Q3/Q4 FY27 call, presentation or NSE filing states the dedicated defence facility began operations on or before 31-Mar-2027.",
     source="Sansera Q3/Q4 FY27 earnings call transcripts (NSE)", by="2027-06-15",
     spec=doc_spec("SANSERA", "2027-03-31", "transcript|presentation|defence|defense", ["defen[cs]e[^.\\n]{0,40}(facility|plant)[^.\\n]{0,160}(operational|began|commenced|started|inaugurat)"],
                   "event: defence facility operating by 31-Mar-2027", "2027-02-01"))
# ---------------- HAPPYFORGE
call(T="HAPPYFORGE", slug="fy27-revenue-growth-17pct-plus-cred", cat="revenue_growth", promise="promise:HAPPYFORGE:2026-05-22:fy27-late-teen-volume-margin-flat",
     title="Happy Forgings FY27 consolidated revenue growth is >=17.0% (proxy for its late-teen volume guide)",
     evidence="Q4FY26 call (22-May-2026): 'late-teen volume growth ... EBITDA margins broadly in line with FY26'; restated Aug-26 and Nov-26 ('well-positioned to meet our full-year volume growth guidance'). H1FY27 volume +24%, realisation +5%, revenue +30% (screener 950 cr vs 731). FY26 revenue 1,546 cr; needs H2 >= ~859 cr (+5% YoY). Revenue is a proxy: guidance is on volume.",
     rule="YES if FY27 consolidated revenue from operations / FY26 - 1 >= 17.0% (NSE XBRL + screener, one decimal).",
     source="NSE XBRL + screener.in consolidated", by="2027-05-31", spec=fy_spec("sales_growth_pct", ">=", 17.0, 0.5, "proxy for the volume guide; revenue basis only"))
call(T="HAPPYFORGE", slug="fy27-opm-30pct-plus-cred", cat="margin", promise="promise:HAPPYFORGE:2026-05-22:fy27-late-teen-volume-margin-flat",
     title="Happy Forgings FY27 consolidated operating margin is >=30.0% ('broadly in line' with FY26 30.4%)",
     evidence="Q4FY26: margin 'broadly in line with FY26 levels' (30.4% company; screener 30.5%); Q1FY27 'upwards of 30% going forward'; Feb-26 '29-31% over the medium term'. Screener OPM Q1/Q2 FY27 31.4%/30.5%; Nov-26 flags RM/freight pressure.",
     rule="YES if FY27 consolidated Operating Profit / Sales (screener; NSE XBRL second source) is >= 30.0%, to one decimal.",
     source="screener.in + NSE XBRL consolidated", by="2027-05-31", spec=fy_spec("opm_pct", ">=", 30.0, 0.3))
call(T="HAPPYFORGE", slug="orders-500cr-by-mar27-cred", cat="other", promise="promise:HAPPYFORGE:2026-11-06:close-500cr-orders-by-mar27",
     title="Happy Forgings reports >=INR 450 cr of new orders won between 06-Nov-2026 and 31-Mar-2027 (target ~INR 500 cr)",
     evidence="Q2FY27 call (06-Nov-2026): 'by March, we will have orders of close to Rs.500 crores' (data-centre / heavy components); ~INR 300 cr data-centre orders already secured before the call (excluded). 'Close to 500' is read as >=90% of 500.",
     rule="YES if the Q4 FY27 call/presentation (or NSE filings) states new orders/peak-annual business won after the Q2FY27 call and by 31-Mar-2027 totalling >=INR 450 cr (company's own figure; lifetime vs annual basis as the company states it, judged against the ~500 cr statement).",
     source="Happy Forgings Q4 FY27 earnings call transcript / investor presentation (NSE)", by="2027-06-15",
     spec={**doc_spec("HAPPYFORGE", "2027-03-31", "transcript|presentation|order", ["(order|business)[^.\\n]{0,120}(Rs\\.?|INR|₹) ?[0-9,]{3,6} ?cr"],
                   "assisted: order total since 06-Nov-2026 >= INR 450 cr; company basis", "2027-04-15"), "type": "a", "op": ">=", "threshold": 450})
# ---------------- ENDURANCE
call(T="ENDURANCE", slug="tata-4w-driveshaft-sop-q3fy27-cred", cat="capacity", promise="promise:ENDURANCE:2026-08-14:tata-4w-driveshaft-sop-q3fy27",
     title="Endurance starts SOP of 4W driveshafts for Tata Motors by 31-Dec-2026",
     evidence="Q1FY27 call (14-Aug-2026): 'SOP for Tata Motors is expected also in the next quarter'; Q2FY27 (04-Nov-2026): 'expected in this quarter'. Endurance SOP record: dual-channel ABS 13 months late; Chennai brakes Q2FY27 -> Mar-2027; Bajaj SOP Q2 -> Q4; Chinese OEM Q1 -> Q3.",
     rule="YES if the Q3 FY27 call/presentation (or an NSE filing) states that 4W driveshaft supplies/SOP for Tata Motors started on or before 31-Dec-2026. Started in Jan-2027 or later, or not mentioned by the Q3 call = NO.",
     source="Endurance Q3 FY27 earnings call transcript (NSE)", by="2027-02-28",
     spec=doc_spec("ENDURANCE", "2026-12-31", "transcript|presentation", ["Tata[^.\\n]{0,160}(driveshaft|drive shaft)[^.\\n]{0,120}(SOP|started|commenced|began)|(driveshaft|drive shaft)[^.\\n]{0,160}Tata[^.\\n]{0,120}(SOP|started|commenced|began)"],
                   "event: SOP by 31-Dec-2026 per Q3 FY27 call", "2027-02-01"))
call(T="ENDURANCE", slug="chennai-disc-brake-sop-by-mar27-cred", cat="capacity", promise="promise:ENDURANCE:2026-11-04:chennai-disc-brake-sop-mar27",
     title="Endurance's new Chennai disc-brake plant starts SOP by 31-Mar-2027",
     evidence="Q2FY27 call (04-Nov-2026): 'At our new Chennai plant for disc brake assembly systems, the SOP will start in March 2027.' First promised for Q2FY27 (Nov-25), then July-2026 (May-26) and Sep-2026 (Aug-26).",
     rule="YES if the Q4 FY27 call/presentation (or an NSE filing) states SOP at the new Chennai disc-brake plant started on or before 31-Mar-2027.",
     source="Endurance Q4 FY27 earnings call transcript (NSE)", by="2027-06-15",
     spec=doc_spec("ENDURANCE", "2027-03-31", "transcript|presentation", ["Chennai[^.\\n]{0,160}(disc brake|brake)[^.\\n]{0,160}(SOP|started|commenced)"],
                   "event: Chennai disc-brake SOP by 31-Mar-2027", "2027-05-01"))
call(T="ENDURANCE", slug="fifth-forging-press-sop-by-mar27-cred", cat="capacity", promise="promise:ENDURANCE:2026-05-15:forging-plant-sop-q3fy27",
     title="Endurance's fifth aluminium forging press starts SOP by 31-Mar-2027",
     evidence="Q4FY26 (15-May-2026): new forging plant 'will start SOP in Q3 of this financial year'; Q1FY27: 'fifth forging press with SOP expected in the next quarter'; Q2FY27: 'SOP expected in Q4 of FY 27'. Deadline used is the latest stated date (Q4FY27).",
     rule="YES if the Q4 FY27 call/presentation (or an NSE filing) states SOP of the fifth aluminium forging press / new forging plant started on or before 31-Mar-2027.",
     source="Endurance Q4 FY27 earnings call transcript (NSE)", by="2027-06-15",
     spec=doc_spec("ENDURANCE", "2027-03-31", "transcript|presentation", ["(fifth|5th)[^.\\n]{0,80}(forging )?press[^.\\n]{0,160}(SOP|started|commenced|commissioned)"],
                   "event: fifth press SOP by 31-Mar-2027", "2027-05-01"))
call(T="ENDURANCE", slug="fy27-driveshaft-revenue-100cr-cred", cat="revenue_growth", promise="promise:ENDURANCE:2026-11-04:driveshaft-revenue-over-100cr-fy27",
     title="Endurance FY27 driveshaft revenue exceeds INR 100 cr (company-reported)",
     evidence="Q2FY27 call (04-Nov-2026): 'we expect our driveshaft revenue to cross ₹ 100 crores in FY 27' (3W programmes of Bajaj, Mahindra, TVS supplying; Tata 4W SOP due Q3).",
     rule="YES if Endurance's Q4 FY27 call/presentation states FY27 driveshaft revenue > INR 100 cr. Not disclosed = review (void if never disclosed by 2027-06-30).",
     source="Endurance Q4 FY27 earnings call transcript / presentation (NSE)", by="2027-06-30",
     spec={**doc_spec("ENDURANCE", "2027-03-31", "transcript|presentation", ["(driveshaft|drive shaft)[^.\\n]{0,40}revenue[^.\\n]{0,120}(₹|Rs\\.?|INR) ?[0-9,]+ ?cr"],
                   "assisted: company-reported FY27 driveshaft revenue > INR 100 cr", "2027-05-01"), "type": "a", "op": ">", "threshold": 100})

recs, specs = [], {}
for k in C:
    T = k["T"]; p, p0, b = prob(T, k["cat"]); sac = S["sac"][T]
    cid = f"thesis:paper-call:{T}:{k['slug']}"
    adj = f"p0 = {p0:.2f} (leave-one-out peer strict delivery rate, category '{k['cat']}'" + (", all-category fallback" if b.get("fallback_all") else "") + f", n={b['n']}); SAC {sac['sac_pts']:+} pts x weight {sac['shrink_weight']} (N={sac['n_scored']}) -> p = {p:.2f}"
    body = (f"Credibility-generated forward test (NOT a recommendation; not buy/sell). Probability {p:.2f} (naive sector base rate {p0:.2f}) that: {k['title'][len(T)+1:] if False else k['title']}. "
            f"Probability set only by the pre-stated rule (research_notes/Promise tracker pilot/AUTO_COMPONENTS_peer_comparison.md section 5): {adj}. "
            f"Evidence: {k['evidence']} Resolution: {k['rule']} Source: {k['source']}. Resolve by {k['by']}; score with Brier vs the base rate, to test whether the credibility adjustment adds skill.")
    recs.append({"type": "thesis", "id": cid, "title": "Paper call: " + k["title"], "body": body, "tickers": [T],
                 "tags": ["paper-call", "method-test", "credibility-generated", "promise-tracker", "india", "sector-auto-ancillary", f"cat-{k['cat'].replace('_','-')}"],
                 "date": MADE, "status": "open",
                 "data": {"probability": p, "base_rate_probability": p0, "method": "promise-tracker credibility (sector-adjusted, rule-generated)",
                          "made_on": MADE, "resolve_by": k["by"], "resolution_rule": k["rule"], "resolution_source": k["source"],
                          "base_rate_reasoning": f"Naive forecaster = sector delivery rate for '{k['cat']}' promises among the other auto-component peers (strict: delivered only, specificity-weighted; n={b['n']}" + (", too few in category so all-category peer rate used" if b.get("fallback_all") else "") + "). No company-specific information.",
                          "adjustment_rule": S["adjustment_rule"], "adjustment_applied": adj,
                          "sector_adjusted_score": sac["sac_pts"], "sac_shrink_weight": sac["shrink_weight"], "sac_n_scored": sac["n_scored"],
                          "promise_category": k["cat"], "promise_id": k["promise"], "peer_set": S["companies"],
                          "outcome": None, "brier": None},
                 "sources": [CALLS_URL for CALLS_URL in []] + [SCR.format(T)],
                 "confidence": "single-source",
                 "links": [{"to": k["promise"], "rel": "tests"}, {"to": f"analysis:{T}:credibility-2026-11", "rel": "derived_from"},
                           {"to": "insight:auto-components-promise-credibility-base-rate", "rel": "derived_from"}]})
    sp_ = dict(k["spec"])
    if sp_.get("kind") == "doc_scan":   # the confirming document (next results call) arrives after the event date
        sp_["event_deadline"] = sp_["deadline"]; sp_["deadline"] = k["by"]
    specs[cid] = sp_
# transcript urls as sources
import importlib.util
for r in recs:
    T = r["tickers"][0]
    if T == "UNIPARTS": continue
    sp = importlib.util.spec_from_file_location("L", os.path.join(HERE, f"promises_{T}.py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    d = r["data"]["promise_id"].split(":")[2]
    if d in m.CALLS: r["sources"].insert(0, m.CALLS[d][1])
out = os.path.join(ROOT, "memdb/seeds/2026-11-22_paper_calls_credibility.json")
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
for r in recs: print(f"{r['tickers'][0]:11} {r['data']['promise_category']:15} p={r['data']['probability']:.2f} base={r['data']['base_rate_probability']:.2f} {r['data']['resolve_by']} {r['id']}")
