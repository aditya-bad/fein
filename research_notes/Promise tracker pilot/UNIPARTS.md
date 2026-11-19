# Promise tracker pilot: Uniparts India (NSE: UNIPARTS)

*As of 2026-11-19. This is research, not SEBI-registered advice.*
Seed file: `memdb/seeds/2026-11-19_promises_UNIPARTS.json`. It holds 68 `promise` records and 1 `analysis` record (`analysis:UNIPARTS:credibility-2026-11`). Nothing has been ingested yet.

## 1. What was done
- **Sources.** Ten earnings-call transcripts, from Q1 FY25 (call held 2024-08-09) to Q2 FY27 (call held 2026-11-05), were pulled with `tools/nse_fetch.py transcripts UNIPARTS --download` and converted with `pdftotext -layout`. The Q4 FY24 call (2024-05-28) was read for background only.
- **Numbers.** Actual figures come from the screener.in consolidated page (quarterly P&L, annual P&L, balance sheet, cash flow and ratios), plus the CFO's figures in each later call. Ratios were re-derived by hand: FY25 OPM, H1/H2 sums, capex totals, ROCE, aftermarket ₹ from share-of-revenue figures.
- **Extraction.** Each call was condensed into speaker turns, with management turns kept in full and analyst questions shortened. Every forward-looking statement that had a metric or a direction was logged, by hand, against the schema in `edge_methods_data_access.md` §2.
- **Scoring.** Status is one of: delivered (+1), partly (+0.5), missed (−1), moved-goalpost (−1.5), silently-dropped (−1.5) or pending. The weight of each promise is specificity score (1–3) × materiality (1–3) × 0.5^(quarters elapsed / 8).

## 2. Headline

| Measure | Value |
|---|---|
| Promises logged / resolved | 68 / 47 (21 pending) |
| Delivered / partly / missed / moved-goalpost / silently-dropped | 26 / 7 / 6 / 6 / 2 |
| Hit rate (delivered ÷ resolved) | 55% |
| **Management Credibility Score (MCS)**, scale −1.5..+1 | **+0.28** (+0.33 without the disputed small-ag item) |
| Average delivery ratio (actual ÷ promised, n=22) | 1.07 |
| Candour index (shortfalls admitted unprompted) | **~5%** (1 of 21: Hurricane Helene) |
| Moved goalposts | 6 (4 of them are the Mexico/third-platform storyline) |

**Breakdown. This is the useful part.**

| Slice | n resolved | MCS | Hit rate |
|---|---|---|---|
| FY25 calls (promoter Paramjit Soni guiding, downturn) | 24 | **−0.24** | 33% |
| FY26–27 calls (COO, later CEO, Tanushree Bagrodia, upturn) | 23 | **+0.65** | 78% |
| Cycle/financial promises (revenue, margin, FCF, capex, working capital) | 27 | **+0.53** | 63% |
| Execution/strategic promises (Mexico, acquisition/third platform, fabrication, aftermarket, tariff) | 20 | **−0.08** | 45% |
| Volunteered (opening remarks) | 10 | −0.29 | 30% |
| Prompted (in answer to analysts) | 37 | +0.43 | 62% |
| Precise / range / vague | 16 / 19 / 12 | +0.46 / +0.15 / +0.09 | 69% / 42% / 58% |

**What it means.**
1. **Promises that ride the cycle are now reliable, and conservative.** FY26 was guided mid-teens and came in at +21.4%. Every quarter-on-quarter guide from Q4 FY25 to Q2 FY27 was met or beaten. FY27 has been raised three times: mid-teens (Feb-26), "in line with FY26" (May-26), "couple of points above" (Aug-26), and **+24%** (Nov-26). H1 FY27 is running at +32%.
2. **Execution promises slip, and each slip is described as "on track".** Mexico was due to start in January 2026. The first dispatch went out in November 2026, about 10 months late, after four restated dates that were each called on schedule. The USD 9–10m CY26 base case quietly became "single-digit USD m in H2 FY27".
3. **The acquisition was a two-year narrative with no deal.** In Aug-24 it was coming "soon". In Nov-24 it was due "within the next year or so". In Feb-25 it was meant to supply 25–30% of sales. On 2026-05-26 management finally admitted it, when asked: about 12 targets screened and 2 near-misses that both fell through. The "third platform" is now organic fabrication, at under 2% of revenue today, aiming for 8–10% in 18–24 months. The October 2025 special dividend of ₹101.6 cr was the honest result of that admission.
4. **Aftermarket is the clearest case of goalposts moving.** In FY25 it was guided at +25–30% (Nov-24, and again in Feb-25, 7 weeks before year-end) and delivered +20%. For FY26 it was guided at "mid-teens" (Aug-25), then "single digit" (Nov-25, with the COO saying "we definitely have not de-grown"), then called a "stable contributor". The actual figure was **about −9%**: 20% of ₹964 cr fell to 15% of ₹1,170 cr, per the CEO's own shares given in Aug-26. In Q2 FY27 it rebounded more than 50% YoY, which met the Aug-26 promise that it would "normalise in 12 months".
5. **Candour is low.** Explanations for misses (tariffs, IMMEX registration, customer destocking, deals falling apart) are reasonable, but almost all came out only when an analyst pushed. The worst example is Feb-25. Asked whether Q4 FY25 would be the highest quarter, the promoter said "somebody asked me, is it going to be the highest? I said no", although he had said exactly that on the Aug-24 and Nov-24 calls. In Aug-24 an analyst said the calls sounded like *"Tarikh pe tarikh"* (date after date). The Q4 FY24 call adds the pre-history: FY25 had been guided at mid-teens growth in Feb-24, was "being reassessed" by May-24, cut to flat/−3% in Aug-24, and landed at −15%.

