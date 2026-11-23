# Sunflag Iron & Steel (NSE: SUNFLAG) — LIVE deep dive #1 (method test, protocol v1.3, stages 2→7)

**Date:** 2026-11-23 · **Analyst:** Claude · **Status:** live (not practice). Its paper calls are scored.
**Purpose:** to measure whether the deep-dive method has forecasting skill (`memory/strategy_review.md` §3 item 2b;
roadmap stages 2→7). The company was **drawn at random**. This is test material (L9, L21): **no buy/sell verdict**. The outputs are a decision card and
dated probabilistic calls, each scored later against a naive base rate.
**Roadmap:** builds stage 4 (deep dive), stage 5 (valuation) and stage 6 (decision), and feeds stage 7 (scoreboard). It unlocks the first
live Brier score for deep-dive probabilities vs base rates (`strategy_review.md` §4, question 2).
Research, not SEBI-registered advice.

Source tags: `[AR26]`/`[AR25]`/`[AR24]`/`[AR23]` annual reports (NSE annual_reports); `[Q2FY27]` results of 13-Nov-2026;
`[SCR]` screener.in consolidated page (fetched 23-Nov-2026); `[NSE]` NSE announcements/bhavcopy/SHP XBRL; `[CRISIL]` rating
letter 14-Nov-2025; `[YH]` Yahoo v8 daily closes; `[EST]` my estimate (the method is shown next to it). Money is in ₹ crore unless stated.

---

## 0. Selection (recorded verbatim, done first)

**Rule (from the task):** take `research_notes/Backtests/india_pead_live/universe.csv` (1,547 symbols); drop financials, banks,
NBFCs and insurers; keep ₹1,000–20,000 cr market cap; shuffle with Python `random.Random(20261123).shuffle`; walk the list. The **first** company that passes
the stage-2 hard filters becomes the subject.

**How it was run** (scripts in the scratchpad `live_dd1/scripts/sel1.py`, `sel2.py`):
1. **Market cap** = `shares` (universe.csv) × NSE close on **20-Nov-2026** (bhavcopy `sec_bhavdata_full_20112026.csv`, the
   latest published file; the 21-Nov and 23-Nov files were not yet available). Every one of the 1,547 symbols had a price. **810** were in ₹1,000–20,000 cr.
2. **Financials removed.** Two sources were used. (a) The NSE index files `ind_niftytotalmarket_list.csv` + `ind_niftymicrocap250_list.csv`, industry
   = "Financial Services": 29 names (AAVAS APTUS BAJAJHLDNG CAMS CANFINHOME CHOICEIN CREDITACC CSBBANK DCBBANK EDELWEISS
   EQUITASBNK FEDFINA HOMEFIRST IEX IFCI IIFLCAPS J&KBANK JMFINANCIL KFINTECH KTKBANK PAISALO RELIGARE SAMMAANCAP SBFC
   SHAREINDIA SOUTHBANK TMB UJJIVANSFB UTIAMC). (b) 484 in-range names had no index industry. Among them I classified 40 by hand as
   financial (lenders, brokers, rating agencies, investment holding companies): 5PAISA AFSL ARMANFIN BFINVEST CARERATING CONSOFINVT CREST DHANBANK
   ESAFSFB FUSION GEOJITFSL IBULLSLTD ICRA INDIASHLTR INDOSTAR JSWHL KICL MAHSCOOTER MASFIN MONARCH MUFIN MUTHOOTMF NSIL PFS
   PILANIINVS PNBGILTS PRIMESECU PRUDENT PSB REPCOHOME SATIN SMCGLOBAL SPANDANA SUMMITSEC SURYODAY TFCILTD TSFINV UGROCAP
   UTKARSHBNK VHL. This left **741 eligible names**. They were sorted alphabetically, then `random.Random(20261123).shuffle`d.
3. **Order drawn (first 10):** NRBBEARING, VSTIND, HINDWAREAP, **SUNFLAG**, QUESS, ASHAPURMIN, ROUTE, RAMCOIND, OAL, POKARNA.

**Walk log (every skip and why):**
| # | Symbol | Mcap ₹ cr | Result | Reason |
|---|---|---|---|---|
| 1 | NRBBEARING | 4,142 | **skip** | PEAD avoid window. Q2 FY27 SUE −0.09 ≤ cut-point −0.001 → **quintile 2** (event 04-Nov-2026, inside the 63-trading-day window that starts 20-Aug-2026). Computed with `live_tracker.sue_for` on `eps_history.csv` and the fixed `sue_cutpoints.json`. |
| 2 | VSTIND | 3,294 | **skip** | PEAD avoid window. Q2 FY26 EPS was missing from eps_history, so I added it from the NSE integrated XBRL (EPS 6.79, filed 29-Oct-2025) and bonus-adjusted the pre-Oct-2024 EPS for the 10:1 bonus (shares 1.544 → 16.986 cr). Q2 FY27 SUE **−1.30 → quintile 1** (event 28-Oct-2026). |
| 3 | HINDWAREAP | 1,308 | **skip** (judgment, see note) | Passed the mechanical hard filters: no promoter encumbrance (SHP 30-Sep-2026 XBRL), PEAD Q3 (SUE +0.06), solvency not red (S2 interest cover 1.17x and S3 fired, but India grade = S1 or S5 = blank). Same-day CEO/CFO/CS exits were explained as transfers to the subsidiary Hindware Ltd. **But** NCLT Kolkata sanctioned (14-Oct-2026, certified copy 06-Nov-2026) a composite scheme. Under it the consumer business is demerged into HHIL Ltd and the rest of the listed company is **amalgamated into Hindware Ltd, and HINDWAREAP is dissolved**. The scheme becomes effective on ROC filing, and the record date is pending. The subject cannot be scored through 2027-09-30, which is the whole purpose of the run. |
| 4 | **SUNFLAG** | 6,643 | **SUBJECT** | Passed every check (section 1): no promoter encumbrance, no qualified audit and no auditor exit (rotation after a 5-year term), PEAD **quintile 4** (Q2 FY27 SUE +1.04, event 13-Nov-2026), solvency screen 0 flags, no fraud-judgment flags found. |

