# Promise tracker: Happy Forgings (NSE: HAPPYFORGE)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `AUTO_COMPONENTS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_sectors.json` (`analysis:HAPPYFORGE:credibility-2026-11`). Ledger source: `scripts_auto_peers/promises_HAPPYFORGE.py`.

## 1. Method

- Last 6 earnings calls on NSE (Q1FY26 to Q2FY27), fetched with `tools/promise_tracker/pipeline/fetch.py --since 2025-01-01`; `turns.py` + `candidates.py` (rules) produced the candidate sentences.
- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.
- Outcomes: group numbers from screener.in consolidated (re-derived: growth and OPM computed from the quarterly table); segment, SOP and order figures from the company's own later calls (single-source).
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 19 / 7 |
| Status counts | delivered 3, missed 2, moved-goalpost 1, partly 1, pending 12 |
| Weighted delivery ratio | 54.1% |
| Specificity-only delivery | 50.0% |
| Raw hit rate | 42.9% |
| MCS (-1.5 .. +1) | +0.08 |
| Candour index (shortfalls admitted unprompted) | 25.0% (1/4) |
| **Sector-adjusted credibility (SAC)** | **+3.6 pts** (shrink weight 0.259 at N=7) |

By category (credit basis): capacity 65.0% (n=4); margin 100.0% (n=1); other 0.0% (n=2).
SAC components: pooled:margin+capacity+other: own 50.0% vs peer median 46.400000000000006% (n=7, gap +3.6).

**Caveat: n is small** (6 calls; few hard numbers). No category reaches the L18 threshold of 5 scored promises with 2+ peers, except as noted, so SAC is computed on pooled categories and shrunk toward zero when used.

## 3. Reading

