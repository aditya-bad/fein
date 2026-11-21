# Paper calls — batch 2 (made 2026-11-21)

Forward, dated, probabilistic predictions about measurable events, used to **test methods** (lessons L11, L15).
They are **not recommendations** — no call says or implies buy/sell. Each is scored with Brier score against
a naive base-rate forecaster when it resolves (Jan–Jun 2027). Seed file: `memdb/seeds/2026-11-21_paper_calls_batch2.json`.
Companion to batch 1 (`research_notes/Paper calls/batch1.md`); no company or event from batch 1 or the 7 pilot calls is repeated.

Context noted across Q2 FY27 / Q3 CY26 calls and filings (Oct–Nov 2026): RBI tightening (repo hiked to 5.5%; banks
'expect repo up to 6%' with two more 25 bp hikes), West Asia conflict keeping oil, freight and input costs high (Brent
averaged ~$103 in Q4-to-date vs ~$91.5 in Jul–Sep; Yahoo BZ=F), US 10-year yield ~4.9–5.1% (Yahoo ^TNX), Indian cement/steel
prices firm, weak IT/high-tech demand narrative, a festive season (Diwali early Nov 2026) falling inside Q3 FY27.
Index levels for price-relative calls (20-Nov-2026 closes, Yahoo): Nifty 50 25,800.6; SPY $689.81.

Margin convention for India calls: unless the rule says 'company-reported', margins are computed as Operating Profit ÷ Sales
from screener.in's quarterly table (consolidated unless marked standalone), to one decimal.

Method balance target for batch 2 (user brief): at least 5 calls per method, and the methods batch 1 under-used
(flags-judgment, valuation-temperature) brought up to parity. New sectors vs batch 1: private bank, life and general
insurance, AMC, exchange, cement, steel, aluminium/copper, real estate, defence, EMS, telecom, card issuer, infra/EPC,
US money-centre and regional bank, net-lease REIT, utility, SaaS, consumer staples, energy, levered cable.

**Count:** 16 calls — india: 16, us: 0. By method: promise-tracker: 5, mgmt-tone: 4, sector-cycle: 3, base-rate: 3, valuation-temperature: 1.

## Summary table

| # | Market | Ticker | Call (event) | Method | P(ours) | P(base) | Resolve by |
|---|---|---|---|---|---|---|---|
| 1 | india | EICHERMOT | Eicher Motors Q3 FY27 consolidated operating margin is ≥24.0% | mgmt-tone | 0.42 | 0.60 | 2027-02-28 |
| 2 | india | DEEPAKNTR | Deepak Nitrite Q3 FY27 consolidated operating profit is ≥₹500 cr | sector-cycle | 0.55 | 0.45 | 2027-02-28 |
| 3 | india | ICICIBANK | ICICI Bank reports a higher net interest margin for Q4 FY27 than for Q3 FY27 | promise-tracker | 0.62 | 0.45 | 2027-05-15 |
| 4 | india | PERSISTENT | Persistent Systems announces completion (closing) of its Nagarro acquisition on or before 31-Mar-2027 | promise-tracker | 0.75 | 0.70 | 2027-04-15 |
| 5 | india | BAJAJCON | Bajaj Consumer Care FY27 consolidated revenue from operations grows ≥17.0% YoY ("high teens" guide) | promise-tracker | 0.52 | 0.55 | 2027-05-31 |
| 6 | india | HDFCLIFE | HDFC Life FY27 value of new business (VNB) grows ≥12.0% YoY | mgmt-tone | 0.52 | 0.45 | 2027-05-15 |
| 7 | india | HDFCAMC | HDFC AMC Q3 FY27 revenue from operations is ≥₹1,200 cr | base-rate | 0.60 | 0.65 | 2027-02-15 |
| 8 | india | BSE | BSE Ltd Q3 FY27 consolidated revenue from operations exceeds ₹1,566 cr (a new quarterly record) | sector-cycle | 0.60 | 0.45 | 2027-02-28 |
| 9 | india | ULTRACEMCO | UltraTech Cement Q3 FY27 consolidated operating profit is ≥₹4,500 cr | mgmt-tone | 0.45 | 0.50 | 2027-02-28 |
| 10 | india | TATASTEEL | Tata Steel announces a binding (definitive) agreement with the Dutch State/North Holland on the IJmuiden decarbonisation project by 31-Mar-2027 | base-rate | 0.20 | 0.30 | 2027-04-15 |
| 11 | india | GODREJPROP | Godrej Properties FY27 booking value is ≥₹40,000 cr | promise-tracker | 0.58 | 0.50 | 2027-04-30 |
| 12 | india | BEL | Bharat Electronics FY27 order inflow is ≥₹25,000 cr | promise-tracker | 0.66 | 0.60 | 2027-05-31 |
| 13 | india | DIXON | Dixon Technologies confirms that its Vivo JV began production/consolidation in Q4 FY27 (by 31-Mar-2027) | base-rate | 0.45 | 0.55 | 2027-06-15 |
| 14 | india | BHARTIARTL | Bharti Airtel announces a headline prepaid mobile tariff increase (≥10% on its core unlimited plans) by 30-Jun-2027 | sector-cycle | 0.35 | 0.30 | 2027-06-30 |
| 15 | india | TITAN | Titan's share price return from 20-Nov-2026 to 30-Jun-2027 beats the Nifty 50's price return | valuation-temperature | 0.45 | 0.48 | 2027-06-30 |
| 16 | india | POLYCAB | Polycab India Q3 FY27 consolidated operating margin is ≥13.0% | mgmt-tone | 0.72 | 0.70 | 2027-02-28 |

