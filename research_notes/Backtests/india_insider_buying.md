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

*Everything below was written after the data run. The pre-registration above has not been edited.*

## Verdict (short)
**H1 not supported under the pre-registered decision rule. The result looks like a lottery ticket, not a reliable signal.**
351 usable events (2021–2024, ₹500–20,000 cr). Against 5 size-matched random NSE stocks on the same date, the mean
12-month excess was **+6.3%** (95% event-month bootstrap CI **−0.9% to +13.2%**). The **median was −6.9%** (CI −12.8% to −1.5%)
and the **hit rate 43.6%**. The CI includes zero, so the rule says "not supported". The point estimate passes the +5%
"practically relevant" bar with seed 11 but not robustly: seeds 12 and 13 give +5.6% and +4.1%, and both CIs include 0.
The positive mean comes entirely from a right tail. **Dropping the 10 best events turns it into −1.1%.** Most events lag
their controls. Promoter buying sorted the market toward 2021–24's multibaggers (Gallantt, Texmaco Rail, Apar,
Gravita, Titagarh, Jindal Saw…) slightly more often than chance. It did not make the typical pick beat a random
same-size stock.

Compared with the US test (insider_clusters_us.md: 12m 0.0%, CI −4.8 to +5.0), India is directionally more positive, with
the same "mean > 0 > median" shape. That fits the idea that the signal is less arbitraged in India. It is not proof.

## 1. Data and method (as run)
| Item | Choice / approximation |
|---|---|
| PIT source | NSE `corporates-pit` date-range queries, 7-day chunks, broadcast 2020-12-01 → 2025-01-31 (218 files, 0 failures). 92,026 unique rows after de-duplication on (symbol, name, from, to, qty, mode, type). Spot check: for VSSL and GANECOS, every row returned by the per-symbol query was also in the range pull. Monthly row counts fall over time (≈3.4k/mo in 2021 → ≈1.6k/mo in 2024), with regular dips in trading-window months (Jan/Apr/Jul/Oct). I did not establish whether the fall is a reporting change or a real one (see caveat 5). |
| Qualifying buys | `acqMode = Market Purchase`, `tdpTransactionType = Buy`, `secType = Equity Shares`, category ∈ {Promoters, Promoter Group} → promoter; {Director, Key Managerial Personnel} → KMP. Dropped: "Immediate relative" (969 rows; the field does not say whose relative), "Other"/"-", and every other mode (Market Sale 40.7k, ESOP 18.7k, pledge rows 9.2k, off-market 2.4k, gift, inter-se, preferential, rights, scheme…). → **9,831 buys** (8,785 promoter, 1,046 KMP). Median trade → broadcast lag is 2 days (90th pct 5). |
| Event | Pre-registered 30-day rolling rule, ≥ ₹1 cr or ≥ 0.25% of equity. One per company per 365 days. Event = broadcast date. → **684 events** (619 promoter-only, 43 KMP-only, 22 mixed) in 2021–2024. |
| Shares outstanding | Not available point-in-time from a clean source. **Approximation:** implied total shares = `afterAcqSharesNo / afterAcqSharesPer × 100`, using PIT rows with holding ≥ 1% (rounding error ≤ 0.5%). Event mcap = implied shares × insider VWAP. Both come from the same disclosure, so they are unadjusted and consistent. |
| Control mcap | Implied shares (PIT row nearest in time, ≤ 365 d) × k × Yahoo close on the event date. k = unadjusted PIT market-trade price ÷ Yahoo close near the share row's date, which puts shares on Yahoo's adjusted basis. **Yahoo's split-event list is incomplete for Indian bonuses** (e.g. 360ONE 2023 shows 2:1, but prices are adjusted 4:1), so split events are not used. Universe = every NSE symbol with any PIT filing in the window (1,705 symbols; 80 have no Yahoo history). |
| Prices | Yahoo v8 `.NS`, adjusted close, ≥ 1.1 s per call. A long browser User-Agent got HTTP 429; `Mozilla/5.0` works. Benchmark ^CRSLDX (NIFTY 500 price index, so no dividends; used for context only). |
| Entry / horizons | First trading day strictly after the broadcast date; 63/126/252 trading days. |
| Controls | 5 random (seed 11) from the universe. mcap ×0.5–×2 of the event firm, listed ≥ 180 d, no own event within ±365 d, same entry day, no data-error jump (daily adj move outside −50%/+100%) in the 12m window. 351/351 events got 5 controls. |
| Stats | Mean, 1/99 winsorised mean, median, hit rate, naive t, 95% bootstrap CI resampling event-months (2,000). |

