# tools/decision: the decision card (roadmap stage 6) and paper-call emitter (stage 7)

`decision_card.py` builds one card from the outputs of stages 2–5 and fills it into `decision_card.md`. It also
writes the card's probabilities as dated **paper-call records** in memdb seed format, so every decision is
scored later (Brier vs base rate). It uses only the standard library and runs on a Raspberry Pi.

Guide, worked examples, design choices and known limits: `research_notes/Templates/valuation_and_decision.md`.

## Run
```bash
python3 tools/decision/decision_card.py --template > my_card.json
python3 tools/decision/decision_card.py my_card.json -o card.md --calls paper_calls.json [--with-worksheet]
```
`my_card.json` points at a worksheet input (`"worksheet": "path/relative/to/card.json"`), and the card runs the worksheet itself.

## Files
| File | What |
|---|---|
| `decision_card.md` | The template. Every `{{field}}` must be filled, and an unknown placeholder is an error |
| `decision_card.py` | The assembler, the gates and the sizing rule. It writes the paper calls |
| `base_rates.json` | The reference classes shown next to every probability, each with its source, biases, 95% CI and size band. `null` means no honest number on file. **v2 (2026-11-23):** `india_nonfin_1000_20000cr_5y` and `us_float_500m_10b_5y`, survivorship-free (method: `research_notes/Backtests/base_rates_5y.md`; script `tools/backtests/base_rates_5y/build.py`). Old classes keep a `_deprecated` suffix; an old card that names the old key resolves to it and prints "Deprecated class" |
| `calibration_2026-11-23/` | All 6 cards re-run with worksheet v1.3, card v1.1 and base rates v2 (no calls written). Results and reasons in its README: all 6 still size 0 |
| `examples/` | Cards for VMM, CUMMINSIND and US-FIVE (TEST MATERIAL, no verdict), plus a fictional SYNTHETIC card that exercises the path where every gate clears |

Card v1.1 (2026-11-23) adds three stage-5 lines when the worksheet has them: cash tax, reinvestment realism and
the exit-multiple bet (EV of the 5-year multiple at the stated exits, at the DCF-consistent P/E and at the own median).
It also prints base-rate CIs and the size-band warning, and applies the market-specific PEAD gate.

Bank/NBFC worksheets (`"mode": "bank"`, v1.1) are supported: the stage-5 block then reports reverse P/B, implied CoE,
residual-income scenarios, P/B temperature and book stress. Example: `examples/FEDERALBNK_card.json` (practice).

## Card fields
These come in this order: thesis in one line → variant view → what the price implies (stage 5) → stage 2 hard filters and graded
flags → stage 3 signals (PEAD avoid flag, sector-adjusted credibility, detector alerts) → stage 4 soft flags and
the override log → P(≥3x/5y), P(≤0.5x), P(blow-up) next to their base rates → expected value → position size by
the written rule → dated kill criteria → pre-mortem → gate log and review date.

## Gates (each one written down; any "blocks" sets the size to 0)
| Gate | Blocks when | Source |
|---|---|---|
| Stage 2 hard filters | any rule `fail` (disqualified, no override) or `unknown` (incomplete), or none supplied | `insight:disqualifiers` |
| Stage 3 PEAD avoid flag | **India only:** SUE quintile 1–2 and decision date ≤ event + 92 calendar days (~63 trading days). **US: no gate.** The quintile is shown but never blocks, because the US SUE proxy cut-points are uncalibrated and no US PEAD back-test exists (card v1.1, 2026-11-23) | L17, L19, L31, L34 |
| Stage 4 soft flags | ≥3 open (deep-dive open flags + fired graded stage-2 flags + high-severity detectors + credibility ≥15 pts below peers) and no written variant view | `insight:flag-override-template` |
| Expected value | EV of the 5-year multiple < hurdle multiple (index CAGR^5) | — |
| Kill criteria | missing or undated | — |
| Outside-view check (note only) | model P is >2x or <0.5x the base rate | `insight:lit-base-rate-neglect-outside-view` |
| Size outside the class (note only, v1.1) | market cap outside the class `size_band` (same money units) | `base_rates.json` |

## Sizing rule
`size = min(kelly_fraction × f*, tier cap at cost, liquidity cap)`, then 0 if any gate blocks.
- `f*` maximises `E[ln(1 + f·(M/H − 1))]` over the scenario outcomes (each spread by 5-point Gauss-Hermite on σ, with the blow-up as a point mass). `H` is the index hurdle multiple, so the bet is measured against the alternative.
- Kelly fraction defaults to 0.25 (`strategy:thorp-kelly`).
- Tier caps (`strategy:position-sizing`): core 5%, satellite 4%, speculative 2%.
- Liquidity cap = `adv_pct × ADV × days_to_exit ÷ portfolio value`, in the same money units.
- Phase A: every size is a **paper size**. In practice mode the card says that this is a mechanical rule output, not a size for anyone.

## Paper calls emitted
For each card there are three `thesis` records plus one `decision` record:
- `thesis:paper-call:<T>:card-<date>-5y-ge3x`
- `…-5y-le0p5x`
- `…-5y-blowup`
- `decision:card:<T>:<date>`

Each paper call carries `probability`, `base_rate_probability`, `entry_price`, `resolve_by` (entry + 5 years) and a mechanical `resolution_rule`. Practice cards are tagged `practice-example`. The example call files in `examples/` were **not** ingested into memdb. Whether practice calls should enter the stage-7 scoreboard is a decision for the user (they would add 5-year calls on test inputs).
