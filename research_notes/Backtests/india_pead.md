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

- **2026-11-21 D1 (data, before any returns were computed): standalone, not consolidated.** NSE's quarterly
  consolidated results were optional before FY2020 for most firms, so a consolidated series would not reach
  back to 2015 for the SUE denominator. All EPS/revenue are **standalone** for every company (one basis
  throughout, as the pre-registration requires).
- **D2 (data): EPS split/bonus adjustment.** Reported EPS is divided by the product of Yahoo split/bonus
  ratios dated *after* that quarter's filing date (Ind AS 33 restates EPS for a split between quarter-end and
  filing). Revenue SUE needs no adjustment.
- **D3 (data): returns are price returns** (Yahoo `close`, split-adjusted, not dividend-adjusted) for events
  and controls alike; dividends (~1%/yr) are ignored on both sides.
- **D4 (data): sample, not full universe.** Fetching ~40 quarterly filings per company at polite rates takes
  ~15 s/company, so the test uses the first N symbols of a seeded shuffle (seed 20261121) of all 1,791 NSE
  EQ/BE equities listed on or before 2023-06-30 in the *current* NSE equity list (survivors only). Symbols are
  dropped if their mcap never touched ₹400–60,000 cr in 2018–2025 (pre-filter); event-level ₹500–50,000 cr
  filter as pre-registered.
