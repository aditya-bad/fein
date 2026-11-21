# Vishal Mega Mart (NSE: VMM): practice deep dive at "security-guard depth"

**Date:** 2026-11-20 · **Purpose:** to learn *how* to go deep and to build the reusable protocol (see `deep_dive_protocol.md`).
**This is test material (lesson L9). There is no buy/sell/watchlist verdict and none should be read in.** Research, not SEBI-registered advice.

Every number carries a source tag. Every estimate shows its method.
- `[AR26]` = VMM FY26 Annual Report (NSE, 24-Aug-2026), audited notes
- `[BRSR26]` = BRSR FY26 (NSE, 24-Aug-2026) · `[BRSR25]` = BRSR FY25
- `[UDRHP]` = Updated Draft RHP-I, 17-Oct-2024 (NSE archive)
- `[PPT-Q2]` = Q2 FY27 investor presentation (21-Oct-2026) · `[CC-Q2]` = Q2 FY27 call transcript (26-Oct-2026) · `[CC-Q3FY26]` = Q3 FY26 transcript (28-Jan-2026)
- `[HSIE]` = HDFC Securities update, 25-Sep-2026 · `[ELARA]` = Elara result note, May 2025
- `[SCR]` = screener.in consolidated pages, fetched 20-Nov-2026
- `[EST]` = my estimate, with the method shown in the same row

Price/valuation snapshot `[SCR]` (20-Nov-2026), for context only: CMP ₹91.5, market cap ₹42,852 cr, trailing P/E 47.7, 52-week high ₹140 (HSIE gives ₹152/99 as of 24-Sep). DMart: P/E 73.5. V2 Retail: P/E 36.7.

---

## 0. Edge question first (what could we know that the market doesn't?)
VMM is covered by about 20 brokers, so the public P&L has no edge. Possible edges sit only in:
1. **Cost-line micro-drivers the sell side models as "% of sales"**, such as state minimum wages, outsourced security, and related-party logistics. These move with notifications and contracts, not with sales (see §2.3 and §2.4).
2. **Ground truth on store productivity in new geographies.** South/West stores and small-format stores are where the next 1,000 stores must work, and quarterly disclosures blur them.
3. **Supply overhang mechanics.** The PE sponsor still holds about 40%. Who absorbs the supply, and at what discount?

The rest of this file is the scaffolding needed to ask those three questions well.

---

## 1. Store-level unit economics

### 1.1 Footprint by year
| Year-end | Stores | Retail area (mn sq ft) | Avg size (sq ft) | Source |
|---|---|---|---|---|
| FY24 (Mar-24) | 611 | ~11.0 | ~18,000 | [ELARA] chart; stores implied by FY25 −85 net |
| FY25 (Mar-25) | 696 | ~12.2 | ~17,500 | [ELARA], [HSIE] |
| FY26 (Mar-26) | 795 | 13.45 | 16,918 [EST: 13.45m/795] | web/PPT summary, [CC-Q3FY26] 13.2m @771 Dec-25 |
| Sep-26 | 844 (net +49 in H1; 53 gross) | 14.1 | ~16,700 | [PPT-Q2], [CC-Q2] |

- **Tier mix Sep-26** `[PPT-Q2]`: 443 Tier III (<200k pop), 197 Tier II, 204 Tier I. **Region:** North 315, East 237, South 208, West 84. **Revenue by region Q2:** North 37.4%, East 30.5%, South 23.5%, West 8.6%.
- **The average size is shrinking.** Analysts flagged this on the Q2 call `[CC-Q2]`. Management will open 15k sq ft stores in high-cost states (Gujarat/Maharashtra: "minimum wages … electricity … rental costs are the highest"). 18 small-format (~8k sq ft) stores are open, only in UP/Haryana, where the "target audience is ~85–90% tapped" `[HSIE]`.

### 1.2 Productivity
| Metric | VMM FY26 | DMart FY26 | V2 Retail FY26 | Method |
|---|---|---|---|---|
| Revenue per sq ft per yr | **₹10,063** (avg area) / ₹9,596 (closing) | **₹33,422** (company) | ~₹11,100 (₹925/month) | [EST] VMM: ₹1,29,063 mn ÷ avg(12.2, 13.45) mn sq ft. DMart and V2 as reported by the companies (single-source web summaries) |
| Revenue per store per yr | ₹17.3 cr | ~₹134 cr [EST: ₹66,968 cr ÷ avg(415, 500) stores] | — | [EST] |
| Gross margin | 28.4% [AR26] | ~15% [SCR: material cost 85%] | ~30% [SCR: material 70%] | |
| **Gross profit per sq ft per yr** | **~₹2,860** | **~₹5,000** | ~₹3,300 | [EST] = rev/sq ft × GM |

**Lesson:** VMM's 28% gross margin looks twice DMart's 15%. But DMart turns each square foot about 3.3× faster, so it earns about 75% *more* gross profit per square foot. Margin % without density is half a number. (DMart also owns most of its stores, so its occupancy cost is capex rather than rent. That is the next layer.)

