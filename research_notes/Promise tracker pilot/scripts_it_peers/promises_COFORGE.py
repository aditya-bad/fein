# Promise ledger for Coforge (NSE: COFORGE). Built 2026-11-22, IT mid-caps peer set.
# Method: Coforge files only cover letters on NSE ("transcript ... is available at the below link"), so all six
# transcripts (Q1FY26..Q2FY27) were downloaded from investors.coforge.com and fed with fetch.py --local PDF@FILED.
# turns.py + candidates.py (rules, v1.2 IT vocabulary) produced 326 candidates; LLM step done by Claude by hand:
# opening remarks in full (Coforge's CEO reads a numbered "key messages" list) + targeted greps (guidance, EBIT,
# FY27, ETR, free cash flow, Encora, Cigniti, large deals) + later calls for outcomes.
# Same scoring as scripts_TD_peers/build_seed.py (clarifications A-D of TD_peer_comparison.md apply).
# Coforge GUIDES explicitly (EBIT, EBITDA, FCF/PAT, ETR) - the opposite of Persistent. Q4FY26 restated revenue/EBIT
# to put realised hedge gains/losses in other income ("aligns our presentation with peer practice"); company EBIT is
# used throughout, screener-derived (OP-dep)/sales FY26 13.7% vs company 14.4%.
TICKER = "COFORGE"
SCREENER = "https://www.screener.in/company/COFORGE/consolidated/"
H = "https://investors.coforge.com/hubfs/"
CALLS = {
    "2025-07-24": ("Q1FY26 concall transcript (company website)", H + "Coforge%20Earnings%20Conference%20Call%20Transcript%20Q1FY26.pdf"),
    "2025-10-24": ("Q2FY26 concall transcript (company website)", H + "Coforge-Limited-Earnings-Call-Transcript-Q2-FY26.pdf"),
    "2026-01-23": ("Q3FY26 concall transcript (company website)", H + "Coforge-Limited-Earnings-Call-Transcript-Q3-FY26.pdf"),
    "2026-05-05": ("Q4FY26 concall transcript (company website)", H + "Coforge-Limited-Earnings-Call-Transcript-Q4FY26%20_AJ.pdf"),
    "2026-07-28": ("Q1FY27 concall transcript (company website)", H + "Coforge_Q1FY27%20Earnings%20Conference%20Call%20Transcript.pdf"),
    "2026-10-23": ("Q2FY27 concall transcript (company website)", H + "Coforge-Limited-Earnings-Call-Transcript-Q2FY27-October-23-2026.pdf"),
}
SS = "Sudhir Singh (CEO)"
SG = "Saurabh Goel (CFO)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q1FY26 (24-Jul-2025)
add(said_on="2025-07-24", slug="fy26-ebit-14pct", speaker=SG, category="margin",
    title="FY26 reported EBIT margin ~14% (from ~13% in Q1, exit ~15%)",
    quote="we were able to maintain EBIT margins and I am talking about EBIT because that is what the guidance is going forward",
    metric="EBIT margin (company, reported)", target="14%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=3,
    status="delivered", evidence="FY26 reported EBIT 14.4% ('14.4% reported EBIT in FY26', Q4FY26 call; +370 bp YoY). Screener-derived (OP-dep)/sales 13.7% (hedge-loss classification differs).", delivered_value="14.4%", delivery_ratio=1.03, confidence="verified",
    later_restatements="2025-10-24 'touch 14% in FY'26? - Yes'; 2026-01-23 '13.4% ... and our plan to register a 15% EBIT in Q4 will lead us to the 14% EBIT guidance'")
add(said_on="2025-07-24", slug="q2fy26-equally-robust-growth", speaker=SS, category="revenue_growth",
    title="Q2FY26 growth to be 'equally robust' as Q1 (~6% organic CC QoQ)",
    quote="we have grown organically, excluding acquisitions by almost 6% CC. I would expect Q2 also to be an equally robust quarter.",
    metric="CC revenue growth QoQ (organic)", target="~6% QoQ", deadline="2025-09-30", deadline_precision="quarter",
    specificity="vague", volunteered=False, materiality=2,
    status="delivered", evidence="Q2FY26 sequential CC growth 5.9% ('sequential CC growth of 8%, 5.9%, and 4.4% recorded between Q1 and Q3', Q4FY26 call).", delivered_value="5.9% CC QoQ", delivery_ratio=0.98)
