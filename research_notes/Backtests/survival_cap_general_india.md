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
