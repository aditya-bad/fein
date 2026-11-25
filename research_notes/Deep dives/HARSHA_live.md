# Harsha Engineers International (NSE: HARSHA) — LIVE deep dive #6 (method test, protocol v1.4, stages 2→7; first capital-goods draw)

**Date:** 2026-11-25 · **Analyst:** Claude · **Status:** live (not practice). Its paper calls are scored.
**Purpose:** test the deep-dive method on a frame drawn from the new full industry map (IT / Chemicals / Capital Goods), with a
company **drawn at random**. Test material (L9, L21): **no buy/sell verdict**. Outputs: a decision card (**card v1.5** — the task
named v1.4; the tool moved to 1.5 on 2026-11-25, which only changes lender cards) and dated probabilistic calls scored later against
naive base rates.
**Roadmap:** stage 2 (filters) → 3 (signals) → 4 (deep dive) → 5 (valuation) → 6 (decision) → 7 (scoreboard). It unlocks the first
live test on an **export-led industrial component supplier in a capex phase**, where the question is return on new capital, not
survival or a legal binary.
Research, not SEBI-registered advice.

Source tags: `[AR26]`/`[AR25]` annual reports (NSE; AR26 filed 29-Jun-2026); `[XBRL]` NSE integrated-filing XBRL (consolidated unless
marked; Q2 FY27 filed 03-Nov-2026, FY26 filed 07-May-2026, plus Q4 FY25–Q1 FY27); `[CALL]` earnings-call transcripts on NSE (Q2 FY27 =
04-Nov-2026; earlier calls Nov-2024 → Aug-2026); `[NSE]` announcements / bhavcopy / SHP XBRL / pledge API; `[BSE]` BSE announcements
(scrip 543600, two ≤1-year windows 25-Nov-2024 → 25-Nov-2026, 160 items); `[SCR]` screener.in pages fetched 25-Nov-2026; `[YH]` Yahoo v8
daily closes (last bar 25-Nov-2026 intraday); `[WEB]` web search 25-Nov-2026 (single-source); `[EST]` my estimate (method shown).
Money in ₹ crore unless stated. "Two sources" for P&L lines = XBRL and screener agree (checked for every quarter used).

---

## 0. Selection (rules fixed before drawing; full log in `HARSHA_selection/`)
**Task rule:** universe.csv joined to industry_map.csv; India; mcap ₹1,000–20,000 cr at the latest NSE bhavcopy close; sector column ∈
{IT/software, Chemicals, Capital Goods}; exclude SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK and financials; `random.Random(20261203)`
shuffle of the sorted eligible list; first name passing stage-2 filters, outside the PEAD avoid window, and scoreable.
**Pre-registration:** `HARSHA_selection/prereg_selection.md`, written **09:37 IST 25-Nov-2026 before the frame was built** (sha256
`47b2b58e…deaa`, recorded in the walk log). Exact sector values: `Information Technology`, `Chemicals`, `Capital Goods`.
**How it ran:** the 24-Nov bhavcopy file exists but carries 23-Nov data (identical bytes; 24-Nov was not a trading day) → frame close
**23-Nov-2026**. 1,547 symbols, all priced; **809** in band; **0** in-band names missing from the map (the map fixed dd4/dd5's 60%
unclassified problem). In-band by sector: Capital Goods 153, Chemicals 72, IT 38. SUNFLAG removed. **Eligible 262.**
**Walk:** #1 **HARSHA** (₹3,990 cr) passed all five checks → subject. **Skips: none.** Next in order (not checked): HPL, RATEGAIN, GHCL,
DEEPAKFERT.

## 0b. Rule zero: edge before depth
1. **What the market knows.** Largest independent bearing-cage maker (7,500+ designs, 20–2,000 mm; brass, steel, polyamide) supplying
   global bearing majors from Ahmedabad, Changshu (China) and Ghimbav (Romania); FY27 guidance: consolidated revenue +10–12%, India
   mid-to-high teens, India EBITDA ~22% `[CALL Q2 FY27]`. Trailing P/E 24.4. The five most-asked Q2 questions: Romania downsizing (×4),
   why H2 guidance is soft after +21% H1 (×2), metal pass-through and margins (×3), Advantek breakeven and capex (×3), China growth (×2).
2. **The variable nobody asks about:** **the return on the ₹~600 cr capex wave** (Advantek Bhayla phases 1–2 "₹350 cr plus", China
   phase 2 ~₹100 cr) versus a **group ROIC of ~11.5%**, below a 12.5% cost of equity. Advantek runs at ~54% utilisation and is still adding
   capacity `[NSE Reg-30 28-May-2026]`.
3. **Layers:** L2 (group ROIC/ROIIC re-derived), L3 (plant utilisation and capex per piece), L5 (votes, subsidies). Honest limit: no
   information edge on customers' outsourcing decisions.

