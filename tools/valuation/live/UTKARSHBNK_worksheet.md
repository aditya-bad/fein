## Valuation worksheet (bank mode): Utkarsh Small Finance Bank Ltd (UTKARSHBNK) · as of 2026-11-23

*Worksheet v1.1-bank (2026-11-22). Money in INR cr. Cost of equity 12.5% (market default 12-13%), terminal growth 5.0%, 10-year explicit period, payout 0%. Book is fully diluted for pending issues.*

> Note: fully diluted: +45.45 cr shares, +500 cash to be received; BVPS 15.04 -> 14.22

### Snapshot
| Price | Mcap (diluted) | BVPS undiluted → diluted | P/B undiluted → diluted | P/E | ROE (reported) |
|---|---|---|---|---|---|
| 11.71 | 2,616 | 15.04 → 14.22 | 0.78x → 0.82x | -12.6 | -24.7% |

### (a) Reverse P/B: what today's price needs
| Question | Answer |
|---|---|
| ROE needed forever (Gordon: g + P/B × (CoE − g)) | **11.2%** |
| ROE needed for 10 years, then only CoE (no franchise value left) | 10.3% |
| Cost of equity the market is using if today's ROE (-6.5% on diluted book) is permanent | **-9.0%** (ours 12.5%) |
| Justified P/B on the base case's long-run ROE 13.0% | 1.07x |
| IRR the price offers if the base case happens | **12.0%** (hurdle 12.0%) |

### (b) Residual-income scenarios
| Scenario | Prob | ROE start → end | RIM value | vs price | BVPS yr 5 | Exit P/B used | RIM-consistent P/B yr 5 | 5-yr multiple |
|---|---|---|---|---|---|---|---|---|
| bear | 30% | -4.0% → 8.0% | 2.1 | -82% | 13.3 | 0.60x | 0.29x | 0.68x |
| base | 40% | 4.0% → 13.0% | 10.5 | -10% | 19.0 | 0.90x | 1.00x | 1.46x |
| bull | 15% | 10.0% → 15.0% | 18.7 | 59% | 23.5 | 1.40x | 1.41x | 2.85x |
| blow-up | 15% | — | — | — | — | — | — | 0.15x |

> **Exit-multiple gap:** in bear the exit P/B is >1.3× what the residual-income path justifies at our CoE. That part of the return is a bet on the market paying up (L21).

| P(≥2x) | P(≥3x) | P(≥5x) | P(≤0.5x) | P(blow-up) | EV multiple (CAGR) | Median | Hurdle | Prob-weighted RIM value |
|---|---|---|---|---|---|---|---|---|
| 20% | 7% | 1% | 21% | 15% | 1.24x (4.4%) | 1.08x | 1.76x | 7.9 (-32%) |

### (c) Twin engine on book: BVPS CAGR needed (5 yrs, ignoring dividends) from P/B 0.82x
| Target | exit P/B 0.49x | exit P/B 0.66x | exit P/B 0.82x |
|---|---|---|---|
| 2x | 27% (re-rating -75%) | 20% (re-rating -32%) | 15% (re-rating -1%) |
| 3x | 38% (re-rating -47%) | 30% (re-rating -20%) | 25% (re-rating -0%) |
| 5x | 53% (re-rating -32%) | 44% (re-rating -14%) | 38% (re-rating -0%) |

### (d) Temperature
| Basis | Value | Own median (n) | vs own | Own band | Sector median | vs sector | Sector band |
|---|---|---|---|---|---|---|---|
| P/B (fully diluted) | 0.82x | 0.82x (3) | n/a | INSUFFICIENT HISTORY (n=3 < 5) | 1.01x | 0.82x | COOL |

Market: Nifty 50 P/E 20.6 (2026-11 (insight:india-valuation-forward-returns)): around the long-run average

### (e) Book-value stress (lender-specific)
Leverage (assets ÷ diluted book): 9.16x. Net NPA as % of book: 16.7%.

| Extra loss on loans | Post-tax hit | % of book | BVPS after |
|---|---|---|---|
| 1% | 145 | 5% | 13.6 |
| 2% | 290 | 9% | 12.9 |
| 3% | 434 | 14% | 12.3 |
| 5% | 724 | 23% | 11.0 |

### (f) Sensitivity: RIM value per share, CoE (rows) × long-run ROE (columns)

