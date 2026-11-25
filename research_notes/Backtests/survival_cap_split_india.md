# Back-test: should the survival cap treat pledge and weak interest cover differently? (Roadmap stages 2 → 6)

*Method calibration, not stock picking. Research, not SEBI-registered advice.*
Started 2026-11-25. Builds **stage 2 (hard filters)** and feeds **stage 6** (the decision card's survival cap,
`tools/decision/decision_card.py` v1.4). Follows L39 / `survival_cap_general_india.md`, whose post-hoc reading was:
pledge > 25% looked bad on both tails (more failures *and* fewer 3x winners, negative 3-year excess in the snapshot
panel), while interest cover < 1.5x mostly widened the spread (more failures and more winners). That reading was not
pre-registered. This file tests a split rule.
**Unlocks:** if adopted, the card distinguishes a "0 new money" pledge tier from the starter-size cap (stage 6), the
nightly pledge screen becomes a near-veto feed (stage 2), and stage-4 deep dives on pledged promoters start with the
pledge-lender terms. If not adopted, v1.3/v1.4 stays as is (one trigger, starter size, no additions) and the split
idea is closed until new data (e.g. 2026+ events) exist.

## PRE-REGISTRATION (written 25-Nov-2026, before any outcome below was computed)

### State of knowledge (honest — this is NOT a blind test)
Already published (survival_cap_general_india.md results, L39), for the *overlapping* single flags:
- E (events, non-financial): B25 H12 RR 3.10 [2.36, 3.97], FAIL3 5.88; B50 H12 3.46, FAIL3 6.26; S2 H12 2.12, FAIL3 3.54.
  Winner share flagged vs event share flagged: B25 15.4% / 9.8%, B50 11.0% / 6.0%, S2 22.1% / 16.4% — i.e. in E even
  pledge was flagged on *more* than its share of winners. Card-level WIN3 RR 1.46 in 2018–21, 1.07 in 2022–25.
- P (snapshots, weighted): B25 H12 1.76 [1.01, 2.82], O_fail 2.63, winners 0.55× [0.19, 0.99], 3-year excess
  −41.9 pp; S2 O_fail 2.01, H12 1.38, winners 1.08×.
What has **not** been computed anywhere: the four **mutually exclusive** groups (pledge-only, ICR-only, both,
neither), the single flags by period, pledge-only by period, and firm-cluster CIs in P. B25 overall already being
known means the pledge-only results are partly predictable (pledge-only is a large part of B25), so:
- **E full sample = re-estimate, not blind.**
- **Replication** = (i) the **period split of E** (2018–21 vs 2022–25 entries): the group-by-period numbers have never
  been computed, though the card-level period numbers have; (ii) **P**, which is the only survivorship-free sample but
  whose B25 numbers are already known. Neither is fully blind; I state this in advance and the rule below asks for
  agreement across all three slices (E-early, E-late, P) rather than any one.
Expectation written now (so a surprise is visible): from the known numbers I expect pledge-only to pass the halving
bar in E, to *fail* the winner bar in E (E showed pledge on more than its share of winners), and to be marginal in P
(B25 H12 was 1.76 < 2.0). My prior is therefore **NOT ADOPTED** for the pledge tightening.

### Samples (reused, no new fetches)
- **E (events):** `survival_cap_general_outputs/events_out.tsv` (10,242 firm-quarter results 2018–2025, ₹500–50,000 cr,
  flags as of the event, outcomes exactly as computed in the general test: halve12, fail3, win3, xs156, xs52).
  Primary = non-financial (fin = 0). Censoring as before (3-year outcomes need an uncensored 156-week window ⇒ entries
  to ~Nov-2023).
- **P (snapshots):** `survival_cap_general_outputs/panel_out.tsv` (489 company-snapshots, T = 30-Sep-2016 and
  30-Sep-2018, ₹200–20,000 cr, non-financial, survivorship-free, sampling weights D 1 / X 4.264 / L 5.633).

### Groups (both flags must be known; else excluded and counted)
- **G0 unflagged:** pledge ≤ 25% and interest cover ≥ 1.5x (B25 = 0, S2 = 0).
- **Gp pledge-only:** B25 = 1, S2 = 0. **Gi ICR-only:** B25 = 0, S2 = 1. **Gb both:** B25 = 1, S2 = 1.
- **B50:** pledge > 50% (any interest cover) vs G0; **B50-only:** B50 = 1, S2 = 0 vs G0 (reported).
- Every group is compared with **G0**. Also reported: Gp vs Gi directly (WIN3 RR and XS156 difference).

