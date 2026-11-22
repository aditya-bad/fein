# Promise ledger for Sona BLW Precision Forgings (NSE: SONACOMS). Built 2026-11-22, auto-components peer set.
# Method: pipeline v1.1 fetch/turns/candidates (rules) on the last 6 NSE transcripts (Q1FY26..Q2FY27), then the
# LLM step done by Claude by hand (opening remarks in full + tier-A/volunteered guidance sentences + targeted greps).
# Same scoring as scripts_TD_peers/build_seed.py (clarifications A-D of TD_peer_comparison.md apply).
# Sona gives NO revenue guidance ("we don't give forward growth guidance") - most statements are mix/order-book
# commentary, so few promises are scoreable. Company EBITDA margin (company-reported) vs screener OPM: FY26 24.7% vs 24.3%.
TICKER = "SONACOMS"
SCREENER = "https://www.screener.in/company/SONACOMS/consolidated/"
N = "https://nsearchives.nseindia.in/corporate/"
CALLS = {
    "2025-08-04": ("Q1FY26 concall transcript", N + "SONACOMS_09082025173136_Transcript.pdf"),
    "2025-10-27": ("Q2FY26 concall transcript", N + "SONACOMS_31102025175705_Transcript.pdf"),
    "2026-01-23": ("Q3FY26 concall transcript", N + "SONACOMS_31012026114914_Transcript.pdf"),
    "2026-04-30": ("Q4FY26 concall transcript", N + "SONACOMS_06052026103543_Intimation.pdf"),
    "2026-07-23": ("Q1FY27 concall transcript", N + "SONACOMS_30072026142213_Transcript.pdf"),
    "2026-10-26": ("Q2FY27 concall transcript", N + "SONACOMS_31102026183421_Intimation.pdf"),
}
VVS = "Vivek Vikram Singh (MD & Group CEO)"
RN = "Rohit Nanda (Group CFO)"
SMG = "Sat Mohan Gupta (CEO, Sensors/Software)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q1FY26 (04-Aug-2025)
add(said_on="2025-08-04", slug="bev-share-improve-next-quarters", speaker=VVS, category="other",
    title="BEV revenue share to improve over the next few quarters (from 28% in Q1FY26)",
    quote="share remains low at 9%, and we expect the BEV share to improve in the next few quarters",
    metric="BEV share of automotive revenue", target="higher than Q1FY26 28%", deadline="2026-03-31", deadline_precision="vague",
    specificity="vague", volunteered=True, materiality=2,
    status="delivered", evidence="BEV share 38% in Q3FY26, 39% in Q4FY26, 44% Q1FY27, 51% Q2FY27 (company, later calls).", delivered_value="39% (Q4FY26)", delivery_ratio=1.4)
add(said_on="2025-08-04", slug="non-auto-share-over-25pct", speaker=VVS, category="other",
    title="Non-automotive revenue share to rise above 25% in the coming quarters (railways consolidation)",
    quote="The share from Asia, including India, obviously, will likely exceed 50% in the coming quarters, and we expect non-automotive revenue shares to also increase to over 25%.",
    metric="Non-automotive share of revenue", target=">25%", deadline="2026-03-31", deadline_precision="vague",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="'The share of non-automotive revenues from 9% in FY25 today is 31% in the first nine months of this year' (Q3FY26 call). Mostly mechanical (railway acquisition consolidated from Q2FY26).", delivered_value="31% (9MFY26)", delivery_ratio=1.24)
add(said_on="2025-08-04", slug="asia-share-over-50pct", speaker=VVS, category="other",
    title="Asia incl. India to exceed 50% of revenue in the coming quarters",
    quote="The share from Asia, including India, obviously, will likely exceed 50% in the coming quarters",
    metric="Asia share of revenue", target=">50%", deadline="2026-03-31", deadline_precision="vague",
    specificity="precise", volunteered=True, materiality=1,
    status="unverifiable", evidence="Geography split not restated in later transcripts read; deck not checked.")