**Deviation note (for the user/caller to accept or reverse).** Skipping HINDWAREAP adds a rule that was not in the task: *"the
listed entity must not be scheduled to cease to exist before the call horizon."* It is objective and it was decided before
SUNFLAG was looked at, but it is still a deviation. If it is rejected, the subject would be HINDWAREAP, and the calls would have to be written on
the successor shares.
**Tool note.** On 23-Nov-2026 `nse_fetch.py pledge` returned **0 rows for every symbol**. That includes INDOTECH, which had data on 21-Nov. So promoter
encumbrance was read from the latest **SHP XBRL** instead (`WhetherAnySharesHeldByPromotersAreEncumbered…` flags). The scoreboard's
`sources.py` already handles this transient empty answer.

---

## 0b. Rule zero: edge before depth
1. **What the market already knows.** Sunflag owns 6.00 cr shares of Lloyds Metals & Energy (LMEL, 10.66%), received in 2022 under an
   arbitral award. That stake is worth more than Sunflag's whole market cap. The price tracks LMEL (weekly corr 0.54, beta 0.73 over
   2 years `[YH]`). No earnings calls are held, so there are no "5 most-asked questions". Institutional ownership is ~1.1% (FII 0.70%, DII 0.37%
   `[SCR]` Sep-2026).
2. **The variable that would move value most if known better than consensus:** what the company will do with the LMEL stake
   (hold, use as collateral, sell to fund mining, or distribute). The discount the market applies to the stake depends on it. Second: the
   steel business's through-cycle margin. With ROIIC close to the cost of equity, growth hardly matters; margin does.
3. **The layers most likely to reveal it:** L5 (governance, capital allocation, collateral notes) and the mine-status tables (the only
   forward statements management makes). L4 matters for the steel margin.

---

## 1. S2 checklist (disqualifiers v3; filled before L1, every rule dated)
| Rule | Status | Evidence (source, date) |
|---|---|---|
| H1a fake cash | **pass** | Cash ₹322.8 cr + other bank ₹44.1 cr at 30-Sep-2026 `[Q2FY27]`. FY26 interest income ₹9.85 cr `[AR26 n.25b]` is consistent with a smaller FY26 balance (₹180 cr at Mar-2026). The dominant asset is a **listed** stake at an observable price. |
| H1b implausible economics | **pass** | 467,540 t rolled × ~₹84k/t ≈ ₹3,939 cr revenue `[AR26 §7]`. BRSR energy 2,302,310 GJ ÷ 4,032 MJ/t ≈ 571k t equivalent, which cross-foots with SMS 497.5k t + DRI 156k t. |
| H1c unverifiable profits | **pass** | No customer ≥10% `[AR26 n.35]`. B2B auto/forging/bearing channel. Listed SBQ peers exist. |
| H2 auditor exit / qualified opinion | **pass** | FY25 (B P & Co.) and FY26 (Lodha & Co LLP) opinions unmodified. The change came when the 5-year term completed at the Sep-2025 AGM `[AR25 AGM notice]`. CARO 3(xviii): "no resignation" `[AR26]`. Q2 FY27 limited review unmodified (13-Nov-2026). |
| H3 rating not cooperating | **pass** | CRISIL AA-/Stable & A1+ on ₹1,850 cr, letter 14-Nov-2025 (valid to 01-Jan-2027) `[CRISIL]`. CARE letter 26-Nov-2024 before that. |
| H4 pump pattern | **pass (watch)** | Main board, listed 1984. NSE surveillance queries 05-May-2026 (volume) and 29-Sep-2026 (price) were answered "market driven". The stock moved ₹194 → ₹456 → ₹369 (Mar → Sep → Nov 2026 `[YH]`), in line with LMEL. |
| H5 RPT leakage | **pass** | RPTs are tiny `[AR26 n.39]`: Daido royalty ₹2.36 cr; rent to Haryana Televisions ₹0.57 cr; wire-rod sales to the 49% JV Ramesh Sunwire ₹32.7 cr (0.8% of sales). LMEL is **not** a related party: the stake came from an arbitral award on past claims. |
| Exit triggers (auditor exit on denied info, late results) | **none** | Results filed on time (Q2 FY27 on 13-Nov-2026). |
| G pledge (v3: >25% red, >50% strong) | **clear** | SHP 30-Sep-2026 XBRL: promoter pledge/NDU/other encumbrance = false. Promoters 51.16%, unchanged since Mar-2021 `[SCR]`. |
| G accounting trouble (5 y) | **clear** | None found. Minor: SOP fine (Jun-2025) for a late secretarial compliance report after the PCS resigned on the due date `[NSE 21-Jul-2025]`. |
| G dilution | **clear** | 18,02,19,448 shares, unchanged since FY16 `[AR26 n.32]`. |
| G solvency set (S1/S5) | **clear** | `solvency_screen.py` 23-Nov-2026: 0 flags, ICR 5.2x. Net debt ₹26 cr at Sep-2026 (excluding ₹42.7 cr of leases). |
| Q CFO/PAT | ok | FY22–26 CFO ₹1,147 cr vs PAT ex the FY23 award ~₹940 cr = **1.22x** `[SCR]`. |
| Q CARO 3(ii)(b) stock statements | **question** | Bank stock statements differ from the books in both years. FY25: −₹109 to +₹168 cr ("provisional DP"). FY26: ₹19–31 cr. Shrinking. |
| Q other-income share | ok | FY26 other income ₹16.4 cr (5% of PBT). It includes the LMEL dividend of ₹6.0 cr. |