## Evidence and resolution rules

### 1. EICHERMOT — Eicher Motors Q3 FY27 consolidated operating margin is ≥24.0%
- **id:** `thesis:paper-call:EICHERMOT:q3fy27-opm-24pct-plus`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.42 · **P(base)** 0.60 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (13-Nov-2026): record revenue ₹7,422 cr (+20%), EBITDA ₹1,760 cr; Royal Enfield Q2 volume 376,722 (+15%), YTD Apr–Oct ~+18%, bookings +21% YTD, 'highest-ever monthly sales in September and October', channel stock below normal. Three price hikes in CY26; CEO Vidhya Srinivasan: 'we don't give forward-looking guidances… there is volatility'; MD Govindarajan: 'the range bound on the percentage is not what is driving us… absolute profit'; analyst notes 'other expenditure surge'. Screener OPM (OP÷Sales): Q3 FY26 25.5% (1,557/6,114), Q4 FY26 24.9%, Q1 FY27 24.0% (1,591/6,632), Q2 FY27 23.7% (1,760/7,422). Cheyyar module 1 started Q2 FY27 (capacity 1.65 mn), module 2 pulled into Q4 FY27.
- **Why our number differs from base:** Management repeatedly steered analysts away from margin percentage toward absolute profit while costs (steel, freight, marketing, new-plant ramp) rise — a tone we read as a soft warning. Two consecutive quarters at/below 24% and new capacity costs lean below the naive 'stays near recent levels' base.
- **Base-rate reasoning:** Persistence: in 7 of the last 9 quarters Eicher's screener OPM was ≥24.0%; naive forecaster ~60%.
- **Resolution rule:** YES if Eicher Motors' consolidated Operating Profit ÷ Sales for the quarter ended 31-Dec-2026, from screener.in's consolidated quarterly table (or recomputed as EBITDA ÷ revenue from operations from the results filing), is ≥24.0% (one decimal).
- **Resolution source:** Eicher Motors Q3 FY27 results (NSE filing) / screener.in consolidated quarterly table
- **Sources used:** https://nsearchives.nseindia.in/corporate/EICHERMOT_17112026181815_EMLTranscriptofConferencecallNov132026Signed.pdf; https://www.screener.in/company/EICHERMOT/consolidated/
- **Confidence of evidence:** verified

### 2. DEEPAKNTR — Deepak Nitrite Q3 FY27 consolidated operating profit is ≥₹500 cr
- **id:** `thesis:paper-call:DEEPAKNTR:q3fy27-op-500cr-plus`
- **Method:** sector cycle/lead indicator · **P(ours)** 0.55 · **P(base)** 0.45 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (30-Oct-2026): record revenue ₹3,091 cr (+61%), EBITDA ₹643 cr (+187%), margin ~21%; Phenolics revenue ₹2,291 cr, EBIT ₹515 cr, 'principal driver… disruptions to international supply chains, higher landed cost of imports' (West Asia); H1 Phenolics EBIT ₹933 cr already above best-ever full year (FY22 ₹867 cr). Advanced Intermediates EBIT fell to ₹49 cr (6%); CFO guided Q3 AI EBIT% 'between Q1 and Q2, closer to Q1', Q4 better. New DCTL chlorination/photohalogenation assets commissioned end-Q2. Screener OP: Q3 FY26 211, Q4 FY26 376, Q1 FY27 540, Q2 FY27 627 (₹ cr).
- **Why our number differs from base:** Lead indicator: phenol/acetone spreads are being held up by import disruption that was still in place into Q3 (Brent Q4-to-date ~$103 vs Q3 ~$91.5), while AI segment guidance points up and new assets add volume. A 20% fall from Q2 is needed to miss. We lean above the mean-reversion base.
- **Base-rate reasoning:** After a record spread-driven quarter, Indian commodity-chemical makers see a ≥20% sequential operating-profit fall roughly half the time or more; naive P(OP ≥ ₹500 cr) ~45%.
- **Resolution rule:** YES if Deepak Nitrite's consolidated Operating Profit (screener.in quarterly table; equivalently EBITDA excluding other income) for the quarter ended 31-Dec-2026 is ≥₹500 cr.
- **Resolution source:** Deepak Nitrite Q3 FY27 results (NSE) / screener.in consolidated quarterly table
- **Sources used:** https://nsearchives.nseindia.in/corporate/DEEPAKNTR_04112026111452_NSE-concall_transcript.pdf; https://www.screener.in/company/DEEPAKNTR/consolidated/; https://query1.finance.yahoo.com/v8/finance/chart/BZ%3DF
- **Confidence of evidence:** verified

