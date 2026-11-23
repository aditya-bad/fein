# Decision card: Automotive Axles Ltd (AUTOAXLES) · 2026-11-23

> Phase A: every size on this card is a **paper size** until the phase-B gate in `memory/roadmap.md` is passed.

| Card | Value |
|---|---|
| Card version | 1.2 (2026-11-23; India survival cap, outside-view tail anchoring in the EV/Kelly gate) · worksheet 1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode) |
| Price used | INR 1,776 on 2026-11-23 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/AUTOAXLES_live.md) · 5 valuation worksheet |
| **Rule output** | size 0: blocked by Expected value vs hurdle (EV 1.40x anchored (raw 1.49x) vs hurdle 1.76x → below hurdle → size 0) |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:AUTOAXLES:card-2026-11-23-5y-ge3x`, `thesis:paper-call:AUTOAXLES:card-2026-11-23-5y-le0p5x`, `thesis:paper-call:AUTOAXLES:card-2026-11-23-5y-blowup` |

## 1. Thesis in one line
Method-test thesis: Automotive Axles is cheap only on peak-cycle earnings (12.9x trailing, 25.8x 10-year normalised EPS); over 5 years it compounds roughly with the M&HCV cycle at a through-cycle ROIC ~15-18% while its parent (Cummins/Meritor) takes ~4.5% of sales as a technical fee under an annually renewed agreement, so the 5-year outcome is driven by cycle position in FY31-32 and the exit multiple, not by a mispricing.

## 2. Variant view (what we believe that the price does not, and why we could know it)
Market (reverse DCF and temperature): at Rs 1,776 the stock is at 12.9x trailing EPS, 8.1x EV/EBITDA net of Rs 394 cr cash, the lowest P/E on the highest earnings in its 11-year history; the market is pricing a cyclical peak (record FY27 M&HCV volume of 500k+ guided, a regulatory pre-buy to April 2027, capacity nearly full at a Rs 2,650 cr annualised run-rate). Our view: we largely AGREE that it is cheap for a reason, so there is no claimable mispricing. On 10-year normalised EPS (Rs 69) the P/E is 25.8x (warm vs own history); the last cycle took revenue -53% and EPS -81% (FY19-21) and the price -80% peak to trough. What we found that the market may be MIS-weighting, in both directions: (1, negative) like-for-like FY26 revenue was roughly flat while the industry grew ~16% - the reported +4.8% is mostly the gross-up from selling direct to OEMs at OEM prices since 1-Apr-2025 (materials fell 71.0% -> 67.5% of revenue, other expenses rose 11.7% -> 14.3% with the new Rs 97.5 cr technical fee) - so content/share per industry vehicle has lagged; (2, negative) the parent take is now an explicit 4.5%-of-sales fee to Meritor HVS India (Cummins) under a one-year agreement renewable 30-Apr-2027, structured below the shareholder-approval threshold after minority holders voted 79.5% against a Rs 2,500 cr material-RPT resolution in Dec-2024; (3, positive) the balance sheet is clean (net cash 15% of market cap, AA- ICRA, payout ~30%) and the business earned 15-22% ROIC across FY23-26, so the downside is a cyclical drawdown, not a solvency event. What would prove us wrong: FY27 revenue >= Rs 2,500 cr AND FY28 H1 revenue holding within 10% of H1 FY27 after the pre-buy (the cycle is longer than we assume), or a fee cut/stable fee with rising content per vehicle. Departure from the outside view: P(>=3x) far below the class (6% vs 21%) because a 3x needs ~25% EPS CAGR from a cyclical-peak base (twin engine); tail probabilities are anchored at w=0.6 toward the class because this stock already printed a ~0.2x drawdown in the last cycle. Checked by paper calls thesis:paper-call:AUTOAXLES:* (6 operating/fee/price calls to 2027-09-30, plus the 3 card calls).

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 12.5%, TG 5.0%, ROIIC 18%): revenue CAGR 15.8% for 10 years at a 7.7%→6.8% NOPAT margin; or year-1 growth 26.1% fading to 5.0%. Base case IRR at today's price: 10.4%.
- Feasibility: the implied path needs reinvestment above 100% of NOPAT (peak 145%) at ROIIC 18%.
- **Scenario DCF:** probability-weighted value 1,316 (-26% vs price); bear 1,107 (-38%).
- **Twin engine, 3x in 5 yrs** from P/E 25.8: exit P/E 12.9 → EPS CAGR 43%; exit P/E 18.8 → EPS CAGR 33%; exit P/E 19.3 → EPS CAGR 32%; exit P/E 20.8 → EPS CAGR 30%; exit P/E 25.8 → EPS CAGR 25%. Track record: 4.4% Peak-to-peak EPS FY19 80.43 -> FY26 108.77 = 4.4%/yr [SCR]; FY16->FY26 16.8%/yr starts from a weak base and is not used.
- **Temperature:** P/E 12.9; own history: COLD; sector: COLD (0.62x of sector median).
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- **Reinvestment realism:** last-5y incremental ROIC 21.0%; price-implied ROIIC on the base path none up to 300% (on this growth/margin path no ROIIC reproduces the price); **flag** (>5 pts): scenario bear.
- **Exit-multiple bet (L21):** exit P/E used 14.0/16.0/18.0 vs DCF-consistent 11.8/11.5/12.2 vs own median 18.8. EV of the 5-yr multiple at the used exits 1.49x, at DCF exits 1.13x, at the own median 1.73x (hurdle 1.76x).
- Full worksheet: `tools/valuation/live/AUTOAXLES.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: S2 checklist in research_notes/Deep dives/AUTOAXLES_live.md section 1 (AR FY26/FY25 auditor's reports + CARO, 774 NSE announcements to 23-Nov-2026, NSE pledge API + SHP XBRL 30-Sep-2026, ICRA letter 02-Feb-2026, tools/detectors/solvency_screen.py run 23-Nov-2026).

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal | PASS | Liquid assets Rs 407 cr at 30-Sep-2026 (cash 30.8 + other bank 206.7 + MFs 169.7) [Q2FY27 SoAL]; FY26 treasury income Rs 27 cr on ~Rs 330 cr average (~8%) [AR26 n.22]; ICRA AA-(Stable)/A1+ 02-Feb-2026 |
| H1b economics implausible | PASS | Revenue per industry M&HCV ~Rs 45k (FY26) vs ~Rs 41k (FY19); materials 67.5% with back-to-back steel pass-through; OPM 7-12% over 11 years, in line with CV component peers |
| H1c profits unverifiable by outsiders | PASS | Listed OEM customers (Customer A Rs 1,440 cr = 66% of FY26 revenue, Customer B Rs 214 cr) [AR26 n.32]; exports to Meritor group plants; trade receivables 30-90 days |
| H2 auditor exit / qualified opinion | PASS | S R Batliboi & Associates LLP unmodified FY25 and FY26 (one KAM: inventory provision); CARO 3(xviii) no resignation; the Jan-2024 'Change in Auditors' filing was an internal-auditor appointment (Deloitte), read in full |
| H3 rating 'issuer not cooperating' | PASS | ICRA AA-(Stable)/A1+ on Rs 135 cr reaffirmed 02-Feb-2026 |
| H4 SME/Telegram pump | PASS | Main board; no exchange surveillance queries 2025-26; ADV ~Rs 1-2.4 cr |
| H5 related-party cash leakage to promoter entities | PASS | Technical fee to Meritor HVS (India) Rs 97.5 cr FY26 (4.5% of sales) under a disclosed services agreement on 'arm's length' terms; OPM rose 10.6% -> 10.9% after the switch, so no evidence of leakage; graded below as an open soft flag (minority rejected the Rs 2,500 cr MRPT in Dec-2024) |

| Graded flag | Status | Evidence |
|---|---|---|
| G1 promoter pledge > 25% (v3: >50% strong red) | CLEAR | NSE pledge API 23-Nov-2026: promoter shares pledged 0 (0.00%); SHP XBRL 30-Sep-2026 encumbrance flags all false; promoters 71.04% unchanged |
| G2 accounting-trouble events in 5 years | CLEAR | None; NSE format query on the Q4 FY21 audit report resolved 27-May-2021 |
| G3 dilution | CLEAR | 1,51,11,975 shares unchanged |
| G4 solvency set (S1/S5 India) | CLEAR | solvency_screen 23-Nov-2026: grade blank, 0 flags, ICR 110.5x; only lease liabilities Rs 13 cr |
| Q CFO/PAT 5y (question) | CLEAR | FY22-26 CFO Rs 656 cr vs PAT Rs 722 cr = 0.91x [SCR] |
| Q supplier loans (CARO 3(iii)) | CLEAR | Rs 5.6 cr secured loans to five suppliers for machinery [AR26 n.37]; Rs 0.03 cr overdue (AB Auto Brakes) |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD):** SUE quintile 5 (event 2026-11-12). Avoid flag not active. Rule L19: bottom two quintiles = avoid/exit for ≥63 trading days.
- **Survival cap (v1.2):** not applicable (PEAD avoid flag not active).
- **Promise credibility:** 43% vs peer median 60% → sector-adjusted -17 pts (hand ledger, 11 calls May-2024..Nov-2026: margin, capex/SOP dates, industry forecasts, n=7). Hand ledger (LLM pipeline not run): 2 met, 2 partly/late (0.5 each), 3 missed = 43% credit. Dates slip 1-4 quarters (bus axle, capex phase 1); industry forecasts were too BEARISH twice (FY26 'flat' vs +16%; FY27 '-3 to -4%' vs record). Peer median 60% = median of UNIPARTS 64.8 / SONACOMS 83.3 / SANSERA 60.0 / HAPPYFORGE 50.0 / ENDURANCE 26.1 (AUTO_COMPONENTS_peer_comparison.md, credit basis). Not comparable in method (hand vs pipeline).

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| Material-RPT resolution rejected by minority | 2024-12-14 | Rs 2,500 cr FY26 RPT with Meritor HVS (India) rejected 79.47% against; company switched to direct OEM sales + a services agreement (fee Rs 97.5 cr FY26) | med |
| Pollution-board notices | 2025-03-19 / 2026-08-09 | KSPCB cautionary letter (Mar-2025); Water Act non-compliance notice at Mysuru STP (Jul/Aug-2026), disclosed 5 days late with reason | low |
| KMP churn | 2025-11 to 2026-11 | CFO Ranganathan S left 21-Nov-2025; Raman K CFO from 04-Feb-2026 (re-announced full-time 12-Nov-2026); two senior-management cessations Feb-2026; Hosur plant closed Feb-2025 | low |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| 'Cheap' is peak-cycle cheap (good-but-misleading): 12.9x trailing vs 25.8x on 10-year normalised EPS; FY26 industry ~480k = prior FY19 peak; FY27 pre-buy to April 2027 | OPEN | H1 FY28 revenue within 10% of H1 FY27 after the pre-buy ends | 2027-11-15 |
| Customer A = 66% of FY26 revenue (almost certainly Ashok Leyland) | OPEN | Customer A share < 55% with total revenue rising (diversification), disclosed in FY27 AR n.32 | FY27 AR (Jul-2027) |
| Parent take: technical fee to Meritor HVS (India) Rs 97.5 cr = 4.5% of sales, ~41% of FY26 core EBITDA; one-year agreement renewable 30-Apr-2027; set below the MRPT approval threshold after minority rejection | OPEN | Fee <= 4.6% of revenue in FY27 and a multi-year agreement on disclosed terms | 2027-05-15 |
| Like-for-like FY26 revenue ~flat vs industry +16% [EST from materials ratio 71.0% -> 67.5%]: content/share per vehicle lagging | OPEN | FY27 revenue growth >= industry M&HCV growth + 5 pts | 2027-05-31 |
| Capacity near full at peak (Rs 2,700 cr capacity vs Rs 2,650 cr Q2 run-rate); Rs 120 cr phase-1 capex ~2 quarters late; steel scarcity | WATCH | Phase 1 complete by Q4 FY27 and Q4 revenue > Q2 | 2027-05-31 |
| Management credibility 43% vs peer 60% (dates slip; industry forecasts too bearish) | WATCH | Tandem-axle ramp by Q4 FY27 as stated on 13-Nov-2026 | 2027-05-31 |
| KSPCB notices and a late Reg-30 disclosure | WATCH | Any closure direction or a third notice | each quarter |
| CCI order: Bharat Forge commitments on access to AAL business information | WATCH | - | FY27 AR |
| FY26 revenue +4.8% includes the direct-sales gross-up (good-but-misleading) | ADJUSTED | - | - |
| Q3 FY26 labour-code exceptional Rs 12 cr | ADJUSTED | - | - |

