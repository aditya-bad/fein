# Promise ledger for Kalpataru Projects International (NSE: KPIL). Same method/thresholds as scripts_SKIPPER
# (plus clarifications A and B in promises_KEC.py header). Built 2026-11-21.
# Transcripts from kalpataruprojects.com (NSE filings for KPIL are cover letters pointing there). The Q2FY27 call
# transcript (Nov-2026) was not yet downloadable; the Q2FY27 investor presentation (BSE, 05-Nov-2026) is used for H1FY27 actuals.
# KPIL guides on STANDALONE revenue/PBT and CONSOLIDATED order inflow; both are checked. Screener standalone quarterly
# finance cost matches company % (e.g. Q3FY25 107/4,826 = 2.2%).
TICKER = "KPIL"
SCREENER = "https://www.screener.in/company/KPIL/consolidated/"
W = "https://kalpataruprojects.com/api/view-file/"
PRES_Q2FY27 = "https://www.bseindia.com/xml-data/corpfiling/AttachHis/aa471fd5-764a-4c79-9732-96785b3ad1cc.pdf"
SA = "https://www.screener.in/company/KPIL/"
CALLS = {
    "2025-02-14": ("Q3FY25 concall transcript", W + "KPIL_Q3_FY25_Transcript.pdf"),
    "2025-05-19": ("Q4FY25 concall transcript", W + "KPIL_Q4_FY25_Transcript.pdf"),
    "2025-08-08": ("Q1FY26 concall transcript", W + "KPIL_Q1FY26_transcript.pdf"),
    "2025-10-31": ("Q2FY26 concall transcript", W + "KPIL_Q2_FY26_Transcript.pdf"),
    "2026-02-05": ("Q3FY26 concall transcript", W + "KPIL_Q3_FY26_Earnings_Call_Transcript-5th_feb_2026.pdf"),
    "2026-05-15": ("Q4FY26 concall transcript", W + "KPILQ4_FY26_Earnings_Call_Transcript_final.pdf"),
    "2026-08-11": ("Q1FY27 concall transcript", W + "KPIL_Q1%20FY27_Earnings%20Call%20Transcript.pdf"),
}
MM = "Manish Mohnot (MD & CEO)"
SKT = "S.K. Tripathi (Deputy MD)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---------------- Q3FY25 (14-Feb-2025) ----------------
add(said_on="2025-02-14", slug="fy25-revenue-consol-13-15pct", speaker=MM, category="revenue_growth",
    title="FY25 consolidated revenue growth 13-15% (cut from 18-20% for water)",
    quote="we believe we should be more in the range of 13% to 15% for annualized basis at a consol basis and standalone maybe 12% to 13%",
    metric="Consolidated revenue growth", target="+13-15%", deadline="2025-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="delivered", evidence="FY25 consol revenue INR 22,316 cr vs 19,626 = +13.7% (screener; company 14%).", delivered_value="+13.7%", delivery_ratio=1.05, confidence="verified")
add(said_on="2025-02-14", slug="fy25-revenue-sa-12-13pct", speaker=MM, category="revenue_growth",
    title="FY25 standalone revenue growth 12-13%",
    quote="standalone maybe 12% to 13%, Q4 growth will be 15% to 20% both stand-alone and consol",
    metric="Standalone revenue growth", target="+12-13%", deadline="2025-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="delivered", evidence="FY25 standalone INR 18,888 cr vs 16,760 = +12.7% (screener; company 13%).", delivered_value="+12.7%", delivery_ratio=1.06, confidence="verified")
add(said_on="2025-02-14", slug="q4fy25-growth-15-20pct", speaker=MM, category="revenue_growth",
    title="Q4FY25 revenue growth 15-20%",
    quote="We're targeting growth of 15% to 20% in Q4, with margins expected to be around 5% at the PBT level, at the stand-alone level",
    metric="Q4 revenue growth YoY", target="+15-20%", deadline="2025-03-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q4FY25 standalone +21%, consol +18% (Q4FY25 call; screener consol Q4 +18%).", delivered_value="SA +21%, consol +18%", delivery_ratio=1.2, confidence="verified")
add(said_on="2025-02-14", slug="q4fy25-sa-pbt-5pct", speaker=MM, category="margin",
    title="Standalone PBT margin ~5% in Q4FY25, not lower thereafter",
    quote="we are targeting to reach closer to 5% margins at the PBT level in Q4 itself, and I don't see us going down from there at least for the next couple of years",
    metric="Standalone PBT margin", target="~5% in Q4FY25", deadline="2025-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=3,
    status="delivered", evidence="Q4FY25 standalone PBT 5.9% (company); screener 331/6,204 = 5.3%. FY26 standalone ~5.9% ex-exceptional; H1FY27 6.2%.", delivered_value="5.9%", delivery_ratio=1.18, confidence="verified")
add(said_on="2025-02-14", slug="interest-mid-2pct", speaker=MM, category="debt_reduction",
    title="Finance cost 'middle 2%' of sales in Q4 and going forward",
    quote="definitely, as a target, we should be middle 2% of interest cost in Q4, and that will be a target going forward also",
    metric="Standalone finance cost / sales", target="~2.5% or lower", deadline="2025-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=2,
    status="delivered", evidence="Q4FY25 standalone 88/6,204 = 1.4%; FY25 ~2.0%; FY26 1.6% (company; screener quarterly sum 368/23,211 = 1.6%).", delivered_value="1.4% (Q4), 2.0% (FY25)", delivery_ratio=1.0, confidence="verified")
add(said_on="2025-02-14", slug="water-collect-500-700cr-q4-q1", speaker=MM, category="working_capital",
    title="Water (JJM) dues of INR 500-700 cr collected in Q4FY25 or Q1FY26",
    quote="we anticipate collecting the remaining INR500 crores to INR700 crores, which is already billed in Q4 or Q1 '26",
    metric="Water receivable collections", target="INR 500-700 cr", deadline="2025-06-30", deadline_precision="half-year",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Jan-Feb INR 240 cr + March ~INR 370 cr = ~INR 610 cr in Q4FY25 (Q4FY25 call).", delivered_value="~INR 610 cr", delivery_ratio=1.0)
add(said_on="2025-02-14", slug="fy26-water-double-digit-growth", speaker=MM, category="revenue_growth",
    title="Water revenue back to double-digit growth in FY26",
    quote="we believe that we should be going back to that double-digit growth in that business from next year onwards",
    metric="Water revenue growth", target=">=+10% (later '20-25%')", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=1,
    status="unverifiable", evidence="FY26 water revenue INR 2,112 cr (Q4FY26 call), but the FY25 water base is not given in the calls read; quarterly FY26 was -5% (Q1, Q2) and lower in Q3, then +40% QoQ in Q4.")
add(said_on="2025-02-14", slug="fy26-urban-infra-20-25pct", speaker=MM, category="revenue_growth",
    title="Urban Infra revenue +20-25% (maybe 40%) in FY26",
    quote="in the next year, I see this business going up by 20%, 25% if not more than that ... They might even go closer to 40%",
    metric="Urban Infra revenue growth", target="+20-25%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="FY26 Urban Infra +49% (Q4FY26 call).", delivered_value="+49%", delivery_ratio=2.0)
add(said_on="2025-02-14", slug="lmg-ebitda-plus-100bp-fy26", speaker=MM, category="margin",
    title="LMG (Sweden) EBITDA margin up at least 100 bp in FY26",
    quote="I personally believe that this number should go up by at least 100 basis points getting into the next year",
    metric="LMG EBITDA margin", target="+100 bp (from ~4.8-5%)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="delivered", evidence="FY26 LMG EBITDA 6.7-6.8%, PBT 5.6-5.7%, 'improvement of more than 100 basis points' (Q4FY26 call).", delivered_value="+170 bp", delivery_ratio=1.7)
add(said_on="2025-02-14", slug="fasttel-ebitda-7-8pct", speaker=MM, category="margin",
    title="Fasttel (Brazil) EBITDA to stay at 7-8%",
    quote="we have improved the EBITDA margins from as low as 1% to 7% in the current year, and we believe it will stay at this levels of 7% to 8% going forward also",
    metric="Fasttel EBITDA margin", target="7-8%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="missed", evidence="May-25: FY25 Fasttel EBITDA 'closer to 2.9%'. FY26: EBITDA loss INR 186 cr in 9M; INR 515 cr standalone provision in Q4; Brazil projects wrapped up.", delivery_ratio=0.0,
    explanation_for_miss="old-project losses, Brazil currency (prompted, Oct-25 and Feb-26: 'a setback for us')", admitted_unprompted=False)
add(said_on="2025-02-14", slug="vepl-divest-by-q2fy26", speaker=MM, category="other",
    title="Vindhyachal Expressway (VEPL) divested by Q2FY26",
    quote="As VEPL will be divested by Q2",
    metric="Asset sale closing", target="by 30-Sep-25", deadline="2025-09-30", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="Closed January 2026 (Q4FY26): about two quarters late. Interim dates: 'Q2, Q3' (May-25), 'Q3' (Aug-25), 'H2' (Oct-25).", delivery_ratio=1.0,
    explanation_for_miss="NHAI approvals (stated as process, not as a delay)", admitted_unprompted=False)
add(said_on="2025-02-14", slug="indore-vepl-500cr-cy25", speaker=MM, category="working_capital",
    title="Indore real estate + VEPL to bring ~INR 500 cr equity in CY2025",
    quote="Indore and VEPL we definitely expect closer to INR500 crores to come from both of them net excluding debt in calendar year '25",
    metric="Monetisation cash (equity)", target="~INR 500 cr in CY25", deadline="2025-12-31", deadline_precision="half-year",
    specificity="precise", volunteered=False, materiality=2,
    status="partly", evidence="VEPL net cash inflow >INR 600 cr in January 2026 (about one month late); Indore INR 75 cr still outstanding at Dec-25, fully collected by Mar-26.", delivered_value=">INR 600 cr VEPL (Jan-26)", delivery_ratio=1.2)
add(said_on="2025-02-14", slug="nwc-below-100-days", speaker=MM, category="working_capital",
    title="Standalone NWC below 100 days",
    quote="our focus would be more on net working capital days below 100",
    metric="Standalone NWC days", target="<100 days (from 112)", deadline="2025-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="delivered", evidence="Mar-25 94 days; Mar-26 90; Sep-26 81 (company).", delivered_value="94 days", delivery_ratio=1.0)
add(said_on="2025-02-14", slug="net-debt-1x-ebitda", speaker=MM, category="debt_reduction",
    title="Net debt to EBITDA ~1x 'very soon'",
    quote="Our net debt will be equivalent to EBITDA very soon",
    metric="Consolidated net debt / EBITDA", target="~1x", deadline="2025-12-31", deadline_precision="vague",
    specificity="vague", volunteered=False, materiality=2,
    status="delivered", evidence="Mar-25 consol net debt INR 1,953 cr vs EBITDA INR 1,834 cr (~1.06x); Mar-26 915 cr (~0.4x); Sep-26 72 cr.", delivery_ratio=1.0)
add(said_on="2025-02-14", slug="pledge-only-down", speaker=MM, category="other",
    title="Promoter pledge will only come down",
    quote="the guidance to us is exactly what it was in the past of being at the pledge levels will only come down going forward and not go up",
    metric="Promoter pledge %", target="down only", deadline="ongoing", deadline_precision="vague",
    specificity="vague", volunteered=False, materiality=1,
    status="delivered", evidence="May-26: 'over the last 6 quarters, every quarter pledge has come down' (company). NSE pledge endpoint returned no rows, so not independently checked.", delivery_ratio=1.0)
add(said_on="2025-02-14", slug="fy26-capex-below-fy25", speaker=MM, category="capex",
    title="FY26 capex below FY25 (INR 600-650 cr)",
    quote="next year we expect capex to be below the current year ... It should definitely be lower than this year",
    metric="Capex", target="< ~INR 620 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=1,
    status="missed", evidence="FY26 capex 'nearly INR 900 crores' (Q4FY26 opening). Guidance drifted up: 600-650 (May-25), 600-700 (Aug-25), 700-750 (Feb-26).", delivered_value="~INR 900 cr", delivery_ratio=0.0,
    explanation_for_miss="framed as growth investment funded from cash flow (volunteered)", admitted_unprompted=False)
add(said_on="2025-02-14", slug="railways-international-win-q2-q3fy26", speaker=MM, category="customer_win",
    title="First international railway order by Q2-Q3 FY26",
    quote="getting into the next year, maybe Q2, Q3 of next year, we should be targeting a win at the international level",
    metric="Order win", target="international railway win", deadline="2025-12-31", deadline_precision="half-year",
    specificity="range", volunteered=False, materiality=1,
    status="missed", evidence="Aug-25: 'looking at options more in the Africa side ... It might still take some more time'. No international railway win reported through Nov-26.", delivery_ratio=0.0,
    explanation_for_miss="'might still take some more time' (Aug-25, prompted)", admitted_unprompted=False)
add(said_on="2025-02-14", slug="saudi-og-40pct-fy26", speaker=MM, category="other",
    title="~40% of the USD 800 mn Aramco project executed in FY26",
    quote="out of the $800-odd million on that project, we believe that closer to 40% would get delivered in the next year",
    metric="Project execution share", target="~40% in FY26", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="unverifiable", evidence="May-25: 'more than 1/3 ... physical already'; Feb-26: 'closer to 50% of the project'. The FY26 share cannot be separated; O&G revenue +55% in FY26.")

# ---------------- Q4FY25 (19-May-2025) - FY26 guidance given in opening remarks ----------------
add(said_on="2025-05-19", slug="fy26-oi-26000-28000cr", speaker=MM, category="order_inflow",
    title="FY26 order inflow INR 26,000-28,000 cr",
    quote="we expect order inflows in the range of INR 26,000 crores to INR 28,000 crores for full year '26",
    metric="Consolidated order inflow", target="INR 26,000-28,000 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="FY26 order wins 'past the INR 26,000 crores mark' (Q4FY26). Note: in Oct-25 the target was quietly restated as 'INR 25,000 crores plus', then back to '26,000-plus' in Feb-26.", delivered_value=">INR 26,000 cr", delivery_ratio=1.0)
add(said_on="2025-05-19", slug="fy26-revenue-20pct-plus", speaker=MM, category="revenue_growth",
    title="FY26 revenue growth 20%+ (standalone and consolidated)",
    quote="we will target around 20% plus revenue growth for stand- alone and consol basis",
    metric="Revenue growth", target=">=+20%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    status="delivered", evidence="FY26 consol INR 27,143 cr (+21.6%), standalone 23,210 cr (+22.9%) (screener).", delivered_value="+21.6% / +22.9%", delivery_ratio=1.08, confidence="verified")
add(said_on="2025-05-19", slug="fy26-sa-pbt-5-25-5-5pct", speaker=MM, category="margin",
    title="FY26 standalone PBT margin 5.25-5.5%",
    quote="we expect stand-alone PBT margin in the range of 5.25% to 5.5%",
    metric="Standalone PBT margin", target="5.25-5.5% (+35-60 bp over FY25 4.9%)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="Company: 5.9% 'excluding exceptional items and a one-off dividend income from VEPL' (+100 bp). Reported basis (screener) 1,143/23,210 = 4.9% after an INR 515 cr Fasttel provision. Delivered on the company's adjusted definition only; single-source.",
    delivered_value="5.9% adjusted (4.9% reported)", delivery_ratio=1.07)
add(said_on="2025-05-19", slug="fy26-consol-pbt-4-5-4-75pct", speaker=MM, category="margin",
    title="FY26 consolidated PBT margin 4.5-4.75% (+~100 bp)",
    quote="consol PBT margin of 4.5% to 4.75% for full year, which is improvement of closer to 100 basis points",
    metric="Consolidated PBT margin", target="4.5-4.75%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY26 consol PBT before exceptional items INR 1,334 cr = 4.9% (+120 bp) (company); screener PBT 1,371/27,143 = 5.05%.", delivered_value="4.9%", delivery_ratio=1.2, confidence="verified")
add(said_on="2025-05-19", slug="fy26-nwc-below-100-sa", speaker=MM, category="working_capital",
    title="FY26 standalone NWC below 100 days",
    quote="We remain confident to maintain our net working capital below 100 days on a stand-alone basis",
    metric="Standalone NWC days", target="<100", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="Mar-26 standalone 90 days, consol 75 (company). Screener consol WC days 43 -> 38.", delivered_value="90 days", delivery_ratio=1.0)
add(said_on="2025-05-19", slug="fy26-finance-cost-below-2pct-sa", speaker=MM, category="debt_reduction",
    title="FY26 standalone finance cost below 2% of sales",
    quote="finance costs below 2% of sales at a stand-alone level",
    metric="Standalone finance cost / sales", target="<2%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="FY26 1.6% (company); screener standalone quarterly interest 84+102+93+89 = 368 / 23,211 = 1.6% (the annual screener line 526 includes other items).", delivered_value="1.6%", delivery_ratio=1.0, confidence="verified")
add(said_on="2025-05-19", slug="fy26-water-growth-10pct", speaker=MM, category="revenue_growth",
    title="Water revenue +10% in FY26 (budgeted)",
    quote="As of now, we have assumed a minimal growth of closer to 10% in FY'26 in our budgeted numbers in Water",
    metric="Water revenue growth", target="~+10%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="unverifiable", evidence="Restated as 'would not see any growth' in Aug-25 (no acknowledgement). FY26 water INR 2,112 cr; FY25 base not disclosed in the calls read.")
add(said_on="2025-05-19", slug="fy26-td-growth-20pct-plus", speaker=MM, category="revenue_growth",
    title="T&D revenue +20%+ in FY26",
    quote="we expect TL to do 20% plus",
    metric="T&D revenue growth", target=">=+20%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="delivered", evidence="FY26 T&D revenue +25% (Q4FY26).", delivered_value="+25%", delivery_ratio=1.25)
add(said_on="2025-05-19", slug="fy26-bf-growth-18-20pct", speaker=MM, category="revenue_growth",
    title="B&F revenue +18-20% in FY26",
    quote="We expect B&F to be in the range of 18% to 20%",
    metric="B&F revenue growth", target="+18-20%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=2,
    status="delivered", evidence="FY26 B&F +19% (Q4FY26).", delivered_value="+19%", delivery_ratio=1.06)
add(said_on="2025-05-19", slug="fy26-og-growth-100pct-plus", speaker=MM, category="revenue_growth",
    title="Oil & Gas revenue +100%+ in FY26",
    quote="Oil and Gas will still continue to grow at 100% plus given that large Saudi Aramco order",
    metric="Oil & Gas revenue growth", target=">=+100%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="FY26 Oil & Gas +55% (Q4FY26).", delivered_value="+55%", delivery_ratio=0.55,
    explanation_for_miss="none given; growth described as 'phenomenal'", admitted_unprompted=False)
add(said_on="2025-05-19", slug="fy26-urban-infra-40-50pct", speaker=MM, category="revenue_growth",
    title="Urban Infra revenue +40-50% in FY26",
    quote="Urban Infra should be in a good 40% to 50% basis plus",
    metric="Urban Infra revenue growth", target="+40-50%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="FY26 +49%.", delivered_value="+49%", delivery_ratio=1.2)
add(said_on="2025-05-19", slug="fy26-eps-min-50", speaker=MM, category="other",
    title="FY26 EPS at least INR 50 (from ~INR 40)",
    quote="from INR 32, we have reached closer to INR 40 in the previous year. And current year, based on numbers, we should be targeting a minimum of INR 50",
    metric="EPS", target=">= INR 50 (standalone basis implied by the INR 40 base)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="delivered", evidence="FY26 standalone EPS INR 49 (98%), consol EPS INR 61 (company). In Feb-26 the target was restated as 'consol EPS exceeding INR 50', an easier basis.", delivered_value="SA 49 / consol 61", delivery_ratio=0.98, confidence="verified")
add(said_on="2025-05-19", slug="fy26-capex-600-650cr", speaker=MM, category="capex",
    title="FY26 capex INR 600-650 cr",
    quote="Our guidance for FY '26 is in a similar range of INR 600-650 crores",
    metric="Capex", target="INR 600-650 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="missed", evidence="FY26 capex 'nearly INR 900 crores' (+38% vs top of range).", delivered_value="~INR 900 cr", delivery_ratio=0.72,
    explanation_for_miss="growth investment, funded internally (volunteered as a positive)", admitted_unprompted=False, confidence="single-source")
add(said_on="2025-05-19", slug="fy26-td-oi-above-fy25", speaker=MM, category="order_inflow",
    title="FY26 T&D order inflow better than FY25 (INR 14,461 cr)",
    quote="Our own belief is that we should be doing better than this in terms of order inflow in our T&D business getting into the next year or getting into '26 itself",
    metric="T&D order inflow", target="> INR 14,461 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=1,
    status="partly", evidence="FY26 T&D order inflow 'closer to INR 13,000 crores' (90%); India T&D fell from ~7,000 to ~4,500 cr.", delivered_value="~INR 13,000 cr", delivery_ratio=0.9,
    explanation_for_miss="L1 positions in large projects slipped into FY27 (May-26, prompted)", admitted_unprompted=False)
add(said_on="2025-05-19", slug="lmg-ebitda-5-6-25pct-fy26", speaker=MM, category="margin",
    title="LMG EBITDA 5-6.25% in FY26",
    quote="from 5%, it might go to 6%-6.25%",
    metric="LMG EBITDA margin", target="5-6.25%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="FY26 6.7-6.8% (beat). Guidance was formally withheld in Aug-25 because of the LMG IPO evaluation.", delivered_value="6.7-6.8%", delivery_ratio=1.1)
add(said_on="2025-05-19", slug="lmg-fundraise-plan-6-9-months", speaker=MM, category="m&a",
    title="LMG fundraising plan to be announced within 6-9 months",
    quote="we'll be exploring whatever options are available in terms of fundraising and coming back to all of you all over the next 6 to 9 months in terms of what our plans are",
    metric="LMG fundraise decision", target="plan announced", deadline="2026-02-28", deadline_precision="quarter",
    specificity="range", volunteered=False, materiality=1,
    status="moved-goalpost", evidence="Oct-25: 'in '26, '27, we should see some light'; Feb-26: 'I'm expecting in FY26-27 should give us further cash flows'; May-26: 'in whatever form it comes'. No plan announced; the 6-9 month window was not referred to.", admitted_unprompted=False)
add(said_on="2025-05-19", slug="fasttel-breakeven-fy26", speaker=MM, category="margin",
    title="Fasttel (Brazil) to break even in FY26",
    quote="We're working hard to break even this company in the next year ... I can tell you confidently that numbers will be much better than what the numbers are right now",
    metric="Fasttel PBT", target="break-even (from ~INR -35 cr)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="Oct-25: EBITDA 'continues to be negative'. Feb-26: 9M EBITDA loss INR 186 cr, 'a setback for us'. Q4FY26: INR 515 cr standalone provision; all Brazil projects wrapped up.", delivery_ratio=0.0,
    explanation_for_miss="hits on old projects (prompted, Oct-25 / Feb-26); exit volunteered May-26", admitted_unprompted=False)
add(said_on="2025-05-19", slug="fasttel-ebitda-4-5pct-2yrs", speaker=MM, category="margin",
    title="Fasttel EBITDA 4-5% within two years",
    quote="We definitely expect this to go up to levels of 4% to 5% in the next 2 years",
    metric="Fasttel EBITDA margin", target="4-5%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="withdrawn", evidence="May-26 opening: 'We have successfully wrapped up all ongoing projects in Brazil and took a full provision for our exposure'. Explicit exit, explained, ahead of the deadline.",
    explanation_for_miss="exit of Brazil operations", admitted_unprompted=True)
add(said_on="2025-05-19", slug="indore-130cr-60-90-days", speaker=MM, category="working_capital",
    title="Indore real estate: ~INR 130 cr collected within 60-90 days",
    quote="we expect all the money to come in the next 60 to 90 days. So INR 130-odd crores of Indore is all expected in the next 60 to 90 days",
    metric="Collections", target="INR 130 cr by ~Aug-25", deadline="2025-08-17", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="Aug-25: ~INR 100 cr still to collect 'in Q2 or early Q3'; Dec-25: INR 75 cr outstanding; fully collected by Mar-26. Two-plus quarters late.", delivery_ratio=1.0, admitted_unprompted=False)
add(said_on="2025-05-19", slug="vepl-close-q2-q3fy26", speaker=MM, category="other",
    title="VEPL sale to close in Q2-Q3 FY26",
    quote="assuming that VEPL happens in, let's say, in Q2, Q3",
    metric="Asset sale closing", target="by Dec-25", deadline="2025-12-31", deadline_precision="half-year",
    specificity="range", volunteered=False, materiality=1,
    status="partly", evidence="Closed January 2026: one quarter late.", delivery_ratio=1.0)
add(said_on="2025-05-19", slug="wepl-clarity-6-months", speaker=MM, category="other",
    title="Clarity on Wainganga Expressway (WEPL) within six months",
    quote="that's something over the next 6 months, we'll have clarity on how do we want to progress with WEPL",
    metric="Decision", target="decision by Nov-25", deadline="2025-11-19", deadline_precision="half-year",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="Termination notice issued to NHAI 15-Jul-25; asset handed over 30-Sep-25.", delivery_ratio=1.0)
add(said_on="2025-05-19", slug="jjm-recovery-60-70pct-from-june", speaker=SKT, category="working_capital",
    title="60-70% of ~INR 1,500 cr JJM receivables to start coming from June / Q2",
    quote="today on INR 1,500 crores, we have visibility to the extent of about 60% to 70%. And it should start coming out either in the June or in the quarter 2",
    metric="Water receivables", target="~INR 900-1,050 cr recovered from Jun-25", deadline="2025-09-30", deadline_precision="quarter",
    specificity="range", volunteered=False, materiality=2,
    status="missed", evidence="Water receivables rose to INR 1,551 cr at Sep-25 (from 1,427 at Jun-25) despite INR 420 cr collected in Q2; still ~INR 1,600 cr in May-26 and ~1,500 cr billed+unbilled in Aug-26. FY26 collections INR 1,800 cr vs INR 2,500 cr invested.",
    delivery_ratio=0.0, explanation_for_miss="UP and Jharkhand JJM funding stalled at the centre (volunteered in Oct-25 opening: 'slow compared to our expectations')", admitted_unprompted=True)
add(said_on="2025-05-19", slug="international-water-wins-fy26", speaker=MM, category="customer_win",
    title="A few significant international water wins in FY26",
    quote="we believe that during the year, we should at least have a few significant wins in this business in the international front",
    metric="Order wins", target="a few international water orders", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=1,
    status="partly", evidence="None in FY26 ('favorably placed', May-26). First Middle East water order (INR 344 cr) won in Q1FY27: one order, about one quarter late.", delivery_ratio=0.5)
add(said_on="2025-05-19", slug="tower-capacity-50kt-6-12-months", speaker=MM, category="capacity_commissioning",
    title="Tower plant capacity +50,000 t/yr within 6-12 months",
    quote="we're looking at expansion of close to 50,000 tons per annum ... INR 20-odd crores further in the next 6 to 12 months",
    metric="Tower capacity", target="+50k t/yr", deadline="2026-05-19", deadline_precision="half-year",
    specificity="range", volunteered=False, materiality=1,
    status="unverifiable", evidence="Company capacity figures conflict: '2.25 lakh plus tons' (Aug-25), 'closer to 275,000' (Feb-26), '2,40,000 tons' (May-26 and Nov-26 presentation).")
add(said_on="2025-05-19", slug="revenue-27500cr-fy26-vision", speaker=MM, category="revenue_growth",
    title="Revised 'Vision 25': ~INR 27,500 cr revenue (25,000 + ~10%) in FY26",
    quote="we have extended that vision and said, in '26, how do we reach a number which is INR 25,000 crores plus, let's say, 10% or something like that",
    metric="Consolidated revenue", target="~INR 27,500 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="delivered", evidence="FY26 consol revenue INR 27,143 cr = 98.7% (screener).", delivered_value="INR 27,143 cr", delivery_ratio=0.99, confidence="verified")

# ---------------- Q1FY26 (08-Aug-2025) ----------------
add(said_on="2025-08-08", slug="fy26-revenue-20-25pct", speaker=MM, category="revenue_growth",
    title="FY26 revenue growth 20-25%, 'closer to 25%'",
    quote="We are on track to achieve revenue growth in the range of 20% to 25% at both stand-alone and consol level",
    metric="Revenue growth", target="+20-25%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY26 consol +21.6%, standalone +22.9% (inside the range, below the 'closer to 25%' said in Q&A).", delivered_value="+21.6% / +22.9%", delivery_ratio=1.0, confidence="verified")
add(said_on="2025-08-08", slug="fy26-sa-pbt-5-5-5pct", speaker=MM, category="margin",
    title="FY26 standalone PBT 5-5.5%, 'more towards the higher side'",
    quote="Current year, we stay confident that we would be at a PBT standalone in the range of 5% to 5.5%, more towards the higher side",
    metric="Standalone PBT margin", target="5-5.5%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="delivered", evidence="5.9% adjusted (4.9% reported). Note the floor was quietly lowered from 5.25% (May-25) to 5%, without comment.", delivered_value="5.9% adjusted", delivery_ratio=1.07)
add(said_on="2025-08-08", slug="vepl-q3fy26", speaker=MM, category="other",
    title="VEPL sale to complete in Q3FY26",
    quote="We are progressing well on approval for sale of Vindhyachal Expressway and expect to complete the transaction in Q3 of '25/'26",
    metric="Asset sale closing", target="by 31-Dec-25", deadline="2025-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="partly", evidence="Completed January 2026 (EV ~INR 799 cr, net cash >INR 600 cr): one quarter late; Oct-25 had already widened to 'second half'.", delivery_ratio=1.0)
add(said_on="2025-08-08", slug="indore-100cr-q2-early-q3", speaker=MM, category="working_capital",
    title="Indore: remaining ~INR 100 cr collected in Q2 or early Q3 FY26",
    quote="We have to collect close to INR100 crores, which we believe collection should all happen in Q2 or early Q3, not beyond that",
    metric="Collections", target="INR 100 cr by ~Oct-25", deadline="2025-10-31", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="INR 75 cr still outstanding at 31-Dec-25; collected by Mar-26 ('not beyond that' missed by about two quarters).", delivery_ratio=0.25, admitted_unprompted=False)
add(said_on="2025-08-08", slug="debt-stabilise-q3-q4", speaker=MM, category="debt_reduction",
    title="Debt to rise in Q1-Q2 and stabilise in Q3-Q4 FY26",
    quote="my own view is Q1, Q2 debt should go up, and it should start stabilizing in Q3/Q4",
    metric="Net debt", target="stable/lower in H2", deadline="2026-03-31", deadline_precision="half-year",
    specificity="vague", volunteered=False, materiality=2,
    status="delivered", evidence="Consol net debt Sep-25 3,169 -> Dec-25 2,240 -> Mar-26 915 cr (company).", delivery_ratio=1.0)
add(said_on="2025-08-08", slug="shubham-sell-2-3-warehouses", speaker=MM, category="other",
    title="Shree Shubham Logistics to sell 2-3 large warehouses in FY26",
    quote="We should be selling at least 2 to3 large warehouses in the current year. One of them may be in as early as Q2",
    metric="Asset sales", target="2-3 warehouses", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="unverifiable", evidence="Calls report warehouse sales and debt reduction (external debt ~0 by 31-Jul-26) but not the number sold.")
add(said_on="2025-08-08", slug="growth-20-25pct-next-2-3yrs", speaker=MM, category="revenue_growth",
    title="Revenue growth 20-25% a year for the next 2-3 years",
    quote="our own belief is that we would like to continue this 20%, 25% growth for the next 2-3 years",
    metric="Revenue CAGR", target="+20-25% p.a. FY26-FY28", deadline="2028-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="withdrawn", evidence="May-26: FY27 guided at '15% plus'; when an analyst recalled the ~20% expectation, management explained the Middle East and labour constraints ('could revisit this number at the end of Q2').",
    explanation_for_miss="Middle East disruption, election-period labour (May-26, prompted)", admitted_unprompted=False)

# ---------------- Q2FY26 (31-Oct-2025) ----------------
add(said_on="2025-10-31", slug="fy26-revenue-25pct-plus", speaker=MM, category="revenue_growth",
    title="FY26 revenue growth 25%+ (raised from 20-25%)",
    quote="we are on track to achieve targeted revenue growth of 25% plus at both standalone and consol level, compared to our earlier guidance of 20% to 25%",
    metric="Revenue growth", target=">=+25%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    status="partly", evidence="FY26 consol +21.6% (0.86), standalone +22.9% (0.92). In May-26 management listed its FY26 target as '20% to 25%' and said it had 'fully delivered on each of these promises'; the raise to 25%+ was not mentioned.",
    delivered_value="+21.6% / +22.9%", delivery_ratio=0.89, explanation_for_miss="none; the raised target was not referred to", admitted_unprompted=False, confidence="verified")
add(said_on="2025-10-31", slug="fy26-pbt-plus-50bp", speaker=MM, category="margin",
    title="FY26 PBT margin up at least 50 bp (standalone and consolidated)",
    quote="we reaffirm our guidance of FY26 of improving PBT by a minimum of 50 basis points",
    metric="PBT margin change", target=">=+50 bp", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    status="delivered", evidence="Consol +120 bp (4.9% pre-exceptional); standalone +100 bp on the adjusted basis (reported basis flat at 4.9% after the Fasttel provision).", delivered_value="+120 bp consol", delivery_ratio=2.0)
add(said_on="2025-10-31", slug="fy26-oi-25000-plus", speaker=MM, category="order_inflow",
    title="FY26 order inflow INR 25,000 cr+ (restated from 26,000-28,000)",
    quote="we stick to our guidance of 25,000 crores plus on a consol basis for FY26",
    metric="Consolidated order inflow", target=">INR 25,000 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="FY26 >INR 26,000 cr. The restatement lowered the target without acknowledging the earlier 26,000-28,000 range ('stick to our guidance').", delivered_value=">INR 26,000 cr", delivery_ratio=1.04)
add(said_on="2025-10-31", slug="fy26-nwc-sa-100-consol-85-90", speaker=MM, category="working_capital",
    title="Year-end NWC <100 days standalone, <85-90 consolidated",
    quote="we continue to stay on a target of less than 100 days for standalone and less than 90 days on consol or less than 85 days on consol",
    metric="NWC days", target="SA <100, consol <85-90", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=2,
    status="delivered", evidence="Mar-26 standalone 90, consol 75.", delivered_value="90 / 75", delivery_ratio=1.0)
add(said_on="2025-10-31", slug="vepl-h2fy26", speaker=MM, category="other",
    title="VEPL sale to complete in H2FY26",
    quote="we are progressing well on approval for sale and expect to complete the transaction in the second half of FY26",
    metric="Asset sale closing", target="by Mar-26", deadline="2026-03-31", deadline_precision="half-year",
    specificity="range", volunteered=True, materiality=1,
    status="delivered", evidence="Completed January 2026.", delivery_ratio=1.0)
add(said_on="2025-10-31", slug="shubham-debt-40-50cr-mar26", speaker=MM, category="debt_reduction",
    title="Shree Shubham external debt cut to INR 40-50 cr by Mar-26",
    quote="Our target is to bring this -- reduce this by at least a further 50%, get it to levels of INR 40 crores to INR 50 crores by the year-end",
    metric="Subsidiary external debt", target="INR 40-50 cr (from ~90)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="unverifiable", evidence="Mar-26 figure not given; May-26 'reduced that significantly', 'closer to 0 by June'; 31-Jul-26 'repaid all banks'.")
add(said_on="2025-10-31", slug="lmg-growth-30-40pct-fy26", speaker=MM, category="revenue_growth",
    title="LMG revenue +30-40% in FY26",
    quote="The current year itself, we are looking at a growth, which is more in the range of 30% to 40% and improved margins",
    metric="LMG revenue growth", target="+30-40%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="FY26 LMG revenue +64% to ~INR 3,000 cr.", delivered_value="+64%", delivery_ratio=2.0)
add(said_on="2025-10-31", slug="lmg-pbt-6-5-7-5pct", speaker=MM, category="margin",
    title="LMG PBT margin 6.5-7.5%",
    quote="we believe that margins should stay in that range of 6.5% to 7.5%",
    metric="LMG PBT margin", target="6.5-7.5%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="partly", evidence="FY26 LMG PBT 5.6-5.7% (~87% of 6.5%); Feb-26 had already lowered to '6% to 7%'.", delivered_value="5.6-5.7%", delivery_ratio=0.87, admitted_unprompted=False)
add(said_on="2025-10-31", slug="bf-growth-20pct-double-digit-ebitda", speaker=MM, category="revenue_growth",
    title="B&F: growth of at least 20% with double-digit EBITDA",
    quote="I do not see this business doing less than double digit on EBITDA, and I do not see us growing at less than 20%, whatever happens",
    metric="B&F revenue growth / EBITDA", target=">=+20%, EBITDA >=10%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="delivered", evidence="FY26 B&F +19% (95% of 20%); EBITDA 'double digits, 10% to 11% plus' (company).", delivered_value="+19%", delivery_ratio=0.95)
add(said_on="2025-10-31", slug="fy27-ebitda-9pct-feasible", speaker=MM, category="margin",
    title="Consolidated EBITDA 9%+ in FY27 'sounds feasible'",
    quote="Can it go to 9% plus levels getting into next year? It sounds feasible, but let's just come back to you",
    metric="Consolidated EBITDA margin", target=">=9%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=2,
    status="pending", evidence="H1FY27 consol core EBITDA 8.5%, standalone 8.6% (Q2FY27 presentation).")

# ---------------- Q3FY26 (05-Feb-2026) ----------------
add(said_on="2026-02-05", slug="fy26-revenue-approx-25pct", speaker=MM, category="revenue_growth",
    title="FY26 revenue growth ~25%",
    quote="We expect revenue growth for the full year to be approx 25%",
    metric="Revenue growth", target="~+25%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    status="partly", evidence="FY26 consol +21.6%, standalone +22.9% (9M had been +27/+28%; Q4 consol +10%, standalone +12%).", delivered_value="+21.6% / +22.9%", delivery_ratio=0.89,
    explanation_for_miss="Middle East disruption ~INR 200-250 cr of Q4 revenue (May-26, prompted)", admitted_unprompted=False, confidence="verified")
add(said_on="2026-02-05", slug="fy26-consol-eps-above-50", speaker=MM, category="other",
    title="FY26 consolidated EPS above INR 50",
    quote="we remain confident in reaching our target consol EPS exceeding INR 50 per share for the current year",
    metric="Consolidated EPS", target=">INR 50", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="FY26 consol EPS INR 60.9 (screener; company INR 61).", delivered_value="INR 61", delivery_ratio=1.22, confidence="verified")
add(said_on="2026-02-05", slug="indore-fully-monetised-mar26", speaker=MM, category="working_capital",
    title="Indore real estate fully monetised by Mar-26",
    quote="we are on track to complete the full monetization of inventory in our Indore real estate project before the end of March 2026",
    metric="Collections", target="all collected", deadline="2026-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="May-26: Vindhyachal and Indore commitments 'fully delivered'.", delivery_ratio=1.0)
add(said_on="2026-02-05", slug="mar26-net-debt-below-dec", speaker=MM, category="debt_reduction",
    title="Mar-26 net debt 'much lower' than Dec-25",
    quote="it will be much lower than Q3, whatever we've reported net debt at Q3, it will be much lower than that, both at stand-alone and consol",
    metric="Net debt", target="< Dec-25 (consol 2,240, SA 1,849)", deadline="2026-03-31", deadline_precision="quarter",
    specificity="vague", volunteered=False, materiality=2,
    status="delivered", evidence="Mar-26 consol INR 915 cr, standalone 749 cr.", delivery_ratio=1.0)
add(said_on="2026-02-05", slug="water-collections-improve-q4", speaker=MM, category="working_capital",
    title="Water collections to improve in Q4FY26",
    quote="We remain confident on improving collections from water projections in Q4 itself",
    metric="Water collections", target="higher in Q4", deadline="2026-03-31", deadline_precision="quarter",
    specificity="vague", volunteered=True, materiality=1,
    status="delivered", evidence="May-26: 'Our Q4 delivered strong results in terms of collection'; FY26 collections INR 1,800 cr (9M ~1,250 incl. Jan).", delivery_ratio=1.0)
add(said_on="2026-02-05", slug="fy26-capex-700-750cr", speaker=MM, category="capex",
    title="FY26 capex outflow INR 700-750 cr",
    quote="capex outflow should be in the range of INR 700 crores to INR 750 crores in terms of outflow",
    metric="Capex", target="INR 700-750 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="missed", evidence="FY26 'nearly INR 900 crores' (+20% vs top of range), two months after this estimate.", delivered_value="~INR 900 cr", delivery_ratio=0.83, admitted_unprompted=False, confidence="single-source")
add(said_on="2026-02-05", slug="fy26-intl-td-oi-9500-10000cr", speaker=MM, category="order_inflow",
    title="FY26 international T&D order inflow INR 9,500-10,000 cr incl. Sweden",
    quote="if I include Sweden also, TLI should reach a number around IN 9,500 crores to INR 10,000 crores order inflow in the current year",
    metric="International T&D order inflow", target="INR 9,500-10,000 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="partly", evidence="May-26: international (LMG, Fasttel, TLI) FY26 'around INR 8,000' cr = 84%.", delivered_value="~INR 8,000 cr", delivery_ratio=0.84,
    explanation_for_miss="large L1s shifted into FY27 (prompted)", admitted_unprompted=False)
add(said_on="2026-02-05", slug="td-oi-15-20pct-pa-next-2yrs", speaker=MM, category="order_inflow",
    title="T&D order inflow +15-20% a year for the next two years",
    quote="Going forward, next couple of years, I expect the inflows to increase by at least 15%, 20% on an annualized basis",
    metric="T&D order inflow growth", target="+15-20% p.a. FY27-28", deadline="2028-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="withdrawn", evidence="May-26 (prompted): FY27 T&D inflow 'INR 15,000 crores max', more likely 13,000-14,000; 'our order inflow on T&D might not grow at 20% ... or at 15%', explained as a choice to stay selective.",
    explanation_for_miss="selectivity, labour, 2.5-year order cover (prompted)", admitted_unprompted=False)

# ---------------- Q4FY26 (15-May-2026) - FY27 guidance ----------------
add(said_on="2026-05-15", slug="fy27-oi-above-30000cr", speaker=MM, category="order_inflow",
    title="FY27 order inflow above INR 30,000 cr",
    quote="We expect full year order wins to exceed INR30,000 crores in FY '27",
    metric="Consolidated order inflow", target=">INR 30,000 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    status="pending", evidence="YTD FY27 INR 23,934 cr by 05-Nov-26 (Q2FY27 presentation); reaffirmed Aug-26. On track.")
add(said_on="2026-05-15", slug="fy27-revenue-15pct-plus", speaker=MM, category="revenue_growth",
    title="FY27 revenue growth ~15%+",
    quote="we are guiding for around 15% plus top line growth, coupled with robust profitability",
    metric="Revenue growth", target=">=+15%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    status="pending", evidence="Reaffirmed Aug-26 ('at least 15%'). H1FY27 reported consol +6% (core, ex Brazil/roads, +11%), standalone +12% (Q2FY27 presentation). At risk.")
add(said_on="2026-05-15", slug="fy27-consol-pbt-plus-75bp", speaker=MM, category="margin",
    title="FY27 consolidated PBT margin +75 bp",
    quote="This bottom line performance will be driven by a 75 basis point expansion in the consol PBT margins",
    metric="Consolidated PBT margin", target="~5.65% (+75 bp over 4.9%)", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    status="pending", evidence="H1FY27 consol PBT 6.1% (+130 bp YoY). On track.")
add(said_on="2026-05-15", slug="fy27-capex-800cr-plus", speaker=MM, category="capex",
    title="FY27 capex INR 800 cr+",
    quote="we should be doing capex of INR 800-plus crores",
    metric="Capex", target=">=INR 800 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1, status="pending", evidence="Q1FY27 >INR 250 cr.")
add(said_on="2026-05-15", slug="fy27-water-collections-2500cr", speaker=MM, category="working_capital",
    title="FY27 water collections INR 2,500 cr+",
    quote="Current year, we're expecting INR 2,500 crores plus. And I'm reasonably sure we should be able to get that collections",
    metric="Water collections", target=">=INR 2,500 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1, status="pending", evidence="~INR 650 cr collected Apr-Jul 2026.")
add(said_on="2026-05-15", slug="jjm-receivables-majority-h1fy27", speaker=MM, category="working_capital",
    title="Majority of ~INR 1,600 cr water receivables recovered in Q1-Q2 FY27",
    quote="our total outstanding receivables on that business is closer to INR1,600- odd crores. And we're pretty confident that majority of this should get recovered in the first 2 quarters itself",
    metric="Water receivables", target=">INR 800 cr of the 1,600 recovered", deadline="2026-09-30", deadline_precision="half-year",
    specificity="vague", volunteered=False, materiality=2,
    status="unverifiable", evidence="Aug-26: billed + unbilled still 'INR 1,500 plus crores'; ~INR 650 cr collected by July but new work keeps adding. No Sep-26 receivable figure in the Q2FY27 presentation.")
add(said_on="2026-05-15", slug="shubham-external-debt-zero-june26", speaker=MM, category="debt_reduction",
    title="Shree Shubham external debt ~0 by June 2026",
    quote="We believe that our outside debt would be closer to 0 by June ... which I expect would happen in Q1, Q2 itself",
    metric="Subsidiary external debt", target="~0", deadline="2026-09-30", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1,
    status="delivered", evidence="Aug-26: 'They have repaid all banks as of 31st July'.", delivery_ratio=1.0)
add(said_on="2026-05-15", slug="fy27-td-oi-13-15kcr", speaker=MM, category="order_inflow",
    title="FY27 T&D order inflow INR 13,000-15,000 cr",
    quote="my view could be more in the range of INR 13,000 crores to INR 14,000 crores would be a very good number",
    metric="T&D order inflow", target="INR 13,000-15,000 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1, status="pending", evidence="T&D YTD FY27 INR 9,322 cr + ~5,000 cr favourably placed (Nov-26).")
add(said_on="2026-05-15", slug="jjm-projects-complete-fy27", speaker=MM, category="other",
    title="Most JJM water projects physically complete in FY27",
    quote="majority of our Water projects, except maybe 5 or 6 would all get completed physically in the current year",
    metric="Project completion", target="all but 5-6 projects", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=1, status="pending", evidence="")

# ---------------- Q1FY27 (11-Aug-2026) ----------------
add(said_on="2026-08-11", slug="og-large-wins-q3-or-late-q2", speaker=MM, category="customer_win",
    title="Large Middle East oil & gas wins by Q3FY27, 'if not late part of Q2'",
    quote="we believe that it should be in place in Q3, if not late part of Q2",
    metric="Order wins", target="large ME O&G order(s)", deadline="2026-12-31", deadline_precision="quarter",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="Q2FY27 presentation: 'Secured first major project in UAE for gas pipeline infrastructure'; O&G order inflow INR 5,279 cr YTD FY27.", delivery_ratio=1.0)

SUMMARY_EXTRA = {
    "calls_covered": "7 concalls, Q3FY25 (14-Feb-2025) to Q1FY27 (11-Aug-2026), plus the Q2FY27 investor presentation (05-Nov-2026) for H1FY27 actuals",
    "grade": "B+ (high delivery on group P&L, working capital and debt guidance; misses cluster in subsidiaries (Fasttel), asset-sale/collection dates and capex budgets; mild habit of re-stating targets without comment)",
}
ANALYSIS_BODY = ("Promise tracker on Kalpataru Projects International (peer calibration for SKIPPER). 7 concalls (Feb-2025 to Aug-2026) plus the Nov-2026 results deck; "
    "{n_promises} promises extracted, {n_scored} scored. Status counts: {status_counts}. Weighted delivery ratio {weighted_delivery_ratio_pct}% "
    "(specificity-only {specificity_weighted_delivery_ratio_pct}%; raw hit rate {raw_hit_rate_pct}%); MCS {mcs_schema_scale}. Candour index {candour_index_pct}%. "
    "Group-level guidance was met or beaten: FY25 revenue inside the cut 12-13%/13-15% ranges; FY26 revenue +22-23% vs 20%+; consol PBT 4.9% vs 4.5-4.75%; NWC 90 days vs <100; "
    "finance cost 1.6% vs <2%; order inflow >26,000 vs 26,000-28,000. Shortfalls: the mid-year raise to '25%+' revenue (delivered 22-23%, later recalled as '20-25%'); "
    "Fasttel break-even (ended in a INR 515 cr write-off); asset-sale and collection dates (VEPL two quarters late vs first date; Indore; JJM receivables); capex overspent every guide (~900 vs 600-650). "
    "Standalone PBT target met only on the company's adjusted basis (5.9% vs 4.9% reported). Order-inflow guidance was quietly restated downward once (26-28k -> 25k+) before being met. Research, not advice.")
