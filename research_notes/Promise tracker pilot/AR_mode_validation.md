# Promise tracker: annual-report mode (v1.4) validation

**Date:** 2026-11-23 · **Analyst:** Claude · **Tool:** `tools/promise_tracker/pipeline/` v1.4 (`ar_fetch.py`, `ar_sections.py`,
`ar_run.py`, `regress_concall.py`; README section "v1.4 changes").
**Roadmap:** stage 3 (signals). The tool extends management-credibility scoring to companies that hold no earnings calls.
It unlocks a credibility read and a disclosure-quality read in stage-4 deep dives of small caps (the SUNFLAG gap, `research_notes/Deep dives/SUNFLAG_live.md` section 10, item 2).
This is research, not SEBI-registered advice.

## 0. Bottom line
1. **The mechanics work.** The tool fetches the last 5 annual reports (ARs) per company, extracts the text, deletes the PDFs, finds the forward-looking zone, rebuilds the tables, runs the existing candidates/score/report modules, and uses later ARs as evidence. The concall outputs are **byte-identical** to the reference version (section 6).
2. **SUNFLAG (vs the hand ledger in SUNFLAG_live.md section 5.4):** the asset tracker reproduces **17/17** ledger cells (5 mines x 3 reports, plus the 2 FY26 wins). It finds the only dated promise ("EC and Stage I clearances ... by end of September 2026", status pending). It flags the **unchanged Belgaon extractable balance of 5.391 MT** in AR FY24 and AR FY25, the stale-disclosure catch made by hand.
3. **Two seeded-random no-concall small caps (GULFPETRO, REPRO):** I hand-read one AR each. The pipeline found **3/7 and 2/8** of the hand-read forward statements at the promise stage (zone 5/7 and 3/8; candidates 4/7 and 3/8). Hand precision of the promise stage was **28/48 (58%)** across all 15 reports.
4. **The credibility score is thin.** Auto-scored n = 5 (SUNFLAG), 0 (GULFPETRO), 0 (REPRO). With the hand statuses added (seed): 5, 1 and 2. Annual reports of companies without calls almost never put a date or a number on a plan. **AR-mode MCS is not comparable with concall MCS.**
5. **SUNFLAG's pipeline MCS (+0.91, n=5) looks better than the hand read ("0 of 5 mines reached production; timelines slip by years").** The reason: management never dated the mine milestones (except Bajna), so slow progress produces no "missed" promise. What scores is the vague "looking to acquire mines" (stated 3 times and delivered via new LOIs). Read SUNFLAG's slow execution in the **asset tracker**, not in the MCS.
6. **For small caps, the most useful AR-mode outputs are the disclosure-quality flags:** stale forward dates at filing (REPRO x3), "commissioned during the year" repeated in 2 consecutive reports (SUNFLAG Blooming mill, FY24 and FY25 ARs), an unchanged reserve figure (SUNFLAG Belgaon), and identical outlook sentences copied year to year (GULFPETRO PCMO). Each of these is a cheap governance signal.

## 1. Method
- **Reports:** the latest 5 ARs per symbol from `nse_fetch.annual_reports`. One row per FY; a later "Revised" upload wins. Each AR is dated at its NSE submission date. ZIPs (FY22-FY23) are read in memory and only `*.pdf` members are used. The PDFs are deleted after `pdftotext -layout`.
- **Zone:** the Chairman's/MD's message, the Board's (Directors') Report, the MD&A, and the energy-conservation/technology-absorption annexure. Report-level headings count only in the first 8 lines of a page. Two-column pages are split. Tables are rebuilt row by row.
- **Promises:** `candidates.py` (unchanged), then the rule builder in `ar_run.py`. A statement is kept only if (a) the company is the subject, (b) it is not macro or industry text, (c) it has a project or target word, and (d) it has a future marker. Chain key = `asset:milestone`.
- **Evidence:** later ARs' sentences on the same asset, classified done / pending / dropped and dated.
- **As-of date:** 2026-11-23. Cache: scratchpad `ar_mode/` (the text only; it is not kept in git).
- **Hand reads:** for GULFPETRO and REPRO, every sentence with a broad forward marker in the AR text before the auditors' report (`scripts_ar_mode/handread_dump.py`; independent of the zone and promise rules), read and judged by hand. This yielded 90 and 148 sentences. The SUNFLAG baseline is the ledger built by hand on the same day (`SUNFLAG_live.md` section 5.4).

