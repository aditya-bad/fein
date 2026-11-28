# Gold study, November 2026: how bad gold falls get, what ends them, and what our rule does about it

Stage fit: the **wealth-allocation defence layer** (L52: fixed gold share, January rebalance, new money to the underweight
asset), **stage 5** (valuation context for the defence asset) and **stage 7** (dated, scored calls). It unlocks drawdown
base rates that later scenario work can cite instead of judgment, a monthly monitor (`tools/gold/`), and a scored check of
bank forecasts. The method was pre-registered in [`prereg.md`](prereg.md), written at 09:30 UTC on 28-Nov-2026 before any
data was fetched. All numbers come from `results.json` and the raw files are in `data/`.
This supersedes `research_notes/Gold/gold_state_2026-11-28.md`. Research, not SEBI-registered advice.

## Plain-language summary

- **Where gold is now.** It closed at **$3,640 on 27-Nov-2026**, which is **32% below its best close** ($5,318, 29-Jan-2026)
  and 35% below its intraday record (~$5,590). It is down 10% over 1 month, 20% over 3 months and 13% over 1 year. In
  rupees the fall is about the same, −31% from the January peak, because the rupee has strengthened about 3% since
  August. The rupee has not cushioned this fall.
- **How bad gold falls have been before.** Since 1968 the monthly-average gold price has fallen 20% or more from a record
  5 times. The median fall was −39%, and the median wait to get back to the old peak was 3.5 years. The worst fall was
  1980–99: −62%, and **26 years** to regain the peak in dollars. The most recent, 2011–15, fell −39% and took 9 years.
  Today's fall on the same monthly-average basis is −27.5%. If it reaches the median depth, that is about −16% more from
  here (~$3,060).
- **What ends a gold bear market.** Real interest rates do. Every past fall happened while US inflation-adjusted yields
  rose, and every recovery began with them falling. Whether the Fed is "hiking" or "cutting" adds nothing beyond that.
  Today the 10-year real yield is **2.79%**. When it has been above 2%, gold's next 12 months were a coin flip, with a
  median return of about 0%.
- **What the analogs say for the next year.** Roughly half the time gold moved within −5% to +25%. About a third of the
  time it fell another 5–25%. Big rebounds above +25% happened ~10% of the time, and further crashes worse than −25%
  happened ~5%. Over 2 years both tails get fatter. How wide depends on whether the long 1980s bear is the template: big
  rebounds come out at 23% if it is (each month counted) and 46% if it is not (each episode counted equally).
- **Big run-ups led to bigger falls, but the evidence is weak.** The three run-ups of 2.5× or more in 3 years fell a
  median −40%. The two smaller ones fell −21% and −39%. Five episodes are too few to rest a conclusion on.
- **Bank forecasts and "buy zones."** The LBMA analyst consensus beat "no change" in all 5 full years we could check, but
  only narrowly: average error 10% vs 12.5%. It was 12–21% too low in the three big up-years. Every bank's end-2026
  target set this spring ($4,500–5,500) is now 24–51% above the price. **No fund house could be found saying it is
  "accumulating below $3,600/$3,500".** The phrase comes from technical commentary. The central-bank buying (321 t in Q3)
  happened at $4,000–4,700, not at today's price. No floor is evidenced.
- **Rupee and India.** In 91% of past 12-month periods when dollar gold fell, rupee gold did better, by a median 7.5
  percentage points. Rupee gold was still negative 59% of the time, so the rupee cushions a fall but does not remove it.
  Indian prices also carry the **15% import duty in force since 13-May-2026**. That duty explains the "16% gap" we could
  not explain last week: IBJA ₹126,299/10 g vs ₹108,181 world price. If the duty is cut back to 6%, domestic gold falls
  ~8% overnight.
- **What we do: rules, not predictions.** Keep gold at its fixed share (20%). Rebalance only in January. Send new money to
  whichever asset is most below target. The rule already sold gold near the top: in Jan-2026 gold had drifted to 29% of
  the portfolio, and the reset moved 9% of the portfolio out of it. If gold stays here, the Jan-2027 reset will buy back
  about 4% of the portfolio. A further 16% fall would cost a 70/20/10 portfolio about 3%, and a 1980-style collapse about
  10%. That is the insurance premium, and it is survivable.
