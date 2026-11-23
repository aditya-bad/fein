# Decision card: The Federal Bank Ltd (FEDERALBNK) · 2026-11-22

> **TEST MATERIAL. No verdict, no buy/sell/watchlist call (lesson L9).** This card was produced to test the template. Every scenario input is an illustrative [EST]; the rule output below is what the written rules compute from those inputs, nothing more.

| Card | Value |
|---|---|
| Card version | 1.1 (2026-11-23; market-specific PEAD gate, base-rate CIs/size band, v1.3 worksheet lines) · worksheet 1.1-bank (2026-11-22) |
| Price used | INR 373.50 on 2026-11-20 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/FEDERALBNK_dryrun.md) · 5 valuation worksheet |
| **Rule output** | **Practice, no verdict.** Mechanical rule output: size 0: blocked by Stage 4 soft flags (11 open, no variant view → NO POSITION); Expected value vs hurdle (EV 1.36x vs hurdle 1.76x → below hurdle → size 0) |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:FEDERALBNK:card-2026-11-22-5y-ge3x`, `thesis:paper-call:FEDERALBNK:card-2026-11-22-5y-le0p5x`, `thesis:paper-call:FEDERALBNK:card-2026-11-22-5y-blowup` |

## 1. Thesis in one line
TEST THESIS (illustrative): a granular Kerala/NRI deposit franchise plus a mix shift to mid-yield secured loans lifts RoA from ~1.25% to ~1.4% and ROE on diluted book from ~10% to ~14%.

## 2. Variant view (what we believe that the price does not, and why we could know it)
_None written._

## 3. What the price implies (stage 5)
- **Reverse P/B** (CoE 12.5%, g 5.0%): P/B 2.24x fully diluted (2.33x undiluted) needs ROE **21.8% forever**; today's ROE on diluted book 10.1% means the market is using a CoE of **7.3%**. Justified P/B on the base case's long-run ROE 14.0%: 1.20x. Base-case IRR at today's price: 10.0%.
- **Residual-income scenarios:** probability-weighted value 187.6 (-50% vs price); bear 117.1 (-69%). Exit P/B used vs RIM-consistent P/B at year 5: bear 1.30x vs 0.75x; base 1.80x vs 1.25x; bull 2.60x vs 1.64x.
- **Twin engine on book, 3x in 5 yrs** from P/B 2.24x: exit P/B 1.34x → BVPS CAGR 38%; exit P/B 1.38x → BVPS CAGR 37%; exit P/B 1.79x → BVPS CAGR 30%; exit P/B 2.24x → BVPS CAGR 25%.
- **Temperature:** P/B 2.24x; own history: HOT (1.63x of own median 1.38x); sector: HOT (1.51x of peer median). P/E 22.1.
- **Book stress:** leverage 9.31x; an extra 2% loan loss (post-tax) is 10% of book.
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- Full worksheet: `tools/valuation/examples/FEDERALBNK.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: Dry-run §2 (AR FY26 notes 1.4.5/1.4.9/AS-18, NSE/BSE Reg-30 filings Jan-2025..Nov-2026, rating letters, NSE shareholding/pledge API).

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal (bank form: cash/RBI balances and investments verifiable; HTM/AFS marks) | PASS | Cash+RBI Rs 16,801 cr and investments Rs 84,045 cr (Sep-26 XBRL); audited, unmodified opinion FY26 |
| H1b economics implausible | PASS | NIM 3.32%, RoA 1.32%, C/I 52% sit inside the mid-size private-bank range; yield 8.70% vs CoD 5.18% re-derived |
| H1c profits outsiders cannot verify | PASS | Profit is spread + fees on a supervised balance sheet; one-offs (Rs 456 cr IT-refund interest, Rs 238 cr Q2 treasury) are disclosed and backed by IT orders filed on NSE |
| H2 auditor exit / qualified opinion | PASS | May-2026 change = RBI-mandated rotation on term completion (Suri & Co, MSKA -> Price Waterhouse LLP, K S Aiyar); FY26 opinion unmodified |
| H3 rating 'issuer not cooperating' | PASS | CARE AA+/Stable reaffirmed 9-Oct-2026; IND AA+/Stable 22-Sep-2026; CRISIL AAA FD 30-Dec-2025; S&P BBB-/Stable first rating 9-Jul-2026 |
| H4 pump pattern | PASS | Nifty constituent, 100% public float, MF 37% / FII ~29% |
| H5 related-party cash leakage | PASS | No promoter. AS-18 FY26: loans Rs 1,126 cr + NCDs Rs 235 cr to the 60.6% subsidiary Fedbank Financial (listed); KMP-relative balances ~Rs 1 cr |
| EXIT trigger: RBI NPA divergence | PASS | AR FY26 note 1.4.5: divergence for FY25 and FY24 below the disclosure threshold |
| EXIT trigger: restatement / delayed results | PASS | No restatement filings Jan-2025..Nov-2026; results 16 days after quarter-end |