Funnel: 684 events → 241 outside ₹500–20,000 cr · 40 no share count · 12 no mcap estimate · 18 listed < 180 d ·
4 failed the price-consistency check · 9 in band but no Yahoo history (survivorship, §5) · 9 no Yahoo history and size unknown
→ **351 usable** (321 promoter-only, 21 KMP-only, 9 mixed). Median event mcap ₹2,378 cr; median buy ₹2.2 cr.
The identity check (VWAP vs Yahoo × k) is weak because k is estimated from nearby trades that partly overlap the event.
It catches only gross symbol or price mismatches.

## 2. Primary result (excess vs 5 matched controls, n = 351)
| Horizon | Mean [95% CI] | Winsorised mean | Median [95% CI] | Hit | naive t |
|---|---|---|---|---|---|
| 3m | −1.1% [−3.8, +1.6] | −1.4% | −3.1% [−5.4, +0.6] | 44.7% | −0.80 |
| 6m | +1.0% [−3.2, +5.4] | +0.7% | −4.5% [−8.4, +0.5] | 45.3% | +0.44 |
| **12m (primary)** | **+6.3% [−0.9, +13.2]** | +5.9% | **−6.9% [−12.8, −1.5]** | **43.6%** | +1.53 |

Context (not tests): raw 12m event return +38.8% mean / +18.3% median. Versus NIFTY 500 the events show +22.9%, but the
**random size-matched controls beat NIFTY 500 by +16.6%** too (CI +9.1 to +23.7). Almost all of the "beats the index" figure
is the 2021–24 small/mid-cap boom, not the signal. **Anyone quoting promoter-buying returns vs Nifty is mostly quoting
the size effect.**

Robustness (12m mean [CI], median, hit):
| Variant | Mean [CI] | Median | Hit |
|---|---|---|---|
| seed 11 (primary) | +6.3% [−0.9, +13.2] | −6.9% | 43.6% |
| seed 12 | +5.6% [−1.6, +13.2] | −4.0% | 46.2% |
| seed 13 | +4.1% [−3.9, +11.6] | −7.5% | 43.6% |
| controls not jump-screened | +6.7% [−0.4, +13.6] | −6.9% | 43.9% |
| events with price-jump flag dropped (3) | +7.2% [+0.1, +13.7] | −6.5% | 44.0% |
| drop top 5 / top 10 events | +2.2% / −1.1% | — | — |

The CI excludes zero in only one variant, a post-hoc exclusion. It is not counted.

## 3. Pre-registered secondary splits (12m excess vs controls)
| Split | n | 12m mean [CI] | median | hit | 6m mean |
|---|---|---|---|---|---|
| Promoter-only | 321 | +7.1% [−0.2, +14.5] | −6.4% | 43.9% | +1.5% |
| KMP-only | 21 | −4.6% [−29.3, +19.4] | −16.7% | 33.3% | −5.3% |
| (mixed, 9 events) | 9 | +3.1% [−28.5, +36.4] | +10.4% | 55.6% | −1.2% |
| Small ₹500–2,000 cr | 149 | +10.7% [−3.3, +23.7] | −8.3% | 44.3% | +4.8% |
| Large ₹2,000–20,000 cr | 202 | +3.1% [−6.6, +12.1] | −5.2% | 43.1% | −1.7% |

