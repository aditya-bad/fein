# Uttam Sugar Mills (NSE: UTTAMSUGAR) — LIVE deep dive #8 (method test, protocol v1.4, stages 2→7; first IT/FMCG/Consumer-Durables-frame draw)

**Date:** 2026-11-25 · **Analyst:** Claude · **Status:** live (not practice). Its paper calls are scored.
**Purpose:** test the deep-dive method on a new sector frame with a company **drawn at random**. Test material (L9, L21):
**no buy/sell verdict**. Outputs: decision card v1.5 and dated probabilistic calls scored later against naive base rates.
**Roadmap:** stage 2 (filters) → 3 (signals) → 4 (deep dive) → 5 (valuation) → 6 (decision) → 7 (scoreboard). It unlocks the
first live test of a **government-administered spread business** (cane price, sugar floor price, export bans and ethanol tender
design are all set by the state) and the first live use of L40 on a *recurring* government input rather than a one-off lease.
Research, not SEBI-registered advice.

Source tags: `[AR26]` annual report FY2025-26 (NSE, filed 24-Aug-2026; standalone notes unless marked); `[XBRL]` NSE
integrated-filing XBRL, consolidated (Q2 FY27 filed 31-Oct-2026; Q1 FY27, FY26/Q4, Q3 FY26, Q2 FY26, FY25/Q4); `[DECK]` Q2 FY27
results presentation (31-Oct-2026); `[NSE]` announcements (100, 25-Nov-2024 → 25-Nov-2026) / bhavcopy / SHP XBRL / pledge API;
`[BSE]` announcements (scrip 532729, 118 items); `[AGM]` Reg-44 voting results (18-Sep-2026; 19-Sep-2025); `[RAT]` rating letters
(CARE 12-Dec-2024, 17-Sep-2025; India Ratings 18-Mar-2025, 10-Jun-2026); `[SCR]` screener.in fetched 25-Nov-2026; `[YH]` Yahoo v8
daily closes; `[WEB]` web search 25-Nov-2026 (news; single-source unless two outlets agree); `[EST]` my estimate (method shown).
Money in ₹ crore. "Two sources" for P&L lines = XBRL and screener agree (checked for every quarter and year used).

---

## 0. Selection (rules fixed before drawing; full log in `UTTAMSUGAR_selection/`)
**Task rule:** universe.csv joined to industry_map.csv; India; mcap ₹1,000–20,000 cr at the latest bhavcopy close (DATE1 column,
L42); sector ∈ {`Information Technology`, `Fast Moving Consumer Goods`, `Consumer Durables`} (exact map values; map sector list
checked first: 22 values); exclude SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA, SHK and financials; `random.Random(20261205)`
shuffle of the sorted eligible list; first name passing stage-2 filters, outside the PEAD avoid window, and scoreable.
**Pre-registration:** `UTTAMSUGAR_selection/prereg_selection.md`, written **04:57 UTC (10:27 IST) 25-Nov-2026 before the frame was
built** (sha256 `511f2565…f70e37b0`, recorded in the walk log). Disclosed there: I had seen dd7's eligible list (incl. the 38 IT
names) and its first-15 order.
**How it ran:** 25-Nov file → 404; the 24-Nov file holds DATE1 = 23-Nov-2026 on every row (byte-identical to the 23-Nov file) →
frame close **23-Nov-2026**. 1,547 symbols, all priced; **809** in band; 0 unmapped. In band: IT 38, FMCG 53, Consumer Durables 58;
no excluded subject present. **Eligible 149.**
**Walk:** #1 **UTTAMSUGAR** (₹1,329 cr) passed all five checks → subject. **Skips: none.** Next (not checked): INFOBEAN, DOMS,
BSOFT, WHIRLPOOL. Third live draw in a row on walk #1 (HARSHA, SHK, UTTAMSUGAR).
**Frame note (lesson candidate):** industry_map files a sugar miller under *Fast Moving Consumer Goods / Agricultural Food & other
Products*. The frame meant "consumer" but delivered an agri-commodity processor. The draw is valid (no hand reclassification was
allowed), but sector frames built on the NSE macro map carry commodity names; 53 FMCG names include sugar, tea, edible oil and
dairy mills.