# ---- Q2FY26 (27-Oct-2025)
add(said_on="2025-10-27", slug="consol-ebitda-margin-24-25pct", speaker=VVS, category="margin",
    title="Consolidated EBITDA margin target 24-25% after consolidating lower-margin railways",
    quote="But I would say that is the range, 24-25%, and that is our target.",
    metric="Consolidated EBITDA margin (company)", target="24-25%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="delivered", evidence="FY26 company EBITDA margin 24.7% ('we have still managed to end FY26 with a full year EBITDA margin of 24.7%', Q4FY26 call); screener OPM 24.3%. Q4FY26 alone 23.5% (screener).", delivered_value="24.7% (company)", delivery_ratio=1.0, confidence="verified",
    later_restatements="2026-04-30: 'now it is 23 to 25%' (band widened down, acknowledged); 2026-10-26: 'around 23%'")
add(said_on="2025-10-27", slug="return-ratios-improve-gradually", speaker=RN, category="other",
    title="Return ratios (ROCE 16%, ROE 13% in H1FY26) to improve in the quarters and years ahead",
    quote="We expect these ratios to improve in the quarters and years ahead.",
    metric="ROCE / ROE", target="higher than H1FY26 (ROCE 16%)", deadline="2027-03-31", deadline_precision="vague",
    specificity="vague", volunteered=True, materiality=2,
    status="partly", evidence="Screener FY26 ROCE 14% (FY25 18%) - fell; Q2FY27 call: 'Our return ratios have also improved' for H1FY27 (company, figure not checked). Direction right only from H1FY27.", delivery_ratio=0.5)
add(said_on="2025-10-27", slug="mexico-driveline-sop-q2fy28", speaker=VVS, category="capacity",
    title="Mexico driveline plant: first program production from Q2 FY28",
    quote="This program has added 2.6 billion to our order book with production expected to start in the second quarter of FY 28.",
    metric="SOP Mexico plant", target="Q2FY28", deadline="2027-09-30", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=2)

# ---- Q3FY26 (23-Jan-2026)
add(said_on="2026-01-23", slug="traction-motors-fastest-5yr", speaker=VVS, category="other",
    title="Traction motors & controllers to be the highest-growth segment for the next 5 years",
    quote="I would expect traction motors and controllers to be our highest growth segment, by far, I think.",
    metric="Segment growth ranking", target="highest growth segment", deadline="2031-03-31", deadline_precision="vague",
    specificity="vague", volunteered=False, materiality=1)

# ---- Q4FY26 (30-Apr-2026)
add(said_on="2026-04-30", slug="margin-pressure-continues-fy27", speaker=VVS, category="margin",
    title="Commodity pass-through lag will keep pressure on margins in the foreseeable future",
    quote="that lag along with the arithmetic impact on both revenue and cost, will put pressure on our margins, which we expect to continue seeing in the foreseeable future",
    metric="EBITDA margin direction", target="below FY26 24.7%", deadline="2026-09-30", deadline_precision="vague",
    specificity="vague", volunteered=True, materiality=2,
    status="delivered", evidence="Q1FY27 and Q2FY27 company EBITDA margin ~23% (screener 22.5% / 22.5%) vs FY26 24.7%.", delivered_value="~23%", delivery_ratio=1.0, confidence="verified")
