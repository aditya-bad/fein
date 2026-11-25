# Promise-credibility forward test — Nov-2026 cohort (12 companies, 38 forward calls)

Built 2026-11-25. Roadmap **stage 3 (signal: management credibility) → stage 7 (scorekeeping)**; answers strategy_review §4
"Does sector-adjusted credibility predict delivery better than the sector base rate?". Unlocks: credibility as a stage-6 decision-card
input if it passes; retire the rule-generated credibility calls if it fails. Research, not SEBI-registered advice.

- **Pre-registration:** [`prereg.md`](prereg.md) (sha256 990c8180…435aec, saved before the frame/draw; walk log appended below its heading).
- **Selection:** `random.Random(20261210)` over the NSE universe joined to the industry map, mcap ₹1,000–20,000 cr at the 25-Nov-2026
  bhavcopy close, sectors Capital Goods (overlaps the T&D peer ledger: KEC, KPIL, SKIPPER), Chemicals, Healthcare; ≥6 transcripts
  since Jan-2025 and ≥1 since 15-Jul-2026. 7 names skipped for missing transcripts (log in prereg.md). Order: [`selection_order.json`](selection_order.json).
- **Rule (fixed before any transcript was read):** P_base = leave-one-out sector-peer strict delivery rate in the promise's group
  (revenue / margin / dates / balance_sheet / other; fallbacks to the all-group peer rate, then the pooled cohort+T&D rate, then 0.5).
  SAC = mean(y − p0) over the company's resolved past promises; **P_cred = clip(p0 + N/(N+20)·SAC, 0.05, 0.95)**, P_cred = P_base if N < 3.
- **Decision rule:** PASS if ΔBrier = Brier(P_base) − Brier(P_cred) ≥ +0.005 with the 90% company-bootstrap CI above 0, on ≥30 resolved
  calls from ≥8 companies; FAIL if ΔB ≤ 0 or the CI's upper bound < +0.005; else INCONCLUSIVE. Tercile hit rates are secondary.
- **Files:** `build.py` (ledgers + rule → seed + specs), `ledger.json`, `specs_lines.txt`; memdb seed
  `memdb/seeds/2026-11-25_promise_forward_test.json` (38 thesis records, tags `paper-call`, `promise-forward-test`); resolver specs appended to
  `tools/scoreboard/specs.json` (ids end `-pft`).

## Honest caveats (read before using the numbers)
1. **Thin credibility evidence.** Past ledgers are N = 1–6 per company (36 promises in all; the pilots had 15–78). With the
   pre-stated shrink, P_cred moves at most ±0.10 from P_base, and 4 companies (KIRLOSBROS, GALAXYSURF, TATVA, SHILPAMED) have N < 3,
   so their P_cred = P_base. Expected |ΔBrier| is ~0.002–0.01: **INCONCLUSIVE is the most likely verdict**; this cohort is built to be
   pooled with the 38 Nov-22 credibility calls (same rule family) and future cohorts.
2. **Hand ledgers.** Claude did the LLM step from the pipeline's tier-A candidates (`candidates.py`) plus targeted text search, not a
   full read; recall is lower than a full pipeline run. Several past outcomes rest on one source (screener numbers or a single call
   remark); GALAXYSURF's FY26 volume miss is inferred from regional data.
