# Backtest: "Lazy Prices" v2 — PRE-REGISTERED fresh-data test, US small/mid caps, 10-Ks filed 2024-01 → 2025-06

*Roadmap stage 3 (signals). Method calibration, not stock picking. Research, not SEBI/SEC-registered advice.*
*Builds on v1 (`research_notes/Backtests/lazy_prices_us.md`, lesson L29). Unlocks: either a proven stage-2/3
"avoid / look-harder" flag from 10-K text change, or a clean "not proven" that retires the plain US version and
moves the idea to the Indian annual-report test (v1 §7).*

## 0. PRE-REGISTRATION (written 2026-11-22, before any v2 firm-year was sampled, any v2 similarity score or any v2 return was computed)

Nothing in v2 has been computed when this section is written. v1 data (2021–23 filings) is used only as a
download cache (identical documents / price series are not re-fetched). Every choice below is fixed; any later
change is logged under "Deviations" with a date and the reason, and marked as made before or after returns.

### Hypotheses
- **H1 (primary, Lazy Prices):** firms whose 10-K full text changes most versus the prior-year 10-K (bottom
  quintile of full-text **Jaccard** similarity within filing year) underperform sector-and-size-matched controls
  over the 12 months after the filing. Expected sign: negative.
- **H2 (separate pre-registered test, "stale risk factors"):** firms whose Item 1A Risk Factors changed least
  (TOP quintile of Item 1A **Jaccard** similarity within filing year) underperform sector-and-size-matched
  controls over 12 months. Expected sign: negative. (Origin: v1 exploratory finding, cos_1a Q5 −11.5%, t −5.1;
  v2 tests it on Jaccard as specified, on data v1 never saw.)

