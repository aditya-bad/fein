# Decision card: Cummins India (CUMMINSIND) · 2026-11-21

> **TEST MATERIAL. No verdict, no buy/sell/watchlist call (lesson L9).** This card was produced to test the template. Every scenario input is an illustrative [EST]; the rule output below is what the written rules compute from those inputs, nothing more.

| Card | Value |
|---|---|
| Card version | 1.0 (2026-11-21) · worksheet 1.0 (2026-11-21) |
| Price used | INR 4,100 on 2026-11-21 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/CUMMINSIND_practice.md) · 5 valuation worksheet |
| **Rule output** | **Practice, no verdict.** Mechanical rule output: size 0: blocked by Stage 2 hard filters (INCOMPLETE: 1 of 7 rules unchecked (H3 rating 'issuer not cooperating') → size 0 until checked); Stage 4 soft flags (8 open, no variant view → NO POSITION); Expected value vs hurdle (EV 1.33x vs hurdle 1.76x → below hurdle → size 0) |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:CUMMINSIND:card-2026-11-21-5y-ge3x`, `thesis:paper-call:CUMMINSIND:card-2026-11-21-5y-le0p5x`, `thesis:paper-call:CUMMINSIND:card-2026-11-21-5y-blowup` |

## 1. Thesis in one line
TEST THESIS (illustrative): data-centre gensets and the CPCB IV+ price step keep revenue growing ~12% with core NOPAT margin ~14-15%, while cash keeps flowing out ~100% as dividends.

## 2. Variant view (what we believe that the price does not, and why we could know it)
_None written._

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 12.5%, TG 5.0%, ROIIC 40%): revenue CAGR 31.2% for 10 years at a 14.8%→14.5% NOPAT margin; or year-1 growth 56.2% fading to 5.0%. Base case IRR at today's price: 7.3%.
- Feasibility: the implied path needs reinvestment above 100% of NOPAT (peak 141%) at ROIIC 40%.
- **Scenario DCF:** probability-weighted value 1,274 (-69% vs price); bear 978.8 (-76%).
- **Twin engine, 3x in 5 yrs** from P/E 52.0: exit P/E 26.0 → EPS CAGR 43%; exit P/E 39.0 → EPS CAGR 32%; exit P/E 52.0 → EPS CAGR 25%; exit P/E 57.5 → EPS CAGR 22%. Track record: 30.0% PAT FY21 618 -> FY26 2,330 cr, from a cyclical low (FY15 786 -> FY21 618 was negative) [SCR].
- **Temperature:** P/E 52.0; own history: INSUFFICIENT HISTORY (n=0 < 5); sector: NORMAL (0.90x of sector median).
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- Full worksheet: `tools/valuation/examples/CUMMINSIND.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: Cummins practice deep dive §2, §5, §7 (AR26, AGM-notice RPT annex) and the hard-filter Part B snapshot (research_notes/Backtests/hard_filters_outputs/partB_flags.csv, T0 30-Sep-2020).

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal | PASS | Cash/MFs ~Rs 3.8-4.0k cr yield treasury income ~Rs 264 cr (consistent); FCF ~= dividends paid |
| H1b economics implausible | PASS | BRSR units x realisation cross-foot revenue (+7% volume, +10% price/mix) |
| H1c profits unverifiable by outsiders | PASS | GOEM channel and dealer price sheets checkable |
| H2 auditor exit / qualified opinion | PASS | No auditor issues noted [AR26]; Part B R3 (auditor resignation before T0) = False |
| H3 rating 'issuer not cooperating' | UNKNOWN | Not checked in the practice run |
| H4 SME/Telegram pump | PASS | Large cap, 51% MNC parent |
| H5 related-party cash leakage to promoter entities | PASS | Cash to the parent ~8.9% of sales but under disclosed formulas (royalty 4% x eligible sales, cost +11%) with shareholder approvals -> graded soft flags, not diversion |

