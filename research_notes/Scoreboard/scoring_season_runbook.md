# Scoring season runbook, Jan–Jul 2027 (stage 7: scorekeeping)

*Written 2026-11-25. Run it by hand in a cloud session; the Pi cron is deferred. Research tooling, not SEBI-registered advice.*
**Unlocks:** the first resolved calls → Brier vs base by method → the phase-B gate (≥50 resolved, clearly positive skill)
and the pre-registered evaluations at the bottom. Background: `tools/scoreboard/README.md`; the dry run is in `dry_run_2026-11-25.md`.

## 0. Session setup (fresh cloud container, about 2 minutes)
```bash
cd /home/user/fein && git pull --ff-only
which pdftotext || sudo apt-get install -y poppler-utils    # needed for the NSE PDFs; curl and flock are already there
python3 -m memdb stats                                     # rebuilds the sqlite index if it is missing
python3 -m unittest discover -s tools/scoreboard/tests     # 31 tests, no network
```
The HTTP cache (`~/.cache/fein_scoreboard`) does not survive a new container. That is fine: the first run refetches it at
polite rates, which takes about 5–10 minutes when results are in.

## 1. The weekly run (Mondays; also daily in peak weeks)
```bash
python3 tools/scoreboard/calls.py                          # re-export calls; check its output for "NEEDS SPEC"
python3 tools/scoreboard/resolve.py                        # live: seed (if anything resolved) + review_queue.md + resolver_status.md
#   read research_notes/Scoreboard/review_queue.md -> add decisions (section 2) -> run resolve.py again
tools/scoreboard/apply.sh                                  # writes outcomes to memdb, then refreshes scoreboard.md + curriculum block
git add memory/store memory/curriculum.md research_notes/Scoreboard memdb/seeds tools/scoreboard/specs.json
git commit -m "scoreboard: weekly run YYYY-MM-DD" && git push
```
To preview before memdb changes, use `resolve.py --dry-run --report /tmp/x.md` and `scoreboard.py --seed memdb/seeds/<seed>.json`.
To replay one call, use `resolve.py --only TICKER --dry-run`. The resolver is idempotent: calls already in a seed or not
`open` are skipped, so running it twice does no harm.

| Weeks (2027) | What lands | Due | Run |
|---|---|---|---|
| 4–31 Jan | INFY guide, US big banks/PG/ISRG/UNH guides, PNC NII | 6 calls by 31-Jan (1 auto, 5 assisted) | weekly; review on 1-Feb |
| 10 Jan–14 Feb | India Q3 FY27 results (deadline 14-Feb); US Q4 8-Ks | 33 by 28-Feb (21 auto, 12 assisted) | **daily 20-Jan → 20-Feb** |
| 15 Feb–31 Mar | US 10-Ks (SEC XBRL FY calls), India event deadlines (31-Mar) | 31 in Mar (15 auto, 16 assisted) | twice a week |
| Apr | TVS Q4 volumes, Q4 bank/NBFC KPIs start, INDOTECH pledge (Mar SHP) | 7 | weekly |
| 15 May–7 Jun | India FY27/Q4 results (deadline 30-May); DECK 10-K | **54 in May, mostly 31-May (33 auto, 18 assisted, 3 human)** | **daily 15-May → 7-Jun** |
| Jun | event deadlines 30-Jun (OPTU, CAT dividend, AAPL buyback…) | 20 (incl. 7 price calls ending 30-Jun) | weekly |
| 2–10 Jul | price calls (end 30-Jun; checked from 2-Jul), last events | 2 (+ the June price calls, read from 2-Jul) | once, then season close (section 5) |

Later in 2027: 14 calls (Sep–Nov: beats-Nifty500/SPY to 30-Sep, Sunflag/Indramedco events). The 24 five-year
card tail calls resolve in Nov-2031.

## 2. The review queue (where most of the work is)
`review_queue.md` lists each call that needs a human, with its written rule, the reason, the resolver's proposal, and
evidence links with snippets. The reasons are: assisted doc scan, type d judgment, sources disagree, near the
threshold, the company's own figure governs, and **OVERDUE** (resolve_by has passed with no data).
1. Open the evidence link. Apply the **written rule** (memdb `resolution_rule`) strictly. A proposal is a lead, not an
   outcome: the regex catches the *first* number, and that can be H1, a normalised figure, or the prior quarter. Known
   traps: ICICIGI (H1 vs quarter), MPHASIS (the rule wants the reported DSO, not the "normalised" one), and GE (no number is captured; read the snippet).
2. Append one line to `review_decisions.jsonl` (an outcome of 1 or 0 needs a `source`):
   `{"id": "thesis:paper-call:X:y", "outcome": 1, "value": 24.3, "source": "https://…", "source_date": "2027-02-05", "note": "Q3 press release p2", "decided_by": "user"}`
   Use `"void"` only when the source stopped publishing the metric, or when the rule says "not disclosed = void" (for example ENDURANCE driveshaft). Never void a call because it was a miss.
