# Decision card: Five Below (US-FIVE) · 2026-11-21

> **TEST MATERIAL. No verdict, no buy/sell/watchlist call (lesson L9).** This card was produced to test the template. Every scenario input is an illustrative [EST]; the rule output below is what the written rules compute from those inputs, nothing more.

| Card | Value |
|---|---|
| Card version | 1.2 (2026-11-23; India survival cap, outside-view tail anchoring in the EV/Kelly gate) · worksheet 1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode) |
| Price used | USD 220.00 on 2026-09-30 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/FIVE_practice.md) · 5 valuation worksheet |
| **Rule output** | **Practice, no verdict.** Mechanical rule output: size 0: blocked by Stage 4 soft flags (6 open, no variant view → NO POSITION); Expected value vs hurdle (EV 1.14x anchored (raw 1.19x) vs hurdle 1.47x → below hurdle → size 0) |
| Review date | **2027-03-31** |
| Paper-call ids (stage 7) | `thesis:paper-call:US-FIVE:card-2026-11-21-5y-ge3x`, `thesis:paper-call:US-FIVE:card-2026-11-21-5y-le0p5x`, `thesis:paper-call:US-FIVE:card-2026-11-21-5y-blowup` |

## 1. Thesis in one line
TEST THESIS (illustrative): ~150 net new stores a year plus traffic-led comps keep revenue growing mid-teens while operating margin returns toward the FY16-21 range (11-13%).

