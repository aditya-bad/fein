## Valuation worksheet: Synthetic Test Co (fictional) (SYNTH) · as of 2026-11-21

> **TEST MATERIAL. No verdict.** These inputs exist to exercise the template (lesson L9). The scenario assumptions are illustrative [EST], not research conclusions. Research, not SEBI-registered advice.

*Worksheet v1.0 (2026-11-21). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 30%, terminal ROIC 30%.*

### Snapshot (FY26)
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 100.00 | 1,000 | -50.0 | 950.0 | 10.0 | 5.9 | 14.3 | 7.0% | 10.5% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 100.00 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 10.5% | **-0.2%** |
| Revenue CAGR for 10 yrs, margin moving to base-case 12.0% | **-2.1%** |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 12.0%) | **-7.0%** |
| NOPAT margin needed by year 10 on the base-case growth path (20.0% → 8.0%) | **4.1%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 4.8% |
| Expected return (IRR) the price offers if the base case happens | **19.5%** (vs cost of equity 12.5%) |

Implied path (fade-to-terminal case). Reinvestment = growth ÷ ROIIC; P/E column = today's price ÷ that year's EPS:

| Year | Growth | Revenue | NOPAT margin | NOPAT | Reinvestment % NOPAT | FCF | EPS | Price ÷ EPS |
|---|---|---|---|---|---|---|---|---|
| 1 | -7.0% | 929.6 | 10.7% | 99.0 | -23% | 122.2 | 9.43 | 10.6 |
| 2 | -5.7% | 876.5 | 10.8% | 94.7 | -19% | 112.7 | 9.02 | 11.1 |
| 3 | -4.4% | 838.3 | 10.9% | 91.8 | -15% | 105.2 | 8.74 | 11.4 |
| 5 | -1.7% | 799.1 | 11.2% | 89.9 | -6% | 95.0 | 8.56 | 11.7 |
| 7 | 1.0% | 804.2 | 11.5% | 92.9 | 3% | 89.8 | 8.85 | 11.3 |
| 10 | 5.0% | 895.6 | 12.0% | 107.5 | 17% | 89.6 | 10.24 | 9.8 |

Reading: the price needs revenue of ~895.6 INR cr by year 10 (0.9x today's) and terminal value is 41% of EV. Compare with what the business has shown (unit runway, reinvestment capacity, ROIIC), not with a consensus number.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 25% | 8.0% → 5.0% | 8.0% | 30% | 114.0 | 14% | 4.6% | 8.0 | 15.1 | 1.00x |
| base | 50% | 20.0% → 8.0% | 12.0% | 30% | 236.3 | 136% | 18.9% | 14.0 | 17.4 | 3.33x |
| bull | 22% | 28.0% → 10.0% | 14.0% | 30% | 368.1 | 268% | 27.8% | 20.0 | 19.2 | 6.83x |
| blow-up | 3% | — | — | — | 10.0 | -90% | — | — | — | 0.10x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 228.0 | 128% | 14% | 3% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.30, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 70% | 54% | 23% | 3% | 3% | 3.42x | 27.9% | 3.18x | 1.76x |

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 10.0 on EPS 10.00. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 5.0 | exit P/E 7.5 | exit P/E 10.0 | exit P/E 14.5 | exit P/E 18.0 |
|---|---|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -42%) | 15% (r 0%) | 7% (r 54%) | 2% (r 85%) |
| 3x | 43% (r -63%) | 32% (r -26%) | 25% (r 0%) | 16% (r 34%) | 11% (r 54%) |
| 5x | 58% (r -43%) | 46% (r -18%) | 38% (r 0%) | 28% (r 23%) | 23% (r 37%) |

Track record for comparison: EPS CAGR 18.0% .

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=6) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (price / base EPS) | 10.0 | 0.69x | COLD | 0% | 0.56x | COLD |

Own P/E history: FY20 14.0, FY21 18.0, FY22 16.0, FY23 12.0, FY24 15.0, FY25 13.0 (median 14.5).
Sector P/Es: Peer X 18.0, Peer Y 22.0, Peer Z 15.0 (median 18.0).
Market: Nifty 50 P/E 20.6 (2026-11): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 258 (158%) | 298 (198%) | 345 (245%) | 401 (301%) | 465 (365%) |
| 11.5% | 214 (114%) | 246 (146%) | 282 (182%) | 325 (225%) | 374 (274%) |
| 12.5% | 183 (83%) | 208 (108%) | 236 (136%) | 270 (170%) | 308 (208%) |
| 13.5% | 159 (59%) | 179 (79%) | 202 (102%) | 228 (128%) | 259 (159%) |
| 14.5% | 140 (40%) | 156 (56%) | 175 (75%) | 197 (97%) | 221 (121%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 10.0% | 11.0% | 12.0% | 13.0% | 14.0% |
|---|---|---|---|---|---|
| 4.0% | 190 (90%) | 206 (106%) | 222 (122%) | 238 (138%) | 254 (154%) |
| 5.0% | 202 (102%) | 219 (119%) | 236 (136%) | 254 (154%) | 271 (171%) |
| 6.0% | 218 (118%) | 236 (136%) | 255 (155%) | 274 (174%) | 293 (193%) |

### Input notes
- Fictional inputs for a unit test of the template.