## 2. Selection of the two random companies (seeded, done before any AR was read)
- **Universe:** `live_dd1/mcap_rows.json`, the 1,547 symbols of `research_notes/Backtests/india_pead_live/universe.csv` x the NSE close on 20-Nov-2026 (the SUNFLAG selection data).
- **Rule:** small cap = ₹300-5,000 cr; drop "Financial Services" and the 69 hand-classified financials; drop SUNFLAG. **722 eligible**, sorted alphabetically, `random.Random(202611232).shuffle`. Walk the list.
- **Accept if:** 0 transcript filings **and** 0 announcements mentioning an earnings/conference call or an analyst/investor meet since 01-Jan-2023 (NSE announcement list), **and** NSE ARs exist for at least FY24-FY26 (`scripts_ar_mode/select.py`).
- **Walk:** WONDERLA (₹3,173 cr) skipped (16 transcripts, 3 call intimations). **GULFPETRO** (GP Petroleums, ₹309 cr) accepted: 0/284 announcements. **REPRO** (Repro India, ₹431 cr) accepted: 0/205.

## 3. Recall against the hand reads (one AR each)
| Company, report (filed) | Hand items | In zone | Candidates | Promises | Pipeline promises in that AR (all matched hand items) |
|---|---|---|---|---|---|
| GULFPETRO AR FY25 (22-Aug-2025) | 7 | 5 | 4 | **3** | 3 |
| REPRO AR FY25 (22-Jul-2025) | 8 | 3 | 3 | **2** | 2 |

GULFPETRO hand items (status on AR FY26 evidence, by hand):
| # | Item | Zone / cand. / promise | Status 2026-11-23 |
|---|---|---|---|
| G1 | PCMO: launch new products, expand the segment | Y / N / N | pending; **identical sentence repeated in AR FY26** |
| G2 | Repsol alliance into Bangladesh/Nepal via exclusive distributors | N / N / N | pending; not mentioned in AR FY26 (silently dropped?) |
| G3 | Bitumen: expand; supply to HPCL; explore public/private opportunities | Y / Y / Y | pending (vague); AR FY26 reports bitumen growth |
| G4 | Lubricant opportunities beyond India | N / N / N | pending; not mentioned in AR FY26 |
| G5 | Automotive: channel partners in new territories, "LAKSHYA", market coverage | Y / Y / Y | pending (vague) |
| G6 | SPA 07-Jun-2025 to acquire 50% of Amron Oil Resources (JV) | Y / Y / N | **delivered** (AR FY26: stake acquired June 2025; the JV operated in FY26) |
| G7 | "GP Petroleums is going to be one of the key beneficiaries" (tyre oils) | Y / Y / Y | pending (vague) |

REPRO hand items:
| # | Item | Zone / cand. / promise | Status 2026-11-23 |
|---|---|---|---|
| R1 | Content monetisation to play an increasingly significant role in turnover | N / N / N | pending (vague) |
| R2 | Content monetisation remains the key growth driver | N / N / N | pending; restated in AR FY26 |
| R3 | New Bindwel binding capacity "planned to be installed in April 2025" | Y / Y / Y | **partly**: still "planned" in the July-2025 report (stale at filing); commissioned during FY26 per AR FY26 |
| R4 | Marketing priorities: global accessibility, GMV, reader engagement | Y / Y / Y | pending (vague) |
| R5 | Expand sales and marketing teams across segments | Y / Y / N | pending (vague) |
| R6 | BRSR target: top-5 online book-seller ranking | N / N / N | pending; not reported in AR FY26 |
| R7 | BRSR: Phase-1 of the data-analytics platform | N / N / N | **delivered** (AR FY26 BRSR: first phase operationalised) |
| R8 | BRSR: plant-assessment corrective actions to complete next year | N / N / N | pending |

