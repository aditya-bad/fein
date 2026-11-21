# Paper calls — batch 1 (made 2026-11-21)

Forward, dated, probabilistic predictions about measurable events, used to **test methods** (lessons L11, L15).
They are **not recommendations** — no call says or implies buy/sell. Each is scored with Brier score against
a naive base-rate forecaster when it resolves (Jan–Jun 2027). Seed file: `memdb/seeds/2026-11-21_paper_calls_batch1.json`.

Context noted across Q2 FY27 / Q3 CY26 calls (Oct–Nov 2026): RBI in a tightening cycle (repo hiked to 5.5%, more hikes
expected), El Niño/drought stress in parts of India, high crude and 'exceptional' input-cost inflation, West Asia supply-chain
disruption, transmission-line delays for renewables. These shape several sector-cycle calls.

Margin convention for India calls: unless the rule says 'company-reported', margins are computed as Operating Profit ÷ Sales
from screener.in's quarterly table (consolidated unless marked standalone), to one decimal.

**Count:** 35 calls — india: 20, us: 15. By method: promise-tracker: 12, sector-cycle: 6, base-rate: 6, mgmt-tone: 6, flags-judgment: 3, valuation-temperature: 2.

## Summary table

| # | Market | Ticker | Call (event) | Method | P(ours) | P(base) | Resolve by |
|---|---|---|---|---|---|---|---|
| 1 | india | BAJFINANCE | Bajaj Finance consolidated AUM growth YoY at 31-Mar-2027 is ≥26.0% | promise-tracker | 0.60 | 0.55 | 2027-05-15 |
| 2 | india | AUBANK | AU Small Finance Bank FY27 credit cost (excl. CGFMU premium) is ≤0.90% | sector-cycle | 0.72 | 0.80 | 2027-05-15 |
| 3 | india | INFY | Infosys raises the midpoint of its FY27 constant-currency revenue guidance above 1.5% at Q3 FY27 results | base-rate | 0.55 | 0.70 | 2027-01-31 |
| 4 | india | HCLTECH | HCLTech FY27 company-level constant-currency revenue growth is ≥3.25% (midpoint of its 2.5–4% guide) | promise-tracker | 0.62 | 0.50 | 2027-04-30 |
| 5 | india | LUPIN | Lupin Q3 FY27 company-reported EBITDA margin (ex-forex & other income) is ≥24.0% | mgmt-tone | 0.35 | 0.60 | 2027-02-28 |
| 6 | india | LAURUSLABS | Laurus Labs Q3 FY27 consolidated operating margin is ≥30.0% | promise-tracker | 0.80 | 0.75 | 2027-02-28 |
| 7 | india | TVSMOTOR | TVS Motor total sales volume for Jan–Mar 2027 grows ≥15% YoY | sector-cycle | 0.45 | 0.55 | 2027-04-15 |
| 8 | india | SONACOMS | Sona BLW (Sona Comstar) Q3 FY27 consolidated operating margin is ≥23.0% | mgmt-tone | 0.42 | 0.50 | 2027-02-28 |
| 9 | india | NAVINFLUOR | Navin Fluorine confirms the Chemours (advanced-cooling) project was commissioned by 31-Dec-2026 | promise-tracker | 0.45 | 0.60 | 2027-02-28 |
| 10 | india | HINDUNILVR | Hindustan Unilever Q3 FY27 consolidated operating margin is ≥22.0% (inside its 22–24% guided band) | sector-cycle | 0.70 | 0.85 | 2027-02-28 |
| 11 | india | ASIANPAINT | Asian Paints Q3 FY27 standalone operating margin is ≥20.0% | sector-cycle | 0.45 | 0.55 | 2027-02-28 |
| 12 | india | HONASA | Honasa Consumer Q3 FY27 consolidated operating margin is ≥12.0% | mgmt-tone | 0.68 | 0.60 | 2027-02-28 |
| 13 | india | TATAPOWER | Tata Power reports ≥2.5 GW of renewable capacity added (commissioned) in FY27 | sector-cycle | 0.30 | 0.40 | 2027-05-31 |
| 14 | india | NTPC | NTPC group adds ≥4.8 GW of renewable capacity (commercial operation) in FY27 | promise-tracker | 0.30 | 0.40 | 2027-05-31 |
| 15 | india | MARICO | Marico FY27 consolidated EBITDA grows ≥24% YoY | promise-tracker | 0.68 | 0.55 | 2027-05-31 |
| 16 | india | TRANSRAILL | Transrail Lighting FY27 order intake is ≥₹10,000 cr | promise-tracker | 0.38 | 0.50 | 2027-05-31 |
| 17 | india | IOLCP | IOL Chemicals & Pharmaceuticals FY27 consolidated operating margin is ≥14.0% | base-rate | 0.58 | 0.50 | 2027-05-31 |
| 18 | india | CUMMINSIND | Cummins India Q3 FY27 standalone operating margin recovers to ≥17.0% | sector-cycle | 0.38 | 0.45 | 2027-02-28 |
| 19 | india | INDOTECH | Indo Tech Transformers' promoter pledge (as % of total shares) is lower in the Mar-2027 disclosure than the 57.93% reported for Sep-2026 | flags-judgment | 0.20 | 0.30 | 2027-04-30 |
| 20 | india | GENUSPOWER | Genus Power's share price return from 20-Nov-2026 to 30-Jun-2027 beats the Nifty 50's price return | valuation-temperature | 0.52 | 0.45 | 2027-06-30 |
| 21 | us | NVDA | NVIDIA Q4 FY27 revenue is ≥$133.9B (above the top of its $130.0B ±3% guide) | flags-judgment | 0.72 | 0.85 | 2027-03-10 |
| 22 | us | AMD | AMD Q4 2026 revenue is ≥$17.51B (above the top of its ~$17B ±3% guide) | base-rate | 0.38 | 0.35 | 2027-02-20 |
| 23 | us | PLTR | Palantir's share price return from 20-Nov-2026 to 30-Jun-2027 beats SPY's price return | valuation-temperature | 0.42 | 0.47 | 2027-06-30 |
| 24 | us | AAPL | Apple announces a new share-repurchase authorization of ≥$100B with its fiscal Q2 2027 results | base-rate | 0.75 | 0.60 | 2027-05-31 |
| 25 | us | GE | GE Aerospace FY2026 adjusted EPS is ≥$8.10 (top of its raised $8.00–8.10 guide) | promise-tracker | 0.62 | 0.40 | 2027-02-15 |
| 26 | us | CAT | Caterpillar announces a quarterly dividend increase of ≥7% (to ≥$1.75) by 30-Jun-2027 | base-rate | 0.72 | 0.75 | 2027-06-30 |
| 27 | us | AAON | AAON FY2026 net sales growth is ≥72% (low end of its raised 72–75% outlook) | flags-judgment | 0.72 | 0.80 | 2027-03-15 |
| 28 | us | WMT | Walmart FY27 adjusted EPS is ≥$2.89 (top of its $2.84–2.89 guide) | promise-tracker | 0.58 | 0.35 | 2027-03-01 |
| 29 | us | TGT | Target Q4 2026 comparable sales growth is ≥+3.0% | base-rate | 0.62 | 0.55 | 2027-03-15 |
| 30 | us | FIVE | Five Below FY2026 comparable sales growth is ≥+11.0% (midpoint of its 10–12% outlook) | promise-tracker | 0.58 | 0.50 | 2027-03-31 |
| 31 | us | ULTA | Ulta Beauty FY2026 diluted EPS is ≥$29.00 (top of its August outlook) | mgmt-tone | 0.52 | 0.45 | 2027-03-31 |
| 32 | us | DECK | Deckers FY27 diluted EPS is ≥$7.95 (top of its $7.80–7.95 guide) | promise-tracker | 0.52 | 0.40 | 2027-06-05 |
| 33 | us | UNH | UnitedHealth's initial 2027 adjusted EPS outlook has a low end/floor ≥$22.50 | mgmt-tone | 0.42 | 0.50 | 2027-01-31 |
| 34 | us | ISRG | Intuitive Surgical reports FY2026 worldwide da Vinci procedure growth of ≥14.5% | promise-tracker | 0.45 | 0.50 | 2027-01-31 |
| 35 | us | HIMS | Hims & Hers Q4 2026 adjusted EBITDA is ≥$80M (midpoint of its $70–90M guide) | mgmt-tone | 0.40 | 0.50 | 2027-03-10 |

