# Promise-credibility forward test — cohort 2 (Nov-2026) — PRE-REGISTRATION

Written 2026-11-26 (session date), **before** the cohort-2 frame was built, before any company was drawn and before any
transcript of a candidate company was read. The text above the heading "Frame and walk log" is not edited after it is
saved; its sha256 is recorded in the walk log. Research, not SEBI-registered advice.

**Roadmap:** stage 3 (signal: management credibility) → stage 7 (scorekeeping). Same question as cohort 1
(`../forward_test_2026-11/prereg.md`, sha256 990c8180…435aec): "Does sector-adjusted credibility predict delivery better
than the sector base rate?" Built to fix lesson L49 (cohort 1 had only 1–6 scored past promises per company, so P_cred
barely moved). Results are **pooled with cohort 1** under the same probability and decision rules. Unlocks: credibility
as a stage-6 decision-card input if the pooled test passes; credibility stays descriptive if it fails.

**Seen before writing (disclosed):** the industry map's sector value counts (Information Technology 86, Consumer Durables 90,
Automobile and Auto Components 86, ...) and the map rows of the existing pilot companies; the existing India concall ledgers
in `memdb/seeds/` (status counts only: IT 4 companies 27 resolved, auto/HAPPYFORGE 30 resolved, UNIPARTS 47, T&D 169) and
cohort 1's 36 past promises and 38 calls. No mcap, filing or transcript of any IT / Consumer Durables / Auto candidate was
looked at. The seed is fixed by the caller (20261211).

