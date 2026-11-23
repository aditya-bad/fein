# Backtest PILOT: Indian annual-report text change ("Lazy Prices, India"), FY22→FY23 and FY23→FY24

*Roadmap stage 3 (signals). Method calibration, not stock picking. Research, not SEBI-registered advice.*
*Builds on `lazy_prices_us.md` §7 (India feasibility) and `lazy_prices_us_v2.md` (method, controls, lottery-profile
caution); lessons L27–L30. Why India: annual reports here are long, under-read PDFs (L30: edges are likelier in
information that is costly to process). Unlocks: a go/no-go for a full multi-year run on the Pi pipeline (stage 1),
and, whatever the verdict, a working annual-report fetcher + section parser for stage-4 deep dives.*

## Step 0 — feasibility (done 2026-11-22, before the pre-registration below; no returns looked at)
- **Listing + dates:** `api/annual-reports?index=equities&symbol=X` on www.nseindia.in answers JSON without
  cookies (same headers as the other `/api/corporate*` calls). One row per financial year (FY21–FY26 for the five
  test firms), file on `nsearchives.nseindia.in/annual_reports/`. `broadcast_dttm` is filled only from FY24/FY25 on;
  for older rows it is "-", but the file name carries the upload stamp (`..._DDMMYYYYhhmmss`) and, on older ZIPs, a
  second dissemination stamp (`_MMDDYYYYhhmmss`). `submitted` = broadcast time, else the later stamp.
  New command: `python3 tools/nse_fetch.py annual_reports SYMBOL [--download DIR]`. The endpoint does not accept a
  date range without a symbol (tested: non-JSON reply), so a company list has to come from elsewhere (below).
- **Files:** FY22/FY23 are ZIPs holding one PDF; FY24+ plain PDFs. Sizes on the 5 firms × 3 years: 4–48 MB
  (median ~7 MB). Download 2–8 s each at ≥1.5 s spacing; `pdftotext` (reading order) < 1 s per report; all 15
  reports were text PDFs (no OCR needed), 177–374 pages, 0.8–1.0 M characters.
- **Sections** (`tools/backtests/india_ar_text/sections.py`): pages are labelled from heading-like lines in their
  first 12 lines (MD&A, corporate governance, BRSR, board's report, auditor, financial statements, AGM notice),
  unlabelled pages inherit; contents pages (≥ 3 labels) reset. MD&A = longest contiguous MD&A run. Auditor
  section = text from the first "Independent Auditor's Report" heading that is followed by "To the Members" up to
  the first stand-alone "Balance Sheet" heading line (standalone report + Annexure A/B incl. CARO).
  Result on 15 reports (KPITTECH, 20MICRONS, SANSERA, APARINDS, VGUARD × FY22–24): MD&A found 13/15 (APAR FY22 and
  FY24 missed: MD&A folded into other sections), auditor+CARO found cleanly 14/15 (APAR FY23 missed the start and
  ran to the 200k cap), CARO marker present in 14/15 (KPIT FY22 CARO wording differs). BRSR pages detected and
  never used (0–84 pages per report; BRSR appears in FY23 for top-1000 firms → the template break §7 warned about
  is avoided by construction). Fixed quality gates below catch the failures.

## 0. PRE-REGISTRATION (written 2026-11-22, before the company frame was fetched, before any firm was sampled, any similarity score or any return was computed)

### Hypotheses
- **H1 (MD&A change):** firms whose MD&A changed most vs the prior year's report (bottom quintile of MD&A Jaccard
  word-set similarity, within pair-year) underperform sector-and-size-matched controls over 12 months. Sign: negative.
- **H2 (auditor + CARO change):** same with the auditor's report + CARO section (bottom quintile of AUD Jaccard).
  Sign: negative.
- **H3 (auditor-section change flag):** firm-years whose auditor section contains, for the first time vs the
  prior year, an emphasis of matter, a qualified / adverse / disclaimer opinion, a material uncertainty related to
  going concern, an ICFR material weakness, or a CARO adverse clause (default in repayment, cash losses, auditor
  resignation, short-term funds used long-term, CARO going-concern doubt, fraud noticed, undisputed statutory
  dues in arrears > 6 months) underperform controls over 12 months. Detected by keyword-in-sentence without a
  negator ("no", "not", "nil", "none") in the same sentence, current year vs prior year; **every flagged case is
  then checked by hand** (read the sentence); only confirmed new items count. Sign: negative.

