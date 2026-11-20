# Promise tracker pilot: Skipper Ltd (NSE: SKIPPER)

*As of 19-Nov-2026. Research, not SEBI-registered advice.*
Seed file: `memdb/seeds/2026-11-19_promises_SKIPPER.json` (68 `promise` records + `analysis:SKIPPER:credibility-2026-11`).
Rebuild script and ledger: `research_notes/Promise tracker pilot/scripts_SKIPPER/` (`promises_data.py` holds every quote and its status; `build_seed.py` computes the score).

## 1. What was done
- **Calls read:** 10 concall transcripts, every quarter from Q1FY25 (30-Jul-2024) to Q2FY27 (30-Oct-2026). All came from NSE via `tools/nse_fetch.py transcripts SKIPPER --download` and were converted with `pdftotext`. Every call was read in full, not keyword-searched.
- **Promises extracted:** 68 forward-looking promises. For each one the ledger records the call date, speaker, exact quote, metric, target, deadline, specificity (precise / range / vague), materiality (1-3), and whether it was volunteered or prompted by an analyst.
- **Checking delivery:** each promise was checked against later calls (company-reported numbers) and screener.in consolidated data (P&L, quarterly results, balance sheet, ratios, and the "Other Assets" schedule for receivables), fetched 19-Nov-2026.
- **Speakers:** nearly every promise came from **Sharan Bansal** (Director/ED). The CFO (Shiv Shankar Gupta) gave one (the two-year >25% closing statement, Jul-24) and IR (Aditya Dujari) gave one (polymer INR 1,000 cr, Jul-24).

**Scoring rule.** These are the thresholds I used, stated up front:

| Status | Rule | Score |
|---|---|---|
| delivered | ≥ 95% of target (low end of a range), on time | +1 |
| partly | 80-95% of target, or at most 1 quarter late | +0.5 |
| missed | < 80% of target, or more than 1 quarter late | −1 |
| moved-goalpost | target or date changed at a later call without acknowledging the change | −1.5 |
| withdrawn | explicitly lowered, with an explanation | −0.5 |
| silently-dropped | not repeated for 4 or more calls | −1.5 |
| pending | deadline not yet reached | not scored |
| unverifiable | deadline passed, but no public number to check | not scored |

- **Weights** = specificity (precise 3 / range 2 / vague 1) × materiality (1-3) × recency decay (half-life 8 quarters).
- **Headline delivery ratio** = weighted share of credit, where delivered = 1, partly = 0.5 and everything else = 0.

## 2. Score

| Metric | Value |
|---|---|
| Promises extracted / scored | 68 / 48 (19 pending, 1 unverifiable) |
| Status counts | delivered 16 · partly 11 · missed 10 · moved-goalpost 9 · withdrawn 1 · silently-dropped 1 |
| **Weighted delivery ratio** | **41%** (specificity-only weighting: 41%; raw hit rate 33%) |
| MCS on the −1.5 to +1 schema scale | **−0.18** |
| Candour index (shortfalls admitted unprompted at the next call) | **12.5%** (4 of 32) |
| Core promises (materiality 3: group revenue, margin, capacity) | 52% |
| Promises made in FY25 calls vs FY26 calls | 56% vs 25% |
| Precise vs range vs vague | 33% vs 53% vs 64% |
| **Grade** | **C−**: good on group margin and finance-cost guidance, poor on dates and segment targets |

### Where management delivers
- **Group revenue in FY25:** guided +25%; delivered +41% (INR 3,282 → 4,624 cr). FY25 order inflow was INR 5,335 cr against INR 4,500-5,000 cr guided.
- **Margins:** the FY26 margin promises were met. "At least +50 bp" came in at 10.3% vs 9.8%. The 10-10.5% range came in at 10.3%. Engineering margin stayed in its 11-12% band.
- **Finance cost:** guided to ~4% of sales in FY26; delivered 3.9% (screener 218/5,553 = 3.93%).
- **The Apr-25 range for FY26 revenue:** guided +20-25%; delivered +20.1%, the bottom of the range. The Jan-26 cut to "21-22%" was also met (+20.1%; Q4 +29.4% vs the 25-30% said).
- **First 75k t block:** about one quarter late against the March-2025 date, then delivered (fully operational by Jul-2025).