- **V2 Retail is the cannibalisation and immaturity warning for the format.** V2 sold ₹700 per sq ft per month in Q2 FY27 against ₹933 a year earlier, after 139 stores were added in FY26 and SSSG went negative (−3.7% H1, calendar basis). Source: V2 Q2 FY27 transcript summary, single-source. Fast rollout in the same value format can dilute density sharply. VMM's 5.4% Q2 SSSG (about 9% festive-adjusted) has not shown this, but it is the metric to watch.

### 1.3 Category economics
| Category | FY26 revenue ₹ mn [HSIE] | Mix FY26 | FY22–26 CAGR | Private label share | PL margin premium |
|---|---|---|---|---|---|
| Apparel | 57,100 | 44.4% | 22.7% | ~100% ("fashion 100% own brand") | n/a |
| General merchandise | 36,802 | 28.6% | 22.2% | 73–74% | +300–400 bps vs national brands [HSIE] |
| FMCG | 34,804 | 27.0% | 25.4% | 35% of value, **60% of volume** | +10 pp [HSIE] |
| Total own brands | | **74.1%** FY26 (73.1% FY25); 72.5% Q2 FY27 [PPT-Q2] | | | |

- BRSR26 confirms the mix as 44/29/27. Q2 FY27 was 40.5/29.6/29.7 (the festive shift pulled apparel down).
- **Category gross margins are not disclosed. These are estimates.** Method: solve GM = Σ(mix × category GM) = 28.4%, with FMCG anchored at a DMart-like ~14–16% on national brands (VMM gets +10 pp on 35% of FMCG value, so FMCG ≈ 0.65×15% + 0.35×25% ≈ 18.5%). GM assumed at ~30–32%. That makes apparel ≈ (28.4 − 0.27×18.5 − 0.286×31)/0.444 ≈ **33–34%**. **Confidence: unverified.** Re-solve when any quarter gives a category GP.
- **Mix shift is the real gross-margin lever.** Opening price points fell from 60% of sales four years ago to 20% `[HSIE]`. Management says GM gains will be "reinvested in product quality". Read that as a stated **cap** on gross margin.
- Brand concentration: Brink (apparel) alone was about ₹1,000 cr in FY25 `[ELARA]`.

### 1.4 Store P&L (average FY26 store, ₹ per year)
Method: company FY26 line items `[AR26]` ÷ 745.5 average stores and ÷ 12.83 mn average sq ft. Company-level lines include head-office and distribution-centre costs, so this is a **fully loaded** store. A "four-wall" store P&L would be about 1–2 pp better.

| Line | % of sales | ₹ lakh/store/yr | ₹/sq ft/yr | Comment |
|---|---|---|---|---|
| Revenue | 100 | 1,731 | 10,063 | |
| Gross profit | 28.4 | 492 | 2,860 | |
| Employee cost ex-ESOP | 5.25 | 91.0 | 529 | ₹678 cr; HQ included |
| Lease cash outflow (Ind AS 116 interest + principal) | 5.34 | 92.5 | 538 | **₹44.8/sq ft/month**, plausible for tier 2–3 rents |
| Short-term rent and warehousing | 0.52 | 9.0 | 52 | ~47% paid to promoter Samayat (§4.3) |
| Transportation | 1.99 | 34.4 | 200 | 28% paid to promoter Samayat |
| Power and fuel | 1.82 | 31.6 | 184 | |
| **Security charges** | **0.68** | **11.8** | **68** | ₹87.7 cr, outsourced (§2.4) |
| Manpower charges (outsourced) | 0.45 | 7.7 | 45 | |
| Housekeeping | 0.39 | 6.8 | 39 | |
| A&P | 0.53 | 9.2 | 53 | |
| Repairs, packaging, bank charges, other | ~1.7 | ~29 | ~170 | |
| **Pre-Ind AS, pre-ESOP EBITDA** | **9.8** | **~170** | ~990 | Company: ₹1,271 cr (EBITDA ₹18,836 mn − Ind AS 116 impact ₹6,127 mn) [AR26] |

### 1.5 Capex per store, payback, ROCE
- **Company claim** `[UDRHP]`: "average payback per store for new stores opened during FY2023 was 19 months … calculated as CapEx invested in stores opened during FY2023 divided by EBITDA generated by these stores until FY2024." JM Financial estimates about 21 months. A blog says ₹23 cr capex per store, which cannot be right for an 18k sq ft leased box: it fails the sanity check.
- **The definition hides two things.** (a) It is *cumulative* EBITDA up to a date, which is not a steady-state payback. (b) It does not say whether EBITDA is before or after rent. If it is Ind AS 116 EBITDA, rent (5.3% of sales) is excluded and payback is flattered by roughly 35% (pre-Ind AS EBITDA is about 0.67× Ind AS EBITDA). **Status: open.** Ask IR, or check the RedSeer page (p.128) of the RHP.
- **Capex per new store, estimated two ways:**
  1. Top-down: FY26 capex ₹322 cr `[HSIE cash flow]` ÷ about 105 gross openings (net 99 + 6 closures `[PPT-Q2]`) = **₹3.1 cr, an upper bound** (it includes DC, IT, RFID and refurbishments).
  2. Bottom-up: 17k sq ft × ₹1,200–1,600 per sq ft fit-out (value-retail benchmark) = ₹2.0–2.7 cr. Add net working capital: inventory about ₹2.5 cr per store (₹2,017 cr ÷ 795) minus payables about ₹2.0 cr (₹1,619 cr ÷ 795), so about ₹0.5 cr. **Total ≈ ₹2.5–3.2 cr.**
  - At a mature store's ~₹1.7 cr fully loaded pre-Ind AS EBITDA (about ₹2 cr four-wall), payback is **about 15–23 months**. That is consistent with the claim, *if* the store reaches network-average density in year 1. New stores in new states usually don't, so the true marginal payback is likely longer. A ground check can test this (§5).