**Stage-3 signals.** PEAD: Q2 FY27 consolidated SUE **+1.04 → quintile 4** (Q1 FY27 +0.26 → Q3); not in the avoid zone.
Promise credibility: **the pipeline cannot run**. `tools/promise_tracker/pipeline/fetch.py SUNFLAG --since 2023-01-01` found 0 transcript PDFs
in 584 announcements, because the company holds no earnings calls. Section 5.4 has a substitute hand ledger.

---

## 2. Map (L1): what is the unit?
**Business.** Sunflag runs an integrated special/alloy steel (SBQ) plant at Warthi, Bhandara (Maharashtra). The route is DRI + mini blast furnace →
EAF/SMS (plus VIM for super alloys) → bar/rod mill. It sells bars, wire rods and blooms to auto/forging, bearing, engineering, railways,
oil & gas and defence customers `[AR26 BRSR]`. It runs a captive underground coal mine (Belgaon) and a captive power plant. It holds a 10%
strategic shareholder (**Daido Steel, Japan**), which also receives a royalty, and JVs: Daido DMS India (17.6%, tool steel), Ramesh Sunwire (49%,
alloy wire with 3S Applied Technologies), ReNew Green MPR Three (31.2%, 71 MW solar captive) and Sunsure Solarpark 37 (36%, 11 MW solar).
**The non-operating asset:** 6.00 cr LMEL shares (10.66%), carried at fair value through OCI. They were acquired in FY23 when Sunflag settled
past-period claims on LMEL through an arbitral award (22/28-Apr-2022), paid as 6 cr zero-coupon OFCDs that converted 1:1 `[AR23]`.

**Units (manufacturer row of the protocol):** (1) the **plant**: melt-shop tonnes × utilisation, from production disclosures; (2) the **product
node**: SBQ bars per tonne (realisation, carbon basket); (3) the **channel**: OEM/forger accounts. Customer concentration is low (no customer ≥10%). Add
(4) the **stake** as a separate unit: LMEL price × shares × (1 − tax) × (1 − discount).

**Production `[AR26 §7]` (tonnes):**
| | FY25 | FY26 | Δ |
|---|---|---|---|
| DRI (I+II) | 152,937 | 156,397 | +2.3% |
| Steel melting (SMS/VIM) | 479,429 | 497,506 | +3.8% |
| Rolled products | 449,117 | 467,540 | +4.1% |
| Mini blast furnace hot metal / pig iron | 402,530 | 471,652 | +17.2% |
| Belgaon coal | 117,820 | 103,860 | −11.9% |
| Captive power (lakh kWh) | 1,550 | 1,577 | +1.7% |

**Peers with comparable units:** Kalyani Steels (KSL; SBQ for forgings, also part of a holdco-discounted group), Vardhman Special Steels (VSSL),
Mukand (alloy bars), and Usha Martin (wire/rope, more downstream). P/Es on 23-Nov-2026 `[SCR]`: KSL 12.6, VSSL 39.0, USHAMART 25.4, MUKANDLTD 3.1
(one-off).

---

## 3. Reported financials, re-derived (L2)
**Ten-year shape `[SCR]` consolidated:**
| FY | Sales | OPM | Other inc. | PAT | EPS | CFO | FCF |
|---|---|---|---|---|---|---|---|
| FY17 | 1,456 | 10.0% | 8 | 65 | 3.62 | −18 | −48 |
| FY18 | 2,018 | 11.7% | 17 | 129 | 7.14 | 117 | 21 |
| FY19 | 2,186 | 10.8% | 11 | 110 | 6.12 | 177 | 46 |
| FY20 | 1,758 | 9.7% | 11 | 92 | 5.11 | 209 | 67 |
| FY21 | 1,892 | 13.4% | 11 | 141 | 7.80 | 223 | 170 |
| FY22 | 2,698 | 14.8% | 5 | 217 | 12.04 | 43 | −296 |
| FY23 | 3,488 | 12.8% | **1,201** | 1,115 | 61.89 | 278 | 109 |
| FY24 | 3,415 | 11.0% | 8 | 144 | 7.96 | 244 | 119 |
| FY25 | 3,536 | 11.0% | 17 | 162 | 8.99 | 192 | 104 |
| FY26 | 3,939 | 12.1% | 9 | 202 | 11.23 | 390 | 262 |
| TTM Sep-26 | 4,144 | 11.9% | 15 | 219 | 12.15 | — | — |