**Open soft flags: 5** (4 from the deep dive, 1 from stage 3: credibility -17 pts vs peers), plus 4 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-23 | Selection EV used screener cash only | true EV/EBITDA 8.1x (net cash Rs 394 cr incl. MFs) used in the worksheet; the subject stays in the tercile either way | Rule fixed before drawing; disclosed, not changed |
| 2026-11-23 | Trailing P/E 12.9 looks cold | valuation read on 10-year normalised EPS (25.8x) and cycle-position scenarios | M&HCV cycle at a record; FY19-21 analogue |
| 2026-11-23 | Promise pipeline not run | hand ledger n=7 used as the credibility read | Time budget; concall mode applies (11 transcripts exist) |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base | Anchored (w=0.60 on base) |
|---|---|---|---|---|
| P(≥3x in 5 yrs) | 6% | 21.3% [95% CI 14.1%–28.7%] | 0.26x | not anchored |
| P(≤0.5x in 5 yrs) | 4% | 11.3% [95% CI 7.0%–16.1%] | 0.32x | 8.2% |
| P(blow-up) | 3% | 15.4% [95% CI 10.2%–21.4%] | 0.20x | 10.4% |

**Outside-view anchoring (v1.2, L36):** anchored P = 0.60 × base rate + 0.40 × model for P(≤0.5x) and P(blow-up) (weight: stated). The expected-value gate and Kelly use the anchored tails; the paper calls keep the raw model probability (with the anchored one alongside), so Brier scoring can tell which was better. This is a calibration safeguard, not a change to the hurdle. The default weight is 0.5; a lower weight needs a written evidence note, never below 0.25.

