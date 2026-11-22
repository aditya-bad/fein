# Back-test: do SOLVENCY flags see leverage blow-ups coming? US, survivorship-free (Roadmap stage 2)

*Method calibration, not stock picking. Research, not SEBI/SEC-registered advice.*
Started 2026-11-21. Stage 2 (hard filters) of `memory/roadmap.md`. Why: `research_notes/Backtests/hard_filters_test.md`
found our hard set caught **0 of 15 leverage blow-ups**; `insight:disqualifiers-v2-proposal` added an
**untested** solvency set. This test decides whether each solvency flag is graded red, hard, or a question.
Unlocks: a calibrated solvency gate for stage 2 (and the Pi detector set), and the template for the Indian re-test.

## PRE-REGISTRATION (written 2026-11-21 before any outcome — price, bankruptcy, delisting — was fetched or computed)

### Snapshots and point-in-time rule
- T ∈ {2015-06-30, 2017-06-30, 2019-06-30}. Outcome window (T, T+5y] (ends 2020-06-30 / 2022-06-30 / 2024-06-30).
- Fundamentals come from the **latest 10-K (or 10-KT) whose filing date ≤ T**, taken *as first reported in that
  filing* (SEC companyfacts keeps each fact with its accession and filing date; we use the facts of that accession).
  The 10-K must be filed within 15 months before T (live filer). Prior-year values (YoY tests) = the comparative
  column of the same 10-K; if absent, the prior 10-K filed ≤ T. Nothing filed after T is used for flags or size.

### Universe (fate-independent by construction)
- Candidates: every CIK in the SEC XBRL frames for `dei:EntityPublicFloat` at any quarter-end in the 2 years before T
  (this includes companies that later went bankrupt, were delisted or acquired — EDGAR keeps them).
