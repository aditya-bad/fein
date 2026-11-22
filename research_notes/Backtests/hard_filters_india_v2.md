# Back-test: the v2 mechanical hard-filter rules on a survivorship-free Indian panel (Roadmap stage 2)

*Method calibration, not stock picking. Research, not SEBI-registered advice.*
Started 2026-11-22. Stage 2 (hard filters) of `memory/roadmap.md`. It redoes **Part B** of
`hard_filters_test.md`, which used one survivors-only snapshot (30-Sep-2020, 495 firms drawn from the current NSE
list: 0 of 495 died, base rate of a >50% loss 1.8%). Lesson L27: screener still serves ~87% of dead Indian
companies, so the same rules can now be tested with dead companies included.
Unlocks: a calibrated stage-2 gate for India (which v2 rules are graded red / hard / questions) and a new record
`insight:disqualifiers-v3-proposal`. Next: stage 3 signals running behind that gate.

## PRE-REGISTRATION (written 22-Nov-2026, before any v2 rule was computed or compared with an outcome)

What is already known before this test: the panel and its outcomes were built for the solvency test
(`solvency_flags_india.md`, 489 company-snapshots, weighted 5-year failure rate 19.7%, 168 failures, 92 ≥3x
winners) and the solvency-flag results are public. No v2 rule below has been computed on this panel. Pledge
data at T has not been fetched yet.

### Panel (identical to the solvency test — reused, not rebuilt)
- Snapshots T = 30-Sep-2016 (FY2016) and 30-Sep-2018 (FY2018); FY0 = latest standalone annual column ending in
  (T−18m, T−6m]; columns after FY0 are not used.
- Same frame and weights: stratum D (dead/distress lists: IBBI CIRP/liquidation, NSE compulsory/liquidation
  delisting, NSE/BSE suspension; census, weight 1), X (other BSE/NSE delisted; 500 of 2,132, weight 4.264),
  L (live; 900 of 5,070, weight 5.633). Mcap ₹200–20,000 cr at T. Financials excluded, including the dead-bank fix
  (unlabeled pages with a Deposits row or "Bank" in the name). Companies already in insolvency at T excluded.
- Source: `research_notes/Backtests/solvency_india_outputs/panel.csv` (keys, weights, FY0, outcomes) and the
  cached standalone screener pages under scratchpad `bt_solv_in/sc/<slug>/page.html`. No screener refetch.

### Rules (mechanical v2 set; all from data public at T)
Annual values from the screener standalone page, fiscal years ≤ FY0 only (year = calendar year of FY0's column
month; columns in a different month — half-year/transition columns — are dropped).
- **(a) A — CFO/PAT 5y < 0.3** (v2 status: question). Σ CFO / Σ PAT over the up-to-5 fiscal years ending FY0, using
  years where both are present; ≥ 3 such years required. Σ PAT ≤ 0 ⇒ unknown (ratio undefined; counted).
  Secondary **A7** < 0.7.