### 3. ICICIBANK — ICICI Bank reports a higher net interest margin for Q4 FY27 than for Q3 FY27
- **id:** `thesis:paper-call:ICICIBANK:q4fy27-nim-above-q3fy27`
- **Method:** promise-tracker credibility · **P(ours)** 0.62 · **P(base)** 0.45 · resolve by 2027-05-15
- **Evidence:** Q2 FY27 call (Oct-2026): NIM 4.18% vs 4.36% in Q1 (4.28% ex tax-refund interest); drag from ~$18 bn FCNR(B) deposits under the RBI swap window and lower CASA (9–10 bp mix impact). CFO Sandeep Batra: 'The full impact would largely get reflected in the third quarter, after which we expect the margins to start moving up, even based on the current level of policy rates'; 'when repo repricing happens, there is a positive movement on the NIM… repo rates can go up to 6%… another two hikes'. Loans +30% YoY (24% ex FCNR-funded), deposits +27%, provisions ₹851 cr (0.2% of advances).
- **Why our number differs from base:** This is a dated, specific promise (margins trough in Q3, rise thereafter) from a bank whose margin guidance has generally been reliable, and the rate-hike cycle reprices ICICI's large repo-linked book faster than deposits. Risks: deposit repricing and FCNR deployment. Above base.
- **Base-rate reasoning:** Indian large private banks report a sequential NIM increase in roughly 45% of quarters (flat or down otherwise).
- **Resolution rule:** YES if the net interest margin ICICI Bank reports for Q4 FY27 (Jan–Mar 2027) in its Q4 results/presentation is strictly greater than the NIM it reports for Q3 FY27 (as stated in the Q3 release, both on the bank's headline basis). Equal = NO.
- **Resolution source:** ICICI Bank Q3 and Q4 FY27 results press releases / investor presentations (NSE)
- **Sources used:** https://nsearchives.nseindia.in/corporate/ICICI2022_23102026175603_NSEBSE23102026.pdf
- **Confidence of evidence:** single-source

### 4. PERSISTENT — Persistent Systems announces completion (closing) of its Nagarro acquisition on or before 31-Mar-2027
- **id:** `thesis:paper-call:PERSISTENT:nagarro-deal-closes-by-mar27`
- **Method:** promise-tracker credibility · **P(ours)** 0.75 · **P(base)** 0.70 · resolve by 2027-04-15
- **Evidence:** Q2 FY27 call (15-Oct-2026): voluntary public takeover offer for Nagarro reached ~94.04% of share capital after the additional acceptance period (ended 6-Oct); squeeze-out planned after closing. All merger-control and FDI clearances received except Austria and Spain ('confident… over the next several weeks'); RBI approval applied for. Financing: €1.4 bn 18-month bridge to be replaced; $1.25 bn long-term raise incl. $450 mn equity — QIP opened 21-Oct-2026 and allotments followed (NSE filings 26-Oct, 4-Nov). CEO: 'We expect the deal closure by Q4-CY26 or Q1-CY27.' Q2: revenue $487.6 mn (+20% YoY), EBIT 15%, ₹185 cr deal costs.
- **Why our number differs from base:** Acceptance and financing — usually the hard parts — are done; what remains is two FDI screens and RBI. Persistent's stated window ends exactly on our date, so a modest slip would flip it. Slightly above base.
- **Base-rate reasoning:** Announced cross-border acquisitions with financing done and most approvals in hand close within ~5 months about 70% of the time; regulatory tails often slip a quarter.
- **Resolution rule:** YES if, on or before 31-Mar-2027, Persistent (NSE filing or press release) announces that the Nagarro acquisition/offer has completed (settlement/closing of the takeover offer). Completion of the later squeeze-out is not required. Announcement only of further approvals = NO.
- **Resolution source:** Persistent Systems NSE announcements / press releases
- **Sources used:** https://nsearchives.nseindia.in/corporate/PERSISTENTUSER1_23102026204328_PSLTranscriptSubmissionOctober2026Sd.pdf; https://www.nseindia.com/companies-listing/corporate-filings-announcements (PERSISTENT, 15-Oct to 21-Nov-2026)
- **Confidence of evidence:** verified

### 5. BAJAJCON — Bajaj Consumer Care FY27 consolidated revenue from operations grows ≥17.0% YoY ("high teens" guide)
- **id:** `thesis:paper-call:BAJAJCON:fy27-revenue-growth-17pct-plus`
- **Method:** promise-tracker credibility · **P(ours)** 0.52 · **P(base)** 0.55 · resolve by 2027-05-31
- **Evidence:** Q2 FY27 call (15-Oct-2026): H1 revenue ₹674 cr (+28%), H1 EBITDA ₹167 cr (+85%), Q2 EBITDA margin 25%; Almond Drops double-digit unit volume growth; GT and organized trade both 'mid-20s' growth. MD Naveen Pandey: 'for the year, we are expecting a high teens' growth. Gross margin 59.9% (West Asia war, edible-oil inflation); ~5% consumer price increase in Q3 (2–3% frontal + ml-age cut). Screener: FY26 sales ₹1,165 cr; quarterly sales Q3 FY26 306 (+31%), Q4 FY26 327 (+30%), Q1 FY27 342, Q2 FY27 333.
- **Why our number differs from base:** H1 at +28% makes a high-teens year look easy, but the H2 base is hard (H2 FY26 grew ~30%), so ≥17% needs H2 growth of ~+10% while the company takes price and cuts ml-age into an inflationary rural market. Management's own 'high teens' (not 'mid-20s') signals they expect H2 to slow sharply. We sit fractionally below base.
- **Base-rate reasoning:** Small-cap FMCG companies restating a full-year growth range at H1 with H1 well above it meet the range's lower part roughly 55% of the time when the H2 comparison base is much tougher.
- **Resolution rule:** YES if Bajaj Consumer Care's FY27 consolidated revenue from operations ÷ FY26 consolidated revenue from operations − 1 ≥ 17.0% (company's own reported growth figure if stated; else from the audited results; screener.in annual table as fallback).
- **Resolution source:** Bajaj Consumer Care Q4 FY27 results / investor presentation (NSE); screener.in
- **Sources used:** https://nsearchives.nseindia.in/corporate/BAJAJCON_21102026110839_Exchanges_Transcript.pdf; https://www.screener.in/company/BAJAJCON/consolidated/
- **Confidence of evidence:** verified

