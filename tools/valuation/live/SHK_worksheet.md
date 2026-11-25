## Valuation worksheet: S H Kelkar and Company Ltd (fragrances and flavours; Keva) (SHK) · as of 2026-11-23

*Worksheet v1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 8%, terminal ROIC 8%.*

### Snapshot (TTM Sep-2026 (core: ex exceptional items and other income))
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 127.53 | 1,765 | 911.0 | 2,676 | 18.7 | 9.4 | 88.3 | 1.1% | 3.7% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 127.53 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 3.7% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Revenue CAGR for 10 yrs, margin moving to base-case 5.5% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 5.5%) | none in tested range -30% to 120% (the price is outside what this path can produce) |
| NOPAT margin needed by year 10 on the base-case growth path (12.0% → 8.0%) | **33.4%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 11.7% |
| ROIIC the price implies on the base-case growth and margin path | none in tested range 1% to 300% (the price is outside what this path can produce) |
| Expected return (IRR) the price offers if the base case happens | **7.3%** (vs cost of equity 12.5%) |

Reinvestment realism (v1.3): last-5y incremental ROIC **3.0%** (given). Flag when a ROIIC used or implied differs by more than 5%:

| ROIIC | Value | Gap vs history | Flag |
|---|---|---|---|
| default ROIIC (input) | 8.0% | +5.0 pts | ok |
| scenario bear | 4.0% | +1.0 pts | ok |
| scenario base | 8.0% | +5.0 pts | ok |
| scenario bull | 12.0% | +9.0 pts | **FLAG** |
| implied by price on the base-case path | none in tested range 1-300% | n/a | ok |

> **Reinvestment-realism flag:** scenario bull. Either the business will earn on new capital what it has not earned recently, or the path is mis-specified (e.g. pricing-led growth that needs little capital). Say which in the deep dive.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 30% | 6.0% → 5.0% | 3.5% | 4% | -66.8 | -152% | 9.2% | 14.0 | -11.5 | 0.60x |
| base | 47% | 12.0% → 8.0% | 5.5% | 8% | -42.7 | -133% | 25.6% | 22.0 | -1.7 | 1.89x |
| bull | 15% | 14.0% → 11.0% | 7.0% | 12% | -1.6 | -101% | 33.8% | 28.0 | 3.5 | 3.30x |
| blow-up | 8% | — | — | — | 31.9 | -75% | — | — | — | 0.25x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| -37.8 | -130% | -152% | 100% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.35, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 34% | 14% | 2% | 17% | 8% | 1.59x | 9.7% | 1.50x | 1.76x |

> **Exit-multiple gap:** in bear, base, bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

**Exit-multiple bet (v1.3, L21).** The 5-year multiple is a bet on the P/E the market pays in year 5. Own median P/E: 23.9 (n=10).

| Scenario | Exit P/E used | DCF-consistent P/E yr5 | Own median P/E | Used ÷ DCF | Used ÷ own | 5-yr multiple at used | at DCF P/E | at own median |
|---|---|---|---|---|---|---|---|---|
| bear | 14.0 | -11.5 | 23.9 | n/a | 0.59x | 0.60x | -0.49x | 1.02x |
| base | 22.0 | -1.7 | 23.9 | n/a | 0.92x | 1.89x | -0.14x | 2.06x |
| bull | 28.0 | 3.5 | 23.9 | 8.10x | 1.17x | 3.30x | 0.41x | 2.82x |
| **EV (incl. blow-up)** | | | | | | **1.59x** | **-0.13x** | **1.72x** |

Hurdle 1.76x. The card's gate uses the stated exit; the other two columns show how much of the answer is the multiple bet.

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 19.1 on EPS 6.69. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 9.5 | exit P/E 14.3 | exit P/E 19.1 | exit P/E 23.9 | exit P/E 37.2 |
|---|---|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -41%) | 15% (r 0%) | 10% (r 33%) | 0% (r 96%) |
| 3x | 43% (r -63%) | 32% (r -26%) | 25% (r 0%) | 19% (r 21%) | 9% (r 61%) |
| 5x | 59% (r -43%) | 46% (r -18%) | 38% (r 0%) | 32% (r 14%) | 21% (r 42%) |