---

## 1. S2 checklist (disqualifiers v3; filled before L1, every rule dated)
| Rule | Status | Evidence (source, date) |
|---|---|---|
| H1a fake cash | **pass** | Liquid ₹533.5 cr at 30-Sep-2026: cash 22.13 + other bank 21.78 + current inv. 265.51 + non-current inv. 224.04 `[XBRL Q2]`; screener investments 490 `[SCR]` (two sources). Gross debt ₹438.5 cr held alongside — management: debt "backed by either lower interest rate or … government subsidy" `[CALL Q2]`; AR26 has **no** government-grant or interest-subsidy note (open item, 6.4). |
| H1b implausible economics | **pass** | India Engineering EBITDA 23.7% Q2 FY27 `[CALL]` vs Rolex Rings ROCE 21% `[SCR]`; consolidated OPM 15–17%. |
| H1c unverifiable profits | **pass** | Global bearing majors as customers (one ≥10%: ₹205.3 cr FY26) `[AR26 consol. segment note]`; exports ₹480 cr FY26 `[CALL]`; debtor days 85 `[SCR]`. |
| H2 auditor | **pass** | FY26 standalone + consolidated opinions unmodified `[AR26]`; statutory auditor Pankaj R. Shah & Associates completed its term at the 23-Jul-2026 AGM; Mukesh M. Shah & Co appointed for 5 years `[NSE Reg-30 23-Jul-2026]` — rotation. |
| H3 rating | **pass (single-source, stale)** | CARE AA- (Stable)/A1+ reaffirmed on ₹483.87 cr facilities `[NSE 13-Mar-2024]`; no INC/withdrawal; **no 2025–26 rating filing found** in NSE or BSE lists (open). |
| H4 pump | **pass** | Main board IPO 26-Sep-2022 (issue ₹330); 6-month ADV ₹7.5 cr mean / ₹5.1 cr median `[YH]`. |
| H5 RPT leakage | **pass** | 6.1. |
| Exit triggers | **none** | Results on time; no restatement. |
| G pledge | **clear** | Pledge API 25-Nov-2026: 0 rows; SHP XBRL 30-Sep-2026 encumbrance flags all false; promoters 75.00% (74.61% Mar-2025 → 75.00% Sep-2025) `[SCR]`. |
| G accounting trouble | **clear** | None; FY25 ₹95.0 cr standalone impairment of the Romania investment is disclosed `[AR26 RPT note]`. |
| G dilution | **watch** | ESOP 2026: ≤18 lakh options = 1.98% of 9.104 cr shares (approved 23-Jul-2026, 99.76% for) `[AR26 notice; NSE AGM results]`. |
| G solvency (S1/S5) | **clear** | `solvency_screen.py` 25-Nov-2026: grade blank, 2 flags (ST borrowings 170 > cash 45 + 0.5×CFO 68; dividends 9 > FCF −47 while debt 200→372). ICR FY26 13.9x; TTM 9.6x (EBIT ex-OI 220 / finance cost 23). |
| Q CFO/PAT | ok (FY26 weak) | FY22–26 CFO 583 vs PAT 570 = 1.02x; FY26 alone 0.44x `[SCR]`. |
| Q negative FCF | watch | FCF FY25 −2, FY26 −47 `[SCR]`. |
| Q other-income share | ok | TTM OI ₹30 cr = 13% of PBT; core PBT ~₹197 cr. |

**Survival cap / L39 addendum.** Pledge 0% and ICR 9.6x → **neither flag fires**, so the "both flags → answer the balance-sheet question
first" rule is not triggered. (Recorded so the check is visible; the balance-sheet facts are still in 3 and 6.4.)

**Stage-3 signals.** PEAD: Q2 FY27 SUE **+1.81 → quintile 5** (event 03-Nov-2026); Q1 FY27 −0.10 → Q2 but outside the window. Survival cap
clear. **Credibility (concall mode, hand ledger, n=7): 57% vs auto-components peer median 60%** (nearest sector file; no bearing-component
set). Met: FY26 consolidated growth "at least higher single digit" (May-2025) → +15.6%; "much stronger bottom line" → PAT +74%; India
"low to mid-teen" (Nov-2025) → standalone +12.8%; Japan customer back to growth in FY27 (May-2025) → H1 +28%. Missed: bushings ~30% FY26
→ ~25% `[AR26]`; Romania operating breakeven (hoped Q4 FY25, Nov-2024; "EBITDA first", Feb-2026) → still loss-making; ₹117 cr/yr bushing
contract sales from Q4 FY26 (Aug-2025) → "a little bit delayed" (Nov-2026). **Pattern: numbers met, dates slip (L26).**

---

