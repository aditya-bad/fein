# Backtest: US insider-buying clusters (Form 4, code P) — small/mid caps, signals 2021–2024

*Run 2026-11-20/21. Method calibration, not stock picking. Research, not SEBI/SEC-registered advice.*

## Hypothesis tested
"Clusters of open-market insider BUYING (Form 4 code P, not 10b5-1, ≥2 insiders within 30 days) in US
small/mid caps predict positive excess returns over the next 6–12 months."

## Verdict (short)
**Not supported in 2021–2024 for this simple public rule.** Against size-matched random controls drawn
on the same dates, 849 cluster events (ex-biotech) earned **0.0% mean / −3.9% median excess over 12 months**
(95% month-clustered bootstrap CI for the mean **−4.8% to +5.0%**; hit rate 44.9%). At 6 months: −0.3% mean
(CI −3.3% to +2.6%). The CI is wide enough to hide a small effect (~+2–4%/yr) but rules out an effect of
the size Cohen–Malloy–Pomorski report for *opportunistic* insiders (~10%/yr) for this unfiltered rule, even
after a generous survivorship correction (see §6). **As a standalone screen it is not an edge for us.** At most it is
a weak tilt / research-queue prioritiser; any real edge would have to come from extra filtering
(opportunistic vs routine, buy size vs holdings, governance, banks) that this test did not establish.

## 1. Data and method
| Item | Choice |
|---|---|
| Form 4 source | SEC **Insider Transactions Data Sets** (quarterly zips, 2020q4–2025q1) — SEC's own parse of every Form 3/4/5 XML, i.e. the *full population*, not a sample of daily `form.idx`. Spot-checked 4 DTM filings (May-2023) against the raw XML parsed by `tools/sec_fetch.py`: shares, price, date, owner, 10b5-1 flag all matched. |
| Purchases | Form 4/4-A, `TRANS_CODE = P`, acquired. 122,312 purchase rows → 71,899 kept. |
| Excluded | 10b5-1 (checkbox from 2023-04 *or* any footnote mentioning 10b5-1: 7,964 rows); pure 10%-owners/"Other" (28,908); price < $1 (10,502); preferred/warrants/units/notes (2,447); bad/NONE tickers. Option exercises (M), grants (A), etc. never enter (code P only). |
| Cluster | ≥2 **distinct** directors/officers with purchase trade dates within 30 days of each other. **Event date = filing date** on which the 2nd insider's buy became public. One event per issuer per 365 days. Signal dates 2021-01-01 → 2024-12-31. → 3,339 events, 2,267 issuers. |
| Size | Market cap at event = dei `EntityCommonStockSharesOutstanding` (latest XBRL frame ≤ event date, ≤200 days old) × insider VWAP. Kept **$300M–$10B**. Multi-class firms can be understated. |
| Sector | SIC from SEC submissions. Dropped SPACs (6770) and funds (6722/6726/6799); **biotech/pharma (2834/2835/2836/8731) reported separately.** Banks/thrifts reported as a subset. |
| Listing age | Dropped events < 180 days after first Yahoo price (IPO / de-SPAC PIPE "purchases" at $10 etc.). |
| Prices | Yahoo v8 chart, adjusted close, 1.1 s between calls. Identity check: Yahoo un-split-adjusted close on entry day must be within 0.6–1.67× insider VWAP (10 events failed → dropped as likely ticker reuse). 64 events recovered via the issuer's current ticker (renames). |
| Entry / horizons | Adjusted close on first trading day **after** the filing date; returns over 21/63/126/252 trading days (≈1/3/6/12 m). |
| Benchmarks | IWM and SPY over the identical window; **matched control**: for each event, 5 random firms (seeded) from the point-in-time universe (any issuer with a Form 4 that quarter, 1,500 random draws), same exclusions, mcap within ×0.6–×1.67 of the event firm on that date, no own cluster within ±365 days, ≥180 days listed. Biotech events matched to biotech controls. 953/956 events got the full 5 controls. |
| Stats | Mean, 1/99% winsorised mean, median, hit rate (excess > 0); naive t; **95% bootstrap CI resampling event-months** (events in the same month share shocks; 2,000 draws). The naive t overstates significance — read the CIs. |

Funnel: 3,339 events → 1,421 outside $300M–$10B, 669 no shares frame, 2 SPAC/fund, 61 recent listing,
221 no Yahoo history, 10 price mismatch → **955 usable (849 ex-biotech + 106 biotech).** Median event mcap
≈ $1.0B; median cluster buy ≈ $238k.

## 2. Main results (ex-biotech, n = 849)
Excess return = event return − benchmark return over the same window.

