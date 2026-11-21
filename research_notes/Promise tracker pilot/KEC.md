# Promise tracker (peer calibration): KEC International (NSE: KEC)

*As of 21-Nov-2026. Research, not SEBI-registered advice. No buy/sell view is implied: this is a method-calibration exercise for the Skipper score.*
Seed file: `memdb/seeds/2026-11-21_promises_TD_peers.json` (75 KEC `promise` records + `analysis:KEC:credibility-2026-11`).
Ledger and scripts: `research_notes/Promise tracker pilot/scripts_TD_peers/` (`promises_KEC.py` holds every quote, status and evidence; `build_seed.py` computes the score with the Skipper formula; `make_seed.py` writes the seed).

## 1. What was done
- **Calls read:** 8 concall transcripts, Q3FY25 (04-Feb-2025) to Q2FY27 (03-Nov-2026). NSE's filings for KEC are cover letters that point to kecrpg.com, so the PDFs came from the company site (URLs in Sources). Converted with `pdftotext -layout`.
- **Reading depth (differs from Skipper):** opening remarks read in full; Q&A read as every management answer containing at least three guidance keywords (targets, %, crore, FY, margin, debt, NWC, etc.), with the analyst question. About 7,000 words per call. Skipper was read in full. Vague, unnumbered promises may be under-counted here; numeric guidance is unlikely to be missed.
- **Promises extracted:** 75 (58 scored, 15 pending, 2 unverifiable). Same fields as Skipper (quote, metric, target, deadline, specificity, materiality, volunteered/prompted).
- **Checking delivery:** later calls (company-reported) plus screener.in consolidated and standalone (P&L, quarters, balance sheet, cash flow, ratios), fetched 21-Nov-2026.
- **Speakers:** almost all from **Vimal Kejriwal** (MD & CEO); CFO **Rajeev Aggarwal** gave the debt, NWC, interest and Afghanistan numbers.