- **D5 (data): event date** = earliest of the filing's broadcast date, filing date and the date stamped in its
  XBRL filename (NSE's `broadCastDate` sometimes shows a later revision). Filings > 150 days after quarter-end
  are dropped (these are mostly prior-year comparatives re-filed under Ind AS, not real announcements).
  2025 results come from NSE's new "Integrated Filing – Financials" feed (SEBI regime from 2025).
- **D6 (data): SUE needs ≥ 4 prior seasonal changes**, so the first eligible events of 2018 rely on EPS back to
  2015; NSE's result feed for some companies starts later (e.g. only 2022+), so those firms enter later.
- **D7 (2026-11-21, stopping rule fixed before any return statistic was computed):** the sample is
  shuffled-list positions **0–349 and 500–849** (700 symbols; two fetch processes ran on the two slices).
  Data collection stops when both slices are done; no T−B number was looked at before that. A usage-limit
  pause interrupted the fetch at ~290 companies; it was resumed with this rule written down first.
- **D8 (2026-11-21, before analysis): event date refined with exchange announcements.** A spot-check of 8
  random events against NSE corporate announcements found the results-feed date was **one day late in 4/8**
  (late-evening filings get next-day XBRL/filing stamps) and one (YESBANK Sep-2020) dated to a revision weeks
  later. Fix: event = earliest "Financial Result Updates" / results "Outcome of Board Meeting" announcement
  timestamp after quarter-end and not after the feed date; else the feed date. Entry rule unchanged
  (close of first trading day strictly after the event date). The old dating was conservative (late), the
  new one is what the pre-registration meant ("results filing/broadcast timestamp on NSE").

---

# RESULTS — written 2026-11-21 AFTER the run (everything above this line is unchanged pre-registration + deviation log)

## Verdict (short)
**H1 supported in both periods. H2 supported gross but misses the pre-committed 1%-cost rule by 0.06 pp. H3 not supported.
Under decision rule 2 the long-only "edge candidate" label is therefore NOT awarded (borderline). The anomaly itself
is real out of sample.**

- **Top-minus-bottom SUE quintile, 63 trading days after entry (next-day close):** train 2018–21 **+4.84%**
  (95% quarter-bootstrap CI +2.61 to +7.07, t = 4.06, 16 quarters); **test 2022–25 +4.24% (CI +2.20 to +6.18, t = 3.99)**.
  It passes Harvey–Liu–Zhu t > 3 in *both* periods, has the same sign, and survives out of sample.
- **Long-only (top quintile vs size-matched controls, 63d), test:** **+2.36% gross** (CI +0.94 to +3.67, t = 3.23);
  net of 0.5% round trip +1.86% (CI +0.44 to +3.17); **net of 1.0% +1.36% (CI −0.06 to +2.67) → fails rule 2 by a hair.**
  At 126 days it clears the 1% hurdle (+2.69% net, CI +0.61 to +4.73), but 126d was not the primary horizon, so this
  is not used to rescue the verdict.
- **Most of the drift is on the short side.** The bottom quintile lags its controls by −2.70% (train) / −2.13% (test) at
  63d (t ≈ −4.4 / −4.8). The quintile ladder is monotone in both periods (test Q1…Q5: −2.13, −0.80, +0.17, +1.02, +2.36%).
- **H3 (bigger drift in the smallest tertile) is not supported.** Small-minus-large tertile T−B at 63d: train +3.35%
  (CI −3.1 to +10.5), test −0.44% (CI −4.8 to +3.8). Exploratory: the *middle* tertile (median ₹2,800–3,600 cr) had the
  strongest drift in both periods (63d T−B +6.7% train, +5.9% test, t = 3.1 / 4.6).
- **The announcement reaction confirms the dating and SUE work.** The top-minus-bottom return from the close before the
  filing to the entry close was +3.75% (train, t = 9.3) and +4.95% (test, t = 18). The drift is *on top of* that day-0/1
  move, which our entry rule deliberately gives up.

## 1. Data and method (as run)
- **Sample** (D4, D7): shuffled-list positions 0–349 and 500–849 (seed 20261121) of 1,791 current NSE EQ/BE equities
  listed by 2023-06-30 → 700 symbols fetched; 119 never touched ₹400–60,000 cr (pre-filter), 1 had no quarterly filings,
  **580 usable companies**. This is a documented random sample, not the full universe.
- **Event funnel:** 15,977 quarterly results dated 2018–2025 → −19 filed > 150 days after quarter-end, −1,804 without
  enough history for SUE (EPS and revenue), −9 with < 250 days of prices, −4,119 outside ₹500–50,000 cr at entry →
  **10,026 events** (train 4,336 from 363 companies; test 5,690 from 496). EPS-SUE available for 9,782; quintile analysis
  used cross-sections with ≥ 25 events (train 4,092, test 5,690 events; 16 + 16 fiscal quarters).
- Event date source (D8): exchange announcement earlier than the feed date 4,312; same day 5,197; feed date only 517.
  Results figures: XBRL 9,466, NSE detail API 560 (37 companies had a lakh/rupee unit mismatch rescaled by implied
  shares).
- Events: median mcap ₹3,197 cr (IQR 1,352–9,443). Size-matched controls per event: median 116 stocks (min 19).
- Ranking: SUE quintiles within each fiscal quarter of the result; equal-weight; inference across fiscal quarters.
- Scripts: `tools/backtests/india_pead/s1_universe.py` → `s2_prices.py` → `s3_results.py` → `s3b_announce.py` →
  `s4_events.py` → `s5_analyze.py` (pre-registered) → `s6_robust.py` (exploratory, written after the run).

## 2. Primary results (EPS SUE quintiles; entry = close of first trading day after the filing; mean of quarterly values; 95% CI = 5,000 bootstrap draws over quarters)

| Horizon | Period | T−B | t | Top vs controls | Bottom vs controls | All events vs controls |
|---|---|---|---|---|---|---|
| 21d | train | +1.31% [−0.18, +2.76] | 1.69 | −0.26% [−1.48, +0.86] | −1.45% | −0.50% |
| 21d | **test** | **+1.73% [+0.86, +2.54]** | 3.89 | +1.18% [+0.45, +1.88] | −0.77% | −0.11% |
| **63d** | train | **+4.84% [+2.61, +7.07]** | 4.06 | +1.81% [+0.34, +3.56] | −2.70% | −0.26% |
| **63d** | **test** | **+4.24% [+2.20, +6.18]** | **3.99** | **+2.36% [+0.94, +3.67]** (t 3.23) | −2.13% | +0.12% |
| 126d | train | +8.93% [+4.87, +13.07] | 4.07 | +3.50% [+0.09, +7.07] | −4.95% | −0.35% |
| 126d | **test** | **+6.18% [+2.93, +9.68]** | 3.47 | +3.69% [+1.61, +5.73] | −3.07% | +0.22% |

"All events vs controls" ≈ 0 in every row, so the size-matched controls are well calibrated. 126d windows overlap the next
quarter's cross-section, so the 126d t-stats are a little flattering. Split into alternate quarters (no overlap), test 126d T−B
is +7.2% (t 3.4, 8 q) and +5.1% (t 1.7, 8 q).

**Long-only, net of costs (top quintile minus controls, test):**

| Horizon | Gross | Net 0.5% | Net 1.0% |
|---|---|---|---|
| 21d | +1.18% | +0.68% [−0.05, +1.38] | +0.18% [−0.55, +0.88] |
| 63d (primary) | +2.36% | +1.86% [+0.44, +3.17] | **+1.36% [−0.06, +2.67]** |
| 126d | +3.69% | +3.19% [+1.11, +5.23] | +2.69% [+0.61, +4.73] |

The T−B long-short pays two round trips (−1% to −2%) and needs ~3 months of cash-equity shorting, which is not practical for
retail in India (pre-registration rule 4). The gross T−B (+4.2%) still exceeds two 1% round trips.

**Mcap tertiles (63d T−B):** train small +5.13% (t 1.8) / mid +6.73% (t 3.1) / large +1.79% (t 1.4); test small +2.35%
(t 1.2) / mid +5.90% (t 4.6) / large +2.79% (t 1.75). Small-minus-large: train +3.35% [−3.1, +10.5], test −0.44%
[−4.8, +3.8] → **H3 not supported.**

## 3. Secondary / exploratory (hypotheses only)
- **Deciles** (EPS SUE): test 63d T−B +3.59% (t 2.8); top decile vs controls +2.16%. Not sharper than quintiles.
- **Revenue SUE** is weaker: test 63d T−B +2.06% (CI −0.10 to +4.08, t 1.9); its announcement reaction is about half of EPS's.
  The market drifts on profits, not sales surprises.
- **Next-day OPEN entry:** test 63d T−B +3.77% (t 3.6), top vs controls +1.55% (t 1.97). Open-entry returns include the
  entry-day move, and all events lag controls by −0.6% on this basis (a day-1 reversal), so close entry is the cleaner rule.
- **Skew.** Event-level, test, 63d: top-quintile *mean* excess +2.2% but *median* −1.0%, hit rate 47%. That median is
  mechanical in part: each stock is compared with the equal-weight mean of ~116 stocks, and the median of *all* events is
  −2.6% (hit 43%). Relative to that, the top quintile is +1.6 pp better at the median. Per-quarter *median* T−B is still
  +3.2% (test, t 2.6), and 1%/99% winsorised T−B is +4.1% (t 4.5). **The drift is broad-based, not three outliers.**
- **Basket size (test, 63d, random draws from each quarter's top quintile, 2,000 trials):** 10 names → 4-year average
  excess p5 −0.45% / median +2.34% / p95 +5.07%, below the 1% cost line 21% of the time; 15 names → p5 +0.33%, 14%;
  30 names → p5 +1.13%, 3%. You need ~30 names a quarter to collect the average reliably.
- **Mcap < ₹1,000 cr vs ≥ ₹1,000 cr (test):** top vs controls +0.36% (t 0.2) vs **+2.74% (t 3.9)**. In the test period the
  long-only effect lives in ₹1,000–50,000 cr, not in the smallest and least liquid names (train was the reverse: +4.2% vs
  +1.3%).
- **Top quintile with a positive announcement-window return** (test): +3.32% vs controls (t 4.0). With a non-positive
  reaction: +1.16% (t 1.05). This is a candidate "confirmed beat" filter for a future pre-registered test.
- **By year (63d T−B):** 2018 +2.3%, 2019 +6.9%, 2020 +7.6%, 2021 +2.5%, 2022 +3.5%, 2023 +7.9%, 2024 +4.6%, **2025 +0.9%**.
  Test quarters Dec-24 → Jun-25 were roughly 0 (−0.1, −1.9, +0.8%) and Sep-25 rebounded to +4.6%. That could be decay or
  noise. Watch it, and re-run with 2026 data.
- Per-quarter test T−B was positive in 13 of 16 quarters (negative: quarters ended Mar-22 −5.4%, Dec-24 −0.1%, Mar-25 −1.9%;
  see `india_pead_outputs/robust.json`). Train: 14 of 16 positive.

## 4. Survivorship audit
- The sample comes from the *current* NSE list, so firms delisted before Nov-2026 are absent. Among the companies in it,
  no usable price series ends early (the fetch required ≥ 300 days and survival to today).
- **Size of the hole:** 1,508 unique companies filed Q3 FY19 results on NSE (Jan–Feb 2019; corporates-financial-results feed).
  **253 (16.8%) are no longer in the current equity list by symbol or ISIN.** A sample of the names shows a mix of failures
  and insolvencies (Punj Lloyd, Reliance Naval, Future Retail/Consumer, Lakshmi Vilas Bank, Ballarpur, SREI Infra, Naga
  Fertilisers) and mergers or delistings at a premium (Syndicate/Dena/Corporation Bank, Bharat Financial, Equitas Holdings, JMC
  Projects, JB Chemicals, GSPL). Many of the failures were below ₹500 cr when they died.
- **Direction of the bias.** Failures cluster in bad-earnings, bad-return firm-quarters, i.e., the *bottom* SUE quintile. Missing
  them makes the bottom quintile look better than it was, so **T−B is, if anything, understated**. For top-vs-controls both
  sides are survivors. The bias roughly cancels, unless delisted firms were disproportionately top-SUE with collapsing prices.
  That is implausible, and mergers (the other half) usually exit at a premium.
- **Rough bound (adverse):** suppose the missing firms are ~8% of event firm-quarters, spread evenly across SUE quintiles,
  with −20% 63d returns, and they are missing only on the event side (the controls do not include them either way). Then
  top-vs-controls falls ~1.8 pp, to ~+0.6% gross. A realistic mix (failures mostly bottom, mergers spread
  out) moves the long-only result by < ±0.5 pp.

## 5. Caveats
1. **Standalone EPS** (D1). For holding-company and group structures this misses subsidiaries. A consolidated re-test from
   FY2020 onward is a natural follow-up.
2. **Price returns** (D3), dividends ignored on both sides. Equal-weighted; no capacity or impact model. ₹500–1,000 cr names can
   cost well over 1% round trip at size.
3. **Sample, not universe:** 580 of ~1,800 companies, so ~50–85 top-quintile names per quarter. A full-universe run would have
   ~2.5× more names per quarter and the same expected effect.
4. **Only 16 quarters per period.** The bootstrap CIs are honest but wide, and one bad quarter (e.g., Mar-2022 −5.4%) moves the
   mean by ~0.6 pp.
5. **Decision-rule edge case:** the long-only rule fails by 0.06 pp on the CI. We report that literally and do not "round up".
6. **Everything in §3 was found after looking at the data.** That includes the mid-tertile strength, the ≥ ₹1,000 cr long-only
   effect, the confirmed-reaction filter and 126d clearing costs. Each needs its own pre-registered test before it is believed.

## 6. What this means for us (edge check)
- PEAD is **public and well known**, so the edge is not the idea. Our edge is that in India it is still **operationally
  expensive to compute** (XBRL/PDF results, scattered dates, standalone vs consolidated, unit errors) and few retail investors
  do it systematically. The anomaly survives out of sample at t ≈ 4, unlike the US large/mid-cap market (Martineau 2022).
- **Practical long-only use (hypothesis-grade, not a trading system):**
  1. **Avoid or exit after a big negative SUE.** This is the most robust leg (−2.1% to −2.7%/quarter vs controls, t ≈ −4.5 in
     both periods), it costs nothing to apply, and it needs no shorting.
  2. **Tilt the research queue toward top-SUE names**, ideally ₹1,000–50,000 cr with a positive announcement reaction, and hold
     ~3–6 months. Expect roughly +2% per quarter vs same-size stocks before costs, and a skewed distribution (most single
     names lag; the basket wins). You need ~30 names to collect it reliably.
- It is **not a multibagger engine.** It is a quarterly-earnings timing and filtering layer that can sit on top of
  fundamental research (base rate: top-SUE stocks beat same-size peers ~47% of the time individually).
- Next tests (pre-register first): (a) consolidated EPS from FY2020; (b) the full universe; (c) the confirmed-reaction filter;
  (d) the 2026 quarters as fresh out-of-sample data, given the weak 2025 H1.

## 7. Reproduce
OUT = `/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_pead/` (ephemeral) holds
`EQUITY_L.csv`, `sample.txt`, `prices/` (Yahoo v8 chart JSON), `results/` (per-company quarterly results), `ann/` (NSE
announcement timestamps), `events.tsv`, `surv_q3fy19.json`. Durable copies of the outputs (`events.tsv`, `s4_funnel.json`,
`results.json`, `s5_out.txt`, `robust.json`, `s6_out.txt`) are in `research_notes/Backtests/india_pead_outputs/`. Run the scripts in `/home/user/fein/tools/backtests/india_pead/` in order, each with OUT as the argument
(s3 ≈ 15 s/company; s3b ≈ 1.5 s/company; s4 ≈ 35 s; s5 ≈ 6 s; s6 ≈ 60 s).
Sources: https://www.nseindia.com/api/corporates-financial-results ; …/api/integrated-filing-results ;
…/api/corporate-announcements ; nsearchives.nseindia.com XBRL ; https://query1.finance.yahoo.com/v8/finance/chart/<SYM>.NS.