**Adjustments that matter:**
- **FY23 is a one-off.** ₹1,201 cr other income = the LMEL award gain. Core PAT ≈ ₹215 cr [EST: PBT 1,485 − 1,201 + ~5 normal OI, × 0.75], so core EPS is ~12.0.
- **FY26 PAT is understated by ~₹34 cr.** Exceptional item −₹8.7 cr, and ₹25.1 cr of deferred tax from earlier years (Q4 tax rate 58%) `[AR26 P&L]`. Normalised FY26 PAT ≈ ₹230 cr.
- **ROCE/ROE on screener (4%/2%) are meaningless.** The denominator holds the LMEL mark: investments ₹11,369 cr standalone / ₹11,359 cr consolidated at Sep-2026 `[Q2FY27]`, plus
  a **deferred tax liability of ₹1,639 cr**, which is mostly on the MTM. **Operating ROCE** ≈ EBIT 364 ÷ (FA 1,577 + CWIP 214 + NWC ~750 [EST]) ≈ **14% pre-tax,
  ~10.7% post-tax**. That is about the cost of equity.
- **Book value ₹672/share (P/B 0.55)** is ~85% LMEL mark net of DTL. It is not a measure of steel-business value.
- **Customer concentration:** no customer ≥10% in FY25 or FY26. Exports ₹114 cr (2.9%) vs ₹48 cr `[AR26 n.25a]`.
- **Other-income decomposition FY26 `[AR26 n.25b]`:** interest 9.85, LMEL dividend 6.00, insurance/other 0.5 → core PBT (ex OI) ≈ ₹283 cr.
- **H1 FY27 `[Q2FY27]`:** standalone revenue ₹2,201 cr (+10.3%), PBT ₹164 cr (+17%), PAT ₹112 cr. **CFO ₹339 cr is flattered by trade payables
  +₹191 cr** (good but misleading). Long-term debt repaid ₹79 cr; net debt fell from ~₹245 cr (Mar-26: borrowings ₹475 cr − cash/bank ₹230 cr) to **₹26 cr** (Sep-26).
- **Quarterly OPM `[SCR]`** (Sep-23 → Sep-26): 12,11,11,9,11,12,11,12,10,14,12,11,11%. H2 runs above H1 by 1.5–2.5 pp in FY25 and FY26.

---

## 4. Unit economics (L3) — per tonne of rolled product, FY26 `[AR26]`, ÷ 467,540 t
| Line | ₹ cr | ₹/t | % of sales |
|---|---|---|---|
| Revenue (net of ₹113 cr discounts) | 3,939 | 84,250 | 100% |
| Raw materials | 2,352 | 50,300 | 59.7% |
| Power (net of captive) | 270 | 5,770 | 6.9% |
| Contract expenses (outsourced labour/services) | 223 | 4,760 | 5.6% |
| Employees | 151 | 3,230 | 3.8% |
| Freight & forwarding | 121 | 2,600 | 3.1% |
| Fuel | 71 | 1,520 | 1.8% |
| Coal-mine costs (Belgaon) | 62 | 1,320 | 1.6% |
| **EBITDA** | **477** | **~10,200** | **12.1%** |

