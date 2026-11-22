# Promise ledger for Mphasis (NSE: MPHASIS). Built 2026-11-22, IT mid-caps peer set.
# Method: pipeline v1.2 fetch on the last 6 NSE transcripts (Q1FY26..Q2FY27). turns.py failed on the Mphasis layout
# (speaker names on their own column; 0-3 management turns in 4 of 6 calls even with --roster), so the LLM step was
# done by Claude by hand on the raw pdftotext output: opening remarks in full (CEO + CFO "outlook" paragraphs) +
# targeted greps (band, 2x industry, guidance, FY27, DSO, logistics, insurance, cash flow) + later calls for outcomes.
# fetch.py dated the Q1FY26 call 2025-07-01 (wrong); the transcript header says 25-Jul-2025, used here.
# Same scoring as scripts_TD_peers/build_seed.py (clarifications A-D of TD_peer_comparison.md apply).
# Mphasis guides a CC growth range and an EBIT band (14.75-15.75%) every call. Company EBIT vs screener-derived
# (OP-dep)/sales: FY26 15.3% vs 15.3%; Q1/Q2 FY27 ~14.7% vs 14.8%/14.7% - close for Mphasis.
TICKER = "MPHASIS"
SCREENER = "https://www.screener.in/company/MPHASIS/consolidated/"
N = "https://nsearchives.nseindia.in/corporate/"
CALLS = {
    "2025-07-25": ("Q1FY26 concall transcript", N + "MPHASIS_29072025155615_IntimationoftranscriptJuly2025.pdf"),
    "2025-10-31": ("Q2FY26 concall transcript", N + "MPHASIS_05112025182431_Intimation_of_Transcript-signed.pdf"),
    "2026-01-22": ("Q3FY26 concall transcript", N + "MPHASIS_27012026181732_Intimation_of_transcript_-_22_January_2026-signed.pdf"),
    "2026-04-30": ("Q4FY26 concall transcript", N + "MPHASIS_04052026185004_SE_Intimation_-_transcript_-_30_April_2026-signed.pdf"),
    "2026-07-24": ("Q1FY27 concall transcript", N + "MPHASIS_28072026133016_Intimation_of_transcript_-_June_2026-signed.pdf"),
    "2026-11-06": ("Q2FY27 concall transcript", N + "MPHASIS_09112026150003_Intimation_of_transcript_-_Q2FY2027.pdf"),
}
NR = "Nitin Rakesh (CEO)"
AV = "Aravind Viswanathan (CFO)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q1FY26 (25-Jul-2025)
add(said_on="2025-07-25", slug="fy26-2x-industry-growth", speaker=AV, category="revenue_growth",
    title="FY26 revenue growth ~2x industry growth",
    quote="For FY26, we expect to be at ~2X industry growth, on the back of our Q1 performance and steady conversion of TCV to revenue",
    metric="FY26 CC revenue growth vs industry", target="~2x industry", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY26 CC growth 6.7% ('For the full year, revenues grew 6.7% in constant currency terms'); company: 'delivering more than 2x industry growth' (Q4FY26). 'Industry' is the company's own benchmark (large-cap peers ~2-3% CC) - single-source.", delivered_value="6.7% CC (>2x per company)", delivery_ratio=1.0,
    later_restatements="2025-10-31 and 2026-01-22 'greater than 2x of industry growth'")
add(said_on="2025-07-25", slug="fy26-ebit-band-14-75-15-75", speaker=AV, category="margin",
    title="FY26 EBIT margin within the 14.75-15.75% band",
    quote="Our target EBIT operating margin would be within the band of 14.75% to 15.75%.",
    metric="EBIT margin band (company)", target="14.75-15.75%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY26 EBIT 15.3% (Q1 15.3, Q2 15.3, Q3 15.2, Q4 15.4; company). Screener-derived (OP-dep)/sales FY26 15.3%.", delivered_value="15.3%", delivery_ratio=1.0, confidence="verified")
add(said_on="2025-07-25", slug="logistics-recover-rest-of-fy26", speaker=NR, category="revenue_growth",
    title="Logistics & Transportation vertical to recover gradually through the rest of FY26",
    quote="We believe the impact from these is largely behind us, and we expect this vertical to gradually recover through the remainder of the year.",
    metric="Logistics & Transportation vertical revenue", target="sequential recovery in FY26", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=2,
    status="moved-goalpost", evidence="Q3FY26: 'the headwind of the Logistics in one of the major customers through the year'; Q4FY26 re-dated: 'we do expect this to gradually recover through FY27' (no acknowledgement that the FY26 expectation was missed); Q2FY27: Logistics & Transportation -12.0% QoQ. Segment figures single-source.", delivery_ratio=0.0,
    later_restatements="2025-10-31 'start delivering sequential growth from Q3'; 2026-04-30 'gradually recover through FY27'")