- Size: **public float reported on the cover of that 10-K** (non-affiliate market value, measured at the end of the
  filer's prior fiscal Q2, i.e. 6–18 months before T). Keep **$300M ≤ float ≤ $20B**. Why float rather than shares ×
  price: price at T needs a ticker with surviving price history, and dead firms usually have none on Yahoo; using
  price for selection would quietly drop the failures this test is about. Float understates market cap for
  controlled firms and is stale — "roughly $300M–$20B", as briefed. Sanity check: float / total assets outside
  [0.001, 1000] ⇒ treated as a filer scaling error ⇒ excluded and counted.
- Exclude by SIC (SEC submissions, current code): 6000–6799 (banks, insurers, brokers, REITs 6798, SPACs/blank checks
  6770, funds), 4900–4949, 4961, 4991 (utilities), missing SIC. Foreign private issuers (20-F/40-F) are not in the set.
- One row per (firm, snapshot). The same firm can appear in several snapshots → all CIs are **bootstrapped by CIK**.

### Inputs (us-gaap tags, first available in order; values from the T-filing)
- Equity E: StockholdersEquity → StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest.
- EBIT: OperatingIncomeLoss → (pre-tax income from continuing ops [IncomeLossFromContinuingOperationsBeforeIncomeTaxes…
  variants] + interest expense).
- Interest expense I: InterestExpense → InterestExpenseDebt → InterestAndDebtExpense → InterestExpenseNet? no (not used) →
  InterestPaidNet / InterestPaid (cash, last resort).
- Short-term debt STD: DebtCurrent if tagged; else max(LongTermDebtCurrent, LongTermDebtAndCapitalLeaseObligationsCurrent)
  + (ShortTermBorrowings, or if absent CommercialPaper + LinesOfCreditCurrent + ShortTermBankLoansAndNotesPayable).
  None tagged ⇒ 0 (a balance sheet without a short-term debt line has none).
- Total debt TD: STD + noncurrent debt (LongTermDebtNoncurrent → LongTermDebtAndCapitalLeaseObligations →
  (LongTermDebt − current portion)). None tagged ⇒ 0.
- Cash C: CashAndCashEquivalentsAtCarryingValue → CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents → Cash.
- CFO: NetCashProvidedByUsedInOperatingActivities → …ContinuingOperations. Capex: PaymentsToAcquirePropertyPlantAndEquipment
  → PaymentsToAcquireProductiveAssets (missing ⇒ 0, counted). FCF = CFO − capex.
- Dividends D: PaymentsOfDividends → PaymentsOfDividendsCommonStock (missing ⇒ 0). Buybacks B:
  PaymentsForRepurchaseOfCommonStock → PaymentsForRepurchaseOfEquity (missing ⇒ 0). Treasury: TreasuryStockValue.
- Scaling sanity: any balance-sheet/flow input with |x| > 5 × total assets ⇒ that firm's dependent flags = unknown.
- A flag is **unknown** when its required inputs are missing; it is then excluded from that flag's statistics
  (denominator = firms where the flag is known). Coverage per flag is reported.

### Flags (fired = 1)
- **S1 negative equity (adjusted):** E < 0, **unless** buyback-driven and cash-generative: FCF(FY0) > 0 **and**
  TreasuryStockValue(FY0) + Σ(D + B) over the last 3 fiscal years filed ≤ T ≥ |E|. Exempted firms are not fired.
  Reported alongside: **S1raw** = any E < 0 (secondary).
- **S2 interest cover:** I > 0 and EBIT / I < 1.5 (negative EBIT with any interest fires). I missing or 0 ⇒
  not fired if TD < 5% of total assets, else unknown.
- **S3 short-term funding gap:** STD > 0 and STD > C + 0.5 × CFO (CFO with its sign: cash burners get no credit).
- **S4 payouts beyond FCF while borrowing:** D + B > 0 and D + B > FCF and TD(FY0) > TD(FY−1).
- **S5 combined:** ≥ 2 of S1–S4 fired (unknown counts as not fired; S5 known if ≥ 2 component flags known).
- Reference only (not a candidate): **S0** EBIT < 0 (operating loss) — tells us whether S2's lift is just "loss-maker".

### Outcomes (within (T, T+5y])
- O_bk: 8-K with item 1.03 (bankruptcy/receivership) filed in window (SEC submissions, all pages).
- O_delist: delisting for cause = 8-K item 3.01 in window **and** a Form 25 / 25-NSE / 15 in window **and no merger
  evidence** in window (8-K item 5.01, DEFM14A/DEFM14C/PREM14A, SC 14D9, SC TO-T, SC 13E3, 425).
- O_px: lowest month-end adjusted close in window ≤ 0.2 × adjusted close on the last trading day ≤ T (Yahoo v8).
- **O_fail = O_bk ∨ O_delist ∨ O_px** (primary). Firms without usable Yahoo history can fail only via EDGAR events;
  how many there are, and their EDGAR fate (acquired / bankrupt / delisted / went dark / alive), is audited.
  Secondary **O_strict = O_bk ∨ O_delist** (pure EDGAR, fully survivorship-free). Sensitivity: primary metrics on
  firms with full price history or an EDGAR failure event only.
- 5-year total return R5 = adj close at last trading day ≤ T+5y ÷ adj close at T (missing if the series ends > 10 days
  early or Yahoo identity check fails: unadjusted close at T × shares (latest dei cover value ≤ T) must be within
  0.4–8 × float). **Winner** = R5 > 3. Size-matched excess for flag F = R5 − median R5 of F-unflagged firms in the same
  snapshot and float quintile.

### Metrics and decision rule (fixed now)
- Per flag, per snapshot and pooled: n known, n fired, precision P(O_fail | F), base rate P(O_fail) (known set),
  recall P(F | O_fail), **lift = precision / base rate**, relative risk vs unflagged, winners excluded = flagged
  winners / all winners (known), median size-matched excess of flagged firms. 95% CIs from 2,000 bootstrap draws
  resampling CIKs (pooled) — percentile intervals.
- **Graded red** if pooled lift ≥ 2.0 **and** the lift CI lower bound > 1 **and** the flag excludes < 10% of
  eventual > 3x winners. **Hard** only if additionally pooled lift ≥ 4.0. Otherwise it stays a **question** (prompt
  for the deep dive), not a flag. Decided on primary O_fail; O_strict and per-snapshot results are reported as
  robustness, not used to overturn the verdict. Any subgroup beyond these is exploratory and labelled so.
- Known biases stated in advance: (1) Yahoo lacks most dead tickers → O_px and R5 are survivor-tilted; O_bk/O_delist
  are not; (2) float-based size is stale and understates controlled firms; (3) as-first-reported XBRL with tag
  fallbacks — firms using custom tags fall to "unknown"; (4) current SIC for exclusions; (5) the 2015 and 2017 windows
  contain the 2015–16 energy bust and COVID-2020, the 2019 window COVID and 2022 — O_px is regime-sensitive, which is
  why results are shown per snapshot; (6) 8-K item codes exist in submissions metadata from 2004 — fine for these windows.

---
## Stage log
- 2026-11-21: pre-registration above written; scripts in `tools/backtests/solvency_us/` (s1 candidates from float
  frames → s2 SEC submissions + reduced companyfacts → s3 flags → s4 EDGAR events → s5 tickers + Yahoo → s6 analysis).
  4,843 candidate CIKs. Fetch interrupted by a usage limit at 1,162 firms; resumed 2026-11-22 from cache.
  Implementation notes fixed before outcomes: the float fact is taken from the T-10-K's own accession (some filers
  tag the float with a wrong date, e.g. Sanmina FY2015); S4 requires payouts > 0 (otherwise every cash burner fires).
