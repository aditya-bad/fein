# Promise-credibility forward test (Nov-2026 cohort) — PRE-REGISTRATION

Written 2026-11-25 (session date), **before** the frame was built, before any company was drawn and before any
transcript of a candidate company was read. The text above the heading "Frame and walk log" is not edited after it
is saved; its sha256 is recorded in the walk log. Research, not SEBI-registered advice.

**Roadmap:** stage 3 (signal: management credibility) → stage 7 (scorekeeping). Answers strategy_review §4
"Does sector-adjusted credibility predict delivery better than the sector base rate?" Unlocks: if it passes,
credibility becomes a stage-6 input (decision card probability adjustment); if it fails, credibility stays a
descriptive deep-dive section only and the rule-generated credibility calls stop.

**Seen before writing (disclosed):** the industry map's sector value counts over the whole map (Capital Goods 249,
Chemicals 127, Healthcare 113, ...) and the map rows of KEC/KPIL/SKIPPER/SANSERA/UNIPARTS/COFORGE; the existing T&D
ledgers (KEC, KPIL, SKIPPER; 169 resolved promises, strict delivery: all 0.40, revenue/orders 0.35, margin 0.48,
dates 0.28, balance-sheet 0.47, other 0.56); the earlier credibility-call rule (AUTO_COMPONENTS_peer_comparison.md §5:
p = p0 + N/(N+20)·SAC). No mcap, filing or transcript of any Capital Goods / Chemicals / Healthcare candidate was looked at.
The seed is fixed by the caller (20261210), so prior knowledge of names cannot steer the order.

## 1. Selection (fixed now)
1. **Frame.** `research_notes/Backtests/india_pead_live/universe.csv` joined to `industry_map.csv` on symbol. Mcap =
   shares × close / 1e7 (₹ cr), close = latest NSE bhavcopy (`sec_bhavdata_full_DDMMYYYY.csv`, try 25-, 24-, 23-Nov-2026;
   frame close date = the file's DATE1 column, L42; series EQ/BE/BZ). Keep 1,000 ≤ mcap ≤ 20,000. Unpriced dropped (counted).
2. **Sectors (exact map `sector` values):** `Capital Goods` (overlapping: SKIPPER is mapped Capital Goods, and the T&D
   peer ledger KEC/KPIL/SKIPPER supplies an existing peer base rate), `Chemicals` (new; L44 open item), `Healthcare` (new).
3. **Exclusions:** prior live/practice deep-dive subjects (SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA, SHK,
   UTTAMSUGAR, CUMMINSIND, VMM, FEDERALBNK, FIVE) and promise-tracker companies (KPIL, SKIPPER, KEC, UNIPARTS, SANSERA,
   SONACOMS, HAPPYFORGE, ENDURANCE, PERSISTENT, COFORGE, MPHASIS, KPITTECH, GULFPETRO, REPRO).
4. **Draw.** One `rng = random.Random(20261210)`. For sector in the order Capital Goods, Chemicals, Healthcare: eligible list
   sorted alphabetically by symbol, `rng.shuffle(list)`, walk in order, accept the first 4 passing the check below.
5. **Check (only skip reason): concall coverage.** `tools/nse_fetch.py transcripts SYM` lists **≥ 6 earnings-call
   transcripts filed 2025-01-01 → 2026-11-25** (distinct calls; cover-letter-only filings whose website PDF can be fetched
   count; scanned/unreadable ones do not), **and ≥ 1 call held on or after 2026-07-15** (Q1 or Q2 FY27, the source of
   forward promises). Fail = skip, logged with the count. No other judgment skip. An accepted company stays in the test even
   if it yields zero forward calls (reported as 0; dropping it would bias the sample).

## 2. What is a scoreable promise
A management statement in an earnings call (opening remarks or Q&A, management speaker) that is **forward-looking,
attributable to the company, and has (a) a measurable target** (a number, range, floor/ceiling, or a discrete event such as
commissioning / approval / launch / closing / repayment) **and (b) a deadline** that is explicit or resolvable with the
pipeline's later-date rule (FY27 = 31-Mar-2027; "by end of Q4" = quarter end; "H1 FY28" = 30-Sep-2027; undated = excluded,
not FY+2, for forward calls). Industry/macro commentary, "aspirations" without a number or date, and multi-year CAGRs
due after Jul-2027 are not scoreable.
- **Past promises (credibility input):** said in calls from 2025-01-01, deadline on or before 2026-09-30, resolved from
  later calls, results (screener/NSE XBRL) or filings as delivered / partly / missed / moved-goalpost / withdrawn /
  silently-dropped (pipeline v1.4 thresholds: growth within max(0.5 pp, 5% of target), margins 0.3 pp, amounts 95%,
  explicit floors strict, dates: done by the deadline). Unresolvable = excluded. Repeated restatements of one target are
  one promise (chain rule: the earliest statement, scored once).
