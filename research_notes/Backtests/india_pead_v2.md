# Backtest v2: post-earnings drift (PEAD) in Indian stocks: consolidated EPS, full universe, fresh 2026 data

*Method calibration, not stock picking. Research, not SEBI-registered advice.*

Builds on `research_notes/Backtests/india_pead.md` (v1; lesson L17; memdb `insight:bt-india-pead-2018-2025`).
v1 found top-minus-bottom SUE-quintile drift of +4.2% at 63 days, out of sample (t ≈ 4). The long-only top quintile beat
size-matched controls by +2.36% gross / +1.36% net of 1%, which missed the pre-committed cost rule by 0.06 pp. v1 left
four open items: standalone EPS, a 580-company sample, an exploratory "price rose on results" filter, and a weak 2025.
v2 tests these, with the rules fixed below.

## Pre-registration (written 2026-11-21, BEFORE any 2026 event or return statistic was computed)

**State of knowledge when this was written (honest disclosure).** v1's price cache (Yahoo, fetched 2026-11-21) already
holds daily prices to 18-Nov-2026 for 1,000 symbols. No 2026 event was ever built from it: v1's event window ended
2025-12-31, and no 2026 SUE, quintile or return was computed or looked at. The only 2026 facts looked at before writing
this are the NSE feed schemas: one company's (KPITTECH) list of 2025–26 consolidated and standalone filings, and the
count and subject mix of one day's corporate announcements. Neither contains returns.

### Hypotheses
- **H1 (primary).** v1's long-only rule (buy the top EPS-SUE quintile at the close of the first trading day after the
  results filing, hold 63 trading days) beats size-matched controls by **more than the 1% round-trip cost**. This uses
  **consolidated EPS where available** on the **full eligible NSE universe** (₹500–50,000 cr at entry). It is tested
  (a) in the **fresh period** of results announced 2026-01-01 → 2026-11-21, which is out of sample for v1, and (b) in a
  **2022–25 re-run** under the v2 data rules (replication).
- **H2 (primary; exploratory in v1).** Adding the filter **"announcement-window return > 0"** (close before the filing
  date to the entry close, as in v1's `ann_ret`) improves the top-quintile result. **Judged on 2026 data only** (fresh
  OOS). 2022–25 is reported as replication; v1 found it there, so it cannot confirm itself.
- **H3 (primary).** The bottom quintile ("avoid" leg) stays negative vs controls, **≤ −1% at 63 days**, in 2026.
- **H4 (EXPLORATORY, labelled so).** The middle mcap tertile shows the strongest drift (T−B and top-vs-controls). It is
  reported, never used for a verdict.

### Fresh-period structure (fixed)
Fiscal-quarter cross-sections announced in 2026: quarters ended **Dec-2025** (filed Jan–Feb 2026), **Mar-2026**
(Apr–May), **Jun-2026** (Jul–Aug) and **Sep-2026** (Oct–Nov).
- **63-day tests use events whose 63-trading-day window has closed** by the last price date. In practice that means
  Dec-25 and Mar-26, plus most of Jun-26. Events with an open window are excluded from 63d statistics, and the count is
  reported.
- **Sep-2026 quarter: only 21-day results (where that window has closed). Its 63-day result is marked PENDING**
  (closes about mid-Feb 2027). It is not a primary result.
- Quintiles are always assigned among **all** eligible events of the fiscal quarter, whatever their window status. The
  assignment uses only announcement-time information, so it cannot depend on outcomes.

### Data rules (changes from v1 marked ★)
- ★ **Universe:** every symbol in the current NSE equity list (`EQUITY_L.csv`, EQ/BE) **listed on or before
  2023-12-31** (1,870 symbols), not a sample. The SUE-history requirement removes late listers anyway. Pre-filter:
  drop a symbol only if shares (latest filing) × unadjusted close never touches ₹400–60,000 cr in 2021–2026. Event-level
  filter ₹500–50,000 cr at entry, as in v1. Survivorship: current list only (same as v1). Delisted firms are absent and
  get the same audit logic as v1 §4.
- ★ **EPS basis:** for each event, **consolidated basic EPS** is used if the company filed consolidated results for the
  event quarter, the same quarter a year earlier, and at least 4 of the 8 prior seasonal-change pairs. All of those come
  from filings for quarters ended 30-Jun-2019 or later (FY2020+). Otherwise the event uses **standalone** EPS (v1
  basis). The SUE of an event never mixes bases. The basis is recorded per event, and the consolidated-only subset is
  reported as a sensitivity check (not a verdict).
