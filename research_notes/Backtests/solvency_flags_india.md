# Back-test: do the SOLVENCY flags see Indian failures coming? Survivorship-free re-test (Roadmap stage 2)

*Method calibration, not stock picking. Research, not SEBI-registered advice.*
Started 2026-11-22. Stage 2 (hard filters) of `memory/roadmap.md`. Why: the US test
(`solvency_flags_us.md`, decision:solvency-flags-graded, lesson L24) graded S1 and S5 red; lesson L25 and
decision:india-solvency-s3-excluded say the US rules do not transfer to India as-is (S3 fired on half of Indian
names). This test decides, on Indian data with dead companies included, which flags are graded red, hard, or only a
deep-dive question in the live India screen (`tools/detectors/solvency_screen.py`).
Unlocks: a calibrated India stage-2 gate (and the Pi detector alerts `solvency_s1` / `solvency_s5`), and an answer
to whether an India-specific S3 belongs in S5.

## STEP 0 — Feasibility (22-Nov-2026, before any outcome was computed)

Question: does screener.in still serve pages for dead / delisted Indian companies, with annual tables that reach
back to FY2016 / FY2018?

| Company (event) | Slug tried | Page | Annual years on page | FY2016 col | FY2018 col |
|---|---|---|---|---|---|
| Era Infra Engineering (IBBI CIRP 2017) | 530323 → ERAINFRA | yes | 2008–2026 (gaps) | yes | no (did not file) |
| Murli Industries (CIRP 2017) | 519323 → MURLIIND | yes | 2006–2016 | yes | no |
| Future Lifestyle Fashions (liquidation) | 536507 → FLFL | yes | 2013–2022 | yes | yes |
| Rainbow Papers (liquidation) | 523523 → RAINBOWPAP | yes | 2007–2018 | yes | yes |
| Bheema Cements (liquidation) | 518017 | yes | 2014–2025 | yes | yes |
| Stewarts & Lloyds (liquidation 2017) | 504960 | yes | 2006–2016 | yes | no |
| REI Agro (liquidation 2017) | REIAGROLTD | yes | 2006–2016 | yes | no |
| Innoventive Industries (first IBC case, 2017) | 533402 (404) → INNOIND | yes | to 2016 | yes | no |
| Tecpro Systems (NSE compulsory delisting 2018) | TECPRO | yes | to 2014 | no (stopped filing) | no |
| Deccan Chronicle (NSE compulsory delisting 2017) | DCHL | yes | to 2014 | no | no |
| GEI Industrial Systems (compulsory delisting 2018) | GEINDSYS | yes | old | no | no |
| Indus Fila (compulsory delisting 2019) | INDUSFILA | yes | to 2016 | yes | no |
| Bhushan Steel (IBC-resolved, then merged) | BHUSANSTL | **404** | – | – | – |
| Monnet Ispat (IBC-resolved, renamed) | MONNETISPA | **404** | – | – | – |