- **Goodwill distorts ROCE.** Goodwill is ₹4,284 cr = 37% of total assets and 58% of equity `[AR26]`, left over from the 2018 PE buyout. Reported ROE is 12.2% and ROCE 15.2% `[SCR]`. Return on tangible equity is about **27%** [EST: PAT ₹839 cr ÷ (₹7,413 − 4,284) cr]. HSIE puts ex-goodwill ROIC at 57%.

### 1.6 Same-store sales growth and cannibalisation
- SSSG: FY25 12.3%, FY26 **11.0%** `[AR26]`. Q2 FY27 5.4% (about 9% adjusted for an 18-day festive shift), H1 FY27 7.7% `[PPT-Q2]`.
- **What drives it** `[CC-Q3FY26]`: about 70% from transactions (number of bills) and 30% from bill value. Bills grew about 10% YoY like-for-like `[ELARA]`. Average bill was ₹875 (FY25). Loyalty members: 18.1 cr registered, and **95% of revenue comes from loyalty customers** `[PPT-Q2]`. That gives VMM a large first-party data asset, and it means the "registered" count is cumulative and inflated (anyone who gives a phone number at checkout is counted).
- **SSSG definition:** stores operational for at least 15 months at the start of the quarter, *excluding* stores closed for "refurbishment, area reduction, or any one-off reason" `[PPT-Q2]`. Ask: how many stores are excluded each quarter? Excluded stores can quietly hold the weak ones.
- **Cannibalisation:** UP/Haryana are being deepened with small-format stores. Management claims the same revenue per sq ft `[HSIE]`. That is not yet testable from disclosures, because SFS are not split out (only 18 stores). The test is North-region revenue per store, which HSIE notes is still the highest. "West is the only region to contract in FY26" `[HSIE]`.

---

## 2. Cost structure line by line

### 2.1 FY26 P&L walk `[AR26]` (₹ mn)
Revenue 1,29,063 → COGS 92,382 (GM 28.4%) → employee 7,283 (of which ESOP 501) → other expenses 10,561 → EBITDA 18,836 (14.6%) → D&A 6,734 (of which ROU amortisation 4,792) → finance cost 1,715 (of which lease interest 1,697; **bank interest ≈ ₹18 mn**) → PBT 11,250 → PAT 8,392.

### 2.2 The lease model (asset-light) and Ind AS 116
- **All stores are leased** `[UDRHP p.140]`. DMart, by contrast, owns most stores (memdb `case_study:false-alarm-dmart-permanent-high-pe`).
- Lease liabilities ₹1,988 cr (current ₹581 cr + non-current ₹1,407 cr) `[AR26 n.33]`. **This is the whole of screener's "Borrowings: ₹1,988 cr". Bank debt is zero** (HSIE: total debt nil since FY24).
- Total lease cash outflow FY26 ₹689 cr (5.3% of sales). P&L lease cost under Ind AS 116 is ₹716 cr (ROU amortisation 479 + interest 170 + short-term rent 67).
- Lease maturity: <1 year ₹621 cr, 1–5 years ₹1,618 cr, >5 years **only ₹211 cr**. These are short contracts, which gives flexibility to exit bad stores but means frequent re-pricing. Management says rentals are "not seeing significant pressure" and there was "no significant renegotiation" `[CC-Q3FY26]`, `[CC-Q2]`.
- **Pre-Ind AS EBITDA margins:** FY22 7.5% → FY24 8.3% → FY25 9.1% → FY26 9.8% `[HSIE]`. Q2 FY27 fell to 7.7% (from 8.5%) because of operating deleverage and wages.

### 2.3 Employees: the minimum-wage engine (the key "security-guard depth" finding)
**Primary data `[BRSR26]`:**
- 21,913 permanent employees (FY25: 18,029) across 813 "plants" (stores + DCs). That is **about 27 per location**. "Other than permanent" employees and workers are **0**, so guards, housekeeping and loaders sit with agencies (§2.4).
- **66% of employees (14,562) are paid exactly the statutory minimum wage.** That is 89% of women and 55% of men (FY25: 70%).
- Median annual remuneration: men ₹1,63,245 (₹13.6k/month), women ₹1,02,402 (₹8.5k/month). The KMP median is ₹3.61 cr.
- **Attrition 84%** (FY25 74%, FY24 90%).
- Women's share of the gross wage bill: 23%. MD pay is 215× the median `[AR26]`.

