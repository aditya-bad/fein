# Promise ledger for Persistent Systems (NSE: PERSISTENT). Built 2026-11-22, IT mid-caps peer set.
# Method: pipeline v1.2 fetch/turns/candidates on the last 6 calls (Q1FY26..Q2FY27). Persistent held NO Q1FY27
# earnings call (results 02-Aug-2026, during the Nagarro offer), so the 6 are: Q1FY26, Q2FY26, Q3FY26, Q4FY26
# (website PDF via --local; NSE has a cover letter only), the 28-Jun-2026 Nagarro acquisition call, Q2FY27.
# turns.py needed --roster (cover page not parsed). LLM step done by Claude by hand: opening remarks in full +
# targeted greps (aspiration, $2 billion, basis points, FY27, tax rate, wage, next quarter) + later calls for outcomes.
# Same scoring as scripts_TD_peers/build_seed.py (clarifications A-D of TD_peer_comparison.md apply).
# Persistent says "we don't give forward-looking guidance" every call; its scoreable statements are an FY27 revenue
# aspiration, an EBIT-margin expansion aspiration, tax-rate and quarter-ahead margin walk guidance.
# Company EBIT margin = company-reported. Screener-derived (OP - dep)/sales differs: FY26 16.2% vs company 15.6%;
# Q1/Q2 FY27 13.5% / 10.0% vs company ~16.0% / 15.0% (screener puts Nagarro transaction costs in expenses).
TICKER = "PERSISTENT"
SCREENER = "https://www.screener.in/company/PERSISTENT/consolidated/"
N = "https://nsearchives.nseindia.in/corporate/"
CALLS = {
    "2025-07-23": ("Q1FY26 concall transcript", N + "PERSISTENTUSER1_29072025232737_PSLTranscript_of_Investors_call_recordingsigned.pdf"),
    "2025-10-14": ("Q2FY26 concall transcript", N + "PERSISTENTUSER1_20102025194609_PSLEarningscallTranscriptQ2FY26.pdf"),
    "2026-01-20": ("Q3FY26 concall transcript", N + "PERSISTENTUSER1_27012026213814_PSLSubmissionoftheTranscriptforQ3FY26Sd.pdf"),
    "2026-04-21": ("Q4FY26 concall transcript (company website; NSE filing is a cover letter)", "https://www.persistent.com/wp-content/uploads/2026/04/Analyst-Call-Transcript-Q4FY26.pdf"),
    "2026-06-28": ("Nagarro acquisition investor call transcript", N + "PERSISTENTUSER1_03072026121301_PSLInvestorCallTranscriptSubmissionSd.pdf"),
    "2026-10-15": ("Q2FY27 concall transcript", N + "PERSISTENTUSER1_23102026204328_PSLTranscriptSubmissionOctober2026Sd.pdf"),
}
SK = "Sandeep Kalra (ED & CEO)"
VT = "Vinit Teredesai (CFO)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q1FY26 (23-Jul-2025)
add(said_on="2025-07-23", slug="usd-2bn-revenue-by-fy27", speaker=SK, category="revenue_growth",
    title="Reach USD 2 billion revenue by end of FY27 (needs ~19-20% CAGR)",
    quote="we have to get to $2 billion by FY27, which is ending in March, 2027. We need a compounded annual growth rate in the range of 19%-20%. We are tracking to that",
    metric="Annual revenue (USD)", target="USD 2,000 mn in FY27", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3, conditionality="aspiration",
    evidence="FY26 USD 1,654 mn (+17.4%); Q2FY27 USD 487.6 mn (+7.8% QoQ, organic - Nagarro not closed). GOALPOST FLAG: on 2026-04-21 the CEO said '$2 billion by FY27, that's a run rate ... Q4 exit ... in the range of $500 million or so ... plus minus a quarter at worst' - a full-year target re-cast as an exit run rate without saying it had changed. Resolve at the deadline (pipeline v1.1: a pending original is not pre-judged). Nagarro (closing ~Dec-2026/Jan-2027) will inflate reported FY27 revenue.",
    later_restatements="2025-10-14 'steady progress towards our aspiration of reaching $2 billion by end of FY27'; 2026-01-20 'aspiration of $2 billion by March 2027'; 2026-04-21 re-cast as Q4FY27 exit run rate ~$500 mn")
add(said_on="2025-07-23", slug="ebit-margin-plus-200-300bp-by-fy27", speaker=VT, category="margin",
    title="EBIT margin to improve 200-300 bp from FY25 (14.7%) by FY27, i.e. ~16.7-17.7%",
    quote="We have mentioned in the past that it needs to be improved by 200-300 basis point by the time we reach FY27. If you look at our last year, it was 14.7.",
    metric="EBIT margin (company)", target="+200-300 bp vs FY25 14.7% (16.7-17.7%)", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3, conditionality="aspiration",
    evidence="FY26 15.6% (+90 bp); Q1FY27 ~16.0% (derived from Q2's +1.6% QoQ EBIT on +8.4% QoQ INR revenue), Q2FY27 15.0% (wage hike, large-deal amortisation). GOALPOST FLAG: 2026-01-20 'we are not aspiring now to take it another 200 basis points up'; 2026-04-21 'we have achieved whatever we had said ... Our aspiration continues to be in the 16 to 17% range' - the floor moved from 16.7% to 16% without acknowledging it. Scored at FY27 on the expansion promised (clarification B).",
    later_restatements="2025-10-14 '100 bp in FY26 and probably another 100 bp in FY27'; 2026-04-21 and 2026-10-15 '16 to 17% range' aspiration")
