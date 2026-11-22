# Promise tracker: KPIT Technologies (NSE: KPITTECH)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `IT_MIDCAPS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_it.json` (`analysis:KPITTECH:credibility-2026-11`). Ledger source: `scripts_it_peers/promises_KPITTECH.py`.

## 1. Method

- 6 NSE calls Q1FY26-Q2FY27 (590 rule candidates). The Q4FY26 file is a long outlook call with run-together text.
- Pipeline v1.2 (`fetch.py --since 2025-07-01`, `turns.py`, `candidates.py` with the new IT vocabulary: deal_wins / people / client_concentration categories; CC growth, TCV, EBIT band measures in `score.py`).
- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.
- Outcomes: IT KPIs (CC growth, EBIT/EBITDA margin as the company defines it, TCV, DSO, large deals) from the company's own later calls (single-source); INR revenue and screener-derived margins re-computed from screener's quarterly table as a cross-check (they differ from company EBIT/EBITDA for Persistent, Coforge and KPIT).
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 12 / 5 |
| Status counts | delivered 4, partly 1, pending 7 |
| Weighted delivery ratio | 95.9% |
| Specificity-only delivery | 95.5% |
| Raw hit rate | 80.0% |
| MCS (-1.5 .. +1) | +0.96 |
| Candour index (shortfalls admitted unprompted) | 0.0% (0/1) |
| **Sector-adjusted credibility (SAC)** | **+6.6 pts** (shrink weight 0.2 at N=5) |

By category (credit basis): margin 100.0% (n=2); revenue_growth 90.0% (n=3).
SAC components: pooled:revenue_growth+margin: own 95.5% vs peer median 88.9% (n=5, gap +6.6).

