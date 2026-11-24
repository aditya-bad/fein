# Indraprastha Medical Corporation (NSE: INDRAMEDCO) — LIVE deep dive #4 (method test, protocol v1.4, stages 2→7; first healthcare draw)

**Date:** 2026-11-24 · **Analyst:** Claude · **Status:** live (not practice). Its paper calls are scored.
**Purpose:** to test the deep-dive method on a sector type no live dive had covered (prior: steel holdco, US retailer-ish, auto
ancillary). The frame was pharma/healthcare + IT/software services; the company was **drawn at random**. This is test material
(L9, L21): **no buy/sell verdict**. Outputs are a decision card (**v1.3**, tail-anchored, general India survival cap; L39) and dated
probabilistic calls, each scored later against a naive base rate.
**Roadmap:** stage 2 (filters) → 3 (signals) → 4 (deep dive) → 5 (valuation) → 6 (decision) → 7 (scoreboard). It unlocks the first
live test of the method on a **single-asset services business whose key risk is legal/political rather than operating or cyclical**,
and a test of whether our tails can sit *above* the class base rate when the evidence says so.
Research, not SEBI-registered advice.

Source tags: `[AR26]`/`[AR25]`/`[AR24]` annual reports (NSE annual_reports; AR26 filed 01-Sep-2026); `[Q2FY27]` integrated-filing XBRL of
29-Oct-2026 (standalone; IMCL has no subsidiaries); `[NSE]` NSE announcements / bhavcopy / SHP XBRL / pledge API; `[SCR]` screener.in page
fetched 24-Nov-2026; `[YH]` Yahoo v8 daily closes (last bar 18-Nov-2026); `[PRESS]` news reports of Supreme Court hearings and Delhi-government
affidavits (ThePrint/PTI 12-Nov-2025, LiveLaw 25-Mar-2025, Medical Buyer Jan/Feb-2026 — single-source each, not court records); `[EST]` my
estimate (method shown). Money in ₹ crore unless stated. No concall transcripts exist on NSE.

---

## 0. Selection (recorded verbatim; rules fixed before drawing)

**Task rule:** universe = `research_notes/Backtests/india_pead_live/universe.csv`, India, market cap ₹1,000–20,000 cr at the latest NSE close;
restrict to pharma/healthcare OR IT/software services (NSE industry classification), non-financial; draw with `random.Random(20261201)` over the
alphabetically sorted eligible list; the first company passing the stage-2 filters (v3: pledge, solvency, governance) and scoreability is the subject.

**Operational rules** were written and timed to `live_dd4/prereg_selection.md` (scratchpad) at **2026-11-24 16:15 IST, before the frame was built**
(seen before writing: only the CSV headers and the count of index constituents per industry):
1. Latest close = NSE bhavcopy `sec_bhavdata_full_23112026.csv` (the 24-Nov file was not yet published). Mcap = universe shares × close.
2. Sector = NSE index "Industry" column (Nifty Total Market + Microcap 250 lists); keep "Healthcare" and "Information Technology". In-range names
   **without** an index industry were classified by hand and the list written into the prereg file **before the shuffle**; unsure → excluded.
3. Eligible list sorted alphabetically → `random.Random(20261201).shuffle` → walk.
4. Skip checks in order: (a) scoreability — entity not scheduled to cease to exist before 2027-11-30; (b) governance/fraud-judgment flags and
   qualified audit/auditor resignation; (c) promoter pledge ≤ 50%; (d) PEAD avoid window (quintile 1–2, event within 63 trading days before
   23-Nov-2026, i.e. from 21-Aug-2026); (e) solvency screen not red.

**How it ran** (scripts `live_dd4/scripts/frame.py`, `draw.py`, `s2check.sh`, `pead.py`):
- 1,547 symbols, all priced; **809** in ₹1,000–20,000 cr; **482** of them have no index industry (the index lists cover only ~1,000 names).
- Index-classified: Healthcare 26, IT 18. Hand-classified (pre-shuffle): Healthcare 40, IT 18; 10 unsure names excluded (ALEMBICLTD, TTKHLTCARE,
  AMRUTANJAN, CYIENTDLM, DLINKINDIA, KERNEX, MATRIMONY, NELCO, AURUM, RPSGVENT). **Eligible = 102.**
- **Walk order (first 15):** EXPLEOSOL, 63MOONS, **INDRAMEDCO**, SAKAR, SUPRIYA, ALIVUS, NEWGEN, BLUEJET, PANACEABIO, FDC, SOLARA, AARTIDRUGS, MPSLTD,
  RATEGAIN, JUBLPHARMA.

**Walk log:**
| # | Symbol | Mcap ₹ cr | Result | Reason |
|---|---|---|---|---|
| 1 | EXPLEOSOL | 1,196 | **skip (d)** | Passed a–c (NCLT scheme with Expleo was sanctioned in Feb-2023, nothing pending; no fraud flags in 875 announcements; promoter 71.05%, SHP XBRL 30-Sep-2026 encumbrance flags false). **PEAD Q2 FY27 SUE −0.32 → quintile 2, event 14-Nov-2026**, inside the avoid window. |
| 2 | 63MOONS | 4,205 | **skip (b)** | Governance/fraud-judgment flag: the NSEL payment-default legacy — on 23-Nov-2026 the company announced payouts to NSEL creditors under the NSEL scheme of arrangement, and the NSEL Investors Forum OTS correspondence continues `[NSE 01-Sep-2024, 23-Nov-2026]`. (It would also fail (d): Q2 FY27 SUE −0.01 → quintile 2, event 04-Nov-2026; solvency screen 1 flag, FY26 EBIT negative.) |
| 3 | **INDRAMEDCO** | 3,262 | **SUBJECT** | Passed a–e (section 1). Note on rule (a): the hospital-land lease has **expired** (section 2), but the *listed entity* is not scheduled to cease to exist — rule (a) is about entity dissolution, so the lease risk goes into the tails and calls, not the skip log. Disclosed here rather than changed. |