### 6. HDFCLIFE — HDFC Life FY27 value of new business (VNB) grows ≥12.0% YoY
- **id:** `thesis:paper-call:HDFCLIFE:fy27-vnb-growth-12pct-plus`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.52 · **P(base)** 0.45 · resolve by 2027-05-15
- **Evidence:** H1 FY27 call (15-Oct-2026): H1 VNB ₹2,037 cr (+12%), Q2 VNB +15%; new-business margin 24.7% (H1 FY26 24.5%); individual APE +9% H1, total APE +11% H1 / +13% Q2; HDFC Bank channel APE +12% in Q2 ('growth momentum coming back'). MD: 'momentum is building… VNB growth ahead of APE'; GST impact 'now gets baked into the business model from second half'. Headwinds: H2 FY26 protection grew 57% (base effect), ULIP persistency softer, IRDAI consultation papers on distribution economics. FY26 (Q4 FY26 call, Apr-2026): VNB ₹4,034 cr (+2%), margin 24.2% (25.5% ex GST/SSV).
- **Why our number differs from base:** Management tone is the most upbeat in two years and the GST drag on margins laps in H2, so H2 VNB growth ≥12% is plausible; but the 57% protection base and IRDAI commission rules are real. Tone slightly ahead of what H1 numbers alone imply; we are a bit above base.
- **Base-rate reasoning:** Naive: a life insurer's full-year VNB growth lands at or above its H1 growth rate a bit under half the time (H2 is the larger half and often slower).
- **Resolution rule:** YES if HDFC Life's reported FY27 VNB ÷ FY26 VNB (₹4,034 cr, or FY26 as restated in the Q4 FY27 deck) − 1 ≥ 12.0%, using the company's stated growth if given.
- **Resolution source:** HDFC Life Q4 FY27 investor presentation / earnings call (NSE)
- **Sources used:** https://nsearchives.nseindia.in/corporate/HDFCLIFE2_23102026153545_SE_Transcript.pdf; https://nsearchives.nseindia.in/corporate/PRASAD_23042026224833_EarningsCallTranscript.pdf
- **Confidence of evidence:** verified

### 7. HDFCAMC — HDFC AMC Q3 FY27 revenue from operations is ≥₹1,200 cr
- **id:** `thesis:paper-call:HDFCAMC:q3fy27-revenue-1200cr-plus`
- **Method:** base rate · **P(ours)** 0.60 · **P(base)** 0.65 · resolve by 2027-02-15
- **Evidence:** Q2 FY27 call (15-Oct-2026): revenue from operations ₹11.7 bn (+14% YoY), operating profit ₹9.1 bn (36 bps of AUM); QAAUM ₹9.69 tn (+10% YoY, +4% QoQ); equity 67.1% of AUM; active-equity yield 61 bps, debt 28–29, liquid 13. Industry: 67th straight month of equity inflows; Nifty fell ~5% in the Sep quarter. Screener revenue (₹ cr): Q3 FY26 1,074, Q4 1,050, Q1 FY27 1,098, Q2 FY27 1,169. Nifty 20-Nov-2026: 25,800.6 (52-wk high 26,373).
- **Why our number differs from base:** Base-rate call: AMC revenue mostly follows average equity AUM, which rises with flows unless markets fall. Needs only +2.7% QoQ. We shade a little below base because yields drift down as AUM grows (TER slabs) and the Nifty has been range-bound since September.
- **Base-rate reasoning:** HDFC AMC revenue grew ≥2.7% QoQ in 4 of the last 5 quarters; long-run share of quarters with QoQ revenue growth for Indian listed AMCs ~70%. Base ~65%.
- **Resolution rule:** YES if HDFC AMC's revenue from operations (consolidated; standalone if only that is given) for the quarter ended 31-Dec-2026 is ≥₹1,200 cr (₹12.0 bn).
- **Resolution source:** HDFC AMC Q3 FY27 results (NSE) / screener.in quarterly table
- **Sources used:** https://nsearchives.nseindia.in/corporate/DEEPTI_21102026121612_NSEBSE_Transcript.pdf; https://www.screener.in/company/HDFCAMC/
- **Confidence of evidence:** verified