- Consolidated EPS = basic EPS attributable to owners of the parent as tagged in the filing's XBRL (same tag priority as
  v1). Split/bonus adjustment as v1 D2. Returns are price returns (v1 D3).
- **Filings and dates:** quarters to Dec-2024 come from `corporates-financial-results`, and quarters from Dec-2024 on
  from `integrated-filing-results`. The union is used, with the earliest timestamp per quarter and basis. Event date is
  the earliest results announcement ("Financial Result Updates" / results "Outcome of Board Meeting") after
  quarter-end and no later than the feed date, else the feed date (v1 D8). ★ Announcements for symbols not in v1's
  cache come from NSE's all-company corporate-announcements feed queried one calendar day at a time. Filings more than
  150 days after quarter-end are dropped (v1 D5).
- Entry: adjusted close of the first NSE trading day strictly after the event date. Horizons: 21 / 63 / 126 days;
  **primary = 63**.
- **SUE:** as v1: `(EPS_q − EPS_{q−4}) / sd(previous up to 8 seasonal changes)`, with ≥ 4 prior changes required and
  sd > 0. Quintiles within each fiscal quarter (≥ 25 events). Tertiles by mcap within each fiscal quarter.
- **Controls:** as v1. Equal-weight return over the identical window of all universe stocks with fetched shares and
  prices, mcap ×0.5–×2 of the event firm on the entry date, firm itself excluded, ≥ 5 required. Excess = event return
  − control return.
- **Costs:** a long-only position pays one round trip: **net = excess − 1.0%** (also shown at 0.5%).
- **Fetch order and stopping rule (★, written before fetching):** pass A fetches, for every universe symbol in v1's
  seeded order (seed 20261121; then the 79 symbols listed in H2-2023, in alphabetical order), both filing lists and the
  XBRL for quarters ended **Dec-2022 → Sep-2026**. That is all the fresh test needs. Pass B then fetches quarters
  **Jun-2019 → Sep-2022** in the same order, for the 2022–25 re-run. If pass B cannot finish within this session's
  fetch budget, the re-run uses the symbols pass B completed. That subset is random by construction, and the report
  says so. No result statistic is computed before pass A is complete for every symbol.

### Inference (fixed)
- **Fresh 2026 data (verdicts):** with only 2–4 fiscal quarters, a t-stat across quarters is meaningless. Inference is
  **event-level**: the pooled mean of event excess returns, a **t-stat with standard errors clustered by entry
  calendar week**, and a **95% cluster bootstrap CI** that resamples entry weeks (5,000 draws, seed 1). As a
  sensitivity check, the same statistics clustered by entry calendar month are reported. The mean of quarterly values
  is shown for context.
- **2022–25 re-run (replication):** v1's method, with the mean of the 16 quarterly values, a t-stat across quarters and
  a 95% bootstrap over quarters (5,000).

### Decision rules (pre-committed; anything that fails a rule is "not proven")
- **H1, fresh:** **PROVEN-fresh** if the top-quintile mean excess **net of 1%** at 63d is > 0, **and** either the
  week-clustered t on the net figure is > 3 or its 95% cluster-bootstrap CI excludes zero.
  **H1, re-run:** **REPLICATES** if the 2022–25 quarter-level net-of-1% mean is > 0 with t > 3 or a 95% CI that excludes
  zero.
  **H1 is "supported" only if PROVEN-fresh and REPLICATES both hold.** Fresh alone counts as "fresh pass, no replication"
  and re-run alone as "not proven OOS". Neither half is called an edge.
- **H2:** the statistic is the contrast **D = mean excess(top ∩ ann_ret > 0) − mean excess(top ∩ ann_ret ≤ 0)** at 63d,
  using fresh 2026 events only. H2 is supported if D > 0 and (week-clustered t > 3 or the 95% cluster-bootstrap CI of D
  excludes zero) **and** the filtered top quintile's net-of-1% mean is above the unfiltered one. 2022–25 D is
  replication only.
- **H3:** supported if the bottom-quintile mean excess at 63d in 2026 is **≤ −1%** and (week-clustered t < −3 or the
  95% CI upper bound < 0). No cost adjustment applies, because avoiding a stock costs nothing.
- **H4:** descriptive only.
- **Everything else is exploratory:** 21d and 126d, T−B, the consolidated-only subset, by-quarter results, the Sep-26
  21d result, deciles and mcap splits.
- No hypothesis, horizon, filter or statistic will be added to the verdict after results are seen. Deviations go in
  the log below with a date and a reason, written before the affected numbers are computed where possible.

---

## Deviation log (append-only, dated)

*(empty at pre-registration)*
