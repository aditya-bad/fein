# Promise ledger for Watts Water Technologies (NYSE: WTS). Built 2026-11-22, US industrials peer set (first US sector).
# Method: 5 Motley Fool call transcripts (Q2-2025, Q4-2025, Q1-2026, Q2-2026, Q3-2026; fetched with curl, UA 'Mozilla/5.0',
# HTML -> text) + the Q3-2025 8-K Exhibit 99.1 press release (no Fool transcript exists for that call; its "Full Year 2025
# Outlook" paragraph is used as the call's guidance). Reading: Fool takeaway list + targeted greps (organic, adjusted operating
# margin, conversion, 80/20, price/cost, outlook) on the full text; outcomes from later calls and SEC XBRL (companyfacts).
# Same scoring as scripts_it_peers/build_seed.py (clarifications A-D of TD_peer_comparison.md apply).
# Watts guides EXPLICITLY every quarter: organic and reported sales growth ranges, adjusted operating / EBITDA margin
# (as bp expansion), next-quarter organic growth and margin bands, FCF conversion. It raised guidance at every call in 2025-26.
TICKER = "US-WTS"
SCREENER = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000795403.json"
F = "https://www.fool.com/earnings/call-transcripts/"
CALLS = {
    "2025-08-07": ("Q2-2025 earnings call transcript (Motley Fool)", F + "2025/08/07/watts-water-wts-q2-2025-earnings-call-transcript/"),
    "2025-11-05": ("Q3-2025 results press release (8-K Ex 99.1; no transcript found)", "https://www.sec.gov/Archives/edgar/data/795403/000110465925107038/wts-20251105xex99d1.htm"),
    "2026-02-12": ("Q4-2025 earnings call transcript (Motley Fool)", F + "2026/02/12/watts-water-wts-q4-2025-earnings-call-transcript/"),
    "2026-05-07": ("Q1-2026 earnings call transcript (Motley Fool)", F + "2026/05/07/watts-water-wts-q1-2026-earnings-transcript/"),
    "2026-08-06": ("Q2-2026 earnings call transcript (Motley Fool)", F + "2026/08/12/watts-water-technologies-wts-q2-2026-earnings-call-transcript/"),
    "2026-11-05": ("Q3-2026 earnings call transcript (Motley Fool)", F + "2026/11/05/watts-water-wts-q3-2026-earnings-call-transcript/"),
}
RP = "Robert J. Pagano Jr. (CEO)"
CFO = "CFO (Shashank Patel to 2025; Diane McClintock from 2026)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q2-2025 (07-Aug-2025)
add(said_on="2025-08-07", slug="fy25-organic-flat-to-3pct", speaker=CFO, category="revenue_growth",
    title="FY2025 organic sales growth flat to +3% (raised two points)",
    quote="We now expect organic sales growth of flat to up 3%, a two-point increase to the midpoint from our previous outlook.",
    metric="organic sales growth FY2025 (company)", target="0% to +3%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY2025 organic +5% (Q4-2025 call: 'organic sales grew 8% in the quarter and 5% for the year'); beaten above the top of the range.", delivered_value="+5% organic", delivery_ratio=1.67, confidence="single-source")
