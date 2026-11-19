# Quant Pattern Hunt: Early-Multibagger Fingerprint (NSE/BSE)
**Date:** 2026-11-19 | **Method:** stock-research-analyst skill (5 stages + verification gate) | Research only, not investment advice.

## Stage 1: Context (theme-agnostic)
I didn't screen by theme. I looked for the Radico 2016-17 / Motilal Oswal "twin engine" setup: a step-change in OPM and ROCE lasting several quarters, debt falling, no equity dilution, self-funded capex, no promoter pledge (ideally promoter buying), FII/DII holdings rising for several quarters in a row, market cap ₹300-10,000 cr and P/E of about 30 or less.

## Stage 2: Universe
- **Screens pulled (all pages, 19 Nov 2026):** Debt reduction (246 names), Growth without dilution (338), Capacity expansion (1,357), FII buying (99), Quarterly growers (414), Best of latest quarter (707), Loss-to-profit (130), Piotroski (566) and Magic formula (120).
- **Overlap filter:** market cap ₹300-10,000 cr. That left 85 names in 3 or more screens and about 80 in 2 screens with P/E ≤30 and ROCE ≥15.
- **Exclusions:** SME and recent micro listings (Kalind, Shera, APS, SJ Logistics, the 544xxx codes), holding companies, NBFCs, InvITs and trading houses.
- **Pages fetched:** consolidated screener.in pages for 42 names. The consolidated view was empty or stale for 16 of them, so I refetched those as standalone and flagged them below.
- **Raw files:** `/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/quant/`

## Price verification (Stage 3)
Each finalist's price comes from two sources dated the same day:
- Source A: Screener page, 19 Nov 2026, 3:32-3:50 pm.
- Source B: Google Finance NSE close, 19 Nov 2026, 3:30 pm IST.

P/E is recomputed as market cap at the Google close divided by the sum of the last four quarters' net profit.

| Ticker | Screener (19 Nov) | Google Fin (19 Nov close) | Mcap @ close | TTM PAT (4Q sum) | Recomputed P/E | Screener P/E |
|---|---|---|---|---|---|---|
| SANDUMA | ₹168 | ₹167.61 | ~₹8,150 cr | 841 (116+236+228+261) | **9.7x** | 9.5 |
| IOLCP | ₹192 | ₹192.00 | ~₹5,634 cr | 203 (21+53+64+65) | **27.7x** (H1 annualised 21.8x) | 26.6 |
| GULPOLY (standalone) | ₹161 | ₹161.70 | ~₹1,008 cr | 172 (41+38+54+39) | **5.9x** | 5.9 |
| BIRLACABLE | ₹301 | ₹301.20 | ~₹904 cr | 84 (4+11+31+38) | **10.8x** (H1 annualised 6.5x) | 10.8 |
| SYNCOMF | ₹22.2 | ₹22.19 | ~₹2,085 cr | 96 (19+25+25+27) | **21.7x** | 21.8 |

Earlier dated quotes found by web search (all within ±15%): IOLCP ₹180 (2 Nov, Upstox) and ₹210 intraday (9 Nov, Bajaj); GULPOLY ₹171 (13 Nov); SANDUMA ₹164 (3 Nov, Upstox); BIRLACABLE ₹316 (3 Nov, Upstox). These do not contradict the 19 Nov figures.

**Reverse-DCF check.** Assumptions: 12% required return, 10 years, exit P/E 15x, dividends ignored. The PAT CAGR each price implies:
- Gulshan: ~2%
- Sandur: ~7%
- Birla Cable: ~8% from TTM, ~3% from run-rate
- Syncom: ~16%
- IOL: ~19% from TTM, ~16% from H1 run-rate

---

## Finalist 1: Sandur Manganese & Iron Ores (SANDUMA). Conviction 68/100. BUY-ZONE (research)
**Financials (consolidated, ₹ cr)**

