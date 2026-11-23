# Back-test: is the PEAD avoid flag much stronger when a stage-2 red flag is also present? (Roadmap stages 2 + 3)

*Method calibration, not stock picking. Research, not SEBI-registered advice.*
Started 2026-11-23. Builds **stage 2 (hard filters) and stage 3 (signals) together**, feeding **stage 6** (the decision
card's avoid gate, `tools/decision/decision_card.py`). Lesson L31: after a bottom-two-quintile result, firms that later
landed on a distress list lagged controls by −16.6% in 13 weeks (71 events, descriptive, picked by later fate). This
test asks the forward-looking version with flags known *at the event*: promoter pledge (graded red, L28,
`hard_filters_india_v2.md`) and interest cover / S5-India (`solvency_flags_india.md`).
**Unlocks:** if the combination is much worse than either flag alone, the decision card gets a stronger
"miss + red flag = exit / no entry" gate (and the live PEAD tracker can tag events with flags); if not, the two gates
stay independent and simple.

## PRE-REGISTRATION (written 23-Nov-2026 before any flag was joined to any outcome)
State of knowledge: the PEAD survivorship results (L31) and the pledge / solvency panel results (L27, L28, solvency
test) are known. **No pledge or annual-report flag has been computed for any PEAD event, and no flag has been joined to
any PEAD return or price path.** Only the event file's row count (10,242 events, 557 firms) and cache coverage counts
(151 of 557 firms already have a cached screener page; 78 a cash-flow schedule) have been looked at.

### Event set (reused, not rebuilt)
- The survivorship-check event set exactly: `bt_pead_surv/events_w.tsv` (ALL universe = v1 live sample + sampled
  dead/off-series firms; 10,242 events dated 2018-01-01 → 2025-12-31; standalone-EPS SUE; weekly closes; entry = first
  weekly close after the event). 13-week return `r13`, size-matched control mean `cA13` (ALL universe, mcap ×0.5–×2,
  ≥ 5 firms, delisted firms' returns run to their last traded close) are used exactly as computed there.
- SUE quintiles within each fiscal quarter (≥ 25 events) with `india_pead_survivorship/s5_analyze.groups`, unchanged.
  **Bottom two** = quintiles 1–2 (the decision card's avoid quintiles, L19).

### Flags as of the event (only data available before the event date)
- **Pledge.** Promoter pledged/encumbered shares ÷ promoter shares, from BSE shareholding-pattern XBRL, parsed with
  `hard_filters_v2/h2_panel.pledge_from` (unchanged). BSE code from the firm's screener page (else none ⇒ unknown).
  **Budget deviation, fixed now:** fetching the latest SHP before every one of ~10,000 events would take ~10,000 BSE
  requests (~5 h at one stream ≥ 1.6 s). Instead, for each firm we fetch its SHP list plus **one SHP per calendar
  year: the June-quarter SHP** (2017–2025). An event uses the **latest of these fetched June-quarter SHPs whose BSE
  filing date is before the event date**, and only if that quarter ended ≤ 15 months before the event. Staleness is
  therefore 0–15 months (mean ≈ 7). Stated bias: stale pledge readings misclassify some flagged firms as unflagged
  and vice versa — this dilutes group differences, i.e. it works *against* H1/H2. `B25` = pledge > 25%, `B50` = > 50%.
  A SHP declaring no promoter pledge = 0%; no promoter shares = 0%; no XBRL / parse failure = unknown.
- **Annual flags.** Screener **standalone** company page (cached from `bt_solv_in/sc/` or `bt_pead_surv/sc/`, else
  fetched) and its *Cash from Financing Activity* schedule (needed for S4's dividends). Annual columns are cut with
  `solvency_india/s3_panel.cut` at **FY0 = the latest fiscal-year column ending ≤ event date − 6 months** (annual
  reports are due within ~6 months; same convention as the solvency test's T − 6 months) and with a balance sheet at
  the same date; then `solvency_screen.inputs()` / `flags()` unchanged. **S2** = interest cover (EBIT / interest)
  < 1.5x; **S5-India** = ≥ 2 of S1 (negative net worth, not payout-driven), S2, S4 (dividends > FCF while borrowings
  rose). FY0 more than 24 months before the event ⇒ unknown (firm stopped filing). Stated biases: restated, not
  as-first-reported screener numbers; standalone accounts under-flag holdco debt. Financials are **not** excluded
  from the event set (they are in it); for them S2/S5 usually come out unknown or not meaningful — reported as a
  sensitivity (financials excluded).
- **RED** (any red flag) = B25 ∨ S2 ∨ S5-India. RED = 1 if any known component fires; RED = 0 only if pledge is known
  **and** S2 is known and none of the known components fires (S5 may be unknown — it needs S4); otherwise unknown and
  the event is excluded from groups A–D (counted). Sensitivity: unknown treated as RED = 0.

### Groups
(A) bottom-two SUE quintile **and** RED; (B) bottom-two **without** RED; (C) RED in quintiles 3–5; (D) neither.
n reported per group; **small-n warning** if a group has < 50 events.

### Outcomes
- **Primary:** 13-week excess return = `r13 − cA13` (size-matched controls), from the event file.
- **P(halving):** the lowest weekly close in (entry, entry + 52 weeks] ≤ 0.5 × the entry close (weekly series from the
  same price caches as the event file: v1 Yahoo daily → Friday weekly closes, with v1 split adjustment; screener
  weekly for MISSING firms). A firm whose series stops inside the window counts on what traded (halved or not); an
  event whose series ends because the data end (last close within 14 days of the latest date in the cache) before
  entry + 52 weeks − 7 days, without having halved, is dropped from this outcome (counted).

### Hypotheses and decision rules (fixed now)
Inference as the survivorship check: unit = fiscal quarter; 95% bootstrap CIs resampling quarters (5,000 draws,
seed 1); all events 2018–2025 primary, 2018–21 / 2022–25 shown.
- **H1 (primary).** Per quarter, mean excess of A minus mean excess of B (quarters where A and B each have ≥ 3 events);
  mean across quarters ≤ **−2.0 pp** and the bootstrap CI upper bound < 0 ⇒ **SUPPORTED**. CI excluding 0 but
  |effect| < 2 pp ⇒ "weaker than hypothesised (real but < 2 pp)". Otherwise **NOT SUPPORTED**.
- **H2 (primary).** Pooled event-level P(halving within 12 months) of A ÷ that of D; quarter-bootstrap CI (resample
  quarters, recompute both pooled rates). Ratio ≥ **2.0** and CI lower bound > 1 ⇒ **SUPPORTED**; CI lower bound > 1
  but ratio < 2 ⇒ "weaker than hypothesised"; otherwise **NOT SUPPORTED**.
- Reported alongside (do not decide H1/H2): A, B, C, D mean excess and P(halving) with CIs; A vs C (is it the miss or
  the flag?); the interaction (A − B) − (C − D); components B25 / B50 / S2 / S5 alone in place of RED; sub-periods;
  LIVE-only events; unknown-as-unflagged; financials excluded.
- **How the decision card uses it (rule fixed now):**
  - H1 supported → the avoid gate escalates: bottom-two SUE **with** a red flag = "EXIT / no entry for ≥ 63 trading
    days, re-check only after the next result"; bottom-two without a flag stays the current WAIT.
  - H1 not supported but H2 supported → the combination is a **tail-risk** rule: keep WAIT as is, but a bottom-two
    result with a red flag caps the position at the minimum size / blocks new money (survival, not drift).
  - Neither → no interaction rule; the PEAD gate and the stage-2 flags stay separate and additive (no new gate).
- Known biases stated in advance: (1) stale pledge (annual June-quarter SHP); (2) firms with no BSE code or no XBRL SHP
  are unknown (NSE-only firms; dead firms that stopped filing) — may hide the worst cases; (3) restated standalone
  annual data; (4) the event set already drops firms below ₹500 cr, where most failures sit (L31), so halving events
  are rarer than in the solvency panel; (5) weekly closes; price returns only; (6) dead firms are a 39% sample.

---
## Stage log
- 2026-11-23: pre-registration saved before any flag was computed or joined to an outcome. Fetch next: screener
  (pages + cash-flow schedules for firms not cached) and BSE (SHP lists + June-quarter XBRLs) — one stream per host,
  ≥ 1.5 s (screener) / ≥ 1.6 s (BSE); the two hosts run in parallel.
- 2026-11-23, **D1 (data access, logged before any flag was joined to an outcome; only coverage counts seen):** BSE
  lists the June-2025 SHPs with an HTML link (`…/SHPXBRLDataXML/…_SP.html`) instead of an XBRL link, though the
  listing still names the XBRL file (`XbrlFile`). Plan: after the BSE stream finishes, one probe request for
  `/XBRL1/<XbrlFile>`; if BSE serves it, the June-2025 XBRLs are fetched the same way for firms with Jul–Dec 2025
  events (same stream, ≥ 1.6 s). If not, those events have pledge unknown (no fallback to an older SHP). The rule
  itself is unchanged.
- 2026-11-23: `c3_flags.py` was run once on the partial cache purely to debug the code (it prints coverage counts
  only; no flag × outcome table was produced or looked at).
- 2026-11-23: fetch complete. Screener: 557 of 557 event firms have a standalone page and cash-flow schedule (159
  cached, 398 fetched; 869 requests, one stream ≥ 1.55 s). BSE: SHP lists + needed June-quarter XBRLs, 2,988 + 9
  requests (one stream ≥ 1.6 s; 1 list retried after a connection reset; 5 files failed). D1 probe succeeded:
  `/XBRL1/<XbrlFile>` serves the June-2025 XBRL; 418 fetched (same stream). The screener and BSE streams ran in
  parallel (different hosts, one stream each). A usage-limit pause came after the fetch. Next: `c3_flags.py` (full),
  then `c4_analyze.py`, run once.
- 2026-11-23: `c3_flags.py` (full) and `c4_analyze.py` ran once, unchanged. One post-hoc check (`c5_posthoc.py`,
  labelled exploratory) added after reading the primary tables: halving ratio A ÷ C.

---

# RESULTS (written 2026-11-23 after the run; everything above is the unchanged pre-registration and log)

## Coverage
10,242 events (557 firms). Annual flags known for all 10,242 (S2 unknown 79, S5 unknown 11). Pledge known for
9,564: 133 events have no BSE code, 515 no June-quarter SHP in the 15-month window, 30 no XBRL or a parse failure.
**RED known for 9,623 events (619 unknown, excluded).** RED fires on 2,531 (26%): S2 (interest cover < 1.5x) on 20% of
events, B25 on 7%, S5-India on 3%. Halving outcome known for all events (the price data reach Nov-2026; the last entry
is Nov-2025).

## Verdicts (13 weeks; all events 2018–2025; 32 fiscal quarters; 5,000-draw quarter bootstrap)
| group | n | 13-week excess vs size-matched controls | P(price ≤ 0.5× within 12 months) |
|---|---|---|---|
| **A** bottom-two SUE + red flag | 989 | −1.71% [−4.27, +1.08], t −1.25 | **17.6%** (174) |
| **B** bottom-two SUE, no flag | 2,861 | −1.13% [−1.92, −0.33], t −2.76 | 8.3% (238) |
| **C** red flag, quintiles 3–5 | 1,542 | +0.56% [−1.13, +2.33] | 15.1% (233) |
| **D** neither | 4,231 | +1.22% [+0.59, +1.85], t 3.71 | 6.1% (257) |

| hypothesis | result | verdict |
|---|---|---|
| **H1** A − B ≤ −2 pp at 13 weeks, CI < 0 | **−0.58 pp [−3.49, +2.58]**, t −0.37 | **NOT SUPPORTED** |
| **H2** P(halving) A ÷ D ≥ 2×, CI > 1 | **2.90× [2.46, 3.59]** | **SUPPORTED** |

No group is below 50 events in the primary test (smallest: A, 989).

## What sits behind the verdicts
- **The red flag adds no extra drift after a miss.** A lags controls a little more than B on average, but the
  difference is noise (CI −3.5 to +2.6 pp). The interaction (A − B) − (C − D) is +0.08 pp [−2.79, +2.92]. The
  miss itself still matters: B − D = −2.35 pp [−3.25, −1.41], t −4.8, the known avoid leg.
- **The halving risk comes from the flag, not from the combination.** C (flag without a miss) halves 15.1% of the
  time, 2.49× D [2.08, 3.07]. A ÷ C = 1.16× [0.93, 1.45] (post-hoc): adding the miss to a flagged firm does not
  clearly raise the halving rate. A ÷ B = 2.11× [1.65, 2.89]: among misses, the flag doubles the halving risk.
- **Sensitivities agree** (H1 not supported and H2 supported in every one): unknown treated as unflagged (A ÷ D 2.71×),
  live firms only (2.72×), financials excluded (3.26×; A − B −0.22 pp), 2018–21 (2.51×; A − B −3.12 pp
  [−6.84, +1.13] — the only period that points toward H1, and its CI includes 0), 2022–25 (2.66×; A − B +1.96 pp),
  26 weeks (A − B −0.91 pp [−4.28, +2.36]).
- **By component:** pledge is the strongest halving signal. B50: A halves 29.1% (251 events), A ÷ D 3.91×
  [2.91, 5.14]; C 25.8%. B25: A 26.3%, 3.71×. S2 alone 2.41×. **S5-India alone carries no signal here** (A ÷ D
  1.05× [0.42, 1.81]; A has 110 events). For drift, B50's A − B is −2.0 pp, but the CI is −7.4 to +3.5 (251 events).

## Decision-card rule (as pre-registered: H1 not supported, H2 supported → a tail-risk rule)
1. **Keep the PEAD avoid gate as it is** (bottom-two SUE = WAIT for ≥ 63 trading days). The red flag does not make
   the 13-week drift worse, so there is no "EXIT" escalation.
2. **Add a survival cap:** bottom-two SUE **and** a red flag (pledge > 25% or interest cover < 1.5x) → no new money /
   minimum size, and a deep-dive question on the balance sheet. About 1 in 6 such events halved within a year
   (1 in 4 with pledge > 50%), against 1 in 16 for clean firms with no miss.
3. **The honest refinement:** C shows the same halving risk without a miss. So the stage-2 red flag is the tail-risk
   signal on its own (≈ 2.5× base), and the miss adds little to it. The pre-registered rule ties the cap to the
   combination. The data say the cap could apply to any red-flag firm. **That broader rule was not pre-registered, so it is a
   proposal for a future test, not an adopted rule.** S5-India should not trigger the cap (no signal here).

## Caveats
- Pledge comes from one June-quarter SHP per year (0–15 months stale, pre-registered). This dilutes the flags, so the
  true halving gaps are probably a little larger.
- S2 fires on 20% of events, including banks and NBFCs (their interest cover is structurally < 1.5x). The verdicts
  are the same with financials excluded.
- Restated standalone screener annuals (holdco debt under-flagged); weekly closes; price returns only; dead firms
  are a 39% sample and most failures were below the ₹500 cr floor (L31).
- Halving is about the path, and events overlap (the same firm appears in several quarters). The quarter bootstrap
  handles the time clustering but not the firm clustering, so the halving CIs are somewhat too narrow.
- 2018–21 includes the IL&FS/NBFC squeeze and COVID: halving rates there are about 2–3× those of 2022–25.

Scripts: `tools/backtests/combined_avoid/` (common3, c1_fetch_screener, c2_fetch_bse, c2b_june2025, c3_flags,
c4_analyze, c5_posthoc). Outputs: `research_notes/Backtests/combined_avoid_outputs/` (results.json, tables.md,
events_flags.tsv, c3_coverage.json, posthoc_A_over_C.json). Caches: scratchpad `bt_comb/` (sc/, shp/, status_sc.json).
