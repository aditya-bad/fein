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