| Graded flag | Status | Evidence |
|---|---|---|
| Pledge > 25% of promoter holding | CLEAR | No promoter (NSE shareholding 30-Sep-2026: promoter 0%); pledge API 0 rows |
| Accounting-trouble events within 5 yrs | CLEAR | RBI penalty Rs 27.3 lakh (Feb-2025, deposit-interest directions); GST order set aside (13-Nov-2026). Minor |
| Solvency: capital (CET1 vs floor) | CLEAR | CET1 15.76% (Sep-26 XBRL) vs management floor 12%; leverage ratio 8.42% (FY26) |
| Solvency: funding concentration (lender form) | FIRED | Kerala = 58.8% of deposits (Ind-Ra, Q1FY27); NR deposits 34.7% of deposits; FCNR(B) +239% YoY via the 2026 special window. Granular (<Rs 3 cr) share fell 85% -> 81% in one quarter |
| Frauds reported (value trend) | FIRED | Rs 207 cr FY26 vs Rs 79 cr FY25 (AR note 1.4.9); count fell 3,803 -> 510. A question, not a disqualifier |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD):** SUE quintile 5 (event 2026-10-16). Avoid flag not active. Rule L19: bottom two quintiles = avoid/exit for ≥63 trading days.
- **Promise credibility:** 93% absolute (, n=9). **No peer base rate → not usable as a signal (L18).** Pipeline + manual LLM step on 6 calls (Q4FY25-Q2FY27, Q2FY26 transcript blocked): 29 promises, 9 resolved, MCS +0.93. NOT USABLE (L18): no bank peer base, n_resolved < 5 per category, and guidance looks conservative (NIM guided -5-10 bps, delivered +12). 3 unacknowledged goalpost changes (C/I ceiling 53.5 -> 55 -> 56; CASA 36% '3 years' -> 'at some point').

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| CEO tenure | 2027-09 | MD & CEO KVS Manian appointed for 3 years from Sep-2024 (Ind-Ra); RBI re-approval or succession inside the 5-yr window | med |
| M&A rumours | 2026-09-25 / 2026-10-19 | Jana SFB 'final stages' report; company: no material event. MFI-type acquisition questioned on the Q2 call | med |
| Regulatory transition | 2027-04-01 | ECL provisioning: one-time 1.5-2% of net worth guided | med |
| Capital overhang | 2027 | Blackstone warrants: Rs 4,647 cr due on exercise (27.3 cr shares, ~10% dilution at Rs 227) | low |
| Auditor rotation | 2026-05-15 | RBI-mandated rotation; new joint auditors audit FY27 | low |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| Loan/deposit/retail growth inflated by the FCNR special window (Rs 9,438 cr loans against FCNR deposits; Rs 14,922 cr mobilised) | OPEN | Core retail (ex FCNR-backed) growing >= 12% for two quarters; NIM ex-FCNR disclosed | Q4 FY27 |
| GNPA 'decadal low' is write-off driven (Q2 write-offs Rs 498 cr > fresh slippage Rs 420 cr) | OPEN | GNPA flat or lower with write-offs below slippages for two quarters | Q4 FY27 |
| Kerala 59% of deposits; NR deposits 35%; Gulf remittance cycle | OPEN | Kerala share < 50% and NR share stable through a Gulf slowdown | FY27 AR |
| Opex +25% YoY in Q2; C/I guidance ceiling drifted 53.5% -> 56% then 'around 52%' | OPEN | FY27 C/I <= 53% with opex growth <= revenue growth | Q4 FY27 |
| Gold loans +37% YoY, LTV up from ~55% to ~61% in a quarter, PSU price competition | OPEN | LTV back below 60% and gold credit cost < 20 bps through a gold-price fall | each quarter |
| Excess capital (Rs 4,647 cr to come) + inorganic appetite (Jana SFB / MFI rumours) | OPEN | Capital deployed organically at RoRWA >= 2.2%; any deal priced < 1.5x book with disclosed asset quality | 2027-09-30 |
| Valuation HOT: P/B 2.24x diluted vs own 10-yr median 1.38x and peer median 1.48x | OPEN | ROE on diluted book >= 15% sustained (justifies ~1.4x at CoE 12.5%; more at lower CoE) | stage 5 |
| Fintech-partner dependence (AR: 'resumption of business with a key fintech partner') | OPEN | Partner list, share of cards/deposits sourced via partners, any RBI direction | ground check |
| ESOP fair-value cost called 'one-time' while the policy change is recurring | OPEN | Q3/Q4 FY27 employee cost without a Rs 30 cr+/qtr step | Q3 FY27 |
| PCR 87% partly a one-time buffer funded by IT-refund interest (Q4 FY26) | ADJUSTED | - | - |
| Q2 FY27 treasury Rs 238 cr (management: 'may not repeat') | ADJUSTED | - | - |
| CEO 3-yr term ends Sep-2027 | WATCH | RBI re-approval or a named internal successor | 2027-06-30 |
| ECL transition 1.5-2% of net worth on 1-Apr-2027 | WATCH | Gross impact > 2.5% of NW or no use of the buffer | 2027-07-31 |