Base-rate class: **India non-financial, mcap Rs 1,000-20,000 cr at T, 5 yrs from 30-Sep-2016 and 30-Sep-2018 (survivorship-free, dead firms included, stratum-weighted)** (n=208, 5-yr horizon). Source: research_notes/Backtests/base_rates_5y.md; tools/backtests/base_rates_5y/build.py on research_notes/Backtests/solvency_india_outputs/panel.csv (= hard_filters_india_v2_outputs/panel_v2.csv, same 489 rows); outputs research_notes/Backtests/base_rates_5y_outputs/results.json. Caveats: n=208 company-snapshots (54 distress-census D, 153 live L at weight 5.63, 1 delisted-other X at 4.26); 95% CIs (company bootstrap within stratum): P(>=3x) 14.1-28.7%, P(<=0.5x) 7.0-16.1%, P(blow-up) 10.2-21.4%. Two start dates only, and they disagree (2016: >=3x 16%, blow-up 21%; 2018: 26%, 10%). Price return only (no dividends, ~1%/yr). Blow-up = close <=0.2x the close at T, liquidation or compulsory delisting (no fraud field). Remaining survivorship leak toward FEWER failures (IBBI firms renamed/merged and 221 IBBI rows without identifiers missing; voluntary/merger delistings X under-covered). A survivors-only sample from the same frame says P(<=0.5x) 7% instead of 11%.
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.35 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(≥3x in 5 yrs) is 0.26x the base rate; P(≤0.5x in 5 yrs) is 0.32x the base rate; P(blow-up) is 0.20x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.49x | 8.3% | 1.43x | 1.76x | 1,316 (-26%) | -38% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

