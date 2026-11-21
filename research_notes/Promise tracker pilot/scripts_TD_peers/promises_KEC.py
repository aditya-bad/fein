# Promise ledger for KEC International (NSE: KEC). Same method/thresholds as scripts_SKIPPER.
# Built 2026-11-21. Transcripts from kecrpg.com (NSE filings for KEC are cover letters that point there).
# Status rules (fixed across companies; see SKIPPER.md section 1 + two clarifications written down in TD_peer_comparison.md):
#   delivered >=95% of target (low end of range) on time | partly 80-95% or <=1 qtr late | missed <80% or >1 qtr late
#   moved-goalpost = target/date changed later w/o acknowledging | withdrawn = explicitly lowered with explanation
#     (clarification A: a cut made in the final quarter before the deadline is scored on outcome, not as withdrawn)
#   silently-dropped = not repeated >=4 calls | pending | unverifiable
#   clarification B: ceiling targets (interest %, debt, NWC days): delivered if <= target, partly if overshoot <=5%, else missed;
#     margin-expansion targets are scored on the expansion promised (bp from the stated base), not on the margin level.
TICKER = "KEC"
SCREENER = "https://www.screener.in/company/KEC/consolidated/"
W = "https://www.kecrpg.com/public/media/earningsCallRecordingFilesMedia/"
CALLS = {
    "2025-02-04": ("Q3FY25 concall transcript", W + "KEC%20Q3%20FY25%20Earnings%20Call%20Transcript.pdf"),
    "2025-05-27": ("Q4FY25 concall transcript", W + "KEC%20Q4%20FY25%20Earnings%20Call%20Transcript.pdf"),
    "2025-07-29": ("Q1FY26 concall transcript", W + "KEC%20Q1%20FY26%20Earnings%20Call%20Transcript.pdf"),
    "2025-11-11": ("Q2FY26 concall transcript", W + "KEC%20Q2%20FY26%20Earnings%20Call%20Transcript.pdf"),
    "2026-01-30": ("Q3FY26 concall transcript", W + "KEC%20Earnings%20Call%2030th%20Jan%202026.pdf"),
    "2026-05-18": ("Q4FY26 concall transcript", W + "KEC%20Q4%20FY26%20Earnings%20Call%20Transcript.pdf"),
    "2026-08-11": ("Q1FY27 concall transcript", W + "KEC%20Q1%20FY27%20Earnings%20Call%20Transcript.pdf"),
    "2026-11-03": ("Q2FY27 concall transcript", W + "KEC%20Q2%20FY27%20Earnings%20Call%20Transcript.pdf"),
}
VK = "Vimal Kejriwal (MD & CEO)"
RA = "Rajeev Aggarwal (CFO)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---------------- Q3FY25 (04-Feb-2025) ----------------
add(said_on="2025-02-04", slug="fy25-order-inflow-exceed-25000cr", speaker=VK, category="order_inflow",
    title="FY25 order inflow to exceed INR 25,000 cr guidance",
    quote="we hold an L1 position of over Rs. 4,000 crores ... positioning us to exceed our order inflow guidance of Rs. 25,000 crores for the year",
    metric="Order inflow FY25", target=">INR 25,000 cr", deadline="2025-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="FY25 order intake INR 24,689 cr (Q4FY25 call) = 98.8% of 25,000; 'largely in line with our guidance'. Not 'exceeded', but inside the >=95% band.",
    delivered_value="INR 24,689 cr", delivery_ratio=0.99)
add(said_on="2025-02-04", slug="fy25-revenue-growth-12-14pct", speaker=VK, category="revenue_growth",
    title="FY25 revenue growth 12-14% (cut from 15%)",
    quote="we could end up anywhere between 12% to 14%",
    metric="Consolidated revenue growth YoY", target="+12-14% (needs Q4 +22-23%)", deadline="2025-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="partly", evidence="FY25 revenue INR 21,847 cr vs 19,914 cr = +9.7% (screener; company '10%'). Ratio 9.7/12 = 0.81. Q4 grew +11%, not the 22-23% needed.",
    delivered_value="+9.7%", delivery_ratio=0.81, explanation_for_miss="water-project slowdown (delayed state payments), labour shortage, T&D supply-chain bottlenecks (Q4FY25 opening remarks)",
    admitted_unprompted=True, confidence="verified")
add(said_on="2025-02-04", slug="fy26-revenue-growth-at-least-15pct", speaker=VK, category="revenue_growth",
    title="FY26 revenue growth of at least 15%",
    quote="we will definitely have a growth of at least 15% for the company next year",
    metric="Consolidated revenue growth YoY", target=">=+15%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=3,
    status="missed", evidence="FY26 revenue INR 23,506 cr vs 21,847 cr = +7.6% (screener; company '8%'). Ratio 0.51. Q4FY26 revenue -7% YoY.",
    delivered_value="+7.6%", delivery_ratio=0.51, explanation_for_miss="Middle East war (~INR 380-400 cr Q4 revenue deferred), labour/LPG shortages, calibrated water execution, delayed project closures (Q4FY26 opening remarks)",
    admitted_unprompted=True, confidence="verified")
add(said_on="2025-02-04", slug="fy26-ebitda-plus-150bp", speaker=VK, category="margin",
    title="FY26 EBITDA margin up at least 150 bp",
    quote="very clearly we are talking about EBITDA going up by at least 150 basis points sort of next year",
    metric="Consolidated EBITDA margin (company definition)", target="+150 bp over FY25 (7.0% -> ~8.5%)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=3,
    status="missed", evidence="Company EBITDA margin FY25 7.0%, FY26 ~7.1% (9M 7.1%, Q4 7.0%): +10 bp of +150 bp promised. Screener OPM 7.7% -> 7.95% (+25 bp) on its own definition.",
    delivered_value="+10 bp", delivery_ratio=0.07, explanation_for_miss="cut to 7-7.5% only when asked (Jan-26): water slowdown, closure costs, arbitration provisions, ROW/land delays",
    admitted_unprompted=False, confidence="verified")