## 0b. Rule zero: edge before depth
1. **What the market knows.** A 27,000 TCD western-UP/Uttarakhand sugar miller with 300 KLPD of molasses distilleries, 122 MW of
   co-generation and a 40 KLPD grain distillery (UDL, 83.7%) being expanded to 160 KLPD. FY26 revenue ₹2,202 cr, PAT ₹101 cr.
   SS 2025-26 crush −25% (floods). The stock is up ~86% from its 2026 low (₹187 → 389) on the Jul-Aug 2026 sugar-price spike
   (₹48.18 → ₹55.70/kg retail; stock limits from 1-Aug-2026 `[WEB: PIB factsheet]`). **No earnings calls** (0 analyst-meet /
   con-call items in 100 NSE filings), so there is no "most-asked questions" list; institutions own 0.46%.
2. **The variable that matters:** the **government-set spread** — cane SAP (₹390–405/qtl, 2026-27 SAP not yet announced) vs the
   sugar MSP (₹31/kg, frozen since Feb-2019) and ethanol tender design (B-heavy/syrup ethanol **excluded** from ESY 2026-27,
   16-Oct-2026). At 9.42% recovery the SAP alone costs ~₹4,150 per qtl of sugar ≈ the ₹4,143 FY26 realisation.
3. **Layers:** L1/L4 (per-tonne-of-cane economics; L40 government inputs), L2 (group ROIC first, L42; core EPS, L44), L5 (votes
   net of promoters; MD pay; promoter preference shares). Honest limit: no information edge on the SAP decision or the crop.

---

## 1. S2 checklist (disqualifiers v3; filled before L1, every rule dated)
| Rule | Status | Evidence (source, date) |
|---|---|---|
| H1a fake cash | **pass** | Cash ₹37.4 cr + bank 4.0 vs borrowings ₹71.8 cr at 30-Sep-2026; cash ₹9.2 cr vs ₹721.8 cr at 31-Mar-2026 `[XBRL]` — no idle cash beside debt. |
| H1b implausible economics | **pass** | EBITDA 9–20% FY17–26 `[SCR]`; per-tonne rebuild (§4) reproduces FY26 EBITDA within ~2%; peers' ROCE 6–9% `[SCR]`. |
| H1c unverifiable profits | **pass** | Counterparties are 1.02 lakh farmers at a notified price, OMCs (ethanol) and state utilities UPPCL/UPCL (power) `[AR26]`. |
| H2 auditor | **pass (EoM)** | B.K. Kapur & Co. unmodified FY26 (15-May-2026) with **Emphasis of Matter**: interest on an unsecured **State of Uttarakhand loan** not provided (₹26.26 lakh/yr, ₹52.52 lakh cumulative; waiver application pending, no demand since Jan-2008) `[AR26 directors' report; auditor's report]`. Term to the 32nd AGM (2027) — rotation due next year. CARO: one title deed not in the company's name. |
| H3 rating | **pass (upgraded)** | CARE A- → **A Stable** / A2+ → A1 (17-Sep-2025); India Ratings A- → **A Stable** / A1 on ₹1,000 cr lines (10-Jun-2026) `[RAT]` (two agencies, two dates). |
| H4 pump | **pass** | Main board; 6-month ADV ₹12.1 cr mean / ₹5.6 cr median `[YH]`; NSE volume/price clarification letters (Apr, Aug, Oct 2026) — routine. |
| H5 RPT leakage | **pass (watch)** | §6.1. |
| Exit triggers | **none** | Results on time (Q2 FY27 31-Oct-2026); no restatement. |
| G pledge | **clear** | Pledge API 0 rows; SHP XBRL 30-Sep-2026 every promoter encumbrance flag `false`; promoter 74.71%. |
| G accounting trouble | **watch** | EoM above; CFO resigned 15/16-Sep-2026 ("personal reasons"), successor 18-Sep-2026 `[NSE]`. |
| G dilution | **clear** | 38,138,120 shares unchanged since FY17; preference capital fully redeemed 10-Jul-2026. |
| G solvency (S1/S5) | **watch** | `solvency_screen.py` 25-Nov-2026: grade blank, 1 flag (S3: ST borrowings 675 > cash 17 + 0.5×CFO 270, FY26) — the seasonal sugar-inventory cash credit; ICR 3.6x FY26, **4.1x TTM** (154.9 / 38.1). |
| Q CFO/PAT | ok | FY22–26 CFO 883 vs PAT 578 = 1.53x `[SCR]`. |
| Q negative FCF | watch | FY24 −91, FY25 +55, FY26 +213 `[SCR]`; FY27 UDL capex ₹110 cr. |
| Q other-income share | ok | TTM other income 6.7 = 5% of PBT; exceptional −1.35 (labour codes) `[XBRL]`. |

