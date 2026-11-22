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
