# Paper-call scoreboard (roadmap stage 7: scorekeeping)

Resolves our forward paper calls from primary data, scores them (Brier and log loss) against the base rate
each call stated, and keeps a calibration table. Built 2026-11-22. It uses only the Python standard library,
plus the `curl`, `pdftotext` (poppler-utils) and `flock` binaries, so it runs on a Raspberry Pi from cron.
**What it unlocks:** the phase-B gate (≥50 resolved calls clearly beating base rates). It also gives a
method-level skill score that steers stages 3–6 (which methods to trust, which to drop).
Research tooling, not SEBI-registered advice.

```
memdb (thesis, tag paper-call)
   │  calls.py      export + classify ──► research_notes/Scoreboard/calls.csv, calendar.md, calendar.ics
   ▼
resolve.py  ──fetch (only when due)──► NSE XBRL · screener · NSE pledge/announcements · Yahoo v8 · SEC EDGAR
   │   decides 1/0 only from structured data; everything else → review_queue.md (+ .jsonl)
   │   human decisions ◄── research_notes/Scoreboard/review_decisions.jsonl
   ▼
memdb/seeds/<date>_scoreboard_resolutions.json ──apply.sh──► python3 -m memdb add --json-file (same id: status
   │                                                         "resolved"/"void", data.outcome/brier/evidence)
   ▼
scoreboard.py ──► research_notes/Scoreboard/scoreboard.md, history.csv,
                  memory/curriculum.md (ONLY between <!-- SCOREBOARD:START --> and <!-- SCOREBOARD:END -->)
```

## Files
| File | What |
|---|---|
| `sb_common.py` | paths, memdb loading/normalising, Brier/log loss, polite cached HTTP (`$SB_CACHE`, default `~/.cache/fein_scoreboard`) |
| `specs.json` | **curated machine-checkable spec per call** (type, source, metric, period, threshold, guard, check_from). The written rule in memdb always wins; if a spec disagrees with the rule, fix the spec |
| `calls.py` | export open calls to `calls.csv`; heuristic classifier (`type_auto`) next to the curated `type`; calendar |
| `sources.py` | fetchers (NSE integrated-filing XBRL, screener via `promise_tracker/pipeline/financials.py`, NSE pledge + announcements, Yahoo v8, SEC via `tools/sec_fetch.py`, PDF/HTML → text) |
| `resolve.py` | decision engine + review queue + seed writer |
| `scoreboard.py` | metrics, groups, calibration, curriculum block |
| `apply.sh` | applies unapplied resolution seeds to memdb, then refreshes the scoreboard |
| `run_daily.sh` | cron wrapper: calls → resolve → apply → scoreboard, with a lock and a log under `state/` |
| `tests/test_scoreboard.py` | 31 unit tests: synthetic calls with known Brier values, every resolver path, no network; `tests/fixtures/` holds a trimmed real banking XBRL (UTKARSHBNK Q2 FY27) |

## Resolution types (the 77 calls open on 2026-11-22)
| Type | Meaning | Calls | Automation |
|---|---|---|---|
| a | reported number vs threshold (revenue, margin, op profit, growth, EPS, NII, pledge %, NIM, GNPA, AUM, VNB, order inflow…) | 48 | 28 structured (22 India via NSE XBRL + screener, incl. the INDOTECH pledge; 6 US via SEC XBRL), 20 assisted (company-defined KPIs in press releases/decks/8-K exhibits) |
| b | price return vs Nifty 50 / SPY (Yahoo v8 closes) | 7 | 7 structured |
| c | corporate event or guidance (8-K 1.03 bankruptcy, dividend raise, buyback, regulatory order, deal closing, commissioning, ICFR remediation, initial guidance) | 18 | 2 structured (OPTU 8-K 1.03, CAT dividend), 16 assisted |
| d | human judgment (basis "as the company counts it", "most popular plan") | 4 | AUBANK, TATAPOWER, NTPC, BHARTIARTL |