## 2. Map (L1)
**Business.** Bearing cages (the separator that holds rolling elements; ~5% of a bearing's value by management's estimate `[CALL Q2]`),
plus bushings for wind gearboxes (FY26 ~₹127 cr, +25%), precision stampings (FY26 ~₹72 cr; railway seal inserts, AC-compressor parts,
accumulators) and large-size cages. Solar EPC + O&M (rooftop/ground-mount) is a separate segment.
**Segments FY26** `[AR26 MD&A table + segment note]`: Engineering & others revenue ₹1,443.6 cr, EBITDA (incl. OI) ₹263.9 cr; Solar EPC
₹183.2 cr, ₹14.2 cr. *Disclosure quirk:* the MD&A table labels the FY26 EBITDA column "2024-25" (₹263.85 + 14.15 = ₹278.2 cr = FY26 KPI
EBITDA ₹278.17 cr `[AR26 KPI note]`).
**Geography FY26:** India ₹786.5 cr / outside India ₹840.3 cr (SEZ sales counted as outside). Non-current assets India ₹565 cr of ₹635 cr
(**89% in Ahmedabad district, Gujarat**).
**Subsidiaries:** Harsha Engineers Advantek Ltd (HEAL, India; Bhayla; FY26 loss ₹11.6 cr); Harsha Precision Bearing Components (China)
(FY26 profit ₹4.9 cr); Harsha Engineers Europe SRL (Romania; FY26 loss ₹14.2 cr); Cleanmax Harsha Solar LLP (JV) `[AR26 consolidation
table]`.
**Ownership:** promoters (Rangwala and Shah families) 75.00%, DIIs 13.92%, FIIs 1.11%, public 9.95%; shareholders 63,505 (96,528 in
Dec-2023) `[SCR]`.
**Peers (P/E, `[SCR]` 25-Nov-2026):** Rolex Rings 22.1 (bearing rings — same chain position), NRB 28.2, Schaeffler 43.4, SKF India 44.6,
Timken 50.5 (bearing makers = customers), Sansera 70.2; median 44.0.
**Flags (v1.4):** holdco — none (liquid assets 13% of mcap, offset by debt). Cyclical — industrial/auto demand; FY23→FY25 PAT fell 123→89
(−28%) on European weakness + Romania; FY21 COVID revenue −1%. Price: ₹599.5 (03-Jul-2024) → ₹314.2 (30-Mar-2026), −48% `[YH]`.

## 3. Financials re-derived (L2) `[SCR consolidated; XBRL checks]`
| FY | Revenue | OPM % | Op. profit | Other inc. | PAT | EPS | FY-end close | FY-end P/E |
|---|---|---|---|---|---|---|---|---|
| FY20 | 886 | 10 | 86 | 13 | 22 | 2.84 | — | — |
| FY21 | 874 | 14 | 122 | 3 | 45 | 5.88 | — | — |
| FY22 | 1,321 | 13 | 169 | 17 | 92 | 11.90 | — | — |
| FY23 | 1,364 | 14 | 190 | 29 | 123 | 13.54 | 335.05 | 24.7 |
| FY24 | 1,392 | 12 | 171 | 30 | 111 | 12.24 | 401.10 | 32.8 |
| FY25 | 1,408 | 12 | 175 | 10 | 89 | 9.81 | 371.70 | 37.9 |
| FY26 | 1,627 | 15 | 240 | 38 | 155 | 17.05 | 314.25 | 18.4 |
| **TTM Sep-26** | **1,781** | **15** | **272** | **30** | **163** | **17.94** | 438.25 | **24.4** |
FY17–19 on screener are a pre-restructuring standalone entity — not used. FY26 from XBRL: revenue 1,626.79; materials 875.84 − inventory
change 26.84 = 849.0 (52.2%); employees 215.0 (13.2%); other expenses 323.1 (19.9%); finance 16.26; D&A 46.66; PAT 155.20; EPS 17.05 — =
screener ✓. Q2 FY27: revenue 440.09, PAT 45.03, EPS 4.95 (XBRL = screener ✓). H1 FY27: revenue 897.52 (+20.7%), PAT 82.41 (+10.8%).
- **Group ROIC [EST].** Invested capital ≈ equity 1,486 + debt 438.5 − liquid 533.5 = **₹1,391 cr** (incl. goodwill 44); NOPAT = EBIT ex-OI
  220 × 0.73 = 160 → **ROIC ~11.5%**. FY23→TTM: ΔNOPAT ~+46 on ΔIC ~+390 → **ROIIC ~11%**. India Engineering's 22–24% EBITDA margin is
  real but is diluted by Romania, solar, working capital (~135 days) and new plants (**looks-good flag**: the segment margin flatters).