**Estimates:**
- Average cost per employee ex-ESOP = ₹678 cr ÷ 19,971 average employees = **₹28.3k/month** [EST]. The median is far below the mean because (a) managers, DC and HQ staff pull the mean up, and (b) **with 84% attrition, many people are on the rolls for only part of the year, so "median *annual* remuneration" understates the monthly wage.** Women's ₹8.5k median is *below* every state minimum. It most likely reflects part-year tenure, not underpayment. That is a classic "looks bad, probably benign" item; the check is in the next bullet.
- Check with state wage notifications (unskilled, monthly, from 1-Apr-2026): **UP** ₹12,356 (other districts) / ₹13,006 (Nagar Nigam) / ₹13,690 (Noida/Ghaziabad), up from about ₹11,313 (SCC Online, Business Today, Apr-2026). **Haryana** ₹15,220, up from ₹11,275, a **+35%** step (Haryana notification 2/25/26-2 Lab./914/2026, multiple news sources). Gross ₹12.4–15.2k plus PF 12%, ESI 3.25%, statutory bonus 8.33% and leave gives **CTC ≈ ₹15.5–19k/month for a cashier or floor associate**. Job-portal data for VMM/V-Mart cashiers and associates is ₹12–18k/month (AmbitionBox, small samples, single-source), which is consistent.
- **Sensitivity.** Minimum-wage-linked cost pool ≈ on-roll minimum-wage staff (14,562 × ~₹2.0 lakh/yr CTC ≈ ₹290 cr) + outsourced security, manpower and housekeeping (₹196 cr) ≈ **₹490 cr ≈ 3.8% of sales** [EST]. A 15% blended wage step (Haryana +35%, UP +9–21%, other states smaller) = about ₹70–75 cr = **about 55–60 bps of EBITDA margin, roughly 6% of pre-Ind AS EBITDA**.
- **This happened in Q1/Q2 FY27.** Employee cost rose ~25% YoY ex-ESOP against revenue +14% `[CC-Q2]`. The CFO said "significant increase in minimum wages", which hit in Q1, plus new stores. He said 8–10% SSSG is "good enough to offset" `[CC-Q2]`.
- **Broader lesson:** for a minimum-wage employer, **state labour-department gazettes are a leading indicator for margins.** UP said a permanent wage board would follow the interim revision, which means another step may be coming. The four Labour Codes (Code on Wages 2019) are now the legal basis, and UDRHP risk factor 2.4 flagged the "deemed wages" (50% rule) effect on PF and gratuity.

### 2.4 Security guards (the literal "security-guard depth")
- **Security charges ₹87.65 cr in FY26** (FY25 ₹71.87 cr, +22% against revenue +20%) `[AR26 n.24]`. Separate lines: manpower ₹57.5 cr, housekeeping ₹50.4 cr. With zero non-permanent staff in BRSR, these are agency contracts.
- **Per store:** ₹87.65 cr ÷ 745.5 average stores = **₹98k per store per month** [EST]. DCs are included, so per store it is slightly lower.
- **Guards per store, triangulated** [EST]. An agency bills about minimum wage (UP FY26 ≈ ₹11.3k, Haryana ≈ ₹11.3k, before the April-26 hikes) + ~29% statutory load + 8–12% agency margin + uniforms ≈ **₹16–17.5k per guard per month**. ₹98k ÷ ₹16–17.5k ≈ **5.5–6 guard-equivalents per store**, for example two shifts × three posts (entrance/bag counter, exit/bill check, floor). **A ground check should count them (§5).** After the April-2026 hikes, the same staffing costs about 10–35% more, so security alone adds roughly ₹10–20 cr a year in FY27.
- **Context:** the May-2025 viral "VMM security guard recruitment" memes (UPSC-style exams) were *not* company-initiated. Per ThePrint (24-May-2025), the marketing team said "we don't know where it came from". **Lesson: social-media "ground data" can be fabricated. Use filings first, then a physical check.**
- Shrinkage: VMM claims only 1 insured theft a year (₹0.6–2.2 mn) `[UDRHP]`. That number is meaningless, because minor theft is "not tracked". Inventory shrinkage provisioning is a Key Audit Matter in AR26. Per-store security spend of about 0.7% of sales is the insurance premium against shrinkage. Ask: shrink as % of sales, versus a typical 0.5–1.5% in Indian apparel/value retail (unverified benchmark).

### 2.5 Working capital and suppliers
| Days (HSIE basis, on sales) | FY22 | FY23 | FY24 | FY25 | FY26 |
|---|---|---|---|---|---|
| Inventory | 79 | 72 | 60 | 63 | 57 |
| Payables | 95 | 72 | 50 | 50 | 46 |
| Cash conversion cycle | −9 | 6 | 19 | 13 | 11 |
(Screener on COGS basis, FY26: inventory 80, payables 64.)

- Payables fell faster than inventory (95→46 days). Possible reasons: deliberately paying contract manufacturers faster for better prices (a positive), MSME 45-day payment rules (Sec 43B(h) from FY24), or post-buyout normalisation. **Open question** for management and the vendor scuttlebutt (§5).
- All manufacturing is outsourced to third-party contract manufacturers `[BRSR26]`. Vendors absorb about 50% of raw-material inflation `[HSIE]`. That shows purchasing power, and it is also a pressure point on vendors: ask them.
- Supply chain `[HSIE]`: one central DC (6–7 days of inventory) plus 17 third-party regional warehouses of 60–65 stores each, capacity about 1,000–1,100 stores. VMM is moving to 4 hubs; a 600k sq ft Haryana DC is live. RFID tags cost ₹15 each, on items above ₹200, reused 10–15 times.

