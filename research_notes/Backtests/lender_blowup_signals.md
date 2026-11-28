# Do lender blow-up signals beat the lender base rate? (pre-registration, 2026-11-28)

**Stages:** 2 (hard filters, lender version) and 6 (decision: card blow-up floor for lenders). **Unlocks:** either a
lender-specific blow-up floor for the v1.6b card patch (today the lender floor is size-only, which L54 found adds
nothing), or a recorded "no" so lender cards keep anchoring to the 27% class rate. Parents: insight:lender-blowup-signals,
L41 (+ follow-up), L48, L54, analysis:blowup-model-test-2026-11-26.
**Status of §A: written and saved BEFORE any signal or result in §B was computed.** No live card or card code is changed.
Research, not SEBI-registered advice.

## A. Pre-registration (frozen 2026-11-28, before computing)

### A1. Sample and outcome
- Rows: `base_rates_lenders_india_outputs/panel.csv` — the 107 lender company-starts (64 companies; T = 30-Sep-2016,
  30-Sep-2018; mcap ₹1,000–20,000 cr), weight 1, same row rule as L54 (no row excluded: none lacks R5 without failing).
- Outcome y = `o_fail` (5-yr blow-up: close ≤0.2× T close, liquidation, compulsory delisting, equity write-off). 29 events.
- Secondary outcome (reported, never decides): permanent blow-up `o_fail ∧ (R5 ≤ 0.5 or no R5)`.

### A2. Data (public, no login, no CAPTCHA)
- The screener.in public company page already cached for each row by the base-rate build (scratchpad `bt_solv_in/sc/<slug>/page.html`),
  copied with an as_of stamp to `lender_blowup_signals_outputs/data/`. Annual columns (standalone, as screener shows by default).
- FY0 = the Mar column used by the panel (`snap`: FY2016 → Mar-2016, FY2018 → Mar-2018); FY−1 = the previous Mar column.
  Both are public before T (annual results are out by May–Jun of the FY0 year, T = 30-Sep).
- **Not computable for the whole panel at T from public no-login sources, so NOT tested here (honest gap):** GNPA % and
  credit cost (screener shows GNPA only for the last ~13 quarters; BSE API returns 403/Akamai to scripts, checked
  2026-11-28), CET1/CRAR (not on screener; in Pillar-3 / annual-report PDFs only), ALM 1-yr gap and CP share (NBFC annual
  report PDFs), ARC sales / write-offs (annual-report notes), RBI divergence, concentration. The test uses **balance-sheet
  and P&L proxies** for those signals, listed next. A null here therefore says "these proxies don't help", not "the
  signals don't work".

### A3. Signals (binary, fixed now; L = loan-book proxy = Total Assets − Investments − Fixed Assets − CWIP; NW = Equity Capital + Reserves)
Primary set (exactly 4, enter M1):
| Flag | Insight signal it proxies | Definition at T |
|---|---|---|
| GROW | fast loan growth (insight: >30%/yr) | L(FY0) / L(FY−1) − 1 > 30% |
| WEAKPROF | rising credit cost / bad-loan recognition | ROA = Net Profit(FY0) / avg(Total Assets FY−1, FY0) < 0.4% (incl. losses) |
| THINCAP | thin capital buffer (CET1/CRAR, leverage) | NW / Total Assets (FY0) < 6.5% for banks (kind = bank), < 12.5% (≈8x leverage) for NBFC/HFC/FI |
| WHOLESALE | wholesale / non-deposit funding (ALM, CP reliance) | Borrowing / (Deposits + Borrowing) (FY0) > 50% |

