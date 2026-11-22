# Promise-tracker pipeline (v1.3, 2026-11-22; v1 2026-11-21)

This pipeline turns the two manual pilots (UNIPARTS, SKIPPER; see `research_notes/Promise tracker pilot/`)
into a repeatable process. It uses the Python standard library only, plus the `pdftotext` (poppler) and
`curl` binaries, so it runs on a Raspberry Pi. The LLM step calls any CLI that reads a prompt on stdin
and prints text: `claude -p` (tested) or the Gemini CLI.
This is research, not SEBI-registered advice.

```
fetch.py ──> turns.py ──> candidates.py ──> llm_extract.py ──> score.py ──> report.py
 NSE list     speaker      rule filter        LLM confirms      screener     MCS, candour,
 + PDFs in    turns,       (high recall)      + structures      numbers +    breakdowns,
 date range   boilerplate                     (JSONL)           chains       memdb seed
```
`run.py` chains all six stages. `validate.py` compares any stage with a manual ledger.

## v1.3 changes (2026-11-22, first US sector: US-WTS, US-AOS, US-SSD, US-LECO)
- **US gate in `score.py`.** A promise is US if its id starts `promise:US-`, or its `symbol` starts `US-`, or `market` is `us`. US
  promises use only the US vocabulary below and **never fall through** to the India/screener measures (INR cr, OPM, debtor days).
  If no US measure matches, the result is *not-auto-scorable* ("US company: no recognised US measure").
  | Measure | Phrases it catches (metric text first) | Scored from |
  |---|---|---|
  | `organic_growth_pct` | "organic" | `--csv` only (company-reported) |
  | `net_sales_growth_pct` | "net sales", "sales/revenue growth", "top line" | `--csv` (SEC XBRL or release) |
  | `segment_sales_growth_pct`, `segment_margin_pct` | the metric names a segment, region, product line or country (Americas, International, Europe, APMEA, Rest of World, North America, boiler, water treatment/heater, automation, Harris, China, India, Leonard) | `--csv` only |
  | `adj_op_margin_pct` / `gaap_op_margin_pct` | "adjusted operating", "operating (income) margin" (GAAP only when the text says "GAAP") | `--csv` only |
  | `adj_ebitda_margin_pct` | "EBITDA" | `--csv` only |
  | `adj_eps_usd` / `gaap_eps_usd` | "EPS", "per share" ("adjusted" or "continuing" -> adjusted) | `--csv` only |
  | `fcf_conversion_pct`, `cash_return_pct_fcf`, `fcf_usd_mn` | "cash conversion", "FCF / net income"; "return ... of free cash flow"; "free cash flow" | `--csv` only |
  | `capex_usd_mn`, `buyback_usd_mn`, `cost_savings_usd_mn`, `price_realisation_usd_mn` | "capex"; "repurchase/buyback"; "savings", "operating expenses"; "price/cost", "price actions" | `--csv` only |
  - Multi-year targets (CAGR, a year 2030+, "across the cycle") and segment/acquired-business **dollar** amounts ("Leonard Valve ~$70 mn") return *not-auto-scorable* (judgment).
  - Margins and ratios use the 0.3 / 1.5 pp thresholds and growth uses the growth thresholds (the sets join `PP_MEASURES` / `GROWTH_MEASURES`); amounts use the 95% / 80% ratio rule.
- **`parse_target(text, us=False)`:** with `us=True` (passed automatically for US promises) it also parses per-share ranges ("$3.42 to $3.52" -> 3.42-3.52 USD/share; "$0.96") and the US growth words "low single digit" 1-3%, "mid single digit" 4-6%, "low teens" 11-13%, "mid teens" 14-16%. India/IT parsing is unchanged.
  - **Known limit:** bp-expansion targets ("+50 to +110 bp") are still read by the bank bps rule as 0.50-1.10 *%* levels. Score these by hand on the expansion (clarification B), or give `target_low/high` explicitly.
