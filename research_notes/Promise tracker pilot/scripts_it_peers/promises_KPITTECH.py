# Promise ledger for KPIT Technologies (NSE: KPITTECH). Built 2026-11-22, IT mid-caps peer set.
# Method: pipeline v1.2 fetch/turns/candidates on the last 6 NSE transcripts (Q1FY26..Q2FY27; 590 candidates).
# The Q4FY26 file (filed under "MeghanaPhadnis_...") is a 22k-word investor-day style call with run-together OCR text.
# LLM step done by Claude by hand: opening remarks in full + targeted greps (EBITDA, 21%, H2, Q4, next quarter, FY27,
# constant currency, solutions and products) + later calls for outcomes.
# Same scoring as scripts_TD_peers/build_seed.py (clarifications A-D of TD_peer_comparison.md apply).
# KPIT guides EBITDA margin (company-reported) and growth shape, not a revenue number after FY25. Company EBITDA vs
# screener OPM: FY26 20.8% vs 18.9%; Q1/Q2 FY27 17.2% / 17.8% vs 15.3% / 15.8% (screener includes items KPIT excludes).
TICKER = "KPITTECH"
SCREENER = "https://www.screener.in/company/KPITTECH/consolidated/"
N = "https://nsearchives.nseindia.in/corporate/"
CALLS = {
    "2025-07-30": ("Q1FY26 concall transcript", N + "KPITTECH_06082025193155_CoverTransacriptJuly30_Signed.pdf"),
    "2025-11-10": ("Q2FY26 concall transcript", N + "KPITTECH_17112025223456_ransacriptNov10_Signed.pdf"),
    "2026-01-30": ("Q3FY26 concall transcript", N + "KPITTECH_06022026223507_CoverTranscript_Signed.pdf"),
    "2026-05-07": ("Q4FY26 concall / outlook transcript", N + "MeghanaPhadnis_13052026221810_covertranscript_Signed.pdf"),
    "2026-07-29": ("Q1FY27 concall transcript", N + "KPITTECH_04082026205946_KPIT_Transcript_Cov_let_signed.pdf"),
    "2026-10-28": ("Q2FY27 concall transcript", N + "KPITTECH_03112026220723_KPIT_Q2FY27_Transcript_Signed.pdf"),
}
KP = "Kishor Patil (Co-founder, CEO & MD)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q1FY26 (30-Jul-2025)
add(said_on="2025-07-30", slug="fy26-ebitda-21pct", speaker=KP, category="margin",
    title="Maintain ~21% EBITDA margin for FY26",
    quote="in a foreseeable future, we believe we can maintain the margins at 21% ... as long as it is in a reasonable way, we should be in a position to maintain it at 21% EBITDA",
    metric="EBITDA margin (company)", target="21%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=3, conditionality="barring currency",
    status="delivered", evidence="FY26 EBITDA 20.8% ('EBITDA growth margin is for the year 20.8%', Q4FY26 call), within 0.3 pp. Screener OPM FY26 18.9% (different classification).", delivered_value="20.8%", delivery_ratio=0.99, confidence="verified",
    later_restatements="2025-11-10 'we will be in a position to maintain 21% EBITDA for the full year'")
add(said_on="2025-07-30", slug="h2fy26-higher-than-h1", speaker=KP, category="revenue_growth",
    title="H2FY26 revenue higher than H1; growth momentum returns in H2",
    quote="we will be in a position to have certain wins and H2 will be higher than H1. And as we move into the second half, we will start gaining the growth momentum.",
    metric="Revenue H2FY26 vs H1FY26", target="H2 > H1", deadline="2026-03-31", deadline_precision="half-year",
    specificity="vague", volunteered=True, materiality=2,
    status="delivered", evidence="Screener sales H1FY26 1,539 + 1,588 = 3,127 cr; H2FY26 1,617 + 1,711 = 3,328 cr (+6.4%); CC QoQ Q3 +1.5%, Q4 +1.8% vs Q2 +0.3%.", delivered_value="H2 +6.4% vs H1 (INR)", delivery_ratio=1.0, confidence="verified")

