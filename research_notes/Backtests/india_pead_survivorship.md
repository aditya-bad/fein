# Back-test: does survivorship bias change Indian PEAD? Dead and delisted firms added (Roadmap stage 3)

*Method calibration, not stock picking. Research, not SEBI-registered advice.*
Started 2026-11-22. **Stage 3 (signals)** of `memory/roadmap.md`. It checks our one proven signal, the Indian PEAD
avoid leg (lessons L17, L19; `india_pead.md`, `india_pead_v2.md`). Both earlier tests drew their universe from
**today's** NSE equity list, so firms that died, were delisted or merged before Nov-2026 were absent (v1 §4: 16.8% of
Q3 FY19 filers are no longer listed). Lessons L27/L28: screener.in still serves dead Indian firms' weekly prices, and
survivors-only samples have already flipped one of our conclusions.
**Unlocks:** if the avoid leg holds with the dead firms back in, the stage-2/3 "avoid/exit after a big earnings miss"
rule keeps its proven status, and the live tracker's secondary test (`india_pead_live/`) is the right benchmark. If
it does not, the rule is downgraded before the live test starts in Jan-2027.

## STEP 0 — Feasibility (22-Nov-2026, before any outcome was computed)
- **NSE still serves dead firms' result filings.** `api/corporates-financial-results?symbol=X` returned the full
  quarterly filing list with XBRL links for FLFL (Future Lifestyle, 54 filings to Sep-2022), PUNJLLOYD (88, to
  Mar-2019) and RNAVAL (71, to Sep-2023). So dead firms' EPS and filing dates come from the **same source and the same
  code as the live firms** (v1 `s3_results.py`). Screener's 13-quarter tables are not needed.
- NSE's all-company version of the same feed (date-range query) lists every filer, dead or alive, with symbol and ISIN.
  NSE re-labels renamed live firms with their current symbol (e.g. Magma → POONAWALLA), so a filer missing from today's
  `EQUITY_L.csv` by symbol and ISIN is a firm that left the main board.
- Prices: Yahoo has no delisted Indian tickers. Screener's chart API serves a weekly (Friday-dated), split- and
  bonus-adjusted close for dead firms up to the week trading stopped (`solvency_flags_india.md` step 0).

## PRE-REGISTRATION (written 22-Nov-2026 before any return of any dead firm was fetched or computed)
State of knowledge: the v1/v2 results (daily prices, live firms only) are known (L17, L19). Before writing this, the
only new data looked at are the three filing lists above and the row counts of the first weeks of the all-company
filing feed (still running). No dead-firm price, EPS or return has been fetched.

### Universes (two, compared like for like)
- **LIVE** = v1's sample exactly: shuffled current-list positions 0–349 and 500–849 (700 of the 1,791 NSE EQ/BE
  symbols listed ≤ 2023-06-30; seed 20261121), with v1's cached standalone EPS, filing dates and announcement dates.
  This is the universe behind lesson L17. Sampling fraction **f = 700 / 1,791 = 0.3908**.
- **MISSING** = every symbol that filed quarterly results on NSE between 2018-01-01 and 2025-03-31 (all-company feed,
  7-day windows) and is **not** in v1's frame: (a) **dead/left** = neither its symbol nor its ISIN is in today's
  `EQUITY_L.csv` or today's NSE SME list; (b) **off-series** = in `EQUITY_L` but not EQ/BE series (e.g. BZ), so v1 also
  excluded it. Both are shown separately in the audit. Shuffled with seed **20261122**, and the first round(f × N)
  symbols are taken, so MISSING is sampled **at the same rate as LIVE** and the union is an unweighted, proportionate
  random sample of all NSE quarterly filers 2018–2025.
- **ALL** = LIVE ∪ MISSING. The comparison is ALL vs LIVE. Everything below is computed identically for both.

