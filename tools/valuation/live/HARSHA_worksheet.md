## Valuation worksheet: Harsha Engineers International Ltd (precision bearing cages, bushings, stampings; solar EPC) (HARSHA) · as of 2026-11-23

*Worksheet v1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 14%, terminal ROIC 13%.*

### Snapshot (TTM Sep-2026)
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 438.25 | 3,990 | -95.0 | 3,895 | 24.4 | 14.3 | 66.5 | 1.5% | 9.0% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 438.25 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 9.0% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Revenue CAGR for 10 yrs, margin moving to base-case 9.5% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 9.5%) | none in tested range -30% to 120% (the price is outside what this path can produce) |
| NOPAT margin needed by year 10 on the base-case growth path (12.0% → 9.0%) | **24.5%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 10.8% |
| ROIIC the price implies on the base-case growth and margin path | none in tested range 1% to 300% (the price is outside what this path can produce) |
| Expected return (IRR) the price offers if the base case happens | **8.7%** (vs cost of equity 12.5%) |

Reinvestment realism (v1.3): last-5y incremental ROIC **11.0%** (given). Flag when a ROIIC used or implied differs by more than 5%:

| ROIIC | Value | Gap vs history | Flag |
|---|---|---|---|
| default ROIIC (input) | 14.0% | +3.0 pts | ok |
| scenario bear | 8.0% | -3.0 pts | ok |
| scenario base | 14.0% | +3.0 pts | ok |
| scenario bull | 20.0% | +9.0 pts | **FLAG** |
| implied by price on the base-case path | none in tested range 1-300% | n/a | ok |

> **Reinvestment-realism flag:** scenario bull. Either the business will earn on new capital what it has not earned recently, or the path is mis-specified (e.g. pricing-led growth that needs little capital). Say which in the deep dive.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 25% | 3.0% → 6.0% | 7.0% | 8% | 115.9 | -74% | 1.1% | 15.0 | 9.2 | 0.68x |
| base | 50% | 12.0% → 9.0% | 9.5% | 14% | 185.9 | -58% | 10.6% | 24.0 | 10.6 | 1.64x |
| bull | 20% | 17.0% → 12.0% | 11.5% | 20% | 307.7 | -30% | 17.0% | 32.0 | 13.5 | 2.89x |
| blow-up | 5% | — | — | — | 131.5 | -70% | — | — | — | 0.30x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 190.0 | -57% | -74% | 100% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.30, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 30% | 10% | 1% | 9% | 5% | 1.58x | 9.6% | 1.51x | 1.76x |

> **Exit-multiple gap:** in bear, base, bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

**Exit-multiple bet (v1.3, L21).** The 5-year multiple is a bet on the P/E the market pays in year 5. Own median P/E: n/a (n=4 < 5).

| Scenario | Exit P/E used | DCF-consistent P/E yr5 | Own median P/E | Used ÷ DCF | Used ÷ own | 5-yr multiple at used | at DCF P/E | at own median |
|---|---|---|---|---|---|---|---|---|
| bear | 15.0 | 9.2 | n/a | 1.64x | n/a | 0.68x | 0.42x | n/a |
| base | 24.0 | 10.6 | n/a | 2.26x | n/a | 1.64x | 0.73x | n/a |
| bull | 32.0 | 13.5 | n/a | 2.37x | n/a | 2.89x | 1.23x | n/a |
| **EV (incl. blow-up)** | | | | | | **1.58x** | **0.73x** | **n/a** |

Hurdle 1.76x. The card's gate uses the stated exit; the other two columns show how much of the answer is the multiple bet.

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 43.8 on EPS 10.00. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 21.9 | exit P/E 32.9 | exit P/E 43.8 | exit P/E 44.0 |
|---|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -41%) | 15% (r -0%) | 15% (r 1%) |
| 3x | 43% (r -63%) | 32% (r -26%) | 25% (r -0%) | 24% (r 0%) |
| 5x | 59% (r -43%) | 46% (r -18%) | 38% (r -0%) | 38% (r 0%) |

Track record for comparison: EPS CAGR 13.9% Consolidated PAT FY22 92 -> FY26 155 = 13.9%/yr [SCR]; FY23-25 fell 123 -> 89 (European industrial slowdown + Romania impairment) before recovering; EPS CAGR from FY20 (2.84) is distorted by the 2022 IPO share issue.

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=4) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 24.4 | n/a | INSUFFICIENT HISTORY (n=4 < 5) | n/a | 0.55x | COLD |
| normalised EPS | 43.8 | n/a | INSUFFICIENT HISTORY (n=4 < 5) | n/a | 1.00x | NORMAL |

