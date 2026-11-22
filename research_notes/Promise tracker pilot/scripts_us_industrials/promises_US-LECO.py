# Promise ledger for Lincoln Electric (NASDAQ: LECO). Built 2026-11-22, US industrials peer set (first US sector).
# Method: 4 Motley Fool call transcripts (Q3-2025, Q4-2025, Q1-2026, Q3-2026; curl, UA 'Mozilla/5.0') + the Q2-2025 and
# Q2-2026 8-K Exhibit 99.1 press releases (no Fool transcripts found for those two calls; Lincoln's releases carry almost no
# outlook, so those two quarters contribute only the Alloy Steel deal statement). This is the thinnest read of the four.
# Lincoln gives an 'operating framework' (sales growth in words - 'mid single digit', 'high single digit', 'low teens' - plus
# segment EBIT-margin bands, incremental margin, capex, cash conversion) rather than numeric EPS guidance.
# Outcomes from later calls, the Q4-2025 press release (cash conversion table) and SEC XBRL.
TICKER = "US-LECO"
SCREENER = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000059527.json"
F = "https://www.fool.com/earnings/call-transcripts/"
CALLS = {
    "2025-07-31": ("Q2-2025 results press release (8-K Ex 99.1; no transcript found)", "https://www.sec.gov/Archives/edgar/data/59527/000005952725000022/leco-20250731xex99d1.htm"),
    "2025-10-30": ("Q3-2025 earnings call transcript (Motley Fool)", F + "2025/10/30/lincoln-electric-leco-earnings-call-transcript/"),
    "2026-02-12": ("Q4-2025 earnings call transcript (Motley Fool)", F + "2026/02/12/lincoln-electric-leco-earnings-call-transcript/"),
    "2026-04-30": ("Q1-2026 earnings call transcript (Motley Fool)", F + "2026/04/30/leco-q1-2026-earnings-transcript/"),
    "2026-07-30": ("Q2-2026 results press release (8-K Ex 99.1; no transcript found)", "https://www.sec.gov/Archives/edgar/data/59527/000005952726000021/leco-20260730xex99d1.htm"),
    "2026-10-27": ("Q3-2026 earnings call transcript (Motley Fool)", F + "2026/10/27/lincoln-electric-leco-q3-2026-earnings-call-transcript/"),
}
SH = "Steven Hedlund (CEO)"
GB = "Gabriel Bruno (CFO)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q2-2025 (31-Jul-2025, press release)
add(said_on="2025-07-31", slug="alloy-steel-close-aug25", speaker="Company press release", category="m&a",
    title="Acquisition of the remaining 65% of Alloy Steel (~$90 mn) to close on 01-Aug-2025",
    quote="The Company has entered into an agreement to acquire the remaining 65% of Alloy Steel ... for approximately $90 million, which is expected to close on August 1, 2025",
    metric="deal closing", target="closed 01-Aug-2025", deadline="2025-08-31", deadline_precision="month",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="Q3-2025 call: International Welding sales +~4% 'benefit from our alloy steel acquisition'; interest expense raised 'due to recent borrowings for the alloy steel transaction'.", delivery_ratio=1.0)
# ---- Q3-2025 (30-Oct-2025)
add(said_on="2025-10-30", slug="q4-25-automation-up-15-20pct-seq", speaker=SH, category="revenue_growth",
    title="Q4-2025 automation sales up 15%-20% sequentially (from $200 mn), still below Q4-2024",
    quote="If this trend continues, we expect fourth quarter automation sales to be 15% to 20% higher sequentially but still below last year's sales level.",
    metric="automation sales Q4-2025 vs Q3-2025", target="+15% to +20% QoQ", deadline="2025-12-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q4-2025 automation sales $240 mn (down 11% YoY) vs $200 mn in Q3 = +20% QoQ (Q4-2025 call).", delivered_value="+20% QoQ", delivery_ratio=1.0)
add(said_on="2025-10-30", slug="q4-25-modest-seq-margin-improvement", speaker=GB, category="margin",
    title="Q4-2025 adjusted operating margin modestly above Q3 (17.4%)",
    quote="We expect traditional seasonality in our sales performance as we move from the third quarter to the fourth quarter with a modest sequential improvement in our operating income margin.",
    metric="adjusted operating income margin Q4-2025 vs Q3-2025", target="> 17.4%", deadline="2025-12-31", deadline_precision="quarter",
    specificity="vague", volunteered=True, materiality=2,
    status="delivered", evidence="Q4-2025 adjusted operating income margin 18.0% (Q4-2025 call: 'declined 20 basis points to 18%' YoY) vs Q3-2025 17.4%.", delivered_value="18.0%", delivery_ratio=1.03)