- **(b) B25 — promoter pledge > 25% of promoter holding at T** (v2: graded); **B50 > 50%** (escalation level).
  Source: the latest BSE shareholding-pattern XBRL *filed before T* (normally the June quarter of the snapshot
  year), and only if that quarter ends within 12 months before T. Pledge % = pledged/encumbered promoter shares ÷
  promoter shares (re-derived). A filing that declares "no promoter shares pledged" = 0%. No promoter shares ⇒ 0%
  (not fired). Unknown if no BSE code, no SHP filed in that window, no XBRL, or parse failure (all counted).
  Exploratory: **B_rise** = pledge % at T ≥ pledge % a year earlier + 10 pp (needs the SHP filed ~12 months
  earlier; FY2016's prior-year SHPs mostly have no XBRL, so this is FY2018-only in practice).
- **(c) C — debt growth with negative CFO** (v2: question). Borrowings FY0 ≥ 1.5 × borrowings FY0−3 (from zero:
  fired only if FY0 borrowings > 5% of FY0 sales) **and** Σ CFO FY0−2..FY0 < 0 (all three years present).
- **(d) D50 — other income > 50% of PBT** (v2: question). Σ other income / Σ PBT over FY0−2..FY0 (≥ 2 years),
  Σ PBT > 0; Σ PBT ≤ 0 ⇒ unknown (counted). Secondary **D30** > 30% (the old Part B R5 threshold).
- **(e) E — receivable days up > 50% in 3 years** (v2: graded with counterparty). Debtor days FY0 ÷ debtor days
  FY0−3 > 1.5, with FY0−3 debtor days > 0. Exploratory **E60**: also FY0 debtor days ≥ 60 (removes tiny bases).
- **(f) "Implausible economics" is NOT tested** — lesson L20: a mechanical proxy (ROCE > 40% or OPM +10 pp)
  did not reproduce the judgment rule. It stays judgment-only.
- **ANY** = A ∨ B25 ∨ C ∨ D50 ∨ E; fired if any component fires, not fired only if every component is known and
  none fires, else unknown. Secondary **ANY_np** (without pledge, so coverage does not depend on BSE data) and
  **TWO+** (≥ 2 of the five fire; exploratory).

### Outcomes (unchanged from the solvency test; read from panel.csv)
- **O_fail** (primary) = IBBI liquidation ∨ compulsory delisting / exit for cause ∨ lowest weekly close ≤ 0.2× the
  close at T, all within (T, T+5y]. **O_strict** = liquidation ∨ compulsory exit (robustness).
- **Winner** = 5-year price ratio R5 ≥ 3 (a failed firm with no R5 is not a winner; R5 missing otherwise ⇒ excluded
  from the winner denominator).
- For comparison with the old Part B only: **loss50** = R5 < 0.5, or failed with no R5.

### Metrics and decision rule (identical to the solvency tests)
- Weighted by stratum; per rule: n known, n fired, precision P(O_fail | fired), base rate (known set), recall,
  lift = precision / base rate, share of ≥3x winners flagged. 95% percentile CIs from 2,000 bootstrap draws,
  resampling companies within stratum (seed 7), using `tools/backtests/solvency_india/s4_analyze.stats`.
- **Graded red** if pooled lift ≥ 2.0 **and** lift CI lower bound > 1 **and** the rule flags < 10% of eventual ≥3x
  winners. **Hard** if additionally lift ≥ 4.0. Otherwise a **question** for the deep dive. Decided on pooled
  O_fail for the primary rules A, B25, B50, C, D50, E and ANY. Secondary/exploratory rules (A7, D30, E60, B_rise,
  ANY_np, TWO+), O_strict, per-snapshot, live-stratum-only and mcap ≥ ₹400 cr results are robustness and do not
  overturn a verdict.
- Comparison with the old Part B: flagged vs unflagged rates of loss50 and x3 (weighted), plus the same table
  restricted to stratum L (the survivor-like slice of this panel) to show how much the survivors-only design hid.

### Known biases stated in advance
(1) Everything from the solvency test: standalone accounts, restated screener numbers, mcap-to-sales rounding,
weekly closes, BSE suspension dates proxied by the end of the price series, ~15–17% of IBBI firms unretrievable,
windows contain the 2018–19 small-cap/IL&FS crash and COVID. (2) Pledge needs a BSE code and an XBRL SHP: firms
that never filed one (common among the worst distressed names) are unknown, which may hide pledge's best cases.
(3) Screener "Debtor Days" and "Other Income" are screener's derived/classified figures. (4) The rules are
applied
mechanically, without the counterparty or context judgment v2 asks for — a mechanical rule failing does not mean
the judgment version fails. (5) ~300 companies and ~170 failures: power for rare rules (B50, C) is low.

---
## Stage log
- 2026-11-22: pre-registration saved before the pledge fetch and before any v2 rule was computed.
- 2026-11-22, **deviation logged before any rule was compared with an outcome** (only coverage and fired counts
  had been looked at): screener's standalone pages for live companies start at FY2015 (12-column window), so at
  the FY2016 snapshot rules that need 3–5 years of history (A, A7, C, E, E60) are computable for 1 of 145 live
  rows but for 17–29 of 106 stratum-D rows (dead firms' pages end earlier and reach further back). Coverage would
  then depend on the company's fate, which biases any pooled estimate. **Change:** A, A7, C, E, E60 and the
  composites that contain them (ANY, ANY_np, TWO+) are decided on the **FY2018 snapshot only** (coverage there:
  D 37–68 of 71, L 152–157 of 162; A's remaining unknowns are mostly Σ PAT ≤ 0, which is part of the rule's
  definition). Their FY2016 numbers are reported as uninterpretable. B25, B50, D50, D30 keep the pooled primary
  as registered (D50 is known for 128 of 145 live and 55 of 106 dead FY2016 rows — the gap is Σ PBT ≤ 0, again part
  of the definition). The decision rule itself is unchanged.
- 2026-11-22: pledge fetch running from BSE (`h1_pledge_fetch.py`, one stream, ≥ 1.6 s).
- 2026-11-22: pledge fetch done — 938 BSE requests (301 SHP lists + XBRL files), one stream, ~1.6–1.8 s apart,
  0 errors, 1 failed file. Rules computed (`h2_panel.py`), statistics run (`h3_analyze.py`). One post-hoc check
  (`h4_posthoc.py`, labelled exploratory) added after reading the primary table.

---

# RESULTS (written 2026-11-22 after the run)

## Coverage
489 company-snapshots (FY2016 255, FY2018 234; 301 companies), weighted 5-year O_fail base rate 19.7% (FY2016
27.6%, FY2018 12.2%). Pledge known for **419** rows (163 with a pledge tag, 256 declaring none; unknown: 40 SHPs
without XBRL, 27 with no SHP filed in the 12 months before T, 3 without a BSE code) — 79% of stratum D and 74–97%
of stratum L, so pledge coverage does not depend much on fate. FY2018-scope rules: A 190 known (most unknowns are
Σ PAT ≤ 0), C 226, E 222, D50 380 pooled (Σ PBT ≤ 0 ⇒ unknown).

## Primary results — O_fail within 5 years (weighted; stratified company bootstrap, 2,000 draws)

| rule | scope | fired / known | fired & failed | wtd share flagged | precision | lift [95% CI] | recall | ≥3x winners flagged | verdict |
|---|---|---|---|---|---|---|---|---|---|
| (a) CFO/PAT 5y < 0.3 | FY2018 | 22 / 190 | 7 | 10.7% | 22% | 2.08 [0.57, 3.85] | 22% | 11.3% (7/59) | **question** (CI includes 1; > 10% of winners) |
| (a′) CFO/PAT < 0.7, secondary | FY2018 | 40 / 190 | 10 | 19.8% | 14% | 1.29 [0.48, 2.28] | 26% | 20.4% | (question) |
| **(b) pledge > 25% of promoter holding** | pooled | 98 / 419 | 59 | 14.4% | 39% | **2.13 [1.53, 2.94]** | 31% | **8.5% (8/81)** | **GRADED RED** |
| **(b′) pledge > 50%** | pooled | 68 / 419 | 42 | 8.3% | 44% | **2.43 [1.65, 3.47]** | 20% | **5.9% (6/81)** | **GRADED RED** |
| (b″) pledge up ≥ 10 pp in a year, exploratory | pooled (≈FY2018) | 13 / 219 | 7 | 3.9% | 32% | 2.93 [0.78, 6.93] | 12% | 1.7% | (question) |
| (c) debt ≥ 1.5x in 3y with 3y CFO < 0 | FY2018 | 17 / 226 | 6 | 6.1% | 10% | 0.83 [0.26, 2.06] | 5% | 8.9% (6/64) | **question / no signal** |
| (d) other income > 50% of PBT | pooled | 77 / 380 | 29 | 17.9% | 24% | 1.36 [0.85, 1.92] | 25% | 13.8% (11/78) | **question** |
| (d′) > 30%, secondary | pooled | 128 / 380 | 42 | 32.1% | 20% | 1.15 [0.79, 1.54] | 37% | 28.7% | (question) |
| (e) debtor days ×1.5 in 3y | FY2018 | 51 / 222 | 19 | 21.2% | 19% | 1.51 [0.83, 2.37] | 32% | 19.2% (12/64) | **question** |
| (e′) same and ≥ 60 days, exploratory | FY2018 | 37 / 222 | 17 | 13.8% | 24% | 1.91 [1.01, 3.15] | 26% | 14.0% | (question) |
| **ANY of a–e** | FY2018 | 112 / 207 | 42 | 45.8% | 17% | 1.31 [0.96, 1.74] | 60% | **46.7% (29/60)** | **question** |
| ANY without pledge, secondary | FY2018 | 88 / 198 | 30 | 39.3% | 17% | 1.32 [0.89, 1.84] | 52% | 42.5% | (question) |
| ≥ 2 of a–e, exploratory | FY2018 | 44 / 191 | 18 | 17.5% | 21% | 1.92 [1.02, 3.09] | 34% | 19.5% | (question) |

(f) "implausible economics" was not tested (judgment-only, L20).

## Robustness (does not overturn the verdicts)
- **O_strict** (liquidation or compulsory exit only): pledge > 25% 3.48 [1.99, 5.62]; **pledge > 50% 5.19 [2.78,
  8.70]** — at the "hard" level on this narrower outcome, but O_strict is robustness by the fixed rule. CFO/PAT < 0.3
  0 of 22 strict failures; other income 0.35; debtor days 1.09; ANY 1.64 [1.02, 2.31].
- **Per snapshot (O_fail):** pledge > 25% FY2016 2.03 [1.41, 2.87] / FY2018 1.95 [1.12, 3.27] (10.4% of winners —
  on FY2018 alone it would be a question); **pledge > 50% 2.47 / 2.44** (CI lower bounds 1.60 / 1.31, winners 1.2% /
  7.1%) — the most stable result. FY2016 numbers for A, C, E, ANY are uninterpretable (coverage is mostly dead firms).
- **Mcap ≥ ₹400 cr:** pledge > 25% 2.45 [1.67, 3.77], > 50% 2.97 [1.92, 4.58]; others unchanged.
- **Live stratum only** (what a survivors-only universe sees): pledge > 25% 1.80 [0.79, 3.05], > 50% 2.06 [0.40,
  3.97] — the same direction, but the CIs include 1. Debt growth with negative CFO: 0 failures in 9.
- **Post-hoc (exploratory, after reading the primary table):** 58–60% of pledge-flagged rows also have interest
  cover < 1.5x. Among rows with adequate interest cover, pledge lift falls to 1.75 [0.91, 2.98] (> 25%) and 1.52
  [0.58, 3.02] (> 50%). Among non-loss-makers it stays 2.21 / 2.41, and outside S5-India 1.86 / 2.18. Pledge is
  partly a leverage signal, and partly an extra one.

## Comparison with the old survivors-only Part B (30-Sep-2020, 495 firms)

| rule | old Part B: flagged vs unflagged >50% loss (5y) | old: flagged vs unflagged ≥3x | new panel: loss50 flagged vs unflagged (wtd) | new: ≥3x flagged vs unflagged |
|---|---|---|---|---|
| CFO/PAT < 0.3 | 2.4% vs 0.9% | 60% vs 52% | 15.9% vs 6.0% (FY2018) | 36% vs 34% |
| pledge > 25% | 2.9% vs 1.6% | **69% vs 51%** | **30.7% vs 10.5%** | **15% vs 28%** |
| pledge > 50% | 4.5% vs 1.5% | 70% vs 52% | 33.9% vs 11.5% | 18% vs 26% |
| debt ≥ 1.5x + negative CFO | 0% vs 1.7% | 70% vs 54% | 10.2% vs 9.0% (FY2018) | 50% vs 34% |
| other income > 30% / > 50% | 2.7% vs 0.7% (> 30%) | 61% vs 48% | 15.5% vs 10.2% (> 30%); 16.9% vs 10.8% (> 50%) | 23% vs 26%; 20% vs 26% |
| ANY | 2.9% vs 1.4% | 64% vs 51% | 13.6% vs 6.1% (FY2018) | 36% vs 34% |

The old Part B said pledged firms tripled *more* often (69% vs 51%, p = 0.006). With dead firms in and the snapshot
not at a market low, pledged firms tripled about **half as often** (15% vs 28%) and lost half their value three
times as often. Even within the live slice of this panel, pledged firms tripled less (20% vs 29%). The old result
was not only survivorship: it came from a COVID-low snapshot plus a sample that admitted small firms only if they
later grew (both biases named there). For the cash-flow rules the direction holds: they fire on winners about as
often as on others (CFO/PAT x3 36% vs 34%; debt + negative CFO 50% vs 34%), which confirms L20.

## Names behind the numbers (`hard_filters_india_v2_outputs/tables.md`)
- Pledge > 50% caught: ABG Shipyard, Sical Logistics (both snapshots), Essar Shipping, KSK Energy, AJR Infra, Future
  Consumer, Gammon India, Ballarpur (both), Coffee Day, Gayatri Projects (both), B.L. Kashyap (both), IVRCL. Pledge
  > 25% also caught Sadbhav Engineering (both) and Reliance Communications FY2016.
- Winners it would have cost (pledge > 50%): Alok Industries FY2016 (7.1x, after the Reliance-JM resolution), Dr
  Agarwal's Eye Hospital, Granules, Jindal Stainless (8.9x), Steel Exchange, Birlasoft; > 25% adds Aurionpro (7.6x) and
  Zen Technologies (11x).
- Jet Airways FY2018 passed pledge (0% at June 2018; the pledges came later) and was flagged only by other income.

## Verdicts (pre-registered rule: lift ≥ 2, CI lower bound > 1, < 10% of ≥3x winners flagged → graded red; hard if ≥ 4)
- **(b) Pledge > 25% of promoter holding → GRADED RED** (2.13 [1.53, 2.94], 8.5% of winners). Borderline on the
  winner condition and only a question on FY2018 alone.
- **(b′) Pledge > 50% → GRADED RED, the strongest mechanical rule tested in India** (2.43 [1.65, 3.47], 5.9% of
  winners; stable across snapshots; 5.19 on liquidation/compulsory exit). **Not hard:** lift is below 4 on the primary
  outcome, and it would have cost Alok, Jindal Stainless and four other ≥ 3x winners.
- **(a) CFO/PAT < 0.3 → QUESTION.** Point lift 2.08 on FY2018 but the CI is [0.57, 3.85], it flags 11% of
  winners, and it caught none of the liquidations or compulsory exits.
- **(c) Debt growth with negative CFO → QUESTION, no signal** (0.83). Third test in which it fails (Part A, old
  Part B, now).
- **(d) Other income > 50% of PBT → QUESTION** (1.36, CI includes 1; 0.35 on strict failures). It stays the
  starting point of the H1a fake-cash test, not a flag.
- **(e) Debtor days ×1.5 in 3y → QUESTION** (1.51, CI includes 1, 19% of winners). The ≥ 60-day variant reaches
  1.91 [1.01, 3.15] (exploratory) — consistent with v2's "judge debtor days by counterparty", not a mechanical flag.
- **ANY → QUESTION.** It flags 46% of firms and 47% of later ≥ 3x winners for a lift of 1.31 — a mechanical
  "any red flag" gate would throw away half the multibaggers.
- **Nothing is HARD.**

## What it means
1. Survivorship mattered most for pledge: the survivors-only test said pledge flagged *more* multibaggers; with dead
   companies in, it is the one mechanical rule that clears the bar. This settles the conflict between Part A
   (8/20 traps vs 2/13 winners) and the old Part B in Part A's favour.
2. The cash-flow and balance-sheet "tells" (CFO/PAT, debt + negative CFO, other income, debtor days) stay questions.
   Two have point lifts near 1.5–2 but wide CIs and costs of 11–19% of winners. The v2 decision to make them deep-dive
   questions is confirmed, now on survivorship-free data.
3. Pledge is partly a leverage signal (60% overlap with weak interest cover), so pledge and the solvency flags should be
   read together, not added up as independent votes.

## Recommendation (new record insight:disqualifiers-v3-proposal; v2 and insight:disqualifiers unchanged)
Keep the v2 structure (judgment fraud signals hard at entry; auditor exit and accounting-trouble events hard at exit;
cash-flow tests as questions; P/E in stage 5). Changes from v2:
- **Pledge becomes the top graded red flag, with numbers:** > 50% of promoter holding = graded red at "strong"
  level (needs a written override: why the pledge exists, the lender, the margin-call price vs today's price); > 25% =
  graded red (normal override). Rising pledge (≥ 10 pp in a year) = escalation, untested beyond 13 cases. Still
  **not hard** (Alok, Jindal Stainless, Zen Technologies).
- **Pledge + interest cover < 1.5x together** = the main stage-2 "look much harder, size small" combination
  (post-hoc, so it needs a forward check).
- **Confirmed questions, not flags:** CFO/PAT, debt growth with negative CFO, other-income share, debtor-day jumps —
  ask what working capital is made of and who owes the money.
- **No mechanical "any flag" gate:** it would have cut 47% of later ≥ 3x winners.
- Proof still missing for the judgment rules (H1a–H5) — they cannot be tested mechanically; the forward scoreboard
  (stage 7) is where they get tested.

## Caveats
All of the solvency test's caveats apply (standalone accounts, restated screener data, mcap rounding, weekly closes,
BSE suspension dates from the end of the price series, 15–17% of IBBI firms unretrievable, crisis-heavy windows).
In addition: history-dependent rules are FY2018-only (logged deviation), so they rest on ~200 rows and 2018–23 only.
Pledge needs an XBRL SHP (from mid-2016). The rules are mechanical versions of judgment rules. The post-hoc
interest-cover split was not pre-registered. Research, not SEBI-registered advice.

Scripts: `tools/backtests/hard_filters_v2/` (common2, h1_pledge_fetch, h2_panel, h3_analyze, h4_posthoc). Outputs:
`research_notes/Backtests/hard_filters_india_v2_outputs/` (panel_v2.csv, coverage.json, results.json, tables.md,
posthoc.json). Raw BSE SHP cache: scratchpad `bt_hf2/shp/` (not durable).
