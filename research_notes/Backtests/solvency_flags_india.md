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