## 3. Tone versus delivery
- **FY25 (promoter-led):** tone was very upbeat ("light at the end of the tunnel", "Q4 turnaround", "worst is behind us") while delivery was poor on every near-term number. Tone was well above delivery, which is the pattern the India research (Jain, Khizer & Thirumalai) calls cheap talk.
- **FY26–27 (COO/CEO-led):** numeric tone is measured and is beaten every time, so the tone-delivery gap is negative, which is good. Execution tone is still "on track / absolutely on track / in line with planned schedule" while timelines slip, so that gap is still large.
- **Confound.** The change in leadership coincides with the turn in the cycle. These data cannot separate "a better guider" from "a guide set in a rising market". The cycle/execution split gives the same answer in both eras: execution items under-deliver whoever is speaking.

## 4. Change detectors noticed (not scored)
- After May-2025 the promoter Paramjit Soni, who gave all the FY25 guidance, no longer appears on calls. Tanushree Bagrodia joined as Group COO in Nov-2024 and was Group CEO by Feb-2026.
- The CFO changed from Rohit Maheshwari to Sandeep Taneja by May-2026. The IR lead changed three times, and the call host moved from Go India Advisors to EY in Aug-2026.
- The capex band crept up: 2.5% of revenue (May-25), then 2.5–3% (Feb-26), then 2.5–3.5% "we will not be deviating" (May-26), then about ₹60 cr, roughly 4% (Nov-26).
- Gross margin was helped by FX inventory gains (about 2% of material cost in Q2 FY26 and Q4 FY26), and management disclosed this when asked. The tariff "P&L neutral" claim was made four times and cannot be checked from outside.

## 5. What to watch next (pending items with dates)
- Q3 FY27 revenue of about ₹347 cr (in line with Q1). Freight cost recovery in Q3.
- Ludhiana finishing shop rebuilt by 31-Dec-2026.
- FY27 revenue +24% (about ₹1,450 cr). EBITDA "comfortably above 20%". Working capital 136–140 days.
- Mexico: single-digit USD m in H2 FY27, with 2 of 3 customers still to ramp up.
- Capex of about ₹60 cr over the next year.
- Fabrication at 8–10% of revenue by about Nov-2028.
- Peak revenue (FY23 ₹1,366 cr) regained by FY27 or mid-FY28. TTM is already ₹1,346 cr.
- Long-dated items: ROCE ≥ 25% (re-derived TTM about 24.5%), share of >70 hp three-point linkage at 20–25% by FY30, ₹2,000 cr revenue in the "5-year plan", geographic mix 40/30/25/5.

**Practical read.** Treat the revenue and margin guide in this upturn as a floor. Push any strategic or timeline promise (Mexico, fabrication, acquisition) out by 1–3 quarters, and give the acquisition story no value until a deal is signed. Ask next time: (a) the FY26 small-ag growth number; (b) the aftermarket ₹ figure each quarter; (c) Mexico revenue in ₹; (d) the fabrication ₹ figure and its OEM share.

## 6. Full ledger
Full quotes, evidence and explanations are in the seed JSON (`data.quote`, `data.evidence`, `data.explanation`).

