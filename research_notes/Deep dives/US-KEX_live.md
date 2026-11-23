# Kirby Corporation (NYSE: KEX) — LIVE deep dive #2, first US live run (method test, protocol v1.3, stages 2→7)

**Date:** 2026-11-23 · **Analyst:** Claude · **Status:** live (not practice). Its paper calls are scored.
**Purpose:** measure whether the deep-dive method has forecasting skill on a US filer (`memory/strategy_review.md` §3 item 2b;
roadmap stages 2→7). The company was **drawn at random** from an SEC-built frame. This is test material (L9, L21): **no buy/sell
verdict**. Outputs are a decision card and dated probabilistic calls, each scored later against a naive base rate.
**Roadmap:** builds stage 4 (deep dive), 5 (valuation) and 6 (decision) and feeds stage 7 (scoreboard). Unlocks the second live Brier
comparison of deep-dive probabilities vs base rates, and the first on SEC-XBRL-resolvable calls (`strategy_review.md` §4 q2).
Research, not SEBI/SEC-registered advice.

Source tags: `[10K25]` 10-K FY2025 (filed 17-Feb-2026, acc. 0001193125-26-054016) · `[10K24]` 10-K FY2024 (18-Feb-2025) ·
`[10Q3-26]` 10-Q Q3 2026 (6-Nov-2026) · `[PR-Qn-yy]` 8-K Item 2.02 Ex-99.1 earnings release · `[8K-date]` other 8-Ks ·
`[XBRL]` `sec_fetch.py facts` (companyfacts) · `[F4]` `sec_fetch.py insider` · `[13F]`/`[13G]` · `[YH]` Yahoo v8 daily closes ·
`[EST]` my estimate (method shown next to it). $ unless stated; M = million.

---

## 0. Selection (rules written 2026-11-23 before the frame was built or any name was seen)

**Rule (from the task):** US frame from SEC data via `tools/sec_fetch.py`; public float $500M–$10B on the latest 10-K cover; exclude
financials, REITs, utilities, SPACs and biotech without revenue; sort by CIK; shuffle with `random.Random(20261124)`; walk; the first company
that passes the stage-2 filters becomes the subject. Every skip is logged.

**Operational definitions (fixed before the frame was built):**
1. **Candidates:** every CIK in the `dei:EntityPublicFloat` frames CY2024Q3I … CY2026Q2I (8 instant frames, `sec_fetch.py frames
   EntityPublicFloat <P> --taxonomy dei --raw`) with any frame value in a loose band $250M–$15B.
2. **Latest 10-K:** the most recent `10-K`/`10-KT` (amendments ignored) filed 2025-08-23 … 2026-11-23 (a live filer: ≤15 months old), from SEC
   submissions. **Float** = the `EntityPublicFloat` fact carried by that accession (frame row with the same accession; else
   companyconcept, summing share classes at the latest date). Keep $500M ≤ float ≤ $10B.
3. **Exclusions by current SIC (submissions):** 6000–6799 (banks, insurers, brokers, REITs 6798, blank checks/SPACs 6770, funds),
   4900–4949, 4961, 4991 (utilities), missing SIC. **Biotech without revenue:** SIC 2833–2836 or 8731 and latest-FY revenue on that 10-K
   (`Revenues` or `RevenueFromContractWithCustomerExcludingAssessedTax`, max) < $10M or untagged.