## 1. Selection (fixed now)
1. **Frame.** Same as cohort 1: `research_notes/Backtests/india_pead_live/universe.csv` joined to `industry_map.csv` on
   symbol. Mcap = shares × close / 1e7 (₹ cr), close = latest NSE bhavcopy (`sec_bhavdata_full_DDMMYYYY.csv`, try 26-, 25-,
   24-Nov-2026; frame close date = the file's DATE1 column; series EQ/BE/BZ). Keep 1,000 ≤ mcap ≤ 20,000. Unpriced dropped (counted).
2. **Sectors (exact map `sector` values, none in cohort 1), in this order:** `Information Technology`, `Consumer Durables`,
   `Automobile and Auto Components`. 2 companies per sector, 6 in all.
3. **Exclusions:** prior live/practice deep-dive subjects (SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA, SHK,
   UTTAMSUGAR, CUMMINSIND, VMM, FEDERALBNK, FIVE, VIYASH); cohort 1 (JASH, KIRLOSBROS, RISHABH, ANUP, NEOGEN, GALAXYSURF,
   YASHO, TATVA, KRSNAA, ORCHPHARMA, SYNGENE, SHILPAMED); promise-tracker pilots (KPIL, SKIPPER, KEC, UNIPARTS, SANSERA,
   SONACOMS, HAPPYFORGE, ENDURANCE, PERSISTENT, COFORGE, MPHASIS, KPITTECH, GULFPETRO, REPRO).
4. **Draw.** One `rng = random.Random(20261211)`. For sector in the order above: eligible list sorted alphabetically by symbol,
   `rng.shuffle(list)`, walk in order, accept the first 2 that pass both checks below.
5. **Check A (transcript coverage, before reading):** `tools/nse_fetch.py transcripts SYM` (or the company website where NSE
   files a cover letter) gives **≥ 12 distinct earnings-call transcripts of calls filed 2023-07-01 → 2026-11-26**
   (cover-letter-only filings count if the website PDF can be fetched; scanned/unreadable ones do not), **and ≥ 1 call held on
   or after 2026-07-15**. Fail = skip, logged with the count.
6. **Check B (the one change vs cohort 1, after reading):** after the full pipeline read (§2), the company must have
   **≥ 10 scored (resolved) past promises** (chain-deduplicated, §2). Fewer = skip, logged with N, draw the next name in the
   same sector's shuffled order. No other judgment skip. An accepted company stays even if it yields zero forward calls.

## 2. Reading and what is a scoreable promise
- **Full pipeline read, not tier-A shortcuts:** `tools/promise_tracker/pipeline` v1.4 — `fetch.py --since 2023-07-01` (all
  calls in the window, ≥ 12), `turns.py`, `candidates.py` (tiers A **and** B), `llm_extract.py --cmd "claude -p"` on every
  call (the LLM sees the full management Q&A context per the prompt template), `score.py` (screener numbers, chain rule).
  Claude then reviews every extracted promise: confirms the status from screener/XBRL or from later calls/filings, sets
  `human_status` overrides where the auto status is wrong or missing (human > numbers > LLM, report.py hybrid), and
  marks the rest unresolvable. Unresolvable = excluded.
- **Past promises (credibility input):** as cohort 1 §2 (forward-looking, attributable to the company, measurable target,
  deadline explicit or resolvable with the later-date rule), except the window: **said in calls held 2023-07-01 onwards,
  deadline on or before 2026-09-30**. Outcomes delivered / partly / missed / moved-goalpost / withdrawn / silently-dropped with
  pipeline v1.4 thresholds (growth within max(0.5 pp, 5% of target), margins 0.3 pp, amounts 95%, explicit floors strict,
  dates done by the deadline). Repeated restatements of one target = one promise (chain rule: the earliest statement, scored once).
  Vague-deadline promises (pipeline FY+2 default) are kept only if the FY+2 deadline is ≤ 2026-09-30 and Claude confirms the
  statement implied that horizon; otherwise excluded.
- **Forward promises (the test):** identical to cohort 1 §2: said in the latest available call (or the one before if not
  restated later), deadline **2026-12-01 → 2027-07-31**, each with a written YES/NO rule resolvable from an NSE filing, results
  XBRL/screener, or a call/press release; numeric YES threshold = target low end minus the pipeline's "delivered" tolerance;
  floors/ceilings strict; events YES only if a document dated ≤ deadline + 75 days states it happened by the deadline. One call
  per chain; **at most 6 per company** (most material first: revenue/orders, margin, dated events, balance sheet). Undated = excluded.

## 3. Outcome coding and categories (copied from cohort 1)
Strict y = 1 if delivered, else 0. Groups: **revenue** (revenue_growth, order_inflow, order_book, deal_wins), **margin**,
**dates** (capacity_commissioning, capex, new_product, approval_regulatory, m&a, customer_win), **balance_sheet**
(debt_reduction, working_capital), **other** (everything else, incl. people, client_concentration).

## 4. Probabilities (copied from cohort 1; only the peer pools are new)
- **P_base = p0(sector, group):** pooled strict delivery rate of the company's sector peers **excluding the company itself**
  (leave-one-out) in that group. If the peer pool has < 8 resolved promises in the group, use the peer pool's all-group rate;
  if that is < 8, use the pooled all-India rate in that group (leave-one-out); if still < 8, 0.5.
- **Peer pools:** Information Technology = the other drawn IT company + PERSISTENT, COFORGE, MPHASIS, KPITTECH
  (`memdb/seeds/2026-11-22_promises_it.json`). Automobile and Auto Components = the other drawn auto company + SONACOMS, SANSERA,
  ENDURANCE (`2026-11-22_promises_sectors.json`) + UNIPARTS (`2026-11-19_promises_UNIPARTS.json`). **Consumer Durables has no
  existing peer ledger**, so its p0 is the **pooled all-India group rate** (leave-one-out), stated as such in every record.
- **Pooled all-India set:** every India concall ledger — T&D (KEC, KPIL, SKIPPER), UNIPARTS, the 4 IT and 4 auto/capital-goods
  pilot ledgers (incl. HAPPYFORGE), cohort 1's 36 past promises, and the cohort-2 ledgers. Excluded: US ledgers and AR-mode
  ledgers (L37: not comparable). Resolved = status not in (None, pending, unverifiable).
- **SAC_i** = mean over company i's resolved past promises of (y − p0(sector, group of that promise)); N_i = count.
- **P_cred = clip(p0 + w_i · SAC_i, 0.05, 0.95), w_i = N_i / (N_i + 20)**; if N_i < 3, P_cred = P_base (cannot happen here,
  N ≥ 10 by Check B). Exploratory only: P_raw = clip(p0 + SAC_i), P_co = company raw hit rate.

## 5. Scoring and decision rule (copied from cohort 1; pooling made explicit)
- Brier for P_cred and P_base per resolved call. ΔB = mean Brier(P_base) − mean Brier(P_cred) (positive = credibility helps).
- **Primary verdict = pooled cohort 1 + cohort 2** (same rule family, 18 companies): company-cluster bootstrap (10,000 draws,
  `random.Random(20261210)`, cohort 1's seed), 90% percentile CI of ΔB. Minimum data ≥ 30 resolved calls from ≥ 8 companies.
  **PASS:** ΔB ≥ +0.005 and CI lower bound > 0. **FAIL:** ΔB ≤ 0, or CI upper bound < +0.005. **INCONCLUSIVE:** otherwise.
- **Cohort 2 alone** (reported, not decisive; 6 companies < 8 → "insufficient" by the minimum-data rule): ΔB, bootstrap with
  `random.Random(20261211)`, tercile hit rates (top 2 / middle 2 / bottom 2 by SAC), calibration.
- **Power note (stated now):** with N ≈ 10–40, w ≈ 0.33–0.67 and |SAC| ≈ 0.1–0.3, P_cred − P_base ≈ 0.03–0.20 (vs ≤ 0.10 in
  cohort 1). Pooled INCONCLUSIVE remains likely after one season; cohort 2 raises the expected |ΔB| per call.
- **Voids:** only if delisted/merged or the metric is no longer published and no document can decide; listed, never dropped.
  No call, threshold or probability is edited after this cohort is saved.

## Frame and walk log
