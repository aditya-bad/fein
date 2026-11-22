# Promise tracker: Lincoln Electric (NASDAQ: LECO; memdb ticker US-LECO)

*As of 22-Nov-2026. Research, not investment advice (not SEBI- or SEC-registered). This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `US_INDUSTRIALS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_us_industrials.json` (`analysis:US-LECO:credibility-2026-11`). Ledger source: `scripts_us_industrials/promises_US-LECO.py`.

## 1. Method

- 6 calls Q2-2025..Q3-2026: 4 Motley Fool transcripts plus the Q2-2025 and Q2-2026 8-K Ex 99.1 press releases (no Fool transcripts found). Lincoln's releases carry almost no outlook, so those two quarters add only the Alloy Steel closing. **Thinnest read of the four.**
- Ledger built by hand (fetch.py reads NSE, not US sources): Motley Fool takeaway list + targeted greps of the full text (guidance, outlook, organic, adjusted operating margin, EPS, free cash flow / conversion, capex, savings, price/cost). Quotes marked [Fool summary] are the transcriber's takeaway wording, not management's words. Pipeline v1.3 adds the US measure vocabulary to `score.py` for future runs.
- Restatements are folded into the first promise (`later_restatements`), not double-counted; a cut >= 2 quarters before the deadline is 'withdrawn' (clarification A).
- Outcomes: company-adjusted KPIs (organic growth, adjusted operating margin, adjusted EPS, segment margins) from the company's own later calls/releases (single-source); GAAP revenue, operating income, EPS, capex, FCF, buybacks and dividends re-derived from SEC XBRL companyfacts (`tools/sec_fetch.py facts`) as the second source.
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 18 / 6 |
| Status counts | delivered 5, partly 1, pending 12 |
| Weighted delivery ratio | 91.5% |
| Specificity-only delivery | 88.5% |
| Raw hit rate | 83.3% |
| MCS (-1.5 .. +1) | +0.92 |
| Candour index (shortfalls admitted unprompted) | 0.0% (0/1) |
| **Sector-adjusted credibility (SAC)** | **-11.5 pts** (shrink weight 0.231 at N=6) |

By category (credit basis): margin 100.0% (n=3); other 75.0% (n=2); revenue_growth 100.0% (n=1).
SAC components: pooled:revenue_growth+margin+other: own 88.5% vs peer median 100.0% (n=6, gap -11.5).