### Where management misses
- **The second 75k t block has had five dates.** In order: Mar-26 (said Jul-25); "partly before March, rest Q1" (Jan-26); June-26 (Apr-26); "H2" and "end of Q2" (Aug-26); "end of Q3 or early Q4" (Oct-26). Each new date was given **without acknowledging the previous one**. The only explanation offered was "minor delays", in Jan-26, and only when asked.
- **600k t moved from FY28 to FY29.** The Oct-26 opening remarks gave FY29 with no mention that the target had been FY28-end since Jul-25.
- **FY26 revenue "25% plus", raised in Jul-25 and re-affirmed in Nov-25:** delivered +20%. The cut first appeared in the Jan-26 presentation. When an analyst asked, management said: "the 25% is -- was our aspirational growth."
- **FY26 order inflow:** guided INR 6,500-7,000 cr in Jul-25, quietly re-stated as "INR 6,000 cr plus" in Nov-25. Actual: INR 5,678 cr.
- **Export order inflow:** promised to "double to INR 1,500 crores this year for sure" in FY26. Actual: about INR 730 cr. That figure is implied by the Q1FY27 statement that ~INR 1,100 cr would be "+50% over last year".
- **Polymer (pipes):**
  - growth guided at 20-25% (Oct-24), then 25-30% (Apr-25); actual FY25 roughly flat, FY26 +11%;
  - the INR 1,000 cr target moved from "2-3 years" (Jul-24) to "if not next year, the year after" (Nov-25), then lost its date entirely (Apr-26);
  - the double-digit margin moved from "next year" (Jul-25) to "long term" four months later (Nov-25).
- **Infra segment FY26:** guided +20-25%; derived actual about +2% (≈ INR 687 cr vs 674 cr).
- **"No further capital raising beyond the rights issue; internal accruals will be strong enough" (Jul-24):**
  - three months later the Board took an enabling resolution for ~INR 600 cr;
  - in 2026 the company raised INR 433.5 cr by preferential issue;
  - free cash flow was negative in both FY25 (−83 cr) and FY26 (−88 cr).
- **FY25 finance cost below 4.5% of revenue:** actual 4.6-4.8%. The miss was never acknowledged. Later calls described the FY25 base as 4.7% (Nov-25) and then 4.8% (Jan-26), which makes the FY26 improvement look larger.
- **Silently dropped:** "25% CAGR over three years, INR 10,000 cr revenue by ~FY29" (Oct-24 interview claim, affirmed on the call). It was never repeated in the eight later calls; in Feb-25 management "would refrain from putting any specific guidance numbers". It is still arithmetically reachable, since FY24 to FY27e is about a 25% CAGR if FY27 delivers +15%.

## 3. The debtor-day rise (55 → 98): what management said vs the numbers

| Date | What management said | What the numbers show (screener) |
|---|---|---|
| 30-Apr-2025 (volunteered, opening remarks) | "Working capital days also improved with inventory and debtor days sharply reducing." "Cash flow and working capital are expected to improve considerably going forward." | FY25 receivables INR 701 cr, debtor days 55 |
| 31-Jul-25, 07-Nov-25, 29-Jan-26 | No mention of debtors; credit given to "better working capital management" for the lower finance cost | (no half-year receivables data checked) |
| 28-Apr-2026 (only after an analyst asked; the opening remarks spoke of "stronger cash generation") | "None of them are sticky debtors." INR 260 cr "due to a technical reason" arrived on 1-2 April. Q4 domestic revenue was up ~45%, and domestic customers pay more slowly. GST inflates the number. "Already realized close to about INR 600-700 crores ... in April." | FY26 receivables INR 1,485 cr (2.1x on +20% revenue), debtor days 98. WC days 28 → 43. Cash INR 121 → 32 cr. CFO did improve, INR 153 → 277 cr. |
| 12-Aug-26, 30-Oct-26 | Debtors not raised by management. Oct-26 reframed the target as "net working capital days ... in this 90 to 100 days stable region", calling it "best in the industry". (The company itself had quoted NWC days of 62 in Sep-24 and 88 in Dec-24.) | Sep-26 receivables INR 1,223 cr: ~78 days on TTM revenue, ~83 days on annualised H1 |

