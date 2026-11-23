## Valuation worksheet: Sunflag Iron & Steel (SUNFLAG) · as of 2026-11-20

*Worksheet v1.2 (2026-11-23; non_operating_growth adds non-operating value to the 5-year multiple; 1.1 added bank mode). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 12%, terminal ROIC 12%.*

### Snapshot (FY26)
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 368.60 | 6,643 | 26.0 | 6,669 | 32.8 | 14.0 | 25.4 | 3.9% | 6.9% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 368.60 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 6.9% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Revenue CAGR for 10 yrs, margin moving to base-case 7.0% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 7.0%) | none in tested range -30% to 120% (the price is outside what this path can produce) |
| NOPAT margin needed by year 10 on the base-case growth path (8.0% → 6.0%) | **8.2%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 8.2% |
| Expected return (IRR) the price offers if the base case happens | **11.7%** (vs cost of equity 12.5%) |

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 30% | 3.0% → 4.0% | 5.0% | 10% | 321.3 | -13% | 0.2% | 9.0 | 13.2 | 0.70x |
| base | 50% | 8.0% → 6.0% | 7.0% | 12% | 351.0 | -5% | 7.7% | 12.0 | 12.9 | 1.54x |
| bull | 18% | 12.0% → 7.0% | 8.5% | 15% | 398.0 | 8% | 13.3% | 16.0 | 14.2 | 2.22x |
| blow-up | 2% | — | — | — | 92.2 | -75% | — | — | — | 0.25x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 345.4 | -6% | -13% | 82% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.40, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 24% | 6% | 0% | 8% | 2% | 1.38x | 6.7% | 1.33x | 1.76x |

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 32.8 on EPS 11.24. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 10.3 | exit P/E 16.4 | exit P/E 19.0 | exit P/E 24.6 | exit P/E 32.8 |
|---|---|---|---|---|---|
| 2x | 45% (r -167%) | 32% (r -100%) | 28% (r -79%) | 22% (r -42%) | 15% (r 0%) |
| 3x | 57% (r -105%) | 43% (r -63%) | 39% (r -50%) | 32% (r -26%) | 25% (r 0%) |
| 5x | 74% (r -72%) | 58% (r -43%) | 54% (r -34%) | 46% (r -18%) | 38% (r 0%) |

Track record for comparison: EPS CAGR 7.6% Consolidated EPS FY21 7.80 -> FY26 11.23 [SCR]; FY23 61.89 incl. the LMEL arbitral-award gain excluded.

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=10) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 32.8 | 3.17x | VERY HOT | 100% | 1.73x | HOT |

