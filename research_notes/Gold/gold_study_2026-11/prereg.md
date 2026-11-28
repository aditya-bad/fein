# Gold study 2026-11 — pre-registration

**Written 2026-11-28 09:30 UTC, BEFORE any study data was fetched or any number computed.** Changes after this point
are recorded as dated deviations at the bottom, never edited in place. Research, not SEBI-registered advice.

Roadmap fit: wealth-allocation defence layer (L52: fixed gold share, January rebalance, new money to the underweight
asset) + stage 5 (valuation context for gold, the defence asset) + stage 7 (dated, scored calls). Unlocks: a reusable
monthly gold monitor (`tools/gold/`), base rates for gold drawdowns that future allocation and scenario work can cite
instead of judgment, and a scored test of whether published bank forecasts carry information.

Supersedes (when finished): `research_notes/Gold/gold_state_2026-11-28.md` (quick, single-source first pass). The 5
existing `thesis:paper-call:GOLD:*` calls stay untouched; if this study's probabilities differ, new calls get `-v2` ids.

## Data (two sources per series; raw files saved with as_of under `data/`)
| Series | Primary | Second / cross-check |
|---|---|---|
| Gold USD, monthly history | World Bank pink sheet (LBMA-based monthly average, 1960→) | FRED LBMA series if still served; else Yahoo GC=F month-end (2000→) for overlap check |
| Gold USD, recent daily | Yahoo GC=F (COMEX front month) | a second spot quote (gold-api / other public page), and LBMA/WB monthly average |
| USD/INR | FRED EXINUS (monthly, 1973→) / DEXINUS (daily) | Yahoo INR=X; RBI/FBIL reference where scriptable |
| US real 10-yr yield | FRED DFII10 / FII10 (TIPS, 2003→) | pre-2003 proxy = FRED GS10 − CPI y/y (CPIAUCSL), stated as a proxy |
| Fed funds | FRED FEDFUNDS (monthly) | FRED DFEDTARU (target upper) for recent |
| Dollar | FRED DTWEXBGS (broad, 2006→) + Yahoo DX-Y.NYB (DXY) | — |
| Central-bank buying, ETF holdings | World Gold Council public pages only | news reports (marked secondary) |
| India domestic price | IBJA (public page) | computed USD × INR per 10 g |
No CAPTCHA/anti-bot bypass; failed sources are recorded as missing, never guessed.

## Definitions (monthly data)
- **History series:** World Bank monthly average gold price (USD/oz). Two start dates reported: **1968-04** (two-tier
  market; free price exists) and **1975-01** (US citizens may own gold; the market is broad). INR series = USD × EXINUS
  monthly (1973→; INR results start 1975-01).
- **Peak / drawdown episode:** running all-time high (ATH) of the monthly series. An episode starts at an ATH month and
  counts if the price later falls **≥20% below that ATH** before a new ATH. Depth = trough/peak − 1; fall duration =
  peak → trough months; **recovery = months from peak until the series first closes ≥ the old peak** (nominal). Open
  episodes are reported as open with duration so far. A 15% threshold is reported as a sensitivity only.
- **Real recovery** (sensitivity): same, deflated by US CPI.
- **Run-up (Q2):** ratio of peak to the minimum of the prior 36 months. "Big run-up" = ≥2.5× in ≤36 months. Also report
  the continuous relationship (run-up ratio vs depth and vs recovery months) across all episodes.
- **Fed regime (Q3):** at each month, 6-month change in FEDFUNDS: > +0.25pp = **hiking**, < −0.25pp = **cutting**, else
  **hold**. Real-yield level = DFII10 monthly average (2003→), proxy before (GS10 − CPI y/y). Real-yield change = 12-month
  change. For each episode: regime at the peak and during the fall; real-yield level and change over the fall; regime
  when recovery started (trough month).
- **Q4 cushion:** for each USD episode, INR return over the same peak→trough months, and the INR-series own episodes.
  Cushion = INR return − USD return (pp). Report how often INR depreciated during USD falls.
