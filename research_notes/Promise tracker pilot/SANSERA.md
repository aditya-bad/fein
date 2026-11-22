# Promise tracker: Sansera Engineering (NSE: SANSERA)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `AUTO_COMPONENTS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_sectors.json` (`analysis:SANSERA:credibility-2026-11`). Ledger source: `scripts_auto_peers/promises_SANSERA.py`.

## 1. Method

- Last 6 earnings calls on NSE (Q1FY26 to Q2FY27), fetched with `tools/promise_tracker/pipeline/fetch.py --since 2025-01-01`; `turns.py` + `candidates.py` (rules) produced the candidate sentences.
- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.
- Outcomes: group numbers from screener.in consolidated (re-derived: growth and OPM computed from the quarterly table); segment, SOP and order figures from the company's own later calls (single-source).
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 19 / 8 |
| Status counts | delivered 5, missed 1, moved-goalpost 1, pending 9, unverifiable 2, withdrawn 1 |
| Weighted delivery ratio | 70.1% |
| Specificity-only delivery | 60.0% |
| Raw hit rate | 62.5% |
| MCS (-1.5 .. +1) | +0.33 |
| Candour index (shortfalls admitted unprompted) | 33.3% (1/3) |
| **Sector-adjusted credibility (SAC)** | **-4.8 pts** (shrink weight 0.286 at N=8) |

By category (credit basis): capacity 0.0% (n=3); revenue_growth 100.0% (n=5).
SAC components: pooled:revenue_growth+capacity: own 60.0% vs peer median 64.8% (n=8, gap -4.8).

**Caveat: n is small** (6 calls; few hard numbers). No category reaches the L18 threshold of 5 scored promises with 2+ peers, except as noted, so SAC is computed on pooled categories and shrunk toward zero when used.

## 3. Reading

