# Decision card: Synthetic Test Co (fictional) (SYNTH) · 2026-11-21

> **TEST MATERIAL. No verdict, no buy/sell/watchlist call (lesson L9).** This card was produced to test the template. Every scenario input is an illustrative [EST]; the rule output below is what the written rules compute from those inputs, nothing more.

| Card | Value |
|---|---|
| Card version | 1.0 (2026-11-21) · worksheet 1.0 (2026-11-21) |
| Price used | INR 100.00 on 2026-11-21 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (none) · 5 valuation worksheet |
| **Rule output** | **Practice, no verdict.** Mechanical rule output: rule size 4.0% of portfolio at cost |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:SYNTH:card-2026-11-21-5y-ge3x`, `thesis:paper-call:SYNTH:card-2026-11-21-5y-le0p5x`, `thesis:paper-call:SYNTH:card-2026-11-21-5y-blowup` |

## 1. Thesis in one line
Fictional: unit test of the sizing path.

## 2. Variant view (what we believe that the price does not, and why we could know it)
Fictional variant view, present so the soft-flag gate is satisfied.

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 12.5%, TG 5.0%, ROIIC 30%): revenue CAGR -2.1% for 10 years at a 10.5%→12.0% NOPAT margin; or year-1 growth -7.0% fading to 5.0%. Base case IRR at today's price: 19.5%.
- **Scenario DCF:** probability-weighted value 228.0 (128% vs price); bear 114.0 (14%).
- **Twin engine, 3x in 5 yrs** from P/E 10.0: exit P/E 5.0 → EPS CAGR 43%; exit P/E 7.5 → EPS CAGR 32%; exit P/E 10.0 → EPS CAGR 25%; exit P/E 14.5 → EPS CAGR 16%; exit P/E 18.0 → EPS CAGR 11%. Track record: 18.0% .
- **Temperature:** P/E 10.0; own history: COLD; sector: COLD (0.56x of sector median).
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- Full worksheet: `tools/valuation/examples/SYNTHETIC.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: fictional

| Hard rule | Status | Evidence |
|---|---|---|
| H1a | PASS |  |
| H1b | PASS |  |
| H1c | PASS |  |
| H2 | PASS |  |
| H3 | PASS |  |
| H4 | PASS |  |
| H5 | PASS |  |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD):** SUE quintile 4 (event 2026-11-01). Avoid flag not active. Rule L19: bottom two quintiles = avoid/exit for ≥63 trading days.
- **Promise credibility:** 70% vs peer median 55% → sector-adjusted +15 pts (near-term, n=12). 
- **Detector alerts:** none supplied.

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| fictional flag A | OPEN |  |  |
| fictional flag B | OPEN |  |  |

**Open soft flags: 2** (2 from the deep dive), plus 0 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base |
|---|---|---|---|
| P(≥3x in 5 yrs) | 54% | 44.4% | 1.21x |
| P(≤0.5x in 5 yrs) | 3% | 2.0% | 1.63x |
| P(blow-up) | 3% | n/a | n/a |

Base-rate class: **India, random NSE sample, mcap >= Rs 400 cr at T0, 5 yrs from 30-Sep-2020** (n=304, 5-yr horizon). Source: research_notes/Backtests/hard_filters_test.md Part B; research_notes/Backtests/hard_filters_outputs/partB_summary.json (base_rates.mcap_ge400). Caveats: Survivors only (firms delisted before mid-2023 absent -> loss rates understated); T0 was six months after the Mar-2020 low and 2020-25 was a strong small/mid-cap bull market (-> x3 overstated). One snapshot. Treat as an upper bound for P(>=3x) and a lower bound for P(<=0.5x).
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.30 (worksheet block b). They are only as good as the scenario inputs.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 3.42x | 27.9% | 3.18x | 1.76x | 228.0 (128%) | 14% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

## 7. Position size (written rule)
| Sizing step | Value |
|---|---|
| Full Kelly f* (5-yr bet vs index hurdle, scenario outcomes) | 91.9% |
| × Kelly fraction 0.25 | 23.0% |
| Cap: max % at cost (satellite tier) | 4.0% |
| Cap: liquidity (10% of ADV × 5 days ÷ portfolio) | 100.0% |
| Rule size before gates = min(fractional Kelly, caps) | 4.0% |
| **Size after gates** (no gate blocks) | **4.0%** |

Written rule: size = min(Kelly fraction × f*, tier cap at cost, liquidity cap); any blocking gate → 0. f* maximises E[ln(1 + f·(M/H − 1))] over the scenario outcomes (each scenario spread by 5-point Gauss-Hermite on the same σ, blow-up as a point mass), with H = the index hurdle multiple. Fractional Kelly because the inputs are opinions (strategy:thorp-kelly); tier caps from strategy:position-sizing (max 5% at cost, satellites 3.5–4%, speculative 1–3%).

_Practice mode: this is the mechanical output of the rule on illustrative inputs, NOT a position size for anyone._

## 8. Kill criteria (each one dated and checkable)
| # | Kill if… | Measured by | Check by |
|---|---|---|---|
| 1 | fictional | fictional | 2027-06-30 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. fictional

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (7 rules) | no |
| Stage 3 PEAD avoid flag | clear | no |
| Stage 4 soft flags | 2 open, variant view written | no |
| Expected value vs hurdle | EV 3.42x vs hurdle 1.76x → above hurdle | no |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