| | FY22 | FY23 | FY24 | FY25 | FY26 | TTM |
|---|---|---|---|---|---|---|
| Sales | 2,249 | 2,126 | 1,252 | 3,135 | 5,088 | 5,602 |
| OPM | 43% | 18% | 26% | 25% | 24% | 24% |
| PAT | 675 | 271 | 239 | 471 | 658 | 841 |
| Borrowings | 206 | 133 | — | 1,890 | 999 | 904 (Sep-26) |
| CFO | 873 | 142 | 153 | 841 | 1,143 | |
| ROCE | — | — | 15% | 21% | 24% | |

FY22 borrowings were reported at a different year-end, so the FY23 figure shown is the Mar-2023 value.

| Qtr | Dec24 | Mar25 | Jun25 | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|---|---|---|
| Sales | 952 | 1,321 | 1,135 | 1,232 | 1,209 | 1,511 | 1,375 | 1,506 |
| OPM | 25% | 24% | 26% | 22% | 21% | 26% | 25% | 25% |
| Interest | 41 | 67 | 54 | 57 | 46 | 55 | 26 | 26 |
| PAT | 137 | 156 | 167 | 139 | 116 | 236 | 228 | 261 |

**Shareholding**

| | Jun25 | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|---|
| Promoter | 74.22 | 74.22 | 74.22 | 74.22 | 74.22 | 74.22 |
| FII | 1.00 | 1.01 | 1.20 | 1.63 | 1.73 | 1.98 |
| DII | 0.59 | 0.70 | 0.67 | 0.66 | 0.58 | 0.58 |

- FII holding has risen for six straight quarters.
- Screener shows no pledge flag.
- Equity went from ₹162 cr to ₹486 cr in FY26. This is a bonus issue: the share count tripled with no cash raised, and reserves kept growing.

**Structural story and named cause**
- The Arjas Steel acquisition (FY25, debt-funded, now Royal Sandur Metals) turned a mining company into an integrated ore-to-steel business. Revenue went from 1,252 to 5,602.
- FY26 free cash flow of ₹988 cr was used to cut debt from 1,890 to 904. Quarterly interest halved from 55 to 26.
- In Q2 FY27, iron ore sales rose about 59% and value-add steel projects started running. Q2 PAT was ₹260 cr, up 87-88% YoY (Multibagg, SteelOrbis, Univest).
- This is the Radico-type deleveraging setup: PAT has stepped up from ~₹140 cr/qtr to ~₹240 cr/qtr for three quarters running, while OPM is flat. The jump comes from lower interest plus higher volumes.

**Bull case**
- Run-rate PAT is about ₹1,000 cr (Q1+Q2 FY27 annualised ≈ 978).
- Debt could be close to zero by FY28 from free cash flow.
- At 12-14x on ₹1,100-1,200 cr PAT, market cap would be ₹13-17k cr, 1.6-2.1x in 2-3 years. That needs commodity prices to hold.