| Graded flag | Status | Evidence |
|---|---|---|
| R5 other income > 30% of PBT (FY18-20, Part B) | FIRED | Part B flag True; FY26 other income 23% of PBT (now below 30%), keep as a question: core PBT Rs 2,384 cr used for multiples |
| R1/R2/R4 (CFO/PAT, pledge, debt+neg CFO) | CLEAR | Part B: all False; CFO/PAT 5y 0.89; pledge 0% |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD) avoid flag:** no live quintile. Q2 FY27 OPM fell to ~15% (from 21%): likely a large miss, but no SUE computed (live tracker starts Q3 FY27). If it lands in quintile 1-2 the avoid flag would be active ~92 days.
- **Promise credibility:** not scored. Promise tracker not run; management gives ranges (e.g. DC 30-40% of power gen), which the protocol treats as a definitional flag.

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| KMP churn | 2025-2026 | MD x3 and CFO x2 in 26 months; senior manager resigned Aug-2026 | med |
| RPT step-up | FY26 / Q2 FY27 | Support services to parent Rs 111 -> 223 cr, then a Q2 'true-up' | med |
| Dated contract | 2027-03-31 | Royalty agreement with the parent expires | low |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| 51% of purchases from related parties (cost-plus pass-in) | OPEN | Materials ratio vs KOEL through a commodity cycle | FY27 |
| Support services to parent doubled; Q2 true-up | OPEN | Disclosure of the allocation key; FY27 support < 2% of sales | FY27 AR |
| Sales +4% vs KOEL +19% (Q2 FY27) | OPEN | Two quarters of growth back in line with peers | Q4 FY27 |
| 3 customers = 31% of sales (GOEM channel) | OPEN | GOEM MCA financials; brand switching | FY27 |
| DC = '30-40%' of power gen (band hides the ex-DC trend) | OPEN | Installer DG/IT ratio, brand split | ground visit C |
| MD x3, CFO x2 in 26 months | OPEN | Further senior exits | each quarter |
| IT appeal on Rs 210.8 cr adjustments | OPEN | High Court order | - |
| Royalty agreement expires 31-Mar-2027 | WATCH | FY28 AGM-notice RPT annex: rate or eligible base raised | 2027-07-31 |
| Other income 23% of PBT | ADJUSTED | - | - |
| Payout 79%, FCF ~= dividends | CLEARED | Capex spike or payout > 100% | FY27 |

**Open soft flags: 8** (7 from the deep dive, 1 graded stage-2 flag(s)), plus 1 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-21 | Other income 23% of PBT | use core PBT Rs 2,384 cr; treasury income held flat in the EPS path; rent/JV dividends valued separately | AR26 n.27 split: rent 186, JV/associate dividends 217, interest 189, MF 75 |
| 2026-11-21 | Labour-code exceptional Rs 94 cr | cleared as one-off; ~80 bps recurring tracked | Q2 results note 6 (regulatory catch-up) |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base |
|---|---|---|---|
| P(≥3x in 5 yrs) | 2% | 44.4% | 0.05x |
| P(≤0.5x in 5 yrs) | 2% | 2.0% | 1.22x |
| P(blow-up) | 1% | n/a | n/a |

Base-rate class: **India, random NSE sample, mcap >= Rs 400 cr at T0, 5 yrs from 30-Sep-2020** (n=304, 5-yr horizon). Source: research_notes/Backtests/hard_filters_test.md Part B; research_notes/Backtests/hard_filters_outputs/partB_summary.json (base_rates.mcap_ge400). Caveats: Survivors only (firms delisted before mid-2023 absent -> loss rates understated); T0 was six months after the Mar-2020 low and 2020-25 was a strong small/mid-cap bull market (-> x3 overstated). One snapshot. Treat as an upper bound for P(>=3x) and a lower bound for P(<=0.5x).
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.30 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(≥3x in 5 yrs) is 0.05x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.33x | 5.8% | 1.27x | 1.76x | 1,274 (-69%) | -76% |

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
| 1 | Royalty rate or eligible base raised at renewal | FY28 AGM-notice RPT annex | 2027-07-31 |
| 2 | Standalone OPM below 17% in both Q3 and Q4 FY27 (pass-through failed) | screener / results filings | 2027-05-31 |
| 3 | Parent take (royalty + support) above 3% of sales in FY27 | AR27 RPT note | 2027-08-31 |
| 4 | Payout above 100% of FCF or a capex spike above 2x D&A without a stated plan | AR27 cash flow | 2027-08-31 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. The parent raised the royalty and cost allocations at the 2027 renewal; the minority's share of DC economics shrank while reported growth looked fine.
2. HHP engines were allocated to other regions; India lost DC share to KOEL and imports, and the '30-40%' band hid it for four quarters.
3. The FY26 margin was a CPCB IV+ price-step peak; normalised OPM settled at 17-18% and the P/E fell from ~50x to ~30x.
4. Rates fell and the 79% payout shrank the cash pile, so treasury income (~10% of PAT) stopped growing.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | INCOMPLETE: 1 of 7 rules unchecked (H3 rating 'issuer not cooperating') → size 0 until checked | yes |
| Stage 3 PEAD avoid flag | unknown (no live quintile): does not block, noted | no |
| Stage 4 soft flags | 8 open, no variant view → NO POSITION | yes |
| Outside-view check | model departs from base rate with no variant view → shrink | no |
| Expected value vs hurdle | EV 1.33x vs hurdle 1.76x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