### Outcomes (as defined in survival_cap_general_india.md, unchanged)
- **H12** 12-month halving (E: halve12; P: h12).
- **FAIL3** 3-year failure (E: ≤ 0.2× within 156 weeks or distress-listed firm stopped trading). P has no 3-year
  failure field; its failure outcome is **O_fail (5-year)** as published — reported in the FAIL row, labelled 5-yr.
- **WIN3** ≥ 3x within 3 years (E: win3 at 156 weeks; P: `winner`, 5-year ≥ 3x — labelled 5-yr).
- **XS156** 3-year price return minus the mean of size-matched controls (mean, and median reported). XS52 reported.

### Inference
- RR = P(outcome | group) ÷ P(outcome | G0); for XS156 the difference in means.
- **E: firm-cluster bootstrap** (resample firms with replacement with all their events; 5,000 draws, seed 1).
- **P: firm-cluster bootstrap within stratum** (resample firms — the ISIN key, so the 2016 and 2018 snapshots of a
  firm move together — within D / X / L; weighted rates; 5,000 draws, seed 1). This fixes the slightly narrow P CIs
  flagged in the general test.
- Period split of E by entry year: 2018–21 vs 2022–25.
- Minimum size: a criterion on a group/slice with < 30 outcome-eligible events or < 15 firms (E), or < 20 snapshots (P)
  counts as **not met** (insufficient data), not as passed.

### Decision rules (fixed now)
**Rule T (tighten pledge: → 0 new money outside the PEAD window; already owned → hold, no adds).** Candidate groups,
in this order: (1) **Gp** → if it passes, the tighter rule applies to *any* pledge > 25% (Gp ∪ Gb), provided Gb's
WIN3 RR point estimate is also ≤ 1.0 in E; (2) else **B50** → if it passes, the tighter rule applies to pledge > 50%;
(3) else **Gb** → if it passes, it applies to pledge > 25% *and* interest cover < 1.5x. A candidate passes only if
ALL of:
- **T1 (E full, non-financial):** WIN3 RR ≤ 1.0 with firm-cluster CI upper < 1.2, AND H12 RR ≥ 2.0 with CI lower > 1.3.
- **T2 (P):** winner RR ≤ 1.0 with CI upper < 1.2, AND H12 RR ≥ 2.0 with CI lower > 1.0.
- **T3 (E period replication):** in both 2018–21 and 2022–25, WIN3 RR point ≤ 1.0 and H12 RR point ≥ 2.0.
- **T4 (no upside being blocked):** XS156 mean difference vs G0 ≤ 0 (point) in E and in P.
If T1 + T3 + T4 pass but T2 fails only on the P CI widths (points on the right side), → **PROVISIONAL**: record as a
"look harder / prefer 0" note, no code change. Anything else → **NOT ADOPTED** (keep v1.3/v1.4).
Testing three nested/overlapping candidates is a multiple-comparison risk; the strict all-slices requirement is the
guard, and it is stated now.

**Rule L (loosen interest cover alone: Gi → no cap, "look harder" only).** Because the costs are asymmetric (L27),
loosening needs evidence of *no* tail signal: Gi H12 RR CI upper < 1.5 AND FAIL3 RR CI upper < 2.0 in E, AND P O_fail
RR CI upper < 1.5. Otherwise Gi keeps the starter-size cap (v1.3). (Expected: fails — S2 alone was 2.12 / 3.54.)

**Unchanged in all cases:** PEAD avoid window + any red flag → 0 new money (v1.2); manual core-asset threat (v1.4);
interest cover not applied to lenders.

Sensitivities (reported, do not decide): all events incl. financials; live firms only; unknown flag treated as 0;
quarter bootstrap for E; P with stratum-only (snapshot) bootstrap as before.

### Known biases (stated in advance)
(1) Not blind (above). (2) Pledge in E is stale (0–15 months) → dilutes Gp. (3) Gp is small (B25 ≈ 10% of E events,
14% of P weight; pledge-only smaller still) ⇒ wide CIs, especially in P and in 2022–25 3-year windows (entries ≤ Nov-2023).
(4) Sector tilt: pledge skews to promoter-group infra / real estate / textiles; not sector-matched. (5) P is one regime
(2016/18 into the 2018–20 credit squeeze, which hit pledged promoters specifically — may overstate pledge harm).
(6) Weekly closes, price returns only; 5-year P winners vs 3-year E winners are different horizons.

---
## Stage log
- 2026-11-25: pre-registration written before any group outcome was computed. Next: `tools/backtests/survival_cap_split/`
  (ss1_analyze.py: group tables for E and P, verdict) run once; outputs to `survival_cap_split_outputs/`.
- 2026-11-25: `ss1_analyze.py` ran once (method unchanged). The first run wrote results.json but crashed on printing
  (numpy bool not JSON-serialisable); the serialiser was fixed and the script re-run with identical numbers. No other edit.

