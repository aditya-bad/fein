# Allocation test (India, rupees): does a gold/bond defence layer earn its keep vs 100% equity?

## Plain-language summary (added 2026-11-26, after the computation; the pre-registration below is unchanged)

**What we tested:** ₹10 lakh put in at the start of April 2006 and left alone until the end of October 2026 (20.5 years,
which includes the 2008 crash, 2011, 2020 Covid and the 2025 gold boom). Equity = a real Nifty 50 index fund (UTI, regular
plan, after its fees); gold = world gold price converted to rupees, minus 0.5%/yr; bonds = a real 10-year government-bond
fund (SBI 10-yr Constant Maturity Gilt, after fees). Rebalancing pays 0.1% trading cost and capital-gains tax.

| Strategy | ₹10 lakh became | Return per year | Worst fall | Worst fall in rupees | Time from peak back to peak | Worst 5-yr stretch (per yr) | 5-yr periods it beat 100% equity |
|---|---|---|---|---|---|---|---|
| 1. 100% equity | **₹71.8 lakh** | 10.1% | −55% (Dec-07 → Nov-08) | ₹17.5L → ₹7.8L (**−₹9.6L**) | **5.8 years** (to Oct-2013) | −1.4% | — |
| 2. 70/20/10 equity/gold/bonds, reset every January | **₹83.3 lakh** | 10.9% | −38% | ₹15.4L → ₹9.5L (−₹5.9L) | 1.8 years (to Sep-2009) | +4.0% | 33% |
| 3. Same 70/20/10, reset only when 5pp off | ₹82.1 lakh | 10.8% | −39% | −₹6.0L | 1.9 years | +3.7% | 36% |
| 6. 50/50 equity/gold, reset every January (reference) | ₹102.2 lakh | 12.0% | −27% | −₹3.8L | 1.4 years | +4.0% | 39% |

Monthly SIP of ₹10,000 (₹24.7 lakh paid in): all equity → ₹81.8L (10.5%/yr); 70/20/10 reset yearly → ₹87.3L (11.1%);
**"new money to whatever is most below target", never selling → ₹89.9L (11.3%)**, with no capital-gains tax at all.

P/E-tilted version (2014–2026 only, because P/E data starts 2012): 11.3%/yr vs 11.8% for plain 70/20/10 and 11.9% for
100% equity; worst fall −15% vs −19% and −29%.

**What it means, honestly:**
1. **The defence layer worked, and cost nothing here — it even added return.** A 70/20/10 split cut the worst fall from −55% to
   −38% and the wait to get back to even from ~6 years to under 2, while ending *higher* (₹83L vs ₹72L). It passes our
   pre-set test. 
2. **But a big part of that is gold having an unusually good 20 years in rupees** (13.2%/yr vs equity 10.1%; the rupee fell
   from ~45 to ~95 per dollar, and gold rose ~72% in 2025 alone). If gold had earned only 7%/yr, the 70/20/10 split would
   have cost ~0.4%/yr of return — still a fair price for cutting the worst fall by 16pp. 50/50 would then cost ~1.1%/yr.
3. **It is mostly a 2008 story.** In 2 out of 3 five-year periods, 100% equity still won. Starting after the crash (Apr-2009),
   the split cut the worst fall by 11pp (not 15) for 0.2%/yr less return. Its job is insurance against the rare crash, not
   beating equity in normal years.
4. **Timing by P/E did not earn its place.** It held less equity on average (67%), and a plain fixed 67% split got almost the
   same protection with more return. Same finding as our earlier P/E test (L51).
5. **The YouTube "new money to the laggard" idea, done mechanically, was the best SIP** — ₹2.6L more than yearly
   rebalancing and no tax. Caveat: once the pot is big, new money can't steer it; it ended at 60/31/9 (too much gold), so a
   yearly check is still needed.
6. **Rebalancing by bands instead of every January made no difference.** Keep it simple: once a year.

Research, not SEBI-registered advice. One country, ~4 independent 5-yr periods, gold near a record: treat this as a base
rate, not a forecast.

