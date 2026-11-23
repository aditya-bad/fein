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
- **D1 (2026-11-23, after ~140 text firms were downloaded, before any similarity score was looked at and before any
  return was computed).** (a) FY24 file names often have a 13-digit time stamp (`2908202422056`, no zero padding),
  which the first `_stamp` regex missed, so `submitted` was empty and those FY24 reports were skipped. Fixed: the
  first 8 digits give the date (time set to 00:00 when the stamp is short); skipped FY24 reports are fetched on the
  resumed walk. Entry is the first weekly close after the date, so the missing time does not matter.
  (b) Section parser tuned on the downloaded texts (extraction stats only, no scores or returns): MD&A wins when
  it shares a page head with another label ("Board's Report including MD&A", combined running headers); the contents
  page rule applies only to the first 20 pages; the auditor-report start must be followed by "To the Members"
  (also "To, The Members" / "TO THE MEMBERS") within 400 chars and by "we have audited" / "opinion" within 3,000;
  the contents-page skip needs a page number nearby; the end line also accepts "Revised", "as on" and "(contd.)".
  Effect on 385 reports: MD&A usable 86% (was ~75%), auditor+CARO usable 90% (was ~78%).

---
*Everything below this line is written after returns were computed.*

## Verdict (short)
**NO-GO.** No pre-registered test meets its go bar. The 12-month excess return is measured against
sector-and-size-matched controls; "wins." means the 5/95% winsorised mean.

| Test (12 m) | n | Mean [95% firm-bootstrap CI] | Wins. mean | Median | Hit | t | Go bar | Result |
|---|---|---|---|---|---|---|---|---|
| **H1** MD&A Jaccard, bottom quintile (big change) | 60 | −2.1% [−16.4, +14.7] | −4.1% | −16.8% | 37% | −0.30 | wins. ≤ −5%, median < 0, t ≤ −1.5 | **fail** (wins. and t miss the bar) |
| **H2** Auditor + CARO Jaccard, bottom quintile | 65 | −0.8% [−13.0, +11.9] | −3.7% | −10.0% | 42% | −0.12 | same | **fail** |
| **H3** new auditor-section adverse item (hand-checked) | 21 | **+7.7%** [−15.2, +34.4] | +4.8% | **+17.5%** | 52% | +0.60 | ≥ 10 flags, wins. ≤ −10%, median < 0 | **fail** (wrong sign) |
| Feasibility: share of attempted pairs usable | MD&A 298/385 = **77%**; auditor 319/385 = **83%** | | | | | | ≥ 75% | pass |

Calibration (descriptive): all scored events vs controls were −4.0% (MD&A sample, t −1.35) and −6.6% (auditor
sample, t −2.41, CI −12.2 to −1.1). The 200 text firms lagged the 150 control-only firms over these two years,
which is sampling noise in a small pool where single stocks move ±100%. **Relative to the other text firms**,
the big changers did *better*, not worse: MD&A Q1 was +1.9 pp vs all events, auditor Q1 +5.8 pp. So the
negative raw numbers in H1 and H2 are not a text-change effect.

## 1. Data actually used
- Frame: 2,021 NSE symbols with ≥ 1 announcement Jun–Sep 2023 (122 daily all-company feeds), seed 2026112203.
  Walked 810 symbols to reach 350 eligible. Exclusions: 298 outside ₹500–20,000 cr, 67 financial,
  39 with no market cap at 2023-03-31, and 4 with no screener page (VICEROY, DOLPHINOFF, SABTN, SICAL: stressed or
  suspended names, so a small survivorship leak at the screener step).
- Text firms: the first 200 eligible firms (median market cap ₹2,030 cr; mostly consumer discretionary 57,
  industrials 45, commodities 26, healthcare 22). Every one had an NSE annual-report list. 585 reports attempted:
  577 OK, 5 empty or scanned, 3 failed downloads. PDFs ran 6.9 MB median, 17.5 MB p90, 85 MB max, **5.1 GB
  downloaded in total**. Only gzip page text is kept (121 MB); every PDF was deleted straight after extraction.
  The whole walk (screener for 810 symbols + 585 report downloads) took about 1 h 15 min in one polite stream (≥ 1.5 s per request).
- Pairs: P1 (FY23 vs FY22) 188 attempted, P2 (FY24 vs FY23) 197. Of these, 142 / 156 had a usable MD&A in both
  years and 157 / 162 a usable auditor section. 375 firm-years carry at least one score, and all 375 were priced
  (screener weekly adjusted closes).
- Controls: 350-firm pool; Tier A (same sector) matched 95% of primary events (57/60, 60/65, 18/21).
- Delisted inside the window: only TATACOFFEE and TATASTLLP, both merged into parents, so their last price was
  used. Survivorship was handled by the frame (firms listed in mid-2023), but the pilot is too short and too
  mid-cap to contain real failures.