add(said_on="2025-07-24", slug="h2fy26-robust", speaker=SS, category="revenue_growth",
    title="H2FY26 to be a 'robust second half'",
    quote="And H2, just using that term for a third time, should also be a robust second half for us.",
    metric="CC revenue growth H2FY26", target="robust (Q1-Q2 ran ~6-8% CC QoQ)", deadline="2026-03-31", deadline_precision="half-year",
    specificity="vague", volunteered=False, materiality=2,
    status="partly", evidence="Q3FY26 +4.4% CC QoQ, Q4FY26 +2.0% CC QoQ (slowest of the year); FY26 +29.2% USD. Robust in Q3, not in Q4; the Q4 slowdown was not flagged in advance.", delivered_value="4.4% / 2.0% CC QoQ", delivery_ratio=0.6, admitted_unprompted=False)
add(said_on="2025-07-24", slug="cigniti-merger-by-dec25-jan26", speaker=SG, category="m&a",
    title="Cigniti merger to complete by December 2025 / January 2026 ('minus a month or two')",
    quote="it is more with regulators so it would be minus a month or two, but December, January",
    metric="Cigniti amalgamation effective", target="by ~31-Jan-2026", deadline="2026-01-31", deadline_precision="month",
    specificity="range", volunteered=False, materiality=2,
    status="partly", evidence="Q3FY26 (23-Jan-2026): still awaiting NCLT; Q4FY26 (05-May-2026): 'Following the effective implementation of the Cigniti amalgamation' - effective around FY26 year-end (Mar-Apr 2026), ~2-3 months late, regulator-driven (NCLT meeting dates).", delivery_ratio=0.5, explanation_for_miss="NCLT/regulatory timetable", admitted_unprompted=True,
    later_restatements="2025-10-24 'getting completed by either December, Jan timeframe'")
add(said_on="2025-07-24", slug="q3-wage-hike-offset-by-esop", speaker=SG, category="margin",
    title="Q3FY26 wage-hike impact to be 'very, very limited', largely offset by 80-90 bp lower ESOP cost",
    quote="the wage hike impact is going to be very, very limited in Q3, which will largely get set off by the lower ESOP cost. We are looking at probably 80-90 BPS reduction on the account of ESOP cost",
    metric="EBIT margin Q3FY26 (company)", target="roughly flat QoQ vs Q2 14.0%", deadline="2025-12-31", deadline_precision="quarter",
    specificity="vague", volunteered=False, materiality=2,
    status="partly", evidence="Q3FY26 EBIT 13.4%, down 60 bp QoQ: wage hikes cost 150 bp, hedge losses 90 bp; ex-hedge 14.4% (company). The wage hit was larger than 'very, very limited' but the margin was held on the company's underlying basis.", delivered_value="13.4% reported / 14.4% ex-hedge", delivery_ratio=0.8, admitted_unprompted=True)

# ---- Q2FY26 (24-Oct-2025)
add(said_on="2025-10-24", slug="fcf-to-pat-70-80pct", speaker=SS, category="other",
    title="Free cash flow / PAT ~70-80% on a sustained basis",
    quote="we believe on a sustained basis, you should expect free cash flow to PAT at around 70% to 80% going forward",
    metric="FCF / PAT", target="70-80%", deadline="2026-03-31", deadline_precision="vague",
    specificity="range", volunteered=False, materiality=2,
    status="delivered", evidence="Q3FY26 110%, Q4FY26 110% (normalised 156%); FY26 FCF USD 135 mn (+68%). Guidance raised to 100% from FY27 (Q4FY26 call).", delivered_value="110% (Q3, Q4)", delivery_ratio=1.4)
add(said_on="2025-10-24", slug="etr-23-5-24pct-sustained", speaker=SG, category="other",
    title="Sustained effective tax rate ~23.5-24%",
    quote="ETR on a sustained basis is roughly 23.5% to 24% is what a sustained ETR is what we would maintain",
    metric="Effective tax rate (normalised)", target="23.5-24%", deadline="2026-03-31", deadline_precision="vague",
    specificity="range", volunteered=False, materiality=1,
    status="partly", evidence="FY26 normalised ETR 23%, reported 13% (Cigniti-merger tax true-up, Q4 ETR -7%). Normalised is 0.5 pp below the band floor (lower tax is not adverse, but the forecast was off); FY27 guide reset to 23-24%.", delivered_value="23% normalised / 13% reported", delivery_ratio=0.9)

