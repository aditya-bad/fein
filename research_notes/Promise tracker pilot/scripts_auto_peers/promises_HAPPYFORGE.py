# Promise ledger for Happy Forgings (NSE: HAPPYFORGE). Built 2026-11-22, auto-components peer set.
# Method as promises_SONACOMS.py. Last 6 NSE transcripts (Q1FY26..Q2FY27). Screener consolidated: FY26 revenue
# 1,546 cr (+9.7%), OPM 30.5% (company EBITDA 30.4%); H1FY27 revenue 950 cr (+30%), OPM ~30.9%.
TICKER = "HAPPYFORGE"
SCREENER = "https://www.screener.in/company/HAPPYFORGE/consolidated/"
N = "https://nsearchives.nseindia.in/corporate/"
CALLS = {
    "2025-08-11": ("Q1FY26 concall transcript", N + "9876964720_18082025121524_TranscriptEarningsCall.pdf"),
    "2025-11-07": ("Q2FY26 concall transcript", N + "9876964720_13112025134935_TranscriptOfEarningsCall.pdf"),
    "2026-02-10": ("Q3FY26 concall transcript", N + "9876964720_16022026172207_TranscriptOfEarningsCall.pdf"),
    "2026-05-22": ("Q4FY26 concall transcript", N + "9876964720_28052026180252_TranscriptOfEarningsCall28052026.pdf"),
    "2026-08-05": ("Q1FY27 concall transcript", N + "9876964720_11082026155459_TranscriptOfEarningsCall.pdf"),
    "2026-11-06": ("Q2FY27 concall transcript", N + "9876964720_13112026122617_TranscriptEarningscall13112026.pdf"),
}
AG = "Ashish Garg (MD)"
PG = "Pankaj Goyal (CFO)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q1FY26 (11-Aug-2025)
add(said_on="2025-08-11", slug="sustain-ebitda-margin-28-6pct", speaker=AG, category="margin",
    title="Sustain EBITDA margins around the Q1FY26 peak (28.6%) going forward",
    quote="our EBITDA margins stood at 28.6%, both around peak levels. We remain confident of sustaining these margins going forward as well.",
    metric="EBITDA margin", target=">= ~28.6%", deadline="2026-03-31", deadline_precision="vague",
    specificity="precise", volunteered=True, materiality=3,
    status="delivered", evidence="FY26 company EBITDA margin 30.4% (screener OPM 30.5%); every quarter Q2FY26..Q2FY27 >= 30.5% (screener).", delivered_value="30.4%", delivery_ratio=1.06, confidence="verified")
add(said_on="2025-08-11", slug="pv-share-8-10pct-2yrs", speaker=AG, category="other",
    title="Passenger-vehicle share of revenue to rise to 8-10% within two years (from 6%)",
    quote="We expect this segment to grow 8-10% of our total revenues over the next two years",
    metric="PV share of revenue", target="8-10%", deadline="2027-08-31", deadline_precision="vague",
    specificity="range", volunteered=True, materiality=2,
    later_restatements="2025-11-07 'contribute 8% to 10% of our total revenues within 2 years' (restates); 2026-08-05 'PV ... 12% to 15% of our revenues' (longer-term)")
add(said_on="2025-08-11", slug="presses-10000t-4000t-fy26", speaker=AG, category="capacity",
    title="Commission 10,000-t and 4,000-t presses during FY26 (+~20,000 MTPA)",
    quote="During the year, we expect additional commissioning for 10,000-ton press and 4,000-ton press with annual capacity addition of approximately 20,000 MTPA.",
    metric="Press commissioning", target="both in FY26", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    status="partly", evidence="10,000-t line commissioned Q4FY26 (Q4FY26 call); 4,000-t press slipped to Q1FY27 ('commissioning a new forging press in Q1 FY2027', Q2FY27 call). Slip acknowledged on 2026-02-10 ('4,000 ton press in H1 FY27').",
    delivery_ratio=0.5, admitted_unprompted=True)
add(said_on="2025-08-11", slug="us-pv-order-ramp-nov-dec-25", speaker=AG, category="other",
    title="US passenger-vehicle order to ramp up from Nov-Dec 2025",
    quote="Even for the US market, we have expected ramp up this year from November, December for one of the large PV order wins",
    metric="US PV programme ramp-up", target="from Nov-Dec 2025", deadline="2025-12-31", deadline_precision="month",
    specificity="precise", volunteered=False, materiality=2,
    status="missed", evidence="Q2FY27 call: 'this line was commissioned for a North American client for PV application, and for which we have started ramping up in Q1 and Q2' (FY27) - about two quarters late; no explanation volunteered.",
    delivery_ratio=0.0, admitted_unprompted=False)