add(said_on="2025-07-25", slug="insurance-momentum-fy26", speaker=NR, category="revenue_growth",
    title="Insurance vertical to continue its growth momentum in FY26",
    quote="our insurance vertical turned into a growth engine and is expected to continue the momentum in FY'26",
    metric="Insurance vertical growth", target="continued strong growth", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=1,
    status="delivered", evidence="Q4FY26: BFS 'healthy double digits and our Insurance business actually grew even more than that'; Q1FY27 Insurance +17.8% YoY CC.", delivery_ratio=1.0)

# ---- Q2FY26 (31-Oct-2025)
add(said_on="2025-10-31", slug="logistics-sequential-growth-from-q3", speaker=NR, category="revenue_growth",
    title="Logistics & Transportation to start delivering sequential growth from Q3FY26",
    quote="We expect the Logistics and Transportation vertical to start delivering sequential growth from Q3.",
    metric="Logistics & Transportation vertical QoQ growth", target="positive QoQ from Q3FY26", deadline="2025-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=2,
    status="missed", evidence="Q3FY26 call: continuing headwind from 'one of the major customers through the year'; vertical still a drag in Q1FY27 ('a little bit more headwinded given the macro') and -12.0% QoQ in Q2FY27. Single-source (segment).", delivery_ratio=0.0,
    explanation_for_miss="client-specific headwind, then macro/geopolitics", admitted_unprompted=False)
add(said_on="2025-10-31", slug="dso-normalise-3-4-quarters", speaker=AV, category="working_capital",
    title="DSO (89 days, up on fixed-price mix) to normalise over the next 3-4 quarters",
    quote="this change of business has seen an increase in DSO. We do expect normalization over the course of next three to four quarters.",
    metric="DSO (company)", target="back to ~84 days (pre-increase)", deadline="2026-09-30", deadline_precision="quarter",
    specificity="vague", volunteered=True, materiality=2,
    status="missed", evidence="DSO 89 (Q2FY26) -> 91 (Q3) -> ~86 adjusted (Q4) -> 95 (Q1FY27) -> 105 'after normalizing for the delayed remittances' (Q2FY27). Q2FY27: 'a quarterly aberration ... expected to get to double digit levels in Q3'.", delivered_value="105 days (Q2FY27, company-normalised)", delivery_ratio=0.0,
    explanation_for_miss="fixed-price mix; remittance delays at quarter-end", admitted_unprompted=True)
add(said_on="2025-10-31", slug="h2fy26-decent-growth", speaker=AV, category="revenue_growth",
    title="'Decent growth' in H2FY26 (strong Q3 expected after Q1 deal ramps)",
    quote="if you extrapolate what we are guiding for the remainder of the year, at least at a gross level, you can see that we should have decent growth in the second half of the year",
    metric="CC revenue growth QoQ H2FY26", target="decent (>2x industry pace)", deadline="2026-03-31", deadline_precision="half-year",
    specificity="vague", volunteered=False, materiality=2,
    status="delivered", evidence="Q3FY26 +1.5% QoQ CC (furlough quarter), Q4FY26 +2.5% QoQ CC; FY26 6.7% CC met the >2x guide.", delivered_value="1.5% / 2.5% CC QoQ", delivery_ratio=0.9)

# ---- Q3FY26 (22-Jan-2026)
add(said_on="2026-01-22", slug="direct-business-double-digit-trend", speaker=NR, category="revenue_growth",
    title="Direct business trending to double-digit YoY growth (template for future growth)",
    quote="our direct business is trending to double digit in Q3, potentially giving you a sense of what the template of growth is likely to be for the future",
    metric="Direct business CC growth YoY", target=">=10% YoY", deadline="2026-12-31", deadline_precision="vague",
    specificity="vague", volunteered=False, materiality=2,
    status="delivered", evidence="Direct CC YoY: Q3FY26 9.6%, Q1FY27 9.9%, Q2FY27 11.3% (company). Reached 10%+ only in Q2FY27.", delivered_value="11.3% (Q2FY27)", delivery_ratio=1.0)

# ---- Q4FY26 (30-Apr-2026)
add(said_on="2026-04-30", slug="fy27-cc-growth-hsd-to-ldd", speaker=AV, category="revenue_growth",
    title="FY27 revenue growth high single-digit to low double-digit (CC)",
    quote="we expect to deliver high single-digit to low double-digit growth, supported by disciplined execution and increasing demand for AI-led transformation in FY27",
    metric="FY27 CC revenue growth", target="7-12%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    evidence="Q1FY27 +8.3% YoY CC, Q2FY27 Direct +11.3% YoY CC. Raised on 2026-11-06 to 'low double digits' (acknowledged upgrade). Includes acquisitions (TAP / Red Oak).",
    later_restatements="2026-07-24 maintained; 2026-11-06 raised to low double digits")
