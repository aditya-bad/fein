# Backtest: Indian promoter / insider open-market buying (SEBI PIT Reg 7) — signals 2021–2024

*Run 2026-11-21. Method calibration, not stock picking. Research, not SEBI-registered advice.*

## Pre-registration (written 2026-11-21 BEFORE any PIT or price data was downloaded)

**Hypothesis (H1).** In NSE-listed companies with market cap ₹500 cr–₹20,000 cr, a cluster of
open-market purchases by promoters/promoter group or by KMP/directors (≥ ₹1 cr total, or ≥ 0.25% of
equity, within 30 days) predicts positive 12-month excess return versus 5 size-matched random NSE stocks
measured from the same entry date. H0: mean 12m excess = 0.

**Data.** NSE `corporates-pit` (SEBI PIT Reg 7(2) disclosures), date-range queries 2021-01-01 → 2024-12-31
(broadcast date). Prices: Yahoo v8 chart (`.NS`), adjusted close, ≥ 1 s per call.

**Transaction filter (fixed).**
- Include: acquisition mode = "Market Purchase" (open market on exchange), transaction type = Buy/Acquisition,
  person category in {Promoters, Promoter Group, Director, Key Managerial Personnel (KMP)} (incl.
  "Immediate relative" of these only if the category field itself is one of the above).
- Exclude: off-market, inter-se transfer, ESOP/ESOS, gift, inheritance, pledge creation/invocation/revocation,
  preferential allotment, rights, bonus, conversion of warrants, buy-back, scheme of arrangement, any
  non-"Market Purchase" mode; sales; securities other than equity shares; rows with zero/missing value.
- Person classes: "promoter" = Promoters / Promoter Group (and their immediate relatives);
  "KMP" = Director / KMP / Designated person who is not tagged promoter.

**Event definition (fixed).**
- Rolling window: starting at the first qualifying purchase (by broadcast date) for a company, accumulate
  qualifying purchases whose *broadcast* dates fall within the next 30 calendar days. Event fires on the
  broadcast date on which cumulative value first reaches ≥ ₹1 crore **or** cumulative shares reach ≥ 0.25%
  of equity (where the disclosure reports post-holding % change; otherwise ₹1 cr test only).
- One event per company per 365 days (first qualifying one).
- Signal (event) dates 2021-01-01 → 2024-12-31.
- Market cap at event (₹500–₹20,000 cr) = shares outstanding × close on event date (shares from the best
  available source; approximation documented in §1).

**Entry / horizons.** Adjusted close on the first NSE trading day strictly **after** the event broadcast date.
Horizons 63 / 126 / 252 trading days (≈ 3 / 6 / 12 months).

**Primary metric.** 12m excess return = event stock return − mean return of 5 size-matched random NSE
stocks over the identical window. Controls: drawn with a fixed seed from the control universe, mcap within
×0.5–×2 of the event firm on the event date, listed ≥ 180 days, no own qualifying event within ±365 days.
Inference: mean, median, hit rate (excess > 0); 95% bootstrap CI resampling **event-months** (2,000 draws).
Decision rule: H1 "supported" only if the 12m mean-excess CI excludes 0 on the positive side; "not
supported" otherwise; an effect is "practically relevant" only if the point estimate ≥ +5%/yr.

**Secondary (pre-registered, only these two splits).**
1. Promoter-only events vs KMP-only events (events with both buyer types reported as "mixed").
2. Small (₹500–₹2,000 cr) vs large (₹2,000–₹20,000 cr).
Also reported as context (not tests): 3m/6m horizons, NIFTY 500 index excess if an index series is available.

**Everything else is exploratory** (buy-size buckets, year splits, sector, pledge status, etc.) and must be
re-tested out of sample before being believed.

**Survivorship plan.** Event and control stocks with no Yahoo history (delisted / merged / renamed) are
listed and audited; a bound is computed under stated assumptions.

---