add(said_on="2025-08-11", slug="heavy-capex-650cr-done-q2-q3-fy27", speaker=AG, category="capacity",
    title="INR 650 cr heavy-component capex finished by Q2-Q3 FY27",
    quote="Because right now, we are in a phase where it is coming up and the CAPEX will get finished by, say, second quarter or third quarter of next financial",
    metric="Heavy-component plant completion", target="by Q3FY27 (Dec-2026)", deadline="2026-12-31", deadline_precision="quarter",
    specificity="range", volunteered=False, materiality=3,
    status="moved-goalpost", evidence="2025-11-07 'will probably start from third quarter of next year'; 2026-02-10 'on track ... as per the schedule', utilisation 'some bit from FY28'; 2026-05-22 'by end of FY27 we expect to complete our large capex ... trials early FY28'; 2026-11-06 'going as per the scheduled timelines ... expected to be completed and commence operation in the quarter four of FY2028'. Five quarters later than first stated while each call says 'on schedule' - a silent goalpost move. Scored before the Dec-2026 deadline because the company's own latest date makes it unreachable.",
    delivery_ratio=0.0, admitted_unprompted=False, confidence="verified")

# ---- Q2FY26 (07-Nov-2025)
add(said_on="2025-11-07", slug="inorganic-deal-6-8-months", speaker=AG, category="other",
    title="Close an inorganic (M&A) deal within 6-8 months",
    quote="We are very hopeful that in next 6 to 8 months, probably we should be able to close something on the inorganic side as well.",
    metric="Acquisition closed", target="by ~Jul-2026", deadline="2026-07-31", deadline_precision="month",
    specificity="precise", volunteered=False, materiality=1, conditionality="hopeful",
    status="missed", evidence="No acquisition announced or mentioned in the Q4FY26, Q1FY27 or Q2FY27 calls (grep 'inorganic|acquisition'); not raised again by management.", delivery_ratio=0.0, admitted_unprompted=False)
add(said_on="2025-11-07", slug="fy27-growth-trajectory-better", speaker=AG, category="revenue_growth",
    title="Growth trajectory better from FY27 ('back on a full trend')",
    quote="So, on the growth side, we expect that from next year onwards, the growth trajectory should be better, and we should be back on a full trend.",
    metric="Revenue growth FY27 vs FY26 (+9.7%)", target="FY27 growth > FY26", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=2, evidence="H1FY27 revenue +30% (screener).")
add(said_on="2025-11-07", slug="return-ratios-improve", speaker=PG, category="other",
    title="Return ratios to improve going forward",
    quote="And we expect this return ratio to improve going forward.",
    metric="ROCE", target="> FY25 (19%)", deadline="2027-03-31", deadline_precision="vague",
    specificity="vague", volunteered=True, materiality=1, evidence="Screener ROCE FY26 18% (FY25 19%).")

# ---- Q3FY26 (10-Feb-2026)
add(said_on="2026-02-10", slug="ebitda-29-31pct-medium-term", speaker=AG, category="margin",
    title="EBITDA margin sustained in a 29-31% range over the medium term",
    quote="Our focus remains on maintaining EBITDA margins within a sustained range between 29% to 31% over the medium term.",
    metric="EBITDA margin", target="29-31%", deadline="2028-03-31", deadline_precision="vague",
    specificity="range", volunteered=True, materiality=3, evidence="FY26 30.4%; Q1FY27 31.4%, Q2FY27 30.5% (screener).")
add(said_on="2026-02-10", slug="10000t-q4fy26-4000t-h1fy27", speaker=AG, category="capacity",
    title="New 10,000-t press in Q4FY26 and 4,000-t press in H1FY27",
    quote="we will strengthen our forging capacities by commissioning a new 10,000 ton press in quarter 4 FY '26 and the 4,000 ton press in H1 FY '27",
    metric="Press commissioning", target="Q4FY26 / H1FY27", deadline="2026-09-30", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="10,000-t commissioned Q4FY26 (Q4FY26 call); new forging press commissioned Q1FY27 and an extra hammer in Q2FY27 (Q2FY27 call).", delivery_ratio=1.0)