## 2. Variant view (what we believe that the price does not, and why we could know it)
_None written._

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 9.5%, TG 3.0%, ROIIC 20%): revenue CAGR 17.1% for 10 years at a 7.2%→8.5% NOPAT margin; or year-1 growth 29.9% fading to 3.0%. Base case IRR at today's price: 7.9%.
- Feasibility: the implied path needs reinvestment above 100% of NOPAT (peak 149%) at ROIIC 20%.
- **Scenario DCF:** probability-weighted value 153.0 (-30% vs price); bear 94.9 (-57%).
- **Twin engine, 3x in 5 yrs** from P/E 34.0: exit P/E 17.0 → EPS CAGR 43%; exit P/E 25.5 → EPS CAGR 32%; exit P/E 34.0 → EPS CAGR 25%. Track record: 12.9% diluted EPS 3.12 (FY ended Feb-2020) -> 6.47 (Jan-2026), 6 years [XBRL].
- **Temperature:** P/E 34.0; own history: INSUFFICIENT HISTORY (n=0 < 5); sector: no peers given.
- **Exit-multiple bet (L21):** exit P/E used 14.0/20.0/26.0 vs DCF-consistent 15.7/17.7/19.8 vs own median n/a (n=0). EV of the 5-yr multiple at the used exits 1.19x, at DCF exits 1.04x, at the own median n/a (hurdle 1.47x).
- Full worksheet: `tools/valuation/examples/FIVE.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: FIVE practice deep dive §5, §8 (10-K FY25, 8-Ks, DEF 14A not yet read). US version of the hard rules.

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal | PASS | Cash $932M with interest income consistent; zero funded debt |
| H1b economics implausible | PASS | Store model triangulated; capex gap is a definitional flag, not implausibility |
| H1c profits unverifiable by outsiders | PASS | Store counts, prices and traffic observable |
| H2 auditor exit / restatement (8-K 4.01/4.02) | PASS | No auditor change, no non-reliance, no going-concern language [practice file §8.2] |
| H3 rating 'issuer not cooperating' | PASS | n/a in the US form; no funded debt |
| H4 pump pattern | PASS | S&P MidCap-size, widely held |
| H5 related-party cash leakage | PASS | No controlling holder; Item 404 not yet read in DEF 14A (management-as-related-party read via 8-K 5.02 only) |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD) avoid flag:** not applicable. PEAD avoid leg is tested on India only (L17, L19); no US test on file.
- **Survival cap (v1.2):** not applicable (India only).
- **Promise credibility:** 75% absolute (long-range (prior team, 65-84% delivered), n=3). **No peer base rate → not usable as a signal (L18).** Near-term guides beaten 5/5 by the new team; no US retail peer base rate yet.

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| Form 4 cluster sale | 2026-09 | 5 insiders sold $6M+ at $241-255 (L14: weak signal) | low |
| 8-K 5.02 executive turnover | 2024-2026 | CEO, 2 CFOs, CMO and other senior exits in 18 months | med |
| 8-K 8.01 cyber incident | 2026-07-22 | Disclosed incident | low |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| New-store investment vs capex gap ($0.4M vs ~$0.65M gross) | OPEN | Tenant allowance disclosed >= $0.4M/store or a cohort payback table | FY26 10-K |
| Comp durability (2-yr stack ~+30%) | OPEN | FY27 comps positive with transactions positive | Q1 FY27 |
| Tariff regime and vendor pass-through | OPEN | Merchandise margin holds in FY27 at new tariff rates | FY27 |
| Insider cluster selling | OPEN | CEO/CFO sell outside 10b5-1, or an insider buys at scale | each quarter |
| Executive turnover | OPEN | 4+ quarters with a stable team | 2027-09 |
| Class action in discovery | OPEN | Dismissal or settlement < ~1% of market cap | - |
| GAAP EPS/GM include $163.6M tariff refund | ADJUSTED | - | 4 quarters |
| FY25 FCF $412M is a cyclical high | ADJUSTED | - | - |

**Open soft flags: 6** (6 from the deep dive), plus 0 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-21 | Vanguard 13G/A shows 0% | closed as false alarm | Jan-2026 realignment; 13F still shows 5.34M shares |
| 2026-11-21 | Q2 FY26 GAAP EPS $3.99 | use adjusted EPS (forward guide midpoint $10.07) | Ex-99.1 reconciliation: $163.6M IEEPA refund in COGS |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base | Anchored (w=0.50 on base) |
|---|---|---|---|---|
| P(≥3x in 5 yrs) | 4% | 7.0% [95% CI 6.0%–8.1%] | 0.51x | not anchored |
| P(≤0.5x in 5 yrs) | 14% | 14.2% [95% CI 12.7%–15.7%] | 0.97x | 14.0% |
| P(blow-up) | 2% | 10.9% [95% CI 9.6%–12.3%] | 0.18x | 6.5% |

**Outside-view anchoring (v1.2, L36):** anchored P = 0.50 × base rate + 0.50 × model for P(≤0.5x) and P(blow-up) (weight: default). The expected-value gate and Kelly use the anchored tails; the paper calls keep the raw model probability (with the anchored one alongside), so Brier scoring can tell which was better. This is a calibration safeguard, not a change to the hurdle. The default weight is 0.5; a lower weight needs a written evidence note, never below 0.25.

Base-rate class: **US non-financial, non-utility 10-K filers, public float $500M-$10B at T, 5 yrs from 30-Jun-2015/2017/2019 (survivorship-free: EDGAR fates for unpriced firms)** (n=3125, 5-yr horizon). Source: research_notes/Backtests/base_rates_5y.md; tools/backtests/base_rates_5y/build.py on research_notes/Backtests/solvency_us_outputs/panel.csv; outputs research_notes/Backtests/base_rates_5y_outputs/results.json. Caveats: n=3125 firm-snapshots used of 3,691 in band (1,823 firms; 2,074 priced, 152 unpriced EDGAR failures, 899 unpriced acquisitions counted as neither tail; 566 unpriced alive/stopped-filing/exchange-transfer rows excluded as missing at random). 95% CIs (CIK bootstrap): P(>=3x) 6.0-8.1%, P(<=0.5x) 12.7-15.7%, P(blow-up) 9.6-12.3%. Assumption bounds (acquisitions excluded instead of neutral): P(>=3x) up to 9.8%, P(<=0.5x) up to 19.9%, blow-up up to 15.3%. Three start dates (2015: >=3x 5.4%, <=0.5x 17.3%; 2017: 5.9%, 9.9%; 2019: 9.5%, 14.9%); windows include the 2015-16 energy bust, COVID and 2022. Total return (adjusted close). Float is stale and understates controlled firms' market cap. Blow-up excludes fraud findings and misses firms that fell 80% and were then bought (unpriced).

> **Size outside the class:** market cap 12,188 USD M vs the class band 500.0–10,000 USD M (float). No class on file fits better; read the base rates as the nearest class, not as this stock's.
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.35 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(blow-up) is 0.18x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 8%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.19x | 3.6% | 1.11x | 1.47x | 153.0 (-30%) | -57% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

**Anchored EV (v1.2, used by the gate):** 1.14x (raw model 1.19x). Tails reweighted to P(blow-up) 6.5% and P(≤0.5x) 14.0%; the rest of the distribution is scaled in proportion, its shape kept.

## 7. Position size (written rule)
| Sizing step | Value |
|---|---|
| Full Kelly f* (5-yr bet vs index hurdle, anchored outcomes; raw model 0.0%) | 0.0% |
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
| 1 | Comparable sales negative with transactions negative in any FY27 quarter | 8-K 2.02 Ex-99.1 | 2027-12-15 |
| 2 | FY26 10-K raises the $0.4M new-store investment or drops the payback sentence | 10-K Item 1/7 text diff | 2027-04-15 |
| 3 | Adjusted operating margin below 8% for FY2026 | Q4 FY26 release reconciliation | 2027-03-31 |
| 4 | CEO or CFO sells outside a 10b5-1 plan | Form 4 (box checked on the form itself) | 2027-11-30 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. The +14-23% comps were a pricing-reset and trend spike; traffic turned negative in FY27 and operating deleverage hit a fixed lease base of $2.0B.
2. Replacement tariffs were higher than IEEPA and the domestic-vendor 60% passed them through; merchandise margin fell 200 bps.
3. New stores cost ~$1M all-in, not $0.4M; ROIIC was ~12%, so growth destroyed value at a 9.5% cost of equity.
4. Another executive change reset strategy and guidance credibility.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (7 rules) | no |
| Stage 3 PEAD avoid flag | n/a | no |
| Stage 3 survival cap | n/a | no |
| Stage 4 soft flags | 6 open, no variant view → NO POSITION | yes |
| Outside-view check | model departs from base rate with no variant view → shrink | no |
| Expected value vs hurdle | EV 1.14x anchored (raw 1.19x) vs hurdle 1.47x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

