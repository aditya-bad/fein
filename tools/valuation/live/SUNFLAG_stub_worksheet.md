## Valuation worksheet: Sunflag Iron & Steel - steel-business STUB (supplementary; not used for paper calls) (SUNFLAG) · as of 2026-11-20

*Worksheet v1.2 (2026-11-23; non_operating_growth adds non-operating value to the 5-year multiple; 1.1 added bank mode). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 12%, terminal ROIC 12%.*

### Snapshot (FY26)
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 140.43 | 2,531 | 26.0 | 2,557 | 12.5 | 5.4 | 9.7 | 10.4% | 6.9% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 140.43 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 6.9% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Revenue CAGR for 10 yrs, margin moving to base-case 7.0% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 7.0%) | none in tested range -30% to 120% (the price is outside what this path can produce) |
| NOPAT margin needed by year 10 on the base-case growth path (8.0% → 6.0%) | **8.2%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 2.0% |
| Expected return (IRR) the price offers if the base case happens | **11.7%** (vs cost of equity 12.5%) |

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 30% | 3.0% → 4.0% | 5.0% | 10% | 93.1 | -34% | 0.2% | 9.0 | 13.2 | 0.76x |
| base | 50% | 8.0% → 6.0% | 7.0% | 12% | 122.8 | -13% | 7.7% | 12.0 | 12.9 | 1.41x |
| bull | 18% | 12.0% → 7.0% | 8.5% | 15% | 169.8 | 21% | 13.3% | 16.0 | 14.2 | 2.41x |
| blow-up | 2% | — | — | — | 35.1 | -75% | — | — | — | 0.25x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 120.6 | -14% | -34% | 82% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.40, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 22% | 7% | 1% | 7% | 2% | 1.37x | 6.6% | 1.28x | 1.76x |

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 12.5 on EPS 11.23. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 6.2 | exit P/E 8.0 | exit P/E 9.4 | exit P/E 12.5 | exit P/E 19.0 |
|---|---|---|---|---|---|
| 2x | 32% (r -101%) | 26% (r -64%) | 22% (r -41%) | 15% (r 0%) | 6% (r 60%) |
| 3x | 43% (r -64%) | 36% (r -41%) | 32% (r -26%) | 25% (r 0%) | 15% (r 38%) |
| 5x | 59% (r -44%) | 51% (r -28%) | 46% (r -18%) | 38% (r 0%) | 27% (r 26%) |

Track record for comparison: EPS CAGR 7.6% Consolidated EPS FY21 7.80 -> FY26 11.23 [SCR]; FY23 61.89 incl. the LMEL arbitral-award gain excluded.

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=7) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 12.5 | 1.56x | HOT | 100% | 0.66x | COLD |

Own P/E history: FY17 10.2, FY18 10.5, FY19 7.9, FY20 4.7, FY21 8.0, FY22 5.2, FY23 12.3 (median 8.0).
Sector P/Es: Kalyani Steels 12.6, Vardhman Special Steels 39.0, Usha Martin 25.4, Mukand (one-off inflated EPS) 3.1 (median 19.0).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 163 (16%) | 169 (20%) | 176 (25%) | 184 (31%) | 192 (37%) |
| 11.5% | 140 (-0%) | 142 (1%) | 145 (3%) | 147 (5%) | 149 (6%) |
| 12.5% | 123 (-13%) | 123 (-12%) | 123 (-13%) | 121 (-14%) | 118 (-16%) |
| 13.5% | 110 (-22%) | 109 (-23%) | 106 (-25%) | 102 (-28%) | 96 (-32%) |
| 14.5% | 99 (-29%) | 97 (-31%) | 93 (-34%) | 87 (-38%) | 78 (-44%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 5.0% | 6.0% | 7.0% | 8.0% | 9.0% |
|---|---|---|---|---|---|
| 4.0% | 94 (-33%) | 108 (-23%) | 123 (-13%) | 137 (-2%) | 152 (8%) |
| 5.0% | 94 (-33%) | 108 (-23%) | 123 (-13%) | 137 (-2%) | 152 (8%) |
| 6.0% | 94 (-33%) | 108 (-23%) | 123 (-13%) | 137 (-2%) | 152 (8%) |

### Input notes
- STUB = (market cap 6,643 - stake valued at a 55% discount to post-tax value 4,112) / 18.022 = Rs 140.43 per share: what the market pays for the steel business IF the stake carries a 55% holdco discount. Supplementary view for the variant-perception section only; the card and its paper calls use SUNFLAG.json at the real price.
- Own P/E history restricted to FY17-FY23 (steel-only years before the LMEL stake entered the price).
- Net debt 26 cr at 30-Sep-2026 [Q2 FY27 consolidated SoAL: borrowings 30.67 + 362.13 = 392.8 cr; cash 322.8 + other bank 44.1 = 366.9 cr]; lease liabilities 42.7 cr excluded (rent inside EBITDA is small).
- Base FY26 consolidated [SCR; AR26 P&L]: revenue 3,939, EBITDA 477 (12.1%), D&A 113, EBIT 364 (core, ex other income 9), PAT 202 (after exceptional -8.7 and prior-year deferred tax -25.1), FCF 262, EPS 11.23 (includes ~0.25/share of LMEL dividend: 6 cr pre-tax [AR26 n.25b]).
- ROIIC 12% [EST]: operating capital ~2,540 cr (FA 1,577 + CWIP 214 + NWC ~750) vs FY26 EBIT 364 -> pre-tax ROCE ~14%, post-tax ~10.7%; the steel business earns roughly its cost of capital through the cycle (screener ROCE 4% is diluted by the LMEL mark).

Sources: research_notes/Deep dives/SUNFLAG_live.md; https://nsearchives.nseindia.in/annual_reports/AR_31025_SUNFLAG_2025_2026_A_4883414_01092026183814.pdf; https://nsearchives.nseindia.in/corporate/SUNFLAG_13112026171507_SE_outcome_BM_13112026_.pdf; https://www.screener.in/company/SUNFLAG/consolidated/; https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_20112026.csv