---

# RESULTS (written 2026-11-25 after the single run; everything above is the unchanged pre-registration and log)

## Coverage
E (non-financial, both flags known): G0 6,822 · pledge-only (Gp) 444 · ICR-only (Gi) 1,036 · both (Gb) 413 · unknown 663.
3-year outcomes (WIN3, FAIL3, XS156) use ~65–85% of these (uncensored windows). P: G0 250 · Gp 41 (28 firms) ·
Gi 67 · Gb 57 · unknown 74.

## Verdict (pre-registered rules)
| candidate (vs G0) | T1 E: WIN3 ≤1.0, CI hi <1.2; H12 ≥2.0, CI lo >1.3 | T2 P: winners ≤1.0, CI hi <1.2; H12 ≥2.0, CI lo >1.0 | T3 both E halves | T4 XS156 ≤0 in E and P | result |
|---|---|---|---|---|---|
| **Gp pledge-only** | no — WIN3 **1.27 [0.77, 1.88]**; H12 2.68 [1.82, 3.75] | no — winners 0.67 [0.15, 1.41]; H12 1.67 [0.76, 3.08] | no — 2022–25 H12 1.10 | yes (−2.7 pp E; −35 pp P) | fail |
| **B50 pledge > 50%** | no — WIN3 **1.57 [1.00, 2.22]**; H12 4.01 [3.01, 5.18] | points yes, CIs no — winners 0.68 [0.19, 1.31]; H12 2.66 [1.68, 4.14] | no — WIN3 1.65 / 1.05 | no (+7.6 pp E) | fail |
| **Gb both** | no — WIN3 1.51 [0.93, 2.21]; H12 4.21 [3.09, 5.43] | no — winners 0.46 [0.00, 1.04]; H12 1.98 [1.14, 3.27] | no — WIN3 1.58 / 1.20 | no (+22 pp E) | fail |
| **Rule L: loosen Gi** (needs H12 CI hi <1.5, FAIL3 CI hi <2.0, P O_fail CI hi <1.5) | H12 1.69 [1.24, **2.21**]; FAIL3 2.92 [1.39, **5.35**] | O_fail 1.58 [0.78, **2.90**] | — | — | fail |

**Decision: NOT ADOPTED on both sides.** Card v1.3/v1.4 stays as is: pledge > 25% or interest cover < 1.5x
(non-financials) → starter size, no additions; PEAD window → 0 new money. No patch proposed. The prior written in the
pre-registration (E would fail the winner bar) was right.

## Sample E (events 2018–2025, non-financial; RR vs G0, firm-cluster 95% CI)
| group | H12 | FAIL3 | WIN3 | XS156 mean diff (median flagged / G0) |
|---|---|---|---|---|
| G0 base rates | 7.1% | 2.8% | 15.6% | −3.6% mean (−34% median) |
| Gp pledge-only | 2.68 [1.82, 3.75] (19.1%) | 6.02 [3.18, 10.8] | 1.27 [0.77, 1.88] | −2.7 pp [−43, +40] (−39%) |
| Gi ICR-only | 1.69 [1.24, 2.21] (12.1%) | 2.92 [1.39, 5.35] | 1.26 [0.89, 1.71] | +13.8 pp [−15, +46] (−38%) |
| Gb both | **4.21 [3.09, 5.43] (30.0%)** | **9.40 [5.54, 16.0]** | 1.51 [0.93, 2.21] | +22.1 pp [−33, +84] (−46%) |
| B50 (any ICR) | 4.01 [3.01, 5.18] (28.6%) | 9.21 [5.47, 15.7] | 1.57 [1.00, 2.22] | +7.6 pp [−41, +58] (−48%) |
| B50-only | 3.11 [2.02, 4.38] | 6.85 [3.56, 12.7] | 1.62 [0.84, 2.52] | +13.2 pp (−34%) |
| Gp vs Gi directly | 1.59 [1.04, 2.38] | — | **1.01 [0.58, 1.66]** | −16.4 pp [−65, +32] |

In E, pledge-only firms triple **as often as** ICR-only firms (19.8% vs 19.7%). The "pledge kills the upside" reading
from L39 does not hold in the event sample.

### Period replication (E)
| group | 2018–21: H12 / FAIL3 / WIN3 | 2022–25: H12 / FAIL3 / WIN3 |
|---|---|---|
| Gp | 2.27 / 6.70 / 1.29 | **1.10 [0.26, 2.32] / 0.55 / 0.96** |
| Gi | 1.21 [0.76, 1.72] / 1.96 / 1.41 | **3.25 [2.11, 4.80] / 5.65 / 1.09** |
| Gb | 3.53 / 10.6 / 1.58 | 3.75 [1.75, 6.41] / 3.96 / 1.20 |
| B50 | 3.33 / 10.2 / 1.65 | 2.42 [1.16, 4.18] / 2.90 / 1.05 |