- **Normalised EPS (v1.4):** mean consolidated PAT FY20–26 = ₹91 cr ÷ 9.104 cr shares = **₹10.0 → 43.8x** vs 24.4x trailing. Not
  "cheap" on any lens: 0.85x own median (n=4), 0.55x bearing peers but ≈ Rolex Rings.
- **Customer concentration (Ind AS 108):** one customer ₹205.3 cr = **12.6%** of FY26 revenue (₹155.3 cr = 11.0% in FY25).
- **Other income:** TTM ₹30 cr (treasury + FX); core PBT ~₹197 cr.
- **Cash:** CFO FY23–26 137/136/206/68; FY26 CFO = 24% of EBITDA incl. OI (₹278 cr) as working capital and solar receivables rose.

## 4. Unit economics (L3) — the plant and the piece
| Item | Value | Source / route |
|---|---|---|
| Advantek capacity, utilisation | 38 m pieces/yr, **~54%** | `[NSE Reg-30 28-May-2026]` |
| Advantek Phase 2 | +12 m pieces for ₹110 cr → **₹9.2 per annual piece** | same |
| Advantek revenue FY27 guide | ~₹140 cr `[CALL Q2]` → ~₹6.8/piece at 54% of 38 m `[EST]` | revenue ÷ (38 m × 0.54) |
| Advantek total capex | "₹350 cr plus", ~₹250 cr loans `[CALL Q2]` | → asset turn ~0.4x on ₹140 cr revenue today |
| Mgmt asset-turn claim | ~2x on productive (non-building) capex `[CALL Q2]` | at full utilisation |
| Q-run interest + D&A at Advantek | ₹7.5–8 cr/quarter, rising to ~₹10 cr `[CALL Q2]` | |
**Payback two ways [EST].** (a) Management route: ₹110 cr productive capex × 2x = ₹220 cr revenue × ~22% EBITDA = ₹48 cr/yr → ~2.3-year
EBITDA payback *at full use*. (b) Utilisation route: Advantek today ≈ ₹140 cr revenue on ~₹350 cr capital (0.4x) at a loss; to reach a
12.5% pre-tax return on ₹350 cr it needs ~₹44 cr EBIT ≈ ₹300 cr+ revenue at ~15% EBIT margin — i.e. **utilisation roughly double today's**
before the new 12 m pieces are counted. The 6x gap between routes is the finding: the payback depends on filling capacity, which depends on
customer outsourcing (₹75 cr project from Q3–Q4 FY27; ₹117 cr bushing contract delayed).

## 5. Cost drivers (L4), ranked by weight (FY26 consolidated, % of revenue ₹1,626.8 cr)
| Line | ₹ cr | % | Physical driver | Sensitivity |
|---|---|---|---|---|
| **Materials (net)** | 849.0 | **52.2%** | Brass (copper + zinc) and steel strip; solar modules in EPC | 10% metal move on an assumed 70–80% metal-linked share [EST] = ₹60–68 cr ≈ 370–420 bp before pass-through; pass-through "very standard" with customer-specific lags `[CALL Q2]` |
| Employees | 215.0 | 13.2% | 1,745 permanent employees + workers, 1,539 contract `[AR26 BRSR]`; Romania/China staff | +10% wages = −132 bp |
| Contractor labour | 59.4 | 3.7% | Gujarat contract workers (minimum-wage-linked VDA, Apr/Oct) `[AR26 n.26]` | +10% = −37 bp |
| Stores & spares + packing | 86.7 | 5.3% | Tooling consumption, export packing | — |
| Power & fuel | 36.7 | 2.3% | Gujarat industrial tariff; captive solar (10.4 MW commissioned at Wada FY26) | +10% = −23 bp |
| Freight & forwarding | ~41 (standalone) | ~2.5% | Exports to Europe/US/Japan | +20% ocean freight ≈ −50 bp [EST] |
**Materials ratio by quarter (XBRL, net of inventory change):** Q4 FY25 54.1% · Q1 FY26 51.1 · Q2 51.0 · Q3 51.5 · Q4 54.5 · Q1 FY27 52.5
· **Q2 FY27 48.3**. The Q4 spikes coincide with solar-heavy quarters; Q2 FY27's low ratio = pass-through lag on rising brass + low solar
share (CFO: "a mix of both"). Pass-through inflated H1 growth by ~4–5 pts `[CALL Q2]`: of +21%, ~16% is volume/mix.

