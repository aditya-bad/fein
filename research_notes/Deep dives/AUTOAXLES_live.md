# Automotive Axles (NSE: AUTOAXLES) — LIVE deep dive #3 (method test, protocol v1.3, stages 2→7; cheap-tercile draw)

**Date:** 2026-11-23 · **Analyst:** Claude · **Status:** live (not practice). Its paper calls are scored.
**Purpose:** to measure whether the deep-dive method has forecasting skill on a stock that is **cheap at entry** and inside the
base-rate size band (the "next useful card" named in L36). The company was **drawn at random from the cheapest EV/EBITDA tercile**.
This is test material (L9, L21): **no buy/sell verdict**. Outputs are a decision card (v1.2, tail-anchored) and dated probabilistic
calls, each scored later against a naive base rate. The deep dive must test *why* it is cheap (L10, L20, L36).
**Roadmap:** stage 2 (filters) → 3 (signals) → 4 (deep dive) → 5 (valuation) → 6 (decision) → 7 (scoreboard). It unlocks the first
live test of whether our probabilities beat base rates on a *statistically cheap* name, and the first "value-trap vs cyclical peak" test.
Research, not SEBI-registered advice.

Source tags: `[AR26]`/`[AR25]`/`[AR24]` annual reports (NSE annual_reports); `[Q2FY27]` results of 12-Nov-2026 (standalone; AAL has no
subsidiaries); `[T-Qn]` earnings-call transcripts (NSE, 11 calls May-2024 → Nov-2026); `[SCR]` screener.in page fetched 23-Nov-2026 (the
"consolidated" URL shows standalone figures because there are no subsidiaries); `[NSE]` NSE announcements / bhavcopy / SHP XBRL / pledge API;
`[ICRA]` rating letter 02-Feb-2026; `[YH]` Yahoo v8 daily closes; `[EST]` my estimate (method shown next to it). Money in ₹ crore unless stated.

---

## 0. Selection (recorded verbatim; rules fixed before drawing)

**Task rule:** universe = `research_notes/Backtests/india_pead_live/universe.csv`, non-financial, market cap ₹1,000–20,000 cr (inside base-rate
class `india_nonfin_1000_20000cr_5y`) at the latest NSE close; trailing EV/EBITDA and P/E from screener consolidated data for a random sample of
120 (`random.Random(20261125)`); keep the CHEAPEST tercile on EV/EBITDA (exclude negative EBITDA); shuffle the tercile with
`random.Random(20261126)`; the first company passing the stage-2 filters (v3) is the subject.

**Operational definitions** were written to `live_dd3/prereg_selection.md` (scratchpad) *before* the frame was built or any ratio seen:
1. Latest close = NSE bhavcopy `sec_bhavdata_full_23112026.csv` (23-Nov-2026 close, published by 18:00 IST). Mcap = universe shares × close.
2. Financials out = NSE index industry "Financial Services" (29) + the live-dd1 hand list (39 in range) + any new unclassified name judged
   financial (the two new no-industry names, APLLTD = Alembic Pharma and SUBEXLTD = Subex, are non-financial).
3. Eligible list sorted alphabetically → `random.Random(20261125).sample(eligible, 120)`.
4. Screener `/company/<SYM>/consolidated/` + the "Other Assets" schedule API. EBITDA_TTM = Σ last 4 quarterly "Operating Profit" (ex other
   income); PAT_TTM = Σ last 4 "Net Profit"; net debt = last Borrowings − last "Cash Equivalents"; EV = mcap + net debt. "Financing Profit"
   P&L format → financial, dropped.
5. Valid = EBITDA_TTM > 0; tercile = first ceil(n/3) by EV/EBITDA ascending.
6. Tercile sorted alphabetically → `random.Random(20261126).shuffle` → walk.
7. Stage-2 v3 checks in order: scoreability (entity exists through 2027-09-30), fraud-judgment flags, pledge ≤ 50% (NSE pledge API, SHP XBRL
   fallback), no qualified audit / auditor exit, not in the PEAD avoid window (63 trading days before 23-Nov-2026 → window starts 21-Aug-2026),
   solvency screen not red.

**How it ran** (scripts `live_dd3/scripts/frame.py`, `sample.py`, `fetch_scr.sh`, `rank.py`, `pead.py`, `s2check.sh`):
- 1,547 symbols, all priced; **809** in ₹1,000–20,000 cr; financials removed 29 (index) + 39 (hand) → **741 eligible**.
- Sample of 120 drawn (first ten: ADFFOODS JINDALPHOT OMAXE SEJALLTD HATHWAY ARVIND RENUKA MAXESTATES EVEREADY UFBL). All 120 pages and
  schedules fetched (HTTP 200); none had a financing-format P&L.
- 9 had EBITDA_TTM ≤ 0 (JINDALPHOT, OMAXE, BGRENERGY, RTNINDIA, ZOTA, NITCO, MMTC, VIPIND, ABREL) → **111 valid**; median EV/EBITDA 14.75x.
- **Cheapest tercile = 37 names, EV/EBITDA ≤ 11.86x** (tercile median 8.66x), from JSWDULUX 2.51x to TCI 11.86x.
- **Walk order (`Random(20261126)`):** JPPOWER, **AUTOAXLES**, GVPIL, GOODLUCK, TVSSCS, HCC, SESHAPAPER, JINDALSAW, JKTYRE, NRAIL, SANDHAR,
  BALMLAWRIE, NAVA, PANAMAPET, TIMETECHNO, NIITMTS, MOL, IFGLEXPOR, TCI, MSTCLTD, EPL, JSWDULUX, SOMANYCERA, HEIDELBERG, JAYNECOIND, CMSINFO,
  HATHWAY, UDS, UNIPARTS, GUJALKALI, STYRENIX, MONTECARLO, LINCOLN, GANDHAR, CIEINDIA, SKIPPER, STAR.

