# Promise tracker: A. O. Smith (NYSE: AOS; memdb ticker US-AOS)

*As of 22-Nov-2026. Research, not investment advice (not SEBI- or SEC-registered). This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `US_INDUSTRIALS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_us_industrials.json` (`analysis:US-AOS:credibility-2026-11`). Ledger source: `scripts_us_industrials/promises_US-AOS.py`.

## 1. Method

- 6 Motley Fool transcripts Q2-2025..Q3-2026 (the Q2-2026 call is listed twice; the 30-Jul-2026 copy is used). The CFO's outlook section was read in full on every call. CFO changed in Q3-2026 (Charles Lauber -> Carrie Anderson).
- Ledger built by hand (fetch.py reads NSE, not US sources): Motley Fool takeaway list + targeted greps of the full text (guidance, outlook, organic, adjusted operating margin, EPS, free cash flow / conversion, capex, savings, price/cost). Quotes marked [Fool summary] are the transcriber's takeaway wording, not management's words. Pipeline v1.3 adds the US measure vocabulary to `score.py` for future runs.
- Restatements are folded into the first promise (`later_restatements`), not double-counted; a cut >= 2 quarters before the deadline is 'withdrawn' (clarification A).
- Outcomes: company-adjusted KPIs (organic growth, adjusted operating margin, adjusted EPS, segment margins) from the company's own later calls/releases (single-source); GAAP revenue, operating income, EPS, capex, FCF, buybacks and dividends re-derived from SEC XBRL companyfacts (`tools/sec_fetch.py facts`) as the second source.
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 28 / 18 |
| Status counts | delivered 10, missed 1, partly 2, pending 10, withdrawn 5 |
| Weighted delivery ratio | 60.5% |
| Specificity-only delivery | 65.9% |
| Raw hit rate | 55.6% |
| MCS (-1.5 .. +1) | +0.40 |
| Candour index (shortfalls admitted unprompted) | 87.5% (7/8) |
| **Sector-adjusted credibility (SAC)** | **-35.3 pts** (shrink weight 0.474 at N=18) |

By category (credit basis): capacity 50.0% (n=1); margin 75.0% (n=4); other 86.7% (n=6); revenue_growth 43.3% (n=7).
SAC components: revenue_growth: own 43.3% vs peer median 100.0% (n=7, gap -56.7); other: own 86.7% vs peer median 100.0% (n=6, gap -13.3); pooled:margin+capacity: own 68.2% vs peer median 100.0% (n=5, gap -31.8).