## Evidence and resolution rules

### 1. BAJFINANCE — Bajaj Finance consolidated AUM growth YoY at 31-Mar-2027 is ≥26.0%
- **id:** `thesis:paper-call:BAJFINANCE:fy27-aum-growth-26pct-plus`
- **Method:** promise-tracker credibility · **P(ours)** 0.60 · **P(base)** 0.55 · resolve by 2027-05-15
- **Evidence:** Q2 FY27 call (19-Oct-2026): AUM +26.5% YoY to ₹5,84,624 cr; net AUM add ~₹38k cr/qtr for two quarters. CEO Rajeev Jain: 'probably between 26%, 27% growth we should deliver now on a full year basis'; medium-term guide stays 20–25%. Headwinds named: RBI hikes ('baking in two more increases… 6% kind of rates'), NIM compression slightly worse than the 10–15 bps guide, gold-loan short-tenor schemes stopped, El Niño (monsoon 87% LPA). Track record: FY25 guide 26–27%, delivered ~26%.
- **Why our number differs from base:** BFL has a long record of hitting AUM guidance, and the guide was given with H1 already at 26.5%; but 26% is the bottom of the range and rate hikes plus rural stress lean against H2 acceleration. Slightly above base.
- **Base-rate reasoning:** A large lender restating a full-year growth range at H1 with H1 at/above the range bottom meets the range bottom roughly 55% of the time (range bottoms are often missed by tenths).
- **Resolution rule:** YES if consolidated AUM at 31-Mar-2027 ÷ consolidated AUM at 31-Mar-2026 − 1 ≥ 26.0% (both as stated in BFL's Q4 FY27 results press release/investor deck; use BFL's own reported YoY if it states one).
- **Resolution source:** Bajaj Finance Q4 FY27 results press release / investor presentation (NSE announcements)
- **Sources used:** https://nsearchives.nseindia.in/corporate/BAJFINANCE_23102026145254_BFL_Investor_Call_outcome_Transcript_for_filing.pdf

### 2. AUBANK — AU Small Finance Bank FY27 credit cost (excl. CGFMU premium) is ≤0.90%
- **id:** `thesis:paper-call:AUBANK:fy27-credit-cost-within-90bps`
- **Method:** sector cycle/lead indicator · **P(ours)** 0.72 · **P(base)** 0.80 · resolve by 2027-05-15
- **Evidence:** Q2 FY27 call (24-Oct-2026): H1 credit cost ~73–74 bps (81 bps incl. CGFMU premium) vs guidance 'close to 90 bps'. Loans +25% YoY, deposits +29%. MD Sanjay Agarwal: drought/high oil 'vulnerabilities', 'let's see how quarter three behaves because whatever will be there will come in quarter three'. MPC hiked repo 25 bps to 5.5% with stance 'calibrated tightening'. 99% of MFI book under CGFMU.
- **Why our number differs from base:** 16 bps of cushion is decent, but the cycle indicators (rate hikes, El Niño drought in Central India, high fuel) all point to rising small-borrower stress in H2; management itself flags Q3. Shade below base.
- **Base-rate reasoning:** Full-year credit-cost guidance with H1 comfortably inside is met ~80% of the time for Indian banks outside crisis years.
- **Resolution rule:** YES if AU's FY27 credit cost on the same basis as the guidance (management states ~90 bps excl. CGFMU premium; H1 was 73–74 bps) is ≤0.90%, as stated in the Q4 FY27 presentation or call. If only the incl.-CGFMU figure is given, YES requires it ≤0.97% (guide + H1 premium gap ~7 bps).
- **Resolution source:** AU SFB Q4 FY27 investor presentation / earnings call transcript
- **Sources used:** https://nsearchives.nseindia.in/corporate/SUMIT1_28102026192812_Investor_call_transcript_SE_Submission.pdf

### 3. INFY — Infosys raises the midpoint of its FY27 constant-currency revenue guidance above 1.5% at Q3 FY27 results
- **id:** `thesis:paper-call:INFY:q3fy27-guidance-midpoint-raised`
- **Method:** base rate · **P(ours)** 0.55 · **P(base)** 0.70 · resolve by 2027-01-31
- **Evidence:** Q2 FY27 (Oct-2026): FY27 cc guidance cut from 1.5–3% to 1–2%; op-margin guide 20–22% kept (Q2 ~21%). Q2 cc growth +1.5% YoY, +1.2% QoQ; H1 +1.9% cc. Mgmt cites soft volumes, pricing pressure/AI deflation, weak Retail/Hi-Tech, rate rises; large deals TCV $8.8 bn. Infosys history at Q3: midpoint raised in FY23, FY25 and FY26, unchanged (narrowed) in FY24.
- **Why our number differs from base:** H1 at 1.9% means the 1–2% band already embeds a weak H2; Q3 has furloughs, and they just cut. A narrow-upward revision (e.g., 1.5–2%) is plausible but so is a hold. Below the historical base because this year's direction of revision was down.
- **Base-rate reasoning:** Infosys raised the guidance midpoint at Q3 in ~3 of the last 4 years.
- **Resolution rule:** YES if the FY27 cc revenue guidance announced with Q3 FY27 results has a midpoint strictly greater than 1.5% (e.g., 1.5–2.0% or 1.75–2.25%). Hold at 1–2% or any cut = NO.
- **Resolution source:** Infosys Q3 FY27 press release / fact sheet (infosys.com, NSE)
- **Sources used:** https://nsearchives.nseindia.in/corporate/Infosys_28102026173824_SE_filing_Earnings_call_transcript.pdf

### 4. HCLTECH — HCLTech FY27 company-level constant-currency revenue growth is ≥3.25% (midpoint of its 2.5–4% guide)
- **id:** `thesis:paper-call:HCLTECH:fy27-cc-growth-above-midpoint`
- **Method:** promise-tracker credibility · **P(ours)** 0.62 · **P(base)** 0.50 · resolve by 2027-04-30
- **Evidence:** Q2 FY27 call (13/15-Oct-2026): FY27 company guide 2.5–4% cc (incl. 87 bps inorganic), Services 3–4% (62 bps inorganic); top end trimmed to narrow the band; EBIT 17.5–18.5%. CEO: 'For Services, we feel confident to be slightly above the midpoint'; mega-deal adds no revenue until Q1 FY28; 3 of top-20 clients ramping down already 'factored in'. Q3 is 'our strongest quarter'. History: FY25 guided 3.5–5%, delivered ~4.7% (upper half).
- **Why our number differs from base:** HCL guides conservatively and has usually landed in the upper half; mgmt explicitly says above-midpoint for Services. Acquisitions add mechanical growth. Risk: software-products seasonality and client ramp-downs.
- **Base-rate reasoning:** Coin-flip for landing above a guidance midpoint absent a track record.
- **Resolution rule:** YES if HCLTech's reported FY27 company revenue growth in constant currency (Q4 FY27 press release) is ≥3.25%.
- **Resolution source:** HCLTech Q4 FY27 results press release / investor release
- **Sources used:** https://nsearchives.nseindia.in/corporate/HCLTECH_15102026223802_Transcript.pdf

### 5. LUPIN — Lupin Q3 FY27 company-reported EBITDA margin (ex-forex & other income) is ≥24.0%
- **id:** `thesis:paper-call:LUPIN:q3fy27-ebitda-margin-24pct-plus`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.35 · **P(base)** 0.60 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (Nov-2026): Q2 EBITDA ex-forex/other income ₹1,957 cr, margin 25.1% vs 31.3% a year ago; FY27 margin guide 'around 24–25%' with CEO Vinita Gupta saying margins 'likely to moderate in the coming quarters' (US competition in key products, R&D ~8% of sales, input costs). Screener OPM path: Mar-26 33%, Jun-26 30%, Sep-26 26%. US revenue guide $1.1–1.2 bn.
- **Why our number differs from base:** Management is telling us, unusually explicitly, that margins fall from 25.1%; a full-year 24–25% with H1 ~27–28% implies H2 nearer 21–23%. We weight management's downbeat tone over persistence.
- **Base-rate reasoning:** Naive persistence: a quarter's margin stays within ~1 pt of the prior quarter about 60% of the time.
- **Resolution rule:** YES if the EBITDA margin excluding forex and other income for Q3 FY27, as stated in Lupin's Q3 press release/call, is ≥24.0%. If not stated, compute (EBITDA − other income − forex gain) ÷ revenue from operations from the results.
- **Resolution source:** Lupin Q3 FY27 results press release / earnings call transcript
- **Sources used:** https://nsearchives.nseindia.in/corporate/Lupin2_06112026203743_SE_Intimation_of_Investor_Meet_Transcript.pdf; https://www.screener.in/company/LUPIN/consolidated/

