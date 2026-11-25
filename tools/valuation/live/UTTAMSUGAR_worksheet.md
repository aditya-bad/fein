## Valuation worksheet: Uttam Sugar Mills Ltd (integrated sugar, distillery, co-generation; western UP + Uttarakhand) (UTTAMSUGAR) · as of 2026-11-23

*Worksheet v1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 7%, terminal ROIC 9%.*

### Snapshot (TTM Sep-2026 (core: ex exceptional items and other income))
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 348.50 | 1,329 | 460.0 | 1,789 | 14.7 | 8.7 | 13.3 | 7.5% | 5.6% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 348.50 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 5.6% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Revenue CAGR for 10 yrs, margin moving to base-case 5.0% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 5.0%) | none in tested range -30% to 120% (the price is outside what this path can produce) |
| NOPAT margin needed by year 10 on the base-case growth path (6.0% → 5.0%) | **20.0%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 6.5% |
| ROIIC the price implies on the base-case growth and margin path | none in tested range 1% to 300% (the price is outside what this path can produce) |
| Expected return (IRR) the price offers if the base case happens | **7.5%** (vs cost of equity 12.5%) |

Reinvestment realism (v1.3): last-5y incremental ROIC **5.6%** (given). Flag when a ROIIC used or implied differs by more than 5%:

| ROIIC | Value | Gap vs history | Flag |
|---|---|---|---|
| default ROIIC (input) | 7.0% | +1.4 pts | ok |
| scenario bear | 4.0% | -1.6 pts | ok |
| scenario base | 7.0% | +1.4 pts | ok |
| scenario bull | 12.0% | +6.4 pts | **FLAG** |
| implied by price on the base-case path | none in tested range 1-300% | n/a | ok |

> **Reinvestment-realism flag:** scenario bull. Either the business will earn on new capital what it has not earned recently, or the path is mis-specified (e.g. pricing-led growth that needs little capital). Say which in the deep dive.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 30% | 3.0% → 4.0% | 3.5% | 4% | -43.9 | -113% | -1.2% | 6.0 | 0.2 | 0.38x |
| base | 45% | 6.0% → 5.0% | 5.0% | 7% | 11.8 | -97% | 6.1% | 9.0 | 3.5 | 0.81x |
| bull | 15% | 9.0% → 6.0% | 6.5% | 12% | 118.3 | -66% | 12.7% | 13.0 | 6.9 | 1.58x |
| blow-up | 10% | — | — | — | 104.5 | -70% | — | — | — | 0.30x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 20.3 | -94% | -113% | 100% |

> **DCF value below net debt — EV above 1x is an exit-multiple bet (L21, L44)** (bear). The DCF of the operating business (PV of FCF + terminal value + other income + non-operating assets) is less than net debt of 460.0 INR cr, so equity DCF ≤ 0 and the negative DCF values above are this, not a bug or missing data. Any 5-year multiple above 1x rests on the exit P/E, not on cash flows at this cost of equity.

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.40, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 5% | 1% | 0% | 38% | 10% | 0.74x | -5.8% | 0.64x | 1.76x |

> **Exit-multiple gap:** in bear, base, bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

**Exit-multiple bet (v1.3, L21).** The 5-year multiple is a bet on the P/E the market pays in year 5. Own median P/E: 8.0 (n=10).

| Scenario | Exit P/E used | DCF-consistent P/E yr5 | Own median P/E | Used ÷ DCF | Used ÷ own | 5-yr multiple at used | at DCF P/E | at own median |
|---|---|---|---|---|---|---|---|---|
| bear | 6.0 | 0.2 | 8.0 | 24.97x | 0.75x | 0.38x | 0.02x | 0.50x |
| base | 9.0 | 3.5 | 8.0 | 2.58x | 1.12x | 0.81x | 0.32x | 0.72x |
| bull | 13.0 | 6.9 | 8.0 | 1.88x | 1.62x | 1.58x | 0.85x | 0.98x |
| **EV (incl. blow-up)** | | | | | | **0.74x** | **0.31x** | **0.65x** |