| CoE \ ROE | 10.0% | 11.5% | 13.0% | 14.5% | 16.0% |
|---|---|---|---|---|---|
| 10.5% | 9 (-20%) | 13 (11%) | 17 (47%) | 22 (86%) | 27 (131%) |
| 11.5% | 7 (-38%) | 10 (-14%) | 13 (13%) | 17 (44%) | 21 (78%) |
| 12.5% | 6 (-51%) | 8 (-32%) | 11 (-10%) | 13 (14%) | 17 (41%) |
| 13.5% | 5 (-60%) | 6 (-45%) | 8 (-27%) | 11 (-8%) | 13 (14%) |
| 14.5% | 4 (-68%) | 5 (-55%) | 7 (-41%) | 9 (-24%) | 11 (-6%) |

Justified P/B (same grid): CoE 10.5%: 0.91x, 1.18x, 1.45x, 1.73x, 2.00x; CoE 11.5%: 0.77x, 1.00x, 1.23x, 1.46x, 1.69x; CoE 12.5%: 0.67x, 0.87x, 1.07x, 1.27x, 1.47x; CoE 13.5%: 0.59x, 0.76x, 0.94x, 1.12x, 1.29x; CoE 14.5%: 0.53x, 0.68x, 0.84x, 1.00x, 1.16x

### Input notes
- Price Rs 11.71 = NSE bhavcopy 23-Nov-2026 close (sec_bhavdata_full_23112026) and Yahoo v8 UTKARSHBNK.NS 23-Nov-2026 11.71; screener 'Current Price' Rs 11.7 (3 sources).
- Shares 177.952 cr = paid-up capital Rs 1,779.52 cr / FV 10 (Q2 FY27 banking XBRL); includes 67.79 cr rights shares at Rs 14 allotted 05-Nov-2025 (8:13).
- Book Rs 2,676.33 cr = capital 1,779.52 + reserves 896.81 (Q2 FY27 XBRL; deck 'net worth 2,676'; BVPS 15.0 in deck). Screener shows reserves 846 for Sep-2026 (BVPS 14.8) - unexplained Rs 50 cr gap; XBRL used.
- Book INCLUDES deferred tax assets Rs 495.45 cr and intangibles Rs 245.67 cr, both deducted from CET1 (Pillar 3 DF-11, 30-Sep-2026): CET1 book Rs 1,906.7 cr = Rs 10.71/share. See UTKARSHBNK_cet1book.json for the same scenarios on CET1 book.
- PAT TTM -666.8 = Q3 FY26 -375.02 + Q4 FY26 -188.02 + Q1 FY27 -33.92 + Q2 FY27 -69.85 (XBRL; screener -667). pat_normalised = H1 FY27 x 2 (-103.77 x 2).
- Dilution [EST]: management said no equity this FY, 'sometime in the next financial year ... We may not require this'. 25-30% loan growth on CRAR 17.05% (cushion Rs 306 cr over 15%) needs capital; Rs 500 cr at Rs 11 assumed in ALL scenarios (conservative for bull, light for bear).
- ROE paths are linear year 1 -> year 10 (tool limitation): base 4% -> 13% passes ~8% in year 5 - slower than guidance (FY28 ROE ~15%). Base-rate class for anchoring is the India NON-financial class (no lender class on file) - disclosed on the card.
- pb_history: Yahoo March-end close / BVPS from screener balance sheets (single source; listed Jul-2023 so only 3 FY-ends, < 10 required). sector_pbs: screener price / book value, 24-Nov-2026 (single source).
- dispersion 0.35 (vs 0.30 default): a 10.9x-levered lender's outcome around each scenario is wider [EST].

Sources: NSE integrated-filing XBRL INTEGRATED_FILING_BANKING_1752247_03112026084750_WEB.xml (Q2 FY27) and six earlier quarters; Utkarsh SFB investor presentation Q2 FY27 (NSE, 03-Nov-2026); press release 03-Nov-2026; Q2 FY27 call transcript (NSE, 11-Nov-2026); Basel III Pillar 3 disclosures as on 30-Sep-2026 (utkarsh.bank.in); Annual report FY2025-26 (NSE, 10-Jul-2026); screener.in UTKARSHBNK and SFB peers (fetched 24-Nov-2026); NSE bhavcopy 23-Nov-2026; Yahoo Finance chart API UTKARSHBNK.NS

