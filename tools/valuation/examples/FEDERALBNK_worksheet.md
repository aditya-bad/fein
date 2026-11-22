## Valuation worksheet (bank mode): The Federal Bank Ltd (FEDERALBNK) · as of 2026-11-20

> **TEST MATERIAL. No verdict.** Inputs exist to exercise the template (lesson L9). Scenario ROEs and exit P/Bs are illustrative [EST]. Research, not SEBI-registered advice.

*Worksheet v1.1-bank (2026-11-22). Money in INR cr. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, payout 8%. Book is fully diluted for pending issues.*

> Note: fully diluted: +27.30 cr shares, +4647 cash to be received; BVPS 160.44 -> 167.06

### Snapshot
| Price | Mcap (diluted) | BVPS undiluted → diluted | P/B undiluted → diluted | P/E | ROE (reported) |
|---|---|---|---|---|---|
| 373.50 | 102,551 | 160.44 → 167.06 | 2.33x → 2.24x | 22.1 | 13.6% |

### (a) Reverse P/B: what today's price needs
| Question | Answer |
|---|---|
| ROE needed forever (Gordon: g + P/B × (CoE − g)) | **21.8%** |
| ROE needed for 10 years, then only CoE (no franchise value left) | 22.4% |
| Cost of equity the market is using if today's ROE (10.1% on diluted book) is permanent | **7.3%** (ours 12.5%) |
| Justified P/B on the base case's long-run ROE 14.0% | 1.20x |
| IRR the price offers if the base case happens | **10.0%** (hurdle 12.0%) |

### (b) Residual-income scenarios
| Scenario | Prob | ROE start → end | RIM value | vs price | BVPS yr 5 | Exit P/B used | RIM-consistent P/B yr 5 | 5-yr multiple |
|---|---|---|---|---|---|---|---|---|
| bear | 35% | 10.5% → 11.0% | 117.1 | -69% | 266.2 | 1.30x | 0.75x | 0.95x |
| base | 45% | 12.0% → 14.0% | 205.9 | -45% | 287.2 | 1.80x | 1.25x | 1.41x |
| bull | 18% | 13.5% → 16.0% | 287.3 | -23% | 306.9 | 2.60x | 1.64x | 2.17x |
| blow-up | 2% | — | — | — | — | — | — | 0.30x |

> **Exit-multiple gap:** in bear, base, bull the exit P/B is >1.3× what the residual-income path justifies at our CoE. That part of the return is a bet on the market paying up (L21).

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV multiple (CAGR) | Median | Hurdle | Prob-weighted RIM value |
|---|---|---|---|---|---|---|---|---|
| 17% | 3% | 0% | 3% | 2% | 1.36x (6.4%) | 1.30x | 1.76x | 187.6 (-50%) |

### (c) Twin engine on book: BVPS CAGR needed (5 yrs, ignoring dividends) from P/B 2.24x
| Target | exit P/B 1.34x | exit P/B 1.38x | exit P/B 1.79x | exit P/B 2.24x |
|---|---|---|---|---|
| 2x | 27% (re-rating -74%) | 27% (re-rating -70%) | 20% (re-rating -32%) | 15% (re-rating 0%) |
| 3x | 38% (re-rating -47%) | 37% (re-rating -44%) | 30% (re-rating -20%) | 25% (re-rating 0%) |
| 5x | 53% (re-rating -32%) | 52% (re-rating -30%) | 44% (re-rating -14%) | 38% (re-rating 0%) |

### (d) Temperature
| Basis | Value | Own median (n) | vs own | Own band | Sector median | vs sector | Sector band |
|---|---|---|---|---|---|---|---|
| P/B (fully diluted) | 2.24x | 1.38x (10) | 1.63x | HOT | 1.48x | 1.51x | HOT |

Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average

### (e) Book-value stress (lender-specific)
Leverage (assets ÷ diluted book): 9.31x. Net NPA as % of book: 1.1%.