### Data rules (v1 rules unless marked ★)
- EPS: **standalone** basic EPS from NSE filings (v1 D1; v1 `s3_results.do_symbol`, reused unchanged for MISSING,
  including its mcap pre-filter: skip a symbol whose shares × close never touches ₹400–60,000 cr in 2018–2025).
- SUE = (EPS_q − EPS_{q−4}) / sd(up to 8 previous seasonal changes), ≥ 4 prior changes, sd > 0 (v1).
- Event date: earliest NSE results announcement after quarter-end and ≤ feed date, else feed date (v1 D8);
  announcements from NSE `corporate-announcements` per symbol (v1 `s3b_announce.py` logic). Filings > 150 days after
  quarter-end dropped. Events dated **2018-01-01 → 2025-12-31**.
- ★ **Weekly prices for everyone.** MISSING firms: screener weekly close. LIVE firms: v1's daily Yahoo closes are
  turned into weekly closes (last close of each Mon–Fri week, labelled with that week's Friday, as screener does).
  **LIVE is re-run on these weekly closes**, so the ALL-vs-LIVE difference is not a daily-vs-weekly artefact. The
  weekly LIVE result is also compared with v1's published daily result (calibration only).
- ★ Entry = first weekly close dated strictly after the event date (dropped if > 10 days after it). Horizons:
  **4 / 13 / 26 weeks ≈ 21 / 63 / 126 trading days; primary = 13 weeks**. ≥ 50 weekly closes before entry required.
- Size at entry: shares (median of the last 3 filings' paid-up capital / face value, filings dated ≤ entry) × close.
  LIVE uses v1's Yahoo split un-adjustment. ★ MISSING firms have no split history: adjusted close × shares is used
  (stated bias: a later split or bonus makes a dead firm's earlier mcap look smaller). Band ₹500–50,000 cr.
- ★ **Delisting rule (the point of this test).** Exit price = the last weekly close dated ≤ entry + h weeks
  (+ 3 days). If a firm's price series ends inside the window, its return runs to its **last traded weekly close**
  (it is not dropped). Events need at least one close after entry. The same rule applies to controls.
- Controls: equal-weight mean return over the same window of all firms **in the same universe** (ALL or LIVE) with a
  close on the entry date, mcap ×0.5–×2 of the event firm, firm excluded, ≥ 5 required. Excess = event − control.
- Quintiles of SUE within each fiscal quarter of the universe being tested (≥ 25 events), so ALL and LIVE each get
  their own cut points.

### Hypotheses and decision rules (fixed now)
Inference as v1: unit = fiscal quarter; equal-weight mean within each quarter's portfolio; mean of quarterly values;
t across quarters; 95% bootstrap CI resampling quarters (5,000 draws, seed 1). **Primary period: all events
2018–2025** (the deaths cluster in 2018–21, v1's train period); 2018–21 and 2022–25 are shown separately.
- **H1 (primary).** In **ALL**, the bottom SUE quintile's 13-week excess return vs size-matched controls is
  **≤ −1%**, and (t < −3 or CI upper bound < 0). Supported / not supported. Expectation: stronger than in LIVE,
  because failures cluster among big earnings misses.
- **H2 (primary).** In **ALL**, the top quintile's 13-week excess **net of 1%** is > 0 with t > 3 or CI excluding 0 →
  "proven"; otherwise "not proven". Expectation: not proven (as in v1 and v2); reported whichever way it falls.
- **H3 (measurement).** Survivorship bias of each leg = ALL − LIVE (bottom, top, top−bottom) at 13 weeks, with a
  **paired bootstrap over fiscal quarters** (same resampled quarters for both universes). Reported as a number with
  its CI; "material" if |bias| ≥ 0.5 pp and the CI excludes 0.
- **Sensitivities (do not overturn H1/H2):** (S1) a Shumway-style **−30% delisting return** added for MISSING firms
  that are on a distress list (IBBI CIRP/liquidation, NSE compulsory/liquidation delisting, NSE/BSE suspension, from
  `research_notes/Universe/india_dead_companies_2026-11-22.csv`) whose series ends inside the window; (S2) the
  survivors-style rule — drop every event whose window is not fully traded; (S3) events of dead/left firms only vs
  off-series firms; (S4) 4- and 26-week horizons; (S5) top-minus-bottom.
- Known biases stated in advance: (1) renamed-then-delisted firms may appear under an old symbol with a broken screener
  page → a firm lost from MISSING (counted); (2) MISSING firms without a screener page or price series are lost
  (counted, by distress status) → residual survivorship bias toward *better* bottom-quintile returns; (3) weekly
  closes coarsen entry by up to 4 trading days for everyone; (4) dead firms' mcap without split adjustment; (5) firms
  that stopped filing before their price stopped (common in distress) leave the event sample before the collapse —
  only their last pre-silence events count; (6) price returns, no dividends (v1 D3); (7) sampling noise of ~40% of the
  missing firms.

---
## Stage log
- 2026-11-22: feasibility done; all-company filer list fetch started (7-day windows, one NSE stream at ≥ 1.5 s); this
  pre-registration saved before any dead-firm price or EPS was fetched.
- 2026-11-22: filer list complete: 379 seven-day windows (none failed), **2,403 filer symbols**. 1,779 are in v1's
  frame; 247 are in today's list as EQ/BE but listed after 2023-06-30 (outside v1's frame by design, not missing);
  **377 MISSING** = 347 dead/left + 30 off-series. Sample at f = 0.3908 → **147** (132 dead, 15 off-series).
  Fetch started: screener stream and NSE stream run in parallel, **one stream per host** at ≥ 1.5 s (the screener and
  NSE servers are different sites; each sees a single polite stream).
- **D1 (2026-11-22, before any return was computed): distress-tag fix.** The tag list in `s2_missing.py` used
  `nse_delisted:compulsory` / `:liquidation`, but the dead-company file spells the events
  `delisted_compulsory_delisting` / `delisted_delisting_liquidation`, so those were not counted as distress. Fixed;
  sampled distress-listed firms 77 → 80. The sample and its order are unchanged (checked). It only affects the S1
  sensitivity.
- 2026-11-23 (resumed after a usage-limit pause): fetch complete. Screener: 131 of 147 sampled MISSING firms have a weekly price series (66 from the solvency cache, 65 fetched; 16 no page). NSE: 61 'ok', 70 out of the ₹400–60,000 cr pre-filter range, 16 skipped (no prices). Event build and analysis run next, unchanged.
- 2026-11-23: `s4_events.py` and `s5_analyze.py` ran once, unchanged from the pre-registered rules. Results below.

---

# RESULTS (written 2026-11-23 after the run; everything above is the unchanged pre-registration and log)

## Funnel and survivorship audit
| step | count |
|---|---|
| NSE quarterly filers 2018-01 → 2025-03 | 2,403 symbols |
| MISSING (not in v1's frame): dead/left 347 + off-series 30 | 377 |
| sampled at f = 0.3908 (seed 20261122) | **147** (80 on a distress list) |
| no screener page or price series | 16 (all *not* distress-listed: mostly old mergers / renamed firms) |
| mcap never ₹400–60,000 cr in 2018–25 (v1 pre-filter) | **70 (49 of them distress-listed)** |
| results fetched, no eligible event (no SUE history, < ₹500 cr at entry, or filing after trading stopped) | 20 (15 distress) |
| **firms contributing events** | **41 (16 distress-listed)** |
| MISSING events / ALL events | **468 / 10,242 (4.6%)**; 332 in 2018–21, 136 in 2022–25 |

LIVE re-run on weekly closes: 580 firms, 9,774 events (v1 daily: 9,782 EPS-SUE events). Of the 468 MISSING events only
19 had the price series end inside the 13-week window. Most dead firms stopped filing results well before their
shares stopped trading (bias 5), so the delisting-return rules (S1 −30% penalty, S2 drop) barely move anything.
**The main reason dead firms matter little here: most Indian failures were already below ₹400–500 cr by the time
they were in trouble** (49 of 80 sampled distress firms never reached the band in 2018–25). MISSING is about half
failures (JP Associates, Future Consumer / Lifestyle, Max Ventures, Nagarjuna Fertilizers, Manpasand, Rolta,
Kwality, JBF, Amtek Auto…) and half mergers / buy-outs at a premium (Piramal Enterprises, Tata Coffee, JMC Projects,
Cigniti, Ujjivan, Equitas, the merged PSU banks…). Firm list: `india_pead_survivorship_outputs/missing_sample.csv`.

## Verdicts (13 weeks ≈ 63 trading days; all events 2018–2025; 32 fiscal quarters; bootstrap over quarters)
| | ALL (live + missing) | LIVE (weekly re-run) | bias = ALL − LIVE (paired) | verdict |
|---|---|---|---|---|
| **H1** bottom quintile vs controls | **−2.43% [−3.18, −1.66], t −6.17** | −2.08% [−2.73, −1.42], t −6.00 | **−0.35 pp [−0.82, +0.06]**, t −1.48 | **H1 SUPPORTED** (≤ −1%, t < −3); stronger with the dead firms in, as expected |
| **H2** top quintile net of 1% | **+1.00% [−0.03, +2.20], t 1.72** (gross +2.00%, t 3.44) | +0.76% [−0.25, +1.86], t 1.37 | +0.25 pp [−0.03, +0.53], t 1.70 | **H2 NOT PROVEN** (CI touches 0, t < 3), third time |
| top − bottom (raw) | +4.39% [+2.86, +5.91], t 5.55 | +3.81% [+2.44, +5.19], t 5.20 | +0.57 pp [−0.01, +1.19], t 1.84 | — |
| all events vs controls | +0.01% | +0.02% | −0.02 pp | controls calibrated |

**H3 (how much survivorship bias the live-only universe carried):** survivors-only data *understated* the avoid leg by
**0.35 pp** (−2.08% → −2.43%) and the top-minus-bottom spread by **0.57 pp**, and understated the top leg's excess by
0.25 pp. **None is "material" by the pre-registered rule** (|bias| ≥ 0.5 pp and CI excluding 0): the T−B bias reaches
0.57 pp but its CI touches −0.01. The bias is larger in 2018–21, where the deaths are: bottom −0.66 pp [−1.58, +0.15],
T−B +1.02 pp [−0.14, +2.16]; in 2022–25 it is ≈ 0 (−0.04 / +0.13 pp).

**Where the bias comes from (decomposition, 13 weeks, full period):**
- *Event side:* the dead firms' own events push the bottom quintile down by 0.56 pp; the top quintile is unchanged.
- *Control side:* adding dead firms to the size-matched controls lowers control returns, which lifts every excess
  return by ~0.2–0.25 pp. This is why the top leg looks *better*, not worse, with the dead firms in.
- MISSING firms' events lag controls in every quintile (event level, 13w: Q1 −7.3%, Q2 −5.1%, Q3 −3.6%, Q4 −0.8%,
  Q5 −2.4%). **Distress-listed firms after a bottom-two-quintile result: −16.6% mean (median −16.6%, 71 events);**
  distress-listed firms in Q3–Q5 −8.4% (67). Non-distress missing firms (mostly mergers): about −0.4% to −0.9%.

## Robustness (does not overturn H1/H2)
| 13 weeks, full period | bottom | top net 1% | T−B |
|---|---|---|---|
| S1: −30% delisting return for distress firms whose series ends in the window | −2.44% (t −6.18) | +1.01% (t 1.73) | +4.40% |
| S2: survivors-style, drop events whose window is not fully traded | −2.44% (t −6.25) | +1.00% (t 1.71) | +4.39% |
| S3: without off-series firms | −2.33% (t −6.38) | +1.00% (t 1.68) | +4.27% |
| ALL, 2018–21 / 2022–25 | −3.07% (t −5.18) / −1.78% (t −3.70) | +0.98% / +1.02% | +5.18% / +3.60% |
| ALL, 4 weeks | −0.83% (t −3.62) | −0.60% | +1.22% |
| ALL, 26 weeks | −3.94% (t −5.20) | **+2.23% [+0.49, +4.07], t 2.40** | +7.22% |

The avoid leg holds in both sub-periods, at every horizon, and under every delisting rule. At 26 weeks the long leg's
net CI excludes zero but t is 2.40 < 3, and 26 weeks is not the primary horizon (as in v1, it is not used to rescue H2).

**Weekly vs daily calibration.** The LIVE weekly re-run gives bottom −2.08% / top +1.76% / T−B +3.81% over 2018–25,
against v1's daily figures on the same firms of −2.42% / +2.08% / +4.54% (v1 events through the same functions).
Weekly closes cost about 0.3 pp per leg (entry up to four trading days later, so some of the drift is missed). The
ALL-vs-LIVE comparison is weekly on both sides, so this does not affect H3. Daily ALL figures would be about 0.3 pp
stronger on each leg.

## What it means
1. **The avoid leg survives the survivorship check and gets a little stronger.** Lesson L19's rule (treat the bottom
   two SUE quintiles as an avoid/exit flag for ≥ 63 trading days) stands. With the dead firms back in, it is −2.4% vs
   controls per quarter, t ≈ −6, 2018–2025.
2. **The live-only universe was a mild, not a fatal, bias** (≈ 0.35 pp on the avoid leg, ≈ 0.6 pp on T−B, both pointing
   the way v1 §4 predicted). Unlike lesson L28 (pledges), the conclusion does not flip. The reason is the ₹500 cr
   floor: most failures fell below it before they failed.
3. **The cheapest edge is the overlap with distress:** a big earnings miss at a firm that later lands on a distress
   list lost −16.6% vs controls in 13 weeks. That supports pairing the PEAD avoid flag with the stage-2 solvency /
   pledge flags (L27, L28). This is descriptive only (71 events, 16 firms, picked by later fate), not a tested rule.
4. **The long leg is still not proven net of costs** (+1.0%, t 1.7). No change to "don't buy on a positive surprise
   alone."

## Caveats
- MISSING is a 39% sample (147 of 377). Only 41 firms and 468 events contribute, so the bias CIs are wide, and a
  different seed could move the bias by a few tenths of a point.
- 16 sampled firms (11%) had no screener page or price series. None was distress-listed, so this loss is mostly
  mergers and probably does not affect the bottom leg.
- Dead firms' mcap uses adjusted price × shares without split un-adjustment, and their EPS has no split adjustment
  (pre-registered bias 4). Standalone EPS throughout (v1 D1). Price returns only.
- Weekly closes for everyone (see calibration). Screener's weekly close is labelled with the Friday.
- Firms that stopped filing before their shares stopped trading drop out of the event set before the collapse. This is
  the realistic case (no fresh SUE exists), but it means "avoid after a miss" cannot catch a firm that goes silent;
  a missed filing deadline is a separate red flag.
- Fetching: one stream per host (NSE and screener in parallel, each ≥ 1.5 s); logged above.

Scripts: `tools/backtests/india_pead_survivorship/` (common, s1_filers, s2_missing, s3_fetch, s4_events, s5_analyze).
Outputs: `research_notes/Backtests/india_pead_survivorship_outputs/` (results.json, tables.md, events_w.tsv,
missing_sample.csv, funnel_audit.json). Raw cache: scratchpad `bt_pead_surv/` (not durable). Research, not
SEBI-registered advice.