Promoter-only is just the full sample minus 30 events. **KMP-only is far too small to test** (21 events; Indian KMPs rarely
buy ≥ ₹1 cr on market). Small > large in direction, as in the US test and the literature, but CIs overlap heavily.
None of these splits is significant.

## 4. Exploratory (NOT pre-registered; hypotheses only)
| Subset | n | 12m mean [CI] | median | hit |
|---|---|---|---|---|
| Buy ≥ ₹5 cr | 94 | −0.8% [−14.3, +15.0] | −7.6% | 42.6% |
| Buy ≥ 1% of equity | 27 | +1.6% [−18.6, +26.4] | −2.0% | 44.4% |
| ≥ 2 distinct buyers | 59 | −1.8% [−17.4, +15.6] | −7.9% | 44.1% |
| Signals 2021 | 102 | +9.9% [−0.3, +22.8] | −6.0% | 45.1% |
| Signals 2022 | 89 | +1.6% [−10.4, +12.9] | −12.4% | 39.3% |
| Signals 2023 | 83 | +13.4% [−0.3, +33.1] | −2.0% | 48.2% |
| Signals 2024 | 77 | −0.7% [−26.0, +15.8] | −8.3% | 41.6% |

The intuitive "stronger" versions (bigger buys, ≥ 1% stake, several buyers) were *not* better. The US test showed the
same pattern (≥ 3 insiders, CEO/CFO were worse).

## 5. Survivorship audit
- Universe: 80 of 1,705 PIT-filing symbols (4.7%) have no Yahoo history, far fewer than the US test's ~19%, because NSE
  reports *current* symbols. Events: 17 symbols missing, 9 of them in the ₹500–20,000 cr band (mcap estimated from PIT):
  DHANI (×2, 2021-03 and 2022-03), JSLHISAR (merged into JSL 2023), MANGCHEFER, SUPPETRO, SHRIRAMCIT (merged into
  Shriram Finance Dec-2022), CIGNITITEC (taken over by Coforge), SANGHIIND (acquired, Ambuja/Adani), ISMTLTD
  (Kirloskar Ferrous merger). Classified from NSE announcement keywords (`missing_audit.json`). The outcomes were not
  priced.
- Bound: 9 missing vs 351 usable. If every missing event earned ±50% excess, the 12m mean would move by about ±1.3 pp.
  The verdict does not change. Direction is unclear: Dhani was a large loser in 2021–22; JSL Hisar was a large winner.
- No usable series ends inside its window (0 truncated), so the usable sample is survivors-only. The controls carry the
  same bias.

## 6. Literature (memdb + web)
- memdb `insight:ownership-disclosure-early-signals` (single-source) treats PIT buying, especially by several KMPs, as an
  informative early signal. **This test does not support that as a return predictor.** KMP buying ≥ ₹1 cr is rare (21 usable
  events) and "≥ 2 buyers" did worse.
- Deuskar, Khatri & Sunder, *Insiders' Other Trades* (ISB/Arizona, NSE-NYU working paper, Apr-2019; BSE 2009–2011,
  SEBI PIT 1992 regime): insiders' own-stock **purchases earn ~3% abnormal over 3 months and ~5.9% over 6 months**, and
  sales earn nothing. Insiders at better-governed firms profit less in their own stock.
  https://archives.nseindia.com/research/content/1718_BS1.pdf (read). Our 3m/6m means are −1.1%/+1.0%, well below those
  figures. Possible reasons: post-2015 PIT regime, the ≥ ₹1 cr filter (larger, more visible promoters), matched-control
  benchmark vs factor models, and publication / free screening.
- IIM Bangalore paper on the 2015 PIT regulations (search snippet only; full text returned 403): own-stock trade
  likelihood and abnormal returns fall after controlling for insider fixed effects, i.e. the 2015 rules appear to have
  worked. https://www.iimb.ac.in/sites/default/files/inline-files/insider-trading-restrictions-informed-trading.pdf. This is
  consistent with a weaker post-2015 signal. Single-source and unread.