`structured` = the resolver may decide. `assisted` = the resolver finds the documents, pulls snippets and the
first number that matches, and *proposes* an outcome; a human confirms. `human` = judgment queue (it still
gathers documents). The heuristic classifier agrees with the curated type on 75 of the 77 calls. The two
differences are deliberate: TRANSRAILL is kept as type a, and NTPC is kept as type d.

**Banks (added 2026-11-25).** NSE files bank results in the IFBanking taxonomy, not Ind AS, so `india_fin`
detects it (`InterestEarned` present, no `RevenueFromOperations`) and reads `sources.bank_period_values`:
`net_profit_cr` (ProfitLossForThePeriod), `interest_earned_cr`, `interest_expended_cr`, `nii_cr`, `other_income_cr`,
`opex_cr`, `ppop_cr`, `provisions_cr`, `pbt_cr`, `gnpa_pct` / `nnpa_pct` (PercentageOfGrossNpa / PercentageOfNpa,
fraction x 100), `cet1_pct`, `at1_pct`, `roa_pct` (quarterly, not annualised), and `advances_cr` / `deposits_cr`
(balance sheet at period end). Any `<x>_growth_pct` uses `<x>_cr`. Screener adds `net_profit_cr` as the second
source. **Not tagged** (calls stay assisted): total CRAR (only CET1 and AT1 ratios), gross loan portfolio / AUM,
NIM, credit cost. NBFC filings (Ind AS taxonomy) carry no GNPA tag either (SBICARD stays assisted).

## Rules that keep it honest (never resolve early on partial data)
- **Check dates.** Before `check_from`, no network is used for a call. India Q3 FY27 results are checked from
  10-Jan-2027 and FY27 from 15-Apr-2027. US checks start around each company's report date. Price calls are
  checked from 2-Jul-2027.
- **Exact periods.** An India number is used only when the NSE XBRL has a context with *exactly* the quarter
  or fiscal-year dates, or when screener has that column. For a US fiscal year, the 10-K for that year must
  be filed, and Q4 = FY − 9-month YTD (or a tagged 3-month Q4).
- **Two sources for India.** NSE XBRL and screener must land on the same side of the threshold. If the
  value is within `guard` of the threshold and the two sources differ by more than 0.3 pp (or 1%), or the
  rule says the company's own figure governs, the call goes to review. A single source is used only on or
  after `resolve_by`, and only when it is further than `guard` from the threshold.
- **Prices.** The resolver uses the last close on or before the end date. It reads that close only after
  the end date has passed and a later bar exists (or 4 days have gone by), and only if the close is within
  6 days of the end date. If the Yahoo start close differs from the rule's base price by more than 0.5% and
  there was no split, the call goes to review. Yahoo `close` is split-adjusted, not dividend-adjusted, which
  matches the rules.
- **Events.** YES comes only from a structured signal: an 8-K Item 1.03, or a Yahoo dividend of at least the
  required amount with an ex-date on or before the deadline. A NO is always a proposal for a human to confirm.
- **Overdue.** If `resolve_by` passes with no data, the call goes to review marked OVERDUE (decide, or void
  if the source stopped publishing). It is never auto-voided.
- **Skips.** Calls already in a resolution seed are skipped, and calls whose memdb status is not `open` are
  skipped.

## Human review workflow
1. Read `research_notes/Scoreboard/review_queue.md`. Each entry has the rule, why it is there, the
   resolver's proposal, and evidence links with snippets.
2. Apply the **written rule** strictly, then append one line to
   `research_notes/Scoreboard/review_decisions.jsonl`:
   `{"id": "thesis:paper-call:ICICIGI:q3fy27-combined-ratio-103-5-or-better", "outcome": 1, "value": 102.9, "source": "https://nsearchives…pdf", "source_date": "2027-01-20", "note": "Q3 n-basis incl. CAT, press release p1", "decided_by": "user"}`
   - `outcome`: 1, 0 or `"void"`. A 1 or 0 needs a `source`.
