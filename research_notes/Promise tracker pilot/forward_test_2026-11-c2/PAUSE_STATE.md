# Cohort 2 — pause state (2026-11-26, paused at the coordinator's request; user low on usage)

**Done:** prereg.md (sha256 43f23229…4563, saved 07:21 UTC before the frame) plus the Check-A walk log; draw.py and
selection_order.json (frame close 25-Nov-2026). All 6 drawn names pass Check A: INTELLECT and RATEGAIN (IT), SFL and GREENLAM (Consumer
Durables), SUPRAJIT and LANDMARK (Auto). Skipped for having no transcripts: BOSCH-HCIL, LAOPALA, BANCOINDIA. Check B (>= 10 scored past
promises) has not been run yet for any company. Scripts written: normalize_speakers.py (already applied to the INTELLECT and SFL cached text),
resolve_past.py (written, not yet run), build.py, and forward_c2.py (SECTOR and NAME filled in; FWD still empty).

**Pipeline cache:** `/root/pt_cache_c2/<SYM>/` (PT_CACHE). LLM outputs are cached per call in `llm/<date>.raw.txt`, so re-running only
calls the model for calls that are still missing.
| Company | LLM-extracted calls / total | Next step |
|---|---|---|
| Intellect Design Arena (INTELLECT) | 14/14 | the score.py + report.py step was killed mid-run: re-run run.py (no model calls needed) |
| Greenlam Industries (GREENLAM) | 14/14 | same as INTELLECT |
| Suprajit Engineering (SUPRAJIT) | 11/14 | re-run run.py: 3 calls left |
| RateGain Travel Technologies (RATEGAIN) | 3/17 | re-run run.py with `$(cat /root/pt_cache_c2/RATEGAIN.locals)` (website PDFs in /root/pt_dl/RATEGAIN) |
| Sheela Foam (SFL) | 2/14 | re-run run.py |
| Landmark Cars (LANDMARK) | 3/14 | re-run run.py |

Command (from tools/promise_tracker/pipeline, `export PT_CACHE=/root/pt_cache_c2`):
`python3 -I run.py SYM --since 2023-07-01 --as-of 2026-11-26` (for INTELLECT add `--local /root/pt_dl/INTELLECT/q4fy26.pdf@2026-05-14`).
Run at most 3 at a time: the first attempt hit the usage limit with 6 running in parallel.

**After extraction, for each company:**
1. `python3 -I resolve_past.py SYM --cache /root/pt_cache_c2 --name "<Company>"`.
2. Claude reviews the output, writes past_c2.json (rows: sym, said_on, category, y, status, title, evidence, id) and applies Check B
   (N < 10 → skip the company and draw the next name in selection_order.json: IT 3rd = AURUM, CD 5th = MAYURUNIQ, Auto 4th = MMFL).
3. Add forward calls (deadline Dec-2026 to Jul-2027, max 6 per company) to forward_c2.py FWD, taken from the Q2FY27/Q1FY27 promises with
   their quotes checked against the transcript text.
4. Run build.py.
5. memdb: `add --json-file memdb/seeds/2026-11-26_promise_forward_test_c2.json`.
6. Add the specs_lines.txt lines to tools/scoreboard/specs.json as one-line inserts before the final `}`. Do not reformat; another agent
   has appended VIYASH lines.
7. Write the README, then `ingest-md` with `--tag research --tag promise-tracker`.
If usage is tight, finish fewer companies cleanly. INTELLECT and GREENLAM are the closest to done.

## Cache backup (added by lead, 26-Nov-2026)
The pipeline cache lives in /root/pt_cache_c2/ (111 MB, outside the repo; lost if the container is reclaimed).
The expensive part — model extraction outputs (*.jsonl), md and logs — is backed up here as `extraction_cache.tgz`.
To restore: `mkdir -p /root/pt_cache_c2 && tar xzf extraction_cache.tgz -C /root/pt_cache_c2`. PDFs/text are re-fetchable.

## Paused again (lead, 28-Nov-2026)
Second run stopped at the weekly usage limit while doing the LANDMARK resolver with SFL extracting in parallel. User asked to
pause everything for Pi setup. Cache re-backed-up into extraction_cache.tgz (now includes llm/*.raw.txt). Resume from the
table above; check run logs in /root/pt_cache_c2/<SYM>*.log (or restore the tgz) to see which steps finished.
