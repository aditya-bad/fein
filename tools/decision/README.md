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
| `tests/test_decision_card.py` | Unit tests (synthetic inputs) for the survival cap (v1.2–v1.4, incl. the core-asset threat trigger), tail anchoring and the anchoring-lowered warning: `python3 -m unittest discover -s tools/decision/tests` |
| `calibration_2026-11-23/v1.2/` | The same 6 cards (plus the US-KEX persistent-tax variant) re-run with card v1.2, no calls written. All still size 0; see the v1.2 changelog below |
| `calibration_2026-11-23/` | All 6 cards re-run with worksheet v1.3, card v1.1 and base rates v2 (no calls written). Results and reasons in its README: all 6 still size 0 |
| `examples/` | Cards for VMM, CUMMINSIND and US-FIVE (TEST MATERIAL, no verdict), plus a fictional SYNTHETIC card that exercises the path where every gate clears |

Card v1.1 (2026-11-23) adds three stage-5 lines when the worksheet has them: cash tax, reinvestment realism and
the exit-multiple bet (EV of the 5-year multiple at the stated exits, at the DCF-consistent P/E and at the own median).
It also prints base-rate CIs and the size-band warning, and applies the market-specific PEAD gate.

Bank/NBFC worksheets (`"mode": "bank"`, v1.1) are supported: the stage-5 block then reports reverse P/B, implied CoE,
residual-income scenarios, P/B temperature and book stress. Example: `examples/FEDERALBNK_card.json` (practice).

## Changelog: card v1.4 (2026-11-24, L40)
Two additions from the INDRAMEDCO live dive (a ~54% ROIC that rests on an expired government land lease).
Neither changes a threshold; the six calibration cards are unaffected unless they set the new input.

**1. Manual core-asset threat trigger.** New optional input `survival.core_asset_threat` =
`{"description": "...", "source": "...", "date": "YYYY-MM-DD"}` (a plain string is also accepted). Use it when a
government-granted input the business depends on (land lease, licence, concession, PPP) has expired, is contested
or is being withdrawn. When the description is non-empty it fires the survival cap exactly like a pledge /
interest-cover red flag, in both modes (PEAD window → 0 new money; otherwise starter size ≤1%, no additions), with
reason text `core-asset licence/lease threat (L40): <description> [<source>, <date>]`. Missing pledge / interest-cover
inputs are still listed (`also not checked: ...`). The pledge/ICR screen cannot see legal or licence risk, hence a
manual input. India only like the rest of the cap; on a non-India card the threat is printed in stage 3 but not applied.

**2. Anchoring-lowered-tails warning.** When outside-view anchoring *lowers* our raw P(≤0.5x) or P(blow-up) (base
rate below the model), the card prints `WARNING: anchoring lowered documented tails — check evidence note` in §5 and
adds a non-blocking `Tail anchoring (v1.4 warning)` row to the gate log. The decision record carries
`anchor_lowered_tails` (list of the lowered events). The mechanical size still uses the anchored tails.

## Changelog: card v1.2 (2026-11-23)
Two safeguards from the 2026-11-23 back-tests. Neither changes the hurdle or any v1.1 gate threshold.

**1. Survival cap, India only (L35, `decision:pead-avoid-plus-redflag-survival-cap`).** It fires when the PEAD avoid flag
is active (bottom-two SUE quintile within ~63 trading days) **and** either promoter pledge is above 25% of the
promoter holding or interest cover is below 1.5x. Input: card field `survival` with `pledge_pct_of_promoter` (fraction),
`interest_cover` (x), `already_owned`, `source`, `as_of` and `note`. If the window is active and an input is missing,
the status is UNCHECKED and the cap is treated as triggered until the input is checked, as a stage-2 `unknown` would be.
- **Policy chosen: 0 new money, not a minimum size.** If the stock is already owned, the position goes to
  **hold-review**: no additions, and it is reviewed against the balance-sheet question. The red flag is a solvency
  risk, and a small new position would still be money committed to a ~3x halving risk (17.6% vs 6.1% in 12 months).
- The card prints a **mandatory balance-sheet question** (debt service and the promoter's ability to meet a margin
  call through a 12-month stress, answered from filings rather than from management) and logs the gate as blocking.
- **S5-India alone is not a trigger** (no signal in the test). Outside the window, and in the US, the cap is `n/a`.
- While the window is open, the PEAD WAIT gate already sets the size to 0. What the cap adds is the hold-review rule
  for existing holders, the balance-sheet question, and a separate gate-log entry. That entry shows *why* the WAIT is
  a survival issue and not just drift.