- Margin promises are reliable: 'sustain ~28.6%' (Aug-25) -> FY26 30.4%; every quarter since is >=30.5% on screener.
- Near-term capacity was nearly on time (10,000-t press Q4FY26 as promised; 4,000-t press one quarter late, acknowledged).
- Big-project dates are not: the INR 650 cr heavy-component plant went from 'finished by Q2-Q3 FY27' (Aug-25) to 'commence operation in Q4 FY2028' (Nov-26) while every call in between said it was on schedule. That is the clearest silent goalpost move in this peer set.
- Also missed: a US PV programme ramp promised for Nov-Dec 2025 began in Q1-Q2 FY27; a hoped-for acquisition 'in 6-8 months' never came up again.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-08-11 | Sustain EBITDA margins around the Q1FY26 peak (28.6%) going forward | margin | precise | V | 2026-03-31 | **delivered** | FY26 company EBITDA margin 30.4% (screener OPM 30.5%); every quarter Q2FY26..Q2FY27 >= 30.5% (screener). |
| 2025-08-11 | Passenger-vehicle share of revenue to rise to 8-10% within two years (from 6%) | other | range | V | 2027-08-31 | **pending** |  |
| 2025-08-11 | Commission 10,000-t and 4,000-t presses during FY26 (+~20,000 MTPA) | capacity | precise | V | 2026-03-31 | **partly** | 10,000-t line commissioned Q4FY26 (Q4FY26 call); 4,000-t press slipped to Q1FY27 ('commissioning a new forging press in Q1 FY2027', Q2FY27 call). Slip acknowledged on 2026-02-10 ('4,000 ton press in H1 FY27'). |
| 2025-08-11 | US passenger-vehicle order to ramp up from Nov-Dec 2025 | other | precise | P | 2025-12-31 | **missed** | Q2FY27 call: 'this line was commissioned for a North American client for PV application, and for which we have started ramping up in Q1 and Q2' (FY27) - about two quarters late; no explanation volunteered. |
| 2025-08-11 | INR 650 cr heavy-component capex finished by Q2-Q3 FY27 | capacity | range | P | 2026-12-31 | **moved-goalpost** | 2025-11-07 'will probably start from third quarter of next year'; 2026-02-10 'on track ... as per the schedule', utilisation 'some bit from FY28'; 2026-05-22 'by end of FY27 we expect to complete our large capex ... trials early FY28'; 2026-11-06 'going as per... |
| 2025-11-07 | Close an inorganic (M&A) deal within 6-8 months | other | precise | P | 2026-07-31 | **missed** | No acquisition announced or mentioned in the Q4FY26, Q1FY27 or Q2FY27 calls (grep 'inorganic/acquisition'); not raised again by management. |
| 2025-11-07 | Growth trajectory better from FY27 ('back on a full trend') | revenue_growth | vague | P | 2027-03-31 | **pending** | H1FY27 revenue +30% (screener). |
| 2025-11-07 | Return ratios to improve going forward | other | vague | V | 2027-03-31 | **pending** | Screener ROCE FY26 18% (FY25 19%). |
| 2026-02-10 | EBITDA margin sustained in a 29-31% range over the medium term | margin | range | V | 2028-03-31 | **pending** | FY26 30.4%; Q1FY27 31.4%, Q2FY27 30.5% (screener). |
| 2026-02-10 | New 10,000-t press in Q4FY26 and 4,000-t press in H1FY27 | capacity | precise | V | 2026-09-30 | **delivered** | 10,000-t commissioned Q4FY26 (Q4FY26 call); new forging press commissioned Q1FY27 and an extra hammer in Q2FY27 (Q2FY27 call). |
| 2026-02-10 | FY26 total capex INR 400-500 cr | capacity | range | V | 2026-03-31 | **delivered** | 'capex of around Rs.460 crores deployed during FY 26' (Q4FY26 call). (In Aug-2025 the FY26 plan was ~INR 300 cr ex-solar; raised openly.) |
| 2026-02-10 | Captive solar plant to start cutting power cost from Q3 FY27 (INR 25-30 cr p.a.) | capacity | precise | P | 2026-12-31 | **pending** | 2026-05-22: 'partial benefits starting from FY28'; 2026-11-06: 'we expect some generations to happen in Q4' - re-dated twice; goalpost flag, resolve at deadline. |
| 2026-05-22 | FY27 late-teen volume growth with EBITDA margin broadly in line with FY26 | revenue_growth | range | V | 2027-03-31 | **pending** | Restated 2026-08-05 and 2026-11-06 ('well-positioned to meet our full-year volume growth guidance'). H1FY27 finished-goods volume +24%, revenue +30%. |
| 2026-05-22 | FY27 capex INR 450-500 cr | capacity | range | V | 2027-03-31 | **pending** | H1FY27 spend ~INR 378 cr; additional INR 500 cr programme approved 2026-11-06. |
| 2026-05-22 | FY27 CV segment growth 35-40% on new programmes | revenue_growth | range | P | 2027-03-31 | **pending** | Q1FY27: CV 'healthy single-digit growth' (domestic +18%) - well short so far. |
| 2026-05-22 | Forging capacity to 161,000 t by FY27 (from 147,000) | capacity | precise | P | 2027-03-31 | **pending** |  |
| 2026-08-05 | EBITDA margin 'upwards of 30%' going forward (power savings +1-1.5 pp) | margin | precise | P | 2027-03-31 | **pending** |  |
| 2026-11-06 | Close ~INR 500 cr of new orders (data-centre / heavy) by March 2027 | other | precise | P | 2027-03-31 | **pending** | Also: 'We aim to close nearly Rs.500 crores of orders by this financial year'. |
| 2026-11-06 | Heavy-component plant (+20 MW solar) completed and operating in Q4 FY28 | capacity | precise | V | 2028-03-31 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5: P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:HAPPYFORGE:fy27-revenue-growth-17pct-plus-cred` - Happy Forgings FY27 consolidated revenue growth is >=17.0% (proxy for its late-teen volume guide) | revenue_growth | 0.65 | 0.64 | 2027-05-31 | see specs.json |
| `thesis:paper-call:HAPPYFORGE:fy27-opm-30pct-plus-cred` - Happy Forgings FY27 consolidated operating margin is >=30.0% ('broadly in line' with FY26 30.4%) | margin | 0.68 | 0.67 | 2027-05-31 | see specs.json |
| `thesis:paper-call:HAPPYFORGE:orders-500cr-by-mar27-cred` - Happy Forgings reports >=INR 450 cr of new orders won between 06-Nov-2026 and 31-Mar-2027 (target ~INR 500 cr) | other | 0.54 | 0.53 | 2027-06-15 | see specs.json |

## Sources

- https://nsearchives.nseindia.in/corporate/9876964720_11082026155459_TranscriptOfEarningsCall.pdf 
- https://nsearchives.nseindia.in/corporate/9876964720_13112025134935_TranscriptOfEarningsCall.pdf 
- https://nsearchives.nseindia.in/corporate/9876964720_13112026122617_TranscriptEarningscall13112026.pdf 
- https://nsearchives.nseindia.in/corporate/9876964720_16022026172207_TranscriptOfEarningsCall.pdf 
- https://nsearchives.nseindia.in/corporate/9876964720_18082025121524_TranscriptEarningsCall.pdf 
- https://nsearchives.nseindia.in/corporate/9876964720_28052026180252_TranscriptOfEarningsCall28052026.pdf 
- https://www.screener.in/company/HAPPYFORGE/consolidated/ 
