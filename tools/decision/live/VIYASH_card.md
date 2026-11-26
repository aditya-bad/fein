# Decision card: Viyash Scientific Ltd (formerly SeQuent Scientific; human + animal-health APIs, animal-health formulations (Alivira), US human generics via 60%-owned Appco Pharma) (VIYASH) · 2026-11-26

> Phase A: every size on this card is a **paper size** until the phase-B gate in `memory/roadmap.md` is passed.

| Card | Value |
|---|---|
| Card version | 1.5 (2026-11-25; lender base-rate class auto-selected for lenders, L41; 1.4 core-asset threat, L40) · worksheet 1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode) |
| Price used | INR 228.88 on 2026-11-25 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/VIYASH_live.md) · 5 valuation worksheet |
| **Rule output** | size 0: blocked by Expected value vs hurdle (EV 1.07x anchored (raw 0.97x) vs hurdle 1.76x → below hurdle → size 0) |
| Review date | **2027-02-28** |
| Paper-call ids (stage 7) | `thesis:paper-call:VIYASH:card-2026-11-26-5y-ge3x`, `thesis:paper-call:VIYASH:card-2026-11-26-5y-le0p5x`, `thesis:paper-call:VIYASH:card-2026-11-26-5y-blowup` |

## 1. Thesis in one line
Method-test thesis: Viyash Scientific is the 16-Dec-2025 common-control merger of Carlyle's two Indian pharma holdings - SeQuent Scientific (animal-health APIs and Alivira formulations in Europe, Turkey, Brazil, India) and Viyash Life Sciences (human APIs/advanced intermediates in Hyderabad/Vizag, ex-Mylan units; Symed Labs) - plus 60%-owned Appco Pharma (US generics). TTM revenue Rs 3,713 cr (Q2 FY27: formulations 57%, APIs 42%; Europe 19%, emerging markets 21%, USA 12%, India 5% of sales), pre-ESOP EBITDA ~21%, 16 plants of which 10 USFDA-approved API sites, no customer above 10% of revenue, net debt Rs 26 cr. Reported earnings are depressed by two temporary lines: a merger ESOP charge (FY27 ~Rs 148 cr vs ~25 cr steady state) and acquired-intangible amortisation (~Rs 100 cr FY26 -> ~38 cr FY27 -> ~0). Group ROIC ~10% (13% ex goodwill) vs a 12.5% cost of equity.

