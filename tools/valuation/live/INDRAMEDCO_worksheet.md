## Valuation worksheet: Indraprastha Medical Corporation Ltd (Indraprastha Apollo Hospitals, Sarita Vihar) (INDRAMEDCO) · as of 2026-11-23

*Worksheet v1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 30%, terminal ROIC 25%.*

### Snapshot (TTM Sep-2026)
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 355.85 | 3,262 | -521.4 | 2,741 | 17.0 | 9.8 | 28.4 | 3.5% | 11.2% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 355.85 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 11.2% | **11.0%** |
| Revenue CAGR for 10 yrs, margin moving to base-case 10.0% | **12.8%** |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 10.0%) | **19.4%** |
| NOPAT margin needed by year 10 on the base-case growth path (9.0% → 7.0%) | **13.6%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 8.0% |
| ROIIC the price implies on the base-case growth and margin path | none in tested range 1% to 300% (the price is outside what this path can produce) |
| Expected return (IRR) the price offers if the base case happens | **10.9%** (vs cost of equity 12.5%) |

Implied path (fade-to-terminal case). Reinvestment = growth ÷ ROIIC; P/E column = today's price ÷ that year's EPS:

| Year | Growth | Revenue | NOPAT margin | NOPAT | Reinvestment % NOPAT | FCF | EPS | Price ÷ EPS |
|---|---|---|---|---|---|---|---|---|
| 1 | 19.4% | 1,857 | 11.1% | 206.3 | 65% | 73.2 | 24.28 | 14.7 |
| 2 | 17.8% | 2,187 | 11.0% | 240.2 | 59% | 98.0 | 27.86 | 12.8 |
| 3 | 16.2% | 2,541 | 10.9% | 276.0 | 54% | 127.2 | 31.63 | 11.2 |
| 5 | 13.0% | 3,289 | 10.6% | 349.1 | 43% | 198.1 | 39.35 | 9.0 |
| 7 | 9.8% | 4,022 | 10.4% | 417.0 | 33% | 281.0 | 46.52 | 7.7 |
| 10 | 5.0% | 4,870 | 10.0% | 487.0 | 17% | 405.8 | 53.90 | 6.6 |

Reading: the price needs revenue of ~4,870 INR cr by year 10 (3.1x today's) and terminal value is 61% of EV. Compare with what the business has shown (unit runway, reinvestment capacity, ROIIC), not with a consensus number.

Reinvestment realism (v1.3): last-5y incremental ROIC **40.0%** (given). Flag when a ROIIC used or implied differs by more than 5%:

| ROIIC | Value | Gap vs history | Flag |
|---|---|---|---|
| default ROIIC (input) | 30.0% | -10.0 pts | **FLAG** |
| scenario bear | 15.0% | -25.0 pts | **FLAG** |
| scenario base | 30.0% | -10.0 pts | **FLAG** |
| scenario bull | 35.0% | -5.0 pts | **FLAG** |
| implied by price on the base-case path | none in tested range 1-300% | n/a | ok |

> **Reinvestment-realism flag:** default ROIIC (input); scenario bear; scenario base; scenario bull. Either the business will earn on new capital what it has not earned recently, or the path is mis-specified (e.g. pricing-led growth that needs little capital). Say which in the deep dive.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 20% | -8.0% → 5.0% | 5.0% | 15% | 164.0 | -54% | -9.5% | 14.0 | 14.7 | 0.59x |
| base | 45% | 9.0% → 7.0% | 10.0% | 30% | 290.7 | -18% | 6.6% | 20.0 | 14.8 | 1.70x |
| bull | 15% | 11.0% → 8.0% | 12.0% | 35% | 358.2 | 1% | 10.0% | 28.0 | 16.1 | 2.74x |
| blow-up | 20% | — | — | — | 89.0 | -75% | — | — | — | 0.25x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 235.1 | -34% | -54% | 85% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.30, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 26% | 7% | 0% | 26% | 20% | 1.35x | 6.1% | 1.35x | 1.76x |

> **Exit-multiple gap:** in base, bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

**Exit-multiple bet (v1.3, L21).** The 5-year multiple is a bet on the P/E the market pays in year 5. Own median P/E: 15.7 (n=10).

| Scenario | Exit P/E used | DCF-consistent P/E yr5 | Own median P/E | Used ÷ DCF | Used ÷ own | 5-yr multiple at used | at DCF P/E | at own median |
|---|---|---|---|---|---|---|---|---|
| bear | 14.0 | 14.7 | 15.7 | 0.95x | 0.89x | 0.59x | 0.62x | 0.65x |
| base | 20.0 | 14.8 | 15.7 | 1.35x | 1.28x | 1.70x | 1.28x | 1.35x |
| bull | 28.0 | 16.1 | 15.7 | 1.74x | 1.79x | 2.74x | 1.62x | 1.57x |
| **EV (incl. blow-up)** | | | | | | **1.35x** | **0.99x** | **1.02x** |

Hurdle 1.76x. The card's gate uses the stated exit; the other two columns show how much of the answer is the multiple bet.

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 17.0 on EPS 20.93. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 8.5 | exit P/E 12.8 | exit P/E 15.7 | exit P/E 17.0 | exit P/E 48.0 |
|---|---|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -41%) | 17% (r -11%) | 15% (r 0%) | -7% (r 150%) |
| 3x | 43% (r -63%) | 32% (r -26%) | 27% (r -7%) | 25% (r 0%) | 1% (r 94%) |
| 5x | 58% (r -43%) | 46% (r -18%) | 40% (r -5%) | 38% (r 0%) | 12% (r 64%) |

