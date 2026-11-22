# Promise ledger for Sansera Engineering (NSE: SANSERA). Built 2026-11-22, auto-components peer set.
# Method as promises_SONACOMS.py. Last 6 NSE transcripts (Q1FY26..Q2FY27). Group numbers checked on screener
# (consolidated): FY26 revenue 3,498 vs 3,017 cr = +15.9%; H1FY26 1,591 / H2FY26 1,907 cr; H1FY27 2,112 cr (+33%).
# ADS = aerospace, defence & semiconductor-equipment segment (company figures only).
TICKER = "SANSERA"
SCREENER = "https://www.screener.in/company/SANSERA/consolidated/"
N = "https://nsearchives.nseindia.in/corporate/"
CALLS = {
    "2025-08-12": ("Q1FY26 concall transcript", N + "SANSERA_17082025151807_Transcript.pdf"),
    "2025-11-13": ("Q2FY26 concall transcript", N + "SANSERA_20112025093848_Transcript.pdf"),
    "2026-02-10": ("Q3FY26 concall transcript", N + "SANSERA_17022026122638_transcript.pdf"),
    "2026-05-21": ("Q4FY26 concall transcript", N + "SANSERA_28052026152825_Transcript.pdf"),
    "2026-08-13": ("Q1FY27 concall transcript", N + "SANSERA_20082026120039_Transcript.pdf"),
    "2026-11-06": ("Q2FY27 concall transcript", N + "SANSERA_13112026120144_transcript.pdf"),
}
BRP = "B.R. Preetham (Group CEO)"
VG = "Vikas Goel (CFO)"
HK = "Hari Krishnan (ADS business head)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q1FY26 (12-Aug-2025)
add(said_on="2025-08-12", slug="fy26-ads-revenue-280-300cr", speaker=BRP, category="revenue_growth",
    title="FY26 ADS revenue to double to INR 280-300 cr",
    quote="So we are quite hopeful that we should be able to reach our targeted revenue of INR280 crores to INR300 crores this year.",
    metric="ADS segment revenue FY26", target="INR 280-300 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="delivered", evidence="'ADS revenue from product sales reaching INR3,155 million, representing an exceptional growth of 155%' (Q4FY26 call). Company figure.", delivered_value="INR 315.5 cr", delivery_ratio=1.1,
    later_restatements="2025-11-13 'very close to INR 3000 million'; 2026-02-10 'target of between INR275 crores and INR300 crores'")