### 6. LAURUSLABS — Laurus Labs Q3 FY27 consolidated operating margin is ≥30.0%
- **id:** `thesis:paper-call:LAURUSLABS:q3fy27-opm-30pct-plus`
- **Method:** promise-tracker credibility · **P(ours)** 0.80 · **P(base)** 0.75 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (29-Oct-2026): EBITDA margin ~34%, highest ever; +₹200 cr revenue QoQ (operating leverage), CDMO ~40% of mix. Founder Dr Chava: 'comfortable in maintaining over 60% gross margin and over 30% EBITDA… we still stick to our guidance.' Screener OPM: Dec-25 27%, Mar-26 28%, Jun-26 32%, Sep-26 34%; sales growth +29%/+33% YoY in Q1/Q2. Capex guide ₹3,000 cr over FY27–28; H1 run-rate below that.
- **Why our number differs from base:** Guide is a floor with 4 pts of headroom and a rising trend; CDMO lumpiness is the main risk. Slightly above persistence base.
- **Base-rate reasoning:** A margin 4 pts above a threshold stays above it next quarter ~75% of the time for mid-cap pharma/CDMO.
- **Resolution rule:** YES if Q3 FY27 (Dec-2026 quarter) consolidated Operating Profit ÷ Sales on screener.in is ≥30.0% (company-reported EBITDA margin used if screener unavailable).
- **Resolution source:** screener.in Laurus Labs consolidated quarterly results; Laurus Q3 FY27 press release
- **Sources used:** https://nsearchives.nseindia.in/corporate/LAURUSLABS_03112026113343_Transcript03112026.pdf; https://www.screener.in/company/LAURUSLABS/consolidated/

### 7. TVSMOTOR — TVS Motor total sales volume for Jan–Mar 2027 grows ≥15% YoY
- **id:** `thesis:paper-call:TVSMOTOR:q4fy27-volume-growth-15pct-plus`
- **Method:** sector cycle/lead indicator · **P(ours)** 0.45 · **P(base)** 0.55 · resolve by 2027-04-15
- **Evidence:** Q2 FY27 call (Nov-2026): Q2 volume 1.9 mn vs 1.5 mn (+27%); revenue +44%; domestic ICE 2W +16% vs industry +10%; 2W exports +33%; EV 2W +129%; 3W +47%. Management: 'You will see much higher growth from TVS in quarter 3 and quarter 4.' Macro: repo hikes, El Niño rural stress, high fuel prices; Jan–Mar 2026 base is elevated by the post-GST-cut demand surge.
- **Why our number differs from base:** Share gains and exports are real, but the base quarter (Jan–Mar 2026) was strong and the rate/rural cycle is turning against two-wheelers. Lean slightly below base.
- **Base-rate reasoning:** For a company growing ~25% in the latest quarter, the chance of ≥15% two quarters later is ~55% (growth mean-reverts).
- **Resolution rule:** YES if the sum of TVS Motor's reported total sales (2W + 3W, domestic + exports, incl. EV) for Jan, Feb and Mar 2027 ÷ the same sum for Jan–Mar 2026 − 1 ≥ 15.0%, per TVS monthly sales press releases.
- **Resolution source:** TVS Motor monthly sales press releases (NSE announcements), Jan–Mar 2027
- **Sources used:** https://nsearchives.nseindia.in/corporate/TVSMOTOR_04112026174008_NSEBSEInvestorcalltranscript.pdf

### 8. SONACOMS — Sona BLW (Sona Comstar) Q3 FY27 consolidated operating margin is ≥23.0%
- **id:** `thesis:paper-call:SONACOMS:q3fy27-opm-23pct-plus`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.42 · **P(base)** 0.50 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (Oct-2026): EBITDA margin 23%, down 2.3 pts YoY; H1 EBITDA +34% to ₹659 cr. Mgmt keeps 23–25% range ('I do not see any reason to change that range') while describing 'exceptional inflation… In my career, I've not seen inflation like this'; mix shift to lower-margin motor controllers. Screener OPM: Sep-25 25%, Dec-25 25%, Mar-26 24%, Jun-26 23%, Sep-26 23%; sales +52%/+35% YoY.
- **Why our number differs from base:** Two quarters sit exactly at the range floor with a down-drift, rising low-margin mix and self-described extreme inflation. Reassurance without a mechanism ('ghee shakkar') = tone test; we lean below the floor.
- **Base-rate reasoning:** Coin-flip on whether a margin at a threshold stays at/above it next quarter.
- **Resolution rule:** YES if Q3 FY27 consolidated Operating Profit ÷ Sales on screener.in ≥23.0% (company-reported EBITDA margin used if screener unavailable).
- **Resolution source:** screener.in Sona BLW consolidated quarterly results; company Q3 FY27 press release
- **Sources used:** https://nsearchives.nseindia.in/corporate/SONACOMS_31102026183421_Intimation.pdf; https://www.screener.in/company/SONACOMS/consolidated/

### 9. NAVINFLUOR — Navin Fluorine confirms the Chemours (advanced-cooling) project was commissioned by 31-Dec-2026
- **id:** `thesis:paper-call:NAVINFLUOR:chemours-plant-commissioned-q3fy27`
- **Method:** promise-tracker credibility · **P(ours)** 0.45 · **P(base)** 0.60 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (30-Oct-2026): 'The Chemours project… is also progressing towards commissioning in Q3 FY27.' Analyst notes 'we've seen some delay'; MD Anish Ganatra calls the delay 'a conscious choice' over process route. Other promises in the same call: R32/HFC expansion 'on track for commissioning shortly'; cGMP-4 Phase 2 (~₹125 cr) operational by end Q4 FY27; MPP debottleneck commissioned Sep-2026 (a kept promise).
- **Why our number differs from base:** Promise-tracker prior: a project that has already slipped once has a materially higher chance of slipping again, even when the remaining window is short; partner-dependent qualification adds risk. Navin's other recent near-term promises were kept, which keeps us from going lower.
- **Base-rate reasoning:** Indian chemical capex promised for the very next quarter is commissioned on time roughly 60% of the time.
- **Resolution rule:** YES if a Navin filing, press release, investor presentation or the Q3 FY27 earnings call states that the Chemours/advanced-cooling (two-phase immersion fluid) plant was commissioned (mechanically complete and started production) on or before 31-Dec-2026. 'Commissioning in Q4'/'in January' = NO.
- **Resolution source:** Navin Fluorine Q3 FY27 results presentation / earnings call transcript / NSE announcements
- **Sources used:** https://nsearchives.nseindia.in/corporate/NAVINFLUOR_06112026142511_NFILIntimationofTranscriptofEarningsCallQ2FY27.pdf

### 10. HINDUNILVR — Hindustan Unilever Q3 FY27 consolidated operating margin is ≥22.0% (inside its 22–24% guided band)
- **id:** `thesis:paper-call:HINDUNILVR:q3fy27-opm-22pct-plus`
- **Method:** sector cycle/lead indicator · **P(ours)** 0.70 · **P(base)** 0.85 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (Oct/Nov-2026): USG 15%, UVG 7% (price increases taken); EBITDA margin 22.6%, 'well within our guided range'; 'Commodity inflation is expected to remain elevated. We expect medium-term EBITDA Margin to be within the current guided range of 22% to 24%.' Screener OPM: Mar-25 24%, Sep-25 24%, Dec-25 23%, Mar-26 23%, Jun-26 23%, Sep-26 22% — steady downward drift.
- **Why our number differs from base:** Cushion is only ~0.6 pt and the cost cycle (crude, palm, inflation) is adverse; HUL protects margins with price but with a lag. Shade below the 'always in band' base.
- **Base-rate reasoning:** HUL's quarterly EBITDA margin has stayed ≥22% in essentially every quarter of the last ~3 years (~85%).
- **Resolution rule:** YES if HUL's Q3 FY27 (Dec-2026 quarter) consolidated EBITDA margin as reported by the company is ≥22.0%; cross-check with screener Operating Profit ÷ Sales (if they differ, the company-reported figure governs).
- **Resolution source:** HUL Q3 FY27 results press release; screener.in consolidated quarterly
- **Sources used:** https://nsearchives.nseindia.in/corporate/HINDUNILVR_04112026193825_SEIntimationTranscriptofEarningsCallSigned.pdf; https://www.screener.in/company/HINDUNILVR/consolidated/

