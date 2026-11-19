# Theme: AI/data-centre build-out + India power grid — picks-and-shovels

Research date: 2026-11-19. Research, not investment advice. Process: stock-research-analyst skill (5 stages + verification checklist).
All financials are from **screener.in consolidated pages** fetched 2026-11-19 (where the company has no consolidated accounts, screener serves standalone — flagged "(S)"). Prices are from the screener price-chart API (daily close series, last point dated 2026-11-19) and cross-checked against dated third-party quotes from web search. All P/E and market-cap figures are **recomputed** by me as price ÷ TTM EPS (sum of the last 4 quarters) and price × (TTM PAT ÷ TTM EPS) shares. I did not use screener's precomputed ratios, because the top-ratio block came back empty without a login.

---

## Stage 1 — Macro thesis (dated sources)

- **Data centres:** India had about 1.8 GW IT of operational DC stock in H1 2026, after adding 258 MW in H1 2026 (Savills). Forecasts for 2030 are 6–8 GW (Jefferies: 8 GW). Hyperscaler commitments include Google/AdaniConneX Vizag (about $15bn, 2026–30), Microsoft ($17.5bn) and AWS (figures conflict). Each GW of DC load needs EHV substations, transformers, switchgear, gensets, cooling and BESS.
- **Grid:** Peak demand hit a record **270.8 GW on 21 May 2026** (MoP data, via DownToEarth/PolicyCircle). T&D capex is put at about ₹9 trn to 2032 (April 2026 report), and ICRA estimates ₹5.6 trn of transmission capex FY27–32. About 56,000 ckm and 338 GVA were under construction through FY30 (Mercom, June 2026). Transformer lead times are long and pricing has been firm (April 2026 report).
- **Storage:** 100+ GWh of BESS was tendered in 2025 (IESA; counts conflict between 58.7 and 102 GWh). Operational BESS was only about 9 GWh by Aug 2026, so execution is lagging tenders.

**Thesis in one line:** the demand side is real and dated. **But the obvious "shortage" trade (transformer OEMs) is already showing peak-margin behaviour.** Shilchar, Voltamp, Indo Tech and Vilas Transcore have all printed 3–4 consecutive quarters of falling OPM while everyone adds capacity. The less-crowded trade is **transmission EPC and towers**, where order books are 1.8–1.9x revenue and P/Es are 14–24x. Capital goods took 14 years to regain the 2007 peak, so I did not pay 50–80x for anything.