- **Our earlier calls were too optimistic about a quick rebound.** The study puts P(≥$4,000 by Jun-2027) at **0.14** (we
  said 0.35) and P(≥$4,500 at end-2027) at **0.12** (we said 0.30). It also puts P(close ≤$3,200 before Jun-2027) at
  0.15, or ~0.27 after correcting for monthly averages, against our 0.35. Three new -v2 calls are filed below. The old
  calls stay as they were.

## Data and source checks
| Series | Source 1 | Source 2 | Agreement |
|---|---|---|---|
| Gold monthly history | World Bank pink sheet (1960–2024-12; the WB file has not been updated since Dec-2024) | datahub.io mirror (WB/LBMA monthly, to 2026-10) | identical lineage (max diff 1.3% over 681 months). **Not independent before 2000** |
| Gold monthly 2001–2026 | WB/datahub | Yahoo GC=F monthly average of daily closes | median +0.05%, p5–p95 −0.2% to +0.7% (310 months) |
| Latest price | Yahoo GC=F close **$3,639.6** (27-Nov) | gold-api spot **$3,650** (28-Nov 09:30 UTC) | 0.3% |
| Record | GC=F best close $5,318.4 and intraday $5,586.2 (29-Jan-2026) | spot $5,589 (CBS/Nasdaq, 28-Jan) / $5,595 (Nation Thailand, 29-Jan); Feb future $5,626.8 (Reuters via Kitco) | intraday ~$5,590 ± $40, depending on contract |
| USD/INR | Yahoo 92.45 (27-Nov) | FBIL 92.49 (25-Nov, RBI); FRED DEXINUS 92.67 (20-Nov) | <0.3% |
| US 10-yr real yield | Treasury real curve **2.79%** (27-Nov) | FRED DFII10 2.73% (25-Nov; Treasury same day 2.73) | match |
| Fed funds | FRED DFEDTARU 4.00% upper (hike on 17-Sep-2026; cuts Sep/Oct/Dec-2025) | FRED FEDFUNDS Oct-2026 3.88% | consistent |
| Dollar | Yahoo DXY 104.0 (27-Nov; +4.4% y/y, +4.9% in 3 m) | FRED broad dollar 123.6 (20-Nov; +1.9% y/y) | same direction |
| India price | IBJA 999 PM ₹126,299/10 g (27-Nov, ex-GST) | computed GC=F × INR = ₹108,181 (no duty) | gap explained by duty (below) |
| Pre-2003 real yield | proxy = GS10 − trailing CPI y/y (backward-looking) | — | proxy, stated |
FRED's LBMA series (GOLDPMGBD228NLBM) is discontinued (404). No CAPTCHA or anti-bot workarounds were used.

## Q1. Base rates: gold falls of 20% or more from a record (USD, monthly averages)
| Peak | Peak $ | Trough | Depth | Months to trough | Months to regain peak | Real (CPI) months to regain | Run-up before peak |
|---|---|---|---|---|---|---|---|
| Jul-1973 | 120 | Nov-1973 | −21% | 4 | 6 | 6 | 3.4× / 36 m |
| Dec-1974 | 184 | Aug-1976 | −40% | 20 | 43 | 50 | 4.2× / 36 m |
| Jan-1980 | 675 | Jul-1999 | **−62%** | 234 | **316 (May-2006)** | 541 (~2025) | 5.1× / 36 m |
| Mar-2008 | 968 | Nov-2008 | −21% | 8 | 18 | 18 | 2.3× / 34 m |
| Sep-2011 | 1,772 | Dec-2015 | −39% | 51 | **106 (Jul-2020)** | 155 | 2.3× / 34 m |
| **Feb-2026** | **5,020** | open | **−27.5% today** (Oct average −18%) | 9 so far | ? | ? | **2.7× / 36 m** |

- **Since 1968 (5 completed episodes):** median depth −39%, median recovery 43 months, range 6–316 months.
  **With a peak in 1975 or later (3):** −62%, −21%, −39%, and recoveries of 316, 18 and 106 months.
- **At a 15% threshold** (sensitivity) three more appear: 1969 (−20%, 31 m), 1974 (−17%, 7 m) and 2020–22 (−16%, 32 m).
- **Monthly averages understate daily extremes.** By daily closes 2008 was about −30% and 2011–15 about −45%. The median
  month's lowest close sits 2.6% below its average.
