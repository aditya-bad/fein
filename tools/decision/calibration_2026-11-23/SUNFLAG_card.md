# Decision card: Sunflag Iron & Steel (SUNFLAG) · 2026-11-23

> Phase A: every size on this card is a **paper size** until the phase-B gate in `memory/roadmap.md` is passed.

| Card | Value |
|---|---|
| Card version | 1.1 (2026-11-23; market-specific PEAD gate, base-rate CIs/size band, v1.3 worksheet lines) · worksheet 1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode) |
| Price used | INR 368.60 on 2026-11-20 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/SUNFLAG_live.md) · 5 valuation worksheet |
| **Rule output** | size 0: blocked by Expected value vs hurdle (EV 1.38x vs hurdle 1.76x → below hurdle → size 0) |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:SUNFLAG:card-2026-11-23-5y-ge3x`, `thesis:paper-call:SUNFLAG:card-2026-11-23-5y-le0p5x`, `thesis:paper-call:SUNFLAG:card-2026-11-23-5y-blowup` |

## 1. Thesis in one line
Method-test thesis: about three quarters of Sunflag's value is a 10.66% stake in Lloyds Metals & Energy (post-tax ~Rs 9,016 cr vs a Rs 6,643 cr market cap); the special-steel business compounds ~8%/yr at ~7% NOPAT margin with ROIIC close to the cost of equity, and the market's ~50% discount on the stake persists over 5 years unless the stake is monetised and distributed.

## 2. Variant view (what we believe that the price does not, and why we could know it)
Market (reverse DCF): at Rs 368.60 the price implies either a 45-61% discount on the post-tax LMEL stake (if the steel business is worth our bear-to-bull DCF of Rs 93-170/share) or, at a 55% discount, 5.4x EV/EBITDA and 12.5x P/E for steel (KSL 12.6x). Our view: the gap is NOT a mispricing we can claim. The discount sits inside the Indian holdco base range (insight:group-holdco-discount) and is justified by three things we verified: no stated monetisation or payout policy (dividend Re 1, ~9% payout), the stake already serves as loan collateral (74 lakh LMEL shares pledged to Indian Bank), and management is spending on a 10-block mining programme with a weak delivery record (Lohardongri LOI 2019, still not operating; Belgaon reserve figure stale for a year). What we add that the market may underweight: the steel balance sheet is now near debt-free (net debt Rs 26 cr at Sep-2026, CRISIL AA-/Stable) and the business earns a ~14% pre-tax ROCE, so the bear case is LMEL-driven, not steel-driven. What would prove us wrong: (a) a board decision to sell LMEL shares with a buyback/special dividend (gap closes; our 'persists' call fails), or (b) LMEL proceeds or new debt going into mining capex (discount widens; our steel-is-safe view fails). Departure from the outside view (card §5): our P(>=3x in 5y) is far below the base class and P(<=0.5x) above it on purpose. The class is survivors of the 2020-25 small-cap bull run (x3 overstated, losses understated, per its caveats); Sunflag's 5-year outcome is ~75% a single listed stock (LMEL, already up ~3.2x in 3 years) held at a discount, plus a steel business whose ROIIC is close to the cost of equity, so a 3x needs LMEL to roughly triple again or the discount to close; the fatter left tail is single-stock concentration (beta 0.73 to LMEL). These 5-year card calls are the cleanest test in this file of whether our structural adjustment beats the naive class. Checked by paper calls thesis:paper-call:SUNFLAG:* (6 operating/event/price calls to 2027-09-30, plus the 3 card calls).

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 12.5%, TG 5.0%, ROIIC 12%): revenue CAGR n/a for 10 years at a 6.9%→7.0% NOPAT margin; or year-1 growth n/a fading to 5.0%. Base case IRR at today's price: 11.7%.
- **Scenario DCF:** probability-weighted value 345.4 (-6% vs price); bear 321.3 (-13%).
- **Twin engine, 3x in 5 yrs** from P/E 32.8: exit P/E 10.3 → EPS CAGR 57%; exit P/E 16.4 → EPS CAGR 43%; exit P/E 19.0 → EPS CAGR 39%; exit P/E 24.6 → EPS CAGR 32%; exit P/E 32.8 → EPS CAGR 25%. Track record: 7.6% Consolidated EPS FY21 7.80 -> FY26 11.23 [SCR]; FY23 61.89 incl. the LMEL arbitral-award gain excluded.
- **Temperature:** P/E 32.8; own history: VERY HOT; sector: HOT (1.73x of sector median).
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- **Exit-multiple bet (L21):** exit P/E used 9.0/12.0/16.0 vs DCF-consistent 13.2/12.9/14.2 vs own median 10.3. EV of the 5-yr multiple at the used exits 1.38x, at DCF exits 1.42x, at the own median 1.30x (hurdle 1.76x).
- Full worksheet: `tools/valuation/live/SUNFLAG.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: S2 checklist in research_notes/Deep dives/SUNFLAG_live.md section 1 (AR FY26/FY25 auditor's reports + CARO, 584 NSE announcements to 23-Nov-2026, SHP XBRL 30-Sep-2026, CRISIL letter 14-Nov-2025, tools/detectors/solvency_screen.py run 23-Nov-2026).

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal | PASS | Cash + bank Rs 367 cr (Sep-2026) vs interest income Rs 9.9 cr FY26 on a smaller FY26 average balance (consistent); the big asset (LMEL stake) is a listed, observable price; CRISIL AA-/Stable assigned 14-Nov-2025 |
| H1b economics implausible | PASS | Rolled products 467,540 t [AR26 board report] x ~Rs 84k/t = revenue Rs 3,939 cr; EBITDA ~Rs 10.2k/t; BRSR energy 2.30 m GJ / 4,032 MJ/t = ~571k t equivalent (cross-foots with SMS 497.5k t + DRI) |
| H1c profits unverifiable by outsiders | PASS | Auto/forging/bearing customers, no customer >=10% [AR26 n.35]; listed SBQ peers (KSL, VSSL, Mukand) report comparable spreads |
| H2 auditor exit / qualified opinion | PASS | Unmodified opinions FY25 (B P & Co.) and FY26 (Lodha & Co LLP); change = completion of the 5-year term at the Sep-2025 AGM; CARO 3(xviii): no resignation; Q2 FY27 limited review unmodified |
| H3 rating 'issuer not cooperating' | PASS | CRISIL AA-/Stable + A1+ on Rs 1,850 cr facilities, letter 14-Nov-2025 (valid to 01-Jan-2027); CARE rating letter 26-Nov-2024 earlier; no INC tag |
| H4 SME/Telegram pump | PASS | Main board since 1984 listing; NSE volume/price queries 05-May-2026 and 29-Sep-2026 answered 'market driven' (watch item, not a pump pattern); no promoter selling in SAST filings |
| H5 related-party cash leakage to promoter entities | PASS | RPTs tiny: Daido royalty Rs 2.4 cr, rent to Haryana Televisions Rs 0.57 cr, wire-rod sales to 49% JV Ramesh Sunwire Rs 32.7 cr (0.8% of sales) [AR26 n.39]; directors' commission Rs 8.2 cr FY26 (2.7% of PBT) graded below |

| Graded flag | Status | Evidence |
|---|---|---|
| G1 promoter pledge > 25% (v3: >50% strong red) | CLEAR | SHP 30-Sep-2026 XBRL: promoter encumbrance flags all false (pledge, NDU, other); nse_fetch pledge returned 0 rows on 23-Nov-2026 (the endpoint returned 0 rows for every symbol that day, so the SHP XBRL is the source) |
| G2 accounting-trouble events in 5 years | CLEAR | None in 584 announcements; one SOP fine (Jun-2025) for a late secretarial compliance report after the PCS resigned on the due date |
| G3 dilution | CLEAR | 18.02 cr shares unchanged FY16-FY27 |
| G4 solvency set (S1/S5 India) | CLEAR | solvency_screen 23-Nov-2026: grade blank, 0 flags, interest cover 5.2x FY26; net debt Rs 26 cr Sep-2026 |
| Q CFO/PAT 5y (question) | CLEAR | FY22-26 CFO Rs 1,147 cr vs PAT ex the FY23 award gain ~Rs 940 cr = 1.2x |
| Q CARO 3(ii)(b) stock statements vs books (question) | FIRED | Mismatch both years: FY25 up to Rs 168 cr (provisional DP statements), FY26 within Rs 19-31 cr; shrinking, kept as a question |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD):** SUE quintile 4 (event 2026-11-13). Avoid flag not active. Rule L19: bottom two quintiles = avoid/exit for ≥63 trading days.
- **Promise credibility:** not scored. No earnings calls exist (0 transcripts in 584 NSE filings, fetch.py 23-Nov-2026), so the promise-tracker pipeline has nothing to score. Hand ledger of 5 mine-status statements FY24->FY26: 0 reached production; 2 moved one statutory step (Bhivkund ML executed Apr-2026; Surjagad-6 drilling May-2026); 1 reversed (Lohardongri: LOI 2019 -> PIL in the High Court 2026); 1 dated promise open (Bajna EC + Stage-I 'likely by end Sep-2026'); 1 disclosure inconsistency (Belgaon extractable reserve 5.391 MT repeated FY24 and FY25, then 3.5 MT FY26).

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| KMP churn | 2025-02 to 2026-09 | COO ceased Feb-2025; CEO (appointed Nov-2024) resigned Nov-2025, new CEO Nov-2025; 3 independent directors left Aug-2025 to Sep-2026 | med |
| Exchange surveillance | 2026-05-05 / 2026-09-29 | Volume spurt and price-movement queries; company: no undisclosed information | low |
| Company-level pledge of the LMEL stake | FY26 AR n.15 | 74 lakh of 600 lakh LMEL shares pledged to Indian Bank as additional security | low |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| P/B 0.55 and 'cheap vs stake' look (good-but-misleading): the LMEL stake is 156% of market cap pre-tax | OPEN | Board policy to monetise and distribute; or two consecutive years of discount < 30% | FY27 AR (Sep-2027) |
| Mining diversification: 10 blocks, commercial coal (Tambia South), weak delivery record | OPEN | One block producing on the stated timeline (Bhivkund or Bajna) with capex funded from steel cash flow | 2027-09-30 |
| No earnings calls; ~1.1% institutional ownership; sparse disclosure | OPEN | First investor call / presentation | each quarter |
| Belgaon coal reserve figure stale (5.391 MT in FY24 and FY25) then cut to 3.5 MT | OPEN | Reserve reconciliation in the FY27 AR | FY27 AR |
| Commission on sales Rs 3.4 cr -> 16.5 cr (5x) in FY26 | OPEN | Counterparty and export link (exports Rs 48 -> 114 cr) disclosed; ratio to export sales stable | FY27 AR |
| Directors' commission Rs 4.2 cr -> 8.2 cr | WATCH | Commission > 5% of PBT | FY27 AR |
| 74 lakh LMEL shares pledged by the company to Indian Bank | WATCH | Pledged share count rises, or margin-call language | FY27 AR n.15 |
| H1 FY27 CFO Rs 339 cr flattered by payables +Rs 191 cr (good-but-misleading) | ADJUSTED | - | - |
| FY23 EPS 61.9 = arbitral-award settlement in LMEL OFCDs; FY26 Q4 tax 58% (prior-year deferred tax) | ADJUSTED | - | - |
| CARO 3(ii)(b) stock-statement mismatch | WATCH | Mismatch > Rs 50 cr again | FY27 AR |
| KMP and independent-director churn | WATCH | CFO or another CEO exit within 12 months | each quarter |