### 11. ASIANPAINT — Asian Paints Q3 FY27 standalone operating margin is ≥20.0%
- **id:** `thesis:paper-call:ASIANPAINT:q3fy27-standalone-opm-20pct-plus`
- **Method:** sector cycle/lead indicator · **P(ours)** 0.45 · **P(base)** 0.55 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (Nov-2026): Q2 'a little bit of a soft quarter' on mix; H1 PBDIT margin 19.6% ('higher range of the overall band'); H1 volume ~8%, value ~16% (price increases). MD Amit Syngle: for the year 'we should be able to maintain the band… 18% to 20%' via price calibration, cost-excellence programme and VAE in-house intermediates. Screener standalone OPM: Sep-25 18%, Dec-25 21%, Mar-26 21%, Jun-26 22%, Sep-26 17%.
- **Why our number differs from base:** Q3 is seasonally the strongest margin quarter and price hikes are flowing, but input inflation is the highest in years and the full-year band (18–20%) with H1 at 19.6% implies H2 near 19%. 20%+ in Q3 needs a strong mix.
- **Base-rate reasoning:** Seasonality base: Asian Paints' Dec quarter standalone OPM has been ≥20% in roughly half to 60% of recent years.
- **Resolution rule:** YES if Q3 FY27 standalone Operating Profit ÷ Sales from screener.in (standalone view) ≥20.0%; company-reported standalone PBDIT margin used as tiebreak if screener is unavailable.
- **Resolution source:** screener.in Asian Paints standalone quarterly; company Q3 FY27 press release
- **Sources used:** https://nsearchives.nseindia.in/corporate/ASIANPAINT_03112026182217_Stock_exchange_intimation_Transcript_Q2FY26.pdf; https://www.screener.in/company/ASIANPAINT/

### 12. HONASA — Honasa Consumer Q3 FY27 consolidated operating margin is ≥12.0%
- **id:** `thesis:paper-call:HONASA:q3fy27-opm-12pct-plus`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.68 · **P(base)** 0.60 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (6-Nov-2026): net sales +36%, UVG 31.3%, EBITDA margin 12.7%; H1 ~13.5% incl. a Q1 one-off. CEO Varun Alagh on raising the 150–200 bps improvement guidance: 'I have not seen any benefits of being too aggressive. Conservative probably the better place to be'; for H2 'confident of being able to hold our current trajectory… around 12.5'. Festive A&P accelerated in Q3. Screener OPM: Dec-25 11%, Mar-26 12%, Jun-26 15%, Sep-26 13%. (Company had an FY25 distributor-inventory correction — see company:HONASA.)
- **Why our number differs from base:** After the FY25 credibility hit, management now under-promises; the ~12.5% H2 guide with Q2 at 12.7% and operating leverage at +30% volume growth gives cushion even with festive A&P.
- **Base-rate reasoning:** Persistence: a margin ~0.7 pt above a threshold stays above it next quarter ~60% for a young consumer brand with volatile A&P.
- **Resolution rule:** YES if Q3 FY27 consolidated Operating Profit ÷ Sales on screener.in ≥12.0% (company-reported EBITDA margin used if screener unavailable).
- **Resolution source:** screener.in Honasa consolidated quarterly; Honasa Q3 FY27 results presentation
- **Sources used:** https://nsearchives.nseindia.in/corporate/HONASA16_10112026170619_Transcript_s.pdf; https://www.screener.in/company/HONASA/consolidated/

### 13. TATAPOWER — Tata Power reports ≥2.5 GW of renewable capacity added (commissioned) in FY27
- **id:** `thesis:paper-call:TATAPOWER:fy27-capacity-addition-2-5gw`
- **Method:** sector cycle/lead indicator · **P(ours)** 0.30 · **P(base)** 0.40 · resolve by 2027-05-31
- **Evidence:** Q2 FY27 call (11-Nov-2026): CEO Praveer Sinha: 'we have missed the targets in first and second quarter, but many of the projects are now ready. The evacuation lines which were delayed, we are expecting some of them to come by December or January… this year target is 2.5 GW of capacity addition, and we will be able to meet that.' NTPC's call the same month also cites transmission (evacuation) delays leaving ~1.5 GW stranded (sector-wide lead indicator).
- **Why our number differs from base:** Lead indicator: transmission/evacuation delays are sector-wide and outside the developer's control; H1 shortfall means H2 must carry most of 2.5 GW. Promise reaffirmation after two misses is weak evidence.
- **Base-rate reasoning:** Indian RE developers meet annual commissioning targets after a behind-plan H1 roughly 40% of the time.
- **Resolution rule:** YES if Tata Power's Q4 FY27 results presentation/press release states renewable (utility-scale + group captive, as Tata Power itself counts it) capacity commissioned/added during FY27 ≥2.5 GW (2,500 MW). Rooftop/distributed solar excluded unless Tata Power includes it in the same 2.5 GW target definition.
- **Resolution source:** Tata Power Q4 FY27 investor presentation / press release
- **Sources used:** https://nsearchives.nseindia.in/corporate/KSTPCL_17112026152929_Q2_FY27_Earning_Call_Transcript.pdf; https://nsearchives.nseindia.in/corporate/9425178051_06112026150753_6__Disclosure_for_Transcript_of_Earnings_Conference_Call_Q2_FY27_Signed.pdf

### 14. NTPC — NTPC group adds ≥4.8 GW of renewable capacity (commercial operation) in FY27
- **id:** `thesis:paper-call:NTPC:fy27-re-addition-4-8gw`
- **Method:** promise-tracker credibility · **P(ours)** 0.30 · **P(base)** 0.40 · resolve by 2027-05-31
- **Evidence:** Q2 FY27 call (31-Oct-2026): began FY27 'with an estimation of close to 8 gigawatt'; ~1,300 MW RE added by end-October; 'another 3.5 gigawatt is something which would be able to do'; ~1,615 MW built but 'covered under… the delay in the transmission'. Group installed capacity 91,506 MW at H1; H1 group addition 2,398 MW (NGEL 1,136 MW). Power demand +15% in H1 FY27.
- **Why our number differs from base:** The revised target (1.3 + 3.5 = 4.8 GW) has already been cut 40% from 8 GW; PSU RE targets are routinely back-ended and missed, and the transmission bottleneck persists. The cut does reduce the bar, keeping us near 0.3 rather than lower.
- **Base-rate reasoning:** Large Indian developers hit a mid-year-revised capacity target roughly 40% of the time.
- **Resolution rule:** YES if NTPC (group, incl. NGEL and JVs as NTPC reports it) states RE (solar + wind) capacity added/declared commercial in FY27 ≥4,800 MW in its Q4 FY27 results presentation/call or NGEL's Q4 FY27 disclosures (operational RE capacity 31-Mar-2027 minus 31-Mar-2026).
- **Resolution source:** NTPC & NGEL Q4 FY27 investor presentations / earnings calls
- **Sources used:** https://nsearchives.nseindia.in/corporate/9425178051_06112026150753_6__Disclosure_for_Transcript_of_Earnings_Conference_Call_Q2_FY27_Signed.pdf

### 15. MARICO — Marico FY27 consolidated EBITDA grows ≥24% YoY
- **id:** `thesis:paper-call:MARICO:fy27-ebitda-growth-24pct-plus`
- **Method:** promise-tracker credibility · **P(ours)** 0.68 · **P(base)** 0.55 · resolve by 2027-05-31
- **Evidence:** Q2 FY27 call (Nov-2026): revenue +13%, India volume +10%, international +13% cc; EBITDA +27%, margin +200 bps to 18.2%. Guidance raised (second upgrade): 'mid-twenties EBITDA growth up from around 20%'; CFO: 'mid-20s about in the range of 24%, 25% on the minimum side'; revenue 'teens' growth, crossing ₹15,000 cr; margin +120–150 bps for the year. Company notes teens+ revenue growth in 8 of last 10 quarters.
- **Why our number differs from base:** Marico has upgraded twice and frames 24–25% as a minimum, with H1 above it (EBITDA +27% in Q2). Copra/input deflation tailwind and operating leverage support it; risk is A&P reinvestment in H2.
- **Base-rate reasoning:** A raised full-year guide with H1 above the new bar is delivered ~55–60% of the time for FMCG (H2 re-investment often trims it).
- **Resolution rule:** YES if Marico's consolidated EBITDA for FY27 ÷ FY26 − 1 ≥ 24.0%, using the company's reported EBITDA (Q4 FY27 information update/press release); else screener Operating Profit FY27 vs FY26.
- **Resolution source:** Marico Q4 FY27 information update / press release; screener.in annual P&L
- **Sources used:** https://nsearchives.nseindia.in/corporate/marico_06112026165447_SEtranscript.pdf

