# Decision card: Harsha Engineers International Ltd (precision bearing cages, bushings, stampings; solar EPC) (HARSHA) · 2026-11-25

> Phase A: every size on this card is a **paper size** until the phase-B gate in `memory/roadmap.md` is passed.

| Card | Value |
|---|---|
| Card version | 1.5 (2026-11-25; lender base-rate class auto-selected for lenders, L41; 1.4 core-asset threat, L40) · worksheet 1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode) |
| Price used | INR 438.25 on 2026-11-23 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/HARSHA_live.md) · 5 valuation worksheet |
| **Rule output** | size 0: blocked by Expected value vs hurdle (EV 1.58x anchored (raw 1.58x) vs hurdle 1.76x → below hurdle → size 0) |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:HARSHA:card-2026-11-25-5y-ge3x`, `thesis:paper-call:HARSHA:card-2026-11-25-5y-le0p5x`, `thesis:paper-call:HARSHA:card-2026-11-25-5y-blowup` |

## 1. Thesis in one line
Method-test thesis: Harsha Engineers is the largest independent maker of precision bearing cages (steel, brass, polyamide; 20-2,000 mm), selling mainly to a handful of global bearing majors from Ahmedabad (Changodar, Moraiya, Bhayla), Changshu (China) and Ghimbav (Romania), plus bushings for wind gearboxes, stampings and a solar-EPC side business (~11% of revenue, ~5% of EBITDA). India Engineering earns ~22-24% EBITDA margins; the group earns ~11.5% ROIC because of Romania losses, a working-capital-heavy model (~135 days) and a Rs ~600 cr capex wave (Advantek Bhayla phases 1-2, China phase 2) that is still ramping. The 5-year outcome depends on whether that capex earns well above its recent ~11% incremental return.

## 2. Variant view (what we believe that the price does not, and why we could know it)
Market: at Rs 438 the stock trades at 24.4x trailing P/E and 14.3x EV/EBITDA - below its short listed history (FY23-26 FY-end median 28.8x) and well below bearing makers (43-50x), near the closest chain peer Rolex Rings (22.1x). Analysts on the Q2 FY27 call asked about Romania downsizing, the conservative H2 guidance, metal pass-through and Advantek breakeven; nobody asked about group ROIC or the utilisation of the capacity being built. Our read: the worksheet's reverse DCF finds no growth path at the historical ~11-14% ROIIC that justifies the price - it needs a year-10 NOPAT margin of ~24.5% (vs 9.0% now) on the base growth path, i.e. the market is already paying for India-Engineering-style returns on the new capital. Evidence against that: Advantek runs at ~54% utilisation (Reg-30 28-May-2026) yet is adding 12 m pieces (Rs 110 cr) and 'Rs 350 cr plus' in total; the Rs 117 cr/yr bushing contract (Aug-2025) is 'a little bit delayed'; Romania has missed operating breakeven targets since FY25; FY26 CFO was Rs 68 cr on Rs 278 cr EBITDA. Evidence for: India Engineering +23% in H1 FY27 with 23.7% EBITDA margin, outsourcing projects worth Rs 75 cr + Rs 75-100 cr in the pipeline, a strategic sourcing deal with a European major, net cash ~Rs 95 cr, CARE AA- (Mar-2024), promoter 75% unpledged. No claimable mispricing: we have no information edge on customer outsourcing decisions; the question we can track (utilisation and ROIC on the new capex) is dated and public. Departure from the outside view: raw P(blow-up) 5% is below the class 15% (strong balance sheet, AA- rating, no pledge) - anchored at the default w=0.5, which raises it; we do not claim enough evidence to go below 0.5. Checked by paper calls thesis:paper-call:HARSHA:*.

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 12.5%, TG 5.0%, ROIIC 14%): revenue CAGR n/a for 10 years at a 9.0%→9.5% NOPAT margin; or year-1 growth n/a fading to 5.0%. Base case IRR at today's price: 8.7%.
- **Scenario DCF:** probability-weighted value 190.0 (-57% vs price); bear 115.9 (-74%).
- **Twin engine, 3x in 5 yrs** from P/E 43.8: exit P/E 21.9 → EPS CAGR 43%; exit P/E 32.9 → EPS CAGR 32%; exit P/E 43.8 → EPS CAGR 25%; exit P/E 44.0 → EPS CAGR 24%. Track record: 13.9% Consolidated PAT FY22 92 -> FY26 155 = 13.9%/yr [SCR]; FY23-25 fell 123 -> 89 (European industrial slowdown + Romania impairment) before recovering; EPS CAGR from FY20 (2.84) is distorted by the 2022 IPO share issue.
- **Temperature:** P/E 24.4; own history: INSUFFICIENT HISTORY (n=4 < 5); sector: COLD (0.55x of sector median).
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- **Reinvestment realism:** last-5y incremental ROIC 11.0%; price-implied ROIIC on the base path none up to 300% (on this growth/margin path no ROIIC reproduces the price); **flag** (>5 pts): scenario bull.
- **Exit-multiple bet (L21):** exit P/E used 15.0/24.0/32.0 vs DCF-consistent 9.2/10.6/13.5 vs own median n/a (n=4). EV of the 5-yr multiple at the used exits 1.58x, at DCF exits 0.73x, at the own median n/a (hurdle 1.76x).
- Full worksheet: `tools/valuation/live/HARSHA.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: S2 checklist in research_notes/Deep dives/HARSHA_live.md section 1 (AR FY26 auditors' reports + CARO, 290 NSE announcements + 160 BSE announcements (two <=1-year windows, 25-Nov-2024 to 25-Nov-2026), NSE pledge API 25-Nov-2026 (0 rows) + SHP XBRL 30-Sep-2026, CARE rating filing 13-Mar-2024, solvency_screen run 25-Nov-2026).

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal | PASS | Liquid assets Rs 533.5 cr at 30-Sep-2026 (cash 22.1, other bank 21.8, current investments 265.5, non-current investments 224.0) [Q2FY27 XBRL]; screener Sep-2026 investments 490 + cash (consistent); FY26 standalone interest income Rs 11.6 cr [AR26 standalone cash-flow statement]. Gross debt Rs 438.5 cr held alongside: a question (subsidised loans per management), not a fake-cash pattern - treasury yields are plausible |
| H1b economics implausible | PASS | India Engineering EBITDA ~22-24% vs Rolex Rings ~20% (bearing-component peer); consolidated OPM 15-17% after Romania losses; gross margin moves track brass/steel pass-through and solar mix (Q2 FY27 call) |
| H1c profits unverifiable by outsiders | PASS | Customers are global bearing majors (one = 12.6% of FY26 revenue); exports Rs 480 cr FY26 [Q2 FY27 call]; debtor days 85 [SCR]; customs-recorded exports and CARE-rated bank lines |
| H2 auditor exit / qualified opinion | PASS | AR FY26 standalone and consolidated opinions unmodified; statutory auditor Pankaj R. Shah & Associates completed its term at the 23-Jul-2026 AGM and Mukesh M. Shah & Co was appointed for 5 years (Reg-30 23-Jul-2026) - rotation, not resignation; Q2 FY27 limited review filed 03-Nov-2026 |
| H3 rating 'issuer not cooperating' | PASS | CARE AA- (Stable) / A1+ reaffirmed, bank facilities Rs 483.87 cr (Reg-30 13-Mar-2024); no INC/withdrawal found in NSE or BSE announcements to 25-Nov-2026. Single-source and dated: no 2025-26 rating filing found (open item) |
| H4 SME/Telegram pump | PASS | Main board IPO Sep-2022 (Rs 330 issue price); 6-month ADV Rs 7.5 cr mean / 5.1 cr median [YH]; no price-movement queries in 2025-26 |
| H5 related-party cash leakage to promoter entities | PASS | FY26 related-party sales to AIA Engineering (directors' significant influence) Rs 28.3 cr (1.7% of revenue), purchases from KMP-linked entities Rs 1.6 cr, managerial remuneration Rs 11.0 cr (7.1% of PAT), CSR to promoter-linked trusts Rs 2.95 cr [AR26 consolidated RPT note]; no promoter-entity loans |

| Graded flag | Status | Evidence |
|---|---|---|
| G1 promoter pledge > 25% (v3: >50% strong red) | CLEAR | NSE pledge API 25-Nov-2026: 0 rows; SHP XBRL 30-Sep-2026: all three encumbrance flags false; promoters 75.00% (up from 74.61% in Mar-2025) |
| G2 accounting-trouble events in 5 years | CLEAR | None found (FY25 Rs 95 cr impairment of the Romania investment in standalone books is an accounting recognition of losses, disclosed) |
| G3 dilution | WATCH | ESOP 2026 approved 23-Jul-2026 (99.76% for): up to 18 lakh options = 1.98% of shares; IPO Sep-2022 (fresh issue Rs 455 cr) fully deployed |
| G4 solvency set (S1/S5 India) | CLEAR | solvency_screen 25-Nov-2026: grade blank (not red), 2 flags: short-term borrowings 170 > cash 45 + 0.5 x CFO 68; dividends 9 > FCF -47 while debt 200 -> 372 (FY26). ICR FY26 13.9x (screen), TTM 9.6x (EBIT ex other income 220 / finance cost 23) |
| Q CFO/PAT 5y (question) | CLEAR | FY22-26 CFO Rs 583 cr vs PAT Rs 570 cr = 1.02x [SCR]; FY26 alone 0.44x (CFO 68 vs PAT 155; working capital + solar) |
| Q negative FCF (question) | WATCH | FCF FY25 -2, FY26 -47 [SCR] during the Advantek build; capex guided ~Rs 150 cr more by Jun-2027 |
| Q other-income share | CLEAR | TTM other income Rs 30 cr = 13% of PBT (treasury + FX); core PBT ~Rs 197 cr |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD):** SUE quintile 5 (event 2026-11-03). Avoid flag not active. Rule L19: bottom two quintiles = avoid/exit for ≥63 trading days.
- **Survival cap (v1.3):** clear: pledge 0% of promoter holding and interest cover 9.60x are inside the limits (> 25% / < 1.5x).
- **Promise credibility:** 57% vs peer median 60% → sector-adjusted -3 pts (concall mode, hand ledger (7 transcripts Nov-2024 to Nov-2026); peer median = auto-components (research_notes/Promise tracker pilot/AUTO_COMPONENTS_peer_comparison.md) - nearest sector on file, not a bearing-component peer set, n=7). Met: FY26 consolidated growth 'at least higher single digit' (May-2025) -> +15.6%; 'much stronger growth in bottom line' -> PAT +74%; India 'low to mid-teen' FY26 (Nov-2025) -> standalone +12.8%; Japan customer back to growth in FY27 (May-2025) -> H1 +28%. Missed: bushings ~30% FY26 (Nov-2025) -> ~25%; Romania operating breakeven (Nov-2024 hoped Q4 FY25; Feb-2026 'EBITDA first') -> still loss-making Q2 FY27; Rs 117 cr bushing contract sales from Q4 FY26 (Aug-2025) -> 'a little bit delayed' (Nov-2026). Pattern: numbers met, dates slip (L26). Pending: Advantek PAT-positive FY27 (Feb-2026) - H1 loss ~Rs 7 cr, management now says FY may stay 'minor negative'.

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| Minority vote against an independent director | 2026-07-23 | AGM resolution 9 (re-appointment of ID Kunal Shah, special): 69.21 m for vs 11.40 m against (14.14%). Promoters hold 68.28 m (75%); if all promoter shares voted for, ~92% of non-promoter votes cast were against [EST: scrutiniser report gives no category split]. Other 11 resolutions >= 99.76% for | med |
| Capacity added at low utilisation | 2026-05-28 | Advantek Phase 2 Rs 110 cr for +12 m pieces while existing 38 m pieces run at ~54% (Reg-30); total Advantek capex 'Rs 350 cr plus' with ~Rs 250 cr of loans (Q2 FY27 call) | med |
| Cash conversion dip | 2026-03-31 | FY26 CFO Rs 68 cr = 24% of EBITDA incl. other income (Rs 278 cr); screener pre-tax CFO/EBITDA 54%; FCF -47; working capital ~135 days at Q2 FY27 (call) | low |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| Group ROIC ~11.5% is below the 12.5% cost of equity while a ~Rs 600 cr capex wave (Advantek phases 1-2, China phase 2) is under way; Advantek at ~54% utilisation is adding capacity; the price implies far better returns on that capital (reverse DCF: year-10 NOPAT margin 24.5% needed) | OPEN | Advantek PAT-positive for two consecutive half-years and consolidated ROIC (EBIT x 0.73 / (equity + debt - liquid)) >= 14% on FY28 numbers | 2027-05-31 |
| Romania (Harsha Engineers Europe SRL): FY26 loss Rs 14.2 cr, Rs 95 cr investment impaired in FY25; 'downsizing' announced on the Q2 FY27 call with no capacity, headcount or one-off cost disclosed | OPEN | A Reg-30 restructuring plan with costs, then two quarters of foreign-subsidiary losses below Rs 1 cr | 2027-02-15 |
| Minority shareholders voted ~92% against re-appointing ID Kunal Shah (14.14% of all votes) at the 23-Jul-2026 AGM [EST split]; reason not disclosed | OPEN | Proxy-adviser reports or a company explanation showing a technical (non-independence) reason, and no repeat on other resolutions | 2027-09-30 |
| Debt 'backed by government subsidy' or lower rates (Q2 FY27 call) but AR FY26 has no government-grant / interest-subsidy disclosure; Rs 438 cr gross borrowing held alongside Rs 533 cr of liquid assets (L40: government input + external fact absent from the AR) | OPEN | AR FY27 / a Reg-30 note naming the scheme, rate, tenure and amount recognised | 2027-09-30 |
| Customer concentration: one customer Rs 205 cr = 12.6% of FY26 revenue (11.0% FY25); AR risk table names concentration among 'a limited number of large bearing manufacturers' and in-sourcing risk | WATCH | Top-customer share below 10% with growth intact, or a multi-year sourcing contract disclosed | 2027-09-30 |
| Rs 117 cr/yr bushing contract (Aug-2025) delayed; outsourcing project (Rs 75 cr peak) to start Q3-Q4 FY27 | WATCH | Bushing revenue >= Rs 45 cr in a quarter and the outsourcing project shipping by Q4 FY27 | 2027-05-31 |
| Q2 FY27 gross margin 51.7% (record) - partly metal pass-through and a low solar share; ~4-5 pts of H1 growth is pass-through, not volume (call) - good-but-misleading | EXPLAINED | - | 2027-02-15 |
| India Engineering +23% H1 FY27 at 23.7% EBITDA margin; XBRL = screener; no pledge; RPTs small; AA- rating; promoter 75% | CONFIRMED | - | 2027-05-31 |

**Open soft flags: 4** (4 from the deep dive), plus 2 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-25 | Survival cap core-asset threat (v1.4) | not set | L40 checked: solar-EPC ALMM/import relaxations to Dec-2026 and subsidy norms affect a segment with ~5% of EBITDA; the interest subsidy is a financing input; the Bhayla plant (Survey 376-379) replaced a leased plant vacated 31-Oct-2025 (Reg-30); whether the Bhayla land is owned or leased is not stated (open item); no expiring licence/lease for the core cage business found |
| 2026-11-25 | Both-flags balance-sheet question (L39 addendum) | not triggered | Pledge 0% and ICR 9.6x TTM / 13.9x FY26: neither flag fires, so the both-flags rule does not apply |
| 2026-11-25 | Credibility peer median | auto-components median used | No bearing/precision-component peer set on file (L18); disclosed |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base | Anchored (w=0.50 on base) |
|---|---|---|---|---|
| P(≥3x in 5 yrs) | 10% | 21.3% [95% CI 14.1%–28.7%] | 0.48x | not anchored |
| P(≤0.5x in 5 yrs) | 9% | 11.3% [95% CI 7.0%–16.1%] | 0.79x | 10.1% |
| P(blow-up) | 5% | 15.4% [95% CI 10.2%–21.4%] | 0.33x | 10.2% |

**Outside-view anchoring (v1.2, L36):** anchored P = 0.50 × base rate + 0.50 × model for P(≤0.5x) and P(blow-up) (weight: stated). The expected-value gate and Kelly use the anchored tails; the paper calls keep the raw model probability (with the anchored one alongside), so Brier scoring can tell which was better. This is a calibration safeguard, not a change to the hurdle. The default weight is 0.5; a lower weight needs a written evidence note, never below 0.25.

Base-rate class: **India non-financial, mcap Rs 1,000-20,000 cr at T, 5 yrs from 30-Sep-2016 and 30-Sep-2018 (survivorship-free, dead firms included, stratum-weighted)** (n=208, 5-yr horizon). Source: research_notes/Backtests/base_rates_5y.md; tools/backtests/base_rates_5y/build.py on research_notes/Backtests/solvency_india_outputs/panel.csv (= hard_filters_india_v2_outputs/panel_v2.csv, same 489 rows); outputs research_notes/Backtests/base_rates_5y_outputs/results.json. Caveats: n=208 company-snapshots (54 distress-census D, 153 live L at weight 5.63, 1 delisted-other X at 4.26); 95% CIs (company bootstrap within stratum): P(>=3x) 14.1-28.7%, P(<=0.5x) 7.0-16.1%, P(blow-up) 10.2-21.4%. Two start dates only, and they disagree (2016: >=3x 16%, blow-up 21%; 2018: 26%, 10%). Price return only (no dividends, ~1%/yr). Blow-up = close <=0.2x the close at T, liquidation or compulsory delisting (no fraud field). Remaining survivorship leak toward FEWER failures (IBBI firms renamed/merged and 221 IBBI rows without identifiers missing; voluntary/merger delistings X under-covered). A survivors-only sample from the same frame says P(<=0.5x) 7% instead of 11%.
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.30 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(≥3x in 5 yrs) is 0.48x the base rate; P(blow-up) is 0.33x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.58x | 9.6% | 1.51x | 1.76x | 190.0 (-57%) | -74% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

**Anchored EV (v1.2, used by the gate):** 1.58x (raw model 1.58x). Tails reweighted to P(blow-up) 10.2% and P(≤0.5x) 10.2% (floored at the anchored blow-up: a blow-up ends ≤0.5x in the model); the rest of the distribution is scaled in proportion, its shape kept.

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
| 1 | Consolidated ROIC (EBIT ex other income x 0.73 / (equity + debt - liquid assets)) below 11% on FY27 numbers | AR FY27 / FY27 XBRL | 2027-09-30 |
| 2 | Advantek still loss-making in H2 FY27 (management guided H2 positive) | AR FY27 subsidiary financials / Q4 FY27 call | 2027-06-30 |
| 3 | Romania restructuring cost above Rs 50 cr or any further impairment of the Europe investment | Reg-30; results notes | 2027-11-30 |
| 4 | Top customer share above 15% of revenue, or a disclosed loss/in-sourcing of a major account | AR Ind AS 108 major-customer note; Reg-30 | 2027-09-30 |
| 5 | CARE rating downgrade below AA- or a rating withdrawal | Reg-30 / CARE site | 2027-11-30 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. European wind and industrial demand stayed soft through FY28; a bearing major moved part of its cage need in-house; Advantek ran below 60% utilisation with Rs 250 cr of new loans; ROIC fell to ~8% and the market re-rated the stock to 15x on lower EPS.
2. Romania downsizing turned into a closure with Rs 60-100 cr of severance and asset write-offs; the subsidised-loan terms were not what investors assumed and finance costs rose.
3. The outsourcing wave arrived, but at cost-plus prices from customers with buying power; revenue grew 15% while margins and asset turns lagged management's '2x' claim.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (7 rules) | no |
| Stage 3 PEAD avoid flag | clear | no |
| Stage 3 survival cap | clear | no |
| Stage 4 soft flags | 4 open, variant view written | no |
| Expected value vs hurdle | EV 1.58x anchored (raw 1.58x) vs hurdle 1.76x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