**Risks**
- Iron ore, manganese and steel price cycles. Manganese, ferroalloy and coke sales fell in Q2.
- Karnataka mining levies (the state's mineral-rights tax regime) and lease or mining-cap rules.
- The promoter is at the 75% cap, which limits free float. Market cap is near the top of the band.
- Inventory days are volatile (794 in FY24, 149 in FY26).

**Kill criteria**
- Quarterly PAT below ₹180 cr for two quarters.
- Net debt rising again for a new debt-funded acquisition.
- FII trend reverses below 1.5%.
- An adverse change in Karnataka mining tax or caps.

## Finalist 2: IOL Chemicals & Pharmaceuticals (IOLCP). Conviction 64/100. WATCHLIST (near buy-zone)
**Financials (consolidated, ₹ cr)**

| | FY22 | FY23 | FY24 | FY25 | FY26 | TTM |
|---|---|---|---|---|---|---|
| Sales | 2,184 | 2,217 | 2,133 | 2,079 | 2,319 | 2,751 |
| OPM | 12% | 10% | 11% | 10% | 12% | 13% |
| PAT | 168 | 139 | 134 | 101 | 138 | 203 |
| Borrowings | 44 | 80 | 33 | 117 | 135 | 201 (Sep-26) |
| CFO | 93 | 122 | 290 | 179 | 214 | |
| ROCE | — | 14% | 12% | 9% | 11% | |

| Qtr | Dec24 | Mar25 | Jun25 | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|---|---|---|
| Sales | 523 | 528 | 552 | 568 | 580 | 619 | 756 | 795 |
| OPM | 9% | 12% | 11% | 10% | 10% | 15% | 14% | 14% |
| PAT | 21 | 31 | 34 | 30 | 21 | 53 | 64 | 65 |

**Shareholding**

| | Jun25 | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|---|
| Promoter | 52.62 | 52.62 | 52.62 | 57.48 | 62.28 | 62.28 |
| FII | 2.59 | 2.25 | 2.08 | 1.72 | 4.87 | 7.26 |
| DII | 0.02 | 0.05 | 0.03 | 0.02 | 0.43 | 0.30 |

- The promoter stake rose about 9.7 percentage points through open-market buying (NCVI Enterprises and Mayadevi Polycot, March 2026) with no new shares issued. Equity capital stayed at ₹59 cr.
- The promoter disclosed no encumbrance for FY26.
- FII holding has tripled in two quarters.

**Structural story and named cause**
- Product mix is shifting away from ibuprofen. Non-ibuprofen APIs reached 45% of pharma revenue in Q2 FY27 (38% a year earlier), with that line growing about 70% YoY.
- Pharma segment EBIT nearly doubled (35.5 to 68.1). Chemicals EBIT also improved.
- Q2 FY27 numbers: revenue ₹795 cr (+40%), EBITDA ₹115 cr (+80%), PAT ₹65 cr (2.2x). Guided EBITDA margin is 14-15% (FPJ, Multibagg, Sahi).
- This is a Radico-style mix shift combined with heavy promoter buying, the strongest insider signal in the set.
- Debtor days have crept up (79 to 95), CFO/EBITDA was 93% in FY26 and capex is self-funded (CWIP of ₹189 cr).

**Bull case**
- If FY28 sales reach ₹3,600 cr at 15% OPM, PAT would be about ₹330 cr. At 22-25x, market cap would be ₹7.3-8.3k cr, 1.3-1.5x.
- Real multibagger upside needs ROCE to move toward 18-20%. FY20-21 (30% OPM) shows what operating leverage can do.

**Risks**
- P/E of 27.7x on TTM is already at the top of the allowed range.
- ROCE of 11% is low.
- The stock has already rerated, from a 52-week low of ~₹67 to a high of ~₹224 and ₹192 now.
- Ibuprofen pricing is cyclical and exposed to Chinese supply.
- The promoter stake is now 62%, so further buying is limited by takeover rules.

**Kill criteria**
- OPM below 12% for two quarters.
- Non-ibuprofen share stalls below 40%.
- The promoter sells.
- Debtor days above 110.
- **Entry discipline:** wait for Q3 FY27 confirmation or a P/E ≤22x on TTM.

## Finalist 3: Gulshan Polyols (GULPOLY, standalone; consolidated data stale). Conviction 58/100. WATCHLIST
**Financials (standalone, ₹ cr)**

| | FY22 | FY23 | FY24 | FY25 | FY26 | TTM |
|---|---|---|---|---|---|---|
| Sales | 1,101 | 1,180 | 1,378 | 2,020 | 2,312 | 2,432 |
| OPM | 14% | 7% | 4.2% | 4.8% | 10% | 13% |
| PAT | 85 | 45 | 18 | 25 | 107 | 171 |
| Borrowings | 112 | 248 | 349 | 397 | 318 | 234 (Sep-26) |
| CFO | 61 | 16 | 66 | 42 | 207 | |
| ROCE | 23% | 9% | 3% | 6% | 19% | |

| Qtr | Dec24 | Mar25 | Jun25 | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|---|---|---|
| Sales | 610 | 515 | 593 | 542 | 627 | 551 | 640 | 615 |
| OPM | 4.4% | 6% | 6% | 8% | 14% | 12% | 13% | 11% |
| PAT | 7 | 7 | 13 | 16 | 41 | 38 | 54 | 39 |

**Shareholding**

| | Jun25 | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|---|
| Promoter | 66.71 | 66.71 | 66.80 | 66.80 | 66.80 | 66.80 |
| FII | 0.00 | 0.00 | 0.00 | 0.29 | 0.32 | 0.26 |
| DII | 0.56 | 0.07 | 0.00 | 0.00 | 0.00 | 0.00 |

- No pledge flag on Screener.
- No dilution: equity capital flat at ₹6 cr.
- Debtor days are 32. FY26 CFO was 1.9x PAT.

**Named cause**
- Its grain-ethanol distilleries, built with debt in FY22-24, are now running at about 82% utilisation.
- Ethanol EBITDA margin was 16% in H1 FY27 against 8% a year earlier.
- The 2026-27 allocation is 1.97 lakh KL, worth about ₹1,305 cr.
- Q2 FY27 PAT was ₹39 cr, +151% (Multibagg, Arthneeti, Univest).

**Why not BUY-ZONE**
- The margin is a feedstock spread, not a franchise. Management says ethanol becomes unviable with maize above ₹26-27/kg. Maize is at ₹30-32/kg now, and H2 ethanol margins are guided 1-2 percentage points lower.
- Full-year ethanol EBITDA guidance is 11-12%. Q2 OPM has already dipped to 11%.
- Institutions are absent: DII went to zero and FII is only about 0.3%.
- The positives are real: deleveraging (397 to 234, with an HSBC loan exit targeted by February), 5.9x P/E and a reverse DCF implying only about 2% growth.

**Bull case**
- If FY27 sales are ₹2,600 cr at 10-11% EBITDA (guidance), PAT would be ₹140-160 cr. At 9-10x, market cap would be ₹1,400-1,600 cr, 1.4-1.6x.
- Grain-price normalisation plus a ₹100-120 cr sorbitol/maltodextrin capex could add a less cyclical leg.

**Kill criteria**
- OPM below 8% in Q3/Q4 FY27.
- Debt rising above ₹300 cr.
- The ethanol procurement price is not revised up while grain costs stay high.

## Finalist 4: Birla Cable (BIRLACABLE). Conviction 45/100. WATCHLIST (do not chase)
**Financials (consolidated, ₹ cr)**

| | FY22 | FY23 | FY24 | FY25 | FY26 | TTM |
|---|---|---|---|---|---|---|
| Sales | 535 | 792 | 686 | 662 | 771 | 1,040 |
| OPM | 8% | 8% | 6% | 4.9% | 6% | 13% |
| PAT | 22 | 33 | 22 | 5 | 17 | 83 |
| Borrowings | 82 | 129 | 165 | 111 | 133 | 106 (Sep-26) |
| CFO | 3 | -8 | 16 | 112 | -21 | |

| Qtr | Dec24 | Mar25 | Jun25 | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|---|---|---|
| Sales | 158 | 156 | 176 | 176 | 205 | 214 | 267 | 355 |
| OPM | 6% | 5% | 4.4% | 4.1% | 5% | 9% | 17% | 15% |
| PAT | 1 | 1 | 1 | 1 | 4 | 11 | 31 | 38 |

**Shareholding**
- Promoter steady at 66.35%.
- FII went from 0.02% to 0.87% in Sep-26. That is one quarter, not a trend.

**Named cause**
- Optical fibre prices spiked on AI/data-centre demand (forum and industry reports cite about 3x in 18 months) and Q2 revenue doubled YoY.
- The 10-year OPM history shows the same spike in FY19 (16%) during the last fibre boom, followed by a bust to 8%.
- This is a cyclical price spike, not a structural shift.

**Other flags**
- FY26 CFO was ₹-21 cr.
- Debtor days are about 96 and the cash conversion cycle is 124 days.
- The stock is up about 153% YTD.
- Sector peers fell 31% after the October 2026 AI-stock rout.

**Bull case**
- If the H1 run-rate holds, PAT would be about ₹140 cr. At 10x, market cap would be ₹1,400 cr, 1.5x.

**Kill criteria**
- OPM below 10%.
- Fibre spot prices roll over.
- CFO stays negative in H1 FY27.

## Downgraded on verification
**Syncom Formulations (SYNCOMF): 40/100, AVOID for now**
- The numbers fit the pattern well:
  - Six-quarter OPM climb, 12% to 22%.
  - Debt down from 83 to about 0.
  - FII 0.35% to 2.23%.
  - Recomputed P/E 21.7x.
- But no operational cause could be found. There is no new plant. The only cited 2026 capital spend is a ₹57 cr purchase of commercial property in Andheri, a capital-allocation flag.
- Other income is about 27% of PBT. The base is about 4.2 lakh retail holders on a ₹22 stock, and the CFO changed in August 2026.
- Per the skill rule, a margin jump with no identifiable cause is a reason to downgrade.

## Rejected (one line each)
- **Jayaswal Neco**: textbook deleveraging (debt ₹3,845 cr to ₹1,496 cr), but **promoters have pledged 99.9%**. Disqualified.
- **KRBL**: debt down from 545 to 33 and OPM up to 19-21%, but there were governance concerns (a 2024 independent-director resignation and a promoter enforcement case). Market cap ₹9.6k cr is at the ceiling.
- **Manaksia Steels**: OPM step from 5% to 9-11% has no identified cause, and the board approved ₹800 cr of Haldia capex against a ₹760 cr market cap, so funding or dilution risk.
- **Emami Paper**: four-quarter OPM recovery (7% to 16%) at a 5.2x P/E, but debt of ₹933 cr is not falling and paper is cyclical.
- **Sportking India**: only two strong quarters (19-20% OPM), on a cotton-yarn spread. Cyclical.
- **Vardhman Special Steels**: five-quarter OPM step to 10-12%, but the promoter stake fell from 60% to 51% and equity capital rose from 82 to 97 (dilution). Watch.
- **Apcotex**: one 22% OPM quarter, then back to 12%. Lumpy.
- **Antelopus Selan**: strong E&P ramp-up, but reverse-merger dilution (equity 15 to 35) and FII exiting (3.9% to 0.45%).
- **Websol Energy**: margins falling (47% to 35%) on solar-cell oversupply. Opposite pattern.
- **Kernex Microsystems**: Kavach ramp-up, but CFO is negative, debtor days are 268, debt is rising and the promoter holds only 28.7%.
- **Welspun Enterprises**: one lumpy 37% OPM quarter and ₹2,100 cr debt.
- **Rashi Peripherals**: negative CFO and debt doubled.
- **EFC (I)**: equity diluted (10 to 30) and ₹1,386 cr debt.
- **Hariom Pipe, Lumax, Greenply, SSWL**: debt rising (and SSWL's P/E is about 30).
- **Chamanlal Setia**: single 21% OPM quarter on basmati. Watch only.
- **InfoBeans**: margins reverting to the FY22 level rather than a new step, and the promoter is trimming.
- **Madras Fertilizers**: PSU (85% government), 5% OPM.
- **Gokul Agro**: commodity trader at 3% OPM.
- **IMFA**: ferrochrome cyclical and FII holding falling.
- **Taal Tech**: debtor days up from 63 to 96.
- **Amrutanjan**: no growth and DII exiting (12.3% to 6.9%).
- **No inflection, or already well covered:** Fiem, Swaraj Engines, MPS, VRL Logistics, J Kumar, Vimta, Dynamic Cables, Bharat Seats, Pudumjee, Haldyn Glass, Jindal Drilling, R Systems (Blackstone overhang), TIIL (promoter at 74.7%).
- **Excluded as SME, micro-cap, holding company or finance company:** Kalind, Shera, APS, SJ Logistics, Resonance, Dynamic Services, Career Point Edu, SIL Investments, Kama Holdings, UY Fincorp, Unifinz, Nisus, Arman, Indus InvIT, Dolat Algotech.

## Caveats
- Financials and shareholding are from screener.in, an aggregator of exchange filings. I did not re-read the filings myself.
- Cause and Q2 FY27 numbers come from secondary summaries (Multibagg, Univest, Arthneeti, FPJ, SteelOrbis). Confirm against the NSE/BSE filings before any action.
- Pledge status comes from Screener's auto-flag, which only appears when a pledge exists, plus IOL's own FY26 non-encumbrance disclosure. Check the NSE SAST pledge data separately.