- **Q5 forecasts:** LBMA annual precious-metals forecast survey (published each January: consensus average-price
  forecast for the year) where the public pages give it; compare with actual annual average (World Bank). Benchmark =
  random walk (the December average before the forecast). Informative only if consensus mean absolute % error is lower
  than the random walk's in a majority of years AND on average. Bank year-end targets: list published 2025–26 targets with
  dates and sources and how they moved; no score unless ≥8 dated target/outcome pairs exist. "Buy zone below
  $3,600/$3,500" claim: find who said it, when, where; a "floor" counts as evidenced only by a dated, attributable flow
  number (e.g., WGC central-bank tonnes, ETF tonnes) at those prices, not by a commentator's sentence.

## Scenario probabilities (12m and 24m) — how they will be derived
1. **State today:** price % below ATH (month-end basis), run-up before the ATH, Fed regime, real-yield level.
2. **Analog months:** all historical month-ends (1975→, monthly average series) with gold **25–45% below its running ATH**
   within an open drawdown episode. For each, forward 12m and 24m USD return.
3. Three sets: (a) unconditional analogs; (b) analogs where the episode's run-up was ≥2.5× in ≤36 months (Q2);
   (c) analogs where the Fed regime at that month is hiking or real yield ≥ 2% (Q3).
4. **Buckets** for forward return from today's price: **best** > +25%, **base** −5% to +25%, **bad** −25% to −5%,
   **worst** < −25%. (12m and 24m use the same buckets.)
5. **Blend:** p = average of (b) and (c) bucket frequencies, each shrunk toward (a): p_x = (n_x·f_x + k·f_a)/(n_x + k)
   where n_x = number of **independent episodes** contributing to set x and k = 3. If a conditional set has < 2 episodes it
   gets weight 0 (use (a)). Then each bucket is floored at 5% (L36: don't zero tails) and renormalised to 100%.
6. Overlapping monthly windows are not independent; the effective sample is the number of episodes (likely 3–6). All
   probabilities will be stated as wide (±10–15pp) and labelled low-confidence.
7. Prices for each bucket = the bucket's median analog return applied to today's price.

## Calls rule
For each existing GOLD call, compute the study's probability for the same event (from the analog set used in step 5,
event-specific: touch/close thresholds converted to % from today; touch uses the analog path's monthly min/max as a
conservative proxy, noted). If |study − existing| ≥ 0.10, issue a NEW `-v2` call dated 2026-11-28 with the study's
probability; old calls untouched. Same resolution source (Yahoo GC=F daily close).

## Allocation tie (Q-rules)
Simulate the L52 rule (fixed 20% gold, January reset; and new-money-to-underweight SIP) through historical gold
drawdowns in INR (e.g., 2011–15) using the allocation-test data, reporting portfolio-level damage and how much gold the
rule bought. Rules, not predictions.

## Known caveats (stated before results)
- Gold has ~4–6 independent ≥20% drawdowns since 1968 → base rates are anecdotes with numbers; small-sample.
- Monthly averages understate intraday/closing extremes (peak and trough depth); recent-state numbers use daily data.
- Pre-2003 real yield is a proxy (backward-looking inflation).
- 1980 involved 20% nominal rates and a Volcker shock; 2011–15 involved QE taper and a strong dollar — regimes differ.
- Central-bank buying since 2022 is structurally new; no historical analog weights it.

## Deviations (appended 2026-11-28, after results; nothing above was edited)
1. FRED LBMA series GOLDPMGBD228NLBM returned 404 (discontinued). The World Bank workbook ends 2024-12, so 2025-01 → 2026-10
   come from the datahub.io WB/LBMA mirror (same lineage; cross-checked against Yahoo GC=F monthly averages, median +0.05%).
2. "Today's % below ATH" = latest GC=F close vs the monthly-average ATH (Feb-2026, $5,020) = −27.5%, so the analog band
   (25–45%, monthly-average basis) is applied like-for-like. Close-basis −31.6% is reported too.
3. Added, as sensitivities only (they do not set the calls): (a) episode-equal weighting of analogs (1980–2006 supplies
   147 of 224 analog months); (b) a daily-close adjustment for touch/record events (median monthly min close −2.6% vs
   average, max +2.8%).
4. Fed regime today by the pre-set rule is "hold" (FEDFUNDS 6-month change +0.24pp, just under +0.25); set (c) still
   applies through the real yield ≥ 2% branch.
5. Q5: 2021 LBMA figures excluded (the LBMA page is internally inconsistent); 5 full years scored.