- 2026-11-22, **deviation found on audit of EDGAR events (before any flag-vs-outcome statistic was run):** the
  pre-registered O_delist (8-K 3.01 + Form 25/15 + no merger) was dominated by *voluntary exchange transfers*
  (Workday, Garmin, Xerox, Expeditors, Palo Alto… moving Nasdaq↔NYSE file exactly that pattern). Revised O_delist =
  the 3.01 8-K text shows a substantive listing-rule failure (deficiency / minimum bid / not in compliance / late
  filing / suspension; the item-heading boilerplate stripped; transfer language and pure governance-composition
  notices excluded) **and** a Form 25/15 on or after that notice in the window **and** no merger evidence
  (`s4b_item301_text.py`). Results under the as-registered definition are also reported (`O_fail_asreg`).

---

# RESULTS (written 2026-11-22 after the run)

## Funnel and data audit
| | 2015-06-30 | 2017-06-30 | 2019-06-30 |
|---|---|---|---|
| Candidate CIKs (float frames, 2 yrs before T, loose band) | 4,843 (union) | | |
| Excluded SIC (financials / REITs / SPACs / utilities / none) | 1,349 | 1,349 | 1,349 |
| No 10-K filed in the 15 months before T | 744 | 808 | 843 |
| Float outside $300M–$20B | 894 | 1,039 | 899 |
| Float/assets scaling check failed, no float or no assets on T-10-K | 173 | 133 | 128 |
| **Universe (firm-snapshots)** | **1,683** | **1,514** | **1,624** |

4,821 firm-snapshots, 2,271 distinct firms. Flags are known for 98–99% of rows (S1 4,717; S2 4,739; S3 4,785; S4 4,782).
Fired: S1 3.3%, S1raw 5.3%, S2 25%, S3 4.6%, S4 13%, S5 6.8%, S0 (operating loss) 23%. The S1 buyback exemption
excused 93 rows (AutoZone, Domino's-type, H&R Block, Dunkin', Choice Hotels…); their O_fail rate was **4.3%**, under
half the base rate, so the exemption does what it was meant to do.

**Outcomes:** 213 bankruptcies (8-K 1.03), 19 delistings for cause (revised definition; 199 under the as-registered
one, mostly exchange transfers — see stage log), 233 price collapses (≤ 0.2× at a month-end), **O_fail 460 (9.5%)**,
O_strict 232 (4.8%). 228 of the 233 price collapses had no EDGAR event.

**Price coverage (survivorship audit):** full 5-year Yahoo history for 2,667 rows (55%); none for 2,154. EDGAR fate of
the no-price rows: 1,002 acquired/merged, 207 bankrupt, 147 merger evidence but still filing, 119 stopped filing,
43 delisted for cause, 636 alive (ticker changes, share classes, 247 rows hit the identity check). So **97% of the
bankruptcies have no Yahoo price** — had we needed prices to define the universe or the failure, the test would have lost
almost every failure. In the no-price rows, failure can come only from EDGAR events, so O_fail is understated there (a firm that
fell 85% and was then bought cheaply counts as no failure). Sensitivity "priced or EDGAR-failed" (2,876 rows) is
shown below. Winners (R5 > 3x) are measurable only on the 2,667 priced rows: **276 winners**.