- **Scoring US ledgers:** the four 2026-11-22 ledgers were built by hand (`research_notes/Promise tracker pilot/scripts_us_industrials/promises_US-*.py`), not through `fetch.py` (which reads NSE). For a pipeline run on a US company, pass the Motley Fool HTML converted to text, or the 8-K Ex 99.1 press release, as `--local FILE@YYYY-MM-DD` (pdf_to_text is skipped for .txt only if you pre-place the .txt in the cache; simplest is to print the page to PDF). Supply company figures in the `--csv` (field = measure name).
- **Regression check:** all 426 promises in the existing `memdb/seeds/*promises*.json` (India + IT, excluding the new US seed) give the same `infer_measure` and `parse_target` result as v1.2 (0 changed).
- **Scoreboard (`tools/scoreboard/resolve.py`):** `sec_fact` gained `operating_income` (OperatingIncomeLoss), `capex` (PaymentsToAcquirePropertyPlantAndEquipment, else PaymentsToAcquireProductiveAssets) and the ratio `op_margin_pct` = 100 x operating income / revenue (both first-reported, same period rules). One new unit test.
- **Data access notes (US):** fool.com quote pages (`/quote/nyse/<t>/`) list the transcript URLs. Several calls had no Fool page (WTS Q3-25, SSD Q2-26, LECO Q2-25 and Q2-26); guessed slugs 404. Use the 8-K Item 2.02 Exhibit 99.1 instead: `python3 tools/sec_fetch.py filings T --form 8-K --items 2.02`, then `doc T ACCESSION --file <ex99 name> --text` (the `--file` flag is needed; without it the 8-K cover document is downloaded). Lincoln Electric's releases carry almost no outlook; Watts, A. O. Smith and Simpson put the outlook in the release.

## v1.2 changes (2026-11-22, IT mid-caps: PERSISTENT, COFORGE, MPHASIS, KPITTECH)
- **IT measures in `score.py`** (matched on the metric text, after the bank measures and before the segment filter):
  | Measure | Phrases it catches | Scored from |
  |---|---|---|
  | `cc_revenue_growth_yoy_pct`, `cc_revenue_qoq_pct` | "constant currency", "CC growth", "CC QoQ / sequential" | `--csv` only (company-reported) |
  | `usd_revenue_growth_yoy_pct`, `usd_revenue_qoq_pct` | "revenue in USD", "dollar growth", "USD QoQ" | `--csv` only |
  | `ebit_margin_pct` | "EBIT margin", "EBIT band", "operating band" (not EBITDA) | `--csv` (company EBIT governs), else screener (OP − depreciation) / sales |
  | `tcv_usd_mn` | "TCV", "total contract value", "deal wins", "large deals", "bookings", "ACV" | `--csv` (FY = sum of quarters) |
  | `utilisation_pct`, `attrition_pct` (lower is better), `headcount` | "utilisation" (not plant/capacity utilisation), "attrition", "headcount" | `--csv` only |
  | `top5_client_share_pct`, `top10_client_share_pct` (lower is better) | "top 5 / top 10 clients" | `--csv` only |
  - Growth measures use the growth thresholds, margins and people ratios use the 0.3 / 1.5 pp thresholds, and TCV and headcount use the 95% / 80% ratio thresholds.
  - Vertical, geography or client-level CC growth, "organic" or "ex-acquisition" variants, CAGRs and segment EBIT are **blocked**: they return *not-auto-scorable* rather than falling through to INR revenue growth or screener OPM. In v1.1, "EBIT margin 14-16%" was read as EBITDA margin (screener OPM runs about 3 pp higher for IT). "CC growth 10%" was read as INR revenue growth, which can be off by 2-4 pp of FX.
  - **Company EBIT and EBITDA differ from screener for most IT firms** (IT_MIDCAPS_peer_comparison.md, section 3.4). Supply a CSV row `ebit_margin_pct` whenever the company figure is known.
- **`parse_target`:** "USD 500 mn", "$1.5 bn", "$300-350 million" and "$500 mn+" become USD mn (with a floor for "+"). "Double-digit" means ≥10%, "low double-digit" 10-12% and "high single-digit" 7-9%. Previously these returned nothing.
- **`candidates.py` categories:** `deal_wins` (TCV, ACV, large/mega deals, bookings, executable order book; placed before `order_book`/`order_inflow` only for these words). `people` (attrition, utilisation, headcount, freshers, wage hikes). `client_concentration` (top-N clients, $X mn+ client buckets). "Constant currency" and "CC" also count toward `revenue_growth`, and "EBIT band" toward `margin`. The memdb category map (`scripts_it_peers/build_seed.py`) puts the three new categories in the "other" group.
- **Regression check:** all 363 promises in the existing `memdb/seeds/*promises*.json` give the same `infer_measure` and `parse_target` result as v1.1. Plant-capacity "utilisation" (SKIPPER, ENDURANCE) is deliberately excluded from `utilisation_pct`.
- **Data access notes:**
  - Coforge's NSE transcript filings are one-page cover letters with a link. Download the PDFs from `investors.coforge.com/quarter-reports` and pass them with `--local`. Its results, press releases and factsheets *are* on NSE.
  - Persistent's Q4FY26 filing is a cover letter (`persistent.com/wp-content/uploads/2026/04/Analyst-Call-Transcript-Q4FY26.pdf`), and Persistent held no Q1FY27 call.
  - `turns.py` needs `--roster` for Persistent and cannot split Mphasis's layout. For Mphasis, read the raw text.
  - `fetch.py` dated Mphasis's Q1FY26 call 2025-07-01; the correct date is 25-Jul-2025.