**Survival cap / L39 addendum:** pledge 0%, ICR 4.1x — neither flag fires.
**Stage-3 signals.** PEAD: Q2 FY27 SUE **+0.28 → quintile 3** (event 31-Oct-2026); Q1 FY27 −1.15 → Q1 (10-Aug-2026, ~70 trading
days before the close, superseded). **Credibility: not scored (AR mode, L37)** — only 2 dated promises: UDL 160 KLPD "by March, 2027"
(open; the Q2 FY27 deck still lists UDL at 40 KLPD) and the preference-redemption extension to 2029 (Feb-2026) that was reversed by
full redemption in Jul-2026. Disclosure flags in §6.4.

---

## 2. Map (L1)
| Unit | State | Cane TCD | Co-gen MW | Distillery KLPD | Notes |
|---|---|---|---|---|---|
| Barkatpur (Bijnor) | UP | 8,500 | 53 | 250 (B-heavy/syrup rating) | 200 TPD potash |
| Shermau (Saharanpur) | UP | 6,000 | 25 | – | |
| Khaikheri (Muzaffarnagar) | UP | 5,500 | 15 | – | |
| Libberheri (Haridwar) | Uttarakhand | 7,000 | 29 | 50 | refined/pharma sugar, 50 TPD potash; regd. office |
| UDL, Bahadarabad (83.73%) | Uttarakhand | – | – | 40 (48 installed) → 160 by Mar-2027 | grain-based; bought in two tranches FY25 incl. 16.2 m shares from promoter-group **Uttamenergy Ltd** for ₹25.6 cr `[AR26 n.34g]` |
**UP = 74% of crush capacity → L41 state-law check (§6.4).** Value chain: farmer cane (SAP) → mill → sugar (open market under
monthly release quotas; branded/specialty line to HORECA, quick-commerce) + molasses/B-heavy/syrup → ethanol (OMC tenders) or ENA
(potable) + bagasse → power (state utilities). Peers with the same unit (western-UP mills): Balrampur Chini, Triveni, Dhampur,
Dwarikesh, Avadh. **Cyclical flag: yes** (sugar cycle + monsoon + policy). Holdco flag: no.

## 3. Financials re-derived (L2) `[SCR; XBRL checks]`
| FY | Sales | OP | OPM | Interest | PAT | EPS | March IC (eq+debt) | FY-end P/E |
|---|---|---|---|---|---|---|---|---|
| FY17 | 1,085 | 217 | 20% | 74 | 107 | 27.95 | 876 | 3.7 |
| FY18 | 1,243 | 117 | 9% | 80 | 17 | 4.46 | 947 | 22.0 |
| FY19 | 1,228 | 172 | 14% | 80 | 58 | 15.24 | 959 | 8.9 |
| FY20 | 1,645 | 182 | 11% | 79 | 52 | 13.54 | 1,095 | 3.8 |
| FY21 | 1,819 | 218 | 12% | 86 | 60 | 15.67 | 1,158 | 5.8 |
| FY22 | 2,034 | 271 | 13% | 75 | 135 | 35.38 | 1,103 | 6.1 |
| FY23 | 2,059 | 245 | 12% | 52 | 124 | 32.41 | 1,170 | 7.1 |
| FY24 | 2,047 | 266 | 13% | 56 | 132 | 34.67 | 1,457 | 9.0 |
| FY25 | 1,846 | 213 | 12% | 57 | 86 | 23.16 | 1,621 | 11.2 |
| FY26 | 2,202 | 229 | 10% | 52 | 101 | 26.30 | 1,598 | 9.5 |
FY17–23 standalone, FY24+ consolidated (UDL). FY-end P/E = Yahoo close on the last March trading day ÷ that FY's EPS; median **8.0x**.
Quarter check: every quarter Q2 FY26 → Q2 FY27 matches XBRL = screener to the rupee crore (e.g. Q2 FY27 revenue 494.00, OP 22.63,
PAT 4.54).
- **TTM (Q3 FY26..Q2 FY27):** revenue 2,091.7; OP 204.7; D&A 49.8; EBIT ex OI **154.9**; interest 38.1; PBT 122.1; PAT 90.9; EPS 23.72
  → **14.7x** at ₹348.50.
- **L44 core EPS:** other income 6.7 (5% of PBT), exceptional −1.35 → core EPS **22.9–23.0** (two routes) → **15.2x**. Core ≈
  reported: the L44 strip changes nothing here (contrast SHK, where it moved P/E from 18.7x to ~35x).