- **In rupees** (FRED EXINUS × USD gold) there were four 20%+ falls since 1975: 1975–76 −31% (37 m to regain), 1980–82
  −45% (81 m), 1996–99 −25% (74 m) and 2012–15 −25% (82 m). The 1980 bear lasted ~6.8 years in rupees against 26 years in
  dollars. Today rupee gold is −31% from its 29-Jan close (₹157,381 → ₹108,181 per 10 g, no duty).

## Q2. Does a bigger run-up mean a deeper or longer fall?
The three run-ups of 2.5× or more within 36 months (1973, 1974, 1980) fell −21%, −40% and −62%, a median of −40%. They took
6, 43 and 316 months to recover. The two smaller run-ups (2008 and 2011, both 2.3×) fell −21% and −39%. The biggest run-up
(1980, 5.1×) did have the biggest fall. But 1973 (3.4×) fell only briefly, and 2011 fell almost as far as 1974 on a
smaller run-up. **Verdict: weak, directionally supportive, n = 5. It does not justify a deeper scenario on its own.** The
definition also matters. On monthly averages 2008–11 was a 2.3× run-up; the quick note's "2.8×" used daily highs and lows.
Today's 2.7× run-up puts it in the "big" set, whose analogs are 1974–76 and 1980–2006 (see the scenarios).

## Q3. Does the Fed or real-rate regime explain falls and recoveries?
| Episode | Fed (6-month change rule) at peak | Real yield at peak → trough | Change during fall | Real-yield change in the 12 m after trough |
|---|---|---|---|---|
| 1973 | hiking | 1.4% → −1.5% | −2.9 pp | −3.0 pp |
| 1974–76 | cutting | −4.7% → 2.1% | **+6.7 pp** | −1.3 pp |
| 1980–99 | hiking | −3.1% → 3.6% | **+6.7 pp** | −1.2 pp |
| 2008 | cutting | 1.1% → 2.9% | +1.8 pp | −1.6 pp |
| 2011–15 | hold (zero rates) | 0.1% → 0.7% | +0.65 pp | −0.2 pp |
| 2026 (to Jul) | cutting | 1.8% → 2.4% | +0.5 pp | — (now 2.79%, +0.96 pp y/y) |

Across all months since 1975:
- The 12-month gold return correlates **−0.39** with the 12-month change in real yield (1975–2002, proxy) and **−0.42**
  (2003–2026, TIPS).
- **The Fed label alone carries no information.** Next-12-month median returns were +7.1% when hiking (196 months), +6.9%
  when cutting (183) and +1.4% on hold (231).
- **The real-yield level matters.** Next-12-month medians were −4.6% below 0% (78 months, mostly the late 1970s), +12.8% at
  0–2% (225) and **+0.5% at 2% or above (307 months, 47% negative)**.

**Verdict:** rising real yields accompanied 5 of 6 falls, and falling real yields began all 5 recoveries we can measure.
The exception, 1973, was an inflation spike. Today's 2.8% real yield is the setting in which gold has historically gone
nowhere. Recovery needs real yields to fall, for example if the Fed stops hiking or inflation cools faster than nominal
yields.

## Q4. How much does rupee weakness cushion a fall?
- **During each dollar fall:** the rupee cushion was +5 pp (1973), +6.5 pp (1974–76), +17 pp (2008) and +24 pp (2011–15,
  when the rupee fell 39%). Across 1980–99 the rupee lost about 80% of its value against the dollar, so rupee gold *rose*
  106% while dollar gold fell 62%.
- **Across all 246 twelve-month periods since 1975 in which dollar gold fell:** rupee gold did better 91% of the time, by
  a median 7.5 pp. **It was still negative 59% of the time.** The rupee fell 4.9% a year on average from 1975 to 2026.
- **Now the cushion is working in reverse.** The rupee strengthened from ~95.5 (Sep/Oct) to 92.4, so rupee gold fell 12.7%
  in the last month against 10.2% in dollars.
- **Domestic price and duty (checked per L50).** India raised the gold import duty to an effective **15%** (10% basic +
  5% AIDC) from **13-May-2026** (Goodreturns, IIFL; also Khaleej Times and Telangana Today). One outlet says 18.4%, which
  conflicts with the others. The February-2026 Budget had left the duty at 6% (Motilal Oswal, NewsBytes). Arithmetic:
  ₹108,181 × 1.15 = ₹124,408, against IBJA ₹126,299, a residual premium of **+1.5%**. This settles the "~16% unexplained"
  gap in L51 and `tools/macro/README.md`. **Two risks follow for Indian holders.** A rollback to 6% would cut domestic
  prices ~7.8% (1.06/1.15 − 1). And the WGC notes that past duty hikes raised smuggling, which tends to bring pressure for
  a rollback.