## v1.1 changes (2026-11-22, FEDERALBNK dry run: first bank)
- **Cover-letter transcripts:** many banks file only a letter on NSE saying the transcript is on their website.
  `fetch.py` now marks these `cover_letter_only` (not "scanned") and skips them; download the website PDF and pass
  `--local PDF@YYYY-MM-DD` (repeatable, also on `run.py`); it replaces the cover letter for that quarter.
- **Quarter labels:** 7-day lag (banks report in 12–20 days) and a quarter named in the transcript wins.
- **Bank measures** in `score.py`: nim_pct, credit_cost_pct, gnpa_pct, nnpa_pct, slippage_pct, pcr_pct,
  cost_income_pct, cod_pct, cof_pct, yield_advances_pct, casa_ratio_pct, roa_pct, roe_pct, cet1_pct, crar_pct,
  cd_ratio_pct, loan/deposit/casa/fee growth. bps targets are parsed ("40-50 bps" → 0.40–0.50%); ratios use a
  5-bp (tight) or 0.3-pp (wide) tolerance; segment growth and multi-year CAGRs are left to judgment.
  v1 mapped "net interest margin 3.2%" to finance cost (a false miss).
- **`bank_kpis.py`** builds the `--csv` from NSE integrated-filing XBRL (GNPA/NNPA %, CET1, RoA, NII, opex,
  provisions, EPS) plus a `--manual` CSV of deck KPIs (company definitions). Screener's bank page lacks these.
- **Bug fixes (all companies):** "18-20%" was parsed as −20% (dash read as a minus sign); chains now compare the
  ceiling for lower-is-better measures and treat "by FY28" → "at some point" as a goalpost move; a *pending*
  original target is no longer pre-judged moved-goalpost (flag `goalpost_flag`, resolve at its deadline). On the
  19-Nov pilot seeds: SKIPPER auto moved-goalposts 12 → 9 and restatements 4 → 7, statuses otherwise unchanged;
  UNIPARTS unchanged.
- Candour heuristic no longer treats "slippage(s)" as an admission; bank categories added to the LLM prompt.

## Usage
```bash
cd tools/promise_tracker/pipeline
export PT_CACHE=~/pt_cache            # or pass --cache DIR to every script
# full run (first time: ~10 calls x ~2-4 min of LLM time)
python3 -I run.py SKIPPER --since 2024-07-01 --llm-cmd "claude -p" --as-of 2026-11-19
# quarterly update: same command plus --refresh-list. Only the new call is downloaded and sent to the LLM.
# without an LLM: stops after candidates and writes ready-to-paste prompts
python3 -I run.py SKIPPER --since 2024-07-01 --no-llm

# stage by stage
python3 -I fetch.py SKIPPER --since 2024-07-01 [--until 2026-11-30] [--refresh]
python3 -I turns.py SKIPPER [--roster "Name One,Name Two"]     # or: turns.py --txt f.txt --print
python3 -I candidates.py SKIPPER [--min-tier A] [--emit-prompts DIR]
python3 -I llm_extract.py SKIPPER --cmd "claude -p"            # or --cmd "gemini -p ''"
python3 -I financials.py SKIPPER [--csv-out numbers.csv]       # inspect the parsed screener tables
python3 -I score.py SKIPPER --promises $PT_CACHE/SKIPPER/promises.jsonl [--csv fixes.csv] --as-of 2026-11-19
python3 -I report.py SKIPPER --scored $PT_CACHE/SKIPPER/scored.jsonl --candour-auto \
        --seed-out seed.json --md-out SKIPPER_credibility.md --json-out summary.json
# score a pilot ledger directly (memdb seed JSON)
python3 -I score.py SKIPPER --seed memdb/seeds/2026-11-19_promises_SKIPPER.json --as-of 2026-11-19 --out s.jsonl
python3 -I report.py SKIPPER --scored s.jsonl --status-source manual --as-of 2026-11-19
```
**Human corrections** go in `<out>/<SYMBOL>_overrides.jsonl`, one object per line, for example
`{"id": "...", "human_status": "missed", "admitted_unprompted": false}`. They are merged before scoring
and always take precedence.