## 2. Results (12 m unless stated; excess vs sector-size controls)
| Cut | n | Mean | Wins. | Median | Hit | t | P1 / P2 mean |
|---|---|---|---|---|---|---|---|
| H1 MD&A Q1 (changers) | 60 | −2.1% | −4.1% | −16.8% | 37% | −0.30 | +4.9% / −8.8% |
| H1 at 6 m | 60 | −2.3% | −3.1% | −8.5% | 33% | −0.55 | |
| MD&A Q5 (stalest) | 59 | −2.7% | −3.2% | −5.2% | 39% | −0.42 | −10.6% / +4.5% |
| All MD&A-scored | 297 | −4.0% | −5.8% | −9.0% | 40% | −1.35 | −5.2% / −2.8% |
| H2 auditor Q1 (changers) | 65 | −0.8% | −3.7% | −10.0% | 42% | −0.12 | +7.2% / −8.6% |
| H2 at 6 m | 65 | −3.9% | −4.0% | −12.1% | 34% | −1.12 | |
| Auditor Q5 (stalest) ★ | 62 | **−15.2%** | −15.6% | −15.4% | 37% | **−2.54** (CI −27.4, −2.0) | −28.5% / −2.0% |
| All auditor-scored | 318 | −6.6% | −7.7% | −10.8% | 39% | −2.41 | −8.8% / −4.6% |
| H3 flags | 21 | +7.7% | +4.8% | +17.5% | 52% | +0.60 | +1.9% (14) / +19.2% (7) |
| H3 "trouble" items (post-hoc split) | 13 | +3.4% | | −10.3% | | | |
| H3 "technical" items (post-hoc split) | 8 | +14.6% | | +18.6% | | | |

★ Secondary, so it cannot change the verdict. Firms whose auditor + CARO text changed *least* lagged by −15%,
which is −8.6 pp below all auditor-scored events. Almost all of it came from P1 (2023-24: −28.5%) and almost
none from P2 (−2.0%). One period, 62 events, and the US "stale risk factors" idea already failed on fresh data
(L30). Treat it as a hypothesis, not a finding.

The lottery profile is back (L30). The changers' medians (−17% and −10%) are far below their means, and hit
rates are 37–42%. Single names range from −96% to +247% excess.

## 3. Auditor-section changes found, and what happened next (case notes)
The detector raised 36 sentences in 32 (firm, pair, category) items, and all were read by hand
(`india_annual_report_text_outputs/auditor_flags_checked.tsv`). **21 were confirmed** as new versus the prior
year. 11 were rejected:
- 4 items were already in the prior year but the detector missed them there: GREENPANEL, JAYNECOIND, and MTNL's
  P1 cash loss and P2 EoM.
- 3 cash losses were already reported the year before: BOSCH-HCIL, PANACEABIO, NETWORK18.
- 2 were boilerplate: SANGAMIND, and COHANCE (a sentence broken by a table).
- GTLINFRA's EoM *replaced* a qualified opinion, which is an upgrade.
- SHIVALIK's auditor left at the end of its statutory term.

12-month outcome, excess vs controls (raw return in brackets):

| Firm | Pair (entry) | New item | 12-m excess (raw) |
|---|---|---|---|
| VALIANTORG | FY23 (2023-08-25) | EoM: OCPS from a scheme not converted by the Feb-2022 deadline | **−77%** (−14%) |
| SATIA | FY23 (2023-09-08) | EoM: depreciation estimate changed (residual value 10%→5%) | **−73%** (−15%) |
| GRINFRA | FY23 (2023-09-08) | EoM: ongoing regulatory matter, sub-judice | **−65%** (+28%) |
| GHCL | FY23 (2023-09-08) | EoM: restatement (deferred tax on land revaluation; revenue reclassification) | **−50%** (+6%) |
| EXPLEOSOL | FY23 (2023-07-21) | EoM: amalgamation of four group companies | −47% (−21%) |
| POWERMECH | FY23 (2023-09-08) | EoM: Income Tax search Jul-2022, no provision | −44% (+48%) |
| CONFIPET | FY23 (2023-09-15) | **Qualified opinion** (none the year before) | −42% (+1%) |
| CONFIPET | FY24 (2024-09-13) | EoM: Ind AS 8 restatement (prior-period errors) | −24% (−46%) |
| ITDC | FY24 (2024-08-16) | Qualified ICFR opinion: material weakness at 31-Mar-2024 | −10% (−24%) |
| SCHAND | FY24 (2024-08-30) | EoM: composite scheme of arrangement | −10% (−15%) |
| TITAGARH | FY23 (2023-09-08) | EoM: amalgamation of subsidiary, prior year restated | +18% (+74%) |
| CENTURYPLY | FY24 (2024-09-06) | EoM: demerger of CFS division | +20% (−1%) |
| NATIONALUM | FY23 (2023-09-01) | EoM: coal-mine capitalisation; R&R capex not accounted | +27% (+86%) |
| DIAMONDYD | FY24 (2024-09-06) | EoM: ESOP trust consolidated (policy change) | +39% (+22%) |
| KRITI | FY23 (2023-08-11) | CARO: first cash loss (₹14.3 cr) | +42% (+118%) |
| SEPC | FY23 (2023-09-01) | EoM: lender resolution plan (already qualified) | +55% (+89%) |
| BOMDYEING | FY23 (2023-08-11) | EoM: SEBI order, ₹2.25 cr penalty + 2-year market ban | +58% (+78%) |
| DCAL | FY24 (2024-09-06) | EoM: merger accounting + Swiss regulator audit observation | +58% (+40%) |
| RAMRAT | FY24 (2024-08-16) | EoM: Income Tax search & seizure Nov-2023 | +63% (+51%) |
| MTNL | FY23 (2023-09-01) | CARO: interest default (41-day delay) on a bank term loan | +80% (+139%) |
| COCHINSHIP | FY23 (2023-09-08) | EoM: ship-repair-facility capitalisation | +144% (+208%) |