### 16. TRANSRAILL — Transrail Lighting FY27 order intake is ≥₹10,000 cr
- **id:** `thesis:paper-call:TRANSRAILL:fy27-order-intake-10000cr`
- **Method:** promise-tracker credibility · **P(ours)** 0.38 · **P(base)** 0.50 · resolve by 2027-05-31
- **Evidence:** Q2 FY27 call (Nov-2026): order book ₹14,218 cr at 30-Sep-2026, plus ₹1,747 cr declared after quarter-end; MD Randeep Narang: 'confident to achieve an annual order intake of INR10,000-plus crores'; 'Already INR3,500 crores, INR4,000 crores in the bag'; ₹18,000 cr already bid + ~₹30,000 cr more to bid in 5 months at a 10–12% historical win ratio. 'Since listing, we have not missed any of our revenue or margin guidance' (revenue Q2 ₹2,056 cr, +32%; EBITDA margin 11.6%).
- **Why our number differs from base:** Arithmetic check: ₹48,000 cr of bids × 10–12% ≈ ₹4,800–5,800 cr more wins → ₹8,300–9,800 cr total, i.e., the target needs above-normal win rates. The clean record is on revenue/margin, not order intake (more lumpy). Lean below base.
- **Base-rate reasoning:** Indian EPC order-intake guidance with ~40% done at H1 is met roughly half the time.
- **Resolution rule:** YES if Transrail reports FY27 order intake/inflow (incl. L1 converted to orders within FY27, as the company counts it) ≥₹10,000 cr in its Q4 FY27 presentation, press release or call.
- **Resolution source:** Transrail Q4 FY27 investor presentation / earnings call transcript
- **Sources used:** https://nsearchives.nseindia.in/corporate/TRANSRAIL_11112026120533_EarningcallTranscriptUFRSept2026.pdf

### 17. IOLCP — IOL Chemicals & Pharmaceuticals FY27 consolidated operating margin is ≥14.0%
- **id:** `thesis:paper-call:IOLCP:fy27-opm-14pct-plus`
- **Method:** base rate · **P(ours)** 0.58 · **P(base)** 0.50 · resolve by 2027-05-31
- **Evidence:** Q2 FY27 call (2-Nov-2026): Q2 revenue ₹795 cr (+~40% YoY), EBITDA ~₹115 cr, margin 14.4%; H1 revenue ₹1,551 cr (+39%), EBITDA ₹227 cr, margin 14.5%. Mgmt: FY27 '25% plus revenue growth with 14% to 15% of EBITDA'; 'Q3 and Q4… perhaps we should have the same performance'; ethyl acetate/acetic anhydride at full utilisation with better prices; other expenses up on power/fuel and freight (hopes to pass on). Screener OPM: Dec-25 10%, Mar-26 15%, Jun-26 14%, Sep-26 14%. Ibuprofen expansion FY28.
- **Why our number differs from base:** Commodity-chemical margins mean-revert; the recent step-up from ~10% to ~14–15% came with favourable spreads (cycle-dependent). H1 at 14.5% means H2 only needs ~13.5%, so modestly above a coin-flip.
- **Base-rate reasoning:** For a commodity-linked small cap whose margin just jumped ~4 pts, the chance it holds within ~0.5 pt for the full year is roughly half.
- **Resolution rule:** YES if FY27 consolidated Operating Profit ÷ Sales on screener.in's annual P&L ≥14.0% (if screener is unavailable, EBITDA excl. other income ÷ revenue from operations from the Q4 FY27 results).
- **Resolution source:** screener.in IOLCP annual P&L; IOLCP Q4 FY27 results
- **Sources used:** https://nsearchives.nseindia.in/corporate/IOLCP_05112026173447_Intimation.pdf; https://www.screener.in/company/IOLCP/consolidated/

### 18. CUMMINSIND — Cummins India Q3 FY27 standalone operating margin recovers to ≥17.0%
- **id:** `thesis:paper-call:CUMMINSIND:q3fy27-opm-17pct-plus`
- **Method:** sector cycle/lead indicator · **P(ours)** 0.38 · **P(base)** 0.45 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (16-Nov-2026): gross margin down ~400 bps on raw-material inflation and mix; management declined to say margins have bottomed ('refrained from giving a guidance on gross margins bottoming out'); data-centre gensets remain the growth driver, exports marginally down. Screener standalone: OPM Mar-25 21%, Jun-25 21%, Sep-25 22%, Dec-25 21%, Mar-26 21%, Jun-26 18%, Sep-26 15%; Sep-26 sales ₹3,301 cr (+4% YoY), operating profit ₹506 cr.
- **Why our number differs from base:** Input-cost inflation is broad (Sona, HUL, Asian Paints all flag it) and price increases lag; a 2-pt rebound in one quarter needs pricing plus mix help. We lean toward a slow recovery.
- **Base-rate reasoning:** Mean-reversion base: after a sharp 2-quarter margin fall, a quality industrial recovers ≥2 pts next quarter roughly 45% of the time.
- **Resolution rule:** YES if Q3 FY27 (Dec-2026) standalone Operating Profit ÷ Sales on screener.in (standalone view) ≥17.0%.
- **Resolution source:** screener.in Cummins India standalone quarterly; company Q3 FY27 results
- **Sources used:** https://nsearchives.nseindia.in/corporate/CUMMINSIND_20112026163131_SEIntimationTranscriptQ2Final.pdf; https://www.screener.in/company/CUMMINSIND/

### 19. INDOTECH — Indo Tech Transformers' promoter pledge (as % of total shares) is lower in the Mar-2027 disclosure than the 57.93% reported for Sep-2026
- **id:** `thesis:paper-call:INDOTECH:promoter-pledge-reduced-by-mar27`
- **Method:** flags-judgment context · **P(ours)** 0.20 · **P(base)** 0.30 · resolve by 2027-04-30
- **Evidence:** NSE pledge data (broadcast 20-Nov-2026, SHP 30-Sep-2026): promoter holding 70.29% of 1.062 cr shares; 82.41% of promoter shares encumbered = 57.93% of total. Pledges/encumbrances in favour of trustees (Catalyst Trusteeship, SBICAP Trustee) on behalf of the promoter Shirdi Sai Electricals (SSEL)'s lenders since Oct–Nov 2025; SSEL sold shares on the open market on 29–30 Jun 2026. memdb event:INDOTECH:avoid-2026-11-19 flags this as a red flag.
- **Why our number differs from base:** The encumbrance secures the promoter group's own borrowings (not a margin loan), which tends to persist until the group refinances; open-market sales by the promoter suggest liquidity need, not release. Flags-judgment: this flag has a verifiable mechanism (lender security), so we expect it to stay.
- **Base-rate reasoning:** Indian promoter pledges above 50% of total equity are reduced within ~6 months roughly 30% of the time.
- **Resolution rule:** YES if the NSE pledge/encumbrance disclosure for the 31-Mar-2027 shareholding pattern shows promoter shares pledged/encumbered as % of total shares < 57.93% (a fall caused only by the promoter selling pledged shares still counts as YES; any increase or no change = NO).
- **Resolution source:** NSE corporate pledge data (tools/nse_fetch.py pledge INDOTECH), SHP for quarter ended 31-Mar-2027
- **Sources used:** https://www.nseindia.com/companies-listing/corporate-filings-pledged-data (via tools/nse_fetch.py pledge INDOTECH, 20-Nov-2026); https://www.nseindia.com/companies-listing/corporate-filings-sast-regulations (via tools/nse_fetch.py sast INDOTECH)