3. Run `resolve.py` again. The decision becomes a seed, and `apply.sh` writes it to memdb.
4. Claude may draft decisions in a session. The user confirms type d calls and anything within the guard of the threshold (`decided_by` records who decided).

## 3. Recording outcomes and post-mortems in memdb
- Outcomes go into memdb only through `apply.sh`, which runs `python3 -m memdb add --json-file memdb/seeds/<date>_scoreboard_resolutions.json`.
  It keeps the same id with status `resolved`/`void` and adds `data.outcome`, `brier`, `evidence` and `resolved_on`. Old versions stay in the JSONL. Do not hand-edit the store.
- For each call listed under "Post-mortems owed" (|p − outcome| > 0.6), write a post-mortem:
  `python3 -m memdb add --type analysis --title "Post-mortem: <call>" --ticker X --tag post-mortem --tag paper-call --link <call id>:post_mortem_of --body "what we missed / was it the method or the data" --confidence verified`
- Add a lesson to `memory/lessons.md` only when a pattern repeats across ≥3 misses of one method.

## 4. Brier and calibration report
`scoreboard.py` (run by `apply.sh`) writes `scoreboard.md`: overall, by method/market/sector/batch, a 10-bin calibration
table (ours and base), post-mortems owed, and the resolved list. It also appends a row to `history.csv` and rewrites
only the block between the SCOREBOARD markers in `memory/curriculum.md`. Read method-level numbers only once a method has
≥5 resolved calls. Skill = 1 − Brier(ours)/Brier(base), on calls that state a base rate (the 7 pilot calls are
scored for "ours" only). At each month end, add a manual dated row to the curriculum scoreboard table and give the user a short summary.

## 5. Season close (after the 2–10 Jul run): the pre-registered evaluations
Write each result as a memdb `analysis` (tag `season-2027h1`). Link it to the decision. Report the bootstrap CI on skill, not just the point estimate.
1. **Sector-adjusted credibility** (§4 open question; `research_notes/Promise tracker pilot/*_peer_comparison.md`).
   There are 38 calls with method `promise-tracker credibility (sector-adjusted, rule-generated)`: 16 auto-ancillary,
   11 IT and 11 US industrials. 14 are auto and 24 assisted, and all resolve Feb–Jul 2027. Test: Brier(ours) vs
   Brier(sector base) on the same calls, with a paired bootstrap CI on the difference, overall and by sector. The power
   sits in the calls where P(ours) − P(base) is large (Endurance, Sona). Report how many calls differ by ≥5 pp. A
   verdict of "adds skill" needs the CI to exclude 0. Otherwise the verdict is "not shown" (not "refuted") at n=38.
2. **`decision:card-audit-fixes-prereg-2026-11-25`.** Adopt fixes (1), (5) and (6) regardless. Fixes (2)–(4) need
   *resolved card calls*. **No card tail call resolves in 2027** (all 24 resolve in Nov-2031), so the "raw vs anchored
   tails" comparison cannot run at this season close (open decision, flagged 2026-11-25). What can run: card EV
   vs realised for the near-term calls from the same live dives (8 beats-index calls resolve 30-Sep-2027, plus the
   dives' Q3/FY27 operating calls). Never lower the hurdle to open cards.
3. **L39 "both flags" follow-up** (`memory/lessons.md` L39 addendum). This is not an evaluation this season. It is a
   *pre-registration to freeze*. After the Q3 FY27 results (mid-Feb) and again after FY27 (June), list the Indian
   non-financials with pledge >25% AND interest cover <1.5x at each results date. Commit the event list and the rule
   ("both flags → 0 new money"; outcomes are 12-month halving and 3-year failure versus single-flag and no-flag firms)
   **before** any outcome is known. The 12-month verdict is due in 2028.
4. Then update `memory/strategy_review.md` §4 and `next_steps.md`, and decide which methods earn their place (strategy review §3 item 5).

## 6. When something breaks
- The NSE API returns an empty list or a 403: it is transient. Rerun later; the resolver never decides on a missing source.
- Screener is blocked: India structured calls wait. They go single-source only at or after resolve_by, and only beyond the guard.
- A call says `NO SPEC`: copy the nearest spec of the same kind into `specs.json`, then run the tests and `resolve.py --dry-run --only X`.
- A spec disagrees with the written rule: fix the spec with a one-line edit. The rule always wins.
- SEC: XOM now resolves to *ExxonMobil Holdings Corp* (CIK 2115436, the 2026 holding-company reorganisation). Its 8-Ks file there, so this is expected.
