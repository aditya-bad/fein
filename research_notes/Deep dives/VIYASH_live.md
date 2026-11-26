# Viyash Scientific (NSE: VIYASH; formerly SeQuent Scientific) — LIVE deep dive #9 (method test, protocol v1.4, stages 2→7; first IT/Healthcare-frame draw; first pharma)

**Date:** 2026-11-26 · **Analyst:** Claude · **Status:** live (not practice). Its paper calls are scored.
**Purpose:** test the deep-dive method on a company **drawn at random**. This is test material (L9, L21), so there is
**no buy/sell verdict**. Outputs: decision card v1.5 and dated probabilistic calls, scored later against naive base rates.
**Roadmap:** stage 2 (filters) → 3 (signals) → 4 (deep dive) → 5 (valuation) → 6 (decision) → 7 (scoreboard). New in this dive:
(a) consensus forward P/E beside our scenarios (L47); (b) news run plus L50 verification; (c) worksheet core-EPS inputs (L44).
It unlocks the first live test of a **post-merger entity**, which has no usable own history, and of **pharma-specific S2 checks**
(USFDA status, US price erosion, API/China dependence). This is research, not SEBI-registered advice.

Source tags:
- `[AR26]` annual report FY2025-26 (NSE, filed 17-Jul-2026; consolidated notes unless marked).
- `[XBRL]` NSE integrated-filing XBRL, consolidated (Q2 FY27 filed 13-Nov-2026; Q1 FY27; Q4/FY26; Q3 FY26; Q2 FY26 and Q4 FY25 are pre-merger SeQuent as first reported).
- `[DECK]` Q2 FY27 and Q4 FY26 investor presentations.
- `[CALL]` earnings-call transcripts of 20-May, 12-Aug and 14-Nov-2026 (NSE PDFs).
- `[NSE]` announcements (209 items, 26-Nov-2024 → 26-Nov-2026), bhavcopy, SHP and pledge API.
- `[BSE]` announcements (scrip 512529, 224 items).
- `[RAT]` rating letters (ICRA 22-Apr-2026; India Ratings 30-Apr-2026).
- `[SCR]` screener.in, fetched 26-Nov-2026.
- `[YH]` Yahoo v8 daily closes; Yahoo quoteSummary consensus, 26-Nov-2026.
- `[FDA]` FDA Import Alert 66-40 page, fetched 26-Nov-2026.
- `[WEB]` web search (single-source unless two outlets agree).
- `[EST]` my estimate, with the method shown.

Money is in ₹ crore. "Two sources" for P&L lines means XBRL and screener agree (checked for every quarter used). The worksheet values the company on an
**attributable basis**: group lines × 0.86, because 40% minorities sit in Appco and Karizoo.

---

## 0. Selection (rules fixed before drawing; full log in `VIYASH_selection/`)
**Task rule:**
- Universe: universe.csv joined to industry_map.csv; India.
- Size band: mcap ₹1,000–20,000 cr at the latest bhavcopy close (DATE1 column).
- Sector: `Information Technology` or `Healthcare`. Both exact values exist in the map: 86 / 113 rows.
- Exclusions: the 7 prior live subjects, the 12 promise-forward-test companies and financials.
- Draw: a `random.Random(20261206)` shuffle of the sorted eligible list; the subject is the first name that passes S2, sits outside the PEAD avoid window and is scoreable.