### 20. GENUSPOWER — Genus Power's share price return from 20-Nov-2026 to 30-Jun-2027 beats the Nifty 50's price return
- **id:** `thesis:paper-call:GENUSPOWER:cold-valuation-beats-nifty-to-jun27`
- **Method:** valuation-temperature · **P(ours)** 0.52 · **P(base)** 0.45 · resolve by 2027-06-30
- **Evidence:** screener.in 20-Nov-2026: price ₹266, P/E 11.9 vs its own 5-yr median P/E 38.3 (≈0.3× own median — 'cold'); ROCE 25.3%, ROE 30.9%; 52-wk range ₹207–359. Known flags (memdb event:GENUSPOWER:avoid-2026-11-19): CFO negative 3 years (smart-meter AMISP model), borrowings ~₹2,482 cr, FII 18.7%→7.4%. Nifty 50 close 20-Nov-2026: 25,800.6 (Yahoo ^NSEI).
- **Why our number differs from base:** Valuation-temperature test of the cold end: a stock at ~0.3× its own median multiple with high reported ROE. Lesson L12 cuts both ways — cheap can stay cheap when cash conversion is poor, so we are only mildly above base.
- **Base-rate reasoning:** A single Indian small cap beats the Nifty 50 over a ~7-month window roughly 45% of the time (return skew: the median small cap lags the index).
- **Resolution rule:** YES if (Genus close on NSE 30-Jun-2027 ÷ 266.0) > (Nifty 50 close 30-Jun-2027 ÷ 25,800.6). Use the last trading day ≤30-Jun-2027; adjust Genus for any split/bonus; dividends ignored for both.
- **Resolution source:** NSE/Yahoo Finance closes (GENUSPOWER.NS, ^NSEI); screener.in price
- **Sources used:** https://www.screener.in/company/GENUSPOWER/consolidated/; https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI

### 21. NVDA — NVIDIA Q4 FY27 revenue is ≥$133.9B (above the top of its $130.0B ±3% guide)
- **id:** `thesis:paper-call:US-NVDA:q4fy27-revenue-above-top-of-guide`
- **Method:** flags-judgment context · **P(ours)** 0.72 · **P(base)** 0.85 · resolve by 2027-03-10
- **Evidence:** 8-K 17-Nov-2026 (Q3 FY27): revenue $115.8B (+20% QoQ, +103% YoY) vs Q3 guide $108.0B ±2% (top $110.2B) — beat the top by ~5%. Q4 guide (14-week quarter) $130.0B ±3%, gross margin 71–72% (Q3 74.8%), no China DC compute assumed. Governance flags: 8-K 12-Nov-2026 (Item 5.02) — Board accepted Jen-Hsun Huang's resignation as CEO and director effective 11-Nov-2026; CFO Colette Kress interim CEO; Harvey Jones named Chair; Q3 release references an ongoing independent board-committee investigation and pending Hugging Face acquisition. $150B buyback increase (Sep-2026).
- **Why our number differs from base:** Flags-judgment test: does a severe governance shock change near-term delivery when demand and supply are already contracted? We think mostly not, but the range was widened to ±3% (vs ±2%) and margins are guided down, so we shade below NVDA's own beat history.
- **Base-rate reasoning:** NVIDIA's revenue exceeded the top of its own guidance range in essentially every quarter of the last ~3 years (Q3 FY27 included), ~85–90%.
- **Resolution rule:** YES if NVIDIA's reported Q4 FY27 total revenue (8-K Item 2.02 earnings release) ≥ $133.9B.
- **Resolution source:** NVIDIA Q4 FY27 earnings 8-K (SEC EDGAR, CIK 1045810)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/1045810/000104581026000088/nvda-20261117.htm; https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm; https://www.sec.gov/Archives/edgar/data/1045810/000104581026000073/nvda-20260826.htm

### 22. AMD — AMD Q4 2026 revenue is ≥$17.51B (above the top of its ~$17B ±3% guide)
- **id:** `thesis:paper-call:US-AMD:q4-2026-revenue-above-top-of-guide`
- **Method:** base rate · **P(ours)** 0.38 · **P(base)** 0.35 · resolve by 2027-02-20
- **Evidence:** 8-K 3-Nov-2026: Q3 2026 revenue record $13.4B (+45% YoY), 'exceeding the high end of our guidance'; Data Center nearly doubled. Q4 guide ~$17B ±3% (midpoint +66% YoY, +27% QoQ), non-GAAP GM ~55%. SEC XBRL quarterly revenue: $10.25B, $11.54B, $13.38B (Q1–Q3 2026).
- **Why our number differs from base:** A +27% sequential guide already embeds a big MI-series ramp; beating the top needs supply upside on top of that. AMD's beat-the-top frequency is lower than NVIDIA's.
- **Base-rate reasoning:** Large-cap semis beat the top of their own quarterly revenue range roughly a third of the time.
- **Resolution rule:** YES if AMD's reported Q4 2026 revenue (8-K earnings release) ≥ $17.51B.
- **Resolution source:** AMD Q4 2026 earnings 8-K (SEC EDGAR, CIK 2488)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/2488/000000248826000188/q32026991.htm

### 23. PLTR — Palantir's share price return from 20-Nov-2026 to 30-Jun-2027 beats SPY's price return
- **id:** `thesis:paper-call:US-PLTR:hot-valuation-beats-spy-to-jun27`
- **Method:** valuation-temperature · **P(ours)** 0.42 · **P(base)** 0.47 · resolve by 2027-06-30
- **Evidence:** Yahoo close 20-Nov-2026: PLTR $143.49 (52-wk $106.37–212.94), SPY $689.81 (fell 3.6% that day). SEC XBRL: TTM diluted EPS ≈ $1.43 (Q4-25 0.24 derived as FY25 0.63 − 9M 0.39; Q1–Q3 26: 0.34/0.41/0.44) → P/E ≈100×; TTM revenue ≈ $7.30B vs market cap ≈ $346B (2.41B shares) → ≈47× sales; Q3-26 revenue $2.31B, +96% YoY.
- **Why our number differs from base:** Valuation-temperature test at the hot end: ~100× earnings and ~47× sales leave little room for any growth deceleration, but momentum and +96% growth can carry a hot stock for months. We lean modestly toward underperformance.
- **Base-rate reasoning:** A single S&P 500 stock beats the index over ~7 months a bit under half the time (~47%).
- **Resolution rule:** YES if (PLTR close 30-Jun-2027 ÷ 143.49) > (SPY close 30-Jun-2027 ÷ 689.81); last trading day ≤30-Jun-2027; split-adjust; dividends ignored.
- **Resolution source:** Yahoo Finance / Nasdaq closes for PLTR and SPY
- **Sources used:** https://query1.finance.yahoo.com/v8/finance/chart/PLTR; https://query1.finance.yahoo.com/v8/finance/chart/SPY; https://data.sec.gov/api/xbrl/companyfacts/CIK0001321655.json

### 24. AAPL — Apple announces a new share-repurchase authorization of ≥$100B with its fiscal Q2 2027 results
- **id:** `thesis:paper-call:US-AAPL:buyback-authorization-100bn-may27`
- **Method:** base rate · **P(ours)** 0.75 · **P(base)** 0.60 · resolve by 2027-05-31
- **Evidence:** 8-K 30-Apr-2026: dividend raised 4% to $0.27; 'additional program to repurchase up to $100 billion'. Q4 FY26 8-K (2-Nov-2026): $0.27 dividend declared. Annual May authorizations (from memory, partly unverified): 2022 $90B, 2023 $90B, 2024 $110B, 2025 $100B, 2026 $100B.
- **Why our number differs from base:** Apple has set ≥$100B for three straight years and still generates >$100B FCF; a cut would signal a capital shift (AI capex/M&A) that we see no evidence for yet.
- **Base-rate reasoning:** In 3 of the last 5 years the May authorization was ≥$100B (60%).
- **Resolution rule:** YES if Apple's fiscal Q2 2027 earnings release (or another announcement on or before 31-May-2027) authorizes a new/additional repurchase program of ≥$100B.
- **Resolution source:** Apple Q2 FY27 earnings 8-K (SEC EDGAR, CIK 320193)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/320193/000032019326000011/aapl-20260430.htm; https://www.sec.gov/Archives/edgar/data/320193/000032019326000024/aapl-20261102.htm