**Scoring.** Identical thresholds and weights to SKIPPER.md section 1 (delivered >=95%, partly 80-95% or <=1 quarter late, missed, moved-goalpost -1.5, withdrawn -0.5, silently-dropped -1.5; weights = specificity x materiality x 8-quarter half-life). Two clarifications were needed and are applied to both peers (see TD_peer_comparison.md section 5):
- **A.** A target cut in the final quarter before its deadline is scored on outcome, not as "withdrawn" (otherwise KEC's Jan-26 margin cut would earn -0.5 instead of -1 for four separate misses).
- **B.** Ceiling targets (interest %, debt, NWC days): delivered if at or below target, partly if the overshoot is <=5%, else missed. Margin-expansion targets are scored on the expansion promised, not on the margin level (7.1% vs 8% is "89% of target" by level but +10 bp of +100 bp by expansion).

## 2. Score

| Metric | KEC | (Skipper) |
|---|---|---|
| Promises extracted / scored | 75 / 58 | 68 / 48 |
| Status counts | delivered 13 · partly 7 · missed 26 · moved-goalpost 9 · withdrawn 3 | 16 · 11 · 10 · 9 · 1 (+1 dropped) |
| **Weighted delivery ratio** | **19.8%** | 41.3% |
| Specificity-only / raw hit rate | 26.9% / 22.4% | 41.2% / 33.3% |
| MCS (-1.5 to +1) | **-0.60** | -0.18 |
| Candour index (shortfalls admitted unprompted) | 31% (14 of 45) | 12.5% |
| Core promises (materiality 3: group revenue, margin) | 8.8% | 52% |
| Promises made in FY25 calls vs FY26 calls | 53% vs 20% | 56% vs 25% |
| Precise / range / vague | 21% / 42% / 25% | 33% / 53% / 64% |
| Volunteered / prompted | 48% (n=9) / 22% (n=49) | 39% / 42% |
| **Grade** | **D+** | C- |

### Where management delivered
- **FY25 (promises made Feb-25):** order inflow INR 24,689 cr vs ">25,000" (99%); net debt incl. acceptances INR 4,558 cr inside the 4,500-5,000 range; aluminium conductor plant on time; FY25 revenue +9.7% vs the cut 12-14% (partly).
- **Under-promised segments:** SAE Towers +36% vs +5-6% guided; cables +23% vs +11-12% and INR 2,217 cr vs 2,300-2,400 (96%); T&D share of revenue 68% vs ">60%".
- **The final FY26 margin range** (7-7.5%, given in Jan-26) was met at ~7.1%; first wind EPC order won; 1,000 MW of solar commissioned in Q4FY26; FY26 capex ~INR 400 cr as guided (derived from screener).

### Where management missed
- **FY26 group revenue:** "+15%" was stated in Feb-25, May-25, Jul-25 (CFO) and Nov-25. Actual +7.6% (INR 23,506 cr vs 21,847). H2FY26 grew only 1.4% YoY.
- **FY26 margin:** "+150 bp at least" (Feb-25), "8-8.5%" (May-25, reaffirmed Jul-25 with "no major issue meeting the lower end"), "closer to 8%" (Nov-25), then 7-7.5% (Jan-26, only when asked). Actual ~7.1%: +10 bp of the promised +100-150 bp. Screener OPM moved 7.7% -> 7.95% on its own definition.
- **FY27-28 margin re-dated three times without acknowledgement:** "FY27 9%, no doubt about it" (May-25) and "closer to 10%" (Jul-25) -> "9-10% ... FY28" (Jan-26) -> no guidance, double digit "maybe FY29" (May-26) -> "FY28 ... whether 7% or 8% or 9% is difficult to say" (Nov-26). H1FY27 EBITDA ~5.4%.
- **Debt and working capital - every FY26-27 target missed:**

| Said | Target | Outcome |
|---|---|---|
| May-25 (CFO) | NWC ~100 days by Mar-26 | moved to 110 in Jul-25 with no reference to 100; actual ~137 |
| Jul-25 (CFO) | net debt ~INR 4,500 cr by Mar-26 | INR 6,722 cr |
| May-25 / Jul-25 / Nov-25 | interest ~2.5% of revenue | 2.8% (presented as "-20 bp") |
| Nov-25 | Sep-25 debt (6,480) "is our peak" | Dec-25 6,806; Sep-26 7,793 (record) |
| Jan-26 | debt "normalise by Mar-26" | 6,722, "marginally lower than December" |
| May-26 | net debt -INR 500 cr by Sep-26 | +INR 1,071 cr |
| May-26 | receivables "normalised" in two quarters | NWC ~125 days, Saudi closures slipped |
| Aug-26 (CFO) | net debt ~5,500 by Mar-27 | restated "almost 6,000" in Nov-26 with no reference to 5,500 |

  Screener cross-check: borrowings 3,957 (Mar-25) -> 5,378 (Mar-26) -> 6,305 (Sep-26); FY26 CFO -INR 414 cr, FCF -691 cr; debtor days 84 -> 101; working-capital days 42 -> 57.
- **Segments:** Civil "+15%" (Feb-25), then "at least +25%" (May-25), then "~INR 5,000 cr" (Nov-25) -> actual INR 3,823 cr (-15%). Railways "won't go below ~2,100" -> 1,555. Water INR 1,200-1,500 cr -> ~800. Non-T&D "significant uptick in Q3-Q4" -> non-T&D revenue down ~16% (derived from T&D share).
- **Dates:** E-Beam/elastomeric cables have had five dates (Q4FY26 -> Q1FY27 -> Q2FY27 -> Q2/Q3 -> Q3FY27), none acknowledged as a slip. Karnataka 500 MW: Q2 -> Q3 -> Q4FY26. Afghanistan ADB receivable: "Q3FY26" -> "Q4" -> "Q1" -> received October 2026 (three quarters late). Legacy railway projects "physically complete in 1-2 quarters" (Feb-25) were still closing in Nov-26.
- **FY27 revenue:** 12-15% (May-26, reaffirmed Aug-26 with "maybe 0.5% or 1% here and there") cut to 8-10% in Nov-26 after H1 -5.6%. Scored "withdrawn" (explicit, explained, two quarters before the deadline).
- **Governance item (single-source):** in Jul-25 an analyst asked about "this bribery case with Power Grid officials, which is under inquiry". The CEO said a PGCIL action would not hurt "our T&D growth in any manner". T&D revenue did grow (+24% in FY26), but KEC then received no PGCIL orders for ~15 months ("after a break of 15 months", Nov-26) and India T&D order intake fell to ~INR 6,400 cr (derived) from ~7,200. Scored "partly". Worth a separate check (court/CBI records) before any use.

## 3. Candour and tone
- **Misses get explained, and often unprompted.** The Q4FY26 and Q1/Q2FY27 opening remarks open with what went wrong: Middle East war (~INR 380-400 cr of Q4 revenue deferred), LPG and election-driven labour shortages, JJM water payments, metro hand-over delays, INR 450-600 cr of collections slipping past quarter-end. That is why the candour index (31%) is well above Skipper's 12.5%.
- **But targets are re-set silently.** Nine moved goalposts: NWC 100 -> 110 -> 110 again for the next year; civil 25% -> 10-15%; FY27 margin -> FY28 -> FY29; cables FY27 3,400-3,500 -> 2,500-2,600; net debt 5,500 -> 6,000. The explanation of the miss is volunteered; the fact that a specific number was promised is not.
- **Guidance mostly comes from Q&A.** 64 of 75 promises were extracted by analyst questions; the opening remarks rarely state FY guidance. Prompted numbers delivered 22%, volunteered ones 48%.
- **Credibility fell as conditions worsened:** promises made in FY25 calls delivered 53%, in FY26 calls 20%. Same shape as Skipper (56% -> 25%), at a lower level.
- **A recurring "one more quarter" pattern on cash:** every quarter from Q2FY26 to Q2FY27 attributes high debt to collections that "came in the first week" of the next month (Saudi in Jan-26, INR 450 cr in Apr-26, INR 600 cr in Oct-26). Each was true, but the quarter-end debt kept rising.

**How to use this.** Treat KEC's group margin, debt and NWC guidance as a direction, not a number: on this record, haircut margin-expansion promises by ~90% and expect quarter-end debt above guidance. Segment growth and plant dates need a 2-3 quarter haircut. Under-promising has been consistent only in SAE and cables.

## 4. Pending (15) - what to check next
- **Q3FY27 (Jan/Feb-2027):** E-Beam/elastomeric production (fifth date, Q3FY27); Afghanistan balance (~INR 100-150 cr); H2 revenue run-rate vs 8-10% FY27 (needs H2 +20-24% YoY); net debt path to ~INR 6,000 cr.
- **Q4FY27:** FY27 order intake ~INR 30,000 cr (H1 ~13,500); interest ~2.3% (H1 ~3.4%); FY27 EBITDA "better than 7-7.5%" (H1 ~5.4%, likely miss); civil +30-35% (H1 +2%); cables +15% (on track); railway claims INR 150-200 cr; cables margin 8% (now 5.5-6%).
- **Further out:** renewables INR 3,000-4,000 cr by FY28; legacy closures by Q2FY28; water exit within 12-15 months of Jan-26.

## 5. Method notes specific to KEC
1. **Two margin definitions.** Company EBITDA (7.0% FY25, ~7.1% FY26) differs from screener OPM (7.7%, 7.95%). Interest % also differs (company 2.8% vs screener 3.7% for FY26). Scored on company definitions, as the promises were made on them, and the screener figure is shown alongside.
2. **Net debt "including acceptances" is not on screener.** Screener borrowings move the same way (+36% in FY26, +17% in H1FY27) but are lower. Debt records stay single-source on the level, verified on the direction.
3. **Segment data is company-reported** (civil, railways, SAE, cables, water) and some is derived (India T&D intake = T&D intake less international; non-T&D revenue from the T&D share). Flagged in `evidence`.
4. **Q3FY26 transcript is not under the usual file name** on kecrpg.com (`KEC Earnings Call 30th Jan 2026.pdf`; found via screener's concall links).

## Sources
- Transcripts (kecrpg.com, `public/media/earningsCallRecordingFilesMedia/`): KEC Q3 FY25, Q4 FY25, Q1 FY26, Q2 FY26 Earnings Call Transcript.pdf; KEC Earnings Call 30th Jan 2026.pdf; KEC Q4 FY26, Q1 FY27, Q2 FY27 Earnings Call Transcript.pdf. NSE cover letters: `nsearchives.nseindia.in/corporate/KEC_*_SE_Intimation*.pdf`.
- screener.in, fetched 21-Nov-2026: https://www.screener.in/company/KEC/consolidated/ and https://www.screener.in/company/KEC/ (standalone).