| Extra loss on loans | Post-tax hit | % of book | BVPS after |
|---|---|---|---|
| 1% | 2,237 | 5% | 158.9 |
| 2% | 4,473 | 10% | 150.8 |
| 3% | 6,710 | 15% | 142.6 |
| 5% | 11,183 | 24% | 126.3 |

### (f) Sensitivity: RIM value per share, CoE (rows) × long-run ROE (columns)

| CoE \ ROE | 11.0% | 12.5% | 14.0% | 15.5% | 17.0% |
|---|---|---|---|---|---|
| 10.5% | 198 (-47%) | 259 (-31%) | 328 (-12%) | 404 (8%) | 489 (31%) |
| 11.5% | 155 (-58%) | 203 (-46%) | 257 (-31%) | 316 (-15%) | 381 (2%) |
| 12.5% | 125 (-66%) | 163 (-56%) | 206 (-45%) | 253 (-32%) | 305 (-18%) |
| 13.5% | 103 (-72%) | 134 (-64%) | 168 (-55%) | 207 (-45%) | 249 (-33%) |
| 14.5% | 86 (-77%) | 112 (-70%) | 140 (-63%) | 171 (-54%) | 206 (-45%) |

Justified P/B (same grid): CoE 10.5%: 1.09x, 1.36x, 1.64x, 1.91x, 2.18x; CoE 11.5%: 0.92x, 1.15x, 1.38x, 1.62x, 1.85x; CoE 12.5%: 0.80x, 1.00x, 1.20x, 1.40x, 1.60x; CoE 13.5%: 0.71x, 0.88x, 1.06x, 1.24x, 1.41x; CoE 14.5%: 0.63x, 0.79x, 0.95x, 1.11x, 1.26x

### Input notes
- Price Rs 373.5 = NSE close 20-Nov-2026 (Yahoo chart API); screener 'Current Price' Rs 374 and BSE LTP Rs 373.00 on 21/22-Nov agree (3 sources).
- Shares 247.27 cr = paid-up Rs 494.54 cr / FV 2 (NSE integrated-filing XBRL Q2FY27). Book Rs 41,222 cr = capital 495 + reserves 39,178 + share-warrant money 1,549 (deck slide 30; XBRL capital+reserves 41,221.5).
- Dilution: EGM notice 27-Oct-2025: 27,29,74,043 warrants at Rs 227, 25% (Rs 1,549 cr) paid, 75% (Rs 4,647 cr) on exercise within 18 months. Diluted BVPS = (41,222 + 4,647) / 274.57.
- PAT TTM 4,863 = Q3FY26 1,041 + Q4FY26 1,259 + Q1FY27 1,177 + Q2FY27 1,386 (XBRL/screener). Normalised 4,645 [EST]: Q4 excl one-off 1,145 (deck) and Q2 less ~Rs 104 cr post-tax treasury income above a ~Rs 100 cr/qtr run-rate.
- ROE paths are on DILUTED book: H1FY27 annualised normalised PAT ~4,900 / diluted book ~45,900 = ~10.7% if the warrant cash sat idle; RoA 1.32% x leverage 9.3x (post-issue) = ~12.3%. Base 12% -> 14% assumes RoA 1.35-1.45% and gradual deployment [EST].
- pb_history: March-end price (Yahoo monthly) / (equity capital + reserves) per share from screener standalone balance sheets; single-source computation, reserves include revaluation reserves.
- sector_pbs: screener top-ratios price / book value, 21-22 Nov 2026 (single source; peer books not adjusted for pending dilution).
- CoE 12.5% = India default for comparability (L21); an argument exists for 13-14% for a 10x-levered bank - see the sensitivity grid.
- Scenario probabilities and exit P/Bs are illustrative [EST] for the practice run (no verdict).

Sources: NSE integrated-filing XBRL INTEGRATED_FILING_BANKING_1740409_16102026072531_WEB.xml; FBL investor presentation Q2FY27 (NSE, 16-Oct-2026); FBL EGM notice 27-Oct-2025 (NSE); screener.in FEDERALBNK standalone (fetched 22-Nov-2026); Yahoo Finance chart API FEDERALBNK.NS