- **Normalised (cyclicals rule):** 10-yr mean EPS 22.88 → **15.2x**; trailing and normalised agree, both **HOT vs own history**
  (90th percentile). The cheap-looking absolute P/E is a high one for this stock. Last down-cycle: FY17 → FY18 EPS −84% (27.95 →
  4.46); price 2023 high ₹522 → 2025 low ₹178 (−66%); Jun-2015 loss year with negative reserves and the stock at ₹18–26.
- **Seasonality:** net debt swings ₹828 cr (Mar-25) → 264 (Sep-25) → 712 (Mar-26) → **30 (Sep-26)** as sugar inventory (₹1,154 →
  ₹143 cr) is financed and sold. I use the four-point average **₹460 cr [EST]** in valuation; the September balance sheet flatters
  leverage and ROIC.
- **L42 group ROIC first:** TTM NOPAT 116 ÷ seasonal-average IC ~1,300 = **8.9%** (7.3% on March IC). Full-cycle ROIIC FY17–19 →
  FY24–26 = (191 − 144)×0.75 ÷ (1,559 − 927) = **5.6%**. Both below the 12.5% cost of equity (3rd draw in a row with group ROIC < CoE).
  Segment pre-tax returns on average segment assets FY26: sugar ~13%, distillery ~12%, co-gen ~30% — but inter-segment transfer
  prices (₹489 cr) decide the split, so segment ROAs are not evidence of a strong unit.
- **Concentration:** no customer ≥10% disclosed for sugar; ethanol buyer set = 3 OMCs (one tender); power = 2 state utilities.

## 4. Unit economics (L3) — one tonne of cane (FY26 / SS 2025-26 `[AR26]`, per-tonne figures `[EST]`)
| Line | Physical | ₹ per tonne cane |
|---|---|---|
| Cane cost | SAP ₹390–400/qtl + society commission ₹5.50/qtl | ~4,000 |
| Sugar | net recovery 9.42% × ₹4,143/qtl net realisation | 3,903 |
| Ethanol / ENA | 877 lakh BL ÷ 30.15 lakh t ≈ 29 L/t × ~₹58/L | ~1,690 (before distillery conversion cost) |
| Power export | 1,006 lakh kWh ÷ 30.15 lakh t ≈ 33 kWh/t × ₹5.68 | ~190 |
| Conversion (staff, stores, power, other) | employees ~₹110 cr + other expenses ~₹145 cr + distillery costs [EST from H1 FY27 ×2] | ~1,000 |
| **EBITDA** | | **~770 → ×3.0 mt ≈ ₹232 cr vs FY26 reported 229** |
**Two-way capex payback (L42), UDL 40 → 160 KLPD (₹110 cr, Reg-30 29-Sep-2025):** (a) at FY26 UDL economics (EBITDA ₹12.96 cr
on 40 KLPD at 95% utilisation = ₹0.32 cr/KLPD-yr) the added 120 KLPD earns ~₹39 cr/yr → **2.8-yr pre-tax payback**; (b) at the
FY25–26 average (₹7.0 cr; FY25 was ₹1.0 cr) → ~₹21 cr/yr → **5.2 years**, and at FY25 margins ~35 years. The spread is the grain
price (FCI rice / maize) vs a government-fixed ethanol price — another administered input. Grain plants are favoured in the
ESY 2026-27 tender (DEP preference `[WEB]`), which helps UDL and hurts the B-heavy distillery at Barkatpur.

## 5. Cost drivers (L4), ranked by weight (FY26)
| Line | % of revenue | Physical driver | Sensitivity [EST] |
|---|---|---|---|
| Cane (materials + inventory change) | ~80–85% (H1 FY27 84%) | tonnes crushed × SAP | +₹10/qtl SAP = +₹100/t ≈ **₹30–39 cr EBITDA (15–19% of TTM)** at 3.0–3.9 mt |
| Employees | ~5% | 3,197 staff (H1 FY27 ₹54.5 cr) | — |
| Other expenses (stores, power, repairs) | ~7% | | — |
| Finance cost | 2.4% | seasonal cash credit, ~8% | crop size drives inventory and interest |
**Revenue-side administered prices:** sugar MSP ₹31/kg (Feb-2019), monthly release quotas, export prohibited 13-May → 30-Sep-2026
`[AR26]`; FRP ₹365/qtl for 2026-27 (+₹10) `[AR26; WEB]`; ethanol prices for juice/B-heavy unchanged since ESY 2022-23 (NFCSF `[WEB]`).
Recovery: each 0.1% of recovery ≈ 3 kg sugar/t ≈ ₹124/t ≈ ₹37–48 cr — the one lever the company controls (cane development).

