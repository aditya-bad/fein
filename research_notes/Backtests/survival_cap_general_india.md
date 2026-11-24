# Back-test: should the survival cap apply to every red-flag firm, not only after a bad result? (Roadmap stages 2 → 6)

*Method calibration, not stock picking. Research, not SEBI-registered advice.*
Started 2026-11-24. Builds **stage 2 (hard filters)** and feeds **stage 6** (the decision card's survival cap,
`tools/decision/decision_card.py` v1.2). The combined-avoid test (`combined_avoid_india.md`, L35,
decision:pead-avoid-plus-redflag-survival-cap) adopted a cap only when a bottom-two SUE result coincides with
pledge > 25% or interest cover < 1.5x. Its own post-hoc reading: group C (red flag, no miss) halves 15.1% of the
time, ≈ 2.5× clean firms, so the flag, not the miss, carries the tail risk. That broader rule was not
pre-registered. This file tests it.
**Unlocks:** if adopted, the card's cap becomes a standing stage-2 size rule (independent of the PEAD window), the
nightly solvency/pledge screen feeds it directly, and stage 4 deep dives start with the balance-sheet question for
every flagged firm. If not, the cap stays tied to the PEAD window and the flags stay "look harder".

## PRE-REGISTRATION (written 24-Nov-2026, before any new outcome below was computed)

### State of knowledge (honest)
Already known from published results: the event-level 12-month halving rates of groups A–D in the combined-avoid
test (A 17.6%, B 8.3%, C 15.1%, D 6.1%; quarter bootstrap). Those pooled numbers already imply that, on all
events, red-flag vs no-flag halving is about 2.3×. **So the event-sample halving ratio below is a re-estimate, not a
blind test.** What is new and not yet computed: (1) the ratio for the *card's* trigger (pledge > 25% ∨ interest
cover < 1.5x, without S5) with financials excluded; (2) **firm-cluster** bootstrap CIs (the earlier test flagged its
halving CIs as too narrow because the same firm repeats across quarters); (3) 1-year and 3-year excess returns vs
size-matched controls; (4) 3-year failure; (5) the winner cost; (6) an **independent replication** on the
survivorship-free 2016/2018 snapshot panel (solvency + hard-filter v2 panel), where no halving or excess-return
comparison by this flag combination has been run (only 5-year failure lifts by single flag, L27/L28).

### Samples (reused, not rebuilt; no new fetches)
- **Sample E (primary): event panel.** `combined_avoid_outputs/events_flags.tsv`: 10,242 firm-quarter results
  2018–2025, 557 firms (v1 live sample + sampled dead/off-series firms), mcap ₹500–50,000 cr, flags as of the event
  (pledge from the latest June-quarter SHP, 0–15 months stale; annual flags at FY0 ≤ event − 6 months). **All SUE
  quintiles pooled** — the question is "any red-flag firm regardless of earnings surprise". Entry = the event's
  entry weekly close (a "decision date" proxy: a card can be written any week; result weeks are a sample of them).
  **Financials (fin = 1) excluded from the primary** (interest cover is structurally < 1.5x for lenders; a general
  rule would cap every bank). All events as a sensitivity.
- **Sample P (replication): snapshot panel.** `hard_filters_india_v2_outputs/panel_v2.csv` (= the solvency panel +
  pledge): 489 company-snapshots, T = 30-Sep-2016 and 30-Sep-2018, mcap ₹200–20,000 cr, financials excluded,
  survivorship-free by design: stratum D (dead/distress census, weight 1), X (other delisted, weight 4.264),
  L (live sample, weight 5.633). All rates are weighted.