**Anchored EV (v1.2, used by the gate):** 1.40x (raw model 1.49x). Tails reweighted to P(blow-up) 10.4% and P(≤0.5x) 10.4% (floored at the anchored blow-up: a blow-up ends ≤0.5x in the model); the rest of the distribution is scaled in proportion, its shape kept.

## 7. Position size (written rule)
| Sizing step | Value |
|---|---|
| Full Kelly f* (5-yr bet vs index hurdle, anchored outcomes; raw model 0.0%) | 0.0% |
| × Kelly fraction 0.25 | 0.0% |
| Cap: max % at cost (satellite tier) | 4.0% |
| Cap: liquidity (10% of ADV × 5 days ÷ portfolio) | n/a (ADV not supplied) |
| Rule size before gates = min(fractional Kelly, caps) | 0.0% |
| **Size after gates** (blocked by: Expected value vs hurdle) | **0.0%** |

Written rule: size = min(Kelly fraction × f*, tier cap at cost, liquidity cap); any blocking gate → 0. f* maximises E[ln(1 + f·(M/H − 1))] over the scenario outcomes (each scenario spread by 5-point Gauss-Hermite on the same σ, blow-up as a point mass), with H = the index hurdle multiple. Fractional Kelly because the inputs are opinions (strategy:thorp-kelly); tier caps from strategy:position-sizing (max 5% at cost, satellites 3.5–4%, speculative 1–3%).