add(said_on="2026-04-30", slug="fy27-margin-23-25-band", speaker=VVS, category="margin",
    title="FY27 consolidated EBITDA margin to stay in a 23-25% band",
    quote="I think now it is 23 to 25%, and that, I think we can say we should be able to continue being in that band.",
    metric="FY27 consolidated EBITDA margin", target="23-25%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    evidence="H1FY27 company ~23.0% (screener 22.5%); 2026-10-26 CFO: 'around 23% ... don't hold us to every 10 or 20 bps'.")
add(said_on="2026-04-30", slug="novelic-india-sensor-sop-cy26", speaker=SMG, category="capacity",
    title="Sensor assembly (Novelic India) SOP by end of 2026",
    quote="The SOP is going to be end of this year. the lines are already set up, because it's a sensor assembly unit.",
    metric="SOP sensor line", target="by Dec-2026", deadline="2026-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1)

# ---- Q1FY27 (23-Jul-2026)
add(said_on="2026-07-23", slug="margin-recovery-visible-from-q2", speaker=VVS, category="margin",
    title="Cost-recovery measures to become progressively visible in margins from Q2FY27",
    quote="We expect that these recovery measures will become progressively more visible from quarter 2 onwards.",
    metric="EBITDA margin Q2FY27 vs Q1FY27", target="margin up from Q1FY27 (~23%)", deadline="2026-09-30", deadline_precision="quarter",
    specificity="vague", volunteered=True, materiality=2,
    status="missed", evidence="Q2FY27 company EBITDA margin 23% ('lower by 2.x pp' YoY), screener 22.5% = flat QoQ; mgmt: 'continued margin pressure ... mainly driven by change in product mix'.",
    delivered_value="23.0% vs ~23% in Q1", delivery_ratio=0.0, admitted_unprompted=True, explanation_for_miss="Product mix (traction motors), West Asia inflation in steel/copper")
add(said_on="2026-07-23", slug="fy27-phenomenal-ev-growth", speaker=VVS, category="other",
    title="'Phenomenal' EV (BEV) revenue growth in FY27",
    quote="But despite that, I think we will see phenomenal, EV growth in the, in this year at least.",
    metric="FY27 BEV revenue growth", target="very high growth", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=2, evidence="H1FY27 BEV revenue +119% YoY to INR 1,042 cr (Q2FY27 call).")

# ---- Q2FY27 (26-Oct-2026)
add(said_on="2026-10-26", slug="jv1-denso-carveout-close-dec26", speaker=RN, category="other",
    title="Close JV1 (2W/3W carve-out with Denso) by end-December 2026, possibly spilling to January",
    quote="So we're targeting to close this JV 1 part of it which is carving out of the business by end of December because of the year-end holidays there is a possibility it may spill over to January",
    metric="JV1 completion", target="by 31-Dec-2026 (Jan-2027 at the latest)", deadline="2027-01-31", deadline_precision="month",
    specificity="precise", volunteered=False, materiality=2)
add(said_on="2026-10-26", slug="jv2-close-h1-cy27", speaker=SMG, category="other",
    title="JV2 (high-voltage, Denso majority) to close in H1 of calendar 2027",
    quote="JV2 has not yet formed up but we are targeting to close and have it sometime in the 1st half of calendar year 2027.",
    metric="JV2 completion", target="by 30-Jun-2027", deadline="2027-06-30", deadline_precision="half-year",
    specificity="range", volunteered=False, materiality=2)
add(said_on="2026-10-26", slug="normal-margin-around-23pct", speaker=RN, category="margin",
    title="Normalised consolidated EBITDA margin 'around 23%' given product mix",
    quote="if the world is operating in a normal fashion then we should probably around 23% I don't hold us to like every 10 or 20 bps",
    metric="EBITDA margin (company)", target="~23%", deadline="2027-03-31", deadline_precision="vague",
    specificity="precise", volunteered=False, materiality=2,
    evidence="Restates 2026-04-30 '23-25%' at its floor - an acknowledged downward drift (24-25 -> 23-25 -> ~23) over 12 months.")
add(said_on="2026-10-26", slug="revenue-cagr-25pct-medium-term", speaker=VVS, category="revenue_growth",
    title="Medium-term aspiration implies ~25% revenue CAGR",
    quote="Pamod, in short we've already given our aspiration which actually does imply a 25% CAGR.",
    metric="Revenue CAGR", target="~25% p.a.", deadline="2030-03-31", deadline_precision="vague",
    specificity="precise", volunteered=False, materiality=3, conditionality="aspiration")

ANALYSIS_TITLE = "SONACOMS - Management Credibility Score (auto-components peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Promise tracker on Sona BLW (auto-components peer set). 6 concalls (Aug-2025 to Oct-2026); {n_promises} promises, {n_scored} scored. "
                 "Status counts: {status_counts}. Weighted delivery {weighted_delivery_ratio_pct}% (specificity-only {specificity_weighted_delivery_ratio_pct}%; hit rate {raw_hit_rate_pct}%); MCS {mcs_schema_scale}. "
                 "Sona refuses revenue guidance, so the scoreable record is thin: mix/BEV-share statements (delivered), the 24-25% FY26 margin target (delivered 24.7%) and a Q2FY27 margin-recovery statement (missed). "
                 "The margin band drifted down openly (24-25% -> 23-25% -> ~23%) - acknowledged, not hidden. Pending: JV1 close by Jan-2027, JV2 in H1 CY27, FY27 23-25% band. n is too small to rank. Research, not advice.")
