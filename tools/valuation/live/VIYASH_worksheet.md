## Valuation worksheet: Viyash Scientific Ltd (formerly SeQuent Scientific; human + animal-health APIs, animal-health formulations (Alivira), US human generics via 60%-owned Appco Pharma) (VIYASH) · as of 2026-11-25

*Worksheet v1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode). Money in INR cr; per-share figures in INR. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, ROIIC 15%, terminal ROIC 13%.*

### Snapshot (TTM Sep-2026 (Q3 FY26..Q2 FY27), attributable basis (group lines x 0.86 for the 40% minorities in Appco Pharma and the Karizoo group))
| Price | Market cap | Net debt (−=cash) | EV | P/E | EV/EBITDA | P/FCF | FCF yield | NOPAT margin |
|---|---|---|---|---|---|---|---|---|
| 228.88 | 11,062 | -380.0 | 10,682 | 47.6 | 17.7 | 55.9 | 1.8% | 9.3% (base.ebit x (1 - tax) / revenue) |

### (a) Reverse DCF: what today's price implies
| Question | Implied by price 228.88 |
|---|---|
| Revenue CAGR for 10 yrs, NOPAT margin flat at 9.3% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Revenue CAGR for 10 yrs, margin moving to base-case 12.5% | none in tested range -30% to 80% (the price is outside what this path can produce) |
| Year-1 growth, fading linearly to 5.0% by year 10 (margin to 12.5%) | none in tested range -30% to 120% (the price is outside what this path can produce) |
| NOPAT margin needed by year 10 on the base-case growth path (14.0% → 8.0%) | **35.4%** |
| Gordon check: perpetual FCF growth implied by trailing FCF yield | 10.5% |
| ROIIC the price implies on the base-case growth and margin path | none in tested range 1% to 300% (the price is outside what this path can produce) |
| Expected return (IRR) the price offers if the base case happens | **8.4%** (vs cost of equity 12.5%) |

Reinvestment realism (v1.3): last-5y incremental ROIC **15.0%** (given). Flag when a ROIIC used or implied differs by more than 5%:

| ROIIC | Value | Gap vs history | Flag |
|---|---|---|---|
| default ROIIC (input) | 15.0% | +0.0 pts | ok |
| scenario bear | 9.0% | -6.0 pts | **FLAG** |
| scenario base | 15.0% | +0.0 pts | ok |
| scenario bull | 20.0% | +5.0 pts | **FLAG** |
| implied by price on the base-case path | none in tested range 1-300% | n/a | ok |

> **Reinvestment-realism flag:** scenario bear; scenario bull. Either the business will earn on new capital what it has not earned recently, or the path is mis-specified (e.g. pricing-led growth that needs little capital). Say which in the deep dive.

### (b) Scenario DCF and 5-year outcome distribution
| Scenario | Prob | Growth yr1 → yr10 | NOPAT margin yr10 | ROIIC | DCF value/sh | vs price | EPS CAGR 5y | Exit P/E used | DCF-consistent P/E yr5 | 5-yr multiple (incl. distributions) |
|---|---|---|---|---|---|---|---|---|---|---|
| bear | 30% | 7.0% → 5.0% | 9.5% | 9% | 52.5 | -77% | 6.8% | 15.0 | 12.7 | 0.44x |
| base | 45% | 14.0% → 8.0% | 12.5% | 15% | 89.2 | -61% | 16.4% | 24.0 | 14.8 | 1.08x |
| bull | 18% | 18.0% → 10.0% | 14.0% | 20% | 127.2 | -44% | 21.6% | 32.0 | 17.2 | 1.80x |
| blow-up | 7% | — | — | — | 80.1 | -65% | — | — | — | 0.35x |

| Probability-weighted DCF value | vs price | Bear-case downside | P(DCF value < price) |
|---|---|---|---|
| 84.4 | -63% | -77% | 100% |