## Q5. Are forecasts and "buy zones" informative?
**LBMA annual survey: consensus average-price forecast (published each January) vs the actual annual average**
| Year | Consensus | Actual average | Consensus error | No-change error (prior Dec) | Consensus better? |
|---|---|---|---|---|---|
| 2020 | 1,558.8 | 1,770 | −11.9% | −16.4% | yes |
| 2022 | 1,801.9 | 1,801 | +0.1% | −0.6% | yes |
| 2023 | 1,859 | 1,943 | −4.3% | −7.5% | yes |
| 2024 | 2,059 | 2,388 | −13.8% | −15.1% | yes |
| 2025 | 2,735 | 3,442 | −20.5% | −23.1% | yes |
| 2026 (Jan–Oct) | 4,742 | 4,507 | +5.2% | −4.4% | no (so far) |
Source: lbma.org.uk survey pages (2021 is missing: its page is internally inconsistent). Mean absolute error over the 5
full years was 10.1% for the consensus against 12.5% for no change. **This passes the pre-set bar, but narrowly.** The
consensus works like a slightly upward-tilted "no change" forecast, missing big moves in both directions (−12% to −21% in
the three surge years). It is useful for direction in quiet years and useless for turning points.

**Bank targets in 2026 (secondary sources, mostly single-sourced each; no score because there are fewer than 8 dated
pairs):**
- **Goldman:** end-2026 $4,900 → $4,650 → **$4,150** (early/13-Nov-2026: Kitco, Mining Weekly, investinglive); end-2027
  $5,400 → $4,800 → $4,650 (the last step is single-source).
- **UBS:** end-2026 $5,900 → $5,500 (27-May-2026, Kitco).
- **JPMorgan:** Q4-2026 ~$6,000 → $4,500 (Jul-2026, Mitrade).
- **BofA:** cut its 2026 average (Jul-2026, BNN Bloomberg).
Every end-2026 target set in the first half of 2026 ($4,500–5,500) is now 24–51% above the price with a month left, and each cut followed
the fall rather than preceding it.

**The "fund houses accumulate below $3,600/$3,500" claim**
- **What we found:** FXEmpire (Nov-2026: "$3,500 support in focus", technical analysis); Edgen ("the bank identifies
  $3,500 as next major support zone", bank not named, and a claim that central-bank buying of ~81 t/month "provides a
  floor"); FXStreet video (2-Nov-2026, "buy below $4,000 or wait for $3,500?"); Investing.com ("$3,500 deep-value zone",
  2025, stale).
- **What we did not find:** any named fund house or bank stating, on a date, that it is buying below $3,600 or $3,500.
- **Flow evidence:**
  - WGC Gold Demand Trends Q3-2026 (3-Nov-2026, primary): central banks bought 321 t (+42% y/y). Only 120 t was reported;
    63% is WGC's estimate of unreported buying. China (63 t) and Poland (40 t) made up 86% of the reported total.
  - ETFs added 211 t in Q3, to a record 4,256 t (secondary: TradeArabia, Engineering News).
  - October ETF inflows were +$2.7 bn (WGC via FXEmpire, single source).
  - **The Q3 average price was ~$4,270.** No flow data yet covers prices below $3,600, which gold first reached in November.
  - The WGC itself says only that lower prices "may have supported purchases at the margin". It makes no floor claim.
- **Verdict:** the "buy zone" is opinion and technical analysis. A floor at $3,500–3,600 is **not evidenced**.

## Today's drivers: facts vs opinions
| Facts (dated, two sources) | Opinions or market pricing (not facts) |
|---|---|
| Fed hiked to 3.75–4.00% on 17-Sep-2026 after three cuts in late 2025 (FRED target series) | ~90–96% market odds of a 25 bp hike on 9-Dec (CME FedWatch via news, 17-Nov; secondary) |
| 10-yr real yield 2.79% (+0.96 pp y/y); nominal 10-yr 4.85–4.94% | Goldman expects a third hike in March 2027 (single source) |
| DXY 104.0, +4.4% y/y and +4.9% in 3 months | "Central-bank buying is a floor" (Edgen); "$3,500 support" (technical) |
| Central banks bought 321 t in Q3 (WGC, estimate-heavy); ETFs +211 t in Q3 | Bank year-end targets ($4,150–5,500 for 2026; $4,650–4,800 for 2027) |
| India duty 15% since 13-May-2026; IBJA premium over duty-paid world price ~+1.5% | "Weakening Chinese ETF demand in early November" (single source) |

