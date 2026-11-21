# Backtest: post-earnings-announcement drift (PEAD) in Indian stocks — announcements 2018–2025

*Method calibration, not stock picking. Research, not SEBI-registered advice.*

## Pre-registration (written 2026-11-21 BEFORE any results or price data was downloaded)

**Why.** memdb `insight:lit-pead-post-earnings-drift`: Bernard–Thomas (1989) found ~4% top-minus-bottom
SUE-decile drift over 60 trading days in the US; Martineau (2022) shows it has vanished in US large/mid caps
and survives in microcaps. India has thin analyst coverage below the top ~300 names, results scattered over
~45 days and filed as PDFs — plausible conditions for underreaction. No academic Indian study was found in our
literature sweep. Bar for an "edge": `insight:lit-harvey-liu-zhu-multiple-testing` (t > 3, or out-of-sample).
Hygiene copied from `research_notes/Backtests/insider_clusters_us.md` (L14: matched controls, date at filing,
survivorship audit, pre-registered subgroups).

**Hypotheses.**
- **H1 (primary).** Stocks in the top SUE quintile out-perform stocks in the bottom SUE quintile over the
  63 trading days (≈3 months) after entry. H0: mean top-minus-bottom (T−B) = 0.
- **H2 (primary, long-only relevance).** Top-quintile stocks out-perform size-matched controls over 63 days.
- **H3 (pre-registered split).** The T−B spread is larger in the smallest mcap tertile (proxy for low analyst
  coverage) than in the largest tertile.

**Surprise measure (fixed).**
- Primary: **SUE (EPS)** from a seasonal random walk: `SUE_q = (EPS_q − EPS_{q−4}) / sd(ΔEPS over the
  previous 8 quarters)`, where ΔEPS_k = EPS_k − EPS_{k−4}, using only changes known before quarter q
  (k = q−1 … q−8). Require ≥ 4 prior changes (sd over what exists, up to 8); require sd > 0.
  EPS = basic EPS as reported for the quarter (consolidated if the company files consolidated results,
  else standalone; the same basis throughout for a company). Quarters with EPS restated later: use the
  figure in the filing for that quarter (first-reported where available).
- Secondary: **revenue SUE**, same formula on quarterly revenue from operations (per share not needed: the
  scale cancels in the ratio).
- Winsorise SUE at ±10 before ranking is not needed (ranks only); SUE is used only for ranking.

**Event date (fixed).** The NSE (or BSE if NSE missing) broadcast/filing timestamp of the quarterly result.
Entry = **adjusted close on the first NSE trading day strictly after the broadcast date** (so a result filed
during market hours or after the close is fully public before entry; this sacrifices the day-1 reaction,
on purpose — it is what we could actually trade). Secondary (context only): entry at the next-day open.

**Portfolios (fixed).** Cross-sections = fiscal quarter of the result (e.g., all Q3 FY24 results, quarter
ended 31-Dec-2023). Within each fiscal quarter, rank eligible events by SUE into **quintiles (primary)**
and deciles (secondary). Event-time returns: each stock enters on its own entry date. Portfolio return for a
quarter = equal-weighted mean of member returns. T−B per quarter = mean(top) − mean(bottom).
Horizons: **21, 63, 126 trading days** (≈1, 3, 6 months). Primary horizon = 63 days.

**Universe (fixed).** NSE main-board equities with market cap ₹500 cr–₹50,000 cr at the entry date. Market cap
= shares outstanding (best available point-in-time source; approximation documented in §1) × close.
Exclude: banks/NBFCs/insurers are **kept** (EPS-based SUE works for them) but reported as a subset;
exclude stocks with < 250 days of price history before entry; exclude EPS series with gaps that prevent
the SUE computation. If full-universe data is infeasible, a seeded random sample of ≥ 300 companies from the
NSE equity list is used, and the report says so.

**Size-matched controls (H2).** For each event, control return = equal-weight mean return over the
identical window of all *sampled* universe stocks with mcap within ×0.5–×2 of the event firm on the entry
date (excluding the event firm; require ≥ 5 controls). Excess = event return − control return.

**Coverage proxy (H3).** Mcap tertile of the event firm, cut points recomputed each fiscal quarter among that
quarter's eligible events.

**Sample periods.** Train = announcements 2018-01-01 → 2021-12-31; Test = 2022-01-01 → 2025-12-31.
Both are reported; **the verdict is based on the test period**.

**Inference.** Unit = fiscal quarter (16 train, 16 test). Mean of quarterly T−B, t-stat across quarters
(Newey–West not needed at 63d since quarters barely overlap; reported naive across-quarter t), and a
**95% bootstrap CI resampling quarters** (5,000 draws). Event-level means also reported for context.

**Decision rules (pre-committed).**
1. Train-period result with **t < 3 will not be called an edge** (Harvey–Liu–Zhu), whatever its sign.
2. "Edge candidate" requires: test-period 63d T−B bootstrap CI excludes 0 (positive), **and** same sign as
   train, **and** top-vs-controls (H2) net of a 1% round-trip cost still > 0 with CI excluding 0 for a
   long-only version. Otherwise: "not established".
3. H3 "supported" only if the small-tertile T−B minus large-tertile T−B is > 0 in both periods with the test
   CI of the difference excluding 0.
4. Costs: report gross and net of 0.5% and 1.0% round trip (T−B long-short = two round trips; India shorting
   of cash equities over 3 months is not practical for retail, so the long-only H2 is the practical test).

**Everything else is exploratory** (revenue SUE, deciles, next-day open entry, sector, year-by-year,
both-beat EPS+revenue, Friday/crowded-day effects) and must be re-tested before it is believed.

**Survivorship plan.** Current NSE equity list misses delisted/merged firms. Count sampled firms with
truncated price history, and bound the effect under stated assumptions.

---

## Deviation log (append-only, each dated)

*(empty at pre-registration)*