# ---- Q2FY26 (10-Nov-2025)
add(said_on="2025-11-10", slug="q3-marginal-cc-growth-q4-meaningful", speaker=KP, category="revenue_growth",
    title="Q3FY26 marginal CC growth, Q4FY26 'meaningful growth'",
    quote="from next quarter we will start seeing marginal growth on constant currency terms and in Q4 there will be meaningful growth",
    metric="CC revenue growth QoQ Q3/Q4 FY26", target="Q3 >0%, Q4 meaningful", deadline="2026-03-31", deadline_precision="quarter",
    specificity="vague", volunteered=False, materiality=2,
    status="partly", evidence="Q3FY26 +1.5% CC QoQ (marginal: met); Q4FY26 +1.8% CC QoQ ('a bit of a muted growth year, but ultimately, we had a good Q4') - barely above Q3, hard to call 'meaningful' (a spike was implied).", delivered_value="1.5% / 1.8% CC QoQ", delivery_ratio=0.6)
add(said_on="2025-11-10", slug="fy26-ebitda-21pct-after-increments", speaker=KP, category="margin",
    title="Q3FY26 profitability: absorb increments in Q3-Q4 and still hold FY26 at 21%",
    quote="That would be considering the fact that we will be giving increments, some in next quarter and some in the quarter after. So, after giving that, I think we will be in a position to maintain our EBITDA margins at 21% for the whole year.",
    metric="EBITDA margin (company) H2FY26", target="~21% full year after increments", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="Q4FY26 EBITDA 20.6%; FY26 20.8% (company).", delivered_value="20.8% FY26", delivery_ratio=0.99)

# ---- Q3FY26 (30-Jan-2026)
add(said_on="2026-01-30", slug="q4fy26-highest-growth-quarter", speaker=KP, category="revenue_growth",
    title="Q4FY26 to be the highest-growth quarter of FY26, with profitability up from Q3",
    quote="in the last quarter that is Q4, we will improve, our growth will be higher, it will be the highest quarterly growth in FY26 ... And our profitability will improve from what we have in Q3",
    metric="CC revenue growth QoQ Q4FY26", target="highest QoQ of FY26", deadline="2026-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=2,
    status="delivered", evidence="Q4FY26 +1.8% CC QoQ vs Q3 +1.5%, Q2 +0.3%, Q1 +0.4% (company); Q4 EBITDA 20.6%.", delivered_value="1.8% CC QoQ", delivery_ratio=1.0)
add(said_on="2026-01-30", slug="fy27-growth-higher-than-fy26", speaker=KP, category="revenue_growth",
    title="FY27 growth to be higher than FY26 ('for sure')",
    quote="We will for sure grow next year higher than this year. And we believe that we will be in a position to do it.",
    metric="FY27 CC revenue growth vs FY26", target="FY27 growth > FY26 growth", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=3,
    evidence="Q1FY27 CC -3.6% QoQ, +0.1% YoY (two largest SDV programmes ended); Q2FY27 services flat, products +5% QoQ. Off track.")