**Pre-registration:** `VIYASH_selection/prereg_selection.md`, written 07:06 UTC on 26-Nov-2026, before the frame was built
(sha256 `882f9b3b…5b6e21d4c4`). It discloses what I had already seen (dd8's eligible list incl. 38 IT names; the 4 Healthcare forward-test names).

**Frame:**
- The 26-Nov file returned 404. The 25-Nov file has DATE1 = 25-Nov-2026 on every row, so the frame close is **25-Nov-2026**.
- 1,547 symbols, all priced; **806** in band; 0 unmapped.
- In band: IT 38, Healthcare 67. Excluded names present: INDRAMEDCO, KRSNAA, ORCHPHARMA, SHILPAMED, SYNGENE. **Eligible: 100.**

**Walk:**
| # | Symbol | Result |
|---|---|---|
| 1 | DCAL | **skip (d)**: Q2 FY27 SUE −1.94 → quintile 1, event 13-Nov-2026. It passed a–c (Ind-Ra downgrade to A/Negative is not INC; pledge 8.4%). |
| 2 | ZOTA | **skip (d)**: SUE −0.75 → quintile 1, event 28-Oct-2026. |
| 3 | **VIYASH** | **subject** (a–e pass; §1) |

**Skips: 2, both from the PEAD avoid window.** In the first 15 names, 5 of 15 sit in quintile 1, so the avoid window binds often in this frame.

**Frame note (lesson candidate):** the subject's identity changed 11 months ago. SeQuent (animal health, ~₹1,400 cr revenue) absorbed
Viyash Life Sciences + Symed (human APIs) under common control. Consequences:
- The listed symbol's 10-year history (EPS, P/E band, ROIIC) describes a different business.
- The PEAD SUE compares merged Q2 FY27 with pre-merger Q2 FY26, so the quintile-5 "beat" is mostly the merger.

Scoreability rule (a) passed it correctly, because the entity survives. The protocol has no rule yet for "identity-changing merger in the last 2 years".

## 0b. Rule zero: edge before depth
1. **What the market knows.** An integrated API + animal-health formulation platform: TTM revenue ₹3,713 cr; pre-ESOP EBITDA ~21%; net debt ≈ 0; 16 plants (10 USFDA-approved).
   - The stock trades at 43x reported TTM EPS but 19.4x consensus FY28 EPS (4 analysts; Yahoo, 26-Nov-2026). Most-asked call questions (14-Nov-2026): US
     de-growth; capex; ESOP path; Carlyle exit; 20–25% growth possibility; API margins/raw materials.
   - Promoter Carlyle sold ~12% in Jul–Sep 2026.
2. **The variable that matters:** how much of the TTM depression is temporary, and what growth/ROIIC the remainder can earn.
   - Temporary items: merger ESOP (FY27 ~₹148 cr vs ~25 steady) and acquired-intangible amortisation (~₹100 cr FY26 → ~38 FY27 → 0).
   - The other question is whether ~20% growth can be sustained with ROIIC above CoE while the PE owner exits.
3. **Layers:** L2 (core vs temporary costs, minorities, dilution), L5 (warrants, ESOP, PE exit, votes), L4/L6 (US erosion, USFDA, KSM sourcing).
   Honest limit: no information edge on FDA inspections or the Carlyle timetable. The analyst count (4) is higher than in prior draws (0–1), so there is less room for a depth edge.

---

## 1. S2 checklist (disqualifiers v3; filled before L1, every rule dated)
| Rule | Status | Evidence (source, date) |
|---|---|---|
| H1a fake cash | **pass** | Cash ₹492.5 + bank 12.3 vs borrowings ₹531.0 at 30-Sep-2026 `[XBRL]`. Mar-2026: 255.8 vs 435.8 `[AR26]`. Cash is spread over 20 subsidiaries in 9 countries; no idle-cash pattern. |
| H1b implausible economics | **pass** | Gross margin 53.7–55.5%, pre-ESOP EBITDA 21.0–21.7% for 4 quarters `[DECK]`; peers' ROCE 12–27% `[SCR]`. Appco margin spike is explained by a CGT-exclusivity launch `[CALL]`. |
| H1c unverifiable profits | **pass** | 250+ customers, **none ≥10% of revenue** `[AR26 risk note]`; public FDA inspection record; two rating agencies. |
| H2 auditor | **pass (EoM)** | S R B C & Co LLP: unmodified FY26 opinion with an EoM on common-control restatement (Note 57). KAMs: goodwill ₹868.7 cr and DTA ₹83.4 cr. Unmodified-opinion declarations in the FY25 and FY26 XBRL. |
| H3 rating | **pass** | ICRA **AA-/Stable** (22-Apr-2026). India Ratings A/Positive → **AA-/Stable** (30-Apr-2026), then withdrawn at the company's request (22-May-2026). These are withdrawals, not INC. |
| H4 pump | **pass** | Main board; 6-month ADV ₹91 cr mean / ₹56 cr median `[YH]`; 4 analysts. |
| H5 RPT leakage | **pass (watch)** | §6. |
| Exit triggers | **none** | Results on time (13-Nov-2026); no restatement beyond the scheme-mandated one. |
| G pledge | **clear** | Pledge API, SHP 30-Sep-2026: promoter shares pledged 0 of 217.9 m. |
| G accounting trouble | **watch** | SEBI administrative warning (1-Jul-2026) to the former CS on the insider-trading SDD (Jun–Oct 2024): procedural. ₹5.6 cr customer-claim provision for prior-year shipments in Q1 FY27 `[DECK]`. |
| G dilution | **watch** | 43.69 cr shares (Mar-2026) → 44.16 cr (Sep-2026). Plus MD warrants (2.03 cr at ₹181.94) and ~2.1 cr options [EST] ≈ 9% potential. |
| G solvency | **clear** | solvency_screen 26-Nov-2026: 0 flags, ICR 6.1x FY26; TTM 8.3x. |
| Q CFO/PAT | watch | FY26 1.44x `[SCR]`; H1 FY27 1.11x `[XBRL]`. Receivable days ~110, up from 98 in FY25. |
| Q other income | ok | 11% of pre-exceptional PBT. |
| **Pharma: USFDA status** | **clear (partly single-source)** | Import Alert 66-40 page `[FDA]`, 26-Nov-2026: no Viyash/SeQuent/Symed/Appco/Alivira/Vindhya/Vandana entry. Web search found no warning letter. Clean EIR for the US facility, EU-GMP and WHO-Geneva audits "without major observations" `[CALL 14-Nov]` (company source). A third-party FDA-records site lists a 25-Apr-2025 inspection and a 2-observation 483 at the Viyash Life Sciences Panvel API site, classification not seen `[WEB, single-source]`. The FDA dashboard was not queried (login). |

**Survival cap / L39:** pledge 0%, ICR 8.3x, so neither flag fires.

**Stage-3 signals.**
- **PEAD:** Q2 FY27 SUE **+3.23 → quintile 5** (event 13-Nov-2026). The comparability caveat in §0 applies.
- **Credibility:** **not scored** (n = 4 resolved promises < 5; L49). Light ledger:
  - Met (3): FY27 amortisation "~₹35 cr" (actual ~38); "API revival in Q2" (+8% q/q, +12% y/y); "₹800 cr EBITDA, internal target FY27" (TTM pre-ESOP 798).
  - **Missed (1):** CFO, Aug-2026: ESOP for "Q2, Q3 and Q4 … about Rs. 40 crores" in total. Nov-2026: Q2 alone 42.1, FY27 ~148–149, so Q2–Q4 ≈ ₹122 cr (~3x).
  - Open: FY27 growth guide moved from "13–14%/mid-teens" (Aug) to "20%+" (Nov).
  - Same pattern as L26 at the operating level (numbers met). The miss is on the one line the company's "adjusted PAT" removes.

---

## 2. Map (L1)
| Business (Q2 FY27 sales `[DECK]`) | ₹ cr | Share | y/y | Unit / notes |
|---|---|---|---|---|
| Formulations: Europe | 186 | 19% | +22% | Alivira animal health: Spain (Karizoo 60%), Belgium/NL, Germany (Bremer), Sweden; BioForLife Italy from Q3 FY27 |
| Formulations: Emerging markets | 203 | 21% | +39% | Turkey (Provet, Topkim; Ind AS 29 hyperinflation), Brazil, Mexico; Vietnam entity registered |
| Formulations: India | 50 | 5% | +39% | own + distributed (BI companion-animal products) |
| Formulations: USA | 119 | 12% | **−11%** | Appco Pharma LLC (60%): human generics; exclusivity product eroded |
| APIs (human + animal) | 415 | 42% | +12% | 10 API sites (Hyderabad, Vizag ex-Mylan, Mahad, Vizag), 110+ APIs, CDMO |
| Other / Ind AS 29 | 14 | 1% | | |

- **Value chain:** KSMs/intermediates → API (own and third-party customers; backward integration for "key formulation products") → formulations (vet in EU/EM; human generics in US via Appco) → distributors/vets/pharmacies.
- **Peers with the same unit:** Granules, Neuland, Aarti Drugs, Solara (APIs). There is no clean listed Indian animal-health peer.
- **Flags:** cyclicality none (the API price cycle is mild); holdco none. The NCI structure is material: 40% of Appco and 40% of Karizoo belong to others.

## 3. Financials re-derived (L2) `[XBRL; SCR checks]`
| Quarter (merged entity) | Revenue | Resolver OPM | ESOP | D&A | PBT pre-exc. | Exceptional | PAT (group) | Owners | NCI |
|---|---|---|---|---|---|---|---|---|---|
| Q3 FY26 | 858.41 | 20.5% | 7.9 | 58.53 | 114.33 | −41.26 | 48.52 | 38.44 | 10.08 |
| Q4 FY26 | 919.96 | 20.0% | 5.3 | 60.41 | 125.24 | 0 | 66.38 | 52.11 | 14.27 |
| Q1 FY27 | 946.36 | 18.8% | 24.6 | 61.77 | 112.41 | 0 | 79.29 | 65.87 | 13.42 |
| Q2 FY27 | 987.94 | 16.7% | 42.1 | 45.33 | 117.68 | 0 | 84.65 | 76.17 | 8.48 |
| **TTM** | **3,712.67** | 18.9% | **79.9** | **226.04** | **469.66** | −41.26 | **278.84** | **232.59** | 46.25 |

- Screener quarterlies match XBRL to the crore (e.g. Q2 FY27 sales 988, OP 165, PAT 85).
- FY26 (restated, merged): revenue 3,420.31; PBT 349.02 after −44.21 exceptional; PAT 224.65; EPS 4.09. FY25 restated: revenue 3,007; PAT 15.8 after ₹81.6 cr exceptionals `[DECK]`.
- **Pre-merger history** (SeQuent FY15–FY24: revenue 443 → 1,370, three loss years) is a different business. It is not used for bands or ROIIC.
- **L44 core EPS.** Exceptional (−41.26) and other income (50.0) are stripped once from reported owners' PAT (worksheet inputs `exceptional_items_cr`, `other_income_cr`, × 0.86). Core P/E is 48.7x vs 47.6x trailing on the fully diluted share count, so L44 barely moves this one.
- **The bigger hidden items are temporary operating costs, not exceptionals:**
  - Excess ESOP: TTM ₹79.9 cr vs ~25 steady state. Guide: FY27 ~148, FY28 ~32 `[CALL]`.
  - Acquired-intangible amortisation inside D&A: ~₹84 cr TTM. Q1 FY27 25, Q2 8.9, Q3 ~4, then nil `[CALL]`. Visible in D&A 61.8 → 45.3.
  - Together ~₹139 cr pre-tax ≈ ₹2.1 per diluted share after tax and minorities.
  - The ESOP is a real cost; its dilution is already in the 48.33 cr fully diluted share count.
- **Bottom-up FY27/FY28 [EST]:**
  - FY27 H2: revenue ~2,170 (to hit the "20%+" guide incl. BioForLife); pre-ESOP EBITDA 21.5%; ESOP 80; D&A ~90; interest 26; OI 20 → PBT ~291 → group PAT ~209 → owners ~182. **FY27 EPS ≈ 7.35 basic.**
  - FY28: revenue +15% → ~4,720; pre-ESOP EBITDA ~1,015; ESOP 32; D&A ~185 → owners' PAT ~500. **EPS ≈ 11.3 basic / 10.3 fully diluted.**
- **L42 group ROIC first.** TTM EBIT ex OI 477.2 × 0.72 = NOPAT 343.6.
  - On Sep-2026 invested capital ₹3,473 cr (owners' equity 3,164.7 + NCI 228.5 + net debt 26.1 + leases ~54): **9.9%**.
  - Ex goodwill (₹877 cr): 13.2%. With ESOP/amortisation normalised: ~12.8%.
  - Group ROIC sits around the 12.5% CoE. The company's "ROCE ex goodwill 20%" `[CALL]` is pre-tax and pre-ESOP.
  - ROIIC FY25 → TTM ≈ 52% is a merger/turnaround window and is not used (L38 analogue); 15% [EST] is used instead.
- **Concentration:** no customer ≥10% `[AR26]`. Appco contributed ₹88 cr of FY26 entity-level profit (39% of the entity sum before consolidation adjustments; AR26 note 49): the US business is the profit pocket that has faded.
- **Minorities:** NCI took 16.6% of TTM PAT and 13.4% of H1 FY27. Management plans to "acquire remaining stake from minority" after the acquisition phase `[CALL 14-Nov]`, a future cash call.

## 4. Unit economics (L3) — partial
- **Revenue per site:** 16 plants → ~₹232 cr per site TTM [EST].
- **Per India head:** 4,131 people in the listed entity (2,568 employees + 1,563 workers, BRSR FY26).
- **New capacity:** "128 KL" additional API capacity approved at Viyash-IV, Nalgonda. Capex is not split by block, so payback **cannot be rebuilt two ways** (gap).
- **Companion-animal plant (Ambernath):** commissioning Q1 FY28; the launches it serves are 2029+ `[DECK; CALL]`.
- **Acquisition unit:** BioForLife at EUR 16.976 m (~₹170 cr) for 85–90 products with 85% vet-clinic coverage in Italy. Revenue is not disclosed, so the price/sales multiple is unknown (gap).
- **US unit (Appco):**
  - One CGT-exclusivity product: ~USD 5 m in 45 days at 90%+ GM (Q2 FY26).
  - After that, quarterly US revenue fell ₹126 → ~110–115 cr, with ~50% share retained on that product `[CALL]`.
  - MD: launch price erosion ~40%, "even 60%" at 10–15% share is attractive. These are company statements; no IQVIA data was available.

## 5. Cost drivers (L4), ranked by weight (TTM, % of revenue) `[XBRL]`
| Line | % rev | Physical driver | Sensitivity |
|---|---|---|---|
| Materials (consumed + traded + inventory change) | ~46% | KSMs, solvents, intermediates; China share **not disclosed** | GM −180 bps y/y in Q2 FY27, partly raw material/solvents (MD: "around 0.3–0.4%" impact from price variance). 100 bps of material cost = ₹37 cr EBITDA ≈ 5% |
| Employees (incl. ESOP) | ~17% | 4,131 India staff in the listed entity + EU/Turkey/Brazil/US; attrition 16.5% (employees) / 8% (workers) FY26, down from 24.2% / 16% `[AR26 BRSR]` | ESOP alone = 4.3% of Q2 revenue; it falls to ~0.6% by FY29 on guidance |
| Other expenses | ~18% | freight, power, R&D (animal-health R&D "ramped up three times"), regulatory filings | n/a |
| D&A | ~6% | PP&E ₹1,063 cr + ending intangible amortisation | −₹84 cr amortisation = +2.3 pts EBIT margin |

US tariff / Section 232 exposure: US formulations are 12% of sales, made by Appco (US plant, so tariff-exempt) plus APIs shipped to US customers.
Pharma tariff headlines in the news run (§6.5) are sector items, not company-specific.

## 6. Governance, ownership, related parties (L5)
### 6.1 Owner, MD and the capital structure
- **Promoter:** CA Hull Investments / CA Harbor (Carlyle). Promoter holding was **61.31% at 30-Jun-2026 and 49.24% at 30-Sep-2026** (NSE SHP); the call corroborates "a block of around 11%". Carlyle entered 2020–21; the analyst on the call cited a 7–8-year fund life.
- **Carlyle exit:** MD: "next 12 months, I don't see anything"; any exit would go to "highly credible mutual funds" `[CALL 14-Nov]`. This is a supply overhang with a stated timetable we can score (call 5).
- **Nominee directors:** Neeraj Bharadwaj and Anuj Poddar draw no fees. Two other Carlyle-side directors (Kausche, Andrews) resigned 30-Mar-2026, and the covering letter was mis-dated "2025" (clarified 31-Mar).
- **MD/Group CEO Dr Haribabu Bodepudi** (founder of Viyash Life Sciences):
  - Holds **2,03,41,257 warrants** at ₹181.94 (25% paid = ₹92.5 cr). The remaining ₹277.6 cr is due on conversion within 18 months of allotment (≈ Jun-2027) `[AR26]`.
  - The warrants are in the money at ₹228.88 (+26%).
  - Remuneration 116.7x the median employee (FY26 part-year as MD) `[AR26]`.
- **ESOP:** 1.32 cr options outstanding at 31-Mar-2026 (WAEP ₹86 and ₹58.5 plans) plus 1.3 cr granted in Q1 FY27 `[AR26; CALL Aug]`. ESOP allotments run almost monthly (8 Reg-30 items Apr–Nov 2026).

### 6.2 Vote results — dissent net of promoter votes (L42) `[NSE scrutiniser reports]`
| Meeting / item | Against | Non-promoter votes cast | Against % of non-promoter votes |
|---|---|---|---|
| AGM 11-Aug-2026, #6 new Articles of Association | 6,375,107 (institutions 30.8% against) | 317,141,060 − 267,840,334 = 49,300,726 | **12.9%** |
| AGM #2 re-appoint MD | 421,263 | 34,321,373 | 1.2% |
| Postal ballot Jun-2026, appoint WTD & CEO-Animal Health | 3,742,825 | 42,596,248 | **8.8%** |

Non-promoter turnout at the AGM was ~29% (49.3 m of ~169 m public shares). The AoA item draws institutional dissent; its content was not read (open item).

### 6.3 RPTs
No material RPTs with promoter entities were found in the AR26 governance pages read. The related-party note was not fully tabulated (gap; L5 says the RPT table is never skipped).
**Partial:** the promoter is a PE fund with no operating businesses in the group, and the parent-take table is n/a. The cash flows to watch are:
- MD warrants (cash in ₹277.6 cr);
- ESOP;
- dividends to NCI (₹4.9 cr FY26 `[AR26 cash flow]`);
- future minority buy-outs.

### 6.4 L40/L41 — government inputs and missing external facts
- No land/licence concession found. USFDA/EU-GMP approvals are regulatory permissions over 10 sites (no single-site dependence disclosed).
- State law: Telangana/AP host most API sites; no state-specific levy was identified.
- Turkey: hyperinflation accounting (Ind AS 29) affects revenue (+₹2–3 cr/qtr adjustment) and goodwill (+₹21.6 cr FY26).
- **Material-fact check:** the Carlyle block sale is not mentioned in the Q2 FY27 deck; it surfaced only through the SHP and an analyst question. Disclosure flag (mild).

### 6.5 News (run 26-Nov-2026, `tools/news/news.py --tickers VIYASH --since 30d`; VIYASH added to watchlist.csv) and L50 verification
55 items, 17 flagged material. Most "policy" matches are other companies' FDA items (Natco, Granules, Aarti Drugs, Marksans, Zydus) or US-tariff opinion pieces: not about Viyash.
| Item | Verdict (L50) | Primary source / verb |
|---|---|---|
| "Viyash acquires BioForLife for EUR 16.975 m" (22-Nov-2026 feed) | **confirmed, stale** (closed 1-Oct-2026; the feed resurfaced it) | Reg-30 21-Jul-2026 "executed a Sale and Purchase Agreement", EUR 16.976 m; Reg-30 1-Oct-2026 "has completed the acquisition" |
| "Targets Rs 150 crore annual capex for two years" (17-Nov) | **confirmed** | CALL 14-Nov: "INR150 crores, INR170 crores level … both growth capex as well as operational capex" |
| "Q2 PAT up 38.7% to Rs 76.17 cr" (14-Nov) vs "net profit up 16.1% to ₹847 m" (13-Nov) | **both true, different lines** | XBRL: owners' PAT 76.17 (+38.7% implies a restated merged Q2 FY26 owners' PAT of ~54.9, not shown in the filings read); group PAT 84.65 vs merged 72.9 = +16.1% (DECK). Owners vs group lines; the owners' growth is flattered by lower NCI (Appco). Use both, labelled. |
| "Growing fast, why is the stock falling?" (26-Nov) | opinion; not used | — |
| RTA office change (24-Nov) | confirmed, immaterial | Reg-30 24-Nov-2026 |
No item was turned into an event record except BioForLife (primary Reg-30, already in the card).

## 7. Scuttlebutt plan (L6; not executed — the user's ground checks)
1. **FDA:** query the FDA Data Dashboard (inspection classifications) for FEI 3003908605 (Viyash Life Sciences) and the Symed/Vizag FEIs; confirm VAI/NAI for the 2025 Panvel 483.
2. **US erosion:** Appco's exclusivity product — identify the molecule (not named) and check the competitor count in the FDA ANDA approvals list.
3. **KSM sourcing:** ask IR for the share of KSMs from China (not disclosed); check DGCIS import data for the top 3 APIs' intermediates.
4. **Carlyle:** watch NSE bulk/block deals and SAST filings for CA Hull / CA Harbor monthly.
5. **Companion animal:** vet-clinic checks in Italy/Spain on BioForLife/Alivira brands; Ambernath plant status (MPCB consent).

## 8. Override (L7) and valuation (L8)
### 8.1 Override table
| Flag | Verdict | What changes my mind | Review |
|---|---|---|---|
| Group ROIC ~10% (13% ex goodwill) vs CoE 12.5%; no valid ROIIC window | open | FY28 after-tax ROIC ≥ 12.5% | 2028-05-31 |
| 47.6x TTM / ~21–22x our FY28 diluted / 19.4x consensus FY28; base IRR 8.4% | open | FY27 PAT ≥ ₹400 cr and FY28 growth guide ≥ 18% | 2027-05-31 |
| Guidance quality: ESOP guide missed ~3x; "adjusted" headline metrics | open | Q3 FY27 ESOP ₹35–45 cr; FY28 ESOP ≤ ₹40 cr | 2027-02-28 |
| Carlyle exit overhang (61.3% → 49.2%) | open | Promoter ≥ 45% at the Mar-2027 SHP | 2027-04-30 |
| US/Appco erosion (−11% y/y) | watch | US ≥ ₹110 cr/qtr in Q3–Q4 FY27 | 2027-05-31 |
| KSM/China dependence undisclosed | watch | disclosed in AR FY27 | 2027-09-30 |
| Goodwill ₹877 cr incl. Turkey (hyperinflation); DTA KAM | watch | no FY27 impairment | 2027-05-31 |
| "43x looks absurd": ~₹139 cr of temporary costs | explained (bad-looking, partly benign) | — | — |
| Net debt ~0, AA- ×2, no customer >10%, clean US EIR (good) | confirmed | — | — |

**Result: 4 open soft flags, so a variant view is written (card §2). The variant view is "no claimable mispricing".**

### 8.2 What the price implies (`tools/valuation/live/VIYASH_worksheet.md`, worksheet v1.3)
Scenarios were written before the run. Tails start from the class base rates; raw blow-up is 7%.
- **Snapshot (fully diluted 48.33 cr shares [EST], attributable ×0.86):** mcap 11,062; net cash 380 (incl. warrant/option money [EST]); EV 10,682; P/E 47.6; EV/EBITDA 17.7; FCF yield 1.8%.
- **Base-case IRR 8.4%** vs CoE 12.5%. Reverse DCF: no tested growth path reproduces the price at the 12.5% CoE; it needs a 35% year-10 NOPAT margin on the base growth path.
  DCF value per share: bear 52 / base 89 / bull 127 (probability-weighted 84). At a 12.5% CoE the cash flows do not carry the price, so every scenario above ~0.6x is the exit-P/E bet (L21).
- **Exit-multiple bet:**
  - Exits used 15/24/32x vs DCF-consistent 12.7/14.8/17.2x; own median n/a (n = 1, FY26 44.7x on merger-depressed EPS).
  - EV of the 5-yr multiple: **0.97x** at the used exits, 0.61x at DCF exits.
  - Peers: Granules 32.5x, Neuland 59.9x, Aarti Drugs 19.5x, Solara 62.6x (median 46.2x incl. Solara; 32.5x for the three earning peers).
- **Temperature:** NORMAL vs peers (1.03x the 46.2x median); INSUFFICIENT own history.
- **Run log (disclosed):** a run-2 sensitivity started the margin at the 11.9% "economic" margin. EV *fell* to 0.85x, because the worksheet grows EPS from the depressed base EPS (4.81) with NOPAT.
  - Neither run can express a step-up in FY28 EPS from cost roll-off.
  - Our bottom-up FY28 diluted EPS (~10.3) is reached only in worksheet year 5.
  - The written run 1 is adopted; this is a worksheet limitation (lesson candidate).
- **Consensus cross-check (L47; `research_notes/Consensus/snapshot_2026-11-26_VIYASH.json`, Yahoo, 4 analysts):**
| | FY27 EPS | FY28 EPS | P/E at ₹228.88 |
|---|---|---|---|
| Consensus mean (range) | 7.43 (6.5–9.2) | 11.83 (10.2–14.1) | 30.8x / 19.4x |
| Ours, basic shares [EST] | ~7.35 | ~11.3 | 31.1x / 20.3x |
| Ours, fully diluted [EST] | ~6.8 | ~10.3 | 33.7x / 22.2x |
| Worksheet base path (diluted) | — | year-5 EPS ~10.3 (FY31) | — |
  - **Adjusted vs reported:** the company's headline is "adjusted PAT with normalised ESOP" (Q2 FY27 ₹110 cr vs reported ₹85 cr). The consensus high end (9.2 for FY27) is likely on that basis. Yahoo does not say which; I treat consensus as possibly adjusted, so it is not like-for-like.
  - Our bottom-up is within ~4% of the consensus mean on basic shares. The disagreement is not the near-term EPS. It is (i) dilution (~9%) and (ii) how long ~15–20% growth at ROIIC > CoE lasts, which is the exit multiple.
  - The tool fails silently on `VIYASH.NS` on some calls (empty result; `.BO` worked first, then both). It needed 3 tries: a tool-reliability note.

### 8.2b Why is it not cheaper / is it a trap?
- The market pays ~20x consensus FY28 for an AA-rated, net-cash API/animal-health platform growing high-teens. That is in line with API peers. The 43x TTM optics are mostly accounting.
- Not a fraud-type trap: clean auditor, diversified customers, no FDA import alert found.
- The plausible traps are ordinary:
  - supply from a PE seller in year 5–6;
  - a management team that steers to "pre-ESOP / adjusted" metrics and just missed its own ESOP guide 3x;
  - US generic erosion of the profit pocket (Appco).

### 8.3 Variant perception
None claimable. Our near-term EPS agrees with consensus. What we found that a headline screen misses:
- the ~9% dilution (warrants + options);
- the ESOP guidance miss;
- the Carlyle block;
- the identity change that makes every historical band meaningless.

These are reasons for caution, not for a price view.

### 8.4 Decision card (`tools/decision/live/VIYASH_card.md`, **card v1.5**)
**Rule output: size 0.** EV 1.07x anchored (raw 0.97x) vs hurdle 1.76x.
- **Gates:** S2 passed (7/7); PEAD clear (Q5); survival clear; 4 open soft flags with a variant view.
- **Probabilities (5 yrs):**
  - P(≥3x): model 2.0% vs base 21.3%.
  - P(≤0.5x): model 26.8% vs 11.3% (anchored 19.0%).
  - P(blow-up): 7% vs 15.4% (anchored 11.2%).
- The card printed the **anchoring-lowered warning** on P(≤0.5x). Our raw tail rests on the entry multiple (47.6x diluted TTM, ~22x our FY28) and a 15x bear exit, not on company-specific legal evidence. The anchored figure is kept for the gate as the rule says; both are scored.
- **9 of 9 live cards are size 0.**

## 9. Forward calls (live; tags paper-call, deepdive-generated, live, india, sector-pharma; specs in `tools/scoreboard/specs.json`)
| id (thesis:paper-call:VIYASH:…) | Claim | P | Base | Base reasoning | Resolver |
|---|---|---|---|---|---|
| q3fy27-revenue-1050cr-plus | Q3 FY27 consolidated revenue ≥ ₹1,050 cr | 0.40 | 0.33 | needs +6.3% q/q; q/q growth in the last 4 merged quarters +1.0/+7.2/+2.9/+4.4% → 1 of 4 ≥ 6.3% → Laplace 2/6 | india_fin structured |
| q3fy27-opm-17p5pct-plus | Q3 FY27 OPM (resolver basis, ESOP inside) ≥ 17.5% | 0.40 | 0.67 | last 4 quarters 20.5/20.0/18.8/16.7% → 3 of 4 → Laplace 4/6 | india_fin structured |
| fy27-revenue-4100cr-plus | FY27 consolidated revenue ≥ ₹4,100 cr (≈ the "20%+" guide) | 0.35 | 0.40 | our ledgers: revenue/order promises met 6 of 15 (L26/L49) | india_fin structured |
| fy27-net-profit-375cr-plus | FY27 consolidated group PAT (incl. NCI) ≥ ₹375 cr (≈ consensus FY27 EPS 7.43) | 0.45 | 0.50 | coin flip around consensus | india_fin structured |
| promoter-45pct-plus-mar27 | Promoter holding ≥ 45.0% at the 31-Mar-2027 SHP | 0.75 | 0.60 | [EST] a PE promoter that just sold 12% in year 5–6; no measured base rate | nse_pledge structured |
| beats-nifty500-to-sep27 | Total return beats Nifty 500 from 25-Nov-2026 to 30-Sep-2027 | 0.42 | 0.50 | coin flip | price_relative structured |
| card 5y-ge3x / le0p5x / blowup | from the card | 0.020 / 0.268 / 0.07 | 0.213 / 0.113 / 0.154 | class base rates | human |

Reasoning:
- Q3 revenue includes a first quarter of BioForLife (~₹25–35 cr [EST]).
- Q3 OPM bears ~₹40 cr of ESOP (CFO guide), ~4 pts of revenue, against a 21% pre-ESOP margin, so ~17%.
- FY27 at 4,100 needs H2 +22% y/y vs H1 +17.8%.
- Group PAT 375 needs H2 ~211 vs our bottom-up ~209, so close to a coin flip, with a slight lean to "no" because the ESOP guide has already moved up once.

## 10. What this run taught the method (lesson candidates)
1. **Identity-changing mergers break the history layer.** A common-control merger 11 months before the draw left the listed symbol with no usable 10-yr P/E band, ROIIC window or PEAD comparator (SUE +3.23 was the merger). Add an S0/L2 rule: if a scheme changed >50% of revenue in the last 2 years, mark own-history and PEAD "not comparable" and use peer bands and restated pro-forma data only.
2. **The worksheet cannot express temporary cost roll-off.** Merger ESOP and acquired-intangible amortisation (~₹139 cr pre-tax, ~₹2.1/share) depress the base EPS. Raising the starting margin *lowers* EV because EPS grows from the depressed base. A `base.eps_normalised_bridge` or per-year margin override would let FY28 step up. Until then, show the bottom-up next-2-year EPS beside the worksheet (done here).
3. **L44 extension: "core" also needs a temporary-cost line, not just exceptionals.** Exceptionals and other income moved P/E only 2%; the temporary ESOP/amortisation moved it ~40%. Record them separately, never inside `exceptional_items_cr` (that would double-subtract and would also hide a real cost).
4. **Management "adjusted" metrics deserve a credibility check of their own.** The one cost line the company excludes was the one it forecast worst (ESOP guide missed ~3x within a quarter). Add "guidance on excluded items" as a ledger category.
5. **Minorities and dilution belong in the base.** NCI took 13–17% of PAT, and warrants + options add ~9% shares. Both are absent from the trailing P/E that screens show (43x basic vs 47.6x diluted attributable).
6. **PEAD avoid window binds often in pharma/IT** (2 of 3 walked; 5 of the first 15 in quintile 1). Expected given post-results timing, but worth tracking as a frame-level count.
7. **Consensus tool reliability:** `consensus.py` returned empty results on the first calls (no error text); a retry worked. Log the retry count in snapshots.
8. **9/9 live cards size 0;** here the base IRR (8.4%) is below CoE again, consistent with L43.

## 11. Open items
- FDA Data Dashboard classification for the Apr-2025 Panvel inspection (483, 2 observations, single-source).
- KSM China share; the Appco exclusivity molecule and competitor count.
- AR26 related-party note: full RPT table (not tabulated this run); the content of the 2026 AoA change that drew 31% institutional dissent.
- Exact outstanding options and strikes after the Q1 FY27 grant (dilution [EST]).
- Carlyle remaining stake path; MD warrant conversion (~Jun-2027, ₹277.6 cr inflow).
- BioForLife revenue and margin (first consolidated in Q3 FY27).

## Sources
- AR FY26: https://nsearchives.nseindia.in/annual_reports/AR_29856_VIYASH_2025_2026_A_10469798_17072026165453.pdf
- Q2 FY27 XBRL (consolidated): https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1757557_13112026055107_WEB.xml ; Q1 FY27 …1711894_11082026055628…; Q4 FY26 …1669663_19052026101914…; Q3 FY26 …1619650_05022026091714…
- Q2 FY27 deck: https://nsearchives.nseindia.in/corporate/SEQUENT2_13112026184257_SE_Intimation_Investor_Presentation.pdf ; Q4 FY26 deck: https://nsearchives.nseindia.in/corporate/SEQUENT1_19052026191045_Investor_Presentation.pdf
- Transcripts: https://nsearchives.nseindia.in/corporate/SEQUENT2_17112026182841_SE_Intimation_Earnings_Transcript.pdf ; https://nsearchives.nseindia.in/corporate/SEQUENT1_16082026111555_Transcriptsigned.pdf ; https://nsearchives.nseindia.in/corporate/SEQUENT1_22052026104104_SE_Intimation_Earnings_Transcript.pdf
- AGM 2026 scrutiniser: https://nsearchives.nseindia.in/corporate/SEQUENT1_11082026203053_AGMVSLScrutinisersReportsigned.pdf ; postal ballot Jun-2026: https://nsearchives.nseindia.in/corporate/SEQUENT1_29062026154542_SEIntimationVotingResultsJune2026.pdf
- Ratings: https://nsearchives.nseindia.in/corporate/SEQUENT1_22042026215035_VSLratingletter.pdf ; https://nsearchives.nseindia.in/corporate/SEQUENT1_30042026194448_SEintimation.pdf
- SEBI warning: https://nsearchives.nseindia.in/corporate/SEQUENT_07072026215717_SEintimationWL.pdf
- BioForLife: https://nsearchives.nseindia.in/corporate/SEQUENT1_21072026173844_SE_Intimation.pdf ; https://nsearchives.nseindia.in/corporate/SEQUENT1_01102026175658_VSL_Reg_30_Completion_of_acquisition.pdf
- Scheme/NCLT: NSE announcements 18–28-Nov-2025, record date 08-Dec-2025; name change 09-Jan-2026.
- FDA Import Alert 66-40: https://www.accessdata.fda.gov/cms_ia/importalert_189.html (fetched 26-Nov-2026; no match)
- Third-party FDA record (single-source): https://www.globalkeysolutions.net/records/483/viyash-life-sciences-private-limited/8542a8db-79bd-4f89-928b-23e99d99d6a3
- Bhavcopy: https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_25112026.csv
- screener: https://www.screener.in/company/VIYASH/consolidated/ (and GRANULES, NEULANDLAB, AARTIDRUGS, SOLARA)
- Consensus: `research_notes/Consensus/snapshot_2026-11-26_VIYASH.json`