| # | Said on | Speaker | Promise | Deadline | Spec. | Vol./Prompted | Status | Evidence (short) |
|---|---|---|---|---|---|---|---|---|
| 1 | 2024-08-09 | Paramjit Soni | FY25 revenue flat to -2/-3% vs FY24 | 2025-03-31 | range | prompted | **missed** | FY25 revenue INR 964 cr = -15.4% YoY (screener; Q4FY25 call). Guidance cut to 'flattish H2' in Nov-2024 and missed by ~12 pts. |
| 2 | 2024-08-09 | Paramjit Soni | H2 FY25 above H1; Q4 FY25 the highest run-rate quarter | 2025-03-31 | range | prompted | **moved-goalpost** | H1 FY25 = 261+241 = INR 502 cr; H2 = 208+253 = INR 461 cr (-8%). Q4 INR 253 cr < Q1 INR 261 cr. On 2025-02-07 the guide became 'between Q1 and Q2', and when asked the promoter said: 'somebod… |
| 3 | 2024-08-09 | Paramjit Soni | Q2 FY25 revenue sequentially flat | 2024-09-30 | range | prompted | **missed** | Q2FY25 revenue INR 241 cr = -7.6% QoQ (company Q2 call; screener). About 2.5 pts blamed on Hurricane Helene shutting the Augusta, Georgia plant. |
| 4 | 2024-08-09 | Paramjit Soni | FY25 EBITDA margin ~18% (including other income) | 2025-03-31 | precise | prompted | **partly** | FY25 operating margin 15.0% ex other income (145/964); including other income ~17.3% ((145+22)/964), re-derived from screener. Close on the company's own definition, ~0.7 pt short; 3 pts sho… |
| 5 | 2024-08-09 | Paramjit Soni | Long-term EBITDA margin of 20% maintained | 2027-03-31 | vague | prompted | **delivered** | FY26 OPM 21.1% (247/1,170); Q4FY26-Q2FY27 OPM 22-24% (screener). Achieved once volumes recovered. |
| 6 | 2024-08-09 | Paramjit Soni | FY25 capex INR 35-40 cr | 2025-03-31 | range | prompted | **partly** | Quarterly capex disclosed in calls: Q1 8.3 + Q2 ~6 + Q3 ~11 + Q4 6.5 = ~INR 32 cr (82-91% of the range). Under-spend in a downturn is benign; scored 'partly' mechanically. |
| 7 | 2024-08-09 | Paramjit Soni | Mexico near-shoring projects to start from January 2026 | 2026-01-31 | precise | prompted | **moved-goalpost** | First Mexico customer dispatch happened in Nov-2026, ~10 months after the Jan-2026 start; each new date was called 'on track'. Timeline: Aug-24 'projects start Jan-2026' -> Nov-24 'USD 6.5m … |
| 8 | 2024-08-09 | Paramjit Soni | Through-cycle revenue growth of 15-16% a year | 2029-03-31 | range | prompted | **pending** | Unscorable yet. FY23-FY26 revenue CAGR is -5% (1,366 to 1,170); TTM +33%. Needs a full cycle (FY23 peak to next peak). |
| 9 | 2024-08-09 | Paramjit Soni | Dividend policy unchanged; 'expect to do good dividends' while funding growth | 2025-03-31 | vague | prompted | **delivered** | FY25 dividend payout 73% of profit, FY26 108% (screener) despite lower profit; interim dividends kept. |
| 10 | 2024-08-09 | Paramjit Soni | Aftermarket to grow ~20% in FY25 | 2025-03-31 | precise | prompted | **delivered** | Q4FY25 call (2025-05-28, COO Tanushree Bagrodia): 'in FY '25, we actually grew 20% year-on-year' in aftermarket. Single source (management); segment revenue is not in screener. |
| 11 | 2024-08-09 | Paramjit Soni | Q4 FY25 'is where you will see the turnaround' | 2025-03-31 | vague | prompted | **missed** | Q4FY25 revenue INR 253 cr, -13% YoY (Q4FY24 INR 290 cr). Sequentially +22% off a seasonal Q3 low, but YoY growth only returned in Q1FY26 (+5%). |
| 12 | 2024-08-09 | Paramjit Soni | A third product platform (PTO/hydraulics/fabrication), organic or by acquisition, 'soon' | 2025-11-30 | vague | volunteered | **missed** | No acquisition or third platform by Nov-2026. Q4FY26 call (2026-05-26), when asked: 'We acknowledge that this has been talked about for a long time ... evaluated about a dozen targets since … |
| 13 | 2024-11-08 | Gurdeep Soni | Aftermarket to grow 25-30% YoY in FY25 | 2025-03-31 | range | volunteered | **partly** | Delivered +20% (Q4FY25 call) vs 25-30% guided in Nov-2024 and repeated on 2025-02-07, 7 weeks before year-end. The shortfall was never called a miss; the 20% was presented as a success. |
| 14 | 2024-11-08 | Gurdeep Soni | Q3 FY25 sequentially lower; Q4 highest; H2 flattish over H1 | 2025-03-31 | range | volunteered | **partly** | Q3 INR 208 cr < Q2 INR 241 cr (correct). Q4 INR 253 cr below Q1 INR 261 cr (wrong). H2 INR 461 cr vs H1 INR 502 cr = -8% (missed 'flattish'). Score: 1 of 3 parts. |
| 15 | 2024-11-08 | Gurdeep Soni | USD 6.5m annual Mexico award to start Q4 FY26 | 2026-03-31 | precise | volunteered | **moved-goalpost** | No Mexico supplies in Q4FY26 or Q1-Q2FY27; dispatch started Nov-2026 (Q3FY27). The USD 6.5m/yr figure has not been repeated since Feb-2025. Timeline: Aug-24 'projects start Jan-2026' -> Nov-… |
| 16 | 2024-11-08 | Paramjit Soni | Mexico base case USD 9-10m of sales in CY2026 | 2026-12-31 | range | prompted | **moved-goalpost** | Effectively impossible: dispatches only began in Nov-2026. Target quietly restated as 'mid-single-digit million dollar' for FY27 (Aug-26) and 'single-digit million dollar ... next 6 months' … |
| 17 | 2024-11-08 | Paramjit Soni | Third platform (inorganic) 'within the next year or so' | 2025-12-31 | vague | prompted | **missed** | Deadline (~end-2025) passed with no deal. Admitted only in answer to an analyst on 2026-05-26 (two near-misses, about a dozen targets screened). Small/mid fabrication is being built organica… |
| 18 | 2024-11-08 | Paramjit Soni | Small ag and small construction recover in H2 CY2025; large ag in CY2026 | 2025-12-31 | vague | prompted | **partly** | Construction did recover from H2 CY2025 (Q2/Q3 FY26 calls: 'green', AI/data-centre demand; Q3FY26 revenue +35%). Small ag recovered only in India/Asia and Europe; North American small ag was… |
| 19 | 2024-11-08 | Paramjit Soni | ROCE back above 25% once out of the downturn | 2027-03-31 | precise | prompted | **partly** | FY26 ROCE 22% (screener). Re-derived TTM to Sep-2026: EBIT (PBT 258 + interest 13) / (equity 944 + debt 162) = ~24.5%. Chairman claims 'north of 27%' TTM (2026-08-05; definition not given). … |
| 20 | 2024-11-08 | Paramjit Soni | Mexico phase 1: hardly any capex and no margin erosion; phase 2 capex at most a couple of USD m | 2026-12-31 | vague | prompted | **delivered** | Phase 1 was a warehouse only; no large Mexico capex disclosed; group OPM rose to 21-24%. Phase 2 (local production) not yet started. Management-only evidence. |
| 21 | 2025-02-07 | Paramjit Soni | FY26 revenue growth 'double-digit mid-teen', driven by new business | 2026-03-31 | range | prompted | **delivered** | FY26 revenue INR 1,170 cr vs INR 964 cr = +21.4% (screener), beating mid-teens. Q3FY26 +35% and Q4FY26 +34% YoY. |
| 22 | 2025-02-07 | Paramjit Soni | Q4 FY25 revenue between Q1 and Q2 levels (INR 241-261 cr), 'not the highest' | 2025-03-31 | range | prompted | **delivered** | Q4FY25 revenue INR 253 cr (screener; Q4 call) - inside the range. NB: this quietly replaced the Aug/Nov-2024 'Q4 highest run-rate' guidance; the change was only stated when an analyst asked. |
| 23 | 2025-02-07 | Paramjit Soni | Growth starts H1 FY26; new projects 'really blooming' in H2 FY26 | 2026-03-31 | vague | prompted | **delivered** | H1 FY26 INR 551 cr vs H1 FY25 INR 502 cr (+10%); H2 FY26 INR 620 cr vs INR 461 cr (+34%) (screener). |
| 24 | 2025-02-07 | Paramjit Soni | Margins back toward 20%+ as volumes recover | 2026-03-31 | vague | prompted | **delivered** | OPM: FY25 15.0% -> FY26 21.1%; Q4FY26 24% (screener). |
| 25 | 2025-02-07 | Paramjit Soni | Share of >70hp 3-point-linkage market from 8-9% to 20-25% over 5 years | 2030-03-31 | range | prompted | **pending** | Not checkable from public data; management has not re-disclosed the share figure since. Needs a recurring question on calls. |
| 26 | 2025-02-07 | Paramjit Soni | Third platform (inorganic, PTO/hydraulics/fabrication) worth 25-30% of sales; a fourth 1-2 years later | 2027-03-31 | vague | prompted | **moved-goalpost** | No acquisition. The third platform is now presented as organic small/mid fabrication, targeted at 'high single digits, if not 10% of revenue' in 18-24 months (Nov-26), down from 25-30% of sa… |
| 27 | 2025-05-28 | Tanushree Bagrodia | FY26 top-line growth mid-teens (reiterated by COO) | 2026-03-31 | range | prompted | **delivered** | FY26 revenue +21.4% (INR 1,170 cr vs 964 cr, screener). |
| 28 | 2025-05-28 | Tanushree Bagrodia | Q1 FY26 revenue in line with Q4 FY25 | 2025-06-30 | precise | prompted | **delivered** | Q1FY26 revenue INR 274 cr (+8% vs Q4FY25 INR 253 cr; screener) - beat. |
| 29 | 2025-05-28 | Tanushree Bagrodia | US tariffs to be P&L neutral in FY26 (cost passed to customers; working-capital hit only) | 2026-03-31 | precise | prompted | **delivered** | FY26 OPM 21.1% vs 15.0% (screener); management repeated 'P&L neutral' on 2025-08-11, 2025-11-17 and 2026-05-26 as tariffs went 10% -> 25% -> 50% -> 18%. Gross margin was flattered by FX inve… |
| 30 | 2025-05-28 | Paramjit Soni | Quarterly free cash flow sustained at FY25 levels | 2026-03-31 | range | volunteered | **delivered** | FY26 FCF INR 148 cr vs FY25 INR 152 cr (screener), 97%, despite revenue +21% and tariff working-capital drag. |
| 31 | 2025-05-28 | Tanushree Bagrodia | Fabrication (own facility) revenue from OEMs within 10-15 months | 2026-08-31 | range | prompted | **partly** | By Nov-2026 fabrication is under 2% of revenue but 12-15% of new business wins. In Aug-26 OEM supply was still 'in deep discussion ... to now start supplying'; in Nov-26 they were 'working w… |
| 32 | 2025-05-28 | Tanushree Bagrodia | Capex held at ~2.5% of revenue (INR 30-40 cr) | 2026-03-31 | precise | prompted | **delivered** | FY26 capex ~INR 30 cr (7+6+5+12 per CFO quarterly remarks) = 2.6% of revenue. |
| 33 | 2025-08-11 | Tanushree Bagrodia | Q2 FY26 revenue in line with Q1 FY26 | 2025-09-30 | precise | prompted | **delivered** | Q2FY26 revenue INR 277 cr (screener) / INR 283 cr total revenue (company), +1-1.5% QoQ. |
| 34 | 2025-08-11 | Tanushree Bagrodia | FY26 mid-teens growth maintained after the 50% US tariff shock | 2026-03-31 | range | prompted | **delivered** | FY26 revenue +21.4% (screener). Note: in Nov-2025 the Chairman's script softened this to 'double-digit growth for FY26' while the COO kept 'mid-teens'. |
| 35 | 2025-08-11 | Tanushree Bagrodia | FY26 EBITDA margin 'in the range of 18%' | 2026-03-31 | precise | prompted | **delivered** | FY26 OPM 21.1% ex other income (screener 247/1,170). Beat, though management attributed much of the gross-margin gain to rupee depreciation lifting inventory values (Q1/Q2 FY26 calls). |
| 36 | 2025-08-11 | Gurdeep Soni | Aftermarket to grow mid-teens in FY26 | 2026-03-31 | range | volunteered | **moved-goalpost** | Cut to 'single digit' growth 3 months later (Chairman, 2025-11-17) without calling it a cut. The 9M FY26 aftermarket share then fell to 14% from 19% (analyst figure, not disputed by the CEO … |
| 37 | 2025-08-11 | Gurdeep Soni | Small-ag segment to grow mid-teens in FY26 despite flat OEM outlook | 2026-03-31 | range | volunteered | **silently-dropped** | No FY26 small-ag growth figure was ever reported, though in Q2FY27 they did give quarterly segment growth (small ag +25% YoY). Agriculture revenue fell from ~INR 970 cr (FY23) to ~INR 717 cr… |
| 38 | 2025-08-11 | Tanushree Bagrodia | Mexico warehouse operational in October 2025 | 2025-10-31 | precise | prompted | **delivered** | Q2FY26 call (2025-11-17, Chairman): 'the Mexico warehouse become operationally ready in October 2025, in line with our planned schedule'. Management-only evidence (single-source). |
| 39 | 2025-08-11 | Tanushree Bagrodia | INR 2,000 cr+ revenue within the 5-year plan | 2030-03-31 | vague | prompted | **pending** | TTM revenue to Sep-2026 INR 1,346 cr (screener). Needs ~10% CAGR from FY26 INR 1,170 cr to reach INR 2,000 cr by FY31-ish; 'aspiration', not guidance. |
| 40 | 2025-08-11 | Tanushree Bagrodia | Long-term revenue mix: US 40% / Europe 30% / Asia 25% / RoW 5% | 2030-03-31 | precise | prompted | **pending** | H1FY26: Europe 25% (from 23%), Japan 6% (from 5%) per Q2FY26 call; North America still >50%. Direction right, long way to go. |
| 41 | 2025-11-17 | Gurdeep Soni | Aftermarket guidance cut to single-digit growth for FY26 | 2026-03-31 | range | volunteered | **silently-dropped** | No FY26 aftermarket growth number disclosed. Language moved from '25-30% growth' (FY25) to 'important business driver' (Nov-25) to 'stable contributor' (Feb/May-26). The implied 9M FY26 decl… |
| 42 | 2025-11-17 | Tanushree Bagrodia | Return to peak (FY23) revenue by FY27 or mid-FY28 | 2027-09-30 | range | prompted | **pending** | On track: TTM to Sep-2026 INR 1,346 cr; H1FY27 INR 726 cr (screener) annualises to ~INR 1,450 cr. Resolve after Q4FY27. |
| 43 | 2025-11-17 | Tanushree Bagrodia | FY27 growth better than FY26 | 2027-03-31 | vague | prompted | **pending** | H1FY27 revenue INR 726 cr vs H1FY26 INR 551 cr = +32% (screener). On track; resolve after Q4FY27. |
| 44 | 2025-11-17 | Tanushree Bagrodia | Normalised EBITDA (ex-FX) 18-20%, with 20% the through-cycle target | 2026-03-31 | range | prompted | **delivered** | Reported OPM H2FY26 ~22.8% ((56+81)/(281+339)), FY26 21.1% (screener). FX normalisation cannot be checked from outside; reported numbers are above the range. |
| 45 | 2026-02-10 | Tanushree Bagrodia | Close FY26 with mid-teens growth (9M at +17%) | 2026-03-31 | range | prompted | **delivered** | FY26 +21.4% (screener); Q4FY26 +34% YoY. Chairman (2026-05-26): 'performance exceeding the guidance shared earlier'. |
| 46 | 2026-02-10 | Tanushree Bagrodia | FY27 revenue growth mid-teens (first FY27 guide) | 2027-03-31 | range | prompted | **pending** | Raised to 'in line with FY26' (~20%) on 2026-05-26. H1FY27 +32% (screener). On track to beat. |
| 47 | 2026-02-10 | Tanushree Bagrodia | 20% EBITDA margin 'sustainable over the cycle' | 2027-03-31 | precise | prompted | **pending** | Q4FY26 24%, Q1FY27 ~26% (company EBITDA 90/347), Q2FY27 23.4% (company). Above target so far; a through-cycle claim needs the next downturn to test it. |
| 48 | 2026-02-10 | Tanushree Bagrodia | Ludhiana fire (27-Dec-2025): 'nothing significant envisaged for Q4' | 2026-03-31 | vague | prompted | **delivered** | Q4FY26 revenue INR 339 cr, a record, +21% QoQ (screener). Insurance claim filed; rebuild under way (Q4FY26 call). |
| 49 | 2026-02-10 | Tanushree Bagrodia | Mexico supplies 'hopefully' start next quarter (Apr-Jun 2026) after customer's IMMEX registration | 2026-06-30 | precise | prompted | **missed** | Slipped about 2 quarters: Aug-26 call moved first deliveries to Q3FY27; dispatch began Nov-2026 (Q2FY27 call, 2026-11-05). New date given unprompted in the Aug-26 opening remarks, but framed… |
| 50 | 2026-02-10 | Tanushree Bagrodia | Capex 2.5-3% of revenue (range widened from 2.5%) | 2026-03-31 | range | prompted | **delivered** | FY26 capex 7+6+5+12 = ~INR 30 cr = 2.6% of INR 1,170 cr (quarterly CFO disclosures). Note the band drifting up: 2.5% (May-25) -> 2.5-3% (Feb-26) -> 2.5-3.5% (May-26) -> INR ~60 cr 'over next… |
| 51 | 2026-05-26 | Gurdeep Soni | FY27 growth 'in line with FY26' (~20%); H2 FY27 stronger than H1 | 2027-03-31 | range | volunteered | **pending** | H1FY27 INR 726 cr, +32% YoY (screener). Running well ahead; resolve after Q4FY27. |
| 52 | 2026-05-26 | Gurdeep Soni | Q1 FY27 revenue in line with Q4 FY26 | 2026-06-30 | precise | volunteered | **delivered** | Q1FY27 revenue INR 347 cr (+2% QoQ; screener and CFO). |
| 53 | 2026-05-26 | Tanushree Bagrodia | FY27 EBITDA 'comfortably above' 20% | 2027-03-31 | precise | prompted | **pending** | H1FY27 company EBITDA INR 178 cr on INR 726 cr = 24.5%; screener OPM 22-24%. On track. |
| 54 | 2026-05-26 | Tanushree Bagrodia | Working-capital improvement (155 -> 136 days; inventory 146 -> 134 days) to be sustained | 2027-03-31 | precise | prompted | **pending** | 139 days at Jun-2026, 137 days at Sep-2026 (CFO). Holding so far. |
| 55 | 2026-05-26 | Tanushree Bagrodia | Fire-damaged surface-finishing shop rebuilt and online by end of the year | 2026-12-31 | vague | prompted | **pending** | Check Q3FY27 call. 'End of the year' is ambiguous (Dec-2026 vs Mar-2027) - a deadline_precision lesson. |
| 56 | 2026-05-26 | Tanushree Bagrodia | Tariffs remained P&L neutral through FY26 | 2026-03-31 | precise | prompted | **delivered** | Restatement of the May-2025 promise; FY26 OPM rose to 21%. Management-only evidence; FX inventory gains (~2% of material cost in Q2 and Q4) help mask any leakage. |
| 57 | 2026-08-05 | Tanushree Bagrodia | Q2 FY27 revenue in line with Q1 FY27 | 2026-09-30 | precise | prompted | **delivered** | Q2FY27 revenue INR 379 cr (+9% QoQ, record quarter; screener and CFO) - beat. |
| 58 | 2026-08-05 | Gurdeep Soni | First Mexico warehouse deliveries in Q3 FY27 | 2026-12-31 | precise | volunteered | **delivered** | Q2FY27 call (2026-11-05): 'our first customer dispatch will take place this month'; CEO: 'we've only started dispatches in November'. Management-only evidence. This is the 4th Mexico date an… |
| 59 | 2026-08-05 | Tanushree Bagrodia | Aftermarket demand to normalise and return to growth over the next 12 months | 2027-08-31 | vague | prompted | **delivered** | Q2FY27 (2026-11-05): aftermarket 16.5% of revenue vs 14.7% in Q2FY26; 'In absolute terms, the segment grew over 50% year-on-year'. One quarter; management warns it varies quarter to quarter.… |
| 60 | 2026-08-05 | Tanushree Bagrodia | FY27 growth 'a couple of percentage points' above FY26's 21% | 2027-03-31 | range | prompted | **pending** | Third FY27 raise: mid-teens (Feb-26) -> 'in line with FY26' (May-26) -> +~23% (Aug-26) -> +24% (Nov-26). H1 +32%. |
| 61 | 2026-08-05 | Tanushree Bagrodia | Warehouse-channel share of sales at 52-56% over 12-18 months | 2027-12-31 | range | prompted | **pending** | Q1FY27 56%, Q2FY27 53% (CEO). In range so far. |
| 62 | 2026-11-05 | Tanushree Bagrodia | FY27 revenue +24% YoY | 2027-03-31 | precise | prompted | **pending** | Implies H2FY27 ~INR 725 cr (+17% YoY), about level with H1 INR 726 cr, consistent with 'Q3 in line with Q1'. Check Q3/Q4 FY27. |
| 63 | 2026-11-05 | Tanushree Bagrodia | Q3 FY27 (seasonally weakest) revenue broadly in line with Q1 FY27 | 2026-12-31 | precise | prompted | **pending** | Check Feb-2027 results. |
| 64 | 2026-11-05 | Tanushree Bagrodia | Organic fabrication to be a 'meaningful third platform' at high single digits to ~10% of revenue in 18-24 months | 2028-11-30 | range | prompted | **pending** | Starting point under 2% of revenue; 12-15% of trailing new wins. First stated Aug-26 ('meaningful vertical in 18-24 months'); quantified Nov-26. Replaces the 25-30% acquired third platform (… |
| 65 | 2026-11-05 | Sandeep Taneja | Capex of ~INR 60 cr over the next year (~4% of revenue), mostly approved | 2027-11-30 | precise | volunteered | **pending** | Above the '2.5-3.5% of revenue, we will not be deviating' line of 2026-05-26; the CEO now calls it 'about 4% of our revenue because there is growth'. A goalpost shift to watch, though growth… |
| 66 | 2026-11-05 | Sandeep Taneja | FY27 net working capital 136-140 days | 2027-03-31 | range | prompted | **pending** | 137 days at Sep-2026. Some US customer payment delays ('technical issues', not disputes). |
| 67 | 2026-11-05 | Sandeep Taneja | Higher freight costs recovered from customers next quarter | 2026-12-31 | vague | prompted | **pending** | Check Q3FY27 other-expense ratio. |
| 68 | 2026-11-05 | Gurdeep Soni | Ludhiana finishing shop back up by end of calendar 2026 | 2026-12-31 | precise | volunteered | **pending** | Restates and clarifies the May-26 'end of the year' promise as calendar 2026. Check Q3FY27 call. |

## 7. Lessons learned on the method

**What was hard**
1. **Volume and noise.** Each call runs to about 9–11k words, and roughly 70% of that is restated strategy ("global delivery model", "best-cost country"). Only about 6–8 statements per call are real promises. Condensing to speaker turns (management in full, questions shortened) cut reading by about 40% without losing promises.
2. **Speaker attribution in pdftotext output is unreliable.** Labels such as "Q Management:", misspellings ("Parmjit", "Paramjit Sonis") and the CFO's turn sometimes tagged as a question all appear. A name list per company is needed, and the management list from the cover page should be parsed automatically.
3. **Deadlines are fuzzy.** "Second half next year" (calendar or fiscal? the speaker said calendar only when asked), "end of the year" (Dec-26 or Mar-27, resolved one call later), and "within the next year or so" all need a precision field plus a rule. Here: treat ambiguous as the later date, and record which one was assumed.
4. **Restatements versus new promises.** The same FY26 mid-teens guide was repeated in 5 calls. Counting each repeat inflates the "delivered" count. Logging only material restatements (after a shock or a change of speaker) fixed most of this, but a `restates: <id>` link is needed, with credit for the first statement only.
5. **Segment KPIs often can't be checked from outside.** Aftermarket, small ag, Mexico revenue and fabrication are reported only as percentages, now and then, and only when asked. The aftermarket miss had to be pieced together from share-of-revenue numbers in different calls. One promise (small-ag mid-teens) had to be marked "silently-dropped" because no number ever came back. That is the most debatable call in the set, so MCS is shown with and without it.
6. **Judging moved-goalpost against missed is subjective.** The line drawn here: a target revised before its deadline *without being called a revision* is moved-goalpost; a target missed after an honest restatement is missed. This rule should be written down and a second reviewer should check it.
7. **Era is confounded with the cycle.** A cyclical company guiding in a downturn will always score worse. MCS should be reported next to an industry cycle indicator, such as the change in Deere or CAT segment sales, or we will reward luck.
8. **Company-defined metrics.** Reported "EBITDA" includes other income, while screener OPM does not. Store both and score on the company's own definition (FY25: 17.3% against an 18% guide gives "partly"). Flag the gap.

**What to automate (priority order)**
1. **Fetch + diff pipeline:** run `nse_fetch transcripts` → `pdftotext` → speaker-turn JSON with the management roster parsed from the cover page. This is fully scriptable now; the scratch code is `turns.py`.
2. **LLM extraction pass** with a fixed prompt that outputs the schema fields (quote, metric, target_low/high, unit, deadline, precision, volunteered flag, conditionality). A human then spot-checks about 20%. Expect about 8 candidates per call and a precision of about 70%.
3. **Auto-resolver for financial promises:** connect to screener quarterly and annual tables through `memdb metric`, so that revenue, OPM, FCF, capex and working-capital items score themselves once the quarter is reported. That is about 60% of the promises here.
4. **Restatement linker:** use embedding similarity on metric + deadline against open promises for the same ticker, then either attach to the existing promise (with status history) or create a new one. This also catches quiet target changes, for example a target number that differs from the last call while the wording says "maintain".
5. **"Stopped mentioning" detector:** track KPI terms per call (aftermarket %, Mexico USD, the 6.5m award, third platform 25–30%) and alert when a quantified KPI disappears for 2 or more calls.
6. **Candour tagger:** for each shortfall, check whether the next call's *opening remarks* mention it (unprompted) or whether it appears only in Q&A (prompted).
7. **Change-detector sidecar:** compare the management roster across calls (CFO, promoter attendance, IR host). This is cheap and flagged three changes here.

**Cost of this pilot:** about 100k words of transcript read, 68 promises, and roughly one person-day equivalent of work. With steps 1–4 automated, a quarterly update per company should take about 15 minutes of human review.