---

## 3. Customer and ground reality
- **Catchment:** 52% of stores are in Tier III towns (<200k population) `[PPT-Q2]`. A Tier III town of 100–200k supports one ~17k sq ft store at ₹17 cr/year, which is about ₹850–1,700 per head per year of catchment. Plausible only if the store draws from surrounding villages (40–50 km radius on market days). Ground check: ask shoppers where they came from.
- **Ticket and footfall** [EST]: ₹17.3 cr/store ÷ ₹875 average bill ≈ **~19,800 bills per store per month ≈ 650/day**, peaking on weekends and festivals. At about 30–40% conversion (typical value apparel/general retail; *unverified* benchmark), footfall is about 1,600–2,200 per day. That ties to security: 1–2 exit checkers per shift for 650 bills is consistent.
- **Competition:**
  - Kirana and unorganised traders are the main share donors. Management says the "largest bucket" of growth is new customers from "mom-and-pop stores" `[CC-Q3FY26]`.
  - Zudio (Trent) is the apparel overlap in Tier I/II. *Zudio store count and density were not checked this session* (open).
  - V2 Retail (founded by the original Vishal founder, see below) and V-Mart (VMART) compete head-on in Tier II/III North and East.
  - DMart overlaps in FMCG only in larger towns.
  - **Quick commerce:** VMM runs its own "quick commerce" from stores: 781 stores, 1.52 cr registered users, about 5% of revenue, a 2-hour SLA, roughly cash break-even `[PPT-Q2]`, `[HSIE]`. The mix is 70% grocery, so it dilutes gross margin. In metros quick commerce is 1.5–2% of store revenue; in Tier II/III, 3–4% `[ELARA]`.
- **Brand history matters for the consumer and the landlord.** The original Vishal Retail (founder Ram Chandra Agarwal) went into CDR in 2009 with about ₹730 cr debt. The business went to TPG/Shriram in 2010–11, then to Kedaara/Partners Group in 2018 (deal size unverified). Agarwal now runs V2 Retail. The same brand has failed once on debt-funded expansion. Today's version has no bank debt and leased stores, which is a different risk profile (Business Standard 2009 "Vishal promoter to exit in debt recast"; V2 Retail FY26 AR).

---

## 4. Ownership, governance, incentives

### 4.1 No founder-promoter. The "promoter" is a PE vehicle.
- Promoters: Samayat Services LLP (an SPV of Kedaara Capital and Partners Group) and Kedaara Capital Fund II LLP `[UDRHP]`. Pre-IPO stake was 96.55%.
- Sell-downs (screener promoter %): IPO Dec-2024, a pure ₹8,000 cr OFS, 28.7× subscribed → 74.55%. Jun-2025 block of 19.36%, ₹10,220 cr → 54.2%. Early 2026, 14% bulk deal of ₹7,635 cr at ₹117 (an 8% discount) → **40.0% (Sep-26)**. Total realised ≈ **₹25,855 cr**, none of it to the company.
- Absorbed by DIIs (9.9% → 36.5%) and FIIs (6.6% → 18.8%). Retail holders fell from 9.33 lakh to 6.43 lakh `[SCR]`.
- Supply overhang ≈ 40% × ₹42,852 cr ≈ ₹17,000 cr at CMP. At 1–1.5 blocks a year that is 2–3 more years of periodic supply. Management says the sponsors "intend to remain invested for the long term" `[HSIE]`. PE sponsors exit by design, so that statement should be treated as unverified.
- **Pledge: 0** `[HSIE]`.

### 4.2 The CEO is the "founder". Incentives.
- Gunender Kapur (ex-Unilever, joined 2019/20, MD & CEO from 27-Jun-2024) was **redesignated "Founder, MD & CEO"**, reappointed to Aug-2031 (age ~65) `[AR26 AGM notice]`.
  - Fixed pay ₹6.30 cr, cap ₹10 cr, with variable pay tied to EBITDA.
  - Managerial remuneration recognised: ₹30.3 cr FY26 / ₹35.1 cr FY25 `[AR26 n.35]`, including ESOP perquisites.
  - Unvested options: 79.3 lakh at ₹35 (Jun-2024) plus **4.68 crore at ₹102.60 (granted 21-Aug-2026)** `[NSE filing]`. That is about 1.0% of the equity. At CMP ₹91.5 the new grant is **under water**. His wealth is now tied to the share price above ₹102.6, which aligns him with outside holders. Dilution is about 1% plus the older pools: 5.6 cr options were outstanding at Mar-26 `[AR26]`.
- **Management churn:** COO Manoj Kumar resigned 16-Jul-2026 (left 11-Sep), and Sashi Gumma was appointed Chief of Operations 15-Jun-2026. Independent director Soumya Rajan resigned 2-Nov-2026, citing "professional commitments". A new ID is being appointed by postal ballot (vote ends 17-Dec-2026) `[NSE announcements]`. Not alarming alone; record and track.
- **Board:** 8 directors, 3 Kedaara/Partners nominees (Tandon, Sharma, Gupta), Sanjeev Aga non-independent, 2–3 independents `[AR26]`.

