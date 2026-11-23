# Decision card: Kirby Corporation (US-KEX) · 2026-11-23

> Phase A: every size on this card is a **paper size** until the phase-B gate in `memory/roadmap.md` is passed.

| Card | Value |
|---|---|
| Card version | 1.1 (2026-11-23; market-specific PEAD gate, base-rate CIs/size band, v1.3 worksheet lines) · worksheet 1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode) |
| Price used | USD 122.89 on 2026-11-20 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/US-KEX_live.md) · 5 valuation worksheet |
| **Rule output** | size 0: blocked by Expected value vs hurdle (EV 1.16x vs hurdle 1.47x → below hurdle → size 0) |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:US-KEX:card-2026-11-23-5y-ge3x`, `thesis:paper-call:US-KEX:card-2026-11-23-5y-le0p5x`, `thesis:paper-call:US-KEX:card-2026-11-23-5y-blowup` |

## 1. Thesis in one line
Method-test thesis: Kirby is a cyclical, capital-heavy tank-barge operator (28% of the ~4,004-barge US inland fleet, Jones Act protected) plus an engine/power-generation distributor riding data-center backup and prime-power demand; over 5 years it compounds EPS ~4-9%/yr (pricing on a near-fixed fleet plus ~4-5%/yr buybacks) at a return on total capital close to its cost of capital (~10%), so shareholder returns track EPS plus buybacks minus any de-rating from today's ~17x forward P/E.

## 2. Variant view (what we believe that the price does not, and why we could know it)
Market (reverse DCF): at $122.89 (19.4x FY25 EPS, 17.0x the FY26 guide, 9.5x EV/EBITDA, FCF yield 6.3%) the worksheet's NOPAT-based DCF cannot reproduce the price at a 10% ROIIC; even at a 20% ROIIC (sensitivity file, written after the outputs) the price needs ~11%/yr revenue growth for 10 years or a 17% NOPAT margin (FY25 11.1%). On reported FCF the price is consistent with ~3.8% perpetual FCF growth at a 9.5% cost of equity, i.e. roughly fair if 2025's cash taxes (bonus depreciation, deferred tax $82M) persist. Our view: NO claimable mispricing, with a mild negative tilt. What the market appears to price: an inland up-cycle (utilization low-90%, term renewals 'north of inflation', newbuilds 60-70/yr only matching retirements) plus a power-generation growth story (backlog > $1.5bn, book-to-bill > 1). What we verified that cuts against it: (1) ROTC 10.4% over 2023-25 (proxy) - the business earns about its cost of capital even at good points of the cycle; (2) contract escalators slowed from +9.5% (Jan-2024) to +3-5% (Jan-2025) and term renewals were flat to low-single-digit in 2025-26 - the rate cycle has been decelerating, not accelerating; (3) 2026 inland margins are capped by fuel ($3.91/gal Q3-26 vs $2.46) with a ~120-day escalator lag, and the Jones Act waiver (17-Mar-2026, now extended to 14-Feb-2027) adds foreign-flag competition risk in coastal; (4) 21 open-market insider sales, 0 buys in 12 months (weak signal, L14); (5) receivables +36% YoY vs revenue +12% (fuel-related, but CFO 9M-26 $313M vs $358M). What would prove us wrong: FY2026 EPS above the top of the guide (>= $7.28) with 2027 term renewals up high-single digits and power-gen revenue growth > 20% - i.e. a genuine margin step-up, not a buyback-driven EPS line. Departure from the outside view: the US seasoned-stock 5-year distribution is NOT on file (base_rates.json us_seasoned_5y), so the card's 5-year probabilities are compared with an EST naive class in the deep-dive file (P(>=3x) ~10%, P(<=0.5x) ~12% for US mid caps [EST, unverified]); our P(>=3x) is lower on purpose (a ~10%-ROTC cyclical at 17x forward needs a re-rating and a supercycle to triple). Checked by thesis:paper-call:US-KEX:* (6 calls to 2027-09-30, plus the 3 card calls).

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 9.5%, TG 3.0%, ROIIC 10%): revenue CAGR n/a for 10 years at a 11.1%→11.0% NOPAT margin; or year-1 growth n/a fading to 3.0%. Base case IRR at today's price: 7.2%.
- **Scenario DCF:** probability-weighted value 70.4 (-43% vs price); bear 51.8 (-58%).
- **Twin engine, 3x in 5 yrs** from P/E 19.4: exit P/E 9.7 → EPS CAGR 43%; exit P/E 14.6 → EPS CAGR 32%; exit P/E 19.4 → EPS CAGR 25%; exit P/E 19.7 → EPS CAGR 24%; exit P/E 21.5 → EPS CAGR 22%. Track record: 4.4% diluted EPS 4.11 (2015) -> 6.33 (2025), 10 years [XBRL]; trough-to-peak 2.37 (2019) -> 6.33 is 17.8%/yr, which is cycle, not trend.
- **Temperature:** P/E 19.4; own history: NORMAL; sector: NORMAL (0.99x of sector median).
- **Cash tax:** 7.9% → 20.0% (book 24.6%); FCF includes the deferral, EPS does not.
- **Reinvestment realism:** last-5y incremental ROIC 11.7%; price-implied ROIIC on the base path none up to 300% (on this growth/margin path no ROIIC reproduces the price); no flag.
- **Exit-multiple bet (L21):** exit P/E used 13.0/16.0/19.0 vs DCF-consistent 10.0/12.3/14.4 vs own median 21.5. EV of the 5-yr multiple at the used exits 1.16x, at DCF exits 0.94x, at the own median 1.50x (hurdle 1.47x).
- Full worksheet: `tools/decision/calibration_2026-11-23/US-KEX_v13.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: S2 checklist in research_notes/Deep dives/US-KEX_live.md section 1 (SEC submissions to 23-Nov-2026; EDGAR full-text search on CIK 56047; 10-K FY2025 Items 9A/auditor report; solvency flags per tools/backtests/solvency_us/s3_flags.py at T=2026-11-23).

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal | PASS | Cash is small ($38M at Sep-2026); value sits in a physical fleet (1,148 inland barges active, 294 towboats operated) and receivables; KPMG ICFR opinion effective FY2025 |
| H1b economics implausible | PASS | Inland revenue $460.1M Q3-26 = 4,183M ton-miles x 11.0 c/tm (company-stated, re-derived); fleet 28% of the ~4,004-barge industry; peers private but the ton-mile identity cross-foots |
| H1c profits unverifiable by outsiders | PASS | Customers are large refiners/chemical makers (five KMT customers ~17% of revenue); dealer/distributor roles for MTU, Allison, Cummins, EMD (~12% of revenue) are verifiable with the OEMs |
| H2 auditor exit / qualified opinion | PASS | KPMG, unqualified FS and ICFR opinions FY2025; no 8-K 4.01 in the submissions file; one 8-K 4.02 on 10-Jul-2020 (Q1-2020 goodwill impairment understated; outside the 3-year window, graded below) |
| H3 rating 'issuer not cooperating' | PASS | US equivalent: investment-grade-priced revolver (SOFR + 87.5-150 bp by rating), $750M facility amended 26-Mar-2026 to 2031; covenants ICR >= 2.5x, debt/cap <= 60% vs 23.7% |
| H4 SME/Telegram pump | PASS | NYSE, ~$77M/day ADV (6 months), ~70% of float held by large institutions (BlackRock 10.4%, Vanguard entities ~10%, DFA 5.2%) |
| H5 related-party cash leakage | PASS | No Item 404 transactions found in the 2026 proxy text; CEO pay $6.7M (66:1 median); widely held |