**Open soft flags: 6** (5 from the deep dive, 1 graded stage-2 flag(s)), plus 4 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-23 | FY23 other income Rs 1,201 cr | excluded from EPS history and the base year | AR FY23: settlement of past-period claims on LMEL via arbitral award (22/28-Apr-2022) paid in 6 cr OFCDs converted 1:1 into LMEL shares |
| 2026-11-23 | Screener ROCE 4% / ROE 2% | replaced by operating ROCE ~14% pre-tax on ~Rs 2,540 cr operating capital | Denominator includes the Rs 11,369 cr LMEL mark (Sep-2026) |
| 2026-11-23 | Promise tracker not runnable | hand ledger of AR mine-status statements used as the credibility read (n=5, not comparable with transcript-based scores) | No earnings calls since at least 2017 |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base |
|---|---|---|---|
| P(≥3x in 5 yrs) | 6% | 21.3% [95% CI 14.1%–28.7%] | 0.30x |
| P(≤0.5x in 5 yrs) | 8% | 11.3% [95% CI 7.0%–16.1%] | 0.73x |
| P(blow-up) | 2% | 15.4% [95% CI 10.2%–21.4%] | 0.13x |

Base-rate class: **India non-financial, mcap Rs 1,000-20,000 cr at T, 5 yrs from 30-Sep-2016 and 30-Sep-2018 (survivorship-free, dead firms included, stratum-weighted)** (n=208, 5-yr horizon). Source: research_notes/Backtests/base_rates_5y.md; tools/backtests/base_rates_5y/build.py on research_notes/Backtests/solvency_india_outputs/panel.csv (= hard_filters_india_v2_outputs/panel_v2.csv, same 489 rows); outputs research_notes/Backtests/base_rates_5y_outputs/results.json. Caveats: n=208 company-snapshots (54 distress-census D, 153 live L at weight 5.63, 1 delisted-other X at 4.26); 95% CIs (company bootstrap within stratum): P(>=3x) 14.1-28.7%, P(<=0.5x) 7.0-16.1%, P(blow-up) 10.2-21.4%. Two start dates only, and they disagree (2016: >=3x 16%, blow-up 21%; 2018: 26%, 10%). Price return only (no dividends, ~1%/yr). Blow-up = close <=0.2x the close at T, liquidation or compulsory delisting (no fraud field). Remaining survivorship leak toward FEWER failures (IBBI firms renamed/merged and 221 IBBI rows without identifiers missing; voluntary/merger delistings X under-covered). A survivors-only sample from the same frame says P(<=0.5x) 7% instead of 11%.
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.40 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(≥3x in 5 yrs) is 0.30x the base rate; P(blow-up) is 0.13x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.38x | 6.7% | 1.33x | 1.76x | 345.4 (-6%) | -13% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