### 4.3 Related-party logistics: the item a screen never shows
- **Samayat Services LLP, the PE promoter vehicle, is also VMM's transporter and warehouse operator** `[UDRHP risk factor 16]`, `[AR26 n.35]`.

| | FY22 | FY23 | FY24 | FY26 |
|---|---|---|---|---|
| Transport paid to Samayat (₹ mn) | 142.9 | 223.1 | 255.9 | **721.0** |
| As % of total transport | 13.8% | 15.9% | 16.2% | **28.1%** [EST: 721/2,563] |
| Warehousing paid to Samayat (₹ mn) | 106.9 | 119.8 | 163.7 | **311.7** |
| As % of rent and warehousing | 61.9% | 59.7% | 54.9% | 46.6% |

  Q1 FY25 transport share was 22.3%. Rishay Services LLP (admin and facility management) and Rishanth Services LLP (quality control) also bill VMM: ₹7.3 cr in FY26.
- About ₹103 cr a year flows to the controlling shareholder's entity. That is about 8% of pre-Ind AS EBITDA, and the transport share has doubled since FY22.
- **Benign version:** a legacy logistics arm carved out at the 2018 buyout, priced at arm's length (the audit committee approves RPTs, and the auditor gave no qualification).
- **Malign version:** a margin-extraction channel that survives the PE exit or is sold with it.
- **Open questions:** (1) What happens to these contracts when Samayat's stake drops below 20%? (2) Rates per km and per sq ft against VMM's non-related transporters, which the RHP says are hired "on a needs basis" without agreements. (3) Who owns Samayat's trucks and warehouses? Use MCA filings of Samayat Services LLP. **Grade: soft flag, open** (not a hard disqualifier; there is no sign of diversion).

---

## 5. Ground check (scuttlebutt): task list for one person visiting 3 stores
Pick stores to test the thesis, not for convenience:
- **Store A:** a mature Tier III store in UP/Haryana, open 5+ years.
- **Store B:** a store opened in the last 12 months in a *new* state (Kerala, Gujarat or Maharashtra).
- **Store C:** one of the ~18 small-format (~8k sq ft) stores in UP/Haryana, ideally within 5 km of a large store, to test cannibalisation.

Visit each twice: a weekday 11:00–13:00 and a Saturday 17:00–20:00. Total about 2 days including travel.

**A. Count (numbers only, no opinions)**
1. Billing counters open vs installed; queue length at 15-minute intervals; time one checkout.
2. **Bills per hour:** watch one counter for 20 minutes, count receipts, multiply by counters open. Compare with my estimate of ~650 bills/day per store (~55–80 per hour at peak).
3. Footfall at the entrance for 15 minutes (clicker), to compute conversion = bills ÷ footfall.
4. **Security guards:** count posts (entrance, bag counter, exit/bill-check, floor, parking). Read the agency name on the uniform; ask one guard their shift hours, monthly in-hand pay and agency. Test the estimate of 5.5–6 guard-equivalents and ~₹16–17.5k billed per guard.
5. Staff on the floor per 1,000 sq ft, and the ratio of uniformed VMM staff to agency staff.
6. Basket composition at the exit: share of bags that are apparel, FMCG only, or mixed.

**B. Price and product**
7. A basket of 15 fixed SKUs (5 apparel opening-price-point items, 5 own-brand FMCG, 5 national-brand FMCG). Price them at VMM, the nearest V-Mart/V2, the nearest kirana, and on Blinkit/Zepto/JioMart for that PIN code. Repeat the same basket every quarter.
8. Own-brand versus national-brand shelf space in FMCG (count facings in atta, detergent, oil, biscuits). Test the "35% of value, 60% of volume" claim.
9. Opening-price-point share: how many items in men's shirts are under ₹199, ₹199–499, and over ₹499? Test the "60% → 20%" premiumisation claim.
10. Newness: tags with season codes; ask staff how often new stock comes.

**C. People** (ask politely; never pay for information or ask for anything confidential)
11. Store staff: tenure, in-hand pay, whether it rose in April 2026 (wage notification), training, which incentive they chase. Test the 84% attrition figure: how many colleagues left in the last 3 months?
12. Store manager (if willing): how they rank vs other stores in the cluster; whether the small-format store nearby took footfall.
13. Two or three neighbouring shopkeepers (kirana, cloth shop, mobile shop): did footfall in the market go up or down after VMM opened? Did they cut prices?
14. Landlord or local broker: rent per sq ft for a similar ground-floor plus first-floor box; lock-in and escalation (5%/year or 15% every 3 years?). Compare with my estimated ~₹45/sq ft/month.
15. Ten shoppers: town or village of origin and distance; how often they come; what they buy here vs elsewhere; whether they use the VMM app or Blinkit.
16. A truck or warehouse driver if visible at the back gate: whose vehicle (Samayat, or the agency name), and trips per week. Relevant to the related-party question in §4.3.

