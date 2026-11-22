## Valuation worksheet: Five Below (US-FIVE) · as of 2026-09-30

> **TEST MATERIAL. No verdict.** These inputs exist to exercise the template (lesson L9). The scenario assumptions are illustrative [EST], not research conclusions. Research, not SEBI-registered advice.

*Worksheet v1.0 (2026-11-21). Money in USD M; per-share figures in USD. Cost of equity 9.5% (market default 9-10%), terminal growth 3.0%, 10-year explicit period, ROIIC 20%, terminal ROIC 18%.*

### Snapshot (FY2025 (to 31-Jan-2026))
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 220.00 | 12,188 | -932.2 | 11,256 | 34.0 | n/a | 29.6 | 3.4% | 7.2% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 220.00 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 7.2% | **20.0%** |
| Revenue CAGR for 10 yrs, margin moving to base-case 8.5% | **17.1%** |
| Year-1 growth, fading linearly to 3.0% by year 10 (margin to 8.5%) | **29.9%** |
| NOPAT margin needed by year 10 on the base-case growth path (16.0% → 5.0%) | **12.4%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 5.6% |
| Expected return (IRR) the price offers if the base case happens | **7.9%** (vs cost of equity 9.5%) |

Implied path (fade-to-terminal case). Reinvestment = growth ÷ ROIIC; P/E column = today's price ÷ that year's EPS:

| Year | Growth | Revenue | NOPAT margin | NOPAT | Reinvestment % NOPAT | FCF | EPS | Price ÷ EPS |
|---|---|---|---|---|---|---|---|---|
| 1 | 29.9% | 6,188 | 7.3% | 452.0 | 149% | -223.2 | 8.56 | 25.7 |
| 2 | 26.9% | 7,852 | 7.4% | 584.0 | 134% | -201.2 | 11.06 | 19.9 |
| 3 | 23.9% | 9,728 | 7.6% | 736.5 | 120% | -143.8 | 13.95 | 15.8 |
| 5 | 17.9% | 13,873 | 7.8% | 1,087 | 90% | 112.4 | 20.59 | 10.7 |
| 7 | 12.0% | 17,854 | 8.1% | 1,446 | 60% | 581.5 | 27.39 | 8.0 |
| 10 | 3.0% | 21,239 | 8.5% | 1,805 | 15% | 1,535 | 34.19 | 6.4 |

> **Feasibility flag:** on this path reinvestment exceeds 100% of NOPAT (peak 149%), so FCF is negative and growth would need outside capital at ROIIC 20%. Either ROIIC is higher than assumed or the implied path is not self-fundable.

Reading: the price needs revenue of ~21,239 USD M by year 10 (4.5x today's) and terminal value is 85% of EV. Compare with what the business has shown (unit runway, reinvestment capacity, ROIIC), not with a consensus number.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 30% | 8.0% → 4.0% | 6.0% | 15% | 94.9 | -57% | 5.3% | 14.0 | 15.7 | 0.55x |
| base | 47% | 16.0% → 5.0% | 8.5% | 20% | 159.9 | -27% | 15.6% | 20.0 | 17.7 | 1.23x |
| bull | 21% | 22.0% → 7.0% | 9.5% | 25% | 231.9 | 5% | 22.3% | 26.0 | 19.8 | 2.11x |
| blow-up | 2% | — | — | — | 33.0 | -85% | — | — | — | 0.15x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 153.0 | -30% | -57% | 79% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.35, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (8%/yr) |
|---|---|---|---|---|---|---|---|---|
| 16% | 4% | 0% | 14% | 2% | 1.19x | 3.6% | 1.11x | 1.47x |

> **Exit-multiple gap:** in bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 34.0 on EPS 6.47. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 17.0 | exit P/E 25.5 | exit P/E 34.0 |
|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -42%) | 15% (r -0%) |
| 3x | 43% (r -63%) | 32% (r -26%) | 25% (r -0%) |
| 5x | 58% (r -43%) | 46% (r -18%) | 38% (r -0%) |

Track record for comparison: EPS CAGR 12.9% diluted EPS 3.12 (FY ended Feb-2020) -> 6.47 (Jan-2026), 6 years [XBRL].

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=0) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (price / base EPS) | 34.0 | n/a | INSUFFICIENT HISTORY (n=0 < 5) | n/a | n/a | no sector P/Es given |
| forward EPS | 21.8 | n/a | INSUFFICIENT HISTORY (n=0 < 5) | n/a | n/a | no sector P/Es given |

Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 7.5% | 190 (-14%) | 211 (-4%) | 242 (10%) | 279 (27%) | 322 (46%) |
| 8.5% | 155 (-29%) | 171 (-22%) | 193 (-12%) | 220 (-0%) | 250 (14%) |
| 9.5% | 131 (-40%) | 143 (-35%) | 160 (-27%) | 179 (-18%) | 202 (-8%) |
| 10.5% | 114 (-48%) | 123 (-44%) | 136 (-38%) | 150 (-32%) | 167 (-24%) |
| 11.5% | 101 (-54%) | 108 (-51%) | 118 (-47%) | 129 (-41%) | 141 (-36%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 6.5% | 7.5% | 8.5% | 9.5% | 10.5% |
|---|---|---|---|---|---|
| 2.0% | 122 (-44%) | 137 (-38%) | 151 (-31%) | 165 (-25%) | 180 (-18%) |
| 3.0% | 129 (-41%) | 144 (-34%) | 160 (-27%) | 175 (-20%) | 191 (-13%) |
| 4.0% | 138 (-37%) | 155 (-30%) | 172 (-22%) | 189 (-14%) | 206 (-7%) |

### Input notes
- PRICE IS NOT A QUOTE: $220 = BlackRock 13F value / shares at 30-Sep-2026 [EST in practice file]. No valuation work was done in the practice run; a live card must use a dated close.
- FY2025: net sales 4,764.1, operating income 457.4 (after SBC 34.7), net income 358.6, diluted EPS 6.47, diluted shares 55.4M, FCF 411.7 [10K25, XBRL].
- FCF 411.7 is a cyclical high (capex halved, payables build); practice file normalises to ~250-300 - so P/FCF here flatters.
- eps_forward 10.07 = midpoint of the FY2026 ADJUSTED EPS guide 9.83-10.31 [PR-Q2 FY26]; GAAP guide 12.10-12.58 carries the one-off $163.6M tariff refund and is not used.
- Net cash 932.2 [10K25: cash 723.7 + ST investments 208.5]; ~1.2B at Q2 FY26 incl. the refund. Operating leases 2,032 excluded because occupancy is inside COGS (rent is in the margin).
- ROIIC 20% [EST]: new-store investment ~$0.65M gross build-out + ~$0.14M DC capex per store + inventory, against ~$2M sales per new store.
- No own P/E history or peer P/Es in the practice file -> temperature shows trailing vs forward only.

Sources: research_notes/Deep dives/FIVE_practice.md

