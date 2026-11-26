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
## B. Results (computed after §A was saved)

**Order of work (audit trail):** §A saved 2026-11-26 07:30:33 UTC; `tools/backtests/blowup_model/blowup_model.py` written
07:31:16; `research_notes/Backtests/blowup_model_outputs/results.json` written by its single run at 07:31:18 — i.e.
**results.json was computed AFTER the pre-registration was saved** (file mtimes; both files are unchanged since and are
identical to the WIP commit fcff33f made by the lead at 12:28 UTC). §A text was not edited after computing; this §B is
the only addition. Post-hoc diagnostics below are labelled as such.

### B1. Primary (leave-one-cohort-out), P(blow-up) over 5 years
| Panel (n, blow-ups) | Forecast | Brier | Log score | Mean pred / realised | CITL | AUC |
|---|---|---|---|---|---|---|
| India non-fin (205, 58 unweighted; 15.5% weighted) | **M1** | **0.1357** | −0.457 | 16.2% / 15.5% | **+0.7pp** | 0.45 |
| | B (base rate) | 0.1409 | −0.470 | 16.1% | +0.6pp | — |
| | C0 (card v1.5) | 0.1374 | −0.468 | 10.5% | −4.9pp | — |
| | C1b = max(C0, M1) | 0.1357 | −0.457 | 16.2% | +0.7pp | 0.45 |
| India lenders (107, 29; 27.1%) | M1 (size only) | 0.2150 | −0.628 | 28.0% / 27.1% | +0.9pp | 0.44 |
| | **B** | **0.2136** | −0.625 | 27.5% | +0.4pp | — |
| | C0 | 0.2160 | −0.650 | 16.3% | −10.8pp | — |
| | C1b | 0.2150 | −0.628 | 28.0% | +0.9pp | — |
| US float (2,226, 341; 15.3%) | **M1** | **0.1194** | −0.392 | 15.4% / 15.3% | **+0.1pp** | 0.70 |
| | B | 0.1306 | −0.432 | 15.3% | 0.0pp | — |
| | C0 | 0.1328 | −0.444 | 10.2% | −5.2pp | — |
| | C1b | 0.1198 | −0.394 | 16.5% | +1.2pp | 0.70 |

Card variants, mean Brier over the 3 panels: C1a (model replaces scenario p, anchoring kept) 0.1577; **C1b (model as a
floor on the anchored value) 0.1568** → C1b chosen by the §A5 rule; C1b beats C0 on **all 3** panels
(India −0.0017, lenders −0.0010, US −0.0130). C2 (base-rate floor) beats C0 on lenders and US only (India +0.0035).

Fitted coefficients (log-odds, prior N(0,1)), LOCO folds: India {B25 0.35–0.52, S2 0.26–0.41, BOTH 0.43–0.74, S15
0.32–0.55}; lenders SMALL 0.46–0.58; US {S1 0.30–0.54, **S2 1.35–1.45**, S5 0.20–0.34, SMALL 0.64–0.84}. Full-panel fit
(for the card): India const −1.876, B25 0.460, S2 0.387, BOTH 0.759, S15 0.384; lenders const −1.205, SMALL 0.604
(cut ₹3,480 cr); US const −2.440, S1 0.408, S2 1.401, S5 0.246, SMALL 0.755 (cut $1,271M float).
Raw rates (pooled, weighted): India B25 28.7% (36 firms), S2 27.8% (42), BOTH 57.6% (15), S15 38.6% (9) vs 15.5% all.

Reliability (M1, by predicted bin, pred → realised): US deciles 6.7→9.4, 7.2→9.9, 8.5→5.9, 8.6→4.0, 8.8→6.8, 11.4→9.9,
14.6→21.5, 17.6→15.3, 26.5→32.3, 43.7→38.3 (monotone at the top, good). India quintiles 8.4→21.7, 9.3→19.1,
17.8→14.2, 19.7→9.1, 26.2→13.3 (**inverted — see B3**). Lenders quintiles flat/noisy (17–44% pred vs 19–43% real).