| Benchmark | Horizon | Mean [95% CI] | Median [95% CI] | Hit rate | naive t |
|---|---|---|---|---|---|
| vs IWM | 1m | +0.9% [−0.3, +2.1] | +0.4% | 51.8% | 2.24 |
| vs IWM | 3m | +0.7% [−1.4, +2.8] | −0.1% | 49.6% | 1.00 |
| vs IWM | 6m | +0.8% [−1.8, +3.4] | −0.3% | 49.6% | 0.82 |
| vs IWM | 12m | +1.7% [−2.7, +6.4] | −2.7% [−6.8, +1.6] | 46.5% | 0.94 |
| vs SPY | 6m | −4.0% [−6.8, −1.5] | −5.6% | 39.9% | −3.85 |
| vs SPY | 12m | −7.9% [−12.9, −2.6] | −13.3% | 35.0% | −4.26 |
| **vs matched controls** | 1m | +0.6% [−0.4, +1.7] | +0.5% | 52.4% | 1.42 |
| **vs matched controls** | 3m | −1.0% [−3.7, +1.6] | −1.4% | 47.5% | −1.10 |
| **vs matched controls** | 6m | −0.3% [−3.3, +2.6] | −1.8% [−4.9, +0.3] | 46.2% | −0.25 |
| **vs matched controls** | 12m | **0.0% [−4.8, +5.0]** | **−3.9% [−8.6, +0.3]** | **44.9%** | 0.01 |
| controls vs IWM (sanity) | 12m | +1.7% [+0.4, +3.2] | +1.0% | 52.3% | 2.55 |

Reading: the "beats IWM" numbers are entirely explained by the size/survivor profile of the firms —
the random size-matched controls beat IWM by the same ~1.7%/yr (they are survivors and mid-cap-tilted).
Versus SPY the events lost badly because 2021–2025 was a mega-cap decade, not because of the signal.
Mean > median throughout: a few big winners, most events lag. That skew is the classic small-cap lottery shape.

## 3. Subsamples (excess vs matched controls)
| Subset | n | 6m mean [CI] | 12m mean [CI] | 12m median | 12m hit |
|---|---|---|---|---|---|
| Banks/thrifts | 207 | +4.0% [−2.5, +10.0] | +1.3% [−7.7, +10.0] | +1.2% | 52.2% |
| Non-banks | 642 | −1.7% [−5.0, +1.5] | −0.4% [−5.2, +4.9] | −5.7% | 42.5% |
| ≥3 insiders | 190 | −2.3% [−8.0, +2.9] | −4.4% [−12.9, +5.0] | −5.1% | 45.3% |
| CEO or CFO among buyers | 429 | −1.9% [−5.8, +1.6] | −1.5% [−8.6, +6.5] | −9.7% | 40.8% |
| Cluster buy ≥ $250k | 390 | −0.9% [−5.5, +3.3] | +2.6% [−3.9, +10.1] | −2.9% | 46.2% |
| Mcap $300M–$1B | 407 | +1.9% [−3.0, +6.5] | +4.8% [−2.2, +12.3] | −0.4% | 49.6% |
| Mcap $1B–$10B | 442 | −2.3% [−5.5, +0.7] | −4.4% [−8.9, +0.6] | −8.1% | 40.5% |
| Signals in 2021 | 186 | +2.2% [−1.9, +7.5] | **+6.3% [+0.7, +12.3]** | +2.0% | 54.8% |
| Signals in 2022 | 238 | +0.5% [−3.5, +4.7] | −2.0% [−10.1, +9.8] | −8.1% | 38.2% |
| Signals in 2023 | 248 | −0.2% [−9.7, +5.2] | −0.6% [−11.9, +8.7] | −4.4% | 44.4% |
| Signals in 2024 | 177 | −4.0% [−10.7, +2.3] | −2.9% [−14.7, +8.7] | −4.4% | 44.1% |
| **Biotech/pharma (separate)** | 106 | +2.5% [−7.8, +12.5] | +10.7% [−5.1, +27.0] | +3.6% | 50.9% |

Nothing survives cleanly. Directionally consistent with the literature: the smaller half ($300M–$1B) and
banks look better than $1B–$10B; the "stronger" variants people assume (≥3 insiders, CEO/CFO) were *not*
better. Biotech is a lottery (huge dispersion; mean driven by a few takeovers/approvals). Subsets were not
pre-registered — treat any positive one as a hypothesis for a fresh out-of-sample test, not a finding.