**Open soft flags: 11** (9 from the deep dive, 2 graded stage-2 flag(s)), plus 2 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-22 | Q4 FY26 one-offs | use company 'excl one-off' NIM 3.20 / C/I 52.86 / credit cost 47 bps / PAT 1,145 for trend and scoring | IT orders on NSE (19-Feb, 26/27-Mar-2026) total Rs 1,499 cr refund incl. interest; Rs 456 cr interest booked; ~Rs 470 cr buffer provision |
| 2026-11-22 | Q2 FY27 treasury | normalised PAT removes ~Rs 104 cr post-tax treasury above a Rs 100 cr/qtr run-rate | Fee table slide 20: treasury 238 vs 12-126 in the prior four quarters |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base |
|---|---|---|---|
| P(≥3x in 5 yrs) | 3% | n/a | n/a |
| P(≤0.5x in 5 yrs) | 3% | n/a | n/a |
| P(blow-up) | 2% | n/a | n/a |

Base-rate class: none chosen.
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.30 (worksheet block b). They are only as good as the scenario inputs.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.36x | 6.4% | 1.30x | 1.76x | 187.6 (-50%) | -69% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

## 7. Position size (written rule)
| Sizing step | Value |
|---|---|
| Full Kelly f* (5-yr bet vs index hurdle, scenario outcomes) | 0.0% |
| × Kelly fraction 0.25 | 0.0% |
| Cap: max % at cost (satellite tier) | 4.0% |
| Cap: liquidity (10% of ADV × 5 days ÷ portfolio) | n/a (ADV not supplied) |
| Rule size before gates = min(fractional Kelly, caps) | 0.0% |
| **Size after gates** (blocked by: Stage 4 soft flags; Expected value vs hurdle) | **0.0%** |

Written rule: size = min(Kelly fraction × f*, tier cap at cost, liquidity cap); any blocking gate → 0. f* maximises E[ln(1 + f·(M/H − 1))] over the scenario outcomes (each scenario spread by 5-point Gauss-Hermite on the same σ, blow-up as a point mass), with H = the index hurdle multiple. Fractional Kelly because the inputs are opinions (strategy:thorp-kelly); tier caps from strategy:position-sizing (max 5% at cost, satellites 3.5–4%, speculative 1–3%).

_Practice mode: this is the mechanical output of the rule on illustrative inputs, NOT a position size for anyone._

## 8. Kill criteria (each one dated and checkable)
| # | Kill if… | Measured by | Check by |
|---|---|---|---|
| 1 | Core retail growth (ex FCNR-backed loans) below 8% YoY in Q4 FY27 | investor deck retail mix slide | 2027-05-15 |
| 2 | Gross slippage ratio above 1.0% annualised in any quarter of FY28 | investor deck slippage slide | 2028-05-15 |
| 3 | FY27 cost-to-income above 54% (company definition) | Q4 FY27 deck | 2027-05-15 |
| 4 | An acquisition at > 2x book or into unsecured MFI/SFB without disclosed asset quality | Reg-30 filings | 2028-03-31 |
| 5 | RBI divergence disclosure appears, or an RBI direction on a fintech partnership | AR note 'Divergence'; Reg-30 | 2027-08-31 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. The FCNR window closed and its loans ran off; underlying loan growth was ~12%, not 18-22%, and NIM gains reversed as term deposits repriced up after the Oct-2026 repo hike.
2. A Gulf slowdown cut NRI remittances; Kerala deposits (59%) grew slower and CASA stalled at ~32%, so the 36% target and the RoA path both slipped.
3. Gold prices fell 20%; LTVs near 60-65% forced auctions and the gold book's credit cost rose while PSU banks undercut pricing.
4. The bank used the Blackstone capital to buy an SFB/MFI at a premium; credit cost rose to 80-100 bps and the market de-rated it from 2.2x to its 1.4x median book.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (9 rules) | no |
| Stage 3 PEAD avoid flag | clear | no |
| Stage 4 soft flags | 11 open, no variant view → NO POSITION | yes |
| Expected value vs hurdle | EV 1.36x vs hurdle 1.76x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