### 8. BSE — BSE Ltd Q3 FY27 consolidated revenue from operations exceeds ₹1,566 cr (a new quarterly record)
- **id:** `thesis:paper-call:BSE:q3fy27-revenue-record-above-1566cr`
- **Method:** sector cycle/lead indicator · **P(ours)** 0.60 · **P(base)** 0.45 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (Nov-2026): H1 operational revenue ₹2,999 cr (+48%); transaction charges ₹2,456 cr (+60%). Index-options premium ADTV: Q1 FY27 ₹29,615 cr, Q2 ₹22,531 cr ('first sequential quarterly contraction'), then 'a decisive recovery in September and a record-breaking October 2026… highest ever monthly index options premium ADTV of Rs. 35,481' crore; record single-day expiry premium ₹85,356 cr on 22-Oct-2026. MSCI derivatives collaboration. Screener revenue (₹ cr): Q4 FY26 1,564, Q1 FY27 1,566, Q2 FY27 1,433; OPM 67–68%.
- **Why our number differs from base:** Lead indicator: premium ADTV drives ~80% of revenue. A linear fit of Q1/Q2 (revenue ≈ ₹1,009 cr + 0.0188 × ADTV) says a Q3 average ADTV above ~₹29.7k cr beats the record; October alone ran at ₹35.5k. Risk: November–December fade or a SEBI F&O tightening. Above base.
- **Base-rate reasoning:** A naive forecaster gives a fast-growing exchange setting a new quarterly revenue record after a down quarter roughly 45% (records are set in about half of quarters in an uptrend).
- **Resolution rule:** YES if BSE's consolidated revenue from operations for the quarter ended 31-Dec-2026 (results filing; screener.in 'Sales') is > ₹1,566 cr.
- **Resolution source:** BSE Ltd Q3 FY27 results (NSE) / screener.in consolidated quarterly table
- **Sources used:** https://nsearchives.nseindia.in/corporate/BSE1_11112026122425_NSeintimation11112026.pdf; https://www.screener.in/company/BSE/consolidated/
- **Confidence of evidence:** verified

### 9. ULTRACEMCO — UltraTech Cement Q3 FY27 consolidated operating profit is ≥₹4,500 cr
- **id:** `thesis:paper-call:ULTRACEMCO:q3fy27-op-4500cr-plus`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.45 · **P(base)** 0.50 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (19-Oct-2026): volume +13.8% YoY, utilisation 71%, fuel and raw-material costs up (West Asia), other fixed cost/t −6%; Chairman's-office commentary: trade prices rose ₹7–10/bag in late September, 'Prices… have risen substantially in the month of October and continue to stay high. My sense is that there is more price improvement that will happen… in the next couple of months', 'full benefit… in the Q3 earnings'; South 'transforming. Mark my words.' Screener (₹ cr): OP Q3 FY26 3,911 (OPM 17.9%), Q4 FY26 5,599, Q1 FY27 5,015, Q2 FY27 3,719 (16.0%); sales Q2 FY27 23,295 (+19%).
- **Why our number differs from base:** ₹4,500 cr needs roughly sales ~₹24.5k cr at ~18.4% OPM, i.e. the October price hikes must largely stick through the post-Diwali lull while fuel stays expensive. Management is unusually emphatic about prices; Indian cement hikes announced in October are often partly rolled back in November–December. We lean slightly below base.
- **Base-rate reasoning:** Naive: Q3 operating profit grows ~15% YoY in line with volume growth plus modest pricing, landing near ₹4,500 cr — a coin-flip-ish 50%.
- **Resolution rule:** YES if UltraTech's consolidated Operating Profit (screener.in quarterly table; equivalently EBITDA excluding other income from the results) for the quarter ended 31-Dec-2026 is ≥₹4,500 cr.
- **Resolution source:** UltraTech Cement Q3 FY27 results (NSE) / screener.in consolidated quarterly table
- **Sources used:** https://nsearchives.nseindia.in/corporate/ULTRACEMCO1_27102026142336_SE_Transcript.pdf; https://www.screener.in/company/ULTRACEMCO/consolidated/
- **Confidence of evidence:** verified

### 10. TATASTEEL — Tata Steel announces a binding (definitive) agreement with the Dutch State/North Holland on the IJmuiden decarbonisation project by 31-Mar-2027
- **id:** `thesis:paper-call:TATASTEEL:nl-binding-decarb-agreement-by-mar27`
- **Method:** base rate · **P(ours)** 0.20 · **P(base)** 0.30 · resolve by 2027-04-15
- **Evidence:** Q2 FY27 call (Nov-2026): 'Tata Steel, the Government of the Netherlands and the Province of North Holland have agreed to extend the Joint Letter of Intent by five months to March 2027… additional time… towards a more comprehensive framework'; 'while the DRI–EAF pathway remains the reference case… we continue to assess a range of strategic alternatives and sequencing options'; outcomes 'difficult to predict'. JLoI signed Sep-2025. Netherlands EBITDA €72 mn in Q2 (€56/t) after DSP restart; European gas >2× Jan-2026 levels. Consolidated net debt ₹91,423 cr.
- **Why our number differs from base:** A first extension plus explicit talk of 'strategic alternatives' are classic signs that a subsidy deal is not converging; Tata Steel also faces UK losses and high net debt, lowering its appetite to commit. Below base.
- **Base-rate reasoning:** Government–industry letters of intent on large decarbonisation subsidies become binding agreements by the extended deadline perhaps 30% of the time; second extensions are common.
- **Resolution rule:** YES if, on or before 31-Mar-2027, Tata Steel (stock-exchange filing or press release) announces a signed binding/definitive agreement (e.g., 'agreement', 'binding term sheet', 'final investment framework') with the Dutch State and/or Province of North Holland for the IJmuiden decarbonisation/health project. A further extension of the LoI, an MoU or a non-binding framework = NO.
- **Resolution source:** Tata Steel NSE/BSE announcements; Tata Steel / Rijksoverheid press releases
- **Sources used:** https://nsearchives.nseindia.in/corporate/NIDHIFADNAVIS_12112026221915_BSENSE_Signed.pdf
- **Confidence of evidence:** single-source