- **Forward promises (the test):** said in the latest available call (or the one before if not restated later), deadline
  **2026-12-01 → 2027-07-31** (Q3 FY27, Q4/FY27, Q1 FY28, or a dated event), each with a written YES/NO rule resolvable
  from an NSE filing, results XBRL/screener, or a call/press release. Numeric YES threshold = target low end minus the
  pipeline's "delivered" tolerance (so YES ≡ "delivered" in the base-rate data); floors/ceilings strict; events: YES only if
  a document dated ≤ deadline + 75 days states it happened on or before the deadline. One forward call per chain; at most
  6 forward calls per company (most material first: revenue/orders, margin, dated events, balance sheet) so one company
  cannot dominate.

## 3. Outcome coding and categories
Strict outcome y = 1 if delivered, else 0 (partly, missed, moved-goalpost, withdrawn, silently-dropped = 0). Category
groups: **revenue** (revenue_growth, order_inflow, order_book, deal_wins), **margin**, **dates** (capacity_commissioning,
capex, new_product, approval_regulatory, m&a, customer_win), **balance_sheet** (debt_reduction, working_capital), **other**.

## 4. Probabilities (both fixed by rule; no judgment)
- **Baseline P_base = p0(sector, group):** the pooled strict delivery rate of the company's *sector peers excluding the
  company itself* (leave-one-out) in that category group. Peer pool: Capital Goods = the 3 other drawn Capital Goods
  companies + KEC, KPIL, SKIPPER ledgers; Chemicals / Healthcare = the 3 other drawn companies of that sector. If the peer
  pool has < 8 resolved promises in the group, use the peer pool's all-group rate; if that is < 8, use the pooled rate of all
  12 drawn companies + T&D ledgers in that group (leave-one-out); if still < 8, 0.5.
- **Credibility SAC_i** (sector-adjusted credibility, in probability units) = mean over company i's resolved past promises of
  (y − p0(sector, group of that promise)). N_i = number of those promises.
- **P_cred = clip(p0 + w_i · SAC_i, 0.05, 0.95), w_i = N_i / (N_i + 20)** (empirical-Bayes shrink, prior weight 20 promises;
  same k as the Nov-2026 credibility calls, so results are poolable). If N_i < 3, P_cred = P_base.
- Exploratory only (reported, not decisive): P_raw = clip(p0 + SAC_i) (no shrink), and P_co = company's raw past hit rate.

## 5. Scoring and decision rule
- Each forward call is scored at resolution with Brier for P_cred and for P_base. ΔB = mean Brier(P_base) − mean
  Brier(P_cred) (positive = credibility helps).
- **Uncertainty:** company-cluster bootstrap (resample companies with replacement, 10,000 draws, `random.Random(20261210)`),
  90% percentile CI of ΔB.
- **Minimum data:** ≥ 30 resolved forward calls from ≥ 8 companies. Below that: "insufficient", no verdict; the cohort is
  pooled with the next season's cohort under the same rule.
- **PASS ("credibility predicts"):** ΔB ≥ +0.005 **and** 90% CI lower bound > 0.
  **FAIL:** ΔB ≤ 0, or 90% CI upper bound < +0.005. **INCONCLUSIVE:** anything else.
- **Secondary (reported, not decisive):** hit rate of forward calls by credibility tercile (companies ranked by SAC_i; top 4 /
  middle 4 / bottom 4); a working signal should show top − bottom ≥ 10 pp. Also ΔB pooled with the 38 Nov-22 credibility
  calls (same rule family) and calibration (mean P vs hit rate) for both forecasters.
- **Power note (stated now):** with w ≈ 0.3–0.5 and |SAC| ≈ 0.1–0.25, P_cred differs from P_base by only ~0.03–0.12, so the
  expected |ΔB| is ~0.002–0.015. INCONCLUSIVE is the most likely single-season result; the test is designed to be pooled.
- **Voids:** a call is void only if the company is delisted/merged or stops publishing the metric and no document can decide it;
  voids are listed, never silently dropped. No call, threshold or probability is edited after this cohort is saved.
