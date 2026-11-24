# Decision card: Indraprastha Medical Corporation Ltd (Indraprastha Apollo Hospitals, Sarita Vihar) (INDRAMEDCO) · 2026-11-24

> Phase A: every size on this card is a **paper size** until the phase-B gate in `memory/roadmap.md` is passed.

| Card | Value |
|---|---|
| Card version | 1.3 (2026-11-24; general India survival cap outside the PEAD window, L39) · worksheet 1.3 (2026-11-23; cash-tax input, reinvestment-realism check, exit-multiple bet line; 1.2 non-operating growth; 1.1 bank mode) |
| Price used | INR 355.85 on 2026-11-23 (see worksheet notes for the source) |
| Stages feeding this card | 2 hard filters · 3 signals · 4 deep dive (research_notes/Deep dives/INDRAMEDCO_live.md) · 5 valuation worksheet |
| **Rule output** | size 0: blocked by Expected value vs hurdle (EV 1.39x anchored (raw 1.35x) vs hurdle 1.76x → below hurdle → size 0) |
| Review date | **2027-02-15** |
| Paper-call ids (stage 7) | `thesis:paper-call:INDRAMEDCO:card-2026-11-24-5y-ge3x`, `thesis:paper-call:INDRAMEDCO:card-2026-11-24-5y-le0p5x`, `thesis:paper-call:INDRAMEDCO:card-2026-11-24-5y-blowup` |

## 1. Thesis in one line
Method-test thesis: Indraprastha Medical (one ~700-bed Apollo-run hospital in Delhi) earns a ~50% ROIC partly because its land is leased from the Delhi government at Re 1/month in exchange for a free-treatment obligation it has under-delivered (7-10% vs 33% IPD / 40% OPD per GNCTD). The lease expired 31-Jul-2023 and the JV agreement 10-Mar-2018; GNCTD told the Supreme Court on 27-Jan-2026 that renewal would be 'contrary to public interest'. The 5-year outcome is a legal/political binary layered on a good operating business, not an operating-earnings call.

## 2. Variant view (what we believe that the price does not, and why we could know it)
Market: at Rs 356 the stock trades at 17.0x trailing P/E and 9.8x EV/EBITDA net of Rs 521 cr cash, against hospital peers at 33-59x (median 48x) - a ~65% discount that IS the lease risk. A simple two-state read (going concern at ~30x = ~Rs 630/share vs handover value ~Rs 60-90/share) puts the price-implied probability of a workable renewal at roughly 50% [EST]. Our view: no claimable mispricing - we have no edge on a Supreme Court / Delhi-government outcome, and the evidence we found leans NEGATIVE relative to how the company presents it: (1) the FY26 annual report, the Q2 FY27 results notes and the MD&A do not mention that the lease and JV agreement have expired or the January affidavit (only a 3-Feb-2026 board-outcome paragraph 'noted' it), while the contingent-liability note says the company 'has remained compliant with the applicable requirements under the lease'; (2) the Delhi government (26% holder, a promoter) did not vote its shares at the 24-Sep-2026 AGM (promoter votes polled 21.44m of 46.75m) and has not nominated its 3 directors including the Chairman; (3) the MD's term ended 4-Nov-2026 with no successor announced; (4) ROIC is flattered by the land subsidy, so any renewal on market or stricter-EWS terms compresses margins. Positive offsets: Rs 521 cr net cash (16% of market cap, Rs 57/share), no debt, steady ARPP-led growth (+11% TTM revenue, 18% OPM), and courts and governments usually prefer stricter terms to closing a 700-bed hospital. What would prove us wrong: a 30-year renewal on terms close to IMCL's own ask (10% IPD / 25% OPD incl. medicines) with no retrospective claim. Departure from the outside view: our raw P(blow-up) 20% and P(<=0.5x) 26% are ABOVE the class base rates (15% / 11%) because of a specific, dated legal threat; anchored at w=0.3 (evidence note). Checked by paper calls thesis:paper-call:INDRAMEDCO:*.