## 4. Comparison with the literature (memdb `insight:us-insider-buying-evidence`)
- **Lakonishok & Lee (2001)**: purchases informative, sales not, effect concentrated in small firms (1975–1995).
  Our data: no detectable effect in $300M–$10B; the $300M–$1B half is the only size slice with a positive
  mean, CI includes zero. Consistent with "small firms drive it" *and* with the effect being largely in
  micro-caps (< $300M), which our filter excluded on purpose (liquidity).
- **Cohen, Malloy & Pomorski (2012)**: ~82 bp/month (~10%/yr) value-weighted for *opportunistic* insiders,
  ~0 for routine ones (1986–2007). We did **not** apply the routine/opportunistic split (needs 3 prior years of each
  insider's history). Our 12m CI upper bound (+5.0%, or ≈ +7% with a generous survivorship add-on) is below
  ~10%/yr, so a naive "any cluster" rule does not capture a CMP-sized edge in 2021–2024. Possible reasons:
  dilution by routine buyers; decay after publication (signal is free and widely screened — OpenInsider,
  Form 4 bots); period-specific regime (mega-cap leadership, 2022 rate shock, regional-bank stress in 2023).

## 5. Caveats (read before using any number)
1. **Survivorship.** 221 of ~1,180 otherwise-eligible events (~19%) had no Yahoo history. SEC audit of the
   189 non-biotech ones: **162 were acquired** (merger proxy/tender filed after the event), **23 went bankrupt**
   (8-K item 1.03), 4 deregistered. None of the usable series ended mid-window (Yahoo simply drops delisted
   tickers), so the usable sample is survivors-only. Controls have the same bias (29% of the random pool missing).
2. **Bound.** If every missing acquired event earned +25% excess and every bankrupt −80% inside the window,
   the blended 12m excess would rise from 0.0% to about **+2.1%** — still small, and an upper-ish bound because
   controls also lose their acquired firms and many takeovers came > 12 months after the signal.
3. **Overlap / dependence.** Events cluster in time (e.g. 2022 sell-off, Mar-2023 bank stress). Month-clustered
   bootstrap handles part of this; it is not a full calendar-time factor regression (no FF5/momentum alpha here).
4. **Market cap** from cover-page shares × insider price; multi-class issuers understated; 669 events had no
   frame and were dropped (skews to larger, XBRL-compliant filers).
5. **Control draw sensitivity.** Re-running with a slightly different event set moved control-relative means by
   ~0.5–1 pp (e.g. 3m −1.6% → −1.0%) — noise level, conclusions unchanged.
6. **Window.** Four signal years, one regime. A null here is not proof the effect never exists; it is evidence
   the plain public rule was not worth paying for in this period.
7. **Costs** ignored (would make results worse, especially for $300M–$1B names).
8. Code P also includes privately negotiated purchases; the 180-day listing filter removes most IPO/PIPE cases
   but not all.

## 6. What this means for us (edge check)
- Public cluster screens are free and widely used → by our own rule ("public screens = no edge") the prior was
  weak; the data now agrees: **no standalone edge** in US $300M–$10B, 2021–2024.
- Useful role: a **research-queue trigger** (a reason to read the 10-K/proxy), not a buy signal. If we want to
  test further, pre-register *one* refined rule and test it out of sample, e.g.: CMP opportunistic-only
  (insider did not trade the same month in the prior 3 years) + buy ≥ 10% of the insider's existing holding +
  ≤ $1B mcap or banks; evaluate on signals 2017–2020 (build) and 2021–2024 (test).
- For India: SEBI PIT disclosures (Reg 7) could be tested the same way — lower coverage there might
  make the signal *more* informative; that is the more promising follow-up.

## 7. Reproduce
Scripts (standard library only): `/home/user/fein/tools/backtests/insider_clusters/`
`s1_download_extract.py` → `s2_clusters.py` → `s3_size_sector.py` → `s3b_control_pool.py` →
`s4_prices.py` (events, controls, renamed tickers) → `s5_analyze.py` → `s6_missing_audit.py`.
Raw data / outputs: `/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_insider/`
(`purchases.tsv`, `events_sized.tsv`, `results.json`, `results.txt`, `missing_audit.json`, `prices/`).
Scratch data is ephemeral; rerun s1–s6 (~1.5 h, mostly polite Yahoo pacing) to regenerate.

Sources: https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2021q1_form345.zip (quarterly series 2020q4-2025q1) ;
https://data.sec.gov/api/xbrl/frames/ ; https://data.sec.gov/submissions/ ;
https://query1.finance.yahoo.com/v8/finance/chart/ ; literature per memdb `insight:us-insider-buying-evidence`.