add(said_on="2026-02-10", slug="fy26-capex-400-500cr", speaker=PG, category="capacity",
    title="FY26 total capex INR 400-500 cr",
    quote="we expected our total capex for FY '26 to be in the range of INR400 crores to INR500 crores",
    metric="Capex FY26", target="INR 400-500 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    status="delivered", evidence="'capex of around Rs.460 crores deployed during FY 26' (Q4FY26 call). (In Aug-2025 the FY26 plan was ~INR 300 cr ex-solar; raised openly.)", delivered_value="INR 460 cr", delivery_ratio=1.0)
add(said_on="2026-02-10", slug="solar-power-savings-from-q3fy27", speaker=AG, category="capacity",
    title="Captive solar plant to start cutting power cost from Q3 FY27 (INR 25-30 cr p.a.)",
    quote="with regard to the solar project, which is coming up, we expect that to also improve our power cost starting from third quarter",
    metric="Solar plant generation start", target="from Q3FY27", deadline="2026-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1,
    evidence="2026-05-22: 'partial benefits starting from FY28'; 2026-11-06: 'we expect some generations to happen in Q4' - re-dated twice; goalpost flag, resolve at deadline.")

# ---- Q4FY26 (22-May-2026)
add(said_on="2026-05-22", slug="fy27-late-teen-volume-margin-flat", speaker=AG, category="revenue_growth",
    title="FY27 late-teen volume growth with EBITDA margin broadly in line with FY26",
    quote="We expect late-teen volume growth for the business while maintaining EBITDA margins broadly in line with FY '26 levels.",
    metric="FY27 volume growth (and margin ~30.4%)", target="+17-19% volume", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    evidence="Restated 2026-08-05 and 2026-11-06 ('well-positioned to meet our full-year volume growth guidance'). H1FY27 finished-goods volume +24%, revenue +30%.")
add(said_on="2026-05-22", slug="fy27-capex-450-500cr", speaker=PG, category="capacity",
    title="FY27 capex INR 450-500 cr",
    quote="Looking ahead, we expect total capex for FY '27 to be in the range of Rs.450 crores to Rs.500 crores",
    metric="Capex FY27", target="INR 450-500 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1, evidence="H1FY27 spend ~INR 378 cr; additional INR 500 cr programme approved 2026-11-06.")
add(said_on="2026-05-22", slug="fy27-cv-growth-35-40pct", speaker=AG, category="revenue_growth",
    title="FY27 CV segment growth 35-40% on new programmes",
    quote="So CV alone, we are expecting almost 35%, 40% growth this year for us because of the new programs and the new ramp-ups",
    metric="CV segment revenue growth FY27", target="+35-40%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=2,
    evidence="Q1FY27: CV 'healthy single-digit growth' (domestic +18%) - well short so far.")
add(said_on="2026-05-22", slug="forging-capacity-161k-fy27", speaker=AG, category="capacity",
    title="Forging capacity to 161,000 t by FY27 (from 147,000)",
    quote="So forging capacities in the last year have ramped up from 125,000 to 147,000, which is further expected to go up to 161,000 by FY '27.",
    metric="Forging capacity", target="161,000 t", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1)

# ---- Q1FY27 (05-Aug-2026)
add(said_on="2026-08-05", slug="margin-upwards-of-30pct", speaker=AG, category="margin",
    title="EBITDA margin 'upwards of 30%' going forward (power savings +1-1.5 pp)",
    quote="So I'm quite confident that, you know, we should be seeing upwards of 30% going forward.",
    metric="EBITDA margin", target=">30%", deadline="2027-03-31", deadline_precision="vague",
    specificity="precise", volunteered=False, materiality=2)

# ---- Q2FY27 (06-Nov-2026)
add(said_on="2026-11-06", slug="close-500cr-orders-by-mar27", speaker=AG, category="other",
    title="Close ~INR 500 cr of new orders (data-centre / heavy) by March 2027",
    quote="As I have mentioned that by March, we will have orders of close to Rs.500 crores.",
    metric="New order wins", target="~INR 500 cr", deadline="2027-03-31", deadline_precision="month",
    specificity="precise", volunteered=False, materiality=2,
    evidence="Also: 'We aim to close nearly Rs.500 crores of orders by this financial year'.")
add(said_on="2026-11-06", slug="heavy-plant-ops-q4fy28", speaker=AG, category="capacity",
    title="Heavy-component plant (+20 MW solar) completed and operating in Q4 FY28",
    quote="This facility, with our 20 MW captive solar power plant, is expected to be completed and commence operation in the quarter four of FY2028.",
    metric="Heavy plant start", target="Q4FY28", deadline="2028-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=3)

ANALYSIS_TITLE = "HAPPYFORGE - Management Credibility Score (auto-components peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Promise tracker on Happy Forgings (auto-components peer set). 6 concalls (Aug-2025 to Nov-2026); {n_promises} promises, {n_scored} scored. "
                 "Status counts: {status_counts}. Weighted delivery {weighted_delivery_ratio_pct}% (specificity-only {specificity_weighted_delivery_ratio_pct}%; hit rate {raw_hit_rate_pct}%); MCS {mcs_schema_scale}. "
                 "Margin and near-term capacity promises are reliable (EBITDA 30.4% vs 'sustain 28.6%'; presses one quarter late at most; FY26 capex in range). "
                 "Dates on large projects and customer ramps are not: the INR 650 cr heavy-component plant moved from Q2-Q3 FY27 to Q4 FY28 while every call said 'as per schedule'; a US PV ramp came two quarters late; a hoped-for acquisition did not happen. "
                 "Most FY27 guidance (late-teen volume, margin ~30%) is pending and on track at H1. Research, not advice.")
