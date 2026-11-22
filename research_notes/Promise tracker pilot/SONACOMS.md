# Promise tracker: Sona BLW Precision Forgings (NSE: SONACOMS)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `AUTO_COMPONENTS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_sectors.json` (`analysis:SONACOMS:credibility-2026-11`). Ledger source: `scripts_auto_peers/promises_SONACOMS.py`.

## 1. Method

- Last 6 earnings calls on NSE (Q1FY26 to Q2FY27), fetched with `tools/promise_tracker/pipeline/fetch.py --since 2025-01-01`; `turns.py` + `candidates.py` (rules) produced the candidate sentences.
- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.
- Outcomes: group numbers from screener.in consolidated (re-derived: growth and OPM computed from the quarterly table); segment, SOP and order figures from the company's own later calls (single-source).
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 16 / 6 |
| Status counts | delivered 4, missed 1, partly 1, pending 9, unverifiable 1 |
| Weighted delivery ratio | 82.4% |
| Specificity-only delivery | 83.3% |
| Raw hit rate | 66.7% |
| MCS (-1.5 .. +1) | +0.70 |
| Candour index (shortfalls admitted unprompted) | 50.0% (1/2) |
| **Sector-adjusted credibility (SAC)** | **+50.0 pts** (shrink weight 0.231 at N=6) |

By category (credit basis): margin 75.0% (n=3); other 90.0% (n=3).
SAC components: pooled:margin+other: own 83.3% vs peer median 33.3% (n=6, gap +50.0).

**Caveat: n is small** (6 calls; few hard numbers). No category reaches the L18 threshold of 5 scored promises with 2+ peers, except as noted, so SAC is computed on pooled categories and shrunk toward zero when used.

## 3. Reading