5-year price outcomes (each scenario's multiple ± lognormal dispersion σ=0.40, blow-up as a point mass):

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (12%/yr) |
|---|---|---|---|---|---|---|---|---|
| 10% | 2% | 0% | 27% | 7% | 0.97x | -0.7% | 0.88x | 1.76x |

> **Exit-multiple gap:** in base, bull the exit P/E used is >1.25x the DCF-consistent P/E at year 5. Those 5-year multiples assume the market keeps paying more than this worksheet's own cost of equity justifies. Show the card both ways (set `exit_pe` to "dcf" to test).

**Exit-multiple bet (v1.3, L21).** The 5-year multiple is a bet on the P/E the market pays in year 5. Own median P/E: n/a (n=1 < 5).

| Scenario | Exit P/E used | DCF-consistent P/E yr5 | Own median P/E | Used ÷ DCF | Used ÷ own | 5-yr multiple at used | at DCF P/E | at own median |
|---|---|---|---|---|---|---|---|---|
| bear | 15.0 | 12.7 | n/a | 1.18x | n/a | 0.44x | 0.38x | n/a |
| base | 24.0 | 14.8 | n/a | 1.62x | n/a | 1.08x | 0.67x | n/a |
| bull | 32.0 | 17.2 | n/a | 1.87x | n/a | 1.80x | 0.97x | n/a |
| **EV (incl. blow-up)** | | | | | | **0.97x** | **0.61x** | **n/a** |

Hurdle 1.76x. The card's gate uses the stated exit; the other two columns show how much of the answer is the multiple bet.

Base rates for these probabilities live in the decision card (stage 6), not here.

### (c) Twin engine: EPS growth needed × exit multiple
Starting P/E 47.6 on EPS 4.81. Cell = EPS CAGR needed over 5 years; (r) = share of the return that must come from re-rating (negative = de-rating eats part of EPS growth).

| Target | exit P/E 23.8 | exit P/E 35.7 | exit P/E 46.2 | exit P/E 47.6 |
|---|---|---|---|---|
| 2x | 32% (r -100%) | 22% (r -42%) | 16% (r -4%) | 15% (r 0%) |
| 3x | 43% (r -63%) | 32% (r -26%) | 25% (r -3%) | 25% (r 0%) |
| 5x | 58% (r -43%) | 46% (r -18%) | 39% (r -2%) | 38% (r 0%) |

Base rates to read this against: Indian winners got ~2/3 of their return from EPS and ~1/3 from re-rating over long runs; when more than half of a gain is multiple, it is fragile (`insight:india-mb-twin-engine-base-rate`). Starting P/E ≥35 had a median outcome of ~19x vs ~266x from ≤15 in our winner library, survivorship-biased (`insight:india-mb-starting-pe`).

### (d) Valuation temperature
| Basis | P/E | vs own median (n=1) | Own band | Percentile in own history | vs sector median | Sector band |
|---|---|---|---|---|---|---|
| trailing (given) | 47.6 | n/a | INSUFFICIENT HISTORY (n=1 < 5) | n/a | 1.03x | NORMAL |
| core EPS (ex exceptional, ex other income) | 48.7 | n/a | INSUFFICIENT HISTORY (n=1 < 5) | n/a | 1.05x | NORMAL |

Own P/E history: FY26 44.7 (median 44.7).
Sector P/Es: Granules India 32.5, Neuland Laboratories 59.9, Aarti Drugs 19.5, Solara Active Pharma 62.6 (median 46.2).
Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average.
Trailing P/E **47.6** vs core P/E **48.7** (core EPS 4.70, ex exceptional items and ex other income, after interest; (PAT 232.6 - (exceptional -35.5 + other income 43.0) x (1 - tax 28%)) / shares): core is +2% vs the trailing P/E.
Bands (P/E ÷ reference): <0.7 cold, 0.7–0.9 cool, 0.9–1.1 normal, 1.1–1.5 warm, 1.5–2 hot, ≥2 very hot. ≥2x own median preceded 4–6 flat years even with EPS growth (L12, `insight:flag-high-pe-context`).

### (e) Sensitivity (base case; value per share, and vs price)
Cost of equity (rows) × shift in base-case growth path (columns; year-10 growth shifts by half):

| CoE \ Δgrowth | -6 pp | -3 pp | +0 pp | +3 pp | +6 pp |
|---|---|---|---|---|---|
| 10.5% | 109 (-52%) | 120 (-48%) | 131 (-43%) | 144 (-37%) | 159 (-31%) |
| 11.5% | 92 (-60%) | 99 (-57%) | 107 (-53%) | 115 (-50%) | 124 (-46%) |
| 12.5% | 80 (-65%) | 84 (-63%) | 89 (-61%) | 94 (-59%) | 100 (-56%) |
| 13.5% | 71 (-69%) | 73 (-68%) | 76 (-67%) | 79 (-66%) | 81 (-64%) |
| 14.5% | 63 (-72%) | 65 (-72%) | 66 (-71%) | 67 (-71%) | 68 (-70%) |

Terminal growth (rows) × year-10 NOPAT margin (columns):

| TG \ margin | 10.5% | 11.5% | 12.5% | 13.5% | 14.5% |
|---|---|---|---|---|---|
| 4.0% | 76 (-67%) | 82 (-64%) | 88 (-61%) | 94 (-59%) | 100 (-56%) |
| 5.0% | 77 (-66%) | 83 (-64%) | 89 (-61%) | 95 (-58%) | 101 (-56%) |
| 6.0% | 78 (-66%) | 84 (-63%) | 90 (-60%) | 97 (-58%) | 103 (-55%) |

### Input notes
- RUN LOG: this file is run 1, the inputs as written before any output (adopted). A run-2 sensitivity added nopat_margin 0.119 (economic margin: ESOP at the 25 cr steady state, no acquired-intangible amortisation) and gave EV 0.85x (base 0.94x) - LOWER, because the worksheet grows EPS from base.eps 4.81 with NOPAT, so a higher starting margin leaves less margin expansion. Neither run lets the ESOP/amortisation roll-off lift EPS as a step in FY28 (bottom-up FY28 EPS ~10.3 diluted vs worksheet base EPS5 ~10.3 in year 5): a worksheet limitation logged as a lesson candidate. Run 2 is reported, not used.
- Price Rs 228.88 = NSE bhavcopy close 25-Nov-2026 (sec_bhavdata_full_25112026.csv, DATE1 25-Nov-2026) = Yahoo v8 VIYASH.NS close 25-Nov-2026 (two sources). screener.in 26-Nov-2026: Rs 229, mcap Rs 10,128 cr.
- Shares 48.33 cr FULLY DILUTED [EST]: 44.16 cr issued (paid-up Rs 88.32 cr / Rs 2 face, Q2 FY27 XBRL; NSE pledge API totIssuedShares 441,627,670 at SHP 30-Sep-2026) + 2.034 cr warrants held by MD Dr Haribabu Bodepudi (issue price Rs 181.94, 25% paid, Rs 277.57 cr due on conversion within 18 months of allotment, AR26) + ~2.14 cr ESOP options [EST: 0.84 cr left of the 1.32 cr outstanding at 31-Mar-2026 (AR26 note) after ~0.48 cr allotted Apr-Nov 2026, plus 1.3 cr granted in Q1 FY27 (CFO, Aug-2026 call)].
- Net debt -380 [EST] = Sep-2026 borrowings 531.03 (52.40 non-current + 478.63 current) - cash 492.54 - other bank 12.34 = 26.1 (XBRL; company deck/call 'Rs 26 cr' = two sources), less warrant money 277.6 and option money ~128 [EST, avg Rs 60 strike] that conversion brings in. Lease liabilities (~Rs 54 cr at Mar-2026) ignored.
- Attributable scaling 0.86: non-controlling interests took 46.25 of 278.84 TTM PAT (16.6%) and 21.90 of 163.94 in H1 FY27 (13.4%) [XBRL]; NCI = 40% of Appco Pharma LLC (USA; Rs 88 cr of FY26 entity profit, AR26 note 49) and 40% of the Karizoo/Vila Vina/Phytotherapic group (Spain/Mexico). Management intends to buy out minorities 'in the second year' after acquisitions (Nov-2026 call) - a future cash use not modelled.
- Base TTM group [XBRL Q3 FY26, Q4 FY26, Q1 FY27, Q2 FY27 consolidated; screener quarterlies agree to the crore]: revenue 858.41 + 919.96 + 946.36 + 987.94 = 3,712.67; other income 13.98 + 15.92 + 8.31 + 11.78 = 49.99; finance 57.49; D&A 58.53 + 60.41 + 61.77 + 45.33 = 226.04; PBT before exceptional 469.66; exceptional -41.26 (Q3 FY26 only); PAT 278.84; owners 232.59; EBITDA = 469.66 + 57.49 + 226.04 - 49.99 = 703.2 (screener OP 703); EBIT ex OI 477.2. x0.86 -> revenue 3,192.9, EBITDA 604.8, EBIT 410.3.
- L44 core EPS: exceptional_items_cr -35.5 and other_income_cr 43.0 are the TTM group items x 0.86 (pre-tax, gains positive). base.pat is the REPORTED owners' PAT (232.6), so the worksheet strips them once - no double subtraction. Net effect small (+7.5 cr pre-tax).
- What the TTM P/E hides (not stripped; real costs, but temporary in size): ESOP cost TTM 79.9 cr (7.9 + 5.3 + 24.6 + 42.1, decks) vs management's steady state ~25 cr/yr (FY27 ~148-149, FY28 ~32, CFO Nov-2026); acquired-intangible amortisation inside D&A ~84 cr TTM (FY26 ~100; Q1 FY27 25, Q2 8.9, Q3 ~4, then nil, per calls) -> together ~139 cr pre-tax (~Rs 2.1/diluted share after tax and minorities). The dilution from the merger ESOP grants is already in the 48.33 cr share count; the base margin path carries only the ~25 cr steady-state ESOP (sbc 68.7 = TTM 79.9 x 0.86 shown for reference).
- NOPAT margin today 410.3 x 0.72 / 3,192.9 = 9.3%; with ESOP at 25 and no amortisation ~11.9%. Scenarios (written before outputs; tails started from the India class 21%/11%/15%): bear 30% = API price competition from China plus US generic erosion, Carlyle exit overhang, growth 7% -> 5%, NOPAT margin 9.5%, ROIIC 9%, exit 15x (Aarti Drugs 19.5x less a discount); base 45% = mid-teens revenue growth (management guides 20%+ FY27 incl. BioForLife; we assume 14% fading to 8%), margin 12.5% as ESOP/amortisation roll off plus modest operating leverage, ROIIC 15%, exit 24x (below the peer median 32.5x as growth fades; FY26 exit 44.7x was on merger-depressed EPS); bull 18% = USD 1 bn by 2032 path (17-18% CAGR), companion-animal launches 2029+, oncology FDF, margin 14%, ROIIC 20%, exit 32x (peer median).
- ROIIC 15% [EST]: the only measurable window, FY25 restated (EBIT ex OI 148, IC ~3,016) -> TTM (477, IC ~3,473), gives ~52% - a merger/turnaround trough-to-recovery window that L38 forbids using. TTM ROIC on Sep-2026 IC (owners' equity 3,164.7 + NCI 228.5 + net debt 26.1 + leases ~54 = 3,473): 477.2 x 0.72 / 3,473 = 9.9% (13.2% ex goodwill 877); with ESOP/amortisation normalised ~12.8%.
- Tax 28%: H1 FY27 effective 28.7% (66.15 / 230.09); Q4 FY26 47% incl. Rs 16 cr regime-change deferred-tax charge.
- FCF 198 [EST] = ~230 group x 0.86: FY26 CFO 323 - capex ~98 = FCF 225 [SCR]; H1 FY27 CFO 182.7 - capex 67.4 = 115 [XBRL]. Capex guide Rs 150-170 cr/yr (Nov-2026 call). BioForLife (EUR 16.976 m ~ Rs 170 cr, closed 1-Oct-2026) is an acquisition outside FCF.
- Exit P/Es: own history is one year (FY26: Mar-2026 close Rs 182.8 / EPS 4.09 = 44.7x) because the listed entity changed; SeQuent's FY17-25 P/Es are a different, smaller animal-health business and are NOT used. Peers [screener 26-Nov-2026, consolidated]: Granules 32.5x, Neuland 59.9x, Aarti Drugs 19.5x, Solara 62.6x (depressed earnings); median of the three earning peers 32.5x.
- Dispersion 0.40: price Rs 126.7 (7-Apr-2025 low) -> 294.2 (3-Jul-2026 high) -> 228.9 [YH].

Sources: research_notes/Deep dives/VIYASH_live.md; https://nsearchives.nseindia.in/annual_reports/AR_29856_VIYASH_2025_2026_A_10469798_17072026165453.pdf; https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1757557_13112026055107_WEB.xml; https://nsearchives.nseindia.in/corporate/SEQUENT2_13112026184257_SE_Intimation_Investor_Presentation.pdf; https://nsearchives.nseindia.in/corporate/SEQUENT2_17112026182841_SE_Intimation_Earnings_Transcript.pdf; https://www.screener.in/company/VIYASH/consolidated/; https://nsearchives.nseindia.in/products/content/sec_bhavdata_full_25112026.csv