**Walk log:**
| # | Symbol | Mcap ₹ cr | EV/EBITDA (rule) | P/E TTM | Result | Reason |
|---|---|---|---|---|---|---|
| 1 | JPPOWER | 9,074 | 5.40 | 18.4 | **skip** | PEAD avoid window: Q2 FY27 SUE −0.70 → **quintile 1**, event 19-Oct-2026 (inside the window from 21-Aug-2026). `live_tracker.sue_for` on `eps_history.csv`, fixed `sue_cutpoints.json`. |
| 2 | **AUTOAXLES** | 2,684 | 8.66 | 13.5 | **SUBJECT** | Passed every check (section 1): entity continues (no scheme/delisting/open offer since the 2022 Cummins–Meritor open offer); no fraud flags in 774 announcements; promoter encumbrance 0 (NSE pledge API 23-Nov-2026 *and* SHP XBRL 30-Sep-2026); unmodified audit opinions FY25 and FY26, CARO 3(xviii) no resignation (the Jan-2024 "Change in Auditors" filing was an *internal* auditor appointment, read in full); PEAD Q2 FY27 SUE **+4.19 → quintile 5** (event 12-Nov-2026); solvency screen 0 flags, interest cover 110x. |

**Rule note (not a deviation, a disclosure):** the rule's EV uses screener "Cash Equivalents" (₹238 cr, which includes bank deposits) but not
"Investments" (₹170 cr of mutual funds). The true net cash is ₹394 cr, so AAL's EV/EBITDA is **8.1x**, not 8.66x. It stays in the tercile
either way. **Tool note:** the NSE pledge API answered normally on 23-Nov-2026 (it returned 0 rows for every symbol on the same date in live
dive #1), so pledge was read from both sources.

---

## 0b. Rule zero: edge before depth
1. **What the market already knows.** AAL is a 50/50 Kalyani (Bharat Forge's BF Investment) × Meritor (now Cummins) JV making
   medium/heavy commercial-vehicle (M&HCV) drive axles and brakes. The CV cycle is at a record (FY26 M&HCV industry ~480k, FY27 guided
   500k+ `[T-Q4FY26, T-Q2FY27]`), Q2 FY27 revenue +43% YoY and EPS +67%. The stock trades at 13.5x trailing P/E and 8.1x EV/EBITDA (net of
   cash) — the lowest P/E on the highest earnings in its 11-year history. The 5 most-asked call questions (Q2 FY27): capacity for H2, margin
   sustainability, exports, product/regulatory roadmap, steel cost pass-through.
2. **The variable that would move value most if known better than consensus:** *mid-cycle earnings power* — where FY27 sits in the cycle
   (pre-buy until April 2027, then "a watch") and whether the 4.5%-of-sales technical fee to Meritor HVS India (a Cummins company) stays
   flat at its annual renewal. Nobody on the last call asked about the fee or the 66% single-customer share.
3. **Layers most likely to reveal it:** L2 (cycle history, 10-year margins), L5 (parent-take table: the fee, the rejected related-party
   resolution, the annual services agreement), L4 (steel pass-through) and the promise ledger (are management's industry forecasts any use?).

---

## 1. S2 checklist (disqualifiers v3; filled before L1, every rule dated)
| Rule | Status | Evidence (source, date) |
|---|---|---|
| H1a fake cash | **pass** | Liquid assets ₹407 cr at 30-Sep-2026 (cash 30.8 + other bank 206.7 + MF investments 169.7) `[Q2FY27 SoAL]`. FY26 interest on bank deposits ₹19.5 cr + MF gains/fair value ₹7.5 cr `[AR26 n.22]` on an average ~₹330 cr balance ≈ 8% — consistent. ICRA AA-(Stable)/A1+ reaffirmed 02-Feb-2026. |
| H1b implausible economics | **pass** | Revenue/industry vehicle: FY26 ₹2,178 cr ÷ ~480k M&HCV = ₹45k per vehicle; FY19 ₹1,939 cr ÷ ~476k = ₹41k (industry volumes are management statements `[T-Q4FY26]`, single-source). Materials 67.5% of revenue with back-to-back steel pass-through — normal for a forging/machining axle maker. |
| H1c unverifiable profits | **pass** | Customers are listed OEMs (Customer A ₹1,440 cr = 66% of FY26 revenue `[AR26 n.32]`, almost certainly Ashok Leyland per call questions; Customer B ₹214 cr). Exports to group companies (Cameri, Troy) ₹62 cr. |
| H2 auditor exit / qualified opinion | **pass** | S R Batliboi & Associates LLP (EY), unmodified opinions FY25 and FY26; one KAM (slow-moving inventory provision) `[AR26 p.94]`. CARO 3(xviii) no resignation. Audit-trail exception for direct DB changes (common). Q2 FY27 limited review unmodified. |
| H3 rating not cooperating | **pass** | ICRA AA-(Stable)/A1+ on ₹135 cr, letter 02-Feb-2026 `[ICRA]`. |
| H4 pump pattern | **pass** | Main board since 1980s; 6-month ADV ₹2.4 cr mean / ₹1.0 cr median `[YH]` (illiquid, but no surveillance queries in 2025–26). |
| H5 RPT leakage | **pass (watch, see L5)** | Largest RPT is the **technical fee to Meritor HVS (India) Ltd (MHVSIL)** ₹97.5 cr FY26 (4.5% of sales) under an annual services agreement after minority shareholders **rejected** (79.5% against, Dec-2024) a ₹2,500 cr material-RPT resolution with MHVSIL `[AR25 CG report]`. Not leakage on present evidence (OPM rose 10.6% → 10.9% after the switch), but it is the single biggest parent take. |
| Exit triggers | **none** | Results on time; KSPCB notice disclosed 5 days late (09-Aug-2026, reason given). |
| G pledge (v3) | **clear** | NSE pledge API 23-Nov-2026: promoter shares pledged 0 (0.00% of promoter holding); SHP XBRL 30-Sep-2026: all three encumbrance flags false. Promoters 71.04%, unchanged since 2017 `[SCR]`. Cummins Reg 31(4) annual declaration 24-Jul-2026. |
| G accounting trouble (5 y) | **clear** | None. Minor: NSE format query on the Q4 FY21 audit report (resolved 27-May-2021). |
| G dilution | **clear** | 1,51,11,975 shares, unchanged. |
| G solvency set (S1/S5) | **clear** | `solvency_screen.py` 23-Nov-2026: grade blank, 0 flags, ICR 110.5x (FY26). Debt = lease liabilities ₹13 cr only. |
| Q CFO/PAT | ok | FY22–26 CFO ₹656 cr vs PAT ₹722 cr = **0.91x** `[SCR]`; FY25 receivables via MHVSIL ₹387 cr unwound in FY26. |
| Q other-income share | ok | FY26 other income ₹32 cr = 15% of PBT (treasury). |
| Q CARO 3(iii) loans | note | Loans to five **suppliers** (₹5.6 cr, secured on machinery they bought; one ₹0.03 cr overdue >365 days at AB Auto Brakes) `[AR26 n.37]`. Supplier financing to secure capacity — consistent with the "supply-chain constraint" story. |

**Stage-3 signals.** PEAD: Q2 FY27 SUE **+4.19 → quintile 5** (Q1 FY27 +2.02 → Q5); not in the avoid zone; survival cap n/a.
**Promise credibility (concall mode).** The company holds calls (11 transcripts May-2024 → Nov-2026 fetched), so the AR-mode tool was not
needed. I built a **hand ledger** (section 6.3) instead of running the LLM pipeline (time budget): **43% credit (n=7)** vs the auto-components
peer median **60%** (`AUTO_COMPONENTS_peer_comparison.md`: 64.8/83.3/60.0/50.0/26.1) → 17 pts below peers (counts as a soft flag).

---

## 2. Map (L1): what is the unit?
**Business.** AAL makes M&HCV drive axles (rear/front, single and tandem, 7–70 t GVW), brakes and gear sets at Mysuru (main), Rudrapur
and Jamshedpur (Hosur closed Feb-2025 `[NSE 04-Feb-2025]`). FY26 revenue split `[AR26 n.21.1]`: axles ₹1,209 cr (56%), brakes ₹531 cr (24%),
others (gear sets, carriers, housings, suspensions, scrap) ₹437 cr (20%); exports ₹219 cr (10%, mostly to Meritor plants in Italy and the US).
**Ownership.** 35.52% BF Investment (Kalyani / Bharat Forge) + 35.52% Meritor HVS LLC (Cummins since 2022) = 71.04%; DIIs 15.4%; FIIs 0.8%;
23,260 shareholders (down from 34,527 in Dec-2023) `[SCR]`.
**Sales model change (the key structural fact).** Until FY25, ~80% of sales went to OEMs *through* Meritor HVS (India) Ltd (MHVSIL, a Cummins
group company): ₹1,668.6 cr of FY25's ₹2,077.5 cr `[AR26 n.35]`. Minority shareholders rejected the ₹2,500 cr FY26 material-RPT resolution with
MHVSIL on 14-Dec-2024 (20.53% for, 79.47% against) `[AR25 CG report]`. From 1-Apr-2025 AAL sells direct to OEMs and pays MHVSIL a **technical
fee** (₹97.5 cr in FY26) for marketing, engineering, account and programme management under a services agreement dated 31-Mar-2025, extended
on 29-Apr-2026 to **30-Apr-2027** ("no impact") `[NSE 29-Apr-2026]`. AAL is "in the process of finalising direct agreements with OEMs" `[AR26 n.1]`.
**Units (manufacturer + MNC-subsidiary rows):** (1) the **plant**: revenue capacity ~₹2,700 cr on the existing base `[T-Q4FY26]` vs a Q2 FY27
run-rate of ₹2,650 cr, so ~98% used; phase-1 capex ₹120 cr adds 20–30% `[T-Q2FY27]`. (2) the **product node**: axle per vehicle (single → tandem →
tractor-trailer raises content per vehicle). (3) the **channel**: Customer A = 66% of revenue (almost certainly Ashok Leyland). (4) the **parent
relationship**: fee, exports to group plants, warranty claims routed via MHVSIL.
**Peers:** GNA Axles (axles, mostly tractor/export), Jamna Auto (CV springs), Wheels India (CV wheels); P/Es 15.6 / 20.8 / 29.7 `[SCR 23-Nov-2026]`.

## 3. Reported financials, re-derived (L2) — the cycle in ten years `[SCR, standalone; AR26]`
| FY | Revenue | OPM % | Core EBIT | PAT | EPS | NOPAT | Invested capital* | ROIC | FY-end P/E |
|---|---|---|---|---|---|---|---|---|---|
| FY17 | 1,172 | 9.7 | 75 | 49 | 32.7 | 50 | 341 | 14.5% | 21.6 |
| FY18 | 1,520 | 11.0 | 124 | 84 | 55.5 | 82 | 400 | 20.5% | 26.1 |
| **FY19 (peak)** | **1,939** | **11.8** | 183 | 122 | 80.4 | 121 | 571 | 21.2% | 16.0 |
| FY20 | 952 | 9.8 | 56 | 41 | 27.2 | 42 | 493 | 8.5% | 14.1 |
| **FY21 (trough)** | **906** | **7.3** | 30 | 23 | 15.0 | 23 | 498 | 4.5% | 70.3 |
| FY22 | 1,491 | 9.1 | 99 | 74 | 49.2 | 74 | 546 | 13.6% | 34.8 |
| FY23 | 2,324 | 11.1 | 216 | 162 | 107.2 | 162 | 741 | 21.9% | 22.1 |
| FY24 | 2,229 | 11.0 | 210 | 166 | 110.0 | 158 | 794 | 19.8% | 16.0 |
| FY25 | 2,078 | 10.6 | 186 | 156 | 102.9 | 140 | 882 | 15.8% | 15.7 |
| FY26 | 2,178 | 10.9 | 201 | 164 | 108.8 | 151 | 714 | 21.1% | 14.2 |
| **TTM Sep-26** | **2,406** | **11.8** | 246 | 208 adj | 137.6 adj | 185 | — | — | 12.9 |
*Equity + borrowings − cash − investments. NOPAT = core EBIT × (1 − tax). FY-end P/E = Yahoo close ÷ reported EPS.

**Re-derivations and adjustments.**
- **Other income** FY26 ₹32.2 cr `[AR26 n.22]` = deposits interest 19.5 + other interest 2.2 + MF gains/FV 7.5 + PPE gains 1.4 + misc 1.6 → 15% of PBT;
  core PBT = ₹188 cr. Screener nets the FY26 labour-code exceptional (₹11.99 cr) into Q3 "other income" (−3).
- **The FY26 revenue gross-up (good-but-misleading).** Materials (RM + inventory change) fell from **71.0%** of revenue (FY25) to **67.5%** (FY26) while
  other expenses rose from 11.7% to 14.3% (technical fee 1.07 → 97.5 cr). If physical material cost per unit was unchanged, revenue per unit rose
  ~5% (71.0/67.5 = 1.052) purely from selling at OEM prices instead of MHVSIL's transfer price `[EST]`. So FY26 "+4.8%" ≈ **flat like-for-like**,
  while M&HCV industry volume grew ~16% to ~480k `[T-Q4FY26; single-source, management]`. H1 FY26 was −3.6% reported (≈ −8% like-for-like), H2 FY26
  +12% reported (≈ +7%).
- **Revenue per industry vehicle** (₹ revenue ÷ M&HCV units): FY19 ₹40.7k; FY26 ₹45.4k reported, ~₹43.2k like-for-like (+6% in 7 years, ~0.9%/yr,
  below steel/price inflation) `[EST; industry volumes management-sourced]`. The "tonnage shift raises our content" story is not yet visible in the
  numbers.
- **Cash conversion.** CFO/EBITDA 41–129% (FY23–26); FY25 receivables ₹438 cr included ₹387 cr from MHVSIL, which unwound to ₹1 cr in FY26.
  H1 FY27 CFO ₹86 cr after an inventory build of ₹48 cr for the pre-buy `[Q2FY27 CF]`.
- **Customer concentration** `[AR26 n.32]`: Customer A ₹1,440 cr (66%), Customer B ₹214 cr (10%), MHVSIL ₹28 cr (FY26); in FY25 MHVSIL was 80%.

## 4. Unit economics (L3)
No unit volumes are disclosed (axles/brakes per year). Two routes on the incremental unit of capacity:
- **Top-down (management):** ₹120 cr capex for +20–30% capacity on a ~₹2,700 cr revenue base → ₹540–810 cr of revenue capacity, i.e. capex ÷
  revenue capacity 0.15–0.22 (asset turn 4.5–6.7x on new fixed capital) `[T-Q2FY27, T-Q4FY26]`.
- **Add working capital:** FY26 working-capital days 66 (≈18% of sales) `[SCR]` → capital per ₹100 of new revenue ≈ ₹33–40.
- **Return on that capital:** at a 10% core EBIT margin, pre-tax ROIIC = 25–30%, post-tax 19–23%. **Cross-check:** observed peak-to-peak FY19 → FY26
  ΔNOPAT ₹30 cr ÷ ΔIC ₹143 cr = 21%. The two routes agree, so the worksheet uses 18% base (15% bear, 22% bull).
- **Operating leverage:** OPM moved from 7.3% (FY21, revenue ₹906 cr) to 11.8% (FY19, ₹1,939 cr) and 12.5% (Q2 FY27 run-rate ₹2,650 cr). Roughly
  +1 pt of OPM per +₹400 cr of revenue in the up-leg; the down-leg is faster (FY20: revenue −51%, OPM −2 pts; FY21 a further −2.5 pts).

## 5. Cost drivers in physical terms (L4), ranked by weight (FY26, % of revenue ₹2,178 cr) `[AR26 n.23–29]`
| Line | ₹ cr | % rev | Physical driver | Sensitivity |
|---|---|---|---|---|
| Materials (RM + inventory change) | 1,471 | 67.5% | Forgings/castings/gears (steel), bought-out parts; Bharat Forge supplies ₹9.3 cr direct + ₹18.5 cr processing | "Back-to-back" pass-through with customers `[T-Q2FY27]`; lag ~1 quarter `[EST]`: a 10% steel move on ~70% steel content of materials ≈ 4.7% of revenue for one quarter ≈ **−120 bp of quarterly OPM** before repricing `[EST]` |
| Employee cost | 159 | 7.3% | Mysuru/Rudrapur/Jamshedpur workforce; labour codes added ₹12 cr one-off (gratuity) | +10% wage = −73 bp |
| **Technical fee to MHVSIL** | 97.5 | **4.5%** | % of OE sales (formula not disclosed); export sales to group excluded (Q1 FY26 call) | each +0.5 pt of fee rate on domestic OE sales ≈ −45 bp of OPM |
| Outside processing | 55 | 2.5% | Machining/heat-treat subcontract incl. Bharat Forge | capacity-linked |
| Stores & spares | 47 | 2.2% | Tooling consumption | — |
| Freight | 30 | 1.4% | Diesel-linked; "conversion cost increases on account of fuel" `[T-Q2FY27]` | +10% diesel ≈ −10 bp `[EST]` |
| Repairs (plant) | 27 | 1.3% | Machine age | — |
| Power & fuel | 22 | 1.0% | KSEB/HT tariff; solar captive via Torrent Saurya Urja 3 (₹8 cr) | +10% tariff ≈ −8 bp |
| Warranty | 11 | 0.5% | Routed via MHVSIL (₹10.8 cr) | — |
**Quarterly materials ratio (pass-through lag table):** H1 FY26 67.5%; H2 FY26 67.6%; Q1 FY27 64.6%; Q2 FY27 67.1%; H1 FY27 66.0% `[Q2FY27; AR26]`
(Q1 FY27 is flattered by a ₹51 cr build of finished goods/WIP, which moves cost into inventory; it reverses as stock is sold). Management flags "steel scarcity" and supply-chain constraints at gear suppliers (6–8 week lead
times) `[T-Q2FY27]` — the peak is supply-capped, which is itself a late-cycle signature.

## 6. Governance, ownership, incentives, related parties (L5; 15% share for a JV/MNC subsidiary)
### 6.1 Parent-take table `[AR26 n.35, n.29]` (₹ cr)
| Item | FY25 | FY26 | FY26 % of sales | FY26 % of core EBITDA (237) |
|---|---|---|---|---|
| Sales **to** MHVSIL (old channel) | 1,668.6 | 28.5 | — | — |
| Technical fee **to** MHVSIL | 10.7 | **97.5** | **4.48%** | **41%** |
| Warranty claims via MHVSIL | 8.4 | 10.8 | 0.50% | 5% |
| Rent to MHVSIL / Axletech | 1.7 | 0.6 | — | — |
| Purchases from group (BFL, Meritor Sweden, Cameri) | 25.7 | 20.1 | 0.9% | — |
| Services from Bharat Forge (incl. outside processing) | 18.4 | 18.5 | 0.85% | 8% |
| Exports **to** Meritor Cameri / Troy | — | 62.2 | 2.9% | — |
| Dividends to the two promoters | 34.4 | 32.7 | — | — |
| **Fee + warranty + BFL services** | — | **126.8** | **5.8%** | **54%** |
**Reading.** The fee replaced a margin that MHVSIL used to earn on resale (Q1 FY26 call: MHVSIL's gross margin on that business was "typically
10%"; an analyst calculated it implied 40–50% gross margin on its remaining aftermarket business — management "has not reviewed their financials").
OPM after the switch went *up* 0.3 pt, so the switch did not leak value on the evidence we have. But the fee is (a) **renewed annually** (next
30-Apr-2027), (b) ₹97.5 cr sits below the material-RPT approval threshold (lower of ₹1,000 cr or 10% of last audited turnover ≈ ₹208–218 cr), so shareholders do not vote on it, and
(c) its pricing formula is not disclosed ("arm's length"). **Dated watch items:** services agreement expiry 30-Apr-2027; FY27 AR note 29 fee line;
any new MRPT resolution. Also: the CCI order on Bharat Forge (commitments on access to AAL's business information) `[AR26 secretarial audit]`.
### 6.2 People and incentives
Chairman Dr B N Kalyani (attended 3/6 board meetings FY26). WTD & President Nagaraja Gargeshwari. CFO change: Ranganathan S left 21-Nov-2025;
Raman K CFO from 04-Feb-2026, announced as full-time CFO 12-Nov-2026. KMP pay ₹3.0 cr; independent-director commission ₹0.21 cr. Promoters have not
bought or sold since 2017. Minority holders showed they will vote (Dec-2024).
### 6.3 Promise ledger (concall mode; hand-built from 11 transcripts, May-2024 → Nov-2026)
| # | Said (call) | Promise | Outcome (source) | Credit |
|---|---|---|---|---|
| 1 | Q4 FY24 (28-May-2024) | "Early-teen margin 13–15%" once volume is at scale ("Absolutely") | Volume at scale FY26–27; company-defined EBITDA (incl. other income) 13.7% in H1 FY27, core OPM 12.1% `[T-Q2FY27; SCR]` | partly (0.5) |
| 2 | Q1 FY25 (07-Aug-2024) / Q4 FY25 (21-May-2025) | ~₹100 → ₹120 cr capex for line upgrades, "started by end of next year" | Started; Q3 FY26: complete by Q3 FY27; Q2 FY27: "a bit of delay", complete "by next quarter"; H1 FY27 capex ₹45 cr | late (0.5) |
| 3 | Q1 FY25 → Q3 FY25 | MIDV/low-floor bus axle: "Q4 this year" → "mid next year" → "end of Q1 next year" | Not launched at Q2 FY27 ("90–95% validated", deliberately slowed) | missed (0) |
| 4 | Q2–Q4 FY25 | FY26 M&HCV market "flat", "conservatively flat, 10% upside possible" | FY26 ~480k, +16% `[T-Q4FY26]` | missed (0) |
| 5 | Q2 FY26 (31-Oct-2025) | FY27 market "maybe 3–4% down" | H1 FY27 at record; FY27 guided 500k+ | missed (0) |
| 6 | Q1 FY26 (07-Aug-2025) | Direct-sales consolidation gives a "marginal" margin improvement | FY26 OPM 10.9% vs 10.6% | met (1) |
| 7 | Q1 FY25 | FY25 market "may remain flat" | FY25 ≈ flat (FY26 +16% on it) | met (1) |
| — | Q3 FY25 / Q4 FY25 / Q4 FY26 | Revenue "doubling by 2029–30" → "₹5,000 cr by 2030" → "₹4,000–5,000 cr" | Open (softened over time) | not scored |
| — | Q2 FY27 | Tandem axle "ramp-up by Q4 of this year" | Open (→ watch item) | not scored |
**Score: 3.0 / 7 = 43% credit** vs auto-components peer median 60%. **Pattern:** product and capex dates slip 1–4 quarters (sector-wide per the
peer study); industry forecasts were too **bearish** twice — so management guidance is not a useful cycle-timing signal in either direction.

## 7. Ground truth (L6): scuttlebutt plan (not executed; the user's ground checks)
1. **Vahan / SIAM monthly M&HCV registrations** (Jan–Jun 2027): the pre-buy shape and the post-April drop — the single most important number.
2. **Ashok Leyland dealer and fleet-owner checks:** whose axle is on the new tractor-trailers (AAL tandem vs in-house/other)? Wait times?
3. **Plant visit, Mysuru** (management said investors are welcome, `[T-Q2FY27]`): count shifts, new lines installed (phase 1), gear-shop queue.
4. **Gear/forging suppliers in Mysuru–Hosur belt** (e.g. the five suppliers AAL lent to, `[AR26 n.37]`): lead times, steel availability.
5. **Job portals** (AmbitionBox/Naukri) for AAL hiring on 3-shift operations vs layoffs — an early cycle signal.
Ethics: no unpublished price-sensitive information; identify ourselves if asked.

---

## 8. Flag override (L7) and valuation (L8)
### 8.1 Override table (bad-but-benign vs good-but-misleading)
| Flag | Type | Verdict | What changes my mind |
|---|---|---|---|
| P/E 12.9, EV/EBITDA 8.1x "cheap" | good-but-misleading | **OPEN**: peak-cycle cheap; 25.8x normalised | H1 FY28 revenue within 10% of H1 FY27 |
| FY26 revenue +4.8% | good-but-misleading | adjusted: ~flat like-for-like (gross-up) | — |
| Record margin 12.5% (Q2) | good-but-misleading | **OPEN**: operating leverage at capacity; FY20–21 shows the reverse | FY28 OPM ≥ 11% with lower revenue |
| Customer A 66% | bad | **OPEN** | Share < 55% with growth |
| Technical fee 4.5% of sales, annual renewal | bad (governance) | **OPEN** | Multi-year agreement, fee ≤ 4.6% |
| Content per vehicle lagging industry | bad | **OPEN** [EST] | FY27 growth ≥ industry + 5 pts |
| Net cash ₹394 cr, AA-, ICR 110x | good | confirmed (SoAL + screener + ICRA) | — |
| Minority vote against MRPT | good (governance works) / bad (conflict exists) | watch | — |
| Labour-code exceptional ₹12 cr | bad-but-benign | adjusted | — |
| KSPCB notices; late Reg-30 | bad-but-small | watch | Third notice / closure direction |
| CFO churn | bad-but-small | watch | Another CFO/WTD exit within 12 months |
Open soft flags: 5 (plus credibility −17 pts vs peers) → a written variant view is required (8.3).

### 8.2 What the price implies (worksheet `tools/valuation/live/AUTOAXLES_worksheet.md`)
**Inputs collected (L8 step 1):** close ₹1,776.30 on 23-Nov-2026 (NSE bhavcopy = Yahoo); 10 FY-end P/Es FY17–26 (21.6, 26.1, 16.0, 14.1, 70.3, 34.8,
22.1, 16.0, 15.7, 14.2; median 18.8 — cyclical: high at troughs); peers GNA 15.6 / JAMNAAUTO 20.8 / WHEELS 29.7; 6-month ADV ₹2.44 cr mean, ₹1.05 cr
median `[YH]`; net cash ₹393.9 cr; no pending dilution.
**Scenarios (written before the outputs; cycle position in FY31–32):** bear 35% (revenue ~flat over 5 years, NOPAT margin → 5.5%, ROIIC 15%, exit 14x);
base 45% (+5–6%/yr, 6.8%, 18%, 16x); bull 17% (+11% fading to 7%, 8.0%, 22%, 18x); blow-up 3% (0.3x: Customer A dual-sources in a downturn + fee step-up).
**Outputs:** 5-year multiples bear 1.04x / base 1.60x / bull 2.32x; **EV 1.49x raw, 1.40x anchored** vs hurdle 1.76x; P(≥2x) 24%, P(≥3x) 6%, P(≤0.5x) 4%
raw (8.2% anchored), P(blow-up) 3% raw (10.4% anchored). Base-case IRR **10.4%** vs CoE 12.5%. Probability-weighted DCF ₹1,316 (−26%).
**Exit-multiple bet:** DCF-consistent exit P/E 11.5–12.2 vs used 14/16/18 vs own median 18.8 → EV 1.13x / 1.49x / 1.73x. Even at the own-median exit the
EV (1.73x) sits just under the hurdle: **the binding choice is again the exit multiple** (L36), and for a cyclical the right exit multiple depends
on where FY31 sits in the cycle.
**Temperature:** trailing 12.9x = **COLD** (0th percentile of own history, 0.62x sector median); on 10-year normalised EPS ₹68.9 = 25.8x = **WARM**
(70th percentile). Reverse DCF at flat 7.7% NOPAT margin needs 12.6% revenue CAGR for 10 years — far above the 4.4% peak-to-peak EPS CAGR.

### 8.2b Value-trap test (why is it cheap?) — L10, L20, L36
| Question | Evidence | Answer |
|---|---|---|
| Is the "cheap" multiple on peak earnings? | TTM EPS ₹137.6 = record (FY19 peak ₹80, FY24 ₹110); OPM 12.5% in Q2 = record (prior peak 11.8%); FY26 M&HCV ~480k = FY19 peak 476k; FY27 guided 500k+; capacity ~98% used; steel and gear supply constrained | **Yes.** On 10-year normalised EPS the P/E is 25.8x. The last time the stock looked "cheap" at a peak (16x at FY19) it fell 80% in 18 months |
| Is a cycle turn dated? | Management: pre-buys "until April of next year" ahead of regulation changes; "beyond April up to September is a watch" `[T-Q2FY27]` | **A known, dated catalyst** inside our call window (Apr–Sep 2027) |
| Is the business deteriorating under the cycle? | Like-for-like FY26 revenue ~flat vs industry +16% (gross-up) `[EST]`; content per vehicle +0.9%/yr since FY19; 66% one customer | **Possibly** (single-source industry data; open flag) |
| Capital allocation history | Debt-free; net cash built to ₹394 cr (15% of mcap); payout ~30%; no buyback; capex ~₹70 cr/yr + ₹120 cr phase 1 at the top of the cycle; Hosur closed; supplier loans ₹5.6 cr | **Conservative, not value-destroying**; cash drag (treasury ~7.5%) and capex timing pro-cyclical |
| Who takes value before minorities? | Technical fee 4.5% of sales, annually renewed; total parent take ~5.8% of sales / 54% of core EBITDA (fee + warranty + BFL services) | **The main governance question**; minorities pushed back once (Dec-2024) |
| Fraud / solvency trap? | Clean audit, AA-, no pledge, ICR 110x | **No** |
**Conclusion:** cheap because the market is correctly discounting a cyclical peak and a parent take; **not a fraud or solvency trap; partly a
cyclical value trap**. The deep dive's job here was to say *which kind of cheap* — it found the cycle and the fee, not a hidden mispricing.

### 8.3 Variant perception
- **What the market appears to price:** peak earnings that will fall after the April-2027 pre-buy (P/E 12.9 on peak EPS, ~26x normalised).
- **Our view:** *no claimable mispricing; we agree with the market's direction.* We add two things it may under-weight: (1) the like-for-like
  revenue lag in FY26 (content/share per vehicle not growing) and (2) an annually renewable 4.5%-of-sales parent fee that minorities cannot vote on.
  Positive offset: net cash 15% of market cap and through-cycle ROIC ~15%, so the left tail is a cyclical drawdown (FY19–21 type), not ruin.
- **What would prove us wrong:** FY27 revenue ≥ ₹2,500 cr *and* H1 FY28 revenue within 10% of H1 FY27 (cycle longer than assumed); fee stable or
  lower on a multi-year agreement; FY27 revenue growth ≥ industry + 5 pts (content story real).
- **Base-class departure (card §5):** P(≥3x) 6% vs 21% class — a 3x from a peak-EPS base needs ~25% EPS CAGR at a 26x exit (twin engine); the
  peak-to-peak record is 4.4%. Tails anchored at w = 0.6 (above the 0.5 default) because this stock printed a ~0.20x drawdown in the last cycle.

### 8.4 Decision card (`tools/decision/live/AUTOAXLES_card.md`)
**Rule output: size 0**, blocked by *Expected value vs hurdle* (anchored EV 1.40x, raw 1.49x vs 1.76x). Stage 2 passed (7 hard rules); PEAD
quintile 5 (clear); survival cap n/a; 5 open soft flags with a written variant view (not blocking). Tier: satellite. Review **2027-02-15**.
Card calls (live, 5-year to 2031-11-23): P(≥3x) 0.056 (base 0.213); P(≤0.5x) 0.036 raw / 0.082 anchored (base 0.113); P(blow-up) 0.030 raw / 0.104
anchored (base 0.154).

---

## 9. Forward calls (live; tags paper-call, deepdive-generated, live, india, cheap-tercile; specs in `tools/scoreboard/specs.json`)
| # | Call (YES if…) | Resolve by | Our P | Naive base | Reasoning |
|---|---|---|---|---|---|
| 1 | Q3 FY27 revenue from operations **≥ ₹675 cr** (+20% YoY vs ₹562 cr) | 2027-02-28 | **0.55** | 0.15 | Naive: 2 of the last 13 quarters grew ≥20% YoY `[SCR]`. Ours: Q2 ₹663 cr; Q2→Q3 has averaged +7% (−7% to +22%); pre-buy momentum; capacity completing; steel/gear constraints |
| 2 | FY27 revenue from operations **≥ ₹2,500 cr** (+14.8%) | 2027-05-31 | **0.62** | 0.40 | Naive: 4 of 10 FYs (FY17–26) grew ≥14.8%. Ours: H1 ₹1,179 cr (+24%); needs H2 ≥ ₹1,321 cr (+7.7% vs H2 FY26 ₹1,226 cr; ≈ 2× the Q2 run-rate); pre-buy to April |
| 3 | FY27 OPM (resolver definition) **≥ 12.0%** | 2027-05-31 | **0.55** | 0.08 | Naive: 0 of 11 FYs ≥12.0% (max 11.8% FY19), Laplace ~0.08. Ours: H1 12.1% (Q1 11.6%, Q2 12.5%); H2 volume absorption vs commodity headwinds |
| 4 | FY27 net profit **≥ ₹220 cr** (+34%) | 2027-05-31 | **0.58** | 0.50 | Naive: 5 of 10 FYs with PAT growth ≥34%. Ours: H1 ₹105.7 cr; H2 needs ₹114.3 cr (Q2 run-rate ₹120 cr); no repeat of the ₹12 cr exceptional |
| 5 | FY27 technical fees to MHVSIL **≤ 4.75% of revenue from operations** (AR FY27 note "Other expenses" ÷ note "Revenue") | 2027-08-31 | **0.75** | 0.50 | Naive: a related-party fee at an annual renewal, coin flip [EST]. Ours: the 29-Apr-2026 extension said "no impact"; FY26 4.48%; falling export share (no fee on group exports) adds ~0.1 pt mechanically |
| 6 | AUTOAXLES price **beats Nifty 500** from 23-Nov-2026 (₹1,776.30; 23,748.15) to 30-Sep-2027 | 2027-09-30 | **0.40** | 0.44 | Naive: share of small caps beating the index over ~10 months (skew) [EST, as in live #1]. Ours: the window ends 5 months after the pre-buy; CV ancillaries usually de-rate into a volume turn; low starting P/E limits the damage |
Card calls (5-year, `decision-card-v1`, card v1.2) are in 8.4.
**Spec check (23-Nov-2026):** the four financial specs use `basis: standalone` (AAL files standalone only). The resolver's data path was probed on past periods with `sources.Live`: Q2 FY27 revenue screener ₹663.0 cr vs XBRL ₹662.6 cr, OPM 12.52% vs 12.47%, XBRL net profit ₹60.1 cr; FY26 OPM 10.88% vs 10.89% — two sources agree. `calls.build_rows` on the seed: 0 calls need a spec.

---

## 10. What this run taught the method (curriculum)
1. **"Cheap tercile" mostly selects cycle position.** The draw landed on a cyclical at a record peak; the valuation answer flipped from COLD
   (trailing) to WARM (normalised). Proposal: the worksheet should accept `eps_normalised` as a *second* reverse-DCF base and print both temperature
   rows (it already prints both temperatures; add the normalised reverse DCF).
2. **A sales-model change can fake growth.** The materials-ratio test (71.0% → 67.5%) exposed a ~5% revenue gross-up from routing sales directly to
   OEMs. Technique for the protocol: when a related-party channel is removed, re-derive like-for-like growth from the cost ratio before using growth.
3. **Minority votes are data.** A 79.5% "against" vote on a material RPT is a rare, hard governance signal; the company's response (restructure below
   the approval threshold, annual renewal) is the thing to track. Add to the L5 checklist: AGM/postal-ballot *results*, not just notices.
4. **Tail anchoring above default needs no note but deserves one** — used w = 0.6 with the stock's own last-cycle 0.20x drawdown as evidence.
5. **Tool notes:** the NSE pledge API worked on 23-Nov-2026 (empty in live #1 the same day earlier); screener's "consolidated" URL silently shows
   standalone data for a company without subsidiaries (quarters marked "(S)"); the selection-rule EV missed MF investments (disclose, don't change).

## 11. Open items
Unit volumes (axles/brakes per year; not disclosed — ask at the plant visit); the fee formula (% of what?); Customer A identity confirmation (AR does
not name it); SIAM monthly M&HCV data to replace management's industry numbers; the regulation behind the April-2027 pre-buy (management did not
name it); Ashok Leyland's own axle sourcing plans; BRSR physical-intensity cross-check (not done).

## Sources
- AR FY2025-26: https://nsearchives.nseindia.in/annual_reports/AR_29891_AUTOAXLES_2025_2026_A_16112201_18072026164730.pdf
- AR FY2024-25: https://nsearchives.nseindia.in/annual_reports/AR_27028_AUTOAXLES_2024_2025_A_18072025200747.pdf
- AR FY2023-24: https://nsearchives.nseindia.in/annual_reports/AR_24459_AUTOAXLES_2023_2024_12072024201545.pdf
- Q2 FY27 results 12-Nov-2026: https://nsearchives.nseindia.in/corporate/AUTOAXLES_12112026175115_BMOutcome12112026.pdf
- Q2 FY27 call transcript: https://nsearchives.nseindia.in/corporate/AUTOAXLES_17112026155524_CallTranscription_Q2_17112026.pdf (and 10 earlier calls, NSE "Analysts/Institutional Investor Meet" filings May-2024 → Aug-2026)
- Services agreement 31-Mar-2025 and amendment 29-Apr-2026: https://nsearchives.nseindia.in/corporate/AUTOAXLES_31032025180101_Service_Agreement_AAL_MHVSIL31032025.pdf ; https://nsearchives.nseindia.in/corporate/AUTOAXLES_29042026151440_ServiceAgreement_2026.pdf
- KSPCB notice 09-Aug-2026: https://nsearchives.nseindia.in/corporate/AUTOAXLES_09082026225408_Notice_KSPCB_09082026.pdf
- ICRA letter 02-Feb-2026: https://nsearchives.nseindia.in/corporate/AUTOAXLES_02022026155147_CreditRatingFeb2026.pdf
- Internal-auditor appointment 31-Jan-2024: https://nsearchives.nseindia.in/corporate/AUTOAXLES_31012024145359_OutcomeBM31012024.pdf
- NSE bhavcopy 23-Nov-2026; NSE pledge API and SHP XBRL 30-Sep-2026; Yahoo v8 AUTOAXLES.NS, ^CRSLDX
- screener.in AUTOAXLES, GNA, JAMNAAUTO, WHEELS, RKFORGE, BHARATFORG (23-Nov-2026); selection: 120 screener pages (scratchpad `live_dd3/dl/scr/`)
- JPPOWER skip: `research_notes/Backtests/india_pead_live/eps_history.csv` + `sue_cutpoints.json`