**Seed output** is written to the path you give; nothing is written into `memdb/seeds/` automatically.
Review the seed, copy it into `memdb/seeds/`, then run `python3 -m memdb add --json-file`. Promise ids
follow the pilot scheme, `promise:SYM:<said_on>:<slug>`. The analysis id is
`analysis:SYM:credibility-YYYY-MM`. Each promise carries `data.supersedes`, `data.restates` and
`supersedes`/`restates` links.

### Files
| File | What it does |
|---|---|
| `common.py` | Cache layout, the Indian fiscal calendar, date parsing |
| `fetch.py` | Pulls the NSE announcement list with the short UA `Mozilla/5.0` and filters it to transcript PDFs (catches typos such as "Trancript"; skips .zip files). Downloads **only the PDFs in the date range**, which fixes pilot lesson 1. Runs `pdftotext -layout`, detects the call date (the "held on …" date, never the quarter-end date) and the quarter. Flags PDFs that look scanned (fewer than 1,500 words; these need OCR). |
| `turns.py` | Splits the text into speaker turns: management, analyst, moderator or host. Speaker roles are resolved in this order: (1) the cover-page roster, merged across all of the company's calls, with fuzzy matching (handles "Parmjit Soni", "Paramjit Sonis", "Aditya Dujari :", dropped middle names); (2) generic labels such as "Management:"; (3) analysts named in the moderator's announcement; (4) a content vote. Each turn records `role_basis` so it can be audited. Turns are tagged opening / qa / closing. Removes the cover letter, page headers, safe-harbour text and operator housekeeping. Optional `rosters.json` maps `{SYMBOL: [names]}`. |
| `candidates.py` | Rule-based extraction of forward-looking sentences. Signals: guidance verbs; numbers with %, ₹/INR/cr, tonnes, days; qualitative magnitudes ("mid-teens", "double-digit", "flat"); timelines (FY28, Q3FY27, H2, "next year", "in 2-3 years", "end of the year", month names). A metric may come from the analyst's question when the answer only says "it". Also catches "Yes, absolutely" answers that endorse a target the analyst stated. Output is `candidates.jsonl` with quote, speaker, call date, section, volunteered flag, the question being answered, numbers, and a deadline resolved with the **later-date rule** (`assumed` explains each choice). Tier A = strong, tier B = directional. |
| `llm_extract_prompt.md` | Prompt template for the LLM confirmation and structuring step. The output schema matches `score.py`'s input: measure vocabulary, period, target_low/high, comparator, deadline rules, `chain_key`, `restates_earlier`, `acknowledges_revision`. |
| `llm_extract.py` | Runs the template call by call, oldest first. Feeds the `chain_key`s already used into each later prompt so the same target keeps the same key. Validates the output and assigns ids. Caches raw output in `llm/`. |
| `llm_candour_prompt.md` | Optional per-shortfall prompt: "was this miss admitted unprompted?" |
| `financials.py` | Fetches the screener.in consolidated page with curl (cached for 3 days) and parses the quarterly, P&L, balance-sheet, cash-flow and ratio tables. A CSV can be supplied instead or as an override. |
| `score.py` | Auto-scores financial promises and builds the supersedes chains (details below). |
| `report.py` | MCS, weighted delivery ratio, hit rate, candour index; breakdowns by category, driver (cycle vs execution), specificity, volunteered/prompted, year said and speaker; markdown ledger; memdb seed. |
| `validate.py` | Compares pipeline output with a manual ledger (recall/precision, field agreement, status agreement, goalposts). |
| `run.py` | Orchestrator. |

### How score.py decides
- **Measures** it can check against screener: revenue YoY / QoQ / absolute (quarter, half or FY),
  EBITDA margin (screener OPM, which excludes other income, or including other income when the
  promise says so), PAT growth / absolute, finance cost % of revenue, debtor days, ROCE, FCF,
  dividend payout and borrowings. Capex counts only if it is in a CSV or `--derived-capex` is set,
  because screener has no capex line and the balance-sheet proxy is rough.
- The scorer **does not touch** segment, export, order-book/inflow, capacity, market-share,
  "normalised"/ex-FX or company-defined working-capital metrics (pilot lesson 7). These keep the
  LLM or human status.
