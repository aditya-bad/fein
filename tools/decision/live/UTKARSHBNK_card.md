# Decision card: Utkarsh Small Finance Bank Ltd (UTKARSHBNK) · 2026-11-24

> Phase A: every size on this card is a **paper size** until the phase-B gate in `memory/roadmap.md` is passed.

| Card | Value |
|---|---|
| Card version | 1.4 (2026-11-24; manual core-asset threat trigger + anchoring-lowered-tails warning, L40) · worksheet 1.1-bank (2026-11-22) |
| Price used | INR 11.71 on 2026-11-23 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/UTKARSHBNK_live.md) · 5 valuation worksheet |
| **Rule output** | size 0: blocked by Expected value vs hurdle (EV 1.29x anchored (raw 1.24x) vs hurdle 1.76x → below hurdle → size 0) |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:UTKARSHBNK:card-2026-11-24-5y-ge3x`, `thesis:paper-call:UTKARSHBNK:card-2026-11-24-5y-le0p5x`, `thesis:paper-call:UTKARSHBNK:card-2026-11-24-5y-blowup` |

## 1. Thesis in one line
Method-test thesis: Utkarsh SFB (a microfinance-born small finance bank, 1,110 outlets, GLP Rs 20,062 cr, 52% secured) lost Rs 1,151 cr in FY26 in the 2024-26 microfinance cycle, was recapitalised by a Rs 950 cr rights issue at Rs 14 (Nov-2025) and is now at PPOP +Rs 85 cr/quarter with GNPA 5.9%. The 5-year outcome depends on whether ROE climbs from about -8% (H1 FY27 annualised) to the low teens before another microfinance or MSME credit shock, and at what price the next equity raise happens.

## 2. Variant view (what we believe that the price does not, and why we could know it)
Market: Rs 11.71 = 0.78x reported book (0.82x after an assumed Rs 500 cr raise) but 1.09x CET1 book (net worth less DTA Rs 495 cr and intangibles Rs 246 cr). The Gordon read says the price needs ~11% ROE forever on reported book, ~13% on CET1 book - roughly management's FY28 target of ~15% haircut for execution risk, so the market already prices a recovery. Our view: no claimable mispricing, and the evidence leans NEGATIVE versus the company's framing: (1) the GNPA fall from 12.4% to 5.9% is mostly write-offs and ARC sales (FY26 write-offs + ARC Rs 1,743 cr > fresh slippage Rs 1,724 cr; ARC sale of Rs 1,515 cr principal for Rs 207 cr consideration), not cures; (2) Q2 FY27 PPOP (+34% QoQ) leaned on a 16% QoQ drop in personnel cost (Rs 241 -> 202 cr) while headcount rose by 164 - unexplained, unasked on the call; (3) Tier-1 fell from 15.13% to 12.78% in one quarter (intangibles deduction 53 -> 246 after the new core banking system was capitalised; DTA 495) - nobody asked; total-CRAR cushion over the 15% floor is only Rs 306 cr while management guides 25-30% loan growth, so an equity raise below book is likely; (4) loan-growth guidance has a record of misses (Nov-2025: ~25% for 2-3 years -> FY26 -1.7%; FY27 25-30% guided vs +3.8% in H1); (5) the reverse merger of the promoter holdco will turn 42.7% of the bank (held by BII, RBL Bank, NMI, Faering, Hero, responsAbility via UCL) into directly held liquid shares - a supply overhang. Positive offsets: NIM 5.1% -> 6.3%, cost of funds -50 bp, CASA + retail TD 82%, LCR 177%, X-bucket collection 99.5%, SMA down, no RBI divergence or penalty, CGFMU guarantee on ~Rs 6,500 cr of the microfinance book, and SFB peers that went through the same cycle (ESAF, Suryoday) recovered to profit. What would prove us wrong: two consecutive profitable quarters with credit cost < 2.5% and an equity raise at or above book. Departure from the outside view: P(blow-up) at the class rate (15%), P(<=0.5x) above it (21% vs 11%) because a 10.9x-levered lender with CET1 book Rs 1,907 cr lost 60% of that in one year last cycle; tails anchored at w = 0.3 with an evidence note (the class is non-financial). Checked by paper calls thesis:paper-call:UTKARSHBNK:*.

## 3. What the price implies (stage 5)
- **Reverse P/B** (CoE 12.5%, g 5.0%): P/B 0.82x fully diluted (0.78x undiluted) needs ROE **11.2% forever**; today's ROE on diluted book -6.5% means the market is using a CoE of **-9.0%**. Justified P/B on the base case's long-run ROE 13.0%: 1.07x. Base-case IRR at today's price: 12.0%.
- **Residual-income scenarios:** probability-weighted value 7.9 (-32% vs price); bear 2.1 (-82%). Exit P/B used vs RIM-consistent P/B at year 5: bear 0.60x vs 0.29x; base 0.90x vs 1.00x; bull 1.40x vs 1.41x.
- **Twin engine on book, 3x in 5 yrs** from P/B 0.82x: exit P/B 0.49x → BVPS CAGR 38%; exit P/B 0.66x → BVPS CAGR 30%; exit P/B 0.82x → BVPS CAGR 25%.
- **Temperature:** P/B 0.82x; own history: INSUFFICIENT HISTORY (n=3 < 5) (n/a of own median 0.82x); sector: COOL (0.82x of peer median). P/E -12.6.
- **Book stress:** leverage 9.16x; an extra 2% loan loss (post-tax) is 9% of book.
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- Full worksheet: `tools/valuation/live/UTKARSHBNK.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: S2 checklist in research_notes/Deep dives/UTKARSHBNK_live.md section 1 (bank form): AR FY26 (joint auditors' report, Schedule 18 notes, DF-11), Pillar 3 30-Sep-2026, 417 NSE announcements + BSE page 1 (2025, 2026), SHP XBRL 30-Sep-2026, rating letters ICRA 02-Jul-2026 / CARE 14-Jul-2026 and 03-Sep-2026, Q2 FY27 XBRL and deck.

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal (bank form: RBI balances, investments, HTM marks) | PASS | Cash + RBI balances Rs 1,368 cr and investments Rs 6,263 cr (Q2 FY27 XBRL = deck); LCR 177%, surplus liquidity ~Rs 2,540 cr (call); SR investments Rs 102.9 cr fully provided [AR26 18.4.8] |
| H1b economics implausible (NIM, yield-CoD, RoA, C/I in peer band) | PASS | Q2 FY27 yield 15.9%, CoF 7.5%, NIM 6.3%, C/I 84% (deck) - inside the MFI-SFB band; NII re-derived 909.26 - 473.95 = 435.3 (XBRL) = deck 435 |
| H1c profits unverifiable | PASS | Granular retail book (5.21 m customers); DICGC premium Rs 23.28 cr incl. GST / 1.18 / 0.12% = ~Rs 16,400 cr assessable deposits vs Rs 21,654 cr total (76%; institutional/interbank excluded) - consistent |
| H2 auditor exit / qualified opinion | PASS | FY26 joint statutory auditors: unmodified opinion (board outcome 09-May-2026); FY26 joint auditors MM Nissim & Co LLP + KKC & Associates LLP replaced Deloitte Haskins & Sells + Kirtane & Pandit (FY25); no 'Change in Auditors'/resignation filing in 417 NSE announcements - treated as RBI rotation [single-source on the reason] |
| H3 rating 'issuer not cooperating' | PASS | ICRA A- (Stable) 02-Jul-2026, CARE A- (Stable) 14-Jul-2026 and 03-Sep-2026 - cooperating; but downgraded A+ -> A (Aug-2025) -> A- (Jul-2026) |
| H4 pump pattern | PASS | Main board since IPO Jul-2023 (Rs 500 cr); 276,844 holders; 6-month ADV Rs 12.0 cr mean / 6.3 cr median [YH] |
| H5 related-party leakage / connected lending (AS-18) | PASS | AR26 18.19: holding co UCL deposits Rs 60.5 cr, rent Rs 0.08 cr, ESOP cross-charge; CSR Rs 8.16 cr to Utkarsh Welfare Foundation (KMP influence); MD remuneration Rs 2.64 cr; no loans to related parties disclosed |

| Graded flag | Status | Evidence |
|---|---|---|
| G1 promoter pledge > 25% | CLEAR | SHP XBRL 30-Sep-2026: all three encumbrance flags false; promoter (UCL) 42.67% |
| G2 accounting-trouble events in 5 years | CLEAR | SEBI settlement 10-Apr-2024 (Rs 1.24 cr, LODR violations, SCN 16-Mar-2023) - a compliance event, not a misstatement; RBI ATM cash-out penalty Rs 10,000 (Jun-2025); no RBI divergence (AR26 18.4.5) |
| G3 dilution (price x purpose x buyer) | FIRED | Rights issue Nov-2025: 67.79 cr shares at Rs 14 (8:13) = +62% shares, to recapitalise after losses; promoter UCL did not subscribe (69% -> 42.7%), specific investors (Cohesion MK, India Capital, Kotak Life, ICICI Pru Life, MIT, Singularity) took it. Next raise guided for FY28 [EST below book] |
| G4 solvency set (bank form: CRAR/CET1 vs floor, LCR, CD, ALM) | CLEAR | CRAR 17.05% vs 15% floor (cushion Rs 306 cr); Tier 1 12.78% vs 7.5%; LCR 177%; CD 80.9%; leverage ratio 6.71% (Pillar 3) - clear but thin on total capital |
| Lender signals (insight:lender-blowup-signals) | FIRED | Discount to book (0.78x) + (a) two-notch rating downgrade in 12 months, (b) GNPA improvement driven by write-offs/ARC, (c) JLG concentration Bihar 44% + UP 27% - the memdb rule 'two+ flags + discount to book = avoid' fires |
| Q CFO / other-income share | CLEAR | n/a for a lender (cash flows are balance-sheet flows); other income FY26 Rs 431 cr incl. PSLC income Rs 87 cr and write-off recoveries |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD):** SUE quintile 5 (event 2026-11-03). Avoid flag not active. Rule L19: bottom two quintiles = avoid/exit for ≥63 trading days.
- **Survival cap (v1.3):** clear: pledge 0% of promoter holding and interest cover n/ax are inside the limits (> 25% / < 1.5x).
- **Promise credibility:** not scored. Numbers on credit and margins mostly moved in the guided direction (NIM up, CoF down, credit cost down from Q4 FY26); dated quantities missed: 'material improvement in profitability after H1 FY26' (May-2025) -> H2 FY26 loss Rs 563 cr; '~25% loan growth for 2-3 years' (Nov-2025) -> FY26 -1.7%; 'asset quality to improve meaningfully from Q3' -> Q3 FY26 credit cost 9.6% vs 9.7%. Current: FY27 GLP growth 25-30% (H1 +3.8%), double-digit ROE exit Q4 FY27, FY28 ROE ~15%, NIM ~8%, C/I 70-75% FY27. Not comparable to the concall credibility scores of other sectors.

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| Tier-1 down 235 bp in one quarter | 2026-11-03 | Tier-1 CRAR 15.13% (Jun-26) -> 12.78% (Sep-26); CET1 deductions: intangibles 53.18 (Mar-26) -> 245.67 (Sep-26), DTA 473 -> 495 (Pillar 3 DF-11); not discussed on the call | med |
| Write-off-driven GNPA decline | 2026-03-31 | FY26: additions 1,724; reductions 2,119 of which write-offs 1,013 + 76, ARC sale 654; upgrades + recoveries only 375 [AR26 18.4.1] | med |
| Bihar Micro Finance Institutions Act 2026 | 2026-05-11 | Act 11 of 2026 (Gazette 11-May-2026): banks exempt from state registration but its coercive-recovery provisions apply to all lenders in Bihar (s.2(3)); Bihar = 44% of JLG, 48% of MBBL; not mentioned in AR FY26 or the May/Aug/Nov-2026 calls | med |
| Rating downgrades | 2026-07-14 | ICRA/CARE A+ -> A (Aug-2025) -> A- (Jul-2026); ICRA CD A1+ -> A1 | med |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| GNPA 12.4% -> 5.9% is mostly write-offs and ARC sales (FY26 write-offs + ARC 1,743 > slippage 1,724; ARC recovery 13.6% of principal) - good-but-misleading | OPEN | Two quarters with net slippage (additions - upgrades - recoveries) below Rs 120 cr and write-offs below Rs 60 cr | 2027-05-15 |
| 28% of book is DTA (Rs 495 cr, recognised on an 'independent expert's opinion') plus intangibles (Rs 246 cr); CET1 book Rs 1,907 cr = Rs 10.71/share | OPEN | Return to taxable profit that starts using the DTA (DTA falling) by FY28 | AR FY27 |
| Q2 FY27 personnel cost -16% QoQ (241 -> 202) with headcount +164; PPOP 85 would be ~45-50 without it | OPEN | Q3 FY27 personnel cost stays <= Rs 215 cr or the one-off is explained | 2027-02-15 |
| Total-capital cushion Rs 306 cr over the 15% floor vs guided 25-30% growth; equity raise likely in FY28, below book at today's price | OPEN | Raise at >= book, or profits that keep CRAR >= 16% while loans grow >= 15% | 2027-11-30 |
| Microfinance concentration: JLG Bihar 44% + UP 27%, MBBL Bihar 48% + UP 28%; Bihar MFI Act 2026 absent from AR FY26 and calls (L40: external fact absent from AR) | OPEN | Disclosure of the Act's impact and Bihar collection efficiency >= 99% through FY27 | 2027-05-15 |
| Guidance record: growth and profitability dates missed three times (May-2025, Nov-2025, FY27 H1) | OPEN | FY27 GLP growth >= 20% | 2027-05-15 |
| Reverse merger of UCL turns 42.7% held by PE/DFI funds (BII 13.8% of UCL, RBL Bank 8.6%, NMI 7.8%, Faering 7.7%) into direct, liquid holdings - supply overhang | WATCH | Lock-in disclosed in the NCLT order, or holders stay through the first year | 2027-06-30 |
| CGFMU (government guarantee, NCGTC) supplies provision relief (Rs 75 cr credit in Q1 FY27) and claims (Rs 80 cr submitted, Rs 209 cr NPAs in covered book); window was closed for new guarantees in Q2 (L40 government input) | WATCH | Claims paid in cash and the window reopened for FY27 disbursements | 2027-05-15 |
| NIM 5.1% -> 6.3%, CoF -50 bp, CASA + retail TD 82%, LCR 177%, X-bucket CE 99.5%, no RBI divergence or penalty | CONFIRMED | - | 2027-05-15 |

**Open soft flags: 8** (6 from the deep dive, 2 graded stage-2 flag(s)), plus 2 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-24 | Lender-blowup-signals rule ('two+ flags + discount to book = avoid') | recorded as fired; not used to change the card (method test, no verdict); the card's own gates decide size | memdb rule is a heuristic, not a pre-registered card gate |
| 2026-11-24 | Base-rate class | india_nonfin_1000_20000cr_5y used for anchoring although the subject is a lender | No lender class on file; disclosed; candidate work item |
| 2026-11-24 | Survival cap core-asset threat (v1.4) | not set: the Bihar Act exempts scheduled banks from registration; CGFMU is a credit enhancement, not the core licence | L40 checked; no expiring or contested licence/lease for the core business found |
| 2026-11-24 | Credibility score | manual guidance-bias table, no score | No bank peer median (L18) |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base | Anchored (w=0.30 on base) |
|---|---|---|---|---|
| P(≥3x in 5 yrs) | 7% | 21.3% [95% CI 14.1%–28.7%] | 0.35x | not anchored |
| P(≤0.5x in 5 yrs) | 21% | 11.3% [95% CI 7.0%–16.1%] | 1.84x | 17.9% |
| P(blow-up) | 15% | 15.4% [95% CI 10.2%–21.4%] | 0.98x | 15.1% |

**Outside-view anchoring (v1.2, L36):** anchored P = 0.30 × base rate + 0.70 × model for P(≤0.5x) and P(blow-up) (weight: evidence: Weighted LESS toward the class (w=0.3 < 0.5) because (1) the class is NON-financial - no lender class exists - and a lender at 10.9x leverage (assets / net worth) has a fatter left tail by construction; (2) documented company evidence: FY26 post-tax loss Rs 1,151 cr = 60% of today's CET1 book (Rs 1,907 cr, Pillar 3 30-Sep-2026); CRAR cushion over the 15% floor Rs 306 cr; a below-book raise is guided for FY28; microfinance cycles hit this lender in FY17 (demonetisation), FY21 (COVID) and FY25-26. Anchoring at 0.5 would pull P(<=0.5x) down from 21% to 16% on a class that cannot see bank leverage.). The expected-value gate and Kelly use the anchored tails; the paper calls keep the raw model probability (with the anchored one alongside), so Brier scoring can tell which was better. This is a calibration safeguard, not a change to the hurdle. The default weight is 0.5; a lower weight needs a written evidence note, never below 0.25.

> **WARNING: anchoring lowered documented tails — check evidence note** (P(≤0.5x): the class base rate is below our model tail, so anchoring made the card more optimistic, L40). If the model tail rests on company-specific evidence (a lease expiry, a licence dispute, a debt wall), the raw tail is the honest number: write that evidence in the deep dive and size off the raw tail by hand; the mechanical size below uses the anchored one.

Base-rate class: **India non-financial, mcap Rs 1,000-20,000 cr at T, 5 yrs from 30-Sep-2016 and 30-Sep-2018 (survivorship-free, dead firms included, stratum-weighted)** (n=208, 5-yr horizon). Source: research_notes/Backtests/base_rates_5y.md; tools/backtests/base_rates_5y/build.py on research_notes/Backtests/solvency_india_outputs/panel.csv (= hard_filters_india_v2_outputs/panel_v2.csv, same 489 rows); outputs research_notes/Backtests/base_rates_5y_outputs/results.json. Caveats: n=208 company-snapshots (54 distress-census D, 153 live L at weight 5.63, 1 delisted-other X at 4.26); 95% CIs (company bootstrap within stratum): P(>=3x) 14.1-28.7%, P(<=0.5x) 7.0-16.1%, P(blow-up) 10.2-21.4%. Two start dates only, and they disagree (2016: >=3x 16%, blow-up 21%; 2018: 26%, 10%). Price return only (no dividends, ~1%/yr). Blow-up = close <=0.2x the close at T, liquidation or compulsory delisting (no fraud field). Remaining survivorship leak toward FEWER failures (IBBI firms renamed/merged and 221 IBBI rows without identifiers missing; voluntary/merger delistings X under-covered). A survivors-only sample from the same frame says P(<=0.5x) 7% instead of 11%.
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.35 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(≥3x in 5 yrs) is 0.35x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.24x | 4.4% | 1.08x | 1.76x | 7.9 (-32%) | -82% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

**Anchored EV (v1.2, used by the gate):** 1.29x (raw model 1.24x). Tails reweighted to P(blow-up) 15.1% and P(≤0.5x) 17.9%; the rest of the distribution is scaled in proportion, its shape kept.

## 7. Position size (written rule)
| Sizing step | Value |
|---|---|
| Full Kelly f* (5-yr bet vs index hurdle, anchored outcomes; raw model 0.0%) | 0.0% |
| × Kelly fraction 0.25 | 0.0% |
| Cap: max % at cost (speculative tier) | 2.0% |
| Cap: liquidity (10% of ADV × 5 days ÷ portfolio) | n/a (ADV not supplied) |
| Rule size before gates = min(fractional Kelly, caps) | 0.0% |
| **Size after gates** (blocked by: Expected value vs hurdle) | **0.0%** |

Written rule: size = min(Kelly fraction × f*, tier cap at cost, liquidity cap); any blocking gate → 0. f* maximises E[ln(1 + f·(M/H − 1))] over the scenario outcomes (each scenario spread by 5-point Gauss-Hermite on the same σ, blow-up as a point mass), with H = the index hurdle multiple. Fractional Kelly because the inputs are opinions (strategy:thorp-kelly); tier caps from strategy:position-sizing (max 5% at cost, satellites 3.5–4%, speculative 1–3%).

## 8. Kill criteria (each one dated and checkable)
| # | Kill if… | Measured by | Check by |
|---|---|---|---|
| 1 | CRAR below 16.0% or Tier-1 below 11% at any quarter-end | Quarterly press release / Pillar 3 | 2027-11-30 |
| 2 | A quarterly loss larger than Rs 150 cr, or credit cost above 5% in any quarter of FY28 | Results XBRL / deck | 2028-03-31 |
| 3 | Equity raise priced below Rs 10 (below CET1 book per share) | Reg-30 board outcome | 2028-03-31 |
| 4 | Bihar or UP microfinance collection efficiency below 98% for two months, or a state action restricting bank MFI recovery | Deck CE table; state gazette; Reg-30 | 2027-11-30 |
| 5 | RBI divergence, supervisory action or an auditor emphasis of matter on DTA recoverability | AR FY27 notes 18.4.5 / auditor report | 2027-09-30 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. A second microfinance stress (state law, floods, election-year loan-waiver talk in UP/Bihar) arrived before the secured book was big enough; FY28 lost another Rs 600-900 cr, CRAR breached 15%, and the bank raised equity at Rs 6-7 - half today's price - to stay compliant.
2. The secured MSME/LAP, CV and wholesale books (slippages already 72% of Q2 FY27 additions) seasoned badly: LAP recoveries via SARFAESI took years, and credit cost never fell below 3%.
3. Profits returned slowly; the DTA was written down when 'virtual certainty' lapsed, and the ex-UCL PE holders sold into every rally after the reverse merger.
4. Growth guidance was chased with unsecured personal and MBBL loans to existing JLG customers - the same borrowers, a bigger ticket.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (7 rules) | no |
| Stage 3 PEAD avoid flag | clear | no |
| Stage 3 survival cap | clear | no |
| Stage 4 soft flags | 8 open, variant view written | no |
| Tail anchoring (v1.4 warning) | anchoring lowered documented tails — check evidence note: P(≤0.5x) | no |
| Expected value vs hurdle | EV 1.29x anchored (raw 1.24x) vs hurdle 1.76x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

