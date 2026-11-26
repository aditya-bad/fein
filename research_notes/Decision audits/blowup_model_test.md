# Blow-up probability model: out-of-sample calibration test (pre-registration, 2026-11-26)

**Stage:** 6 (decision). **Unlocks:** an anchor for the card's blow-up probability that is calibrated out of sample
(or a recorded "no"), ready to go into the post-season card patch with v1.6, so stage-7 scoring tests a card whose
blow-up tail matches history. Parent: L48 (`research_notes/Decision audits/card_fixes_historical_test.md` §B2: every
card variant under-predicts blow-ups — India 10.5% vs 15.5%, lenders 16.3% vs 27.1%, US 10.1% vs 15.3%).
**Status of §A: written and saved BEFORE any number in §B was computed.** No live card or card code is changed.

## A. Pre-registration (frozen 2026-11-26, before computing)

### A1. Panels, rows, outcome (same rows and weights as L48 / card_fixes_historical_test.py `load()`)
| Panel | Rows | Weight | Cohorts (LOCO folds) | Features available |
|---|---|---|---|---|
| P1 India non-fin, mcap ₹1,000–20,000 cr | `solvency_india_outputs/panel.csv` (+ `pledge`/`B25` joined from `hard_filters_india_v2_outputs/panel_v2.csv` on key+snap) | stratum `weight` | FY2016, FY2018 | B25, S2, S1, S5, size |
| P2 India lenders ₹1,000–20,000 cr | `base_rates_lenders_india_outputs/panel.csv` | 1 | FY2016, FY2018 | size only (no pledge in the file; the card does not apply ICR to lenders) |
| P3 US float $0.5–10B | `solvency_us_outputs/panel.csv` | 1 | 2015, 2017, 2019 | S1, S2, S5, size |

Row rule (as L48): R missing and failed → kept (R = 0); R missing and not failed (incl. acquired) → excluded.
Outcome y = blow-up = `o_fail` / `O_fail` (card definition minus fraud findings). Unknown flag → 0 (not fired).

### A2. Features (binary, ≤ 4 per panel, fixed now)
- B25 = promoter pledge > 25% of promoter holding (latest June SHP ≤ T). S2 = EBIT/interest < 1.5x (panel flag `s2`/`S2`).
- BOTH = B25 ∧ S2 (India only). S15 = S1 ∨ S5 (India; S1 = negative net worth adj., S5 = ≥2 of S1/S2/S4).
- SMALL = size below the **training fold's** weighted 1/3 quantile of size within the class (mcap; US float).
- **P1 India non-fin: {B25, S2, BOTH, S15}** — SMALL is left out to keep ≤ 4 (pledge/ICR are the card's own triggers;
  SMALL reported univariately). **P2 lenders: {SMALL}.** **P3 US: {S1, S2, S5, SMALL}.**
- PEAD bottom quintile is not observable on the 5-yr start-cohort panels (SUE exists only on the quarterly event file);
  it enters only the secondary event panel (A6).

### A3. Model (primary M1) and comparators
- **M1 = L2-penalised logistic regression**, intercept unpenalised, prior N(0, 1) on each coefficient (penalty ½β²),
  training weights normalised to mean 1, fitted by Newton's method on the training fold only. Prediction clipped to
  [0.02, 0.60]. (Base rate × likelihood ratios was considered and rejected as primary: the flags are correlated, so
  multiplying LRs double-counts.)
- **B = class base rate alone** = weighted blow-up rate of the training fold (same for every firm in the test fold).
- **Card comparators** (scenario blow-up p = 0.05, the L48 card-shaped set, anchor weight 0.5):
  C0 = current v1.5 anchoring = 0.5·B + 0.5·0.05; **C1a** = 0.5·B + 0.5·max(0.05, M1) (model replaces the scenario p,
  anchoring kept); **C1b** = max(C0, M1) (model as a floor on the anchored value); C2 = max(C0, B) (base-rate floor).
- **Split:** leave-one-cohort-out within each panel (primary). **By market (secondary, reported):** coefficients of
  {S1, S2, S5} fitted on all US rows, applied to India non-fin with the intercept re-set so the mean prediction on the
  India training fold equals its B; scored on the India held-out fold.

### A4. Metrics (firm-weighted, test folds pooled after LOCO)
Brier of P(blow-up); binary log score (mean ln p(y)); **calibration-in-the-large (CITL) = mean predicted − realised
rate**; reliability table by predicted decile (P3) or by predicted quintile (P1, P2: too few rows for deciles);
AUC (diagnostic). Fitted coefficients per fold reported.

### A5. Adoption rule
**M1 is adopted** if, out of sample, its Brier is lower than B's on **≥ 2 of the 3 panels**, AND on each panel counted
as a win its CITL is within **±3pp**. (CITL is also reported for B and C0 so a cohort-shift failure is visible as
such, not blamed on the flags.)
- If adopted, the card patch uses whichever of C1a / C1b has the lower mean Brier over the 3 panels (tie → C1b);
  it must also beat C0 on Brier on ≥ 2 of 3 panels, else no card patch and the model stays a reported number.
- **Rule B (fallback, decided now):** if M1 is not adopted, C2 (base-rate floor) is proposed instead only if it beats
  C0 on Brier on ≥ 2 of 3 panels with |CITL| ≤ 3pp on those panels. Otherwise: no change.
- Any patch is written unapplied with tests, to apply after the Jan–Feb 2027 season together with v1.6.
- Same caveat as L48: 2–3 start dates in a strong small-cap window; 15–29 blow-ups per India panel → wide noise.

### A6. Secondary event panel (reported, never decides)
`survival_cap_general_outputs/events_out.tsv`: non-financial events, mcap ₹1,000–20,000 cr, `fail3` defined (3-yr
≤0.2x or series stop), LOCO by entry calendar year. Features {PEADQ1 = SUE in the bottom quintile of its quarter-end
(qe), B25, S2, SMALL}; same M1 vs B metrics. Events overlap within firms (no independence claimed).

_Research, not SEBI-registered advice._

---
## B. Results
_(to be filled after computing; §A is frozen)_