- **Thresholds** are fixed across companies (pilot lesson 4):
  - Growth targets: delivered within max(0.5 pp, 5% of the target); partly within max(2 pp, 20%).
  - Margin, ROCE and finance-cost targets: delivered within 0.3 pp; partly within 1.5 pp.
  - Amounts and days: delivered at 95% of the target or better; partly at 80-95%.
  - Explicit floors and ceilings ("25% plus", "below 4.5%") are strict: delivered only if met;
    partly if within 2.5% (relative).
  - Beating a target counts as delivered.
  - A level target met on the TTM figure one quarter after the deadline counts as partly.
- **Fuzzy deadlines.** The period scored is the fiscal period that contains the deadline. Per-quarter
  run-rate targets are divided by the number of quarters in that period. Vague or missing deadlines
  default to the fiscal year two years after the call and are flagged.
- **Supersedes chains.** Promises are grouped by the LLM's `chain_key`, or by `measure+period`.
  Without either, they are clustered by category and metric-token Jaccard similarity; per-period flows
  only chain within one fiscal year, and ordinal words ("second 75k block") must match.
  - A later statement with the same target is linked with `restates`.
  - A later statement with a lower target or a later date is linked with `supersedes`. If it was not
    flagged `acknowledges_revision`, that is a **goalpost move**, counted once per new statement.
  - Final status: an earlier promise that was quietly superseded and whose original target was not
    met becomes `moved-goalpost`. If the revision was acknowledged, it becomes `withdrawn`.
- **"Silently dropped?"** is only ever a *suggestion*: a material, unresolved promise that is not
  restated in the following 4 calls (pilot lesson 5).

## Validation (as of 2026-11-19, the pilots' as-of date)
Pilot ledgers: 68 manual promises each. There are 10 calls per company, the same transcripts as the
pilots, re-fetched from NSE. All 20 call dates detected match the pilots.

### 1. Formula reproduction (report.py on the manual statuses)
| | MCS | Weighted delivery ratio | Hit rate | Candour |
|---|---|---|---|---|
| UNIPARTS pilot | +0.28 | – | 55% | ~5% |
| UNIPARTS report.py | **+0.280** | 65.7% | 55.3% | 4.8% |
| SKIPPER pilot | −0.18 | 41.3% | 33.3% | 12.5% |
| SKIPPER report.py | **−0.178** | 41.3% | 33.3% | 12.5% |

The formula is identical to the pilots.

### 2. Speaker turns
- 67/68 manual quotes per company fall inside a turn labelled management.
- The one exception per company is a quote spanning an analyst interjection.
- Volunteered/prompted flags agree with the manual ledger 95% (SKIPPER) and 98% (UNIPARTS) of the time.

### 3. Candidate extraction (rules only) vs the manual promise list
| | SKIPPER | UNIPARTS |
|---|---|---|
| Recall, tier A | 75% | 78% |
| **Recall, tier A+B** | **93%** (63/68) | **88%** (60/68) |
| Candidates per call (manual promises per call) | 79 (6.8) | 79 (6.8) |
| Precision vs manual (lower bound), A / A+B | 17% / 11% | 14% / 9% |
| Text kept | ~25% of management sentences | ~20% |

How to read these:
- **Precision vs manual is a lower bound.** The pilots logged only material promises.
- In a 40-sentence hand spot-check of unmatched candidates, about 35% were still promise-like
  forward statements (about 18% clearly checkable). The rest were past results, industry commentary
  or boilerplate. That is the LLM's job to drop.
- **The misses (13 in total) are mostly anaphoric answers.** Examples: "I think all those
  expectations are definitely still continuing"; "we'd rather be conservative and outperform"; and a
  quote split across a page break. This supports pilot lesson 2: give the LLM the full Q&A
  exchange, not single sentences.

### 4. Rules + LLM (claude -p on all 20 calls, ~2-4 min per call)
| | SKIPPER | UNIPARTS |
|---|---|---|
| LLM promises | 204 | 154 |
| **Recall vs manual** | **87%** (59/68) | **85%** (58/68) |
| Precision vs manual (lower bound) | 36% | 40% |
| Field agreement on matched pairs: category / deadline FY / volunteered / specificity | 73% / 73% / 97% / 71% | 93% / 83% / 97% / 81% |
| Restatements linked by `chain_key` | 57 | 55 |

How to read these:
- The LLM keeps about 3x as many promises as the pilots did. Many are restatements, now linked
  rather than double-counted, and minor items.
