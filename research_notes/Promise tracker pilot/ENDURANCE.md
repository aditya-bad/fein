# Promise tracker: Endurance Technologies (NSE: ENDURANCE)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*
Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `AUTO_COMPONENTS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_sectors.json` (`analysis:ENDURANCE:credibility-2026-11`). Ledger source: `scripts_auto_peers/promises_ENDURANCE.py`.

## 1. Method

- Last 6 earnings calls on NSE (Q1FY26 to Q2FY27), fetched with `tools/promise_tracker/pipeline/fetch.py --since 2025-01-01`; `turns.py` + `candidates.py` (rules) produced the candidate sentences.
- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.
- Outcomes: group numbers from screener.in consolidated (re-derived: growth and OPM computed from the quarterly table); segment, SOP and order figures from the company's own later calls (single-source).
- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.

## 2. Scores

| Measure | Value |
|---|---|
| Promises logged / scored | 20 / 9 |
| Status counts | delivered 2, missed 4, moved-goalpost 3, pending 10, unverifiable 1 |
| Weighted delivery ratio | 18.9% |
| Specificity-only delivery | 26.1% |
| Raw hit rate | 22.2% |
| MCS (-1.5 .. +1) | -0.81 |
| Candour index (shortfalls admitted unprompted) | 57.1% (4/7) |
| **Sector-adjusted credibility (SAC)** | **-43.0 pts** (shrink weight 0.31 at N=9) |

By category (credit basis): capacity 27.3% (n=8); margin 0.0% (n=1).
SAC components: capacity: own 27.3% vs peer median 65.0% (n=8, gap -37.7); pooled:margin: own 0.0% vs peer median 85.0% (n=1, gap -85.0).

**Caveat: n is small** (6 calls; few hard numbers). No category reaches the L18 threshold of 5 scored promises with 2+ peers, except as noted, so SAC is computed on pooled categories and shrunk toward zero when used.

## 3. Reading