**13 of 15 dead firms have a screener page (87%)** → above the 50% stop line; the test proceeds. The two misses are
IBC-resolved companies that were later renamed or merged (their page now lives under the new name or is gone). Every
page also serves a weekly, split- and bonus-adjusted price series (checked on Infosys around its Sep-2018 1:1 bonus:
continuous at ~₹700) and screener's market-cap-to-sales series, through `/api/company/<id>/chart/`, even after the
stock stopped trading (Era Infra's series ends 12-Sep-2016). Schedules (`/api/company/<id>/schedules/`) also work for
dead firms (Murli Industries' borrowings to Mar-2016). Some dead firms simply stopped filing *before* the snapshot
(Tecpro, Deccan Chronicle): they are correctly not in the universe at T (not live filers).

## PRE-REGISTRATION (written 22-Nov-2026 before any outcome — price path, liquidation, delisting — was fetched or computed)

The page phase of the fetch (company pages only: annual tables, no price path) was started while this was written;
price charts are fetched only after this section was saved. The only outcome information seen so far is the
feasibility table above (15 names).

### Snapshots and point-in-time rule
- T ∈ {**2016-09-30 (FY2016)**, **2018-09-30 (FY2018)**}. Outcome window (T, T+5y] (to 2021-09-30 / 2023-09-30).
- FY0 = latest annual column on screener's **standalone** page ending in (T−18 months, T−6 months], i.e. fiscal
  years ending Apr-2015…Mar-2016 for T=2016 and Apr-2017…Mar-2018 for T=2018, with a balance sheet at the same
  date (annual reports are due within six months, so these were filed by Sep of the snapshot year). Prior-year
  values = the previous balance-sheet column. Columns after FY0 are cut off before the flags are computed.
- **Standalone basis (deviation from the live screen, which is consolidated-first):** one request per company
  instead of two, and most dead firms have only standalone accounts. Consequence: holding-company structures
  (debt in subsidiaries) are under-flagged. Stated bias.
- **Restated, not as-first-reported:** screener shows the latest numbers it holds for each year; FY2016 columns may
  carry Ind AS restatements from the FY2017 report. Stated bias (the US test used as-first-reported XBRL).

### Universe (fate-independent by construction)
- Frame (`s1_frame.py`): every company on BSE's Active (5,138 fetched 22-Nov-2026), Delisted (4,624) and Suspended
  (1,238) scrip lists, NSE-only active symbols (EQUITY_L), and IBBI / NSE-delisting rows with an NSE symbol but no BSE
  code (from `research_notes/Universe/india_dead_companies_2026-11-22.csv`). One row per company (ISIN > BSE code > NSE
  symbol). 221 IBBI rows with no exchange identifier (renamed companies; name did not match) cannot be fetched —
  counted in the survivorship audit.
- **Strata** (stratified sample, the brief allows it when the full universe is too large):
  - **D — distress lists, census (1,739 companies, all fetched):** IBBI CIRP / liquidation / NCLT rows, NSE
    compulsory or liquidation delisting, NSE suspension, BSE suspended list.
  - **X — BSE/NSE delisted, not D (2,132; random sample 500, seed 20161, weight 4.264):** mergers, voluntary
    delistings, old exits, reason unknown.
  - **L — live, not D (5,070; random sample 900, seed 20161, weight 5.633):** on BSE or NSE active lists today.
  All statistics are **weighted by stratum weight** (population / sample) so they estimate the full frame.
- Membership at T: a screener page; FY0 exists as above; a price observation within 31 days before T; size known.
- **Size:** market cap at T = screener market-cap-to-sales at the last weekly price ≤ T × trailing-12-month sales
  (last value dated ≤ T). Keep **₹200 cr ≤ mcap ≤ ₹20,000 cr**. Market-cap-to-sales comes rounded to 0.1, so the
  band uses the point estimate; rows whose ±0.05 rounding interval straddles a boundary are counted as
  "ambiguous size" and reported. Zero or missing sales ⇒ size unknown ⇒ excluded and counted.
- Exclude financials (`solvency_screen.is_financial`: banks, NBFCs, insurers, brokers, housing finance — they need
  an ALM test).
- Exclude companies **already in insolvency at T** (IBBI CIRP admission or liquidation dated ≤ T) and count them.
- One row per (company, snapshot); CIs are bootstrapped by company within stratum.

### Flags (reused unchanged from `tools/detectors/solvency_screen.py` — `inputs()` / `flags()`)
- **S1** net worth < 0 (equity capital + reserves), unless payout-driven (FCF > 0 and 3-year dividends ≥ |net worth|).
  S1raw reported alongside.
- **S2** interest cover EBIT / interest < 1.5x (EBIT = operating profit − depreciation + recurring other income;
  negative EBIT with interest fires; no interest and debt < 5% of assets ⇒ not fired, else unknown).
  **S2b** India variant < 2.5x.
- **S3** (US definition, **reported only**): short-term borrowings > cash equivalents + 0.5 × CFO.
- **S4** dividends paid > 0 and > FCF while borrowings rose.
- **S5-India** = ≥ 2 of S1, S2, S4 (the live India definition). Secondary: S5b-India (S2b instead of S2), S5-US
  (≥ 2 of S1–S4, includes S3).
- **S3-India (exploratory, labelled so):** short-term borrowings > cash equivalents + investments (balance-sheet
  "Investments", total) + 0.5 × CFO. Standalone investments include stakes in subsidiaries, so this over-credits
  holding companies — a first cut only.
- Reference: **S0** EBIT < 0.
- Unknown flags are excluded from that flag's statistics (coverage reported).

### Outcomes (within (T, T+5y])
- **O_liq:** IBBI public announcement of liquidation dated in the window. A liquidation row with a blank date counts
  if the company's CIRP admission is in the window or its price series stops in the window; otherwise it is
  counted as "undated" and not used.
- **O_cdel (compulsory delisting / exit for cause):** NSE "Compulsory Delisting" or "Delisting – Liquidation" dated
  in the window; **or** company on the BSE suspended list (no dates published) whose screener price series stops in
  the window (last weekly price ≤ T+5y − 90 days; the stop date is the event-date proxy).
- **O_px:** lowest weekly close in the window ≤ 0.2 × the last weekly close ≤ T (screener's adjusted prices).
- **O_fail = O_liq ∨ O_cdel ∨ O_px** (primary). **O_strict = O_liq ∨ O_cdel** (secondary, no price needed).
- Recorded separately, **not a failure:** **O_cirp** = IBBI CIRP admission in the window (lesson L25: Inox Wind and VA
  Tech Wabag were admitted and survived). Reported: how many flagged / unflagged firms were admitted, and how many
  admitted firms failed.
- **R5** = last weekly close ≤ T+5y (within 31 days) ÷ close at T; missing when the series stopped early (then a
  company with O_fail is "not a winner", one without is excluded from the winner denominator and counted).
  **Winner = R5 ≥ 3.** Price return only (dividends not included).

### Metrics and decision rule (fixed now; same as the US test)
- Per flag, per snapshot and pooled, all weighted: n known, n fired, precision P(O_fail | F), base rate P(O_fail)
  (known set), recall P(F | O_fail), **lift = precision / base rate**, winners excluded = flagged winners / all
  winners (known). 95% percentile CIs from 2,000 bootstrap draws resampling companies within each stratum.
- **Graded red** if pooled lift ≥ 2.0 **and** the lift CI lower bound > 1 **and** the flag excludes < 10% of
  eventual ≥ 3x winners. **Hard** only if additionally pooled lift ≥ 4.0. Otherwise a **question** for the deep
  dive. Decided on primary O_fail; O_strict, per-snapshot and stratum-D-only results are robustness and do not
  overturn the verdict. S3, S3-India, S2b, S5b and S5-US results are exploratory.
- Known biases stated in advance: (1) renamed/merged IBC companies whose old page is gone (Bhushan Steel, Monnet
  Ispat) and 221 IBBI rows without identifiers fall out — survivorship leak toward *fewer* failures; (2) standalone
  accounts under-flag holdco debt; (3) restated, not as-first-reported, numbers; (4) market-cap-to-sales rounding
  near the size boundaries; (5) BSE suspensions carry no date, so the price-series stop is used as the date; firms
  that stopped trading for unrecorded reasons in stratum X are not failures unless the price fell ≤ 0.2× first;
  (6) both windows contain COVID-2020, and the FY2016 window the 2018–19 IL&FS / NBFC credit squeeze — results are
  shown per snapshot; (7) companies that missed filing by T (common in distress) are out of the universe at T.

---
## Stage log
- 2026-11-22: feasibility done (13/15). Frame built (`s1_frame.py`): D 1,739 census, X 500 of 2,132, L 900 of 5,070.
  Page phase started; pre-registration above saved before the chart phase.
- 2026-11-22 (resumed after a usage-limit pause): pages (3,139 companies, ~82 min), charts (1,345) and schedules (322)
  fetched at ≥ 1.55 s per request from one stream. **Process slip:** a chained job started the chart and schedule
  phases early, so about 32 chart and 6 schedule requests ran alongside the page stream for about a minute (two
  streams). All later fetching was single-stream. All files are cached under the scratchpad `bt_solv_in/`.
- **Deviation found on audit, before the verdict table was read:** dead or merged banks with unlabeled screener pages
  (Oriental Bank, Allahabad, Andhra, State Bank of Mysore / Travancore, Lakshmi Vilas) escaped
  `solvency_screen.is_financial()`, whose label fallback looks only for "Financing Profit". Fix in `s3_panel.py`: an
  unlabeled page with a "Deposits" row or "Bank" in the name counts as financial (10 rows removed; 499 → 489). This
  follows the pre-registered exclusion, so it is not a change of rule. Verdicts are the same before and after the fix
  (before it, S5 was 2.00 [1.04, 3.12], also a question at two decimals). The live screen faces the same gap only for
  label-less pages.

---

# RESULTS (written 2026-11-22 after the run)

## Funnel and data audit

| step | D (census) | X (sample of BSE/NSE delisted) | L (sample of live) |
|---|---|---|---|
| companies sampled (weight) | 1,739 (1.0) | 500 (4.264) | 900 (5.633) |
| no screener page | 795 | 213 | 14 |
| financial (excluded) | 57 | 8 + 6 unlabeled banks | 107 |
| rows FY2016: no annual data at T / no price history / not trading at T / size unknown / outside ₹200–20,000 cr | 236 / 36 / 141 / 55 / 313 | 210 / 23 / 21 / 1 / 14 | 201 / 8 / 133 / 27 / 265 |
| rows FY2018: same | 333 / 31 / 132 / 50 / 264 | 240 / 12 / 13 / 0 / 7 | 177 / 9 / 116 / 39 / 276 |
| already in insolvency at T (excluded) | 6 (FY2018) | 0 | 0 |
| **panel rows** FY2016 + FY2018 | **106 + 71 = 177** | **4 + 1 = 5** | **145 + 162 = 307** |

Panel: **489 company-snapshots** (FY2016 255, FY2018 234). Outcomes in the panel: O_liq 19, O_cdel 29, O_px 165,
**O_fail 168** (weighted base rate **19.7%**: FY2016 27.6%, FY2018 12.2%), O_strict 33 (1.7%), O_cirp admissions 79,
winners ≥ 3x 92. "Not trading at T" among live names is mostly companies that listed after T (IPOs from 2017–2023
whose earlier annual data screener holds). 20 rows have an ambiguous size (rounding interval straddles a boundary).

**Survivorship audit (retrievability of the dead lists):**

| list | companies in frame | screener page | annual data at a T | in panel |
|---|---|---|---|---|
| IBBI liquidation | 169 | 144 (85%) | 115 | 22 |
| IBBI CIRP admission | 492 | 409 (83%) | 350 | 85 |
| NSE compulsory / liquidation delisting | 204 | 203 (100%) | 65 | 5 |
| BSE suspended | 1,213 | 494 (41%) | 446 | 55 |
| NSE suspended (pre-2012) | 128 | 121 | 47 | 0 |
| IBBI rows with no exchange identifier | 221 | not fetchable | – | – |

The IBBI dead firms are 83–85% retrievable. The missing 15–17% are mostly renamed or merged companies; together with
the 221 IBBI rows that had no identifier, this leak means *fewer* failures in the panel. BSE-suspended companies
without a page are mostly old shells far below ₹200 cr. Most NSE compulsory delistings had stopped filing before T,
so they were not live filers. Stratum D has a 68.9% weighted O_fail rate and stratum L 14.7%: dead companies do get
in, and the panel is not a survivors-only set. Price coverage: R5 is missing for 50 rows (the series stopped early);
winner status is unknown for 9.

## Pooled results — primary O_fail (weighted; stratified bootstrap by company, 2,000 draws)

| flag | fired / known | fired & failed | weighted share flagged | precision | lift [95% CI] | recall | >3x winners excluded | verdict |
|---|---|---|---|---|---|---|---|---|
| S1 net worth < 0 (adj.) | 13 / 489 | 7 | 1.4% | 43% | **2.20 [0.50, 4.42]** | 3.1% | 1.4% (2/92) | question (CI includes 1) |
| S2 interest cover < 1.5x | 150 / 484 | 76 | 19.0% | 32% | 1.69 [1.27, 2.20] | 32% | 20% | question |
| S2b interest cover < 2.5x | 220 / 484 | 108 | 31.9% | 32% | 1.68 [1.35, 2.06] | 54% | 35% | question |
| S4 dividends > FCF while debt rose | 89 / 487 | 27 | 20.5% | 15% | 0.76 [0.45, 1.15] | 16% | 25% | question (no signal) |
| **S5-India** ≥ 2 of S1, S2, S4 | 25 / 489 | 14 | 3.7% | 39% | **1.985 [1.01, 3.24]** | 7.3% | 3.8% | **question (misses the 2.0 bar by 0.015)** |
| S5b-India (with S2b), exploratory | 39 / 489 | 22 | 5.9% | 36% | 1.82 [1.07, 2.70] | 11% | 7.4% | (question) |
| S3 US funding gap, reported only | 272 / 469 | 116 | 50% | 25% | 1.29 [1.09, 1.50] | 65% | 63% | (question) |
| S3-India exploratory (STD > cash + investments + 0.5 CFO) | 174 / 469 | 72 | 32% | 23% | 1.15 [0.85, 1.50] | 37% | 47% | (no signal) |
| S5-US (≥ 2 of S1–S4), exploratory | 171 / 489 | 78 | 27% | 26% | 1.27 [0.98, 1.59] | 33% | 36% | (question) |
| S0 EBIT < 0, reference | 42 / 489 | 17 | 4.8% | 22% | 1.12 [0.56, 1.91] | 5.3% | 6.4% | reference |

(Weighted share flagged = estimated share of the full frame, among companies where the flag is known.)

## Robustness (does not overturn the verdict)
- **O_strict** (liquidation or compulsory exit only; 33 events, so CIs are wide): S2 2.87 [1.88, 4.11], S2b 2.28
  [1.70, 2.98], S3-India 1.86 [1.25, 2.55], S3-US 1.55, S5-India 1.64 [0, 4.91], S1 2.17 [0, 10.3], S4 1.03, S0 4.46
  [1.76, 8.96]. Liquidations and compulsory exits are concentrated among loss-makers with weak interest cover.
- **Per snapshot (O_fail):** S5-India 2.08 [0.96, 3.47] in FY2016 and 1.88 [0.19, 5.07] in FY2018; S1 1.91 / 1.90;
  S2 1.66 / 1.42; S4 0.98 / 0.44.
- **Without size-ambiguous rows:** S5 1.89, S1 2.00, S2 1.69 (same verdicts).
- **Live stratum only (survivor-tilted):** S5 2.05 [0, 4.18], S2 1.38, S2b 1.60.
- **CIRP admissions** (not failures): 79 admitted rows, 65 of them also failed, 18 liquidated. 14 admitted
  companies did not fail (Alok Industries FY2016, Essar Shipping, Ashapura Minechem, DCW, V2 Retail…), so lesson L25
  holds. Weighted admission rate: S1-flagged 33.5% vs 3.6% unflagged; S5-flagged 13.8% vs 3.6%; S2 11.1% vs 2.1%.
- Failures caught by S1 or S5-India include ABG Shipyard, GTL, Jet Airways (both snapshots), Reliance Communications,
  McNally Bharat, Mcleod Russel, Ballarpur, Pratibha Industries, Future Enterprises, Gayatri Projects
  (`solvency_india_outputs/tables.md`).

## Verdicts (pre-registered rule: lift ≥ 2 with CI > 1 and < 10% of ≥ 3x winners excluded → graded red; hard if ≥ 4)
- **S1 negative net worth → QUESTION (underpowered, not refuted).** Lift 2.20 is the same size as in the US (2.31),
  but only 13 Indian rows in the ₹200–20,000 cr band have negative net worth, so the CI is [0.50, 4.42]. It excludes
  almost no winners (2 of 92). One in three S1 firms entered CIRP within five years.
- **S2 interest cover < 1.5x → QUESTION.** A real signal (lift 1.69, CI well above 1; 2.87 on liquidation or exit),
  and unlike in the US it is not just "loss-maker" (S0 alone: 1.12). It fires on 19% of the frame and would cut 20%
  of ≥ 3x winners — the same objection as in the US (27%).
- **S2b < 2.5x → QUESTION:** similar lift, flags 32% of companies and 35% of winners. Not a better India threshold.
- **S4 dividends > FCF while debt rose → QUESTION / no signal** (lift 0.76; FY2018 0.44: dividend payers failed
  less). Second market in which it fails.
- **S5-India (≥ 2 of S1, S2, S4) → QUESTION, borderline.** Lift 1.985 [1.01, 3.24], excludes 3.8% of winners. By
  the fixed rule it misses graded red by 0.015 of lift, and the CI lower bound is barely above 1. Recall 7%.
- **S3 (US) stays excluded** from India S5: it flags 50% of companies and 63% of winners for a lift of 1.29. This
  confirms decision:india-solvency-s3-excluded. **S3-India (cash + investments credit) does not rescue it:** lift
  1.15 on O_fail (1.86 on O_strict), and it still flags 47% of winners. Exploratory; no adoption.
- **Nothing is HARD.**

## What it means
1. India's five-year small/mid-cap failure rate (19.7%, almost all ≥ 80% price collapses) is twice the US rate (9.5%).
   Solvency flags only roughly double the odds of failure here too. They are "look harder, size smaller" prompts, not
   protection: S5 catches 7% of failures.
2. The US graded-red pair (S1, S5) is **not confirmed** on Indian data at the pre-registered bar. The point estimates
   are the same size as in the US (≈ 2×), and the miss is a power problem (13 and 25 flagged rows). Honest reading:
   *consistent with the US, not proven in India.*
3. Weak interest cover is the strongest broad Indian signal but costs a fifth of the multibaggers. It belongs in the
   deep-dive checklist, not the gate. Dividends-beyond-FCF is noise in both markets.

## Caveats
- Standalone accounts (holdco debt under-flagged); restated screener numbers, not as-first-reported; market-cap-to-sales
  rounding; weekly adjusted closes (O_px uses the weekly low close, not the intraday low); BSE suspension dates
  proxied by the end of the price series.
- About 15–17% of IBBI firms are unretrievable (renamed or merged); 221 IBBI rows have no identifier → fewer failures.
- Strata X and L are samples (weights 4.3 and 5.6); X contributes only 5 rows. Bootstrap CIs include the sampling.
- FY2016 window includes the 2018–19 small-cap / IL&FS crash and COVID; the FY2018 window includes COVID.
- One process slip (two fetch streams for about a minute) and one logged fix (unlabeled banks), both described above.

Scripts: `tools/backtests/solvency_india/` (common, s1_frame, s2_fetch, s3_panel, s4_analyze, s5_audit). Outputs:
`research_notes/Backtests/solvency_india_outputs/` (panel.csv, results.json, tables.md, funnel.json, frame_meta.json,
survivorship_audit.json). Raw cache: scratchpad `bt_solv_in/` (not durable). Research, not SEBI-registered advice.