| Graded flag | Status | Evidence |
|---|---|---|
| G1 pledge / insider encumbrance (US: n/a) | CLEAR | No pledging disclosed; insiders are small holders |
| G2 accounting-trouble events in 5 years | FIRED | 8-K 4.02 on 10-Jul-2020 (6.4 years ago, just outside 5y): Q1-2020 restated for ASU 2017-04 goodwill impairment error; company flagged a likely material weakness then; none since (FTS 'material weakness' 0 hits since Nov-2023) |
| G3 dilution | CLEAR | Shares 60.2M (2021) -> 52.0M (Oct-2026); 5.2M still authorised (5-Nov-2026) |
| G4 solvency set (S1/S5 US, graded red) | CLEAR | S1 0, S2 0 (EBIT/interest 10.7x), S3 0, S4 0 (buybacks 354 < FCF 406 in 2025), S5 0 |
| Q CFO/NI (question) | CLEAR | CFO/NI 1.89x FY2025; but 9M-2026 CFO $313M vs $358M with receivables +$187M since Dec-2025 |
| Q receivables growth vs revenue (question) | FIRED | AR $711M Sep-2026 vs $524M Sep-2025 (+36%) vs revenue +12%; company: timing of collections and fuel-related receivables |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD):** SUE quintile 5 (event 2026-10-28). **No PEAD gate for US stocks:** the avoid rule is calibrated on Indian data only (L19/L31); US cut-points are uncalibrated. US SUE proxy (SEC calendar-quarter EPS frames, seasonal random walk) CY2026Q3 +2.58 vs frame cut-points (-0.576/0.048/0.589/1.670, n=821) -> quintile 5; CY2026Q2 0.00 -> quintile 2. Not in an avoid window. US cut-points are uncalibrated (no US PEAD test on file).
- **Promise credibility:** 79% vs peer median 84% → sector-adjusted -5 pts (near-term guidance in 8-K Ex-99.1 releases, last 6 calls (Q2-25..Q3-26); peer = US industrials ledger (WTS 100, AOS 65.9, SSD 79.4, LECO 88.5), n=12). Hand ledger (deep dive section 7): 12 resolved items, credit 9.5 (delivered 9, partly 1, missed 2: inland utilization 'low-90%' for Q3-25 came in mid-80%, inland margins 'remain in the 20% range' came in high-teens in Q3-25). All company-level financial ranges (FY25 EPS growth, KDS revenue/margin, CFO, capex) were met; 8 FY2026 items are open and tracking at or above the top. Different sector from the peer set, so the comparison is indicative only.

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| Insider open-market sales | 2025-11 to 2026-11 | 21 sales by 10 insiders, $22.2M, 0 buys; CEO sold 29,451 (Nov-25), 34,152 (Feb-26), 18,310 (2-Nov-26 at $141.32); 8-insider cluster after Feb-2026 vesting (mostly option exercise-and-sell) | low |
| Controller retirement | 2026-10-08 | VP & Controller (30 years) retiring after the FY2026 10-K; 'no disagreement' stated | low |
| Jones Act waiver | 2026-03-17 to 2027-02-14 | Federal waiver extended three times; 10-Q risk factor added | med |
| Vanguard 13G/A at 0% | 2026-03-27 | Reporting realignment (Vanguard Portfolio Management 5.03% and Vanguard Capital Management 5.17% filed separately); not a sale | low |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| Cyclical peak risk: inland utilization low-90%, record EPS, P/E 17x forward on near-peak margins (inland ~20%) | OPEN | 2027 term renewals up >= high-single digits with utilization held >= 90% through a refinery-maintenance year | 2027-04-30 (Q1-27 release) |
| Return on capital ~ cost of capital (ROTC 10.4% 2023-25); growth via barge acquisitions at $4-8M per barge-equivalent | OPEN | ROTC > 12% in the 2026-28 performance award, or acquisitions bought below replacement cost with disclosed returns | 2027 proxy (Mar-2027) |
| Receivables +36% YoY vs revenue +12%; 9M CFO down 12% | OPEN | FY2026 CFO inside the $575-675M guide and AR/revenue back to 2025 levels | FY2026 10-K (Feb-2027) |
| Jones Act waiver (foreign-flag competition in coastal; political precedent) | OPEN | Waiver lapses on 14-Feb-2027 without renewal | 2027-02-15 |
| Power-generation concentration: new 10-K risk factor on data-center demand; 10-Q risk factor on government priorities; backlog > $1.5bn | WATCH | Backlog disclosed in a filing (not only on the call) and book-to-bill < 1 for two quarters | each quarter |
| Insider selling, 0 buys (weak, L14) | WATCH | Open-market buys by >= 2 insiders | each quarter |
| 2020 restatement (8-K 4.02, goodwill impairment); Controller retiring Q1-2027 | WATCH | Any new material weakness or a 4.01/4.02 | FY2026 10-K |
| Trailing P/E vs own history looks 'normal' (19.4 vs median 21.5) - good-but-misleading: the own band is full of depressed-EPS years | ADJUSTED | - | - |
| FY2025 FCF $406M > NOPAT $374M - good-but-misleading: deferred tax $82M (bonus depreciation) and capex ~ D&A | ADJUSTED | - | - |