- Endurance gives no revenue or margin guidance. It gives many dated SOP (start-of-production) promises, and those slip: dual-channel ABS by 13 months, new ABS lines by about two quarters, Chennai brakes Q2FY27 -> March 2027, Bajaj and a Chinese OEM by 2 quarters each.
- About half the slips were explained (OEM clearance, the government's ABS-mandate guidelines, which hit every brake maker); the Chennai, Bajaj and Chinese-OEM re-dates were not.
- The P&L has not suffered yet (FY26 revenue +26%, OPM flat at 13.5%), so the low score is about date reliability, not business quality. Read SOP dates from this management with a 1-2 quarter haircut.
- Q2FY27 margin was guided up on the bigger Q1 base and fell instead (12.4% -> 11.7% on screener); new-plant drag and metal prices were admitted in the next opening remarks.

## 4. Ledger

| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |
|---|---|---|---|---|---|---|---|
| 2025-08-14 | Dual-channel ABS SOP (Royal Enfield / Bajaj) next month (Sep-2025) | capacity | precise | V | 2025-09-30 | **missed** | Re-dated 2026-02-13 ('now expected to start next month, as we await the final clearance from a key OEM'), 2026-05-15 ('June 2026 for Bajaj'), 2026-08-14 ('this quarter'); 2026-11-04: 'supplies to Bajaj Auto has started in October this year' - 13 months late. E... |
| 2025-08-14 | New ABS capacity lines ready by March 2026 | capacity | precise | P | 2026-03-31 | **missed** | 2025-11-13: first 1.2 mn line 'operational in Quarter 1 FY 27', second line tied to final ABS-mandate guidelines; 2026-05-15 'SOP expected in September 2026'; 2026-08-14 'September or early October 2026'. About two quarters late; explained by the government's ... |
| 2025-11-13 | New Chennai disc-brake plant SOP in Q2 FY27 | capacity | precise | V | 2026-09-30 | **moved-goalpost** | 2026-05-15 'SOP for Royal Enfield is planned in July 2026'; 2026-08-14 'expected by next month'; 2026-11-04: 'At our new Chennai plant for disc brake assembly systems, the SOP will start in March 2027' - re-dated two quarters with no reason given. |
| 2025-11-13 | SOP for Hero MotoCorp (BMS / electronics) within FY26 | capacity | precise | V | 2026-03-31 | **delivered** | 'The SOP for Hero MotoCorp started in January 2026' (Q3FY26 call). |
| 2025-11-13 | SOP for a leading Chinese 2W OEM in Q1 FY27 | capacity | precise | V | 2026-06-30 | **moved-goalpost** | 2026-02-13: 'validation is ongoing for a leading Chinese OEM, with SOP expected in Q3 of FY 27' - re-dated by two quarters without acknowledging the change. |
| 2025-11-13 | Win more than INR 1,500 cr of new business in the next 12-18 months | other | precise | V | 2027-05-31 | **pending** | Restated verbatim 2026-02-13. |
| 2026-02-13 | FY26 India capex slightly less than INR 800 cr | capacity | precise | P | 2026-03-31 | **delivered** | 2026-08-14: 'similar to the FY 26 capex of ₹ 800 crores'. |
| 2026-02-13 | FY27 India capex to be 'much below' INR 800 cr | capacity | vague | P | 2027-03-31 | **missed** | 2026-05-15 'similar to FY 26'; 2026-08-14 'similar to the FY 26 capex of ₹ 800 crores'; 2026-11-04 'We expect capital expenditure in FY 27 to be around ₹ 1,100 crores' (consolidated 1,250). Scored before the deadline on the company's own latest guide; revision... |
| 2026-02-13 | SOP for Bajaj Auto (new product line) in Q2 FY27 | capacity | precise | V | 2026-09-30 | **moved-goalpost** | 2026-08-14 'For Bajaj Auto, SOP is expected in the next quarter'; 2026-11-04 'customer validation is in process and SOP is expected in Q4 of this financial year'. |
| 2026-02-13 | 4W drum-brake line for Tata Motors: SOP in Q1 FY27 | capacity | precise | V | 2026-06-30 | **unverifiable** | Not confirmed or re-dated in later calls read (only 'we also established our assembly line', May-26). |
| 2026-05-15 | New aluminium forging plant (fifth press) SOP in Q3 FY27 | capacity | precise | V | 2026-12-31 | **pending** | 2026-08-14 'fifth forging press with SOP expected in the next quarter'; 2026-11-04 'fifth aluminum forging press with SOP expected in Q4 of FY 27' - goalpost flag, resolve at deadline. |
| 2026-05-15 | Isuzu hybrid-model castings (Chennai) SOP by Q4 FY27 | capacity | precise | V | 2027-03-31 | **pending** | Restated 2026-08-14. |
| 2026-08-14 | Q2FY27 EBITDA margin to improve on the higher Q1 revenue base | margin | vague | P | 2026-09-30 | **missed** | Screener consolidated OPM Q1FY27 12.4% -> Q2FY27 11.7%. Q2FY27 call attributes drag to four new plants (-0.5% PBT) and steel/aluminium prices. |
| 2026-08-14 | 4W battery packs: SOP by Q4 FY27 (INR 62 cr capex) | capacity | precise | V | 2027-03-31 | **pending** |  |
| 2026-08-14 | 4W driveshaft SOP for Tata Motors next quarter (Q3 FY27) | capacity | precise | V | 2026-12-31 | **pending** | Restated 2026-11-04 'expected in this quarter'. |
| 2026-08-14 | Alloy-wheel plants at full capacity by end FY27 | capacity | vague | P | 2027-03-31 | **pending** |  |
| 2026-11-04 | Chennai disc-brake plant SOP in March 2027 (re-dated) | capacity | precise | V | 2027-03-31 | **pending** |  |
| 2026-11-04 | Driveshaft revenue to cross INR 100 cr in FY27 | revenue_growth | precise | V | 2027-03-31 | **pending** |  |
| 2026-11-04 | FY27 capex ~INR 1,100 cr standalone (INR 1,250 cr consolidated) | capacity | precise | V | 2027-03-31 | **pending** |  |
| 2026-11-04 | Book a further INR 50 cr of PSI incentives in H2 FY27 | other | precise | V | 2027-03-31 | **pending** |  |

## 5. Credibility-generated forward calls (rule-set probabilities)

Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5: P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.

| Call | Category | P(ours) | P(base) | Resolve by | Resolver |
|---|---|---|---|---|---|
| `thesis:paper-call:ENDURANCE:tata-4w-driveshaft-sop-q3fy27-cred` - Endurance starts SOP of 4W driveshafts for Tata Motors by 31-Dec-2026 | capacity | 0.33 | 0.47 | 2027-02-28 | see specs.json |
| `thesis:paper-call:ENDURANCE:chennai-disc-brake-sop-by-mar27-cred` - Endurance's new Chennai disc-brake plant starts SOP by 31-Mar-2027 | capacity | 0.33 | 0.47 | 2027-06-15 | see specs.json |
| `thesis:paper-call:ENDURANCE:fifth-forging-press-sop-by-mar27-cred` - Endurance's fifth aluminium forging press starts SOP by 31-Mar-2027 | capacity | 0.33 | 0.47 | 2027-06-15 | see specs.json |
| `thesis:paper-call:ENDURANCE:fy27-driveshaft-revenue-100cr-cred` - Endurance FY27 driveshaft revenue exceeds INR 100 cr (company-reported) | revenue_growth | 0.51 | 0.64 | 2027-06-30 | see specs.json |

## Sources

- https://nsearchives.nseindia.in/corporate/ENDURANCE_12112026183008_2026_11_12_-_Transcript_of_Earnings_Conference_Call_on_04_11_2026.pdf 
- https://nsearchives.nseindia.in/corporate/ENDURANCE_19022026174447_Transcript.pdf 
- https://nsearchives.nseindia.in/corporate/ENDURANCE_20112025174935_2025_11_20_-_Transcript_of_Earnings_Conference_Call_on_13_11_2025.pdf 
- https://nsearchives.nseindia.in/corporate/ENDURANCE_21082026161009_2026_08_21_-_Transcript_of_Earnings_Conference_Call_on_14_08_2026.pdf 
- https://nsearchives.nseindia.in/corporate/ENDURANCE_22052026142524_2026_05_22_-_Transcript_of_EarningsCall.pdf 
- https://nsearchives.nseindia.in/corporate/ENDURANCE_22082025153100_20250822TranscriptofEarningsConferenceCallon14082025.pdf 
- https://www.screener.in/company/ENDURANCE/consolidated/ 
