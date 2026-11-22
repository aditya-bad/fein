# Promise ledger for A. O. Smith (NYSE: AOS). Built 2026-11-22, US industrials peer set (first US sector).
# Method: 6 Motley Fool call transcripts Q2-2025..Q3-2026 (curl, UA 'Mozilla/5.0', HTML -> text; the Q2-2026 call is listed
# twice on fool.com, the 30-Jul-2026 copy is used). Reading: Fool takeaway list + the CFO outlook section read in full +
# targeted greps (EPS, free cash flow, segment margin, boiler, water treatment, China, Leonard Valve, savings, repurchase).
# Outcomes from the Q4-2025 call and SEC XBRL companyfacts (EPS, FCF, capex, buybacks re-derived).
# Same scoring as scripts_it_peers/build_seed.py; clarification A (a cut >= 2 quarters before the deadline = 'withdrawn')
# matters here: the FY2026 guide was cut three times (Apr, Jul, Oct-2026), the last time with China moved to discontinued ops.
TICKER = "US-AOS"
SCREENER = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000091142.json"
F = "https://www.fool.com/earnings/call-transcripts/"
CALLS = {
    "2025-07-24": ("Q2-2025 earnings call transcript (Motley Fool)", F + "2025/07/24/a-o-smith-aos-q2-2025-earnings-call-transcript/"),
    "2025-10-28": ("Q3-2025 earnings call transcript (Motley Fool)", F + "2025/10/28/a-o-smith-aos-q3-2025-earnings-call-transcript/"),
    "2026-01-29": ("Q4-2025 earnings call transcript (Motley Fool)", F + "2026/01/29/a-o-smith-aos-q4-2025-earnings-call-transcript/"),
    "2026-04-30": ("Q1-2026 earnings call transcript (Motley Fool)", F + "2026/04/30/a-o-smith-aos-q1-2026-earnings-transcript/"),
    "2026-07-30": ("Q2-2026 earnings call transcript (Motley Fool)", F + "2026/07/30/ao-smith-aos-q2-2026-earnings-call-transcript/"),
    "2026-10-29": ("Q3-2026 earnings call transcript (Motley Fool)", F + "2026/10/29/a-o-smith-aos-q3-2026-earnings-call-transcript/"),
}
SS = "Stephen Shafer (CEO)"
CL = "Charles T. Lauber (CFO to Q2-2026)"
CA = "Carrie L. Anderson (CFO from Q3-2026)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q2-2025 (24-Jul-2025)
add(said_on="2025-07-24", slug="fy25-eps-3-70-3-90", speaker=CL, category="eps",
    title="FY2025 EPS $3.70-$3.90 (narrowed)",
    quote="... to a narrowed range of between $3.70 and $3.90 per share [Fool text split at the decimal point]",
    metric="diluted EPS FY2025 (adjusted = GAAP in 2025)", target="$3.70 to $3.90", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY2025 EPS $3.85 (SEC XBRL EarningsPerShareDiluted 3.85; Q4-2025 call 'record $3.85').", delivered_value="$3.85", delivery_ratio=1.0, confidence="verified",
    later_restatements="2025-10-28 narrowed and lowered to $3.70-$3.85 (the top cut by 5 cents)")
add(said_on="2025-07-24", slug="fy25-fcf-500-525mn", speaker=CL, category="cash_flow",
    title="FY2025 free cash flow $500-525 mn",
    quote="We expect to generate free cash flow of between $500 and $525 million.",
    metric="free cash flow FY2025", target="$500-525 mn", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="FY2025 FCF $546 mn (XBRL CFO 616.8 - capex 70.8 = 546.0, re-derived), above the range; helped by a one-time tax item.", delivered_value="$546 mn", delivery_ratio=1.04, confidence="verified",
    later_restatements="2025-10-28 'approximately $500 million'")