**Triangulation of volume (two routes):** (1) the company's production table, 467.5k t rolled. (2) BRSR energy ÷ intensity, ≈571k t "physical output",
which includes DRI/pig-iron sold. They differ by ~20% because the BRSR output definition is broader. That is fine for checking arithmetic, not definitions (technique #13).
**Capex per tonne:** FY26 investing outflow ₹122 cr vs D&A ₹113 cr, so the company is in maintenance mode. Rated capacity is not disclosed in AR26; a melt shop of ~0.5 Mt
at high utilisation is my [EST, unverified] reading of the production table. **Gap:** capacity and utilisation need the CTO/consent order
(Maharashtra PCB) as a second source.

---

## 5. Cost drivers in physical terms (L4), ranked by weight
**5.1 Materials basket FY26 vs FY25 `[AR26 n.26a]` (₹ cr):** iron ore 481 (507), coke 433 (581), ferro alloys 384 (376), **coking coal 376
(140)**, coal 130 (151), others 302 (326), fluxes 106 (100), scrap/HBI 81 (8), electrodes 33, super-alloy RM 26 (10).
- **Carbon basket (coke + coking coal + coal) = ₹939 cr = 23.8% of sales ≈ ₹18,900/t of liquid steel.** A 10% move in the price of the carbon basket = ±₹94 cr ≈ **±240 bps
  of OPM**. This is the top micro-driver. The FY26 mix shift from coke to coking coal (+₹236 cr coking coal, −₹148 cr coke) suggests own coke/PCI
  usage changed. That is a question for the plant visit.
- **Iron ore ₹481 cr ≈ 12.2% of sales.** Hot metal 471.7k t × ~1.6 t ore/t ≈ 0.75 Mt ore → ~₹6,400/t delivered [EST]. A 10% ore move = ±₹48 cr ≈ ±120 bps.
  LMEL's Surjagarh ore (Gadchiroli) is the nearest large source. Supplier names are not disclosed, so whether Sunflag buys from LMEL is unknown.
- **Ferro alloys ₹384 cr (9.7%)**: SBQ grades need Cr/Mn/Mo/Ni. Alloy prices are a leading series (alloy surcharges are passed through with a lag).
- **Pass-through.** SBQ prices to forgers/OEMs are reset quarterly or monthly (industry practice, [EST]), so OPM lags the carbon basket by ~1 quarter. Leading
  series: SGX/Platts coking coal, Indian met-coke prices (BigMint), Odisha/Chhattisgarh iron-ore lump (NMDC price notices are dated and public).

**5.2 Power: 6.9% of sales.** Purchased electricity = 137.75 m kWh renewable (3x FY25, from the ReNew JV) + 329.3 m kWh grid `[AR26 BRSR P6]`, total 467 m kWh, + 157.7 m kWh captive.
Cost per purchased kWh ≈ ₹270 cr ÷ 467 m ≈ **₹5.8/kWh**. Intensity ≈ 1,335 kWh per t rolled (all electricity). **Sensitivity:** ±₹0.50/kWh on
purchased power = ±₹23 cr ≈ ±60 bps. MSEDCL tariff orders (MERC) are the dated, leading document. The renewable share rose from 10% to 30% and
lowered the grid bill, which is one reason FY26 OPM beat FY25.

**5.3 People: not a micro-driver.** 1,318 permanent staff plus 2,702 contract workers; **1,716 contract workers (63.5%) are paid exactly the minimum wage** `[AR26
BRSR P5]`. Wage pool indexed to the notification ≈ 1,716 × ~₹15k/month × 12 × 1.29 load ≈ ₹40 cr [EST]. A 10% minimum-wage step ≈ ₹4 cr ≈ 10 bps.
The contract-expense line is ₹223 cr (+22% YoY) and is the bigger watch item. Median worker pay is ₹8.37 lakh; the MD earns 41x the median.

**5.4 Mining promises (the only forward statements; used as the credibility ledger)** `[AR24/AR25/AR26 board reports]`:
| Mine | FY24 AR said | FY25 AR said | FY26 AR said | Read |
|---|---|---|---|---|
| Lohardongri iron ore (LOI 13-Sep-2019) | FC pending; wildlife board | LOI-validity extension pending | PIL in Bombay HC (tiger corridor) | **reversed**; 7 years, no mine |
| Bhivkund coal (vesting 18-Sep-2021, 0.72 MTPA) | EC public hearing done 24-Apr-2024 | ML execution pending at Mantralaya | ML executed 21-Apr-2026; village NOC pending | one step/yr |
| Bajna iron ore (LOI 07-Nov-2022) | ToR minutes 02-May-2024 | FRA done; Stage-I FC pending at DFO | "EC and Stage I clearances are **likely … by end Sep-2026**" | **dated promise, open** |
| Surjagad-6 iron ore (LOI 05-Dec-2023) | prospecting scheme submitted | same text | CL executed 05-May-2025; drilling began 29-May-2026 | progressing |
| Belgaon coal (operating) | extractable balance **5.391 MT** | **5.391 MT** (unchanged after 117.8k t mined) | **3.5 MT** | disclosure inconsistency |
| New FY26 wins | — | — | Tambia South coal (commercial, MP) successful bidder 07/14-May-2026; Surajpura phosphorite LOI 13-Feb-2026 | expansion of scope |
Credibility read (n=5, not comparable with transcript scores): 0 of 5 reached production; dated timelines slip by years. This matches the base
rate for Indian captive/commercial blocks, where allocation to production often takes 4–7 years [EST, unverified]. **Capital-allocation question:** 10 mineral assets on a
₹4,000 cr steel business, plus a ₹10,000 cr listed stake that could fund them.

---

## 6. Governance, ownership, incentives, related parties (L5)
**Ownership (30-Sep-2026) `[SCR]`:** promoters 51.16%, unchanged since FY21. The promoter group includes the Bhardwaj family (Ravi Bhushan Bhardwaj, chairman; Pranav
Bhardwaj, MD; Suhrit Bhardwaj, NED), Supra Corporation, Sunflag Ltd and **Zedra Corporate/Directors (Jersey)**, an offshore trustee, from the SAST Reg 31(4) filings. **Daido
Steel ~10%** is a "deemed related party" and sits in the public category. FII 0.70%, DII 0.37%. 55,930 shareholders.
**Pledge:** no promoter encumbrance. **Company-level:** 74 lakh of the 600 lakh LMEL shares are pledged to Indian Bank as extra security for its
facilities `[AR26 n.15]`. The stake is used as collateral, not held aside for shareholders.
**RPT table `[AR26 n.39]` (₹ cr, FY26 / FY25), with share of the matching line:**
| Party | Item | FY26 | FY25 | Share of line |
|---|---|---|---|---|
| Daido Steel (10% holder) | Royalty + technical fees | 2.38 | 2.82 | 0.06% of sales |
| Haryana Televisions (common director) | Rent paid | 0.57 | 0.57 | 0.8 of ₹0.72 cr rent line |
| Ramesh Sunwire (49% JV) | Wire-rod sales | 32.7 | 24.8 | 0.8% of sales |
| Sunflag Foundation (WOS) | CSR | 4.63 | 5.06 | 100% of CSR |
| Khappa Coal (63% sub, block de-allocated 2014) | Loan outstanding | 7.37 | 7.37 | interest waived |
| KMP pay + directors' commission | MD ₹6.12 cr; chairman ₹1.11 cr; FY26 commission provided ₹8.22 cr (FY25 ₹4.16 cr) | | | 2.7% of PBT |
Total take by the promoter and the strategic holder ≈ ₹12–17 cr (≈0.3–0.4% of sales, 2.5–3.6% of EBITDA; the range depends on how the FY26 commission accrual is counted). It is small, but the directors' commission **doubled**.
**Board/KMP churn:** COO ceased Feb-2025; CEO (appointed Nov-2024) resigned Nov-2025; new CEO Dev Dyuti Sen joined Nov-2025; independent directors
Sajiv Dhawan (Aug-2025), Neelam Kothari (Sep-2025) and Anand Kapre (Sep-2026) left. The secretarial auditor resigned on the due date (Jun-2025).
**Other expenses note, items that moved:** commission on sales ₹3.35 → **₹16.52 cr (5x)**, alongside exports ₹48 → ₹114 cr. Legal &
professional ₹16.9 → ₹20.2 cr. Provision for doubtful debts ₹5.8 cr.
**Auditor's report + CARO, FY26 vs FY25 (L32 cue):** opinion unmodified both years. The key audit matter (KAM) changed from {revenue, litigation} to {revenue} after the auditor
rotation. The CARO stock-statement mismatch shrank (₹168 cr max → ₹31 cr max). No fraud reported, no whistle-blower complaints, no defaults. **Verdict: no
new adverse item.** Cue = neutral-to-improving.
**Dated watch items:** CRISIL letter validity 01-Jan-2027 (renewal); Bajna EC "by end Sep-2026"; MD term to Jan-2031.

---

## 7. Ground truth (L6): scuttlebutt plan (not executed; the user's ground checks)
| Visit | Count / ask | Model number it tests |
|---|---|---|
| A. Forging clusters (Pune-Chakan, Ludhiana, Rajkot): 2 forgers who buy Sunflag + a competitor (JSW/Jindal/Mahindra Sanyo/KSL) | Monthly bar price sheet for 3 fixed grades (EN8D, EN19/42CrMo4, 20MnCr5) ₹/t, price-reset dates, lead times, rejection rates | Realisation ₹84k/t; pass-through lag ~1 quarter; OPM path |
| B. Warthi/Bhandara plant gate (off-peak + peak) | Inbound coal/coke/ore trucks per hour, outbound bar trucks; contract-worker shifts; MSEDCL feeder notices | Volume +4%/yr; carbon basket mix (coke vs coking coal) |
| C. Bhivkund (Ballarpur) gram panchayat; MoEF **Parivesh** portal (Bajna, Bhivkund, Tambia South) | NOC status; EC/FC file numbers and dates (public, dated) | Mining calls 4; capex timing |
Ethics: identify yourself honestly if asked; no unpublished price-sensitive information; no recordings.

---

## 8. Flag override (L7) and valuation (L8)

### 8.1 Override table (bad-but-benign vs good-but-misleading)
| Flag | Kind | Verdict | What changes my mind |
|---|---|---|---|
| P/B 0.55; market cap < stake value | good-but-misleading | **OPEN**: cheapness is structural (holdco), not a mispricing | Board monetisation + distribution policy |
| Screener ROCE 4% / ROE 2% | bad-but-benign | adjusted: operating ROCE ~14% pre-tax | — |
| FY23 EPS ₹61.9 | good-but-misleading | adjusted: one-off award | — |
| FY26 Q4 tax 58% | bad-but-benign | adjusted: prior-year deferred tax | — |
| H1 FY27 CFO ₹339 cr | good-but-misleading | adjusted: payables +₹191 cr | FY27 CFO/EBITDA < 0.7 |
| Net debt ₹26 cr, AA- rating | good | confirmed (two sources: SoAL + CRISIL) | Borrowings > ₹1,000 cr (mining) |
| No earnings calls, ~1% institutions | bad-but-benign? | **OPEN** (information gap, possibly our edge) | First investor call |
| Mining programme (10 assets, slips) | bad | **OPEN** | One block producing on time, self-funded |
| Belgaon reserve stale then cut | bad | **OPEN** | Reconciliation in AR27 |
| Commission on sales 5x | unclear | **OPEN** | Counterparty disclosed; tied to exports |
| Directors' commission 2x | bad-but-small | watch | > 5% of PBT |
| LMEL shares pledged by the company (74 lakh) | unclear | watch | Count rises |
| CARO stock statements | bad-but-benign (common) | watch | > ₹50 cr again |
| KMP / ID churn | bad | watch | CFO exit or second CEO exit |
Open soft flags: 6, so a written variant view is required. It is below.

### 8.2 What the price implies (worksheet `tools/valuation/live/SUNFLAG_worksheet.md`; stub `SUNFLAG_stub_worksheet.md`)
**Inputs collected (protocol L8 step 1):** close ₹368.60 on 20-Nov-2026 (NSE bhavcopy = Yahoo); LMEL ₹1,723.80 (same two sources); 10 FY-end
P/Es (FY17–FY26: 10.2, 10.5, 7.9, 4.7, 8.0, 5.2, 12.3, 23.4, 26.1, 17.3; from FY23 on these include the stake, so they are not like-for-like); peers KSL 12.6 / VSSL 39.0 /
USHAMART 25.4 / MUKAND 3.1; **6-month ADV ₹13.5 cr** `[YH]`; net debt ₹26 cr; no pending dilution.
**Sum of the parts at 20-Nov-2026:** LMEL 6.00 cr × ₹1,723.80 = **₹10,343 cr pre-tax (156% of market cap)**. The tax on the ₹9,117 cr gain at 14.56% [EST: 12.5% LTCG ×
1.12 surcharge × 1.04 cess] is ₹1,327 cr. That leaves **₹9,016 cr post-tax = ₹500/share (136% of market cap)**. The company's own DTL of ₹1,639 cr (Sep-2026, at the higher
Sep mark) is consistent with this.
**Discount sensitivity (scenarios written before the outputs):**
| Discount on post-tax stake | Implied steel equity ₹ cr | EV/EBITDA FY26 | P/E on FY26 PAT | Steel "stub" ₹/share |
|---|---|---|---|---|
| 30% | 277 | 0.6x | 1.4x | 15 |
| 45% | 1,629 | 3.5x | 8.1x | 90 |
| **55% (worksheet assumption)** | **2,531** | **5.4x** | **12.5x** | **140** |
| 65% | 3,432 | 7.3x | 17.0x | 190 |
| 75% | 4,334 | 9.1x | 21.5x | 240 |
**Reverse DCF on the steel stub (CoE 12.5%, ROIIC 12%):** no growth rate solves the price. Because ROIIC ≈ CoE, growth adds almost no value. What the price needs is a
**NOPAT margin of 8.2% by year 10 vs 6.9% today** (≈ OPM 13–14% vs 12.1%). The base-case IRR is 11.7%. Turned round: **if the steel business is worth our
bear/base/bull DCF (₹93/₹123/₹170 per share), the market is applying a 45% / 52% / 61% discount to the post-tax stake.**
**Scenario outputs (main worksheet at the real price):** 5-year multiples bear 0.70x / base 1.54x / bull 2.22x. EV 1.38x (6.7%/yr) vs the 1.76x hurdle.
P(≥2x) 24%, P(≥3x) 6%, P(≤0.5x) 8%, P(blow-up) 2%. The DCF-consistent exit P/E for steel is 13–14x, against scenario exits of 9/12/16x. **The exit-multiple bet is
small here (L21).** The hidden bet is the **LMEL return** (`nonop_growth` −8% / +10% / +16%) and the **discount**, which is held constant.
**Temperature:** the trailing P/E of 32.8 reads "very hot" but means nothing here: the stake is outside EPS. On the stub the P/E is 12.5x, against the
pre-stake own band of ~8x (FY17–22 median) and KSL at 12.6x. So it is **warm vs its own steel history and normal vs the closest peer**.
**Discount history (Sunflag market cap ÷ pre-tax stake value) `[YH]`:** Sep-23 1.12, Mar-24 0.93, Sep-24 0.77, Mar-25 0.55, Sep-25 0.64,
Mar-26 0.46, Jun-26 0.56, Sep-26 0.73, **20-Nov-26 0.64**. The ratio has been falling as LMEL rose ~3.2x in 3 years, and it swings ±0.15 within 6 months.

