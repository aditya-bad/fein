# Promise ledger for Simpson Manufacturing (NYSE: SSD). Built 2026-11-22, US industrials peer set (first US sector).
# Method: 5 Motley Fool call transcripts (Q2-2025, Q3-2025, Q4-2025, Q1-2026, Q3-2026; curl, UA 'Mozilla/5.0') + the Q2-2026
# 8-K Exhibit 99.1 press release 'Business Outlook' section (27-Jul-2026; no Fool transcript found). fool.com page dates are
# publication dates; the call dates used are the 'DATE' lines (Simpson reports after the close on Mondays).
# Reading: Fool takeaways + the CFO outlook paragraph + targeted greps (operating margin, capex, Gallatin, cost savings,
# free cash flow, price). Outcomes from later calls and SEC XBRL (operating income / revenue, capex, buybacks re-derived).
# Simpson guides GAAP consolidated operating margin as a range (no sales or EPS guidance), plus capex and tax rate.
TICKER = "US-SSD"
SCREENER = "https://data.sec.gov/api/xbrl/companyfacts/CIK0000920371.json"
F = "https://www.fool.com/earnings/call-transcripts/"
CALLS = {
    "2025-07-28": ("Q2-2025 earnings call transcript (Motley Fool)", F + "2025/08/07/simpson-ssd-q2-2025-earnings-call-transcript/"),
    "2025-10-27": ("Q3-2025 earnings call transcript (Motley Fool)", F + "2025/10/28/simpson-mfg-ssd-q3-2025-earnings-call-transcript/"),
    "2026-02-09": ("Q4-2025 earnings call transcript (Motley Fool)", F + "2026/02/09/simpson-ssd-q4-2025-earnings-call-transcript/"),
    "2026-04-27": ("Q1-2026 earnings call transcript (Motley Fool)", F + "2026/04/27/simpson-ssd-q1-2026-earnings-call-transcript/"),
    "2026-07-27": ("Q2-2026 results press release (8-K Ex 99.1; no transcript found)", "https://www.sec.gov/Archives/edgar/data/920371/000162828026049817/q22026ex991pressrelease.htm"),
    "2026-10-26": ("Q3-2026 earnings call transcript (Motley Fool)", F + "2026/10/26/simpson-manufacturing-ssd-q3-2026-earnings-call-transcript/"),
}
MO = "Michael Olosky (CEO)"
MD = "Matt Dunn (CFO)"
P = []
def add(**k):
    k.setdefault("status", "pending"); P.append(k)

