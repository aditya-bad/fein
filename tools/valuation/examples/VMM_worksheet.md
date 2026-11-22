## Valuation worksheet: Vishal Mega Mart (VMM) · as of 2026-11-20

> **TEST MATERIAL. No verdict.** These inputs exist to exercise the template (lesson L9). The scenario assumptions are illustrative [EST], not research conclusions. Research, not SEBI-registered advice.

*Worksheet v1.0 (2026-11-21). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 30%, terminal ROIC 25%.*

### Snapshot (FY26)
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 91.50 | 42,849 | 0.0 | 42,849 | 47.7 | 33.7 | n/a | n/a | 6.2% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 91.50 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 6.2% | **31.9%** |
| Revenue CAGR for 10 yrs, margin moving to base-case 7.0% | **30.0%** |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 7.0%) | **53.7%** |
| NOPAT margin needed by year 10 on the base-case growth path (18.0% → 8.0%) | **20.5%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | n/a |
| Expected return (IRR) the price offers if the base case happens | **8.2%** (vs cost of equity 12.5%) |

Implied path (fade-to-terminal case). Reinvestment = growth ÷ ROIIC; P/E column = today's price ÷ that year's EPS:

| Year | Growth | Revenue | NOPAT margin | NOPAT | Reinvestment % NOPAT | FCF | EPS | Price ÷ EPS |
|---|---|---|---|---|---|---|---|---|
| 1 | 53.7% | 19,837 | 6.3% | 1,250 | 179% | -987.5 | 2.79 | 32.8 |
| 2 | 48.3% | 29,416 | 6.4% | 1,876 | 161% | -1,144 | 4.19 | 21.9 |
| 3 | 42.9% | 42,028 | 6.5% | 2,714 | 143% | -1,165 | 6.05 | 15.1 |
| 5 | 32.1% | 76,294 | 6.6% | 5,045 | 107% | -345.6 | 11.25 | 8.1 |
| 7 | 21.2% | 117,138 | 6.8% | 7,927 | 71% | 2,317 | 17.68 | 5.2 |
| 10 | 5.0% | 157,286 | 7.0% | 11,010 | 17% | 9,175 | 24.56 | 3.7 |

> **Feasibility flag:** on this path reinvestment exceeds 100% of NOPAT (peak 179%), so FCF is negative and growth would need outside capital at ROIIC 30%. Either ROIIC is higher than assumed or the implied path is not self-fundable.

Reading: the price needs revenue of ~157,286 INR cr by year 10 (12.2x today's) and terminal value is 89% of EV. Compare with what the business has shown (unit runway, reinvestment capacity, ROIIC), not with a consensus number.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 30% | 12.0% → 6.0% | 5.0% | 20% | 18.5 | -80% | 8.4% | 25.0 | 12.0 | 0.73x |
| base | 45% | 18.0% → 8.0% | 7.0% | 30% | 34.1 | -63% | 17.2% | 35.0 | 15.1 | 1.51x |
| bull | 23% | 22.0% → 10.0% | 8.0% | 35% | 47.8 | -48% | 22.5% | 45.0 | 17.1 | 2.44x |
| blow-up | 2% | — | — | — | 13.7 | -85% | — | — | — | 0.15x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 32.2 | -65% | -80% | 100% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.30, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 25% | 6% | 0% | 5% | 2% | 1.46x | 7.9% | 1.40x | 1.76x |

> **Exit-multiple gap:** in bear, base, bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 47.7 on EPS 1.92. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 23.9 | exit P/E 35.8 | exit P/E 47.7 | exit P/E 55.1 |
|---|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -41%) | 15% (r 0%) | 12% (r 21%) |
| 3x | 43% (r -63%) | 32% (r -26%) | 25% (r 0%) | 21% (r 13%) |
| 5x | 58% (r -43%) | 46% (r -18%) | 38% (r 0%) | 34% (r 9%) |

Track record for comparison: EPS CAGR 30.0% FY24-26 (2 years only; IPO Dec-2024) [practice file].

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=2) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 47.7 | n/a | INSUFFICIENT HISTORY (n=2 < 5) | n/a | 0.87x | COOL |

Own P/E history: IPO year (FY25) 76.0, 2026-11-20 47.7 (median 61.9).
Sector P/Es: DMart 73.5, V2 Retail 36.7 (median 55.1).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 37 (-60%) | 43 (-53%) | 50 (-46%) | 58 (-37%) | 67 (-27%) |
| 11.5% | 31 (-66%) | 35 (-61%) | 41 (-56%) | 47 (-49%) | 54 (-41%) |
| 12.5% | 26 (-71%) | 30 (-67%) | 34 (-63%) | 39 (-57%) | 44 (-51%) |
| 13.5% | 23 (-75%) | 26 (-72%) | 29 (-68%) | 33 (-64%) | 37 (-59%) |
| 14.5% | 20 (-78%) | 23 (-75%) | 25 (-72%) | 28 (-69%) | 32 (-65%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 5.0% | 6.0% | 7.0% | 8.0% | 9.0% |
|---|---|---|---|---|---|
| 4.0% | 24 (-73%) | 28 (-69%) | 32 (-65%) | 36 (-60%) | 40 (-56%) |
| 5.0% | 26 (-72%) | 30 (-67%) | 34 (-63%) | 38 (-58%) | 43 (-53%) |
| 6.0% | 27 (-70%) | 32 (-65%) | 36 (-60%) | 41 (-55%) | 46 (-50%) |

### Input notes
- Price, market cap, P/E 47.7 [SCR 20-Nov-2026]. Shares 468.3 cr [EST: mcap 42,852 / 91.5].
- Revenue 12,906 cr, PAT 839 cr, D&A 673 cr incl. ROU 479 cr [AR26]. EBITDA is PRE-Ind AS 116: 1,271 cr (9.8%) [AR26/HSIE], because rent is a real operating cost (protocol trap).
- EBIT 1,077 cr [EST: pre-Ind AS EBITDA 1,271 - non-ROU D&A 194]. Tax 25.4% [EST: 1 - PAT/PBT]. ESOP cost 50 cr is already inside employee cost.
- Net debt 0: bank debt nil [AR26, HSIE]; lease liabilities 1,988 cr excluded because rent is inside the pre-Ind AS margin; cash balance not in the practice file (understates value slightly).
- FCF not in the practice file (capex 322 cr [HSIE]; CFO not recorded) - left null, so P/FCF and the Gordon check are n/a.
- ROIIC 30% [EST]: between RoTE ~27% and HSIE ex-goodwill ROIC 57%; new-state stores at lower density argue for the low end.
- Own P/E history: 2 points only (listed Dec-2024) -> own-median test impossible (practice file override table).

Sources: research_notes/Deep dives/VMM_practice.md