### Survivorship handling
- E: dead firms are a 39% sample with returns run to their last traded close (survivorship check convention).
  A firm whose price series stops inside a window is scored on what traded; a window cut short only because the
  *data* end (series last close within 14 days of the cache's latest date) is censored and dropped from that
  outcome (counted). 3-year outcomes therefore use entries up to ~Nov-2023 only.
- P: census of dead/distress firms with sampling weights; outcomes from screener weekly prices + IBBI/NSE/BSE lists,
  exactly as in the solvency test (`panel.csv`). Prices for 1-year halving and 1y/3y returns from the same cached
  screener charts (`bt_solv_in/sc/<slug>/chart.json`).

### Flags
- **CARD (primary trigger)** = B25 (promoter pledge > 25% of promoter holding) ∨ S2 (EBIT/interest < 1.5x). Fired if
  either known component fires; 0 only if both are known and neither fires; else unknown (excluded, counted). This
  is the card's current trigger, so the test asks: should *this* trigger stand on its own?
- Secondary (reported, decide only the S1/S5 question): B25, B50 (> 50%), S2 alone; S1 (negative net worth, not
  payout-driven); S5-India (≥ 2 of S1, S2, S4); RED = CARD ∨ S5; **S1∨S5 incremental** = S1 or S5 fires among
  CARD = 0.
- In P the same definitions use the panel's columns (B25/B50 at T from the June SHP filed before T; s1, s2, s5 at
  FY0 in (T − 18m, T − 6m]).

### Outcomes
- **H12 (primary):** lowest weekly close in (entry, entry + 52 weeks] ≤ 0.5 × entry close. E: `halve12` as already
  computed. P: computed from the chart series with px_T (last close ≤ T) as the entry.
- **FAIL3:** E: lowest weekly close ≤ 0.2× entry within 156 weeks, or the firm's series stops within 156 weeks and
  the firm is on a distress list (`distress` = 1). P: `o_fail` (5-year: liquidation, compulsory delisting, or ≤ 0.2×),
  as published.
- **XS52, XS156:** price return to the last weekly close ≤ entry + h weeks + 3 days minus the mean return of
  size-matched controls (E: all event-universe firms with a close on the entry Friday, mcap ×0.5–×2, ≥ 5 firms,
  same exit rule — the survivorship check's control rule, extended to 52 / 156 weeks; P: other panel snapshots of the
  same T, mcap ×0.5–×2, ≥ 5, weighted mean).
- **WIN3 (winner):** E: price ratio at 156 weeks ≥ 3. P: `winner` (5-year R5 ≥ 3, published).
- **Winner cost** = share of WIN3 cases that were CARD-flagged at entry (event-level in E; also at firm level: share
  of firms with ≥ 1 WIN3 event whose WIN3 events were *all* flagged, i.e. firms the cap would have kept us out of
  entirely). P: weighted share of winners flagged. Reported next to the share of halvings/failures flagged.

### Inference
- E: risk ratio RR = P(H12 | CARD = 1) ÷ P(H12 | CARD = 0), pooled events. **95% CI by firm-cluster bootstrap**
  (resample firms with replacement, all their events, 5,000 draws, seed 1). Quarter-bootstrap CI shown as well.
  Size check: Mantel–Haenszel RR stratified by fiscal quarter × within-quarter mcap tercile (point estimate only).
- P: weighted RR, bootstrap resampling snapshots within stratum (5,000 draws, seed 1).
- Excess returns: mean (and median) XS by flag; difference flagged − unflagged with firm-cluster CI.

### Decision rule (fixed now)
- **P1 (primary, E, non-financial):** RR(H12, CARD) ≥ **2.0** and firm-cluster CI lower bound > **1.3**.
- **P2 (replication, P):** weighted RR for H12 **or** for O_fail ≥ 1.5 with CI lower bound > 1.0.
- **P1 and P2 → ADOPT** the general cap: any India firm with CARD fired → **minimum (starter) size, no adds**, and
  the balance-sheet question is mandatory, whatever the SUE. The existing stronger rule stays on top: CARD + PEAD
  avoid window → 0 new money. (Minimum size rather than 0 for the general case is fixed now, because a quarter of
  firm-quarters carry the flag and the winner cost is expected to be non-trivial.)
