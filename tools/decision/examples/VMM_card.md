# Decision card: Vishal Mega Mart (VMM) · 2026-11-21

> **TEST MATERIAL. No verdict, no buy/sell/watchlist call (lesson L9).** This card was produced to test the template. Every scenario input is an illustrative [EST]; the rule output below is what the written rules compute from those inputs, nothing more.

| Card | Value |
|---|---|
| Card version | 1.0 (2026-11-21) · worksheet 1.0 (2026-11-21) |
| Price used | INR 91.50 on 2026-11-20 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/VMM_practice.md) · 5 valuation worksheet |
| **Rule output** | **Practice, no verdict.** Mechanical rule output: size 0: blocked by Stage 2 hard filters (INCOMPLETE: 2 of 7 rules unchecked (H3 rating 'issuer not cooperating', H5 related-party cash leakage to promoter entities) → size 0 until checked); Stage 4 soft flags (8 open, no variant view → NO POSITION); Expected value vs hurdle (EV 1.46x vs hurdle 1.76x → below hurdle → size 0) |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:VMM:card-2026-11-21-5y-ge3x`, `thesis:paper-call:VMM:card-2026-11-21-5y-le0p5x`, `thesis:paper-call:VMM:card-2026-11-21-5y-blowup` |

## 1. Thesis in one line
TEST THESIS (illustrative): a value retailer for Tier II/III India keeps adding ~100+ stores a year at network-average density, so revenue compounds ~18% while pre-Ind AS EBITDA margin holds near 10%.

## 2. Variant view (what we believe that the price does not, and why we could know it)
_None written._

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 12.5%, TG 5.0%, ROIIC 30%): revenue CAGR 30.0% for 10 years at a 6.2%→7.0% NOPAT margin; or year-1 growth 53.7% fading to 5.0%. Base case IRR at today's price: 8.2%.
- Feasibility: the implied path needs reinvestment above 100% of NOPAT (peak 179%) at ROIIC 30%.
- **Scenario DCF:** probability-weighted value 32.2 (-65% vs price); bear 18.5 (-80%).
- **Twin engine, 3x in 5 yrs** from P/E 47.7: exit P/E 23.9 → EPS CAGR 43%; exit P/E 35.8 → EPS CAGR 32%; exit P/E 47.7 → EPS CAGR 25%; exit P/E 55.1 → EPS CAGR 21%. Track record: 30.0% FY24-26 (2 years only; IPO Dec-2024) [practice file].
- **Temperature:** P/E 47.7; own history: INSUFFICIENT HISTORY (n=2 < 5); sector: COOL (0.87x of sector median).
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- Full worksheet: `tools/valuation/examples/VMM.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: VMM practice deep dive §4-§6 (AR26, BRSR26, UDRHP). VMM is not in the hard-filter Part B sample (listed Dec-2024).

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal | PASS | Bank debt nil; bank interest ~Rs 1.8 cr; no cash/borrowing mismatch seen [AR26] |
| H1b economics implausible | PASS | Store P&L rebuilt (§1.4); density and margins plausible vs DMart/V2 |
| H1c profits unverifiable by outsiders | PASS | Store counts, area, BRSR headcount and wage data are checkable on the ground |
| H2 auditor exit / qualified opinion | PASS | No qualification in AR26 (shrinkage is a Key Audit Matter, not a qualification) |
| H3 rating 'issuer not cooperating' | UNKNOWN | Not checked in the practice run |
| H4 SME/Telegram pump | PASS | Main-board large cap, ~20 brokers cover it |
| H5 related-party cash leakage to promoter entities | UNKNOWN | ~Rs 103 cr/yr logistics to the controlling shareholder's entity (Samayat), share of transport cost doubled; arm's length unproven -> graded as an open soft flag, hard status unresolved |

| Graded flag | Status | Evidence |
|---|---|---|
| G4 trailing P/E > 50 or > 2x own median | CLEAR | P/E 47.7 (screener TTM); own median not computable (2 points) |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD) avoid flag:** no live quintile. Live PEAD tracker starts Q3 FY27; Q2 FY27 (Oct-2026) SUE not computed for VMM.
- **Promise credibility:** not scored. Promise tracker not run on VMM.

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| promoter/PE supply | 2025-2026 | PE promoter sold ~58% of its stake in 18 months via blocks (Rs 110-117); ~40% left | med |
| ESOP grant (Reg 30) | 2026-08-21 | 4.68 cr options to the MD at Rs 102.60 (above CMP) | low |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| P/E 47.7: own-median test impossible | OPEN | 4 quarters of SSSG < 8% | Q4 FY27 |
| Women's median pay < minimum wage (likely part-year tenure) | OPEN | Staff interviews | next visit |
| Payables days 95 -> 46 | OPEN | Vendor interviews | FY27 |
| PE promoter selling 58% in 18 months | OPEN | Management selling own shares | each quarter |
| SSSG definition excludes refurbished/area-reduced stores | OPEN | Disclosure of excluded-store count | Q3 FY27 |
| 19-month payback: pre- or post-rent EBITDA? | OPEN | RHP p.128 or IR answer | before any use |
| Related-party logistics ~Rs 103 cr/yr to Samayat | OPEN | Rates vs third-party quotes; post-PE-exit fate of the contract | FY27 AR |
| Employee cost +25% vs revenue +14% (wage steps, ~55-60 bps) | OPEN | Next state wage notifications (Oct VDA) | Q4 FY27 |
| Screener 'borrowings' Rs 1,988 cr | CLEARED | Bank/CP borrowing appears | each AR |
| EBITDA margin 14.6% (Ind AS 116) | ADJUSTED | - | - |

