# Pre-registered test: does the Nifty earnings-yield minus 10-yr G-sec gap predict Nifty returns beyond P/E alone?

**Pre-registration written 2026-11-26, before any data was downloaded or any number computed.**
Roadmap stage 5 (valuation context). Unlocks: a tested (or rejected) market-level valuation input for the
decision card's exit-multiple / sizing context (stage 6), and a base rate for the macro snapshot (`tools/macro/`).

## Question
H1: Nifty trailing P/E at month-end t predicts subsequent 3-yr and 5-yr Nifty 50 total-return CAGR (negative sign).
H2: The gap G = (100 / P/E) − y10 (Nifty trailing earnings yield % minus India 10-yr G-sec yield %) adds information
beyond P/E alone (positive sign: a wider gap → higher future returns).

## Data (fixed in advance)
- Nifty 50 trailing P/E (standalone, as published by NSE/NSE Indices) at each month-end; Nifty 50 TRI levels
  (fallback: price index + dividend yield accumulated monthly, noted as a deviation if used).
- India 10-yr government bond yield, monthly: FRED `INDIRLTLT01STM` (OECD MEI, long-term government bond yield),
  second check against RBI DBIE / published spot values where cheap.
- Starts: every month-end from 1999-07 (or the first month all series exist; 2004-01 if earlier P/E is not
  fetchable) to the last month with a complete forward window (3-yr: ≤ 2023-10; 5-yr: ≤ 2021-10). Task brief caps
  starts at 2021; for 3-yr we use starts ≤2021-12 when the window completes, and report the extended set separately.
- Note: NSE changed the P/E basis from standalone to consolidated earnings on 2021-03-31 (known in advance). Our
  5-yr starts end ≤2021-10 so the change affects only the last ~7 starts; flagged, not adjusted.

## Models (OLS, y = forward CAGR in %)
- M0: y = a + b·(1/PE)  — earnings-yield form of "P/E alone" (also report y on log(PE) as a robustness line).
- M1: y = a + b·(1/PE) + c·y10  (equivalent to adding the gap: EY and y10 enter separately; c < 0 expected).
- M2: y = a + d·G  (gap alone).
- Primary comparison for H2: M1 vs M0 (does the bond yield add information beyond P/E?). M2 vs M0 reported too.

## Overlap correction
- Newey-West (HAC) standard errors with lag = horizon in months − 1 (35 for 3-yr, 59 for 5-yr), Bartlett kernel.
- Robustness: non-overlapping subsamples (one start every 36 / 60 months, all phase offsets; report median slope and
  sign agreement across offsets). With ~4–5 independent 5-yr windows, any significance claim is weak by construction.

## Out-of-sample
- Fit on starts ≤ 2012-12; test on starts 2013-01 onward (3-yr: 2013-01..2021/2023; 5-yr: 2013-01..2021-10).
- OOS R² = 1 − SSE_model / SSE_benchmark, where the benchmark is the training-sample mean return (Campbell–Thompson).
- Report OOS R² for M0, M1, M2 at both horizons.

## Decision rules (fixed now)
- H1 "P/E predicts": NW t-stat of b with the expected sign |t| ≥ 2 in the full sample AND OOS R²(M0) > 0 AND
  slope sign correct in both halves (≤2012 fit, 2013+ fit separately).
- H2 "gap adds information beyond P/E alone": OOS R²(M1) − OOS R²(M0) ≥ 0.05 AND the y10 coefficient (c) has the
  expected negative sign in BOTH halves fitted separately. Either horizon passing counts as "adds information at that
  horizon"; we report each horizon separately and do not average.
- If H2 fails: the macro snapshot shows the gap as context only and the decision card does not use it.
- If data is insufficient (P/E history not fetchable before 2004, or yields missing), report that, run on what exists,
  and lower confidence to `single-source`/`unverified`.

## Known limits stated in advance
- Effective sample is tiny (1999–2026 is ~5 non-overlapping 5-yr windows); a regime (2003–07 boom, 2008 crash) can
  dominate. OOS test period 2013+ includes the 2020 Covid low and the 2021 consolidated-earnings switch.
- India yields were partly administered before ~2000s; the OECD series is a monthly average, not month-end.
- Prior work: `insight:india-valuation-forward-returns` (Freefincal: every negative 5-yr Nifty return began at P/E ≥ 24.5).
  This test is a regression check on the same family, not an independent dataset.

## Deviation 1 (written 2026-11-26, after probing data availability, BEFORE computing any regression)
- **P/E history before Feb-2012 is not available from a permitted public static source.** NSE's daily file
  `archives.nseindia.com/content/indices/ind_close_all_DDMMYYYY.csv` (P/E, P/B, div yield) exists from 2012-02-29
  (2012-01-31 and earlier return 404). The niftyindices.com historical-P/E endpoint is a browser-only API; scripted
  access was refused by this session's policy and was not worked around.
- **FRED INDIRLTLT01STM starts 2011-12** (180 rows to 2026-10). No pre-2011 monthly 10-yr series fetched.
- **No TRI in the archive files** → pre-stated fallback: monthly total return = price return + (div yield %/12).
- Consequences, fixed now: starts 2012-02 → 2021-10 (5-yr, ~117 starts, ≈2 independent windows) and 2012-02 → 2023-10
  (3-yr, ~141 starts, ≈4 windows). The ≤2012 / 2013+ split is impossible (≤12 training points); replaced by
  **fit on starts ≤ 2016-12, test on 2017-01 onward**. Decision rules otherwise unchanged. Whatever the result,
  confidence is capped at `unverified` (sample far too short for a valuation-cycle claim), and the 1999–2011 test
  stays open until a P/E history (e.g. a manual niftyindices CSV export by the user) is added.

---
## Results
(Filled in after computation — below this line only.)