## 3. What the price implies (stage 5)
- **Reverse DCF** (CoE 12.5%, TG 5.0%, ROIIC 30%): revenue CAGR 12.8% for 10 years at a 11.2%→10.0% NOPAT margin; or year-1 growth 19.4% fading to 5.0%. Base case IRR at today's price: 10.9%.
- **Scenario DCF:** probability-weighted value 235.1 (-34% vs price); bear 164.0 (-54%).
- **Twin engine, 3x in 5 yrs** from P/E 17.0: exit P/E 8.5 → EPS CAGR 43%; exit P/E 12.8 → EPS CAGR 32%; exit P/E 15.7 → EPS CAGR 27%; exit P/E 17.0 → EPS CAGR 25%; exit P/E 48.0 → EPS CAGR 1%. Track record: 22.4% FY16 2.66 -> FY26 20.03 = 22.4%/yr [SCR]; driven by OPM 10% -> 18% and ARPP, from a low base; not repeatable at the same rate.
- **Temperature:** P/E 17.0; own history: NORMAL; sector: COLD (0.35x of sector median).
- **Market:** Nifty 50 P/E 20.6: around the long-run average.
- **Reinvestment realism:** last-5y incremental ROIC 40.0%; price-implied ROIIC on the base path none up to 300% (on this growth/margin path no ROIIC reproduces the price); **flag** (>5 pts): default ROIIC (input); scenario bear; scenario base; scenario bull.
- **Exit-multiple bet (L21):** exit P/E used 14.0/20.0/28.0 vs DCF-consistent 14.7/14.8/16.1 vs own median 15.7. EV of the 5-yr multiple at the used exits 1.35x, at DCF exits 0.99x, at the own median 1.02x (hurdle 1.76x).
- Full worksheet: `tools/valuation/live/INDRAMEDCO.json` (re-run `python3 tools/valuation/worksheet.py <input>`).