**Why items are missed:**
- **Outside the zone (7 of 15):** REPRO's front "company overview" pages (R1, R2) and the BRSR "specific commitments" row (R6-R8). GULFPETRO G2 is on a company-profile page before the Chairman's message; G4 is in the Executive Director's message, but a CSR page inside that message closes the zone.
- **Present tense (G1):** "is actively expanding ... by aggressively launching" has no future marker for candidates.py.
- **Builder rules (G6, R5):** the Amron sentence was split by pdftotext; R5 has no project word. (After the context-subject fix, R5 still fails the project-word test.)

Widening the zone to the overview pages and the BRSR commitments row would lift recall. The cost is more promotional fluff.

## 4. Precision (hand check of every promise the pipeline kept, 15 reports)
| | Kept | Company forward statements (hand) | Checkable (date or object) | Non-promises kept |
|---|---|---|---|---|
| SUNFLAG | 9 | 7 | 3 (Blooming mill Q2FY23, Bajna EC Sep-2026, ReNew JV) | 2 industry-demand forecasts |
| GULFPETRO | 17 | 8 | 0 | 9: garbled two-column text, past events, macro, dividend mechanics |
| REPRO | 22 | 13 | 5 (solar "soon", ISO recert, Bindwel, certification renewal, Rewari FAMA) | 9: past descriptions, process text |
| **Total** | **48** | **28 (58%)** | **8** | 20 |

## 5. Credibility output (`ar_run.py`, as of 2026-11-23)
| | Promises kept | Auto-scored | MCS | Weighted delivery | Statuses (auto) | Hand-adjusted seed (confirmed records + hand items) |
|---|---|---|---|---|---|---|
| SUNFLAG | 9 | 5 | **+0.91** (grade A) | 90.7% | delivered 4, partly 1 (Blooming mill), pending 4 | n 7, scored 5, MCS +0.91 |
| GULFPETRO | 17 | 0 | n/a | n/a | pending 17 (4 "silently dropped?") | n 12, scored 1 (Amron delivered), MCS +1.0 |
| REPRO | 22 | 0 | n/a | n/a | pending 22 (13 "silently dropped?") | n 19, scored 2 (Bindwel partly, analytics Phase-1 delivered), MCS +0.75 |

How to read it:
- The SUNFLAG score rests on 3 restatements of "looking forward to acquire coal and iron ore mines" (delivered: Surajpura LOI 13-Feb-2026; Tambia South 07-May-2026), the Blooming mill (partly), and the ReNew solar JV (delivered).
  - The ReNew status is right, but the evidence sentence is wrong. The pipeline matched the Sunsure SPV text; the true evidence is AR FY26 BRSR P6, which shows renewable power from the ReNew JV at 3x FY25.
- The pipeline does **not** penalise SUNFLAG's undated mine slippage: Lohardongri (LOI 2019, now a PIL) and Bhivkund (vesting 2021, ML 2026). The hand ledger's verdict ("0 of 5 mines in production") lives in the asset tracker.
- REPRO's "silently dropped?" suggestions (13) are mostly vague aspirations that next year's report simply rewords. Do not treat them as misses.
- Statement counts are too small for any company-level conclusion. n ≤ 5 everywhere.