---


Roadmap: this is the **wealth-plan / defence layer** that sits around the 7-stage stock pipeline (it sizes how much of the
portfolio is exposed to stage 6 decisions at all; it is not a stage of stock selection). Unlocks: a tested default split for
the user's overall money, and a mechanical rule for where new SIP money goes. Follows `research_notes/YouTube/GetMoneyRich -
I Found the One SIP Rule That Beats 90% of Investors/analysis.md` ("Test" section) and `research_notes/Macro/ey_gsec_gap_test.md`
(L51: P/E timing had no out-of-sample power 2012–21). Research, not SEBI-registered advice.

## Pre-registration (written 2026-11-26, BEFORE any data was fetched or any number computed)

### Universe and frequency
India, everything in rupees, month-end data, longest common history obtainable from public, scriptable sources
(aim: 2000 or 2003 → Oct/Nov-2026). Start = first month where all four asset series exist.

### Asset series (in order of preference; any fallback is recorded as a deviation)
- **Indian equity:** Nifty 50 TRI or Sensex TRI if obtainable from a public static file. Fallback: Nifty 50 / Sensex price
  month-end + dividend yield/12 accrued monthly (DY from NSE files where they exist, else a stated constant ≈1.3%, flagged).
- **Gold (INR):** two sources: (a) USD gold (LBMA PM via FRED if available; else Yahoo GC=F/XAU) × USD/INR (FRED
  EXINUS monthly / RBI-FBIL); (b) a second gold series (Yahoo or other) for cross-check. Where IBJA/RBI domestic gold prices
  are available, compare levels and explain the gap (import duty ~ 4–15% over time, GST, local premium/discount).
  The backtest uses international gold × USD/INR (no duty) as the return series — duty level changes add/subtract a few %
  one-off, noted, not modelled. Holding cost assumed 0.5%/yr (≈ gold ETF/fund expense).
- **Bonds:** India 10-yr G-sec total return approximated monthly from yields: r = y_{t-1}/12 − D·(y_t − y_{t-1}) +
  ½·C·(Δy)², with modified duration D ≈ 7 and convexity C ≈ 60 (constant-maturity 10-yr par bond approximation).
  Yield series: FRED INDIRLTLT01STM (OECD; from 2011-12) and/or a longer source if found. If no pre-2011 yield is
  scriptable, record it and use the longest available; a gilt index if public. Fund cost 0.5%/yr.
- **Cash:** 91-day T-bill yield (FRED INDIR3TIB01STM / RBI) accrued monthly; fallback repo-based. Used only as a reference
  (not in the main strategies) and for the taxable-cash check.

### Strategies (start ₹10 lakh lump sum at first month; also report a ₹10,000/month SIP version for (1),(2),(5))
1. **100% equity.**
2. **Fixed 70/20/10 equity/gold/bonds, rebalanced to target every January.**
3. **Same 70/20/10, drift bands:** checked monthly; rebalance all to target when any asset is ±5pp from target.
4. **Valuation-tilt bands:** equity target 80% / 70% / 60% when Nifty trailing P/E is in its bottom / middle / top
   tercile, remainder split gold:bonds 2:1; terciles **expanding-window (only data up to that month)** to avoid look-ahead;
   rebalanced each January. Only for the window where NSE P/E data exists (archive files from 2012-02; L51). Compared with
   (2) and (1) over the same window. Known: P/E basis break Mar-2021.
5. **New money to the most-underweight asset (SIP):** ₹10,000/month SIP, 70/20/10 targets, each month's contribution goes
   entirely to the asset furthest below its target weight; no selling ever. Compared with SIP into (1) and SIP + yearly
   rebalance (2). (Lump-sum version not meaningful.)
6. **Reference: 50/50 equity/gold rebalanced every January.**

### Metrics
CAGR (lump sum) / XIRR (SIP); worst drawdown (month-end, peak-to-trough) in % and in rupees on ₹10 lakh; months from peak
to full recovery for the worst drawdown; worst rolling 5-yr CAGR; % of rolling 5-yr windows (monthly starts) where the
strategy beats 100% equity; longest underwater spell (months below a prior peak) as a behaviour proxy; annual volatility.

### Costs and taxes (simple, stated)
- Rebalancing trades cost 0.1% of turnover (brokerage/spread/stamp).
- Tax on rebalancing gains: equity LTCG 10% pre-Jul-2024 / 12.5% after (exemption ignored — conservative); gold and bonds
  taxed at 20% on realised gains (simplified long-term rate with indexation ignored); applied as a cash leakage at each
  rebalance, approximated as tax rate × realised gain using average cost per asset. 100% equity pays no tax (no sales).
  Final terminal value reported pre-liquidation-tax (same treatment for all), so the rebalancing tax drag is the cost
  difference. Pre-2018 equity LTCG was actually 0%; we use the conservative rates throughout and say so.

### Decision rule (fixed now)
A strategy is **"worth it vs 100% equity"** if, over the full common window, its worst drawdown is ≥ 15pp smaller AND its
CAGR (after costs/taxes) is no more than 1.0pp/yr lower AND its worst 5-yr rolling CAGR is not lower than 100% equity's.
Valuation tilt (4) additionally must beat fixed 70/20/10 (2) on CAGR or drawdown over its own window to count as adding
anything beyond plain rebalancing. Underweight-SIP (5) must beat SIP + yearly rebalance on XIRR or drawdown to count.

### Regime caveats stated in advance
- 2000–2026 included long rupee depreciation (~45 → ~92/USD), which inflated rupee gold returns; this need not repeat.
- Gold is near record highs at the end of the sample; end-point flatters gold-heavy strategies.
- One country, ~5 independent 5-yr windows; results are base rates, not predictions. Confidence capped at `single-source`
  unless every series is cross-checked.

---

## Deviations (written 2026-11-26 after probing data, BEFORE computing strategy results)
- **D1 Window 2006-04 → 2026-10 (246 months), not 2000/2003.** Binding constraint: the bond series. No public scriptable
  India 10-yr yield before 2011-12 (FRED INDIRLTLT01STM starts 2011-12; IMF host unreachable); AMFI fund NAVs (via
  api.mfapi.in) start 2006-04. A real gilt fund NAV is used instead of a yield model.
- **D2 Equity = UTI Nifty 50 Index Fund, regular plan, NAV (a total-return series after the fund's expense), not a TRI.**
  niftyindices TRI is browser-only (L51). This is ~0.6–0.7pp/yr below the index TR (see checks), i.e. it bakes in a
  regular-plan cost. Sensitivity with Sensex price + dividend yield is reported.
- **D3 Bonds = SBI 10-yr Constant Maturity Gilt Fund NAV (regular, after expense)**; the yield/duration model (D=7, C=60) is a
  cross-check from 2011-12 only. No extra bond cost added (already net).
- **D4 Gold = Yahoo GC=F (COMEX front futures, month-end) × Yahoo INR=X**, minus 0.5%/yr. Yahoo's monthly bars have gaps,
  so daily bars are used and the last close of each month taken. LBMA via FRED is discontinued (404); second source =
  World Bank Pink Sheet (LBMA PM monthly average) × FRED EXINUS (monthly average), which ends 2024-12 in the file we got.
- **D5 Cash** = Nippon India Liquid Fund NAV (face-value change chained out) and FRED 91-day T-bill from 2011-12; reference only.
- **D6 Valuation tilt** needs ≥24 months of expanding P/E history (P/E from 2012-02, `research_notes/Macro/ey_gap_test_outputs/monthly.csv`),
  so it runs 2014-01 → 2026-10, January resets.

## Results (computed 2026-11-26 by `tools/allocation/backtest.py`; raw data + `sources.json` (URLs, as_of 2026-11-26),
`results.json`, `monthly.csv` in `research_notes/Allocation/data/`)

### Main window 2006-04 → 2026-10, lump sum ₹10 lakh
| Strategy | CAGR | End ₹ | Worst DD | DD peak→trough | Peak→recovery | Longest underwater | Worst 5-yr CAGR | % 5-yr windows > 100% eq (n=187) | Vol | Tax paid |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 100% equity | 10.09% | 71.8L | −55.2% | 2007-12→2008-11 | 70 m (2013-10) | 69 m | −1.39% | — | 20.3% | 0 |
| 2 70/20/10 yearly | 10.89% | 83.3L | −38.2% | 2007-12→2008-10 | 21 m (2009-09) | 20 m | +3.98% | 33% | 14.4% | 3.08L |
| 3 70/20/10 ±5pp bands | 10.82% | 82.1L | −38.9% | 2007-12→2008-10 | 23 m (2009-11) | 22 m | +3.71% | 36% | 14.5% | 2.83L |
| 6 50/50 eq/gold yearly | 12.01% | 102.2L | −27.0% | 2007-12→2008-10 | 17 m (2009-05) | 18 m | +4.04% | 39% | 12.9% | 4.93L |

### Valuation tilt window 2014-01 → 2026-10 (n=94 5-yr windows)
| Strategy | CAGR | Worst DD | Worst 5-yr | % 5-yr > eq | Longest underwater |
|---|---|---|---|---|---|
| 1 100% equity | 11.92% | −29.4% | +1.16% | — | 17 m |
| 2 70/20/10 yearly | 11.84% | −18.6% | +4.06% | 29% | 16 m |
| 4 P/E tilt (60/70/80) | 11.33% | −15.1% | +4.98% | 26% | 16 m |
| control (post-hoc): fixed 66.9% eq (tilt's average) | 11.82% | −17.5% | +4.34% | — | — |
Equity weight set each January: 2014 70, 2015 60, 2016 70, 2017–2021 60, 2022 70, 2023 80, 2024 70, 2025 80, 2026 70.

### SIP ₹10,000/month, 2006-04 → 2026-10 (₹24.7L invested)
| SIP | XIRR | End ₹ | Max fall % | Max fall ₹ | Tax | Final weights eq/gold/bond |
|---|---|---|---|---|---|---|
| all equity | 10.53% | 81.8L | −32.2% | −13.1L | 0 | 100/0/0 |
| 70/20/10 split + January reset | 11.06% | 87.3L | −17.8% | −9.3L | 2.47L | 70/19/11 |
| 5 new money to most-underweight, no selling | **11.30%** | **89.9L** | −18.1% | −11.9L | 0 | 60/31/9 |

### Asset behaviour (same window)
Equity (UTI fund) 10.09%/yr; gold INR 13.19%/yr (USD gold 9.12% + rupee −3.73%/yr vs USD); bond fund 7.72%; liquid fund
7.04%. Monthly correlations: equity–gold −0.08, equity–bonds +0.08, gold–bonds +0.03. Calendar years: 2008 equity −52%,
gold +30%, bonds +17%; 2011 −25 / +30 / +8; 2013 +7 / −19 / +9; 2025 +12 / **+72** / +7.

### Cross-checks (two sources)
| Item | Source A | Source B | Verdict |
|---|---|---|---|
| Equity TR 2006-04→2026-10 | UTI Nifty fund 10.09% | HDFC Sensex fund 9.40%; Sensex price + DY (1.3% assumed pre-2012) 10.82%; Sensex price only 9.38% | Fund NAVs ~0.7–1.4pp below index TR = regular-plan expense + tracking; direction consistent |
| Equity 2012-02→2026-10 | Nifty price + NSE DY 11.88% | UTI fund 11.27% | 0.6pp fund drag |
| Gold INR 2006-04→2024-12 | Yahoo GC=F × INR=X 11.59% | World Bank LBMA PM avg × FRED EXINUS 11.95% | 0.4pp gap (month-end vs monthly-average endpoints); median level gap 1.5% → verified |
| Gold INR 2009-01→2026-10 vs domestic | computed (no duty) 12.59% | Nippon Gold BeES ETF (Yahoo, domestic, after duty & ~0.8% fee) 12.61% | Match: duty rising from ~1–2% (2009) to 6% (since Jul-2024) roughly offsets ETF fee. Duty path from memory (2%→10% in 2012–13, 12.5% 2019, 15% Jul-2022, 6% Jul-2024) — unverified |
| Gold level today | GC=F $3,742 (18-Nov) × 93.47 = ₹112,450/10g | IBJA 999 ₹122,982 (25-Nov, snapshot) | +9.4% ≈ 6% customs duty (+AIDC/cess) + a week's price move; L51's 16% gap came from gold-api ($3,568), which looks low vs GC=F — still unresolved |
| Bonds 2011-12→2026-10 | SBI 10-yr CM gilt fund 7.99% | yield model (FRED, D=7) 8.13% | 0.14pp → consistent (fund is after fees) |
| Cash 2011-12→2026-10 | Nippon liquid fund 6.95% | 91-day T-bill accrued 6.57% | consistent |
| USD/INR Oct-2026 | Yahoo 95.15 (month-end) | FRED 95.52 (monthly avg) | consistent (FBIL 92.49 on 25-Nov → rupee recovered in Nov) |

### Post-hoc sensitivities (NOT pre-registered; for honesty about the regime)
| Case | 100% eq CAGR / DD | 70/20/10 CAGR / DD / worst 5y | 50/50 CAGR / DD |
|---|---|---|---|
| Base | 10.09% / −55.2% | 10.89% / −38.2% / +3.98% | 12.01% / −27.0% |
| Gold cut to 7%/yr (≈ cash) | 10.09% / −55.2% | 9.71% / −39.1% / +2.86% | 9.02% / −29.3% |
| Equity = Sensex price + DY | 10.82% / −55.5% (underwater 33 m) | 11.46% / −36.4% / +4.83% | 12.44% / −25.8% |
| Start 2009-04 (after crash) | 12.05% / −29.4% | 11.88% / −18.6% / +4.00% | 12.52% / −15.6% |

## Verdict against the pre-registered rule (DD ≥15pp smaller AND CAGR cost ≤1.0pp AND worst 5-yr not lower)
- **2 70/20/10 yearly: PASS** (DD −17.0pp; CAGR +0.80pp; worst 5-yr +5.4pp). Survives the gold-at-7% sensitivity (−16.1pp,
  −0.38pp). Fails the 15pp gate if you start after the 2008 crash (−10.8pp) — the benefit is concentrated in rare crashes.
- **3 ±5pp bands: PASS** (−16.3pp, +0.73pp), but no better than yearly → no reason to prefer it.
- **6 50/50 equity/gold: PASS** (−28.2pp, +1.92pp) — the most gold-dependent: with gold at 7% the CAGR cost is 1.07pp → fails.
- **4 P/E tilt: literal PASS** on the extra rule (DD −15.1% beats 70/20/10's −18.6%), **but not adopted:** CAGR is lower than
  both alternatives, a fixed split at its own average equity weight (66.9%) gets −17.5% DD at +0.49pp more CAGR, the
  remaining edge rests on one episode (Mar-2020, when it sat at 60%), the window has ~2 independent 5-yr periods, and P/E showed
  no out-of-sample power in L51. Lesson for future rules: a timing rule must beat a fixed split *at the same average weight*.
- **5 new money to most-underweight: PASS** its rule (XIRR 11.30% vs 11.06% for SIP + yearly reset; tax 0 vs ₹2.47L). Part of
  the gain is that it drifted to 31% gold during a gold boom; once the pot is large, contributions cannot hold the targets.
- Caveats as pre-stated: rupee depreciation (−3.7%/yr) and a record gold run (+72% in 2025) flatter gold; tax simplified
  (debt-fund gains after Apr-2023 are slab-taxed, gold/bond 20% used throughout; equity 10%/12.5% with no ₹1–1.25L exemption);
  fund NAVs carry regular-plan fees (direct plans would add ~0.5–1pp to equity and bonds).

**Confidence:** `single-source` overall — gold and bonds are cross-checked (verified), equity uses one fund series with index
checks, P/E tilt is `unverified` (13-yr window).