## 4. Gates and flags
### 4.1 Stage 2: hard filters (non-overridable) and graded flags
Source: S2 checklist in research_notes/Deep dives/INDRAMEDCO_live.md section 1 (AR FY26 auditor's report + CARO, 517 NSE announcements to 23-Nov-2026, NSE pledge API 23-Nov-2026 + SHP XBRL 30-Sep-2026, ICRA rating filing 27-May-2026, solvency_screen run 24-Nov-2026).

| Hard rule | Status | Evidence |
|---|---|---|
| H1a fake-cash signal | PASS | Liquid assets Rs 556 cr at 30-Sep-2026 (cash 6.5 + other bank 196.9 + current investments 142.2 + non-current investments 210.9) [Q2FY27 XBRL]; FY26 interest income Rs 27.6 cr on ~Rs 450 cr average (~6%) [AR26 n.23] - consistent |
| H1b economics implausible | PASS | Company KPIs cross-foot: 63,236 discharges x ALOS 3.23 = 204,252 bed-days x Rs 69,714 per bed-day = Rs 1,424 cr = sale of services Rs 1,424.95 cr [AR26 MD&A, n.22]; OPM 18% vs listed hospital peers 15-27% |
| H1c profits unverifiable by outsiders | PASS | Single visible hospital; 607k OPD visits; payers include insurers/TPAs (Family Health Plan Rs 26 cr) and cash; debtor days 28 |
| H2 auditor exit / qualified opinion | PASS | AR FY26 auditor's opinion unmodified; one KAM = free-treatment litigation (SLP 29482/2009); no statutory-auditor resignation; Q2 FY27 limited review filed |
| H3 rating 'issuer not cooperating' | PASS | Credit-rating filings 09-Apr-2024, 28-Apr-2025, 27-May-2026; no INC/withdrawal; no debt outstanding |
| H4 SME/Telegram pump | PASS | Main board since 1990s; NSE volume-spurt queries 16/19-Nov-2026 and price-movement query 09-Oct-2025 (routine); 6-month ADV Rs 11.6 cr mean / 5.5 cr median [YH] |
| H5 related-party cash leakage to promoter entities | PASS | Apollo-group purchases/services ~Rs 82 cr FY26 (5.6% of revenue; Sindoori/Apollo Sindoori housekeeping & food 35.2, reimbursements 19.2, pharmacy consumables 16.7, Vitamed 10.4) vs income from Apollo (pharmacy commission 38.7 + licence fee 1.6) [AR26 n.30.L]; graded as a soft flag (pharmacy economics sit with Apollo) |

| Graded flag | Status | Evidence |
|---|---|---|
| G1 promoter pledge > 25% (v3: >50% strong red) | CLEAR | NSE pledge API 23-Nov-2026: promoter shares pledged 0 (0.00%); SHP XBRL 30-Sep-2026 encumbrance flags false; promoters 51.00% (GNCTD 26.00%, AHEL 22.45%, Reddy family ~0.9%) |
| G2 accounting-trouble events in 5 years | CLEAR | None found |
| G3 dilution | CLEAR | 9,16,73,000 shares unchanged for 10+ years |
| G4 solvency set (S1/S5 India) | CLEAR | solvency_screen 24-Nov-2026: grade blank, 0 flags; ICR ~41x (EBIT/finance cost incl. bank charges); no borrowings |
| Q CFO/PAT 5y (question) | CLEAR | FY22-26 CFO Rs 762 cr vs PAT Rs 614 cr = 1.24x [SCR] |
| Q other-income share | CLEAR | FY26 other income Rs 28.8 cr = 11.7% of PBT (all treasury) |

### 4.2 Stage 3: signals
- **Earnings-surprise (PEAD):** SUE quintile 5 (event 2026-10-29). Avoid flag not active. Rule L19: bottom two quintiles = avoid/exit for ≥63 trading days.
- **Survival cap (v1.3):** clear: pledge 0% of promoter holding and interest cover 41.00x are inside the limits (> 25% / < 1.5x).
- **Promise credibility:** not scored. ar_run.py v1.4 on FY24-26 ARs: 17 candidates, 3 scored (all generic), MCS not meaningful (L37). Disclosure-quality flags are the read: the lease/JV expiry and the GNCTD affidavit are absent from AR FY26 and Q2 FY27 notes; the free-treatment note is boiler-plate carried since FY10; the FY26 note adds 'remained compliant with the applicable requirements under the lease'.

| Detector alert | Date | Detail | Severity |
|---|---|---|---|
| Lease of hospital land expired; government opposes renewal | 2026-01-27 | Lease expired 31-Jul-2023, JV agreement 10-Mar-2018 (GNCTD affidavits per press); IMCL renewal proposal 09-May-2025; GNCTD affidavit 27-Jan-2026: renewal 'contrary to public interest'; IMCL board 'noted' it 03-Feb-2026 (filed 09-Feb-2026); SC hearing listed 19-Mar-2026, outcome not found | high |
| Supreme Court warning | 2025-03-25 | Bench (Surya Kant J) warned it could hand the hospital to AIIMS if poor patients are not treated free; ordered joint inspection | high |
| Delhi government abstains at AGM; board seats vacant | 2026-09-24 | Promoter votes polled 21,442,500 of 46,753,000 (GNCTD's 23.8m not voted); GNCTD yet to nominate 3 directors incl. Chairman [AR26] | med |
| MD term ended | 2026-11-04 | MD Shivakumar Pattabhiraman's 2-year term ended; no successor announced in the 05-Nov-2026 filing | med |

### 4.3 Stage 4: deep-dive soft flags and override log
| Soft flag | Status | What changes my mind | Review |
|---|---|---|---|
| Land lease (Re 1/month) expired 31-Jul-2023; JV agreement expired 2018; GNCTD affidavit opposes renewal; SC threatened AIIMS takeover | OPEN | Executed lease renewal (any term) or an SC order fixing EWS terms short of 33% IPD | 2027-05-31 |
| Disclosure: AR FY26 and Q2 FY27 notes omit the lease/JV expiry and the affidavit; note says 'remained compliant with the lease' while GNCTD alleges 7-10% EWS delivery vs 33%/40% | OPEN | A full Reg-30 disclosure of the lease status and hearing outcomes | 2027-02-15 |
| ROIC ~50% is partly a land subsidy (rent Rs 12/yr; GNCTD funded Rs 15.48 cr of the building; building ownership 'to be decided') - looks-good flag | OPEN | Renewal at a disclosed rent with margin still >= 16% | 2027-11-30 |
| Apollo keeps in-hospital pharmacy economics; IMCL books a commission (Rs 38.7 cr, +29% YoY); pricing formula not disclosed | OPEN | AGM RPT annex disclosing commission rate and term | AR FY27 |
| Advertising/marketing Rs 105 cr = 7.1% of revenue (+23% YoY), high for one hospital; composition undisclosed (agent/facilitator commissions?) | WATCH | Breakdown in AR FY27 or ratio back below 6% | AR FY27 |
| Leadership gap: MD term ended 04-Nov-2026; Chairman seat vacant (GNCTD nominee) | WATCH | MD appointed by Q3 FY27 results | 2027-02-15 |
| Discharges -2% FY26; growth is price/mix (revenue per patient +11%) - ceiling on a single fixed site | WATCH | Discharges growing again with ARPP | AR FY27 |

**Open soft flags: 6** (4 from the deep dive, 2 from stage 3: detector: Lease of hospital land expired; government opposes renewal; detector: Supreme Court warning), plus 3 dated watch item(s). Rule: ≥3 open soft flags means no position without a written variant view.

Override log (a management explanation alone never clears a flag; L10, L12):

| Date | Flag | Decision | Why (external evidence) |
|---|---|---|---|
| 2026-11-24 | Hand classification of an unindexed name | INDRAMEDCO entered the frame via the pre-registered hand list (Healthcare) | 482 in-range names lacked an index industry; list written before the shuffle |
| 2026-11-24 | Expired lease vs S0 scoreability | kept as subject: the listed entity survives the call horizon even if it loses the hospital (rule a is about the entity ceasing to exist); the lease risk goes into tails and calls | Pre-registered rule wording; disclosed |
| 2026-11-24 | Credibility score | no score used; AR-mode disclosure flags instead (L37) | No concalls; n=3 generic promises |

## 5. Probabilities (5 years), with base rates alongside
| Event | Model (worksheet) | Base rate | Model ÷ base | Anchored (w=0.30 on base) |
|---|---|---|---|---|
| P(≥3x in 5 yrs) | 7% | 21.3% [95% CI 14.1%–28.7%] | 0.33x | not anchored |
| P(≤0.5x in 5 yrs) | 26% | 11.3% [95% CI 7.0%–16.1%] | 2.29x | 21.4% |
| P(blow-up) | 20% | 15.4% [95% CI 10.2%–21.4%] | 1.30x | 18.6% |

**Outside-view anchoring (v1.2, L36):** anchored P = 0.30 × base rate + 0.70 × model for P(≤0.5x) and P(blow-up) (weight: evidence: Weighted LESS toward the class (w=0.3 < 0.5) because the raw tails are ABOVE the class rates for a specific, dated, documented reason: land lease expired 31-Jul-2023; GNCTD affidavit 27-Jan-2026 opposing renewal; SC 25-Mar-2025 warning of an AIIMS takeover. Anchoring at 0.5 would pull P(blow-up) DOWN toward 15% on no evidence.). The expected-value gate and Kelly use the anchored tails; the paper calls keep the raw model probability (with the anchored one alongside), so Brier scoring can tell which was better. This is a calibration safeguard, not a change to the hurdle. The default weight is 0.5; a lower weight needs a written evidence note, never below 0.25.

Base-rate class: **India non-financial, mcap Rs 1,000-20,000 cr at T, 5 yrs from 30-Sep-2016 and 30-Sep-2018 (survivorship-free, dead firms included, stratum-weighted)** (n=208, 5-yr horizon). Source: research_notes/Backtests/base_rates_5y.md; tools/backtests/base_rates_5y/build.py on research_notes/Backtests/solvency_india_outputs/panel.csv (= hard_filters_india_v2_outputs/panel_v2.csv, same 489 rows); outputs research_notes/Backtests/base_rates_5y_outputs/results.json. Caveats: n=208 company-snapshots (54 distress-census D, 153 live L at weight 5.63, 1 delisted-other X at 4.26); 95% CIs (company bootstrap within stratum): P(>=3x) 14.1-28.7%, P(<=0.5x) 7.0-16.1%, P(blow-up) 10.2-21.4%. Two start dates only, and they disagree (2016: >=3x 16%, blow-up 21%; 2018: 26%, 10%). Price return only (no dividends, ~1%/yr). Blow-up = close <=0.2x the close at T, liquidation or compulsory delisting (no fraud field). Remaining survivorship leak toward FEWER failures (IBBI firms renamed/merged and 221 IBBI rows without identifiers missing; voluntary/merger delistings X under-covered). A survivors-only sample from the same frame says P(<=0.5x) 7% instead of 11%.
Blow-up = Close falls >= 80% below the entry price at any point within the horizon, OR delisting/insolvency/suspension, OR a regulator or auditor finding of fraud or misstatement. No class above can measure this yet (survivor samples).

Model probabilities come from the scenario multiples with lognormal dispersion σ=0.30 (worksheet block b). They are only as good as the scenario inputs.

> **Departure from the outside view:** P(≥3x in 5 yrs) is 0.33x the base rate; P(≤0.5x in 5 yrs) is 2.29x the base rate. A model this far from the base rate (either way) is a claim of knowledge the reference class lacks: justify it in §2 (variant view) or by a known bias of the class (see caveats), or pull the probabilities toward the base rate.

## 6. Expected value
| EV of 5-yr multiple | EV CAGR | Median multiple | Hurdle (index 12%/yr) | Prob-weighted DCF value | Bear downside |
|---|---|---|---|---|---|
| 1.35x | 6.1% | 1.35x | 1.76x | 235.1 (-34%) | -54% |

Two views on purpose: the 5-year multiple uses the exit P/E each scenario states (how the market might pay); the DCF value uses this worksheet's cost of equity (what the cash flows justify). When they disagree, the card says so; the gap itself is information.

**Anchored EV (v1.2, used by the gate):** 1.39x (raw model 1.35x). Tails reweighted to P(blow-up) 18.6% and P(≤0.5x) 21.4%; the rest of the distribution is scaled in proportion, its shape kept.

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
| 1 | SC order or GNCTD decision refusing lease renewal / directing handover | Reg-30 filing; SC order on SLP(C) 29482/2009 | 2027-11-30 |
| 2 | Renewal or order requiring free treatment above 20% of IPD including medicines, or a retrospective recovery claim > Rs 200 cr | Reg-30; AR FY27 contingent-liability note | 2027-11-30 |
| 3 | No MD appointed by 31-Mar-2027 | Reg-30 | 2027-03-31 |
| 4 | Modified audit opinion or emphasis of matter on going concern / lease | AR FY27 | 2027-09-30 |

## 9. Pre-mortem ("it is 2031 and this went badly; why?")
1. The Supreme Court accepted GNCTD's position in 2027; the hospital was transferred to a government operator against compensation for equipment only; IMCL became a cash shell worth ~Rs 60-80/share and minority holders waited years for distribution.
2. A renewal came with a market-linked lease rent and a monitored 33% IPD free quota including medicines; EBITDA margin fell from 18% to ~8% and the P/E stayed in the teens on halved earnings.
3. Apollo prioritised its own Delhi-NCR hospitals for growth and referrals; IMCL's discharges kept falling while ARPP growth slowed.
4. A retrospective claim for under-delivered free treatment since 2009 (or for medicines) was booked as a large exceptional item.

## 10. Gate log (how the rule output was reached)
| Gate | Result | Blocks size? |
|---|---|---|
| Stage 2 hard filters | passed (7 rules) | no |
| Stage 3 PEAD avoid flag | clear | no |
| Stage 3 survival cap | clear | no |
| Stage 4 soft flags | 6 open, variant view written | no |
| Expected value vs hurdle | EV 1.39x anchored (raw 1.35x) vs hurdle 1.76x → below hurdle → size 0 | yes |

---
*Research, not SEBI-registered advice. Every probability on this card is also written as a dated paper call so it is scored later (Brier vs base rate). Template: `tools/decision/decision_card.md`; generator: `tools/decision/decision_card.py`.*