## 6. SUNFLAG asset tracker vs the hand ledger (section 5.4)
| Asset | FY24 AR | FY25 AR | FY26 AR | Tracker |
|---|---|---|---|---|
| Lohardongri | FC pending; SBWL | LOI-validity extension pending | PIL (tiger corridor) | 3/3 |
| Bhivkund | EC hearing 24-Apr-2024 | ML pending at Mantralaya | EC, CTO; ML executed 21-Apr-2026 | 3/3 |
| Bajna | ToR minutes 02-May-2024 | FRA; Stage-I FC pending at DFO | "EC and Stage I ... likely by end Sep-2026" | 3/3 + dated promise |
| Surjagad-6 | prospecting scheme | same text | CL 05-May-2025; drilling 29-May-2026 | 3/3 |
| Belgaon | 5.391 MT | 5.391 MT | 3.5 MT | 3/3 + **unchanged-quantity flag FY24 -> FY25** |
| Tambia South, Surajpura (new) | — | — | successful bidder / LOI | 2/2 |

Other tracker flags:
- "same 'done during the year' sentence repeated", FY24 -> FY25 ("The Company during the year commissioned its Blooming mill"; the AR FY23 first reported the commissioning).
- Kodalibad not in later status tables.
- Bhivkund 0.72 MTPA unchanged (benign: rated capacity).
- Noise: merged table cells assign one row to two assets (AR FY24 Belgaon/Navegaon). GULFPETRO's tracker picks up non-asset tables ("awareness", "brand").

## 7. Regression: concall mode unchanged
`python3 -I regress_concall.py --ref 5c15082 --cache <scratchpad>/pt_cache` takes the pre-AR-mode pipeline from git. It runs turns -> candidates -> score (seeded promises, `--no-screener` + fin.csv) -> report with the old and new code.
- COFORGE, ENDURANCE, HAPPYFORGE, KPITTECH, MPHASIS, PERSISTENT, SANSERA, SONACOMS: **IDENTICAL**. This covers every turns file, candidates.jsonl, scored.jsonl, seed, summary and markdown.
- `infer_measure` / `parse_target` on all seeded promises (508 before this seed, 546 with it): **0 changed**.
- AR mode edits no existing module.

## 8. Lessons and next steps
1. **Annual reports are a disclosure-quality instrument more than a promise ledger.** Their forward text is mostly undated. The signals that work are stale dates at filing, sentences copied year to year, unchanged quantities, and assets that disappear from tables. Proposal: feed these flags into the stage-2/4 governance soft flags (they are objective and cheap).
2. **Do not compare AR-mode MCS with concall MCS.** The universe of statements differs: no Q&A, no numbers, no prompting.
3. **Next:**
   - Widen the zone to the overview pages and the BRSR "specific commitments" row, then re-measure recall.
   - Add present-tense plan patterns ("is expanding ... by launching").
   - Run the LLM step (`--emit-prompts`, then `llm_extract.py` on the AR cache root) and compare with the rule builder.
   - Re-check Bajna EC when Sunflag files again (live call 4).

## Files
- Code: `tools/promise_tracker/pipeline/ar_fetch.py`, `ar_sections.py`, `ar_run.py`, `regress_concall.py`; README v1.4.
- Scripts: `research_notes/Promise tracker pilot/scripts_ar_mode/` (`select.py` draw, `handread_dump.py` hand-read sentence dump, `recall.py`, `build_seed.py`).
- Seed: `memdb/seeds/2026-11-23_promises_ar_mode.json`, 42 records:
  - 38 promises: 28 pipeline records confirmed by hand and 10 hand-read items the pipeline missed. Hand statuses are in `human_status`.
  - 3 analysis records and 1 insight.
- Sources (NSE annual reports, latest 5 each):
  - SUNFLAG FY22-FY26: `nsearchives.nseindia.in/annual_reports/AR_*_SUNFLAG_*` (URLs in the seed records).
  - GULFPETRO FY22-FY26, filed 19-Aug-2022 ... 03-Aug-2026.
  - REPRO FY22-FY26, filed 08-Jul-2022 ... 26-Oct-2026.