## 6. Governance, ownership, related parties (L5)
### 6.1 RPT table `[AR26 n.34 (q), ₹ cr]`
| Party | Nature | FY26 | FY25 |
|---|---|---|---|
| R.K. Adlakha (MD, promoter) | remuneration 4.08 + commission 5.00 + perqs 0.14 | **9.22** (= 9.3% of cons. PAT) | 11.33 |
| S.L. Sharma (ED) | remuneration | 1.03 | 0.88 |
| Uttam Industrial Engg (promoter co.) | plant & machinery / vehicles; services | 0.90; 0.61 | 0.44; 0.57 |
| Promoter entities | 6.5%/10% non-cumulative redeemable preference shares redeemed | 8.85 (FY26) + 0.53 (10-Jul-2026) | – |
| Promoter entities / family | unsecured loan (10% simple, repayable on demand) | small (₹27 lakh) | |
| Standard Type Foundry | office rent | 0.21 | 0.21 |
RPTs through the P&L are small (<0.2% of costs). The cash to promoters is pay (MD commission) and preference redemptions. The Feb-2026
postal ballot extended preference redemption to 31-Mar-2029 "in view of present cash flow position, future capex"; all of it was then
redeemed by 10-Jul-2026 — a plan reversed within five months (disclosure flag, not leakage).
### 6.2 Vote results — dissent net of promoter votes (L42) `[AGM]`
| Meeting / item | Votes cast | Promoter votes | Against | Against ÷ non-promoter votes | Non-promoter turnout |
|---|---|---|---|---|---|
| AGM 2026 item 6: MD re-appointment + pay (special) | 21,137,530 | 20,925,929 | 11,227 | **5.3%** | 2.2% |
| AGM 2026 routine items | 23,265,937 | 23,060,539 | 353 | 0.2% | 2.1% |
| AGM 2025 all items | 23,445,711 | 23,060,539 | 105–145 | <0.1% | 4.0% |
Institutions (0.46% of shares) voted 52.5% against the MD — a token stake. **L40 vote read:** promoter shares held 28,492,830 but only
23,060,539 voted at **both** AGMs — **~5.43 m promoter shares (19% of the block, 14% of equity) never vote**; on item 6 the MD's
own 2,134,610 shares abstained while the result sheet says "promoter interested: No". I could not identify which holders do not
vote (the SHP lists 14 individuals and 6 companies) — open item.
### 6.3 People and incentives
MD R.K. Adlakha (promoter; re-appointed 2026); ED S.L. Sharma; CFO changed Sep-2026; CS Rajesh Garg. MD commission ₹5–7 cr/yr is
the main incentive and is profit-linked; no ESOPs.
### 6.4 L40/L41 — government inputs and external facts missing from the company's disclosures
| Input | Counterparty | Status (date) | In company disclosure? |
|---|---|---|---|
| Cane price (SAP) | UP / Uttarakhand govts | 2025-26: UP ₹400 early / ₹390 general; UK ₹405/₹395. **2026-27 SAP not announced** (search 25-Nov-2026; crushing began ahead of Diwali; BKU demands ₹500) `[AR26; WEB]` | 2025-26 yes; 2026-27 n/a |
| Sugar MSP / quotas / exports | GoI | MSP ₹31/kg since Feb-2019; exports banned 13-May-2026; stock limit on dealers 1-Aug → 30-Nov-2026 `[AR26; WEB: PIB]` | yes (AR) |
| **Ethanol tender design** | GoI / OMCs | **ESY 2026-27 tender (BPCL, 16-Oct-2026, ~11 bn L): zero sugar diversion; no bids sought for juice, syrup or B-heavy ethanol**; C-heavy and grain eligible; Q1 allocations subject to litigation `[WEB: autocarindia, thefederal, freepressjournal, agrospectrum/ISMA — four outlets agree]` | **No** — the 31-Oct-2026 deck states capacity "based on B-heavy/syrup" and says nothing about the tender |
| Uttarakhand state loan | Govt of Uttarakhand | one-time assistance; interest unprovided since 2008, waiver pending `[AR26 EoM]` | yes (EoM) |
| Power PPAs | UPPCL / UPCL | 1,006 lakh kWh, ₹56.6 cr FY26 `[AR26]` | yes |
| Molasses reservation (UP excise, country liquor) | UP govt | **not verified this run** | open item |
**Read:** this business is an option on four government decisions a year. The B-heavy exclusion cuts the ethanol volume that the 300
KLPD distilleries were built for; diverted sucrose (5.82 lakh qtl in SS 2025-26 = 1.93% of cane) returns as sugar into a tight market,
so the net P&L effect is ambiguous [EST: −₹20 to +₹20 cr depending on the sugar price], but distillery utilisation on own C-heavy
molasses could fall well below half. Survival-cap core-asset trigger **not set** (override log in the card): not a licence/lease
loss, and C-heavy remains eligible.