3. The next `resolve.py` run turns the decision into the seed. `apply.sh` writes it to memdb.
4. Write a post-mortem for every call where |p − outcome| > 0.6. `scoreboard.md` lists them under
   "Post-mortems owed".

## Commands
```bash
python3 tools/scoreboard/calls.py                       # export + type counts + calendar
python3 tools/scoreboard/resolve.py --dry-run --report research_notes/Scoreboard/dry_run.md --probe-past
python3 tools/scoreboard/resolve.py --only POLYCAB --today 2027-02-01 --dry-run   # replay one call
python3 tools/scoreboard/resolve.py                     # live: seed (if any) + review queue + status
tools/scoreboard/apply.sh                               # memdb add --json-file for unapplied seeds, then scoreboard
python3 tools/scoreboard/scoreboard.py [--seed FILE]    # --seed previews an unapplied seed (no curriculum write)
python3 -m unittest discover -s tools/scoreboard/tests -v
```
`--probe-past` fetches the latest *completed* period for every structured type-a call (Q2 FY27, FY26, or the
prior US fiscal year). It prints values only, as a check that the data path works. It never decides a call.

## Cron (Raspberry Pi, daily 22:00 IST)
If the Pi clock is on IST:
```cron
0 22 * * * cd /home/pi/fein && tools/scoreboard/run_daily.sh
```
If the Pi clock is on UTC (22:00 IST = 16:30 UTC):
```cron
30 16 * * * cd /home/pi/fein && tools/scoreboard/run_daily.sh
```
Optional extras:
```cron
# Monday 07:00 IST: refresh the repo first
0 7 * * 1 cd /home/pi/fein && git pull --ff-only -q
```
For local commits after each run, use `SB_GIT_COMMIT=1 tools/scoreboard/run_daily.sh` (it never pushes).
To review before memdb is touched, use `SB_AUTO_APPLY=0`.
Logs go to `tools/scoreboard/state/run_YYYY-MM-DD.log` and `state/resolver_log.jsonl` (both gitignored).
Pi prerequisites: `sudo apt-get install -y poppler-utils curl util-linux` (pdftotext, curl, flock).

## Adding new calls (each results season)
1. Add the calls to memdb as usual (`thesis`, tag `paper-call`, `data.probability`,
   `data.base_rate_probability`, `resolve_by`, `resolution_rule`, `resolution_source`).
2. Run `calls.py`. Any call printed under **NEEDS SPEC** will go to review until it gets a `specs.json` entry.
   Copy the nearest existing spec of the same kind.
3. Run the tests and `resolve.py --dry-run --probe-past` to check the new spec fetches data.

## Known limits (2026-11-22)
- **Screener vs XBRL definitions.** On Q2 FY27 most structured calls agree to within 0.05 pp. Two do not:
  Sona BLW (XBRL OPM 23.04% vs screener 22.53%) and Kaynes (13.18% vs 12.59%). Screener reclassifies some
  items. On the real Q3 data, the disagreement rule sends any such case to review. That matters most for
  SONACOMS, whose threshold is 23.0%.
- **NSE pledge endpoint.** It returned an empty list on 22-Nov-2026, a Sunday. The resolver treats an empty
  answer as transient and retries the next night. INDOTECH is not checked before Apr-2027 anyway.
- **Assisted regexes.** These were tested on Q2/Q3-2026 documents: P&G organic +4% ("four percent") and the
  ICICI Lombard combined ratio. They capture the *first* match, which can be the wrong period. In the
  ICICI Lombard test it caught H1 instead of the quarter. A proposal is never an outcome.
- **The 7 pilot calls (20-Nov-2026).** They have no written resolution rule and no base rate. Their specs
  are taken from their titles, and they are scored for "ours" but left out of skill vs base. Consider
  adding a base rate before they resolve.
- **Possible two-source upgrades.** HUL and Marico (company-reported EBITDA governs) and the bank/NBFC KPIs
  are assisted only. `tools/promise_tracker/pipeline/bank_kpis.py` could move GNPA/NIM checks to
  structured later.