Own P/E history: FY17 10.2, FY18 10.5, FY19 7.9, FY20 4.7, FY21 8.0, FY22 5.2, FY23 12.3, FY24 23.4, FY25 26.1, FY26 17.3 (median 10.3).
Sector P/Es: Kalyani Steels 12.6, Vardhman Special Steels 39.0, Usha Martin 25.4, Mukand (one-off inflated EPS) 3.1 (median 19.0).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 391 (6%) | 397 (8%) | 404 (10%) | 412 (12%) | 420 (14%) |
| 11.5% | 368 (-0%) | 371 (1%) | 373 (1%) | 376 (2%) | 377 (2%) |
| 12.5% | 351 (-5%) | 351 (-5%) | 351 (-5%) | 350 (-5%) | 347 (-6%) |
| 13.5% | 338 (-8%) | 337 (-9%) | 334 (-9%) | 330 (-10%) | 324 (-12%) |
| 14.5% | 327 (-11%) | 325 (-12%) | 321 (-13%) | 315 (-15%) | 307 (-17%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 5.0% | 6.0% | 7.0% | 8.0% | 9.0% |
|---|---|---|---|---|---|
| 4.0% | 322 (-13%) | 336 (-9%) | 351 (-5%) | 366 (-1%) | 380 (3%) |
| 5.0% | 322 (-13%) | 336 (-9%) | 351 (-5%) | 366 (-1%) | 380 (3%) |
| 6.0% | 322 (-13%) | 336 (-9%) | 351 (-5%) | 365 (-1%) | 380 (3%) |

### Input notes
- Price 368.60 = NSE close 20-Nov-2026 [NSE bhavcopy sec_bhavdata_full_20112026] = Yahoo v8 close 20-Nov-2026; screener 23-Nov intraday 363. Shares 18.022 cr [AR26 n.32: 18,02,19,448].
- NON-OPERATING VALUE (the core of this file): 6.00 cr shares of Lloyds Metals & Energy (LMEL, 10.66%) [AR26 n.4] x 1,723.80 (NSE close 20-Nov-2026, Yahoo same) = 10,343 cr pre-tax. Cost 1,226 cr [AR26 n.40: 1,22,610 lakh]. Tax on the gain at 12.5% LTCG x 1.12 surcharge x 1.04 cess = 14.56% [EST, statutory rates] = 1,327 cr -> post-tax 9,016 cr (Rs 500/share). Other JV/associate investments ~55 cr at book [AR26 n.4, EST].
- HOLDCO DISCOUNT ASSUMPTION (written before outputs): the market is assumed to keep valuing the stake at a persistent 55% discount to post-tax value (insight:group-holdco-discount: 40-70% commonly cited, unverified) -> non_operating_value = 0.45 x 9,016 + 55 = 4,112 cr. Sensitivity to d = 0.3/0.45/0.55/0.65/0.75 is in the deep-dive file (section 8.2).
- non_operating_growth: the stake compounds with LMEL; per-scenario bear -8%/yr, base +10%/yr, bull +16%/yr (no edge claimed on LMEL; base ~ CoE less LMEL dividend). The 5-year multiple adds the (discounted) stake at year 5 to EPS5 x exit P/E (worksheet v1.2).
- Net debt 26 cr at 30-Sep-2026 [Q2 FY27 consolidated SoAL: borrowings 30.67 + 362.13 = 392.8 cr; cash 322.8 + other bank 44.1 = 366.9 cr]; lease liabilities 42.7 cr excluded (rent inside EBITDA is small).
- Base FY26 consolidated [SCR; AR26 P&L]: revenue 3,939, EBITDA 477 (12.1%), D&A 113, EBIT 364 (core, ex other income 9), PAT 202 (after exceptional -8.7 and prior-year deferred tax -25.1), FCF 262, EPS 11.23 (includes ~0.25/share of LMEL dividend: 6 cr pre-tax [AR26 n.25b]).
- ROIIC 12% [EST]: operating capital ~2,540 cr (FA 1,577 + CWIP 214 + NWC ~750) vs FY26 EBIT 364 -> pre-tax ROCE ~14%, post-tax ~10.7%; the steel business earns roughly its cost of capital through the cycle (screener ROCE 4% is diluted by the LMEL mark).
- pe_history: FY-end close [Yahoo v8] / consolidated EPS [SCR]. FY23 uses core EPS ~12.0 (ex the 1,201 cr arbitral-award gain). From FY23 the price includes the LMEL stake, so the own-history band is NOT like-for-like (pre-FY23 median ~8x is the steel-only band).
- Trailing P/E 32.8 (price / FY26 EPS) is meaningless for this stock: the temperature block reads it against peers, but the LMEL stake is ~156% of the market cap pre-tax (~136% post-tax). Use the stub P/E in the deep-dive file instead.
- Peer P/Es: screener top ratios 23-Nov-2026 (KSL 12.6, VSSL 39.0, USHAMART 25.4, MUKANDLTD 3.09 one-off). Single-source.

Sources: research_notes/Deep dives/SUNFLAG_live.md; https://nsearchives.nseindia.in/annual_reports/AR_31025_SUNFLAG_2025_2026_A_4883414_01092026183814.pdf; https://nsearchives.nseindia.in/corporate/SUNFLAG_13112026171507_SE_outcome_BM_13112026_.pdf; https://www.screener.in/company/SUNFLAG/consolidated/; https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_20112026.csv

