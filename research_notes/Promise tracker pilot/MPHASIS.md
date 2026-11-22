# Promise tracker: Mphasis (NSE: MPHASIS)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `IT_MIDCAPS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_it.json` (`analysis:MPHASIS:credibility-2026-11`). Ledger source: `scripts_it_peers/promises_MPHASIS.py`.

## 1. Method

- 6 NSE calls Q1FY26-Q2FY27. `turns.py` could not split the Mphasis layout into speaker turns (0-3 management turns in 4 calls even with `--roster`), so the reading was done on the raw `pdftotext` output. `fetch.py` mis-dated the Q1FY26 call (2025-07-01); the header date 25-Jul-2025 is used.
- Pipeline v1.2 (`fetch.py --since 2025-07-01`, `turns.py`, `candidates.py` with the new IT vocabulary: deal_wins / people / client_concentration categories; CC growth, TCV, EBIT band measures in `score.py`).
- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.
- Outcomes: IT KPIs (CC growth, EBIT/EBITDA margin as the company defines it, TCV, DSO, large deals) from the company's own later calls (single-source); INR revenue and screener-derived margins re-computed from screener's quarterly table as a cross-check (they differ from company EBIT/EBITDA for Persistent, Coforge and KPIT).
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 16 / 8 |
| Status counts | delivered 5, missed 2, moved-goalpost 1, pending 8 |
| Weighted delivery ratio | 62.0% |
| Specificity-only delivery | 58.3% |
| Raw hit rate | 62.5% |
| MCS (-1.5 .. +1) | +0.20 |
| Candour index (shortfalls admitted unprompted) | 33.3% (1/3) |
| **Sector-adjusted credibility (SAC)** | **-28.5 pts** (shrink weight 0.286 at N=8) |

By category (credit basis): margin 100.0% (n=1); other 0.0% (n=1); revenue_growth 55.6% (n=6).
SAC components: revenue_growth: own 55.6% vs peer median 82.5% (n=6, gap -26.9); pooled:margin+other: own 66.7% vs peer median 100.0% (n=2, gap -33.3).