**How much of the explanation holds up (my own numbers):**
- **The INR 260 cr late receipt:** even after removing it, Mar-26 debtor days are about **80**, not 55.
- **Q4-heavy billing:** this explains part of the rise. On Q4-annualised revenue, debtor days were ~50 (FY25) and ~81 (FY26), or ~67 after removing the INR 260 cr.
- **GST:** this applied in FY25 as well, so it does not explain a year-on-year change.
- **Six months later:** receivables are down only INR 262 cr, and debtor days are still ~25 above the FY25 level.

**Verdict.** The explanation is plausible but incomplete. It came only when asked. The April-2025 promise that working capital would improve was not met: cash flow improved, the receivables cycle did not, and the target was quietly reset.

Other points:
- This does **not** trip the existing kill criterion of debtor days above 120 (`analysis:SKIPPER:2026-11-19`).
- It is the item to watch at Q4FY27.
- Separately, "other asset items" (likely contract assets) rose from INR 232 cr to 400 cr to 455 cr (Mar-25, Mar-26, Sep-26), which is worth splitting out next time.

## 4. Candour note and tone vs delivery
- **Explanations come when asked.** Misses are usually explained (Rajasthan monsoon, ROW and transformer/HVDC shortages, CEA holding back bids, the Middle East war, freight, resin prices). But in 28 of 32 shortfalls the explanation came only after an analyst raised it.
- **The exceptions:**
  - the Q1FY27 opening admitted "a lower-than-expected order inflow" for FY26;
  - the polymer headwinds (JJM, resin) were volunteered;
  - the equity raise was explained in the opening remarks;
  - the Oct-26 call warned that margin expansion "will not be as high as what we had targeted". This was pre-emptive and is the most candid moment in the ten calls.
- **Missed numbers get relabelled.** A missed number becomes an "aspiration" afterwards ("25% ... was our aspirational growth"). A lowered number is called "maintaining" ("we maintain ... INR 7,500 crores", when the previous call said 7,000+; exports went from ~1,100 to 1,500).
- **Tone is uniformly high-confidence.** Phrases like "absolutely", "for sure", "well on track", "no challenge" and "no reason for concern" appear whatever the outcome. The closing paragraph has been word-for-word identical boilerplate since Q3FY26 ("growth, profitability and return ratios are set to compound together"). With a weighted delivery ratio of ~41%, this is the **high-tone / middling-delivery mismatch** that the India evidence says retail investors over-reward.
- **Precise, volunteered promises do worst.** By specificity, precise promises delivered 33%, ranges 53% and vague 64%. Volunteered promises delivered 39%, about the same as prompted ones at 42%.
- **Credibility is getting worse.** Promises made in FY25 calls (strong demand, spare capacity) delivered 56%. Promises made in FY26 calls delivered 25%. As growth slowed, the guidance did not adjust fast enough.

**How to use this.**
- Haircut management's dates by 1-2 quarters.
- Haircut segment and new-business targets (polymer, infra, exports, substation) by about half.
- Take group-level margin and finance-cost guidance closer to face value.
- Don't read the tone as information.

## 5. Open items to check next (pending, 19)
- **Q3FY27 call (Jan/Feb-2027):**
  - 450k t commissioned (fifth date);
  - H2 revenue running at the +21-22% needed for +15% FY27;
  - order inflow toward INR 7,500 cr, including INR 1,500 cr exports;
  - greenfield land identified.
- **Q4FY27 results:**
  - FY27 revenue +15% ("at worst 13-14%") and PAT +30%;
  - finance cost 3.2-3.5%;
  - polymer ~INR 608 cr;
  - receivables vs the 55-day FY25 base;
  - closing order book above INR 10,000 cr;
  - substation projects commissioned; margin 10-11%.
