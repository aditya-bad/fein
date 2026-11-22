# Promise tracker: Persistent Systems (NSE: PERSISTENT)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `IT_MIDCAPS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_it.json` (`analysis:PERSISTENT:credibility-2026-11`). Ledger source: `scripts_it_peers/promises_PERSISTENT.py`.

## 1. Method

- 6 calls: Q1FY26, Q2FY26, Q3FY26, Q4FY26 (company-website PDF via `fetch.py --local`; the NSE filing is a cover letter), the 28-Jun-2026 Nagarro acquisition call, Q2FY27. Persistent held no Q1FY27 earnings call (results 02-Aug-2026, during the Nagarro offer). `turns.py` needed `--roster`.
- Pipeline v1.2 (`fetch.py --since 2025-07-01`, `turns.py`, `candidates.py` with the new IT vocabulary: deal_wins / people / client_concentration categories; CC growth, TCV, EBIT band measures in `score.py`).
- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.
- Outcomes: IT KPIs (CC growth, EBIT/EBITDA margin as the company defines it, TCV, DSO, large deals) from the company's own later calls (single-source); INR revenue and screener-derived margins re-computed from screener's quarterly table as a cross-check (they differ from company EBIT/EBITDA for Persistent, Coforge and KPIT).
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 15 / 4 |
| Status counts | delivered 4, pending 11 |
| Weighted delivery ratio | 100.0% |
| Specificity-only delivery | 100.0% |
| Raw hit rate | 100.0% |
| MCS (-1.5 .. +1) | +1.00 |
| Candour index (shortfalls admitted unprompted) | n/a (no shortfalls scored) |
| **Sector-adjusted credibility (SAC)** | **+13.9 pts** (shrink weight 0.167 at N=4) |

By category (credit basis): margin 100.0% (n=2); other 100.0% (n=2).
SAC components: pooled:margin+other: own 100.0% vs peer median 86.1% (n=4, gap +13.9).

