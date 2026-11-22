# Backtest: "Lazy Prices" out-of-sample replication — US small/mid caps, 10-Ks filed 2021–2023

*Roadmap stage 3 (signals). Method calibration, not stock picking. Research, not SEBI/SEC-registered advice.*
*Unlocks: a tested text-change detector for stage 2/3 (avoid flag), and the template for an Indian annual-report version.*

## 0. PRE-REGISTRATION (written 2026-11-22, before any similarity score or return was computed)

**Hypothesis (Cohen, Malloy & Nguyen 2020, memdb `insight:lazy-prices-filing-changes`):** firms whose 10-K text
changes a lot versus the prior year's 10-K underperform over the following ~6–18 months; there is no
announcement-day reaction.

| Item | Pre-registered choice |
|---|---|
| Universe | US operating companies filing a 10-K (not 10-K/A) in calendar 2021, 2022 or 2023 that also filed a 10-K 9–15 months earlier. Public float (dei `EntityPublicFloat`, cover page of the same 10-K) **$300M–$10B**. Excluded: SIC 6000–6799 (banks, insurers, brokers, REITs, SPACs, funds), 4900–4999 (utilities), blank SIC. |
| Sample | If the full universe is too heavy: a seeded random sample of firms (seed 20261122) from the frame-based candidate list, taken in shuffled order until ≥ 800 eligible firm-years per filing year; the draw order and every exclusion are logged. |
| Text | 10-K primary document only (no exhibits). HTML/iXBRL tags stripped (hidden `ix:header` removed), entities unescaped, lower-cased, tokens = alphabetic words ≥ 2 letters; numbers dropped. |
| Sections | (a) full text; (b) Item 1A Risk Factors; (c) Item 7 MD&A — extracted as the longest span between a section heading and the next item heading (skips the table of contents). A section shorter than 1,500 characters in either year → missing for that measure. |
| Similarity | **Cosine similarity of raw term-frequency vectors** (this year vs prior year). Secondary: Jaccard similarity of word sets. |
| Signal | Within each filing year, quintiles of similarity. **"Changers" = bottom quintile (least similar), "non-changers" = top quintile.** |
| Entry | Adjusted close on the first trading day **after** the 10-K filing date (EDGAR acceptance date). |
| Horizons | 3, 6, 12 months = 63, 126, 252 trading days. |
| **Primary metric** | **Full-text cosine, changers minus size-matched controls, 12-month return.** Expected sign: negative. |
| Controls | For each event, 5 random (seeded) firm-years from the same filing year's sample, **not** in the event's own quintile group, market cap at entry within ×0.6–×1.67, with price data over the same calendar window (return measured from the event's entry date). |
| Secondary | Same at 3/6 m; non-changers vs controls; changers − non-changers spread; Item 1A and Item 7 cosine; Jaccard (full); per filing year. Six-plus secondary tests → treat any lone secondary "hit" as a hypothesis only. |
| Stats | Mean, median, 1/99% winsorised mean, hit rate, naive t; **95% bootstrap CI resampling filing months** (2,000 draws). |
| Costs | 0.5% round-trip. For the avoid use, the benefit of skipping a changer = −(excess return); cost-adjusted benefit = −excess − 0.5%. |
| **Decision rule** | Call it an edge only if the primary metric has **t ≤ −3, or its 95% month-bootstrap CI lies entirely below −0.5%** (i.e. excludes zero after costs). Otherwise "not proven" (if negative) or "rejected" (if ≥ 0 with CI excluding the paper-sized effect). |
| Survivorship | Firms with no Yahoo series or series ending inside the window are audited via EDGAR submissions: 8-K item 1.03 (bankruptcy), merger forms (DEFM14A / SC TO-T / SC 14D9 / 25-NSE / Form 15). Report counts by quintile and a bound. |
| Use if it works | Long-only: an **avoid / look-harder list** (bottom-quintile changers for 12 months after the 10-K). Shorting is out of scope. |

What would falsify it for us: primary-metric mean ≥ 0, or CI including zero after costs.

**Deviations logged before any return was computed (2026-11-22):**
1. Data-quality exclusion: firm-years where either primary document is < 50,000 characters after stripping
   (stub/wrapper primary documents whose real 10-K sits in an exhibit) are dropped — their "similarity" is an
   artifact, not a text change.
2. Firms whose CIK has no current ticker in EDGAR (mostly acquired/delisted later) get their old trading symbol
   from the 10-K cover page ("Trading Symbol(s)" table); used only if the market-cap identity check passes
   (cover shares × Yahoo close on entry day within 0.2–30× public float).
3. Observation (no change to the rule): raw-TF full-text cosine is compressed near 1 (median ≈ 0.998, stop-words
   dominate), as in the original paper's measure. Quintiles still rank firms; Jaccard is the less
   stop-word-dominated secondary.

---
*Everything below was written after the returns were computed (2026-11-22).*

## Verdict (short)
**NOT PROVEN by the pre-registered rule — direction confirmed, edge not.** Full-text cosine "changers" (bottom
quintile) earned **−7.3% vs size-matched controls over 12 months** (median −14.3%, hit rate 38%, naive t −2.53,
95% filing-month bootstrap CI **−14.1% to +1.0%**). The rule needed t ≤ −3 or a CI wholly below −0.5%; it got neither.
The shape matches the paper: almost nothing at 3 months (−0.6%), −1.3% at 6, −7.3% at 12 — slow drift, no reversal
in the window. The Jaccard version (secondary) was a bit stronger (−8.7%, t −3.08, CI −15.4 to +0.7).
**But about half the raw effect comes from one obvious group: first 10-Ks after a de-SPAC merger** (79 of 634
changers, 12%), where the "text change" is a whole new business and the stocks crashed in 2021–22. With de-SPACs
removed (exploratory), primary changers = −3.2% (CI −9.9 to +5.4). Removing biotech as well (an exploratory
sector-mix fix) brings it back to −7.2% (t −2.7) cosine / −9.5% (t −3.6) Jaccard. Those are post-hoc cuts, so they
are only hypotheses for a fresh test.
**Unexpected (secondary):** in Item 1A Risk Factors the effect ran *backwards*. Firms whose risk factors barely
changed did worst (−11.5% at 12 m, t −5.1). This survives removing de-SPACs and biotech (−10.6%, t −4.5), but it
contradicts the paper's strongest result and was not the hypothesis. Treat it as a new hypothesis ("stale,
copy-pasted risk factors") to test on fresh data, not as a finding.

## 1. Data actually used
| Item | Result |
|---|---|
| Candidates | 3,149 CIKs with any dei `EntityPublicFloat` in $300M–$10B (frames CY2019Q4I–CY2023Q3I); shuffled (seed 20261122); 2,340 processed in that order until every year had ≥ 950 eligible firm-years |
| Eligible firm-years | **3,167** (2021: 950, 2022: 1,145, 2023: 1,072); 3 dropped as stub primary docs → **3,164** scored |
| Documents | 4,706 10-K primary documents (current + prior), 0 download failures, ~4 req/s; stripped text 528 MB gz (scratch) |
| Sections found | Item 1A in both years: 2,706 firm-years (smaller reporting companies may omit it); Item 7: 3,027 |
| Prices | Yahoo v8: 2,372 firm-years usable (75%). 113 had no ticker at all; 598 had no Yahoo series (584 of them via an old ticker recovered from the 10-K cover — Yahoo drops delisted symbols); 61 no trading at entry; 20 failed the market-cap identity check |
| Events | Primary: 421 changers (Q1), 489 non-changers (Q5); 419/421 and 489/489 got 5 size-matched controls; 32 filing months |

## 2. Primary and main secondary results (excess vs 5 size-matched controls; full sample)
| Measure / group | 3 m | 6 m | 12 m mean [95% CI] | 12 m median | hit | t |
|---|---|---|---|---|---|---|
| **cos_full Q1 changers (PRIMARY)** | −0.6% | −1.3% | **−7.3% [−14.1, +1.0]** | −14.3% | 38.4% | −2.53 |
| cos_full Q5 non-changers | +0.4% | −0.1% | +0.9% [−5.6, +8.0] | −0.7% | 48.9% | +0.42 |
| cos_full Q1 − Q5 (excess) | −1.0% | −1.1% | −8.2% [−18.3, +2.8] | | | |
| jac_full Q1 | −3.3% [−5.5, −0.7] | −4.6% | −8.7% [−15.4, +0.7] | −15.3% | 38.2% | −3.08 |
| jac_full Q5 | +0.2% | +1.7% | +3.0% [−3.5, +8.0] | +1.0% | 50.9% | +1.36 |
| jac_full Q1 − Q5 (excess) | −3.5% | −6.2% | −11.6% [−19.5, −0.0] | | | |
| cos_1a Q1 (risk factors changed) | +1.7% | +1.0% | +2.5% [−3.8, +10.5] | −4.0% | 46.9% | +0.86 |
| cos_1a Q5 (risk factors unchanged) | −1.9% | −5.2% [−7.1, −2.8] | **−11.5% [−17.5, −6.6]** | −15.0% | 37.1% | −5.12 |
| jac_1a Q1 | +0.1% | −0.2% | −3.1% [−7.6, +4.1] | −8.0% | 41.8% | −1.14 |
| cos_7 Q1 (MD&A changed) | −0.4% | +0.8% | −1.5% [−12.4, +8.5] | −5.9% | 42.5% | −0.41 |
| jac_7 Q1 | −1.5% | −1.4% | −4.3% [−9.4, +1.4] | −8.7% | 44.2% | −1.51 |

Primary by filing year (12 m): 2021 −7.4% (t −1.8), 2022 −15.7% (t −3.1), 2023 +1.5% (t +0.3). The effect is
mostly a 2022-filings story, which was the de-SPAC / speculative-growth crash.
Cost: the avoid "benefit" = −excess − 0.5% = +6.8% at 12 m — but its CI includes zero, so it is not bankable.

## 3. Exploratory robustness (NOT pre-registered — hypotheses only)
| Variant (12 m, Q1 vs controls) | cos_full | jac_full | cos_1a Q5 (unchanged RF) |
|---|---|---|---|
| Full sample (pre-registered) | −7.3% [−14.1, +1.0] t −2.5 | −8.7% [−15.4, +0.7] t −3.1 | −11.5% t −5.1 |
| Ex-biotech (SIC 2834/35/36, 8731) | −10.1% [−16.3, −2.3] t −3.7 | −12.8% t −4.8 | −5.1% t −2.3 |
| Ex-de-SPAC (prior 10-K was a blank-check shell; 117 firm-years) | −3.2% [−9.9, +5.4] t −1.2 | −7.8% [−13.4, +0.4] t −2.9 | −13.7% t −5.6 |
| Ex-de-SPAC and ex-biotech | −7.2% [−13.6, −0.3] t −2.7 | −9.5% [−16.5, −2.1] t −3.6 | −10.6% t −4.5 |
Why biotech matters: controls are size-matched but not sector-matched. Biotech fell hard in 2021–23 and makes up
25% of the cos_full and cos_1a "non-changer" quintiles (biotech risk-factor sections are long and boilerplate,
so they change little) against 11% of changers. That pushes cross-sector comparisons around. A sector-matched
control is the right fix for v2.
de-SPAC flag: `s6_despac_flag.py` (prior-year 10-K mentions "blank check company" or "special purpose
acquisition" in its first 40k characters). 79 of the 117 flagged firm-years fall in the cosine bottom quintile.

## 4. Survivorship audit (EDGAR events after the filing date, by primary quintile)
Firm-years without usable 12-month prices: Q1 213, Q2 162, Q3 156, Q4 119, Q5 142.
| Quintile | merger/tender | bankrupt (8-K 1.03) | delist/deregister | unexplained |
|---|---|---|---|---|
| Q1 changers | 125 | **42** | 32 | 14 |
| Q5 non-changers | 120 | 11 | 9 | 2 |
| All (3,164) | 590 | 110 | 68 | 24 |
Changers had **4× the later bankruptcies** of non-changers (6.6% vs 1.7% of firm-years; some of these came after the
12-month window). Mergers are evenly spread. So the survivors-only sample probably *understates* how badly changers
do. Bound for the primary metric: missing acquired firms at +25% excess and bankrupt ones at −80%, with the same
treatment applied to the universe-wide control pool → **about −7.1%**. Bankrupt at 0 (failure after the
window) → −4.5%. Acquired at 0 → −7.4%. Survivorship does not change the verdict either way.

## 5. Caveats
1. **Concentrated filing dates.** Most 10-Ks are filed in February–March, so the 32 filing-month clusters are
   unequal and a few months dominate. The bootstrap CIs are wide and some per-year CIs are lopsided. Read the CIs,
   not the t-stats.
2. Three filing years and one regime (the 2021 speculative peak, the 2022 crash, the 2023 recovery). The paper
   covers 1995–2014.
3. Raw term-frequency cosine is dominated by stop-words (median 0.998). The paper's other measures (min-edit,
   simple) were not run. Jaccard (sets) behaved more like the paper.
4. Section extraction uses the longest heading-to-heading span. A cross-reference ("see Item 1A Risk Factors")
   can extend a span a little. Not hand-checked beyond spot tests.
5. Controls are size-matched only (no sector, momentum or value matching), and there is no factor regression.
6. One firm can appear up to 3 times (one per year). The month bootstrap does not cluster by firm.
7. Costs: 0.5% round trip applied to the avoid benefit only. Shorting is out of scope.

## 6. What this means for us (edge check)
- **The edge is not proven for the plain public rule.** The direction and the slow 6–12-month build-up both
  replicate, but the effect is smaller and noisier than the paper's and depends heavily on the de-SPAC crash.
  Don't add "low 10-K similarity" as a hard filter.
- **Usable now, long-only (judgment flags, not rules):**
  1. "First 10-K after a de-SPAC or other business transformation" → treat as an avoid / look-harder case
     (this is an obvious base-rate point, not a text edge).
  2. Bottom-quintile Jaccard similarity → a *reason to read the diff* (what changed: CEO/CFO, litigation, going
     concern, new risk language), in line with the paper's finding that those changes carry the information. It
     goes in the stage-4 research queue and is not an automatic exit.
- **Edge logic:** the text diff is cheap to compute, but few investors read it — the inattention premium (memdb
  `insight:lit-inattention-premium-synthesis`). In US mid-caps it may now be arbitraged by NLP funds. In India
  annual reports are PDFs, not machine-tagged, and coverage is thin. That is where an edge is more plausible.
- **Next (pre-register before looking):** v2 on fresh data — 10-Ks filed 2024 to mid-2025 (12-month windows
  complete by 2026-11). Primary = Jaccard full text, ex-de-SPAC, **sector-matched** (2-digit SIC) size controls. Add
  the "stale risk factors" (cos_1a top quintile) hypothesis as a separately registered second test.

## 7. Indian version — feasibility
- **Source:** annual reports are PDFs on NSE (corporate filings → annual reports) and BSE (AnnualReport archive).
  `tools/nse_fetch.py` / `tools/bse_fetch.py` don't fetch annual reports yet (an endpoint needs adding). `pdftotext`
  is installed here. Typical PDFs are 5–30 MB. Some are scanned and would need OCR (`pdftotext` returns little
  text for those, which is easy to detect).
- **Sections:** SEBI LODR Reg 34 / Schedule V requires an **MD&A** (including "risks and concerns") and a
  corporate-governance report. There is no standardised "Item 1A", so diff the MD&A plus the directors' report
  plus the auditor's report and CARO, and skip the financial statements.
- **Watch for template breaks:** BRSR became mandatory for the top 1,000 firms in FY2022-23, which creates a
  false "change" for every firm that year. Exclude BRSR pages, or diff with a section-aware parser.
- **Timing:** entry = the exchange submission date of the annual report (on or before the AGM notice), not the
  financial year end. Prices from Yahoo `.NS`, with the same size-matched-control method as the PEAD v2 work.
- **Cost:** roughly 1,500 firms × 2 years × ~10 MB ≈ 30 GB of downloads. That is too heavy for a sandbox session
  and belongs on the Pi pipeline (stage 1). A pilot of 200 firms × FY22→FY23→FY24 is feasible in one session.

## 8. Reproduce
Scripts (standard library only): `/home/user/fein/tools/backtests/lazy_prices_us/`
`s1_universe.py` → `s2_docs.py` → `s3_similarity.py` → `s4_prices.py --file tickers.txt` → `s4b_old_tickers.py`
(+ `s4_prices.py --file old_tickers.txt`) → `s6_despac_flag.py` → `s5_analyze.py`
[`--exclude-bio`] [`--exclude-despac`]. Helpers: `common.py`, `textutil.py`.
Data: `/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_lazy/`
(`firmyears.tsv`, `sims.tsv`, `results*.json|txt`, `despac.tsv`, `docs/`, `prices/`). Scratch data is temporary.
A full rerun takes about 1 hour (submissions ~20 min, documents ~20 min, Yahoo ~20 min).

Sources: https://data.sec.gov/api/xbrl/frames/dei/EntityPublicFloat/USD/CY2020Q2I.json (and other quarters);
https://data.sec.gov/submissions/ ; https://www.sec.gov/Archives/edgar/data/ (10-K primary documents);
https://query1.finance.yahoo.com/v8/finance/chart/ ; Cohen, Malloy & Nguyen (2020) J. Finance 75(3) / NBER w25084
(memdb `insight:lazy-prices-filing-changes`).