INDRAMEDCO entered the frame through the **hand list** (no index industry). Without the pre-registered hand list the frame would have been 44
names. Note also: 2 of the first 3 names were skipped, both by stage-2/3 rules — the defensive layer did its job before any depth was spent.

---

## 0b. Rule zero: edge before depth
1. **What the market already knows.** IMCL runs one hospital — Indraprastha Apollo, Sarita Vihar, New Delhi — as a 1988 JV of the Delhi
   government (GNCTD, 26%) and Apollo Hospitals (22.45%), managed by Apollo. FY26 revenue ₹1,482.5 cr (+9.3%), OPM 18.0%, PAT ₹183.6 cr, no debt,
   ₹556 cr liquid assets. The stock is at **17.0x trailing P/E** while listed hospital peers trade at **33–59x** `[SCR]`, and it fell from ₹622.8
   (06-Nov-2025) to ₹299.8 (23-Oct-2026) before ₹355.85 now `[YH, NSE]`. No concalls; nobody asks questions in public.
2. **The variable that would move value most:** **whether IMCL keeps the hospital, and on what free-treatment and rent terms.** The land is leased
   from GNCTD at Re 1/month; the lease expired on 31-Jul-2023 and GNCTD opposes renewal `[PRESS]`. Everything else (ARPP, margins) is second-order.
3. **Layers most likely to reveal it:** L5 (governance: the lease, the JV agreement, the government as co-promoter, vote results), L2 (what the
   ROIC is made of), L7 (how the company *discloses* the issue). Honest limit: we have **no edge on a Supreme Court outcome**.

---

## 1. S2 checklist (disqualifiers v3; filled before L1, every rule dated)
| Rule | Status | Evidence (source, date) |
|---|---|---|
| H1a fake cash | **pass** | Liquid assets ₹556.4 cr at 30-Sep-2026: cash 6.48 + other bank 196.85 + current investments 142.16 + non-current investments 210.90 `[Q2FY27 XBRL]`; screener Sep-2026 investments 142 + other assets 586 (second source, consistent). FY26 interest income ₹27.6 cr + MF gains 1.1 `[AR26 n.23]` on ~₹450 cr average ≈ 6.4% — consistent. |
| H1b implausible economics | **pass** | Company KPIs cross-foot exactly: 63,236 discharges × ALOS 3.23 = 204,252 bed-days × ₹69,714 revenue per bed-day = ₹1,424 cr vs **sale of services ₹1,424.95 cr** `[AR26 MD&A, n.22]`. OPM 18% inside the listed-hospital band. |
| H1c unverifiable profits | **pass** | Visible single hospital; 607,485 OPD visits; payers incl. TPAs (Family Health Plan sales ₹26.2 cr) `[AR26 n.30.L]`; debtor days 28 `[SCR]`. |
| H2 auditor exit / qualified opinion | **pass** | AR FY26 auditor's opinion unmodified; one KAM = the free-treatment litigation; CARO: no resignation; Q2 FY27 limited review filed. |
| H3 rating not cooperating | **pass** | Credit-rating filings 09-Apr-2024, 28-Apr-2025, 27-May-2026 `[NSE]`; no INC/withdrawal; no borrowings ("There are no Loans and Debt Securities" `[Q2FY27 XBRL]`). |
| H4 pump pattern | **pass** | Main board; routine NSE volume-spurt queries 16/19-Nov-2026; 6-month ADV ₹11.6 cr mean / ₹5.5 cr median `[YH]`. |
| H5 RPT leakage | **pass (soft flag, L5)** | Apollo-group purchases/services ~₹82 cr FY26 vs pharmacy commission + licence income from Apollo ₹40.3 cr `[AR26 n.30.L]`; see 6.1. |
| Exit triggers | **none** | Results on time; no restatement. |
| G pledge (v3) | **clear** | NSE pledge API 23-Nov-2026: promoter shares pledged 0 (0.00%); SHP XBRL 30-Sep-2026: all three encumbrance flags false. Promoters 51.00% for 12 quarters `[SCR]`. |
| G accounting trouble (5 y) | **clear** | None found in 517 announcements. |
| G dilution | **clear** | 9,16,73,000 shares unchanged. |
| G solvency set (S1/S5) | **clear** | `solvency_screen.py` 24-Nov-2026: grade blank, 0 flags. ICR FY26 = EBIT 252 / finance cost 6.0 = 42x (finance cost is lease interest 2.9 + bank charges 3.1). |
| Q CFO/PAT | ok | FY22–26 CFO ₹762 cr vs PAT ₹614 cr = **1.24x** `[SCR]`. |
| Q other-income share | ok | FY26 other income ₹28.75 cr = 11.7% of PBT, all treasury `[AR26 n.23]`; **core PBT ₹217.3 cr**. |