### 8.3 Variant perception
- **What the market appears to price:** Sunflag as a discounted LMEL proxy. At our steel DCF the discount on the post-tax stake is ~52% (range 45–61%). That is within
  the 40–70% holdco range (`insight:group-holdco-discount`, unverified) and similar to KSL's group context.
- **Our view:** *no claimable mispricing.* The discount has reasons we verified: (1) no monetisation or payout policy (dividend ₹1/share, ~9% payout);
  (2) the stake already backs bank loans (74 lakh shares pledged); (3) management is widening into mining (10 assets plus a commercial coal block)
  with a weak delivery record, so stake proceeds could flow into low-return capex; (4) there is no investor communication. What the market may **underweight**: the
  steel business is now near debt-free, AA- rated and earns ~14% pre-tax ROCE. The bear case is therefore mostly an LMEL event, not a steel event.
- **What would prove us wrong:** (a) a board decision to sell LMEL shares **and** return the cash (buyback/special dividend). The gap would close, and
  call 5 (no sale) and the "persists" thesis would fail. (b) LMEL proceeds or new debt going into mining (discount widens, borrowings > ₹1,000 cr), which would break the
  "steel is safe" view (kill criterion 2). (c) FY27 OPM < 9%, which would break the margin view (calls 2 and 3).
