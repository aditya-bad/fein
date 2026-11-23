## Valuation worksheet: Automotive Axles Ltd (AUTOAXLES) · as of 2026-11-23

*Worksheet v1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 18%, terminal ROIC 15%.*

### Snapshot (TTM Sep-2026)
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 1,776 | 2,684 | -393.9 | 2,290 | 12.9 | 8.1 | 24.4 | 4.1% | 7.7% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 1,776 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 7.7% | **12.6%** |
| Revenue CAGR for 10 yrs, margin moving to base-case 6.8% | **15.8%** |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 6.8%) | **26.1%** |
| NOPAT margin needed by year 10 on the base-case growth path (5.0% → 6.0%) | **10.4%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 7.3% |
| ROIIC the price implies on the base-case growth and margin path | none in tested range 1% to 300% (the price is outside what this path can produce) |
| Expected return (IRR) the price offers if the base case happens | **10.4%** (vs cost of equity 12.5%) |

Implied path (fade-to-terminal case). Reinvestment = growth ÷ ROIIC; P/E column = today's price ÷ that year's EPS:

| Year | Growth | Revenue | NOPAT margin | NOPAT | Reinvestment % NOPAT | FCF | EPS | Price ÷ EPS |
|---|---|---|---|---|---|---|---|---|
| 1 | 26.1% | 3,034 | 7.6% | 230.0 | 145% | -103.6 | 167.80 | 10.6 |
| 2 | 23.8% | 3,755 | 7.5% | 281.4 | 132% | -90.1 | 201.89 | 8.8 |
| 3 | 21.4% | 4,559 | 7.4% | 337.7 | 119% | -64.1 | 239.25 | 7.4 |
| 5 | 16.7% | 6,337 | 7.2% | 458.4 | 93% | 32.5 | 319.29 | 5.6 |
| 7 | 12.0% | 8,120 | 7.1% | 573.3 | 67% | 190.0 | 395.52 | 4.5 |
| 10 | 5.0% | 10,040 | 6.8% | 682.7 | 28% | 493.1 | 468.05 | 3.8 |

> **Feasibility flag:** on this path reinvestment exceeds 100% of NOPAT (peak 145%), so FCF is negative and growth would need outside capital at ROIIC 18%. Either ROIIC is higher than assumed or the implied path is not self-fundable.

Reading: the price needs revenue of ~10,040 INR cr by year 10 (4.2x today's) and terminal value is 86% of EV. Compare with what the business has shown (unit runway, reinvestment capacity, ROIIC), not with a consensus number.

Reinvestment realism (v1.3): last-5y incremental ROIC **21.0%** (given). Flag when a ROIIC used or implied differs by more than 5%:

| ROIIC | Value | Gap vs history | Flag |
|---|---|---|---|
| default ROIIC (input) | 18.0% | -3.0 pts | ok |
| scenario bear | 15.0% | -6.0 pts | **FLAG** |
| scenario base | 18.0% | -3.0 pts | ok |
| scenario bull | 22.0% | +1.0 pts | ok |
| implied by price on the base-case path | none in tested range 1-300% | n/a | ok |

> **Reinvestment-realism flag:** scenario bear. Either the business will earn on new capital what it has not earned recently, or the path is mis-specified (e.g. pricing-led growth that needs little capital). Say which in the deep dive.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 35% | -3.0% → 5.0% | 5.5% | 15% | 1,107 | -38% | -3.7% | 14.0 | 11.8 | 1.04x |
| base | 45% | 5.0% → 6.0% | 6.8% | 18% | 1,362 | -23% | 3.6% | 16.0 | 11.5 | 1.60x |
| bull | 17% | 11.0% → 7.0% | 8.0% | 22% | 1,765 | -1% | 9.6% | 18.0 | 12.2 | 2.32x |
| blow-up | 3% | — | — | — | 532.9 | -70% | — | — | — | 0.30x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 1,316 | -26% | -38% | 100% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.35, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 24% | 6% | 0% | 4% | 3% | 1.49x | 8.3% | 1.43x | 1.76x |

> **Exit-multiple gap:** in base, bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

**Exit-multiple bet (v1.3, L21).** The 5-year multiple is a bet on the P/E the market pays in year 5. Own median P/E: 18.8 (n=10).

| Scenario | Exit P/E used | DCF-consistent P/E yr5 | Own median P/E | Used ÷ DCF | Used ÷ own | 5-yr multiple at used | at DCF P/E | at own median |
|---|---|---|---|---|---|---|---|---|
| bear | 14.0 | 11.8 | 18.8 | 1.18x | 0.74x | 1.04x | 0.90x | 1.35x |
| base | 16.0 | 11.5 | 18.8 | 1.39x | 0.85x | 1.60x | 1.19x | 1.86x |
| bull | 18.0 | 12.2 | 18.8 | 1.47x | 0.96x | 2.32x | 1.61x | 2.42x |
| **EV (incl. blow-up)** | | | | | | **1.49x** | **1.13x** | **1.73x** |

Hurdle 1.76x. The card's gate uses the stated exit; the other two columns show how much of the answer is the multiple bet.

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 25.8 on EPS 68.90. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 12.9 | exit P/E 18.8 | exit P/E 19.3 | exit P/E 20.8 | exit P/E 25.8 |
|---|---|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -46%) | 22% (r -42%) | 20% (r -31%) | 15% (r 0%) |
| 3x | 43% (r -63%) | 33% (r -29%) | 32% (r -26%) | 30% (r -20%) | 25% (r 0%) |
| 5x | 58% (r -43%) | 47% (r -20%) | 46% (r -18%) | 44% (r -13%) | 38% (r 0%) |