**D. Physical state**
17. Housekeeping, fitting-room queues, out-of-stocks in the top 20 FMCG SKUs, and damaged or soiled apparel (a shrinkage proxy). Electronic article surveillance and CCTV density; RFID tags visible?
18. Parking (two-wheelers count), road access, and the nearest competitor's distance (Google Maps).

**Output template:** one table per store (counts), one price sheet, and 5 quotes. Then a "surprises vs model" list: each estimate in §1–3 marked confirmed, contradicted or no read. **Price every observation against a number in this file.** A visit not tied to a model number is tourism.

---

## 6. Numbers that look bad but may be benign, and that look good but may mislead
Format per `insight:flag-override-template`. "Cleared" requires external evidence, and a management explanation alone stays OPEN (L10, L12).

| Flag | Context questions | Evidence that clears | Evidence that confirms | Verdict now | What changes my mind | Review |
|---|---|---|---|---|---|---|
| **"Borrowings ₹1,988 cr" on screener** (looks bad) | Bank debt or leases? | AR26 n.33: lease liabilities = ₹1,988 cr exactly; bank interest ≈ ₹1.8 cr; HSIE total debt nil | — | **Cleared (benign)** | Any bank/CP borrowing appears | Each AR |
| **ROE 12%, ROCE 15%** (looks bad) | Goodwill? | Goodwill ₹4,284 cr = 58% of equity; ROTE ≈ 27% | Goodwill impairment test failing (KAM) | **Cleared (accounting)** | Impairment; buyback at premium | FY27 AR |
| **P/E 47.7** (looks bad) | Own median? implied growth? | EPS +30%/yr FY24–26; P/E has fallen from ~76 at IPO-year | P/E vs own short history; SSSG falling below 8% | **Open** (only 2 years of listed history; own-median test impossible) | 4 quarters of SSSG <8% | Q4 FY27 |
| **Women's median pay ₹8.5k/month < minimum wage** (looks bad: underpayment?) | Part-year tenure with 84% attrition? | 89% of women recorded as paid *equal to* minimum wage [BRSR26]; median is annual, part-year | Labour-court cases; ground interviews showing pay < minimum | **Open, likely benign** | Staff interviews (§5 item 11) | Next visit |
| **Payables days 95→46** (looks bad: lost supplier power?) | MSME 45-day rule? Deliberate early pay for price? | GM stable/up (27.2%→28.4%) while paying faster suggests a trade-off by choice | GM falling while payables shorten | **Open** | Vendor interviews | FY27 |
| **PE promoter selling 58% in 18 months** (looks bad) | PE fund life; price vs IPO; who bought | Sales at ₹110–117 > IPO ₹78; absorbed by DIIs; business metrics unchanged | Sales accelerating at falling prices; insiders/management selling | **Open (supply, not quality)** | Management selling own shares | Each quarter |
| **SSSG 11% / "double-digit north star"** (looks good) | Definition: what's excluded? | Bills +10% (volume-led) | Rising count of excluded "refurbishment/area reduction" stores; SSSG holds while revenue/sq ft falls | **Open** | Disclosure of excluded-store count | Q3 FY27 |
| **19-month store payback** (looks good) | Pre- or post-rent EBITDA? cumulative definition? | Our triangulation 15–23 months *at mature density* | EBITDA is Ind AS 116 (rent excluded); new-state stores at lower density | **Open** | RHP p.128 or IR answer | Before any use |
| **EBITDA margin 14.6%** (looks good) | Ind AS 116? | Pre-Ind AS 9.8% is the real number | — | **Use 9.8%** | — | — |
| **Gross margin 28% vs DMart 15%** (looks good) | Per sq ft? | — | GP/sq ft ₹2,860 vs DMart ~₹5,000 | **Misleading in isolation** | — | — |
| **18.1 cr loyalty "customers"** (looks good) | Cumulative registrations? | — | Definition counts any phone number given at checkout ever | **Misleading as a customer count**; "95% of revenue from loyalty" is the useful part | Active-member disclosure | — |
| **Related-party logistics ~₹103 cr/yr to Samayat** (looks fine on a screen; is not visible) | Arm's length? post-exit fate? | Audit committee approval; no qualification | Share rising (13.8%→28.1% of transport); rates above third-party | **Open, soft flag** | Rate comparison; contract terms at exit | FY27 AR |
| **Employee cost +25% vs revenue +14% (Q2 FY27)** (looks bad) | One-off wage step or structural? | Wage notifications are discrete steps (Apr-2026); CFO says no further Q2 increase | UP permanent wage board; another step in FY28 | **Open, quantified (~55–60 bps)** | Next notifications (Oct VDA revisions) | Q4 FY27 |

Count of open soft flags: about 8, which is above the 3+ rule. Under our rule this means *no position without a variant view*. This is a statement about our evidence, not about the company.

---