Secondary (reported univariately and in the flag count, never in M1): HIGHYIELD = Revenue(FY0)/avg Total Assets ≥ 13%
(high-yield book); COSTUP = (Expenses/avg TA) FY0 − FY−1 ≥ +0.5pp (provisions surge; screener Expenses include provisions);
CAPFALL = NW/TA FY0 − FY−1 ≤ −0.5pp (falling buffer); COUNT2 = ≥2 of the 4 primary flags (the insight's "two+ flags" rule).
Missing input → flag = 0 (not fired); coverage per flag is reported; a primary flag with coverage < 80% is reported but its
result is marked unreliable.

### A4. Models
- **M1** = L2-penalised logistic on the 4 primary flags, same code as L54 (`blowup_model.py` fit_logit: prior N(0,1),
  intercept unpenalised, Newton, prediction clipped [0.02, 0.60]).
- **B** = training-fold blow-up rate (the lender base rate as the card would know it).
- **M2 (reported, cannot rescue a failed M1):** two-bucket rule = training-fold rate among COUNT2 firms vs the rest.
- Split: **leave-one-cohort-out** (train FY2016 → test FY2018 and vice versa). Full-panel fit reported for the card.

### A5. Metrics
Per held-out cohort and pooled: Brier, log score, CITL (mean predicted − realised), AUC **within the held-out cohort**
(ranking only, free of the cohort level shift), reliability by predicted tertile (pooled). Bootstrap (2,000 draws,
companies resampled, seed 20261128) 95% CI of the pooled Brier difference M1 − B (reported, not deciding). Fitted
coefficients per fold.

### A6. Adoption rule
**M1 is adopted** only if (a) its Brier is lower than B's **in each of the two held-out cohorts**, AND (b) the mean of the
two within-cohort AUCs is **≥ 0.65**. Otherwise: not adopted; lender cards keep the class base rate (via the v1.6b
max(anchored, model) floor with the existing size-only model, unchanged) and the result is recorded as a null for the proxies.
If adopted: a proposed, unapplied patch on top of v1.6b replaces the lender model entry with the full-panel M1 fit and its
flag inputs, with tests.

### A7. Honest caveat about n
107 company-starts, 64 companies (43 appear twice), 29 blow-ups, 2 cohorts that disagree on the level (34.6% vs 20.0%).
With ~18 and ~11 events per held-out cohort, an AUC of 0.65 has a standard error of roughly ±0.08–0.10 and a Brier
difference of 0.005 is noise. Many blow-ups are one system event (2016 PSU-bank AQR / merger path; 2018–20 NBFC funding
freeze; Mar-2020 crash counted by the price rule in 8 of 29). A pass would be a weak "use it", a fail a weak "no", and
neither generalises beyond one Indian credit cycle.

---
## B. Results (computed after §A was saved)

**Order of work (audit trail, file mtimes UTC):** §A saved 2026-11-28 13:21:46; script
`tools/backtests/lender_blowup_signals/lender_signals.py` final edit 13:23:17; `lender_blowup_signals_outputs/results.json`
13:23:22. §A text was not edited after computing. Git can't prove the order (nothing committed yet); the mtimes and this log do.

**B0. Data and one extraction fix (no definition changed).** 64 screener public pages (fetched 2026-11-22 by the
base-rate build, no login) copied to `lender_blowup_signals_outputs/data/<slug>.page.html.gz` with `annual_tables.json`
(as_of + URL per page). First run found older-format pages (mostly merged/dead firms) label rows `Sales` / `Borrowings` and,
for banks, fold deposits into `Borrowings`. Fix before reading any result table: alias Sales→Revenue, Borrowings→Borrowing;
for old-format banks WHOLESALE is *unknown* (→ 0 by §A3; a deposit-funded bank is ≤50% wholesale in any case). Coverage
after the fix: GROW, WEAKPROF, THINCAP, HIGHYIELD, COSTUP, CAPFALL 100%; WHOLESALE 82% (≥80% → usable). Pages are
standalone, so holding-company rows (IIFL Holdings 2016, Reliance Capital, SREI, Equitas Holdings) show the parent, not
the lending book — a known noise source. Per-row metrics and flags: `lender_blowup_signals_outputs/flags.csv`.

### B1. Flags one by one (pooled, n = 107, 29 blow-ups = 27.1%)
| Flag | n on | blow-up if on | if off | permanent if on | on/events FY2016 · FY2018 |
|---|---|---|---|---|---|
| GROW (loan proxy > +30%) | 18 | **22.2%** | 28.1% | 11.1% | 6/1 · 12/3 |
| WEAKPROF (ROA < 0.4%) | 39 | 30.8% | 25.0% | 25.6% | 21/9 · 18/3 |
| THINCAP (NW/TA < 6.5% bank, < 12.5% non-bank) | 48 | **35.4%** | 20.3% | 31.2% | 26/12 · 22/5 |
| WHOLESALE (borrowing > 50% of funding) | 47 | **34.0%** | 21.7% | 23.4% | 21/8 · 26/8 |
| HIGHYIELD (revenue/TA ≥ 13%), secondary | 24 | **20.8%** | 28.9% | 4.2% | 11/2 · 13/3 |
| COSTUP (expenses/TA +0.5pp), secondary | 48 | 29.2% | 25.4% | 22.9% | 18/8 · 30/6 |
| CAPFALL (NW/TA −0.5pp), secondary | 31 | 32.3% | 25.0% | 19.4% | 12/5 · 19/5 |
| COUNT2 (≥ 2 of the 4 primary), secondary | 54 | **35.2%** | 18.9% | 29.6% | 27/12 · 27/7 |

### B2. Primary: leave-one-cohort-out, M1 (4 flags) vs B (training-fold base rate)
| Held-out cohort (n, blow-ups, real rate) | Forecast | Brier | Log score | Mean pred | CITL | AUC within cohort |
|---|---|---|---|---|---|---|
| FY2016 (52, 18, 34.6%) | **M1** | **0.2417** | −0.694 | 19.5% | −15.1pp | 0.612 |
| | B | 0.2477 | −0.703 | 20.0% | −14.6pp | — |
| | M2 (COUNT2 buckets) | 0.2382 | −0.679 | 20.3% | −14.3pp | 0.613 |
| FY2018 (55, 11, 20.0%) | **M1** | **0.1734** | −0.527 | 32.4% | +12.4pp | 0.594 |
| | B | 0.1814 | −0.552 | 34.6% | +14.6pp | — |
| | M2 | 0.1783 | −0.541 | 34.0% | +14.0pp | 0.591 |
| Pooled | M1 | 0.2066 | −0.608 | | −1.0pp | 0.528 (pooled) |
| | B | 0.2136 | −0.625 | | +0.4pp | |
| | M2 | 0.2074 | −0.608 | | +0.3pp | |

- Bootstrap (2,000 company-resamples) 95% CI of pooled Brier M1 − B: **[−0.034, +0.022]** — the improvement is not
  distinguishable from zero.
- Coefficients (log-odds): train FY2018 → {GROW +0.08, WEAKPROF +0.10, THINCAP +0.41, WHOLESALE +1.01}; train FY2016 →
  {GROW −0.43, WEAKPROF +0.47, THINCAP +0.77, WHOLESALE +0.68}. Full panel: const −1.998, GROW −0.276, WEAKPROF 0.454,
  THINCAP 0.781, WHOLESALE 1.074. Only THINCAP and WHOLESALE keep their sign and size across folds.
- Reliability (M1, pooled tertiles, pred → real): 14.3% → 28.6%, 24.5% → 20.0%, 38.8% → 32.4% — not monotone; the cohort
  level shift (each cohort forecast from the other's 20% / 35% level) dominates calibration, exactly as in L54.

### B3. Verdict by the pre-registered rule (§A6)
- (a) Brier below B in **both** held-out cohorts: **yes** (−0.0060 FY2016, −0.0080 FY2018).
- (b) mean within-cohort AUC ≥ 0.65: **no — 0.603** (0.612, 0.594).
- → **NOT ADOPTED.** No card patch. Lender cards keep anchoring to the 27.1% class rate through the existing v1.6b floor
  (size-only lender model, unchanged).

### B4. Honest reading
- **The proxies rank weakly, the Brier gain is small and inside the noise.** AUC ~0.60 means a flagged lender is
  somewhat more likely to blow up, not reliably so. Brier gains of 0.006–0.008 sit inside a CI of ±0.03.
- **Thin capital and wholesale funding are the only stable signals** (35% and 34% vs 20–22%; same sign in both folds).
  This fits the insight (equity a thin slice; NBFC funding freeze 2018–20). COUNT2 (the insight's "two+ flags") also
  separates: 35% vs 19%.
- **Fast growth and high yield point the *wrong* way here** (22% and 21% vs 27–29%; HIGHYIELD permanent blow-up only 4%).
  In this window the fast-growing, high-yield lenders (Bajaj-type NBFCs, gold and microfinance lenders) were the winners;
  the blow-ups were slow-growing, thin-capital PSU banks and wholesale-funded HFCs. One cycle is not a law. "Growth >30%"
  in the insight was about corporate books over several years, and this one-year, all-lender proxy can't test that.
- **Secondary outcome (does not decide):** on *permanent* blow-up (fell to ≤0.2x and never came back) the same M1 ranks
  better: within-cohort AUC **0.69 / 0.77**, Brier 0.1816 vs B 0.1930 pooled, and beats B in both cohorts (0.249 vs 0.260,
  0.118 vs 0.130). The main outcome counts the Mar-2020 crash (8 of 29 blow-ups recovered), which the balance-sheet flags
  shouldn't be expected to predict. **This is post-hoc and can't be adopted from this run.** It is the obvious next
  pre-registration (outcome = permanent blow-up, the same 4 flags and code), best run on new start cohorts (FY2014,
  FY2020) so it isn't tested on the data that suggested it.
- **What wasn't tested:** GNPA, credit cost, CET1/CRAR, ALM gaps, CP share, ARC sales and write-offs (no public no-login
  source at T for the panel; BSE API 403). The L41 rules for live cards (CET1 book, GNPA walk) stand. They're
  judgment-level checks, and this backtest neither supports nor refutes them.
- n caveat as §A7: 29 events, 2 cohorts, one credit cycle.

### B5. Next
1. Pre-register "permanent blow-up" as the lender outcome with the same 4 flags. Test it on new cohorts (needs FY2014 /
   FY2020 lender starts from stage 1), not on these 107 rows.
2. If an XBRL/annual-report route to GNPA and CRAR at T opens (no login), add them as a second prereg; they're the signals
   the insight actually names.
3. On live lender cards, write THINCAP / WHOLESALE / COUNT2 in the evidence notes, as information only. They don't move P(blow-up)
   off the class rate.

_Research, not SEBI-registered advice._