add(said_on="2025-07-24", slug="fy25-na-margin-24-24-5", speaker=CL, category="segment_margin",
    title="FY2025 North America segment margin 24%-24.5%",
    quote="[Fool summary] Segment Margin Guidance: North America: 24%-24.5% for 2025",
    metric="North America segment margin FY2025", target="24.0% to 24.5%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY2025 North America segment margin 24.4% (Q4-2025 call).", delivered_value="24.4%", delivery_ratio=1.0)
add(said_on="2025-07-24", slug="fy25-row-margin-8-9", speaker=CL, category="segment_margin",
    title="FY2025 Rest of World segment margin 8%-9%",
    quote="[Fool summary] Rest of World: 8%-9% for 2025",
    metric="Rest of World segment margin FY2025", target="8% to 9%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="FY2025 Rest of World segment margin 8.7% (Q4-2025 call). The Oct-2025 call's 'about 7.5%' (Fool summary) looks like a quarter figure; not used.", delivered_value="8.7%", delivery_ratio=1.0)
add(said_on="2025-07-24", slug="fy25-boiler-growth-4-6pct", speaker=SS, category="revenue_growth",
    title="FY2025 North America boiler sales +4% to +6% (raised from 3-5%)",
    quote="[Fool summary] North America boiler sales outlook raised to 4%-6% growth for 2025",
    metric="North America boiler sales growth FY2025", target="+4% to +6%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="FY2025 boiler sales +8% (Q4-2025 call).", delivered_value="+8%", delivery_ratio=1.6)
add(said_on="2025-07-24", slug="fy25-water-treatment-decline-5pct", speaker=SS, category="revenue_growth",
    title="FY2025 North America water treatment sales down ~5% (retail de-emphasised)",
    quote="We have not changed our guidance that North America water treatment sales will decline approximately 5% in 2025, as we deemphasize the less profitable retail channel.",
    metric="North America water treatment sales growth FY2025", target="~-5%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="FY2025 water treatment sales -2% (Q4-2025 call): better than guided.", delivered_value="-2%", delivery_ratio=1.0)
add(said_on="2025-07-24", slug="fy25-water-treatment-margin-250-300bp", speaker=CL, category="segment_margin",
    title="FY2025 North America water treatment margin +250 to +300 bp",
    quote="You know, we are tracking to our target of 250 to 300 basis points improvement.",
    metric="water treatment operating margin expansion FY2025", target="+250 to +300 bp", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=2,
    status="delivered", evidence="'expanded operating margin by 400 basis points to almost 13% last year' (Q4-2025 call).", delivered_value="+400 bp", delivery_ratio=1.4)
add(said_on="2025-07-24", slug="fy25-china-decline-5-8pct", speaker=CL, category="revenue_growth",
    title="FY2025 China sales down 5%-8% (local currency)",
    quote="And full year being 5% to 8% down.",
    metric="China sales growth FY2025 (local currency)", target="-5% to -8%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=2,
    status="missed", evidence="FY2025 China third-party sales -12% in local currency (Q4-2025 call), 4 pts below the bottom of the range. Lowered to 'down 10%' in Oct-2025 (final quarter: clarification A, scored on outcome).", delivered_value="-12%", explanation_for_miss="weak consumer demand; subsidy programme ended in H2", admitted_unprompted=True,
    later_restatements="2025-10-28 'we did revise down our China outlook for the year to down 10%'")
add(said_on="2025-07-24", slug="china-restructuring-savings-15mn", speaker=CL, category="cost_savings",
    title="~$15 mn annual savings from the 2024 China restructuring realised in 2025",
    quote="We continue to expect to realize annual savings of approximately $15 million from our 2024 restructuring actions",
    metric="annualised restructuring savings (company)", target="~$15 mn in 2025", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="Q4-2025 call: 'The restructuring actions we took in late 2024 and expense management drove profitability improvement of 130 basis points despite lower sales' (China); RoW earnings flat despite -4% sales. The $15 mn itself is not separately reported.", delivery_ratio=1.0)
add(said_on="2025-07-24", slug="fy25-buyback-400mn", speaker=CL, category="capital_return",
    title="FY2025 share repurchases ~$400 mn",
    quote="we increased our planned full-year repurchase intentions from $306 million in 2024 to approximately $400 million of shares for 2025.",
    metric="share repurchases FY2025", target="~$400 mn", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="XBRL PaymentsForRepurchaseOfCommonStock FY2025 $400.8 mn.", delivered_value="$400.8 mn", delivery_ratio=1.0, confidence="verified")
# ---- Q3-2025 (28-Oct-2025)
add(said_on="2025-10-28", slug="fy25-capex-75mn", speaker=CL, category="capex",
    title="FY2025 capital expenditures ~$75 mn (lowered; projects shift into 2026)",
    quote="[Fool summary] 2025 capital expenditures projected at $75 million, slightly lowered as some projects shift into early 2026.",
    metric="capex FY2025", target="~$75 mn", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    status="partly", evidence="XBRL capex (PaymentsToAcquireProductiveAssets) FY2025 $70.8 mn: 5.6% under a one-quarter-ahead estimate.", delivered_value="$70.8 mn", delivery_ratio=0.94, confidence="verified")
add(said_on="2025-10-28", slug="fy25-china-decline-10pct", speaker=SS, category="revenue_growth",
    title="FY2025 China sales down ~10% (local currency)",
    quote="But I will say when you frame our outlook for China overall to be down 10%, you'll note the fourth quarter gets a little more pressure on year-over-year comps",
    metric="China sales growth FY2025 (local currency)", target="~-10%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    status="partly", evidence="FY2025 China -12% in local currency (Q4-2025 call): 2 pts worse than a one-quarter-ahead estimate.", delivered_value="-12%", delivery_ratio=0.8, admitted_unprompted=True)
# ---- Q4-2025 (29-Jan-2026)
add(said_on="2026-01-29", slug="fy26-eps-3-85-4-15", speaker=CL, category="eps",
    title="FY2026 EPS $3.85-$4.15 (midpoint +4%)",
    quote="Our 2026 outlook includes an expected EPS range of $3.85 to $4.15 per share. The midpoint of our EPS range represents 4% growth over our 2025 EPS.",
    metric="adjusted diluted EPS FY2026", target="$3.85 to $4.15", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="withdrawn", evidence="Cut on 30-Apr-2026 to adjusted $3.70-$4.00 (China, residential volume, input costs; explained, 3 quarters before the deadline: clarification A), then $3.70-$3.85 (Jul) and $3.42-$3.52 ex-China continuing ops (Oct).", explanation_for_miss="China demand, lower residential water-heater volume, steel +15-20%", admitted_unprompted=True,
    later_restatements="2026-04-30 $3.70-$4.00 adjusted; 2026-07-30 $3.70-$3.85; 2026-10-29 $3.42-$3.52 (continuing operations, China excluded)")
add(said_on="2026-01-29", slug="fy26-sales-growth-2-5pct", speaker=SS, category="revenue_growth",
    title="FY2026 total sales growth ~+2% to +5%",
    quote="Based on those 2026 assumptions, we expect top-line growth of approximately 2% to 5%.",
    metric="net sales growth FY2026", target="+2% to +5%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    status="withdrawn", evidence="Narrowed to 2-4% (Apr) and 2-3% (Jul), then re-based to 'approximately 4%' excluding China (Oct). The basis change (China to discontinued operations) means the original total-company target can no longer be measured as stated; scored withdrawn (explicit, explained, >= 2 quarters before the deadline).", admitted_unprompted=True,
    later_restatements="2026-04-30 2-4%; 2026-07-30 2-3%; 2026-10-29 ~4% ex-China")
add(said_on="2026-01-29", slug="fy26-fcf-525-575mn", speaker=CL, category="cash_flow",
    title="FY2026 free cash flow $525-575 mn",
    quote="We project a generate a strong free cash flow of between $525 and $575 million.",
    metric="free cash flow FY2026", target="$525-575 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    later_restatements="2026-04-30 reiterated; 9M-2026 FCF $396 mn (+4%)")
add(said_on="2026-01-29", slug="fy26-row-margin-8-9", speaker=CL, category="segment_margin",
    title="FY2026 Rest of World segment margin 8%-9%",
    quote="[Fool summary] 2026 Segment Margins -- Guidance for North America at 24%-24.5%, Rest of World at 8%-9%.",
    metric="Rest of World segment margin FY2026", target="8% to 9%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    status="withdrawn", evidence="Cut on 30-Apr-2026 to 6%-7% (China demand; explained); China then moved to discontinued operations (Oct).", admitted_unprompted=True)
add(said_on="2026-01-29", slug="fy26-na-margin-24-24-5", speaker=CL, category="segment_margin",
    title="FY2026 North America segment margin 24%-24.5%",
    quote="[Fool summary] 2026 Segment Margins -- Guidance for North America at 24%-24.5%",
    metric="North America segment margin FY2026", target="24.0% to 24.5%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    later_restatements="2026-04-30 'approximately 24%'; 2026-10-29 'We have maintained the North margin guidance of approximately 24%'. Q1-Q3 23.3% / 24.4% adj / 23.6%.")
add(said_on="2026-01-29", slug="fy26-water-treatment-growth-10-12pct", speaker=SS, category="revenue_growth",
    title="FY2026 North America water treatment sales +10% to +12%",
    quote="We expect North America water treatment sales will grow between 10-12% due to tariff-related pricing benefits",
    metric="water treatment sales growth FY2026", target="+10% to +12%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    status="withdrawn", evidence="Cut on 30-Apr-2026 to +5-6% (consumer caution, trade-down; explained), then to +3-4% (Oct).", admitted_unprompted=True)
add(said_on="2026-01-29", slug="fy26-boiler-growth-6-8pct", speaker=SS, category="revenue_growth",
    title="FY2026 North America boiler sales +6% to +8%",
    quote="We project our North America boiler sales will grow between 6 to 8% in 2026 due to the carryover of pricing benefits",
    metric="boiler sales growth FY2026", target="+6% to +8%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    later_restatements="2026-10-29 raised to +10-12% (Q2 +21%, Q3 +13%)")
add(said_on="2026-01-29", slug="fy26-china-decline-mid-single", speaker=SS, category="revenue_growth",
    title="FY2026 China sales down mid-single digits, back to growth in H2",
    quote="we project that our 2026 China sales will decrease mid-single digits compared to last year ... We anticipate a return to growth in the second half of the year.",
    metric="China sales growth FY2026 (local currency)", target="-4% to -6%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=2,
    status="withdrawn", evidence="Cut on 30-Apr-2026 to 'down low double digits' (Q1 -17%); Q3 China sales 'well below our expectations'; business sold (81% to CPE, Oct-2026).", admitted_unprompted=True)
add(said_on="2026-01-29", slug="fy26-leonard-valve-70mn", speaker=SS, category="m&a",
    title="Leonard Valve to contribute ~$70 mn of 2026 sales",
    quote="We expect Leonard Valve to contribute approximately $70 million in sales in 2026.",
    metric="Leonard Valve sales FY2026", target="~$70 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    later_restatements="2026-07-30 'full-year target of approximately $70 million'; 2026-10-29 lowered to $55 mn (regional project delays; final quarter: scored on outcome). 9M: 16 + 16 + 15 = $47 mn.")
add(said_on="2026-01-29", slug="fy26-buyback-200mn", speaker=CL, category="capital_return",
    title="FY2026 share repurchases ~$200 mn",
    quote="[Fool summary] Stock Repurchases -- $200 million targeted for 2026",
    metric="share repurchases FY2026", target="~$200 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    later_restatements="2026-07-30 raised to $300 mn; 9M-2026 $260.6 mn")
# ---- Q1-2026 (30-Apr-2026)
add(said_on="2026-04-30", slug="q2-26-eps-25pct-of-midpoint", speaker=CL, category="eps",
    title="Q2-2026 EPS ~25% of the full-year guidance midpoint ($3.85 x 25% = ~$0.96)",
    quote="Overall, Q2 EPS is expected to be roughly 25% of our full-year guidance midpoint.",
    metric="adjusted EPS Q2-2026", target="~$0.96", deadline="2026-06-30", deadline_precision="quarter",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="Q2-2026 adjusted EPS $1.03 (Q2-2026 call) = 27% of the $3.85 midpoint.", delivered_value="$1.03", delivery_ratio=1.07)
add(said_on="2026-04-30", slug="wt-restructuring-savings-6-8mn-2027", speaker=CL, category="cost_savings",
    title="Water-treatment restructuring ($20 mn charge) to save $6-8 mn a year from 2027",
    quote="[Fool summary] North America Water Treatment Restructuring -- $20 million charge projected in Q2, with annual savings of $6 million to $8 million beginning in 2027.",
    metric="annual restructuring savings", target="$6-8 mn from 2027", deadline="2027-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    later_restatements="2026-07-30 reiterated; 9M-2026 restructuring expense $22.6 mn (above the $20 mn charge)")
# ---- Q2-2026 (30-Jul-2026)
add(said_on="2026-07-30", slug="fy26-buyback-300mn", speaker=SS, category="capital_return",
    title="FY2026 share repurchases ~$300 mn (raised 50%)",
    quote="we increased our 2026 share repurchase target by 50% to $300 million",
    metric="share repurchases FY2026", target="~$300 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    later_restatements="2026-10-29 maintained; 9M $260.6 mn")
# ---- Q3-2026 (29-Oct-2026)
add(said_on="2026-10-29", slug="fy26-adj-eps-3-42-3-52-ex-china", speaker=CA, category="eps",
    title="FY2026 adjusted EPS $3.42-$3.52 (continuing operations, China excluded)",
    quote="Our full year sales, excluding China, are expected to grow approximately 4% with adjusted EPS between $3.42 and $3.52 per share.",
    metric="adjusted diluted EPS from continuing operations FY2026", target="$3.42 to $3.52", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3)
add(said_on="2026-10-29", slug="fy26-sales-growth-4pct-ex-china", speaker=CA, category="revenue_growth",
    title="FY2026 sales excluding China up ~4%",
    quote="Our full year sales, excluding China, are expected to grow approximately 4%",
    metric="net sales growth FY2026, continuing operations", target="~+4%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2)
add(said_on="2026-10-29", slug="china-sale-close-h1-2027", speaker=SS, category="m&a",
    title="Sale of 81% of the China business to CPE to close in H1-2027",
    quote="We plan to close in the first half of 2027 subject to regulatory approvals and customary closing conditions.",
    metric="China divestiture closing", target="closed by 30-Jun-2027", deadline="2027-06-30", deadline_precision="half-year",
    specificity="range", volunteered=True, materiality=2)

ANALYSIS_TITLE = "US-AOS - Management Credibility Score (US industrials peer calibration, Nov 2026)"
ANALYSIS_BODY = ("A. O. Smith (6 calls Q2-2025..Q3-2026): {n_promises} promises logged, {n_scored} scored. "
                 "Weighted delivery {weighted_delivery_ratio_pct}% (specificity-weighted {specificity_weighted_delivery_ratio_pct}%), MCS {mcs_schema_scale}. "
                 "FY2025 guidance on the company-level numbers was met (EPS $3.85 in a $3.70-3.90 band, FCF $546 mn vs $500-525 mn, NA margin 24.4%, buybacks $401 mn); China was the repeated miss (-5..-8% -> -12%). "
                 "FY2026 guidance was cut three times (EPS $3.85-4.15 -> $3.70-4.00 -> $3.70-3.85 -> $3.42-3.52 ex-China); the Jan-2026 EPS, RoW margin, water-treatment and China items score 'withdrawn'. Research, not advice.")