### 25. GE — GE Aerospace FY2026 adjusted EPS is ≥$8.10 (top of its raised $8.00–8.10 guide)
- **id:** `thesis:paper-call:US-GE:fy2026-adj-eps-above-8-10`
- **Method:** promise-tracker credibility · **P(ours)** 0.62 · **P(base)** 0.40 · resolve by 2027-02-15
- **Evidence:** 8-K 20-Oct-2026 (Q3 2026): orders +49%, revenue +18%, EPS +36%; guidance raised 'across the board': adjusted revenue growth ~19–20% (prior high-teens), operating profit $10.9–11.0B (prior $10.55–10.75B), adjusted EPS $8.00–8.10 (prior $7.65–7.85), FCF $9.1–9.4B. 2025 adjusted EPS was $6.37 (vs a final 2025 guide that, from memory, topped out near $6.20 — unverified).
- **Why our number differs from base:** Culp-era GE has habitually guided conservatively and finished above range; the narrow 10-cent band after a big raise still leaves room for a Q4 beat given 49% order growth.
- **Base-rate reasoning:** A large industrial finishes at or above the top of its final-quarter EPS range ~40% of the time.
- **Resolution rule:** YES if GE Aerospace's reported FY2026 adjusted EPS (Q4 2026 earnings release, non-GAAP as defined by the company) ≥ $8.10.
- **Resolution source:** GE Aerospace Q4 2026 earnings 8-K (SEC EDGAR, CIK 40545)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/40545/000004054526000063/ge3q2026earningsrelease.htm

### 26. CAT — Caterpillar announces a quarterly dividend increase of ≥7% (to ≥$1.75) by 30-Jun-2027
- **id:** `thesis:paper-call:US-CAT:dividend-raise-7pct-by-jun27`
- **Method:** base rate · **P(ours)** 0.72 · **P(base)** 0.75 · resolve by 2027-06-30
- **Evidence:** 8-K 11-Jun-2026: Board raised quarterly dividend by 12 cents (+8%) to $1.63, 'maintains our place on the S&P 500 Dividend Aristocrats Index'. Prior June raises (from memory): 2023 +8%, 2024 +8%, 2025 +7%. Q3 2026 8-K: $1.2B buybacks + $0.7B dividends in the quarter; enterprise cash $7.9B; operating cash flow $4.4B.
- **Why our number differs from base:** Pattern is very stable and cash generation strong; the main risk is a smaller raise if the machinery cycle softens (rate hikes globally).
- **Base-rate reasoning:** Persistence: 4 of 4 recent June raises were ≥7%; generic aristocrat repeat-size base ~75%.
- **Resolution rule:** YES if, on or before 30-Jun-2027, Caterpillar declares a regular quarterly dividend ≥ $1.745 per share (rounded: ≥$1.75).
- **Resolution source:** Caterpillar dividend 8-K / press release (SEC EDGAR, CIK 18230)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/18230/000110465926072929/tm2617177d1_8k.htm; https://www.sec.gov/Archives/edgar/data/18230/000001823026000052/0000018230-26-000052-index.htm

### 27. AAON — AAON FY2026 net sales growth is ≥72% (low end of its raised 72–75% outlook)
- **id:** `thesis:paper-call:US-AAON:fy2026-sales-growth-72pct-plus`
- **Method:** flags-judgment context · **P(ours)** 0.72 · **P(base)** 0.80 · resolve by 2027-03-15
- **Evidence:** 8-K 9-Nov-2026: Q3 net sales +84.1% to record $707.4M; BASX (data-centre) +218%; AAON-branded +19.6%; backlog +40.5% YoY to $1.9B but −5.9% QoQ. Outlook raised to 72–75% growth (prior 55–60%), GM ~26%. Same release: restated Q1 and Q2 2026 (H1 net sales +$10.7M, GM +71 bps, EPS +$0.09) and disclosed a material weakness in ICFR; 'no evidence of fraud'.
- **Why our number differs from base:** Flags-judgment: a restatement plus material weakness is a classic warning, but here the restatement raised prior numbers and the guide needs only Q4. The QoQ backlog decline and revenue-recognition-control questions keep us below the 'only one quarter left' base.
- **Base-rate reasoning:** Companies meet the low end of a full-year sales outlook raised with only one quarter left ~80% of the time.
- **Resolution rule:** YES if AAON's FY2026 reported net sales ÷ FY2025 net sales − 1 ≥ 72.0% (per the Q4/FY2026 earnings release or 10-K; use the company's stated growth figure if given).
- **Resolution source:** AAON Q4 2026 earnings 8-K / FY2026 10-K (SEC EDGAR, CIK 824142)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/824142/000082414226000083/liveaaonpressreleaseexs.htm

### 28. WMT — Walmart FY27 adjusted EPS is ≥$2.89 (top of its $2.84–2.89 guide)
- **id:** `thesis:paper-call:US-WMT:fy27-adj-eps-at-or-above-2-89`
- **Method:** promise-tracker credibility · **P(ours)** 0.58 · **P(base)** 0.35 · resolve by 2027-03-01
- **Evidence:** Q3 FY27 earnings presentation (19-Nov-2026): FY27 adjusted EPS guide raised for the third time — $2.75–2.85 (Feb) → $2.80–2.87 (Aug) → $2.84–2.89 (Nov); net sales cc +4.9–5.2%; adjusted operating income cc +8.0–8.6%. Q3 adj EPS $0.65 (+4.8%); FY26 adjusted EPS base $2.64 (which, from memory, was above the top of its own final FY26 range of $2.58–2.63).
- **Why our number differs from base:** Walmart has a recent habit of finishing at or above the top of its final guide, and has raised three times this year; holiday trends and tariff-refund noise are the risks.
- **Base-rate reasoning:** S&P 500 companies finish at or above the top of their final-quarter annual EPS range ~35% of the time.
- **Resolution rule:** YES if Walmart's reported FY27 adjusted EPS (Q4 FY27 earnings release) ≥ $2.89.
- **Resolution source:** Walmart Q4 FY27 earnings 8-K (SEC EDGAR, CIK 104169)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/104169/000010416926000168/earningspresentationfy27.htm

### 29. TGT — Target Q4 2026 comparable sales growth is ≥+3.0%
- **id:** `thesis:paper-call:US-TGT:q4-2026-comps-3pct-plus`
- **Method:** base rate · **P(ours)** 0.62 · **P(base)** 0.55 · resolve by 2027-03-15
- **Evidence:** 8-K 18-Nov-2026 (Q3 2026): net sales +7.1%, comparable sales +5.6% (traffic +5.0%; stores +4.6%, digital +9.8%); November month-to-date 'in line with the Company's guidance… accelerating from October'. FY2026 guide raised: net sales growth ~6% (+1 pt), operating margin ~6.2% incl. ~1.1 pt tariff-refund benefit, EPS $10.65–11.40. Q4 2025 is an easy compare (Target's comps were negative through 2025).
- **Why our number differs from base:** Traffic-led comps and an easy compare favour ≥3%; risks are a weaker holiday consumer (rate hikes, inflation) and the 53rd/calendar shift noise.
- **Base-rate reasoning:** A retailer comping +5–6% with traffic leading sustains ≥3% the next quarter roughly 55% of the time.
- **Resolution rule:** YES if Target's reported Q4 2026 comparable sales change (Q4 earnings release) ≥ +3.0%.
- **Resolution source:** Target Q4 2026 earnings 8-K (SEC EDGAR, CIK 27419)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/27419/000002741926000051/a2026q3ex-99.htm

### 30. FIVE — Five Below FY2026 comparable sales growth is ≥+11.0% (midpoint of its 10–12% outlook)
- **id:** `thesis:paper-call:US-FIVE:fy2026-comps-11pct-plus`
- **Method:** promise-tracker credibility · **P(ours)** 0.58 · **P(base)** 0.50 · resolve by 2027-03-31
- **Evidence:** 8-K 2-Sep-2026 (Q2 FY26): net sales +22.9% to $1.26B, comps +14.1%; double-digit comps for five straight quarters; FY26 comps outlook raised to +10–12% (prior +6–8%), net sales $5.63–5.71B (prior $5.40–5.48B), Q3 comps guide +8–10%; outlook excludes future tariff refunds and buybacks. Q3 results due early Dec-2026 (before resolution).
- **Why our number differs from base:** The guide implies a sharp H2 deceleration from a +14% Q2; management has beaten and raised, which usually signals conservative H2 assumptions.
- **Base-rate reasoning:** Coin-flip for landing above a guidance midpoint absent track record (~50%).
- **Resolution rule:** YES if Five Below's reported FY2026 (year ending ~Jan-2027) comparable sales increase (Q4 FY26 earnings release) ≥ +11.0%.
- **Resolution source:** Five Below Q4 FY2026 earnings 8-K (SEC EDGAR, CIK 1177609)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/1177609/000117760926000023/q22026fivebelowexhibit991.htm