add(said_on="2025-08-12", slug="fy26-sweden-growth-20-25pct", speaker=BRP, category="revenue_growth",
    title="FY26 Swedish subsidiary growth 20-25% (~INR 225 cr)",
    quote="So we continue -overall, I think full year basis, we expect between 20%, 25% growth from the Swedish subsidiary.",
    metric="Sansera Sweden revenue growth FY26", target="+20-25%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="unverifiable", evidence="Q4FY26 call cites 'strong growth in Swedish subsidiary' but no FY figure; Q2FY27: Sweden -16% YoY.")

# ---- Q2FY26 (13-Nov-2025)
add(said_on="2025-11-13", slug="fy26-growth-at-least-teens", speaker=BRP, category="revenue_growth",
    title="FY26 consolidated revenue growth at least in the teens",
    quote="But currently, our visibility shows that on a full year basis, we should be able to enter at least the teens.",
    metric="Consolidated revenue growth FY26", target=">=+13% (teens)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="delivered", evidence="FY26 revenue 3,498 vs 3,017 cr = +15.9% (screener consolidated).", delivered_value="+15.9%", delivery_ratio=1.2, confidence="verified",
    later_restatements="The FY26 plan at the start of the year was 'mid-teens to high-teens' (Q4FY25 call, outside window; restated as such on 2026-02-10, acknowledged).")
add(said_on="2025-11-13", slug="h2fy26-stronger-than-h1", speaker=BRP, category="revenue_growth",
    title="H2FY26 'much, much stronger' than H1FY26",
    quote="Our expectation is that the H2 is going to be much, much, much stronger than the H1.",
    metric="H2 vs H1 FY26 revenue", target="H2 > H1", deadline="2026-03-31", deadline_precision="half-year",
    specificity="vague", volunteered=False, materiality=2,
    status="delivered", evidence="H1FY26 1,591 cr, H2FY26 1,907 cr (+20%) (screener).", delivered_value="+20% H2/H1", delivery_ratio=1.0, confidence="verified")
add(said_on="2025-11-13", slug="ads-run-rate-38-40cr-month", speaker=BRP, category="revenue_growth",
    title="ADS run-rate ~INR 38-40 cr/month for the next five months",
    quote="while our run rate in ADS has been almost now for the next five months should be close to about Rs.38 to 40 crores per month",
    metric="ADS monthly revenue Nov-25..Mar-26", target="INR 38-40 cr/month", deadline="2026-03-31", deadline_precision="quarter",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="H2FY26 ADS = 315.5 - 86.4 (H1) = ~229 cr over 6 months = ~38 cr/month (company figures).", delivered_value="~38 cr/month", delivery_ratio=0.97)
add(said_on="2025-11-13", slug="ads-hangar-ready-jun-jul-26", speaker=HK, category="capacity",
    title="New ADS hangar ready by June-July 2026",
    quote="our basic idea is to finish this by middle of next year, say around June to July",
    metric="New hangar completion", target="Jun-Jul 2026", deadline="2026-07-31", deadline_precision="month",
    specificity="precise", volunteered=False, materiality=2,
    status="moved-goalpost", evidence="Restated 2026-02-10 'June, July'; 2026-05-21 'complete the construction by July, August'; 2026-08-13 'probably by towards October when we have our new hangar ready'. No explanation of the slip given; Q2FY27 call does not confirm completion.",
    delivery_ratio=0.0, admitted_unprompted=False)

# ---- Q3FY26 (10-Feb-2026)
add(said_on="2026-02-10", slug="fy26-teens-to-mid-teens", speaker=BRP, category="revenue_growth",
    title="FY26 revenue growth teens to mid-teens with margin profile maintained",
    quote="we remain confident that we will close the year with teens to mid-teens top line growth while comfortably maintaining our current margin profile",
    metric="Consolidated revenue growth FY26", target="+13-15%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="+15.9% (screener); FY26 company EBITDA margin 18.1% vs 17.5% FY25.", delivered_value="+15.9%", delivery_ratio=1.06, confidence="verified")
add(said_on="2026-02-10", slug="fy26-capex-375-400cr", speaker=BRP, category="capacity",
    title="FY26 capex INR 375-400 cr (below the INR 450 cr plan)",
    quote="And this year, if I say that between INR375 crores and INR400 crores, a similar number could be for the next year as well.",
    metric="Capex FY26", target="INR 375-400 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="missed", evidence="FY26 capex INR 509.7 cr ('we incurred a capex of INR5,097 million', Q4FY26 call) = 27% above the top of the range given 7 weeks before year-end. Growth capex for ADS orders, so economically benign, but a forecast miss.",
    delivered_value="INR 510 cr", delivery_ratio=0.0, admitted_unprompted=False)
add(said_on="2026-02-10", slug="fy27-ads-revenue-550-600cr", speaker=BRP, category="revenue_growth",
    title="FY27 ADS revenue INR 550-600 cr",
    quote="which is what we are looking at for the next year between INR550 crores to INR600 crores is what we look at",
    metric="ADS segment revenue FY27", target="INR 550-600 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    evidence="2026-08-13: ADS growth 'about 75%-80%' for FY27 (= INR 552-568 cr on 315.5).")
add(said_on="2026-02-10", slug="fy27-revenue-growth-about-20pct", speaker=BRP, category="revenue_growth",
    title="FY27 consolidated revenue growth about 20%",
    quote="I think next year, we are looking at about 20% growth.",
    metric="Consolidated revenue growth FY27", target="~+20%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=3,
    evidence="2026-05-21 plan 'mid-to-high teens, more towards high-teens'; 2026-08-13 'high-teens top-line growth' (volunteered) and 'high-teens to 20%'. H1FY27 +33% (screener 2,112 vs 1,591 cr).")
add(said_on="2026-02-10", slug="fy27-margin-better-than-fy26", speaker=BRP, category="margin",
    title="FY27 margin profile better than FY26",
    quote="I don't want to put what number we will have, but our margin profile will continue to be better than the current year.",
    metric="Consolidated EBITDA margin FY27 vs FY26", target="> FY26 (company 18.1%; screener 18.4%)", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=2,
    evidence="2026-08-13: 'happier if we are able to inch towards 19%'. H1FY27 company 19.3%, screener 19.2%.")

# ---- Q4FY26 (21-May-2026)
add(said_on="2026-05-21", slug="fy27-capex-similar-to-fy26", speaker=BRP, category="capacity",
    title="FY27 capex at a similar level to FY26 (~INR 510 cr)",
    quote="On the capex front, during FY '26, we incurred a capex of INR5,097 million, and we expect a similar level of investment in FY '27 as well.",
    metric="Capex FY27", target="~INR 510 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=1,
    status="withdrawn", evidence="Raised openly to INR 800 cr on 2026-11-06 ('we have raised FY27 Capex projection to INR8,000 million', for new ADS orders) - explicit, explained revision >1 quarter before the deadline.", admitted_unprompted=True)
add(said_on="2026-05-21", slug="fy27-auto-h1-stronger-than-h2", speaker=BRP, category="revenue_growth",
    title="FY27 Auto business H1 stronger than H2 (base effect)",
    quote="Within the Auto business, FY '27 H1 is expected to be relatively stronger than the H2, aided by favorable base effect.",
    metric="Auto segment growth H1 vs H2 FY27", target="H1 growth > H2 growth", deadline="2027-03-31", deadline_precision="half-year",
    specificity="vague", volunteered=True, materiality=1)

# ---- Q1FY27 (13-Aug-2026)
add(said_on="2026-08-13", slug="fy27-high-teens-growth", speaker=BRP, category="revenue_growth",
    title="FY27 high-teens top-line growth (volunteered)",
    quote="With this, we expect to end FY27 with high-teens top-line growth with continuous focus on improving margin profile.",
    metric="Consolidated revenue growth FY27", target="+17-19% (high teens)", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3, evidence="H1FY27 +33% (screener).")
add(said_on="2026-08-13", slug="nadcap-approval-q2fy27", speaker=BRP, category="capacity",
    title="NADCAP and customer approvals for the new special-process facility within Q2FY27",
    quote="So with the new facility that we will probably hope to get a NADCAP and customer approvals for this special process within this quarter.",
    metric="NADCAP approval", target="by 30-Sep-2026", deadline="2026-09-30", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1, conditionality="hope",
    status="unverifiable", evidence="Not mentioned in the Q2FY27 call text read.")

# ---- Q2FY27 (06-Nov-2026)
add(said_on="2026-11-06", slug="nichidai-jv-production-end-h2fy27", speaker=BRP, category="capacity",
    title="Sansera-Nichidai JV commercial production towards the end of H2 FY27",
    quote="Adding to our growth pipeline, commercial production at the Sansera-Nichidai JV is expected to commence towards the end of H2 FY 2027.",
    metric="JV commercial production start", target="by 31-Mar-2027", deadline="2027-03-31", deadline_precision="half-year",
    specificity="range", volunteered=True, materiality=2)
add(said_on="2026-11-06", slug="defence-facility-ops-end-q3fy27", speaker=BRP, category="capacity",
    title="Dedicated defence facility to begin operations towards the end of Q3 FY27 (or from Q4)",
    quote="In defense, our dedicated facility is expected to begin operations towards the end of Q3 FY 2027",
    metric="Defence facility start", target="by Dec-2026 / Q4FY27", deadline="2027-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    evidence="Q&A: 'The defense should be operational towards the end of the third quarter or from the fourth quarter.'")
add(said_on="2026-11-06", slug="second-semicon-customer-q3fy27", speaker=HK, category="other",
    title="Add a second customer in the new (semicon/ADS) space in Q3FY27",
    quote="I would say conversations are progressing well, but we haven't yet reached the final point, which we are hopeful in Q3 we should be able to add a second customer in this space.",
    metric="Second customer win", target="by 31-Dec-2026", deadline="2026-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1, conditionality="hopeful")
add(said_on="2026-11-06", slug="fy27-capex-800cr", speaker=VG, category="capacity",
    title="FY27 capex raised to INR 800 cr",
    quote="To deliver these orders, we have raised FY27 Capex projection to INR8,000 million, fased with the customer validations",
    metric="Capex FY27", target="~INR 800 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1)

ANALYSIS_TITLE = "SANSERA - Management Credibility Score (auto-components peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Promise tracker on Sansera Engineering (auto-components peer set). 6 concalls (Aug-2025 to Nov-2026); {n_promises} promises, {n_scored} scored. "
                 "Status counts: {status_counts}. Weighted delivery {weighted_delivery_ratio_pct}% (specificity-only {specificity_weighted_delivery_ratio_pct}%; hit rate {raw_hit_rate_pct}%); MCS {mcs_schema_scale}. "
                 "Revenue promises were met: FY26 group +15.9% vs 'teens/teens to mid-teens' (the start-of-year 'mid-to-high teens' was trimmed openly), ADS INR 315 cr vs 280-300, H2>H1. "
                 "Misses are capacity forecasts: FY26 capex 510 cr vs 375-400 guided seven weeks before year-end, and the new ADS hangar re-dated Jun-Jul -> Jul-Aug -> Oct without explanation. "
                 "Guidance is mostly given under questioning, then repeated in the opening remarks. Research, not advice.")