# ---- Q4FY26 (07-May-2026)
add(said_on="2026-05-07", slug="fy27-ebitda-20-5-21-2pct", speaker=KP, category="margin",
    title="FY27 EBITDA margin 20.5-21.2% (after AI / products investment)",
    quote="it will drive profitability EBITDA 20.5 to 21.2 post increasing investment in AI solutions and products competency development and new markets",
    metric="EBITDA margin (company)", target="20.5-21.2%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    evidence="Given 7-May-2026; Q1FY27 EBITDA 17.2%, Q2FY27 17.8% (company). Q2FY27 CEO: margins 'will go up to some extent, every quarter, but, it will be early next year when we get there' - i.e. 20%+ only in FY28. A June-2026 mid-quarter update (not in these transcripts) reset Q2/Q4 expectations. GOALPOST FLAG: never explicitly withdrawn on a call; resolve at the deadline.")
add(said_on="2026-05-07", slug="fy27-solutions-products-plus-30pct", speaker=KP, category="revenue_growth",
    title="FY27 solutions & products revenue +30% YoY",
    quote="We expect 30% year-on-year revenue growth in solution and products, and we hope it will increase over the period.",
    metric="Solutions & products revenue growth", target=">=30% YoY", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    evidence="Q2FY27: products +25% YoY, +5% QoQ (company).")
add(said_on="2026-05-07", slug="ebitda-22-24pct-medium-term", speaker=KP, category="margin",
    title="Medium-term EBITDA 22-24% as solutions & products reach ~40% of revenue in 3 years",
    quote="So we expect the EBITDA to be between 22% to 24% from where we are today.",
    metric="EBITDA margin (company)", target="22-24%", deadline="2029-03-31", deadline_precision="vague",
    specificity="range", volunteered=True, materiality=2, conditionality="medium term")

# ---- Q1FY27 (29-Jul-2026)
add(said_on="2026-07-29", slug="return-to-growth-by-q4fy27", speaker=KP, category="revenue_growth",
    title="H2FY27 better than H1; return to QoQ growth by Q4FY27",
    quote="we have just mentioned that H2 will be better than H1, and we will return to growth in H2 by Q4, driven by the Q4 performance and our profitability will return largely when the revenues come",
    metric="CC revenue growth QoQ Q4FY27", target=">0% QoQ in Q4FY27; H2 > H1", deadline="2027-03-31", deadline_precision="quarter",
    specificity="vague", volunteered=True, materiality=3,
    evidence="Q2FY27: 'H2 will be better than H1. I think we will maintain that' and 'we expect growth in that quarter' (no number). Screener sales Q1FY27 1,675 cr, Q2FY27 1,691 cr.",
    later_restatements="2026-10-28 reiterated (H2 > H1, growth in Q4)")
add(said_on="2026-07-29", slug="margins-normal-by-q4fy27", speaker=KP, category="margin",
    title="EBITDA back to 'normal' (~20%+) by Q4FY27 as growth returns",
    quote="frankly, the large part is related to the growth and it really depends on that. But yes, fundamentally",
    metric="EBITDA margin Q4FY27 (company)", target="~20%+", deadline="2027-03-31", deadline_precision="quarter",
    specificity="vague", volunteered=False, materiality=2, conditionality="depends on growth",
    evidence="Endorsed an analyst's '20% plus by 4Q' framing; re-dated on 2026-10-28 to 'early next year when we get there' (Q4FY27 or Q1FY28; flag).")

# ---- Q2FY27 (28-Oct-2026)
add(said_on="2026-10-28", slug="ebitda-up-every-quarter", speaker=KP, category="margin",
    title="EBITDA margin to rise every quarter from Q2FY27's 17.8%",
    quote="I can only say right now it will go up to some extent, every quarter, but, it will be early next year when we get there.",
    metric="EBITDA margin QoQ (company)", target="Q3FY27 > 17.8% and Q4 > Q3", deadline="2027-03-31", deadline_precision="quarter",
    specificity="vague", volunteered=False, materiality=2)

ANALYSIS_TITLE = "KPITTECH - Management Credibility Score (IT mid-caps peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Promise tracker on KPIT Technologies (IT mid-caps peer set). 6 concalls (Jul-2025 to Oct-2026); {n_promises} promises, {n_scored} scored. "
                 "Status counts: {status_counts}. Weighted delivery {weighted_delivery_ratio_pct}% (specificity-only {specificity_weighted_delivery_ratio_pct}%; hit rate {raw_hit_rate_pct}%); MCS {mcs_schema_scale}. "
                 "Every FY26 statement resolved delivered or partly (21% EBITDA -> 20.8%; H2 > H1; Q4 highest growth quarter, though only +1.8% CC). "
                 "The record breaks at FY27: the 20.5-21.2% EBITDA guide given on 7-May-2026 met a 17.2% Q1 within weeks as the two largest SDV programmes ended, 'FY27 growth higher than FY26' is off track, and margin recovery has slid to 'early next year'. These are pending, so the score does not yet show it - a clear case where a good scored record coexists with a likely large miss. Research, not advice.")