**Caveat: n is small** (6 calls; 4-10 scored promises; most FY27 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.

## 3. Reading

- Every FY26 statement resolved delivered or partly: EBITDA 'maintain 21%' -> 20.8%; H2 > H1; Q3 'marginal' growth (+1.5% CC); Q4 'highest growth quarter' (+1.8% CC, barely; 'meaningful' growth was implied, scored partly).
- The record breaks in FY27, but the score cannot show it yet because nothing has resolved. In Jan-2026 KPIT said FY27 growth would 'for sure' beat FY26, and on 7-May-2026 it guided FY27 EBITDA 20.5-21.2%. Weeks later Q1FY27 came in at 17.2% EBITDA and -3.6% CC QoQ (two largest SDV programmes ended). Recovery has slid from 'by Q4' (Jul-26) to 'early next year when we get there' (Oct-26).
- This is the clearest example in the IT set of a good scored record next to a probable large miss on the most important current guidance. The credibility rule (P = 0.75 for the FY27 EBITDA call) will look badly wrong on it, and that is part of what the test measures: the rule ignores in-year progress by design.
- Company EBITDA and screener OPM differ by ~2 pp for KPIT (FY26 20.8% vs 18.9%), so the EBITDA call is assisted, not structured.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-07-30 | Maintain ~21% EBITDA margin for FY26 | margin | precise | P | 2026-03-31 | **delivered** | FY26 EBITDA 20.8% ('EBITDA growth margin is for the year 20.8%', Q4FY26 call), within 0.3 pp. Screener OPM FY26 18.9% (different classification). |
| 2025-07-30 | H2FY26 revenue higher than H1; growth momentum returns in H2 | revenue_growth | vague | V | 2026-03-31 | **delivered** | Screener sales H1FY26 1,539 + 1,588 = 3,127 cr; H2FY26 1,617 + 1,711 = 3,328 cr (+6.4%); CC QoQ Q3 +1.5%, Q4 +1.8% vs Q2 +0.3%. |
| 2025-11-10 | Q3FY26 marginal CC growth, Q4FY26 'meaningful growth' | revenue_growth | vague | P | 2026-03-31 | **partly** | Q3FY26 +1.5% CC QoQ (marginal: met); Q4FY26 +1.8% CC QoQ ('a bit of a muted growth year, but ultimately, we had a good Q4') - barely above Q3, hard to call 'meaningful' (a spike was implied). |
| 2025-11-10 | Q3FY26 profitability: absorb increments in Q3-Q4 and still hold FY26 at 21% | margin | precise | V | 2026-03-31 | **delivered** | Q4FY26 EBITDA 20.6%; FY26 20.8% (company). |
| 2026-01-30 | Q4FY26 to be the highest-growth quarter of FY26, with profitability up from Q3 | revenue_growth | precise | P | 2026-03-31 | **delivered** | Q4FY26 +1.8% CC QoQ vs Q3 +1.5%, Q2 +0.3%, Q1 +0.4% (company); Q4 EBITDA 20.6%. |
| 2026-01-30 | FY27 growth to be higher than FY26 ('for sure') | revenue_growth | vague | P | 2027-03-31 | **pending** | Q1FY27 CC -3.6% QoQ, +0.1% YoY (two largest SDV programmes ended); Q2FY27 services flat, products +5% QoQ. Off track. |
| 2026-05-07 | FY27 EBITDA margin 20.5-21.2% (after AI / products investment) | margin | range | V | 2027-03-31 | **pending** | Given 7-May-2026; Q1FY27 EBITDA 17.2%, Q2FY27 17.8% (company). Q2FY27 CEO: margins 'will go up to some extent, every quarter, but, it will be early next year when we get there' - i.e. 20%+ only in FY28. A June-2026 mid-quarter update (not in these transcripts)... |
| 2026-05-07 | FY27 solutions & products revenue +30% YoY | revenue_growth | precise | V | 2027-03-31 | **pending** | Q2FY27: products +25% YoY, +5% QoQ (company). |
| 2026-05-07 | Medium-term EBITDA 22-24% as solutions & products reach ~40% of revenue in 3 years | margin | range | V | 2029-03-31 | **pending** |  |
| 2026-07-29 | H2FY27 better than H1; return to QoQ growth by Q4FY27 | revenue_growth | vague | V | 2027-03-31 | **pending** | Q2FY27: 'H2 will be better than H1. I think we will maintain that' and 'we expect growth in that quarter' (no number). Screener sales Q1FY27 1,675 cr, Q2FY27 1,691 cr. |
| 2026-07-29 | EBITDA back to 'normal' (~20%+) by Q4FY27 as growth returns | margin | vague | P | 2027-03-31 | **pending** | Endorsed an analyst's '20% plus by 4Q' framing; re-dated on 2026-10-28 to 'early next year when we get there' (Q4FY27 or Q1FY28; flag). |
| 2026-10-28 | EBITDA margin to rise every quarter from Q2FY27's 17.8% | margin | vague | P | 2027-03-31 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `IT_MIDCAPS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:KPITTECH:fy27-ebitda-20-5pct-plus-cred` - KPIT FY27 EBITDA margin (company-reported) is >=20.5% | margin | 0.75 | 0.74 | 2027-05-31 | see specs.json |
| `thesis:paper-call:KPITTECH:h2fy27-revenue-above-h1-cred` - KPIT H2FY27 consolidated revenue exceeds H1FY27 (FY27 revenue > INR 6,732 cr = 2 x H1) | revenue_growth | 0.56 | 0.55 | 2027-05-31 | see specs.json |
| `thesis:paper-call:KPITTECH:q4fy27-cc-qoq-growth-positive-cred` - KPIT Q4FY27 constant-currency revenue growth QoQ (company-reported) is >0% | revenue_growth | 0.56 | 0.55 | 2027-05-31 | see specs.json |

## Sources

- https://nsearchives.nseindia.in/corporate/KPITTECH_03112026220723_KPIT_Q2FY27_Transcript_Signed.pdf 
- https://nsearchives.nseindia.in/corporate/KPITTECH_04082026205946_KPIT_Transcript_Cov_let_signed.pdf 
- https://nsearchives.nseindia.in/corporate/KPITTECH_06022026223507_CoverTranscript_Signed.pdf 
- https://nsearchives.nseindia.in/corporate/KPITTECH_06082025193155_CoverTransacriptJuly30_Signed.pdf 
- https://nsearchives.nseindia.in/corporate/KPITTECH_17112025223456_ransacriptNov10_Signed.pdf 
- https://nsearchives.nseindia.in/corporate/MeghanaPhadnis_13052026221810_covertranscript_Signed.pdf 
- https://www.screener.in/company/KPITTECH/consolidated/ 