add(said_on="2025-10-30", slug="q4-25-americas-ebit-18-19pct", speaker=GB, category="segment_margin",
    title="Americas Welding adjusted EBIT margin 18%-19% for the rest of 2025",
    quote="We expect Americas Welding to continue to operate in the 18% to 19% EBIT margin range for the remainder of the year.",
    metric="Americas Welding adjusted EBIT margin Q4-2025", target="18% to 19%", deadline="2025-12-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q4-2025 Americas Welding adjusted EBIT $141 mn, margin ~20% (Fool summary 'Americas Welding: 20% (up 90 bps)'): above the band.", delivered_value="~20%", delivery_ratio=1.05)
add(said_on="2025-10-30", slug="q4-25-international-ebit-11-12pct", speaker=GB, category="segment_margin",
    title="International Welding adjusted EBIT margin 11%-12% for the rest of 2025",
    quote="We expect International Welding's margin performance to continue to operate in the 11% to 12% range for the balance of the year.",
    metric="International Welding adjusted EBIT margin Q4-2025", target="11% to 12%", deadline="2025-12-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=1,
    status="delivered", evidence="Fool Q4-2025 summary: 'International Welding: 11.8% (down 100 bps)' - inside the band; whether this is the quarter or the year is not stated (single-source).", delivered_value="11.8%", delivery_ratio=1.0)