add(said_on="2025-08-07", slug="fy25-reported-growth-2-5pct", speaker=CFO, category="revenue_growth",
    title="FY2025 reported sales growth +2% to +5%",
    quote="[Fool summary] Raised ... reported sales growth to 2%-5% (up three points from previous view).",
    metric="reported net sales growth FY2025", target="+2% to +5%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="SEC XBRL revenue 2.25B (2024) -> 2.44B (2025) = +8.4% (re-derived); company '8% for the year'.", delivered_value="+8.4%", delivery_ratio=1.7, confidence="verified")
add(said_on="2025-08-07", slug="fy25-adj-op-margin-50-110bp", speaker=CFO, category="margin",
    title="FY2025 adjusted operating margin expansion +50 to +110 bp",
    quote="We are also increasing our full-year adjusted operating margin expansion to a range of up 50 basis points to up 110 basis points",
    metric="adjusted operating margin expansion FY2025 (company)", target="+50 to +110 bp", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY2025 adjusted operating margin 19.6%, +190 bp (Q4-2025 call). GAAP op income/revenue 448.1/2,440 = 18.4% (XBRL) vs 17.4% in 2024 (390.4/2,250): +100 bp on GAAP, also inside the band.", delivered_value="+190 bp adjusted (+100 bp GAAP)", delivery_ratio=1.7, confidence="verified")
add(said_on="2025-08-07", slug="q3-25-organic-2-5pct", speaker=CFO, category="revenue_growth",
    title="Q3-2025 organic sales growth +2% to +5%",
    quote="[Fool summary] Organic sales expected to rise 2%-5% in the third quarter of 2025",
    metric="organic sales growth Q3-2025", target="+2% to +5%", deadline="2025-09-30", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q3-2025 organic +9% (press release 05-Nov-2025: 'up 13% on a reported basis and up 9% organically').", delivered_value="+9%", delivery_ratio=1.8)
add(said_on="2025-08-07", slug="q3-25-op-margin-17-1-17-7", speaker=CFO, category="margin",
    title="Q3-2025 operating margin 17.1%-17.7%",
    quote="Operating margin should be in the range of 17.1% to 17.7% [Fool text truncated at '17.'; range from Fool summary]",
    metric="operating margin Q3-2025", target="17.1% to 17.7%", deadline="2025-09-30", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q3-2025 operating margin 18.2% GAAP, 18.5% adjusted (press release).", delivered_value="18.2% / 18.5%", delivery_ratio=1.04)
add(said_on="2025-08-07", slug="fy25-fcf-conversion-100pct", speaker=CFO, category="cash_flow",
    title="FY2025 free cash flow conversion at least 100% of net income",
    quote="[Fool summary] full-year 2025 free cash flow conversion target of at least 100% of net income remains in place",
    metric="FCF / net income FY2025", target=">=100%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="XBRL: CFO 402.0 - capex 45.7 = FCF 356.3 vs net income 340.8 = 104.5% (re-derived); company 105%.", delivered_value="104.5%", delivery_ratio=1.05, confidence="verified")
# ---- Q3-2025 (05-Nov-2025, press release)
add(said_on="2025-11-05", slug="fy25-organic-4-5pct", speaker="Company press release (Pagano quoted)", category="revenue_growth",
    title="FY2025 organic sales growth +4% to +5%; reported +7% to +8%",
    quote="Reported sales are expected to increase between 7% to 8% and organic sales to increase between 4% and 5%.",
    metric="organic sales growth FY2025", target="+4% to +5%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY2025 organic +5%, reported +8.4% (XBRL).", delivered_value="+5% / +8.4%", delivery_ratio=1.0)
add(said_on="2025-11-05", slug="fy25-adj-op-margin-19-1-19-2", speaker="Company press release", category="margin",
    title="FY2025 adjusted operating margin 19.1%-19.2% (+140 to +150 bp)",
    quote="adjusted operating margin is expected to be between 19.1% and 19.2%, or up 140 to 150 basis points.",
    metric="adjusted operating margin FY2025", target="19.1% to 19.2%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    status="delivered", evidence="FY2025 adjusted operating margin 19.6% (+190 bp), above the top of the band.", delivered_value="19.6%", delivery_ratio=1.02)
# ---- Q4-2025 (12-Feb-2026)
add(said_on="2026-02-12", slug="fy26-organic-2-6pct", speaker=CFO, category="revenue_growth",
    title="FY2026 organic sales growth +2% to +6% (about 2 pts more ex 80/20 exits)",
    quote="[Fool summary] 2026 reported sales growth guided at 8%-12%; organic sales growth at 2%-6%",
    metric="organic sales growth FY2026", target="+2% to +6%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    later_restatements="2026-05-07 reiterated 2-6%; 2026-08-06 raised to 8-11%; 2026-11-05 raised to 11-12%. 9M-2026 organic ~12%.")
add(said_on="2026-02-12", slug="fy26-reported-growth-8-12pct", speaker=CFO, category="revenue_growth",
    title="FY2026 reported sales growth +8% to +12%",
    quote="Consolidated organic sales growth is expected to be between +2% and +6% and our reported sales growth is expected to be between +8% and +12%. [restated 07-May-2026]",
    metric="reported sales growth FY2026", target="+8% to +12%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    later_restatements="2026-08-06 raised to 14-17%; 2026-11-05 raised to 17-18%.")
add(said_on="2026-02-12", slug="q1-26-organic-4-8pct", speaker=CFO, category="revenue_growth",
    title="Q1-2026 organic sales growth +4% to +8%",
    quote="[Fool summary] Q1 2026 guidance -- Reported sales growth 12%-16%; organic growth 4%-8%",
    metric="organic sales growth Q1-2026", target="+4% to +8%", deadline="2026-03-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q1-2026 organic +12%, reported +21% (Q1-2026 call).", delivered_value="+12%", delivery_ratio=1.5)
add(said_on="2026-02-12", slug="q1-26-op-margin-18-6-19-2", speaker=CFO, category="margin",
    title="Q1-2026 operating margin 18.6%-19.2%",
    quote="[Fool summary] Q1 margin guidance -- EBITDA margin 21.1%-21.7%; operating margin 18.6%-19.2%",
    metric="adjusted operating margin Q1-2026", target="18.6% to 19.2%", deadline="2026-03-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q1-2026 adjusted operating margin 20.1%, EBITDA 22.3% (Q1-2026 call).", delivered_value="20.1%", delivery_ratio=1.05)
add(said_on="2026-02-12", slug="fy26-americas-80-20-exit-25-30mn", speaker=CFO, category="other",
    title="FY2026 80/20 exits remove $25-30 mn of Americas sales (and $10-15 mn in Europe), margin neutral or accretive",
    quote="Organic sales in The Americas are expected to increase by 3% to 7% ... more than offsetting anticipated product rationalization headwinds of $25 million to $30 million.",
    metric="80/20 product-rationalization sales exited FY2026", target="$25-30 mn Americas", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    later_restatements="2026-08-06 Americas $25-26 mn; 2026-11-05 Americas $26-28 mn, total $30-33 mn.")
add(said_on="2026-02-12", slug="fy26-acquisitions-130mn-plus", speaker=CFO, category="m&a",
    title="FY2026 acquisitions add $130 mn+ of incremental sales, ~50 bp margin dilution",
    quote="[Fool summary] Acquisitions projected to add $130 million+ incremental revenue and dilute adjusted operating margin by about 50 basis points.",
    metric="incremental acquisition sales FY2026", target=">=$130 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    later_restatements="2026-11-05 '$107-109 mn in the Americas and $21-22 mn in APMEA' (= $128-131 mn).")
# ---- Q1-2026 (07-May-2026)
add(said_on="2026-05-07", slug="q2-26-organic-4-8pct", speaker=CFO, category="revenue_growth",
    title="Q2-2026 organic sales growth +4% to +8%",
    quote="[Fool summary] Second Quarter Guidance -- Reported sales expected to rise 10%-14%; organic growth of 4%-8% anticipated",
    metric="organic sales growth Q2-2026", target="+4% to +8%", deadline="2026-06-30", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q2-2026 organic +12.2%, reported +19% (Q2-2026 call).", delivered_value="+12.2%", delivery_ratio=1.5)
add(said_on="2026-05-07", slug="q2-26-op-margin-20-0-20-6", speaker=CFO, category="margin",
    title="Q2-2026 operating margin 20.0%-20.6%",
    quote="[Fool summary] Margin Guidance Q2 -- EBITDA margin projected at 22.3%-22.9%; operating margin at 20.0%-20.6%",
    metric="adjusted operating margin Q2-2026", target="20.0% to 20.6%", deadline="2026-06-30", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2,
    status="delivered", evidence="Q2-2026 adjusted operating margin 21.0%, EBITDA 23.1% (Q2-2026 call).", delivered_value="21.0%", delivery_ratio=1.02)
# ---- Q2-2026 (06-Aug-2026)
add(said_on="2026-08-06", slug="fy26-fcf-conversion-90pct", speaker=CFO, category="cash_flow",
    title="FY2026 free cash flow conversion 90% or more of net income",
    quote="[Fool summary] Free Cash Flow Conversion Guidance -- targeted at 90% or higher of net income for the full year 2026.",
    metric="FCF / net income FY2026", target=">=90%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    later_restatements="2026-11-05 maintained '90% or greater'. 9M-2026 FCF $230 mn.")
add(said_on="2026-08-06", slug="fy26-price-cost-neutral", speaker=RP, category="price_cost",
    title="Price/cost to stay at least neutral through H2-2026 despite new tariffs",
    quote="We feel okay about our price/cost dynamic right now.",
    metric="price/cost (company)", target="neutral or better", deadline="2026-12-31", deadline_precision="half-year",
    specificity="vague", volunteered=False, materiality=1)
# ---- Q3-2026 (05-Nov-2026)
add(said_on="2026-11-05", slug="fy26-organic-11-12pct", speaker=CFO, category="revenue_growth",
    title="FY2026 organic sales growth +11% to +12%",
    quote="We now anticipate organic sales growth of 11% to 12%, which reflects a 2-point increase to the midpoint of our previous outlook.",
    metric="organic sales growth FY2026 (company)", target="+11% to +12%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3)
add(said_on="2026-11-05", slug="fy26-reported-growth-17-18pct", speaker=CFO, category="revenue_growth",
    title="FY2026 reported sales growth +17% to +18%",
    quote="[Fool summary] 2026 Reported Sales Guidance -- 17% to 18% growth, incorporating approximately $128 million to $131 million in incremental acquisition revenue.",
    metric="reported net sales growth FY2026", target="+17% to +18%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3)
add(said_on="2026-11-05", slug="fy26-adj-op-margin-20-3-20-4", speaker=CFO, category="margin",
    title="FY2026 adjusted operating margin 20.3%-20.4% (+70 to +80 bp)",
    quote="[Fool summary] 2026 Adjusted Operating Margin Guidance -- 20.3% to 20.4%, representing a projected increase of 70 to 80 basis points for the year.",
    metric="adjusted operating margin FY2026 (company)", target="20.3% to 20.4%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=3,
    later_restatements="origin 2026-02-12 margin bands by segment; 2026-08-06 19.8-20.4% (+20 to +80 bp)")
add(said_on="2026-11-05", slug="q4-26-organic-9-12pct", speaker=CFO, category="revenue_growth",
    title="Q4-2026 organic sales growth +9% to +12%",
    quote="[Fool summary] Q4 2026 Organic Sales Outlook -- 9% to 12% growth, including anticipated growth of 11% to 14% in the Americas.",
    metric="organic sales growth Q4-2026", target="+9% to +12%", deadline="2026-12-31", deadline_precision="quarter",
    specificity="range", volunteered=True, materiality=2)

ANALYSIS_TITLE = "US-WTS - Management Credibility Score (US industrials peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Watts Water (6 calls Q2-2025..Q3-2026; Q3-2025 from the 8-K press release): {n_promises} promises logged, {n_scored} scored. "
                 "Weighted delivery {weighted_delivery_ratio_pct}% (specificity-weighted {specificity_weighted_delivery_ratio_pct}%), MCS {mcs_schema_scale}. "
                 "Every scored guide was met or beaten: FY2025 organic flat-3% -> +5%, adj. operating margin +50-110 bp -> +190 bp, each next-quarter organic and margin band beaten. "
                 "A systematic sandbagger: guidance raised at every call in 2025-26. FY2026 items (organic 11-12%, reported 17-18%, adj. op margin 20.3-20.4%, FCF conversion >=90%) pending. Research, not advice.")
