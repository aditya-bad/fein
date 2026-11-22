# Promise ledger for Endurance Technologies (NSE: ENDURANCE). Built 2026-11-22, auto-components peer set.
# Method as promises_SONACOMS.py. Last 6 NSE transcripts (Q1FY26..Q2FY27). Endurance gives no revenue/margin
# guidance; its promises are SOP (start-of-production) dates, capex and order-win targets, so this ledger is
# mostly the 'capacity' category. Screener consolidated: FY26 revenue 14,596 cr (+26%), OPM 13.5%.
TICKER = "ENDURANCE"
SCREENER = "https://www.screener.in/company/ENDURANCE/consolidated/"
N = "https://nsearchives.nseindia.in/corporate/"
CALLS = {
    "2025-08-14": ("Q1FY26 concall transcript", N + "ENDURANCE_22082025153100_20250822TranscriptofEarningsConferenceCallon14082025.pdf"),
    "2025-11-13": ("Q2FY26 concall transcript", N + "ENDURANCE_20112025174935_2025_11_20_-_Transcript_of_Earnings_Conference_Call_on_13_11_2025.pdf"),
    "2026-02-13": ("Q3FY26 concall transcript", N + "ENDURANCE_19022026174447_Transcript.pdf"),
    "2026-05-15": ("Q4FY26 concall transcript", N + "ENDURANCE_22052026142524_2026_05_22_-_Transcript_of_EarningsCall.pdf"),
    "2026-08-14": ("Q1FY27 concall transcript", N + "ENDURANCE_21082026161009_2026_08_21_-_Transcript_of_Earnings_Conference_Call_on_14_08_2026.pdf"),
    "2026-11-04": ("Q2FY27 concall transcript", N + "ENDURANCE_12112026183008_2026_11_12_-_Transcript_of_Earnings_Conference_Call_on_04_11_2026.pdf"),
}
AJ = "Anurang Jain (MD)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q1FY26 (14-Aug-2025)
add(said_on="2025-08-14", slug="dual-channel-abs-sop-sep25", speaker=AJ, category="capacity",
    title="Dual-channel ABS SOP (Royal Enfield / Bajaj) next month (Sep-2025)",
    quote="our dual-channel ABS final samples have been sent to Royal Enfield and Bajaj, and we expect SOP to start next month.",
    metric="Dual-channel ABS SOP", target="Sep-2025", deadline="2025-09-30", deadline_precision="month",
    specificity="precise", volunteered=True, materiality=2,
    status="missed", evidence="Re-dated 2026-02-13 ('now expected to start next month, as we await the final clearance from a key OEM'), 2026-05-15 ('June 2026 for Bajaj'), 2026-08-14 ('this quarter'); 2026-11-04: 'supplies to Bajaj Auto has started in October this year' - 13 months late. Each re-date was stated openly with a customer-clearance reason.",
    delivery_ratio=0.0, admitted_unprompted=True, explanation_for_miss="awaiting OEM final clearance")
add(said_on="2025-08-14", slug="abs-new-lines-ready-mar26", speaker=AJ, category="capacity",
    title="New ABS capacity lines ready by March 2026",
    quote="So, we are going ahead because we want to be ready with the capacity, which I said should be by March 2026.",
    metric="ABS expansion ready", target="by Mar-2026", deadline="2026-03-31", deadline_precision="month",
    specificity="precise", volunteered=False, materiality=2,
    status="missed", evidence="2025-11-13: first 1.2 mn line 'operational in Quarter 1 FY 27', second line tied to final ABS-mandate guidelines; 2026-05-15 'SOP expected in September 2026'; 2026-08-14 'September or early October 2026'. About two quarters late; explained by the government's delayed ABS guidelines (sector-wide).",
    delivery_ratio=0.0, admitted_unprompted=True, explanation_for_miss="ABS mandate guidelines not notified")

# ---- Q2FY26 (13-Nov-2025)
add(said_on="2025-11-13", slug="chennai-disc-brake-sop-q2fy27", speaker=AJ, category="capacity",
    title="New Chennai disc-brake plant SOP in Q2 FY27",
    quote="We have started civil work for setting up a new Chennai plant for disc brake systems, which includes the master cylinder, caliper, brake disc and brake hoses, where we expect SOP in Q2 FY '27.",
    metric="Chennai plant SOP", target="Q2FY27 (by Sep-2026)", deadline="2026-09-30", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=2,
    status="moved-goalpost", evidence="2026-05-15 'SOP for Royal Enfield is planned in July 2026'; 2026-08-14 'expected by next month'; 2026-11-04: 'At our new Chennai plant for disc brake assembly systems, the SOP will start in March 2027' - re-dated two quarters with no reason given.",
    delivery_ratio=0.0, admitted_unprompted=False)
add(said_on="2025-11-13", slug="hero-sop-within-fy26", speaker=AJ, category="capacity",
    title="SOP for Hero MotoCorp (BMS / electronics) within FY26",
    quote="The SOP for another OEM Hero MotoCorp is planned within this financial year, while SOP for a leading Chinese 2W OEM is expected to start in Q1 of FY 27.",
    metric="Hero SOP", target="by Mar-2026", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="'The SOP for Hero MotoCorp started in January 2026' (Q3FY26 call).", delivery_ratio=1.0)