- **P1 only → PROVISIONAL**: same rule but marked provisional, re-test when more data come in.
- **P1 fails → NOT ADOPTED**: keep the cap tied to the PEAD window.
- **Return-cost override:** if flagged firms' 3-year mean excess is *positive* with firm-cluster CI lower bound > 0,
  the cap has a measurable return cost: downgrade an ADOPT to PROVISIONAL and say so.
- **S1/S5 question:** S1 or S5 joins the trigger only if, among CARD = 0 events, its RR(H12) vs CARD = 0 & not-S1/S5
  is ≥ 2.0 with firm-cluster CI lower bound > 1.3 (E). Otherwise they stay "look harder" (L27).
- Winner cost is **reported, not a pass/fail criterion** (asked for). Interpretation fixed now: a cap that blocks a
  share of winners close to the share of all firm-quarters it flags has no selectivity on the upside; the case for it
  rests only on the halving/failure lift.
- Sensitivities (do not decide): all events incl. financials; RED instead of CARD; unknown treated as unflagged;
  live firms only; 2018–21 vs 2022–25; quarter bootstrap.

### Known biases (stated in advance)
(1) E overlaps heavily with what is already known (see top); P is the only blind part, and it is small
(489 snapshots, ~25–30% flagged ⇒ wide CIs). (2) Stale pledge (E) dilutes flags. (3) Restated standalone screener
annuals; holdco debt under-flagged. (4) E drops firms < ₹500 cr, where most failures are. (5) Weekly closes, price
returns only (no dividends). (6) Size-matched controls are not sector-matched; flagged firms skew to
infrastructure, metals, real estate — a sector tilt can show up as "excess". (7) Two snapshot dates (2016, 2018)
both run into the 2018–20 credit squeeze and COVID; P is one regime.

---
## Stage log
- 2026-11-24: pre-registration written before any new outcome was computed. Next: `tools/backtests/survival_cap_general/`
  (sg1_outcomes.py: XS52/XS156/WIN3/FAIL3 for E and H12/XS for P from caches; sg2_analyze.py: tables), run once.
- 2026-11-24: `sg1_outcomes.py` and `sg2_analyze.py` ran once, unchanged in method. (The pre-registration above was
  committed as fb02390 before results were written.) Two code-tidy edits to sg2 before its single run: a simplified
  tercile assignment for the MH ratio and removal of a dead line; no output had been produced.

---

# RESULTS (written 2026-11-24 after the single run; everything above is the unchanged pre-registration and log)

## Coverage
Sample E: 10,242 events; primary (non-financial) 9,378, of which CARD known for 8,797 (581 unknown, excluded):
**1,975 flagged (22.5%)**, 6,822 not; 481 firms. 3-year outcomes need an uncensored 156-week window: 3,222 events
censored by the data end (entries after ~Nov-2023), so XS156/WIN3/FAIL3 use ~6,000 events. Sample P: 489 snapshots,
all with prices; CARD known for 441 (191 flagged, 48 unknown — mostly pledge without XBRL).

## Verdict (pre-registered rule)
| criterion | result | pass? |
|---|---|---|
| **P1** E, non-financial: RR(12-month halving), CARD vs not, ≥ 2.0 with firm-cluster CI lower bound > 1.3 | **2.49× [1.96, 3.13]** (17.8% vs 7.1%; 351 / 1,975 vs 487 / 6,822); quarter bootstrap [2.04, 3.16]; size-and-quarter Mantel–Haenszel 2.10× | **yes** |
| **P2** P (survivorship-free 2016/18 panel): H12 **or** O_fail RR ≥ 1.5 with CI lower bound > 1.0 | H12 1.43× [0.90, 2.30] (no); **O_fail (5-yr) 2.36× [1.58, 3.66]** (30.3% vs 12.9% weighted) (yes) | **yes** |
| Return-cost override: flagged 3-yr mean excess > 0 with CI lower bound > 0 | +14.8% [−14.2, +48.7] — CI includes 0 | not triggered |
| S1/S5 join the trigger (incremental, among CARD = 0) | only 8 such events — **not testable**; S1 and S5 alone show no halving signal (0.97–1.18×) | no |

