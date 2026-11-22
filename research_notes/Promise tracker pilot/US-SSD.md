# Promise tracker: Simpson Manufacturing (NYSE: SSD; memdb ticker US-SSD)

*As of 22-Nov-2026. Research, not investment advice (not SEBI- or SEC-registered). This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `US_INDUSTRIALS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_us_industrials.json` (`analysis:US-SSD:credibility-2026-11`). Ledger source: `scripts_us_industrials/promises_US-SSD.py`.

## 1. Method

- 6 calls Q2-2025..Q3-2026: 5 Motley Fool transcripts plus the Q2-2026 8-K Ex 99.1 'Business Outlook' section (no Fool transcript found). Call dates from the transcripts' DATE lines (Monday after-close calls), not the fool.com publication dates.
- Ledger built by hand (fetch.py reads NSE, not US sources): Motley Fool takeaway list + targeted greps of the full text (guidance, outlook, organic, adjusted operating margin, EPS, free cash flow / conversion, capex, savings, price/cost). Quotes marked [Fool summary] are the transcriber's takeaway wording, not management's words. Pipeline v1.3 adds the US measure vocabulary to `score.py` for future runs.
- Restatements are folded into the first promise (`later_restatements`), not double-counted; a cut >= 2 quarters before the deadline is 'withdrawn' (clarification A).
- Outcomes: company-adjusted KPIs (organic growth, adjusted operating margin, adjusted EPS, segment margins) from the company's own later calls/releases (single-source); GAAP revenue, operating income, EPS, capex, FCF, buybacks and dividends re-derived from SEC XBRL companyfacts (`tools/sec_fetch.py facts`) as the second source.
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 14 / 7 |
| Status counts | delivered 4, partly 3, pending 6, unverifiable 1 |
| Weighted delivery ratio | 82.2% |
| Specificity-only delivery | 79.4% |
| Raw hit rate | 57.1% |
| MCS (-1.5 .. +1) | +0.82 |
| Candour index (shortfalls admitted unprompted) | 33.3% (1/3) |
| **Sector-adjusted credibility (SAC)** | **-7.0 pts** (shrink weight 0.259 at N=7) |

By category (credit basis): capacity 50.0% (n=3); margin 100.0% (n=2); other 100.0% (n=2).
SAC components: pooled:margin+capacity+other: own 79.4% vs peer median 86.4% (n=7, gap -7.0).