- Sona does not guide revenue ('we don't give forward growth guidance'). Its scoreable statements are mix targets (BEV share, non-auto share), a margin band and return ratios, so n is small (6 scored).
- The margin band drifted down in the open: 24-25% (Oct-25, met for FY26 at 24.7%) -> 23-25% (Apr-26) -> 'around 23%' (Oct-26). Each change was said out loud with a reason (railway consolidation, traction-motor mix, commodity lag). That is candour, not a goalpost move under the pilot rule.
- The one clear miss: 'recovery measures ... visible from quarter 2' (Jul-26) - Q2FY27 margin was flat at ~23% and management said so in the opening remarks.
- The non-auto >25% delivery is mostly mechanical (railway acquisition consolidated), so it says little about execution. Discount the +50 SAC accordingly - the shrink weight (0.23) already does most of that.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-08-04 | BEV revenue share to improve over the next few quarters (from 28% in Q1FY26) | other | vague | V | 2026-03-31 | **delivered** | BEV share 38% in Q3FY26, 39% in Q4FY26, 44% Q1FY27, 51% Q2FY27 (company, later calls). |
| 2025-08-04 | Non-automotive revenue share to rise above 25% in the coming quarters (railways consolidation) | other | precise | V | 2026-03-31 | **delivered** | 'The share of non-automotive revenues from 9% in FY25 today is 31% in the first nine months of this year' (Q3FY26 call). Mostly mechanical (railway acquisition consolidated from Q2FY26). |
| 2025-08-04 | Asia incl. India to exceed 50% of revenue in the coming quarters | other | precise | V | 2026-03-31 | **unverifiable** | Geography split not restated in later transcripts read; deck not checked. |
| 2025-10-27 | Consolidated EBITDA margin target 24-25% after consolidating lower-margin railways | margin | range | P | 2026-03-31 | **delivered** | FY26 company EBITDA margin 24.7% ('we have still managed to end FY26 with a full year EBITDA margin of 24.7%', Q4FY26 call); screener OPM 24.3%. Q4FY26 alone 23.5% (screener). |
| 2025-10-27 | Return ratios (ROCE 16%, ROE 13% in H1FY26) to improve in the quarters and years ahead | other | vague | V | 2027-03-31 | **partly** | Screener FY26 ROCE 14% (FY25 18%) - fell; Q2FY27 call: 'Our return ratios have also improved' for H1FY27 (company, figure not checked). Direction right only from H1FY27. |
| 2025-10-27 | Mexico driveline plant: first program production from Q2 FY28 | capacity | precise | V | 2027-09-30 | **pending** |  |
| 2026-01-23 | Traction motors & controllers to be the highest-growth segment for the next 5 years | other | vague | P | 2031-03-31 | **pending** |  |
| 2026-04-30 | Commodity pass-through lag will keep pressure on margins in the foreseeable future | margin | vague | V | 2026-09-30 | **delivered** | Q1FY27 and Q2FY27 company EBITDA margin ~23% (screener 22.5% / 22.5%) vs FY26 24.7%. |
| 2026-04-30 | FY27 consolidated EBITDA margin to stay in a 23-25% band | margin | range | P | 2027-03-31 | **pending** | H1FY27 company ~23.0% (screener 22.5%); 2026-10-26 CFO: 'around 23% ... don't hold us to every 10 or 20 bps'. |
| 2026-04-30 | Sensor assembly (Novelic India) SOP by end of 2026 | capacity | precise | P | 2026-12-31 | **pending** |  |
| 2026-07-23 | Cost-recovery measures to become progressively visible in margins from Q2FY27 | margin | vague | V | 2026-09-30 | **missed** | Q2FY27 company EBITDA margin 23% ('lower by 2.x pp' YoY), screener 22.5% = flat QoQ; mgmt: 'continued margin pressure ... mainly driven by change in product mix'. |
| 2026-07-23 | 'Phenomenal' EV (BEV) revenue growth in FY27 | other | vague | P | 2027-03-31 | **pending** | H1FY27 BEV revenue +119% YoY to INR 1,042 cr (Q2FY27 call). |
| 2026-10-26 | Close JV1 (2W/3W carve-out with Denso) by end-December 2026, possibly spilling to January | other | precise | P | 2027-01-31 | **pending** |  |
| 2026-10-26 | JV2 (high-voltage, Denso majority) to close in H1 of calendar 2027 | other | range | P | 2027-06-30 | **pending** |  |
| 2026-10-26 | Normalised consolidated EBITDA margin 'around 23%' given product mix | margin | precise | P | 2027-03-31 | **pending** | Restates 2026-04-30 '23-25%' at its floor - an acknowledged downward drift (24-25 -> 23-25 -> ~23) over 12 months. |
| 2026-10-26 | Medium-term aspiration implies ~25% revenue CAGR | revenue_growth | precise | P | 2030-03-31 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5: P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:SONACOMS:fy27-opm-23pct-plus-cred` - Sona BLW FY27 consolidated operating margin is >=23.0% (floor of its 23-25% band) | margin | 0.63 | 0.51 | 2027-05-31 | see specs.json |
| `thesis:paper-call:SONACOMS:jv1-denso-closed-by-jan27-cred` - Sona BLW completes the JV1 (2W/3W carve-out with Denso) transaction by 31-Jan-2027 | other | 0.51 | 0.39 | 2027-02-28 | see specs.json |
| `thesis:paper-call:SONACOMS:jv2-closed-by-jun27-cred` - Sona BLW closes JV2 (high-voltage e-powertrain JV with Denso) by 30-Jun-2027 | other | 0.51 | 0.39 | 2027-07-31 | see specs.json |

## Sources

- https://nsearchives.nseindia.in/corporate/SONACOMS_06052026103543_Intimation.pdf 
- https://nsearchives.nseindia.in/corporate/SONACOMS_09082025173136_Transcript.pdf 
- https://nsearchives.nseindia.in/corporate/SONACOMS_30072026142213_Transcript.pdf 
- https://nsearchives.nseindia.in/corporate/SONACOMS_31012026114914_Transcript.pdf 
- https://nsearchives.nseindia.in/corporate/SONACOMS_31102025175705_Transcript.pdf 
- https://nsearchives.nseindia.in/corporate/SONACOMS_31102026183421_Intimation.pdf 
- https://www.screener.in/company/SONACOMS/consolidated/ 