### Fixed design
| Item | Pre-registered choice |
|---|---|
| Company frame | Every NSE symbol with ≥ 1 corporate announcement between **2023-06-01 and 2023-09-30** (all-company daily announcement feed). This is the set of firms listed in mid-2023, so firms that later merged, delisted or were suspended are in it (L27/L28: no survivors-only samples). |
| Sample order | Frame sorted, shuffled with **seed 2026112203**. Walked in that order. |
| Eligibility (firm level) | screener.in company page found; not financial (`solvency_screen.is_financial`: banks, NBFC, insurance, broking, housing finance); market cap **₹500–20,000 cr** at the last weekly price ≤ **2023-03-31** (screener market-cap-to-sales × TTM sales, as the solvency tests). |
| Text sample | The first **200 eligible** firms in walk order. For each: `annual_reports` list; per FY (FY22 = fromYr 2021, FY23 = 2022, FY24 = 2023) the earliest-submitted row. |
| Control pool | All eligible firms walked until **350 eligible** firms in total (the 200 text firms + the next 150, price data only). |
| Pairs | P1 = FY23 report vs FY22 report, P2 = FY24 vs FY23. A pair needs both reports downloaded and text-usable for the measure. |
| Text quality gates (per measure, both years) | MD&A ≥ 5,000 chars; AUD 10,000–150,000 chars (a hit on the 200k cap = failed extraction). Report < 50,000 chars in total = scanned / failed → unusable. Failure counts reported. |
| Similarity | Jaccard of lower-case alphabetic word sets (≥ 2 letters), current vs prior year, separately for MD&A (H1) and AUD (H2). |
| Quintiles | Within pair-year (P1, P2) across firms with a score for that measure. Bottom quintile = biggest change. |
| Entry | First screener weekly close dated **after** the current report's `submitted` date (no close within 21 days → not tradable, dropped). |
| Horizon | 12 months: last weekly close ≤ entry + 365 days. **12 months is the only decision horizon**; 6 months descriptive. A series that ends early uses its last close (merger / delisting), logged. |
| Controls | Pool = control-pool firms with a price at the event's entry, different firm, **not in the event's own quintile for that measure in that pair-year** (for H3: not flagged in that pair-year). Market cap measured on the event's entry date. Tier A: same screener **Sector**, mcap ×0.33–×3, up to 5 nearest in log mcap, ≥ 3 needed. Tier B: same **Broad Sector**, same band. Tier C: size only, ×0.5–×2, 5 nearest. Excess = event return − mean of controls' returns over the same weekly dates. Tier shares reported. |
| Stats | n, mean, median, 5/95% winsorised mean, hit rate (excess > 0), naive t, 95% bootstrap CI by firm (2,000 draws). Prices: screener weekly split/bonus-adjusted closes (dividends excluded, same for controls). |
| **Go / no-go rule (decided now)** | The pilot cannot prove a signal (≈ 40 events per quintile per pair-year; ≈ 70–80 in total). Its job is the effect size. **GO (full run: ≥ 1,000 firms, FY19→FY25, on the Pi pipeline)** if, for H1 or H2, the bottom quintile's 12-m excess has **winsorised mean ≤ −5% AND median < 0 AND t ≤ −1.5**; or, for H3, **≥ 10 confirmed flags with winsorised mean ≤ −10% AND median < 0**. Plus a feasibility condition: ≥ 75% of attempted report pairs text-usable for that measure. Otherwise **NO-GO**: the plain text-change idea is shelved in India too; the auditor-change list survives only as a judgment cue (read the auditor section during deep dives) if the case notes show it catches real trouble. No other cut can turn a no-go into a go. |
| Secondary (descriptive only) | Top quintile (stalest), Q1−Q5 spread, all events vs controls (calibration), per pair-year, 6-m horizon, raw returns. |

Known risks written in advance: (a) n is small: a single +500% winner can move a mean (L30 lottery profile), hence
the winsorised mean and median in the rule; (b) section extraction errors add noise that biases toward zero;
(c) two years of one regime (2023–25 Indian small/mid-cap boom, then the 2024-25 correction); (d) screener
weekly prices; (e) firms appear in both pairs (bootstrap by firm handles the clustering).

### Deviations (pre-run)
*(none yet)*

---
*Everything below this line is written after returns were computed.*