3. **Correlated calls.** Several calls share a driver (ANUP revenue/EBITDA/order book; Shilpa's five FY27 milestones), so the bootstrap is
   over companies, not calls.
4. **Base rates are low** (dates 0.22–0.26 in Chemicals/Healthcare because the peer pools are small and mostly misses). This is the
   naive forecaster by rule, not our view.
5. Several healthcare/chemicals calls are company-defined KPIs (EBITDA/MT, cash-based revenue, segment EBITDA): resolver `assisted`,
   a human confirms from the Q4 FY27 deck/call.

## Calls by promise due month
| Due | Calls | Resolution window |
|---|---|---|
| Dec-2026 (events) | 4 | Q3 FY27 calls, Jan–Mar 2027 |
| Mar-2027 (FY27 numbers and events) | 34 | Q4 FY27 results/calls, Apr–Jun 2027 |
Structured (india_fin, auto-resolvable): 11; assisted (doc_scan): 27.
No promise due Apr–Jul 2027 passed the filter (Q1 FY28 guidance is rarely given in Q1/Q2 FY27 calls).

## Credibility table (company name + NSE ticker; SAC in probability units vs the leave-one-out sector base rate)
| Company | Sector | Mcap ₹ cr (25-Nov-26) | N past | Delivered | Hit rate | SAC | Shrink w | Adjusts P? | Tercile | Fwd calls |
|---|---|---|---|---|---|---|---|---|---|---|
| Jash Engineering (JASH) | Capital Goods | 3,235 | 5 | 1 | 20% | -0.19 | 0.20 | yes | bottom | 4 |
| Kirloskar Brothers (KIRLOSBROS) | Capital Goods | 12,423 | 1 | 0 | 0% | -0.37 | 0.05 | no (N<3) | bottom | 1 |
| Rishabh Instruments (RISHABH) | Capital Goods | 2,272 | 4 | 3 | 75% | +0.29 | 0.17 | yes | top | 3 |
| The Anup Engineering (ANUP) | Capital Goods | 3,271 | 6 | 5 | 83% | +0.44 | 0.23 | yes | top | 4 |
| Neogen Chemicals (NEOGEN) | Chemicals | 7,474 | 3 | 1 | 33% | -0.07 | 0.13 | yes | middle | 5 |
| Galaxy Surfactants (GALAXYSURF) | Chemicals | 7,071 | 2 | 1 | 50% | +0.25 | 0.09 | no (N<3) | middle | 2 |
| Yasho Industries (YASHO) | Chemicals | 4,064 | 4 | 0 | 0% | -0.45 | 0.17 | yes | bottom | 3 |
| Tatva Chintan Pharma Chem (TATVA) | Chemicals | 3,650 | 1 | 1 | 100% | +0.78 | 0.05 | no (N<3) | top | 3 |
| Krsnaa Diagnostics (KRSNAA) | Healthcare | 1,637 | 3 | 1 | 33% | -0.13 | 0.13 | yes | middle | 4 |
| Orchid Pharma (ORCHPHARMA) | Healthcare | 5,695 | 3 | 0 | 0% | -0.41 | 0.13 | yes | bottom | 2 |
| Syngene International (SYNGENE) | Healthcare | 18,237 | 3 | 1 | 33% | -0.07 | 0.13 | yes | middle | 2 |
| Shilpa Medicare (SHILPAMED) | Healthcare | 16,682 | 1 | 1 | 100% | +0.78 | 0.05 | no (N<3) | top | 5 |

Read: ANUP (+0.44) and RISHABH (+0.29) beat their sector base rate on past promises; YASHO (−0.45), ORCHPHARMA (−0.41) and JASH (−0.19)
fell short. Same pattern as L18/L26: margins are met far more often than revenue targets or dates (cohort past promises: margin 8 of 10, revenue/orders 6 of 15, dates 1 of 6). TATVA and SHILPAMED
rank "top" only on one promise each (N=1; no adjustment applied).

## Forward call list
| Due | Ticker | Claim | Group | P_cred | P_base | Resolver | id |
|---|---|---|---|---|---|---|---|
| 2026-12 | JASH | Jash Engineering (JASH) finalises the ~Rs 129 cr of orders under negotiation by 31-Dec-2026 | revenue | 0.32 | 0.36 | assisted | `thesis:paper-call:JASH:q3fy27-129cr-orders-finalised-pft` |
| 2026-12 | ORCHPHARMA | Orchid Pharma (ORCHPHARMA) commissions the cefiderocol plant by 31-Dec-2026 | dates | 0.21 | 0.26 | assisted | `thesis:paper-call:ORCHPHARMA:cefiderocol-plant-commissioned-by-dec26-pft` |
| 2026-12 | TATVA | Tatva Chintan Pharma Chem (TATVA) starts commercial production of the other two pharma products by 31-Dec-2026 | dates | 0.22 | 0.22 | assisted | `thesis:paper-call:TATVA:two-pharma-products-commercial-by-dec26-pft` |
| 2026-12 | TATVA | Tatva Chintan Pharma Chem (TATVA) begins commercial supply to its hybrid-battery electrolyte-salt customer by 31-Dec-2026 | dates | 0.22 | 0.22 | assisted | `thesis:paper-call:TATVA:hybrid-battery-commercial-supply-by-dec26-pft` |
| 2027-03 | ANUP | The Anup Engineering (ANUP) FY27 consolidated revenue >= Rs 798 cr (95% of Rs 840 cr) | revenue | 0.45 | 0.35 | structured | `thesis:paper-call:ANUP:fy27-revenue-798cr-plus-pft` |
| 2027-03 | ANUP | The Anup Engineering (ANUP) FY27 consolidated EBITDA >= Rs 114 cr (95% of Rs 120 cr) | margin | 0.64 | 0.54 | structured | `thesis:paper-call:ANUP:fy27-ebitda-114cr-plus-pft` |
| 2027-03 | ANUP | The Anup Engineering (ANUP) pending order book at 1-Apr-2027 >= Rs 760 cr (95% of Rs 800 cr) | revenue | 0.45 | 0.35 | assisted | `thesis:paper-call:ANUP:opening-order-book-apr27-760cr-plus-pft` |
| 2027-03 | ANUP | The Anup Engineering (ANUP) FY27 Mabel Engineers revenue >= Rs 62 cr (95% of Rs 65 cr) | revenue | 0.45 | 0.35 | assisted | `thesis:paper-call:ANUP:fy27-mabel-revenue-62cr-plus-pft` |
| 2027-03 | GALAXYSURF | Galaxy Surfactants (GALAXYSURF) FY27 volume growth >= 5.5% (6% less 0.5 pp) | revenue | 0.25 | 0.25 | assisted | `thesis:paper-call:GALAXYSURF:fy27-volume-growth-5p5pct-plus-pft` |
| 2027-03 | GALAXYSURF | Galaxy Surfactants (GALAXYSURF) FY27 EBITDA per MT >= Rs 22,800 (95% of Rs 24,000) | margin | 0.25 | 0.25 | assisted | `thesis:paper-call:GALAXYSURF:fy27-ebitda-per-mt-22800-plus-pft` |
| 2027-03 | JASH | Jash Engineering (JASH) FY27 consolidated revenue >= Rs 831 cr (95% of the Rs 875 cr guide) | revenue | 0.32 | 0.36 | structured | `thesis:paper-call:JASH:fy27-revenue-831cr-plus-pft` |
| 2027-03 | JASH | Jash Engineering (JASH) FY27 consolidated net profit >= Rs 100 cr | other | 0.52 | 0.56 | structured | `thesis:paper-call:JASH:fy27-pat-100cr-plus-pft` |
| 2027-03 | JASH | Jash Engineering (JASH) FY27 Rodney Hunt (USA) revenue >= USD 33.25 mn (95% of 35) | revenue | 0.32 | 0.36 | assisted | `thesis:paper-call:JASH:fy27-rodney-hunt-usd33mn-plus-pft` |
| 2027-03 | KIRLOSBROS | Kirloskar Brothers (KIRLOSBROS) FY27 standalone revenue growth >= 9.5% (double-digit less 0.5 pp tolerance) | revenue | 0.37 | 0.37 | structured | `thesis:paper-call:KIRLOSBROS:fy27-standalone-revenue-growth-9p5pct-plus-pft` |
| 2027-03 | KRSNAA | Krsnaa Diagnostics (KRSNAA) receivable days < 120 at 31-Mar-2027 | balance_sheet | 0.43 | 0.45 | assisted | `thesis:paper-call:KRSNAA:receivable-days-120-or-less-mar27-pft` |
| 2027-03 | KRSNAA | Krsnaa Diagnostics (KRSNAA) FY27 cash-based revenue >= Rs 380 cr (95% of Rs 400 cr) | revenue | 0.34 | 0.35 | assisted | `thesis:paper-call:KRSNAA:fy27-cash-based-revenue-380cr-plus-pft` |
| 2027-03 | KRSNAA | Krsnaa Diagnostics (KRSNAA) retail business EBITDA positive in Q4FY27 | margin | 0.58 | 0.59 | assisted | `thesis:paper-call:KRSNAA:retail-ebitda-positive-q4fy27-pft` |
| 2027-03 | KRSNAA | Krsnaa Diagnostics (KRSNAA) FY27 Rajasthan project revenue >= Rs 95 cr (95% of Rs 100 cr) | revenue | 0.34 | 0.35 | assisted | `thesis:paper-call:KRSNAA:fy27-rajasthan-revenue-95cr-plus-pft` |
| 2027-03 | NEOGEN | Neogen Chemicals (NEOGEN) FY27 consolidated revenue >= Rs 1,100 cr | revenue | 0.36 | 0.37 | structured | `thesis:paper-call:NEOGEN:fy27-revenue-1100cr-plus-pft` |
| 2027-03 | NEOGEN | Neogen Chemicals (NEOGEN) FY27 standalone (base business) revenue >= Rs 1,000 cr | revenue | 0.36 | 0.37 | structured | `thesis:paper-call:NEOGEN:fy27-standalone-revenue-1000cr-plus-pft` |
| 2027-03 | NEOGEN | Neogen Chemicals (NEOGEN) FY27 standalone operating margin >= 16.2% (18% - 1.5 pp - 0.3 pp tolerance) | margin | 0.55 | 0.56 | structured | `thesis:paper-call:NEOGEN:fy27-standalone-opm-16p2pct-plus-pft` |
| 2027-03 | NEOGEN | Neogen Chemicals (NEOGEN) FY27 battery-materials (Neogen Ionics + salts/electrolyte) revenue >= Rs 285 cr | revenue | 0.36 | 0.37 | assisted | `thesis:paper-call:NEOGEN:fy27-battery-revenue-285cr-plus-pft` |
| 2027-03 | NEOGEN | Neogen Chemicals (NEOGEN) working-capital days <= 180 at 31-Mar-2027 | balance_sheet | 0.43 | 0.44 | assisted | `thesis:paper-call:NEOGEN:fy27-working-capital-180-days-or-less-pft` |
| 2027-03 | ORCHPHARMA | Orchid Pharma (ORCHPHARMA) FY27 EBITDA margin >= 11.7% as the company reports it (12% less 0.3 pp) | margin | 0.54 | 0.59 | assisted | `thesis:paper-call:ORCHPHARMA:fy27-ebitda-margin-11p7pct-plus-pft` |
| 2027-03 | RISHABH | Rishabh Instruments (RISHABH) FY27 EEI adjusted EBITDA >= Rs 133 cr (95% of Rs 140 cr) | margin | 0.57 | 0.52 | assisted | `thesis:paper-call:RISHABH:fy27-eei-adj-ebitda-133cr-plus-pft` |
| 2027-03 | RISHABH | Rishabh Instruments (RISHABH) FY27 EEI segment revenue growth >= 19% (20% less tolerance) | revenue | 0.41 | 0.36 | assisted | `thesis:paper-call:RISHABH:fy27-eei-revenue-growth-19pct-plus-pft` |
| 2027-03 | RISHABH | Rishabh Instruments (RISHABH) FY27 Lumel Alucast adjusted EBITDA margin >= -0.3% (breakeven) | margin | 0.57 | 0.52 | assisted | `thesis:paper-call:RISHABH:fy27-alucast-adj-ebitda-breakeven-pft` |
| 2027-03 | SHILPAMED | Shilpa Medicare (SHILPAMED) commissions its integrated peptide manufacturing block by 31-Mar-2027 | dates | 0.22 | 0.22 | assisted | `thesis:paper-call:SHILPAMED:peptide-block-commissioned-by-mar27-pft` |
| 2027-03 | SHILPAMED | Shilpa Medicare (SHILPAMED) launches its aflibercept biosimilar in India by 31-Mar-2027 | dates | 0.22 | 0.22 | assisted | `thesis:paper-call:SHILPAMED:aflibercept-india-launch-by-mar27-pft` |
| 2027-03 | SHILPAMED | Shilpa Medicare (SHILPAMED) starts the global Phase II study of Nor-UDCA by 31-Mar-2027 | dates | 0.22 | 0.22 | assisted | `thesis:paper-call:SHILPAMED:nor-udca-global-phase2-start-by-mar27-pft` |
| 2027-03 | SHILPAMED | Shilpa Medicare (SHILPAMED) puts two biosimilars into human studies (Europe/RoW) by 31-Mar-2027 | dates | 0.22 | 0.22 | assisted | `thesis:paper-call:SHILPAMED:two-biosimilars-human-studies-by-mar27-pft` |
| 2027-03 | SHILPAMED | Shilpa Medicare (SHILPAMED) starts Phase I human studies for both NBE partnership programs (Alveolus Bio, mAb Tree) by 31-Mar-2027 | dates | 0.22 | 0.22 | assisted | `thesis:paper-call:SHILPAMED:two-nbe-phase1-by-mar27-pft` |
| 2027-03 | SYNGENE | Syngene International (SYNGENE) FY27 EBITDA margin excluding forex/hedge loss >= 23.7% (mid-20s low end 24% less 0.3 pp) | margin | 0.55 | 0.56 | assisted | `thesis:paper-call:SYNGENE:fy27-ebitda-margin-ex-fx-23p7pct-plus-pft` |
| 2027-03 | SYNGENE | Syngene International (SYNGENE) FY27 consolidated revenue growth >= -3.5% (low-single-digit decline, -3% less 0.5 pp) | revenue | 0.36 | 0.37 | structured | `thesis:paper-call:SYNGENE:fy27-revenue-decline-3p5pct-or-better-pft` |
| 2027-03 | TATVA | Tatva Chintan Pharma Chem (TATVA) FY27 consolidated revenue growth >= 23.75% (25% less 5% of target) | revenue | 0.22 | 0.22 | structured | `thesis:paper-call:TATVA:fy27-revenue-growth-23p75pct-plus-pft` |
| 2027-03 | YASHO | Yasho Industries (YASHO) FY27 consolidated operating margin >= 20.0% | margin | 0.50 | 0.58 | structured | `thesis:paper-call:YASHO:fy27-opm-20pct-plus-pft` |
| 2027-03 | YASHO | Yasho Industries (YASHO) FY27 capacity utilisation >= 69.7% (70% less 0.3 pp) | other | 0.45 | 0.53 | assisted | `thesis:paper-call:YASHO:fy27-utilisation-69p7pct-plus-pft` |
| 2027-03 | YASHO | Yasho Industries (YASHO) FY27 capex >= Rs 237.5 cr (95% of Rs 250 cr) | dates | 0.18 | 0.26 | assisted | `thesis:paper-call:YASHO:fy27-capex-237cr-plus-pft` |

## Past-promise ledger (credibility input; strict y: delivered = 1, else 0)
| Ticker | Said on | Group | Promise | Outcome | Evidence |
|---|---|---|---|---|---|
| JASH | 2025-02-13 | revenue | FY25 consolidated revenue Rs 675 cr | delivered | FY25 consolidated sales Rs 735 cr (screener) |
| JASH | 2025-08-08 | revenue | FY26 consolidated revenue Rs 860 cr (restated Rs 825 cr in Nov-25 without saying so) | not delivered | FY26 Rs 736 cr (screener) = 86% |
| JASH | 2025-08-08 | revenue | Consolidated order book Rs 1,100 cr by 31-Mar-2026 | not delivered | Q4FY26 call: Rs 899 cr as on 1-May-2026 |
| JASH | 2025-05-06 | other | Waterfront (US sub) to break even in FY26 | not delivered | Q4FY26 call: "minor increase in revenue and reduction in losses" |
| JASH | 2025-05-06 | dates | Pithampur SEZ plant commissioned Dec-2025/Jan-2026 | not delivered | Q3FY26 call (16-Feb-26): plant ready, commercial production "from the beginning of April" |
| KIRLOSBROS | 2025-05-15 | revenue | Double-digit revenue growth (FY26; "that hasn't changed") | not delivered | FY26 consolidated sales +1.0% (4,492 -> 4,538, screener); Q4FY26 call: double-digit growth "impacted" by Q1-Q3 |
| RISHABH | 2025-02-07 | margin | Lumel Alucast EBITDA breakeven in the next 1-2 quarters | delivered | Q4FY25 call: "for Q4 it is at breakeven"; Q1FY26 "successful turnaround of Lumel Alucast" |
| RISHABH | 2025-05-27 | margin | Lumel Alucast positive EBITDA by end FY26 | delivered | Q4FY26 call: Alucast adjusted EBITDA margin FY26 1.4% |
| RISHABH | 2025-08-14 | dates | Nashik MIDC/Trishala buildings complete by Mar-2026 | not delivered | Q4FY26 call: capex complete, facilities "almost ready and under commissioning"; Q1FY27 "partial commissioning" |
| RISHABH | 2025-11-17 | margin | FY26 consolidated EBITDA ~Rs 100 cr (raised to Rs 115-120 cr adjusted, Feb-26) | delivered | FY26 operating profit ~Rs 127 cr (screener 775 x 16.4%) |
| ANUP | 2025-01-31 | revenue | FY25 revenue growth ~30% | delivered | Q4FY25 call: FY25 revenue Rs 751 cr, +36.5% |
| ANUP | 2025-01-31 | margin | FY25 EBITDA margin ~23% | delivered | Q4FY25 call: EBITDA Rs 172.8 cr at 23% |
| ANUP | 2025-05-13 | revenue | FY26 revenue growth ~25% (cut to 15-20% in Aug-25, acknowledged) | not delivered | FY26 sales +12.1% (733 -> 822, screener) |
| ANUP | 2025-05-13 | margin | FY26 EBITDA margin over 20% | delivered | FY26 OPM 21.5% (screener) |
| ANUP | 2025-05-13 | dates | Kheda Phase-2 expansion commissioned by Q3FY26 | delivered | Q3FY26 call (4-Feb-26): "completed Phase 2 as planned", Kheda fully operational |
| ANUP | 2025-11-10 | revenue | Pending order book Rs 700-750 cr at 1-Apr-2026 | delivered | Q4FY26 call: pending order book ~Rs 770 cr |
| NEOGEN | 2025-02-03 | revenue | FY26 standalone revenue Rs 950-1,000 cr (withdrawn after Mar-25 Dahej fire) | not delivered | Q4FY25 call: revised to Rs 775-850 cr (acknowledged) -> withdrawn = 0 |
| NEOGEN | 2025-02-03 | margin | EBITDA margin 18% +/- 1-1.5% (FY25) | delivered | FY25 OPM 17.5% (screener) |
| NEOGEN | 2025-05-19 | dates | Dahej salts +1,100 t commissioned by Sep-2025 | not delivered | Q3FY26 call: timeline now Mar-2026 (was Dec-2025) |
| GALAXYSURF | 2025-05-19 | revenue | FY26 volume growth ~8% | not delivered | Q4FY26 call: AMET -15% in Q4, RoW +4% FY, India flattish-to-up: group volume well below 8% (inferred from regional data; single-source) |
| GALAXYSURF | 2025-05-19 | margin | FY26 EBITDA/MT Rs 20,500-21,500 | delivered | Quarterly EBITDA/MT ~20,000-20,160 in FY26 (Q1, Q3, Q4 calls) = >=95% of 20,500 (amount rule) |
| YASHO | 2025-02-12 | revenue | FY26 revenue Rs 950-1,000 cr (= 40-50% growth, restated May/Jul-25) | not delivered | FY26 sales Rs 830 cr, +22.8% (screener) |
| YASHO | 2025-05-05 | balance_sheet | Net debt/EBITDA ~3.5x by FY26 | not delivered | Q1FY27 call: 3.75x at end of Q4FY26 |
| YASHO | 2025-05-05 | other | 70% capacity utilisation by Q4FY26 | not delivered | Q3FY26 call: "could not achieve the full utilization in FY26 what we anticipated" |
| YASHO | 2025-05-05 | balance_sheet | Working capital 110-115 days by FY26 | not delivered | Q1FY26 call already re-set to ~150 days by March (unacknowledged move) |
| TATVA | 2025-05-05 | revenue | FY26 "a year of good growth" with H2 recovery | delivered | FY26 sales +32% (383 -> 506, screener) |
| KRSNAA | 2025-05-13 | balance_sheet | Receivables ~90-100 days by FY26 | not delivered | Q4FY26 call: 139 days |
| KRSNAA | 2025-08-12 | revenue | Retail ~8% of revenue by FY26 | delivered | Q4FY26 call: retail ~8% of FY26 revenue |
| KRSNAA | 2025-11-10 | margin | Retail (RPL) business breakeven in Q4FY26 | not delivered | Q2FY27 call: "operationally breakeven in the month of September [2026] more or less" |
| ORCHPHARMA | 2025-05-26 | dates | Dhanuka Laboratories merger completed within FY26 | not delivered | Q1FY27 call: merger effective 10-Jul-2026 |
| ORCHPHARMA | 2025-05-26 | revenue | Combined business revenue > Rs 1,500 cr (FY26) | not delivered | Q1FY27 call: restated FY26 combined revenue below plan (screener FY26 Rs 1,233 cr) |
| ORCHPHARMA | 2025-05-26 | margin | Combined business EBITDA ~Rs 175 cr (FY26) | not delivered | FY26 operating profit ~Rs 48 cr (screener); combined gross margin fell to 32% |
| SYNGENE | 2025-04-24 | revenue | FY26 revenue growth mid-single-digit (constant currency) | not delivered | FY26 sales +2.7% reported (3,642 -> 3,739, screener); no cc beat found |
| SYNGENE | 2025-07-24 | margin | FY26 EBITDA margin in the mid-20s | delivered | FY26 OPM 24.6% (screener) |
| SYNGENE | 2025-07-24 | dates | Bayview (US) biologics facility operational in FY26 | not delivered | Q4FY26 call: "moving toward operationalization" |
| SHILPAMED | 2025-05-26 | revenue | FY26 revenue to grow vs FY25 | delivered | FY26 sales +19.8% (1,281 -> 1,535, screener) |

## How to score (Jan–Jul 2027)
1. `tools/scoreboard/run_daily.sh` resolves the structured calls; review queue for assisted ones (company KPIs, events).
2. When ≥30 calls are resolved: per prereg §5, compute mean Brier for `probability` (P_cred) and `base_rate_probability` (P_base),
   company-cluster bootstrap 10,000× with `random.Random(20261210)`, 90% CI; report PASS / FAIL / INCONCLUSIVE, the tercile hit rates,
   `probability_raw_unshrunk` (exploratory) and the pooled result with the Nov-22 credibility calls.
3. Do not edit any call, threshold or probability after 25-Nov-2026; voids only per prereg §5.