## 7. Position size (written rule)
| Sizing step | Value |
|---|---|
| Full Kelly f* (5-yr bet vs index hurdle, scenario outcomes) | 0.0% |
| × Kelly fraction 0.25 | 0.0% |
| Cap: max % at cost (speculative tier) | 2.0% |
| Cap: liquidity (10% of ADV × 5 days ÷ portfolio) | n/a (ADV not supplied) |
| Rule size before gates = min(fractional Kelly, caps) | 0.0% |
| **Size after gates** (blocked by: Expected value vs hurdle) | **0.0%** |

Written rule: size = min(Kelly fraction × f*, tier cap at cost, liquidity cap); any blocking gate → 0. f* maximises E[ln(1 + f·(M/H − 1))] over the scenario outcomes (each scenario spread by 5-point Gauss-Hermite on the same σ, blow-up as a point mass), with H = the index hurdle multiple. Fractional Kelly because the inputs are opinions (strategy:thorp-kelly); tier caps from strategy:position-sizing (max 5% at cost, satellites 3.5–4%, speculative 1–3%).

## 8. Kill criteria (each one dated and checkable)
| # | Kill if… | Measured by | Check by |
|---|---|---|---|
| 1 | LMEL shares sold or transferred and the proceeds not distributed (buyback/special dividend) within 6 months | LMEL SHP (Sunflag line) + Sunflag Reg-30 + FY27 AR n.4 | 2027-09-30 |
| 2 | Consolidated borrowings above Rs 1,000 cr at any half-year end (debt-funded mining) | Half-year statement of assets and liabilities | 2027-09-30 |
| 3 | FY27 consolidated OPM below 9% | screener / NSE XBRL FY27 | 2027-05-31 |
| 4 | Any promoter encumbrance, or LMEL shares pledged by the company rise above 74 lakh | SHP XBRL quarterly; FY27 AR n.15 | 2027-09-30 |
| 5 | Modified audit opinion, auditor resignation or a rating 'issuer not cooperating' | Reg-30 / AR / rating letters | 2027-09-30 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. LMEL fell 50% on an iron-ore royalty or Gadchiroli mining shock; Sunflag fell ~35% with it although steel did fine (beta to LMEL 0.73, weekly corr 0.54 over 2 years).
2. The board sold part of the LMEL stake to fund Tambia South / Bhivkund mining capex instead of returning cash; the market widened the discount to 70%.
3. A steel-import surge (China/Korea/Japan, flagged in AR26) compressed the SBQ spread; OPM fell to 8-9% and the steel stub de-rated to 4x EBITDA.
4. A promoter-family or trust (Zedra, Jersey) restructuring or a Daido exit created supply overhang in an illiquid stock (ADV Rs 13.5 cr).

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (7 rules) | no |
| Stage 3 PEAD avoid flag | clear | no |
| Stage 4 soft flags | 6 open, variant view written | no |
| Expected value vs hurdle | EV 1.38x vs hurdle 1.76x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

