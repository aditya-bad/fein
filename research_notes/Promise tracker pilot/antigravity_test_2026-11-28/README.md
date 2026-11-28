# Antigravity vs promise-tracker pipeline: one-call test (28-Nov-2026, Pi)

Stage 3 (signals: promise extraction). Research, not SEBI-registered advice. **n = 1 call. Do not generalise.**

**Input:** SKIPPER Q2FY27 concall (held 30-Oct-2026, filed 5-Nov-2026), public NSE PDF
`skipper_05112026165128_ConcallTranscript.pdf`, `pdftotext -layout`, 6,062 words.
**Ground truth:** the hand ledger in `../scripts_SKIPPER/promises_data.py` (6 entries for this call; the inflow entry holds
two targets, so 7 items: revenue 15% / at worst 13-14%, total inflow 7,500 cr, export inflow 1,500 cr, 450k t by end-Q3/early-Q4,
600k t by FY29, NWC 90-100 days, EBITDA margin 10-11% "come what may").

| Run | How | Output |
|---|---|---|
| Antigravity | `agy --sandbox -p` (1.5.19, telemetry off per user), prompt `agy_prompt.txt`, only the transcript in `~/Desktop/money/agy-work` | `agy_out.jsonl`, 13 items |
| Pipeline | `run.py --no-llm` (79 rule candidates: A 45, B 34) then `llm_extract.py --cmd "claude -p"` | `pipeline_promises.jsonl`, 16 items |

Prompts differ: agy was asked only for **dated and measurable** promises; the pipeline prompt also keeps vague ones (scored at
lower weight). So compare recall on the hand ledger, and precision under each prompt's own standard.

## Recall against the hand ledger (7 items)
| Item | Pipeline | Antigravity |
|---|---|---|
| Revenue +15% (at worst 13-14%) | yes (#8) | yes (#3) |
| Total inflow 7,500 cr | yes (#7) | yes (#4) |
| Export inflow 1,500 cr | yes (#5) | yes (#12) |
| 450k t end-Q3 / early-Q4 FY27 | yes (#1, merged both dates) | yes (#1 H2 + #11 end-Q3/early-Q4, split) |
| 600k t by FY29 | yes (#2) | yes (#2, + #10 phase 2) |
| NWC 90-100 days | yes (#15) | **missed** |
| Margin 10-11% "come what may" (analyst's number, ED: "Absolutely") | partial (#4 "improve, no drop") | partial (#13 "at least +20-30 bps") |
| **Recall** | **6.5 / 7 (93%)** | **5.5 / 7 (79%)** |

Neither run picked up the 10-11% band, because the number came from the analyst and management only said "Absolutely".
That is a known blind spot: confirmations given inside an analyst's question.

## Extra items (not in the hand ledger) and precision
- **Found by both, and valid** (the hand ledger was conservative): Q3 employee cost ~5.5% of revenue; operating cash flow
  >= 75%; greenfield location chosen within Q3FY27; greenfield phase 1 by end-FY28.
- **Antigravity errors:** #6 capex INR 250-300 cr is a description of past annual capex, not a promise (**false positive**).
  #10 and #11 duplicate the 600k t and 450k t items. Valid unique items: **10 / 13 (77%)**.
- **Pipeline:** #3 PAT growth (no number), #9 Engineering growth evens out, #12 "significantly better H2", #13 Infra "large
  growth" are direction-only, and #14 (12% long-term aspiration) has a deadline the pipeline filled in itself (FY28).
  These are valid under its own prompt (vague promises are allowed). Under agy's "dated and measurable" standard it scores
  **11 / 16 (69%)**. No false positives or duplicates.

## Verdict
- On this one call, Antigravity is a **usable second extractor**, but not a replacement: it missed one hand-ledger item (NWC),
  added one false positive, and needs de-duplication. The pipeline (rules + claude -p) had better recall and no false positives.
- Possible use: run agy as a **cross-check** and look only at items one extractor has and the other lacks. Here that would
  have flagged the margin framing (+20-30 bps, which is more precise than the pipeline's "improve").
- Cost: agy ran on the user's Antigravity plan, and the pipeline used 1 `claude -p` call. Antigravity got nothing from memory/,
  memdb, predictions or secrets.
- Next, if wanted: 3-5 more calls from different sectors before deciding (n = 1 is an anecdote).