## Pooled results — primary outcome O_fail (bootstrap by CIK, 2,000 draws)
| Flag | known / fired | fired&fail / all fail | precision | base | **lift [95% CI]** | RR vs unflagged | recall | >3x winners excluded | median size-matched excess R5 (flagged) |
|---|---|---|---|---|---|---|---|---|---|
| S1 neg. equity (adj.) | 4717 / 158 (3%) | 34 / 439 | 21.5% | 9.3% | **2.31 [1.63, 3.11]** | 2.42 | 7.7% | 10 / 273 = **3.7%** | +0.08 |
| S2 EBIT/interest < 1.5 | 4739 / 1185 (25%) | 220 / 445 | 18.6% | 9.4% | 1.98 [1.79, 2.17] | 2.93 | 49.4% | 74 / 273 = **27.1%** | −0.05 |
| S3 ST funding gap | 4785 / 218 (5%) | 32 / 452 | 14.7% | 9.4% | 1.55 [1.04, 2.16] | 1.60 | 7.1% | 15 / 276 = 5.4% | +0.03 |
| S4 payouts > FCF + debt up | 4782 / 635 (13%) | 64 / 453 | 10.1% | 9.5% | 1.06 [0.84, 1.31] | 1.07 | 14.1% | 38 / 275 = 13.8% | +0.02 |
| S5 ≥ 2 flags | 4803 / 325 (7%) | 73 / 455 | 22.5% | 9.5% | **2.37 [1.90, 2.86]** | 2.63 | 16.0% | 22 / 276 = **8.0%** | +0.07 |
| S1raw any neg. equity (secondary) | 4717 / 251 (5%) | 38 / 439 | 15.1% | 9.3% | 1.63 [1.12, 2.18] | 1.69 | 8.7% | 16 / 273 = 5.9% | +0.32 |
| S0 operating loss (reference) | 4775 / 1097 (23%) | 198 / 450 | 18.0% | 9.4% | 1.92 [1.72, 2.13] | 2.63 | 44.0% | 66 / 274 = 24.1% | −0.23 |

## Robustness (not used to overturn the verdict)
| Flag | lift O_strict (EDGAR only) | lift O_fail as-registered delisting | lift priced-or-failed subset | lift 2015 / 2017 / 2019 (O_fail) | winners excl. 2015 / 2017 / 2019 |
|---|---|---|---|---|---|
| S1 | 3.12 [1.99, 4.41] | 2.07 [1.47, 2.74] | 2.92 [2.17, 3.78] | 1.65 [0.69, 2.66] / 2.86 / 2.66 | 5% / 4% / 3% |
| S2 | 2.49 [2.22, 2.77] | 1.86 | 2.33 | 1.96 / 2.11 / 1.92 | 31% / 32% / 23% |
| S3 | 1.93 [1.09, 2.87] | 1.50 | 1.49 | 1.58 / 2.23 / 1.12 | 6% / 3% / 7% |
| S4 | 1.11 [0.75, 1.49] | 1.03 | 0.95 | 1.14 / 0.87 / 1.06 | 8% / 15% / 16% |
| S5 | 3.28 [2.59, 4.08] | 2.12 [1.72, 2.56] | 2.39 [1.93, 2.85] | 2.11 / 2.77 / 2.39 | 5% / 11% / 8% |

Per-snapshot O_strict lifts for S1 reach 4.07 (2017) and 4.56 (2019), but 1.61 in 2015 (energy bust: many failures
had positive equity). Full per-snapshot tables: `research_notes/Backtests/solvency_us_outputs/tables.md`.

Exploratory, not pre-registered: S2 on profitable firms (EBIT > 0 but cover < 1.5) lift 1.80, excludes 15 of 273
winners (5.5%); S2 on loss-makers lift 2.04, 59 winners excluded. **S2 is mostly the operating-loss flag:** S0 alone does
almost as well (1.92) and costs almost as many winners.

