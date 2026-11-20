# Promise ledger for SKIPPER pilot. Edited in stages; build_seed.py turns it into memdb seed JSON.
NSE = "https://nsearchives.nseindia.in/corporate/"
CALLS = {
    "2024-07-30": ("Q1FY25 concall transcript", NSE + "SKIPPER_05082024143308_Transcriptletter.pdf"),
    "2024-10-29": ("Q2FY25 concall transcript", NSE + "SKIPPER_02112024134823_Transcript.pdf"),
    "2025-02-06": ("Q3FY25 concall transcript", NSE + "skipper_11022025121248_Trancript.pdf"),
    "2025-04-30": ("Q4FY25 concall transcript", NSE + "skipper_07052025161052_Transcriptletter.pdf"),
    "2025-07-31": ("Q1FY26 concall transcript", NSE + "skipper_06082025120131_Transcriptintimation.pdf"),
    "2025-11-07": ("Q2FY26 concall transcript", NSE + "skipper_13112025165505_Transcript.pdf"),
    "2026-01-29": ("Q3FY26 concall transcript", NSE + "skipper_04022026183852_Earningcall.pdf"),
    "2026-04-28": ("Q4FY26 concall transcript", NSE + "skipper_05052026133011_Transcriptintimation.pdf"),
    "2026-08-12": ("Q1FY27 concall transcript", NSE + "skipper_18082026120803_Transcript_of_Concall.pdf"),
    "2026-10-30": ("Q2FY27 concall transcript", NSE + "skipper_05112026165128_ConcallTranscript.pdf"),
}
SB = "Sharan Bansal (Director / ED)"
CFO = "Shiv Shankar Gupta (CFO)"
AD = "Aditya Dujari (GM Finance & IR)"

# specificity: precise = number+metric+date; range = number range or date range; vague = direction only
# materiality: 1 = minor segment / side metric, 2 = meaningful, 3 = core (group revenue, margin, capacity, debt)
P = []

def add(**k):
    P.append(k)