### 11. GODREJPROP — Godrej Properties FY27 booking value is ≥₹40,000 cr
- **id:** `thesis:paper-call:GODREJPROP:fy27-bookings-40000cr-plus`
- **Method:** promise-tracker credibility · **P(ours)** 0.58 · **P(base)** 0.50 · resolve by 2027-04-30
- **Evidence:** Q2 FY27 call (23-Oct-2026): H1 bookings ₹16,669 cr (+7%; 43% of the ₹39,000 cr FY27 guidance) with only a third of launches done; Q2 bookings ₹8,008 cr; H2 launch pipeline ~₹32,000 cr (Bandra, Sector 63A Gurugram, Thane, Verano). Chairperson Pirojsha Godrej: H2 estimate ₹22,500–25,000 cr; 'We hope to cross INR40,000 crores this year.' Collections H1 ₹9,666 cr (+25%). Track record (Q4 FY26 call, May-2026): FY26 bookings ₹34,171 cr = 105% of guidance; deliveries 121% of guidance; BD 200%+ of guidance. Risks named: GRAP/air-quality construction bans in NCR and Mumbai.
- **Why our number differs from base:** GPL has beaten its booking guidance in recent years and the H2 pipeline is large; ₹40,000 cr needs ~₹23,300 cr in H2, inside management's range. Launch slippage is the main failure mode (half of H1 launches slipped). Above base.
- **Base-rate reasoning:** Indian developers hit 'slightly above guidance' targets (here 103% of guidance) roughly half the time.
- **Resolution rule:** YES if Godrej Properties' reported FY27 (Apr-2026–Mar-2027) booking value (sales bookings), per its Q4 FY27 operational update or results presentation, is ≥₹40,000 cr.
- **Resolution source:** Godrej Properties Q4 FY27 business update / investor presentation (NSE)
- **Sources used:** https://nsearchives.nseindia.in/corporate/GODREJPROP_27102026171202_SEIntimationTranscript.pdf; https://nsearchives.nseindia.in/corporate/GODREJPROP_06052026184101_SEIntimationtranscript.pdf
- **Confidence of evidence:** verified

### 12. BEL — Bharat Electronics FY27 order inflow is ≥₹25,000 cr
- **id:** `thesis:paper-call:BEL:fy27-order-inflow-25000cr-plus`
- **Method:** promise-tracker credibility · **P(ours)** 0.66 · **P(base)** 0.60 · resolve by 2027-05-31
- **Evidence:** Q2 FY27 call (3-Nov-2026): order book ₹68,717 cr (1-Oct-2026); FY27 inflow so far ~₹7,334–8,000 cr. CMD Manoj Jain: guidance 'order inflow of INR25,000 crores minimum, excluding QRSAM and including QRSAM, INR50,000-plus crores'; NGC (next-gen corvettes) cleared, ~₹20,000 cr from two shipyards expected 'staggered… 99% will come in this financial year'; Shatrughat, Samaghat, HAMMER 'confident to get' before March; QRSAM slipped ~7–8 months ('we may get before March'). In May-2026 (Q4 FY26 call) FY27 inflow guide was '>₹55,000 cr' incl. QRSAM 'very soon'. FY26 actual inflow ₹30,045 cr ('met all guidance parameters'). H1 revenue ₹12,824 cr (+26%) vs 15%+ guide.
- **Why our number differs from base:** The ex-QRSAM floor rests mostly on NGC, which is cleared and in contract with shipyards; BEL has met base-order guidance in recent years. The QRSAM history shows timelines slip, so we stay modestly above base.
- **Base-rate reasoning:** Indian defence PSUs meet their 'minimum' order-inflow guidance roughly 60% of the time; big single orders often slip across 31 March.
- **Resolution rule:** YES if BEL's FY27 total order inflow (orders received 1-Apr-2026 to 31-Mar-2027), as stated in its Q4 FY27 results/call or an April-2027 order-book disclosure, is ≥₹25,000 cr (QRSAM included if received).
- **Resolution source:** BEL Q4 FY27 results / earnings call transcript / order-book disclosures (NSE)
- **Sources used:** https://nsearchives.nseindia.in/corporate/BEL_06112026145908_Lettersigned.pdf; https://nsearchives.nseindia.in/corporate/BEL_22052026120346_Letter_signed.pdf
- **Confidence of evidence:** verified