**Decision: ADOPT** the general cap in the pre-registered form: any Indian firm with promoter pledge > 25% or
(non-financial) interest cover < 1.5x → **starter size at most, no additions**, balance-sheet question mandatory,
whatever the earnings surprise. Inside the PEAD avoid window the stronger v1.2 rule (0 new money) stays on top.

## Sample E (events 2018–2025, non-financial, CARD = pledge > 25% ∨ interest cover < 1.5x)
| outcome | flagged | not flagged | flagged vs not (firm-cluster 95% CI) |
|---|---|---|---|
| Halved within 12 months (H12) | 17.8% | 7.1% | **RR 2.49 [1.96, 3.13]** |
| Failed within 3 years (≤ 0.2×, or distress-listed firm stopped trading) | 14.4% (215 / 1,494) | 2.7% (125 / 4,552) | **RR 5.24 [3.26, 8.60]** |
| Rose ≥ 3× within 3 years (WIN3) | 21.3% (313 / 1,472) | 15.6% (706 / 4,532) | RR 1.37 [1.05, 1.75] |
| 1-year excess vs size-matched controls (mean) | +1.2% | −0.1% | +1.4 pp [−4.5, +7.3] |
| 3-year excess vs size-matched controls (mean) | +14.8% | −3.6% | +18.4 pp [−11.3, +52.9] |
| 3-year excess (median) | −41% | −34% | (skew: means are carried by a few huge winners) |

**Flagged firms are a high-variance group, not simply a bad one.** They halve 2.5× and fail 5× as often, but also
triple 1.4× as often, and the mean 3-year excess is positive (noise-level CI). The median flagged firm does worse.

### Winner-blocking cost (asked for)
- The cap flags **22.5%** of firm-quarters. It would have capped **30.7% of the 1,019 events that went on to triple
  within 3 years**, 41.9% of 12-month halvings and **63.2% of the 340 three-year failures**.
- Firm level: of 190 firms that tripled from at least one event, **39 (21%) were flagged at every such entry**
  (the cap would have held us to a starter position throughout) and 67 (35%) at least once.
- So in E the cap is *anti-selective* on the upside (blocks a larger share of winners than of all events) while
  catching most failures. In P it is neutral: 29.2% of (weighted) snapshots flagged, 27.3% of 5-year 3× winners,
  49.3% of failures, 37.1% of 12-month halvings.
- This is why the pre-registered form is a **size cap, not a veto**: a starter position keeps the winner exposure
  while bounding the loss from the 1-in-6 that halve and the 1-in-7 that fail.

### Components (E, non-financial; RR of H12 with firm-cluster CI; winner share vs event share flagged)
| flag | H12 RR | FAIL3 RR | share of WIN3 flagged / share of events flagged |
|---|---|---|---|
| B25 pledge > 25% | 3.10 [2.36, 3.97] | 5.88 [3.66, 9.49] | 15.4% / 9.8% |
| B50 pledge > 50% | 3.46 [2.64, 4.42] | 6.26 [3.96, 9.93] | 11.0% / 6.0% |
| S2 interest cover < 1.5x | 2.12 [1.68, 2.64] | 3.54 [2.33, 5.12] | 22.1% / 16.4% |
| S1 negative net worth | 1.18 [0.28, 2.17] | 2.13 [0.48, 4.92] | 3.8% / 1.5% |
| S5-India | 0.97 [0.46, 1.54] | 1.54 [0.61, 2.82] | 5.2% / 3.0% |

### Sensitivities (H12 RR, firm-cluster CI) — every one passes the P1 bar
All events incl. financials 2.30 [1.84, 2.85]; RED incl. S5 2.49 (identical: S5 never fires without CARD here);
unknown as unflagged 2.33 [1.84, 2.88]; live firms only 2.28 [1.76, 2.90]; 2018–21 2.10 [1.61, 2.69];
2022–25 2.98 [2.05, 4.26]. The extra winners among flagged firms come from 2018–21 (WIN3 RR 1.46 [1.10, 1.90];
likely the post-COVID rebound of levered firms); in 2022–25 WIN3 RR is 1.07 [0.61, 1.70].