# ---------------- Stage 1: Q1FY25 (30-Jul-2024) ----------------
add(said_on="2024-07-30", slug="fy25-revenue-growth-25pct", speaker=SB, category="revenue_growth",
    title="FY25 revenue growth ~25% over FY24",
    quote="As of now, guidance continues to be a 25% growth over last year's revenue.",
    metric="Consolidated revenue growth YoY", target="+25% (FY24 base INR 3,282 cr -> ~INR 4,100 cr)", deadline="2026-03-31" if False else "2025-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=3)
add(said_on="2024-07-30", slug="revenue-25pct-next-two-years", speaker=CFO, category="revenue_growth",
    title="Revenue growth above 25% in each of FY25 and FY26",
    quote="expect to gross revenue growth in excess of 25% each year for the next 2 financial years",
    metric="Consolidated revenue growth YoY", target=">25% in FY25 and in FY26", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=True, materiality=3)
add(said_on="2024-07-30", slug="fy25-order-inflow-4500-5000cr", speaker=SB, category="order_inflow",
    title="FY25 order inflow INR 4,500-5,000 cr",
    quote="our aspiration is that we should secure anywhere between INR4,500 crores to INR5,000 crores of orders this year",
    metric="Order inflow FY25", target="INR 4,500-5,000 cr", deadline="2025-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=2)
add(said_on="2024-07-30", slug="engineering-margin-11-12pct", speaker=SB, category="margin",
    title="Engineering segment EBITDA margin to stay in 11-12% band",
    quote="We have clocked the desired margin range of 11% to 12% now for the past many quarters. Going forward also, we will see a consistent margin performance",
    metric="Engineering segment EBITDA margin", target="11-12%", deadline="ongoing (checked through FY26)",
    deadline_precision="vague", specificity="range", volunteered=True, materiality=3)
add(said_on="2024-07-30", slug="consolidated-margin-11-12pct-few-years", speaker=SB, category="margin",
    title="Consolidated EBITDA margin to 11-12% 'in the next few years'",
    quote="a very clear opportunity for us to move into the 11%, 12% consolidated basis for the company in the next few years",
    metric="Consolidated EBITDA margin", target="11-12% (from ~9.6-10%)", deadline="~FY27-FY28 (unstated)",
    deadline_precision="vague", specificity="range", volunteered=False, materiality=3)
add(said_on="2024-07-30", slug="capacity-75k-tonnes-expansion", speaker=SB, category="capacity_commissioning",
    title="Towers & poles capacity 300k -> 375k tonnes (+75k t) with ~INR 200 cr capex",
    quote="we will have a capacity of 300,000 tonnes, which we are expanding by 25% to increase by 75,000 tonnes",
    metric="Installed tower/pole capacity", target="375,000 MTPA; +INR 800-1,000 cr revenue potential", deadline="FY25 capex year (date given later as Mar-2025)",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=3)
add(said_on="2024-07-30", slug="fy25-utilisation-90pct", speaker=SB, category="other",
    title="FY25 capacity utilisation ~90% (from ~70%)",
    quote="Last year, we were at roughly about 70% utilization. This year, we expect to be about 90% utilization.",
    metric="Engineering capacity utilisation", target="~90%", deadline="2025-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=1)
add(said_on="2024-07-30", slug="interest-below-4-5pct-of-revenue", speaker=SB, category="debt_reduction",
    title="Finance cost below 4.5% of revenue in FY25",
    quote="Our aspiration is to go below 4.5%.",
    metric="Interest / revenue", target="<4.5%", deadline="2025-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=2)
add(said_on="2024-07-30", slug="no-further-equity-beyond-rights", speaker=SB, category="other",
    title="No further capital raising beyond the rights issue; internal accruals sufficient",
    quote="we don't have any immediate plans -- beyond the rights issue as the company because we feel that the internal accruals of the company will be strong enough to meet our growth plans",
    metric="Equity dilution", target="No new equity raise beyond rights issue", deadline="near term (unstated)",
    deadline_precision="vague", specificity="vague", volunteered=False, materiality=2)
add(said_on="2024-07-30", slug="debt-moderate-growth-with-topline", speaker=SB, category="debt_reduction",
    title="Debt to grow only moderately, in line with top line, during capex",
    quote="you can expect some moderate growth in the overall debt number in line with the overall top line of the company",
    metric="Gross borrowings", target="growth <= revenue growth", deadline="2025-03-31",
    deadline_precision="fiscal-year", specificity="vague", volunteered=False, materiality=2)
add(said_on="2024-07-30", slug="polymer-1000cr-double-digit-margin", speaker=AD, category="revenue_growth",
    title="Polymer (pipes) revenue ~INR 1,000 cr in 2-3 years with double-digit margin",
    quote="once we are closer to INR1,000 crores kind of a number, you will -- you can expect a double-digit kind of margin ... In the next 2 to 3 years' time, we see reaching up to that level.",
    metric="Polymer segment revenue / EBITDA margin", target="~INR 1,000 cr revenue (FY24: ~450 cr); >=10% margin", deadline="FY27 (2-3 yrs from Jul-2024)",
    deadline_precision="range", specificity="range", volunteered=False, materiality=1)

# ---------------- Stage 1b: Q2FY25 (29-Oct-2024) ----------------
add(said_on="2024-10-29", slug="75k-commissioning-by-mar-2025", speaker=SB, category="capacity_commissioning",
    title="75,000 MTPA expansion to be commissioned by March 2025",
    quote="The capacity expansion of 75,000 is well on track. We should be looking to commission it by the end of this financial year. ... This will be by the end of this financial year, by March.",
    metric="Commissioning of +75k t towers/poles capacity", target="375,000 MTPA operational", deadline="2025-03-31",
    deadline_precision="exact-date", specificity="precise", volunteered=False, materiality=3)
add(said_on="2024-10-29", slug="revenue-25pct-cagr-3yrs-10000cr-fy29", speaker=SB, category="revenue_growth",
    title="25% revenue CAGR for 3 years; INR 10,000 cr revenue by ~FY29 (re-affirmed interview guidance)",
    quote="Yes, absolutely. I think all those expectations are definitely still continuing.",
    metric="Consolidated revenue", target="25% CAGR FY25-FY27; INR 10,000 cr by ~FY29", deadline="2029-03-31 (interim check FY26/FY27)",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=3,
    conditionality="analyst read out the interview claims; management affirmed")
add(said_on="2024-10-29", slug="consolidated-margin-11pct-2-3yrs", speaker=SB, category="margin",
    title="Consolidated EBITDA margin ~11% within 2-3 years",
    quote="we'd rather be conservative and outperform",
    metric="Consolidated EBITDA margin", target="~11% (from ~10%)", deadline="FY27 (2-3 yrs from Oct-2024)",
    deadline_precision="range", specificity="range", volunteered=False, materiality=3)
add(said_on="2024-10-29", slug="fy25-utilisation-85pct", speaker=SB, category="other",
    title="FY25 utilisation ~85% ('optimum') - quietly lower than the ~90% said in July",
    quote="the capacity utilization for this whole year, we expect it to be near about 85% and that is more or less the optimum capacity utilization",
    metric="Engineering capacity utilisation", target="~85%", deadline="2025-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=1)
add(said_on="2024-10-29", slug="fundraise-600cr-enabling", speaker=SB, category="other",
    title="Enabling resolution for ~INR 600 cr fund raise; ~INR 800 cr capex over 4 years (estimate)",
    quote="as of now, there is no defined timeline. The company has taken an enabling resolution by the Board ... we will look at the opportune time and go for this fund raise",
    metric="Equity/quasi-equity raise; multi-year capex", target="~INR 600 cr raise; ~INR 800 cr capex FY25-FY28", deadline="enabling valid ~1 year (to ~Oct-2025)",
    deadline_precision="vague", specificity="vague", volunteered=False, materiality=2)
add(said_on="2024-10-29", slug="polymer-growth-in-line-with-company", speaker=SB, category="revenue_growth",
    title="Polymer segment to grow at the company's guided ~20-25% rate",
    quote="No, I think polymer will be similar across what we are guiding for the company.",
    metric="Polymer segment revenue growth", target="~20-25% p.a.", deadline="FY26 (next two years)",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=1)
add(said_on="2024-10-29", slug="quarterly-run-rate-1000-1100cr", speaker=SB, category="revenue_growth",
    title="Quarterly revenue run-rate ~INR 1,000-1,100 cr until new capacity; improvement after",
    quote="Of course, absolutely. And once the new capacity comes online, of course, definitely, we should be expecting an improvement in that.",
    metric="Quarterly revenue", target="INR 1,000-1,100 cr/qtr in H2FY25; higher once 75k t is online", deadline="2025-03-31 then FY26",
    deadline_precision="quarter", specificity="range", volunteered=False, materiality=2)

# ---------------- Stage 2a: Q3FY25 (06-Feb-2025) ----------------
add(said_on="2025-02-06", slug="75k-major-part-q4-spill-q1", speaker=SB, category="capacity_commissioning",
    title="75k t: 'major part' commissioned in Q4FY25, some spill-over to Q1FY26; revenue potential now INR 700 cr",
    quote="we are looking to commission part of the facility within quarter 4 and some amount of the commissioning will spill over to quarter 1 next year ... the overall revenue potential of this capacity expansion is about INR700 crores",
    metric="Commissioning of +75k t; revenue potential", target="major part by Mar-2025, rest Q1FY26; INR 700 cr potential (was 800-1,000)", deadline="2025-06-30",
    deadline_precision="quarter", specificity="range", volunteered=False, materiality=3)
add(said_on="2025-02-06", slug="new-capacity-80-85pct-util-by-q2fy26", speaker=SB, category="capacity_commissioning",
    title="New 75k t capacity at 80-85% utilisation by end-Q2FY26",
    quote="I think we should be able to achieve it by the end of quarter 2, we should be able to achieve 80%, 85% utilization.",
    metric="Utilisation of new capacity", target="80-85%", deadline="2025-09-30",
    deadline_precision="quarter", specificity="precise", volunteered=False, materiality=2)
add(said_on="2025-02-06", slug="substation-epc-significant-revenue-fy27", speaker=SB, category="new_product",
    title="Substation EPC (new EPC arm): first major order soon; significant revenue from FY27; industry-average margins",
    quote="I don't expect much revenues in FY '26, but FY '27 onwards, we can expect significant revenue.",
    metric="Substation EPC orders / revenue / margin", target="first major order (~INR 60-70 cr) near term; 'significant' revenue FY27+; >= industry margin (13-15%)", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="vague", volunteered=True, materiality=2,
    conditionality="opening remarks volunteered the substation entry; FY27 timing given on analyst question")
add(said_on="2025-02-06", slug="capex-fy26-200-250cr-min-75kt-per-year", speaker=SB, category="capex",
    title="FY26 capex ~INR 200-250 cr; add at least 75k t capacity per year",
    quote="we are expecting another INR200 crores to INR250 crores of capex in the coming financial year FY '26 ... we will definitely be planning minimum 75,000 tons, maybe higher in the years to come",
    metric="Annual capex / capacity adds", target="INR 200-250 cr FY26; >=75k t per year", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=2)
add(said_on="2025-02-06", slug="no-specific-growth-guidance", speaker=SB, category="revenue_growth",
    title="Declines to repeat the 25% CAGR guidance ('refrain from putting any specific guidance numbers')",
    quote="We are certainly looking at robust revenue growth even on this elevated base. I would refrain from putting any specific guidance numbers on the growth.",
    metric="Guidance behaviour", target="(guidance withdrawn three months after re-affirmation)", deadline="n/a",
    deadline_precision="vague", specificity="vague", volunteered=False, materiality=1, status="not-a-promise")
add(said_on="2025-02-06", slug="polymer-healthier-fy26", speaker=SB, category="revenue_growth",
    title="Polymer to post 'much healthier numbers' in FY26 (JJM restart, stable commodity prices)",
    quote="we will see much healthier numbers in this division in the next year",
    metric="Polymer segment revenue", target="clear growth in FY26", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="vague", volunteered=False, materiality=1)

# ---------------- Stage 2b: Q4FY25 (30-Apr-2025) ----------------
add(said_on="2025-04-30", slug="75k-full-capacity-within-q1fy26", speaker=SB, category="capacity_commissioning",
    title="Full 75k t online within Q1FY26 (presentation: fully operational from May-2025)",
    quote="part of the capacity is already online and the full capacity of 75,000 will be available to us within quarter 1",
    metric="Commissioning of +75k t", target="fully operational", deadline="2025-06-30",
    deadline_precision="quarter", specificity="precise", volunteered=True, materiality=3,
    conditionality="volunteered in opening remarks ('on track ... fully operational from May 25'); analyst then pointed out the original Q4FY25 date")
add(said_on="2025-04-30", slug="fy26-revenue-growth-20-25pct", speaker=SB, category="revenue_growth",
    title="Revenue growth 20-25% in FY26 (and next 2-3 years) on the elevated base",
    quote="We will continue to target about 20% to 25% growth even on this elevated base.",
    metric="Consolidated revenue growth YoY", target="+20-25% (FY25 base INR 4,624 cr -> INR 5,549-5,780 cr)", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=3)
add(said_on="2025-04-30", slug="finance-cost-near-4pct-fy26", speaker=SB, category="debt_reduction",
    title="Finance cost to fall toward ~4% of sales in FY26 (from ~4.4-4.6%)",
    quote="for the full year FY '26, we should be coming closer -- this declining trend should continue, and we should be coming closer to a 4% kind of a finance cost based on revenue",
    metric="Interest / revenue", target="~4%", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=2)
add(said_on="2025-04-30", slug="working-capital-cashflow-improve-fy26", speaker=SB, category="working_capital",
    title="Cash flow and working capital to 'improve considerably' in FY26",
    quote="Cash flow and working capital are expected to improve considerably going forward, considering the quality of order intake this year.",
    metric="Working-capital days / debtor days / CFO", target="further improvement on FY25 (debtor days 55, WC days 28 per screener)", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="vague", volunteered=True, materiality=3)
add(said_on="2025-04-30", slug="polymer-growth-25-30pct-fy26", speaker=SB, category="revenue_growth",
    title="Polymer revenue growth 25-30% in FY26-FY27",
    quote="I think on the polymer side, we can expect a little higher growth between 25% to 30%.",
    metric="Polymer segment revenue growth", target="+25-30% (FY25 base ~INR 455 cr)", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=1)
add(said_on="2025-04-30", slug="infra-growth-20-25pct-margin-6pct", speaker=SB, category="revenue_growth",
    title="Infra segment to grow 20-25% in FY26 at ~6% EBITDA margin",
    quote="The overall guidance of 20%, 25% will be maintained here as well in the Infra segment.",
    metric="Infra segment revenue growth / margin", target="+20-25% (FY25 INR 674 cr); margin ~6%", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=2)
add(said_on="2025-04-30", slug="second-75kt-expansion-fy26", speaker=SB, category="capacity_commissioning",
    title="A further 75k t capacity to be added in FY26 (brownfield + greenfield)",
    quote="We will be adding a further amount of 75,000 tons this year also.",
    metric="Second +75k t capacity", target="450k t total", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=2)
add(said_on="2025-04-30", slug="qip-on-hold-capex-from-accruals", speaker=SB, category="other",
    title="QIP put on hold; capex to be met from debt + internal accruals",
    quote="we have put that decision on hold ... we are able to meet all our capex requirements through a mix of debt and internal accruals",
    metric="Equity dilution", target="no equity raise near term", deadline="vague",
    deadline_precision="vague", specificity="vague", volunteered=False, materiality=2)
add(said_on="2025-04-30", slug="inventory-days-below-95", speaker=SB, category="working_capital",
    title="Inventory days to come down further from ~95",
    quote="we certainly feel that there is opportunity to bring this down further from 95 days",
    metric="Inventory days (company definition)", target="<95 days", deadline="FY26 (implied)",
    deadline_precision="vague", specificity="vague", volunteered=False, materiality=1)

# ---------------- Stage 3a: Q1FY26 (31-Jul-2025) ----------------
add(said_on="2025-07-31", slug="fy26-revenue-growth-25pct-plus", speaker=SB, category="revenue_growth",
    title="FY26 revenue growth 25%+ (raised from 20-25% three months earlier)",
    quote="we are confident of delivering a 25% plus revenue growth for FY '26",
    metric="Consolidated revenue growth YoY", target=">=+25% (FY25 base INR 4,624 cr -> >= INR 5,780 cr)", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=True, materiality=3,
    conditionality="also volunteered in closing remarks: 'revenue growth in excess of 25% for the current financial year'")
add(said_on="2025-07-31", slug="fy26-ebitda-margin-plus-50bp", speaker=SB, category="margin",
    title="FY26 consolidated EBITDA margin at least +50 bp over FY25 (~9.8% -> >=10.3%)",
    quote="we are quite confident that we should be able to deliver at least a 50 basis point improvement in EBITDA margins over last year",
    metric="Consolidated EBITDA margin", target=">=10.3% (FY25 reported 9.8%)", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=3)
add(said_on="2025-07-31", slug="fy26-order-inflow-6500-7000cr", speaker=SB, category="order_inflow",
    title="FY26 order inflow INR 6,500-7,000 cr",
    quote="We expect that our total order inflow for this year should be in the range of INR6,500 crores to INR7,000 crores.",
    metric="Order inflow FY26", target="INR 6,500-7,000 cr", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=2)
add(said_on="2025-07-31", slug="fy26-export-inflow-double-1500cr", speaker=SB, category="order_inflow",
    title="Export order inflow to double to ~INR 1,500-1,600 cr in FY26",
    quote="We have been on an average, taking INR700 crores to INR800 crores of export orders every year. That we should double to INR1,500 crores this year for sure.",
    metric="Export order inflow FY26", target="INR 1,500-1,600 cr", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=2)
add(said_on="2025-07-31", slug="second-75kt-by-mar-2026", speaker=SB, category="capacity_commissioning",
    title="Second 75k t block to be commissioned by end-FY26",
    quote="further capacity expansion plan is taken on for another 75,000, which we hope to commission by end of this financial year",
    metric="Second +75k t commissioning", target="450k t installed", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=2)
add(said_on="2025-07-31", slug="capacity-600k-tonnes-by-fy28", speaker=SB, category="capacity_commissioning",
    title="Capacity 600,000 t by FY28-end ('world's largest transmission tower manufacturer')",
    quote="we have embarked on another 75,000 million tons per annum capacity expansion with a bold vision to become the world's largest transmission tower manufacturer with 6 lakh million tons capacity by FY '28 end",
    metric="Installed tower/pole capacity", target="600,000 MTPA (from 375,000)", deadline="2028-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=True, materiality=3)
add(said_on="2025-07-31", slug="polymer-double-digit-margin-fy27", speaker=SB, category="margin",
    title="Polymer EBITDA margin to double digits 'next year' (FY27)",
    quote="Probably not this year, but yes, next year would be a reasonable expectation.",
    metric="Polymer segment EBITDA margin", target=">=10% (now low single digit)", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=1)
add(said_on="2025-07-31", slug="revenue-25pct-next-2-3-years", speaker=SB, category="revenue_growth",
    title="~25% revenue growth for the next 2-3 years incl. FY27, driven by capacity additions",
    quote="we are sticking to the 25% revenue guidance ... 25% is what the reasonable you can expect from the company over the next 2 to 3 years",
    metric="Consolidated revenue growth YoY", target="~25% p.a. FY26-FY28", deadline="2027-03-31 (first check FY27)",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=3)
add(said_on="2025-07-31", slug="capex-funding-60-debt-40-accruals", speaker=SB, category="capex",
    title="Next 75k t (INR 200-250 cr/block; ~INR 600 cr over 3 yrs) funded ~60% term debt / 40% accruals",
    quote="It will be a mix of internal accruals and term loan ... maybe this year could be maybe 60% debt and 40% internal accruals",
    metric="Capex funding mix", target="no equity; ~60:40 debt:accruals", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=2)

# ---------------- Stage 3b: Q2FY26 (07-Nov-2025) ----------------
add(said_on="2025-11-07", slug="fy26-25pct-reaffirmed-monsoon", speaker=SB, category="revenue_growth",
    title="FY26 25% growth re-affirmed after H1 +14%; H1 shortfall blamed on Rajasthan monsoon (timing only)",
    quote="the moderation in top line growth is largely just, I think, timing related and temporary ... we don't see a challenge in delivering the overall 25% revenue growth for the full year",
    metric="Consolidated revenue growth YoY", target="+25% FY26 (needs ~INR 3,264 cr in H2)", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=3,
    conditionality="also volunteered in closing remarks ('around 25% revenue CAGR growth for FY 26')")
add(said_on="2025-11-07", slug="fy26-closing-order-book-9000-10000cr", speaker=SB, category="order_book",
    title="FY26 closing order book INR 9,000-10,000 cr",
    quote="We expect that this should be somewhere between INR9,000 crores to INR10,000 crores as a closing order book by the end of the year.",
    metric="Closing order book Mar-2026", target="INR 9,000-10,000 cr", deadline="2026-03-31",
    deadline_precision="exact-date", specificity="range", volunteered=False, materiality=2)
add(said_on="2025-11-07", slug="fy26-order-inflow-6000cr-plus", speaker=SB, category="order_inflow",
    title="FY26 order inflow 'INR 6,000 cr plus' (quietly below the 6,500-7,000 said in July)",
    quote="For the full year, we have guided that, okay, we will be -we are targeting an intake of INR6,000 crores plus.",
    metric="Order inflow FY26", target=">INR 6,000 cr", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=2)
add(said_on="2025-11-07", slug="fy26-margin-10-10-5pct", speaker=SB, category="margin",
    title="FY26 EBITDA margin ~10-10.5% (similar to H1 10.3%)",
    quote="Yes. We expect this to be at a similar level for the full year also. ... Very much, yes.",
    metric="Consolidated EBITDA margin", target="10.0-10.5%", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=2)
add(said_on="2025-11-07", slug="export-order-mix-50pct-2-3yrs", speaker=SB, category="order_book",
    title="Export share of order book to reach ~50% in 2-3 years (from 11%)",
    quote="Our internal aspiration is that long term, we should be having an order mix of 50-50 ... But I think it will take us at least 2, 3 years to get there.",
    metric="Export share of order book", target="~50% (25% developed, 25% developing markets)", deadline="FY28 (2-3 yrs from Nov-2025; 'at least')",
    deadline_precision="range", specificity="range", volunteered=False, materiality=2)
add(said_on="2025-11-07", slug="polymer-600cr-fy26-1000cr-fy27-28", speaker=SB, category="revenue_growth",
    title="Polymer ~INR 600 cr in FY26; INR 1,000 cr in FY27 or FY28; double-digit margin now 'long term'",
    quote="for the full year, certainly, I think we can look at a number closer to INR600 crores odd in this division. And then I would say that INR1,000 crores number should be possible, maybe if not next year, certainly in the year after that ... [double digit margin] It's long term.",
    metric="Polymer segment revenue / margin", target="~INR 600 cr FY26; INR 1,000 cr by FY28", deadline="2026-03-31 (600 cr); 2028-03-31 (1,000 cr)",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=1)
add(said_on="2025-11-07", slug="substation-projects-commission-fy27", speaker=SB, category="new_product",
    title="Two substation EPC projects (132 kV, 220 kV) to be commissioned in FY27, then bid for larger jobs",
    quote="the company is executing 2 small and medium-sized projects right now. And we are targeting commissioning of these projects in the next financial year",
    metric="Substation EPC commissioning / qualification", target="2 projects commissioned; qualify for large substations", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=1)
add(said_on="2025-11-07", slug="net-debt-range-bound", speaker=SB, category="debt_reduction",
    title="Net debt + acceptances to stay ~range-bound (~INR 1,268 cr at Sep-25); D/E ~0.6",
    quote="with the growing business, there might be some increase in this. But I would say that even if it is range bound at this level, we would not be surprised",
    metric="Net debt incl. acceptances", target="~INR 1,268 cr, roughly flat", deadline="2026-03-31",
    deadline_precision="vague", specificity="vague", volunteered=False, materiality=2)
add(said_on="2025-11-07", slug="long-term-margin-12pct", speaker=SB, category="margin",
    title="Long-term EBITDA margin aspiration ~12% (from 10-10.5%)",
    quote="Long term, we do aspire that our margins should move from the current 10%, 10.5% level to 12% level in the longer term.",
    metric="Consolidated EBITDA margin", target="~12%", deadline="long term (unstated)",
    deadline_precision="vague", specificity="vague", volunteered=False, materiality=2)

# ---------------- Stage 4a: Q3FY26 (29-Jan-2026) ----------------
add(said_on="2026-01-29", slug="fy26-guidance-cut-to-20pct", speaker=SB, category="revenue_growth",
    title="FY26 revenue guidance cut to ~20-22% (25% re-labelled an 'aspiration'); Q4 to grow 25-30%",
    quote="certainly an overall growth of anything between 21%, 22% is on the cards for the full year. Again, the 25% is -- was our aspirational growth for the full year.",
    metric="Consolidated revenue growth YoY", target="+20-22% FY26; Q4FY26 +25-30% YoY", deadline="2026-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=3,
    conditionality="cut appeared only in the presentation; explained only after analyst asked")
add(said_on="2026-01-29", slug="fy27-order-inflow-grow-20pct", speaker=SB, category="order_inflow",
    title="FY27 order inflow to grow ~20% (in line with revenue)",
    quote="I mean, definitely. I mean I think our aspiration will be that, it should be happening.",
    metric="Order inflow FY27", target="~+20% vs FY26 (~INR 6,800 cr on FY26 actual 5,678)", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=2)

# ---------------- Stage 4b: Q4FY26 (28-Apr-2026) ----------------
add(said_on="2026-04-28", slug="fy27-revenue-15pct-pat-30pct", speaker=SB, category="revenue_growth",
    title="FY27 guidance: revenue +15%, PAT ~+30%",
    quote="For FY '27, we are giving a guidance of 15% growth on revenue and approximately a 30% growth in bottom line.",
    metric="Consolidated revenue / PAT growth FY27", target="revenue ~INR 6,386 cr (+15%); PAT ~INR 270 cr (+30% on 207 cr)", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=3,
    conditionality="framed as 'conservative' because of export/Middle East and freight; 'effort will be to go higher'")
add(said_on="2026-04-28", slug="back-to-20-25pct-from-fy28", speaker=SB, category="revenue_growth",
    title="Revenue growth to return to 20-25% from FY28",
    quote="for sure, we can expect to come back to the 20% to 25% growth run rate from next year onwards",
    metric="Consolidated revenue growth YoY", target="+20-25%", deadline="2028-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=3)
add(said_on="2026-04-28", slug="450kt-by-june-2026", speaker=SB, category="capacity_commissioning",
    title="Second 75k t block (450k t total) by June-2026 (slipped from March-2026)",
    quote="we are on track to reach 450,000 tons per year capacity by June '26 ... This is a spillover from last year, which we were expecting to commission in March, but now that is extended till June.",
    metric="Second +75k t commissioning", target="450,000 MTPA", deadline="2026-06-30",
    deadline_precision="quarter", specificity="precise", volunteered=True, materiality=2)
add(said_on="2026-04-28", slug="fy27-capex-250cr-75kt-fy27-fy28", speaker=SB, category="capex",
    title="FY27 capex ~INR 250 cr; +75k t in FY27 and +75k t in FY28 to reach 600k t",
    quote="For FY '27, our capex guidance will be similar to previous years. It will be about INR250 crores. ... we'll be taking on another 75,000 plus 75,000 in the next 2 financial years in FY '27 and '28.",
    metric="Capex / capacity", target="INR ~250 cr FY27; 525k t by FY27-end; 600k t by FY28-end", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=2)
add(said_on="2026-04-28", slug="debtors-normalise-after-march-spike", speaker=SB, category="working_capital",
    title="Receivables spike (FY26 debtors ~INR 1,485 cr, ~2x) is timing-related; INR 600-700 cr already collected in April",
    quote="none of them are sticky debtors ... close to about INR260 crores of funds, which was supposed to receive on the last week of March was received on the 1st and the 2nd of April ... we have already realized close to about INR600 crores to INR700 crores of debtors in the month of April itself",
    metric="Trade receivables / debtor days", target="normalise in FY27 (implied)", deadline="2027-03-31 (implied)",
    deadline_precision="vague", specificity="vague", volunteered=False, materiality=3,
    conditionality="explanation given only when an analyst asked; not mentioned in opening remarks, which said 'stronger cash generation'")
add(said_on="2026-04-28", slug="fy27-margin-up-toward-12pct", speaker=SB, category="margin",
    title="FY27 EBITDA margin to rise (no number); long-term 12%",
    quote="we definitely should be able to increase margins, but I'm not able to give an exact guidance ... long term, we will definitely move towards our aspirational margin of 12%",
    metric="Consolidated EBITDA margin", target=">10.3% in FY27", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="vague", volunteered=False, materiality=2)

# ---------------- Stage 5a: Q1FY27 (12-Aug-2026) ----------------
add(said_on="2026-08-12", slug="450kt-by-end-q2fy27", speaker=SB, category="capacity_commissioning",
    title="450k t: 'commissioning by the end of quarter 2' FY27 (fourth date for the second 75k t block)",
    quote="there's only a few months deferment in the capacity expansion. So we are going to be commissioning by the end of quarter 2.",
    metric="Second +75k t commissioning", target="450,000 MTPA", deadline="2026-09-30",
    deadline_precision="quarter", specificity="precise", volunteered=False, materiality=2,
    conditionality="opening remarks of the same call said 'during the second half of the year'")
add(said_on="2026-08-12", slug="fy27-finance-cost-3-2-3-5pct", speaker=SB, category="debt_reduction",
    title="FY27 finance cost 3.2-3.5% of revenue after the equity raise",
    quote="this year, our finance cost should be somewhere between 3.2% to 3.5% for the whole year after this fundraise",
    metric="Interest / revenue", target="3.2-3.5%", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=2)
add(said_on="2026-08-12", slug="fy27-order-inflow-7000cr-ob-10000cr", speaker=SB, category="order_inflow",
    title="FY27 order inflow INR 7,000 cr+ (export ~INR 1,100 cr, +50%); closing order book INR 10,000 cr+",
    quote="we should be able to do INR7,000 crores plus for this year ... And that should take us to a closing order book of INR10,000 crores plus ... About INR1,100 crores -- about INR1,100 crores. As I mentioned a 50% jump over last year.",
    metric="Order inflow / export inflow / closing order book FY27", target="inflow >=7,000 cr; export ~1,100 cr; OB >=10,000 cr", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=2)
add(said_on="2026-08-12", slug="polymer-growth-20pct-fy27", speaker=SB, category="revenue_growth",
    title="Polymer revenue +20% in FY27 with some margin improvement",
    quote="we are quite confident that for the full year, we will be able to deliver a 20% improvement -- a 20% growth in top line with some improvement in margins as well",
    metric="Polymer segment revenue growth", target="+20% (FY26 ~507 cr -> ~608 cr)", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=1)

# ---------------- Stage 5b: Q2FY27 (30-Oct-2026) ----------------
add(said_on="2026-10-30", slug="fy27-revenue-15pct-at-worst-13-14", speaker=SB, category="revenue_growth",
    title="FY27 revenue: 'largely in line' with +15%; 'at worst' 13-14% (H1 +7%)",
    quote="at worst, we may see 1% or 2% drop from our 15% guidance",
    metric="Consolidated revenue growth YoY", target="+13-15% (needs ~+21-22% in H2)", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=3)
add(said_on="2026-10-30", slug="fy27-inflow-7500cr-export-1500cr", speaker=SB, category="order_inflow",
    title="FY27 order inflow INR 7,500 cr incl. INR 1,500 cr exports ('maintain the guidance given last time')",
    quote="We maintain our order inflow guidance of INR7,500 crores ... we maintain our guidance of INR1,500 crores of total export order inflow this year",
    metric="Order inflow / export inflow FY27", target="7,500 cr total; 1,500 cr export (Aug said 7,000+ and ~1,100)", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=False, materiality=2,
    conditionality="'maintain' although the August figures were 7,000+ and ~1,100: an upward revision presented as unchanged")
add(said_on="2026-10-30", slug="450kt-end-q3-or-early-q4-fy27", speaker=SB, category="capacity_commissioning",
    title="450k t now 'end of Q3 or latest beginning of Q4' FY27 (fifth date)",
    quote="It could possibly take place in the end of quarter 3 itself or latest, at the beginning part of quarter 4.",
    metric="Second +75k t commissioning", target="450,000 MTPA", deadline="2027-01-31",
    deadline_precision="quarter", specificity="range", volunteered=False, materiality=2)
add(said_on="2026-10-30", slug="600kt-by-fy29-greenfield", speaker=SB, category="capacity_commissioning",
    title="600k t now 'by FY29' via greenfield (phase 1 end-FY28, phase 2 end-FY29)",
    quote="We continue to work towards our longer-term capacity road map of 600,000 tons by FY29",
    metric="Installed tower/pole capacity", target="600,000 MTPA", deadline="2029-03-31",
    deadline_precision="fiscal-year", specificity="precise", volunteered=True, materiality=2,
    conditionality="stated in opening remarks with no mention that the July-2025 target was FY28-end")
add(said_on="2026-10-30", slug="nwc-days-90-100-stable", speaker=SB, category="working_capital",
    title="Net working-capital days to hold in a '90-100 days stable region'",
    quote="the net working capital days of the company should be in this 90 to 100 days stable region",
    metric="Net working-capital days (company definition)", target="90-100 days", deadline="ongoing (check FY27)",
    deadline_precision="vague", specificity="range", volunteered=False, materiality=2,
    conditionality="replaces the Apr-2025 'improve considerably' language; company quoted 62 days (Sep-24) and 88 days (Dec-24)")
add(said_on="2026-10-30", slug="fy27-margin-10-11pct-come-what-may", speaker=SB, category="margin",
    title="FY27 EBITDA margin 10-11% 'come what may'; expansion may be smaller than targeted",
    quote="if cost pressures continue the way they are, then perhaps the margin expansion will not be as high as what we had targeted ... [10-11% range?] Absolutely. Absolutely.",
    metric="Consolidated EBITDA margin", target="10-11% (H1FY27 ~10.6%)", deadline="2027-03-31",
    deadline_precision="fiscal-year", specificity="range", volunteered=False, materiality=2)

# =====================================================================
# SCORING (as of 2026-11-19). Rule used: delivered >= 95% of target (low end of a range) and on time;
# partly = 80-95% of target, or <= 1 quarter late; missed = < 80% or > 1 quarter late;
# moved-goalpost = target/date changed in a later call without acknowledging the change;
# withdrawn = explicitly lowered with an explanation; silently-dropped = never repeated for >= 4 calls;
# pending = deadline not reached; unverifiable = deadline passed but no public number to check.
# Sources for actuals: later transcripts (company-reported) + screener.in consolidated (fetched 2026-11-19).
# =====================================================================
S = {}
def st(slug, status, evidence, **k):
    S[slug] = dict(status=status, evidence=evidence, **k)

st("fy25-revenue-growth-25pct", "delivered", "FY25 revenue INR 4,624 cr vs FY24 3,282 cr = +40.9% (screener; company Q4FY25 call: 'robust growth of 41%').",
   delivered_value="+41%", delivery_ratio=1.64, confidence="verified")
st("revenue-25pct-next-two-years", "partly", "FY25 +41% (beat); FY26 revenue 5,552.8 cr = +20.1% (Q4FY26 call; screener 5,553) vs >25% promised. One of two years delivered.",
   delivered_value="FY25 +41%, FY26 +20%", delivery_ratio=0.8, explanation_for_miss="Rajasthan monsoon, second-capacity delay, export/Middle East disruption (given Nov-25 and Jan-26, only when asked)", admitted_unprompted=False, confidence="verified")
st("fy25-order-inflow-4500-5000cr", "delivered", "FY25 order inflow INR 5,335 cr (Q4FY25 call, 'highest ever'), above the top of the range.",
   delivered_value="INR 5,335 cr", delivery_ratio=1.19)
st("engineering-margin-11-12pct", "delivered", "Company-reported Engineering EBITDA margin: Q1FY25 11.0%, Q2FY25 11.5%, FY25 ~11.2% (40 bp below FY24 11.6%, per Q4FY25 Q&A), Q1FY26 11.3%. Stayed inside band; FY26 full-year segment margin not disclosed in calls read.",
   delivered_value="~11.2-11.5%", delivery_ratio=1.0)
st("consolidated-margin-11-12pct-few-years", "pending", "Consolidated EBITDA margin FY25 9.8%, FY26 10.3%, H1FY27 ~10.6% (company). By Nov-25 the band became '12% in the longer term'. No date was ever given, so it cannot be scored yet.",
   later_restatements="Oct-24: ~11% in 2-3 yrs; Nov-25: 12% longer term; Apr-26 / Oct-26: 'aspirational 12%'")
st("capacity-75k-tonnes-expansion", "partly", "+75k t was 'fully installed and commercially operational' by the Q1FY26 call (31-Jul-2025). Cost ~INR 200 cr as promised. Revenue potential was cut to INR 700 cr (Feb-25), then restored to ~INR 1,000 cr (Jul-25). Delivered about one quarter late against the Mar-2025 date given in Oct-24.",
   delivered_value="375k t by Q1FY26", delivery_ratio=1.0, explanation_for_miss="none given; 'part ... spill over' (Feb-25, prompted)", admitted_unprompted=False)
st("fy25-utilisation-90pct", "moved-goalpost", "Three months later (Oct-24) FY25 utilisation was 'near about 85% ... the optimum', with no reference to the 90% said in July. Q4FY25: 'near about 80-85% now'.",
   delivered_value="~80-85%", delivery_ratio=0.92, admitted_unprompted=False)
st("interest-below-4-5pct-of-revenue", "missed", "FY25 finance cost INR 214 cr / revenue INR 4,624 cr = 4.63% (screener). Management's own later baseline for FY25: 'about 4.7%' (Nov-25), '4.8%' (Jan-26). In Apr-25 it said '4.4% right now', a quarterly figure.",
   delivered_value="4.6-4.8%", delivery_ratio=0.96, explanation_for_miss="none; the miss was never acknowledged, and the FY25 base was later quoted higher, which flatters the FY26 improvement", admitted_unprompted=False)
st("no-further-equity-beyond-rights", "missed", "Three months later (Oct-24) the Board took an enabling resolution for ~INR 600 cr. A QIP was put on hold (Apr-25). Then a INR 433.5 cr preferential issue to institutions (Jul/Aug-2026). Free cash flow was negative in FY25 (-83 cr) and FY26 (-88 cr) (screener), so 'internal accruals strong enough' did not hold.",
   delivered_value="INR 433.5 cr equity raised", delivery_ratio=0.0, explanation_for_miss="Aug-26: to strengthen the balance sheet and be ready for capex/M&A (volunteered in opening remarks)", admitted_unprompted=True)
st("debt-moderate-growth-with-topline", "delivered", "Borrowings Mar-24 592 -> Mar-25 711 cr (+20%) vs revenue +41% (screener). Company: net debt incl. acceptances fell INR 111 cr to 1,016 cr.",
   delivered_value="+20% debt vs +41% revenue", delivery_ratio=1.0, confidence="verified")
st("polymer-1000cr-double-digit-margin", "moved-goalpost", "Polymer revenue FY25 roughly flat (~INR 450-460 cr), FY26 INR 507 cr; FY27 guide +20% (~608 cr). The INR 1,000 cr date moved to 'if not next year, certainly the year after' (Nov-25, i.e. FY28), then had no date (Apr-26: 'as we get closer to ... 1,000 crores'). The double-digit margin became 'long term' (Nov-25).",
   delivered_value="FY26 INR 507 cr; margin low single digit", delivery_ratio=0.51, explanation_for_miss="JJM cuts, resin price volatility, channel destocking", admitted_unprompted=False)

st("75k-commissioning-by-mar-2025", "partly", "Feb-25: 'major part in Q4', some spill to Q1FY26. Apr-25: 'part ... already online', full within Q1. Jul-25: fully operational. About one quarter late.",
   delivered_value="full by Q1FY26", delivery_ratio=1.0, explanation_for_miss="none beyond 'spill over'; analysts raised the slip each time", admitted_unprompted=False)
st("revenue-25pct-cagr-3yrs-10000cr-fy29", "silently-dropped", "Not repeated in any later call (grep of 8 later transcripts). Three months later (Feb-25) management 'would refrain from putting any specific guidance numbers'. Revenue growth since: FY25 +41%, FY26 +20%, FY27 guide +15%. Note: FY24->FY27e CAGR is ~25% if FY27 delivers +15%, and INR 10,000 cr by FY29 still needs ~25% p.a. in FY28-29. So the target is still reachable, but it was abandoned without comment.",
   delivered_value="FY25 +41%, FY26 +20%", admitted_unprompted=False)
st("consolidated-margin-11pct-2-3yrs", "pending", "FY26 10.3%; H1FY27 ~10.6%; FY27 guided 10-11% (Oct-26), with an admission that expansion may fall short. Deadline FY27: on track to fall short unless H2 margin exceeds 11%.")
st("fy25-utilisation-85pct", "delivered", "Q4FY25 call: 'near about 80%, 85% capacity utilization now'.", delivered_value="80-85%", delivery_ratio=0.97)
st("fundraise-600cr-enabling", "partly", "The enabling resolution lapsed unused. INR 433.5 cr was raised later by preferential issue (Jul-26), about 72% of the size. Capex FY25-FY27 runs ~INR 200-300 cr a year, in line with the ~INR 800 cr/4 yrs estimate.",
   delivered_value="INR 433.5 cr in 2026", delivery_ratio=0.72)
st("polymer-growth-in-line-with-company", "missed", "Polymer FY25 ~flat vs company +41%. FY26 +11% (455->507) vs company +20%.", delivered_value="~0% / +11%", delivery_ratio=0.3,
   explanation_for_miss="JJM allocation cut, commodity volatility (volunteered in Feb-25 and Apr-25 calls)", admitted_unprompted=True)
st("quarterly-run-rate-1000-1100cr", "delivered", "Q3FY25 1,135; Q4FY25 1,288; Q1FY26 1,254; Q2FY26 1,262 cr (screener), at or above the run-rate, then up after the capacity came online.", delivery_ratio=1.0, confidence="verified")

st("75k-major-part-q4-spill-q1", "delivered", "Full 75k t operational within Q1FY26 (Jul-25 call). The revenue-potential figure in the same answer (INR 700 cr) was later restated as ~INR 1,000 cr.", delivery_ratio=1.0)
st("new-capacity-80-85pct-util-by-q2fy26", "delivered", "Q2FY26 call (Nov-25): 'operating at about 85% plus capacity utilization' (overall plant; new-line figure not given).", delivery_ratio=1.0)
st("substation-epc-significant-revenue-fy27", "pending", "First substation EPC order was INR ~45 cr (66 kV), vs 'INR 60-70 cr' expected. Nov-25: two small/medium projects (132/220 kV) to commission in FY27. Apr-26: 'executing close to about 4 high-voltage substations'. No substation revenue disclosed yet.")
st("capex-fy26-200-250cr-min-75kt-per-year", "partly", "FY26 cash used in investing INR 272 cr; CWIP 134 -> 273 cr (screener), so capex was in range. But the FY26 75k t block was not commissioned in FY26; still pending in Nov-26.", delivery_ratio=0.5)
st("polymer-healthier-fy26", "partly", "FY26 polymer revenue INR 507 cr, record high, +11%. But far below the 25-30% guided three months later.", delivered_value="+11%", delivery_ratio=0.5)

st("75k-full-capacity-within-q1fy26", "delivered", "Jul-25 call: '75,000 ... new capacity is now fully installed and commercially operational'.", delivery_ratio=1.0)
st("fy26-revenue-growth-20-25pct", "delivered", "FY26 revenue INR 5,552.8 cr = +20.1% (company; screener 5,553 vs 4,624). Bottom of the range.", delivered_value="+20.1%", delivery_ratio=1.0, confidence="verified")
st("finance-cost-near-4pct-fy26", "delivered", "FY26 finance cost 3.9% of sales (Q4FY26 call); screener 218/5,553 = 3.93%.", delivered_value="3.9%", delivery_ratio=1.0, confidence="verified")
st("working-capital-cashflow-improve-fy26", "partly", "Cash flow improved: CFO INR 153 -> 277 cr; CFO/EBITDA 42% -> 56% (screener). Working capital worsened: trade receivables INR 701 -> 1,485 cr (2.1x on +20% revenue); debtor days 55 -> 98; WC days 28 -> 43 (screener). Company-defined NWC days were 62 (Sep-24) and 88 (Dec-24); in Oct-26 the target became '90-100 days stable'. FCF still -88 cr; cash 121 -> 32 cr.",
   delivered_value="CFO +81%; debtor days +43", delivery_ratio=0.5,
   explanation_for_miss="Apr-26, only when asked: INR 260 cr arrived 1-2 April ('technical reason'); Q4 domestic revenue +45% with slower domestic collections; GST on billing", admitted_unprompted=False, confidence="verified")
st("polymer-growth-25-30pct-fy26", "missed", "FY26 polymer INR 507 cr vs FY25 ~455 cr = ~+11% (company Q4FY26 call 'crossed INR 500 crores'; Nov-25 call gave H1FY25 199 cr).", delivered_value="~+11%", delivery_ratio=0.4,
   explanation_for_miss="falling resin prices: 'volume growth ~40% but value lower' (Apr-26, prompted)", admitted_unprompted=False)
st("infra-growth-20-25pct-margin-6pct", "missed", "FY26 Infra revenue derived as 5,552.8 - Engineering 4,359 - Polymer ~507 = ~INR 687 cr vs FY25 674 cr = ~+2% (derived, single-source). Q1FY26 Infra was -39% YoY.", delivered_value="~+2% (derived)", delivery_ratio=0.1,
   explanation_for_miss="'depends on contract execution' (Jul-25, prompted)", admitted_unprompted=False)
st("second-75kt-expansion-fy26", "missed", "Not commissioned in FY26. Dates given since: Mar-26 -> 'spill over to Q1' (Jan-26) -> June-26 (Apr-26) -> H2FY27 / end-Q2 (Aug-26) -> end-Q3 or early Q4 FY27 (Oct-26). Not operational as of the Oct-26 call.",
   delivery_ratio=0.0, explanation_for_miss="'as like any capex project ... minor delays' (Jan-26, prompted)", admitted_unprompted=False)
st("qip-on-hold-capex-from-accruals", "delivered", "No equity in FY26; FY26 capex (~INR 272 cr) funded by debt (+INR 220 cr) and accruals. The 2026 preferential issue came when 'market situation' allowed, as the statement had left open.", delivery_ratio=1.0)
st("inventory-days-below-95", "delivered", "Inventories INR 1,197 -> 1,059 cr while revenue +20%; screener inventory days 152 -> 109 (a different definition from the company's 95).", delivery_ratio=1.0, confidence="verified")

st("fy26-revenue-growth-25pct-plus", "missed", "FY26 +20.1% vs >=25% (raised from 20-25% in Apr-25). Ratio 0.80 on growth rate; revenue 5,553 vs >=5,780 cr = 96% of the revenue level.",
   delivered_value="+20.1%", delivery_ratio=0.8, explanation_for_miss="Nov-25: Rajasthan monsoon (timing). Jan-26: capacity delay + monsoon; '25% ... was our aspirational growth'. All in answer to analyst questions.", admitted_unprompted=False, confidence="verified")
st("fy26-ebitda-margin-plus-50bp", "delivered", "FY26 EBITDA margin 10.3% vs 9.8% (company); screener 575/5,553 = 10.35% vs 455/4,624 = 9.84%: +51 bp.", delivered_value="+50 bp", delivery_ratio=1.0, confidence="verified")
st("fy26-order-inflow-6500-7000cr", "moved-goalpost", "Lowered to 'INR 6,000 crores plus' at the next call (Nov-25) and described as 'we have guided', with no reference to 6,500-7,000. FY26 actual INR 5,678 cr = 87% of the 6,500 floor.",
   delivered_value="INR 5,678 cr", delivery_ratio=0.87, explanation_for_miss="Apr-26 opening: sector bidding slowed (ROW, transformer/HVDC shortages; CEA held back bids); 'lower than our own estimation' in Q&A", admitted_unprompted=False)
st("fy26-export-inflow-double-1500cr", "missed", "Q1FY27 call put FY27 export inflow at ~INR 1,100 cr = '+50% over last year', which implies FY26 export inflow of ~INR 730 cr. Q2FY27: one quarter's INR 1,055 cr 'surpassed the entire export order inflow of FY26'. Export share of order book stayed 10-11% through FY26.",
   delivered_value="~INR 730 cr (implied)", delivery_ratio=0.48, explanation_for_miss="tariffs, Middle East war, sea-freight spike", admitted_unprompted=True,
   confidence="single-source")
st("second-75kt-by-mar-2026", "missed", "See second-75kt-expansion-fy26: still not operational as of 30-Oct-2026, more than two quarters late.", delivery_ratio=0.0,
   explanation_for_miss="'minor delays' (Jan-26, prompted)", admitted_unprompted=False)
st("capacity-600k-tonnes-by-fy28", "moved-goalpost", "Repeated in Nov-25 and Apr-26 as FY28. Oct-26 opening remarks: '600,000 tons by FY29', with greenfield phases at end-FY28 and end-FY29, and no acknowledgement of the one-year shift.",
   admitted_unprompted=False)
st("polymer-double-digit-margin-fy27", "moved-goalpost", "Four months later (Nov-25): 'It's long term'. Apr-26: tied to reaching ~INR 700-1,000 cr revenue, with no date. FY26 segment margin was still 'low single digits'.", admitted_unprompted=False)
st("revenue-25pct-next-2-3-years", "withdrawn", "FY27 guidance set at +15% (Apr-26), with an explanation: export disruption and weak FY26 inflow ('conservative guidance'). The 20-25% path was pushed to FY28.",
   explanation_for_miss="exports/Middle East, freight, low FY26 order intake (Apr-26, prompted by analyst)", admitted_unprompted=False)
st("capex-funding-60-debt-40-accruals", "partly", "FY26 borrowings +INR 220 cr against ~INR 272 cr investing outflow: ~80% debt-funded, not 60%. Then equity in FY27 repaid debt.", delivery_ratio=0.75)

st("fy26-25pct-reaffirmed-monsoon", "missed", "FY26 +20.1%. H2FY26 revenue 3,037 cr vs ~3,264 cr needed. The guidance was cut to ~20% in the Jan-26 presentation, flagged only when an analyst noticed it.",
   delivered_value="+20.1%", delivery_ratio=0.8, explanation_for_miss="monsoon + capacity delay (Jan-26, prompted)", admitted_unprompted=False, confidence="verified")
st("fy26-closing-order-book-9000-10000cr", "partly", "Closing order book Mar-26 INR 8,501.9 cr = 94.5% of the 9,000 floor (Q4FY26 call).", delivered_value="INR 8,502 cr", delivery_ratio=0.945,
   explanation_for_miss="muted sector bidding", admitted_unprompted=False)
st("fy26-order-inflow-6000cr-plus", "partly", "FY26 inflow INR 5,678 cr = 94.6% of 6,000 (Q4FY26 call). Management: 'lower than our own estimation' (Apr-26 Q&A). Q1FY27 opening: 'We ended last year with a lower-than-expected order inflow'.",
   delivered_value="INR 5,678 cr", delivery_ratio=0.946, explanation_for_miss="subdued domestic bidding (CEA, ROW, equipment) + export geopolitics", admitted_unprompted=True)
st("fy26-margin-10-10-5pct", "delivered", "FY26 EBITDA margin 10.3% (company), 10.35% (screener).", delivered_value="10.3%", delivery_ratio=1.0, confidence="verified")
st("export-order-mix-50pct-2-3yrs", "moved-goalpost", "Next call (Jan-26): 'difficult for me to put in a timeline'. Apr-26: 'about 25% and then eventually 50%'. Aug-26: 'I can't say by when'. Export share of order book was 10% (Mar-26), 17% (Sep-26).", admitted_unprompted=False)
st("polymer-600cr-fy26-1000cr-fy27-28", "partly", "FY26 polymer INR 507 cr = 85% of ~600 cr. The INR 1,000 cr leg (FY27/FY28) is pending and lost its date in Apr-26.", delivered_value="INR 507 cr", delivery_ratio=0.85,
   explanation_for_miss="falling resin prices cut value growth (Apr-26, prompted)", admitted_unprompted=False)
st("substation-projects-commission-fy27", "pending", "Apr-26: 'executing close to about 4 high-voltage substations'. No commissioning reported in the Aug-26 or Oct-26 calls.")
st("net-debt-range-bound", "unverifiable", "Mar-26 net debt + acceptances not disclosed in the calls read. Screener borrowings Mar-25 711 -> Mar-26 931 cr (+31% vs revenue +20%); company said D/E 'stable' at 0.62 and debt/EBITDA 1.6x. Sep-26 gross debt incl. acceptances INR 964 cr, down INR 358 cr YoY, but after the INR 433.5 cr equity raise.")
st("long-term-margin-12pct", "pending", "No date. H1FY27 ~10.6%.")
st("fy26-guidance-cut-to-20pct", "delivered", "FY26 +20.1% (inside ~20-22%, ratio 0.96 vs the 21% midpoint-low). Q4FY26 revenue 1,666 cr = +29.4% YoY, inside the 25-30% said.", delivered_value="+20.1%; Q4 +29.4%", delivery_ratio=0.96, confidence="verified")
st("fy27-order-inflow-grow-20pct", "pending", "H1FY27 inflow INR 3,786 cr, +18% YoY. FY27 guide now INR 7,500 cr (+32%).")

st("fy27-revenue-15pct-pat-30pct", "pending", "H1FY27 revenue INR 2,694 cr, +7%. Needs ~+21-22% in H2. Management now says 'at worst 13-14%'. H1 PAT INR 114 cr, +40% (helped by lower finance cost after the equity raise).")
st("back-to-20-25pct-from-fy28", "pending", "Not due until FY28.")
st("450kt-by-june-2026", "moved-goalpost", "Next call (Aug-26) opening remarks: 'expected to become operational during the second half of the year', with no acknowledgement of the June date. In Q&A, 'only a few months deferment ... by the end of quarter 2'.", admitted_unprompted=False)
st("fy27-capex-250cr-75kt-fy27-fy28", "moved-goalpost", "Oct-26: the next blocks are greenfield, with land not yet identified; phase 1 by end-FY28, phase 2 by end-FY29; '600,000 tons by FY29'. The +75k t in FY27 is now only the delayed FY26 block. Capex ~INR 250-300 cr a year is in line.", admitted_unprompted=False)
st("debtors-normalise-after-march-spike", "pending", "Interim check: trade receivables Sep-26 INR 1,223 cr (screener) vs 1,485 (Mar-26) and 701 (Mar-25). That is ~78 days on TTM revenue 5,731 cr, ~83 days on annualised H1, against 55 days in FY25. Even removing the INR 260 cr late receipt, Mar-26 is ~80 days. So the timing story explains only part of the rise. Not raised again by management in the Aug-26 or Oct-26 calls.",
   confidence="verified")
st("fy27-margin-up-toward-12pct", "pending", "H1FY27 margin up ~20-30 bp YoY (Q1 10.7%, Q2 10.5%).")
st("450kt-by-end-q2fy27", "moved-goalpost", "By end-Q2 (30-Sep-26) the block was not commissioned. Oct-26 call: 'end of quarter 3 ... or latest, at the beginning part of quarter 4', with no acknowledgement of the missed date.", admitted_unprompted=False)
st("fy27-finance-cost-3-2-3-5pct", "pending", "Q1FY27 ~3.4%, Q2FY27 3.2% (company). On track.")
st("fy27-order-inflow-7000cr-ob-10000cr", "pending", "Sep-26 order book INR 10,066 cr already above 10,000; H1 inflow 3,786 cr. Export inflow H1 ~INR 1,000-1,100 cr, already ~the August full-year figure. Raised to 7,500 / 1,500 in Oct-26.")
st("polymer-growth-20pct-fy27", "pending", "Q1FY27 polymer 'slightly muted' (destocking).")
st("fy27-revenue-15pct-at-worst-13-14", "pending", "Needs H2 revenue of ~INR 3,400-3,450 cr vs H2FY26 3,037 cr.")
st("fy27-inflow-7500cr-export-1500cr", "pending", "H1 3,786 cr total; Q2 export 1,055 cr.")
st("450kt-end-q3-or-early-q4-fy27", "pending", "Check in the Q3FY27 call (Jan/Feb-2027).")
st("600kt-by-fy29-greenfield", "pending", "Land 'in advanced stages of identification'; target to identify within Q3FY27.")
st("nwc-days-90-100-stable", "pending", "Baseline is ambiguous: company NWC days were 62 (Sep-24) and 88 (Dec-24); screener WC days FY26 43.")
st("fy27-margin-10-11pct-come-what-may", "pending", "H1FY27 ~10.6%.")

for p in P:
    if p["slug"] in S:
        p.update(S[p["slug"]])
missing = [p["slug"] for p in P if "status" not in p]
assert not missing, missing

SUMMARY_EXTRA = {
    "grade": "C- (below-average credibility; good on margins and finance cost, poor on dates and segment targets)",
    "calls_covered": "10 concalls, Q1FY25 (30-Jul-2024) to Q2FY27 (30-Oct-2026)",
    "tone_vs_delivery": "High-confidence language ('absolutely', 'for sure', 'well on track', 'no challenge') accompanies ~41% weighted delivery. The guidance that slipped was framed afterwards as 'aspiration'. Every call closes with near-identical upbeat boilerplate whatever the quarter.",
    "debtor_check": "Trade receivables INR 701 cr (Mar-25) -> 1,485 cr (Mar-26) -> 1,223 cr (Sep-26). Debtor days 55 -> 98 -> ~78-83. In Apr-25 management volunteered that WC would 'improve considerably'. The FY26 spike was explained only when an analyst asked: INR 260 cr received 1-2 April, Q4 domestic mix, GST. Ex-INR 260 cr, days are still ~80. By Oct-26 the target had been reset to NWC '90-100 days stable'.",
    "base_rates_note": "Single-company pilot. There is no peer base rate yet, so the score is meaningful only against future Skipper quarters and other companies scored the same way.",
    "next_checks": ["Q3FY27 call (Jan/Feb-2027): 450k t commissioning; H2 revenue run-rate vs 15%; order inflow toward 7,500 cr",
                    "Q4FY27 results: FY27 +15% revenue / +30% PAT; receivables vs 55-day FY25 base; polymer ~608 cr; finance cost 3.2-3.5%",
                    "Greenfield land announcement for 600k t by FY29"],
    "kill_criteria_link": "analysis:SKIPPER:2026-11-19 kill criteria include debtor days >120 and borrowings >INR 1,000 cr. Neither is triggered (Sep-26 ~78-83 days; borrowings 757 cr).",
}

ANALYSIS_BODY = ("Promise-tracker pilot on Skipper Ltd. 10 concalls (Jul-2024 to Oct-2026); {n_promises} forward-looking promises extracted, "
    "{n_scored} past-deadline or already re-dated promises scored. Status counts: {status_counts}. "
    "Weighted delivery ratio (specificity x materiality x recency) = {weighted_delivery_ratio_pct}%; specificity-only = "
    "{specificity_weighted_delivery_ratio_pct}%; raw hit rate {raw_hit_rate_pct}%; MCS on the -1.5..+1 schema scale = {mcs_schema_scale}. "
    "Strong on group-level P&L promises: FY25 +41% vs 25% guided; FY26 margin +50 bp; finance cost to ~4% (3.9%); FY26 +20% vs 20-25% guided in Apr-25. "
    "Weak on dates and segment targets: both 75k t blocks late (the second block has had five dates: Mar-26, Q1FY27, Jun-26, end-Q2FY27, end-Q3/early-Q4FY27); "
    "600k t moved FY28 -> FY29 without comment; polymer INR 1,000 cr and double-digit margin re-dated twice; export doubling missed (~INR 730 cr vs 1,500); "
    "'no further equity' reversed (INR 433.5 cr preferential, 2026). Precise promises deliver worst (by_specificity), and promises made in FY26 calls delivered far worse than those made in FY25 calls, as growth slowed. "
    "Candour index {candour_index_pct}% of shortfalls admitted unprompted. Misses are usually explained (monsoon, ROW, freight, CEA bidding), but only when an analyst asks, and missed targets are re-labelled 'aspiration'. "
    "Debtors: 55 -> 98 days in FY26 despite a volunteered Apr-25 promise that working capital would 'improve considerably'. The 'timing' explanation covers ~INR 260 cr; Sep-26 is still ~78-83 days. "
    "Use: haircut management dates by 1-2 quarters and segment targets by ~50%; trust the margin and finance-cost guidance more. Research, not advice.")