**Open soft flags: 6** (4 from the deep dive, 2 graded stage-2 flag(s)), plus 3 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-23 | FY2024 EPS 4.91 | use adjusted 5.46 as the base for growth comparisons | $56.3M impairment of conventional frac inventory and a Louisiana tax-law credit (PR-Q4-25 reconciliation); proxy also uses 16% growth on 5.46 |
| 2026-11-23 | Worksheet DCF far below price | kept the pre-registered card input (ROIIC 10%); recorded a post-output ROIIC 20% sensitivity and the cash-tax explanation in the deep dive | Protocol L8 step 2: scenarios fixed before outputs; the gap is a method finding (NOPAT vs cash tax, pricing-led growth), not a reason to re-fit |
| 2026-11-23 | Vanguard 0% 13G/A | ignored as a sale | Realignment into two Vanguard entities filing separately (FIVE lesson) |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base |
|---|---|---|---|
| P(≥3x in 5 yrs) | 1% | 7.0% [95% CI 6.0%–8.1%] | 0.08x |
| P(≤0.5x in 5 yrs) | 3% | 14.2% [95% CI 12.7%–15.7%] | 0.23x |
| P(blow-up) | 2% | 10.9% [95% CI 9.6%–12.3%] | 0.18x |

Base-rate class: **US non-financial, non-utility 10-K filers, public float $500M-$10B at T, 5 yrs from 30-Jun-2015/2017/2019 (survivorship-free: EDGAR fates for unpriced firms)** (n=3125, 5-yr horizon). Source: research_notes/Backtests/base_rates_5y.md; tools/backtests/base_rates_5y/build.py on research_notes/Backtests/solvency_us_outputs/panel.csv; outputs research_notes/Backtests/base_rates_5y_outputs/results.json. Caveats: n=3125 firm-snapshots used of 3,691 in band (1,823 firms; 2,074 priced, 152 unpriced EDGAR failures, 899 unpriced acquisitions counted as neither tail; 566 unpriced alive/stopped-filing/exchange-transfer rows excluded as missing at random). 95% CIs (CIK bootstrap): P(>=3x) 6.0-8.1%, P(<=0.5x) 12.7-15.7%, P(blow-up) 9.6-12.3%. Assumption bounds (acquisitions excluded instead of neutral): P(>=3x) up to 9.8%, P(<=0.5x) up to 19.9%, blow-up up to 15.3%. Three start dates (2015: >=3x 5.4%, <=0.5x 17.3%; 2017: 5.9%, 9.9%; 2019: 9.5%, 14.9%); windows include the 2015-16 energy bust, COVID and 2022. Total return (adjusted close). Float is stale and understates controlled firms' market cap. Blow-up excludes fraud findings and misses firms that fell 80% and were then bought (unpriced).
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.30 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(≥3x in 5 yrs) is 0.08x the base rate; P(≤0.5x in 5 yrs) is 0.23x the base rate; P(blow-up) is 0.18x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 8%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.16x | 3.1% | 1.14x | 1.47x | 70.4 (-43%) | -58% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