add(said_on="2025-11-13", slug="chinese-2w-oem-sop-q1fy27", speaker=AJ, category="capacity",
    title="SOP for a leading Chinese 2W OEM in Q1 FY27",
    quote="while SOP for a leading Chinese 2W OEM is expected to start in Q1 of FY 27",
    metric="Chinese OEM SOP", target="Q1FY27", deadline="2026-06-30", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="moved-goalpost", evidence="2026-02-13: 'validation is ongoing for a leading Chinese OEM, with SOP expected in Q3 of FY 27' - re-dated by two quarters without acknowledging the change.",
    delivery_ratio=0.0, admitted_unprompted=False)
add(said_on="2025-11-13", slug="win-1500cr-business-12-18m", speaker=AJ, category="other",
    title="Win more than INR 1,500 cr of new business in the next 12-18 months",
    quote="We expect to win more than Rs 1,500 crores of business in the next 12 to 18 months.",
    metric="New business wins (lifetime/peak)", target=">INR 1,500 cr", deadline="2027-05-31", deadline_precision="vague",
    specificity="precise", volunteered=True, materiality=2, evidence="Restated verbatim 2026-02-13.")

# ---- Q3FY26 (13-Feb-2026)
add(said_on="2026-02-13", slug="fy26-india-capex-below-800cr", speaker=AJ, category="capacity",
    title="FY26 India capex slightly less than INR 800 cr",
    quote="This year, we will be slightly less than ₹ 800 crores, largely because of these 4 new facilities, plus expansions which we are doing in Brakes.",
    metric="Capex FY26 (India)", target="< ~INR 800 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="delivered", evidence="2026-08-14: 'similar to the FY 26 capex of ₹ 800 crores'.", delivered_value="~INR 800 cr", delivery_ratio=1.0)
add(said_on="2026-02-13", slug="fy27-india-capex-much-below-800cr", speaker=AJ, category="capacity",
    title="FY27 India capex to be 'much below' INR 800 cr",
    quote="But according to me, in India, the CAPEX will be controlled much below this figure of ₹ 800 crores.",
    metric="Capex FY27 (India)", target="well below INR 800 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=1,
    status="missed", evidence="2026-05-15 'similar to FY 26'; 2026-08-14 'similar to the FY 26 capex of ₹ 800 crores'; 2026-11-04 'We expect capital expenditure in FY 27 to be around ₹ 1,100 crores' (consolidated 1,250). Scored before the deadline on the company's own latest guide; revisions were stated openly (new programmes).",
    delivery_ratio=0.0, admitted_unprompted=True)
add(said_on="2026-02-13", slug="bajaj-sop-q2fy27", speaker=AJ, category="capacity",
    title="SOP for Bajaj Auto (new product line) in Q2 FY27",
    quote="The SOP for Bajaj Auto is expected in Q2 of FY 27.",
    metric="Bajaj SOP", target="Q2FY27", deadline="2026-09-30", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="moved-goalpost", evidence="2026-08-14 'For Bajaj Auto, SOP is expected in the next quarter'; 2026-11-04 'customer validation is in process and SOP is expected in Q4 of this financial year'.",
    delivery_ratio=0.0, admitted_unprompted=False)
add(said_on="2026-02-13", slug="tata-drum-brake-sop-q1fy27", speaker=AJ, category="capacity",
    title="4W drum-brake line for Tata Motors: SOP in Q1 FY27",
    quote="We have also installed an assembly line for 4W passenger vehicle drum brakes for Tata Motors, with SOP expected in Q1 of FY 27.",
    metric="Tata drum-brake SOP", target="Q1FY27", deadline="2026-06-30", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="unverifiable", evidence="Not confirmed or re-dated in later calls read (only 'we also established our assembly line', May-26).")

# ---- Q4FY26 (15-May-2026)
add(said_on="2026-05-15", slug="forging-plant-sop-q3fy27", speaker=AJ, category="capacity",
    title="New aluminium forging plant (fifth press) SOP in Q3 FY27",
    quote="All our presses will be set up in a new forging plant at Chhatrapati Sambhajinagar, which will start SOP in Q3 of this financial year.",
    metric="Forging plant / fifth press SOP", target="Q3FY27 (by Dec-2026)", deadline="2026-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    evidence="2026-08-14 'fifth forging press with SOP expected in the next quarter'; 2026-11-04 'fifth aluminum forging press with SOP expected in Q4 of FY 27' - goalpost flag, resolve at deadline.")
add(said_on="2026-05-15", slug="isuzu-hybrid-sop-q4fy27", speaker=AJ, category="capacity",
    title="Isuzu hybrid-model castings (Chennai) SOP by Q4 FY27",
    quote="At our Chennai plant, we have secured orders for hybrid models of Isuzu, with SOP expected by Q4 of this year.",
    metric="Isuzu SOP", target="by Mar-2027", deadline="2027-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1, evidence="Restated 2026-08-14.")

# ---- Q1FY27 (14-Aug-2026)
add(said_on="2026-08-14", slug="q2-margin-improves-on-q1-base", speaker=AJ, category="margin",
    title="Q2FY27 EBITDA margin to improve on the higher Q1 revenue base",
    quote="Now in Q2, we'll be operating on the Q1 base which is definitely much higher than the Q4 base and that should improve the EBITDA margin and percentage.",
    metric="EBITDA margin Q2FY27 vs Q1FY27", target="> Q1FY27 (screener 12.4%)", deadline="2026-09-30", deadline_precision="quarter",
    specificity="vague", volunteered=False, materiality=2,
    status="missed", evidence="Screener consolidated OPM Q1FY27 12.4% -> Q2FY27 11.7%. Q2FY27 call attributes drag to four new plants (-0.5% PBT) and steel/aluminium prices.", delivered_value="11.7%", delivery_ratio=0.0, admitted_unprompted=True, confidence="single-source")
add(said_on="2026-08-14", slug="4w-battery-pack-sop-q4fy27", speaker=AJ, category="capacity",
    title="4W battery packs: SOP by Q4 FY27 (INR 62 cr capex)",
    quote="We have also announced our entry into 4W battery packs from the same plant with a capex of ₹ 62 crores and we expect SOP by Q4 of this financial year.",
    metric="4W battery pack SOP", target="by Mar-2027", deadline="2027-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1)
add(said_on="2026-08-14", slug="tata-4w-driveshaft-sop-q3fy27", speaker=AJ, category="capacity",
    title="4W driveshaft SOP for Tata Motors next quarter (Q3 FY27)",
    quote="In our 4W driveshaft program, SOP for Tata Motors is expected also in the next quarter",
    metric="Tata 4W driveshaft SOP", target="Q3FY27 (by Dec-2026)", deadline="2026-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1, evidence="Restated 2026-11-04 'expected in this quarter'.")
add(said_on="2026-08-14", slug="alloy-wheels-full-capacity-fy27", speaker=AJ, category="capacity",
    title="Alloy-wheel plants at full capacity by end FY27",
    quote="So, I would say by end of this financial year, we should be at full capacities for as far as alloy wheels is concerned.",
    metric="Alloy-wheel utilisation", target="full by Mar-2027", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=1)

# ---- Q2FY27 (04-Nov-2026)
add(said_on="2026-11-04", slug="chennai-disc-brake-sop-mar27", speaker=AJ, category="capacity",
    title="Chennai disc-brake plant SOP in March 2027 (re-dated)",
    quote="At our new Chennai plant for disc brake assembly systems, the SOP will start in March 2027.",
    metric="Chennai plant SOP", target="Mar-2027", deadline="2027-03-31", deadline_precision="month",
    specificity="precise", volunteered=True, materiality=2)
add(said_on="2026-11-04", slug="driveshaft-revenue-over-100cr-fy27", speaker=AJ, category="revenue_growth",
    title="Driveshaft revenue to cross INR 100 cr in FY27",
    quote="we expect our driveshaft revenue to cross ₹ 100 crores in FY 27",
    metric="Driveshaft revenue FY27", target=">INR 100 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1)
add(said_on="2026-11-04", slug="fy27-capex-1100cr", speaker=AJ, category="capacity",
    title="FY27 capex ~INR 1,100 cr standalone (INR 1,250 cr consolidated)",
    quote="We expect capital expenditure in FY 27 to be around ₹ 1,100 crores. Our consolidated capex is expected to be ₹ 1,250 crores.",
    metric="Capex FY27", target="~INR 1,100 cr / 1,250 cr consol", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1)
add(said_on="2026-11-04", slug="psi-incentive-50cr-h2", speaker=AJ, category="other",
    title="Book a further INR 50 cr of PSI incentives in H2 FY27",
    quote="In half one of this year, we have booked an income of ₹ 75 crores against this PSI incentives and expect to book a further ₹ 50 crores in half two of this financial year.",
    metric="PSI incentive income H2FY27", target="~INR 50 cr", deadline="2027-03-31", deadline_precision="half-year",
    specificity="precise", volunteered=True, materiality=1)

ANALYSIS_TITLE = "ENDURANCE - Management Credibility Score (auto-components peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Promise tracker on Endurance Technologies (auto-components peer set). 6 concalls (Aug-2025 to Nov-2026); {n_promises} promises, {n_scored} scored. "
                 "Status counts: {status_counts}. Weighted delivery {weighted_delivery_ratio_pct}% (specificity-only {specificity_weighted_delivery_ratio_pct}%; hit rate {raw_hit_rate_pct}%); MCS {mcs_schema_scale}. "
                 "Endurance gives no revenue or margin guidance; it gives many SOP dates, and most of them slip 1-4 quarters (dual-channel ABS 13 months; Chennai brakes Q2 -> March 2027; Bajaj, Chinese OEM). "
                 "Some slips are explained (OEM clearance, ABS-mandate guidelines), others re-dated silently. Group revenue still grew 26% in FY26, so date slips have not yet hurt the P&L. Research, not advice.")