Hurdle 1.76x. The card's gate uses the stated exit; the other two columns show how much of the answer is the multiple bet.

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 15.2 on EPS 22.88. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 7.6 | exit P/E 8.0 | exit P/E 11.4 | exit P/E 15.2 | exit P/E 15.5 |
|---|---|---|---|---|---|
| 2x | 32% (r -100%) | 31% (r -93%) | 22% (r -42%) | 15% (r -0%) | 14% (r 3%) |
| 3x | 43% (r -63%) | 42% (r -59%) | 32% (r -26%) | 25% (r -0%) | 24% (r 2%) |
| 5x | 59% (r -43%) | 57% (r -40%) | 46% (r -18%) | 38% (r -0%) | 37% (r 1%) |

Track record for comparison: EPS CAGR -0.6% EPS FY17 27.95 -> FY26 26.30 [SCR] = -0.6%/yr over 9 years (cycle-to-cycle), while revenue went 1,085 -> 2,202 (+8.2%/yr) and March invested capital ~1.8x.

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=10) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 14.7 | 1.84x | HOT | 90% | 0.95x | NORMAL |
| normalised EPS | 15.2 | 1.90x | HOT | 90% | 0.98x | NORMAL |

Own P/E history: FY17 3.7, FY18 22.0, FY19 8.9, FY20 3.8, FY21 5.8, FY22 6.1, FY23 7.1, FY24 9.0, FY25 11.2, FY26 9.5 (median 8.0).
Sector P/Es: Balrampur Chini 31.3, Triveni Engineering 15.5, Dhampur Sugar 11.4 (median 15.5).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 120 (-66%) | 99 (-72%) | 73 (-79%) | 30 (-92%) | -25 (-107%) |
| 11.5% | 90 (-74%) | 66 (-81%) | 37 (-89%) | -11 (-103%) | -71 (-120%) |
| 12.5% | 68 (-80%) | 43 (-88%) | 12 (-97%) | -39 (-111%) | -102 (-129%) |
| 13.5% | 52 (-85%) | 25 (-93%) | -7 (-102%) | -60 (-117%) | -124 (-136%) |
| 14.5% | 38 (-89%) | 10 (-97%) | -22 (-106%) | -75 (-122%) | -140 (-140%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 3.0% | 4.0% | 5.0% | 6.0% | 7.0% |
|---|---|---|---|---|---|
| 4.0% | -28 (-108%) | -4 (-101%) | 20 (-94%) | 44 (-87%) | 68 (-80%) |
| 5.0% | -33 (-110%) | -11 (-103%) | 12 (-97%) | 34 (-90%) | 57 (-84%) |
| 6.0% | -40 (-111%) | -20 (-106%) | 0 (-100%) | 21 (-94%) | 41 (-88%) |

### Input notes
- Price Rs 348.50 = NSE bhavcopy close 23-Nov-2026 (sec_bhavdata_full_24112026.csv, DATE1 23-Nov-2026) = Yahoo v8 UTTAMSUGAR.NS close 23-Nov-2026 (two sources). screener.in 25-Nov-2026 Rs 350 / mcap Rs 1,337 cr. Shares 3.8138 cr (38,138,120; universe.csv = AR26 note = AGM 2026 voting results).
- Net debt 460 [EST] = average of the last four half-year balance sheets because debt is seasonal (sugar inventory financed by cash-credit): Mar-2025 832.75 - 4.80 = 828.0; Sep-2025 276.84 - 13.16 = 263.7; Mar-2026 721.75 - 9.22 = 712.5; Sep-2026 71.79 - 37.40 - 4.03 = 30.4 [consolidated XBRL each date; Mar-2026 and Sep-2026 = screener borrowings 722 / 72]. Using the Sep-2026 trough (30) would overstate equity value by ~Rs 110/share; using the Mar peak (712) understates it.
- treasury_income_post_tax -28.6 = TTM finance cost 38.1 (6.28 + 13.01 + 13.32 + 5.48, XBRL = screener) x (1 - 0.25); FY26 finance cost was 51.84 on a bigger crop, so TTM interest is flattered by the small 2025-26 crush.
- Base = TTM Q3FY26..Q2FY27 [XBRL = screener every quarter]: revenue 521.24 + 470.10 + 606.37 + 494.00 = 2,091.7; operating profit 57.43 + 98.43 + 26.19 + 22.63 = 204.7; D&A 12.51 + 12.29 + 12.48 + 12.50 = 49.8 -> EBIT ex other income 154.9. Reported PAT 90.9 / EPS 23.72 (14.7x). Other income TTM 6.7 (5% of PBT) and exceptional -1.35 (labour-code impact, Q4 FY26): L44 core EPS (154.9 x 0.75 - 28.6) / 3.8138 = 22.97 -> 15.2x; second route (PBT 122.1 + 1.35 - 6.7) x 0.748 / 3.8138 = 22.9. Core ~= reported here (unlike SHK).
- eps_normalised 22.88 = mean EPS FY17-26 (27.95, 4.46, 15.24, 13.54, 15.67, 35.38, 32.41, 34.67, 23.16, 26.30) [SCR; FY17-23 standalone, FY24-26 consolidated with 83.7%-owned UDL, small]. 15.2x. No buybacks/issues (38,138,120 shares throughout).
- ROIC/ROIIC (L42, group first; full-cycle windows both containing a peak and a trough year): FY17-19 avg EBIT ex OI 144 on avg March IC 927 (equity + borrowings) -> 15.5% pre-tax, 11.6% after 25% tax; FY24-26 avg EBIT 191 on avg March IC 1,559 -> 12.2% / 9.2%; ROIIC = (191-144) x 0.75 / (1,559-927) = 5.6%. TTM ROIC on seasonal-average IC (equity 887 + avg net debt ~460 = ~1,300): 154.9 x 0.75 / 1,300 = 8.9%; on March IC 7.3%; on the Sep trough IC 12.7%. Segment pre-tax returns FY26 on average segment assets (Mar-25/Sep-25/Mar-26): sugar ~13%, distillery ~12%, cogen ~30% - but internal molasses/bagasse transfer prices decide the split (inter-segment revenue Rs 489 cr).
- Scenarios (5-yr; written before outputs; tails started from the India 1,000-20,000 cr class 21%/11%/15%): blow-up 10% raw (own history: negative reserves 2015); bear 30% = SAP rises Rs 20-30/qtl/yr for two seasons with MSP frozen and B-heavy ethanol excluded again in ESY 2027-28: growth 3% -> 4%, NOPAT margin 3.5%, ROIIC 4%, exit 6x (FY20-21 P/Es 3.8-5.8); base 45% = crush recovers to ~3.6-3.9 mt, SAP drift offset by sugar prices, ethanol partly via C-heavy/grain at UDL: +6% -> +5%, 5.0% (TTM 5.5%, FY26 6.1%), ROIIC 7%, exit 9x (FY22-26 median 9.0x; 10-yr median 8.0x); bull 15% = MSP raised to ~Rs 38-41/kg (ISMA ask), B-heavy restored, UDL 160 KLPD full: +9% -> +6%, 6.5%, ROIIC 12%, exit 13x (between Triveni 15.5x and own FY25 11.2x).
- Exit P/Es: own FY-end P/Es FY17-26 (FY-end close / that FY's EPS) 3.7/22.0/8.9/3.8/5.8/6.1/7.1/9.0/11.2/9.5, median 8.0. Peers [SCR 25-Nov-2026]: Balrampur Chini 31.3 (depressed earnings + PLA project optionality), Triveni Engineering 15.5 (engineering segment), Dhampur Sugar 11.4. The current 15.2x on TTM/normalised EPS is the top of the own range except FY18 (a trough-EPS year).
- Tax 25%: standalone effective 25-27% FY24-26 [SCR]; the company is on the new regime (deferred tax only).
- FCF 100 [EST]: FY22-26 FCF 289/108/-91/55/213 (avg 115) [SCR]; FY27 capex includes UDL 40 -> 160 KLPD (Rs 110 cr by Mar-2027, Reg-30 29-Sep-2025) and the corporate-office building purchase (25-Sep-2026, amount not disclosed).
- Dispersion 0.40 (price range Rs 18 (2016) -> 522 (2023) -> 178 (2025) -> 389 (2026)).

Sources: research_notes/Deep dives/UTTAMSUGAR_live.md; https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_24082026174953_AR_31032026_Signed.pdf; https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1750793_31102026070927_WEB.xml; https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_31102026184438_Presentation_signed.pdf; https://www.screener.in/company/UTTAMSUGAR/consolidated/; https://nsearchives.nseindia.in/products/content/sec_bhavdata_full_24112026.csv

