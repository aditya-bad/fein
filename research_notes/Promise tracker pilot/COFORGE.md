# Promise tracker: Coforge (NSE: COFORGE)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `IT_MIDCAPS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_it.json` (`analysis:COFORGE:credibility-2026-11`). Ledger source: `scripts_it_peers/promises_COFORGE.py`.

## 1. Method

- 6 calls Q1FY26-Q2FY27, all downloaded from investors.coforge.com and passed with `fetch.py --local PDF@FILED`: Coforge's NSE transcript filings are one-page cover letters with a link.
- Pipeline v1.2 (`fetch.py --since 2025-07-01`, `turns.py`, `candidates.py` with the new IT vocabulary: deal_wins / people / client_concentration categories; CC growth, TCV, EBIT band measures in `score.py`).
- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.
- Outcomes: IT KPIs (CC growth, EBIT/EBITDA margin as the company defines it, TCV, DSO, large deals) from the company's own later calls (single-source); INR revenue and screener-derived margins re-computed from screener's quarterly table as a cross-check (they differ from company EBIT/EBITDA for Persistent, Coforge and KPIT).
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 20 / 10 |
| Status counts | delivered 6, partly 4, pending 10 |
| Weighted delivery ratio | 88.3% |
| Specificity-only delivery | 85.0% |
| Raw hit rate | 60.0% |
| MCS (-1.5 .. +1) | +0.88 |
| Candour index (shortfalls admitted unprompted) | 50.0% (2/4) |
| **Sector-adjusted credibility (SAC)** | **+12.6 pts** (shrink weight 0.333 at N=10) |

By category (credit basis): margin 92.9% (n=3); other 81.8% (n=5); revenue_growth 75.0% (n=2).
SAC components: other: own 81.8% vs peer median 50.0% (n=5, gap +31.8); pooled:revenue_growth+margin: own 88.9% vs peer median 95.5% (n=5, gap -6.6).