**Caveat: n is small** (6 calls; 6-18 scored promises; most FY2026 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.

## 3. Reading

- FY2025 company-level guidance was met: EPS $3.85 in a $3.70-3.90 band (narrowed to $3.70-3.85 in Oct), FCF $546 mn vs $500-525 mn, North America margin 24.4% in 24-24.5%, Rest of World 8.7% in 8-9%, buybacks $401 mn vs ~$400 mn (all XBRL-checked where tagged).
- The misses are China and sub-lines: FY2025 China -5..-8% (Jul) -> 'down 10%' (Oct) -> -12%; FY2025 capex $70.8 mn vs ~$75 mn.
- **FY2026 guidance was cut three times.** EPS $3.85-4.15 (Jan) -> $3.70-4.00 adjusted (Apr) -> $3.70-3.85 (Jul) -> $3.42-3.52 ex-China, continuing operations (Oct). Rest of World margin 8-9% -> 6-7%; water-treatment growth 10-12% -> 5-6% -> 3-4%; China 'mid-single-digit decline, growth in H2' -> 'low double digits' -> sold. Each cut was explicit and explained more than two quarters before the deadline, so clarification A scores them **withdrawn** (-0.5), not missed. Candour is high (7 of 8 shortfalls admitted unprompted).
- Leonard Valve: '~$70 mn of 2026 sales' (Jan, Jul) cut to $55 mn in Oct (final quarter: scored on outcome when FY2026 reports; 9M = $47 mn).
- The China sale (81% to CPE, $400 mn, close 'first half of 2027') is one of the calls. It changes the measurement basis of every FY2026 total-company promise: the calls use the ex-China, continuing-operations figures the company now guides.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-07-24 | FY2025 EPS $3.70-$3.90 (narrowed) | eps | range | V | 2025-12-31 | **delivered** | FY2025 EPS $3.85 (SEC XBRL EarningsPerShareDiluted 3.85; Q4-2025 call 'record $3.85'). |
| 2025-07-24 | FY2025 free cash flow $500-525 mn | cash_flow | range | V | 2025-12-31 | **delivered** | FY2025 FCF $546 mn (XBRL CFO 616.8 - capex 70.8 = 546.0, re-derived), above the range; helped by a one-time tax item. |
| 2025-07-24 | FY2025 North America segment margin 24%-24.5% | segment_margin | range | V | 2025-12-31 | **delivered** | FY2025 North America segment margin 24.4% (Q4-2025 call). |
| 2025-07-24 | FY2025 Rest of World segment margin 8%-9% | segment_margin | range | V | 2025-12-31 | **delivered** | FY2025 Rest of World segment margin 8.7% (Q4-2025 call). The Oct-2025 call's 'about 7.5%' (Fool summary) looks like a quarter figure; not used. |
| 2025-07-24 | FY2025 North America boiler sales +4% to +6% (raised from 3-5%) | revenue_growth | range | V | 2025-12-31 | **delivered** | FY2025 boiler sales +8% (Q4-2025 call). |
| 2025-07-24 | FY2025 North America water treatment sales down ~5% (retail de-emphasised) | revenue_growth | precise | V | 2025-12-31 | **delivered** | FY2025 water treatment sales -2% (Q4-2025 call): better than guided. |
| 2025-07-24 | FY2025 North America water treatment margin +250 to +300 bp | segment_margin | range | P | 2025-12-31 | **delivered** | 'expanded operating margin by 400 basis points to almost 13% last year' (Q4-2025 call). |
| 2025-07-24 | FY2025 China sales down 5%-8% (local currency) | revenue_growth | range | P | 2025-12-31 | **missed** | FY2025 China third-party sales -12% in local currency (Q4-2025 call), 4 pts below the bottom of the range. Lowered to 'down 10%' in Oct-2025 (final quarter: clarification A, scored on outcome). |
| 2025-07-24 | ~$15 mn annual savings from the 2024 China restructuring realised in 2025 | cost_savings | precise | V | 2025-12-31 | **delivered** | Q4-2025 call: 'The restructuring actions we took in late 2024 and expense management drove profitability improvement of 130 basis points despite lower sales' (China); RoW earnings flat despite -4% sales. The $15 mn itself is not separately reported. |
| 2025-07-24 | FY2025 share repurchases ~$400 mn | capital_return | precise | V | 2025-12-31 | **delivered** | XBRL PaymentsForRepurchaseOfCommonStock FY2025 $400.8 mn. |
| 2025-10-28 | FY2025 capital expenditures ~$75 mn (lowered; projects shift into 2026) | capex | precise | V | 2025-12-31 | **partly** | XBRL capex (PaymentsToAcquireProductiveAssets) FY2025 $70.8 mn: 5.6% under a one-quarter-ahead estimate. |
| 2025-10-28 | FY2025 China sales down ~10% (local currency) | revenue_growth | precise | V | 2025-12-31 | **partly** | FY2025 China -12% in local currency (Q4-2025 call): 2 pts worse than a one-quarter-ahead estimate. |
| 2026-01-29 | FY2026 EPS $3.85-$4.15 (midpoint +4%) | eps | range | V | 2026-12-31 | **withdrawn** | Cut on 30-Apr-2026 to adjusted $3.70-$4.00 (China, residential volume, input costs; explained, 3 quarters before the deadline: clarification A), then $3.70-$3.85 (Jul) and $3.42-$3.52 ex-China continuing ops (Oct). |
| 2026-01-29 | FY2026 total sales growth ~+2% to +5% | revenue_growth | range | V | 2026-12-31 | **withdrawn** | Narrowed to 2-4% (Apr) and 2-3% (Jul), then re-based to 'approximately 4%' excluding China (Oct). The basis change (China to discontinued operations) means the original total-company target can no longer be measured as stated; scored withdrawn (explicit, expla... |
| 2026-01-29 | FY2026 free cash flow $525-575 mn | cash_flow | range | V | 2026-12-31 | **pending** |  |
| 2026-01-29 | FY2026 Rest of World segment margin 8%-9% | segment_margin | range | V | 2026-12-31 | **withdrawn** | Cut on 30-Apr-2026 to 6%-7% (China demand; explained); China then moved to discontinued operations (Oct). |
| 2026-01-29 | FY2026 North America segment margin 24%-24.5% | segment_margin | range | V | 2026-12-31 | **pending** |  |
| 2026-01-29 | FY2026 North America water treatment sales +10% to +12% | revenue_growth | range | V | 2026-12-31 | **withdrawn** | Cut on 30-Apr-2026 to +5-6% (consumer caution, trade-down; explained), then to +3-4% (Oct). |
| 2026-01-29 | FY2026 North America boiler sales +6% to +8% | revenue_growth | range | V | 2026-12-31 | **pending** |  |
| 2026-01-29 | FY2026 China sales down mid-single digits, back to growth in H2 | revenue_growth | vague | V | 2026-12-31 | **withdrawn** | Cut on 30-Apr-2026 to 'down low double digits' (Q1 -17%); Q3 China sales 'well below our expectations'; business sold (81% to CPE, Oct-2026). |
| 2026-01-29 | Leonard Valve to contribute ~$70 mn of 2026 sales | m&a | precise | V | 2026-12-31 | **pending** |  |
| 2026-01-29 | FY2026 share repurchases ~$200 mn | capital_return | precise | V | 2026-12-31 | **pending** |  |
| 2026-04-30 | Q2-2026 EPS ~25% of the full-year guidance midpoint ($3.85 x 25% = ~$0.96) | eps | precise | V | 2026-06-30 | **delivered** | Q2-2026 adjusted EPS $1.03 (Q2-2026 call) = 27% of the $3.85 midpoint. |
| 2026-04-30 | Water-treatment restructuring ($20 mn charge) to save $6-8 mn a year from 2027 | cost_savings | range | V | 2027-12-31 | **pending** |  |
| 2026-07-30 | FY2026 share repurchases ~$300 mn (raised 50%) | capital_return | precise | V | 2026-12-31 | **pending** |  |
| 2026-10-29 | FY2026 adjusted EPS $3.42-$3.52 (continuing operations, China excluded) | eps | range | V | 2026-12-31 | **pending** |  |
| 2026-10-29 | FY2026 sales excluding China up ~4% | revenue_growth | precise | V | 2026-12-31 | **pending** |  |
| 2026-10-29 | Sale of 81% of the China business to CPE to close in H1-2027 | m&a | range | V | 2027-06-30 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `US_INDUSTRIALS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:US-AOS:fy26-adj-eps-ex-china-3-42-plus-cred` - A. O. Smith FY2026 adjusted EPS excluding China (continuing operations) is >=$3.42 | other | 0.65 | 0.82 | 2027-03-31 | see specs.json |
| `thesis:paper-call:US-AOS:fy26-sales-growth-ex-china-3-5pct-plus-cred` - A. O. Smith FY2026 net sales growth, continuing operations (China excluded), is >=3.5% ('approximately 4%') | revenue_growth | 0.65 | 0.82 | 2027-03-31 | see specs.json |
| `thesis:paper-call:US-AOS:china-sale-closes-by-jun27-cred` - A. O. Smith completes the sale of 81% of its China business to CPE by 30-Jun-2027 | other | 0.65 | 0.82 | 2027-07-31 | see specs.json |

## Sources

- https://data.sec.gov/api/xbrl/companyfacts/CIK0000091142.json 
- https://www.fool.com/earnings/call-transcripts/2025/07/24/a-o-smith-aos-q2-2025-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2025/10/28/a-o-smith-aos-q3-2025-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/01/29/a-o-smith-aos-q4-2025-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/04/30/a-o-smith-aos-q1-2026-earnings-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/07/30/ao-smith-aos-q2-2026-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/10/29/a-o-smith-aos-q3-2026-earnings-call-transcript/ 