## 7. What this exercise taught (method, not stock)
1. **The deepest data was free and audited.** BRSR (minimum-wage share, attrition, headcount, median pay) plus annual-report note 24 (security, manpower, housekeeping) plus note 35 (related parties) beat every broker report on cost drivers. Most investors never open the BRSR.
2. **"Security-guard depth" is a ratio, not a curiosity.** Guard cost per store ÷ state minimum wage → guards per store → a ground-checkable number. The same chain links wages to margin sensitivity.
3. **Every company-defined metric (SSSG, payback, loyalty customers, "operating EBITDA") needs its footnote read.** Three of the four had a definitional catch.
4. **Peers expose what the company won't.** DMart's density shows what VMM's margin hides. V2 Retail's density collapse shows the rollout risk VMM has not yet shown.
5. Time spent: about 70% on primary documents, 20% on estimates, 10% on broker notes. Broker notes were most useful as a **map of what management said in closed analyst meets** (category GM premiums, DC capacity, RFID cost).

## Open items (for a later pass)
- Zudio/Trent density and store counts (not checked); DMart owned-vs-leased split and DMart security cost per store (DMart AR note).
- RHP p.128 payback definition; the RHP's tables (they are images, so OCR them).
- MCA filings of Samayat Services LLP: assets, trucks, other clients.
- Store-level revenue for new-state cohorts (ask IR; or infer from regional revenue ÷ regional stores each quarter).

## Sources
- VMM FY26 Annual Report: https://nsearchives.nseindia.in/annual_reports/AR_30532_VMM_2025_2026_A_25227289_24082026123820.pdf
- BRSR FY26: https://nsearchives.nseindia.com/corporate/VMMP2024_24082026124747_Disclosure_BRSR_VMM.pdf ; BRSR FY25: https://nsearchives.nseindia.com/corporate/VMMP2024_03092025124705_Disclosure_BRSR_2025_VMM.pdf
- UDRHP-I (17-Oct-2024): https://nsearchives.nseindia.com/corporate/VMML_17102024173420.pdf
- Q2 FY27 presentation: https://nsearchives.nseindia.in/corporate/VMMP2024_21102026131308_Disclosure_Investor_Presentation_VMM_Oct_2026.pdf ; transcript: https://nsearchives.nseindia.in/corporate/VMMP2024_26102026130822_Disclosure_Transcript_VMM_Oct_2026.pdf
- Q3 FY26 transcript: https://bsmedia.business-standard.com/_media/bs/data/announcements/bse/30012026/40b6be0c-59be-456b-867a-4974f6e06301.pdf
- ESOP grant 21-Aug-2026: https://nsearchives.nseindia.in/corporate/VMMP2024_21082026203319_Intimation_of_Grant_of_Stock_Options_August_21_2026.pdf
- Resignations: https://nsearchives.nseindia.in/corporate/VMMP2024_02112026181257_Final_Intimation_to_Stock_Exchanges_Resignation_of_Soumya.pdf ; https://nsearchives.nseindia.in/corporate/VMMP2024_11092026183331_Intimation_to_Stock_Exchanges_Resignation_of_Manoj_Kumar.pdf
- HDFC Securities 25-Sep-2026: https://www.hdfcsec.com/hsl.docs//Vishal%20Mega%20Mart%20-%20Update%20-%20Sep26%20-%20HSIE-202609251422114474305.pdf
- Elara May-2025: https://bsmedia.business-standard.com/_media/bs/data/market-reports/equity-brokertips/2025-05/17461767390.58584100.pdf
- screener.in: https://www.screener.in/company/VMM/consolidated/ , /DMART/consolidated/ , /V2RETAIL/consolidated/
- UP minimum wages Apr-2026: https://www.scconline.com/blog/post/2026/04/18/uttar-pradesh-revises-minimum-wages-2026/ ; https://www.businesstoday.in/latest/economy/story/up-hikes-interim-minimum-wages-from-april-1-noida-ghaziabad-workers-get-highest-21-jump-525571-2026-04-14
- Haryana minimum wages Apr-2026: https://www.angelone.in/news/personal-finance/haryana-minimum-wage-hike-2026-workers-get-35-salary-increase-across-categories ; https://www.lokmattimes.com/national/haryana-govt-revises-minimum-wages-new-rates-effective-from-april-1-2026/
- Guard meme story: https://theprint.in/feature/everyones-joking-about-becoming-a-vishal-mega-mart-guard-memes-say-its-better-than-upsc/2635985
- Job-portal pay (low confidence): https://ambitionbox.com/salaries/vishal-mega-mart-salaries/cashier ; https://ambitionbox.com/salaries/vishal-mega-mart-salaries/guard
- DMart FY26 (500 stores, 20.58 mn sq ft, ₹33,422/sq ft): https://scanx.trade/stock-market-news/companies/dmart-reports-strong-fy26-financial-performance-with-revenue-growth-of-15-9/39272599
- V2 Retail Q2 FY27 transcript: https://nsearchives.nseindia.com/corporate/V2RETAIL_06112026144709_Concall_Transcript_V2_Retail_Ltd_Q2H1FY27_06Nov2026.pdf
- Vishal Retail 2009 CDR: https://www.business-standard.com/article/companies/vishal-promoter-to-exit-in-debt-recast-109110100040_1.html
- PE sell-downs: https://www.freepressjournal.in/business/kedaara-capital-partners-group-offload-14-stake-in-vishal-mega-mart-for-7635-crore-via-bulk-deal ; https://upstox.com/news/market-news/stocks/vishal-mega-mart-block-deals-samayat-services-llp-sells-19-6-stake-for-10-220-crore-check-who-bought-the-shares/article-174194
