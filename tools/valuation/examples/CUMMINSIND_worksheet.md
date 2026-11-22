## Valuation worksheet: Cummins India (CUMMINSIND) · as of 2026-11-21

> **TEST MATERIAL. No verdict.** These inputs exist to exercise the template (lesson L9). The scenario assumptions are illustrative [EST], not research conclusions. Research, not SEBI-registered advice.

*Worksheet v1.0 (2026-11-21). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 40%, terminal ROIC 30%.*

### Snapshot (FY26)
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 4,100 | 113,652 | -3,900 | 109,752 | 52.0 | 42.3 | 76.4 | 1.3% | 14.8% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 4,100 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 14.8% | **30.9%** |
| Revenue CAGR for 10 yrs, margin moving to base-case 14.5% | **31.2%** |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 14.5%) | **56.2%** |
| NOPAT margin needed by year 10 on the base-case growth path (12.0% → 7.0%) | none in tested range -5% to 60% (the price is outside what this path can produce) |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 11.0% |
| Expected return (IRR) the price offers if the base case happens | **7.3%** (vs cost of equity 12.5%) |

Implied path (fade-to-terminal case). Reinvestment = growth ÷ ROIIC; P/E column = today's price ÷ that year's EPS:

| Year | Growth | Revenue | NOPAT margin | NOPAT | Reinvestment % NOPAT | FCF | EPS | Price ÷ EPS |
|---|---|---|---|---|---|---|---|---|
| 1 | 56.2% | 18,973 | 14.8% | 2,802 | 141% | -1,138 | 121.44 | 33.8 |
| 2 | 50.6% | 28,565 | 14.7% | 4,210 | 126% | -1,111 | 173.61 | 23.6 |
| 3 | 44.9% | 41,380 | 14.7% | 6,087 | 112% | -739.6 | 242.98 | 16.9 |
| 5 | 33.5% | 76,861 | 14.6% | 11,260 | 84% | 1,838 | 433.85 | 9.5 |
| 7 | 22.1% | 119,899 | 14.6% | 17,493 | 55% | 7,835 | 663.69 | 6.2 |
| 10 | 5.0% | 162,197 | 14.5% | 23,519 | 13% | 20,579 | 886.94 | 4.6 |

> **Feasibility flag:** on this path reinvestment exceeds 100% of NOPAT (peak 141%), so FCF is negative and growth would need outside capital at ROIIC 40%. Either ROIIC is higher than assumed or the implied path is not self-fundable.

Reading: the price needs revenue of ~162,197 INR cr by year 10 (13.4x today's) and terminal value is 80% of EV. Compare with what the business has shown (unit runway, reinvestment capacity, ROIIC), not with a consensus number.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 30% | 7.0% → 5.0% | 12.0% | 30% | 978.8 | -76% | 4.2% | 30.0 | 11.7 | 0.83x |
| base | 48% | 12.0% → 7.0% | 14.5% | 40% | 1,297 | -68% | 9.2% | 40.0 | 13.3 | 1.35x |
| bull | 21% | 17.0% → 8.0% | 16.0% | 50% | 1,654 | -60% | 13.6% | 50.0 | 14.7 | 2.03x |
| blow-up | 1% | — | — | — | 1,025 | -75% | — | — | — | 0.25x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 1,274 | -69% | -76% | 100% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.30, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 16% | 2% | 0% | 2% | 1% | 1.33x | 5.8% | 1.27x | 1.76x |

> **Exit-multiple gap:** in bear, base, bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 52.0 on EPS 78.85. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 26.0 | exit P/E 39.0 | exit P/E 52.0 | exit P/E 57.5 |
|---|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -42%) | 15% (r -0%) | 13% (r 15%) |
| 3x | 43% (r -63%) | 32% (r -26%) | 25% (r -0%) | 22% (r 9%) |
| 5x | 58% (r -43%) | 46% (r -18%) | 38% (r -0%) | 35% (r 6%) |

Track record for comparison: EPS CAGR 30.0% PAT FY21 618 -> FY26 2,330 cr, from a cyclical low (FY15 786 -> FY21 618 was negative) [SCR].

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=0) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 52.0 | n/a | INSUFFICIENT HISTORY (n=0 < 5) | n/a | 0.90x | NORMAL |

Sector P/Es: Kirloskar Oil Engines 57.5 (median 57.5).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 1,421 (-65%) | 1,557 (-62%) | 1,754 (-57%) | 1,986 (-52%) | 2,258 (-45%) |
| 11.5% | 1,225 (-70%) | 1,334 (-67%) | 1,490 (-64%) | 1,672 (-59%) | 1,886 (-54%) |
| 12.5% | 1,081 (-74%) | 1,171 (-71%) | 1,297 (-68%) | 1,444 (-65%) | 1,616 (-61%) |
| 13.5% | 971 (-76%) | 1,046 (-74%) | 1,150 (-72%) | 1,271 (-69%) | 1,411 (-66%) |
| 14.5% | 884 (-78%) | 947 (-77%) | 1,035 (-75%) | 1,136 (-72%) | 1,252 (-69%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 12.5% | 13.5% | 14.5% | 15.5% | 16.5% |
|---|---|---|---|---|---|
| 4.0% | 1,123 (-73%) | 1,175 (-71%) | 1,226 (-70%) | 1,278 (-69%) | 1,330 (-68%) |
| 5.0% | 1,187 (-71%) | 1,242 (-70%) | 1,297 (-68%) | 1,352 (-67%) | 1,407 (-66%) |
| 6.0% | 1,269 (-69%) | 1,329 (-68%) | 1,389 (-66%) | 1,449 (-65%) | 1,509 (-63%) |

### Input notes
- Price 4,100, market cap 1,13,652 cr, P/E 52.0 [SCR 21-Nov-2026]; shares 27.72 cr [AR26].
- FY26 standalone: revenue 12,143, EBITDA ~2,595 (21.4%), D&A 199, PAT 2,330, FCF 1,487 cr [AR26, SCR]. EBIT 2,396 = core (ex other income).
- Margin path starts from FY26 core NOPAT margin 14.8%; Q2 FY27 OPM had fallen to ~15% EBITDA (lag/one-off true-up) - the bear case assumes part of that is structural.
- Net cash ~3,900 cr [single-source: analyst on CC-Q2FY27 'INR 38-40 billion'; borrowings 37 cr are leases]. Treasury income is therefore NOT valued separately.
- Treasury income ~198 cr post-tax [EST: interest 189 + MF gains 75 = 264 x 0.75] is held flat in the EPS path (the cash itself is in net debt).
- Recurring non-treasury other income ~302 cr post-tax [EST: rent 186 + associate/JV dividends 217 = 403 pre-tax x 0.75], valued as a growing perpetuity.
- payout_of_fcf 1.0: FY26 FCF 1,487 ~= dividends 1,483 cr [SCR, AR26].
- ROIIC 40% [EST]: below the 58% core ROCE because part of the DC capital sits in sister companies (practice file: 'ROCE borrowed from the group').
- No own P/E history in the practice file -> own-median test not run (add 10 FY-end P/Es before a live use).

Sources: research_notes/Deep dives/CUMMINSIND_practice.md