### Fixed design
| Item | Pre-registered choice |
|---|---|
| Filings | 10-K (not 10-K/A) **filed 2024-01-01 → 2025-06-30** (EDGAR filing date), which also has a prior 10-K filed 270–460 days earlier. 12-month windows (252 trading days) end by ~2026-07; prices run to 2026-11-20. |
| Universe | US operating companies: public float (dei `EntityPublicFloat`, frames CY2022Q4I–CY2025Q1I; the float whose period end is 120–400 days before the filing date, latest such) **$300M–$10B**. Excluded: SIC 6000–6799 (banks, insurers, brokers, REITs, SPACs, funds), 4900–4999 (utilities), blank SIC. |
| Sample | Candidate CIKs = any float in $300M–$10B in those frames. Shuffled with **seed 2026112202** (a new seed, so the draw is not v1's). Processed in that order; every eligible firm-year of a processed firm is kept; stop when **≥ 2,000 eligible firm-years** have been collected (a firm can contribute a 2024 and a 2025 filing). Draw order and exclusions logged in `s1_log.json`. |
| Filing-year groups | "2024" = filed in calendar 2024; "2025" = filed 2025-01-01 → 2025-06-30. Quintiles are formed within each group. |
| Exclusions (fixed, applied **before** quintiles are formed) | (1) Either primary document < 50,000 characters after stripping (stub/wrapper). (2) **First 10-K after a de-SPAC / merger into a shell**: prior-year 10-K mentions "blank check company" or "special purpose acquisition" in its first 40,000 characters (v1 `s6_despac_flag.py`, unchanged). (3) Firm-years with no score for the measure (e.g. Item 1A shorter than 1,500 chars in either year) are absent from that measure's quintiles. |
| Text | 10-K primary document only. HTML/iXBRL stripped (hidden `ix:header` removed), unescaped, lower-cased, tokens = alphabetic words ≥ 2 letters. Same code as v1 (`textutil.py`). |
| Similarity | Jaccard of word sets, current vs prior 10-K: full text (H1), Item 1A (H2; v1 section extractor, longest heading-to-heading span, ≥ 1,500 chars in both years). |
| Entry | Adjusted close, first trading day **after** the filing date (none within 10 calendar days → not tradable, dropped). |
| Horizons | 3, 6, 12 months = 63 / 126 / 252 trading days. **12 months is the only decision horizon.** A series that ends inside the window uses its last price (delisting). |
| **Controls (primary)** | Pool = all scored firm-years with usable prices in the **same filing-year group**, **not in the event's own quintile** for that measure, different CIK. Market cap measured on the **event's** entry date (cover shares × unadjusted close). Tier A: **same 2-digit SIC** and mcap within **×0.5–×2.0**; if ≥ 3 candidates, take up to **5 nearest in log market cap**. Tier B (fallback, only if Tier A < 3): **same 1-digit SIC** (first digit), same size band, up to 5 nearest. If Tier B < 3 → event has no control and is dropped (counted). The share of events matched at each tier is reported. Excess return = event return − mean of its controls' returns over the same dates. |
| Primary metric (H1) | Mean 12-month excess return of jac_full bottom-quintile events vs sector-size controls. |
| Primary metric (H2) | Mean 12-month excess return of jac_1a top-quintile events vs sector-size controls. |
| Stats | Mean, median, 1/99% winsorised mean, hit rate, naive t; **95% bootstrap CI resampling filing months** (2,000 draws, as v1). |
| Costs | 0.5% round trip. Avoid benefit = −excess − 0.5%. |
| **Decision rule (each of H1, H2 separately)** | **"Proven avoid flag" only if t ≤ −3 OR the 95% filing-month bootstrap CI lies wholly below −0.5%** (upper bound < −0.5%). Otherwise "not proven" (mean < 0) or "rejected / no sign" (mean ≥ 0). No other result, horizon, subgroup or measure can upgrade a verdict. |
| Secondary (descriptive only, cannot change the verdict) | 3/6 m for both; the opposite quintile of each measure; Q1−Q5 spreads; full-text cosine Q1 and Item 1A cosine Q5 (v1's measures); v1-style size-only controls (5 random, ×0.6–×1.67) for comparability; vs IWM; per filing-year group; ex-biotech (SIC 2834/35/36, 8731). With ≥ 8 secondary cuts, a lone secondary "hit" is a hypothesis only. |
| Survivorship | Firm-years with no usable price series, or a series ending inside 252 days, are audited with EDGAR submissions after the filing date: 8-K item 1.03 (bankruptcy), merger forms (DEFM14A / PREM14A / DEFM14C / S-4 / SC TO-T / SC 14D9), delist/deregister (25 / 25-NSE / 15-*). Counted by quintile. **Bound (as v1):** missing firm-years imputed at −80% raw if bankrupt, +25% if merger/tender, 0% otherwise, with the same imputation applied to the universe-wide missing share on the control side; also reported with bankrupt = 0%. The bound is reported next to the verdict; it does not change the rule unless it flips the sign (then flagged). |
| Use if proven | Long-only avoid / look-harder list for 12 months after the 10-K. Shorting out of scope. |

What would falsify each hypothesis for us: mean ≥ 0, or CI including −0.5% / zero.

Known risks written in advance: (a) filing months are concentrated in Feb–Mar, so 18 month-clusters are very
unequal and CIs will be wide; (b) one regime (2024–25: AI-led large-cap market, small caps lagging); (c) sector
matching at 2-digit SIC may be coarse (SIC 28 mixes chemicals and pharma) and Tier-B fallback will be common in
thin sectors; (d) a firm may appear twice (2024 and 2025), not clustered by firm.

### Deviations (pre-run)
*(none yet)*

---
*Everything below this line is written after the v2 returns were computed.*

## Verdicts (short)
| Test (pre-registered, 12 m, vs sector-and-size controls) | n | Mean [95% month-bootstrap CI] | Median | Hit | t | Verdict |
|---|---|---|---|---|---|---|
| **H1** full-text Jaccard, bottom quintile (changers) | 320 | **−1.4% [−10.6, +16.9]** | −10.5% | 39.7% | −0.25 | **NOT PROVEN** |
| **H2** Item 1A Jaccard, top quintile (stale risk factors) | 290 | **+0.5% [−14.0, +4.4]** | −4.8% | 46.2% | +0.13 | **REJECTED / NO SIGN** |

Neither hypothesis comes close to the bar (t ≤ −3 or CI wholly below −0.5%). Avoid benefit after 0.5% costs:
H1 +0.9%, H2 −1.0%. On fresh 2024–25 data, with de-SPACs removed in advance and sector-matched controls, the v1
effect (−7.3% cosine / −8.7% Jaccard) mostly disappears, and v1's "stale risk factors" result does not
replicate. v1's exact measure for it (Item 1A cosine, top quintile) was **+10.7%** vs sector-size controls here,
the opposite sign to v1's −11.5%. That points to v1's sector mix (25% biotech, controls not sector-matched)
rather than a real effect.

## 1. Data actually used
| Item | Result |
|---|---|
| Candidates | 2,235 CIKs with a dei `EntityPublicFloat` in $300M–$10B (frames CY2022Q4I–CY2025Q1I), shuffled with seed 2026112202; 1,797 processed in that order (515 excluded by SIC) until 2,000 eligible firm-years |
| Eligible firm-years | **2,000** (filed 2024: 1,085; filed 2025 H1: 915). 3,215 10-K primary documents (current + prior), 0 download failures (1,727 reused from the v1 cache, 1,488 fetched at ~4 req/s) |
| Pre-registered exclusions | 2 stub documents (< 50k chars); **27 first-10-Ks-after-de-SPAC** (v1 had 117, because the SPAC wave was over) → **1,971 analysed** (2024: 1,067; 2025: 904) |
| Sections | Item 1A scored in both years: 1,672 firm-years; Item 7: 1,888 |
| Prices (Yahoo v8) | 1,675 usable (85%). 45 had no ticker; 222 had no series (212 of them were old tickers recovered from the 10-K cover, because Yahoo drops delisted symbols); 20 had no trading at entry; 9 failed the market-cap identity check |
| Controls | H1: 259/322 events matched on 2-digit SIC (80%), 61 on the 1-digit fallback (19%), 2 unmatched. H2: 213/292 2-digit, 77 1-digit, 2 none |
| Filing months | Heavily concentrated: Feb 2024 + Feb 2025 = 211 of 320 H1 events. 15 month-clusters in total |

## 2. Results (12 m unless stated; excess vs 5 sector-size controls; full analysed sample)
| Measure / group | 3 m | 6 m | 12 m mean [CI] | 12 m median | wins. mean | hit | t |
|---|---|---|---|---|---|---|---|
| **jac_full Q1 (H1)** | +2.7% | +2.9% | **−1.4% [−10.6, +16.9]** | −10.5% [−15.0, +5.0] | −4.0% | 39.7% | −0.25 |
| jac_full Q5 (least change) | +2.1% | +3.0% | +6.7% [−13.5, +14.1] | +0.7% | +5.6% | 51.2% | +1.72 |
| jac_full Q1 − Q5 (excess) | +0.7% | −0.1% | −8.1% [−20.5, +19.7] | | | | |
| **jac_1a Q5 (H2)** | +0.9% | +4.5% | **+0.5% [−14.0, +4.4]** | −4.8% [−13.6, −1.1] | +0.3% | 46.2% | +0.13 |
| jac_1a Q1 (risk factors changed) | +1.7% | +1.7% | −3.0% [−11.5, +5.3] | −10.3% | −3.1% | 39.9% | −0.73 |
| cos_full Q1 (v1 primary) | +3.1% | +3.4% | +5.3% [−3.6, +19.2] | −4.8% | +3.4% | 44.3% | +0.89 |
| cos_1a Q5 (v1 "stale RF") | +1.1% | +4.8% | **+10.7% [−7.5, +19.1]** | −1.1% | +7.1% | 49.5% | +2.10 |
| cos_1a Q1 | +3.4% | −0.6% | −5.3% [−11.4, +1.0] | −12.8% | −5.5% | 39.8% | −1.29 |
| cos_7 Q1 (MD&A changed) | +1.0% | −0.1% | −9.5% [−31.5, +3.9] | −15.7% | −10.7% | 38.7% | −2.13 |
| jac_7 Q1 | +1.9% | +5.5% | +3.4% [−8.2, +27.4] | −6.0% | +1.0% | 45.6% | +0.58 |

Other secondary cuts (none changes a verdict):
- **H1 vs size-only controls (v1 method):** −1.1% (t −0.20). Vs IWM: +0.6%. Raw 12 m return of changers: +14.6% mean, −5.2% median.
- **H1 by filing year:** 2024 +1.3% (t +0.2); 2025 −4.2% (t −0.5). **H2:** 2024 −1.4%; 2025 +2.7%.
- **Ex-biotech:** H1 −1.3% (t −0.2), H2 +2.3% (t +0.5).
- **Outliers:** the H1 mean is pulled up by a handful of huge winners. ASTS was about +970% from its 2024
  filing, and BE, UUUU, COGT and AGX each rose about +300–540% from their 2025 filings (spot-checked; the
  moves are real, not split errors). This is why the winsorised mean (−4.0%) and the median (−10.5%) sit well
  below the mean.

**Pattern worth noting (hypothesis only):** in both v1 and v2, changers have a low median excess (v1 −14%, v2
−10.5%) and a low hit rate (38–40%, against ~50% for non-changers), while their mean is rescued by a fat right
tail. Big text changes look less like "drifts down" and more like "lottery ticket": most underperform, a few
explode. That fits the stage-4 use (read the diff, don't auto-avoid). A mean-based avoid rule would have thrown
away the winners. This was not the pre-registered metric, so it is not a finding.

cos_7 Q1 (−9.5%, t −2.1) comes almost entirely from 2025 filings (−24.7%). It is one of more than 20 secondary
cells, so it is noise until a pre-registered test says otherwise. Do not chase it.

## 3. Survivorship audit (EDGAR events after the filing date; firm-years without usable prices)
| jac_full quintile | missing prices | merger/tender | bankrupt (8-K 1.03) | delist/dereg | unexplained |
|---|---|---|---|---|---|
| Q1 changers | 73 (18.5%) | 47 | **7** | 13 | 6 |
| Q2 | 65 | 53 | 2 | 7 | 3 |
| Q3 | 56 | 47 | 2 | 4 | 3 |
| Q4 | 56 | 45 | 3 | 8 | 0 |
| Q5 non-changers | 46 (11.7%) | 38 | 2 | 4 | 2 |
No usable series ended inside the window (Yahoo drops delisted symbols entirely, so they show as "no series").
Changers again have more missing prices and more bankruptcies (7 vs 2: the same direction as v1's 4×, but the
counts are tiny). **Bounds** (missing firms imputed at bankrupt −80% / merger +25% / other 0%, events within 365
days, with the same treatment applied to the universe-wide missing share on the control side):
**H1 −2.5%** (bankrupt at 0: −1.7%); **H2 +6.6%** (+6.4%). Neither bound comes near the bar or flips a
verdict. Item 1A Q5 had 1 bankruptcy; Q1 had 6.

## 4. What this means (edge check)
- **H1 (Lazy Prices, plain US rule): not proven, now twice.** v1 was −7.3% with t −2.5, half of it de-SPAC.
  v2, on fresh data, with de-SPACs removed and sector-matched controls, is −1.4% with t −0.25. Whatever edge
  CMN (2020) found in 1995–2014, the public version in US $300M–$10B names in 2024–25 is not one we can bank.
  It may well be arbitraged by NLP funds. **Retire it as a mechanical filter or rule.**
- **H2 (stale risk factors): rejected.** v1's −11.5% did not replicate; its own measure now reads +10.7%. Mark
  v1's "unchanged risk factors underperform" as superseded (most likely a biotech / sector-mix artifact).
- **What survives, as judgment and not as an edge:** (a) the first 10-K after a de-SPAC or other transformation
  is a base-rate red flag (v1; only 27 cases in v2, so it was not re-tested); (b) a big text change is a reason to
  *read the diff* in stage 4. It is not an auto-avoid, because changers are skewed: low median, a few huge
  winners.
- **Where an edge could still exist:** Indian annual reports (PDFs, untagged, thin coverage), per v1 §7. That
  is the logical next text-change test (pilot of 200 firms, FY22→FY24), pre-registered the same way.
- **Lesson for the system:** the second fresh-data, pre-registered test shrank a "near-significant" v1
  effect to zero. Only effects that pass a fresh pre-registered test get promoted.

## 5. Caveats
1. Only 15 filing-month clusters, and two Februaries hold about two-thirds of events, so the bootstrap CIs are
   wide and lopsided. The point estimates are far from the bar anyway.
2. One regime: 2024–25, when the market was led by AI and mega-caps, small caps lagged, and there was a
   speculative rally in space, nuclear and quantum names (several of the right-tail outliers).
3. 2-digit SIC is coarse (SIC 28 mixes chemicals and pharma); 19% (H1) and 26% (H2) of events used the 1-digit fallback.
4. No firm clustering (a firm can appear in 2024 and 2025). No factor regression. Costs apply only to the avoid
   benefit.
5. Only full text, Item 1A and Item 7 word-set and term-frequency measures. CMN's min-edit and "simple" measures
   were not run. Specific-content diffs (e.g. new litigation or going-concern language) were not tested.

## Deviations (post-run log)
None. Implementation notes (consistent with §0, decided before returns): ties in "nearest market cap" are
broken by accession number for determinism; the de-SPAC regex is v1's unchanged; the v1 download cache was
hard-linked so that identical accessions and tickers were not re-fetched (the Yahoo cache was fetched
2026-11-22, range 2020-12-01 to 2026-11-20).

## Reproduce
Scripts (standard library only): `/home/user/fein/tools/backtests/lazy_prices_us_v2/`
`s1_universe.py` → `s2_docs.py` → `s3_similarity.py` → `s6_despac_flag.py` → `s4_prices.py <dir> --file tickers.txt`
→ `s4b_old_tickers.py` (+ `s4_prices.py <dir> --file old_tickers.txt`) → `s5_analyze.py` [`--exclude-bio`].
Data (temporary scratch): `/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_lazy_v2/`
(`firmyears.tsv`, `sims.tsv`, `despac.tsv`, `results_v2*.json|txt`, `s1_log.json`, `docs/`, `prices/`).
Runtime about 25 minutes with the v1 cache.

Sources: https://data.sec.gov/api/xbrl/frames/dei/EntityPublicFloat/USD/CY2024Q2I.json (and other quarters);
https://data.sec.gov/submissions/ ; https://www.sec.gov/Archives/edgar/data/ ; https://query1.finance.yahoo.com/v8/finance/chart/ ;
Cohen, Malloy & Nguyen (2020) J. Finance 75(3) / NBER w25084 (memdb `insight:lazy-prices-filing-changes`); v1 memdb `insight:bt-lazy-prices-us-2021-23`.