## 7. Scuttlebutt plan (L6; not executed — user's ground checks)
1. UP cane department SAP notification for 2026-27 (date, ₹/qtl) — the single most important dated number.
2. Barkatpur distillery: is it running on C-heavy or idle in Dec-2026? (tanker traffic; local cane-society officials.)
3. Cane-payment status at the four mills (UP cane department arrears dashboard) — mills short of cash pay late first.
4. Ex-mill sugar prices in Muzaffarnagar (weekly) vs the ₹31 MSP.
5. Who are the non-voting promoter holders? (MCA filings of the six promoter companies.)

## 8. Override (L7) and valuation (L8)
### 8.1 Override table
| Flag | Verdict | What changes my mind | Review |
|---|---|---|---|
| Group ROIC ~9% / ROIIC 5.6% < CoE | open | FY28 ROIC ≥ 11% after tax | 2027-05-31 |
| Administered spread; 2026-27 SAP pending | open | SAP hike ≤ ₹10 or MSP +₹3/kg | 2027-02-15 |
| L40: B-heavy exclusion not disclosed | open | allocation disclosed; FY27 ethanol ≥ 700 lakh BL | 2027-05-31 |
| HOT vs own history (15.2x vs 8.0x) | open | FY27 PAT ≥ ₹115 cr | 2027-05-31 |
| Governance/disclosure (MD pay 9% of PAT; non-voting promoter block; pref plan reversed; CFO change) | watch | AR FY27 explanations | 2027-09-30 |
| Uttarakhand loan EoM; title deed | watch | waiver / registration | 2027-09-30 |
| "14.7x looks cheap" — good-but-misleading | explained | — | — |
| A-rated, near-zero September net debt — good | confirmed | — | — |
**4 open soft flags → variant view written (card §2); the variant view is "no claimable mispricing".**