add(said_on="2025-07-23", slug="fy26-etr-22-5-to-23-5pct", speaker=VT, category="other",
    title="FY26 effective tax rate in the 22.5-23.5% range",
    quote="We expect our overall effective tax rate for the year to remain in the range of 22.5% to 23.5% going forward.",
    metric="Effective tax rate", target="22.5-23.5%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    status="delivered", evidence="FY26 ETR 22.6% ('Effective tax rate for FY26 stood at 22.6%', Q4FY26 call).", delivered_value="22.6%", delivery_ratio=1.0, confidence="verified")
add(said_on="2025-07-23", slug="wage-hike-deferred-to-oct25", speaker=VT, category="other",
    title="Annual wage hike postponed by one quarter (to 1-Oct-2025)",
    quote="In view of the current uncertain business scenario, we have decided to postpone our wage hike by a quarter.",
    metric="Wage-hike timing", target="effective Q3FY26", deadline="2025-10-31", deadline_precision="month",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="'effective October 1, 2025, we have rolled out increments to all our employees ... in line with the previous years' (Q2FY26 call).", delivery_ratio=1.0, confidence="verified")
add(said_on="2025-07-23", slug="europe-15pct-of-revenue-2-3yrs", speaker=SK, category="revenue_growth",
    title="Europe to reach ~15% of revenue in the next 2-3 years",
    quote="Europe, where we have clearly said that we want to be 15% in revenue terms as we go ahead in the next 2-3 years",
    metric="Europe share of revenue", target="~15%", deadline="2028-03-31", deadline_precision="vague",
    specificity="precise", volunteered=False, materiality=2,
    evidence="Q4FY26: Europe declined 1.8% QoQ ('an area where we want to double down'). Nagarro (Europe-heavy) would meet it mechanically once consolidated.")

# ---- Q2FY26 (14-Oct-2025)
add(said_on="2025-10-14", slug="fy26-ebit-plus-100bp", speaker=VT, category="margin",
    title="FY26 EBIT margin ~100 bp above FY25 (14.7%), i.e. ~15.7%",
    quote="if we are looking at our current trajectory, we are looking at 100 basis point improvement in FY26, and probably another 100 basis point in FY27",
    metric="EBIT margin (company)", target="+100 bp vs FY25 14.7%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="delivered", evidence="FY26 EBIT margin 15.6% (+90 bp; company, Q4FY26 call), despite a one-time 230 bp labour-code charge in Q3. Within 0.3 pp of +100 bp. Screener-derived (OP-dep)/sales FY26 16.2% (different classification).", delivered_value="15.6% (+90 bp)", delivery_ratio=0.9, confidence="verified")
add(said_on="2025-10-14", slug="q3fy26-wage-impact-net-80-100bp", speaker=VT, category="margin",
    title="Q3FY26 wage hike costs 180 bp of margin, of which 80-100 bp offset by other levers (net ~-80-100 bp QoQ from 16.3%)",
    quote="We anticipate an impact of 180 basis points on next quarter's margins due to wage hikes. However, on an overall basis, up to 80 to 100 basis points of this impact is expected to get offset",
    metric="EBIT margin Q3FY26 (company)", target="~15.3-15.5% (16.3% less net 80-100 bp)", deadline="2025-12-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q3FY26 reported EBIT 14.4% incl. a one-time 230 bp New Labour Code provision (government change, sector-wide); excluding it 16.7% (+40 bp QoQ) - the wage walk was beaten. Clarification C: delivered on the adjusted basis, both numbers shown; single-source.", delivered_value="16.7% ex-labour code (14.4% reported)", delivery_ratio=1.0, admitted_unprompted=True)

# ---- Q3FY26 (20-Jan-2026)
add(said_on="2026-01-20", slug="usd-5bn-revenue-by-fy31", speaker=SK, category="revenue_growth",
    title="Long-term aspiration: USD 5 billion annual revenue by FY31",
    quote="our long-term aspiration of reaching $5 billion in annual revenue by FY31",
    metric="Annual revenue (USD)", target="USD 5,000 mn", deadline="2031-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2, conditionality="aspiration")
add(said_on="2026-01-20", slug="esop-cost-lower-in-fy27", speaker=VT, category="margin",
    title="Stock-option (ESOP) cost to fall further in FY27",
    quote="This is a reduction in cost that is happening in FY26. There will be a further reduction in cost that will happen in FY27.",
    metric="ESOP cost", target="lower than FY26", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=1,
    evidence="Q2FY27: 'lower ESOP costs enabled us to absorb part of this [wage] impact' - on track.")

# ---- Q4FY26 (21-Apr-2026)
add(said_on="2026-04-21", slug="q4fy27-exit-run-rate-500mn", speaker=SK, category="revenue_growth",
    title="Q4FY27 quarterly revenue ~USD 500 mn (USD 2 bn annualised run rate), 'plus minus a quarter at worst'",
    quote="FY'27, Q4 exit is where we are looking at the run rate being in the range of $500 million or so.",
    metric="Quarterly revenue (USD)", target="~USD 500 mn in Q4FY27", deadline="2027-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=3,
    evidence="Q2FY27 USD 487.6 mn organic. Restates (and re-defines) the 2025-07-23 USD 2 bn FY27 target.")
add(said_on="2026-04-21", slug="ebit-aspiration-16-17pct", speaker=VT, category="margin",
    title="EBIT margin aspiration 16-17% (FY27)",
    quote="Again, that is not a guidance, it's an aspiration. Our aspiration continues to be in the 16 to 17% range.",
    metric="EBIT margin (company)", target="16-17%", deadline="2027-03-31", deadline_precision="vague",
    specificity="range", volunteered=False, materiality=3, conditionality="aspiration",
    evidence="Q2FY27 15.0% (wage hike 140 bp net, 90 bp large-deal amortisation). Restated 2026-10-15 ('we want to be in the 16 to 17 % range, that is our aspiration').",
    later_restatements="2026-10-15 same band; Nagarro (EBITDA 13.9%) not yet consolidated")

# ---- Nagarro call (28-Jun-2026)
add(said_on="2026-06-28", slug="nagarro-close-q4cy26-q1cy27", speaker=VT, category="m&a",
    title="Nagarro acquisition to close in Q4 CY2026 or early Q1 CY2027",
    quote="we expect this transaction to close sometime towards the Q4 of Calendar Year 2026 or early Q1 of Calendar Year 2027",
    metric="Nagarro deal closing", target="by ~31-Mar-2027", deadline="2027-03-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=3,
    evidence="Oct-26: 94.04% tendered; 'We expect in the next 4 to 6 weeks, max, let's say 8 weeks' for the remaining approvals (Austria, Spain). Covered by batch-2 judgment call thesis:paper-call:PERSISTENT:nagarro-deal-closes-by-mar27.")
add(said_on="2026-06-28", slug="nagarro-eps-accretive-year1", speaker=VT, category="m&a",
    title="Nagarro deal cash-EPS and reported-EPS accretive in year 1 (ex transaction expenses)",
    quote="The transaction is expected to be Cash EPS accretive as well as Reported EPS accretive in Year 1 if you remove the transaction expenses",
    metric="EPS accretion", target="accretive in year 1", deadline="2028-03-31", deadline_precision="vague",
    specificity="vague", volunteered=True, materiality=2)
add(said_on="2026-06-28", slug="net-debt-ebitda-1x-by-fy30", speaker=VT, category="debt_reduction",
    title="Net debt / combined EBITDA down to ~1x by FY2030",
    quote="it is expected to reduce down to 1X by FY2030",
    metric="Net debt / EBITDA", target="<=1x", deadline="2030-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2)

# ---- Q2FY27 (15-Oct-2026)
add(said_on="2026-10-15", slug="nagarro-txn-cost-25-30mn-next-2q", speaker=VT, category="m&a",
    title="Further Nagarro transaction expenses of USD 25-30 mn over the next two quarters",
    quote="Over the next two quarters, we expect an incremental amount ranging between USD 25 to 30 million to be incurred towards the Nagarro transaction.",
    metric="Exceptional transaction costs", target="USD 25-30 mn (Q3+Q4 FY27)", deadline="2027-03-31", deadline_precision="half-year",
    specificity="range", volunteered=True, materiality=1)

ANALYSIS_TITLE = "PERSISTENT - Management Credibility Score (IT mid-caps peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Promise tracker on Persistent Systems (IT mid-caps peer set). 6 calls (Jul-2025 to Oct-2026; no Q1FY27 call was held, the Jun-2026 Nagarro call is included); {n_promises} promises, {n_scored} scored. "
                 "Status counts: {status_counts}. Weighted delivery {weighted_delivery_ratio_pct}% (specificity-only {specificity_weighted_delivery_ratio_pct}%; hit rate {raw_hit_rate_pct}%); MCS {mcs_schema_scale}. "
                 "Persistent refuses guidance ('we don't give forward-looking guidance'); its near-term statements (FY26 ETR, FY26 +100 bp EBIT, the Q3 wage-hike walk) were all met. "
                 "The two big aspirations are pending and both show quiet re-framing: USD 2 bn 'by FY27' became a Q4FY27 exit run-rate (~USD 500 mn/qtr, 'plus minus a quarter'), and +200-300 bp from 14.7% became '16-17%'. "
                 "Nagarro (closing ~Dec-26/Jan-27) will blur both. n scored is tiny: provisional. Research, not advice.")