## Sample P (survivorship-free 2016/2018 snapshots, ₹200–20,000 cr, financials excluded, weighted)
| outcome | flagged (191) | not (250) | RR or diff [stratified bootstrap CI] |
|---|---|---|---|
| Halved within 12 months | 21.9% | 15.3% | 1.43 [0.90, 2.30] |
| Failed within 5 years (O_fail) | 30.3% | 12.9% | **2.36 [1.58, 3.66]** |
| Liquidation / compulsory exit (O_strict) | 4.6% | 0.8% | 6.2 [3.0, 16.0] |
| 5-year 3× winner | 23.9% | 26.3% | 0.91 [0.57, 1.35] |
| 1-year excess | +3.8% | +0.9% | +2.9 pp [−11.5, +19.1] |
| 3-year excess | −9.7% | +4.4% | −14.1 pp [−43.1, +18.8] |

By component in P: **pledge is the clean negative** — B25: H12 1.76 [1.01, 2.82], O_fail 2.63 [1.73, 3.98], winners
0.55× [0.19, 0.99], 3-year excess −41.9 pp [−69.9, −15.1], only 8.5% of winners flagged vs 14.4% of firms;
B50 3-year excess −41.7 pp [−80.5, −3.1]. **Interest cover is a variance flag** — S2: O_fail 2.01 [1.38, 2.97] but
H12 1.38 [0.83, 2.19], winners 1.08×, 3-year excess −3.1 pp (noise).

## What this means for the card (and what it does not)
1. Adopted: a standing stage-2 size cap. Pledge > 25% or interest cover < 1.5x (non-financials) → starter size
   (proposed 1% of the portfolio at cost), no additions, balance-sheet question. Inside the PEAD avoid window → 0 new
   money (v1.2, unchanged). Interest cover is not applied to lenders (structurally < 1.5x).
2. Not adopted: S1 / S5-India as triggers (no incremental events; no signal alone). They stay "look harder".
3. **Post-hoc, not adopted (future test):** the two triggers behave differently. Pledge is bad on both tails (more
   failures, fewer winners, negative excess in P); interest cover mostly widens the spread (more failures *and* more
   winners in E). A tighter cap for pledge > 50% and a looser one for interest cover alone may fit better — that
   would need its own pre-registration.
4. Proposed code change (not applied): `survival_cap_general_outputs/proposed_card_v1.3.diff` (card + tests;
   `git apply --check` passes; all 25 tests pass on a scratch copy).

## Caveats
- **E is not blind**: its halving ratio was largely implied by the published A–D groups (stated in the
  pre-registration). The blind replication is P, which passes only on 5-year failure, not on 12-month halving.
- Flags are not sector-matched; flagged firms skew to infrastructure, metals, real estate, power. Part of the
  "variance" is sector beta (2018–21 crash and 2021 rebound).
- 3-year outcomes in E use entries up to ~Nov-2023 only; P covers one regime (2016/18 into the 2018–20 credit squeeze
  and COVID). Weekly closes, price returns only. Restated standalone screener annuals; stale pledge (E, 0–15 months).
- Mean excess returns are dominated by a few multi-baggers; medians tell the opposite story. Neither difference is
  statistically distinguishable from zero.
- Firm-cluster bootstrap handles repeat firms; the stratified bootstrap in P treats 2016 and 2018 snapshots of the
  same firm as independent (slightly narrow CIs).

Scripts: `tools/backtests/survival_cap_general/` (sg1_outcomes.py, sg2_analyze.py). Outputs:
`research_notes/Backtests/survival_cap_general_outputs/` (events_out.tsv, panel_out.tsv, results.json,
sg1_coverage.json, proposed_card_v1.3.diff).