add(said_on="2025-10-30", slug="fy25-cash-conversion-above-100pct", speaker=GB, category="cash_flow",
    title="FY2025 cash conversion above 100% (range raised)",
    quote="we are increasing our cash conversion range to above 100% to better align with performance.",
    metric="cash conversion FY2025 (FCF / adjusted net income, company)", target=">100%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    status="partly", evidence="Q4-2025 press release table: FY2025 cash conversion 97% (FCF $534.2 mn / adjusted net income $551.3 mn); Q4 alone 35%. A floor raised one quarter before the deadline and then missed by 3 pts; not mentioned on the Q4 call.", delivered_value="97%", delivery_ratio=0.97, admitted_unprompted=False)
# ---- Q4-2025 (12-Feb-2026)
add(said_on="2026-02-12", slug="fy26-sales-growth-mid-single", speaker=GB, category="revenue_growth",
    title="FY2026 net sales growth in the mid-single-digit range (half volume, half price carry-over)",
    quote="Our full year 2026 operating framework assumes the sales growth rate in the mid single digit percent range with organic sales split fifty-fifty between volume and the 2025 price actions that carry over to 2026.",
    metric="net sales growth FY2026", target="+4% to +6%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=3,
    later_restatements="2026-04-30 raised to 'high single-digit'; 2026-10-27 'low teens percent range for the full year'. 9M-2026: +12%, ~+10%, +15.1%.")
add(said_on="2026-02-12", slug="fy26-automation-mid-single-growth", speaker=GB, category="revenue_growth",
    title="FY2026 automation sales return to mid-single-digit growth (from $870 mn)",
    quote="So think about a mid single digit type of growth trajectory potentially in automation based on what we have seen in order levels in our backlog.",
    metric="automation sales growth FY2026", target="+4% to +6%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=False, materiality=1,
    later_restatements="2026-10-27 Q3 automation $232 mn, 'high teens percent organic growth', record backlog")
add(said_on="2026-02-12", slug="fy26-modest-margin-improvement", speaker=GB, category="margin",
    title="FY2026 adjusted operating margin modestly above 2025 (17.2%), mid-20% incrementals",
    quote="We will continue to pursue a neutral price-cost posture and expect a mid 20% incremental operating income margin from volume growth and enterprise initiatives, which will result in a modest improvement in our operating margin for the full year.",
    metric="adjusted operating income margin FY2026 vs FY2025", target="> FY2025 adjusted margin", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=3,
    later_restatements="2026-04-30 'We are maintaining our other full-year assumptions on operating income margin improvement, a mid-20% incremental margin'. Q1 16.9% (flat), Q3 18.0% (+60 bp).")
add(said_on="2026-02-12", slug="fy26-americas-ebit-mid-18-mid-19", speaker=GB, category="segment_margin",
    title="FY2026 Americas Welding EBIT margin mid-18% to mid-19%",
    quote="We expect Americas Welding to continue to operate in the mid 18 to mid 19% EBIT margin range in 2026.",
    metric="Americas Welding adjusted EBIT margin FY2026", target="18.5% to 19.5%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    later_restatements="2026-10-27 Q4 guide 20-21% (Q1 17.2%)")
add(said_on="2026-02-12", slug="fy26-international-ebit-mid-11-mid-12", speaker=GB, category="segment_margin",
    title="FY2026 International Welding EBIT margin mid-11% to mid-12%",
    quote="We expect International Welding's margin performance to be in the mid 11 to mid 12% margin range in 2026.",
    metric="International Welding adjusted EBIT margin FY2026", target="11.5% to 12.5%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    later_restatements="2026-10-27 Q4 guide 12-13% (Q1 9.7%)")
add(said_on="2026-02-12", slug="fy26-capex-110-130mn", speaker=GB, category="capex",
    title="FY2026 capex $110-130 mn",
    quote="We will continue to maintain an elevated level of capital spending with a target range of $110 to $130,000,000",
    metric="capex FY2026", target="$110-130 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    later_restatements="2026-04-30 maintained; 2026-10-27 raised to $140-150 mn (final quarter: clarification A, scored on outcome)")
add(said_on="2026-02-12", slug="fy26-cash-conversion-100pct", speaker=GB, category="cash_flow",
    title="FY2026 cash conversion ~100%",
    quote="We are still anchored on 100% cash conversion, so we expect that while we are investing short term with some product transitions, that would turn around in the back half of the year. [restated 30-Apr-2026]",
    metric="cash conversion FY2026 (company)", target="~100%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    later_restatements="2026-10-27 '107% cash conversion for the quarter, and are at 99% on a year to date basis'")
add(said_on="2026-02-12", slug="2030-op-margin-19pct-avg-sales-6bn", speaker=SH, category="margin",
    title="2030 targets: sales >$6 bn, 19% average operating margin (peak 20%+), mid-teens EPS CAGR",
    quote="This will increase our average operating income margin to 19% across the cycle which is a 300 basis point improvement",
    metric="average operating income margin 2026-2030", target="19% average", deadline="2030-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3)
# ---- Q1-2026 (30-Apr-2026)
add(said_on="2026-04-30", slug="fy26-sales-growth-high-single", speaker=GB, category="revenue_growth",
    title="FY2026 net sales growth raised to the high-single-digit range",
    quote="[Fool summary] 2026 Sales Guidance Update -- Management raised net sales growth guidance to a high single-digit percent range",
    metric="net sales growth FY2026", target="+7% to +9%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=2,
    later_restatements="2026-10-27 low teens")
# ---- Q3-2026 (27-Oct-2026)
add(said_on="2026-10-27", slug="fy26-sales-growth-low-teens", speaker=GB, category="revenue_growth",
    title="FY2026 net sales growth in the low-teens percent range",
    quote="We now expect net sales growth to be in the low teens percent range for the full year which aligns with our performance year to date.",
    metric="net sales growth FY2026 (reported)", target="+11% to +13%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=3)
add(said_on="2026-10-27", slug="fy26-capex-140-150mn", speaker=GB, category="capex",
    title="FY2026 capex $140-150 mn",
    quote="[Fool summary] Annual Capital Expenditure Guidance -- $140 million to $150 million, an increase from the initial 2026 assumption of $110 million to $130 million.",
    metric="capex FY2026", target="$140-150 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1)
add(said_on="2026-10-27", slug="q4-26-americas-ebit-20-21pct", speaker=GB, category="segment_margin",
    title="Q4-2026 Americas Welding adjusted EBIT margin 20%-21%; International Welding 12%-13%",
    quote="[Fool summary] Segment Margin Outlook -- 20% to 21% for Americas Welding and 12% to 13% for International Welding in the fourth quarter.",
    metric="Americas Welding adjusted EBIT margin Q4-2026", target="20% to 21%", deadline="2026-12-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2)

ANALYSIS_TITLE = "US-LECO - Management Credibility Score (US industrials peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Lincoln Electric (6 calls Q2-2025..Q3-2026; Q2-2025 and Q2-2026 from press releases only): {n_promises} promises logged, {n_scored} scored. "
                 "Weighted delivery {weighted_delivery_ratio_pct}% (specificity-weighted {specificity_weighted_delivery_ratio_pct}%), MCS {mcs_schema_scale}. "
                 "Lincoln guides in words ('mid single digit', 'modest improvement') plus segment EBIT bands; the near-term Q4-2025 statements were met (automation +20% QoQ, margin 18.0% > 17.4%), the raised FY2025 cash-conversion floor (>100%) was missed at 97% without comment. "
                 "FY2026 sales guide raised twice (mid-single -> high-single -> low teens); capex raised from $110-130 mn to $140-150 mn. Thin sample (6 scored). Research, not advice.")