# ---- Q3FY26 (23-Jan-2026)
add(said_on="2026-01-23", slug="q4fy26-ebit-15pct", speaker=SS, category="margin",
    title="Q4FY26 reported EBIT margin 15%",
    quote="our plan to register a 15% EBIT in Q4 will lead us to the 14% EBIT guidance for FY2026",
    metric="EBIT margin Q4FY26 (company)", target="15%", deadline="2026-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="Q4FY26 EBIT 16.6% ('a record 16.6%, up 231 basis points quarter on quarter', Q4FY26 call).", delivered_value="16.6%", delivery_ratio=1.1, confidence="verified")
add(said_on="2026-01-23", slug="encora-approvals-by-mar-apr26", speaker=SG, category="m&a",
    title="Encora acquisition approvals by March-April 2026, consolidation from then",
    quote="by March timeframe, we should be able to get pretty much all the approvals between March and April. And that is the time when we will start consolidating",
    metric="Encora closing", target="Mar-Apr 2026", deadline="2026-04-30", deadline_precision="month",
    specificity="range", volunteered=False, materiality=3,
    status="delivered", evidence="Q1FY27 revenue 'including two months of contribution from Encora' (US$100.7 mn) - consolidated from ~May-2026 (closing at end-April). Within the stated window.", delivery_ratio=1.0)
add(said_on="2026-01-23", slug="term-loan-no-qip", speaker=SG, category="debt_reduction",
    title="USD 550 mn 3-year term loan for Encora; no QIP needed",
    quote="We are very close to finalizing a term loan of $550 Mn for a period of 3 years ... we will not need to do a QIP for retiring the term loan",
    metric="Acquisition financing", target="term loan, no QIP", deadline="2026-09-30", deadline_precision="vague",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="Q1FY27: term-loan repayment schedule given (~$59 mn FY27, ~$209 mn FY28); no QIP announced through Nov-2026.", delivery_ratio=1.0)
add(said_on="2026-01-23", slug="no-eps-dilution-fy27-encora", speaker=SG, category="m&a",
    title="Encora: no EPS dilution in FY27 for the combined business (later 'EPS accretion in FY27')",
    quote="The guidance related to no dilution of EPS in FY27 of the combined business stays intact even after this debt.",
    metric="FY27 EPS vs FY26", target="not lower than FY26", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=3,
    evidence="Q1FY27/Q2FY27: 'we remain well on track to deliver EPS accretion in FY2027'; Q2FY27 EPS 13.3 vs 12.3 in Q1 (equity base +25%).",
    later_restatements="2026-07-28 and 2026-10-23 'on track to deliver EPS accretion in FY27'")

# ---- Q4FY26 (05-May-2026)
add(said_on="2026-05-05", slug="fy27-ebitda-20-5-21pct", speaker=SG, category="margin",
    title="FY27 consolidated EBITDA margin 20.5-21% (incl. Encora)",
    quote="EBITDA margins of 20.5% to 21% in FY27 on a consolidated basis, which is including Encora",
    metric="EBITDA margin (company, consolidated)", target="20.5-21%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    evidence="H1FY27 20.5% ('We remain confident of the guidance of 20.5% to 21% range', Q2FY27). Screener OPM Q1/Q2 FY27 19.1% / 19.8%.")
add(said_on="2026-05-05", slug="fy27-ebit-15-5pct-consol", speaker=SG, category="margin",
    title="FY27 consolidated EBIT margin 15.5% (incl. Encora); 16.5-17% standalone",
    quote="EBIT margins of 16.5% to 17% on a standalone basis, that is, excluding Encora, and 15.5% on a consolidated basis, which includes Encora",
    metric="EBIT margin (company, consolidated)", target="15.5%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    evidence="Q1FY27 16.0% consolidated (organic 16.7%), Q2FY27 16.0% (standalone 17%). Raised to 16% on 2026-10-23 (acknowledged upgrade).",
    later_restatements="2026-10-23 raised to 16% consolidated, Q4FY27 17%")
add(said_on="2026-05-05", slug="fy27-fcf-to-pat-100pct", speaker=SG, category="other",
    title="FCF / PAT ~100% from FY27 (raised from 70-80%)",
    quote="we anticipate free cash flow to PAT to be maintained at 100% from FY27 onwards in contrast to our earlier guidance of 70 to 80%",
    metric="FCF / PAT", target="100%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    evidence="Q1FY27 FCF $52.9 mn; Q2FY27 90% ('we expect it to be 100% for the year'); H1 conversion 92%.")
add(said_on="2026-05-05", slug="fy27-etr-23-24pct", speaker=SG, category="other",
    title="FY27 steady-state effective tax rate 23-24%",
    quote="Steady state effective tax rate guidance for FY27 is between 23% and 24%.",
    metric="Effective tax rate", target="23-24%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1)
add(said_on="2026-05-05", slug="fy27-highest-margin-midcap", speaker=SS, category="margin",
    title="From FY27, emerge as one of the highest EBITDA/EBIT performers among mid-caps while keeping revenue-growth leadership",
    quote="Starting in FY27, that is this year itself, we believe we will, along with retaining revenue growth leadership, emerge as one of the highest EBITDA and EBIT performers across the mid-cap segment.",
    metric="Relative EBIT and growth rank (mid-cap IT)", target="top tier on both", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=2)

# ---- Q1FY27 (28-Jul-2026)
add(said_on="2026-07-28", slug="encora-integration-cost-15mn", speaker=SG, category="m&a",
    title="Encora acquisition/integration expenses within the USD 15 mn budget",
    quote="We had guided for acquisition and integration-related expenses of $15 million at the time of acquisition, and we remain well within that budget.",
    metric="Exceptional acquisition expenses", target="<= USD 15-16 mn", deadline="2027-03-31", deadline_precision="vague",
    specificity="precise", volunteered=True, materiality=1,
    evidence="Q2FY27: 'we had guided for exceptional expenses of $15 to $16 [mn]'; 'no exceptional expenses in Q3 going forward'.")

# ---- Q2FY27 (23-Oct-2026)
add(said_on="2026-10-23", slug="fy27-ebit-16pct-q4-17pct", speaker=SS, category="margin",
    title="FY27 consolidated EBIT 16% (raised from 15.5%); reported Q4FY27 EBIT 17%",
    quote="We are pleased to raise our consolidated EBIT margin guidance for fiscal year 2027 to 16%, from the 15.5% we had shared at the beginning of the year. We also plan to achieve a reported Q4 EBIT of 17%",
    metric="EBIT margin (company, consolidated)", target="16% FY27; 17% Q4FY27", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    evidence="H1FY27 consolidated EBIT 16.0%.")
add(said_on="2026-10-23", slug="q3fy27-eight-large-deals", speaker=SS, category="deal_wins",
    title="Q3FY27: hope to sign eight, if not more, large deals (Q2 record was eight)",
    quote="in Q3, which has now started, which incidentally is the shortest quarter of the year, we hope to again sign eight, if not more large deals",
    metric="Large deals signed in Q3FY27", target=">=8", deadline="2026-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=2, conditionality="hope")
add(said_on="2026-10-23", slug="fy27-industry-growth-leader", speaker=SS, category="revenue_growth",
    title="FY27: industry growth leader for the third consecutive year",
    quote="This year, we will be the industry growth leader for the third consecutive year.",
    metric="FY27 revenue growth rank vs peers", target="#1 growth", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=2,
    evidence="Reported growth is inflated by Encora (consolidated from May-2026); organic Q2FY27 +3.8% QoQ.")

ANALYSIS_TITLE = "COFORGE - Management Credibility Score (IT mid-caps peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Promise tracker on Coforge (IT mid-caps peer set). 6 concalls (Jul-2025 to Oct-2026; transcripts from the company website - NSE has cover letters only); {n_promises} promises, {n_scored} scored. "
                 "Status counts: {status_counts}. Weighted delivery {weighted_delivery_ratio_pct}% (specificity-only {specificity_weighted_delivery_ratio_pct}%; hit rate {raw_hit_rate_pct}%); MCS {mcs_schema_scale}. "
                 "Coforge guides more explicitly than its peers (EBIT, EBITDA, FCF/PAT, ETR) and its hard margin and cash guidance was met or beaten (FY26 EBIT 14.4% vs 14%; Q4 16.6% vs 15%; FCF/PAT 110% vs 70-80%). "
                 "Weak spots are timing and growth-shape statements: the Cigniti merger ~2-3 months late (regulator), 'robust H2' with a 2% CC Q4, a Q3 wage hit larger than 'very limited'. "
                 "FY27 guidance (EBITDA 20.5-21%, EBIT raised 15.5% -> 16%, FCF/PAT 100%, no EPS dilution from Encora) is pending; H1 is on track. Research, not advice.")