## Scenarios from $3,640: pre-registered analog method
The method: take months since 1975 when gold sat 25–45% below its record (224 months, from 3 episodes: 1974–76, 1980–2006
and 2011–20). Bucket their forward returns. Average the "big run-up" set (2 episodes) and the "real yield ≥2% or hiking"
set (3 episodes), each shrunk toward the unconditional set (k = 3 episodes). Floor every bucket at 5% (L36). Each
scenario's price is the median analog return in that bucket.

| Horizon | Scenario | Return band | Typical price | P (pre-registered) | P (equal weight per episode, sensitivity) | What has to happen |
|---|---|---|---|---|---|---|
| 12 m (Nov-2027) | Best | > +25% | ~$4,780 (+31%) | **9%** | 16% | Fed stops after Dec and real yields fall below ~2%; central banks and ETFs keep buying (the 1976–78 pattern) |
| | Base | −5% to +25% | ~$3,770 (+4%; range $3,460–4,550) | **52%** | 61% | Real yields stay ~2–3%; choppy range trade |
| | Bad | −25% to −5% | ~$3,200 (−12%) | **34%** | 22% | Hikes in Dec and Mar, real yields 3%+, stronger dollar, ETF outflows |
| | Worst | < −25% | ~$2,530 (−30%) | **5%** (floor; raw 2–3%) | 1% | A 1981-style real-rate squeeze and central-bank buying stalling |
| 24 m (Nov-2028) | Best | > +25% | ~$5,510 (+51%, near the record) | **23%** | 46% | Real yields fall substantially and the bull market resumes (1976–78, 2016–20) |
| | Base | −5% to +25% | ~$3,770 | **30%** | 31% | Range |
| | Bad | −25% to −5% | ~$3,180 (−13%) | **42%** | 22% | A 2013–15 style grind: real yields stay positive and high, the dollar strong |
| | Worst | < −25% | ~$2,650 (−27%) | **5%** | 2% | 1980s: years of high real rates. A full 1980 depth (−62% from the record) would mean ~$1,900 |

**How to read this:**
- The pre-registered numbers count every month, so the 1980–2006 bear (147 of 224 months) dominates them. The
  equal-weight column gives 1974–76 (a quick doubling) as much weight as that long bear. The truth for 24 months is
  probably somewhere between: P(best) of 23–46% is honest uncertainty, not precision.
- Three episodes is a very small sample. Read every probability as ±10–15 pp.
- History's left tail is real: the median completed fall reached −39% and the worst −62%. From today's −27.5%
  (monthly-average basis) that means ~−16% more at the median and ~−48% more at the extreme.

## Calls: study vs the existing five (pre-registered rule: issue a -v2 if the gap is 0.10 or more)
| Existing call | Ours (28-Nov) | Study | Equal-weight sensitivity | Daily-close adjusted (touch/record only) | Action |
|---|---|---|---|---|---|
| close ≥ $4,000 on 30-Jun-2027 | 0.35 | **0.14** | 0.20 | — | **-v2 at 0.14** |
| any close ≤ $3,200 by 30-Jun-2027 | 0.35 | **0.15** | 0.20 | 0.27 | **-v2 at 0.15** (biased low, see note) |
| any close ≤ $3,070 by 31-Dec-2027 | 0.25 | 0.21 | 0.16 | 0.30 | keep (gap < 0.10) |
| close ≥ $4,500 on 31-Dec-2027 | 0.30 | **0.12** | 0.20 | — | **-v2 at 0.12** |
| any close > $5,318 by 31-Dec-2028 | 0.20 | 0.19 | 0.32 | 0.20 | keep |

**Note.** "Touch" calls resolve on daily closes, but the pre-registered method uses monthly averages, which understate
touches. The median month's lowest close is 2.6% below its average. The daily-close adjusted figure (0.27 for $3,200) is
stored with each -v2 call so both can be Brier-scored when it resolves. **The bigger lesson is our 28-Nov judgment.** It
put 0.35 on a quick recovery to $4,000 when the base rate is ~0.15–0.20. That is optimism, the mirror image of L36's
left-tail under-weighting.