## Verdicts (pre-registered rule: lift ≥ 2 with CI > 1 and < 10% of >3x winners excluded → graded red; hard if lift ≥ 4)
| Flag | Verdict | Why |
|---|---|---|
| **S1 negative equity (with buyback exemption)** | **GRADED RED** | lift 2.31 [1.63, 3.11]; excludes 3.7% of winners. Not hard (< 4; 2015 CI touches 1). |
| **S5 two or more solvency flags** | **GRADED RED** | lift 2.37 [1.90, 2.86]; excludes 8.0% of winners (11% in 2017 — close to the limit). Not hard. |
| S2 interest cover < 1.5x | QUESTION | lift 1.98 (just below 2) and excludes 27% of winners (Plug-type, biotech, turnarounds). |
| S3 short-term funding gap | QUESTION | lift 1.55; unstable (1.12 in 2019). Dealers funded by floor-plan loans (MarineMax-type) fire without being in distress. |
| S4 payouts > FCF while borrowing | QUESTION, close to no signal | lift 1.06 [0.84, 1.31]; excludes 14% of winners. Drop as a flag; keep as a capital-allocation question. |

**No solvency flag qualifies as HARD.** The best (S5 on EDGAR-only failures, 3.28) is still below 4x, and the
hard rule needs ≥ 4 on the primary outcome.

## What it means
1. Our stage-2 gap (0 of 15 leverage blow-ups caught) is partly fixable mechanically: **negative equity not explained by
   buybacks** and **≥ 2 solvency flags** each find 2.3–2.4x the base failure rate (≈ 1 in 5 flagged firms fails within
   5 years against 1 in 11) and cost few winners. Names behind them: Sears (2015, 2017), California Resources, Cobalt,
   Revlon, Endo, Diebold, Weatherford, Yellow, Tailored Brands, Frontier, GNC, Dean Foods, Alpha Natural, Arch.
2. Recall is low: S1 catches 8% and S5 16% of failures. Most US failures in these windows (2015–16 energy, COVID) had
   positive equity and adequate cover a year earlier. A graded flag is a reason for a deeper look, not a full defence.
3. Flagged-firm *returns* are lottery-shaped: the median size-matched excess for S1/S5 is slightly **positive** (+0.07–0.08)
   because the survivors among them include big recoveries (Caesars, Dell, Tenet, Exelixis, FTAI, Plug). The flag prices
   in survival risk, not lower expected return; it is an AVOID-FOR-SIZING rule, not a short signal.
4. Interest cover < 1.5x mainly re-labels loss-makers and would have cut 27% of the eventual 3x+ winners. Keep it as a deep-dive
   question (what does cover look like at mid-cycle margins?).

## Caveats
- O_fail is understated for the 45% of rows without Yahoo history (they can fail only via EDGAR); price-based failure and
  winner counts are survivor-tilted. EDGAR events are not.
- 8-K item 1.03 is also filed for a subsidiary's bankruptcy; spot check of 30 found only real parent-level Chapter 11s.
- Float-based size is stale; current SIC; as-first-reported XBRL with tag fallbacks (custom tags → unknown/0; capex missing → 0).
- Same firm in up to 3 snapshots → CIK-clustered bootstrap; failures cluster in 2015–16 energy and 2020.
- The revised delisting definition is a post-audit deviation (19 vs 199 events); results under the as-registered version
  are lower but give the same verdicts (S1 2.07, S5 2.12; CIs > 1).

## Indian re-test needed before using these on NSE/BSE
India has more promoter/group leverage (holdco debt, pledges), more IBC cases, and negative equity is rarely buyback-driven
(buybacks are small), so the exemption will hardly ever apply. We need a point-in-time universe with dead companies
(IBC admissions from IBBI, NSE/BSE delistings and suspensions) — Pi/Screener data. Re-test S1, S5 and an ALM/short-term
gap version for NBFCs separately (excluded here). Thresholds may differ: Indian interest cover is lower across the board at
higher rates.

Scripts: `tools/backtests/solvency_us/` (common, s1_candidates, s2_fetch, s3_flags, s4_events, s4b_item301_text,
s5_prices, s6_analyze). Outputs: `research_notes/Backtests/solvency_us_outputs/` (panel.csv, results.json, tables.md,
funnel.json). Raw cache in the session scratchpad `bt_solvency/` (not durable).
