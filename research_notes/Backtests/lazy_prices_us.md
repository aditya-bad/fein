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

