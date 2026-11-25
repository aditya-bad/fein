# Card fixes (3) right-tail anchoring and (4) sigma: historical test (pre-registration addendum, 2026-11-25)

**Stage:** 6 (decision). **Unlocks:** a v1.6 card spec (or "no change") ready before the Jan–Feb 2027 season, so stage-7
scoring tests a card whose tails match history. Parent records: `decision:card-audit-fixes-prereg-2026-11-25` (v2,
amended), audit `research_notes/Decision audits/card_no_machine_audit_2026-11-25.md`.
**Status of this section: written and saved BEFORE any number below §A was computed.** Nothing in the live card code
or the 8 live cards is changed by this work.

## A. Pre-registration (frozen 2026-11-25, before computing)

### A1. Panels and realised outcome (same rows as `tools/backtests/base_rates_5y/` and `base_rates_lenders_india/`)
| Panel | Rows | Weight | Cohorts (start) | Realised 5-yr multiple R |
|---|---|---|---|---|
| India non-fin, mcap ₹1,000–20,000 cr | `solvency_india_outputs/panel.csv` | stratum `weight` | FY2016, FY2018 | `r5` (price only); no `r5` and `o_fail`=1 → R = 0; no `r5`, not failed → excluded |
| India lenders ₹1,000–20,000 cr | `base_rates_lenders_india_outputs/panel.csv` | 1 | FY2016, FY2018 | same rule |
| US float $0.5–10B | `solvency_us_outputs/panel.csv` | 1 | 2015, 2017, 2019 | `R5` (adj. close); unpriced + `O_fail` → 0; other unpriced (incl. acquired) excluded |

Events: ≥3x = R ≥ 3; ≤0.5x = R ≤ 0.5; blow-up = `o_fail`/`O_fail` (card definition minus fraud findings).