## 7. Position size (written rule)
| Sizing step | Value |
|---|---|
| Full Kelly f* (5-yr bet vs index hurdle, scenario outcomes) | 0.0% |
| × Kelly fraction 0.25 | 0.0% |
| Cap: max % at cost (satellite tier) | 4.0% |
| Cap: liquidity (10% of ADV × 5 days ÷ portfolio) | 3835.0% |
| Rule size before gates = min(fractional Kelly, caps) | 0.0% |
| **Size after gates** (blocked by: Expected value vs hurdle) | **0.0%** |

Written rule: size = min(Kelly fraction × f*, tier cap at cost, liquidity cap); any blocking gate → 0. f* maximises E[ln(1 + f·(M/H − 1))] over the scenario outcomes (each scenario spread by 5-point Gauss-Hermite on the same σ, blow-up as a point mass), with H = the index hurdle multiple. Fractional Kelly because the inputs are opinions (strategy:thorp-kelly); tier caps from strategy:position-sizing (max 5% at cost, satellites 3.5–4%, speculative 1–3%).

## 8. Kill criteria (each one dated and checkable)
| # | Kill if… | Measured by | Check by |
|---|---|---|---|
| 1 | FY2026 or any 2027 quarter shows inland utilization below 85% (company language 'mid-80%' or lower) for two consecutive quarters | 8-K Item 2.02 Ex-99.1 | 2027-09-30 |
| 2 | Debt-to-capitalization above 35% (buybacks/acquisitions funded with debt) | 8-K Ex-99.1 / 10-Q balance sheet | 2027-09-30 |
| 3 | Jones Act waiver made permanent, or statutory change to coastwise cabotage | Federal Register / DHS / KEX 10-Q risk factors | 2027-09-30 |
| 4 | Any 8-K 4.01/4.02, material weakness, or Controller/CFO exit with disagreement | EDGAR submissions / 10-K Item 9A | 2027-09-30 |
| 5 | FY2026 CFO below $500M (working-capital drain persists) | 10-K FY2026 cash-flow statement | 2027-03-01 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. A US recession and lower refinery runs after the Middle East shock faded pushed inland utilization to the low-80s in 2027; spot rates fell 10-15%, inland margins went back to the low-teens and the P/E de-rated to 13x on lower EPS.
2. Data-center capex paused (financing or policy) and power-gen orders slipped; KDS margins fell back to mid-single digits while the inventory built for 2026 deliveries had to be worked down.
3. The Jones Act waiver was extended repeatedly and widened to inland-adjacent trades; coastal pricing broke and Washington's precedent weighed on the multiple.
4. Management kept buying back stock at $135-145 with revolver debt; when the cycle turned, debt/cap rose toward 35% just as earnings fell.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (7 rules) | no |
| Stage 3 PEAD avoid flag | not gated (US: uncalibrated); quintile 5 noted | no |
| Stage 4 soft flags | 6 open, variant view written | no |
| Expected value vs hurdle | EV 1.16x vs hurdle 1.47x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

