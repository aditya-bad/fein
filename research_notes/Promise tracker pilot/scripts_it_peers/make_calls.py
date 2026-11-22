"""Credibility-generated paper calls (IT mid-caps, 2026-11-22). Copied from scripts_auto_peers/make_calls.py; the rule is unchanged. The probability of every call is set ONLY by the
pre-stated rule in auto_summary.json ('adjustment_rule'); nothing here is a judgment probability.
  P(base) = p0 = leave-one-out peer strict delivery rate for the promise category
  P(ours) = clip(p0 + N/(N+20) * SAC/100, 0.05, 0.95)
usage: python3 -I make_calls.py <repo_root>   -> memdb/seeds/2026-11-22_paper_calls_credibility_it.json + merges tools/scoreboard/specs.json"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = sys.argv[1]
S = json.load(open(os.path.join(HERE, "it_summary.json")))
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

# ---------------- PERSISTENT (Nagarro closing already has a batch-2 judgment call: not duplicated)
call(T="PERSISTENT", slug="fy27-ebit-16pct-plus-cred", cat="margin", promise="promise:PERSISTENT:2026-04-21:ebit-aspiration-16-17pct",
     title="Persistent FY27 consolidated EBIT margin (company-reported) is >=16.0%",
     evidence="Q4FY26 (21-Apr-2026) and Q2FY27 (15-Oct-2026): EBIT aspiration '16 to 17% range' (not guidance). FY26 15.6%; Q1FY27 ~16.0% (derived), Q2FY27 15.0%. Nagarro (EBITDA ~13.9%) consolidates from ~Dec-2026/Jan-2027. Origin: Jul-2025 '+200-300 bp by FY27' from 14.7%.",
     rule="YES if the FY27 consolidated EBIT margin reported by Persistent (Q4 FY27 press release / factsheet / call, as reported including Nagarro if consolidated, before exceptional items) is >= 16.0%, to one decimal. Screener (OP - depreciation)/sales is NOT used (it differs by 0.5-5 pp).",
     source="Persistent Q4 FY27 press release / investor factsheet (NSE)", by="2027-05-31",
     spec={**doc_spec("PERSISTENT", "2027-03-31", "press|result|presentation|factsheet|transcript", ["EBIT[^.\\n]{0,60}(FY ?27|full year|year)[^.\\n]{0,60}[0-9]{1,2}\\.[0-9] ?%|(FY ?27|full year)[^.\\n]{0,80}EBIT[^.\\n]{0,40}[0-9]{1,2}\\.[0-9] ?%"],
                         "assisted: company-reported FY27 EBIT margin >= 16.0%", "2027-04-15"), "type": "a", "op": ">=", "threshold": 16.0})
call(T="PERSISTENT", slug="q4fy27-organic-revenue-500mn-cred", cat="revenue_growth", promise="promise:PERSISTENT:2026-04-21:q4fy27-exit-run-rate-500mn",
     title="Persistent Q4FY27 revenue excluding Nagarro is >=USD 500 mn (the re-cast 'USD 2 bn by FY27' run rate)",
     evidence="Q4FY26 (21-Apr-2026): 'FY'27, Q4 exit is where we are looking at the run rate being in the range of $500 million or so' ('plus minus a quarter at worst'); re-cast from Jul-2025 'reach $2 billion by FY27'. Q2FY27 USD 487.6 mn organic (+7.8% QoQ incl. a large-deal ramp).",
     rule="YES if Persistent's Q4 FY27 USD revenue excluding Nagarro is >= USD 500.0 mn. If Nagarro is not consolidated in Q4 FY27, reported USD revenue is used. If it is consolidated and Persistent does not disclose an ex-Nagarro (organic/standalone Persistent) USD figure by 2027-06-30, the call is VOID.",
     source="Persistent Q4 FY27 press release / factsheet / call (NSE)", by="2027-06-30",
     spec={**doc_spec("PERSISTENT", "2027-03-31", "press|result|presentation|factsheet|transcript", ["(USD|US\\$|\\$) ?[0-9]{3}(\\.[0-9])? ?(million|mn|Mn)[^.\\n]{0,80}(Q4|quarter)", "(organic|excluding Nagarro|ex-Nagarro|standalone)[^.\\n]{0,120}(USD|US\\$|\\$) ?[0-9]{3}"],
                         "assisted: Q4FY27 USD revenue ex-Nagarro >= 500 mn; void if not disclosed when consolidated", "2027-04-15"), "type": "a", "op": ">=", "threshold": 500.0})
# ---------------- COFORGE (NSE has cover letters for transcripts, but results / press releases / factsheets are filed on NSE)
call(T="COFORGE", slug="fy27-ebit-16pct-plus-cred", cat="margin", promise="promise:COFORGE:2026-10-23:fy27-ebit-16pct-q4-17pct",
     title="Coforge FY27 consolidated EBIT margin (company-reported) is >=16.0%",
     evidence="Q2FY27 (23-Oct-2026): FY27 consolidated EBIT guidance raised to 16% from 15.5% (May-2026); 'reported Q4 EBIT of 17%'. H1FY27 16.0% (Q1 16.0%, Q2 16.0%). FY26 14.4%.",
     rule="YES if Coforge's reported FY27 consolidated EBIT margin (company definition, Q4 FY27 release/factsheet/call) is >= 16.0%, to one decimal. Screener OPM/depreciation is NOT used.",
     source="Coforge Q4 FY27 press release / factsheet (NSE) and earnings call transcript (investors.coforge.com)", by="2027-05-31",
     spec={**doc_spec("COFORGE", "2027-03-31", "press|result|presentation|factsheet|outcome", ["EBIT[^.\\n]{0,80}(FY ?27|FY2027|full year|year)[^.\\n]{0,60}[0-9]{1,2}(\\.[0-9])? ?%|(FY ?27|FY2027|full year)[^.\\n]{0,80}EBIT[^.\\n]{0,40}[0-9]{1,2}(\\.[0-9])? ?%"],
                         "assisted: company-reported FY27 consolidated EBIT >= 16.0% (transcript only on the company site)", "2027-04-15"), "type": "a", "op": ">=", "threshold": 16.0})
call(T="COFORGE", slug="fy27-ebitda-20-5pct-plus-cred", cat="margin", promise="promise:COFORGE:2026-05-05:fy27-ebitda-20-5-21pct",
     title="Coforge FY27 consolidated EBITDA margin (company-reported) is >=20.5%",
     evidence="Q4FY26 (05-May-2026): FY27 consolidated EBITDA 20.5-21% incl. Encora; Q2FY27: 'H1 is at 20.5. We remain confident of the guidance'. Screener OPM Q1/Q2 FY27 19.1% / 19.8% (company definition differs).",
     rule="YES if Coforge's reported FY27 consolidated EBITDA margin (company definition) is >= 20.5%, to one decimal.",
     source="Coforge Q4 FY27 press release / factsheet (NSE) and earnings call transcript (investors.coforge.com)", by="2027-05-31",
     spec={**doc_spec("COFORGE", "2027-03-31", "press|result|presentation|factsheet|outcome", ["EBITDA[^.\\n]{0,80}(FY ?27|FY2027|full year|year)[^.\\n]{0,60}[0-9]{2}(\\.[0-9])? ?%|(FY ?27|FY2027|full year)[^.\\n]{0,80}EBITDA[^.\\n]{0,40}[0-9]{2}(\\.[0-9])? ?%"],
                         "assisted: company-reported FY27 consolidated EBITDA >= 20.5%", "2027-04-15"), "type": "a", "op": ">=", "threshold": 20.5})
call(T="COFORGE", slug="q3fy27-eight-large-deals-cred", cat="other", promise="promise:COFORGE:2026-10-23:q3fy27-eight-large-deals",
     title="Coforge reports >=8 large deals signed in Q3FY27",
     evidence="Q2FY27 (23-Oct-2026): 'in Q3 ... we hope to again sign eight, if not more large deals' (Q2: eight, a record; FY26: 21 in the year).",
     rule="YES if Coforge's Q3 FY27 results release, factsheet or earnings call states that it signed 8 or more large deals in Q3 FY27 (company definition of 'large deal').",
     source="Coforge Q3 FY27 press release / factsheet (NSE) and earnings call transcript (investors.coforge.com)", by="2027-02-28",
     spec={**doc_spec("COFORGE", "2026-12-31", "press|result|presentation|factsheet|outcome", ["(signed|closed|won)[^.\\n]{0,40}(\\b[0-9]{1,2}\\b|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)[^.\\n]{0,20}large deals?"],
                         "assisted: count of large deals signed in Q3FY27 >= 8", "2027-01-10"), "type": "a", "op": ">=", "threshold": 8})
# ---------------- MPHASIS
call(T="MPHASIS", slug="fy27-cc-growth-10pct-plus-cred", cat="revenue_growth", promise="promise:MPHASIS:2026-11-06:fy27-cc-growth-low-double-digit",
     title="Mphasis FY27 constant-currency revenue growth (company-reported) is >=10.0%",
     evidence="Q2FY27 (06-Nov-2026): FY27 guidance raised to 'revenue growth in the low double digits' from 'high single digits to low double digits' (Apr/Jul-2026). Q1FY27 +8.3% YoY CC; Q2FY27 Direct +11.3% YoY CC; includes the TAP / Red Oak acquisitions. FY26 6.7% CC.",
     rule="YES if Mphasis reports FY27 consolidated revenue growth in constant currency of >= 10.0% (as reported, acquisitions included). If only Direct CC growth is reported, it is NOT used (review).",
     source="Mphasis Q4 FY27 press release / investor presentation / call (NSE)", by="2027-05-31",
     spec={**doc_spec("MPHASIS", "2027-03-31", "press|result|presentation|transcript|fact", ["(FY ?27|FY2027|full year|for the year)[^.\\n]{0,120}constant currency[^.\\n]{0,40}[0-9]{1,2}(\\.[0-9])? ?%|[0-9]{1,2}(\\.[0-9])? ?%[^.\\n]{0,60}constant currency[^.\\n]{0,60}(FY ?27|full year|for the year)"],
                         "assisted: company-reported FY27 total CC growth >= 10.0%", "2027-04-15"), "type": "a", "op": ">=", "threshold": 10.0})
call(T="MPHASIS", slug="fy27-ebit-in-band-cred", cat="margin", promise="promise:MPHASIS:2026-04-30:fy27-ebit-band-14-75-15-75",
     title="Mphasis FY27 EBIT margin (company-reported) is within 14.75-15.75%",
     evidence="Q4FY26 (30-Apr-2026), restated Jul and Nov-2026: 'operating within our target band of 14.75% to 15.75%'. FY26 15.3%; Q1FY27 ~14.8% (down 60 bp), Q2FY27 flat; screener-derived (OP-dep)/sales 14.8% / 14.7%.",
     rule="YES if Mphasis's reported FY27 EBIT margin is >= 14.75% and <= 15.75% (company figure, two decimals as reported; one-decimal figures 14.8-15.7 count as inside).",
     source="Mphasis Q4 FY27 press release / investor presentation / call (NSE)", by="2027-05-31",
     spec={**doc_spec("MPHASIS", "2027-03-31", "press|result|presentation|transcript|fact", ["EBIT[^.\\n]{0,80}(FY ?27|full year|for the year)[^.\\n]{0,60}[0-9]{2}\\.[0-9]{1,2} ?%|(FY ?27|full year|for the year)[^.\\n]{0,80}EBIT[^.\\n]{0,40}[0-9]{2}\\.[0-9]{1,2} ?%"],
                         "assisted: company-reported FY27 EBIT within 14.75-15.75% (range)", "2027-04-15"), "type": "a", "op": "between", "threshold": 14.75, "threshold_hi": 15.75})
call(T="MPHASIS", slug="q3fy27-dso-below-100-cred", cat="other", promise="promise:MPHASIS:2026-11-06:dso-double-digit-q3fy27",
     title="Mphasis Q3FY27 DSO (company-reported) is below 100 days",
     evidence="Q2FY27 (06-Nov-2026): DSO 105 days 'after normalizing for the delayed remittances ... expected to get to double digit levels in Q3'. Track record: Q2FY26 'normalise over the next three to four quarters' -> 89, 91, ~86-89, 95, 105 (missed).",
     rule="YES if the DSO Mphasis reports for Q3 FY27 (quarter ending 31-Dec-2026; reported figure, not a company 'normalised' figure if both are given) is <= 99 days.",
     source="Mphasis Q3 FY27 earnings call transcript / investor presentation (NSE)", by="2027-02-28",
     spec={**doc_spec("MPHASIS", "2026-12-31", "transcript|presentation|press|result", ["DSO[^.\\n]{0,60}[0-9]{2,3} days"],
                         "assisted: reported Q3FY27 DSO <= 99 days", "2027-01-10"), "type": "a", "op": "<=", "threshold": 99})
# ---------------- KPITTECH
call(T="KPITTECH", slug="fy27-ebitda-20-5pct-plus-cred", cat="margin", promise="promise:KPITTECH:2026-05-07:fy27-ebitda-20-5-21-2pct",
     title="KPIT FY27 EBITDA margin (company-reported) is >=20.5%",
     evidence="Q4FY26 call (07-May-2026): FY27 EBITDA '20.5 to 21.2' after AI/products investment. Q1FY27 17.2%, Q2FY27 17.8% (company); Q2FY27 CEO: 'it will be early next year when we get there'. The rule deliberately ignores in-year progress.",
     rule="YES if KPIT's reported FY27 consolidated EBITDA margin (company definition, Q4 FY27 release/presentation/call) is >= 20.5%, to one decimal. Screener OPM is NOT used (FY26 18.9% vs company 20.8%).",
     source="KPIT Q4 FY27 press release / investor presentation / call (NSE)", by="2027-05-31",
     spec={**doc_spec("KPITTECH", "2027-03-31", "press|result|presentation|transcript", ["EBITDA[^.\\n]{0,80}(FY ?27|FY2027|for the year|full year)[^.\\n]{0,60}[0-9]{2}(\\.[0-9])? ?%|(FY ?27|for the year|full year)[^.\\n]{0,80}EBITDA[^.\\n]{0,40}[0-9]{2}(\\.[0-9])? ?%"],
                         "assisted: company-reported FY27 EBITDA >= 20.5%", "2027-04-15"), "type": "a", "op": ">=", "threshold": 20.5})
call(T="KPITTECH", slug="h2fy27-revenue-above-h1-cred", cat="revenue_growth", promise="promise:KPITTECH:2026-07-29:return-to-growth-by-q4fy27",
     title="KPIT H2FY27 consolidated revenue exceeds H1FY27 (FY27 revenue > INR 6,732 cr = 2 x H1)",
     evidence="Q1FY27 (29-Jul-2026): 'H2 will be better than H1, and we will return to growth in H2 by Q4'; reiterated 28-Oct-2026. Screener H1FY27 = 1,675 + 1,691 = 3,366 cr; FY26 6,455 cr.",
     rule="YES if FY27 consolidated revenue from operations > INR 6,732 cr (twice H1FY27 screener 3,366 cr, i.e. H2 > H1), NSE XBRL and screener consolidated annual figures. If XBRL restates H1, the review uses H2 = FY - H1 from the same source.",
     source="NSE integrated-filing XBRL (Q4 FY27 results) + screener.in consolidated P&L", by="2027-05-31",
     spec=fy_spec("sales_cr", ">", 6732, 30, "H2 > H1 expressed as FY27 sales > 2 x H1FY27 (screener 3,366 cr)"))
call(T="KPITTECH", slug="q4fy27-cc-qoq-growth-positive-cred", cat="revenue_growth", promise="promise:KPITTECH:2026-07-29:return-to-growth-by-q4fy27",
     title="KPIT Q4FY27 constant-currency revenue growth QoQ (company-reported) is >0%",
     evidence="Q1FY27: 'we will return to growth in H2 by Q4'; Q2FY27: 'we expect growth in that quarter' (no number). Q1FY27 -3.6% CC QoQ; Q2FY27 services flat, products +5% QoQ.",
     rule="YES if KPIT reports Q4 FY27 (Jan-Mar 2027) sequential revenue growth in constant currency > 0.0%. If only USD growth is given, it is used; if neither, INR QoQ from screener.",
     source="KPIT Q4 FY27 press release / investor presentation / call (NSE)", by="2027-05-31",
     spec={**doc_spec("KPITTECH", "2027-03-31", "press|result|presentation|transcript", ["(constant currency|CC)[^.\\n]{0,80}(quarter-on-quarter|Q-o-Q|QoQ|sequential)[^.\\n]{0,40}-?[0-9]{1,2}(\\.[0-9])? ?%|(quarter-on-quarter|Q-o-Q|QoQ|sequential)[^.\\n]{0,80}(constant currency|CC)[^.\\n]{0,40}-?[0-9]{1,2}(\\.[0-9])? ?%"],
                         "assisted: company-reported Q4FY27 CC QoQ growth > 0%", "2027-04-15"), "type": "a", "op": ">", "threshold": 0.0})

recs, specs = [], {}
for k in C:
    T = k["T"]; p, p0, b = prob(T, k["cat"]); sac = S["sac"][T]
    cid = f"thesis:paper-call:{T}:{k['slug']}"
    adj = f"p0 = {p0:.2f} (leave-one-out peer strict delivery rate, category '{k['cat']}'" + (", all-category fallback" if b.get("fallback_all") else "") + f", n={b['n']}); SAC {sac['sac_pts']:+} pts x weight {sac['shrink_weight']} (N={sac['n_scored']}) -> p = {p:.2f}"
    body = (f"Credibility-generated forward test (NOT a recommendation; not buy/sell). Probability {p:.2f} (naive sector base rate {p0:.2f}) that: {k['title'][len(T)+1:] if False else k['title']}. "
            f"Probability set only by the pre-stated rule (research_notes/Promise tracker pilot/IT_MIDCAPS_peer_comparison.md section 5 = AUTO_COMPONENTS_peer_comparison.md section 5, unchanged): {adj}. "
            f"Evidence: {k['evidence']} Resolution: {k['rule']} Source: {k['source']}. Resolve by {k['by']}; score with Brier vs the base rate, to test whether the credibility adjustment adds skill.")
    recs.append({"type": "thesis", "id": cid, "title": "Paper call: " + k["title"], "body": body, "tickers": [T],
                 "tags": ["paper-call", "method-test", "credibility-generated", "promise-tracker", "india", "sector-it", "it", f"cat-{k['cat'].replace('_','-')}"],
                 "date": MADE, "status": "open",
                 "data": {"probability": p, "base_rate_probability": p0, "method": "promise-tracker credibility (sector-adjusted, rule-generated)",
                          "made_on": MADE, "resolve_by": k["by"], "resolution_rule": k["rule"], "resolution_source": k["source"],
                          "base_rate_reasoning": f"Naive forecaster = sector delivery rate for '{k['cat']}' promises among the other IT mid-cap peers (strict: delivered only, specificity-weighted; n={b['n']}" + (", too few in category so all-category peer rate used" if b.get("fallback_all") else "") + "). No company-specific information.",
                          "adjustment_rule": S["adjustment_rule"], "adjustment_applied": adj,
                          "sector_adjusted_score": sac["sac_pts"], "sac_shrink_weight": sac["shrink_weight"], "sac_n_scored": sac["n_scored"],
                          "promise_category": k["cat"], "promise_id": k["promise"], "peer_set": S["companies"],
                          "outcome": None, "brier": None},
                 "sources": [CALLS_URL for CALLS_URL in []] + [SCR.format(T)],
                 "confidence": "single-source",
                 "links": [{"to": k["promise"], "rel": "tests"}, {"to": f"analysis:{T}:credibility-2026-11", "rel": "derived_from"},
                           {"to": "insight:it-midcaps-promise-credibility-base-rate", "rel": "derived_from"}]})
    sp_ = dict(k["spec"])
    if sp_.get("kind") == "doc_scan":   # the confirming document (next results call) arrives after the event date
        sp_["event_deadline"] = sp_["deadline"]; sp_["deadline"] = k["by"]
    specs[cid] = sp_
# transcript urls as sources
import importlib.util
for r in recs:
    T = r["tickers"][0]
    sp = importlib.util.spec_from_file_location("L", os.path.join(HERE, f"promises_{T}.py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    d = r["data"]["promise_id"].split(":")[2]
    if d in m.CALLS: r["sources"].insert(0, m.CALLS[d][1])
out = os.path.join(ROOT, "memdb/seeds/2026-11-22_paper_calls_credibility_it.json")
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
