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