### 8.2 What the price implies (`tools/valuation/live/UTTAMSUGAR_worksheet.md`, worksheet v1.3)
Scenarios were written before the run (tails from the class base rates; blow-up 10% raw because of the company's own 2015 history).
- Snapshot: mcap 1,329, net debt 460 (seasonal average), EV 1,789, P/E 14.7, EV/EBITDA 8.7, FCF yield 7.5%.
- **Base-case IRR 7.5%** vs CoE 12.5%. Reverse DCF: no growth path reproduces the price (needs a 20% NOPAT margin vs 5.6% today).
- **DCF value per share:** bear −44, base 12, bull 118 → probability-weighted ₹20 vs ₹348.50. The bear DCF is below net debt
  (L21/L44 warning): at ROIIC < CoE the cash flows do not carry the price; every multiple above ~0.3x is the exit-P/E bet.
- **Exit-multiple bet:** exits 6/9/13x vs DCF-consistent 0.2/3.5/6.9x vs own median 8.0x → EV of the 5-yr multiple 0.74x at the
  used exits, 0.31x at DCF exits, 0.65x at the own median. Even our base case (exit 9x, above the 10-yr median) is a de-rating from 15x.
- Temperature: HOT vs own history (1.84–1.90x median), NORMAL vs peers (0.95x of 15.5x).
- Reinvestment-realism flag: bull ROIIC 12% vs 5.6% history (bull needs an MSP hike — pricing, not capital).
### 8.2b Why is it not cheaper / is it a trap?
The market is paying a peers-like P/E for a mill whose own history says 4–11x. The plausible reason is cycle position: low national
closing stock (~4.25 mt), a retail price spike, an export ban that ended 30-Sep-2026 and hopes for an MSP rise. That is the market
pricing a *good* 2026-27 season, which our base case does not assume. Not a trap in the fraud sense (A-rated, clean cash) — a
cyclical at a high multiple of normal earnings.
### 8.3 Variant perception
None claimable. The one thing we found that the price may not reflect is the B-heavy exclusion (a negative), and it is public news
the company has not discussed. We cannot know the SAP or the crop before the market.
### 8.4 Decision card (`tools/decision/live/UTTAMSUGAR_card.md`, **card v1.5**)
**Rule output: size 0** — EV 0.89x anchored (raw 0.74x) vs hurdle 1.76x. Gates: S2 passed (7/7), PEAD clear (Q3), survival clear,
4 open soft flags with a variant view. Probabilities (5 yrs): P(≥3x) model 0.8% vs base 21.3%; P(≤0.5x) model 37.9% vs 11.3%
(anchored 24.6%); P(blow-up) 10% vs 15.4% (anchored 12.7%). The card printed the **anchoring-lowered** warning (P(≤0.5x)): our raw
tail rests on company evidence (entry P/E 1.9x own median, own 2015 and 2018 collapses), so the raw tail is the honest number.
**Calibration concern (written before scoring):** P(≥3x) 0.8% is probably too low — this stock went 41 → 522 (12.7x) in 2020–23 and
18 → 208 in 2016–17. The lognormal σ=0.40 and three scenarios cannot reproduce commodity-cycle right tails, and the card anchors only
the left tails (L43). If the ≥3x call resolves YES, that is the lesson, not bad luck.

## 9. Forward calls (live; tags paper-call, deepdive-generated, live, india, sector-sugar; specs in `tools/scoreboard/specs.json`)
| id (thesis:paper-call:UTTAMSUGAR:…) | Claim | P | Base | Base reasoning | Resolver |
|---|---|---|---|---|---|
| q3fy27-revenue-550cr-plus | Q3 FY27 (Dec-2026) consolidated revenue ≥ ₹550 cr | 0.55 | 0.20 | Q3s FY24–26: 517.7 / 424.7 / 521.2 → 0 of 3 ≥550 → Laplace 1/5 | india_fin structured |
| q3fy27-opm-12pct-plus | Q3 FY27 OPM (resolver basis) ≥ 12.0% | 0.45 | 0.60 | Q3 OPM 14.28 / 14.13 / 11.02 → 2/3 → Laplace 3/5 | india_fin structured |
| fy27-revenue-2200cr-plus | FY27 consolidated revenue ≥ ₹2,200 cr (FY26 2,201.65) | 0.45 | 0.67 | revenue grew in 7 of 10 FYs FY17–26 → Laplace 8/12 | india_fin structured |
| fy27-opm-10pct-plus | FY27 OPM ≥ 10.0% (FY26 10.41%; H1 FY27 4.44%) | 0.35 | 0.83 | OPM ≥10% in 9 of 10 FYs → Laplace 10/12 | india_fin structured |
| fy27-net-profit-100cr-plus | FY27 consolidated PAT ≥ ₹100 cr (H1 5.84) | 0.25 | 0.42 | PAT ≥100 in 4 of 10 FYs → Laplace 5/12 | india_fin structured |
| udl-160klpd-by-mar27 | UDL 160 KLPD commissioned by 31-Mar-2027 | 0.35 | 0.40 | our ledgers: dated capacity promises met on time ~40% (L26, dates slip) [EST] | doc_scan assisted |
| beats-nifty500-to-sep27 | Total return beats Nifty 500 from 23-Nov-2026 to 30-Sep-2027 | 0.40 | 0.50 | coin flip | price_relative structured |
| card 5y-ge3x / le0p5x / blowup | from the card | 0.008 / 0.379 / 0.10 | 0.213 / 0.113 / 0.154 | class base rates | human |
Reasoning for the FY calls: H1 FY27 PBT 7.9 vs 21.1; H2 must carry the year. H2 FY26 OPM 15.7% and H2 FY25 17.6% were earned at the
old SAP with B-heavy ethanol; H2 FY27 faces a pending SAP increase and lower ethanol; the crop should recover from the floods. FY27
PAT ≥100 needs H2 ≥ ₹94 cr vs ₹85 cr in H2 FY26.

## 10. What this run taught the method (lesson candidates)
1. **L40 generalises to recurring administered prices.** For a sugar miller the "government input" is not one lease but four annual
   decisions (SAP, MSP, export/quota, ethanol tender design). The rule should require a dated table of each administered price with
   its next decision date — and a check whether the latest one appears in the company's own filings (here the B-heavy exclusion did not).
2. **The core-asset trigger is binary; partial input withdrawals need a graded field.** The ESY 2026-27 exclusion hits ~25% of segment
   EBIT but is not existential; the card has no place for it except the tails.
3. **Seasonal balance sheets: use average capital and average net debt.** September net debt ₹30 cr vs March ₹712 cr; ROIC 12.7% vs
   7.3% depending on the date. Worksheet input should accept a seasonal-average note (or two balance-sheet dates).
4. **L44 is not always the binding adjustment.** Core = reported here; the binding read was "HOT vs own history" — a low absolute P/E
   can be the 90th percentile for a cyclical.
5. **The card's right tail is uncalibrated for commodity cyclicals.** P(≥3x) 0.8% vs class 21% and vs this stock's own 12.7x run in
   2020–23. Tail anchoring covers only the left tails (L43); a pre-registered test of anchoring P(≥3x) too is worth writing.
6. **Frame hygiene:** industry_map's FMCG sector contains agri-commodity processors; a "consumer" frame needs basic_industry filters
   written into the prereg if consumer brands are what we mean.
7. **L42 again:** 3 of 3 draws in these frame families (HARSHA, SHK, UTTAMSUGAR) had group ROIC below CoE, and 8 of 8 live cards are
   size 0. Consistent with L43 (base cases below CoE drive the zeros).
8. **Vote read:** the "promoter interested" field on the result sheet can be wrong (MD's own re-appointment marked "No"); always
   reconcile promoter shares held vs voted per item.

## 11. Open items
- UP molasses-reservation order for 2026-27 and its price (not verified).
- Identify the ~5.43 m promoter shares that never vote (MCA / SHP holder-level).
- Ethanol allocation to Uttam under ESY 2026-27 (OMC allocation lists) and the litigation outcome.
- UP SAP 2026-27 announcement — record the date and ₹/qtl in memdb when it comes.
- The auditor rotation in 2027 (B.K. Kapur & Co. term ends at the 32nd AGM).

## Sources
- AR FY26: https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_24082026174953_AR_31032026_Signed.pdf
- Q2 FY27 XBRL (consolidated): https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1750793_31102026070927_WEB.xml
- Q2 FY27 deck: https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_31102026184438_Presentation_signed.pdf
- AGM 2026 voting results: https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_18092026183612_VotingResultsSigned.pdf
- AGM 2025 voting results: https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_19092025191526_ScrutinizerReportAndVotingResultsSigned.pdf
- Ratings: https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_17092025173826_CreditRatingSigned.pdf ; https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_10062026153514_CreditRatingSigned.pdf
- CFO resignation: https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_16092026151433_ResignationofCFOSigned.pdf
- UDL expansion: https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_29092025125651_ExpansioninDistillerycapacityofUDLSigned.pdf
- Preference postal ballot: https://nsearchives.nseindia.in/corporate/UTTAMSUGAR_16022026180129_Intimationpostalballotsigned.pdf
- SHP XBRL 30-Sep-2026: https://nsearchives.nseindia.in/corporate/xbrl/SHP_1739023_15102026045533_WEB.xml
- Bhavcopy: https://nsearchives.nseindia.in/products/content/sec_bhavdata_full_24112026.csv
- screener: https://www.screener.in/company/UTTAMSUGAR/consolidated/ (and BALRAMCHIN, TRIVENI, DHAMPURSUG)
- ESY 2026-27 tender: https://www.autocarindia.com/industry-amp/government-bars-sugar-based-ethanol-in-2026-27-tender-report-441078 ; https://thefederal.com/category/business/india-sets-zero-sugar-diversion-ethanol-2026-27-259885 ; https://freepressjournal.in/business/india-halts-sugar-diversion-for-ethanol-in-2026-27-invites-bids-for-11-billion-litres-amid-rising-prices ; https://agrospectrumindia.com/index.php/news/112/35044/isma-welcomes-govts-calibrated-approach-on-sugar-and-ethanol-cautions-against-continued-preference-to-dedicated-ethanol-plants.html
- SAP 2026-27 pending: https://www.cmv360.com/news/up-sugarcane-crushing-season-2026-27-begins-at-9-mills-ahead-of-diwali ; https://commodity-board.com/uttar-pradesh-sap-debate-puts-sugarcane-margins-in-the-spotlight
- Sugar price spike / stock limits: https://pib.gov.in/FactsheetDetails.aspx?Id=150971 ; ISMA MSP ask: https://agrospectrumindia.com/index.php/news/8/33951/isma-welcomes-rs-10-qtl-hike-in-sugarcane-frp-for-2026-27-calls-for-timely-alignment-of-sugar-msp-and-ethanol-prices.html