- **Further out:** the ~11% margin "in 2-3 years" from Oct-24 falls due at FY27, and is likely to be missed given H1 at ~10.6%. The 20-25% growth "from FY28", 600k t by FY29 and the 12% margin aspiration come after that.

## 6. Lessons learned on the method
1. **Download with care.** `nse_fetch.py transcripts --download` ignored `--from/--to` and pulled every attachment back to 2015 (27 files, including old .zip files). Either filter rows before downloading or add a date filter to the download loop.
2. **Read whole transcripts, not keyword hits.** Several of the most telling items would not appear in a keyword search:
   - the utilisation target quietly cut from 90% to 85%;
   - "the 25% is -- was our aspirational growth";
   - "we maintain ... 7,500" when the earlier figure was lower;
   - the FY28 → FY29 shift, buried in an opening paragraph.

   Plan about 10-12k tokens per call. Ten calls is the right depth for a first company.
3. **Re-statements need their own records.** One target (for example the second 75k t block) produces a new promise each time it is re-dated. Link these records as a chain (`supersedes`) so the number of slips is countable. In this pilot they are separate records and the slips are listed in `evidence`. Next time add `data.supersedes`.
4. **Define statuses numerically before scoring.** The schema's "partly = 70%" is too generous: it would score an inflow miss of 87% as half-credit. I used delivered ≥ 95%, partly 80-95%. Keep this fixed across companies, or the scores cannot be compared.
5. **"Silently dropped" needs a minimum silence window.** I used 4 or more calls, plus a re-open rule if the target is later hit. The INR 10,000 cr / FY29 target is still reachable, so the record is marked dropped but should be revisited.
6. **Baselines move.** Management re-quoted the same FY25 finance-cost base as 4.4%, then 4.7%, then 4.8%. Always score against an external source (screener or the filed results), not the company's later description of the past.
7. **Company definitions differ from screener's.** NWC days 62 / 88 / "90-100" (company) vs WC days 28 / 43 (screener); inventory days 95 (company) vs 152 / 109 (screener). Track the company's own figure alongside an independent one, and never mix them in one ratio.
8. **Most numbers are company-reported (single-source).** The P&L-level numbers were checked against screener. Segment numbers (Infra FY26, polymer FY25, export inflow FY26) are derived or implied: they are flagged in `evidence`, and the records stay `single-source`. Next time, pull the quarterly results PDFs (`nse_fetch.py results`) for segment data.
9. **Count who asked.** About 85% of promises came from analyst questions, often a single sell-side analyst returning to the same point. The candour index (unprompted admission) is the most informative single number here, and it can only be built by reading what the opening remarks leave out.
10. **Cost of the method.** One company took about 10 transcripts and roughly 2-3 hours of agent work. This scales to a watchlist, not to the whole market. Use it on finalists, and re-run each quarter with only the new call plus the pending list. Change detectors (topic diffs, dropped KPIs) can be automated; promise scoring still needs a careful read.
11. **Next step for credibility as a signal.** One company has no base rate. Score three or four T&D peers (KEC, Kalpataru, Transrail) the same way before treating a 41% delivery ratio as good or bad.

## Sources
- NSE transcripts: `https://nsearchives.nseindia.in/corporate/`, files
  - SKIPPER_05082024143308_Transcriptletter.pdf
  - SKIPPER_02112024134823_Transcript.pdf
  - skipper_11022025121248_Trancript.pdf
  - skipper_07052025161052_Transcriptletter.pdf
  - skipper_06082025120131_Transcriptintimation.pdf
  - skipper_13112025165505_Transcript.pdf
  - skipper_04022026183852_Earningcall.pdf
  - skipper_05052026133011_Transcriptintimation.pdf
  - skipper_18082026120803_Transcript_of_Concall.pdf
  - skipper_05112026165128_ConcallTranscript.pdf
- screener.in consolidated, fetched 19-Nov-2026:
  - https://www.screener.in/company/SKIPPER/consolidated/
  - the balance-sheet "Other Assets" schedule (trade receivables Mar-25 701, Mar-26 1,485, Sep-26 1,223 cr)
