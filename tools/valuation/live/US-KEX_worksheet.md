## Valuation worksheet: Kirby Corporation (US-KEX) · as of 2026-11-20

*Worksheet v1.2 (2026-11-23; non_operating_growth adds non-operating value to the 5-year multiple; 1.1 added bank mode). Money in USD M; per-share figures in USD. Cost of equity 9.5% (market default 9-10%), terminal growth 3.0%, 10-year explicit period, ROIIC 10%, terminal ROIC 10%.*

### Snapshot (FY2025 (to 31-Dec-2025))
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 122.89 | 6,390 | 1,034 | 7,424 | 19.4 | 9.5 | 15.8 | 6.3% | 11.1% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 122.89 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 11.1% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Revenue CAGR for 10 yrs, margin moving to base-case 11.0% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Year-1 growth, fading linearly to 3.0% by year 10 (margin to 11.0%) | none in tested range -30% to 120% (the price is outside what this path can produce) |
| NOPAT margin needed by year 10 on the base-case growth path (5.0% → 3.0%) | **21.7%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 3.8% |
| Expected return (IRR) the price offers if the base case happens | **6.8%** (vs cost of equity 9.5%) |

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 30% | 1.0% → 2.0% | 8.5% | 7% | 42.7 | -65% | -1.3% | 13.0 | 8.6 | 0.80x |
| base | 50% | 5.0% → 3.0% | 11.0% | 10% | 60.0 | -51% | 4.4% | 16.0 | 10.8 | 1.16x |
| bull | 18% | 8.0% → 4.0% | 13.0% | 13% | 83.8 | -32% | 8.9% | 19.0 | 12.7 | 1.63x |
| blow-up | 2% | — | — | — | 36.9 | -70% | — | — | — | 0.30x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 58.6 | -52% | -65% | 100% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.30, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (8%/yr) |
|---|---|---|---|---|---|---|---|---|
| 6% | 0% | 0% | 4% | 2% | 1.12x | 2.3% | 1.09x | 1.47x |

> **Exit-multiple gap:** in bear, base, bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 19.4 on EPS 6.33. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 9.7 | exit P/E 14.6 | exit P/E 19.4 | exit P/E 19.7 | exit P/E 21.5 |
|---|---|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -41%) | 15% (r -0%) | 15% (r 2%) | 13% (r 15%) |
| 3x | 43% (r -63%) | 32% (r -26%) | 25% (r -0%) | 24% (r 1%) | 22% (r 9%) |
| 5x | 59% (r -43%) | 46% (r -18%) | 38% (r -0%) | 38% (r 1%) | 35% (r 6%) |

Track record for comparison: EPS CAGR 4.4% diluted EPS 4.11 (2015) -> 6.33 (2025), 10 years [XBRL]; trough-to-peak 2.37 (2019) -> 6.33 is 17.8%/yr, which is cycle, not trend.

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=9) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (price / base EPS) | 19.4 | 0.90x | NORMAL | 33% | 0.99x | NORMAL |
| forward EPS | 17.0 | 0.79x | COOL | 22% | 0.86x | COOL |

Own P/E history: FY2015 12.8, FY2016 25.4, FY2017 11.9, FY2018 51.4, FY2019 37.8, FY2022 31.7, FY2023 21.1, FY2024 21.5, FY2025 17.4 (median 21.5).
Sector P/Es: Matson (Jones Act liner) 14.5, Cummins (engine OEM) 19.7, Generac (FY25 EPS depressed, not comparable) 71.8 (median 19.7).
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 7.5% | 87 (-29%) | 92 (-25%) | 98 (-20%) | 107 (-13%) | 117 (-5%) |
| 8.5% | 70 (-43%) | 73 (-41%) | 76 (-38%) | 80 (-35%) | 84 (-31%) |
| 9.5% | 57 (-53%) | 59 (-52%) | 60 (-51%) | 61 (-50%) | 62 (-49%) |
| 10.5% | 48 (-61%) | 49 (-60%) | 49 (-60%) | 48 (-61%) | 47 (-62%) |
| 11.5% | 42 (-66%) | 41 (-67%) | 40 (-67%) | 38 (-69%) | 35 (-72%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 9.0% | 10.0% | 11.0% | 12.0% | 13.0% |
|---|---|---|---|---|---|
| 2.0% | 48 (-61%) | 53 (-57%) | 59 (-52%) | 65 (-47%) | 71 (-42%) |
| 3.0% | 48 (-61%) | 54 (-56%) | 60 (-51%) | 66 (-46%) | 72 (-42%) |
| 4.0% | 49 (-60%) | 55 (-55%) | 61 (-50%) | 67 (-45%) | 73 (-41%) |

### Input notes
- Price 122.89 = NYSE close 20-Nov-2026 [Yahoo v8 KEX] = Nasdaq.com historical close 20-Nov-2026 (two sources). Shares 52.0M [10-Q Q3 2026 cover, ~Oct-2026]; 0.3M more bought to 5-Nov-2026.
- Net debt 1,033.5 = debt 1,071.8 - cash 38.3 at 30-Sep-2026 [PR-Q3-26]; the $115M barge/fleeting acquisition closed 4-Nov-2026 (debt-funded, not yet in this figure); operating lease liabilities 215.6 [10K25] excluded because charter/lease cost sits inside operating margin.
- Base FY2025 [XBRL, PR-Q4-25]: revenue 3,364.1 (KMT 1,935.3, KDS 1,428.7), operating income 496.3, net earnings 354.6, EPS 6.33 (no one-time items in 2025; 2024 adjusted 5.46), FCF 405.7 (CFO 670.2 - capex 264.5), SBC 17.6, adjusted EBITDA 781 [DEF 14A].
- eps_forward 7.24 = FY2026 guide 'EPS growth 10-15%, toward the upper end' [PR-Q3-26] applied to 6.33 -> 6.96-7.28; 7.24 = ~14.4%. 9M-2026 EPS 5.26 [10Q3-26].
- ROIIC 10% [EST]: proxy 3-yr Return on Total Capital 10.4% (2023-25 performance award, DEF 14A); unit economics (deep dive section 4) say new-build barges earn ~6-8% pre-tax at current rates, acquisitions of used barges more.
- payout_of_fcf 0.75: 2025 buybacks 354.2 vs FCF 405.7; no dividend. Buybacks are treated as distributions.
- pe_history: FY-end close [Yahoo v8] / diluted EPS [XBRL]. 2020 and 2021 omitted (losses, impairments); 2017 includes a tax-reform gain; 2018-19 depressed EPS. Own band is noisy; median ~21.5.
- Peer P/Es on FY2025 diluted EPS [XBRL] and 20-Nov-2026 closes [Yahoo]: MATX 200.05/13.81, CMI 403.61/20.50, GNRC 193.22/2.69 (depressed). No pure inland-barge peer is listed (ACBL, Canal, Ingram, Marquette are private). Single-source.

Sources: research_notes/Deep dives/US-KEX_live.md; https://www.sec.gov/Archives/edgar/data/56047/000119312526054016/kex-20251231.htm; https://www.sec.gov/Archives/edgar/data/56047/000119312526436155/kex-ex99_1.htm; https://www.sec.gov/Archives/edgar/data/56047/000119312526451723/kex-20260930.htm