**Stage-3 signals.** PEAD: Q2 FY27 SUE **+1.27 → quintile 5** (event 29-Oct-2026); Q1 FY27 +1.07 → Q4. Not in the avoid zone; survival cap (v1.3)
clear (pledge 0, ICR 42x).
**Promise credibility — AR mode (no concalls).** `ar_run.py INDRAMEDCO --n 3` (FY24–26; the FY23 ZIP failed to download as a ZIP): 17 candidates,
3 scored, all generic ("MCS 1.0" is meaningless at n=3, L37). The asset × year table is noise for a one-hospital company (no capacity projects).
**Disclosure-quality flags (the useful read):**
1. **Material omission.** Neither AR FY26 (Directors' Report, MD&A, notes) nor the Q2 FY27 results notes say that the land lease expired on
   31-Jul-2023, that the JV agreement expired in 2018, or what GNCTD's 27-Jan-2026 affidavit says. The only disclosure is one paragraph in the
   03-Feb-2026 board outcome (filed 09-Feb-2026): the board "noted" an affidavit "in relation to the proceedings concerning the lease of land" and is
   "reviewing the contents". The FY26 contingent-liability note instead adds a new sentence: "The Company has remained compliant with the applicable
   requirements under the lease" `[AR26 n.30]` — while GNCTD alleges 7–10% EWS delivery against 33% IPD / 40% OPD `[PRESS]`.
2. **Boiler-plate carried forward.** The free-treatment paragraph (2009 Delhi HC order, SLP admitted 30-Nov-2009, interim order) is repeated
   almost verbatim every year; the "remained compliant" sentence is new in FY26.
3. **The Delhi government stopped participating.** AR26: "The Company is yet to get nomination from the Govt. of NCT of Delhi for appointment of
   3 Directors including Chairman". At the 24-Sep-2026 AGM promoter shares were 46,753,000 but promoter **votes polled were 21,442,500 (45.9%)** on
   every resolution — GNCTD's 23.8 m shares did not vote `[NSE Reg-44 results 25-Sep-2026]`.

---

## 2. Map (L1): what is the unit?
**Business.** One tertiary/quaternary hospital (Sarita Vihar, Mathura Road), ~700 beds `[EST: public descriptions; bed count NOT disclosed in AR24–26]`.
FY26: 63,236 discharges (−2%), ALOS 3.23 days (3.07), revenue per patient ₹2.25 lakh (+11%), 607k OPD visits (+2%), revenue per bed-day ₹69,714 (+6%)
`[AR26 MD&A]`. Occupied beds ≈ 204,252 ÷ 365 = **~560** `[EST]` → ~79% occupancy on ~700 beds `[EST, bed count unverified]`.
**Ownership and the PPP structure.** Founded 1988 "as a joint venture Company between the Govt. of NCT of Delhi and Apollo Hospitals Group … first
of its kind … public-private partnership" `[AR26 MD&A]`. Promoters 51.00% = GNCTD 26.00% + Apollo Hospitals Enterprise 22.45% + Reddy family/others
`[SHP XBRL 30-Sep-2026]`. Public 44.8% across 77,706 holders (up from 51,448 in Dec-2023); FIIs 2.4%, DIIs 1.8% `[SCR]`.
**The land (the key structural fact).** "The Hospital building has been constructed on the land leased out to the Company by the Government of
NCT of Delhi. The Government … has met the expenditure to the extent of ₹15.48 Crore … for construction of building … The ownership of the building
between Government of NCT of Delhi and the Company will be decided at a future date"; ground rent **₹12 per year** `[AR26 n.30.D]`. Net book value of
the building ₹127.2 cr. In return the lease requires free treatment for the poor (GNCTD: **one-third of IPD and 40% of OPD**) `[PRESS]`.
**Holdco/non-operating flag (v1.4):** net cash ₹521 cr = **16% of market cap** — below the 20% stub rule of thumb, but in a handover scenario it is
most of what is left.
**Cyclicality flag:** none (COVID FY21 was the only down year). The stock does screen cheap vs peers, so the "why cheap" test is in 8.2b.
**Peers:** Artemis Medicare (one Gurugram flagship; 44.3x), Shalby (33.3x), Yatharth (54.9x), Jupiter Life Line (51.3x), Narayana (44.6x),
Apollo Hospitals (58.8x) `[SCR 24-Nov-2026]`; median **48.0x**.

### 2.1 The lease/JV timeline (the variable)
| Date | Event | Source |
|---|---|---|
| 16-Mar-1988 | IMCL incorporated (GNCTD–Apollo JV); land leased at Re 1/month with free-treatment conditions | `[AR26]`, `[PRESS]` |
| 22-Sep-2009 | Delhi HC (PIL): free treatment must include medicines and consumables | `[AR26]` |
| 30-Nov-2009 | SC admits IMCL's SLP; interim order lets IMCL charge for medicines for GNCTD-referred patients | `[AR26]` |
| 10-Mar-2018 | JV agreement with Apollo expires (per GNCTD) | `[PRESS]` |
| 31-Jul-2023 | **Land lease expires; not renewed** (per GNCTD) | `[PRESS]` |
| 25-Mar-2025 | SC bench (Surya Kant J) warns it could hand the hospital to AIIMS if the poor are not treated free; orders a joint inspection | `[PRESS: LiveLaw]` |
| 09-May-2025 | IMCL proposes a 30-year renewal to GNCTD | `[PRESS]` |
| Nov-2025 | GNCTD report to SC: EWS share 9–10% of OPD and 7–9% of IPD over 5 years | `[PRESS: ThePrint/PTI 12-Nov-2025]` |
| 27-Jan-2026 | **GNCTD affidavit: renewal "contrary to public interest and contractual discipline"**; Centre advised against renewal | `[PRESS]` |
| 03/09-Feb-2026 | IMCL board "noted" the affidavit; no details | `[NSE]` |
| 19-Mar-2026 | Hearing listed — **outcome not found** (no IMCL filing since; searches found nothing) | `[PRESS]` |
| 24-Sep-2026 | GNCTD does not vote its 26% at the AGM | `[NSE]` |
| 04-Nov-2026 | MD's 2-year term ends; no successor announced | `[NSE 05-Nov-2026]` |
IMCL's own position `[AR26 Directors' Report]`: it has asked the SC (interlocutory application) and GNCTD to apply the norm used for other Delhi
hospitals on concessional land — **10% IPD and 25% OPD free, including medicines and consumables**.

---

## 3. Reported financials, re-derived (L2) `[SCR standalone; AR26]`
| FY | Revenue | OPM % | EBITDA | Core EBIT | PAT | EPS | FY-end close | FY-end P/E |
|---|---|---|---|---|---|---|---|---|
| FY17 | 766 | 10.3 | 79 | 48 | 26 | 2.86 | 53.15 | 18.6 |
| FY18 | 753 | 9.8 | 74 | 43 | 21 | 2.30 | 48.50 | 21.1 |
| FY19 | 788 | 10.4 | 82 | 52 | 28 | 3.10 | 38.55 | 12.4 |
| FY20 | 831 | 10.5 | 87 | 54 | 44 | 4.76 | 33.90 | 7.1 |
| FY21 | 613 | 6.7 | 41 | 8 | 2 | 0.25 | 53.70 | 214.8 |
| FY22 | 888 | 13.5 | 120 | 85 | 59 | 6.39 | 58.40 | 9.1 |
| FY23 | 1,099 | 13.8 | 152 | 113 | 86 | 9.40 | 77.05 | 8.2 |
| FY24 | 1,245 | 15.7 | 195 | 155 | 124 | 13.52 | 171.35 | 12.7 |
| FY25 | 1,356 | 18.1 | 245 | 201 | 161 | 17.56 | 386.10 | 22.0 |
| FY26 | 1,483 | 18.0 | 267 | 223 | 184 | 20.03 | 372.35 | 18.6 |
| **TTM Sep-26** | **1,556** | **18.0** | **280** | **233** | **192** | **20.95** | 355.85 | **17.0** |
FY-end close `[YH]` ÷ reported EPS `[SCR]`. FY26 re-derived from the AR P&L: 1,482.51 − materials 256.34 − employees 287.60 − other expenses 671.65 =
**EBITDA 266.92** (screener 267 ✓); Q2 FY27 revenue 412.85 / PAT 53.58 / EPS 5.84 in XBRL = screener ✓.

**Re-derivations and adjustments.**
- **Margin step-up.** OPM went 10% (FY17–20) → 18% (FY25–26) as revenue per patient rose; discharges are now *falling* (−2% in FY26), so growth is
  price/mix and case-mix, on a fixed site. The stock re-rated from 8x (FY23) to 22x (FY25) during the step-up, then de-rated to 17x as the lease issue
  surfaced (price −43% from the Nov-2025 high).
- **ROIC is largely a land subsidy.** Invested capital ex cash FY26 ≈ equity 740 + lease liabilities 35 − liquid assets ~467 = **~₹310 cr** `[EST]`; NOPAT
  223 × 0.75 = 167 → **ROIC ~54%**. Peers that own or rent land in Delhi-NCR run at 13–17% ROCE `[SCR]`. The difference is (a) land at ₹12/yr, (b) a
  building partly government-funded and fully depreciated in part, (c) a 37-year-old asset base. **"Looks-good" flag**: the return is a concession whose
  price (free treatment) has been under-paid by GNCTD's account, and whose term has run out.
- **Other income** ₹28.75 cr FY26 = interest 27.61 + MF gains 1.14 (11.7% of PBT). Core PBT ₹217.3 cr.
- **Cash conversion** strong (CFO/PAT 1.24x FY22–26; negative working capital in most years).
- **Customer concentration:** none disclosed (Ind AS 108: single segment; no ≥10% customer).
- **Normalised EPS (v1.4 rule, because it screens cheap):** 10-year mean EPS FY17–26 ₹8.02 → 44x — but this is *not* a cyclical; EPS grew
  structurally. The cheapness is relative to peers (0.35x the sector median), and its cause is legal, not cyclical (8.2b).

## 4. Unit economics (L3) — the bed and the patient
| Item (FY26) | Value | Route |
|---|---|---|
| Occupied beds | ~560 | 63,236 × 3.23 ÷ 365 `[AR26]` |
| Revenue per occupied bed-day | ₹69,714 | company `[AR26]`; cross-foot to sale of services ✓ |
| Revenue per occupied bed per year | ₹2.55 cr | ₹1,425 cr ÷ 560 |
| EBITDA per occupied bed per year | ₹0.48 cr | ₹267 cr ÷ 560 |
| Revenue per patient (IPD-weighted) | ₹2.25 lakh | company |
| Doctors' professional fees per bed-day | ~₹19,000 | ₹389 cr ÷ 204k bed-days |
**The free-bed arithmetic (what the dispute is worth).** One-third of ~700 beds = ~233 beds. At ₹2.55 cr revenue per occupied bed, enforcing a full
one-third free IPD quota *on top of* today's ~7–9% would remove ~25% of paying IPD capacity: **~₹350 cr revenue** and, at a ~50% contribution margin
(doctor fees, consumables and part of staff are variable), **~₹170 cr of EBITDA (~60%)** `[EST]`. IMCL's own ask (10% IPD incl. medicines) would cost
roughly 10% of IPD consumables (~₹25 cr) plus forgone medicine charges on referred patients — **~₹25–50 cr EBITDA (10–18%)** `[EST]`. A market lease
rent for the site is unknown `[open item]`.
**Payback on new capacity:** not applicable — no expansion capex (CWIP ₹2.8 cr; capex ₹30–60 cr/yr is equipment replacement and upgrades).

## 5. Cost drivers in physical terms (L4), ranked by weight (FY26, % of revenue ₹1,482.5 cr) `[AR26 n.24, n.27]`
| Line | ₹ cr | % rev | Physical driver | Sensitivity |
|---|---|---|---|---|
| **Professional charges to doctors** | 389.4 | **26.3%** | Consultants on fee-for-service (not on payroll); ~₹19k per bed-day | Fee share +1 pt of revenue = −100 bp OPM; senior-consultant exits move revenue, not just cost |
| Employee cost | 287.6 | 19.4% | 3,000 permanent employees `[AR26 BRSR]` → ₹9.6 lakh average CTC; plus 1,172 contract workers (in outsourcing) | +10% wage = −194 bp; Delhi minimum-wage revisions (Apr/Oct) hit the contract pool |
| Materials (consumables, drugs used) | 256.3 | 17.3% | Implants, consumables; Apollo pharmacy supplies ₹16.7 cr; **free-treatment rulings act here** (medicines for EWS patients) | Each 1% of IPD treated free incl. medicines ≈ −₹2.5 cr `[EST]` |
| **Advertisement, publicity & marketing** | 105.4 | **7.1%** | +23% YoY; composition not disclosed (international-patient facilitators/agents?) | High for a single hospital — open question |
| Outsourcing | 53.4 | 3.6% | Housekeeping/food via Sindoori and Apollo Sindoori (₹35.2 cr, related) + others | — |
| Power & fuel | 24.7 | 1.7% | Delhi commercial tariff; fell 9% (efficiency projects) | +10% tariff = −17 bp |
| Repairs | 21.5 | 1.5% | 37-year-old building, equipment | Rising with age |
| Rates, taxes | 18.5 | 1.2% | — | — |
| Legal & professional | 12.7 | 0.9% | **+35% YoY** — consistent with heavier litigation | — |
| Land rent | ₹12 (rupees) | 0.0% | Lease at Re 1/month `[AR26 n.30.D]` | The line that could change most |
No materials-ratio lag table: hospitals price per procedure/package; materials 17.0% (FY25) → 17.3% (FY26) `[AR26]`.

## 6. Governance, ownership, incentives, related parties (L5; 15% share — group company with two promoters)
### 6.1 Parent-take table (Apollo group) `[AR26 n.30.L]` (₹ cr)
| Item | Direction | FY25 | FY26 | FY26 % of revenue | % of EBITDA (267) |
|---|---|---|---|---|---|
| Pharmacy consumables from AHEL | paid | 16.05 | 16.66 | 1.1% | 6% |
| Reimbursement of expenses to AHEL | paid | 19.14 | 19.18 | 1.3% | 7% |
| Licence fees (AHEL) | received (rev. note "licence fee and commission") | 1.44 | 1.59 | — | — |
| **Commission on pharmacy sales (AHEL)** | **received** | 30.09 | **38.74** | 2.6% | 15% |
| Sindoori Management Solutions (services) | paid | 10.05 | 10.32 | 0.7% | 4% |
| Apollo Sindoori Hotels (food/housekeeping) | paid | 23.48 | 24.92 | 1.7% | 9% |
| Vitamed Logistics (consumables) | paid | 4.63 | 10.43 | 0.7% | 4% |
| Apollo Healthco / Radiology / AHLL | paid | 1.22 | 1.02 | — | — |
| Family Health Plan (TPA) | sale of services | 22.20 | 26.15 | — | — |
| Dividend to AHEL | paid | 9.09 | 9.09 | — | — |
| **Total paid to Apollo group (ex dividend)** | | 74.6 | **82.5** | **5.6%** | **31%** |
**Reading.** Direction is not labelled in the note; I inferred it from the revenue note (licence fee and commission income ₹44.61 cr ≈ 38.74 +
1.59 + others). **Apollo appears to run the in-hospital pharmacy and pay IMCL a commission** (₹38.7 cr, +29%); the pharmacy margin itself stays with
Apollo, and the commission rate and term are **not disclosed**. If the commission is 10–15% of pharmacy sales, Apollo sells ~₹260–390 cr a year
inside IMCL's hospital `[EST, unverified]`. No royalty/brand fee is shown (management is Apollo's, KMP are IMCL employees: MD ₹2.95 cr, CFO ₹1.72 cr).
No transaction is above the material-RPT threshold, so there has been **no RPT vote**.
### 6.2 Vote results (Reg-44)
| Meeting | Resolutions | Result | Note |
|---|---|---|---|
| AGM 24-Sep-2026 | 5 ordinary (accounts, dividend ₹4, two director re-appointments, auditors) | all passed | **Promoter votes polled 21.44 m of 46.75 m** (GNCTD did not vote); institutions 6.2% against re-appointment of Dr Suneeta Reddy; public non-institutions polled 0.39% |
| Postal ballot 20-Mar-2026 | 4 special (3 ID re-appointments, 1 new ID) | all passed | Numbers in the scrutinizer PDF not extracted (scanned) |
### 6.3 People and incentives
MD Shivakumar Pattabhiraman's term ended 04-Nov-2026 (re-appointed for only two years in 2024); **no successor announced**. CFO C P Tyagi. Board chair
vacant (GNCTD nominee). Four independent directors appointed/re-appointed in Feb–Mar 2026. No ESOPs. Promoters have not traded.
**Who gets paid before minorities?** Apollo, through operating control and the pharmacy economics; the government, through the free-treatment duty
(which it says is under-delivered). The minority's claim depends on both partners agreeing to continue a JV whose agreement expired in 2018.

## 7. Ground truth (L6): scuttlebutt plan (not executed; the user's ground checks)
1. **Supreme Court case status** (SLP(C) 29482/2009; diary 33939/2009): order dates and text since March 2026 — the single most important number.
2. **Delhi DHS EWS portal / nodal officer**: free beds displayed at the hospital (all hospitals must display bed availability); count EWS beds occupied.
3. **Site visit, Sarita Vihar**: OPD queue counts, EWS counter, pharmacy (who operates it, how billed), signage of the "free bed" board.
4. **Delhi land and health departments**: any notice inviting operators for the site, valuation of the building, AIIMS proposals.
5. **Apollo Hospitals' own disclosures** (AR, investor deck): how it describes IMCL and its Delhi-NCR expansion (does it plan around losing Sarita Vihar?).
Ethics: no unpublished price-sensitive information; identify ourselves if asked.

---

## 8. Flag override (L7) and valuation (L8)
### 8.1 Override table
| Flag | Type | Verdict | What changes my mind |
|---|---|---|---|
| Land lease expired 2023; JV agreement 2018; GNCTD opposes renewal; SC threatened AIIMS takeover | bad (existential) | **OPEN** | Executed renewal, or an SC order fixing terms below 20% IPD |
| AR/results omit the expiry and affidavit; "remained compliant" sentence | bad (disclosure) | **OPEN** | Full Reg-30 disclosure of status and hearing outcomes |
| ROIC ~54% | good-but-misleading | **OPEN** (land subsidy) | Renewal at a disclosed rent with OPM ≥ 16% |
| P/E 17 vs peers 48 "cheap" | good-but-misleading | explained (legal discount) | — |
| Apollo keeps pharmacy margin; commission formula undisclosed | bad (parent take) | **OPEN** | AGM annex with rate and term |
| Advertising 7.1% of revenue | unclear | watch | Breakdown; ratio < 6% |
| MD term ended, chair vacant, GNCTD not voting | bad | watch | MD appointed by Q3 results |
| Discharges −2% | bad-but-small | watch | Volume growth resumes |
| Net cash ₹521 cr, no debt, ICR 42x, CFO/PAT 1.24x | good | confirmed (XBRL + screener) | — |
| Unit KPIs cross-foot to revenue | good | confirmed | — |
Open soft flags: 4 (+3 watch) → a written variant view is required (8.3).

### 8.2 What the price implies (worksheet `tools/valuation/live/INDRAMEDCO_worksheet.md`, v1.3)
**Inputs (L8 step 1):** close ₹355.85 on 23-Nov-2026 (NSE bhavcopy; screener ₹356 — two sources; Yahoo has no bar after 18-Nov, ₹358.00); 10 FY-end
P/Es FY17–26 (18.6, 21.1, 12.4, 7.1, 214.8, 9.1, 8.2, 12.7, 22.0, 18.6; median 15.7); peers 33.3–58.8 (median 48.0); 6-month ADV ₹11.6 cr mean /
₹5.5 cr median `[YH]`; net cash ₹521.4 cr; no pending dilution.
**Scenarios (written before the outputs; legal outcome over 5 years):** blow-up 20% (non-renewal/handover → ~0.25x: net cash ₹57/share plus uncertain
compensation for the building/equipment); bear 20% (renewal with enforced 33%/40% EWS incl. medicines and/or market rent: revenue −8% then +5%,
NOPAT margin → 5%, exit 14x); base 45% (pendency continues or renewal on IMCL's ask: +9% → +7%, NOPAT margin 11.2% → 10%, ROIIC 30%, exit 20x); bull
15% (30-year renewal near current terms, partial re-rating: +11%, 12%, exit 28x).
**Outputs:** 5-year multiples bear 0.59x / base 1.70x / bull 2.74x / blow-up 0.25x; **EV 1.35x raw** vs hurdle 1.76x; P(≥2x) 26%, P(≥3x) 7%, P(≤0.5x)
26%, P(blow-up) 20%. Base-case IRR **10.9%** vs CoE 12.5%. Probability-weighted DCF ₹235 (−34%). Reverse DCF: flat margin needs 11.0% revenue
CAGR for 10 years — close to recent growth, *if the hospital is kept*.
**Exit-multiple bet:** DCF-consistent exit P/E 14.7–16.1 vs used 14/20/28 vs own median 15.7 → EV 1.35x / 0.99x / 1.02x. As in every card so far
(L21, L36) the exit multiple is the binding choice; here it is also a proxy for the legal outcome (peers' 48x is what "kept the hospital" might fetch).
**Temperature:** 17.0x = NORMAL vs own history (1.09x median; the own history spans the dormant-dispute, low-margin years), **COLD vs sector (0.35x)**.
**Price-implied probability (two-state read) `[EST]`:** going concern at ~30x on ₹192 cr PAT + cash ≈ ₹630/share; handover ≈ ₹60–90/share. ₹356
implies **P(workable renewal) ≈ 50%**. We have no basis to say the market's ~50% is wrong.

### 8.2b Value-trap test (why is it cheap?)
| Question | Evidence | Answer |
|---|---|---|
| Peak-cycle earnings? | Not cyclical; margins stepped up 10% → 18% with ARPP; discharges flat/falling | **No** (but margins are at a record) |
| Dated catalyst? | SC matter active since Mar-2025; affidavit Jan-2026; hearing listed Mar-2026 (outcome unknown) | **Yes, undated but live** |
| Business deteriorating? | Revenue +11% TTM, OPM 18–19% in H1 FY27; volumes −2% | **No** (price-led) |
| Capital allocation | No debt; cash 16% of mcap earning ~6%; payout 20–40%; no expansion capex (single leased site) | Conservative; cash piling up — possibly a buffer for the dispute |
| Who takes value before minorities? | Apollo (pharmacy margin, services ~5.6% of revenue); GNCTD (free-treatment claim) | **Both partners**; the JV contract has lapsed |
| Fraud / solvency trap? | Clean audit, no debt, no pledge | **No** |
**Conclusion:** cheap because a **verified legal cause** (expired lease, hostile government affidavit, SC warning) can remove the operating
business; it is a **legal-option value trap, not a fraud, solvency or cycle trap**. As with SUNFLAG (L33), a discount with verified causes is not a
claimable edge.

### 8.3 Variant perception
- **What the market appears to price:** roughly even odds that IMCL keeps the hospital on workable terms (17x vs peers 48x).
- **Our view:** **no claimable mispricing.** Our evidence leans slightly *negative* versus the company's framing (omitted expiry; "remained
  compliant"; GNCTD abstaining and leaving board seats empty; MD gap), and positive versus a naive "takeover" fear (net cash ₹57/share floor; courts and
  governments usually prefer stricter terms over closing a 700-bed hospital). The tails are **above** the class base rate for documented reasons.
- **What would prove us wrong (upside):** a disclosed 30-year renewal near IMCL's ask without a retrospective claim — then the peer gap (0.35x) is
  the opportunity the market under-priced.
- **What would prove us wrong (downside):** a handover order — then even our 20% blow-up weight was too low.
- **Base-class departure (card §5):** P(≥3x) 7% vs 21% class; P(≤0.5x) 26% vs 11%; P(blow-up) 20% vs 15%. Tails anchored at **w = 0.3** (below the
  0.5 default) with a written evidence note, because anchoring at 0.5 would *lower* the blow-up probability toward a class that has no lease-expiry
  information. First card where anchoring moves the tails **down** (and EV up: 1.35x → 1.39x).

### 8.4 Decision card (`tools/decision/live/INDRAMEDCO_card.md`, **card v1.3**)
**Rule output: size 0**, blocked by *Expected value vs hurdle* (anchored EV 1.39x, raw 1.35x vs 1.76x). Stage 2 passed (7 hard rules); PEAD quintile
5 (clear); survival cap v1.3 clear (pledge 0%, ICR 41x; `is_financial` false) — **note: the survival cap measures pledge and interest cover, so it
cannot see a legal survival risk like this one**. 4 open soft flags with a written variant view (not blocking). Tier: satellite. Review **2027-02-15**.
Card calls (live, 5-year to 2031-11-23): P(≥3x) 0.071 (base 0.213); P(≤0.5x) 0.26 raw / 0.214 anchored (base 0.113); P(blow-up) 0.20 raw / 0.186
anchored (base 0.154).

---

## 9. Forward calls (live; tags paper-call, deepdive-generated, live, india, sector-healthcare; specs in `tools/scoreboard/specs.json`)
| # | Call (YES if…) | Resolve by | Our P | Naive base | Reasoning |
|---|---|---|---|---|---|
| 1 | Q3 FY27 revenue from operations **≥ ₹400 cr** (+7.5% YoY vs ₹372 cr) | 2027-02-28 | **0.40** | 0.77 | Naive: 10 of 13 quarters grew ≥7.5% YoY. Ours: Q3/Q2 seasonal ratio 0.93–0.98 (mean 0.957) × ₹412.85 cr ≈ ₹395 cr; volumes flat |
| 2 | FY27 OPM (resolver definition) **≥ 18.0%** | 2027-05-31 | **0.55** | 0.23 | Naive: 2 of 11 FYs ≥18.0% (Laplace 0.23). Ours: H1 19.2%; H2 seasonally weaker (H2 FY26 16.7%); central ~18.1% |
| 3 | FY27 net profit **≥ ₹210 cr** (+14%) | 2027-05-31 | **0.40** | 0.70 | Naive: 7 of 10 FYs with PAT growth ≥14%. Ours: H1 ₹109.4 cr; H2 needs ₹100.6 cr (+22% vs H2 FY26 ₹82.7 cr); central ~₹205–208 cr; litigation exceptional risk |
| 4 | IMCL discloses an executed **lease renewal/extension** (or an SC order directing renewal on stated terms) by 30-Nov-2027 | 2027-11-30 | **0.15** | 0.25 | Naive [EST]: ~25%/yr resolution hazard, all renewals. Ours: hostile affidavit; 17-year case; no disclosure since Feb-2026 |
| 5 | A final **non-renewal or handover** order/decision disclosed by 30-Nov-2027 | 2027-11-30 | **0.10** | 0.05 | Naive [EST]: court-ordered takeovers of running private hospitals are rare. Ours: GNCTD + Centre opposed; SC warned explicitly |
| 6 | **MD appointed** (or re-appointed) by 31-Mar-2027 | 2027-03-31 | **0.70** | 0.80 | Naive [EST]: vacancies usually filled within ~5 months. Ours: board approvals slowed by the dispute; chair vacant |
| 7 | INDRAMEDCO price **beats Nifty 500** from 23-Nov-2026 (₹355.85; 23,748.15) to 30-Sep-2027 | 2027-09-30 | **0.40** | 0.44 | Naive: small caps beating the index over ~10 months [EST, as in live #1/#3]. Ours: binary overhang, no dated positive catalyst; already −43% from high |
Card calls (5-year, card v1.3) are in 8.4. Calls 1–3 and 7 resolve automatically (structured specs, standalone basis); 4–6 are assisted (Reg-30 scan,
human confirmation); the card calls are human (total-return series).

---

## 10. What this run taught the method (curriculum)
1. **A "sector-type" frame needs a classification source that covers the frame.** 482 of 809 in-range names had no NSE index industry; without a
   pre-registered hand list the frame would have been 44 names and missed the subject. Proposal: a cached industry map for the full universe
   (screener breadcrumb or NSE quote API on the Pi) so selection doesn't depend on hand judgment.
2. **High ROIC can be a concession, not a moat.** The single most important fact was outside the financial statements (a government land lease that
   expired three years ago). Proposed L2/L5 rule: when ROIC is far above peers, list every government-granted input (land, mining lease, spectrum,
   PPP/concession agreement), its expiry, the reciprocal obligation and its delivery record, and read the counterparty's filings
   (`insight:subsidised-input-roic-and-renewal-risk`).
3. **Read what the company does *not* say.** AR FY26 never states the expiry; it adds a "remained compliant" sentence. The press and court filings
   carried the story. AR-mode disclosure flags (L37) should include **"material external fact absent from the AR"** — checked by searching news/court
   records for the company's key asset, not only by diffing the AR against itself.
4. **Vote results show a broken JV before filings do.** The co-promoter (GNCTD) polled zero votes at the AGM and left its board seats empty
   (`insight:promoter-abstention-vote-signal`). Add "promoter shares held vs votes polled" to the L5 vote-results table.
5. **Tail anchoring works in both directions — and the card should say so.** This is the first card where the raw tails were *above* the class
   rate; anchoring at 0.5 would have pulled them down toward an uninformed prior. w = 0.3 with evidence; Brier scoring will show whether that was right.
6. **The survival cap (v1.3) is blind to legal/licence survival risk.** It reads pledge and interest cover only. Candidate: a "licence/lease
   expiry or regulator threat to the core asset" survival trigger (manual input) for the card.
7. **S0 rule wording:** "entity ceases to exist" let a company whose only asset may be taken through; that is correct for scoreability but should be
   stated in the protocol so future runs don't skip such names (they are exactly where tails matter).
8. **Tool notes:** Yahoo v8 had no INDRAMEDCO bars after 18-Nov-2026 (bhavcopy + screener used for the close); `ar_run.py` crashes on an NSE AR link
   that is listed as a ZIP but does not download as one (`BadZipFile`; worked with `--n 3`); NSE Reg-44 voting results are scanned PDFs (read as images).

## 11. Open items
Outcome of the 19-Mar-2026 SC hearing and any order since (not found); the lease deed's exact free-treatment clauses and rent-revision terms; bed
count (not disclosed); pharmacy commission rate and term; composition of the ₹105 cr marketing line; market rent for the site; who will be MD; GNCTD's
intentions for its 26% stake; Apollo's own disclosure on IMCL; postal-ballot vote numbers (scanned, not extracted); FY23 AR (ZIP download failed).

## Sources
- AR FY2025-26: https://nsearchives.nseindia.in/annual_reports/AR_30962_INDRAMEDCO_2025_2026_A_5876360_01092026125250.pdf
- AR FY2024-25: https://nsearchives.nseindia.in/annual_reports/AR_28029_INDRAMEDCO_2024_2025_A_2956928_01092025152150.pdf
- AR FY2023-24: https://nsearchives.nseindia.in/annual_reports/AR_25362_INDRAMEDCO_2023_2024_3108202413345.pdf
- Q2 FY27 integrated XBRL 29-Oct-2026: https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1748879_29102026043325_WEB.xml
- Board outcome noting the GNCTD affidavit (03-Feb-2026, filed 09-Feb-2026): https://nsearchives.nseindia.in/corporate/INDRAMEDCO_09022026115023_IMCLUPDATE09022026.pdf
- MD term completion 05-Nov-2026: https://nsearchives.nseindia.in/corporate/INDRAMEDCO_05112026103901_IMCL05112026.pdf
- AGM voting results 25-Sep-2026 and postal-ballot results 21-Mar-2026 (NSE announcements, INDRAMEDCO)
- SC order 25-Mar-2025 (diary 33939/2009): https://api.sci.gov.in/supremecourt/2009/33939/33939_2009_3_5_60312_Order_25-Mar-2025.pdf
- LiveLaw 25-Mar-2025: https://www.livelaw.in/top-stories/supreme-court-warns-indraprastha-apollo-hospital-free-treatment-to-poor-patients-joint-inspection-ordered-287728
- ThePrint/PTI 12-Nov-2025: https://theprint.in/india/indraprastha-apollo-hospital-attended-only-9-10-percent-ews-opd-patients-in-5-yrs-delhi-govt-to-sc/2782606/
- Medical Buyer (GNCTD affidavit Jan-2026): https://medicalbuyer.co.in/apollo-hospital-faces-lease-denial-for-ignoring-ews-treatment-mandate/
- Medical Dialogues (IMCL seeks relief, 2025): https://medicaldialogues.in/news/health/hospital-diagnostics/indraprastha-apollo-hospital-seeks-sc-relief-to-reduce-ews-treatment-obligation-148712
- NSE bhavcopy 23-Nov-2026; NSE pledge API 23-Nov-2026; SHP XBRL 30-Sep-2026; Yahoo v8 INDRAMEDCO.NS, ^CRSLDX
- screener.in INDRAMEDCO, ARTEMISMED, SHALBY, YATHARTH, JLHL, NH, APOLLOHOSP, KIMS (24-Nov-2026)
- Selection: scratchpad `live_dd4/` (prereg_selection.md, selection_order.json); skips: `research_notes/Backtests/india_pead_live/eps_history.csv` + `sue_cutpoints.json`
