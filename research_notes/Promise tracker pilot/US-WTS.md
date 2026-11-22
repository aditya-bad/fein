# Promise tracker: Watts Water Technologies (NYSE: WTS; memdb ticker US-WTS)

*As of 22-Nov-2026. Research, not investment advice (not SEBI- or SEC-registered). This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `US_INDUSTRIALS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_us_industrials.json` (`analysis:US-WTS:credibility-2026-11`). Ledger source: `scripts_us_industrials/promises_US-WTS.py`.

## 1. Method

- 6 calls Q2-2025..Q3-2026: 5 Motley Fool transcripts (curl, UA 'Mozilla/5.0', HTML -> text) plus the Q3-2025 8-K Ex 99.1 press release (no Fool transcript found; its 'Full Year 2025 Outlook' paragraph stands in for the call). Fool page dates are publication dates: the Q4-2025 call is dated 12-Feb-2026 (8-K filed 11-Feb), Q2-2026 06-Aug-2026.
- Ledger built by hand (fetch.py reads NSE, not US sources): Motley Fool takeaway list + targeted greps of the full text (guidance, outlook, organic, adjusted operating margin, EPS, free cash flow / conversion, capex, savings, price/cost). Quotes marked [Fool summary] are the transcriber's takeaway wording, not management's words. Pipeline v1.3 adds the US measure vocabulary to `score.py` for future runs.
- Restatements are folded into the first promise (`later_restatements`), not double-counted; a cut >= 2 quarters before the deadline is 'withdrawn' (clarification A).
- Outcomes: company-adjusted KPIs (organic growth, adjusted operating margin, adjusted EPS, segment margins) from the company's own later calls/releases (single-source); GAAP revenue, operating income, EPS, capex, FCF, buybacks and dividends re-derived from SEC XBRL companyfacts (`tools/sec_fetch.py facts`) as the second source.
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 22 / 12 |
| Status counts | delivered 12, pending 10 |
| Weighted delivery ratio | 100.0% |
| Specificity-only delivery | 100.0% |
| Raw hit rate | 100.0% |
| MCS (-1.5 .. +1) | +1.00 |
| Candour index (shortfalls admitted unprompted) | n/a (no shortfalls scored) |
| **Sector-adjusted credibility (SAC)** | **+15.3 pts** (shrink weight 0.375 at N=12) |

By category (credit basis): margin 100.0% (n=5); other 100.0% (n=1); revenue_growth 100.0% (n=6).
SAC components: revenue_growth: own 100.0% vs peer median 71.65% (n=6, gap +28.3); margin: own 100.0% vs peer median 100.0% (n=5, gap +0.0); pooled:other: own 100.0% vs peer median 86.7% (n=1, gap +13.3).