The two single flags **swap roles between periods**: pledge-only carried the tail in 2018–21 (the promoter-pledge
squeeze of 2018–20) and showed none in 2022–25 (n = 177, wide CI); ICR-only showed little in 2018–21 and most of the
single-flag signal in 2022–25 (rising rates). Only "both" is consistently bad. Any fixed split by flag *type* would
have been fitted to one regime.

## Sample P (survivorship-free 2016/18 snapshots, weighted; firm-cluster-within-stratum bootstrap)
| group | H12 | O_fail (5-yr) | 5-yr 3× winners | XS156 diff |
|---|---|---|---|---|
| G0 base | 15.3% | 12.9% | 26.3% | +4.4% |
| Gp (41) | 1.67 [0.76, 3.08] | 1.91 [0.92, 3.55] | 0.67 [0.15, 1.41] | −35 pp [−71, +3] |
| Gi (67) | 1.21 [0.55, 2.16] | 1.58 [0.78, 2.90] | 1.41 [0.76, 2.22] | +21 pp [−35, +90] |
| Gb (57) | 1.98 [1.14, 3.27] | **4.41 [2.81, 7.44]** | 0.46 [0.00, 1.04] | **−45 pp [−85, −7]** |
| B50 (68) | 2.66 [1.68, 4.14] | 3.42 [2.09, 5.75] | 0.68 [0.19, 1.31] | **−42 pp [−81, −1]** |
| Gp vs Gi | 1.38 [0.53, 3.41] | — | 0.48 [0.11, 1.14] | −56 pp [−129, +6] |

P keeps the L39 picture (pledge → fewer winners and worse excess; ICR-only → more winners), but P is one regime —
2016/18 entries straight into the 2018–20 pledge squeeze — which is exactly the period in which E also shows pledge as
the bad flag. P and E-2018–21 agree; E-2022–25 does not.

### Sensitivities (do not decide; H12 / WIN3 RR)
Gp: incl. financials 2.68 / 1.24; live only 2.54 / 1.29; unknown as 0 2.50 / 1.28; quarter bootstrap WIN3 CI
[1.04, 1.49]. B50: live only WIN3 1.78 [1.07, 2.55]. Gi: quarter bootstrap H12 1.69 [1.31, 2.31]. None changes a verdict.

## What this means for the card
1. **No change.** The split by flag type fails on its own pre-registered terms: in the larger event sample pledge-only
   firms do not have fewer winners (WIN3 1.27×, same as ICR-only), and the tail signal of each single flag is
   regime-dependent. Weak interest cover alone keeps the starter cap (its tail is real, 1.7× halving / 2.9× failure,
   and was the main single-flag signal in 2022–25).
2. **Post-hoc observation (not adopted, needs its own test):** grading by *number* of flags looks more stable than
   grading by *type*. "Both" (pledge > 25% **and** ICR < 1.5x, ~4.7% of events) halves 30% of the time in 12 months
   (4.2×), fails within 3 years 26% (9.4×), in both E periods (H12 3.5× / 3.7×), and in P fails 57% (4.4×) with
   −45 pp 3-year excess. But in E it still triples 23.5% of the time (1.5×), so a 0-new-money rule would still cost
   winners there. A future pre-registered test on fresh events (2026+ results) could ask whether "both flags → 0 new
   money" holds out of sample. Until then: when both fire, the balance-sheet question should be answered *before*
   even the starter position (judgement, not a code rule).
3. Pledge > 50% is the strongest single tail marker (H12 4.0×, FAIL3 9.2× in E; failure 3.4× and −42 pp excess in P)
   but also carries more winners in E (1.57×) — high variance again, not a clean negative.

## Caveats
- Not blind (stated in advance): B25 overall was known in E and P. The new information is the mutually exclusive
  split and the period replication; the period replication is what overturned the L39 reading.
- Small cells: Gp has 41 snapshots (28 firms) in P and ~100 uncensored 3-year events in 2022–25; CIs are very wide.
- Stale pledge in E (0–15 months) dilutes Gp; sector tilt (promoter-group infra/real estate) not controlled.
- Means are driven by a few multi-baggers; medians for every flagged group are worse than G0 (−38% to −48% vs −34%).

Scripts: `tools/backtests/survival_cap_split/ss1_analyze.py` (reuses `survival_cap_general/sg2_analyze.py`).
Outputs: `research_notes/Backtests/survival_cap_split_outputs/results.json`.