## 2. Variant view (what we believe that the price does not, and why we could know it)
Market: at Rs 228.88 (mcap Rs 10,108 cr basic; Rs 11,062 cr fully diluted for the MD's 2.03 cr warrants and ~2.1 cr ESOP options) the stock trades at 43x reported TTM EPS (5.34 basic) and 47.6x fully diluted - but 4 analysts (Yahoo, 26-Nov-2026) put FY27 EPS at 7.43 and FY28 at 11.83 (forward P/E 19.4x on FY28), i.e. the market is pricing the ESOP/amortisation roll-off plus ~20% growth. Our read: no claimable mispricing. (1) Our bottom-up FY28 EPS (~11.3 basic / ~10.3 diluted) is close to consensus, so the 'expensive on TTM' look is mostly accounting, not a mistake by the market; (2) but at ~21-22x our FY28 diluted EPS the price already needs mid-teens growth sustained with ROIIC above the 12.5% CoE, and the worksheet base case (14% fading to 8%, margin 12.5%, exit 24x) gives an 8.4% IRR and a 1.08x 5-yr multiple; (3) the CFO's own ESOP guidance missed 3x within one quarter (Aug-2026: Q2-Q4 ~Rs 40 cr total; Nov-2026: Q2 alone 42, Q2-Q4 ~122) - the cost line the 'adjusted PAT' framing removes is the one management forecast worst; (4) Carlyle (promoter) sold ~12% in Q2 FY27 (61.31% -> 49.24% SHP) in year 5-6 of its holding: a supply overhang the MD says will not recur 'in the next 12 months'. Evidence for the other side: two AA- ratings (ICRA Apr-2026; Ind-Ra upgrade from A, Apr-2026), net debt ~0, no USFDA import alert found, clean EIR at the US site, diversified customers, API revival delivered in Q2 as guided. Departure from the outside view: raw P(blow-up) 7% < class 15% (no pledge, AA-, no customer >10%) and raw P(<=0.5x) ~27% > class 11% because the entry multiple is high; default w=0.5. Checked by paper calls thesis:paper-call:VIYASH:*.

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 12.5%, TG 5.0%, ROIIC 15%): revenue CAGR n/a for 10 years at a 9.3%→12.5% NOPAT margin; or year-1 growth n/a fading to 5.0%. Base case IRR at today's price: 8.4%.
- **Scenario DCF:** probability-weighted value 84.4 (-63% vs price); bear 52.5 (-77%).
- **Twin engine, 3x in 5 yrs** from P/E 47.6: exit P/E 23.8 → EPS CAGR 43%; exit P/E 35.7 → EPS CAGR 32%; exit P/E 46.2 → EPS CAGR 25%; exit P/E 47.6 → EPS CAGR 25%. Track record: n/a No meaningful EPS history: the listed entity became Viyash Life Sciences + Symed + SeQuent on 16-Dec-2025 (appointed date 1-Apr-2025, common-control pooling); FY25 restated EPS 0.88 -> FY26 4.09 is a merger/turnaround window, not a growth rate..
- **Temperature:** P/E 47.6; own history: INSUFFICIENT HISTORY (n=1 < 5); sector: NORMAL (1.03x of sector median).
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- **Reinvestment realism:** last-5y incremental ROIC 15.0%; price-implied ROIIC on the base path none up to 300% (on this growth/margin path no ROIIC reproduces the price); **flag** (>5 pts): scenario bear; scenario bull.
- **Exit-multiple bet (L21):** exit P/E used 15.0/24.0/32.0 vs DCF-consistent 12.7/14.8/17.2 vs own median n/a (n=1). EV of the 5-yr multiple at the used exits 0.97x, at DCF exits 0.61x, at the own median n/a (hurdle 1.76x).
- Full worksheet: `tools/valuation/live/VIYASH.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: S2 checklist in research_notes/Deep dives/VIYASH_live.md section 1 (AR FY26 consolidated auditor's report (S R B C & Co LLP), 209 NSE + 224 BSE announcements 26-Nov-2024 to 26-Nov-2026, NSE pledge API 25-Nov-2026 + SHP 30-Sep-2026, rating letters ICRA 22-Apr-2026 / Ind-Ra 30-Apr-2026, solvency_screen run 26-Nov-2026, FDA Import Alert 66-40 page 26-Nov-2026).

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal | PASS | Cash Rs 492.5 cr + other bank 12.3 cr against borrowings Rs 531.0 cr at 30-Sep-2026 [XBRL]; Mar-2026 cash 255.8 vs borrowings 435.8 [AR26]; finance cost 57.5 TTM on ~Rs 480-530 cr gross debt (~11-12%, includes overseas subsidiary lines) - cash beside debt is spread across 20 subsidiaries in 9 countries; no idle-cash pattern |
| H1b economics implausible | PASS | Pre-ESOP EBITDA 21.0-21.7% last 4 quarters; gross margin 53.7-55.5% [deck] - within API/formulation peers (Granules ROCE 15.5%, Neuland 26.5%, Aarti Drugs 12.0% [SCR]); Appco EBITDA margin rose from ~1% to 34-35% on a CGT-exclusivity launch that has since eroded (Aug/Nov-2026 calls) - explained |
| H1c profits unverifiable by outsiders | PASS | 250+ customers, none >10% of revenue [AR26 financial-risk note]; 10 USFDA-approved sites with public inspection history; two rating agencies (ICRA, Ind-Ra) |
| H2 auditor exit / qualified opinion | PASS | S R B C & Co LLP (EY network) unmodified consolidated opinion FY26 with an Emphasis of Matter on common-control merger accounting (comparatives restated; Note 57); KAMs: goodwill impairment (Rs 868.7 cr) and DTA recoverability (Rs 83.4 cr, of which Rs 50.0 cr losses/MAT in one Indian subsidiary); XBRL 'Declaration of unmodified opinion' Q4 FY25 and Q4 FY26; no resignation |
| H3 rating 'issuer not cooperating' | PASS | ICRA AA-/Stable on Rs 185 cr working-capital lines (22-Apr-2026); India Ratings upgraded IND A/Positive -> IND AA-/Stable / A1+ (30-Apr-2026), then withdrawn at the company's request (22-May-2026); Crisil rating on merged Symed Labs withdrawn on request (17-Jan-2026) - withdrawals, not INC |
| H4 SME/Telegram pump | PASS | Main board (BSE 512529, NSE VIYASH); 6-month ADV ~Rs 91 cr mean / 56 cr median [YH]; 4 sell-side analysts |
| H5 related-party cash leakage to promoter entities | PASS | Promoter is a PE fund (CA Hull Investments / Carlyle): nominee directors draw no fees [AR26]; the MD/Group CEO (founder of Viyash Life Sciences) holds 2.03 cr warrants at Rs 181.94 (25% paid; Rs 277.6 cr due on conversion) and was paid 116.7x the median employee [AR26]; no material RPT with promoter entities found - watch the warrants and ESOP |

| Graded flag | Status | Evidence |
|---|---|---|
| G1 promoter pledge > 25% (v3: >50% strong red) | CLEAR | NSE pledge API (SHP 30-Sep-2026): promoter shares pledged 0 of 217,886,737 (0.00%); promoter 49.34%. Non-promoter pledged shares 50.6 m (11.45% of shares) are outside the promoter block |
| G2 accounting-trouble events in 5 years | WATCH | No restatement except the scheme-mandated common-control restatement (EoM); SEBI administrative warning (1-Jul-2026) to the former CS on the insider-trading structured digital database (Jun-Oct 2024) - procedural; Rs 5.6 cr customer-claim provision for prior-year shipments in Q1 FY27 [deck]; SeQuent had loss years FY23-24 |
| G3 dilution | WATCH | Shares 43.69 cr (31-Mar-2026) -> 44.16 cr (Sep-2026) via ESOP allotments; plus 2.03 cr MD warrants (Rs 181.94) and ~2.1 cr options [EST] = ~9% potential dilution; FY27 ESOP expense ~Rs 148 cr |
| G4 solvency set (S1/S5 India) | CLEAR | solvency_screen 26-Nov-2026 (FY26 consolidated): grade blank, 0 flags, ICR 6.1x; TTM EBIT ex OI 477.2 / finance 57.5 = 8.3x; net debt Rs 26 cr at Sep-2026 |
| Q CFO/PAT 5y (question) | WATCH | No 5-year history for the merged entity; FY26 CFO 323 vs PAT 225 = 1.44x [SCR]; H1 FY27 CFO 182.7 vs PAT 163.9 = 1.11x; receivable days ~110 (Rs 1,167 cr at Sep-2026 on H1 revenue 1,934) and rising from 98 (FY25) |
| Q negative FCF (question) | CLEAR | FY26 FCF ~225 [SCR]; H1 FY27 115 [XBRL]; capex guide Rs 150-170 cr/yr |
| Q other-income share | CLEAR | TTM other income 50.0 = 11% of pre-exceptional PBT 469.7; exceptional -41.3 (Q3 FY26) |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD):** SUE quintile 5 (event 2026-11-13). Avoid flag not active. Rule L19: bottom two quintiles = avoid/exit for ≥63 trading days.
- **Survival cap (v1.3):** clear: pledge 0% of promoter holding and interest cover 8.30x are inside the limits (> 25% / < 1.5x).
- **Promise credibility:** not scored. Resolved past promises from the May/Aug/Nov-2026 calls: (1) FY27 acquired-intangible amortisation ~Rs 35 cr (May) -> Q1 25 + Q2 8.9 + Q3 ~4 = ~38: met; (2) API revival in Q2 (Aug) -> APIs +8% q/q, +12% y/y: met; (3) EBITDA ~Rs 800 cr run-rate 'FY27 internal target' (May) -> TTM pre-ESOP EBITDA Rs 798 cr: met; (4) ESOP charge Q2-Q4 FY27 'about Rs 40 cr in total' (CFO, Aug) -> Q2 alone 42.1, FY27 ~148 (Nov): MISSED by ~3x. 3/4 met but n<5 (L49) - not scored; open: FY27 revenue growth 'mid-teens' (Aug) raised to '20%+' (Nov).

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| Promoter (PE) sell-down | 2026-09-30 | Promoter holding 61.31% (30-Jun-2026 SHP) -> 49.24% (30-Sep-2026 SHP); analyst on the Nov-2026 call: Carlyle 'did a block of around 11%'; MD: 'next 12 months, I don't see anything'. Carlyle entered 2020-21 (fund life 7-8 years) | med |
| Guidance miss on a cost line | 2026-11-14 | ESOP: Aug-2026 'Q2, Q3 and Q4 ... about Rs 40 crores' vs Nov-2026 Q2 42.1 cr and FY27 ~148-149 cr; management's 'adjusted PAT' removes this line | med |
| Regulatory warning (procedural) | 2026-07-07 | SEBI administrative warning letter dated 1-Jul-2026 to the former Company Secretary: incomplete structured digital database (PIT Reg 3(5)) for 26-Jun to 18-Oct-2024 | low |
| Acquisition | 2026-10-01 | BioForLife Italia S.r.l. (companion-animal, 85-90 products) acquired by Alivira Ireland for EUR 15.0 m at closing + EUR 1.976 m deferred (Reg-30 21-Jul and 1-Oct-2026); consolidated from Q3 FY27 | low |
| Rating upgrade | 2026-04-30 | India Ratings IND A/Positive -> IND AA-/Stable (later withdrawn on request); ICRA AA-/Stable assigned 22-Apr-2026 | low |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| Group ROIC ~10% on Sep-2026 capital incl. Rs 877 cr goodwill (13% ex goodwill; ~12.8% with ESOP/amortisation normalised) vs CoE 12.5%; no valid ROIIC window (FY25->TTM ~52% is a merger/turnaround window, L38) | OPEN | FY28 EBIT ex other income >= Rs 750 cr on invested capital <= Rs 4,300 cr (after-tax ROIC >= 12.5%) | 2028-05-31 |
| Valuation: 47.6x fully diluted TTM EPS; ~21-22x our FY28 diluted EPS (~10.3); 19.4x consensus FY28 (11.83, 4 analysts, likely on basic shares) - the price already discounts the ESOP/amortisation roll-off and ~20% growth; worksheet base IRR 8.4% < CoE | OPEN | FY27 consolidated PAT >= Rs 400 cr with FY28 guidance of >= 18% revenue growth | 2027-05-31 |
| Management guidance quality: ESOP guide missed ~3x within one quarter; 'adjusted PAT with normalised ESOP' and 'pre-ESOP EBITDA' are the headline metrics; revenue guide raised mid-teens -> 20%+ in one quarter | OPEN | Q3 FY27 ESOP charge within Rs 35-45 cr as guided in Nov-2026 and FY28 ESOP <= Rs 40 cr | 2027-02-28 |
| Carlyle exit overhang: promoter 61.3% -> 49.2% in one quarter; fund in year 5-6 | OPEN | Promoter holding >= 45% at the 31-Mar-2027 SHP and a disclosed orderly-exit plan (e.g. to domestic funds) | 2027-04-30 |
| US generics / Appco (60%): exclusivity product eroded (Q2 FY26 ~USD 5 m in 45 days at 90%+ GM); US formulations -11% y/y, -6% q/q in Q2 FY27; management sees a Rs 110-115 cr/qtr stable base; US price erosion ~40% on launches (MD) | WATCH | US formulation sales >= Rs 110 cr in each of Q3 and Q4 FY27 | 2027-05-31 |
| API / China dependence for key starting materials not disclosed (AR mentions 'China+1' only as a tailwind); Q2 FY27 gross margin -180 bps y/y partly on raw-material/solvent prices (MD) | WATCH | KSM sourcing share disclosed in AR FY27 or on a call | 2027-09-30 |
| Goodwill Rs 877 cr (Turkey 104, Spain 86, USA 246, India 338 at Mar-2026) with Turkey under hyperinflation accounting (Ind AS 29); DTA Rs 83 cr KAM | WATCH | No impairment in FY27 | 2027-05-31 |
| Trailing 43-48x P/E looks extreme - but ~Rs 139 cr pre-tax of the TTM costs (excess ESOP + ending amortisation) are temporary; good-but-misleading in reverse (bad-looking, partly benign) | EXPLAINED | - | 2027-05-31 |
| Balance sheet: net debt Rs 26 cr; AA- from two agencies; no customer >10%; clean US EIR - good | CONFIRMED | - | 2027-05-31 |

**Open soft flags: 4** (4 from the deep dive), plus 3 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-26 | Survival cap core-asset threat (v1.4) | not set | L40 checked for government-granted inputs: no lease/licence concession identified; USFDA site approvals are regulatory permissions across 10 sites (no single-site dependence disclosed), and no import alert / warning letter was found (FDA Import Alert 66-40 page searched 26-Nov-2026 for Viyash/SeQuent/Symed/Appco/Alivira/Vindhya/Vandana: none). Weighed in the blow-up note. |
| 2026-11-26 | Both-flags balance-sheet question (L39 addendum) | not triggered | Promoter pledge 0% and TTM ICR 8.3x: neither flag fires. |
| 2026-11-26 | L44 core EPS | done | Exceptional (-41.3, Q3 FY26) and other income (50.0) stripped once from reported owners' PAT (worksheet inputs; no double subtraction): core P/E 48.7x vs 47.6x - small. The bigger hidden items are not exceptionals but temporary operating costs (merger ESOP, acquired-intangible amortisation) - reported, not stripped. |
| 2026-11-26 | Credibility | not scored | n=4 resolved promises (3 met, 1 missed) < 5 (L49). |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base | Anchored (w=0.50 on base) |
|---|---|---|---|---|
| P(≥3x in 5 yrs) | 2% | 21.3% [95% CI 14.1%–28.7%] | 0.10x | not anchored |
| P(≤0.5x in 5 yrs) | 27% | 11.3% [95% CI 7.0%–16.1%] | 2.38x | 19.0% |
| P(blow-up) | 7% | 15.4% [95% CI 10.2%–21.4%] | 0.46x | 11.2% |

**Outside-view anchoring (v1.2, L36):** anchored P = 0.50 × base rate + 0.50 × model for P(≤0.5x) and P(blow-up) (weight: stated). The expected-value gate and Kelly use the anchored tails; the paper calls keep the raw model probability (with the anchored one alongside), so Brier scoring can tell which was better. This is a calibration safeguard, not a change to the hurdle. The default weight is 0.5; a lower weight needs a written evidence note, never below 0.25.

> **WARNING: anchoring lowered documented tails — check evidence note** (P(≤0.5x): the class base rate is below our model tail, so anchoring made the card more optimistic, L40). If the model tail rests on company-specific evidence (a lease expiry, a licence dispute, a debt wall), the raw tail is the honest number: write that evidence in the deep dive and size off the raw tail by hand; the mechanical size below uses the anchored one.

Base-rate class: **India non-financial, mcap Rs 1,000-20,000 cr at T, 5 yrs from 30-Sep-2016 and 30-Sep-2018 (survivorship-free, dead firms included, stratum-weighted)** (n=208, 5-yr horizon). Source: research_notes/Backtests/base_rates_5y.md; tools/backtests/base_rates_5y/build.py on research_notes/Backtests/solvency_india_outputs/panel.csv (= hard_filters_india_v2_outputs/panel_v2.csv, same 489 rows); outputs research_notes/Backtests/base_rates_5y_outputs/results.json. Caveats: n=208 company-snapshots (54 distress-census D, 153 live L at weight 5.63, 1 delisted-other X at 4.26); 95% CIs (company bootstrap within stratum): P(>=3x) 14.1-28.7%, P(<=0.5x) 7.0-16.1%, P(blow-up) 10.2-21.4%. Two start dates only, and they disagree (2016: >=3x 16%, blow-up 21%; 2018: 26%, 10%). Price return only (no dividends, ~1%/yr). Blow-up = close <=0.2x the close at T, liquidation or compulsory delisting (no fraud field). Remaining survivorship leak toward FEWER failures (IBBI firms renamed/merged and 221 IBBI rows without identifiers missing; voluntary/merger delistings X under-covered). A survivors-only sample from the same frame says P(<=0.5x) 7% instead of 11%.
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.40 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(≥3x in 5 yrs) is 0.10x the base rate; P(≤0.5x in 5 yrs) is 2.38x the base rate; P(blow-up) is 0.46x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 0.97x | -0.7% | 0.88x | 1.76x | 84.4 (-63%) | -77% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

**Anchored EV (v1.2, used by the gate):** 1.07x (raw model 0.97x). Tails reweighted to P(blow-up) 11.2% and P(≤0.5x) 19.0%; the rest of the distribution is scaled in proportion, its shape kept.

## 7. Position size (written rule)
| Sizing step | Value |
|---|---|
| Full Kelly f* (5-yr bet vs index hurdle, anchored outcomes; raw model 0.0%) | 0.0% |
| × Kelly fraction 0.25 | 0.0% |
| Cap: max % at cost (satellite tier) | 4.0% |
| Cap: liquidity (10% of ADV × 5 days ÷ portfolio) | n/a (ADV not supplied) |
| Rule size before gates = min(fractional Kelly, caps) | 0.0% |
| **Size after gates** (blocked by: Expected value vs hurdle) | **0.0%** |

Written rule: size = min(Kelly fraction × f*, tier cap at cost, liquidity cap); any blocking gate → 0. f* maximises E[ln(1 + f·(M/H − 1))] over the scenario outcomes (each scenario spread by 5-point Gauss-Hermite on the same σ, blow-up as a point mass), with H = the index hurdle multiple. Fractional Kelly because the inputs are opinions (strategy:thorp-kelly); tier caps from strategy:position-sizing (max 5% at cost, satellites 3.5–4%, speculative 1–3%).

## 8. Kill criteria (each one dated and checkable)
| # | Kill if… | Measured by | Check by |
|---|---|---|---|
| 1 | USFDA warning letter, OAI classification or import alert at any Viyash/Symed/Appco/Alivira site | Reg-30 / FDA warning-letter and import-alert pages | 2027-11-30 |
| 2 | Promoter holding below 40% at any quarterly SHP before Mar-2028 without a disclosed strategic buyer | NSE SHP | 2028-03-31 |
| 3 | FY27 consolidated revenue growth below 12% (vs '20%+' guided Nov-2026) | Q4 FY27 consolidated XBRL | 2027-05-31 |
| 4 | FY28 ESOP charge above Rs 60 cr (guided ~32) | FY28 decks / AR | 2028-05-31 |
| 5 | Goodwill impairment above Rs 100 cr | FY27/FY28 results | 2028-05-31 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. Carlyle sold its remaining 49% through blocks in 2027-28 at a discount, the stock de-rated to API-peer multiples (~20x) while growth slowed to high single digits as US generics kept eroding and Chinese API prices fell; EPS still doubled on the ESOP/amortisation roll-off, but the multiple halved.
2. An FDA inspection at a Hyderabad API site produced an OAI/warning letter; human-API customers dual-sourced away; the companion-animal pipeline (2029+ launches) slipped as registrations took longer; acquisitions (BioForLife and the 'peak year' of deals in FY28) diluted ROIC below 10%.
3. Management kept steering investors to 'pre-ESOP' and 'adjusted' numbers while new grant cycles kept ESOP near Rs 80-100 cr a year, and the minority buy-outs (Appco 40%, Karizoo 40%) were paid at high multiples.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (7 rules) | no |
| Stage 3 PEAD avoid flag | clear | no |
| Stage 3 survival cap | clear | no |
| Stage 4 soft flags | 4 open, variant view written | no |
| Tail anchoring (v1.4 warning) | anchoring lowered documented tails — check evidence note: P(≤0.5x) | no |
| Expected value vs hurdle | EV 1.07x anchored (raw 0.97x) vs hurdle 1.76x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