Track record for comparison: EPS CAGR 4.4% Peak-to-peak EPS FY19 80.43 -> FY26 108.77 = 4.4%/yr [SCR]; FY16->FY26 16.8%/yr starts from a weak base and is not used.

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=10) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 12.9 | 0.69x | COLD | 0% | 0.62x | COLD |
| normalised EPS | 25.8 | 1.37x | WARM | 70% | 1.24x | WARM |

Own P/E history: FY17 21.6, FY18 26.1, FY19 16.0, FY20 14.1, FY21 70.3, FY22 34.8, FY23 22.1, FY24 16.0, FY25 15.7, FY26 14.2 (median 18.8).
Sector P/Es: Jamna Auto (CV springs) 20.8, GNA Axles 15.6, Wheels India (CV wheels) 29.7 (median 20.8).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 1,539 (-13%) | 1,627 (-8%) | 1,750 (-2%) | 1,904 (7%) | 2,080 (17%) |
| 11.5% | 1,373 (-23%) | 1,438 (-19%) | 1,526 (-14%) | 1,635 (-8%) | 1,757 (-1%) |
| 12.5% | 1,250 (-30%) | 1,298 (-27%) | 1,362 (-23%) | 1,438 (-19%) | 1,523 (-14%) |
| 13.5% | 1,155 (-35%) | 1,190 (-33%) | 1,236 (-30%) | 1,289 (-27%) | 1,347 (-24%) |
| 14.5% | 1,078 (-39%) | 1,104 (-38%) | 1,136 (-36%) | 1,172 (-34%) | 1,209 (-32%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 4.8% | 5.8% | 6.8% | 7.8% | 8.8% |
|---|---|---|---|---|---|
| 4.0% | 1,114 (-37%) | 1,227 (-31%) | 1,341 (-24%) | 1,455 (-18%) | 1,569 (-12%) |
| 5.0% | 1,128 (-36%) | 1,245 (-30%) | 1,362 (-23%) | 1,478 (-17%) | 1,595 (-10%) |
| 6.0% | 1,146 (-35%) | 1,267 (-29%) | 1,387 (-22%) | 1,508 (-15%) | 1,628 (-8%) |

### Input notes
- Price Rs 1,776.30 = NSE bhavcopy close 23-Nov-2026 = Yahoo AUTOAXLES.NS close 23-Nov-2026 (two sources). Shares 1,51,11,975 [AR26; NSE pledge API totIssuedShares 15,111,975].
- Net cash 393.9 at 30-Sep-2026 [Q2FY27 SoAL]: cash 30.82 + other bank balances 206.70 + current MF investments 169.67 = 407.2 less lease liabilities 13.29 (115.45+17.47 mn). Screener Sep-2026: cash equivalents 238 + investments 170 - borrowings 13 = 395 (second source).
- Treasury income post-tax 23 [EST]: 407 x ~7.5% x 0.75; FY26 interest on deposits 19.5 + MF gains/FV 7.5 = 27.0 pre-tax [AR26 n.22].
- Base = TTM Q3FY26..Q2FY27 [SCR quarterly, cross-checked to Q2FY27 results]: revenue 562+664+517+663 = 2,406; core EBITDA (ex other income) 64+77+60+83 = 284; D&A 38 -> core EBIT 246; PAT 199 reported + 9 post-tax add-back of the Q3FY26 labour-code exceptional (Rs 11.99 cr pre-tax [AR26 n.25]) = 208; EPS 137.6 adj (131.3 reported).
- FCF 110 [EST]: FY26 CFO 173 - capex ~72 (company: 'more than INR 70 crores') = ~101 [SCR FCF 101]; H1 FY27 CFO 86 - capex 45 = 41 with inventory build for the pre-buy. Not a clean run-rate.
- eps_normalised 68.9 = 10-year mean reported EPS FY17-FY26 (32.7, 55.5, 80.4, 27.2, 15.0, 49.2, 107.2, 110.0, 102.9, 108.8) [SCR]: two full M&HCV cycles.
- ROIIC 18% base [EST]: cross-cycle FY19->FY26 dNOPAT 30 / dIC 143 = 21%; FY18->FY26 22%; through-cycle average ROIC FY16-26 15.6% (min 4.5% FY21, max 21.9% FY23). terminal_roic 15% = through-cycle average. incremental_roic_5y 0.21 is the peak-to-peak window (a trough-to-peak FY21->FY26 window would give ~59% and is NOT used, per README v1.3 cyclicals guidance).
- Scenario design (cycle-position at year 5 = FY31-32; written before outputs): bear = the post-April-2027 pre-buy hangover plus one more downturn leaves FY31 revenue ~flat on TTM and NOPAT margin falling toward 5.5% by year 10 (OPM ~9%, the FY16-26 average is 10.0%); base = mid-cycle, revenue +5-6%/yr (industry 500k by 2030 is management's view, i.e. roughly flat volume from FY27 plus tonnage/content and price), NOPAT margin 6.8% (OPM ~10.7%); bull = management's Rs 4,000-5,000 cr by 2030 aspiration delivered partly (revenue ~2x by year 6-7), NOPAT 8%.
- Exit P/Es 14/16/18 [EST]: below the own FY-end median 21.6 because that median is inflated by trough-year P/Es (FY21 70x, FY22 35x); peers JAMNAAUTO 20.8, GNA 15.6, WHEELS 29.7 [SCR 23-Nov-2026]; RKFORGE 71 and BHARATFORG 84 excluded (depressed/one-off EPS). At the FY19 peak the stock traded at 16x trailing.
- Own P/E history = FY-end close [YH] / FY reported EPS [SCR] (FY17-FY26). Cyclical: high P/E at troughs, low at peaks.
- Payout of FCF 0.45 [EST]: dividend Rs 32/share = Rs 48 cr vs FCF ~101-110; payout ~29-30% of PAT for 5 years [SCR].
- Dispersion 0.35 (cyclical, single-customer 66%).

Sources: research_notes/Deep dives/AUTOAXLES_live.md; https://nsearchives.nseindia.in/annual_reports/AR_29891_AUTOAXLES_2025_2026_A_16112201_18072026164730.pdf; https://nsearchives.nseindia.in/annual_reports/AR_27028_AUTOAXLES_2024_2025_A_18072025200747.pdf; https://nsearchives.nseindia.in/corporate/AUTOAXLES_12112026175115_BMOutcome12112026.pdf; https://nsearchives.nseindia.in/corporate/AUTOAXLES_17112026155524_CallTranscription_Q2_17112026.pdf; https://www.screener.in/company/AUTOAXLES/consolidated/; https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_23112026.csv