**2. Outside-view tail anchoring (L36): a calibration safeguard, not a hurdle change.** For P(≤0.5x) and P(blow-up),
`anchored = w × base rate + (1 − w) × model`, with `w` = 0.5 by default. A card may set
`"tail_anchor": {"base_weight": w, "evidence": "..."}`: a `w` below 0.5 is accepted only with a written evidence
note (otherwise 0.5 is used and the card says so), and `w` is never below 0.25 (raised to the floor). `w` up to 1 is
allowed with no note. §5 shows raw and anchored values side by side. **The EV gate and Kelly use the anchored tails.**
The tagged outcome distribution (5-point Gauss-Hermite per scenario plus the blow-up point) is reweighted so that
P(blow-up) and P(≤0.5x) equal the anchored values. Each group (blow-up / other ≤0.5x / >0.5x) is scaled in proportion,
so its shape is kept. If the model has no non-blow-up mass at or below 0.5x, the extra mass goes to a 0.35x point.
Because a model blow-up ends at or below 0.5x, the ≤0.5x target is floored at the anchored blow-up
(the v2 India class has blow-up 15% > ≤0.5x 11%, because the blow-up definition includes an intra-horizon 80%
drawdown). The anchored EV keeps the worksheet's convention (scenario `mult5` treated as the mean): it is
`ev_mult5 + (EV of the anchored outcomes − EV of the raw outcomes)`. P(≥3x) is shown but not anchored. With no
base rate for a tail (for example FEDERALBNK: no bank class), the raw value is used and the card says so. Anchoring is
two-sided: a model tail fatter than the base rate is pulled *down*. **Paper calls keep the raw model probability** in
`probability` and add `anchored_probability` and `anchor_weight`, so stage-7 Brier scoring can test raw against
anchored against base. The method id stays `decision-card-v1` (scoreboard grouping) and `card_version` is added.

**Regression (`calibration_2026-11-23/v1.2/`, no `--calls`):** all 6 cards still size 0, and every blocking reason is the
same as in v1.1. No card is in an India PEAD avoid window, so the survival cap is `n/a` on all of them. Anchoring lowers EV slightly on every
card with a base rate: VMM 1.46x → 1.45x, CUMMINSIND 1.33x → 1.25x, FIVE 1.19x → 1.14x, SUNFLAG 1.38x → 1.37x,
US-KEX 1.16x → 1.11x (persistent 1.17x → 1.11x). FEDERALBNK has no class, so it is unchanged at 1.36x. Full Kelly f*
stays 0.0% everywhere. The SYNTHETIC example still opens at 4.0%. Its anchored EV is 3.43x vs 3.42x raw, because its
deprecated class has a *thinner* ≤0.5x tail than the model (and no blow-up rate).

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
| Stage 3 survival cap (v1.2) | **India only:** PEAD avoid flag active AND (promoter pledge > 25% of promoter holding OR interest cover < 1.5x), or either input unchecked while the flag is active → 0 new money (hold-review if owned) + balance-sheet question | L35, `decision:pead-avoid-plus-redflag-survival-cap` |
| Stage 3 survival cap, manual trigger (v1.4) | `survival.core_asset_threat` with a description (government lease / licence / concession threat) → same as a red flag: PEAD window → 0 new money, otherwise starter size, no additions | L40 |
| Expected value | **anchored** EV of the 5-year multiple < hurdle multiple (index CAGR^5); v1.2 uses outside-view-anchored tails (raw EV shown alongside) | L36 |
| Kill criteria | missing or undated | — |
| Outside-view check (note only) | model P is >2x or <0.5x the base rate | `insight:lit-base-rate-neglect-outside-view` |
| Size outside the class (note only, v1.1) | market cap outside the class `size_band` (same money units) | `base_rates.json` |

## Sizing rule
`size = min(kelly_fraction × f*, tier cap at cost, liquidity cap)`, then 0 if any gate blocks.
- `f*` maximises `E[ln(1 + f·(M/H − 1))]` over the scenario outcomes, after v1.2 tail anchoring (the raw-model f* is shown alongside) (each spread by 5-point Gauss-Hermite on σ, with the blow-up as a point mass). `H` is the index hurdle multiple, so the bet is measured against the alternative.
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