What the case notes say:
- **New "trouble" items** (regulatory or tax actions, restatements, qualifications, defaults, first cash losses)
  were a coin toss: median −10%, mean +3%. The worst cases were real governance or accounting problems:
  CONFIPET's qualification then restatement, GHCL's restatement, VALIANTORG's broken scheme terms, GRINFRA's
  sub-judice matter. But turnaround and asset stories (MTNL, SEPC, BOMDYEING) won big in a strong 2023-24 market.
- Most new EoMs are **technical** (merger or scheme accounting, policy changes). They carry no information.
- **Use:** in a stage-4 deep dive, read the auditor's report and CARO next to last year's. A new qualification, a
  restatement or a regulatory EoM is a "look harder" cue. It is not a mechanical sell or avoid signal.

## 4. What this means (edge check)
- Plain text-change has now failed three times: US v1 (not proven), US v2 (fresh data, retired) and this Indian
  pilot. The Indian MD&A and auditor-section versions show **no negative drift**. Changers lag in the median and
  win in the tail, the same lottery profile as the US.
- The pilot's job was the effect size, and the effect is about zero relative to peers (+2 to +6 pp the "wrong"
  way). With standard errors of ~7–8% at n≈60, a full run would need roughly 10× the sample to detect a −3%
  effect. That is not worth ~30 GB of downloads for an effect the pilot gives no reason to expect.
- **Kept:** the fetcher and parser (`annual_reports`, `sections.py`, `flags.py`), which make stage-4 reading
  cheap; the auditor-diff habit as a judgment cue; and the secondary "stale auditor text" −15% (P1 only) as an
  untested hypothesis. A fresh-data test is needed before anyone leans on it.
- Meta: 1 of 7 signal tests has survived (Indian PEAD avoid leg).

## 5. Caveats
Small n (60–65 per quintile, 21 flags). Two years in one regime (the 2023-24 small/mid-cap rally, then the
2024-25 correction; P1 and P2 often disagree in sign). The section parser misses about 15–20% of sections, which
adds noise toward zero. Screener weekly prices, dividends excluded. The 150-firm control-only pool beat the text
firms overall, so read every result relative to the "all events" row. The H3 hand check and the
trouble/technical split were done by one reader, and the split is post-hoc and descriptive.

## Deviations (post-run log)
- **P1 (2026-11-23, after returns):** the "trouble vs technical" split of H3 items and the "relative to all
  events" comparison were added after seeing results. Both are descriptive and changed no verdict.

## Reproduce
Scripts (standard library + `pdftotext` + `curl`): `/home/user/fein/tools/backtests/india_ar_text/`.
`s1_frame.py` (frame, ~12 min) → `s2_walk.py` (screener + NSE annual reports, ~75 min, resumable) →
`s3_scores.py` (sections, Jaccard, auditor flags) → hand check into `auditor_flags_checked.tsv` → `s4_analyze.py`.
Helpers: `common.py`, `sections.py`, `flags.py`. Data: `/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_india_ar/`
(`frame.txt`, `firms/`, `text/` = gzip page text, `sc/` = screener pages and charts). Scratch data is temporary.
Copies of the outputs are in `research_notes/Backtests/india_annual_report_text_outputs/`: `results.json`,
`events.tsv`, `firmyears.json`, `frame.txt`, `s3_funnel.json`, `auditor_flags.tsv`, `auditor_flags_checked.tsv`.

Sources: https://www.nseindia.in/api/annual-reports?index=equities&symbol=… ;
https://www.nseindia.in/api/corporate-announcements?index=equities&from_date=…&to_date=… ;
https://nsearchives.nseindia.in/annual_reports/ ; https://www.screener.in/company/…/ and
/api/company/{id}/chart/ ; Cohen, Malloy & Nguyen (2020) J. Finance 75(3) (memdb `insight:lazy-prices-filing-changes`).