### 13. DIXON — Dixon Technologies confirms that its Vivo JV began production/consolidation in Q4 FY27 (by 31-Mar-2027)
- **id:** `thesis:paper-call:DIXON:vivo-jv-production-starts-q4fy27`
- **Method:** base rate · **P(ours)** 0.45 · **P(base)** 0.55 · resolve by 2027-06-15
- **Evidence:** Q2 FY27 call (Nov-2026): 'Consolidation of Vivo operations is expected to commence from Q4, with significant volumes anticipated for the next financial year'; MD Atul Lall: 'the integration process is on. We target to start production from Q4 of the current fiscal… in the JV we should be doing around 20–21 million' units next year. FY27 smartphone volume ~33–34 mn excluding Vivo. Q2 revenue ₹21,806 cr; EBITDA ex-fair-value gain ₹609 cr; margins hit by mobile PLI-1 expiry and memory prices. Screener OPM 2.7% (Q2 FY27). Noida 1 mn sq ft facility 'almost completed', Q3 start.
- **Why our number differs from base:** Base-rate call on 'next-quarter start' promises in EMS: the stated window is the last quarter of the year and integration of a Chinese brand's operations has had a long regulatory path (from memory, the JV was announced in late 2024 — unverified). We put slippage risk above the generic base.
- **Base-rate reasoning:** Indian manufacturers' 'production starts next quarter' commitments are met on time roughly 55% of the time.
- **Resolution rule:** YES if Dixon's Q4 FY27 results, press release or earnings call states that the Vivo JV commenced commercial production and/or was consolidated (revenue included) in Q4 FY27 (on or before 31-Mar-2027). Statements that it will start in Q1 FY28 or later = NO.
- **Resolution source:** Dixon Technologies Q4 FY27 results / earnings call transcript (NSE)
- **Sources used:** https://nsearchives.nseindia.in/corporate/DIXON_05112026163605_EarningCallTranscriptQ2Intimation.pdf; https://www.screener.in/company/DIXON/consolidated/
- **Confidence of evidence:** single-source

### 14. BHARTIARTL — Bharti Airtel announces a headline prepaid mobile tariff increase (≥10% on its core unlimited plans) by 30-Jun-2027
- **id:** `thesis:paper-call:BHARTIARTL:prepaid-tariff-hike-by-jun27`
- **Method:** sector cycle/lead indicator · **P(ours)** 0.35 · **P(base)** 0.30 · resolve by 2027-06-30
- **Evidence:** Q2 FY27 call (Nov-2026): ARPU ₹271 (from ₹264); India mobile ~51% of revenue; consolidated EBITDAaL ~₹31,500 cr (51.7%), net debt/EBITDAaL ~0.70; ~₹2,900 cr spent on a data-centre land parcel. Management: 'long-term ARPU growth ultimately depends on a more rational pricing structure where the industry is able to monetize the continued growth in data consumption'; the Q2 'intervention… on prepaid ladder' (discontinuing the ₹299 pack) was 'experimentation on our own base'; 'the architecture correction is a much broader correction that is required in the industry… to move more decisively'.
- **Why our number differs from base:** Cycle: Indian telecom takes a headline hike every ~2–2.5 years (Dec-2019, Nov-2021, Jul-2024 — from memory, unverified); by mid-2027 the gap would be ~3 years and capex for 5G/data centres keeps pressure on. But Airtel is talking about 'architecture' (data monetisation) rather than a flat hike, and the leader's timing is unknowable. Slightly above base.
- **Base-rate reasoning:** With headline hikes roughly every 30 months, the chance one falls in any given ~7-month window is ~25–30%.
- **Resolution rule:** YES if, between 21-Nov-2026 and 30-Jun-2027, Bharti Airtel announces (press release, NSE filing or widely reported company statement) increases to its prepaid mobile tariffs under which its most popular 28-day unlimited plan price rises ≥10%. Plan withdrawals, validity cuts or postpaid-only changes = NO.
- **Resolution source:** Bharti Airtel press releases / NSE announcements; national press coverage
- **Sources used:** https://nsearchives.nseindia.in/corporate/BHARTIARTL_12112026172851_Airtel_Stx_Intimation.pdf
- **Confidence of evidence:** single-source