**Open soft flags: 8** (8 from the deep dive), plus 0 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-20 | Borrowings Rs 1,988 cr | cleared | AR26 n.33: equals lease liabilities exactly; HSIE: total debt nil since FY24 |
| 2026-11-20 | EBITDA 14.6% | use pre-Ind AS 9.8% in all valuation | Rent is a real cost; AR26 Ind AS 116 impact Rs 613 cr |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base |
|---|---|---|---|
| P(≥3x in 5 yrs) | 6% | 44.4% | 0.14x |
| P(≤0.5x in 5 yrs) | 5% | 2.0% | 2.52x |
| P(blow-up) | 2% | n/a | n/a |

Base-rate class: **India, random NSE sample, mcap >= Rs 400 cr at T0, 5 yrs from 30-Sep-2020** (n=304, 5-yr horizon). Source: research_notes/Backtests/hard_filters_test.md Part B; research_notes/Backtests/hard_filters_outputs/partB_summary.json (base_rates.mcap_ge400). Caveats: Survivors only (firms delisted before mid-2023 absent -> loss rates understated); T0 was six months after the Mar-2020 low and 2020-25 was a strong small/mid-cap bull market (-> x3 overstated). One snapshot. Treat as an upper bound for P(>=3x) and a lower bound for P(<=0.5x).
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.30 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(≥3x in 5 yrs) is 0.14x the base rate; P(≤0.5x in 5 yrs) is 2.52x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.46x | 7.9% | 1.40x | 1.76x | 32.2 (-65%) | -80% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

## 7. Position size (written rule)
| Sizing step | Value |
|---|---|
| Full Kelly f* (5-yr bet vs index hurdle, scenario outcomes) | 0.0% |
| × Kelly fraction 0.25 | 0.0% |
| Cap: max % at cost (satellite tier) | 4.0% |
| Cap: liquidity (10% of ADV × 5 days ÷ portfolio) | n/a (ADV not supplied) |
| Rule size before gates = min(fractional Kelly, caps) | 0.0% |
| **Size after gates** (blocked by: Stage 2 hard filters; Stage 4 soft flags; Expected value vs hurdle) | **0.0%** |

Written rule: size = min(Kelly fraction × f*, tier cap at cost, liquidity cap); any blocking gate → 0. f* maximises E[ln(1 + f·(M/H − 1))] over the scenario outcomes (each scenario spread by 5-point Gauss-Hermite on the same σ, blow-up as a point mass), with H = the index hurdle multiple. Fractional Kelly because the inputs are opinions (strategy:thorp-kelly); tier caps from strategy:position-sizing (max 5% at cost, satellites 3.5–4%, speculative 1–3%).

_Practice mode: this is the mechanical output of the rule on illustrative inputs, NOT a position size for anyone._

## 8. Kill criteria (each one dated and checkable)
| # | Kill if… | Measured by | Check by |
|---|---|---|---|
| 1 | SSSG below 8% for 4 straight quarters | company SSSG (definition unchanged) in quarterly presentations | 2027-11-30 |
| 2 | Pre-Ind AS EBITDA margin below 8.5% for FY27 | AR27: EBITDA - Ind AS 116 impact | 2027-08-31 |
| 3 | Revenue per sq ft falls YoY two quarters running (V2-style density dilution) | revenue / average retail area from PPTs | 2027-05-31 |
| 4 | Management (not the PE fund) sells shares, or the RPT logistics share rises again | SAST/insider filings; AR27 RPT note | 2027-08-31 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. New-state stores (South/West, 15k sq ft) never reached network density; SSSG held only because weak stores were excluded as 'refurbishment'.
2. Minimum-wage steps (UP wage board, Haryana) and rent re-pricing on short leases took 150 bps of margin that 'GM reinvestment' could not cover.
3. Quick commerce and Zudio took the Tier II apparel customer; the P/E de-rated from ~48x to ~25x while EPS grew 12%.
4. The remaining ~40% PE stake came out at a discount and capped the price for two years.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | INCOMPLETE: 2 of 7 rules unchecked (H3 rating 'issuer not cooperating', H5 related-party cash leakage to promoter entities) → size 0 until checked | yes |
| Stage 3 PEAD avoid flag | unknown (no live quintile): does not block, noted | no |
| Stage 4 soft flags | 8 open, no variant view → NO POSITION | yes |
| Outside-view check | model departs from base rate with no variant view → shrink | no |
| Expected value vs hurdle | EV 1.46x vs hurdle 1.76x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