### A2. Forecast each firm gets (no firm's own outcome is used)
**Primary = leave-one-cohort-out (LOCO).** A firm in cohort c gets the forecast built from the *other* cohort(s) of the
same panel only (median, class tail rates, class σ). This avoids scoring a forecast with the data it was fitted on.
- **Centre** M = weighted median of R in the other cohort(s).
- **Scenario set (fixed, the audit's "card-shaped" set, i.e. the live-card pattern bear > bull):** bear p 0.25 at
  0.65·M; base p 0.50 at M; bull p 0.20 at 1.45·M; blow-up p 0.05 at 0.10x. Each scenario multiple is the *median* of a
  lognormal with the variant's σ (as the worksheet does); blow-up is a point mass.
- **Left-tail anchoring (current v1.5):** w = 0.5; P(blow-up) → 0.5·base + 0.5·0.05; P(≤0.5x) → 0.5·base + 0.5·model,
  floored at the anchored P(blow-up); regions (≤0.5x non-blow-up) and (>0.5x) rescaled in proportion (continuous form of
  `anchor_outcomes`).
- **Two-sided anchoring (fix 3):** additionally P(≥3x) → 0.5·base + 0.5·model; the region ≥3x is rescaled to that mass
  and (0.5x, 3x) takes the rest, shape kept within each region.
- **σ (fix 4):** current 0.35 vs σ_class = robust log-SD = IQR(ln R)/1.349 over priced rows (R > 0) of the other
  cohort(s), weighted. (The pooled India non-fin figure in the audit was ~0.68.)
- Base tail rates for anchoring = the other cohort(s)' P(≥3x), P(≤0.5x), P(blow-up), computed with the A1 rules.

**Secondary (reported, does not decide):** in-sample pooled version (centre, rates, σ from the whole panel — circular
for anchoring, shown only to separate "shape" from "cohort shift").

### A3. Variants
V0 = σ 0.35, left-only (current card). V1 = σ_class, left-only (fix 4 alone). V2 = σ 0.35, two-sided (fix 3 alone).
V3 = σ_class, two-sided (both; reported).

### A4. Metrics (firm-weighted means within each panel, cohorts pooled after LOCO)
1. **Primary: 5-bin log score** — mean ln(predicted probability of the bin R fell in); bins (0, 0.5], (0.5, 1],
   (1, H], (H, 3), [3, ∞), H = the market's 5-yr hurdle (India 1.7623x, US 1.4693x). Higher is better.
2. Brier of the three events P(≥3x), P(≤0.5x), P(blow-up); plus predicted − realised frequency (calibration gap).
3. Coverage of the central 50% and 80% intervals of the predicted R distribution (fraction of realised R inside;
   error = |coverage − nominal|).
4. Diagnostic only: predicted mean vs realised mean of R (relevant to fix 1, mean/median).

### A5. Adoption rule (each fix judged against V0 on its own: fix 4 = V1 vs V0, fix 3 = V2 vs V0)
A fix **passes the historical test** if, in the primary (LOCO) run, its 5-bin log score is **higher by ≥ 0.005 nats/firm
on ≥ 2 of the 3 panels and not lower by more than 0.005 on the third**, AND the sum of the three event Brier scores is
not worse by more than 0.002 on any panel (guard). Coverage is reported, not decisive. Per the amended parent prereg, a
pass here is **necessary but not sufficient**: adoption also needs "does not worsen Brier on the near-term live calls"
(8 beat-the-index calls to 30-Sep-2027 + Q3/FY27 metric calls) — that half stays open until they resolve. No re-issue of
any dated card; live-card effects (EV, f*, size) are reported for information only.

### A6. Patches (not applied)
Fix (1) mean/median convention and fix (5) bear>bull shape warning are written as a patch file with tests, to apply after
the season per the parent prereg. Chosen convention for (1): scenario `mult5` is the **median** everywhere (as the
worksheet tails already assume); the EV gate uses the mean of the same outcome distribution Kelly uses.

_Research, not SEBI-registered advice._

---
## B. Results (computed after §A was saved; `card_fixes_historical_test.py`, `card_fixes_live_effect.py`, read-only)

### B1. Primary (leave-one-cohort-out). V0 = card today (σ 0.35, left-only); V1 = σ_class; V2 = two-sided; V3 = both
LOCO inputs: India non-fin M 2.02x / 1.47x (forecast for FY2016 / FY2018), σ_class 0.69 / 0.62; lenders M 1.73x / 0.60x,
σ 0.60 / 0.88; US M 1.13–1.24x, σ 0.68–0.77. (Pooled σ_class: India non-fin 0.682, lenders 0.981, US 0.700.)

| Panel (n) | Var | 5-bin log score | Σ Brier (3 events) | P(≥3x) pred / real | P(≤0.5x) pred / real | P(blow-up) pred / real | 50% / 80% coverage | mean R pred / real |
|---|---|---|---|---|---|---|---|---|
| India non-fin (205) | V0 | −1.760 | 0.4316 | 9.5% / 21.3% | 10.5% / 11.3% | 10.5% / 15.5% | 35% / 60% | 1.67 / 2.24 |
| | V1 | −1.626 | 0.4212 | 19.2% | 10.7% | 10.5% | 47% / 76% | 2.02 |
| | V2 | −1.660 | 0.4206 | 15.3% | 10.5% | 10.5% | 37% / 67% | 1.79 |
| | V3 | −1.614 | 0.4182 | 20.1% | 10.7% | 10.5% | 48% / 77% | 2.04 |
| India lenders (107) | V0 | −3.075 | 0.5862 | 4.0% / 11.2% | 27.3% / 25.2% | 16.3% / 27.1% | 12% / 53% | 1.08 / 1.49 |
| | V1 | −1.965 | **0.5981** | 10.1% | 28.9% | 16.3% | 22% / 67% | 1.34 |
| | V2 | −2.519 | 0.5864 | 7.6% | 27.3% | 16.3% | 12% / 53% | 1.16 |
| | V3 | −1.967 | 0.5994 | 10.6% | 28.9% | 16.3% | 22% / 68% | 1.36 |
| US float (2,226) | V0 | −1.750 | 0.3934 | 1.2% / 9.8% | 14.1% / 19.9% | 10.1% / 15.3% | 33% / 65% | 1.12 / 1.49 |
| | V1 | −1.582 | 0.3837 | 9.5% | 19.3% | 10.1% | 50% / 80% | 1.42 |
| | V2 | −1.632 | 0.3881 | 5.5% | 14.1% | 10.1% | 36% / 70% | 1.22 |
| | V3 | −1.583 | 0.3839 | 9.6% | 19.3% | 10.1% | 50% / 80% | 1.42 |

Changes vs V0 (rule §A5: log score +≥0.005 on ≥2 panels, none worse by >0.005; Σ Brier not worse by >0.002 anywhere):

| Fix | Δ log score (India / lenders / US) | Δ Σ Brier (India / lenders / US) | Verdict |
|---|---|---|---|
| (4) σ 0.35 → σ_class | +0.135 / +1.110 / +0.167 | −0.0104 / **+0.0120** / −0.0097 | **FAILS** (Brier guard, lenders) |
| (3) two-sided anchoring | +0.100 / +0.556 / +0.118 | −0.0110 / +0.0002 / −0.0053 | **PASSES** the historical half |

Secondary (in-sample pooled, not decisive): both pass (σ: Δ log score +0.078 / +0.394 / +0.167, Δ Brier −0.018 / −0.016 /
−0.011; two-sided: +0.076 / +0.234 / +0.121, Δ Brier −0.014 / −0.009 / −0.006).

### B2. Reading
- **σ = 0.35 is too narrow on every panel**: the card's own 50% interval caught 12–35% of outcomes and its 80% interval
  53–65%. σ_class brings coverage to ~nominal on India non-fin and US (47–50% / 76–80%) and lifts the whole-distribution
  log score a lot. It still **fails the pre-registered rule**: on lenders the wider σ raises the model P(≤0.5x), which the
  left anchoring then mixes in at 50%, so P(≤0.5x) over-shoots (28.9% vs 25.2%) and Σ Brier worsens by 0.012. The lender
  LOCO test is harsh (cohort medians 0.60x vs 1.73x), but the rule was fixed in advance: **fix (4) is not adopted**. A
  re-test (e.g. σ_class with the ≤0.5x tail not double-counted) would need its own new pre-registration.
- **Two-sided anchoring passes**: P(≥3x) moves from 0.12–0.45× the realised rate to 0.56–0.72×, log score up on all three,
  Brier guard held (lenders +0.0002). Per the amended parent prereg this is **necessary, not sufficient**: adoption still
  waits for the near-term live calls (to 30-Sep-2027) not to get worse.
- **Not fixed by either:** P(blow-up) is under-predicted in every variant (10.5% vs 15.5%; 16.3% vs 27.1%; 10.1% vs
  15.3%): a 5% model blow-up at w = 0.5 only gets two-thirds of the way to the base rate. The predicted mean is below the
  realised mean in all variants (India 1.67–2.04 vs 2.24): the bear>bull scenario shape (fix 5) is part of this.
- Caveats: two/three start dates in a strong small-cap window (2016–2023); India R is price-only; the forecast is the same
  for every firm in a cohort, so this tests the card's *shape and dispersion*, not stock picking.

### B3. Effect on the 8 live cards (in memory; no card re-issued, nothing written)
Anchored EV (gate) / size after gates. Fix (1) = proposed v1.6 EV convention (gate = mean of the outcome distribution).
Hurdle 1.762x India, 1.469x US.

| Card | Today (v1.5) | + fix 3 | + fix 1 | + fix 1 + fix 3 | info: fix 1 + 3 + 4 |
|---|---|---|---|---|---|
| AUTOAXLES | 1.40 / 0 | 1.66 / 0 | 1.49 / 0 | 1.75 / 0 | 2.04 / 4.0% |
| HARSHA | 1.58 / 0 | **1.87 / 4.0%** | 1.66 / 0 | **1.94 / 4.0%** | 2.12 / 4.0% |
| INDRAMEDCO | 1.39 / 0 | 1.58 / 0 | 1.45 / 0 | 1.64 / 0 | 1.83 / 0.8% (survival cap ≤1%) |
| SHK | 1.59 / 0 | 1.48 / 0 ¹ | 1.69 / 0 | 1.58 / 0 | 1.92 / 1.9% |
| SUNFLAG ² | 1.44 / 0 | 1.96 / 1.0% | 1.55 / 0 | 2.08 / 1.0% | 2.21 / 1.0% |
| — with india_nonfin class | 1.37 / 0 | 1.61 / 0 | 1.48 / 0 | 1.72 / 0 | 1.77 / 0.1% |
| UTKARSHBNK | 1.23 / 0 | 1.38 / 0 | 1.31 / 0 | 1.45 / 0 | 2.21 / 2.0% |
| UTTAMSUGAR | 0.89 / 0 | 1.30 / 0 | 0.95 / 0 | 1.36 / 0 | 1.37 / 0 |
| US-KEX ³ | 1.12 / 0 | 1.12 / 0 | 1.17 / 0 | 1.17 / 0 | 1.43 / 0 |

¹ SHK: the 5-point Gauss-Hermite grid puts 22.7% of mass at ≥3x vs the continuous model's 13.6%, so anchoring to 17.4%
*lowers* it — a quadrature artefact. A fix-3 patch should anchor on a finer grid (≥ 20 points) or the continuous tail.
² SUNFLAG names the deprecated survivor class (P(≥3x) 44% placeholder), which inflates two-sided anchoring; on the
correct class it stays 0. ³ US-KEX names a deprecated class with null tails → no anchoring at all (housekeeping fix 6).
- With only the fix that passed (3), **one live card would open: HARSHA at the 4% cap** (EV 1.87x; its gap was the smallest
  in the audit). With fix 1 too, still only HARSHA. The fix-4 column shows why σ matters more after fix 1: the mean of a
  lognormal is median·e^{σ²/2}, +6% at σ 0.35 but +26% at 0.68, so σ becomes an EV lever — another reason not to adopt it
  without a passed test.
- Under fix 1 alone, 7 of 8 live cards would get the new shape warning (all but HARSHA).

### B4. Proposed patch (not applied): `tools/decision/patches/v1.6_fix1_mean_median_fix5_shape_warning.patch`
Fix (1): `dist_mean()`; the EV gate and the "raw" EV become the mean of the same (anchored) outcome list Kelly uses, i.e.
`mult5` is a median everywhere; worksheet Σp·mult5 still shown, relabelled; decision data adds `ev_mult5_dist_raw`,
`ev_convention`. Fix (5): `scenario_shape_warning()` — P(bear) > P(bull) AND scenario mean < base → non-blocking gate row +
warning. Card version → 1.6. 6 new tests; the byte-identical rebuild test skips (not fails) when no stored card is at the
new version (dated cards are never re-issued). Checked: applies cleanly (`git apply --check`), 56 tests pass (1 skip) on a
patched copy. Apply after the Jan–Feb 2027 season per the parent prereg: `git apply tools/decision/patches/<file>`.

### B5. Next
- Fix (3): write a v1.6.1 patch (two-sided anchoring on a finer grid) now; apply only if the near-term live calls (to
  30-Sep-2027) are not worse.
- Fix (4): not adopted. If revisited, pre-register σ_class *with* a left-tail treatment that avoids double counting.
- P(blow-up) under-prediction persists under every variant: a candidate for the next pre-registration (stage 7).