Own P/E history: FY23 24.7, FY24 32.8, FY25 37.9, FY26 18.4 (median 28.8).
Sector P/Es: Rolex Rings 22.1, NRB Bearings 28.2, Schaeffler India 43.4, SKF India 44.6, Timken India 50.5, Sansera Engineering 70.2 (median 44.0).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 237 (-46%) | 255 (-42%) | 275 (-37%) | 298 (-32%) | 322 (-26%) |
| 11.5% | 201 (-54%) | 212 (-52%) | 223 (-49%) | 236 (-46%) | 248 (-43%) |
| 12.5% | 174 (-60%) | 180 (-59%) | 186 (-58%) | 191 (-56%) | 196 (-55%) |
| 13.5% | 154 (-65%) | 156 (-64%) | 158 (-64%) | 159 (-64%) | 158 (-64%) |
| 14.5% | 138 (-68%) | 138 (-69%) | 136 (-69%) | 134 (-70%) | 129 (-71%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 7.5% | 8.5% | 9.5% | 10.5% | 11.5% |
|---|---|---|---|---|---|
| 4.0% | 150 (-66%) | 167 (-62%) | 184 (-58%) | 200 (-54%) | 217 (-51%) |
| 5.0% | 152 (-65%) | 169 (-61%) | 186 (-58%) | 203 (-54%) | 220 (-50%) |
| 6.0% | 154 (-65%) | 171 (-61%) | 188 (-57%) | 206 (-53%) | 223 (-49%) |

### Input notes
- Price Rs 438.25 = NSE bhavcopy close 23-Nov-2026 (the 24-Nov file carries 23-Nov data; 24-Nov was not a trading day) = Yahoo v8 close 23-Nov-2026 (two sources). screener.in 25-Nov-2026 intraday Rs 441 / mcap Rs 4,016 cr. Shares 9.1044 cr (universe.csv; equity capital Rs 91 cr at FV 10).
- Net cash ~95 at 30-Sep-2026 [Q2FY27 consolidated XBRL]: cash 22.13 + other bank 21.78 + current investments 265.51 + non-current investments 224.04 = 533.5, less borrowings 222.67 + 215.81 = 438.5. Leases not material. Gross borrowing while holding ~Rs 490 cr of investments; management says the debt is 'backed by either lower interest rate or ... government subsidy' (Q2 FY27 call) - terms not disclosed in AR26.
- Treasury income post-tax 22 [EST]: TTM other income 30 x 0.73.
- Base = TTM Q3FY26..Q2FY27 [XBRL + SCR agree]: revenue 409.25 + 473.91 + 457.43 + 440.09 = 1,780.7; operating profit (ex other income) 57+73+67+75 = 272; D&A 53 -> EBIT 220; PAT 163.2; EPS 17.94.
- FCF 60 [EST]: CFO FY23-26 137/136/206/68 (avg 137) less maintenance capex 25-30 (Q2 FY27 call) and part of growth capex; reported FCF FY23-26 63/62/-2/-47 [SCR].
- eps_normalised 10.0 = mean consolidated PAT FY20-26 (22,45,92,123,111,89,155 = 91.0) / today's 9.104 cr shares; 43.8x on it. Not a classic cyclical: FY21 COVID revenue only -1%; the FY23-25 EPS dip (-28%) was a European industrial slowdown + Romania; protocol v1.4 rule applied because the business is industrial-cyclical, not because it screens cheap (it does not: 24.4x vs own median 28.8x and peer median 44x).
- ROIIC: invested capital ex cash ~1,391 (equity 1,486 + debt 438 - liquid 533); NOPAT 220 x 0.73 = 160 -> ROIC ~11.5%. FY23->TTM: dNOPAT ~+46 on d(IC) ~+390 -> ROIIC ~11% [EST]; incremental_roic_5y 0.11. Management claims ~2x asset turn on productive capex (Q2 FY27 call) and Advantek runs at ~54% utilisation (Reg-30 28-May-2026); base roiic 0.14 assumes utilisation improves; terminal 0.13.
- Scenarios (5-yr; written before outputs): blow-up 5% (raw; anchored to class later); bear 25% = European/industrial slowdown + customer in-sourcing, Romania closure, Advantek under-utilised: revenue +3%/yr, NOPAT margin 7%, exit 15x; base 50% = guidance roughly met (FY27 cons +10-12%, India mid-high teens), outsourcing contracts ramp with slips: +12% -> +9%, NOPAT margin 9.5%, exit 24x (~own FY23/FY26 average); bull 20% = outsourcing wave (bushings Rs 300 cr, stampings Rs 300 cr in 3-4 yrs per management) + Romania fixed: +17% -> +12%, 11.5%, exit 32x (below bearing-maker peers 43-50x).
- Exit P/Es: own FY-end P/Es only exist for FY23-26 (listed 26-Sep-2022): 24.7/32.8/37.9/18.4, median 28.8. Closest peer by position in the chain (bearing-component supplier to the same customers) is Rolex Rings at 22.1x; bearing makers (customers with brands) 43-50x.
- Dispersion 0.30.

Sources: research_notes/Deep dives/HARSHA_live.md; https://nsearchives.nseindia.in/annual_reports/AR_29478_HARSHA_2025_2026_A_15877505_29062026151738.pdf; https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1751817_03112026042536_WEB.xml; https://nsearchives.nseindia.in/corporate/Harsha_06112026142552_Transcript_of_Earning_Call_Q2FY2027.pdf; https://www.screener.in/company/HARSHA/consolidated/; https://nsearchives.nseindia.in/products/content/sec_bhavdata_full_24112026.csv