- Group revenue guidance was met: FY26 +15.9% vs 'at least the teens' / 'teens to mid-teens'. The start-of-year 'mid-to-high teens' was trimmed openly in Feb-26 (outside the 6-call window, not scored).
- ADS (aerospace/defence/semicon) guidance was met: INR 315 cr vs 280-300, run-rate ~38 cr/month vs 38-40.
- Capacity forecasts are the weak spot: FY26 capex INR 510 cr vs 375-400 guided seven weeks before year-end; the new ADS hangar re-dated Jun-Jul -> Jul-Aug -> 'towards October' 2026 without an explanation (moved-goalpost).
- The FY27 capex step-up (510 -> 800 cr) was announced openly with its reason (new ADS orders) and is scored withdrawn (-0.5), per clarification A.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-08-12 | FY26 ADS revenue to double to INR 280-300 cr | revenue_growth | range | P | 2026-03-31 | **delivered** | 'ADS revenue from product sales reaching INR3,155 million, representing an exceptional growth of 155%' (Q4FY26 call). Company figure. |
| 2025-08-12 | FY26 Swedish subsidiary growth 20-25% (~INR 225 cr) | revenue_growth | range | P | 2026-03-31 | **unverifiable** | Q4FY26 call cites 'strong growth in Swedish subsidiary' but no FY figure; Q2FY27: Sweden -16% YoY. |
| 2025-11-13 | FY26 consolidated revenue growth at least in the teens | revenue_growth | range | P | 2026-03-31 | **delivered** | FY26 revenue 3,498 vs 3,017 cr = +15.9% (screener consolidated). |
| 2025-11-13 | H2FY26 'much, much stronger' than H1FY26 | revenue_growth | vague | P | 2026-03-31 | **delivered** | H1FY26 1,591 cr, H2FY26 1,907 cr (+20%) (screener). |
| 2025-11-13 | ADS run-rate ~INR 38-40 cr/month for the next five months | revenue_growth | range | P | 2026-03-31 | **delivered** | H2FY26 ADS = 315.5 - 86.4 (H1) = ~229 cr over 6 months = ~38 cr/month (company figures). |
| 2025-11-13 | New ADS hangar ready by June-July 2026 | capacity | precise | P | 2026-07-31 | **moved-goalpost** | Restated 2026-02-10 'June, July'; 2026-05-21 'complete the construction by July, August'; 2026-08-13 'probably by towards October when we have our new hangar ready'. No explanation of the slip given; Q2FY27 call does not confirm completion. |
| 2026-02-10 | FY26 revenue growth teens to mid-teens with margin profile maintained | revenue_growth | range | V | 2026-03-31 | **delivered** | +15.9% (screener); FY26 company EBITDA margin 18.1% vs 17.5% FY25. |
| 2026-02-10 | FY26 capex INR 375-400 cr (below the INR 450 cr plan) | capacity | range | P | 2026-03-31 | **missed** | FY26 capex INR 509.7 cr ('we incurred a capex of INR5,097 million', Q4FY26 call) = 27% above the top of the range given 7 weeks before year-end. Growth capex for ADS orders, so economically benign, but a forecast miss. |
| 2026-02-10 | FY27 ADS revenue INR 550-600 cr | revenue_growth | range | P | 2027-03-31 | **pending** | 2026-08-13: ADS growth 'about 75%-80%' for FY27 (= INR 552-568 cr on 315.5). |
| 2026-02-10 | FY27 consolidated revenue growth about 20% | revenue_growth | precise | P | 2027-03-31 | **pending** | 2026-05-21 plan 'mid-to-high teens, more towards high-teens'; 2026-08-13 'high-teens top-line growth' (volunteered) and 'high-teens to 20%'. H1FY27 +33% (screener 2,112 vs 1,591 cr). |
| 2026-02-10 | FY27 margin profile better than FY26 | margin | vague | P | 2027-03-31 | **pending** | 2026-08-13: 'happier if we are able to inch towards 19%'. H1FY27 company 19.3%, screener 19.2%. |
| 2026-05-21 | FY27 capex at a similar level to FY26 (~INR 510 cr) | capacity | vague | V | 2027-03-31 | **withdrawn** | Raised openly to INR 800 cr on 2026-11-06 ('we have raised FY27 Capex projection to INR8,000 million', for new ADS orders) - explicit, explained revision >1 quarter before the deadline. |
| 2026-05-21 | FY27 Auto business H1 stronger than H2 (base effect) | revenue_growth | vague | V | 2027-03-31 | **pending** |  |
| 2026-08-13 | FY27 high-teens top-line growth (volunteered) | revenue_growth | range | V | 2027-03-31 | **pending** | H1FY27 +33% (screener). |
| 2026-08-13 | NADCAP and customer approvals for the new special-process facility within Q2FY27 | capacity | precise | P | 2026-09-30 | **unverifiable** | Not mentioned in the Q2FY27 call text read. |
| 2026-11-06 | Sansera-Nichidai JV commercial production towards the end of H2 FY27 | capacity | range | V | 2027-03-31 | **pending** |  |
| 2026-11-06 | Dedicated defence facility to begin operations towards the end of Q3 FY27 (or from Q4) | capacity | precise | V | 2027-03-31 | **pending** | Q&A: 'The defense should be operational towards the end of the third quarter or from the fourth quarter.' |
| 2026-11-06 | Add a second customer in the new (semicon/ADS) space in Q3FY27 | other | precise | P | 2026-12-31 | **pending** |  |
| 2026-11-06 | FY27 capex raised to INR 800 cr | capacity | precise | V | 2027-03-31 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5: P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:SANSERA:fy27-revenue-growth-17pct-plus-cred` - Sansera FY27 consolidated revenue growth is >=17.0% (low end of 'high-teens' guide) | revenue_growth | 0.56 | 0.57 | 2027-05-31 | see specs.json |
| `thesis:paper-call:SANSERA:fy27-opm-above-fy26-cred` - Sansera FY27 consolidated operating margin is >18.4% (better than FY26) | margin | 0.71 | 0.72 | 2027-05-31 | see specs.json |
| `thesis:paper-call:SANSERA:nichidai-jv-production-by-mar27-cred` - Sansera-Nichidai JV starts commercial production by 31-Mar-2027 | capacity | 0.42 | 0.43 | 2027-06-15 | see specs.json |
| `thesis:paper-call:SANSERA:defence-facility-operational-by-mar27-cred` - Sansera's dedicated defence facility is operational by 31-Mar-2027 | capacity | 0.42 | 0.43 | 2027-06-15 | see specs.json |

## Sources

- https://nsearchives.nseindia.in/corporate/SANSERA_13112026120144_transcript.pdf 
- https://nsearchives.nseindia.in/corporate/SANSERA_17022026122638_transcript.pdf 
- https://nsearchives.nseindia.in/corporate/SANSERA_17082025151807_Transcript.pdf 
- https://nsearchives.nseindia.in/corporate/SANSERA_20082026120039_Transcript.pdf 
- https://nsearchives.nseindia.in/corporate/SANSERA_20112025093848_Transcript.pdf 
- https://nsearchives.nseindia.in/corporate/SANSERA_28052026152825_Transcript.pdf 
- https://www.screener.in/company/SANSERA/consolidated/ 