Track record for comparison: EPS CAGR 22.4% FY16 2.66 -> FY26 20.03 = 22.4%/yr [SCR]; driven by OPM 10% -> 18% and ARPP, from a low base; not repeatable at the same rate.

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=10) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 17.0 | 1.09x | NORMAL | 50% | 0.35x | COLD |

Own P/E history: FY17 18.6, FY18 21.1, FY19 12.4, FY20 7.1, FY21 214.8, FY22 9.1, FY23 8.2, FY24 12.7, FY25 22.0, FY26 18.6 (median 15.7).
Sector P/Es: Artemis Medicare 44.3, Shalby 33.3, Yatharth Hospital 54.9, Jupiter Life Line 51.3, Narayana Hrudayalaya 44.6, Apollo Hospitals 58.8 (median 48.0).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 310 (-13%) | 339 (-5%) | 381 (7%) | 430 (21%) | 487 (37%) |
| 11.5% | 274 (-23%) | 296 (-17%) | 329 (-8%) | 367 (3%) | 411 (15%) |
| 12.5% | 246 (-31%) | 265 (-26%) | 291 (-18%) | 321 (-10%) | 355 (-0%) |
| 13.5% | 226 (-37%) | 241 (-32%) | 262 (-26%) | 286 (-20%) | 313 (-12%) |
| 14.5% | 209 (-41%) | 222 (-38%) | 239 (-33%) | 258 (-27%) | 281 (-21%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 8.0% | 9.0% | 10.0% | 11.0% | 12.0% |
|---|---|---|---|---|---|
| 4.0% | 246 (-31%) | 263 (-26%) | 280 (-21%) | 297 (-16%) | 314 (-12%) |
| 5.0% | 255 (-28%) | 273 (-23%) | 291 (-18%) | 309 (-13%) | 327 (-8%) |
| 6.0% | 266 (-25%) | 285 (-20%) | 304 (-15%) | 323 (-9%) | 343 (-4%) |

### Input notes
- Price Rs 355.85 = NSE bhavcopy close 23-Nov-2026; screener.in 24-Nov-2026 shows Rs 356 / mcap Rs 3,262 cr (second source). Yahoo v8 has no bar after 18-Nov-2026 (Rs 358.00). Shares 9,16,73,000 [AR26 n.30.M; NSE pledge API totIssuedShares].
- Net cash 521.4 at 30-Sep-2026 [Q2FY27 XBRL]: cash 6.48 + other bank balances 196.85 + current investments 142.16 + non-current investments 210.90 = 556.4, less lease liabilities ~35 (screener borrowings Sep-2026 35). No bank debt ('There are no Loans and Debt Securities').
- Treasury income post-tax 23 [EST]: TTM other income 31 x 0.75; FY26 interest income 27.61 + MF gains 1.14 [AR26 n.23].
- Base = TTM Q3FY26..Q2FY27 [SCR quarterly; Q2FY27 XBRL revenue 412.85 / PAT 53.58 / EPS 5.84 agree]: revenue 372+365+406+413 = 1,556; EBITDA (ex other income) 62+61+80+77 = 280; D&A 46 -> EBIT 233 (incl. ~3 lease interest in finance cost ignored); PAT 192; EPS 20.95.
- FCF 115 [EST]: FY26 CFO 167 - capex ~59 [SCR FCF 108]; FY25 120; FY24 131.
- eps_normalised not used: not a cyclical (FY20-21 COVID dip only). 10-yr mean EPS Rs 8.02 would give 44x but EPS has grown structurally (OPM 10% -> 18%).
- ROIIC: invested capital ex cash is only ~Rs 220-320 cr because the land is leased from GNCTD at Re 1/month (Rs 12/yr, AR26 n.30.D) and GNCTD funded Rs 15.48 cr of the building; ROIC ~50%+ is partly a land subsidy whose price is the free-treatment obligation. incremental_roic_5y 0.40 [EST]; base roiic 0.30, terminal 0.25 assume part of the subsidy is clawed back.
- Scenarios (5-yr, legal outcome; written before outputs): blow-up 20% = non-renewal/handover; bear 20% = renewal with enforced EWS (33% IPD / 40% OPD free incl. medicines) and/or market lease rent -> revenue down, NOPAT margin to 5%; base 45% = litigation continues or renewal on IMCL's own ask (10% IPD / 25% OPD incl. medicines), revenue +9%/yr (TTM +11%, ARPP-led), NOPAT margin 11.2% -> 10%; bull 15% = 30-year renewal on near-current terms and a re-rating toward (but below) peers.
- Exit P/Es 14/20/28 [EST]: own FY-end median 15.6 (FY17-26, includes FY20-23 single-digit years when the lease dispute was dormant and margins 10-14%); peers 33-59x [SCR 24-Nov-2026]; the discount to peers is the lease risk, so a bull exit below peers.
- Dispersion 0.30.

Sources: research_notes/Deep dives/INDRAMEDCO_live.md; https://nsearchives.nseindia.in/annual_reports/AR_30962_INDRAMEDCO_2025_2026_A_5876360_01092026125250.pdf; https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1748879_29102026043325_WEB.xml; https://nsearchives.nseindia.in/corporate/INDRAMEDCO_09022026115023_IMCLUPDATE09022026.pdf; https://www.screener.in/company/INDRAMEDCO/; https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_23112026.csv