**Caveat: n is small** (6 calls; 4-10 scored promises; most FY27 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.

## 3. Reading

- Coforge is the only explicit guider in the set: EBIT, EBITDA, FCF/PAT and ETR numbers, raised or restated almost every call, with a CEO script that cites its own past promises ('made sure they came true').
- Hard financial guidance was met or beaten: FY26 EBIT 14.4% vs 14%; Q4FY26 16.6% vs 15%; FCF/PAT 110% vs 70-80%; Encora closed inside the Mar-Apr 2026 window.
- The misses are softer statements: 'H2 should be robust' then a 2.0% CC Q4; a Q3 wage hit described as 'very, very limited' that cost 150 bp; the Cigniti merger ~2-3 months after 'December, January' (NCLT timetable, acknowledged); normalised ETR 23% vs 23.5-24%.
- FY27 is pending: EBITDA 20.5-21% (H1 20.5%), EBIT raised 15.5% -> 16% (H1 16.0%), FCF/PAT 100% (H1 92%), no EPS dilution from Encora. Reported growth is inflated by Encora from May-2026, so 'industry growth leader' needs an organic read.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-07-24 | FY26 reported EBIT margin ~14% (from ~13% in Q1, exit ~15%) | margin | precise | P | 2026-03-31 | **delivered** | FY26 reported EBIT 14.4% ('14.4% reported EBIT in FY26', Q4FY26 call; +370 bp YoY). Screener-derived (OP-dep)/sales 13.7% (hedge-loss classification differs). |
| 2025-07-24 | Q2FY26 growth to be 'equally robust' as Q1 (~6% organic CC QoQ) | revenue_growth | vague | P | 2025-09-30 | **delivered** | Q2FY26 sequential CC growth 5.9% ('sequential CC growth of 8%, 5.9%, and 4.4% recorded between Q1 and Q3', Q4FY26 call). |
| 2025-07-24 | H2FY26 to be a 'robust second half' | revenue_growth | vague | P | 2026-03-31 | **partly** | Q3FY26 +4.4% CC QoQ, Q4FY26 +2.0% CC QoQ (slowest of the year); FY26 +29.2% USD. Robust in Q3, not in Q4; the Q4 slowdown was not flagged in advance. |
| 2025-07-24 | Cigniti merger to complete by December 2025 / January 2026 ('minus a month or two') | m&a | range | P | 2026-01-31 | **partly** | Q3FY26 (23-Jan-2026): still awaiting NCLT; Q4FY26 (05-May-2026): 'Following the effective implementation of the Cigniti amalgamation' - effective around FY26 year-end (Mar-Apr 2026), ~2-3 months late, regulator-driven (NCLT meeting dates). |
| 2025-07-24 | Q3FY26 wage-hike impact to be 'very, very limited', largely offset by 80-90 bp lower ESOP cost | margin | vague | P | 2025-12-31 | **partly** | Q3FY26 EBIT 13.4%, down 60 bp QoQ: wage hikes cost 150 bp, hedge losses 90 bp; ex-hedge 14.4% (company). The wage hit was larger than 'very, very limited' but the margin was held on the company's underlying basis. |
| 2025-10-24 | Free cash flow / PAT ~70-80% on a sustained basis | other | range | P | 2026-03-31 | **delivered** | Q3FY26 110%, Q4FY26 110% (normalised 156%); FY26 FCF USD 135 mn (+68%). Guidance raised to 100% from FY27 (Q4FY26 call). |
| 2025-10-24 | Sustained effective tax rate ~23.5-24% | other | range | P | 2026-03-31 | **partly** | FY26 normalised ETR 23%, reported 13% (Cigniti-merger tax true-up, Q4 ETR -7%). Normalised is 0.5 pp below the band floor (lower tax is not adverse, but the forecast was off); FY27 guide reset to 23-24%. |
| 2026-01-23 | Q4FY26 reported EBIT margin 15% | margin | precise | V | 2026-03-31 | **delivered** | Q4FY26 EBIT 16.6% ('a record 16.6%, up 231 basis points quarter on quarter', Q4FY26 call). |
| 2026-01-23 | Encora acquisition approvals by March-April 2026, consolidation from then | m&a | range | P | 2026-04-30 | **delivered** | Q1FY27 revenue 'including two months of contribution from Encora' (US$100.7 mn) - consolidated from ~May-2026 (closing at end-April). Within the stated window. |
| 2026-01-23 | USD 550 mn 3-year term loan for Encora; no QIP needed | debt_reduction | precise | V | 2026-09-30 | **delivered** | Q1FY27: term-loan repayment schedule given (~$59 mn FY27, ~$209 mn FY28); no QIP announced through Nov-2026. |
| 2026-01-23 | Encora: no EPS dilution in FY27 for the combined business (later 'EPS accretion in FY27') | m&a | vague | V | 2027-03-31 | **pending** | Q1FY27/Q2FY27: 'we remain well on track to deliver EPS accretion in FY2027'; Q2FY27 EPS 13.3 vs 12.3 in Q1 (equity base +25%). |
| 2026-05-05 | FY27 consolidated EBITDA margin 20.5-21% (incl. Encora) | margin | range | V | 2027-03-31 | **pending** | H1FY27 20.5% ('We remain confident of the guidance of 20.5% to 21% range', Q2FY27). Screener OPM Q1/Q2 FY27 19.1% / 19.8%. |
| 2026-05-05 | FY27 consolidated EBIT margin 15.5% (incl. Encora); 16.5-17% standalone | margin | precise | V | 2027-03-31 | **pending** | Q1FY27 16.0% consolidated (organic 16.7%), Q2FY27 16.0% (standalone 17%). Raised to 16% on 2026-10-23 (acknowledged upgrade). |
| 2026-05-05 | FCF / PAT ~100% from FY27 (raised from 70-80%) | other | precise | V | 2027-03-31 | **pending** | Q1FY27 FCF $52.9 mn; Q2FY27 90% ('we expect it to be 100% for the year'); H1 conversion 92%. |
| 2026-05-05 | FY27 steady-state effective tax rate 23-24% | other | range | V | 2027-03-31 | **pending** |  |
| 2026-05-05 | From FY27, emerge as one of the highest EBITDA/EBIT performers among mid-caps while keeping revenue-growth leadership | margin | vague | V | 2027-03-31 | **pending** |  |
| 2026-07-28 | Encora acquisition/integration expenses within the USD 15 mn budget | m&a | precise | V | 2027-03-31 | **pending** | Q2FY27: 'we had guided for exceptional expenses of $15 to $16 [mn]'; 'no exceptional expenses in Q3 going forward'. |
| 2026-10-23 | FY27 consolidated EBIT 16% (raised from 15.5%); reported Q4FY27 EBIT 17% | margin | precise | V | 2027-03-31 | **pending** | H1FY27 consolidated EBIT 16.0%. |
| 2026-10-23 | Q3FY27: hope to sign eight, if not more, large deals (Q2 record was eight) | deal_wins | precise | V | 2026-12-31 | **pending** |  |
| 2026-10-23 | FY27: industry growth leader for the third consecutive year | revenue_growth | vague | V | 2027-03-31 | **pending** | Reported growth is inflated by Encora (consolidated from May-2026); organic Q2FY27 +3.8% QoQ. |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `IT_MIDCAPS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:COFORGE:fy27-ebit-16pct-plus-cred` - Coforge FY27 consolidated EBIT margin (company-reported) is >=16.0% | margin | 0.86 | 0.82 | 2027-05-31 | see specs.json |
| `thesis:paper-call:COFORGE:fy27-ebitda-20-5pct-plus-cred` - Coforge FY27 consolidated EBITDA margin (company-reported) is >=20.5% | margin | 0.86 | 0.82 | 2027-05-31 | see specs.json |
| `thesis:paper-call:COFORGE:q3fy27-eight-large-deals-cred` - Coforge reports >=8 large deals signed in Q3FY27 | other | 0.86 | 0.82 | 2027-02-28 | see specs.json |

## Sources

- https://investors.coforge.com/hubfs/Coforge%20Earnings%20Conference%20Call%20Transcript%20Q1FY26.pdf 
- https://investors.coforge.com/hubfs/Coforge-Limited-Earnings-Call-Transcript-Q2-FY26.pdf 
- https://investors.coforge.com/hubfs/Coforge-Limited-Earnings-Call-Transcript-Q2FY27-October-23-2026.pdf 
- https://investors.coforge.com/hubfs/Coforge-Limited-Earnings-Call-Transcript-Q3-FY26.pdf 
- https://investors.coforge.com/hubfs/Coforge-Limited-Earnings-Call-Transcript-Q4FY26%20_AJ.pdf 
- https://investors.coforge.com/hubfs/Coforge_Q1FY27%20Earnings%20Conference%20Call%20Transcript.pdf 
- https://www.screener.in/company/COFORGE/consolidated/ 