- Expect a human to trim: about 20 records per call to review, down from about 80 candidates.

### 5. Auto-scoring of financial promises vs manual status
| | SKIPPER | UNIPARTS |
|---|---|---|
| Manual promises the scorer accepts (coverage) | 20/68 (29%) | 23/68 (34%) |
| **Numbers only, both resolved: exact agreement** | **8/11** | **14/14** |
| Same, using the LLM-structured version of each promise | 5/7 | 11/11 |
| After the chain rule, both resolved: exact / direction | 7/12 / 10/12 | 14/14 / 14/14 |
| LLM path after the chain rule: exact | 9/16 | 12/13 |
| Moved goalposts, manual / auto / both | 9 / 12 / 5 | 6 / 2 / 2 |

**The disagreements are boundary cases, not arithmetic errors:**
- SKIPPER "below 4.5%" finance cost: actual 4.63%. The pilot called it missed; the late rule gives
  partly because the next quarter's TTM figure met it.
- ">25% in FY25 and FY26": the pilot gave partly as a composite of the two years; the scorer
  only checks FY26, so it says missed.
- The FY26 "25% plus" revenue chain: the pilot said missed; the chain rule says moved-goalpost
  because the guidance was relabelled "aspirational" and cut without being acknowledged. Arguably the
  stricter reading is correct, but it is a judgment call. The rule pushes SKIPPER's hybrid MCS from
  −0.18 to −0.34.
- UNIPARTS goalposts missed by inference: the Mexico storyline sits under different metric names and
  categories. LLM `chain_key`s fix this partly. The pilot's "H2 > H1 / Q4 highest" shape promise is
  not auto-scorable.

**Coverage is about 30%, not the ~60% the pilot hoped for.** The gap is promises that are financial
but not on screener: segment revenue (polymer, aftermarket, infra), order inflow and order book,
capex, and company-defined working-capital days. The next step is to parse the quarterly results
PDFs (`nse_fetch.py results`) for segment data and feed them in as `--csv`.

### 6. Candour (`report.py --candour-auto`, keyword heuristic)
- On 34 shortfalls where the manual ledger records admitted-unprompted: TP 3, FN 2, FP 2, TN 27.
- The candour index it produces happens to match the pilots (4.8% and 12.5%), but n is tiny.
- Use `llm_candour_prompt.md` or a human for anything that matters.

### 7. Headline MCS from the LLM path alone (not usable on its own)
- SKIPPER −0.64 (44 scored); UNIPARTS +0.52 (21 scored).
- Only auto-resolved and chain-resolved items are scored. The judgment items (segment, execution,
  M&A) remain pending until a human or LLM status is added, so these numbers are biased.
  Pilot values are −0.18 and +0.28.

## What still needs human or LLM judgment
1. **Status of non-financial promises.** Commissioning dates, Mexico/IMMEX, acquisitions, segment
   targets, order inflow. About 65-70% of promises. Use overrides (`human_status`).
2. **Moved-goalpost vs missed vs withdrawn.** Was a revision acknowledged? The LLM's
   `acknowledges_revision` flag helps, but the pilot rule ("revised before the deadline without
   saying so") needs a second reader on every flagged chain.
3. **Composite promises** ("25% in FY25 *and* FY26", "Q3 < Q2, Q4 highest, H2 ≈ H1"). Split them into
   one record per check, or score them by hand.
4. **Company definitions vs screener.** EBITDA including other income; NWC or inventory days on the
   company's own basis. The scorer refuses these unless `measure` says otherwise; keep both figures.
5. **Candour.** Whether a miss was admitted unprompted.
6. **Materiality, and whether an LLM promise is worth keeping.** Trim the roughly 3x over-extraction.
7. **"Silently dropped".** Suggested only; it may have been met, or be immaterial.
8. **Cycle confound.** Read MCS next to an industry cycle indicator (UNIPARTS lesson 7).

## Known limits / next steps
- Scanned PDFs need OCR (`tesseract`, not installed). `fetch.py` flags them.
- NSE only; BSE-only companies need `tools/bse_fetch.py` (HTTP/2).
- Segment numbers are not covered: add a results-PDF/XBRL parser that writes the `--csv` format.
- Data access is fragile: NSE and screener change hosts, headers and markup without notice.
  Re-run `financials.py SYMBOL` and `fetch.py` each quarter as a smoke test.
- Precision tuning: candidates are deliberately high-recall. If the LLM budget on the Pi is tight,
  use `--min-tier A`, which loses about 15 points of recall.