- NSE-IGIDR working paper on block trades 2005–15 (search snippet): 3-day CARs positive for insider/promoter block
  purchases. That is a short-window announcement effect and does not contradict a null at 3–12 months.
  https://nsearchives.nseindia.com/research/content/NSE-IGIDR_CG_RPaper_2015-16_WP4.pdf
- US analogue: Lakonishok & Lee (2001), Cohen–Malloy–Pomorski (2012) via memdb `insight:us-insider-buying-evidence`.
  Effects concentrate in small firms and opportunistic insiders.

## 7. Caveats
1. **Market cap is approximate.** It is built from implied shares in PIT disclosures (holding ≥ 1%) plus a price-basis
   factor. Error is likely ±5–10%, which is fine for ×0.5–×2 matching and for the ₹500–20,000 cr band edges. 52 events were
   lost for lack of a share count or mcap.
2. **Control universe** = companies with any PIT filing in 2020-12 → 2025-01 (≈ all actively traded NSE names). It is not a
   point-in-time NSE equity list. Firms listed after the window (and so absent) cannot be drawn for early dates, a small
   bias.
3. **Skew.** Mean +6%, median −7%. The rule's economic value depends on holding the whole basket, so that the few 3–5×
   winners are captured. A concentrated version (5–10 names) would usually lag.
4. **One regime.** 2021–24 was the strongest Indian small/mid-cap run in a decade. Promoter buyers in metals, capital goods
   and rail rode that wave; part of the +6% may be sector or momentum exposure that size-matching does not remove. No
   sector-matched control was run.
5. **Coverage drift.** NSE PIT row counts halve from 2021 to 2024. If some promoter purchases were disclosed only on BSE
   or under different modes, the event set is incomplete. The magnitude of the drift was not verified.
6. **Costs and impact** are ignored (₹500–2,000 cr names: 0.5–1% round trip plus impact). They would cut the small-cap mean.
7. Index benchmark is NIFTY 500 *price* (no dividends), so the index comparison flatters events by about 1.2%/yr. It is
   context only.

## 8. What this means for us (edge check)
- The pre-registered public rule is **not a proven edge**. The honest read is a *possible* weak right-tail tilt
  (mean +4 to +7%/yr in every variant, CI touching 0, median negative).
- Use: a **research-queue trigger**. Promoter open-market buying ≥ ₹1 cr in a ₹500–2,000 cr company is a reason to read the
  filings (pledge status, capex cycle, order book). It is not a buy signal. This matches L14.
- If tested again, pre-register *one* refinement and test it out of sample (e.g. signals 2017–2020 or 2025–26): promoter-only,
  ₹500–2,000 cr, **no pledge outstanding**, first promoter buy in ≥ 3 years (CMP-style "opportunistic"), plus a sector-matched
  control. Primary metric unchanged.

## 9. Reproduce
Scripts (standard library only): `/home/user/fein/tools/backtests/india_insider/`. Run them in order:
1. `s1_fetch_pit.py OUT` (~8 min)
2. `s2_events.py OUT`
3. `s3_prices.py OUT [symbols]` (~40 min)
4. `s4_analyze.py OUT [--seed N --no-ctl-jump-screen --tag T]`
5. `s5_missing_audit.py OUT`

OUT = `/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_india_insider/` holds `pit/`,
`prices/`, `buys.tsv`, `events.tsv`, `results*.json/txt` and `missing_audit.json`. Scratch data is ephemeral.

Sources: https://www.nseindia.in/api/corporates-pit?index=equities&from_date=…&to_date=… ;
https://query1.finance.yahoo.com/v8/finance/chart/<SYM>.NS ; https://query1.finance.yahoo.com/v8/finance/chart/%5ECRSLDX ;
papers as cited in §6.