**Caveat: n is small** (6 calls; 6-18 scored promises; most FY2026 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.

## 3. Reading

- Simpson guides only a GAAP consolidated operating-margin band (2 pts wide in Jul-2025 and Feb-2026), capex and tax rate: no sales or EPS guidance. Wide bands are easy to hit: FY2025 19.66% (XBRL re-derived) sat inside both 18.5-20.5% and 19-20%. The bands include one-off property-sale gains ($12.9 mn in 2025; ~$11 mn land sale planned for Q4-2026).
- Near misses on capacity and capex: FY2025 capex $161.0 mn vs $140-160 mn and $150-160 mn (0.6% over: partly). The Gallatin fastener plant opened on time in Q3-2025 but was still ramping in Q1-2026 (~100 bp gross-margin headwind), against 'fully operational by the end of this year': partly.
- Delivered: >=35% of FCF returned (56%); the 2025 price actions were worth ~$130 mn annualised vs ~$100 mn guided.
- Pending FY2026: margin band (narrowed to 20.0-20.5%), capex $80-90 mn (raised from $75-85 mn in Jul), the >=$30 mn cost programme and an opex cut of $10-15 mn. With only 7 scored promises, the SAC (-7.0) is mostly the capex/plant near-misses.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-07-28 | FY2025 consolidated operating margin 18.5%-20.5% (incl. $12-13 mn Gallatin property gain) | margin | range | V | 2025-12-31 | **delivered** | XBRL OperatingIncomeLoss 458.1 / revenue 2,330 = 19.66% (re-derived); company 19.6%. |
| 2025-07-28 | FY2025 capex $140-160 mn (reduced), incl. $70-75 mn for Columbus and Gallatin | capex | range | V | 2025-12-31 | **partly** | XBRL PaymentsToAcquirePropertyPlantAndEquipment FY2025 $161.0 mn: 0.6% above the top of the range (ceiling-style overshoot <=5%: clarification B -> partly). |
| 2025-07-28 | New Gallatin, Tennessee fastener plant fully operational by end-2025 | capacity_commissioning | precise | V | 2025-12-31 | **partly** | Opened in Q3-2025 ('our new Gallatin, Tennessee facility opened during the third quarter', Oct-2025) but still ramping in Q1-2026: 'start-up costs from the ongoing ramp of our Gallatin facility that opened late last year' (~100 bp gross-margin headwind). |
| 2025-07-28 | Return at least 35% of 2025 free cash flow to shareholders | capital_return | precise | V | 2025-12-31 | **delivered** | XBRL: dividends 47.6 + buybacks 120.0 = 167.6 vs FCF 458.7 - 161.0 = 297.6 -> 56% (re-derived). |
| 2025-10-27 | FY2025 operating margin 19%-20% (incl. $12.9 mn property gain, $9-12 mn severance) | margin | range | V | 2025-12-31 | **delivered** | FY2025 19.66% (XBRL re-derived). |
| 2025-10-27 | FY2025 capex $150-160 mn | capex | range | V | 2025-12-31 | **partly** | FY2025 capex $161.0 mn (XBRL): 0.6% above the top of a one-quarter-ahead range. |
| 2025-10-27 | Strategic cost programme: at least $30 mn annualised savings, realised in 2026 | cost_savings | precise | V | 2026-12-31 | **pending** |  |
| 2025-10-27 | June + October 2025 price increases worth ~$100 mn of annualised sales | price_cost | precise | V | 2026-06-30 | **delivered** | Q1-2026 call: '2025 Price Increases -- Now expected to contribute approximately $130 million in annualized net sales, up from $100 million' (European surcharges, mix); Q1-2026 price +6%. |
| 2026-02-09 | FY2026 consolidated operating margin 19.5%-20.5% (incl. $10-12 mn asset-sale gain, $3-5 mn footprint costs) | margin | range | V | 2026-12-31 | **pending** |  |
| 2026-02-09 | FY2026 capex $75-85 mn | capex | range | V | 2026-12-31 | **pending** |  |
| 2026-02-09 | FY2026 operating expenses $10-15 mn lower than 2025 (net of ~$5 mn adverse FX) | cost_savings | range | P | 2026-12-31 | **pending** |  |
| 2026-02-09 | Outlook assumes US housing starts down low single digits in 2026 (assumption, not a promise; logged for context) | other | vague | V | 2026-12-31 | **unverifiable** | External market assumption, not a management commitment; excluded from scoring. |
| 2026-10-26 | FY2026 operating margin 20.0%-20.5% (incl. ~$11 mn Q4 land-sale gain) | margin | range | V | 2026-12-31 | **pending** |  |
| 2026-10-26 | FY2026 capex $80-90 mn | capex | range | V | 2026-12-31 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `US_INDUSTRIALS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:US-SSD:fy26-op-margin-20pct-plus-cred` - Simpson FY2026 GAAP consolidated operating margin is >=20.0% | margin | 0.90 | 0.92 | 2027-03-15 | see specs.json |
| `thesis:paper-call:US-SSD:fy26-capex-80-90mn-cred` - Simpson FY2026 capital expenditures are within $80-90 mn | capacity | 0.73 | 0.75 | 2027-03-15 | see specs.json |

## Sources

- https://data.sec.gov/api/xbrl/companyfacts/CIK0000920371.json 
- https://www.fool.com/earnings/call-transcripts/2025/08/07/simpson-ssd-q2-2025-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2025/10/28/simpson-mfg-ssd-q3-2025-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/02/09/simpson-ssd-q4-2025-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/10/26/simpson-manufacturing-ssd-q3-2026-earnings-call-transcript/ 