**Caveat: n is small** (6 calls; 6-18 scored promises; most FY2026 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.

## 3. Reading

- Every scored promise was met or beaten (12 of 12): FY2025 organic flat to +3% (Aug) -> +5%; reported +2-5% -> +8.4% (XBRL); adjusted operating margin +50-110 bp -> +190 bp; FCF conversion >=100% -> 104.5% (XBRL re-derived); every next-quarter organic and margin band beaten (Q3-25 organic +9% vs 2-5%; Q1-26 +12% vs 4-8%; Q2-26 +12.2% vs 4-8%).
- This is the profile of a **systematic sandbagger**: guidance was raised at every call in 2025-26 (FY2026 organic 2-6% -> 8-11% -> 11-12%). A 100% delivery record is evidence of conservative guiding, not of foresight. Data-centre demand (now high-single-digit % of sales) drove most of the 2026 beats.
- Pending FY2026: organic 11-12%, reported 17-18%, adjusted operating margin 20.3-20.4%, FCF conversion >=90%, Q4 organic 9-12%. These are now one-quarter-ahead guides, so delivery should be high again.
- The rule still gives WTS only P = 0.47 on its two FY2026 growth calls, because the peers' strict revenue/growth delivery is low (41%, dragged by A. O. Smith's China and water-treatment misses) and the shrink weight is 0.375. This is the case where 'company credibility' (very high) and 'sector base rate' (low) disagree most: a good test of the shrink.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-08-07 | FY2025 organic sales growth flat to +3% (raised two points) | revenue_growth | range | V | 2025-12-31 | **delivered** | FY2025 organic +5% (Q4-2025 call: 'organic sales grew 8% in the quarter and 5% for the year'); beaten above the top of the range. |
| 2025-08-07 | FY2025 reported sales growth +2% to +5% | revenue_growth | range | V | 2025-12-31 | **delivered** | SEC XBRL revenue 2.25B (2024) -> 2.44B (2025) = +8.4% (re-derived); company '8% for the year'. |
| 2025-08-07 | FY2025 adjusted operating margin expansion +50 to +110 bp | margin | range | V | 2025-12-31 | **delivered** | FY2025 adjusted operating margin 19.6%, +190 bp (Q4-2025 call). GAAP op income/revenue 448.1/2,440 = 18.4% (XBRL) vs 17.4% in 2024 (390.4/2,250): +100 bp on GAAP, also inside the band. |
| 2025-08-07 | Q3-2025 organic sales growth +2% to +5% | revenue_growth | range | V | 2025-09-30 | **delivered** | Q3-2025 organic +9% (press release 05-Nov-2025: 'up 13% on a reported basis and up 9% organically'). |
| 2025-08-07 | Q3-2025 operating margin 17.1%-17.7% | margin | range | V | 2025-09-30 | **delivered** | Q3-2025 operating margin 18.2% GAAP, 18.5% adjusted (press release). |
| 2025-08-07 | FY2025 free cash flow conversion at least 100% of net income | cash_flow | precise | V | 2025-12-31 | **delivered** | XBRL: CFO 402.0 - capex 45.7 = FCF 356.3 vs net income 340.8 = 104.5% (re-derived); company 105%. |
| 2025-11-05 | FY2025 organic sales growth +4% to +5%; reported +7% to +8% | revenue_growth | range | V | 2025-12-31 | **delivered** | FY2025 organic +5%, reported +8.4% (XBRL). |
| 2025-11-05 | FY2025 adjusted operating margin 19.1%-19.2% (+140 to +150 bp) | margin | precise | V | 2025-12-31 | **delivered** | FY2025 adjusted operating margin 19.6% (+190 bp), above the top of the band. |
| 2026-02-12 | FY2026 organic sales growth +2% to +6% (about 2 pts more ex 80/20 exits) | revenue_growth | range | V | 2026-12-31 | **pending** |  |
| 2026-02-12 | FY2026 reported sales growth +8% to +12% | revenue_growth | range | V | 2026-12-31 | **pending** |  |
| 2026-02-12 | Q1-2026 organic sales growth +4% to +8% | revenue_growth | range | V | 2026-03-31 | **delivered** | Q1-2026 organic +12%, reported +21% (Q1-2026 call). |
| 2026-02-12 | Q1-2026 operating margin 18.6%-19.2% | margin | range | V | 2026-03-31 | **delivered** | Q1-2026 adjusted operating margin 20.1%, EBITDA 22.3% (Q1-2026 call). |
| 2026-02-12 | FY2026 80/20 exits remove $25-30 mn of Americas sales (and $10-15 mn in Europe), margin neutral or accretive | other | range | V | 2026-12-31 | **pending** |  |
| 2026-02-12 | FY2026 acquisitions add $130 mn+ of incremental sales, ~50 bp margin dilution | m&a | precise | V | 2026-12-31 | **pending** |  |
| 2026-05-07 | Q2-2026 organic sales growth +4% to +8% | revenue_growth | range | V | 2026-06-30 | **delivered** | Q2-2026 organic +12.2%, reported +19% (Q2-2026 call). |
| 2026-05-07 | Q2-2026 operating margin 20.0%-20.6% | margin | range | V | 2026-06-30 | **delivered** | Q2-2026 adjusted operating margin 21.0%, EBITDA 23.1% (Q2-2026 call). |
| 2026-08-06 | FY2026 free cash flow conversion 90% or more of net income | cash_flow | precise | V | 2026-12-31 | **pending** |  |
| 2026-08-06 | Price/cost to stay at least neutral through H2-2026 despite new tariffs | price_cost | vague | P | 2026-12-31 | **pending** |  |
| 2026-11-05 | FY2026 organic sales growth +11% to +12% | revenue_growth | range | V | 2026-12-31 | **pending** |  |
| 2026-11-05 | FY2026 reported sales growth +17% to +18% | revenue_growth | range | V | 2026-12-31 | **pending** |  |
| 2026-11-05 | FY2026 adjusted operating margin 20.3%-20.4% (+70 to +80 bp) | margin | precise | V | 2026-12-31 | **pending** |  |
| 2026-11-05 | Q4-2026 organic sales growth +9% to +12% | revenue_growth | range | V | 2026-12-31 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `US_INDUSTRIALS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:US-WTS:fy26-reported-sales-growth-17pct-plus-cred` - Watts Water FY2026 reported net sales growth is >=17.0% | revenue_growth | 0.47 | 0.41 | 2027-03-15 | see specs.json |
| `thesis:paper-call:US-WTS:fy26-adj-op-margin-20-3pct-plus-cred` - Watts Water FY2026 adjusted operating margin (company-reported) is >=20.3% | margin | 0.94 | 0.88 | 2027-03-15 | see specs.json |
| `thesis:paper-call:US-WTS:fy26-organic-growth-11pct-plus-cred` - Watts Water FY2026 organic sales growth (company-reported) is >=11.0% | revenue_growth | 0.47 | 0.41 | 2027-03-15 | see specs.json |

## Sources

- https://data.sec.gov/api/xbrl/companyfacts/CIK0000795403.json 
- https://www.fool.com/earnings/call-transcripts/2025/08/07/watts-water-wts-q2-2025-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/02/12/watts-water-wts-q4-2025-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/05/07/watts-water-wts-q1-2026-earnings-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/08/12/watts-water-technologies-wts-q2-2026-earnings-call-transcript/ 
- https://www.fool.com/earnings/call-transcripts/2026/11/05/watts-water-wts-q3-2026-earnings-call-transcript/ 
- https://www.sec.gov/Archives/edgar/data/795403/000110465925107038/wts-20251105xex99d1.htm 