Sources: [Savills via RealtyToday](https://therealtytoday.com/news/market-insights/indias-data-centre-infrastructure-reaches-18-gw-with-rising-global-investments-savills-india-report/), [CXO Digital Pulse 6–8 GW](https://www.cxodigitalpulse.com/?p=64062), [Google Vizag](https://www.pulse.bot/climatetech/news/google-clouds-planned-15-billion-data-centre-in-visakhapatnam-to-have-5-gw-capacity-ca9a7383-3e0d-4c48-955d-a505db15e623/), [270.8 GW peak – DownToEarth](https://www.downtoearth.org.in/amp/story/energy/power-demand-tracker-india-meets-all-time-high-power-demand-of-2708-gw-renewable-energy-share-34), [₹9 trn T&D capex](https://www.ibef.org/news/india-s-power-transmission-sector-to-see-us-96-70-billion-capex-push-by-2032), [ICRA ₹5.6 trn](https://www.energetica-india.net/news/transmission-sector-to-witness-inr-56-trillion-capex-between-202627-and-203132-says-icra), [Mercom build-out](https://mercomindia.com/clean-energy-expansion-spurs-transmission-manufacturing-demand), [BESS tenders – SaurEnergy](https://www.saurenergy.com/solar-energy-news/indias-ess-shift-92-gwh-set-for-commissions-in-2026-after-130-gwh-of-tenders-in-2025-10993901)

---

## Stage 2/4 — Universe screen (31 names fetched; price = 19-Nov-2026 close from screener chart)

Recomputed TTM P/E. "Implied g" comes from a reverse DCF: the 10-yr EPS CAGR the price needs, assuming 12% discount rate, 70% FCF conversion and a terminal P/E of 15.

| Ticker | Segment | Price ₹ | Mcap ₹cr | TTM P/E | Implied g | ROCE FY26 | Note |
|---|---|---|---|---|---|---|---|
| TRANSRAILL | T&D EPC + towers/conductors | 432.25 | 5,802 | 13.9 | 6% | 34% | **Finalist** |
| SKIPPER | Towers / T&D EPC | 487.75 | ~5,955 (diluted) | 24.2 | 13% | 24% | **Finalist** |
| TECHNOE | T&D EPC + DC developer | 929.0 | 10,817 | 22.3 | 12% | 15% | **Finalist (DC angle)** |
| DANISH (SME) | Inverter-duty transformers | 960 | 1,885 | 24.2 | 13% | 22% | Runner-up |
| ORIANA (SME) | Solar/BESS EPC | 193.45 | 1,954 | 7.4 | −2% | 40% | Contrarian watch |
| 515008 Modern Insulators | Porcelain insulators | 560.8 | 2,640 | 20.3 | 11% | 19% | Governance flag |
| INDOTECH | Transformers | 2,454 | 2,613 | 25.9 | 14% | 40% | Pledge flag |
| 531201 Shilchar | Transformers | 3,307 | 3,779 | 30.4 | 16% | 51% | Margin peaking |
| VOLTAMP | Transformers | 9,620 | 9,720 | 30.1 | 16% | 24% | Margin peaking |
| TARIL | Transformers | 304.9 | 9,412 | 30.1 | 16% | 23% | Cash-flow flag |
| ATLANTAELE | Transformers | 1,450 | 11,126 | 49.7 | 23% | 45% | Priced |
| QPOWER | HVDC/grid components | 1,615 | 18,423 | 82.6 | 30% | 32% | Priced |
| MARINE | DC/marine switchboards | 423.6 | 5,977 | 74.7 | 28% | 18% | Priced |
| KRN | HVAC heat exchangers | 986 | 6,315 | 54.9 | 24% | 16% | Priced |
| KIRLOSENG | Gensets | 1,726 | 24,654 | 48.7 | 23% | 15% | Priced, above band |
| APARINDS | Conductors/cables | 14,373 | 58,505 | 42.5 | 21% | 32% | First-order, priced |
| GVT&D | T&D OEM | 4,326 | 1.04 lakh | n.m. | — | — | First-order, priced |
| KPIL | T&D EPC | 1,320 | 22,494 | 19.0 | 10% | 18% | Above band |
| GENUSPOWER | Smart meters | 266.7 | 8,112 | 12.2 | — | 25% | Cash-burn flag |
| others | see rejects | | | | | | |

---

## Finalist 1 — Skipper Ltd (NSE: SKIPPER) — conviction 66/100 — **BUY-ZONE (staggered; strongest near ₹470 preferential price)**

**Verified price block:** ₹487.75 close 19-Nov-2026 (screener chart).
- The screener series matches independent quotes exactly: ₹473.90 on 23-Oct (Kotak Neo ₹473.9), ₹507.90 on 27-Oct (Investing.com 507.90) and ₹526.55 on 5-Nov (Upstox ₹525.40 at 15:29 IST, an intraday snapshot).
- No independent quote dated 19-Nov was found, so the latest price is single-sourced but series-validated.
- Share count rose in July 2026: 92.23 lakh shares were issued preferentially at ₹470 to non-promoter institutions (Bandhan Small Cap, Emerge PO Trust, Cohesion MK). Q2 EPS 4.75 on PAT ₹58 cr implies about 12.2 cr shares.
- **Diluted mcap ≈ ₹5,955 cr. TTM P/E = 487.75 / 21.37 ≈ 22.8x on reported TTM EPS, or ≈ 24.2x on the post-issue share count.** I use 24x.

| ₹ cr | FY22 | FY23 | FY24 | FY25 | FY26 | TTM |
|---|---|---|---|---|---|---|
| Sales | 1,707 | 1,980 | 3,282 | 4,624 | 5,553 | 5,731 |
| OPM | 10% | 10% | 10% | 10% | 10% | 10% |
| PAT | 25 | 36 | 82 | 149 | 213 | 246 |
| ROCE | 10% | 12% | 21% | 24% | 24% | — |
| Borrowings | 575 | 494 | 592 | 711 | 931 | 757 (Sep-26) |
| CFO | 17 | 284 | 199 | 153 | 277 | — |
| Debtor days | 93 | 66 | 85 | 55 | 98 | — |

| Quarter | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|
| Sales | 1,262 | 1,371 | 1,667 | 1,310 | 1,384 |
| OPM | 10% | 10% | 10% | 11% | 10% |
| PAT | 37 | 53 | 78 | 57 | 58 |

No loss quarter. PAT grew YoY in every one of the last 8 quarters; Q2 FY27 PAT was +57% YoY.

**Shareholding (Sep-24 → Sep-26):**
- Promoter 66.48% → 61.48%. The fall is fully explained by the preferential allotment; no promoter selling.
- FII 4.39% → 10.31%.
- DII 0.24% → 2.41%.
- Institutions are rising. No promoter pledge was found (no-encumbrance declaration as of Mar-26).

**Structural story (named cause):** OPM is flat at 10%, so this is **not** a margin step-change. The step-change is in **ROCE (9–12% → 21–24%) and PAT (₹25 cr → ₹246 cr)**. It came from operating leverage on a tower/monopole plant whose utilisation jumped as PGCIL/ISTS EPC orders arrived. Specifically:
- Record order book of **₹10,066 cr (1.76x TTM revenue)** at Sep-26.
- Record Q2 inflow of ₹2,111 cr (+70% YoY), including ₹1,054 cr exports.
- A 75,000 MTPA capacity expansion is underway.
- The ₹433.5 cr equity raise paid down debt (₹327.5 cr earmarked; borrowings ₹931 → ₹757 cr).

**Bull case (numbers):** FY27–29 PAT CAGR of 25%, slightly below the company's ~30% FY27 guide, takes PAT to about ₹420 cr by FY29. At 20x that is about ₹8,400 cr mcap, roughly 1.4x from here in about 2.5 yrs. At 25x with 30% CAGR it is about 2x. Multibagger only if exports and the new EPC arm (Evergrid India, incorporated 4-Nov-26) lift OPM above 11%.

**Risks:**
- Margin ceiling of 10% (steel pass-through). EPC margins are thin.
- Debtor days 55 → 98 in FY26.
- History of single-digit ROCE (FY20–22). This is a cyclical business, not a franchise.
- Polymer-pipes segment is a distraction.

**Kill criteria:**
- Two consecutive quarters of YoY PAT decline.
- Order book below ₹8,000 cr.
- Debtor days above 120.
- Borrowings back above ₹1,000 cr without a matching order-book rise.
- Any promoter pledge.

---

## Finalist 2 — Transrail Lighting (NSE: TRANSRAILL) — conviction 62/100 — **BUY-ZONE (value), conditional on H2 FY27 order inflow**

**Verified price block:** ₹432.25 close 19-Nov-2026 (screener chart).
- Second source: Value Research ₹439.60 NSE on 16-Nov-2026, which equals the screener 16-Nov close of ₹439.60 exactly.
- Upstox ₹431.40 on 2-Nov (10:52 IST) vs screener close ₹434.65: consistent.
- **Discrepancy:** Kotak Neo ₹450.8 on 21-Oct vs screener ₹468.80 (−4%). Kotak may be using a stale or intraday value. I use the screener close.
- Shares ≈ 13.42 cr (TTM PAT 418 / TTM EPS 31.14). **Mcap ≈ ₹5,802 cr. TTM P/E = 13.9x.**

| ₹ cr | FY22 | FY23 | FY24 | FY25 | FY26 | TTM |
|---|---|---|---|---|---|---|
| Sales | 2,338 | 3,152 | 4,077 | 5,308 | 6,880 | 7,452 |
| OPM | 11% | 12% | 14% | 15% | 14% | 12% |
| PAT | 65 | 108 | 233 | 329 | 404 | 418 |
| ROCE | 22% | 27% | 35% | 35% | 34% | — |
| Borrowings | 469 | 621 | 667 | 661 | 678 | 766 (Sep-26) |
| CFO | 46 | 143 | 35 | 287 | 643 | — |
| Debtor days | 100 | 75 | 92 | 91 | 92 | — |

| Quarter | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|
| Sales | 1,561 | 1,796 | 1,863 | 1,736 | 2,056 |
| OPM | 12% | 13% | 11% | 12% | 12% |
| PAT | 92 | 110 | 96 | 108 | 104 |

**The annual figure hides a stall.** Revenue grew +32% YoY in Q2, but TTM PAT (₹418 cr) is only +3.5% over FY26 (₹404 cr). Mar-26 PAT was −24% YoY (₹127 cr → ₹96 cr). Q2 FY27 PAT was +12% and was hit by a one-time tax charge and higher interest. OPM has slid from 15% to 12%.

**Shareholding (Dec-24 → Sep-26):**
- Promoter flat at 71.12%. Zero pledge (Ajanma Holdings no-encumbrance declaration, Apr-26).
- DII 15.15% → 5.95% (IPO anchors exiting, a persistent overhang).
- FII 1.0% → 1.85%.
- Institutional direction is **down**.

**Structural story (named cause):**
- Vertically integrated T&D EPC: it makes its own towers, conductors and poles. That is why ROCE (34%) is about double peers like KPIL (18%).
- Customer advances give a negative cash-conversion cycle (about −147 days).
- FY26 CFO of ₹643 cr was 1.6x PAT.
- Order book ₹14,218 cr (1.9x TTM revenue), 93% T&D. The stock has de-rated from ₹632 (Nov-25) to ₹432.

**Bull case:** The price implies only about 6% 10-yr EPS growth for a business growing revenue 30%. If OPM holds at 12% and revenue grows 20% for 3 years, PAT is about ₹700 cr. At 16x that is about ₹11,200 cr, roughly 1.9x. The FY27 inflow guide is above ₹10,000 cr, and October-26 inflow was ₹1,747 cr.

**Risks (blunt):**
- H1 FY27 inflow was only ₹1,638 cr against about ₹3,800 cr executed. **The order book is shrinking** (about ₹16.4k cr → ₹14.2k cr).
- Interest cost is rising and OPM is compressing.
- The DII exit is ongoing.
- There is a related-party acquisition from the promoter (Gactel, ₹10 cr; small) and a Deputy MD resignation.

**Kill criteria:**
- FY27 order inflow below ₹7,000 cr.
- Order book below ₹12,000 cr at Mar-27.
- OPM below 11% for 2 quarters.
- FY27 CFO below PAT.

---

## Finalist 3 — Techno Electric & Engineering (NSE: TECHNOE) — conviction 50/100 — **WATCHLIST**

**Verified price block:** ₹929.00 close 19-Nov-2026 (screener chart).
- Second sources match the screener series exactly: Upstox ₹850.10 close on 3-Nov and 5paisa ₹928.50 on 6-Nov.
- **Discrepancy:** a 5paisa page from about 13-Nov shows mcap ₹11,817 cr and P/E 24.3. My recompute is lower because I use 11.64 cr shares (₹23 cr equity at FV ₹2 ≈ 11.5–11.6 cr) and TTM EPS 41.74. That gives **mcap ₹10,817 cr and P/E 22.3x**.
- **Ex-other income, the P/E is about 27x.** TTM other income is ₹121 cr out of about ₹600 cr PBT.

| ₹ cr | FY22 | FY23 | FY24 | FY25 | FY26 | TTM |
|---|---|---|---|---|---|---|
| Sales | 999 | 830 | 1,502 | 2,269 | 3,252 | 3,620 |
| OPM | 16% | 11% | 14% | 15% | 14% | 15% |
| Other income | 175 | 165 | 134 | 205 | 175 | 121 |
| PAT | 264 | 187 | 268 | 423 | 474 | 486 |
| ROCE | 18% | 8% | 17% | 17% | 15% | — |
| CFO | 259 | 93 | −198 | 453 | **−590** | — |
| Debtor days | 213 | 282 | 180 | 108 | 137 | — |

| Quarter | Sep25 | Dec25 | Mar26 | Jun26 | Sep26 |
|---|---|---|---|---|---|
| Sales | 843 | 872 | 1,010 | 630 | 1,108 |
| OPM | 13% | 14% | 13% | 16% | 16% |
| PAT | 104 | 119 | 115 | 93 | 158 |

Lumpy, with no loss quarter. Q2 FY27 core EBITDA was +63%, which is real operating improvement.

**Shareholding (Mar-24 → Sep-26):**
- Promoter 61.52% → 56.93%. This is QIP dilution of ₹1,250 cr in Sep-24, not promoter selling.
- FII 3.85% → 9.8% → 8.09%, drifting down.
- DII 23.76% → 21.33%, drifting down.
- Pledge not verified (no data found).

**Story:** This is the only listed small/mid-cap where the DC build-out is in the P&L thesis. But the data centres are **barely visible in earnings**:
- Gurgaon edge DC is live, with RailTel using about 50%.
- Chennai is 35–40 MW (sources conflict), and contracted capacity is cited as low as 0.5 MW.
- A 2 MW Andhra Pradesh DC is due H1 FY28.

The QIP cash is going into data centres and TBCB transmission assets, which are regulated-return and low-ROCE. That pulled ROCE down to 15% and FY26 CFO to −₹590 cr. Order book is about ₹10,000–11,000 cr, about 3x revenue (sources conflict). The stock is down about 34% in 6 months.

**Bull case:** FY27 revenue guide of ₹4,000 cr. EPC OPM at 15–16%. A Chennai lease-up to 35+ MW at about ₹8–10 cr/MW/yr would add ₹300 cr+ of annuity revenue at high EBITDA by FY29. That would justify a re-rate to about 30x core earnings, roughly 1.6–1.8x.

**Why not BUY:**
- ROCE is below the 15% hurdle.
- Two of the last three years had negative CFO.
- Other income is propping up PAT.
- The DC monetisation is unproven.
- The order-book and Chennai MW figures are inconsistent across sources.

**Kill criteria:**
- FY27 CFO negative again.
- No Chennai hyperscaler contract by FY27 end.
- Debtor days above 180.

**Upgrade trigger:** a signed 20+ MW hyperscale lease plus positive CFO.

---

## Rejected / downgraded (one-liners)

- **Indo Tech Transformers (2,454):** ROCE 40%, P/E 26. But on 12-Nov-2026 the promoter SSEL pledged **57.93% of total equity** for a USD 66m loan, after selling shares in June–July 2026. Q2 PAT was only +5% with OPM down to 13%. Fails governance. **AVOID.**
- **Modern Insulators (BSE 515008):** a genuine OPM step-up (5–8% → 16–22%) and P/E 20. But FY26 and Q2 FY27 audits are **qualified**: tax is unprovided pending the Modern Denim amalgamation. Q2 PAT includes ₹23 cr other income, inventory days are about 290, and the stock is up 3.2x in 12 months. **WATCHLIST** until NCLT approves and tax is provided.
- **Shilchar (531201):** best-in-class history (ROCE 51–75%). But OPM fell 31% → 21% → 16% → 21% over the last 3 quarters, Q2 PAT was −28% YoY, and exports are down. TTM P/E is about 30, not the ~24 that FY26 EPS suggests. **Peak-margin signal.** WATCHLIST.
- **Voltamp:** OPM 20% → 15%, FY26 PAT −6%, promoter stake 38% → 30% (Sep-25), P/E 30. Peaking.
- **TARIL:** P/E 30, FY26 CFO −₹105 cr vs PAT ₹272 cr, DII 7.7% → 1.2%, borrowings rising.
- **Atlanta Electricals:** P/E about 50 (implies 23% for 10 yrs); 87% promoter, thin float. Priced.
- **Quality Power:** P/E about 83 (implies 30%). Priced.
- **Marine Electricals:** P/E about 75, debtor days 178. Priced.
- **KRN Heat Exchanger:** P/E about 55, FY26 CFO −₹114 cr, debt up.
- **Kirloskar Oil Engines:** mcap ₹24.7k cr is above the band, P/E 49, ₹5.6k cr borrowings via its NBFC arm.
- **Genus Power:** P/E about 12 looks cheap. But CFO has been negative 3 years running (−152/−443/−219), borrowings are ₹2,482 cr, and FIIs went 18.7% → 7.4% in the Sep-26 quarter. **AVOID.**
- **Oriana Power (SME):** P/E 7.4 after a −64% fall (prices adjusted for the 1:5 split on 18-Sep-26). Receivables are ₹935 cr against H1 revenue of ₹1,000 cr, D/E went 0.49 → 0.80, and it is diversifying into green ammonia/CBG. The −26% move over 16–18 Nov is unexplained. Contrarian WATCHLIST only.
- **Danish Power (SME):** runner-up. P/E 24, ROCE 22%, FY27 revenue guided above ₹700 cr. But the order book is only about ₹600 cr (about 1x revenue), DII went 9.6% → 4.3%, it reports half-yearly, and liquidity is low. WATCHLIST.
- **Vilas Transcore (SME, CRGO cores):** the only CRGO-adjacent name found. OPM 14% → 10%, FY26 CFO −₹42 cr. Watch.
- **Precision Wires:** the consolidated page is stale (2015 data), so I used standalone. P/E about 38 on 5% OPM, and borrowings jumped from ₹293 cr to ₹1,475 cr in Sep-26 (cause unverified).
- **Ram Ratna Wires:** OPM about 5%, P/E 34, debt more than doubled to ₹756 cr.
- **Universal Cables:** ROCE 12%, debt ₹1,473 cr and rising.
- **Salzer:** ROCE 11%, OPM 11% → 7%, debt rising.
- **HPL Electric:** ROCE 13%, debtor days 154.
- **Diamond Power:** P/E 73, ROCE 12%.
- **Hind Rectifiers:** P/E about 89, OPM 5%.
- **Prostarm:** OPM 17% → 8%, debtor days 241, CFO negative.
- **Bajel:** P/E 75, ROCE 11%.
- **Bharat Bijlee:** ROCE 8%.
- **Jyoti Structures:** ROCE 2%, ₹2,175 cr borrowings.
- **Apar, GE Vernova T&D:** first-order and priced (P/E 42 and n.m.).
- **KPIL:** quality is fine at P/E 19 but mcap ₹22.5k cr is above the band.

## Key takeaway

The transformer shortage is turning into a capacity glut on the margin line before the revenue line. Watch OPM, not order books. The value in this theme today is in **transmission EPC and towers** (Skipper, Transrail), at 14–24x with 1.8–1.9x order cover. Pure data-centre exposure in small caps is either priced (Marine, KRN, QPOWER at 55–83x) or not yet showing up in earnings (Techno).

## Gaps / not verified
- No independent quote dated exactly 19-Nov for the finalists. The screener series was validated against dated quotes on 4–6 other days.
- Techno's pledge status and the Precision Wires debt cause are unverified.
- Order-book figures come from secondary aggregators, not exchange filings.

Raw data: /tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/power_dc/raw/ ; scripts: /tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/scripts_power/