- **Base-class departure (card §5):** our P(≥3x in 5y) of 6% vs the 44% class is deliberate (the class is a bull-market survivor sample; here a 3x needs LMEL
  to triple again). This is the cleanest test of whether a structural adjustment beats the naive class.

### 8.4 Decision card (`tools/decision/live/SUNFLAG_card.md`)
**Rule output: size 0**, blocked by *Expected value vs hurdle* (EV 1.38x vs 1.76x). Stage 2 passed (7 hard rules); PEAD clear; 6 open soft flags
with a written variant view (not blocking). Tier: speculative. Review **2027-02-15**. Kill criteria are dated (LMEL sale without distribution; borrowings >
₹1,000 cr; FY27 OPM < 9%; any encumbrance; audit/rating events). The card's own live 5-year calls: P(≥3x) 0.064 (base 0.444), P(≤0.5x) 0.082 (base 0.020),
P(blow-up) 0.02 (base n/a).

---

## 9. Forward calls (live; tags paper-call, deepdive-generated, live, india; specs in `tools/scoreboard/specs.json`)
| # | Call (YES if…) | Resolve by | Our P | Naive base | Base-rate reasoning |
|---|---|---|---|---|---|
| 1 | FY27 consolidated revenue from operations **≥ ₹4,300 cr** | 2027-05-31 | **0.63** | 0.42 | Own history: 5 of 12 FYs grew ≥9%. Ours: H1 +10.3%, needs H2 +8.0% on a soft Q3 FY26 base |
| 2 | FY27 consolidated OPM (resolver definition) **≥ 11.0%** | 2027-05-31 | **0.68** | 0.58 | Own history: 7 of 12 FYs ≥11.0%. Ours: H1 10.8% + the usual H2 lift of 1.5–2.5 pp |
| 3 | FY27 consolidated net profit **≥ ₹240 cr** | 2027-05-31 | **0.65** | 0.55 | Own history: 6 of 11 years with PAT growth ≥19%. Ours: H1 ₹125 cr; no repeat of the FY26 prior-year tax hit |
| 4 | **Bajna iron-ore block Environment Clearance granted** (Sunflag filing/AR or Parivesh) | 2027-09-30 | **0.35** | 0.50 | Naive: management said "likely by end Sep-2026", so a 1-year slack makes it a coin flip. Ours: 0 of 5 mine milestones on time |
| 5 | Sunflag's LMEL holding **falls below 6.00 cr shares** (any sale/transfer) | 2027-09-30 | **0.08** | 0.15 | Naive: rough annual rate of a stake event at Indian holdcos [EST, unverified]. Ours: collateral use, no stated intent |
| 6 | SUNFLAG total price return **beats Nifty 500** from 20-Nov-2026 (₹368.60; 24,088.80) to 30-Sep-2027 | 2027-09-30 | **0.46** | 0.44 | Naive: share of small caps beating the index over ~10 months (skew) [EST]. Ours: no edge on LMEL; the discount sits slightly below its 3-yr average |
Note on call 6: the task asked for a 12-month relative call resolving by 2027-09-30, so the window is 20-Nov-2026 → 30-Sep-2027 (~10.3 months).