Track record for comparison: EPS CAGR 0.0% Consolidated EPS FY16 5.05 -> FY26 5.00 [SCR] = ~0%/yr over 10 years while revenue grew 925 -> 2,368 (+9.9%/yr) and invested capital roughly 2.6x.

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=10) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 18.7 | 0.78x | COOL | 20% | 0.50x | COLD |
| normalised EPS | 19.1 | 0.80x | COOL | 20% | 0.51x | COLD |

Own P/E history: FY17 40.9, FY18 39.9, FY19 24.6, FY20 30.1, FY21 10.9, FY22 13.4, FY23 22.5, FY24 23.2, FY25 33.4, FY26 22.5 (median 23.9).
Sector P/Es: Privi Speciality Chemicals 37.2, Galaxy Surfactants 29.9, Oriental Aromatics 170.0 (median 37.2).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 0 (-100%) | -7 (-106%) | -17 (-114%) | -31 (-124%) | -48 (-138%) |
| 11.5% | -11 (-109%) | -20 (-116%) | -32 (-125%) | -48 (-138%) | -68 (-153%) |
| 12.5% | -19 (-115%) | -29 (-123%) | -43 (-133%) | -60 (-147%) | -81 (-163%) |
| 13.5% | -25 (-120%) | -36 (-128%) | -50 (-139%) | -68 (-153%) | -89 (-170%) |
| 14.5% | -30 (-124%) | -42 (-133%) | -56 (-144%) | -74 (-158%) | -96 (-175%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 3.5% | 4.5% | 5.5% | 6.5% | 7.5% |
|---|---|---|---|---|---|
| 4.0% | -50 (-140%) | -43 (-134%) | -36 (-128%) | -28 (-122%) | -21 (-116%) |
| 5.0% | -55 (-143%) | -49 (-138%) | -43 (-133%) | -37 (-129%) | -31 (-124%) |
| 6.0% | -61 (-148%) | -57 (-144%) | -52 (-141%) | -48 (-137%) | -43 (-134%) |

### Input notes
- Price Rs 127.53 = NSE bhavcopy close 23-Nov-2026 (sec_bhavdata_full_24112026.csv, DATE1 23-Nov-2026) = Yahoo v8 SHK.NS close 23-Nov-2026 (two sources). screener.in 25-Nov-2026 Rs 126 / mcap Rs 1,742 cr. Shares 13.842 cr (138,420,801; universe.csv = SHP XBRL 30-Sep-2026).
- Net debt 911 at 30-Sep-2026: borrowings non-current 203.48 + current 769.28 = 972.76 less cash 61.74 + other bank 0.34 [Q2FY27 consolidated XBRL] = 910.7 = company deck 'Net Debt 911' (two sources). Leases (~Rs 190 cr [EST] = screener borrowings 1,163 - 973) excluded; rent sits inside the margin.
- treasury_income_post_tax -45.8 = TTM finance cost 60.9 (13.50 + 15.03 + 15.00 + 17.40, XBRL) x (1 - 0.25), held flat (management: H2 interest Rs 16-17 cr/quarter; debt 'peaked' Sep-2026).
- Base = TTM Q3FY26..Q2FY27 [XBRL = screener]: revenue 583.80 + 649.94 + 662.42 + 636.19 = 2,532.4; operating profit 56.09 + 60.03 + 88.66 + 78.86 = 283.6; D&A 138.4 -> EBIT ex other income 145.2. Reported PAT 94.4 / EPS 6.82 (18.7x) includes exceptional gains of 63.0 (fire-insurance realisations 33.07 in Q3 FY26 and 29.95 in Q1 FY27) and other income 12.1. Core EPS: (EBIT 145.2 x 0.65 - 45.8) / 13.842 = 3.51 -> 36.3x; cross-check (PBT ex exceptional 96.4 less reported tax ex an assumed 25% on the exceptional) = 47.3 / 13.842 = 3.42; screener's 'Stock P/E 32.5' implies ~Rs 53.6 cr (ex-exceptional profit) = second route, ~3.9/share.
- tax_rate 0.35: Indian rate 25.2% but group effective tax 38% FY26, 36% FY25, 51% on TTM core profit because European/US creative-centre losses get no tax shield [AR26; XBRL]; 0.35 assumes partial normalisation.
- FCF 20 [EST]: CFO FY22-26 50/197/107/16/263 (avg 127) less capex ~Rs 150 cr/yr (Vanavate, Vashivali rebuild, Almere) [SCR; calls].
- eps_normalised 6.69 = mean consolidated EPS FY17-26 (7.25, 6.49, 6.12, 2.53, 10.24, 10.73, 4.42, 8.84, 5.29, 5.00) [SCR]; per-share series, so the FY20/FY22 buybacks are already reflected; FY22 includes a negative tax charge (-13%) and FY24-26 include fire-related exceptional items of both signs. 19.1x on it.
- ROIIC (full-cycle window, L38/L42): FY17-19 avg EBIT ex OI 131 on avg IC ~1,040 (equity + screener borrowings) -> ROIC ~8.8% after 30% tax; FY24-26 avg EBIT 181 on avg IC ~2,124 -> ~6.0%; dEBIT +50 x 0.7 / dIC +1,084 = ROIIC ~3% [EST]. TTM ROIC 145.2 x 0.70 / (equity 1,420.7 + net debt 910.7 = 2,331) = 4.4%; with management's Rs 80 cr creative-centre opex added back 6.8%. incremental_roic_5y 0.03; base ROIIC 0.08 assumes the new capacity and centres start to earn.
- Scenarios (5-yr; written before outputs; tails started from the India 1,000-20,000 cr class 21%/11%/15%): blow-up 8% raw; bear 30% = margins stuck (EBITDA ~11%), Europe/US centres keep losing, growth +6%: NOPAT margin 3.5%, ROIIC 4%, exit 14x (FY21-22 trough P/Es 10.9-13.4); base 47% = guidance partly met (revenue +12-13%/yr, EBITDA drifts to ~14% by FY29 vs 15% promised '12-18 months'): +12% -> +8%, NOPAT margin 5.5%, ROIIC 8%, exit 22x (own 10-yr median 23.9x less a discount for sub-CoE returns); bull 15% = 15%+ EBITDA within 18 months, international ramps, debt falls: +14% -> +11%, 7.0%, ROIIC 12%, exit 28x (below Privi 37x).
- Exit P/Es: own FY-end P/Es FY17-26 (reported EPS) 40.9/39.9/24.6/30.1/10.9/13.4/22.5/23.2/33.4/22.5, median 23.9. Peers [SCR 25-Nov-2026]: Privi Speciality 37.2 (aroma chemicals, ROCE 22%), Galaxy Surfactants 29.9 (FMCG-ingredient supplier), Oriental Aromatics 170 (depressed earnings; outlier). No listed Indian pure fragrance-and-flavour compounder.
- Dispersion 0.35 (higher than default: 5-year price range 343.8 -> 48.9 -> 205).

Sources: research_notes/Deep dives/SHK_live.md; https://nsearchives.nseindia.in/annual_reports/AR_29522_SHK_2025_2026_A_9351211_01072026182209.pdf; https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1751494_02112026084816_WEB.xml; https://nsearchives.nseindia.in/corporate/aditya_joshi_keva_co_in_06112026112611_SHKConcallTranscriptIntimationQ2FY27FinalSigned.pdf; https://www.screener.in/company/SHK/consolidated/; https://nsearchives.nseindia.in/products/content/sec_bhavdata_full_24112026.csv