**Caveat: n is small** (6 calls; 4-10 scored promises; most FY27 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.

## 3. Reading

- Company-level guidance was met: FY26 '~2x industry growth' (6.7% CC; 'industry' is Mphasis's own benchmark, single-source) and the 14.75-15.75% EBIT band (15.3%, every quarter inside).
- Vertical and working-capital promises were not. Logistics & Transportation: 'recover through the remainder of the year' (Jul-25) -> 'sequential growth from Q3' (Oct-25) -> 'gradually recover through FY27' (Apr-26) -> -12% QoQ in Q2FY27. The FY26 version is scored moved-goalpost (re-dated without acknowledgement).
- DSO 'normalise over the next three to four quarters' (Oct-25, 89 days) went to 105 days (Q2FY27, company-normalised). The miss was explained (remittance timing, fixed-price mix) and a new promise made: double digits in Q3FY27 - one of the calls.
- FY27 guidance was raised in Nov-2026 to low-double-digit CC growth (acquisitions included); the EBIT band is held but sits near its 14.75% floor (H1 ~14.7-14.8% on both company and screener-derived bases).

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-07-25 | FY26 revenue growth ~2x industry growth | revenue_growth | range | V | 2026-03-31 | **delivered** | FY26 CC growth 6.7% ('For the full year, revenues grew 6.7% in constant currency terms'); company: 'delivering more than 2x industry growth' (Q4FY26). 'Industry' is the company's own benchmark (large-cap peers ~2-3% CC) - single-source. |
| 2025-07-25 | FY26 EBIT margin within the 14.75-15.75% band | margin | range | V | 2026-03-31 | **delivered** | FY26 EBIT 15.3% (Q1 15.3, Q2 15.3, Q3 15.2, Q4 15.4; company). Screener-derived (OP-dep)/sales FY26 15.3%. |
| 2025-07-25 | Logistics & Transportation vertical to recover gradually through the rest of FY26 | revenue_growth | vague | V | 2026-03-31 | **moved-goalpost** | Q3FY26: 'the headwind of the Logistics in one of the major customers through the year'; Q4FY26 re-dated: 'we do expect this to gradually recover through FY27' (no acknowledgement that the FY26 expectation was missed); Q2FY27: Logistics & Transportation -12.0% ... |
| 2025-07-25 | Insurance vertical to continue its growth momentum in FY26 | revenue_growth | vague | V | 2026-03-31 | **delivered** | Q4FY26: BFS 'healthy double digits and our Insurance business actually grew even more than that'; Q1FY27 Insurance +17.8% YoY CC. |
| 2025-10-31 | Logistics & Transportation to start delivering sequential growth from Q3FY26 | revenue_growth | precise | V | 2025-12-31 | **missed** | Q3FY26 call: continuing headwind from 'one of the major customers through the year'; vertical still a drag in Q1FY27 ('a little bit more headwinded given the macro') and -12.0% QoQ in Q2FY27. Single-source (segment). |
| 2025-10-31 | DSO (89 days, up on fixed-price mix) to normalise over the next 3-4 quarters | working_capital | vague | V | 2026-09-30 | **missed** | DSO 89 (Q2FY26) -> 91 (Q3) -> ~86 adjusted (Q4) -> 95 (Q1FY27) -> 105 'after normalizing for the delayed remittances' (Q2FY27). Q2FY27: 'a quarterly aberration ... expected to get to double digit levels in Q3'. |
| 2025-10-31 | 'Decent growth' in H2FY26 (strong Q3 expected after Q1 deal ramps) | revenue_growth | vague | P | 2026-03-31 | **delivered** | Q3FY26 +1.5% QoQ CC (furlough quarter), Q4FY26 +2.5% QoQ CC; FY26 6.7% CC met the >2x guide. |
| 2026-01-22 | Direct business trending to double-digit YoY growth (template for future growth) | revenue_growth | vague | P | 2026-12-31 | **delivered** | Direct CC YoY: Q3FY26 9.6%, Q1FY27 9.9%, Q2FY27 11.3% (company). Reached 10%+ only in Q2FY27. |
| 2026-04-30 | FY27 revenue growth high single-digit to low double-digit (CC) | revenue_growth | range | V | 2027-03-31 | **pending** | Q1FY27 +8.3% YoY CC, Q2FY27 Direct +11.3% YoY CC. Raised on 2026-11-06 to 'low double digits' (acknowledged upgrade). Includes acquisitions (TAP / Red Oak). |
| 2026-04-30 | FY27 EBIT margin within the 14.75-15.75% band | margin | range | V | 2027-03-31 | **pending** | Q1FY27 down 60 bp QoQ (~14.8%; deal ramp + TAP acquisition costs); Q2FY27 flat. Screener-derived 14.8% / 14.7%. Near the floor. |
| 2026-04-30 | FY27 operating cash flow / net income ~80% | other | precise | V | 2027-03-31 | **pending** | Q1FY27 OCF $39 mn; Q2FY27 $34 mn normalised; analysts flagged a large H2 ask (Q2FY27 Q&A). |
| 2026-04-30 | Hedge losses continue in H1FY27 then taper | margin | vague | P | 2027-03-31 | **pending** |  |
| 2026-07-24 | Insurance to remain a key growth driver through FY27 | revenue_growth | vague | V | 2027-03-31 | **pending** |  |
| 2026-11-06 | FY27 revenue growth 'low double digits' (raised from HSD-LDD) | revenue_growth | range | V | 2027-03-31 | **pending** | H1FY27: Q1 +8.3% YoY CC (total), Q2 Direct +11.3% YoY CC. Raise rests on 'results already delivered' and backlog. |
| 2026-11-06 | DSO back to double digits (<100 days) in Q3FY27 | working_capital | precise | V | 2026-12-31 | **pending** |  |
| 2026-11-06 | Healthcare to emerge as a growth driver after a large deal win | revenue_growth | vague | V | 2027-09-30 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `IT_MIDCAPS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:MPHASIS:fy27-cc-growth-10pct-plus-cred` - Mphasis FY27 constant-currency revenue growth (company-reported) is >=10.0% | revenue_growth | 0.75 | 0.83 | 2027-05-31 | see specs.json |
| `thesis:paper-call:MPHASIS:fy27-ebit-in-band-cred` - Mphasis FY27 EBIT margin (company-reported) is within 14.75-15.75% | margin | 0.75 | 0.83 | 2027-05-31 | see specs.json |
| `thesis:paper-call:MPHASIS:q3fy27-dso-below-100-cred` - Mphasis Q3FY27 DSO (company-reported) is below 100 days | other | 0.75 | 0.83 | 2027-02-28 | see specs.json |

## Sources

- https://nsearchives.nseindia.in/corporate/MPHASIS_04052026185004_SE_Intimation_-_transcript_-_30_April_2026-signed.pdf 
- https://nsearchives.nseindia.in/corporate/MPHASIS_05112025182431_Intimation_of_Transcript-signed.pdf 
- https://nsearchives.nseindia.in/corporate/MPHASIS_09112026150003_Intimation_of_transcript_-_Q2FY2027.pdf 
- https://nsearchives.nseindia.in/corporate/MPHASIS_27012026181732_Intimation_of_transcript_-_22_January_2026-signed.pdf 
- https://nsearchives.nseindia.in/corporate/MPHASIS_28072026133016_Intimation_of_transcript_-_June_2026-signed.pdf 
- https://nsearchives.nseindia.in/corporate/MPHASIS_29072025155615_IntimationoftranscriptJuly2025.pdf 
- https://www.screener.in/company/MPHASIS/consolidated/ 