---

## 10. What this run taught the method (curriculum)
1. **The selection step needs a scoreability filter.** A randomly drawn subject can be mid-scheme (HINDWAREAP). Proposal: add "no sanctioned
   scheme that dissolves the listed entity before the horizon" to the selection rule.
2. **The promise tracker assumes earnings calls.** About a quarter of Indian small caps hold none [EST]. The fallback used here was a hand ledger of annual-report "status"
   tables across 3 years, which turned up a stale reserve number (Belgaon). Proposal: add an `--ar-status` mode to the pipeline.
3. **Worksheet gap (fixed): holdco-like stocks.** The 5-year multiple ignored non-operating value. `worksheet.py` v1.2 adds
   `non_operating_growth` (plus scenario `nonop_growth`) and excludes the non-operating value from the DCF-consistent P/E. The 5 examples were regression-checked:
   identical except the version string and a new zero field.
4. **Stub analysis beats a trailing P/E** when a stake exceeds the market cap. Report the implied discount range, not one number.
5. **Tool note:** the NSE pledge API can return 0 rows for all symbols on a weekday. Read the SHP XBRL encumbrance flags instead.

## 11. Open items
Rated capacity/utilisation (MPCB consent order); supplier names for iron ore (LMEL?); the coke → coking-coal shift; who received the
commission on sales; LMEL fundamentals (not analysed; no edge claimed); KSL as a second holdco/SBQ comparison; CRISIL rationale text (not in
the letter).

## Sources
- AR FY2025-26: https://nsearchives.nseindia.in/annual_reports/AR_31025_SUNFLAG_2025_2026_A_4883414_01092026183814.pdf
- AR FY2024-25: https://nsearchives.nseindia.in/annual_reports/AR_28121_SUNFLAG_2024_2025_A_4649627_02092025130140.pdf
- AR FY2023-24: https://nsearchives.nseindia.in/annual_reports/AR_25512_SUNFLAG_2023_2024_03092024122853.pdf
- AR FY2022-23 (LMEL award): https://nsearchives.nseindia.in/annual_reports/AR_23013_SUNFLAG_2022_2023_28082023183137_08282023190018.zip
- Q2 FY27 results 13-Nov-2026: https://nsearchives.nseindia.in/corporate/SUNFLAG_13112026171507_SE_outcome_BM_13112026_.pdf
- CRISIL letter 14-Nov-2025: https://nsearchives.nseindia.in/corporate/SUNFLAG_15112025132241_SE_Reg_30_CRISIL_Rating_15112025.pdf
- Tambia South: https://nsearchives.nseindia.in/corporate/SUNFLAG_15052026151509_Regulation30-_Successful__Bidder_-Tambia_South.pdf
- NSE price/volume clarifications 06-May-2026, 30-Sep-2026; SOP board comment 21-Jul-2025 (NSE announcements)
- SHP XBRL 30-Sep-2026 (NSE corporate-share-holdings-master); NSE bhavcopy 20-Nov-2026; Yahoo v8 SUNFLAG.NS, LLOYDSME.NS, ^CRSLDX
- screener.in SUNFLAG, KSL, VSSL, USHAMART, MUKANDLTD (23-Nov-2026)
- HINDWAREAP NCLT order (selection log): https://nsearchives.nseindia.in/corporate/SHIL_16102026170015_SE_NCLTOrder_HHIL.pdf
