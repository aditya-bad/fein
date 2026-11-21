# Cummins India (NSE: CUMMINSIND): practice deep dive #2 at "security-guard depth"

**Date:** 2026-11-21 · **Purpose:** the second test of `deep_dive_protocol.md`, this time on a **manufacturer** (run #1, Vishal Mega Mart, was a retailer). The aim is to improve the protocol.
**This is test material (lesson L9). There is no buy/sell/watchlist verdict and none should be read in.** Research, not SEBI-registered advice.
**Open paper call on this stock:** `thesis:paper-call:CUMMINSIND:q3fy27-opm-17pct-plus` (P = 0.38 that Q3 FY27 standalone OPM ≥ 17%). This file does **not** change that call. Relevant facts are noted in §8.

Every number carries a source tag. Every estimate shows its method.
- `[AR26]` = FY26 Annual Report incl. BRSR and 65th AGM notice (NSE, 09-Jul-2026), audited standalone notes (n.26 revenue, n.31 other expenses, n.41 related parties)
- `[Q2R]` = Q2 FY27 standalone results (NSE, 04-Nov-2026) · `[PR-Q2]` = Q2 FY27 press release · `[PR-FY26]` = FY26 press release (27-May-2026)
- `[CC-Q2FY27]` = call of 16-Nov-2026 (transcript filed 20-Nov-2026) · `[CC-Q1FY27]` = 06-Aug-2026 · `[CC-Q4FY26]` = 29-May-2026 · `[CC-Q3FY26]` = 05-Feb-2026 · `[CC-Q2FY26]` = Nov-2025 · `[CC-Q2FY25]` = 08-Nov-2024 · `[CC-Q1FY25]` = 07-Aug-2024
- `[PB-Nov26]` = postal ballot notice, 06-Nov-2026 (new MD + extra RPT limit with Cummins Inc)
- `[SCR]` = screener.in standalone pages, fetched 21-Nov-2026 (CUMMINSIND, KIRLOSENG)
- `[WEB]` = secondary web summaries, single-source unless stated
- `[EST]` = my estimate, with the method shown in the same row

Price/valuation snapshot `[SCR]` (21-Nov-2026), for context only: CMP ₹4,100, market cap ₹1,13,652 cr, trailing P/E 52.0, 52-week high/low ₹6,143/₹3,883 (now 33% below the high), dividend yield 1.6%, ROCE 41.6%. Kirloskar Oil Engines (KOEL): CMP ₹1,706, market cap ₹24,837 cr, P/E 57.5, ROCE 18.7%.

---

## 0. Edge question first (rule zero)
1. **What the market already knows.** On the Q2 FY27 call, 11 analysts asked about five things: (a) whether gross margin has bottomed and how fast price hikes catch up, (b) data-centre (DC) demand and QSK60/QSK95 supply, (c) DC share of power-gen sales and growth outside DC, (d) export geography, (e) industrial sub-segments. Only **one** question touched the parent's cost take, and only by accident: "Any one-offs in other expenses?" The CFO answered: "a true-up on corporate cost allocations, the management cross charges" `[CC-Q2FY27]`.
2. **The variable that would change value most if we knew it better than consensus.** The **steady-state margin**, which has three parts. (i) Commodity pass-through lag. Everyone models this. (ii) The DC share, and whether Cummins keeps it while HHP engines are allocated globally. Everyone asks about this. (iii) **How much of the gross profit the parent takes through royalty, support services, transfer prices and dividends, and how that changes at the royalty renewal on 31-Mar-2027.** Almost nobody models this.
3. **The layers most likely to reveal it.** L5 (the RPT note and the AGM RPT approval tables, which give *prices*, not just amounts) and L6 (GOEM, dealer and installer price checks, which show whether price hikes stick).

For a 51%-owned MNC subsidiary, the edge question is "who gets paid before minority shareholders". It is not "what is the next quarter's margin".

---

## 1. Map (L1): what is the unit?

### 1.1 The business in one paragraph
Cummins India Ltd (CIL) designs, makes, sells and services diesel/gas engines (and some gensets) from 16 hp to 4,500 hp. The parent, **Cummins Inc. (CMI), holds 51.00%** and has done so since at least 2017 `[SCR]`. CIL does **not** make most gensets itself. It sells engines to **three Genset OEMs (GOEMs, e.g. Sudhir Power and Jakson)**, which add an alternator, enclosure and controls. It also sells to industrial OEMs (excavators, compressors, rail, mining, marine, defence) and through **21 dealers with 120+ branches** `[WEB: cummins.com India page]`. "480 customer touchpoints" `[PR-Q2]`. A large part of what it sells is *bought from sister companies*: Tata Cummins (a 50:50 JV of CMI and Tata Motors) and Cummins Technologies India (CTIPL, a CMI subsidiary).

### 1.2 Units for a manufacturer (this was the first protocol gap)
A retailer has one unit (the store). A manufacturer has **three units that must not be mixed up**:
| Unit | What it measures | Where the data is |
|---|---|---|
| **Plant** (capacity × utilisation) | Physical output and fixed-cost absorption | Plant list `[AR26]`, BRSR "physical output" intensity, "70% utilisation" `[CC-Q4FY26]` |
| **Product line / node** (kVA band or engine platform: LHP, MHP, HD, HHP/QSK60/QSK95) | Price, mix and competition | Quarterly segment splits on calls; emission-norm categories |
| **Channel account** (GOEM, dealer, industrial OEM) | Who captures the margin; concentration | Ind AS 108 customer-concentration footnote; dealer counts |

### 1.3 Plants `[AR26]`
Kothrud Engine Plant (Pune; 4,400 kWp of rooftop solar, the largest site); Power Generation Plant and the **Megasite at Phaltan** (Satara); Pirangut Power System Plant; Master Rebuild Centre (Phaltan); and a warehouse. BRSR counts "5 plants (incl. 1 warehouse) + 23 offices". **Installed capacity is not disclosed** in tonnes, engines or MW. The press release says "four manufacturing plants" `[PR-Q2]` against "five" `[PR-FY26]`, so a site was reclassified or sold. *Open: which one?*

### 1.4 Peers with comparable units
- **Kirloskar Oil Engines (KOEL):** the closest listed peer (engines + GOEM gensets, CPCB IV+ < 800 kW). Q2 FY27 standalone sales ₹1,739 cr (+19% YoY), OPM 11% (Q2 FY26 14%) `[SCR]`. PowerGen ₹792 cr (+17%) `[WEB: autocarpro / multibagg summaries, single-source]`.
- **Mahindra Powerol:** a division of M&M with **no separate disclosure** (gap). Usable only through dealer and installer scuttlebutt.
- **HHP/DC competitors:** Perkins (Caterpillar), Baudouin and Adani-linked imports are named by analysts as winning DC orders `[CC-Q4FY26]`, `[CC-Q2FY26]`. Also Greaves (LHP).

---

## 2. Reported financials, re-derived (L2)

### 2.1 Ten-year shape `[SCR]` (standalone, ₹ cr)
| FY | Sales | OPM | Other income | PAT | Payout | CFO | FCF | ROCE |
|---|---|---|---|---|---|---|---|---|
| FY15 | 4,406 | 17% | 287 | 786 | 49% | 498 | 168 | 31% |
| FY19 | 5,659 | 15% | 293 | 723 | 65% | 550 | 277 | 24% |
| FY21 | 4,329 | 14% | 349 | 618 | 67% | 788 | 674 | 19% |
| FY23 | 7,744 | 16% | 406 | 1,130 | 61% | 811 | 657 | 27% |
| FY24 | 8,959 | 20% | 566 | 1,661 | 63% | 1,280 | 999 | 36% |
| FY25 | 10,339 | 20% | 626 | 1,906 | 75% | 1,686 | 1,469 | 38% |
| FY26 | 12,143 | 21% | 670* | 2,330 | 79% | 1,734 | 1,487 | 42% |
*Screener nets the ₹50 cr exceptional against other income. AR26 other income is ₹720.5 cr.

- **The decade is two regimes.** FY15–21: sales ~₹4.4–5.7k cr, OPM 14–17%, ROCE falling 31% → 19%. FY22–26: sales 2.8×, OPM up to 20–21%, ROCE 42%. The step-ups line up with (a) the post-Covid capex/realty cycle, (b) the **CPCB IV+ price step** (§4.2) and (c) **data centres** (§3.4).
- **Quarterly turn** `[SCR]`: OPM 21–22% for five quarters to Mar-26, then **18% (Jun-26) and 15% (Sep-26)**. Sep-26 sales were +4% YoY.

### 2.2 FY26 P&L walk `[AR26]` (₹ cr)
Revenue 12,143 → materials (consumed 6,964 + traded 810 − inventory change 106 = **7,669, 63.2%**; FY25 63.8%) → employee 795 (6.5%) → other expenses 1,085 (8.9%) → EBITDA ~2,595 (21.4%) → D&A 199 → finance 12 → **other income 720** → PBT before exceptionals 3,104 → exceptionals −50 (labour codes −94.2, gain on sale of a subsidiary +44.2) → PAT 2,330.

### 2.3 Adjustments that matter
- **Other income is 23% of PBT (₹720 cr), and much of it is group-related** `[AR26 n.27]`: dividends from the associate (alternators) and the JV (lubes) ₹217 cr; interest ₹189 cr; **rent ₹186 cr** (investment property; "services rendered" to CTIPL include "renting services", ₹225 cr); MF gains ₹75 cr. **Core engine PBT ≈ ₹2,384 cr** [EST: 3,104 − 720]. On a P/E of 52, about a quarter of the "E" is treasury and group rent and dividends.
- **The labour-code charge (₹94.2 cr) is a one-time catch-up** on gratuity and leave under the new "wages" definition, presented as exceptional `[Q2R n.6]`. The *recurring* part shows up as employee cost +18% YoY in Q2 FY27 (§4.4).
- **Customer concentration jumped.** **Three external customers = ₹3,734.7 cr = 30.8% of sales** (FY25: two customers, ₹2,226.8 cr = 21.5%) `[AR26 consolidated n.44]`. Each is ≥10% of revenue (≥ ~₹1,214 cr). CIL sells power-gen engines through *three* GOEMs, so the three customers are **very likely the three GOEMs** [EST; inference, unverified]. The third one crossing 10% fits DC growth flowing through a GOEM.
- **Debt:** borrowings ₹37 cr (leases only); cash and MFs ~₹3,800–4,000 cr ("INR 38–40 billion", analyst on the call `[CC-Q2FY27]`; AR: MFs ₹1,360 cr + other liquid ₹689 cr + deposits).

---

## 3. Unit economics (L3)

### 3.1 Product-line revenue (domestic + export), from calls
| ₹ cr | FY26 `[CC-Q4FY26]` | Q2 FY26 `[CC-Q2FY26]` | Q1 FY27 `[CC-Q1FY27]` | Q2 FY27 `[CC-Q2FY27]` | Q2 YoY |
|---|---|---|---|---|---|
| Power Gen domestic | 4,758 (+24%) | 1,340 | 1,424 | **1,308** | −2% |
| Distribution (aftermarket, parts, service) | 3,278 (+22%) | 796 | 886 | **900** | +13% |
| Industrial domestic | 1,650 (−1%) | n/a | 458 | **406** | +5% |
| HHP exports | 984 (+20%) | 279 | ~298 [EST: 268/0.9] | **268** | −4% |
| LHP exports | ~1,005 [EST: 1,989 total exports − 984] | n/a | ~181 [EST] | **226** | +3% |
| Total sales (ex other op. revenue) | 11,950 | 3,122 | 3,375 | 3,247 | +4% |

- **Inside Power Gen, Q2 FY27** `[CC-Q2FY27]`: LHP ₹98 cr, mid-range ₹236 cr, heavy duty ₹142 cr, and the remaining **~₹832 cr (64%) is HHP + DC**.
- **DC share of power gen over time:** ~10% (Q1 FY25 `[CC-Q1FY25]`) → 23% (Q1 FY26) → ~25% (Q3 FY26) → 30–35% for FY26, ~35% in Q4 → **40% (Q1 FY27)** → "30–40%" (Q2 FY27). So **DC ≈ ₹1,430–1,670 cr in FY26** [EST: 30–35% × 4,758] and **≈ ₹390–520 cr in Q2 FY27**.
- **Ex-DC power gen is ambiguous by design.** A Macquarie analyst pointed out that at 30% DC share, ex-DC growth was mid-teens, and at 40% it was negative `[CC-Q2FY27]`. Management gave a range, not a number. **Definition audit (technique #10): "30–40%" is a 10-point band on a ₹1,308 cr line, so ±₹130 cr. That is wide enough to hide a non-DC slowdown.**
- **Industrial, Q2 FY27:** construction 131, rail 117, compressor 54, mining 49, marine 27, rest defence/O&G/parts `[CC-Q2FY27]`.
- **Exports by region, Q2 FY27:** Europe 29%, LatAm 28%, APAC 22%, Middle East 15% `[CC-Q2FY27]`.

### 3.2 Product-line margins: not disclosed. Bound them with transfer-pricing clauses.
CIL reports **one** segment ("Engines"). The best public handle on line margins is the **AGM-notice RPT pricing table** `[AR26 AGM notice, item 10 annex]`. Copied verbatim:
- **Sales to group companies (CL UK, TCPL, CTIPL, CMI):** "manufactured engines and gensets: **cost plus at least 11% mark-up**; manufactured components and spares: cost plus 14% mark-up / prices charged to third-party dealers".
- **Purchases from CTIPL:** "engines for manufacturing – **cost plus 11%** markup; turbochargers… third-party pricing; components and spares for distribution – cost plus 5%". From TCPL: "cost plus profit margins approved by TCPL Board… uniform to JV partners".
- **Royalty to CMI: "4% of eligible sales."** Agreement "for a period of three years **up to March 31, 2027**… usually renewed".

**What this implies** [EST, method shown, confidence unverified]:
- **Exports are mostly to the group at cost +11%.** Outside-India revenue was ₹2,007 cr `[AR26 n.26]`. Sales to Cummins Ltd UK alone were ₹1,018 cr (51% of exports), and "others" group sales were ₹607 cr. So roughly **50–80% of exports are priced at cost +11%**. A cost-plus-11% sale earns ~10% on sales before CIL's own overheads, against the company's 21% EBITDA. **Exports are structurally the lowest-margin line, and a weak rupee does not flow through in full:** the mark-up is on cost, not on market price.
- **Back-solving domestic margin.** If ~₹2,000 cr of exports earn ~10% [EST], domestic earns ≈ (2,595 − 200) ÷ 10,143 ≈ **23.6% EBITDA** [EST]. Distribution (parts and service) is normally the richest line at Cummins globally, so domestic power gen is probably below 23.6% and distribution above. *Unverified; no line P&L is disclosed.*
- **The FY27 approvals show how far management expects group trade to grow** (ceilings, not forecasts): sales to CL UK up to ₹1,975 cr (FY26 actual ₹1,018 cr); purchases from TCPL ₹2,231 cr (actual ₹1,399 cr), from CTIPL ₹2,074 cr (actual ₹1,317 cr), from CMI ₹779 cr; CMI "other RPTs" ₹619 cr, raised by ₹11 cr in Nov-2026 for the new MD's seconded cost `[PB-Nov26]`.

### 3.3 Plant: capacity × utilisation (technique #6, done a new way)
- **Physical output from BRSR intensity ratios** (new technique). BRSR gives total energy (193,212 GJ) and "energy intensity per unit of physical output" (1.3060 GJ/unit), where the unit is "number of equivalent units manufactured/assembled" `[AR26 BRSR P6]`. Units = 193,212 ÷ 1.3060 = **~147,900 equivalent units in FY26** (FY25: 200,812 ÷ 1.4538 = ~138,100).
- **Check:** water 179,627 kL ÷ 1.2142 kL/unit = 147,939, and waste 7,796.5 t ÷ 0.0527 = 147,941, the same number. This confirms the *arithmetic* only, not the definition (all three share one denominator).
- **Volume vs price.** Units +7.1% against revenue +17.4%, so **realisation/mix per equivalent unit ≈ +9.6%** (₹7.49 lakh → ₹8.21 lakh) [EST]. *Caveat:* "equivalent units" is a company weighting; we cannot tell whether a QSK60 counts as one unit or many.
- **Utilisation:** "70% utilisation" (an analyst repeating management, not contradicted) `[CC-Q4FY26]`. Implied capacity ≈ 147.9k ÷ 0.70 ≈ **~210k equivalent units** [EST]. Headroom ≈ 40% more volume before major capex. That fits management's "no major capital expenditure plan" `[CC-Q4FY26]`.
- **The binding constraint is not CIL's plants.** It is *HHP engines made elsewhere*: QSK60 at CTIPL, and QSK95 imported, made "largely in the US" `[CC-Q4FY26]`. Allocation is global ("demand is outpacing the addition of capacity" `[CC-Q1FY27]`). **Utilisation at CIL's own plants therefore tells you little about DC growth.** Watch CMI's capacity statements instead (an analyst cited "$450 m to raise 20 GW by 2030" `[CC-Q4FY26]`, unverified).

### 3.4 Data-centre genset demand: a physics check (technique #12)
- India DC IT capacity: about 1.5–1.9 GW operational in 2026. Top-7 cities added 178 MW in H1 2026 (1,789 MW operational, 509 MW under construction). ICRA expects 2.4–2.5 GW by FY28 `[WEB: Cushman via newkerala; KPMG Jul-2026; ICRA]`, secondary, ranges differ by definition.
- **DG MW per IT MW** [EST]: facility load ≈ IT × 1.3–1.5 (PUE), times redundancy N+1 (~1.2×) to 2N (2×), gives **~1.6–3.0 MW of DG per MW of IT**.
- **Implied market.** About 400–500 MW of IT a year (shipments lead commissioning by 6–12 months), × 1.6–3.0 = **~650–1,500 MW of DG a year**. At about ₹1.0–1.3 cr per MW for HHP gensets [EST, unverified benchmark; needs installer quotes], that is **~₹650–1,950 cr a year**.
- **The gap is the finding.** Cummins' own DC revenue alone (₹1,430–1,670 cr in FY26) sits at the *top* of this band, with a claimed DC share of "70–80%+" (analyst's framing, Nov-2024 `[CC-Q2FY25]`). Either (a) hyperscale builds run 2N plus extra DG (more DG per IT MW), (b) the pipeline under construction is larger than the top-7 counts, (c) Cummins' "DC" bucket includes enterprise, edge or captive sites, or (d) the share has fallen. **Resolve this with GOEM and installer checks (§6) before using any DC growth assumption.**

### 3.5 Channel unit: the dealer and the GOEM
- **Dealers:** 21 dealers, 120+ branches `[WEB: cummins.com]`. Distribution revenue ₹3,278 cr ÷ 21 ≈ **₹156 cr per dealer a year** [EST]; this flows through CIL's books, and the dealer's own revenue and margin are not disclosed. "Commission on sales" ₹30.9 cr (FY25 ₹21.0 cr, +47%) `[AR26 n.31]`. "Royalty income from dealers" is inside "other operating revenue – others" (₹134.9 cr) `[AR26 n.26]`. **The dealer pays CIL a royalty**, and CIL pays CMI one.
- **CIL sold its own distribution subsidiary,** Cummins Sales and Service Pvt Ltd (gain ₹44.15 cr, FY26) `[AR26 n.46]`. *Open: to whom, and at what price?*
- **LHP channel push:** 14 specialised "2S" dealers onboarded for low-kVA gensets `[AR26 MD&A]`. This is a test of whether CIL can win the price-sensitive band against KOEL and Mahindra.
- **GOEM economics:** not disclosed anywhere. The GOEM buys the engine, adds an alternator (often from **Cummins Generator Technologies India, CIL's associate**, which paid CIL a ₹117 cr dividend in FY26) plus canopy and panel, and sells to the end customer. **Part of the "alternator price hike" analysts blame for genset inflation `[CC-Q2FY27]` flows back to CIL as associate profit.** That is a small hidden hedge.

---

## 4. Line-by-line cost drivers in physical terms (L4)

### 4.1 FY26 cost map `[AR26 n.28–31]` (lines ≥ ~0.3% of sales; ₹ cr, % of sales 12,143)
| Line | ₹ cr | % sales | Physical driver | External input that moves it |
|---|---|---|---|---|
| **Materials (consumed + traded ± inventory)** | 7,669 | **63.2%** | Castings (block, head: pig iron/scrap), forgings (crank: steel), aluminium, copper (alternator, sitting at the associate), electronics/aftertreatment (CPCB IV+), purchased engines (QSK60 from CTIPL, QSK95 imported) | Pig iron, steel, Al, Cu, freight, INR/USD on imports. **51% of purchases are from related parties at cost-plus** (§5) |
| Employee benefits | 795 | 6.5% | 3,088 permanent staff × ~₹26 lakh/yr [EST: 795 ÷ avg 3,056] | Wage settlements (non-managerial +13% FY26), labour codes |
| **Support services to parent (net)** | 223 | **1.83%** | Corporate cost allocations ("management cross charges") | **The parent's allocation key**. FY25: 1.07% |
| Computer and other services | 115 | 0.95% | IT (part group-shared) | — |
| Warranty | 106 | 0.88% | Installed base × failure rate (new CPCB IV+ hardware) | Product maturity. FY25 0.94% |
| **Royalty to CMI** | 78 | 0.64% | **4% × eligible sales (₹1,949 cr ≈ 16% of revenue)** [EST: 77.94 ÷ 0.04] | **Contract renewal 31-Mar-2027** |
| Stores and spares | 78 | 0.64% | Machine hours | — |
| Outside processing | 45 | 0.37% | Sub-contract machining | Supplier capacity |
| Repairs (buildings + machinery) | 52 | 0.43% | Plant age | — |
| Power and fuel | 32 | **0.27%** | 193,212 GJ total (95,123 GJ grid electricity) `[AR26 BRSR]` | MSEDCL tariff. **Immaterial** (VMM: 1.8%) |
| Commission on sales | 31 | 0.25% | Agents/dealers | — |
| Other expenses (net), incl. freight | 218 | 1.80% | Freight not split out (gap) | Diesel, container rates |

### 4.2 CPCB IV+ emission-norm transition: price, volume, aftermarket
- **Timeline:** the norms were notified for gensets ≤800 kW. Cummins launched its CPCB IV+ range on **5-Jul-2023** `[WEB: autocarpro]`, sales switched fully from **1-Jul-2024**, and CPCB II channel inventory was "zero" by Aug-2024 `[CC-Q1FY25]`. HHP (>800 kW, i.e. most DC sets) stayed on CPCB II norms ("the data center space is outside of the CPCB IV+ space" `[CC-Q2FY25]`).
- **Price step:** "35–40% higher realisations" (management via Business Standard, Jun-2024) and "genset prices to jump over 50%" (earlier, BQ Prime) `[WEB]`. Two sources, not reconciled: the first is a realisation, the second a genset price. Cummins "mostly maintaining those prices" after launch `[CC-Q2FY25]`.
- **Pre-buy and dip:** "close to 5,000 sets" of CPCB IV+ sold over two quarters, "30–40% of the sales in the quarter were with CPCB-IV" (Q1 FY25) `[CC-Q1FY25]`.
- **Volume recovery:** "volumes are now back to pre-CPCB IV+ era… across the segments" by Q2 FY26 `[CC-Q2FY26]`. **About 15 months from switch-over to volume recovery.** Rivals launched products later (most during Q2–Q3 FY25), and "competitive intensity… every quarter it increases" `[CC-Q2FY26]`.
- **Margin effect:** OPM stepped up from 16% (FY23) to 20% (FY24), when the price premium arrived before rivals had products and while commodities were benign. The Q1 FY25 MD warned: "I don't think this kind of material margin is sustainable indefinitely" `[CC-Q1FY25]`. That has now happened (§4.3).
- **The aftermarket second wave is not visible yet.** CPCB IV+ sets carry electronics and aftertreatment (more parts and service content). "We are waiting to see all the gensets to come out of the warranty" `[CC-Q3FY26]`. Sets sold from Jul-2024 leave a ~2-year warranty from **mid-2026 onwards** [EST]. That is a dated, checkable tailwind for the distribution line (Q2 FY27 +13%). Also the NGT/CAQM retrofit mandates (RECD, dual-fuel kits) for old CPCB I/II sets in NCR `[AR26 MD&A]`.
- **Template lesson:** an emission-norm change is a *one-time price step, a pre-buy spike, a volume trough, competitor catch-up and then an aftermarket tail*. Each phase has a date and can be measured.

### 4.3 Commodity pass-through lag: the margin engine right now
| Quarter (standalone) | Materials ÷ revenue | OPM `[SCR]` | Note |
|---|---|---|---|
| FY25 | 63.8% | 20% | |
| FY26 | 63.2% | 21% | |
| Q2 FY26 | 63.5% | 22% | |
| Q1 FY27 | 66.5% | 18% | "Steel, pig iron, aluminium, copper significant increases"; "we have taken one [price increase]" `[CC-Q1FY27]` |
| **Q2 FY27** | **67.9%** | **15%** | +440 bps YoY. "Most of it is inflationary… relatively small portion… mix" `[CC-Q2FY27]` |
Method: (materials consumed + traded − change in inventories) ÷ (sales + other operating income) `[Q2R]`.

- **Why the lag is structural, in three mechanisms.**
  1. **Purchases from sister companies are cost-plus,** so their cost inflation passes *into* CIL almost at once.
  2. **Sales are on order books at contracted prices** (DC projects, rail/defence tenders "at agreed prices… price change mechanisms few and far between" `[CC-Q2FY27]`), so inflation passes *out* with a lag. **The minority-owned listed entity carries the timing mismatch.**
  3. **Inventory rose to ₹1,355 cr (Sep-26) from ₹1,168 cr (Mar-26)** `[Q2R]`, bought at higher costs, so Q3 COGS still carries the inflated cost layer.
- **Sensitivity** [EST]. If metal-linked content is ~35–50% of material cost (castings, forgings, sheet, Al; unverified, ask a supplier), a 10% rise in the metal basket costs **~220–320 bps of sales** before pricing. The observed −440 bps fits ~12–15% basket inflation plus some mix and freight. Analyst: "pig iron… up 14–20% YoY" `[CC-Q1FY27]`.
- **Leading indicators (all public, dated):** BigMint/SteelOrbis/Mysteel India pig iron and long-steel weekly prices; LME Al/Cu. Late-Oct/Nov-2026 readings show pig iron **flat to softer** (NMDC auction −₹300/t; SteelOrbis ₹16,500/t ex-works "stable") and the long-steel index down three weeks running `[WEB: SteelOrbis, Mysteel, single-source each]`. **This is the cost side turning before the P&L shows it.**
- **Pass-through history** [EST, from the `[SCR]` annual OPM]: in FY21–22 commodities rose and OPM sat at 14%; it recovered to 16% in FY23. That suggests a **2–4 quarter lag** for full pass-through in the last cycle, helped then by CPCB IV+ pricing, which is not available this time.

### 4.4 People: wages are *not* the micro-driver here (contrast with VMM)
`[AR26 BRSR]`:
- **Headcount:** permanent employees 1,309 + permanent workers 1,779 = **3,088 on rolls**. Contract ("other than permanent") workers 2,057 (FY25: 2,159). Total including contract staff 3,910 `[AR26 Directors' report]`.
- **Minimum wage:** **0% of permanent staff are at minimum wage. 80% of contract workers (1,640) are.**
- **Median pay:** permanent workers (male) ₹10.0 lakh/yr, female ₹7.9 lakh. Employees (male) ₹36.3 lakh, female ₹26.3 lakh. Median remuneration of all employees ₹12.0 lakh. MD = 61× the median.
- **Raises:** non-managerial salaries +13.0%; KMP +29.9%; median +5.55%.
- **Turnover:** permanent employees 7%, workers 4% (VMM: 84%).
- **Minimum-wage pool** [EST]. 1,640 contract workers × ~₹2.3–2.8 lakh/yr all-in agency cost (Maharashtra engineering-industry minimum wage plus a ~29% statutory load and agency margin; the Maharashtra rate was not looked up this session, so unverified) ≈ **₹38–46 cr ≈ 0.3–0.4% of sales**. A 10% minimum-wage revision ≈ **3–4 bps of margin** (VMM: 55–60 bps for a 15% step). **The wage-gazette leading indicator that mattered for the retailer is noise here.**
- **What does matter:** (a) the **labour codes** (₹94.2 cr one-time charge plus a higher recurring gratuity/leave base). Employee cost rose 18% YoY in Q2 FY27 against sales +4% `[Q2R]`, so ~80 bps of margin. (b) The unionised permanent workforce at Kothrud: a retirement-age dispute (58 vs 60) is pending in the Bombay HC; the order is stayed and there is "no material financial impact" `[NSE 12-Jun-2026]`.
- **Productivity:** revenue per permanent employee ₹3.9 cr [EST: 12,143 ÷ 3,088]. KOEL was not computed this session (open).

### 4.5 Working capital, cash conversion, capex
- **Days** `[SCR]`: debtors 83 (FY25 81), inventory 56, payables 79, CCC 60 (FY25 51).
- **FY26 cash flow** `[AR26 CF]`: receivables absorbed ₹445 cr (FY25 ₹222 cr). CFO ₹1,734 cr = 74% of PAT, and 91% CFO (pre-tax)/EBITDA `[SCR]`.
- **H1 FY27:** CFO ₹1,021 cr (H1 FY26 ₹742 cr). Receivables released ₹110 cr; inventory absorbed ₹186 cr `[Q2R]`.
- **Capex vs depreciation:** FY26 ₹252 cr vs ₹199 cr (1.27×); FY25 ₹226 cr vs ₹183 cr (1.23×) `[AR26]`. "More than ₹1,000 cr in the last 5 years… modernisation… more output from the same line" `[CC-Q4FY26]`.
- **Asset turns:** revenue ÷ net fixed assets ≈ 5.1× [EST: 12,143 ÷ 2,383].
- **FCF ≈ dividends:** FCF ₹1,487 cr against dividends paid ₹1,483 cr (FY26) `[SCR, AR26]`. The company is now distributing essentially all its free cash.

---

## 5. Governance, ownership, related parties (L5): the "parent take"

### 5.1 Ownership `[SCR]`
Cummins Inc 51.00% (flat for 10+ years, no pledge). FIIs 19.5% (Sep-26; peak 21.2% Jun-26), DIIs 20.8%, public 8.7%, 1.66 lakh shareholders. **No promoter supply overhang** (unlike VMM's PE seller). The parent has no reason to sell. What it wants is cash flow from the subsidiary.

### 5.2 RPT table by year, with share of each line `[AR26 n.41]`
| Item | FY25 ₹ cr | FY26 ₹ cr | FY26 share of matching line | Trend |
|---|---|---|---|---|
| Purchases from RPs (TCPL 1,399; CTIPL 1,317; others 1,281) | 3,489 | 3,997 | **51.2% of purchases** (FY25 52.3%) | Stable; FY27 ceilings imply up to ~₹5,585 cr |
| Sales to RPs (CL UK 1,018; CTIPL 463; others 607) | 1,870 | 2,088 | 17.2% of revenue; ~**50–80% of exports** | FY27 ceiling for CL UK ₹1,975 cr |
| **Royalty to CMI** | 70.7 | 77.9 | 0.64% of sales; 4% of eligible sales | +10% vs sales +17% |
| **Support services (CMI 213.0 + CAME 9.5)** | 110.6 | **222.5** | **20.5% of other expenses** (FY25 12.2%) | **+101%** |
| Royalty + support | 181.2 | 300.5 | **2.47% of sales (FY25 1.75%); 11.6% of EBITDA (FY25 8.8%)** | +66% |
| Reimbursements paid to CTIPL | 137.7 | 295.2 | — | **+114%** (cost recoveries: employee, IT, travel) |
| Services rendered by CIL to CTIPL (incl. rent) | 203.7 | 225.3 | Part of the ₹186 cr rent in other income | Income to CIL |
| Dividend paid to CMI | 537.2 | 756.3 | 51% of dividends | +41% |
| Payables to CMI for royalty + support (year-end) | 98.6 | 159.2 | — | +62% |
| **Cash to CMI** (dividend + royalty + support + reimbursements) [EST: sum] | 729 | **1,075** | **8.9% of sales** | +47% |

Interpretation, in two versions:
- **Benign:** "Support services" are cost allocations for the global engineering, IT and DC-application teams that serve India's fastest-growing line. The FY27 approval for CMI "other RPTs" (₹630 cr, *incl.* royalty, services and asset purchases) is a ceiling, not a plan. All RPTs are approved by the audit committee and by majority-of-minority shareholder votes (SEBI Reg 23), and AOC-2 says "no transactions not at arm's length". The auditor (Price Waterhouse, reappointed for a second 5-year term in May-2026) gave an unmodified opinion.
- **Malign (or simply less favourable to minorities):** an allocation key the minority cannot see. It doubled in one year and had a further "true-up" in Q2 FY27 `[CC-Q2FY27]`, while minorities also absorb the commodity lag that cost-plus sister suppliers do not.
- **Grade: soft flag, open.** It is not a hard disqualifier: there is no sign of diversion, the amounts are disclosed and the rates are uniform across the group (CIL "confirms… the parent company charges royalty at a uniform rate from all group companies" `[AR26 AGM notice B(7)]`).
- **Dated trigger:** royalty agreement renewal on **31-Mar-2027**. The FY27 AGM notice (around Jul-2027) will show the new rate. **Put it in the calendar.**

### 5.3 Management, board, incentives
- **MD churn:** Ashwath Ram (to Aug-2024) → Shveta Arya (Sep-2024, resigned w.e.f. 31-Aug-2026) → **Adegbile Adewunmi from 1-Nov-2026**, seconded from CMI global. His cost is recharged by CMI "on an actual-cost basis, without any mark-up" (+₹11 cr to the CMI RPT limit) `[PB-Nov26]`. The MD's pay therefore runs through the parent.
- **Other changes:** the CFO changed twice (Patil left Jan-2025; interim; Soma Ghosh from Jul-2025). Senior management person Pankaj Kapoor resigned Aug-2026 `[NSE filings]`.
- **Board:** 10 directors, 5 women; the chair (Jennifer Bush) and 3–4 non-executives are CMI nominees `[AR26]`. Non-executive CMI nominees take no pay. ID commission was approved by postal ballot (Oct-2026).
- **Incentives:** KMP remuneration ₹9.8 cr (FY25 ₹16.2 cr, which included transitions). CMI stock-based pay to CIL staff ₹14.4 cr "equity contribution" `[AR26 n.41]`. **Senior staff are paid in parent (US) stock, not CIL stock.** The incentive is aligned with CMI's global P&L, not with the CIL minority.
- **Tax and legal:** the Income Tax Department appealed to the Bombay HC on ₹210.77 cr of adjustments (nature not stated; likely transfer pricing, unverified) `[NSE 09-Jul-2026]`. GST demand of ₹5.19 cr plus an equal penalty (Jaipur, Oct-2026). Income-tax penalty of ₹0.95 cr (AY2018-19). All are small next to equity of ₹7,600 cr.

### 5.4 Dividend payout to the parent
- **FY26 declared:** ₹66/share (interim 20 + final 46) = ₹1,830 cr = **78.5% payout** [EST: 66 × 27.72 cr shares ÷ PAT 2,330]. The parent's share is **₹933 cr**.
- **Trend:** payout went from 49% (FY15) to 63% (FY24), 75% (FY25) and 79% (FY26) `[SCR]`. Cash in the books is still ₹3.8–4.0k cr. "No major changes" in capital-allocation philosophy `[CC-Q2FY27]`.
- **Minorities get the same per-share dividend.** For them the dividend channel is *fair*. The royalty and support channels are *not pro-rata*. **The mix between the two channels is the governance signal.** In FY26 both rose: the dividend to CMI +41%, royalty plus support +66%.

---

## 6. Ground check (L6): three visits for one person (dealers / genset installers / customers)
Pick visits to test the model, not for convenience. Pune is the natural base (plants, the Balewadi HQ, dealers, a large DC cluster nearby in Mumbai/Navi Mumbai). About 2 days.

**Visit A: a GOEM or GOEM-authorised genset dealer** (e.g. a Sudhir Power or Jakson sales office, Pune or Delhi NCR), plus one KOEL and one Mahindra Powerol dealer in the same city.
1. **Price sheet by node:** list and transaction price for 62.5, 125, 250, 500 and 1,010 kVA CPCB IV+ sets, and for a 2,000+ kVA HHP set: Cummins vs KOEL vs Mahindra vs Greaves. Repeat quarterly (the fixed price basket). This tests the "10–15% Cummins premium" (analyst's assertion, not confirmed `[CC-Q2FY27]`) and whether CIL's Q1 FY27 price hike stuck.
2. **Price-hike log:** dates and % of engine vs alternator vs canopy increases since Apr-2026. This tests the claim that "alternator players took most of the hike, engines single-digit" (Macquarie on the call) and gives the pass-through lag directly.
3. **Lead time** today for a QSK60 and a QSK95 set vs a Perkins/Baudouin set. This tests the "allocation" risk (§3.3) and the DC share.
4. **Who are the three big customers?** Ask how the GOEM's volume split between DC, realty and industrial moved. This tests the 31% concentration inference (§2.3).

**Visit B: a Cummins dealer workshop or parts counter (distribution business)**
5. **Count:** service bays, technicians, jobs on the board, share of CPCB IV+ jobs; parts-counter tickets per hour.
6. **Post-warranty CPCB IV+ tickets:** what fails (DPF/SCR, sensors, ECU), parts price per job, and whether customers come back after warranty or go to independent mechanics. This tests the "aftermarket second wave" (§4.2).
7. **Will-fit vs genuine:** price of 5 fixed parts (filters, injector, turbo, gasket kit, starter) genuine vs will-fit vs "OEM second-line". This tests the MD&A threat about will-fit parts and gives a quarterly time series.
8. **Dealer economics:** margin on parts vs gensets (ask in ranges), the royalty paid to CIL (it exists: "royalty income from dealers" `[AR26 n.26]`), technician pay and attrition, and the dealer's view of the 14 new "2S" LHP dealers. Never ask for confidential CIL data.
9. **Retrofit and dual fuel:** monthly enquiries for RECD and DF kits under the CAQM orders (NCR) — a regulation-driven aftermarket.

**Visit C: customers and installers** (one DC facility/projects engineer or an EPC installer, one commercial-realty or hospital facility manager, one genset rental company)
10. **DC:** DG MW installed per IT MW (redundancy N+1 / 2N), genset brand split on the last 2–3 projects, the price per MW paid, and whether they were offered gas, BESS or fuel-cell alternatives. This resolves the §3.4 physics gap.
11. **Realty/hospital:** brand chosen and why (service reach, TCO, resale), running hours per year (standby utilisation drives parts intensity: the MD&A threat about a "low utilisation profile"), and whether rooftop solar plus BESS is replacing DG hours. Cummins' own BESS pilot is at the Phaltan MRC.
12. **Rental company:** fleet brand mix, utilisation and rental rates per kVA-month — a cyclical read on realty/infrastructure demand.

**Counts first, then opinions. Ethics:** identify yourself honestly if asked; do not solicit unpublished price-sensitive information; do not pay for information; no recordings without consent. Price quotes that a dealer would give any buyer are fair game.

**Output:** a price sheet by node and brand (the quarterly series), a lead-time table, a parts-price table, 5 quotes, and a "surprises vs model" list. Each of §3.1–4.5's estimates gets marked confirmed, contradicted or no read.

---

## 7. Flag override (L7): bad but benign, good but misleading
Format per `insight:flag-override-template`. A management explanation alone keeps a flag OPEN (L10, L12).

| Flag | Context questions | Evidence that clears | Evidence that confirms | Verdict now | What changes my mind | Review |
|---|---|---|---|---|---|---|
| **OPM 21% → 15% in two quarters** (looks bad) | Industry-wide or Cummins-specific? Lag or lost pricing power? | KOEL OPM 14% → 11% in the same quarter `[SCR]`; metal prices up 14–20% YoY; pig iron flattening Nov-26 `[WEB]`; one-off cross-charge true-up in Q2 | Materials ratio stays >66% two quarters after hikes; Cummins growth (+4%) far behind KOEL (+19%) | **Open, likely cyclical lag** | Q3/Q4 FY27 materials ratio; GOEM price log (§6 #2) | Q3 FY27 results (Feb-2027) |
| **Sales +4% vs KOEL +19% (Q2 FY27)** (looks bad: share loss?) | DC lumpiness? HHP allocation? | Management: DC mix timing, rail coach inventory, marine execution, compressor supply `[CC-Q2FY27]` (a management explanation, so not clearing) | Power gen −2% YoY while KOEL PowerGen +17% | **Open, soft flag** | Two more quarters of the gap; lead-time checks | Q4 FY27 |
| **3 customers = 31% of sales** (looks bad) | Channel partners or end users? | CIL sells power gen through 3 GOEMs (cummins.com), so likely channel concentration | GOEM financial stress (MCA filings of Sudhir/Jakson); a GOEM switching engine brand | **Open, likely benign** | GOEM names confirmed; their balance sheets | FY27 AR |
| **51% of purchases from related parties** (looks bad) | Structural MNC sourcing? Priced how? | Pricing formulas disclosed (cost +11% engines, +5% parts); shareholder approvals; localisation "very high" `[CC-Q4FY26]` | Cost-plus pass-in during inflation while CIL eats the lag; rising RP share | **Open, soft flag (mechanism understood)** | RP share of purchases >55%; margin gap widening in inflationary quarters | Each AR |
| **Support services to parent ₹111 → ₹223 cr; Q2 "true-up"** (invisible on a screen; looks bad) | Allocation key? Linked to DC growth? | Management: support rises with India's DC business `[CC-Q2FY27]` (an explanation only) | FY27 support >2% of sales again; further unannounced true-ups | **Open, soft flag** | Disclosure of the key; FY27 AR n.41 | FY27 AR (Jul-2027) |
| **Royalty agreement expires 31-Mar-2027** (neutral, dated) | New rate? scope of "eligible sales"? | Uniform group rate affirmed `[AR26]`; renewed in the past | Rate or eligible base raised | **Open, dated watch** | FY28 AGM notice RPT annex | Jul-2027 |
| **Exports to group at cost +11%** (a weak rupee "should help": looks good, misleads) | Who captures export margin? | — | TP clause caps CIL's export margin; INR gains accrue largely to group buyers | **Misleading in isolation** | Disclosure of the third-party export share | — |
| **ROCE 42%** (looks good) | Cash-inflated or cash-depressed? Capital elsewhere in the group? | Core ROCE ≈ 58% [EST: EBIT ex-OI 2,396 ÷ (CE 7,934 − cash ~3,800)] | QSK60 made at CTIPL and QSK95 imported, so DC capital sits in sister companies | **Good but partly borrowed from the group's balance sheet** | — | — |
| **"70% utilisation, no major capex"** (looks good) | Is own-plant capacity the bottleneck? | — | HHP supply is allocated globally; "demand outpacing capacity" `[CC-Q1FY27]` | **Misleading for DC growth** | CMI capacity plans; lead-time checks | Each call |
| **DC = "30–40%" of power gen** (looks good) | Definition? Band width? | — | Band = ±₹130 cr/quarter; physics check puts Cummins DC revenue at the top of the market band (§3.4) | **Open (definitional)** | Installer DG/IT ratio, brand split | §6 visit C |
| **Other income 23% of PBT** (looks good: "EPS growth") | Treasury, group rent, JV dividends? | Recurring (rent from CTIPL, JV dividends) | Rates fall; cash paid out at 79% shrinks treasury income | **Use core PBT ₹2,384 cr for multiples** | — | — |
| **Payout 79%, FCF ≈ dividend** (looks good) | Sustainable? Crowding out capex? | Capex/D&A 1.27×, 30% headroom, ₹3.8k cr cash | — | **Cleared (benign) for now** | Capex spike or payout >100% | FY27 |
| **Labour-code exceptional ₹94 cr** (looks bad) | One-off or recurring? | Regulatory catch-up, disclosed `[Q2R n.6]`; recurring part visible in employee cost | — | **Cleared (one-off); recurring ~80 bps tracked** | — | — |
| **MD ×3 and CFO ×2 in 26 months** (looks bad) | MNC rotation or problems? | CMI rotates leaders; the new MD came from CMI global; no auditor issues | Further senior exits; strategy reversals | **Open, low** | — | Each quarter |
| **IT appeal on ₹210.8 cr adjustments** (looks bad) | Transfer pricing? Size? | <3% of equity; lower authority ruled for CIL | HC reversal | **Open, small** | HC order | — |

**Count of open soft flags: 7** (RP purchases, support services, sales gap vs KOEL, GOEM concentration, DC definition, MD churn, IT appeal) plus 1 dated watch (royalty renewal). That is above the 3+ rule, so *no position without a written variant view*. This is a statement about our evidence, not about the company.

---

## 8. Note on the open paper call (not a change to it)
`thesis:paper-call:CUMMINSIND:q3fy27-opm-17pct-plus` (made 2026-11-21, P = 0.38, base 0.45). Our rules forbid editing a call after it is made. Facts surfaced here that its reasoning did **not** use, recorded for the post-mortem:
- **Q2 FY27 OPM was 15.3%** [506 ÷ 3,301]. It **included an unquantified one-off "true-up" of corporate cost allocations** in other expenses `[CC-Q2FY27]`. Other expenses were 9.66% of sales against 8.34% a year earlier (+₹54 cr). If ₹25–40 cr was the one-off [EST], normalised Q2 OPM ≈ 16.1–16.5%. Reaching 17% then needs only ~0.5–0.9 pp more from pricing and materials.
- **For YES:** pig iron/steel flat to softer in Oct–Nov 2026 `[WEB]`; price hikes "starting" on new orders `[CC-Q2FY27]`; H1 receivables released.
- **For NO:** the inventory layer at high cost (+₹186 cr in H1) flows into Q3 COGS; employee cost +18% YoY is recurring; management refused to call a bottom; order-book execution at old prices.
- Net: the one-off is the most decision-relevant new fact. **Lesson for the paper-call method: read the other-expenses commentary before setting a margin probability.**

---

## 9. What this exercise taught (method, not stock)
1. **For an MNC subsidiary, the AGM-notice RPT annex is the richest document in the set.** SEBI's Jun-2025 "minimum information" standard forces pricing formulas (cost +11%, +14%, +5%), the royalty rate (4% of eligible sales) and the sunset date. No broker note on the last call mentioned any of these.
2. **"Security-guard depth" for a manufacturer is the materials line, not the wage line.** Contract minimum-wage labour is ~0.3% of sales here (3–4 bps per 10% wage step) against VMM's 3.8%. The protocol's L4 default (wages, guards, rent) must be chosen by cost weight, not by habit.
3. **BRSR intensity ratios give physical volume for free.** Energy (GJ) ÷ GJ per unit gives "equivalent units" (~147.9k), cross-footed by water and waste. That splits growth into volume (+7%) and price/mix (+10%) with no company KPI needed.
4. **Find out who carries the timing mismatch.** Cost-plus purchases from sister companies plus fixed-price order books mean the listed minority absorbs commodity lags. That is a structural fact behind a "cyclical" margin dip.
5. **Physics checks work on demand claims too.** IT MW × PUE × redundancy × ₹/MW puts bounds on the whole DC genset market, and Cummins' DC revenue sits at its top. The gap is a research question, not a conclusion.
6. Time spent: about 75% on primary filings (AR notes, BRSR, AGM notice, 7 transcripts, postal ballot), 15% on estimates, 10% on web/peer. Broker notes were not needed. Analyst questions in transcripts relay what the sell side knows.

## Open items (for a later pass)
- **Mahindra Powerol economics:** M&M does not disclose them. Get via dealers, or M&M analyst-meet slides.
- **KOEL like-for-like:** full KOEL Q2 FY27 transcript (B2B vs B2C split, CPCB IV+ share, LHP pricing), KOEL BRSR units, and revenue per employee.
- **Identity of the 3 customers >10%** and the third GOEM; MCA filings of the GOEMs.
- **Capacity:** which plant was reclassified (5 → 4 plants); consent-to-operate (MPCB) permitted capacity for Kothrud and Phaltan; CTIPL's QSK60 capacity (MCA filings of CTIPL).
- **Freight:** the line is not split out. Ask IR, or derive from the cash-flow/GST data.
- **Maharashtra minimum wage (engineering)** for the contract-labour pool (to firm up §4.4).
- **History:** royalty and support services for FY20–FY24 from old ARs (a 7-year trend); old AGM notices for previous royalty rates.

## Sources
- FY26 Annual Report + BRSR + 65th AGM notice: https://nsearchives.nseindia.in/corporate/CUMMINSIND_09072026220941_SEIntimationAGMNotice_AR.pdf ; BRSR cover letter: https://nsearchives.nseindia.in/corporate/CUMMINSIND_09072026223802_SEintimationBRSRfinal.pdf
- Q2 FY27 results: https://nsearchives.nseindia.in/corporate/CUMMINSIND_04112026223607_SEintimation_OutcomeFR_04112026.pdf ; press release: https://nsearchives.nseindia.in/corporate/CUMMINSIND_04112026232559_SEIntimationPressRelease_04112026.pdf
- FY26 press release: https://nsearchives.nseindia.in/corporate/CUMMINSIND_27052026154234_SEIntimationPressRelease.pdf ; FY26 board outcome (dividend, auditor): https://nsearchives.nseindia.in/corporate/CUMMINSIND_27052026141719_SEintimationOutcome27052026.pdf
- Postal ballot (new MD, extra CMI RPT): https://nsearchives.nseindia.in/corporate/CUMMINSIND_06112026173755_SEIntimationNoticeofPBfinal.pdf ; ID commission PB: https://nsearchives.nseindia.in/corporate/CUMMINSIND_15092026192427_SEintimationNoticeofPBFinal.pdf
- Transcripts: Q2 FY27 https://nsearchives.nseindia.in/corporate/CUMMINSIND_20112026163131_SEIntimationTranscriptQ2Final.pdf ; Q1 FY27 https://nsearchives.nseindia.in/corporate/CUMMINSIND_11082026172947_SEIntimationTranscriptQ1Final.pdf ; Q4 FY26 https://nsearchives.nseindia.in/corporate/CUMMINSIND_03062026175541_SEIntimationTranscriptQ4Final_Signed.pdf ; Q3 FY26 https://nsearchives.nseindia.in/corporate/CUMMINSIND_10022026181728_SEintimationTranscriptQ3CallFinal.pdf ; Q2 FY26 https://nsearchives.nseindia.in/corporate/CUMMINSIND_10112025171553_SIGNEDCombinedSEIntimationTranscriptQ2FY202526.pdf ; Q2 FY25 https://nsearchives.nseindia.in/corporate/CUMMINSIND_11112024140013_SignedFinalCombinedTranscriptIntimation.pdf ; Q1 FY25 https://nsearchives.nseindia.in/corporate/CUMMINSIND_09082024172427_SignedTranscriptAugust072024.pdf
- Litigation/tax: https://nsearchives.nseindia.in/corporate/CUMMINSIND_09072026193815_SEintimationLitigationPendency.pdf ; https://nsearchives.nseindia.in/corporate/CUMMINSIND_12062026110202_SE_IntimationReg30LitigationUpdate_Signed.pdf ; https://nsearchives.nseindia.in/corporate/CUMMINSIND_28102026173906_SEintimationReg30.pdf ; https://nsearchives.nseindia.in/corporate/CUMMINSIND_29092026195426_SEintimationCILITAct29092026.pdf
- screener.in: https://www.screener.in/company/CUMMINSIND/ ; https://www.screener.in/company/KIRLOSENG/
- KOEL Q2 FY27 (secondary): https://www.autocarpro.in/news/kirloskar-oil-engines-q2-net-profit-drops-18-percent-to-rs-130-crore-135718 ; https://www.multibagg.ai/market-pulse/articles/kirloskar-oil-engines-margin-falls-concall-cmwc3wrb600c62rpbbiw8kpaa
- CPCB IV+ pricing: https://www.business-standard.com/amp/markets/news/demand-triggers-remain-strong-for-cummins-india-kirloskar-oil-engines-124062100985_1.html ; https://www.bqprime.com/business/genset-prices-to-jump-over-50-with-new-emission-norms-says-cummins-india-head-publish-with-video ; https://www.autocarpro.in/news/cummins-india-launches-cpcbiv-compliant-power-solutions-115750
- Channel (3 GOEMs, 21 dealers): https://www.cummins.com/en/in/company/cummins-in-india ; https://energetica-india.net/news/cummins-india-and-sudhir-power-unveil-cpcbiv-compliant-genset-range-for-delhi-ncr-markets ; https://www.pv-magazine-india.com/?p=11767
- DC capacity: https://assets.kpmg.com/content/dam/kpmgsites/in/pdf/2026/07/india-data-centre-opportunity-from-emerging-demand-hub-to-integrated-data-centre-powerhouse.pdf ; https://www.newkerala.com/news/a/indias-data-center-capacity-surges-1789-mw-jan-june-969.htm ; https://www.icra.in/Research/ViewResearchReport/6543 ; https://yourstory.com/2026/06/indias-data-centre-pipeline-knight-frank-india
- Metals: https://www.steelorbis.com/steel-prices/steel-prices-market-analyses/scrap-and-raw-materials/local_indian_pig_iron_prices_stable_despite_producers_reducing_base_prices_-908531.htm ; https://www.mysteel.net/news/5147302-india-steel-index-drops-for-third-straight-week-as-long-steel-prices-see-sharp-correction ; https://www.bigmint.co/intel/detail/india-bids-edge-up-in-nmdc-nagarnar-s-latest-pig-iron-auction-35056

---

## 10. Protocol v1.1 changes (what this run taught the protocol)

**What worked**
- **Rule zero pointed straight at L5.** Listing the five most-asked questions showed that nobody models the parent take. That led to the support-services doubling and the royalty renewal date within the first two hours.
- **L13 ("boring filings") held again**, this time through other-expenses note 31, RPT note 41, the BRSR and the AGM-notice annex.
- **Techniques #10 (definition audit) and #12 (physics check) transferred unchanged** to "DC = 30–40%" and "equivalent units".
- The override table format worked, and so did the "looks good" rows: ROCE, utilisation, exports, other income.

**What was missing for a manufacturer (vs a retailer)**
1. **Unit definition.** A manufacturer has three units (plant, product node, channel account). The protocol assumed one (the store).
2. **The L4 default was wage-centred.** It must be chosen by cost weight. Materials were 63% of sales here; wages at minimum-wage level were 0.3%.
3. **No commodity pass-through method.** There was no routine for the materials ratio by quarter, cost-plus pass-in vs contracted pass-out, inventory cost layers, lag estimation, or leading price series.
4. **No MNC parent-take layer:** royalty, support/cost allocations, transfer-pricing formulas, purchases from and sales to group companies, dividends to the parent, and renewal dates. The AGM-notice RPT annex (SEBI Jun-2025 standard) was not listed as a source.
5. **BRSR physical-output intensity → volume** was not a listed technique.
6. **The customer-concentration footnote (Ind AS 108)** and the **other-income decomposition** (treasury, group rent, JV dividends → core PBT) were not in L2.
7. **No regulatory-transition template** (emission norms, BIS/QCOs, labour codes).
8. **Capacity:** own-plant vs group/supplier capacity was not distinguished.
9. **B2B scuttlebutt rules:** the L6 rules were store-centric (footfall, bills). B2B needs price sheets by node, lead times, a parts-price basket and tender results.
10. **Tool note:** `nse_fetch.py transcripts --download` ignores date filters. Listing first and then curling the needed URLs saved time.

**Concrete edits applied to `deep_dive_protocol.md` (v1.1)**
- A new "Choose the unit by business type" table (retailer / manufacturer / MNC subsidiary / lender / platform).
- L4 rewritten: rank cost lines by weight first, and do security-guard depth on the top 3.
- New L5 sub-step: "Parent-take table" for MNC subsidiaries and group companies, with a time-budget shift (L5 10% → 15% for MNC subs, taken from L3).
- New techniques #13 (BRSR intensity → units), #14 (commodity pass-through lag), #15 (transfer-pricing bounds on line margins), #16 (regulatory-transition template), #17 (other-income decomposition) and #18 (customer concentration from Ind AS 108).
- New manufacturer data sources (BigMint/SteelOrbis/Mysteel, LME, CPCB/CAQM notifications, MPCB/SPCB consent orders, GeM/IR tenders, MCA filings of private channel partners) and the AGM-notice RPT annex.
- B2B scuttlebutt rules.
- Deliverables: parent-take table and price-vs-cost lag table.
- Four new common traps.
- A changelog at the bottom.