**Caveat: n is small** (6 calls; 4-10 scored promises; most FY27 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.

## 3. Reading

- Persistent says 'we don't give forward-looking guidance' on every call. Its scoreable near-term statements were all met: FY26 tax rate 22.6% (22.5-23.5% guided), FY26 EBIT +90 bp (~+100 bp guided), the Q3FY26 wage-hike walk (beaten ex the one-time labour-code charge, clarification C) and the deferred wage hike.
- Its two big aspirations are pending and both were quietly re-framed. 'Reach USD 2 billion by FY27' (Jul-2025, 'we need a CAGR of 19-20%') became, in Apr-2026, 'that's a run rate ... Q4 exit ... in the range of $500 million or so, plus minus a quarter at worst'. '+200-300 bp from 14.7% by FY27' (i.e. 16.7-17.7%) became 'our aspiration continues to be in the 16 to 17% range' and 'we have achieved whatever we had said'. Neither change was acknowledged as a change. Under pipeline v1.1 they stay pending with a goalpost flag and are resolved at the deadline.
- Nagarro (announced 27-Jun-2026; 94% tendered by Oct; closing expected Dec-2026/Jan-2027) will blur both FY27 tests: it lifts reported revenue and its ~13.9% EBITDA margin dilutes EBIT. The revenue call therefore uses ex-Nagarro revenue and voids if that is not disclosed.
- Only 4 scored promises: the 100% delivery rate says little. The shrink weight (0.17) keeps it from moving the calls much.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-07-23 | Reach USD 2 billion revenue by end of FY27 (needs ~19-20% CAGR) | revenue_growth | precise | V | 2027-03-31 | **pending** | FY26 USD 1,654 mn (+17.4%); Q2FY27 USD 487.6 mn (+7.8% QoQ, organic - Nagarro not closed). GOALPOST FLAG: on 2026-04-21 the CEO said '$2 billion by FY27, that's a run rate ... Q4 exit ... in the range of $500 million or so ... plus minus a quarter at worst' - ... |
| 2025-07-23 | EBIT margin to improve 200-300 bp from FY25 (14.7%) by FY27, i.e. ~16.7-17.7% | margin | range | P | 2027-03-31 | **pending** | FY26 15.6% (+90 bp); Q1FY27 ~16.0% (derived from Q2's +1.6% QoQ EBIT on +8.4% QoQ INR revenue), Q2FY27 15.0% (wage hike, large-deal amortisation). GOALPOST FLAG: 2026-01-20 'we are not aspiring now to take it another 200 basis points up'; 2026-04-21 'we have a... |
| 2025-07-23 | FY26 effective tax rate in the 22.5-23.5% range | other | range | V | 2026-03-31 | **delivered** | FY26 ETR 22.6% ('Effective tax rate for FY26 stood at 22.6%', Q4FY26 call). |
| 2025-07-23 | Annual wage hike postponed by one quarter (to 1-Oct-2025) | other | precise | V | 2025-10-31 | **delivered** | 'effective October 1, 2025, we have rolled out increments to all our employees ... in line with the previous years' (Q2FY26 call). |
| 2025-07-23 | Europe to reach ~15% of revenue in the next 2-3 years | revenue_growth | precise | P | 2028-03-31 | **pending** | Q4FY26: Europe declined 1.8% QoQ ('an area where we want to double down'). Nagarro (Europe-heavy) would meet it mechanically once consolidated. |
| 2025-10-14 | FY26 EBIT margin ~100 bp above FY25 (14.7%), i.e. ~15.7% | margin | precise | P | 2026-03-31 | **delivered** | FY26 EBIT margin 15.6% (+90 bp; company, Q4FY26 call), despite a one-time 230 bp labour-code charge in Q3. Within 0.3 pp of +100 bp. Screener-derived (OP-dep)/sales FY26 16.2% (different classification). |
| 2025-10-14 | Q3FY26 wage hike costs 180 bp of margin, of which 80-100 bp offset by other levers (net ~-80-100 bp QoQ from 16.3%) | margin | range | V | 2025-12-31 | **delivered** | Q3FY26 reported EBIT 14.4% incl. a one-time 230 bp New Labour Code provision (government change, sector-wide); excluding it 16.7% (+40 bp QoQ) - the wage walk was beaten. Clarification C: delivered on the adjusted basis, both numbers shown; single-source. |
| 2026-01-20 | Long-term aspiration: USD 5 billion annual revenue by FY31 | revenue_growth | precise | V | 2031-03-31 | **pending** |  |
| 2026-01-20 | Stock-option (ESOP) cost to fall further in FY27 | margin | vague | V | 2027-03-31 | **pending** | Q2FY27: 'lower ESOP costs enabled us to absorb part of this [wage] impact' - on track. |
| 2026-04-21 | Q4FY27 quarterly revenue ~USD 500 mn (USD 2 bn annualised run rate), 'plus minus a quarter at worst' | revenue_growth | precise | P | 2027-03-31 | **pending** | Q2FY27 USD 487.6 mn organic. Restates (and re-defines) the 2025-07-23 USD 2 bn FY27 target. |
| 2026-04-21 | EBIT margin aspiration 16-17% (FY27) | margin | range | P | 2027-03-31 | **pending** | Q2FY27 15.0% (wage hike 140 bp net, 90 bp large-deal amortisation). Restated 2026-10-15 ('we want to be in the 16 to 17 % range, that is our aspiration'). |
| 2026-06-28 | Nagarro acquisition to close in Q4 CY2026 or early Q1 CY2027 | m&a | range | V | 2027-03-31 | **pending** | Oct-26: 94.04% tendered; 'We expect in the next 4 to 6 weeks, max, let's say 8 weeks' for the remaining approvals (Austria, Spain). Covered by batch-2 judgment call thesis:paper-call:PERSISTENT:nagarro-deal-closes-by-mar27. |
| 2026-06-28 | Nagarro deal cash-EPS and reported-EPS accretive in year 1 (ex transaction expenses) | m&a | vague | V | 2028-03-31 | **pending** |  |
| 2026-06-28 | Net debt / combined EBITDA down to ~1x by FY2030 | debt_reduction | precise | V | 2030-03-31 | **pending** |  |
| 2026-10-15 | Further Nagarro transaction expenses of USD 25-30 mn over the next two quarters | m&a | range | V | 2027-03-31 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `IT_MIDCAPS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:PERSISTENT:fy27-ebit-16pct-plus-cred` - Persistent FY27 consolidated EBIT margin (company-reported) is >=16.0% | margin | 0.74 | 0.72 | 2027-05-31 | see specs.json |
| `thesis:paper-call:PERSISTENT:q4fy27-organic-revenue-500mn-cred` - Persistent Q4FY27 revenue excluding Nagarro is >=USD 500 mn (the re-cast 'USD 2 bn by FY27' run rate) | revenue_growth | 0.65 | 0.62 | 2027-06-30 | see specs.json |

## Sources

- https://nsearchives.nseindia.in/corporate/PERSISTENTUSER1_03072026121301_PSLInvestorCallTranscriptSubmissionSd.pdf 
- https://nsearchives.nseindia.in/corporate/PERSISTENTUSER1_20102025194609_PSLEarningscallTranscriptQ2FY26.pdf 
- https://nsearchives.nseindia.in/corporate/PERSISTENTUSER1_23102026204328_PSLTranscriptSubmissionOctober2026Sd.pdf 
- https://nsearchives.nseindia.in/corporate/PERSISTENTUSER1_27012026213814_PSLSubmissionoftheTranscriptforQ3FY26Sd.pdf 
- https://nsearchives.nseindia.in/corporate/PERSISTENTUSER1_29072025232737_PSLTranscript_of_Investors_call_recordingsigned.pdf 
- https://www.persistent.com/wp-content/uploads/2026/04/Analyst-Call-Transcript-Q4FY26.pdf 
- https://www.screener.in/company/PERSISTENT/consolidated/ 