add(said_on="2025-02-04", slug="fy26-td-share-above-60pct", speaker=VK, category="other",
    title="T&D share of revenue above 60% in FY26 (maybe 64-65%)",
    quote="Next year, I am very sure we will cross 60%, maybe we may reach 64%, 65%",
    metric="T&D share of revenue", target=">60% (64-65%)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="FY26 T&D share 68% vs 59% in FY25 (Q4FY26 call).", delivered_value="68%", delivery_ratio=1.1)
add(said_on="2025-02-04", slug="fy25-interest-below-3pct", speaker=VK, category="debt_reduction",
    title="FY25 interest cost below 3% of revenue (~2.9%)",
    quote="it should end up below 3, Rajeev, right? So, I think it's about 2.9 or something like that",
    metric="Interest / revenue (company definition)", target="<3% (~2.9%)", deadline="2025-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="partly", evidence="Company: 9M FY25 3.3% and Q4 2.5% -> FY25 ~3.05% (derived: 0.033x14,975 + 0.025x6,872 = 666 / 21,847). Overshoot ~2% vs 3.0. Screener finance cost 839/21,847 = 3.8% (includes other finance charges; different definition).",
    delivered_value="~3.05% (derived)", delivery_ratio=0.98, explanation_for_miss="not discussed", admitted_unprompted=False, confidence="single-source")
add(said_on="2025-02-04", slug="mar25-net-debt-4500-5000cr", speaker=RA, category="debt_reduction",
    title="Net debt incl. acceptances INR 4,500-5,000 cr by Mar-25",
    quote="we should expect the debt level between Rs. 4,500 crores to Rs. 5,000 crores for the quarter ending March",
    metric="Net debt incl. acceptances", target="INR 4,500-5,000 cr (from 5,574)", deadline="2025-03-31", deadline_precision="quarter",
    specificity="range", volunteered=False, materiality=2,
    status="delivered", evidence="Net debt incl. acceptances INR 4,558 cr at 31-Mar-25 (Q4FY25 opening). Screener borrowings 3,961 -> 3,957 (excludes acceptances).",
    delivered_value="INR 4,558 cr", delivery_ratio=1.0)
add(said_on="2025-02-04", slug="al-conductor-final-phase-mar25", speaker=VK, category="capacity_commissioning",
    title="Aluminium conductor plant final phase commissioned by Mar-25",
    quote="the final phase on track for commissioning by end March 2025",
    metric="Plant commissioning", target="final phase by 31-Mar-25", deadline="2025-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="Q4FY25 call: 'successfully commissioned an aluminium conductor plant at our Vadodara facility'; FY26 call: commissioned 'last March'.", delivery_ratio=1.0)
add(said_on="2025-02-04", slug="fy26-civil-growth-15pct", speaker=VK, category="revenue_growth",
    title="Civil revenue +15% in FY26",
    quote="Civil, in my view, will grow by almost let's say 15% or so next year",
    metric="Civil segment revenue growth", target="~+15%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="missed", evidence="Civil FY25 INR 4,483 cr -> FY26 3,823 cr = -15% (company segment figures, Q4FY25/Q4FY26 calls).", delivered_value="-15%", delivery_ratio=0.0,
    explanation_for_miss="labour, delayed work fronts, water payments (volunteered in Q4FY26 opening)", admitted_unprompted=True)
add(said_on="2025-02-04", slug="fy26-railways-flat-to-10pct", speaker=VK, category="revenue_growth",
    title="Railways revenue flat to +10% in FY26",
    quote="next year again our revenues in railways would be flat or at best maybe 5%, 10% growth, not more than that",
    metric="Transportation segment revenue growth", target="0% to +10%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="missed", evidence="Transportation FY25 INR 2,112 cr -> FY26 1,555 cr = -26% (company).", delivered_value="-26%", delivery_ratio=0.74,
    explanation_for_miss="deliberate run-down; divisional-railway contracting; legacy closures (prompted, May-26)", admitted_unprompted=False)
add(said_on="2025-02-04", slug="fy26-sae-growth-5-6pct", speaker=VK, category="revenue_growth",
    title="SAE Towers revenue +5-6% in FY26",
    quote="SAE will keep on growing by 5%, 6% year-on-year, provided the currency remains stable",
    metric="SAE revenue growth", target="+5-6%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="SAE FY25 INR 1,325 cr -> FY26 ~1,800 cr = +36% (company). Under-promised.", delivered_value="+36%", delivery_ratio=6.0)
add(said_on="2025-02-04", slug="fy26-cables-growth-11-12pct", speaker=VK, category="revenue_growth",
    title="Cables revenue +11-12% in FY26",
    quote="Cables outlook is okay, we expect growth to be 11%, 12%",
    metric="Cables & conductors revenue growth", target="+11-12%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="Cables & conductors FY26 INR 2,217 cr, +23% (company).", delivered_value="+23%", delivery_ratio=2.0)
add(said_on="2025-02-04", slug="legacy-rail-physical-completion-1-2qtrs", speaker=VK, category="other",
    title="Legacy railway orders physically complete within 1-2 quarters",
    quote="in the next maybe a quarter or two, maximum, we should be able to physically complete all the legacy orders",
    metric="Legacy railway project completion", target="all physically complete", deadline="2025-09-30", deadline_precision="half-year",
    specificity="range", volunteered=False, materiality=1,
    status="missed", evidence="Jan-26: 'closed at least 10% of our railway projects ... another 20% will close in this quarter'; Aug-26: slow projects 'at 95-97% closure'; Nov-26: 'by March, we'll just have two or three projects to be closed'. More than 1 quarter late.",
    delivery_ratio=0.0, explanation_for_miss="clients reversing agreed de-scoping, block availability, depot design approvals (prompted)", admitted_unprompted=False)
add(said_on="2025-02-04", slug="no-further-equity-raise", speaker=VK, category="other",
    title="No further equity raise (after the 2024 QIP)",
    quote="No, I do not think we are looking at raising any further equity",
    metric="Equity dilution at KEC", target="none", deadline="near term (unstated)", deadline_precision="vague",
    specificity="vague", volunteered=False, materiality=2,
    status="delivered", evidence="Equity capital INR 53 cr unchanged Mar-25 to Sep-26 (screener); no KEC issue in 7 quarters. Nov-26: a stake sale or raise in the cables subsidiary is being discussed as a debt lever, 'maybe by the end of next year'.",
    delivery_ratio=1.0, confidence="verified")

# ---------------- Q4FY25 (27-May-2025) ----------------
add(said_on="2025-05-27", slug="fy26-revenue-15pct-25000cr", speaker=VK, category="revenue_growth",
    title="FY26 revenue +15% (~INR 25,000 cr)",
    quote="what we have said is that we will grow by 15% on the revenue side",
    metric="Consolidated revenue growth YoY", target="+15% (CFO: 'to take it to INR25,000 crores')", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=3,
    status="missed", evidence="FY26 +7.6% (INR 23,506 cr) = 0.51 of the growth, 94% of the INR 25,000 cr level.", delivered_value="+7.6%", delivery_ratio=0.51,
    explanation_for_miss="Middle East war, labour/LPG, water, closures (Q4FY26 opening)", admitted_unprompted=True, confidence="verified")
add(said_on="2025-05-27", slug="fy26-ebitda-8-8-5pct", speaker=VK, category="margin",
    title="FY26 EBITDA margin 8-8.5% (from 7%)",
    quote="On the margin, we have been talking about 8% to 8.5% from the current 7%",
    metric="Consolidated EBITDA margin (company)", target="8-8.5% (+100-150 bp)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="missed", evidence="FY26 ~7.1% (company): +10 bp of the +100 bp minimum. Narrowed to 'closer to 8%' (Nov-25), cut to 7-7.5% (Jan-26), both only when asked.",
    delivered_value="~7.1%", delivery_ratio=0.1, explanation_for_miss="water, closure costs, provisions, client-side delays (Jan-26, prompted)", admitted_unprompted=False, confidence="verified")
add(said_on="2025-05-27", slug="fy26-order-intake-30000cr", speaker=VK, category="order_inflow",
    title="FY26 order intake ~INR 30,000 cr",
    quote="we have said that order intake should be around INR30,000 crores",
    metric="Order intake FY26", target="~INR 30,000 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="partly", evidence="FY26 order intake INR 25,280 cr (record) = 84% (Q4FY26 call).", delivered_value="INR 25,280 cr", delivery_ratio=0.84,
    explanation_for_miss="'subdued order inflows in India' (PGCIL 15-month gap, TBCB shift to private developers), Middle East award delays (Q4FY26 opening)", admitted_unprompted=True)
add(said_on="2025-05-27", slug="fy26-td-order-intake-20-21kcr", speaker=VK, category="order_inflow",
    title="FY26 T&D order intake INR 20,000-21,000 cr",
    quote="INR20,000-odd crores, INR21,000 crores is what we are looking of order growth -- order intake from T&D this year",
    metric="T&D order intake FY26", target="INR 20,000-21,000 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="partly", evidence="T&D FY26 order intake ~INR 17,700 cr = 88.5% of 20,000 (Q4FY26 call).", delivered_value="~INR 17,700 cr", delivery_ratio=0.885,
    explanation_for_miss="India T&D tendering slowed / shifted to private TBCB developers", admitted_unprompted=True)
add(said_on="2025-05-27", slug="fy26-india-td-oi-growth-20pct", speaker=VK, category="order_inflow",
    title="India T&D order intake +20% in FY26",
    quote="India T&D, again, I think we should have a 20% or so growth",
    metric="India T&D order intake growth", target="+20% (FY25 base ~INR 7,200 cr -> ~8,640)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="FY26 T&D intake ~17,700 less international T&D ~11,300 = India ~INR 6,400 cr (derived), about -11% YoY; 74% of the target level.",
    delivered_value="~INR 6,400 cr (derived)", delivery_ratio=0.74, explanation_for_miss="no PGCIL orders for 15 months; private developers' share of TBCB 45% -> 80%", admitted_unprompted=True, confidence="single-source")
add(said_on="2025-05-27", slug="fy27-ebitda-9pct-plus", speaker=VK, category="margin",
    title="FY27 EBITDA margin 9%+ ('no doubt about it')",
    quote="So next year has to be 9%, yes. No doubt about it.",
    metric="Consolidated EBITDA margin", target=">=9%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=3,
    status="moved-goalpost", evidence="Jan-26: 9-10% 'I can always say FY28'. May-26: no margin guidance; double-digit 'maybe FY29'. Aug-26: no double digit in FY27. Nov-26: FY28 'whether we'll achieve 7% or 8% or 9% is difficult to say'. H1FY27 EBITDA ~5.4% (screener 291+271 / 10,492). The FY27 9% was never referred to again.",
    admitted_unprompted=False)
add(said_on="2025-05-27", slug="mar26-nwc-100-days", speaker=RA, category="working_capital",
    title="NWC ~100 days by Mar-26 (from 122)",
    quote="we are quite hopeful that by end of this year, we should be closer to about 100 days of NWC",
    metric="Net working capital days (company)", target="~100 days", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="moved-goalpost", evidence="Two months later (Jul-25) the CEO gave '110 days is what we are still committing', with no reference to 100. Actual Mar-26 ~137 days (analyst figure, not disputed; Q4FY26).",
    delivered_value="~137 days", admitted_unprompted=False)
add(said_on="2025-05-27", slug="fy26-interest-2-5pct", speaker=RA, category="debt_reduction",
    title="FY26 interest cost ~2.5% of revenue",
    quote="we expect the overall interest cost should be about 2.5% of the total revenue despite a revenue growth of almost 15%",
    metric="Interest / revenue (company)", target="~2.5%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="missed", evidence="FY26 2.8% (company, Q4FY26 opening, framed as '-20 bp'); overshoot 12%. Reaffirmed Jul-25 and Nov-25. Screener 872/23,506 = 3.7% (different definition).",
    delivered_value="2.8%", delivery_ratio=0.89, explanation_for_miss="none; never acknowledged", admitted_unprompted=False, confidence="verified")
add(said_on="2025-05-27", slug="fy26-civil-growth-25pct", speaker=VK, category="revenue_growth",
    title="Civil revenue +25% at least in FY26",
    quote="This year, we expect Civil to grow by at least 25%",
    metric="Civil revenue growth", target=">=+25% (FY25 4,483 -> ~5,600 cr)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="moved-goalpost", evidence="Nov-25: 'growth of overall 10% to 12%, 15% maybe ... around INR5,000 crores', no reference to 25%. Actual FY26 INR 3,823 cr, -15%.",
    delivered_value="-15%", delivery_ratio=0.0, admitted_unprompted=False)
add(said_on="2025-05-27", slug="fy26-water-revenue-1200-1500cr", speaker=VK, category="revenue_growth",
    title="Water (JJM) revenue INR 1,200-1,500 cr in FY26",
    quote="INR1,200 crores to INR1,500 crores of revenue targets for this year from water ... unless there's a major setback in terms of payments",
    metric="Water revenue FY26", target="INR 1,200-1,500 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1, conditionality="no major payment setback",
    status="missed", evidence="Jan-26: 'by the end of the year, we'll probably do around INR800 crores of revenue'; FY26 water collections ~INR 800 cr (May-26). ~67% of the floor.",
    delivered_value="~INR 800 cr", delivery_ratio=0.67, explanation_for_miss="state payment delays; cash-and-carry execution (volunteered each quarter)", admitted_unprompted=True, confidence="single-source")
add(said_on="2025-05-27", slug="railways-revenue-floor-2100cr", speaker=VK, category="revenue_growth",
    title="Railways revenue will not fall below ~INR 2,100 cr",
    quote="We did a turnover of around INR2,100 crores. I don't think we want to do below that",
    metric="Transportation revenue", target=">= INR 2,100 cr (FY26)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="FY26 transportation revenue INR 1,555 cr (74%).", delivered_value="INR 1,555 cr", delivery_ratio=0.74,
    explanation_for_miss="'Railways was unexpected' (divisional railways as clients), May-26, prompted", admitted_unprompted=False)
add(said_on="2025-05-27", slug="fy26-cables-revenue-2300-2400cr", speaker=VK, category="revenue_growth",
    title="Cables FY26 revenue INR 2,300-2,400 cr",
    quote="hopefully, next year, we should be around INR2,300 crores, INR2,400 crores of revenue in FY '26",
    metric="Cables & conductors revenue", target="INR 2,300-2,400 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence="FY26 INR 2,217 cr = 96% of 2,300 (company).", delivered_value="INR 2,217 cr", delivery_ratio=0.96)
add(said_on="2025-05-27", slug="fy27-cables-revenue-3400-3500cr", speaker=VK, category="revenue_growth",
    title="Cables FY27 revenue INR 3,400-3,500 cr",
    quote="So around INR3,400 crores, INR3,500 crores should be the Cables' revenue in FY '27",
    metric="Cables & conductors revenue", target="INR 3,400-3,500 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="moved-goalpost", evidence="May-26: 'cables is INR2,300, it will grow at least 15%'. Nov-26: 'this year will be close INR2,500 crores, INR2,600 crores ... by end of next year ... INR3,500 crores or maybe FY28 ... INR4,000'. No reference to the FY27 target.", admitted_unprompted=False)
add(said_on="2025-05-27", slug="cables-margin-8pct-in-2yrs", speaker=VK, category="margin",
    title="Cables margin ~8% in two years (FY27)",
    quote="we are hopeful that we will be reaching 8% in 2 years' time",
    metric="Cables EBITDA margin", target="~8% (from 5.7-5.8%)", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="pending", evidence="Aug-26 ~5% ('200 bp below the market'); Nov-26 5.5-6%. Likely miss.")
add(said_on="2025-05-27", slug="ebeam-elastomeric-q4fy26", speaker=VK, category="capacity_commissioning",
    title="E-Beam and elastomeric cable production to start Q4FY26",
    quote="the capital investment to produce E-Beam and Elastomeric cables is progressing well, and we expect commercial production to commence in Q4 this year",
    metric="Plant commissioning", target="commercial production in Q4FY26", deadline="2026-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="moved-goalpost", evidence="Dates since: Nov-25 elastomeric Q4FY26 / E-Beam Q1FY27; May-26 both Q2FY27; Aug-26 elastomeric Q2 / E-Beam Q3; Nov-26 'part of the facility has got commissioned', both now Q3FY27. No re-date was acknowledged as a slip.", admitted_unprompted=False)
add(said_on="2025-05-27", slug="fy26-capex-400cr", speaker=VK, category="capex",
    title="FY26 capex ~INR 400 cr",
    quote="you can take INR400 crores for this year and maybe a similar amount for next year",
    metric="Capex", target="~INR 400 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="delivered", evidence="Derived from screener: net block 1,647 -> 1,773 (+126) + depreciation 197 + CWIP 39 -> 114 (+75) = ~INR 398 cr.", delivered_value="~INR 398 cr (derived)", delivery_ratio=0.99, confidence="single-source")
add(said_on="2025-05-27", slug="fy26-td-margin-above-10pct", speaker=VK, category="margin",
    title="T&D segment margin in FY26 better than FY25's ~10%",
    quote="whether it will be 11% or 12%, difficult to say, but it will definitely be better than what we have delivered this year",
    metric="T&D EBITDA margin", target=">10%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=2,
    status="unverifiable", evidence="Every FY26 call says T&D is at 'double-digit'; no segment margin is disclosed, so 'better than 10%' cannot be checked.")

# ---------------- Q1FY26 (29-Jul-2025) ----------------
add(said_on="2025-07-29", slug="fy26-ebitda-8-8-5-reaffirmed", speaker=VK, category="margin",
    title="FY26 EBITDA 8-8.5% reaffirmed; 'no major issue' meeting the lower end",
    quote="So for FY '26, we have actually guided at 8% to 8.5% already, okay? So I think I don't see any major issue at least in meeting the lower end of it",
    metric="Consolidated EBITDA margin", target="8-8.5%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="missed", evidence="FY26 ~7.1%.", delivered_value="~7.1%", delivery_ratio=0.1, explanation_for_miss="see fy26-ebitda-8-8-5pct", admitted_unprompted=False, confidence="verified")
add(said_on="2025-07-29", slug="fy27-ebitda-near-10pct", speaker=VK, category="margin",
    title="FY27 EBITDA +50-100 bp more, 'closer to 10%'",
    quote="FY '27, obviously, we should have at least a 50 to 100 basis points improvement in that. So FY '27, we will be probably reaching closer to 10%",
    metric="Consolidated EBITDA margin", target="~9-10%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="moved-goalpost", evidence="See fy27-ebitda-9pct-plus: re-dated to FY28 (Jan-26), then FY29 for double digit (May-26), without reference to this statement.", admitted_unprompted=False)
add(said_on="2025-07-29", slug="mar26-nwc-110-days", speaker=VK, category="working_capital",
    title="NWC 128 -> 110 days by Mar-26",
    quote="the net working capital, which is today 128 days will probably come down to 110 days is what we are still committing",
    metric="Net working capital days (company)", target="110 days", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="missed", evidence="Mar-26 ~137 days (analyst figure in Q4FY26 call, not disputed); the CEO's answer then was 'I thought we said 110 days' - now for Mar-27. Jan-26 had already moved to '110 to 115'.",
    delivered_value="~137 days", delivery_ratio=0.8, explanation_for_miss="water dues, metro back-ended payments, Saudi 20% retention, strategic inventory (prompted)", admitted_unprompted=False)
add(said_on="2025-07-29", slug="mar26-net-debt-4500cr", speaker=RA, category="debt_reduction",
    title="Net debt ~INR 4,500 cr by Mar-26 despite 15% growth",
    quote="we do expect that we will be able to maintain our numbers at about INR4,500 crores debt by the end of the year",
    metric="Net debt incl. acceptances", target="~INR 4,500 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="missed", evidence="Mar-26 net debt incl. acceptances INR 6,722 cr (+49% vs target). Screener borrowings 3,957 -> 5,378. FY26 CFO -414 cr, FCF -691 cr (screener).",
    delivered_value="INR 6,722 cr", delivery_ratio=0.67, explanation_for_miss="INR 450 cr collections spilled to April, Dubai inventory, cable/steel stocking (Q4FY26 opening)", admitted_unprompted=True, confidence="verified")
add(said_on="2025-07-29", slug="afghanistan-payment-q3fy26", speaker=RA, category="working_capital",
    title="Afghanistan receivable to be realised in Q3FY26",
    quote="Some bit of a payment is also, let's say, due from Afghanistan. So we expect that payment to get realized in quarter 3",
    metric="Afghanistan (ADB) receivable ~INR 250-300 cr", target="realised in Q3FY26", deadline="2025-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="Re-dated to Q4FY26 (Nov-25, acknowledged when asked), 'supposed to come in Q1' (Aug-26), received '>INR200 crores ... in October' 2026 (Nov-26). Three quarters late.",
    delivery_ratio=0.0, explanation_for_miss="ADB taking a portfolio-wide position (prompted)", admitted_unprompted=False)
add(said_on="2025-07-29", slug="non-td-growth-uptick-q3-q4fy26", speaker=VK, category="revenue_growth",
    title="Non-T&D revenue to turn from Q2 and rise significantly in Q3/Q4 FY26",
    quote="from Q3, Q4 onwards, you will definitely see a significant uptick happening in the non-T&D, whether it is civil, whether it is cables",
    metric="Non-T&D revenue", target="growth from Q2FY26, significant by Q3-Q4", deadline="2026-03-31", deadline_precision="half-year",
    specificity="vague", volunteered=False, materiality=2,
    status="missed", evidence="Non-T&D revenue FY25 ~41% of 21,847 = ~8,960 cr -> FY26 32% of 23,506 = ~7,520 cr, ~-16% (derived from T&D shares). Only cables grew.",
    delivery_ratio=0.0, explanation_for_miss="labour, work fronts, water, railway run-down (Q4FY26 opening)", admitted_unprompted=True, confidence="single-source")
add(said_on="2025-07-29", slug="pgcil-matter-no-impact-on-td-growth", speaker=VK, category="order_inflow",
    title="PGCIL matter (bribery inquiry raised by analyst) will not hurt T&D growth",
    quote="So even in the unlikely, say, that PGCIL takes something against us or something, I don't think it's going to impact our T&D growth in any manner",
    metric="T&D growth / India T&D order intake", target="no impact", deadline="2026-03-31", deadline_precision="vague",
    specificity="vague", volunteered=False, materiality=2,
    status="partly", evidence="T&D revenue grew +24% in FY26 (no revenue impact). But KEC received no PGCIL orders for ~15 months ('orders & L1 of over INR3,000 crores from PGCIL after a break of 15 months', Nov-26) and India T&D intake fell to ~INR 6,400 cr (derived) from ~7,200. The analyst's question (Jul-25) referred to 'this bribery case with Power Grid officials, which is under inquiry'; management gave no outcome. Governance item - single-source (transcript only).",
    delivery_ratio=0.5, explanation_for_miss="TBCB shift to private developers (volunteered); the PGCIL gap itself was never explained", admitted_unprompted=False)
add(said_on="2025-07-29", slug="renewables-3000-4000cr-2-3yrs", speaker=VK, category="revenue_growth",
    title="Renewables revenue INR 3,000-4,000 cr in 2-3 years",
    quote="in the next 2 to 3 years, we are expecting this business to be -- from INR3,000 crores to INR4,000 crores",
    metric="Renewables revenue", target="INR 3,000-4,000 cr", deadline="2028-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="pending", evidence="FY26 INR 516 cr. Nov-25 restated as 'not next year, but a year after' (FY28).")
add(said_on="2025-07-29", slug="karnataka-500mw-completion-q2fy26", speaker=VK, category="capacity_commissioning",
    title="Karnataka 500 MW solar EPC complete next quarter (Q2FY26)",
    quote="The 500-megawatt solar project in Karnataka has been partly commissioned and is scheduled for completion next quarter",
    metric="Project completion", target="by Q2FY26", deadline="2025-09-30", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="missed", evidence="Nov-25: 'scheduled for completion this quarter' (Q3); Jan-26: 'within this quarter' (Q4); May-26: 1,000 MW across Karnataka and Rajasthan commissioned. Two quarters late; slips not acknowledged.",
    delivery_ratio=1.0, admitted_unprompted=False)

# ---------------- Q2FY26 (11-Nov-2025) ----------------
add(said_on="2025-11-11", slug="fy26-revenue-15pct-reaffirmed", speaker=VK, category="revenue_growth",
    title="FY26 revenue +15% reaffirmed (H2 = 60% of year)",
    quote="15% guidance is also going on, so I think it should be done",
    metric="Consolidated revenue growth", target="+15%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=3,
    status="missed", evidence="FY26 +7.6%. H2FY26 revenue 6,001 + 6,390 = 12,391 cr vs H2FY25 5,349 + 6,872 = 12,221 cr: +1.4% YoY (screener).", delivered_value="+7.6%", delivery_ratio=0.51,
    explanation_for_miss="see fy26-revenue-15pct-25000cr", admitted_unprompted=True, confidence="verified")
add(said_on="2025-11-11", slug="fy26-ebitda-closer-to-8pct", speaker=VK, category="margin",
    title="FY26 EBITDA 'closer to 8%' (lower band of 8-8.5%)",
    quote="we have been talking about 8% to 8.5%. We are not talking about more on the lower band at 8%",
    metric="Consolidated EBITDA margin", target="~8% (H2 >8.5%)", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=3,
    status="missed", evidence="FY26 ~7.1%; H2 ~7.1% vs >8.5% needed. Cut to 7-7.5% in Jan-26 (final quarter, so scored on outcome per clarification A).", delivered_value="~7.1%", delivery_ratio=0.1,
    explanation_for_miss="civil delays and unpaid client claims (this call, prompted)", admitted_unprompted=False, confidence="verified")
add(said_on="2025-11-11", slug="sep25-is-peak-debt", speaker=VK, category="debt_reduction",
    title="Sep-25 net debt (INR 6,480 cr) is the peak; it will come down",
    quote="We expect that to be our peak debt. I think it started to come down.",
    metric="Net debt incl. acceptances", target="< INR 6,480 cr from here", deadline="2026-03-31", deadline_precision="vague",
    specificity="vague", volunteered=False, materiality=2,
    status="missed", evidence="Dec-25 INR 6,806 cr; Mar-26 6,722; Jun-26 6,568; Sep-26 7,793 cr ('a very high number').", delivery_ratio=0.0,
    explanation_for_miss="Saudi receipts slipped to January, water, inventory (prompted Jan-26)", admitted_unprompted=False)
add(said_on="2025-11-11", slug="afghanistan-adb-q4fy26", speaker=RA, category="working_capital",
    title="Afghanistan ADB dues (~USD 30 mn) mostly received in Q4FY26",
    quote="We expect this payment to come in Q4. But there is no doubt in terms of the payment recovery",
    metric="Afghanistan (ADB) receivable", target="majority by Q4FY26", deadline="2026-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="Received >INR 200 cr in October 2026: two quarters late. The previous Q2/Q3 expectation was acknowledged when re-dated.", delivery_ratio=0.0,
    explanation_for_miss="ADB processing (prompted)", admitted_unprompted=False)
add(said_on="2025-11-11", slug="fy26-civil-revenue-5000cr", speaker=VK, category="revenue_growth",
    title="Civil FY26 revenue ~INR 5,000 cr (+10-15%)",
    quote="we should be around INR5,000 crores hopefully for the year ... So second half, we will be able to easily reach close to INR5,000 crores",
    metric="Civil revenue", target="~INR 5,000 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="missed", evidence="FY26 Civil INR 3,823 cr = 76% (company). Jan-26 (prompted): '~INR1,000 crores impact on the revenues'.", delivered_value="INR 3,823 cr", delivery_ratio=0.76,
    explanation_for_miss="labour, NCR seismic-code redesigns, land not acquired by developers, water payments (Jan-26 Q&A, May-26 opening)", admitted_unprompted=True)
add(said_on="2025-11-11", slug="fy26-railways-2000cr", speaker=VK, category="revenue_growth",
    title="Railways FY26 revenue ~INR 2,000 cr",
    quote="we expect to do around INR2,000 crores and odd in railways for the year -- this year",
    metric="Transportation revenue", target="~INR 2,000 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="missed", evidence="FY26 INR 1,555 cr = 78%.", delivered_value="INR 1,555 cr", delivery_ratio=0.78,
    explanation_for_miss="conscious de-growth; legacy closures (prompted)", admitted_unprompted=False)
add(said_on="2025-11-11", slug="karnataka-500mw-completion-q3fy26", speaker=VK, category="capacity_commissioning",
    title="Karnataka 500 MW solar complete in Q3FY26",
    quote="The 500 megawatts solar project to Karnataka is scheduled for completion this quarter",
    metric="Project completion", target="by Q3FY26", deadline="2025-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="partly", evidence="Completed in Q4FY26 (commissioned per May-26 call): one quarter late.", delivery_ratio=1.0, admitted_unprompted=False)
add(said_on="2025-11-11", slug="first-wind-epc-order-fy26", speaker=VK, category="customer_win",
    title="First wind EPC order in FY26",
    quote="we had said earlier that this year, we should announce our first wind EPC also",
    metric="Order win", target="first wind EPC order", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="delivered", evidence="Jan-26: 'breakthrough order for a 100-plus megawatt wind project in Southern India'; two wind orders by FY26-end.", delivery_ratio=1.0)
add(said_on="2025-11-11", slug="fy26-conductor-revenue-500-600cr", speaker=VK, category="revenue_growth",
    title="Aluminium conductor revenue ~INR 500-600 cr in FY26",
    quote="Out of that, we were expecting INR500 crores-INR600 crores. So let's see where we touch",
    metric="Conductor revenue", target="INR 500-600 cr", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1,
    status="unverifiable", evidence="Conductor revenue not split out from cables & conductors (INR 2,217 cr) in later calls.")
add(said_on="2025-11-11", slug="fy27-civil-growth-15-20pct", speaker=VK, category="revenue_growth",
    title="Civil FY27 growth 15-20% at higher single-digit margins",
    quote="next year, we are clearly looking at least 15%, 20% growth, almost, let's say, INR6,500 crores or so revenue",
    metric="Civil revenue growth", target="+15-20%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=2,
    status="pending", evidence="Raised to +30-35% in May-26; Nov-26 civil now 'cautious and selective'. H1FY27 civil 1,950 cr vs 1,908 = +2%.")

# ---------------- Q3FY26 (30-Jan-2026) ----------------
add(said_on="2026-01-30", slug="fy26-ebitda-7-7-5pct", speaker=VK, category="margin",
    title="FY26 EBITDA cut to 7-7.5%",
    quote="probably will be anywhere between 7% to 7.5%. Okay? We are hoping that it goes to 7.5%",
    metric="Consolidated EBITDA margin", target="7-7.5%", deadline="2026-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="delivered", evidence="FY26 ~7.1% (9M 7.1%, Q4 7.0%).", delivered_value="~7.1%", delivery_ratio=1.0, confidence="verified")
add(said_on="2026-01-30", slug="mar26-debt-normalise", speaker=VK, category="debt_reduction",
    title="Debt (INR 6,806 cr at Dec-25) to normalise by Mar-26",
    quote="The debt levels have already come down by almost INR300 crores in January '26 and are expected to normalize by March '26 end",
    metric="Net debt incl. acceptances", target="normalise by Mar-26", deadline="2026-03-31", deadline_precision="quarter",
    specificity="vague", volunteered=True, materiality=2,
    status="missed", evidence="Mar-26 INR 6,722 cr, 'marginally lower than December'.", delivery_ratio=0.0,
    explanation_for_miss="INR 450 cr spillover to April; inventory (volunteered May-26)", admitted_unprompted=True)
add(said_on="2026-01-30", slug="fy27-ebitda-above-fy26", speaker=VK, category="margin",
    title="FY27 EBITDA margin better than FY26's 7-7.5%",
    quote="next year, it will be better than what we are talking. This year, we said 7% to 7.5%, next year, I'm clearly saying it will be better than that",
    metric="Consolidated EBITDA margin", target=">7-7.5%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=3,
    status="pending", evidence="H1FY27 ~5.4% (screener OPM Q1 5.8%, Q2 5.0%; company PBT 1.8% / 0.7%). Margin guidance withheld since May-26. Very likely miss.")
add(said_on="2026-01-30", slug="fy28-ebitda-9-10pct", speaker=VK, category="margin",
    title="EBITDA 9-10% by FY28",
    quote="If you're looking at 9% to 10%, then I can always say FY '28",
    metric="Consolidated EBITDA margin", target="9-10%", deadline="2028-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="moved-goalpost", evidence="May-26: double digit 'maybe FY29'. Nov-26: 'FY28 ... whether we'll achieve 7% or 8% or 9% is difficult to say'. The FY28 9-10% was not referred to.", admitted_unprompted=False)
add(said_on="2026-01-30", slug="fy27-order-intake-30-35kcr", speaker=VK, category="order_inflow",
    title="FY27 order intake ~INR 30,000-35,000 cr",
    quote="we would look at maybe some around INR30,000 crores, INR35,000 crores should be our order intake target for next year",
    metric="Order intake FY27", target="INR 30,000-35,000 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=2,
    status="pending", evidence="May-26 target 'around INR30,000 crores'; H1FY27 ~INR 13,500 cr + L1 3,500.")
add(said_on="2026-01-30", slug="solar-1000mw-complete-q4fy26", speaker=VK, category="capacity_commissioning",
    title="Karnataka and Rajasthan 500 MW solar projects complete in Q4FY26",
    quote="The execution of the existing 500-megawatt solar projects in Karnataka and Rajasthan are progressing well towards completion within this quarter",
    metric="Project completion", target="both by Q4FY26", deadline="2026-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="May-26: 'successfully commissioned a record 1,000 megawatts of solar capacity across Rajasthan and Karnataka'.", delivery_ratio=1.0)
add(said_on="2026-01-30", slug="butibori-expansion-by-mar26", speaker=VK, category="capacity_commissioning",
    title="Butibori (Nagpur) tower plant expansion complete by Mar-26",
    quote="the expansion of our Butibori facility in Nagpur is expected to be completed by March '26",
    metric="Capacity expansion", target="by 31-Mar-26", deadline="2026-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="partly", evidence="May-26 re-dated to 'within this quarter' (no acknowledgement); Aug-26: 'completed ... in Q1', capacity 483,800 t. One quarter late. (Nov-25 had said 'by this year-end'.)", delivery_ratio=1.0, admitted_unprompted=False)
add(said_on="2026-01-30", slug="elastomeric-by-end-fy26", speaker=VK, category="capacity_commissioning",
    title="Elastomeric cable production by end-FY26 (repeat)",
    quote="we expect production for Elastomeric cables to commence by the end of this financial year",
    metric="Plant commissioning", target="by 31-Mar-26", deadline="2026-03-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="moved-goalpost", evidence="May-26: 'slated to commence production in Q2'; Nov-26: Q3FY27. Not acknowledged as late.", admitted_unprompted=False)
add(said_on="2026-01-30", slug="water-projects-close-12-15-months", speaker=VK, category="other",
    title="Exit water (JJM) projects within 12-15 months",
    quote="Optimistically, I think if the same thing continues, then within 12 to 15 months we should be able to close all our projects",
    metric="JJM project closure", target="all closed", deadline="2027-04-30", deadline_precision="quarter",
    specificity="range", volunteered=False, materiality=1, conditionality="payments continue at the same pace",
    status="pending", evidence="Nov-26: JJM order book still INR 1,000-1,100 cr; INR 100 cr more invested to close projects.")

# ---------------- Q4FY26 (18-May-2026) ----------------
add(said_on="2026-05-18", slug="fy27-revenue-12-15pct", speaker=VK, category="revenue_growth",
    title="FY27 revenue growth 12-15%",
    quote="I think we should be able to achieve for the year around 12% to 15%",
    metric="Consolidated revenue growth", target="+12-15%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="withdrawn", evidence="Nov-26 (prompted): '8% to 10% ... because we have lost around INR600 crores of revenue' to the Middle East disruption. H1FY27 revenue INR 10,492 cr vs 11,115 = -5.6% (screener).",
    explanation_for_miss="Middle East supply chain, freight, ROW/land in India T&D (Nov-26)", admitted_unprompted=False)
add(said_on="2026-05-18", slug="fy27-order-intake-30000cr", speaker=VK, category="order_inflow",
    title="FY27 order intake ~INR 30,000 cr (T&D 17-18k, Civil ~8k)",
    quote="we expect that we should be touching around INR30,000 crores of order intake for the year",
    metric="Order intake FY27", target="~INR 30,000 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="pending", evidence="H1FY27 ~INR 13,500 cr. Civil intake deliberately cut ('only 3 orders in civil this year').")
add(said_on="2026-05-18", slug="sep26-net-debt-down-500cr", speaker=VK, category="debt_reduction",
    title="Net debt down INR 500 cr by Sep-26 (INR 1,000 cr in FY27)",
    quote="we are targeting an overall reduction of almost INR1,000 crores in the debt ... INR500 crores should happen by end of Q2 and another INR500 crores by the end of the year",
    metric="Net debt incl. acceptances", target="<= ~INR 6,222 cr at Sep-26", deadline="2026-09-30", deadline_precision="quarter",
    specificity="precise", volunteered=False, materiality=2,
    status="missed", evidence="Sep-26 INR 7,793 cr: up INR 1,071 cr instead of down 500. Screener borrowings 5,378 -> 6,305.", delivered_value="INR 7,793 cr", delivery_ratio=0.0,
    explanation_for_miss="INR 600 cr collections (incl. Afghanistan, client advances) landed in October; INR 160 cr strategic inventory; water/metro collections short (Nov-26 opening)", admitted_unprompted=True, confidence="verified")
add(said_on="2026-05-18", slug="mar27-nwc-110-days", speaker=VK, category="working_capital",
    title="NWC 110 days by Mar-27",
    quote="I thought we said 110 days.",
    metric="Net working capital days", target="110 days", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="withdrawn", evidence="Nov-26 CFO (prompted): 'Yes, 110. Now currently, it is at about 125 days. That is where we are targeting', explained by Saudi closure slippage (20% retention).",
    explanation_for_miss="Saudi project-closure slippage", admitted_unprompted=False)
add(said_on="2026-05-18", slug="fy27-civil-growth-30-35pct", speaker=VK, category="revenue_growth",
    title="Civil FY27 growth 30-35%",
    quote="Civil, as I said earlier, will definitely grow by 30%, 35%",
    metric="Civil revenue growth", target="+30-35%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=2,
    status="pending", evidence="H1FY27 ~+2% (993 + 957 vs 940 + 968). Nov-26: 'cautious and selective approach to Civil'.")
add(said_on="2026-05-18", slug="fy27-cables-growth-15pct", speaker=VK, category="revenue_growth",
    title="Cables FY27 growth at least 15%",
    quote="cables is INR2,300, it will grow at least 15%, if not more",
    metric="Cables & conductors revenue growth", target=">=+15%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=1,
    status="pending", evidence="Q1 >INR 600 cr (+57%), Q2 613 cr (+17%); FY27 guided 2,500-2,600 cr (Nov-26). On track.")
add(said_on="2026-05-18", slug="receivables-normalise-2qtrs", speaker=VK, category="working_capital",
    title="Receivables to normalise within two quarters (Saudi retentions)",
    quote="in the next two quarters, we will receive a lot of release of retentions also. So we expect the receivables to be normalized going forward",
    metric="Receivables / NWC", target="normalised by Sep-26", deadline="2026-09-30", deadline_precision="half-year",
    specificity="vague", volunteered=False, materiality=2,
    status="missed", evidence="Sep-26 NWC ~125 days ('targeting'), net debt at a record INR 7,793 cr; CFO cites 'slippages in terms of the closure of the project in Saudi Arabia'.", delivery_ratio=0.0,
    explanation_for_miss="Saudi closure slippage (prompted)", admitted_unprompted=False)

# ---------------- Q1FY27 (11-Aug-2026) ----------------
add(said_on="2026-08-11", slug="fy27-revenue-12-15pct-reaffirmed", speaker=VK, category="revenue_growth",
    title="FY27 revenue 12-15% reaffirmed ('maybe 0.5% or 1% here and there')",
    quote="we are okay with the guidance ... maybe 0.5% or 1% here and there, but I don't think there's anything major for us to worry",
    metric="Consolidated revenue growth", target="+12-15%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3,
    status="withdrawn", evidence="Cut to 8-10% one quarter later (Nov-26), with an explanation, when asked.", explanation_for_miss="Middle East (prompted)", admitted_unprompted=False)
add(said_on="2026-08-11", slug="mar27-net-debt-5500cr", speaker=RA, category="debt_reduction",
    title="Net debt ~INR 5,500 cr by Mar-27 (-INR 1,200 cr)",
    quote="what we are guiding is by March, we should reach to about INR5,500 crores",
    metric="Net debt incl. acceptances", target="~INR 5,500 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="moved-goalpost", evidence="Nov-26 opening: 'We expect the debt levels to come down to almost INR6,000 crores by the end of the year', with no reference to 5,500.", admitted_unprompted=False)
add(said_on="2026-08-11", slug="fy27-interest-2-3pct", speaker=VK, category="debt_reduction",
    title="FY27 interest ~2.3% of revenue (~INR 600 cr)",
    quote="our expectation is that against the 3.3%, which we did, we should be around 2.3% or so for the whole year",
    metric="Interest / revenue", target="~2.3%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=False, materiality=2,
    status="pending", evidence="Q1 3.3% (company); Q2 screener interest 191 cr / 5,468 = 3.5%. Very likely miss.")
add(said_on="2026-08-11", slug="afghanistan-q2-or-q3fy27", speaker=VK, category="working_capital",
    title="Afghanistan ~INR 300 cr: Q2FY27, 'otherwise definitely Q3'",
    quote="if we are lucky, let me put it, that we should get it in Q2 itself. Otherwise, definitely Q3",
    metric="Afghanistan (ADB) receivable", target="Q2 or Q3 FY27", deadline="2026-12-31", deadline_precision="quarter",
    specificity="range", volunteered=False, materiality=1,
    status="delivered", evidence=">INR 200 cr received in October 2026 (Q3); another ~INR 100-150 cr expected 'within this quarter, otherwise, at least January'.", delivery_ratio=0.7)
add(said_on="2026-08-11", slug="railway-claims-150-200cr-fy27", speaker=RA, category="working_capital",
    title="Railway claims of INR 150-200 cr realised by Mar-27",
    quote="between now and March, we should be able to realize between INR150 crores to INR200 crores from the claims",
    metric="Claims realised", target="INR 150-200 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=1, status="pending", evidence="Nov-26: railway business cash-positive for seven months; claims amount not updated.")

# ---------------- Q2FY27 (03-Nov-2026) ----------------
add(said_on="2026-11-03", slug="fy27-revenue-8-10pct", speaker=VK, category="revenue_growth",
    title="FY27 revenue growth 8-10% (cut from 12-15%)",
    quote="probably anywhere between 8% to 10% is what we will risk",
    metric="Consolidated revenue growth", target="+8-10%", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=3, status="pending",
    evidence="H1 -5.6%; needs H2 ~+20-24% YoY (H2FY26 12,391 cr). Relies on a 'very strong uptick in Q4'.")
add(said_on="2026-11-03", slug="mar27-net-debt-6000cr", speaker=VK, category="debt_reduction",
    title="Net debt ~INR 6,000 cr by Mar-27",
    quote="We expect the debt levels to come down to almost INR6,000 crores by the end of the year",
    metric="Net debt incl. acceptances", target="~INR 6,000 cr", deadline="2027-03-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2, status="pending", evidence="Sep-26 INR 7,793 cr; INR 600 cr received in October.")
add(said_on="2026-11-03", slug="ebeam-elastomeric-q3fy27", speaker=VK, category="capacity_commissioning",
    title="Elastomeric and E-Beam production in Q3FY27",
    quote="while part of the facility has got commissioned, we expect Elastomeric cables and E-Beam to commence production in Q3",
    metric="Plant commissioning", target="Q3FY27", deadline="2026-12-31", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1, status="pending", evidence="Fifth date for E-Beam, fourth for elastomeric.")
add(said_on="2026-11-03", slug="legacy-closures-by-q2fy28", speaker=VK, category="other",
    title="Loss-making legacy projects closed by Q2FY28; this quarter's margin is the floor",
    quote="My expectation is that this is the lowest number which we have got to ... will definitely get closed by -- I think by Q2 of next year",
    metric="Legacy project closure / margin floor", target="margin not below Q2FY27; legacy closed by Sep-27", deadline="2027-09-30", deadline_precision="quarter",
    specificity="vague", volunteered=False, materiality=2, status="pending", evidence="Q2FY27 screener OPM 5.0%.")

SUMMARY_EXTRA = {
    "calls_covered": "8 concalls, Q3FY25 (04-Feb-2025) to Q2FY27 (03-Nov-2026)",
    "grade": "D+ (weak credibility on group-level guidance in FY26-27; segment and date promises poor; candour above Skipper because misses are explained in opening remarks)",
}
ANALYSIS_BODY = ("Promise tracker on KEC International (peer calibration for SKIPPER). 8 concalls (Feb-2025 to Nov-2026); {n_promises} promises extracted, {n_scored} scored. "
    "Status counts: {status_counts}. Weighted delivery ratio {weighted_delivery_ratio_pct}% (specificity-only {specificity_weighted_delivery_ratio_pct}%; raw hit rate {raw_hit_rate_pct}%); "
    "MCS {mcs_schema_scale}. Candour index {candour_index_pct}%. FY25 promises were broadly met (order inflow 24,689 vs 25,000; net debt 4,558 in the 4,500-5,000 range) but FY26 was a near-total miss on the group numbers: revenue +7.6% vs 15% (stated four times), EBITDA ~7.1% vs 8-8.5% (and +150 bp), net debt 6,722 vs 4,500, interest 2.8% vs 2.5%, NWC ~137 vs 100/110 days. "
    "FY27 margin targets (9%+, 'closer to 10%') were re-dated to FY28 and then FY29 without acknowledgement; FY27 revenue cut 12-15% -> 8-10% in Nov-26. Under-promised and beat on SAE, cables and T&D share. "
    "Misses are usually explained in the next opening remarks (water payments, labour, Middle East war, ROW), but targets are re-set silently. Research, not advice.")