# ---- Q2-2025 (28-Jul-2025)
add(said_on="2025-07-28", slug="fy25-op-margin-18-5-20-5", speaker=MD, category="margin",
    title="FY2025 consolidated operating margin 18.5%-20.5% (incl. $12-13 mn Gallatin property gain)",
    quote="We continue to expect our operating margin to be in the range of 18.5% to 20.5% [Fool text split at the decimal; range from the Fool summary]",
    metric="GAAP consolidated operating margin FY2025", target="18.5% to 20.5%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="XBRL OperatingIncomeLoss 458.1 / revenue 2,330 = 19.66% (re-derived); company 19.6%.", delivered_value="19.7%", delivery_ratio=1.0, confidence="verified")
add(said_on="2025-07-28", slug="fy25-capex-140-160mn", speaker=MD, category="capex",
    title="FY2025 capex $140-160 mn (reduced), incl. $70-75 mn for Columbus and Gallatin",
    quote="we are reducing our capital expenditures outlook to be in the range of $140 million to $160 million, which includes approximately $70 million to $75 million for the completion of both the Columbus facility expansion and the new Gallatin fastener facility.",
    metric="capex FY2025", target="$140-160 mn", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=2,
    status="partly", evidence="XBRL PaymentsToAcquirePropertyPlantAndEquipment FY2025 $161.0 mn: 0.6% above the top of the range (ceiling-style overshoot <=5%: clarification B -> partly).", delivered_value="$161.0 mn", delivery_ratio=0.99, confidence="verified",
    later_restatements="2025-10-27 $150-160 mn")
add(said_on="2025-07-28", slug="gallatin-fully-operational-ye25", speaker=MO, category="capacity_commissioning",
    title="New Gallatin, Tennessee fastener plant fully operational by end-2025",
    quote="Our Gallatin, Tennessee facility is scheduled to open in 2025 and is expected to become fully operational by the end of this year.",
    metric="Gallatin plant status", target="fully operational by 31-Dec-2025", deadline="2025-12-31", deadline_precision="year-end",
    specificity="precise", volunteered=True, materiality=2,
    status="partly", evidence="Opened in Q3-2025 ('our new Gallatin, Tennessee facility opened during the third quarter', Oct-2025) but still ramping in Q1-2026: 'start-up costs from the ongoing ramp of our Gallatin facility that opened late last year' (~100 bp gross-margin headwind).", delivery_ratio=0.6, explanation_for_miss="normal start-up ramp", admitted_unprompted=True)
add(said_on="2025-07-28", slug="fy25-return-35pct-fcf", speaker=MD, category="capital_return",
    title="Return at least 35% of 2025 free cash flow to shareholders",
    quote="We also remain committed to returning at least 35% of our free cash flow to stockholders",
    metric="(dividends + buybacks) / FCF FY2025", target=">=35%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=1,
    status="delivered", evidence="XBRL: dividends 47.6 + buybacks 120.0 = 167.6 vs FCF 458.7 - 161.0 = 297.6 -> 56% (re-derived).", delivered_value="56%", delivery_ratio=1.6, confidence="verified")
# ---- Q3-2025 (27-Oct-2025)
add(said_on="2025-10-27", slug="fy25-op-margin-19-20", speaker=MD, category="margin",
    title="FY2025 operating margin 19%-20% (incl. $12.9 mn property gain, $9-12 mn severance)",
    quote="[Fool summary] 2025 Operating Margin Guidance -- Updated to a range of 19%-20%",
    metric="GAAP consolidated operating margin FY2025", target="19.0% to 20.0%", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    status="delivered", evidence="FY2025 19.66% (XBRL re-derived).", delivered_value="19.7%", delivery_ratio=1.0, confidence="verified")
add(said_on="2025-10-27", slug="fy25-capex-150-160mn", speaker=MD, category="capex",
    title="FY2025 capex $150-160 mn",
    quote="our capital expenditures outlook is expected to be in the range of $150 million to $160 million",
    metric="capex FY2025", target="$150-160 mn", deadline="2025-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    status="partly", evidence="FY2025 capex $161.0 mn (XBRL): 0.6% above the top of a one-quarter-ahead range.", delivered_value="$161.0 mn", delivery_ratio=0.99, confidence="verified")
add(said_on="2025-10-27", slug="cost-savings-30mn-2026", speaker=MO, category="cost_savings",
    title="Strategic cost programme: at least $30 mn annualised savings, realised in 2026",
    quote="As a result of these actions, we expect to generate annualized cost savings of at least $30 million with one-time charges of approximately $9 million to $12 million that will be realized in fiscal 2025.",
    metric="annualised cost savings (company)", target=">=$30 mn in 2026", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="precise", volunteered=True, materiality=2,
    later_restatements="2026-02-09 'the full $30 million should show up in 2026' (Oct-25 Q&A) / opex to fall $10-15 mn net of FX; Q3-2026 opex 23.6% of sales vs 25.8%, SG&A headcount -6%")
add(said_on="2025-10-27", slug="price-actions-100mn-annualised", speaker=MD, category="price_cost",
    title="June + October 2025 price increases worth ~$100 mn of annualised sales",
    quote="[Fool summary] Pricing Actions -- June and October increases are expected to contribute a combined $100 million in annualized sales",
    metric="annualised sales from 2025 price actions", target="~$100 mn", deadline="2026-06-30", deadline_precision="half-year",
    specificity="precise", volunteered=True, materiality=2,
    status="delivered", evidence="Q1-2026 call: '2025 Price Increases -- Now expected to contribute approximately $130 million in annualized net sales, up from $100 million' (European surcharges, mix); Q1-2026 price +6%.", delivered_value="~$130 mn", delivery_ratio=1.3)
# ---- Q4-2025 (09-Feb-2026)
add(said_on="2026-02-09", slug="fy26-op-margin-19-5-20-5", speaker=MD, category="margin",
    title="FY2026 consolidated operating margin 19.5%-20.5% (incl. $10-12 mn asset-sale gain, $3-5 mn footprint costs)",
    quote="[Fool summary] 2026 guidance -- Consolidated operating margin expected between 19.5% and 20.5%",
    metric="GAAP consolidated operating margin FY2026", target="19.5% to 20.5%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3,
    later_restatements="2026-04-27 reiterated; 2026-07-27 19.7-20.5% (press release); 2026-10-26 20.0-20.5% incl. ~$11 mn Q4 land-sale gain")
add(said_on="2026-02-09", slug="fy26-capex-75-85mn", speaker=MD, category="capex",
    title="FY2026 capex $75-85 mn",
    quote="[Fool summary] Capital expenditures (2026 outlook) -- $75 million-$85 million projected.",
    metric="capex FY2026", target="$75-85 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1,
    later_restatements="2026-07-27 raised to $80-90 mn (press release); 2026-10-26 $80-90 mn")
add(said_on="2026-02-09", slug="fy26-opex-down-10-15mn", speaker=MD, category="cost_savings",
    title="FY2026 operating expenses $10-15 mn lower than 2025 (net of ~$5 mn adverse FX)",
    quote="So even with that, kinda down 10 to 15,000,000, which if you think about it, we size that $30 million cost savings up",
    metric="total operating expenses FY2026 vs FY2025 ($627 mn)", target="-$10 to -15 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=False, materiality=2)
add(said_on="2026-02-09", slug="fy26-housing-starts-assumption", speaker=MO, category="other",
    title="Outlook assumes US housing starts down low single digits in 2026 (assumption, not a promise; logged for context)",
    quote="[Fool summary] U.S. housing starts expected down low single digits",
    metric="US housing starts 2026 (external)", target="-1% to -3%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="vague", volunteered=True, materiality=1, status="unverifiable",
    evidence="External market assumption, not a management commitment; excluded from scoring.")
# ---- Q3-2026 (26-Oct-2026)
add(said_on="2026-10-26", slug="fy26-op-margin-20-0-20-5", speaker=MD, category="margin",
    title="FY2026 operating margin 20.0%-20.5% (incl. ~$11 mn Q4 land-sale gain)",
    quote="[Fool summary] Full Year Operating Margin Guidance -- 20.0% to 20.5%, including an anticipated $11 million gain from the sale of vacant land in the fourth quarter.",
    metric="GAAP consolidated operating margin FY2026", target="20.0% to 20.5%", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=3)
add(said_on="2026-10-26", slug="fy26-capex-80-90mn", speaker=MD, category="capex",
    title="FY2026 capex $80-90 mn",
    quote="[Fool summary] Full Year CapEx Guidance -- $80 million to $90 million, focused on footprint optimization and operational efficiency.",
    metric="capex FY2026", target="$80-90 mn", deadline="2026-12-31", deadline_precision="fiscal-year",
    specificity="range", volunteered=True, materiality=1)

ANALYSIS_TITLE = "US-SSD - Management Credibility Score (US industrials peer calibration, Nov 2026)"
ANALYSIS_BODY = ("Simpson Manufacturing (6 calls Q2-2025..Q3-2026; Q2-2026 from the 8-K press release): {n_promises} promises logged, {n_scored} scored. "
                 "Weighted delivery {weighted_delivery_ratio_pct}% (specificity-weighted {specificity_weighted_delivery_ratio_pct}%), MCS {mcs_schema_scale}. "
                 "Simpson guides only a wide GAAP operating-margin band (2 pts wide), capex and tax rate - easy to hit: FY2025 19.7% inside 18.5-20.5% and 19-20%. "
                 "Near misses are capex (FY2025 $161 mn vs $150-160 mn) and the Gallatin plant (opened on time, still ramping in Q1-2026). FY2026 margin band, capex and the $30 mn cost programme pending. Research, not advice.")
