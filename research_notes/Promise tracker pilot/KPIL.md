# Promise tracker (peer calibration): Kalpataru Projects International (NSE: KPIL)

*As of 21-Nov-2026. Research, not SEBI-registered advice. No buy/sell view is implied: this is a method-calibration exercise for the Skipper score.*
Seed file: `memdb/seeds/2026-11-21_promises_TD_peers.json` (78 KPIL `promise` records + `analysis:KPIL:credibility-2026-11`).
Ledger and scripts: `research_notes/Promise tracker pilot/scripts_TD_peers/promises_KPIL.py` (+ `build_seed.py`, `make_seed.py`).

## 1. What was done
- **Calls read:** 7 concall transcripts, Q3FY25 (14-Feb-2025) to Q1FY27 (11-Aug-2026), from kalpataruprojects.com (NSE filings are cover letters pointing there; links found via screener's concall list). The Q2FY27 transcript (Nov-2026) was not yet on the site (the guessed URLs returned HTTP 500), so the **Q2FY27 investor presentation** (BSE, 05-Nov-2026) was used for H1FY27 actuals. It was used for checking, not for extracting promises.
- **Reading depth:** same as KEC: full opening remarks plus every management answer with >=3 guidance keywords (~6,000 words per call). Note that KPIL's moderator (the sell-side host) reads the welcome; the CEO's prepared remarks appear as the first "answer" in the extract, so they were read in full.
- **Promises extracted:** 78 (63 scored, 8 pending, 7 unverifiable).
- **Basis:** KPIL guides revenue and PBT on **standalone** and order inflow on **consolidated**. Both were checked. Screener standalone quarterly finance cost matches the company's % (e.g. Q3FY25 107/4,826 = 2.2%), so finance-cost promises are verified on two sources.
- **Speakers:** nearly all from **Manish Mohnot** (MD & CEO); **S.K. Tripathi** (Deputy MD) gave the JJM receivable figures.
- **Scoring:** identical to Skipper and KEC, with clarifications A and B (see KEC.md section 1).

## 2. Score

| Metric | KPIL | (Skipper) | (KEC) |
|---|---|---|---|
| Promises extracted / scored | 78 / 63 | 68 / 48 | 75 / 58 |
| Status counts | delivered 39 · partly 9 · missed 11 · moved-goalpost 1 · withdrawn 3 | 16 · 11 · 10 · 9 · 1 (+1 dropped) | 13 · 7 · 26 · 9 · 3 |
| **Weighted delivery ratio** | **76.7%** | 41.3% | 19.8% |
| Specificity-only / raw hit rate | 69.2% / 61.9% | 41.2% / 33.3% | 26.9% / 22.4% |
| MCS (-1.5 to +1) | **+0.63** | -0.18 | -0.60 |
| Candour index | 8% (2 of 24) | 12.5% | 31% |
| Core promises (materiality 3) | 83% | 52% | 9% |
| FY25 calls vs FY26 calls | 73% vs 67% | 56% vs 25% | 53% vs 20% |
| Precise / range / vague | 72% / 65% / 75% | 33% / 53% / 64% | 21% / 42% / 25% |
| Volunteered / prompted | 91% (n=19) / 58% (n=44) | 39% / 42% | 48% / 22% |
| **Grade** | **B+** | C- | D+ |

### Where management delivered
- **Group revenue, both years.** FY25: cut in Feb-25 to 12-13% standalone / 13-15% consolidated; delivered +12.7% / +13.7%. FY26: guided "20%+" in the May-25 opening remarks; delivered +22.9% standalone (INR 23,210 cr) and +21.6% consolidated (INR 27,143 cr). Also ~98.7% of the "INR 25,000 cr + ~10%" revised Vision target.
- **Margins.** Q4FY25 standalone PBT "~5%" -> 5.9%. FY26 consolidated PBT 4.5-4.75% -> 4.9% before exceptional items (+120 bp; screener 5.05%). "+50 bp minimum" -> +120 bp consolidated.
- **Working capital, debt and finance cost - every target met.** Standalone NWC <100 days: 94 (Mar-25), 90 (Mar-26), 81 (Sep-26). Finance cost "mid-2%" then "<2%": 1.4% (Q4FY25), 1.6% (FY26; screener quarterly sum 368 / 23,211). Net debt ~1x EBITDA "very soon": 1.06x at Mar-25, consolidated net debt INR 915 cr at Mar-26 and INR 72 cr at Sep-26. "Mar-26 net debt much lower than Dec": 915 vs 2,240.
- **Order inflow.** FY26 INR 26,000-28,000 cr guided -> ">26,000" (bottom of range). FY27 >30,000 guided; INR 23,934 cr by 05-Nov-26.
- **Segments:** T&D +25% (vs 20%+), B&F +19% (18-20%), Urban Infra +49% (40-50%), LMG Sweden +64% (30-40%) with EBITDA 6.7-6.8% (vs 5-6.25%).
- **Water collections** of INR 500-700 cr in Q4FY25 (~610 received), and "improve in Q4FY26" (delivered).

### Where management missed
- **Subsidiaries:** Fasttel (Brazil) was to hold 7-8% EBITDA (Feb-25) and break even in FY26 (May-25). Outcome: INR 186 cr EBITDA loss in 9M FY26, called "a setback for us" when asked (Feb-26), then a **INR 515 cr standalone provision** and exit from Brazil in Q4FY26.
- **Dates for asset sales and collections slip 1-2 quarters:**
  - VEPL road sale: "by Q2" (Feb-25), "Q2, Q3" (May-25), "Q3" (Aug-25), "H2" (Oct-25); closed Jan-26.
  - Indore real estate: INR 130 cr "in 60-90 days" (May-25) and INR 100 cr "Q2 or early Q3, not beyond that" (Aug-25); INR 75 cr still due at Dec-25; collected by Mar-26.
  - JJM water receivables: 60-70% of ~INR 1,500 cr to "start coming from June/Q2" (May-25). Instead receivables rose to INR 1,551 cr by Sep-25 and were ~1,600 cr in May-26. FY26 water collections were INR 1,800 cr against INR 2,500 cr invested.
- **Capex overspent every guide:** "below FY25" (Feb-25), INR 600-650 cr (May-25), 600-700 (Aug-25), 700-750 (Feb-26); actual "nearly INR 900 cr". Framed each time as growth investment funded from cash flow.
- **Oil & Gas** +55% vs "+100%+"; **international T&D inflow** ~INR 8,000 cr vs 9,500-10,000 (84%); **T&D inflow** ~INR 13,000 cr vs "better than FY25's 14,461" (90%); India T&D inflow fell from ~7,000 to ~4,500 cr.
- **The mid-year raise.** In Oct-25 FY26 revenue guidance was raised to "25%+", and in Feb-26 restated as "approx 25%". Delivered 22-23% (partly). In May-26 management listed its FY26 targets as "revenue growth of 20% to 25%" and said it had "fully delivered on each of these promises". The raise was not mentioned.
- **Railways:** an international railway win was expected in Q2-Q3 FY26; none was reported. International water: "a few significant wins in FY26"; the first (INR 344 cr, Middle East) came in Q1FY27.

## 3. Candour and tone
- **Low candour index, few misses.** Only 2 of 24 shortfalls were admitted unprompted (water receivables, Oct-25 opening; the Fasttel exit, May-26 opening). With so few misses, the index is noisy (Skipper 12.5% on 32, KEC 31% on 45). The pattern matters more than the number.
- **KPIL's habit is selective recall, not silence.** Three times a target was restated downward without comment, and each time the outcome then cleared the lower bar:
  - order inflow 26,000-28,000 -> "we stick to our guidance of 25,000 crores plus" (Oct-25);
  - standalone PBT 5.25-5.5% -> "5% to 5.5%" (Aug-25);
  - FY26 revenue "25%+" -> recalled as "20% to 25%" (May-26).

  None changes a status, because the outcomes met the original targets in the first two cases. But it is the same reflex as Skipper's "the 25% ... was our aspirational growth", applied with more room to spare.
- **Adjusted metrics carry the margin story.** Standalone FY26 PBT was 5.9% "excluding exceptional items and a one-off dividend income from VEPL", but 4.9% on reported numbers (screener 1,143 / 23,210) after the INR 515 cr Fasttel write-off. The guidance was met on the company's definition only; the record is single-source.
- **Basis shift on EPS.** "Minimum INR 50" (May-25), when the stated base (~INR 40) was standalone, became "consol EPS exceeding INR 50" in Feb-26. Standalone came in at INR 49 (98%: delivered by the threshold) and consolidated at INR 61.
- **Guidance is volunteered and conservative.** FY guidance sits in the opening remarks every May, with mid-year updates, and those promises delivered 91%, against 58% for Q&A answers. FY27 guidance (~15%+ revenue, +75 bp consolidated PBT, >30,000 cr inflow) was set below the FY26 run-rate.

**How to use this.** KPIL's group revenue, PBT, NWC and finance-cost guidance can be taken close to face value; the record supports it on two sources. Haircut dates on asset sales and collections by 1-2 quarters, treat capex guides as floors, and give subsidiary and new-geography targets (Fasttel, LMG IPO timing, international railways or water) about half credit. Read the standalone PBT on a reported basis as well as the adjusted one.

## 4. Pending (8) and items to watch
- **FY27:** revenue >=15% (H1 reported consolidated +6%, core ex-Brazil/roads +11%, standalone +12%: **at risk**); consolidated PBT +75 bp (H1 6.1% vs 4.9%: on track); inflow >30,000 cr (23,934 by Nov: on track); T&D inflow 13,000-15,000 cr (9,322 YTD); capex >=800 cr; water collections >=2,500 cr; most JJM projects complete.
- **Consolidated EBITDA 9%+ "sounds feasible"** for FY27 (H1 core 8.5%).
- **Unverifiable to recheck:** JJM receivables "majority recovered in Q1-Q2 FY27" (Aug-26: still ~INR 1,500 cr billed + unbilled); tower capacity +50k t (company figures conflict: 225k, 275k, 240k t); Shubham warehouse sales; FY25 water revenue base.

## 5. Method notes specific to KPIL
1. **Standalone vs consolidated.** Guidance is split by basis; Fasttel and road SPVs make consolidated noisier. In FY27 the company reports "core" revenue excluding Brazil and road SPVs (+11% in H1 vs +6% reported). Track both.
2. **Screener's annual standalone interest line (INR 526 cr for FY26) does not equal the sum of the quarters (368).** Use the quarterly sum or the company figure.
3. **Promoter pledge:** "will only come down" is single-source (company says it fell every quarter for six quarters); `nse_fetch.py pledge KPIL` returned no rows.
4. **The missing Q2FY27 transcript** means that call's new promises are not in the ledger. Add them at the next refresh.

## Sources
- Transcripts (kalpataruprojects.com/api/view-file/): KPIL_Q3_FY25_Transcript.pdf; KPIL_Q4_FY25_Transcript.pdf; KPIL_Q1FY26_transcript.pdf; KPIL_Q2_FY26_Transcript.pdf; KPIL_Q3_FY26_Earnings_Call_Transcript-5th_feb_2026.pdf; KPILQ4_FY26_Earnings_Call_Transcript_final.pdf; KPIL_Q1 FY27_Earnings Call Transcript.pdf.
- Q2FY27 investor presentation (BSE, 05-Nov-2026): https://www.bseindia.com/xml-data/corpfiling/AttachHis/aa471fd5-764a-4c79-9732-96785b3ad1cc.pdf
- screener.in, fetched 21-Nov-2026: https://www.screener.in/company/KPIL/consolidated/ and https://www.screener.in/company/KPIL/ (standalone).