add(said_on="2026-04-30", slug="fy27-ebit-band-14-75-15-75", speaker=AV, category="margin",
    title="FY27 EBIT margin within the 14.75-15.75% band",
    quote="From a margin perspective, we remain committed to operating within our target band of 14.75% to 15.75%",
    metric="EBIT margin band (company)", target="14.75-15.75%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    evidence="Q1FY27 down 60 bp QoQ (~14.8%; deal ramp + TAP acquisition costs); Q2FY27 flat. Screener-derived 14.8% / 14.7%. Near the floor.",
    later_restatements="2026-07-24 and 2026-11-06 'stable margins within the target band'")
add(said_on="2026-04-30", slug="fy27-ocf-to-ni-80pct", speaker=AV, category="other",
    title="FY27 operating cash flow / net income ~80%",
    quote="We also expect to maintain an operating cash flow to net income conversion ratio of approximately 80%.",
    metric="OCF / net income", target="~80%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    evidence="Q1FY27 OCF $39 mn; Q2FY27 $34 mn normalised; analysts flagged a large H2 ask (Q2FY27 Q&A).")
add(said_on="2026-04-30", slug="hedge-losses-taper-after-h1fy27", speaker=AV, category="margin",
    title="Hedge losses continue in H1FY27 then taper",
    quote="see continued impact of hedge losses in at least the first half of FY27 and then it will kind of taper down a bit",
    metric="Hedge losses", target="lower in H2FY27", deadline="2027-03-31", deadline_precision="half-year",
    specificity="vague", volunteered=False, materiality=1)

# ---- Q1FY27 (24-Jul-2026)
add(said_on="2026-07-24", slug="insurance-key-driver-fy27", speaker=NR, category="revenue_growth",
    title="Insurance to remain a key growth driver through FY27",
    quote="key growth driver for us through FY27",
    metric="Insurance vertical growth", target="above company growth", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=1)

# ---- Q2FY27 (06-Nov-2026)
add(said_on="2026-11-06", slug="fy27-cc-growth-low-double-digit", speaker=NR, category="revenue_growth",
    title="FY27 revenue growth 'low double digits' (raised from HSD-LDD)",
    quote="we are raising our FY27 guidance. We now expect revenue growth in the low double digits for the full year.",
    metric="FY27 CC revenue growth", target="10-12%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    evidence="H1FY27: Q1 +8.3% YoY CC (total), Q2 Direct +11.3% YoY CC. Raise rests on 'results already delivered' and backlog.")
add(said_on="2026-11-06", slug="dso-double-digit-q3fy27", speaker=AV, category="working_capital",
    title="DSO back to double digits (<100 days) in Q3FY27",
    quote="This is more of a quarterly aberration and is expected to get to double digit levels in Q3.",
    metric="DSO (company)", target="<100 days", deadline="2026-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1)
add(said_on="2026-11-06", slug="healthcare-growth-driver", speaker=NR, category="revenue_growth",
    title="Healthcare to emerge as a growth driver after a large deal win",
    quote="On the back of recent deal wins, including a large deal win this quarter, we expect Healthcare to emerge as a growth driver.",
    metric="Healthcare growth", target="above company growth", deadline="2027-09-30", deadline_precision="vague",
    specificity="vague", volunteered=True, materiality=1)

ANALYSIS_TITLE = "MPHASIS - Management Credibility Score (IT mid-caps peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Promise tracker on Mphasis (IT mid-caps peer set). 6 concalls (Jul-2025 to Nov-2026); {n_promises} promises, {n_scored} scored. "
                 "Status counts: {status_counts}. Weighted delivery {weighted_delivery_ratio_pct}% (specificity-only {specificity_weighted_delivery_ratio_pct}%; hit rate {raw_hit_rate_pct}%); MCS {mcs_schema_scale}. "
                 "Company-level guidance was met: FY26 '~2x industry' growth (6.7% CC) and the 14.75-15.75% EBIT band (15.3%, every quarter in the band). "
                 "Vertical and working-capital statements were not: Logistics recovery re-dated FY26 -> 'through FY27' without acknowledgement (moved-goalpost) and still falling; DSO 'normalise in 3-4 quarters' went 89 -> 105 days. "
                 "FY27 guidance (raised to low-double-digit CC growth; band held near its floor) is pending. turns.py could not parse the Mphasis layout; read from raw text. Research, not advice.")