### 15. TITAN — Titan's share price return from 20-Nov-2026 to 30-Jun-2027 beats the Nifty 50's price return
- **id:** `thesis:paper-call:TITAN:cooler-valuation-beats-nifty-to-jun27`
- **Method:** valuation-temperature · **P(ours)** 0.45 · **P(base)** 0.48 · resolve by 2027-06-30
- **Evidence:** Yahoo close 20-Nov-2026: Titan ₹4,620.0 (52-wk ₹3,751–5,187); Nifty 50 25,800.6. Screener: P/E 57.7 on TTM EPS ₹79.22 (consolidated) vs FY-end P/E (May price ÷ FY EPS) of ~79×, 83×, 86×, 98×, 77× for FY22–FY26 → ~0.7× its own 5-yr median ('cooler than usual'). But TTM earnings are flattered: Q2 FY27 standalone OPM 15% vs 10–11% history included a ~₹490 cr customs-duty gain in jewellery (normalised Titan Jewellery margin 11.1–11.7% per the 11-Nov-2026 call) and gold MTM swings; Q2 standalone sales growth slowed to +8%; coins/investment buying soft.
- **Why our number differs from base:** Valuation-temperature test with a twist: the stock looks cool on reported TTM earnings, but on normalised margins the multiple is close to its usual level. If the method only works on clean earnings, it should not help here; we lean slightly under base.
- **Base-rate reasoning:** A single Nifty-50 large cap beats the index over ~7 months a bit under half the time (~48%).
- **Resolution rule:** YES if (Titan NSE close on 30-Jun-2027 ÷ 4,620.0) > (Nifty 50 close on 30-Jun-2027 ÷ 25,800.6). Use the last trading day ≤30-Jun-2027; adjust for splits/bonuses; dividends ignored.
- **Resolution source:** NSE / Yahoo Finance closes (TITAN.NS, ^NSEI)
- **Sources used:** https://query1.finance.yahoo.com/v8/finance/chart/TITAN.NS; https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI; https://www.screener.in/company/TITAN/consolidated/; https://nsearchives.nseindia.in/corporate/TITAN_11112026143915_SEearningcalltranscriptsQ2.pdf
- **Confidence of evidence:** verified

### 16. POLYCAB — Polycab India Q3 FY27 consolidated operating margin is ≥13.0%
- **id:** `thesis:paper-call:POLYCAB:q3fy27-opm-13pct-plus`
- **Method:** management-tone-vs-delivery · **P(ours)** 0.72 · **P(base)** 0.70 · resolve by 2027-02-28
- **Evidence:** Q2 FY27 call (Oct-2026): revenue record (+53% YoY per screener: ₹9,899 cr), EBITDA margin 14.4% (+50 bps QoQ); W&C EBIT margin 14.2%; FMEG EBIT 10.1% (first double-digit), FMEG growth +124% (solar). Management keeps the W&C medium-term EBITDA guide at '11% to 13%' and flags 'near-term inflationary pressures… surfacing'. Screener OPM: Sep-24 11.5%, Dec-24 13.8%, Mar-25 14.7%, Jun-25 14.5%, Sep-25 15.8%, Dec-25 12.7%, Mar-26 13.1%, Jun-26 13.8%, Sep-26 14.4%.
- **Why our number differs from base:** Management talks conservatively (11–13% guide) while delivering above it for most quarters — the mirror image of a hype gap. We side with delivery, shaded for copper/inflation and the Q3 FY26 dip to 12.7%.
- **Base-rate reasoning:** Persistence: Polycab's screener OPM was ≥13.0% in 7 of the last 9 quarters (~70%).
- **Resolution rule:** YES if Polycab's consolidated Operating Profit ÷ Sales for the quarter ended 31-Dec-2026 (screener.in quarterly table, or EBITDA ÷ revenue from operations from the results) is ≥13.0%.
- **Resolution source:** Polycab Q3 FY27 results (NSE) / screener.in consolidated quarterly table
- **Sources used:** https://nsearchives.nseindia.in/corporate/POLYCAB_19102026163912_Intimation_of_Earnings_Call_Transcript.pdf; https://www.screener.in/company/POLYCAB/consolidated/
- **Confidence of evidence:** verified

## Method notes (what each call is testing)

- **promise-tracker credibility** — management stated a number or a date; we judge delivery from their track record and how much of the
  promise is already in the bag. A good method should beat the base rate most when it *disagrees* with management.
- **base rate** — we mostly lean on a reference class (seasonality, how often LoIs become binding, guidance-raise frequency) and move
  only a little for company specifics. If these calls score no better than the base column, that is expected and fine.
- **flags-judgment context** — a red flag is present (pledge, restatement, material weakness, going-concern doubt, missed coupon).
  The test (lesson L10/L12) is whether we can tell which flags have teeth for the specific event named.
- **sector cycle/lead indicator** — we use an observable lead indicator (QTD commodity prices, monthly exchange volumes, rate cycle,
  credit-cost trajectory) to forecast a next-quarter number.
- **valuation-temperature** — a stock is hot or cold versus its own history; we forecast 7-month relative price performance. The base
  rate is "a single stock beats its index a bit under half the time". Expect noise; only many such calls can show skill.
- **management-tone-vs-delivery** — management's words are noticeably more (or less) confident than the numbers; we bet on the gap.

## Scoring protocol

On resolution: set `outcome` (1 if the stated event happened, else 0), `brier` = (p − outcome)², and also
compute the base-rate Brier (base − outcome)². Update the curriculum scoreboard. Write a post-mortem for every call
where |p − outcome| > 0.6. Ambiguous resolutions: decide strictly by the written rule; if the data source no longer
publishes the metric, mark `void` (not scored) and say why. Calls in batch 2 should be scored separately as well as pooled
with batch 1, so that method-level Brier scores can be compared once ≥5 calls per method have resolved.

## Caveats

- Several base rates are judgement-based reference classes, not measured frequencies; where we quote history 'from memory' it is
  marked unverified in the evidence. Building measured base rates (guidance-hit frequency by sector, LoI→binding conversion,
  material-weakness remediation timing) is itself a backlog item.
- Price-relative calls use Yahoo Finance closes of 20-Nov-2026 as the start point; check splits/bonuses at resolution.
- Research, not SEBI-registered advice.