### 31. ULTA — Ulta Beauty FY2026 diluted EPS is ≥$29.00 (top of its August outlook)
- **id:** `thesis:paper-call:US-ULTA:fy2026-eps-at-or-above-29`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.52 · **P(base)** 0.45 · resolve by 2027-03-31
- **Evidence:** 8-K 27-Aug-2026 (Q2 FY26): net sales +8.9% to $3.0B (incl. Space NK acquisition), comps +3.8%; FY26 outlook raised — net sales growth 6.7–7.2% (prior 6–7%), comps 3.2–3.7% (prior 2.5–3.5%), operating income growth 8.3–9.3%, EPS $28.70–29.00 (prior $28.36–28.80); buyback plan raised to $1.8B (from $1.5B). CEO: 'confidence in our strategic priorities… in a dynamic environment.' Q3 results due early Dec-2026.
- **Why our number differs from base:** Confident tone plus bigger buyback supports EPS; the 30-cent band is narrow and the consumer backdrop is softening. Slightly above base.
- **Base-rate reasoning:** Retailers finish at/above the top of an August full-year EPS range ~45% of the time.
- **Resolution rule:** YES if Ulta's reported FY2026 diluted EPS (Q4 FY26 earnings release) ≥ $29.00.
- **Resolution source:** Ulta Beauty Q4 FY2026 earnings 8-K (SEC EDGAR, CIK 1403568)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/1403568/000110465926102438/ulta-20260827xex99d1.htm

### 32. DECK — Deckers FY27 diluted EPS is ≥$7.95 (top of its $7.80–7.95 guide)
- **id:** `thesis:paper-call:US-DECK:fy27-eps-at-or-above-7-95`
- **Method:** promise-tracker credibility · **P(ours)** 0.52 · **P(base)** 0.40 · resolve by 2027-06-05
- **Evidence:** 8-K 22-Oct-2026 (Q2 FY27): record revenue $1.48B; EPS $2.31 (+27%) incl. $0.28 IEEPA tariff-refund benefit; gross margin 60.5% (56.2%). FY27 guide raised: net sales $5.700–5.725B, GM ~58.5%, op margin ~23%, EPS $7.80–7.95 incl. ~$0.52 refund benefit; assumes $1.0B buyback. CEO Stefano Caroti: 'a challenging consumer environment… taking deliberate' actions in H2.
- **Why our number differs from base:** Deckers has a reputation for conservative guidance (track record not yet coded in promise tracker), but the CEO's own words flag a tougher H2 and the range is narrow. Modestly above base.
- **Base-rate reasoning:** Consumer companies finish at/above the top of a mid-year EPS range ~40% of the time.
- **Resolution rule:** YES if Deckers' reported FY27 (ending 31-Mar-2027) diluted EPS (Q4 FY27 earnings release) ≥ $7.95, as reported (including tariff-refund effects).
- **Resolution source:** Deckers Q4 FY27 earnings 8-K (SEC EDGAR, CIK 910521)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/910521/000091052126000028/deckex991pressrelease-9302.htm

### 33. UNH — UnitedHealth's initial 2027 adjusted EPS outlook has a low end/floor ≥$22.50
- **id:** `thesis:paper-call:US-UNH:2027-initial-eps-guide-22-50`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.42 · **P(base)** 0.50 · resolve by 2027-01-31
- **Evidence:** 8-K 13-Oct-2026 (Q3 2026): revenue $112.7B; adjusted EPS $4.69; full-year 2026 outlook raised to net EPS 'at least $19.50' and adjusted EPS 'at least $20.50'; CEO cites 'discipline and execution'. Context: UNH opened 2026 with an 'at least' style floor well below where it now stands (post-2025 reset), i.e., deliberately conservative guidance.
- **Why our number differs from base:** Management-tone test: post-crisis UNH under-promises; an initial 2027 floor ≥$22.50 (≈+10% on the 2026 floor) would break that habit. Medicare Advantage cost trend and rate-hike macro add caution.
- **Base-rate reasoning:** Coin-flip on a threshold set near ~10% growth, roughly UNH's historical long-term EPS growth target low end (~50%).
- **Resolution rule:** YES if the 2027 adjusted EPS outlook first issued (expected with Q4 2026 results, Jan-2027) has a low end or 'at least' floor ≥ $22.50. If issued as a single point, use that point.
- **Resolution source:** UnitedHealth Q4 2026 earnings 8-K (SEC EDGAR, CIK 731766)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/731766/000073176626000255/earningsrelease3q26unh.htm

### 34. ISRG — Intuitive Surgical reports FY2026 worldwide da Vinci procedure growth of ≥14.5%
- **id:** `thesis:paper-call:US-ISRG:fy2026-procedure-growth-14-5-plus`
- **Method:** promise-tracker credibility · **P(ours)** 0.45 · **P(base)** 0.50 · resolve by 2027-01-31
- **Evidence:** 8-K 20-Oct-2026 (Q3 2026): da Vinci procedures +~14%, Ion +~31%; FY2026 outlook: procedure growth ~14–15%, 'The Company expects to be closer to the midpoint of this range'; non-GAAP GM 68.7–69.3% (incl. ~0.9 pt tariff hit); opex growth 11–13%.
- **Why our number differs from base:** Management explicitly steers to ~14.5%; with Q3 at ~14% the outcome hinges on Q4 and on ISRG's rounding ('approximately 14%' would resolve NO). Slight lean below coin-flip because of the rounding convention.
- **Base-rate reasoning:** Coin-flip on a midpoint the company itself points to (~50%).
- **Resolution rule:** YES if ISRG's reported FY2026 worldwide da Vinci procedure growth (Q4 2026 release or preliminary January announcement) is ≥14.5% as stated; 'approximately 14%' = NO, 'approximately 15%' or '14.5%' = YES.
- **Resolution source:** Intuitive Surgical Q4 2026 / preliminary FY2026 release (SEC EDGAR, CIK 1035267)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/1035267/000103526726000067/q326ex-991earningsrelease.htm

### 35. HIMS — Hims & Hers Q4 2026 adjusted EBITDA is ≥$80M (midpoint of its $70–90M guide)
- **id:** `thesis:paper-call:US-HIMS:q4-2026-adj-ebitda-80m-plus`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.40 · **P(base)** 0.50 · resolve by 2027-03-10
- **Evidence:** 8-K 9-Nov-2026 (Q3 2026): revenue +49% YoY (second straight quarter of acceleration). Guidance: Q4 revenue $875–895M, adjusted EBITDA $70–90M (8–10% margin); FY2026 revenue tightened to $3.13–3.15B and adjusted EBITDA reduced to $257–277M. CFO Yemi Okupe: 'deliberate strategic decisions to position… for durable, multi-year growth' (i.e., investment over margin).
- **Why our number differs from base:** A company that just cut its EBITDA guide while framing it as 'deliberate investment' tends to keep spending; the 20M-wide range invites a sub-midpoint print. Lean below coin-flip.
- **Base-rate reasoning:** Coin-flip for landing at/above a guidance midpoint (~50%).
- **Resolution rule:** YES if HIMS's reported Q4 2026 adjusted EBITDA (Q4 earnings release) ≥ $80.0M.
- **Resolution source:** Hims & Hers Q4 2026 earnings 8-K (SEC EDGAR, CIK 1773751)
- **Sources used:** https://www.sec.gov/Archives/edgar/data/1773751/000177375126000242/hims-20260930x8xkearningsr.htm

## Scoring protocol

On resolution: set `outcome` (1 if the stated event happened, else 0), `brier` = (p − outcome)², and also
compute the base-rate Brier (base − outcome)². Update the curriculum scoreboard. Write a post-mortem for every call
where |p − outcome| > 0.6. Ambiguous resolutions: decide strictly by the written rule; if the data source no longer
publishes the metric, mark `void` (not scored) and say why.