## 8. Kill criteria (each one dated and checkable)
| # | Kill if… | Measured by | Check by |
|---|---|---|---|
| 1 | MHVSIL services agreement renewed with technical fees above 5.0% of revenue (or a new MRPT resolution moving margin to the group) | Reg-30 filing at the 30-Apr-2027 renewal; FY27 AR n.29/n.35; H1 FY28 results | 2027-11-15 |
| 2 | FY27 core OPM (ex other income) below 10.5% | screener / NSE XBRL FY27 | 2027-05-31 |
| 3 | Customer A share above 70% while total revenue falls, or loss of a Customer A platform | FY27 AR segment note (n.32) | 2027-07-31 |
| 4 | Any promoter encumbrance, open offer, delisting proposal or merger scheme | SHP XBRL quarterly; Reg-30 | 2027-09-30 |
| 5 | Modified audit opinion, auditor resignation, or rating below AA- | Reg-30 / AR / ICRA | 2027-09-30 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. The regulatory pre-buy pulled M&HCV demand into H2 FY27; H1 FY28 industry volumes fell 20-30%, AAL revenue fell ~25% and EPS ~45%; the P/E stayed ~14x and the price fell ~40% (the FY19-20 pattern).
2. At the 30-Apr-2027 renewal Cummins/Meritor raised the technical fee, taking back the margin the Dec-2024 minority vote denied it; OPM fell 1-2 pts with no volume change.
3. Customer A dual-sourced axles on its new tractor-trailer platforms; AAL's content per industry vehicle kept lagging (as FY26 already hinted).
4. Rs 120 cr of capacity arrived at the top of the cycle and sat idle in the downturn while steel scarcity had capped the peak volumes.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (7 rules) | no |
| Stage 3 PEAD avoid flag | clear | no |
| Stage 3 survival cap | n/a | no |
| Stage 4 soft flags | 5 open, variant view written | no |
| Expected value vs hurdle | EV 1.40x anchored (raw 1.49x) vs hurdle 1.76x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