### B2. Verdict by the pre-registered rule (§A5)
- M1 Brier < B on **India non-fin (−0.0052) and US (−0.0112)**; loses on lenders (+0.0014). CITL on the two wins
  +0.7pp and +0.1pp (within ±3pp). → **M1 ADOPTED** by the rule. Card form = **C1b: P(blow-up) used = max(anchored,
  model)**, which beats the current card on all 3 panels and moves CITL from −4.9 / −10.8 / −5.2pp to +0.7 / +0.9 / +1.2pp.
- Rule B not reached (M1 adopted). Proposed patch, unapplied: `tools/decision/patches/v1.6b_blowup_model_floor.patch`
  (applies on top of the v1.6 patch: `git apply` v1.6 first, then v1.6b; checked `git apply --check` on a v1.6-patched
  copy, 61 tests pass, 1 skip; 6 new tests). Apply after the Jan–Feb 2027 season together with v1.6.

### B3. Honest reading (what the pass does and does not show)
- **US: real discrimination.** Within-cohort AUC 0.69 / 0.72 / 0.75 (post-hoc diagnostic), driven by S2 (interest cover
  < 1.5x; flagged firms blow up 32–39% vs 9–12%) and SMALL. The US win is the solid part.
- **India non-fin: the win is mostly a level effect, not ranking.** Within-cohort AUC only 0.56 (FY2016) / 0.60 (FY2018)
  (post-hoc); pooled AUC 0.45 and the inverted reliability come from the cohort shift: the FY2016 cohort (real 21.6%) is
  forecast from FY2018's 10.0% base and vice versa (real 10.0%, forecast 21.6%). Pooled CITL +0.7pp passes **because the
  two ±11–12pp cohort errors cancel** — per cohort, both B and M1 miss by ~±11pp. The flags still carry information
  (BOTH 58% vs 15% pooled), but with 15 BOTH firms the coefficients are noise-wide.
- **Lenders: size alone does not help** out of sample; the model there equals base rate ± a size bump. The floor still
  helps the card on lenders because the card's 16% is far below the 27% base rate, not because of the model.
- **Cross-market (secondary):** US-fitted {S1, S2, S5} on India with re-set intercept: Brier 0.1381 (vs B 0.1409, M1
  0.1357), CITL +0.2pp, AUC 0.48 — transports weakly; India should keep its own fit.
- **Event panel with PEAD (secondary, India, 3-yr ≤0.2x, 4,660 events, LOCO by entry year):** M1 Brier 0.0508 vs B
  0.0529, CITL +0.2pp. PEAD bottom quintile adds little (coef 0.10–0.51; flagged 4–8% vs 3–6%); B25 dominates (coef
  1.6–2.0; 13–27% vs 2–4%). Consistent with L39: pledge is the India survival signal, PEAD is not.
- Most of the card improvement is simply **"stop pulling P(blow-up) below the base rate"**: C0's 0.5·base + 0.5·5% is
  what under-predicts. The model adds firm-level spread on top (large in the US, small in India).
- Caveats as L48: 2–3 start dates in 2015–2023; India R price-only; 58/29 India blow-ups; flags unknown → 0.

### B4. Effect on the 9 live cards (v1.6 + v1.6b, information only; no card re-issued)
India non-fin cards with no flag get model P(blow-up) 13.3% (anchored v1.5/v1.6: 10.2–12.7%); UTKARSHBNK (lender,
SMALL) 35.4% (anchored 18.6%); INDRAMEDCO keeps its higher anchored 18.6%; SUNFLAG / US-KEX name deprecated classes → no model.
v1.6 EV (fix 1) → v1.6+v1.6b EV: AUTOAXLES 1.49 → 1.45, HARSHA 1.66 → 1.61, UTKARSHBNK 1.31 → 1.10, others unchanged
(to 2 dp: SHK 1.69, UTTAMSUGAR 0.95, INDRAMEDCO 1.45, VIYASH 1.15). All 9 stay size 0. The floor makes the card stricter, never
looser.

### B5. Next
- Apply v1.6 + v1.6b after the season (with fix 3's v1.6.1 if its live half passes). Cards then need `survival.s1/s5`
  filled (optional; unknown = 0).
- Re-fit when more India start cohorts exist (FY2014, FY2020 snapshots would triple the folds); the India cohort level
  (10% vs 22%) is the bigger calibration risk than the flags.