## 6. Governance, ownership, related parties (L5)
### 6.1 RPT table `[AR26 consolidated RPT note]` (₹ cr)
| Item | FY25 | FY26 | Share |
|---|---|---|---|
| Sales to AIA Engineering (directors' significant influence) | 15.1 | 28.3 | 1.7% of revenue |
| Sales to Goldi Harsha Ventures LLP | 0.3 | 1.4 | — |
| Purchases/services from KMP-linked entities (Crest Creative, relatives, Ecological Service Inc.) | 1.0 | 1.6 | 0.2% of other exp. |
| Managerial remuneration (directors/KMP) | 9.5 | 11.0 | 7.1% of PAT, 4.0% of EBITDA |
| CSR to promoter-linked trusts (Aastha, Sant Vinoba) | 1.4 | 3.0 | — |
| Dividends to directors/KMP/relatives | 6.8 | 6.8 | — |
No royalty/parent fee (not an MNC subsidiary). **Verdict: clean**; no RPT required a shareholder vote.
### 6.2 Vote results (Reg-44, AGM 23-Jul-2026) `[NSE scrutiniser report 27-Jul-2026]`
| Resolution | For (m) | Against (m) | Against % | Note |
|---|---|---|---|---|
| 1–6 (accounts, dividend, 2 director rotations, auditor, cost auditor) | 80.4–80.6 | ≤0.17 | ≤0.21% | — |
| 7, 8, 10 (re-appoint IDs Ambar Patel, Bhushan Punani, R. Kasinathan) | ~80.5 | ≤0.10 | ≤0.12% | — |
| **9 (re-appoint ID Kunal Shah, special)** | **69.21** | **11.40** | **14.14%** | **promoter-held 68.28 m; ~0.93 m non-promoter for vs 11.40 m against → ~92% of non-promoter votes cast against [EST]** |
| 11–12 (ESOP 2026, incl. subsidiaries) | 80.42 | 0.20 | 0.24% | — |
**Promoter shares held vs votes polled (L40):** total votes ~80.6 m; promoters hold 68.28 m → non-promoters polled ≈12.3 m of 22.8 m (54%)
[EST: the report has no category split; assumes all promoter shares voted]. The Kunal Shah dissent came from institutions; the reason is not
disclosed (the terms of all four IDs end 09-Jan-2027) `[AR26 notice]`.
### 6.3 People and incentives
CEO Vishal Rangwala; CFO Maulik Jasani; chairman Rajendra Shah; MD Harish Rangwala. Head–Brass SBU resigned 21-Aug-2026 `[NSE]`. ESOP 2026
up to 1.98% dilution (exercise price not extracted — open). Promoter at the 75% MPS ceiling: further promoter buying is capped.
### 6.4 L40 — government and licence-dependent inputs (and what the AR omits)
| Input | Dependence | In AR26? | Status |
|---|---|---|---|
| Interest subsidy / concessional loans for Advantek & capex ("backed by … government subsidy") | Finance cost | **No** (no Ind AS 20 note found) | **External fact absent from AR — open** (Gujarat runs interest-subsidy schemes for manufacturing `[WEB: ic.gujarat.gov.in]`; no company-specific record found) |
| Solar EPC: ALMM / import and subsidy norms; "PV sales relaxations … up to Dec-26" `[CALL Q2]` | ~11% revenue, ~5% EBITDA | Generic | Watch (Dec-2026 date) |
| US tariffs on Indian goods (exports to US via customers) | Export demand | No | Single-source `[WEB]`: Feb-2026 framework cut most Indian goods to 18%; Section 232 parts and newer Section 301 layers unclear; bearings not addressed — open |
| Land: Bhayla plant (Survey 376–379) replaced a leased plant vacated 31-Oct-2025 `[NSE]` | Core plant | Ownership not stated | Open item (low risk) |
| EOU/SEZ status of Moraiya unit (2003 EOU) | Duty/tax | Sales to SEZ unit noted | No expiry found |
**L41 state-law check (concentration applies: 89% of non-current assets in Gujarat):** Gujarat contract-labour wage (VDA) revisions affect
~1,526 non-permanent workers; Gujarat Factories (Amendment) Act 2023 shift flexibility; Gujarat interest-subsidy GRs. **No gazette search
done this run** (open item; none of these is existential). No core-asset threat → card `core_asset_threat` not set.

## 7. Scuttlebutt plan (L6; not executed — user's ground checks)
1. **Bhayla plant (Bavla taluka):** shifts running, trucks/day, lines installed vs the 38 m-piece claim (tests the 54% utilisation).
2. **Customers' India capex** (SKF India/Industrial ~₹500–800 cr, Timken Bharuch, NRB Bharuch SRB/CRB `[CALL]`): do their localisation
   plans buy Harsha cages or in-source? Ask bearing distributors in Ahmedabad/Pune.
3. **Romania (Ghimbav):** local press/labour-office notices of layoffs (dates the "downsizing").
4. **Gujarat Industries Commissionerate** sanction lists for interest subsidy (company name), to size the subsidy.
5. **LME copper/zinc and Indian HR-strip prices** monthly vs the quarterly materials ratio (pass-through lag).
Ethics: public sources only; no unpublished price-sensitive information.

---

## 8. Override (L7) and valuation (L8)
### 8.1 Override table
| Flag | Type | Verdict | What changes my mind |
|---|---|---|---|
| Group ROIC ~11.5% < CoE during a ₹~600 cr capex wave; Advantek 54% utilised and adding capacity | bad (capital allocation) | **OPEN** | Advantek PAT+ two half-years and group ROIC ≥14% on FY28 |
| Romania losses; downsizing undisclosed | bad | **OPEN** | Reg-30 plan with costs; foreign-sub losses < ₹1 cr for two quarters |
| ~92% of non-promoter votes against an ID re-appointment | bad (governance signal) | **OPEN** | Disclosed technical reason; no repeat |
| Subsidised debt not disclosed in AR; gross debt held with ₹533 cr liquid | bad (disclosure, L40) | **OPEN** | AR FY27 note on scheme/rate/amount |
| One customer 12.6% and rising | bad | watch | Share < 10% or long contract disclosed |
| Bushing contract delay; outsourcing project start | bad-but-small | watch | ₹45 cr bushing quarter; project shipping Q4 FY27 |
| Record gross margin Q2 FY27 | good-but-misleading | explained | — (pass-through + mix) |
| India Engineering +23% at 23.7%; XBRL = screener; RPTs small; no pledge | good | confirmed | — |
| Segment EBITDA column mislabelled in AR26 MD&A | disclosure quirk | noted | — |
**Open soft flags: 4** (+2 watch); credibility −3 pts vs peers (not counted as open by the card at −3) → variant view written (card §2).

### 8.2 What the price implies (`tools/valuation/live/HARSHA_worksheet.md`, worksheet v1.3)
**Inputs:** close **₹438.25** on 23-Nov-2026 (NSE bhavcopy = Yahoo; screener 25-Nov ₹441); 4 FY-end P/Es only (listed Sep-2022): 24.7,
32.8, 37.9, 18.4 (median 28.8); peers 22.1–70.2 (median 44.0); 6-month ADV ₹7.5 cr mean; net cash ~₹95 cr; ESOP dilution ≤2%.
**Scenarios (written before outputs):** blow-up 5% raw (−80% path: lost account + stranded capex; 0.3x); bear 25% (+3%/yr, NOPAT margin 7%,
ROIIC 8%, exit 15x); base 50% (+12% → +9%, 9.5%, ROIIC 14%, exit 24x); bull 20% (+17% → +12%, 11.5%, ROIIC 20%, exit 32x).
**Outputs:** 5-year multiples bear 0.68x / base 1.64x / bull 2.89x / blow-up 0.30x; **EV 1.58x** (raw = anchored) vs hurdle 1.76x;
P(≥2x) 30%, P(≥3x) 10%, P(≤0.5x) 9%, blow-up 5%. Base IRR **8.7%** vs CoE 12.5%. Probability-weighted DCF **₹190 (−57%)**.
**Reverse DCF:** no revenue path in −30% to +80% reproduces the price at ROIIC 14%; on the base growth path the price needs a **year-10
NOPAT margin of 24.5%** (today 9.0%). Price-implied ROIIC: none up to 300% on that path. **Reading:** when ROIIC ≈ CoE, growth adds almost no
DCF value, so the price is a bet that new capital earns far more than the last five years' ~11%.
**Exit-multiple bet (L21):** DCF-consistent exit P/E 9.2/10.6/13.5 vs used 15/24/32 → EV 0.73x at DCF exits vs 1.58x at used exits. The
whole EV above 1x is the multiple bet. Bull ROIIC 20% is flagged (>5 pts above history) — the bull case *is* the claim that the new plants
earn India-Engineering returns.
**Temperature:** own history INSUFFICIENT (n=4); COLD vs sector (0.55x) — but the sector set is mostly the customers.
### 8.2b Why is it not cheaper / is it a trap?
| Question | Evidence | Answer |
|---|---|---|
| Peak-cycle earnings? | FY26–H1 FY27 recovery after FY23–25 dip; record gross margin on pass-through | **Partly** (mid-recovery, not peak) |
| Capital allocation | ₹600 cr capex at 54% utilisation; gross debt + gross treasury | **Question** (6.4, 4) |
| Who takes value before minorities? | Promoters' RPTs small; ID vote dissent | Low leakage |
| Fraud/solvency trap? | Clean audit, AA-, no pledge, net cash | **No** |
### 8.3 Variant perception
Market: a quality component franchise worth ~24x on recovering EPS. Our view: **no claimable mispricing**; the testable question is whether
Advantek/China earn >14% ROIC by FY28. Evidence leans sceptical (utilisation, delays, Romania, ROIC < CoE); upside if outsourcing projects
fill Bhayla. Tails: raw blow-up 5% < class 15% (balance sheet), anchored at default w=0.5 → 10.2%.
### 8.4 Decision card (`tools/decision/live/HARSHA_card.md`, **card v1.5**)
**Rule output: size 0**, blocked by *Expected value vs hurdle* (EV 1.58x anchored = raw vs 1.76x). Stage 2 passed (7 hard rules); PEAD Q5;
survival cap clear (pledge 0%, ICR 9.6x; both-flags rule not triggered); 4 open soft flags with a variant view (not blocking); tier
satellite; review **2027-02-15**. Card calls (5-year to 2031-11-23): P(≥3x) 0.101 (base 0.213); P(≤0.5x) 0.089 raw / 0.101 anchored (base
0.113); P(blow-up) 0.050 raw / 0.102 anchored (base 0.154).

---

## 9. Forward calls (live; tags paper-call, deepdive-generated, live, india, sector-capital-goods; specs in `tools/scoreboard/specs.json`)
| # | Call (YES if…) | Resolve by | Our P | Naive base | Reasoning |
|---|---|---|---|---|---|
| 1 | Q3 FY27 consolidated revenue **≥ ₹450 cr** (+10% YoY vs ₹409.25 cr) | 2027-02-28 | **0.35** | 0.38 | Naive: 5 of 13 quarters (Q2 FY24–Q2 FY27) grew ≥10% YoY `[SCR]`. Ours: Q3/Q2 ratio 0.956/0.960/1.082 (FY24–26) on ₹440 cr → ₹421–476 cr, central ~₹440; management warns Q3 is soft and Romania is shrinking; pass-through helps |
| 2 | FY27 consolidated revenue **≥ ₹1,822 cr** (+12%, top of guidance) | 2027-05-31 | **0.70** | 0.38 | Naive: 2 of 6 FYs (FY21–26) grew ≥12% (Laplace 3/8). Ours: H1 ₹897.5 cr; H2 needs ₹924.5 cr = +4.7% vs H2 FY26 ₹883.2 cr while H1 grew +20.7% and India is guided mid-high teens |
| 3 | FY27 consolidated net profit **≥ ₹180 cr** (+16%) | 2027-05-31 | **0.40** | 0.63 | Naive: 4 of 6 FYs had PAT growth ≥16% (Laplace 5/8). Ours: H1 ₹82.4 cr (+10.8%); H2 needs ₹97.6 cr (+21% vs ₹80.8 cr); Advantek H2 turn and smaller foreign losses help; Romania one-offs, Q3 softness hurt; central ~₹175 cr |
| 4 | FY27 consolidated OPM (resolver definition) **≥ 16.0%** | 2027-05-31 | **0.45** | 0.11 | Naive: 0 of 7 FYs (FY20–26) ≥16% (Laplace 1/9). Ours: H1 15.84%, Q2 16.99%; guided consolidated engineering 17–18%; Q4 is solar-heavy (Q4 FY26 materials 54.5%); H2 needs ≥16.15% |
| 5 | A Reg-30 disclosure of the **Romania restructuring** (downsizing plan, closure, sale or capacity cut) by 31-Mar-2027 | 2027-03-31 | **0.55** | 0.50 | Naive [EST]: coin-flip for a "next quarter" promise; our ledger has dated promises slipping 3 of 4 times. Ours: stated twice on the Q2 call ("next quarter… followed by disclosure"); Q3 results due Feb-2027 |
| 6 | HARSHA **beats the Nifty 500** from 23-Nov-2026 (₹438.25; 23,748.15) to 30-Sep-2027 | 2027-09-30 | **0.45** | 0.44 | Naive [EST, as live #1/#3/#4]. Ours: PEAD Q5 drift is a small positive; valuation needs ROIC improvement; no dated catalyst beyond Romania |
Card calls (5-year) are in 8.4. Calls 1–4 and 6 resolve automatically (consolidated XBRL + screener; Yahoo); 5 is assisted (Reg-30 scan,
human confirmation); the card calls are human (total-return series).

---

## 10. What this run taught the method (lesson candidates)
1. **A full industry map makes S0 clean.** 0 of 809 in-band names unclassified (dd4/dd5 had 482); no hand list, no judgement. Keep the
   map refreshed with an `as_of` date.
2. **Check the bhavcopy's DATE1, not the file name.** The 24-Nov-2026 file holds 23-Nov data. Rule: the frame close is the DATE1 value.
3. **Segment margins can hide a group ROIC below the cost of equity.** India Engineering 22–24% EBITDA; group ROIC ~11.5%; ROIIC ~11%.
   When ROIIC ≈ CoE, the reverse DCF finds no growth path and the DCF-consistent exit P/E collapses to ~10x — the price is entirely a bet on
   returns on new capital. Proposed L2/L3 rule: compute group ROIC and ROIIC before reading segment margins; for any capex phase, rebuild
   payback by the utilisation route as well as management's asset-turn route (here they differ ~6x).
4. **Headline vote percentages understate minority dissent when promoters hold 75%.** 14.14% against = ~92% of non-promoter votes cast.
   Proposed L5 rule: always compute dissent as against ÷ (votes cast − promoter shares) and report it next to the headline.
5. **L40 for manufacturers: the government input is often financing.** "Debt backed by government subsidy" appears only on the call; the
   AR has no grant/subsidy note. Generalise the "external fact absent from the AR" flag to financing subsidies and policy-dated segment
   rules (solar ALMM relaxations to Dec-2026).
6. **AR disclosure quirk worth a flag:** the MD&A segment table mislabels the FY26 EBITDA column as 2024-25 (cross-foot to the KPI note).
7. **Tool notes:** `decision_card.py` takes credibility as a fraction (57 printed as "5700%" — candidate input validation); the worksheet's
   own-history temperature needs n ≥ 5 (recent IPOs get "insufficient"); the NSE pledge API returned 0 rows (SHP XBRL used); AR26 two-page
   spreads garble `pdftotext -layout` (consolidated cost lines taken from XBRL instead); no 2025–26 rating filing found on NSE/BSE.

## 11. Open items
Interest-subsidy scheme, rate and amount; current CARE rating (post-Mar-2024); Romania restructuring cost; Advantek FY27 revenue and
utilisation; ESOP 2026 exercise price; reason for the Kunal Shah dissent (proxy-adviser reports); US tariff on bearing parts (HTS 8482.99)
for Indian origin; Bhayla land tenure; Gujarat gazette check (wages, subsidy GRs); metal-linked share of materials; FY23 AR (ZIP, not read).

## Sources
- AR FY2025-26: https://nsearchives.nseindia.in/annual_reports/AR_29478_HARSHA_2025_2026_A_15877505_29062026151738.pdf
- AR FY2024-25: https://nsearchives.nseindia.in/annual_reports/AR_27528_HARSHA_2024_2025_A_20082025181832.pdf
- Q2 FY27 consolidated XBRL: https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1751817_03112026042536_WEB.xml (standalone 1751857)
- FY26 consolidated XBRL: https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1664416_07052026040234_WEB.xml
- Q2 FY27 call transcript (04-Nov-2026): https://nsearchives.nseindia.in/corporate/Harsha_06112026142552_Transcript_of_Earning_Call_Q2FY2027.pdf ; earlier calls 14-Nov-2024, 14-May-2025, 12-Aug-2025, 11-Nov-2025, 11-Feb-2026, 12-May-2026, 17-Aug-2026 (NSE)
- AGM voting results 23-Jul-2026: https://nsearchives.nseindia.in/corporate/Harsha_27072026144843_AGM_Results_2026.pdf
- Auditor rotation 23-Jul-2026: https://nsearchives.nseindia.in/corporate/Harsha_23072026155216_Reg_30_Appointment_of_Statutory_Aud.pdf
- Advantek Phase 2 (28-May-2026): https://nsearchives.nseindia.in/corporate/Harsha_28052026142110_SE_Intimation_HEAL_May2026_F.pdf
- Advantek plant shift (31-Oct-2025): https://nsearchives.nseindia.in/corporate/Harsha_31102025182635_SE_Intimation_HEAL_Lease_Plant_Vacation.pdf
- Bushing contract (01-Aug-2025): https://nsearchives.nseindia.in/corporate/Harsha_01082025183207_SE_Letter__Agreement.pdf
- CARE rating (13-Mar-2024): https://nsearchives.nseindia.in/corporate/HARSHA_13032024214007_CreditratingFY24.pdf
- NSE bhavcopy sec_bhavdata_full_24112026.csv (DATE1 23-Nov-2026); SHP XBRL 30-Sep-2026; pledge API 25-Nov-2026; Yahoo v8 HARSHA.NS, ^CRSLDX
- screener.in HARSHA (consolidated), ROLEXRINGS, NRBBEARING, SKFINDIA, SCHAEFFLER, TIMKEN, SANSERA (25-Nov-2026)
- [WEB] US–India tariff status: https://cleartax.in/s/us-tariff-on-india ; https://theprint.in/diplomacy/us-assures-india-of-comparative-tariff-advantage-as-trade-talks-continue/3098026/ ; Gujarat interest-subsidy schemes: https://ic.gujarat.gov.in/assistance-to-manufacturing-sector-under-the-scheme-of-interest-subsidy
- Selection: `research_notes/Deep dives/HARSHA_selection/` (prereg_selection.md, selection_order.json)