4. **Order:** frame CIKs sorted ascending (int), `random.Random(20261124).shuffle`, walk from the top.
5. **Stage-2 checks per walked name (in this order; first failure = skip):**
   a. **Pending merger / scoreability:** any DEFM14A/PREM14A/DEFM14C/PREM14C/SC TO-T/SC 14D9/SC 13E3/Form 25/15 filed by or about the
      issuer since 2025-11-23, or an 8-K 1.01/2.01 announcing a sale of the company, without a later termination → skip (entity may not exist
      through 2027-09-30; `decision:live-dd-selection-rules`).
   b. **8-K 4.02** (non-reliance/restatement) since 2023-11-23 → skip. **8-K 4.01** since 2023-11-23 → read it; skip only if it reports a
      disagreement or a reportable event (Item 304(a)(1)(iv)/(v)).
   c. **Going concern / material weakness** in any 10-K or 10-Q filed since 2023-11-23: EDGAR full-text search on the CIK for
      "substantial doubt" + "going concern" and "material weakness"; every hit is opened and read (risk-factor boilerplate such as "if we
      identify a material weakness" does not count; an actual conclusion that ICFR/disclosure controls were not effective, or an auditor /
      management going-concern paragraph, does).
   d. **Solvency S1 and S5** (definitions of `research_notes/Backtests/solvency_flags_us.md`, code of
      `tools/backtests/solvency_us/s3_flags.py::snapshot` with T = 2026-11-23, i.e. the latest 10-K's first-reported facts) → skip if
      either fires.
   e. **Earnings-surprise avoid window (if computable):** US SUE proxy = seasonal-random-walk EPS surprise (formula of
      `india_pead/live_tracker.sue_for`) on SEC calendar-quarter EPS frames (diluted, else basic). Bottom quintile = below the 20th
      percentile of SUE across all frame members for the same calendar quarter. Skip if the latest reported quarter is bottom-quintile
      and today is within 63 trading days (~91 calendar days) of its 8-K Item 2.02 (or 10-Q) date. Not computable → noted, not a skip.
   f. **Judgment notes** (not mechanical skips unless they meet (a)–(e)): Chapter 11, delisting notices (8-K 3.01), auditor resignations.

**How it was run** (scripts in the scratchpad `live_dd2/scripts/`: `sel1_fetch.py`, `sel2_frame.py`, `sue.py`, `sel3_walk.py`):
1. **Candidates.** 8 float frames → **2,161 CIKs** in the loose band. SEC submissions fetched for all.
2. **Funnel (exact frame):** financial/REIT/SPAC SIC 577 · utilities 53 · missing SIC 35 · no 10-K in the 15-month window 8 · no float
   fact on the latest 10-K 3 · float outside $500M–$10B 403 · biotech/pharma without revenue 45 → **1,037 companies in the frame**
   (975 floats matched a frame row by accession, 62 read from companyconcept).
3. **SUE cut-points** (same calendar quarter, frame members with a computable SUE): CY2026Q3 n=821, quintile cuts −0.576 / 0.048 /
   0.589 / 1.670; CY2026Q2 n=884, −0.535 / 0.021 / 0.555 / 1.464.
4. **Order drawn (first 10):** **KEX (Kirby)**, GNTX, SOUN, SERV, AEVA, LIVN, BFAM, PBF, NN, KYMR.

**Walk log:**
| # | Company | Float (10-K cover) | Result | Evidence |
|---|---|---|---|---|
| 1 | **Kirby Corp (KEX)**, CIK 56047, SIC 4400 water transportation | $6.30bn (30-Jun-2025, 10-K filed 17-Feb-2026) | **SUBJECT** | (a) no merger forms; the only DEFA14A (6-Mar-2026) is the annual-meeting notice; the only 8-K 1.01 (30-Mar-2026) is the amended $750M revolver to 2031; FTS "Agreement and Plan of Merger" in 8-Ks since Nov-2025: 0 hits. (b) no 8-K 4.01 or 4.02 since 23-Nov-2023 (auditor KPMG). The submissions file holds one older 8-K 4.02, on 10-Jul-2020: Q1-2020 was restated for a goodwill-impairment error. That is outside the 3-year window and is graded in §1. (c) FTS "going concern"+"substantial doubt": 0; "material weakness": 0 hits in 10-K/10-Q since Nov-2023; 10-K FY2025 Item 9A: disclosure controls and ICFR **effective**, KPMG ICFR opinion. (d) solvency S1 0, S2 0 (EBIT $496M / interest $46M = 10.7x), S3 0, S4 0, **S5 0**. (e) SUE CY2026Q3 **+2.58 → quintile 5** (8-K 2.02 on 28-Oct-2026, inside 63 trading days but top quintile); CY2026Q2 0.00 → quintile 2. |

No skips were needed: the first name drawn passed. (For the record, names 2–4 were also run mechanically: GNTX clean, SUE Q2; SOUN S2 fired
(loss-making) but S5 0; SERV had an 8-K 4.01 on 6-Mar-2025 and a material-weakness hit in its FY2024 10-K/A, so it would have needed reading.
None of this affects the draw.)
**Tool fix made during selection:** `sec_fetch.py frames` built per-share units as `USD/shares`, which the frames API rejects (404); it now
uses `USD-per-shares` (one line). Noticed when pulling the EPS frames for the SUE cut-points.

---

## 0b. Rule zero: edge before depth
1. **What the market already knows.** Kirby is the largest US inland tank-barge operator. The inland cycle is tight: utilization is in the
   low-90% range, and industry newbuilds only replace retirements. Power generation for data centers is the growth story in the distribution
   and services segment (KDS). The questions analysts asked on the Q3-26 call (Motley Fool transcript) were: marine pricing durability; coastal
   margins and shipyard timing; the power-gen backlog and when it converts; whether margins grow again in 2027 as fuel changes; how much of
   the book reprices in Q4; and how long the demand tailwinds last (Venezuelan crude, Middle East disruption, Calcasieu, the 2028 maintenance
   cycle).
2. **The variable that would move value most if we knew it better than consensus:** the *through-cycle* inland margin and return on capital.
   Is ~20% inland margin / ~10% return on total capital (ROTC) the new floor, or a cyclical high on a fleet bought at rising prices? Second:
   whether KDS power-gen growth is durable or a one-off order bulge.
3. **The layers most likely to reveal it:** L3 (barge unit economics vs acquisition prices), L4 (fuel and crew pass-through mechanics), and
   the 10-K diff (escalators, term mix, newbuild counts).

---

## 1. S2 checklist (filled before L1; every rule dated)
| Rule | Status | Evidence (source, date) |
|---|---|---|
| H1a fake cash | **pass** | Cash is only $38.3M (30-Sep-2026) `[PR-Q3-26]`. Value sits in the fleet: 1,148 inland and 27 coastal tank barges, 294 towboats operated. KPMG gave an effective ICFR opinion for FY2025 `[10K25 9A]`. |
| H1b implausible economics | **pass** | Inland revenue $460.1M = 4,183M ton-miles × 11.0¢ (Q3-26), re-derived. FY2025: 13,977M ton-miles × 11.1¢ ≈ $1,551M vs ~80% × $1,935M marine revenue ≈ $1,548M. |
| H1c unverifiable profits | **pass** | Five KMT customers ≈ 17% of revenue; three KDS customers ≈ 9% `[10K25]`. OEM franchises (MTU, Allison, Daimler ≈ 12% of revenue; also Cummins and EMD) can be checked with the OEMs. |
| H2 auditor exit / opinion | **pass** | KPMG; FY2025 financial-statement and ICFR opinions unqualified. No 8-K 4.01. |
| H3 credit stress | **pass** | $750M revolver amended and restated 26-Mar-2026 to 2031, at SOFR + 87.5–150 bp depending on rating. Covenants: ICR ≥ 2.5x; debt/cap ≤ 60% vs 23.7% actual `[8K-20260326]`. |
| H4 pump pattern | **pass** | NYSE; 6-month ADV $76.7M `[YH]`. Large institutions are the main holders. |
| H5 RPT leakage | **pass** | No Item 404 transactions found in the 2026 proxy. CEO total pay $6.74M, 66:1 vs the median employee ($101,978) `[DEF14A]`. |
| Exit trigger 8-K 4.02 | **none in 3 years** | One 4.02 on 10-Jul-2020: the Q1-2020 goodwill impairment was understated (ASU 2017-04 tax effect missed). KPMG concurred, and a material weakness was flagged at the time `[8K-20200710]`. |
| G accounting trouble (5 y) | **fired (borderline)** | The 2020 restatement is 6.4 years old. EDGAR full-text search finds no "material weakness" hit since Nov-2023. Watch: the Controller (30 years at the company) retires after the FY2026 10-K `[8K-20261006]`. |
| G dilution | **clear** | Shares fell from 60.2M (2021) to 52.0M (Oct-2026). 5.2M shares remain authorised for buybacks (5-Nov-2026) `[10Q3-26]`. |
| G solvency S1/S5 | **clear** | S1 0, S2 0 (EBIT $496M / interest $46M = 10.7x), S3 0, S4 0, S5 0. |
| Q CFO/NI | ok (watch) | FY2025 CFO/NI = 1.89. But 9M-26 CFO was $313M vs $358M a year earlier, and receivables were +36% YoY vs revenue +12%. |
| Q receivables | **question** | AR rose from $524M to $711M (Sep-25 → Sep-26). The company cites collection timing and fuel-related receivables `[PR-Q3-26]`. |

**Stage-3 signals.** US SUE proxy CY2026Q3 **+2.58 → quintile 5** (event 28-Oct-2026: EPS $2.09 vs $1.65, +27%). Credibility: hand ledger
in §7 (79%, n=12; peer median 84%).

---

## 2. Map (L1): what is the unit?
**Business.** KMT (marine transportation; 57% of FY2025 revenue, 75% of segment operating income) moves petrochemicals (48% of marine
revenue), black oil (26%), refined products (23%) and agricultural chemicals (3%) by tank barge `[10K25]`:
- **Inland:** ~80% of marine revenue. Mississippi River System and the Gulf Intracoastal Waterway. 1,105 barges = **28% of the ~4,004-barge
  industry fleet** (FY2025).
- **Coastal:** ~20%. 28 barges and 24 tugs, ~100% under term contracts.

KDS (43% of revenue) is mainly a distributor and packager:
- Engines and power-generation packages (MTU, Cummins, EMD).
- Allison transmissions; on-highway service.
- Marine repair.
- E-frac equipment.

Power generation was ~52% of KDS revenue in Q4-25 and ~46% in Q3-26; the backlog is "north of $1.5bn" with book-to-bill > 1 (Q3-26 call).

**Units:**
1. The **tank barge** (revenue and EBITDA per barge; ton-miles per barge).
2. The **towboat + crew** (horsepower; ~¼ of horsepower is chartered).
3. The **contract** (term 70% / spot 30% of inland revenue in 2025; time charters 59% of term).
4. For KDS, the **OEM franchise territory** and the **power-gen backlog**.

For a widely held US company, the "related party" is management (protocol v1.2).

**Peers:** no listed pure inland tank-barge peer exists (Ingram, ACBL, Canal Barge and Marquette are private). Matson is the nearest Jones Act
comparison (14.5x FY25 EPS). Cummins (OEM, 19.7x) and Generac (power gen; FY25 EPS depressed) are KDS references.

---

## 3. Reported financials, re-derived (L2) `[XBRL]` ($M)
| FY | Revenue | Op income | Op margin | Net income | Dil. EPS | CFO | Capex | FCF | Buybacks | Shares out (M) |
|---|---|---|---|---|---|---|---|---|---|---|
| 2016 | 1,771 | 247 | 14.0% | 141 | 2.62 | 416 | 231 | 185 | 2 | 54.0 |
| 2017 | 2,214 | 94 | 4.2% | 313 | 5.62* | 353 | 177 | 176 | 0 | 59.7 |
| 2018 | 2,971 | 155 | 5.2% | 79 | 1.31 | 347 | 302 | 45 | 1 | 59.9 |
| 2019 | 2,838 | 242 | 8.5% | 142 | 2.37 | 512 | 248 | 264 | 0 | 60.0 |
| 2020 | 2,171 | −421 | — | −273 | −4.55 | 445 | 148 | 297 | 0 | 60.1 |
| 2021 | 2,247 | −258 | — | −247 | −4.11 | 322 | 98 | 224 | 0 | 60.2 |
| 2022 | 2,785 | 193 | 6.9% | 122 | 2.03 | 294 | 173 | 122 | 23 | 60.0 |
| 2023 | 3,092 | 335 | 10.8% | 223 | 3.72 | 540 | 402 | 138 | 113 | 58.5 |
| 2024 | 3,266 | 399 | 12.2% | 287 | 4.91 (adj 5.46) | 757 | 343 | 414 | 175 | 57.1 |
| 2025 | 3,364 | 496 | 14.8% | 355 | 6.33 | 670 | 265 | 406 | 354 | 53.6 |
| 9M-26 | 2,744 (+9.2%) | 381 (13.9%) | | 282 | 5.26 (+13.4%) | 313 | 189 | 124 | 224 | 52.0 |
\*2017 includes the tax-reform deferred-tax gain. 2020–21: impairments in KDS (oilfield) and inland write-downs.

**Adjustments that matter:**
- **2024 one-offs.** $56.3M impairment of conventional-frac inventory and a Louisiana tax-law credit. Adjusted EPS was 5.46; the proxy also
  computes 2025 growth on this base (+16%).
- **2025 FCF $406M > NOPAT ~$374M.** Two reasons: (a) deferred tax of $82M; the One Big Beautiful Bill Act restored 100% bonus depreciation,
  and income tax payable fell 100%; (b) capex of $264.5M ≈ D&A of $255M. For a fleet that keeps replacing itself, the cash-tax deferral is
  quasi-permanent. This matters for valuation (§8).
- **SBC is small:** $17.6M, 0.5% of sales, 4% of FCF. Buybacks of $354M (2025) shrank the share count 6%, which is the real owner return
  (no dividend).
- **Segment walk FY2025** `[PR-Q4-25]`:
  - KMT: revenue $1,935.3M, operating income $374.5M (19.3%).
  - KDS: revenue $1,428.7M, operating income $130.8M (9.2%).
  - Corporate: −$13.7M.
- **Quarterly pattern.** Q1 is the weakest quarter (winter delays): Q1-26 operating margin 12.8%, Q2 13.3%, Q3 15.4%. Q4-25 was 15.2%, helped
  by corporate expense of only $0.7M (vs $5–9M in other quarters).
- **Working capital.** Receivables went from $474M (Dec-25) to $711M (Sep-26), with fuel-related billings and power-gen deliveries.
  Inventory was built in late 2025 for 2026 power-gen deliveries `[10K25]`.

---

## 4. Unit economics (L3): the tank barge, FY2025
| Line | Value | Method |
|---|---|---|
| Inland revenue | ~$1,550M | 13,977M ton-miles × 11.1¢ `[PR-Q4-25]` = ~80% of marine revenue (two routes agree within 0.2%) |
| Revenue per active barge | **~$1.40M/yr** | ÷ 1,105 barges; ton-miles per barge 12.6M |
| Revenue per towboat operated | ~$5.6M/yr | ÷ 279 average towboats (~4 barges per towboat) |
| Inland operating income | ~$300M (≈19–20%) | KMT $374.5M less coastal ~20% × ~$387M ≈ $75M [EST] |
| Inland EBITDA per barge | **~$430k** | ($300M + ~80% of marine D&A $214M) ÷ 1,105 [EST] |
| Maintenance capex per barge | ~$150–190k | Marine maintenance guide $170–210M ÷ ~1,130 barges + boats [EST] |
| **Price paid per barge-equivalent (incl. ~¼ towboat)** | **$4.2–8.2M** | Mar-2025: 14 barges + 4 high-hp boats, $97.3M → $6.95M/barge · Q1-26: 23 barges + 3 boats, $95.8M → $4.17M · Nov-26: 14 barges (avg age 10) + 9 boats + 9 bow thrusters + a 65-acre fleeting site, $115M → $8.2M `[10K25, PR-Q1-26, 10Q3-26]` |
| Pre-tax cash yield on acquisition price | **~3–6%** after maintenance capex; 5–10% on EBITDA | $250–280k ÷ $4.2–8.2M [EST] |

**Finding.** At today's rates, buying fleet earns *below* a 9.5% cost of equity on replacement-like prices. The fleet's book ROTC (10.4%,
2023–25 `[DEF14A]`) looks fine only because older barges sit at depreciated cost. This is also why the industry does not overbuild:
- 2023: 27 new barges vs 48 retired.
- 2024: 34 new vs 38 retired.
- 2025: 66 new vs 65 retired.
- 60–70 are on order for 2026 `[10K25]`.

About 600 industry barges are 30+ years old. Read the other way, rates must keep rising to justify replacement. That is bullish for pricing
and bearish for return on incremental capital. **Gap:** the 10-K mentions Kirby's average newbuild price but does not state it. The current
cost of a new 30,000-bbl barge is open (ask a Gulf shipyard; see L6).

---

## 5. Cost drivers in physical terms (L4), ranked by weight (KMT, FY2025, % of marine revenue $1,935M)
| Line | % | Physical driver | Sensitivity |
|---|---|---|---|
| Cost of sales & operating (total) | 60.7% | crew, fuel, maintenance/shipyard, chartered towboats, insurance | — |
| ↳ Crew wages + load [EST] | ~14% | **2,337 vessel crew** `[10K25]` × ~$85k average wage [EST from BLS OEWS water-transport occupations, unverified] × 1.35 load ≈ $270M | +5% wage step ≈ $13M ≈ **70 bps**. The mariner shortage is still cited in the Q3-26 10-Q |
| ↳ Fuel (diesel) | **~8%** (company figure) | Inland 49.3M gallons × $2.47 = $122M (2025). 2026 9M average **$3.49/gal**; Q2 $4.23, Q3 $3.91 | $0.10/gal ≈ $5M/yr ≈ 26 bps gross. Term contracts carry escalators with **up to a ~120-day lag** (Q3-26 call); spot prices fuel at signing |
| ↳ Chartered horsepower | n/d | ~¼ of horsepower is chartered `[10K25]`; operating leases $215.6M | flexes with demand |
| D&A | 11.1% | fleet, average age ~16 years (industry ~18) | — |
| SG&A | 7.5% | shore staff | — |

**Micro-drivers to watch (dated, public, leading):**
- **EIA Gulf Coast diesel weekly:** the escalator lag means a fall in fuel *widens* margins for ~1 quarter.
- **Gulf Coast refinery utilization** (EIA weekly).
- **Lock closures** (USACE Lock Performance Monitoring) and delay days: Q3-26 1,809 vs 1,442.
- **Jones Act waiver notices** (DHS/CBP; current expiry 14-Feb-2027).
- **Annual 1-January escalators:** +9.5% (2024) → +3–5% (2025) `[10K25 vs 10K24]`.

**KDS:** cost of sales 73% of revenue, mostly OEM product at franchise pricing. The margin driver is the mix of power-gen packaging and
service vs new-unit pass-through (high-single to low-double-digit margins).

---

## 6. Governance, ownership, incentives (L5): the US version
- **Pay design** `[DEF14A]`:
  - Annual incentive plan (AIP): EPS 30%, EBITDA 40%, ROTC 10%, operating/ESG 20%.
  - Long-term plan: cumulative EBITDA 50%, ROTC 50%. The 2023–25 award paid 122.9% (EBITDA $2,047M vs target $1,947M; ROTC 10.4% vs target
    9.5%).
  - EPS and EBITDA reward buyback-funded and acquisition-funded growth; ROTC partly offsets this.
  - Amendments approved 27-Apr-2026: the cash performance-award cap was **doubled** from $5M to $10M, and the plan was extended to 2036
    (with a new clawback) `[8K-20260427]`.
- **Related parties:** no Item 404 transactions found. **Board:** Tracy Embree joined on 16-Feb-2026 (ex-President of Cummins Distribution;
  power-gen expertise). The VP & Controller retires in Q1-2027.
- **Insiders `[F4]`** (12 months to 2-Nov-2026): **21 open-market sales by 10 insiders, $22.2M, 0 buys.** Most are option exercise-and-sell
  (code M + S) by the CEO, COO, GC and Controller:
  - CEO: 29,451 shares at $107 (Nov-25); 34,152 at $130 (Feb-26); 18,310 at $141.32 (2-Nov-26, after Q3).
  - An 8-insider cluster followed the Feb-2026 vesting.
  - The tool flagged 19 as non-10b5-1; the checkbox was not verified on each form.
  - L14: sales after a rally and vesting are weak evidence. Recorded as low.
- **13G/13F `[13G]`:**
  - BlackRock 10.4% and Vanguard 10.1% (proxy, Dec-25 13F).
  - Vanguard's 13G/A of 27-Mar-2026 shows **0%**. This is a **realignment, not a sale**: Vanguard Capital Management (5.17%, Mar-26) and
    Vanguard Portfolio Management (5.03%, Jun-26) now file separately (the FIVE lesson repeated).
  - Dimensional 5.2% (Jun-26); Goldman Sachs AM 5.1% → 4.4% (Mar → Jun 2026, a trim); Morgan Stanley/Atlanta Capital 4.7% (Dec-25).
- **Capital allocation:** buybacks of $224M in 9M-26 at an average $134.82, plus $41.5M more by 5-Nov. Total debt rose from $919M to $1,072M,
  so buybacks are partly revolver-funded. Three fleet acquisitions totalled $308M in 20 months.

### 6.1 10-K diff FY2025 vs FY2024 (judgment cue, L29–L30: not a mechanical signal)
| Change | Reading |
|---|---|
| Annual contract escalators: "approximately 9.5%" (1-Jan-2024) → "3% to 5%" (1-Jan-2025) | Pricing momentum **halved**. The 2026 figure is not in the text; Q3-26 renewals were "low-single-digit" |
| Term share of inland revenue 60% → 65% → 70% (2023–25); time charters 63% → 61% → 59% of term | More revenue locked in (less spot upside, more fuel-escalator exposure) |
| KDS description now leads with "behind the meter" and "data centers"; **new risk factor** on prime-power/data-center demand; Q3-26 10-Q adds "government priorities could delay data-center investment" | The narrative is moving toward power gen, along with its concentration risk |
| Inventory build "mainly due to power generation orders … scheduled to be delivered in 2026" | 2026 KDS revenue was partly pre-built |
| Newbuild counts 34 → 66 delivered; 60–70 ordered for 2026 | Supply discipline still holds (≈ retirements), but newbuilding is ticking up |
| Added: tariff-recovery contract language in KDS; AI-use policy | Routine |
| Deleted from the MD&A outlook: "acute mariner shortage … continues to drive up labor costs" (softened; the 10-Q still says "mariner shortage") | Wage pressure easing slightly |
**Diff verdict:** neutral-to-slightly-negative on pricing (escalators), positive on visibility (term share), and a new concentration risk in
KDS. **10-Q Q3-26 addition:** the Jones Act waiver risk factor (first waiver 17-Mar-2026; extended to 15-Nov-2026 and then, per press reports
of 13–16 Nov 2026, to **14-Feb-2027**; [WEB: OGJ, gCaptain, Hawaii News Now]).

---

## 7. Promise tracker: last 6 calls (8-K Ex-99.1 outlook paragraphs, Q2-25 → Q3-26; Q3-26 cross-checked with the Motley Fool transcript)
`tools/promise_tracker/pipeline` has no SEC fetcher (README v1.3: US ledgers are built by hand from Ex-99.1 releases). Ledger:
| # | Made | Promise | Outcome | Score |
|---|---|---|---|---|
| 1 | 31-Jul-25 | FY25 EPS growth 15–25% ("closer to the lower end" if softness persists) | +15.9% on adj 5.46 → 6.33 | delivered (low end) |
| 2 | 31-Jul-25 | Inland Q3 utilization "low 90% range" | mid-80% | **missed** |
| 3 | 31-Jul-25 | Inland margins "remain in the 20% range" | Q3 high-teens; Q4 low-20s | **missed** |
| 4 | 31-Jul-25 | Coastal margins mid-to-high teens, modest H2 improvement | ~20% in Q3 and Q4 | delivered (beat) |
| 5 | 31-Jul-25 | KDS FY revenue flat to slightly up, high-single-digit margin | +5.6%, 9.2% | delivered (beat) |
| 6 | 31-Jul-25 | CFO $620–720M | $670.2M | delivered |
| 7 | 31-Jul-25 | Capex $260–290M | $264.5M | delivered |
| 8 | 29-Oct-25 | Q4 inland revenue *and* margins improve modestly vs Q3 | margin up (high-teens → low-20s); revenue ≈ flat (79% × 481.7 vs 80% × 484.9) | partly |
| 9 | 29-Oct-25 | Coastal Q4 revenue and margins comparable to Q3 | ~20% margin; revenue +4% | delivered |
| 10 | 29-Oct-25 | KDS FY revenue up mid-single digits, high-single-digit margins | +5.6%, 9.2% | delivered |
| 11 | 29-Jan-26 | Q1-26 the lowest-margin quarter of 2026 | Q1 12.8% vs Q2 13.3%, Q3 15.4% | delivered |
| 12 | 28-Oct-26 | $115M barge/fleeting acquisition to close in Q4-26 | closed 4-Nov-2026 | delivered |
| open | 29-Jan-26 → | FY26 EPS growth 0–12% → 5–15% (Apr) → "upper end" (Jul) → 10–15%, "upper end" (Oct) | 9M +13.4% | open (resolves Feb-2027; call 1) |
| open | 29-Jan-26 | Inland FY revenue +low-to-mid single digits → raised to low-double-digit | tracking above | open |
| open | 29-Jan-26 | Coastal margins high-teens → cut to mid-teens (Oct) | tracking below | open (likely miss) |
| open | 29-Jan-26 | KDS revenue flat-to-slightly up → high-single digits | tracking above | open |
| open | 29-Jan-26 | CFO $575–675M; capex $220–260M (unchanged in all four releases) | 9M CFO $313M; capex $189M | open (call 4) |
**Score:** credit (delivered 1, partly 0.5) = 9.5 / 12 = **79%** vs the US-industrials peer median of **84%**
(`insight:us-industrials-promise-credibility-base-rate`: WTS 100, AOS 65.9, SSD 79.4, LECO 88.5; different sector). **Pattern (same as the US
peers):** company-level financial ranges are met or beaten, because guidance starts low and is then raised (2026: three raises). The misses
are operating-condition calls (utilization and inland margins in a soft Q3-25). **Team:** the CEO (Grzebinski, since 2014) and the CFO
(Kumar) are unchanged, so the whole ledger belongs to one team.

---

## 8. Ground truth plan (L6; not executed)
| Check | Ask / count | Model number it tests |
|---|---|---|
| Gulf shipyard (Houma/Morgan City) or broker | Current price of a new 30,000-bbl inland tank barge and of a 2,000–3,000 hp towboat; lead time | §4 return on incremental capital; newbuild response |
| USACE Lock Performance Monitoring + EIA weekly | Lockages/delays on the Lower Mississippi and the GIWW; Gulf Coast refinery utilization; diesel price | Q4-26/Q1-27 utilization and the fuel-lag margin |
| Two data-center EPC contractors / gensets buyers in Texas | MTU/Kirby lead times, quote validity, cancellation terms | KDS backlog conversion and durability |
| Mariner job boards (Indeed/Glassdoor, Gulf Coast towboat deckhand/mate pay) | Day rates and sign-on bonuses vs 2025 | Crew-cost EST (~14% of marine revenue) |
Ethics: identify yourself honestly; no material non-public information.

---

## 9. Flag override (L7) and valuation (L8)
### 9.1 Override table
| Flag | Kind | Verdict | What changes my mind |
|---|---|---|---|
| Record EPS, P/E 17x forward, inland margin ~20% at low-90% utilization | good-but-misleading? | **OPEN**: cyclical-high earnings | 2027 renewals ≥ high-single digits, utilization ≥ 90% |
| ROTC 10.4% ≈ cost of capital; acquisitions at $4–8M per barge-equivalent | bad | **OPEN** | ROTC > 12% in the 2026–28 award |
| FCF $406M > NOPAT | good-but-misleading | adjusted (bonus depreciation; quasi-permanent while the fleet is replaced) | Change in tax law |
| Receivables +36% vs revenue +12% | unclear | **OPEN** | FY26 CFO ≥ $575M |
| Jones Act waiver | bad | **OPEN** | Lapse on 14-Feb-2027 |
| Power-gen concentration (new risk factors) | unclear | watch | Book-to-bill < 1 for 2 quarters |
| Insider sales, 0 buys | weak bad | watch | ≥ 2 insider buys |
| 2020 restatement; Controller retiring | bad-but-old | watch | Any new MW / 4.02 |
| Trailing P/E "normal vs own history" | good-but-misleading | adjusted: own band full of depressed-EPS years | — |
| Vanguard 13G/A 0% | bad-but-benign | cleared (realignment) | — |
Open soft flags: 4, so a written variant view is required (below and on the card).

### 9.2 What the price implies (worksheet `tools/valuation/live/US-KEX_worksheet.md`; sensitivity `US-KEX_roiic_sens_worksheet.md`)
**Inputs (step 1):**
- Close **$122.89** on 20-Nov-2026 (Yahoo v8 = Nasdaq.com historical).
- FY-end P/Es FY2015–FY2025, with 2020–21 omitted (losses): 12.8, 25.4, 11.9, 51.4, 37.8, 31.7, 21.1, 21.5, 17.4.
- Peers: MATX 14.5, CMI 19.7, GNRC 71.8 (depressed EPS).
- 6-month ADV $76.7M; net debt $1,033.5M (Sep-26; plus the $115M acquisition in Nov); leases $215.6M excluded.

**Scenarios (written before the outputs):**
| Scenario | Probability | Revenue growth (start → end) | Year-10 NOPAT margin | ROIIC | Exit P/E |
|---|---|---|---|---|---|
| Bear | 30% | 1% → 2% | 8.5% (a 2019-type cycle) | 7% | 13x |
| Base | 50% | 5% → 3% | 11.0% | 10% | 16x |
| Bull | 18% | 8% → 4% | 13% | 13% | 19x |
| Blow-up | 2% | — | — | — | 0.3x outcome |
Shared assumptions: CoE 9.5%, terminal growth 3%, payout of FCF 75% (buybacks).

**Outputs (main file, the card input):**
- Probability-weighted DCF **$58.6/share (−52%)**. EV of the 5-year multiple **1.12x** (2.3%/yr) vs the 1.47x hurdle.
- P(≥2x) 6%, P(≥3x) 0.4%, P(≤0.5x) 4%.
- Base-case IRR 6.8%.
- Reverse DCF: no growth rate reproduces the price at a 10% ROIIC; the base growth path needs a **21.7% NOPAT margin**.
- Temperature: trailing 19.4x is NORMAL vs the own median (21.5x) and the sector median (19.7x); forward 17.0x is COOL.

**Sensitivity (written after the outputs, NOT the card input):** ROIIC 12/20/25%. DCF $78/share (base); the price still needs ~11.6%/yr
revenue growth or a 17.4% NOPAT margin; EV multiple 1.17x.

**Why the DCF and the price disagree (the method finding).** The worksheet computes FCF as NOPAT minus reinvestment at the stated ROIIC.
Kirby's *reported* FCF ($406M, a 6.3% yield) is higher than NOPAT because of deferred cash taxes, and capex ≈ D&A. On reported FCF the Gordon
check gives **3.8% perpetual growth at a 9.5% CoE**, which is roughly fair. So the price is fair on cash and rich on economic earnings. Which
reading is right depends on whether bonus-depreciation tax deferral is permanent (for a fleet that keeps being replaced, mostly yes) and
whether 2025's capex ≈ D&A is sustainable for a fleet that is 16 years old (maintenance guide $170–210M vs D&A $255M; acquisitions are extra).
**Exit-multiple bet (L21):** every scenario's exit P/E exceeds the DCF-consistent P/E (8.6/10.8/12.7) by more than 1.25x. The card's 5-year
multiples therefore already assume the market keeps paying above what the worksheet's cash flows justify.

### 9.3 Variant perception
- **What the market appears to price:** an inland up-cycle plus a data-center power story, at 17x forward / 9.5x EV/EBITDA. The stock fell
  16% from $146 (28-Oct, after the Q3 beat) to $122.89, in a falling market (SPY −5.5% from 18 to 20 Nov).
- **Our view:** *no claimable mispricing, mild negative tilt.* We verified:
  - (1) ROTC ≈ cost of capital, near the cycle top.
  - (2) Escalators decelerated (9.5% → 3–5%), and term renewals were flat to low-single-digit in 2025–26.
  - (3) Fuel lag and the Jones Act waiver.
  - (4) Fleet acquisitions at prices that earn ~3–6% pre-tax cash.
  - (5) Working-capital drain and insider selling (weak).
- **What the market may underweight on the positive side:** supply discipline (~600 barges aged 30+ and newbuilds only matching
  retirements); the term share rising to 70% (visibility); the power-gen backlog of > $1.5bn; and buybacks shrinking the share count ~5%/yr.
- **What would prove us wrong:** FY26 EPS ≥ $7.28 (call 1) together with 2027 renewals in the high single digits and power-gen growth > 20%.
  That would be a margin step-up, not buyback arithmetic.

### 9.4 Decision card (`tools/decision/live/US-KEX_card.md`)
**Rule output: size 0**, blocked by *Expected value vs hurdle* (EV 1.12x vs 1.47x).
- Stage 2: all hard rules pass. G2 fired as a borderline (2020 restatement); receivables is a question.
- PEAD quintile 5. Credibility 79% vs a peer median of 84%.
- Open soft flags: 4, with a written variant view.
- Review **2027-02-15**.

The card's live 5-year calls are below. The US base class `us_seasoned_5y` is **not on file**; the seed carries labelled EST bases.
| Call | Model | EST base |
|---|---|---|
| P(≥3x) | 0.004 | 0.10 |
| P(≤0.5x) | 0.039 | 0.12 |
| P(blow-up) | 0.02 | 0.04 |

---

## 10. Forward calls (live; tags paper-call, deepdive-generated, live, us; specs in `tools/scoreboard/specs.json`)
| # | Call (YES if…) | Resolve by | Our P | Naive base | Base-rate reasoning |
|---|---|---|---|---|---|
| 1 | FY2026 diluted EPS **≥ $7.28** (top of the 10–15% guide) — `sec_fact eps_diluted` | 2027-03-31 | **0.35** | 0.50 | Naive: management says "upper end", and the top of a range is a coin flip. Ours: Q4 needs ≥ $2.02 (+20% YoY) against winter, shipyards and the fuel lag |
| 2 | FY2026 revenue growth **≥ 9.0%** — `revenue_growth_pct` | 2027-03-31 | **0.62** | 0.40 | Naive: 4 of the last 10 years had ≥ 9% growth. Ours: 9M +9.2%, Q3 +12.2%; Q4 needs +8.4%; fuel pass-through plus the acquisition |
| 3 | FY2026 GAAP operating margin **≥ 14.0%** — `op_margin_pct` | 2027-03-31 | **0.55** | 0.50 | Naive: persistence (FY25 14.8%, 9M-26 13.9%). Ours: Q4 needs ~14.3% vs Q4-25 15.2% (low corporate cost) |
| 4 | FY2026 capex **$220–260M** — `capex` between | 2027-03-31 | **0.82** | 0.60 | Naive: US-industrial capex-range delivery is weak (pooled 50%), blended with Kirby's 2025 hit [EST]. Ours: Q4 needs $31–71M; Q4-25 was $47M |
| 5 | **Jones Act waiver extended past 14-Feb-2027** (in effect after that date; announced by 28-Feb-2027) — assisted doc_scan + DHS/CBP | 2027-03-15 | **0.55** | 0.50 | Naive: coin flip. Ours: 3-for-3 renewals while fuel stays high; growing opposition |
| 6 | KEX price return **beats SPY** from 20-Nov-2026 ($122.89; SPY $689.81) to 30-Sep-2027 — `price_relative` | 2027-09-30 | **0.42** | 0.45 | Naive: single US stocks beat the index a little under half the time over ~10 months [EST]. Ours: mild negative tilt; partly de-rated already |
Plus the 3 card calls (5-year, to 2031-11-20). The resolver was dry-run on the FY2025 10-K and gives the expected values: eps_diluted 6.33,
revenue_growth_pct 3.0, op_margin_pct 14.75, capex $264.5M.

---

## 11. What this run taught the method (curriculum)
1. **The US selection frame works from SEC data alone.** Float frames (8 quarters) → submissions → 1,037 names in ~25 minutes of fetching.
   The first draw passed, so the skip machinery (pending merger, 4.01/4.02, FTS going-concern/material-weakness, S1/S5, SUE) was exercised on
   names 1–4 but not truly tested. **Tool bug fixed:** `sec_fetch.py frames` per-share units (`USD-per-shares`).
2. **The US SUE proxy needs its own cut-points.** I built them from the same-quarter cross-section of the frame (EPS frames lack fiscal Q4s
   and adjust for no splits). They are uncalibrated: no US PEAD back-test is on file. Also, the card says "bottom two quintiles = avoid"
   (L19) while the task said bottom quintile. The two rules should be reconciled.
3. **Worksheet gap: cash taxes.** The NOPAT-minus-reinvestment DCF under-values capex-heavy US filers with bonus depreciation (Kirby FCF
   $406M vs NOPAT $374M). Proposal for worksheet v1.3: an optional `cash_tax_rate` (or `deferred_tax_share`) input, and a "reported-FCF
   Gordon" line next to the DCF in the card. Without it, EV-vs-hurdle will block every such stock mechanically.
4. **Pricing-led growth breaks a single ROIIC.** Inland growth is mostly rate on an existing fleet, while fleet growth is bought at $4–8M per
   barge-equivalent. Scenarios should separate the price and volume components.
5. **The US base-rate class is missing** (`us_seasoned_5y` is a placeholder). Card calls therefore carry EST bases. Building a CRSP-style
   5-year distribution from the solvency back-test universe (2015/2017/2019 snapshots with R5) is cheap and would fix this. **Next task
   candidate.**
6. **The promise tracker works by hand on Ex-99.1 releases** (12 items in ~30 minutes). A `--sec` fetch mode (Item 2.02 Ex-99.1 →
   candidates.py) would make it routine.
7. **The Vanguard realignment false alarm recurred** (13G/A at 0%), which confirms the FIVE rule.

## 12. Open items
- Newbuild barge and towboat prices (shipyard check).
- Power-gen backlog in a filing (it has only been stated on calls).
- Kirby's 2026 escalator percentage.
- 10b5-1 checkboxes on the 19 "non-plan" Form 4 sales.
- Q4 coastal shipyard days.
- DEF 14A Item 404 text (the TOC was parsed; the section body was not located in the text extract).
- Crew-cost EST against BLS OEWS.
- The US 5-year base class.

## Sources
- 10-K FY2025: https://www.sec.gov/Archives/edgar/data/56047/000119312526054016/kex-20251231.htm · 10-K FY2024: https://www.sec.gov/Archives/edgar/data/56047/000095017025022012/kex-20241231.htm
- 10-Q Q3 2026: https://www.sec.gov/Archives/edgar/data/56047/000119312526451723/kex-20260930.htm
- Ex-99.1 releases: Q3-26 https://www.sec.gov/Archives/edgar/data/56047/000119312526436155/kex-ex99_1.htm · Q2-26 https://www.sec.gov/Archives/edgar/data/56047/000119312526323594/kex-ex99_1.htm · Q1-26 https://www.sec.gov/Archives/edgar/data/56047/000119312526196337/kex-ex99_1.htm · Q4-25 https://www.sec.gov/Archives/edgar/data/56047/000119312526028839/kex-ex99_1.htm · Q3-25 https://www.sec.gov/Archives/edgar/data/56047/000119312525255469/kex-ex99_1.htm · Q2-25 https://www.sec.gov/Archives/edgar/data/56047/000095017025100695/kex-ex99_1.htm · buyback 8-Sep-2025 https://www.sec.gov/Archives/edgar/data/56047/000095017025113520/kex-ex99_1.htm
- 8-Ks: credit agreement https://www.sec.gov/Archives/edgar/data/56047/000119312526131714/kex-20260326.htm · plan amendments https://www.sec.gov/Archives/edgar/data/56047/000119312526196337/kex-20260427.htm · director https://www.sec.gov/Archives/edgar/data/56047/000119312526060772/kex-20260216.htm · Controller https://www.sec.gov/Archives/edgar/data/56047/000119312526417702/kex-20261006.htm · 2020 non-reliance https://www.sec.gov/Archives/edgar/data/56047/000114036120015822/form8k.htm
- DEF 14A 2026: https://www.sec.gov/Archives/edgar/data/56047/000119312526096979/kex-20260306.htm
- Form 4 (sec_fetch insider KEX --limit 80); 13G primary_doc.xml for accessions 0001229262-26-000026, 0002100121-26-000881, 0000354204-26-000840, 0001229262-26-000008, 0002100119-26-000709, 0000102909-26-001676, 0000895421-26-000044
- Q3-26 call: https://www.fool.com/earnings/call-transcripts/2026/10/28/kirby-kex-q3-2026-earnings-call-transcript/
- Jones Act waiver (Nov-2026 extension): https://www.ogj.com/general-interest/government/news/55419532/white-house-extends-jones-act-waiver-for-another-90-days ; https://gcaptain.com/jones-act-waiver-extended-another-90-days-as-u-s-maritime-groups-sound-alarm/ ; https://www.hawaiinewsnow.com/2026/11/14/trump-reportedly-extends-jones-act-waiver-debate-continues-over-savings-impact/
- Prices: Yahoo v8 KEX/SPY/IWM/MATX/GNRC/CMI (to 20-Nov-2026); https://api.nasdaq.com/api/quote/KEX/historical (20-Nov-2026 close)
- SEC frames: dei:EntityPublicFloat CY2024Q3I–CY2026Q2I; us-gaap EarningsPerShareDiluted/Basic CY2023Q1–CY2026Q3 (data.sec.gov)