**Caveat: n is small** (6 calls; 6-18 scored promises; most FY2026 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.

## 3. Reading

- Lincoln guides in words ('mid single digit', 'modest improvement') plus segment EBIT-margin bands, incremental margin, capex and cash conversion - few hard numbers.
- Near-term Q4-2025 statements were met: automation +20% QoQ vs '15-20%'; adjusted operating margin 18.0% vs Q3's 17.4% ('modest sequential improvement'); Americas Welding ~20% vs '18-19%'; International 11.8% inside '11-12%'.
- The one miss: in Oct-2025 the FY2025 cash-conversion range was **raised** to 'above 100%'; the year came in at 97% (FCF $534.2 mn / adjusted net income $551.3 mn, Q4-2025 release table) and the Q4 call did not mention it.
- FY2026: sales growth guide raised twice (mid single digit -> high single digit -> low teens); capex raised from $110-130 mn to $140-150 mn in the final quarter (scored on outcome). 2030 targets (19% average margin, >$6 bn sales) are logged pending.
- Only 6 scored promises and two of six calls read from press releases only: treat the score as a placeholder.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-07-31 | Acquisition of the remaining 65% of Alloy Steel (~$90 mn) to close on 01-Aug-2025 | m&a | precise | V | 2025-08-31 | **delivered** | Q3-2025 call: International Welding sales +~4% 'benefit from our alloy steel acquisition'; interest expense raised 'due to recent borrowings for the alloy steel transaction'. |
| 2025-10-30 | Q4-2025 automation sales up 15%-20% sequentially (from $200 mn), still below Q4-2024 | revenue_growth | range | V | 2025-12-31 | **delivered** | Q4-2025 automation sales $240 mn (down 11% YoY) vs $200 mn in Q3 = +20% QoQ (Q4-2025 call). |
| 2025-10-30 | Q4-2025 adjusted operating margin modestly above Q3 (17.4%) | margin | vague | V | 2025-12-31 | **delivered** | Q4-2025 adjusted operating income margin 18.0% (Q4-2025 call: 'declined 20 basis points to 18%' YoY) vs Q3-2025 17.4%. |
| 2025-10-30 | Americas Welding adjusted EBIT margin 18%-19% for the rest of 2025 | segment_margin | range | V | 2025-12-31 | **delivered** | Q4-2025 Americas Welding adjusted EBIT $141 mn, margin ~20% (Fool summary 'Americas Welding: 20% (up 90 bps)'): above the band. |
| 2025-10-30 | International Welding adjusted EBIT margin 11%-12% for the rest of 2025 | segment_margin | range | V | 2025-12-31 | **delivered** | Fool Q4-2025 summary: 'International Welding: 11.8% (down 100 bps)' - inside the band; whether this is the quarter or the year is not stated (single-source). |
| 2025-10-30 | FY2025 cash conversion above 100% (range raised) | cash_flow | precise | V | 2025-12-31 | **partly** | Q4-2025 press release table: FY2025 cash conversion 97% (FCF $534.2 mn / adjusted net income $551.3 mn); Q4 alone 35%. A floor raised one quarter before the deadline and then missed by 3 pts; not mentioned on the Q4 call. |
| 2026-02-12 | FY2026 net sales growth in the mid-single-digit range (half volume, half price carry-over) | revenue_growth | vague | V | 2026-12-31 | **pending** |  |
| 2026-02-12 | FY2026 automation sales return to mid-single-digit growth (from $870 mn) | revenue_growth | vague | P | 2026-12-31 | **pending** |  |
| 2026-02-12 | FY2026 adjusted operating margin modestly above 2025 (17.2%), mid-20% incrementals | margin | vague | V | 2026-12-31 | **pending** |  |
| 2026-02-12 | FY2026 Americas Welding EBIT margin mid-18% to mid-19% | segment_margin | range | V | 2026-12-31 | **pending** |  |
| 2026-02-12 | FY2026 International Welding EBIT margin mid-11% to mid-12% | segment_margin | range | V | 2026-12-31 | **pending** |  |
| 2026-02-12 | FY2026 capex $110-130 mn | capex | range | V | 2026-12-31 | **pending** |  |
| 2026-02-12 | FY2026 cash conversion ~100% | cash_flow | precise | V | 2026-12-31 | **pending** |  |
| 2026-02-12 | 2030 targets: sales >$6 bn, 19% average operating margin (peak 20%+), mid-teens EPS CAGR | margin | precise | V | 2030-12-31 | **pending** |  |
| 2026-04-30 | FY2026 net sales growth raised to the high-single-digit range | revenue_growth | vague | V | 2026-12-31 | **pending** |  |
| 2026-10-27 | FY2026 net sales growth in the low-teens percent range | revenue_growth | vague | V | 2026-12-31 | **pending** |  |
| 2026-10-27 | FY2026 capex $140-150 mn | capex | range | V | 2026-12-31 | **pending** |  |
| 2026-10-27 | Q4-2026 Americas Welding adjusted EBIT margin 20%-21%; International Welding 12%-13% | segment_margin | range | V | 2026-12-31 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `US_INDUSTRIALS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:US-LECO:fy26-sales-growth-11pct-plus-cred` - Lincoln Electric FY2026 net sales growth is >=11.0% ('low teens percent') | revenue_growth | 0.60 | 0.63 | 2027-03-15 | see specs.json |
| `thesis:paper-call:US-LECO:fy26-capex-140-150mn-cred` - Lincoln Electric FY2026 capital expenditures are within $140-150 mn | capacity | 0.69 | 0.71 | 2027-03-15 | see specs.json |
| `thesis:paper-call:US-LECO:fy26-adj-op-margin-above-17-6-cred` - Lincoln Electric FY2026 adjusted operating income margin (company-reported) is >=17.7% (above FY2025's 17.6%) | margin | 0.89 | 0.91 | 2027-03-15 | see specs.json |

## Sources

- https://data.sec.gov/api/xbrl/companyfacts/CIK0000059527.json 
- https://www.fool.com/earnings/call-transcripts/2025/10/30/lincoln-electric-leco-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/02/12/lincoln-electric-leco-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/04/30/leco-q1-2026-earnings-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/10/27/lincoln-electric-leco-q3-2026-earnings-call-transcript/ 
- https://www.sec.gov/Archives/edgar/data/59527/000005952725000022/leco-20250731xex99d1.htm 