## The L52 rule in a gold bear market (rules, not predictions)
Data: the allocation test's fund-NAV series (INR, Apr-2006 → Oct-2026), with 70/20/10 equity/gold/bonds reset each January.
| What happened | What the rule did |
|---|---|
| Jan-2025 and Jan-2026: gold had drifted to 25% and **29%** of the portfolio | Sold gold worth 4.7% and **9.2% of the portfolio**, mechanically trimming near the top |
| 2013–15: rupee gold −25% (Aug-2013 → Jul-2015, 70 months to regain) | Jan-2013/14/15 resets **bought** gold worth 2.7%, 2.4% and 4.7% of the portfolio. The portfolio still rose **+34%** over the window (equity +57%) |
| If gold stays ~25% below its Jan-2026 level until Jan-2027 (equity flat) | The reset buys ~4.2% of the portfolio in gold |
| Further fall of 16% (to the median historical depth) / 40% / 50% | Portfolio hit −3.2% / −8.0% / −10.0% (20% sleeve); the January reset then buys 2.6% / 7.0% / 8.9% |

**The rules:**
1. **Keep the target share fixed at 20%.** Don't raise it because gold is "cheap" and don't cut it because it is falling.
   Any timing tilt must beat a fixed split at its average weight (L52) and pass a pre-registered test.
2. **Rebalance once, in January.** No intra-year "buy zone" lump sums. A $3,500 floor is not evidenced.
3. **New SIP money goes to whichever asset is most below target.** While gold sits under 20%, that means gold, gradually
   and with no tax.
4. **Plan for time, not just depth.** Recoveries took 18–316 months in dollars and 37–82 months in rupees. Gold is
   insurance; the growth engine is equity.
5. **Indian holders: know the duty risk.** Domestic prices include a 15% duty that could be cut. Instruments that track the
   domestic price carry that risk; it is a one-off ~8% hit, not a reason to trade.

## Caveats
- **Tiny sample.** 5 completed 20%+ episodes since 1968, 3 analog episodes, and 1980–2006 dominates the month-pooled
  numbers. The monthly history has a single lineage before 2000 (WB/LBMA, mirrored by datahub).
- **Monthly averages** understate peak-to-trough depth by ~5–10 pp and touch probabilities.
- **The pre-2003 real yield is a proxy** (backward-looking CPI), which overstates real-yield swings in the 1970s.
- **Structural break.** Central-bank buying at ~1,000 t a year since 2022 has no historical analog, and the method does
  not weight it. If it persists it argues for the equal-weight (more bullish) column.
- **Opinion data is secondary.** Bank targets and Fed odds come from news; one Goldman figure is single-source.
- **Q5** has 5 full years only. The 2021 LBMA page is inconsistent and was excluded.
- **Deviations from the pre-registration (made after seeing results, marked):** (a) the episode-weighted sensitivity and
  (b) the daily-close adjustment for touch events were added as sensitivities only and do not drive the calls. (c) Today's
  % below the record uses the latest close against the monthly-average record (5,020), consistent with how the history
  analogs are defined. (d) FRED's LBMA series is gone, so datahub replaced it as the "second" history source; it shares
  the WB lineage.

Sources (as of 28-Nov-2026):
- **Data files:** `data/sources.json`, covering FRED (EXINUS, DEXINUS, DFII10, FII10, GS10, DGS10, CPIAUCSL, FEDFUNDS,
  DFEDTARU, DTWEXBGS), the World Bank CMO pink sheet, datahub.io gold-prices, Yahoo (GC=F, INR=X, DX-Y.NYB, ^TNX),
  api.gold-api.com, home.treasury.gov real yield curve, ibjarates.com, and FBIL via RBI (macro snapshot 25-Nov).
- **Pages:** gold.org Gold Demand Trends Q3-2026 central-banks page; lbma.org.uk forecast-survey pages (2023 winners,
  2025 and 2026 at-a-glance; 2020, 2022 and 2024 figures via LBMA pages in search results).
- **News:** Kitco (13-Nov-2026 Goldman; 27-May-2026 UBS; 29-Jan-2026 record); investinglive; Mining Weekly; Mitrade (JPM);
  BNN Bloomberg (BofA); Goodreturns, IIFL, Khaleej Times, Telangana Today, Motilal Oswal, NewsBytes (duty); FXEmpire,
  Edgen, FXStreet, Investing.com (buy-zone claims); CBS, Nasdaq, Nation Thailand (record); TradeArabia, Engineering News
  (ETF tonnes); Finimize (Fed odds).
