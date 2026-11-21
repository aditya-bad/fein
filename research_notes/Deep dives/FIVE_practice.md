# Five Below (US: FIVE): practice deep dive #3 at "security-guard depth" (first US filer)

**Date:** 2026-11-21 · **Purpose:** the third test of `deep_dive_protocol.md`, and the first on a **US filer**. The aim is to adapt the protocol to SEC filings (10-K, 10-Q, 8-K, DEF 14A, Form 4, 13F, 13G). Run #1 (VMM) was an Indian retailer; run #2 (Cummins India) was an Indian manufacturer/MNC subsidiary.
**This is test material (lesson L9). There is no buy/sell/watchlist verdict and none should be read in.** It is research, not investment advice.
**Open paper call on this stock:** `thesis:paper-call:US-FIVE:fy2026-comps-11pct-plus` (P = 0.58 that FY2026 comps ≥ +11.0%). This file does **not** change that call. Relevant facts are noted in §9.

Every number carries a source tag. Every estimate shows its method.
- `[10K25]` = Form 10-K for FY2025 (year ended 31-Jan-2026), filed 19-Mar-2026, acc. 0001177609-26-000010 · `[10K24]` = 10-K FY2024, filed 20-Mar-2025
- `[PR-Qn FYyy]` = earnings press release, the Ex-99.1 of an Item 2.02 8-K. Q1 FY25 = 4-Jun-2025, Q2 FY25 = 27-Aug-2025, Q3 FY25 = 3-Dec-2025, Q4 FY25 = 18-Mar-2026, Q1 FY26 = 3-Jun-2026, Q2 FY26 = 2-Sep-2026 · `[PR-HOL25]` = holiday sales 8-K, 12-Jan-2026
- `[8K-date]` = other 8-Ks: officer changes (Item 5.02), the ABL amendment (Item 1.01, 14-Oct-2026), the cyber incident (Item 8.01, 22-Jul-2026)
- `[CC-Q2FY26]` = Q2 FY26 call, 2-Sep-2026. Taken from an automated transcript (webull) plus the Nasdaq call-highlights summary. **Single-source; names are garbled in places.**
- `[F4]` = Form 4s parsed by `tools/sec_fetch.py insider FIVE --limit 80` · `[13F]` = `sec_fetch.py holdings13f` · `[13G]` = Schedule 13G/A primary_doc.xml
- `[XBRL]` = `sec_fetch.py facts` (companyfacts) for FIVE, OLLI, DG and DLTR
- `[WEB]` = secondary web summary, single-source unless stated · `[EST]` = my estimate, with the method shown in the same row
- Fiscal years: FY2025 = 2-Feb-2025 to 31-Jan-2026. FY2026 = 1-Feb-2026 to 30-Jan-2027.

Context only: FY25 close $191.64 `[10K25]`. Insider sales in Sep-2026 were at $241–255 `[F4]`. BlackRock's 13F implies ~$220 at 30-Sep-2026 [EST: $1,206.6M ÷ 5.495M shares]. No valuation work was done, by design.

---

## 0. Edge question first (rule zero)
1. **What the market already knows.** 15 analysts asked questions on the Q2 FY26 call `[CC-Q2FY26]`. Their topics, in order of frequency:
   - (a) comp durability and difficult comparisons (Lasser, Ciccarelli, Grom, Cattel);
   - (b) how marketing and product split the drivers of the top line (Koenig, Bellinger, McShane);
   - (c) what to do with the ~$170M of tariff refunds (Owens, Ma);
   - (d) the gross-margin bridge: fuel, shrink and tariffs (Kelly, Hamblin);
   - (e) new-store productivity (Boss), the Five Beyond reset cost (Feldman), and store layout (Heinbockle).
   - **Nobody asked about** (i) the split between direct imports and domestic vendors, and what happens to tariffs embedded in the *domestic-vendor* 60% (§4.3); (ii) occupancy per sq ft on the new leases (§4.4); (iii) whether the "$2M / $0.4M / ~1-year payback" model still matches capex per store (§3.3).
2. **The variable that would change value most if we knew it better than consensus.** **Steady-state store-level margin after the tariff cycle and the pricing reset.** It has three parts. (i) Merchandise margin net of tariffs and vendor pass-through. (ii) Whether traffic-led comps of +14–23% are a level shift or a cohort/trend spike; consensus debates this. (iii) Real new-store returns against the company's undefined "payback". Almost nobody models (iii).
3. **The layers most likely to reveal it.**
   - L3: 10-K store-model text, capex guidance and pre-opening cost.
   - L4: the 10-K lease note, the 10-K/10-Q non-GAAP reconciliations, and the sourcing paragraph.
   - L6: a fixed price basket and price-point counts in three stores.

For a US specialty retailer with no controlling shareholder, the money-to-the-parent question (L16) becomes **"what does the company define for itself, and what does it leave out"**. KPI definitions do the work that related-party notes did in India.

---

## 1. Map (L1): what is the unit?

### 1.1 The business in one paragraph
Five Below sells "trend-right" goods to tweens, teens and "the kid in all of us", "most priced at $5 and below". The category worlds are Candy, Style, Party, Room, Create, Tech, Sports and New & Now. A typical store holds 4,000+ SKUs. Sales mix FY25: leisure 44.5%, fashion & home 30.9%, snack & seasonal 24.6% `[10K25 Item 1]`.
- **Stores:** 1,921 at FY25 end in 46 states, **all leased**, ~4% in malls; the rest are in power, community and lifestyle centres. There are 2,022 stores at Q2 FY26 `[PR-Q2 FY26]`.
- **Openings:** 228 gross in FY24 and 157 gross / 150 net in FY25. About 150 net are planned for FY26, and a first "handful" in Puerto Rico in H2 2027 `[CC-Q2FY26]`.
- **Long-run target:** "more than 3,500 locations over time" `[10K25]`.
- **Sourcing:** ~1,000 vendors; none >5% of purchases; **~60% of purchases from domestic vendors** (FY24 and FY25 alike). "China [is] the single largest source of merchandise we import **and source from domestic vendors**" `[10K25 Item 1A]`.

### 1.2 Units to rebuild (retailer row of the table, adapted for the US)
| Unit | What it measures | Where the data is (US) |
|---|---|---|
| **Store** (sq ft, sales, crew, rent) | Four-wall economics and payback | 10-K Item 1 "new store model" paragraph; Item 7 "average net sales per store"; lease note; Item 1 human-capital headcount |
| **Ship center (DC)** | Capacity per store and per $ of sales | 10-K Item 1 "Distribution" and Item 2 Properties (sq ft, purchase price, opening dates) |
| **Price-point band** ($1–5 core vs >$5 "extreme value"/Five Beyond) | Margin mix and traffic | Not disclosed. Calls and ground check only |
| **Vendor channel** (direct import vs domestic vendor) | Tariff exposure and who carries it | 10-K sourcing paragraph (60/40); Item 1A wording; non-GAAP tariff-refund lines |

### 1.3 Peers with comparable units `[XBRL]`, FY ending ~Jan-2026
| | Revenue | Op. income | Op. margin | SBC % sales | Capex % sales |
|---|---|---|---|---|---|
| **Five Below** | $4.76B | $457M | 9.6% | 0.73% | 3.7% (FY24: 8.4%) |
| Ollie's (OLLI) | $2.65B | $298M | 11.2% | 0.49% | 3.8% |
| Dollar Tree (DLTR) | $19.40B | $1.65B | 8.5% | 0.30% | 5.8% |
| Dollar General (DG) | $42.72B | $2.20B | 5.1% | 0.21% | 2.9% |

Caveats:
- **COGS definitions differ.** FIVE puts store occupancy, distribution and buying *inside* COGS `[10K25 Item 7]`. Gross margins are therefore not comparable across peers without a reclassification. Compare operating margin instead, or rebuild "merchandise margin" yourself.
- DLTR's FY25 continuing operations exclude Family Dollar (sold in 2025). Treat its margin history with care. Peer COGS definitions were not verified in this run (open item).
- Ollie's is the closest *unit* peer: closeout pricing, leased boxes of ~30k+ sq ft, and a similar new-store "payback ~2 years" style of KPI. Its store size differs by ~3×, so compare per sq ft, not per store.

---

## 2. Reported financials, re-derived (L2)

### 2.1 Ten-year shape `[XBRL]` ($)
| FY end | Revenue | Op. income | Op. margin | Net income | Dil. EPS | CFO | Capex | FCF | SBC | Buybacks | Dil. shares |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Jan-17 | 1.00B | 114.0M | 11.4% | 71.8M | 1.30 | 106.6M | 44.8M | 61.8M | 12.0M | 0 | 55.1M |
| Feb-20 | 1.85B | 217.3M | 11.7% | 175.1M | 3.12 | 187.0M | 212.3M | −25.3M | 12.4M | 36.9M | 56.2M |
| Jan-22 | 2.85B | 379.9M | 13.3% | 278.8M | 4.95 | 327.9M | 288.2M | 39.7M | 25.8M | 60.0M | 56.3M |
| Feb-24 | 3.56B | 385.6M | 10.8% | 301.1M | 5.41 | 499.6M | 335.1M | 164.6M | 17.9M | 80.5M | 55.6M |
| Feb-25 | 3.88B | 323.8M | 8.4% | 253.6M | 4.60 | 430.6M | 324.0M | 106.7M | 15.6M | 40.2M | 55.2M |
| Jan-26 | 4.76B | 457.4M | 9.6% | 358.6M | 6.47 | 586.4M | 174.7M | 411.7M | 34.7M | 0 | 55.4M |

- **Two regimes.** FY16–FY21: revenue 2.9×, op margin 11–13%. FY22–FY24: a store-growth sprint (~200+ openings a year) while comps sank to −2.7% in FY24, op margin fell to 8.4%, and the CEO changed (§5.3). FY25–H1 FY26: a reset under the new CEO, with comps +12.8% (FY25), +22.7% (Q1 FY26) and +14.1% (Q2 FY26).
- **Diluted shares are flat over 10 years** (55.1M → 55.4M). Buybacks of ~$270M since 2018 `[10K25]` roughly offset SBC plus ESPP issuance (§5.2).

### 2.2 FY25 P&L walk `[10K25]` ($M)
Net sales 4,764.1 → COGS (incl. occupancy, distribution, buying) 3,049.5 (64.0%) → gross profit 1,714.7 (36.0%) → SG&A ex-D&A 1,065.2 (22.4%) → D&A 192.1 (4.0%) → **operating income 457.4 (9.6%)** → interest/other +23.0 → PBT 480.4 → tax 25.3% → net income 358.6.

Drivers of the comp: transactions +7.1%, ticket +5.3% (FY25). Ticket was the pricing reset ("price simplification last year" `[CC-Q2FY26]`). FY26 comps are "driven by traffic" `[CC-Q2FY26]`.

### 2.3 Quarterly turn (GAAP vs adjusted) `[PR-*]` ($M)
| Quarter | Net sales | Comps | GAAP GP % | Adj. GP % | Adj. op. inc. | Adj. op. margin | Main adjustment |
|---|---|---|---|---|---|---|---|
| Q1 FY25 | 970.5 | +7.1% | 33.4% | 33.8% | 59.6 | 6.1% | Retention awards, cost optimisation, lease acquisition |
| Q2 FY25 | 1,026.8 | +12.4% | 33.3% | 33.4% | 55.1 | 5.4% | Retention awards, lease acquisition |
| Q3 FY25 | 1,038.3 | +14.3% | 33.8% | 33.9% | 45.1 | 4.3% | Retention awards, lease acquisition |
| Q4 FY25 | 1,728.5 | +15.4% | 40.3% | 40.3% | 312.7 | 18.1% | Retention awards |
| Q1 FY26 | 1,285.6 | +22.7% | 37.2% | 37.2% | 154.8 | 12.0% | Retention awards |
| Q2 FY26 | 1,261.5 | +14.1% | **48.5%** | 35.6% | 113.2 | 9.0% | **IEEPA tariff refund −$163.6M in COGS** |

**The adjustment that matters:** Q2 FY26 GAAP operating income was $275.4M, of which **$163.6M was an IEEPA tariff refund credited to COGS**. That is 13.0% of the quarter's sales. GAAP diluted EPS was $3.99, adjusted EPS $1.68 `[PR-Q2 FY26]`. The FY26 GAAP EPS guide of $12.10–12.58 against an adjusted guide of $9.83–10.31 carries the same one-off. **Any screen that reads trailing GAAP EPS or GAAP gross margin for FIVE over the next four quarters is wrong by ~$2.3 per share.** This is a textbook "good-but-misleading" row (§8).

### 2.4 Balance sheet re-derived (31-Jan-2026) `[10K25]`
- **Cash and short-term investments:** $932.2M (723.7 + 208.5). At Q2 FY26, ~$1.2B including the refund `[CC-Q2FY26]`. **Funded debt: zero.** The ABL was doubled to $450M and extended to Oct-2031 on 14-Oct-2026 `[8K-20261014]`. It is a liquidity line for the Q3 inventory build, not a sign of stress. Historically it is drawn early in Q4 and repaid by year-end `[10K25]`.
- **Operating lease liabilities:** $2,032.2M (current 301.1 + long-term 1,731.0). The weighted-average remaining term is 7.0 years, at a 5.3% discount rate. **Lease-adjusted net debt ≈ +$1.1B** [EST: 2,032 − 932]. The "no debt" description is true only before leases.
- **Working capital flattered FY25 FCF:** payables +$108M and accrued salaries +$47.8M (19.7 → 67.5, the incentive-comp accrual). Capex also fell to $174.7M from $324.0M with 77 fewer openings. **FY25 FCF of $411.7M is a cyclical high.** On FY26 capex of $250–260M it would be ~$150M lower, before any working-capital reversal [EST].

---

## 3. Unit economics (L3)

### 3.1 The company's store model, quoted (definition audit, technique #10)
> "Our new store model assumes a store size of approximately 9,500 square feet that achieves sales of approximately $2 million in the first full year of operation and an average new store cash investment of approximately $0.4 million, including our store build-out (net of tenant allowances), inventory (net of payables) and cash pre-opening expenses. Our new store model targets an average payback period of approximately one year on our initial investment." `[10K25 Item 1]`. The same wording appears in `[10K24]`.

**What the definition leaves out:**
- **"Payback" has no stated numerator.** Is it four-wall EBITDA? After tax? After store D&A? None is defined. Neither is "first full year": is a store opened in October measured from the next February?
- **The investment is net of tenant allowances *and* of payables.** Vendor credit funds part of the inventory, so the denominator shrinks.
- **Network capex is excluded:** ship centres, systems and new-market marketing (§3.3).
- **The figures did not change between the FY24 and FY25 10-Ks**, although build costs and wages rose. Earlier 10-Ks were not checked (open item).
- **The model is a target ("assumes", "targets").** The realised claim is "average payback periods of approximately one year". It comes with no cohort table, which a US 10-K is not required to give.
- **Comparable sales** = stores open ≥15 full months, plus e-commerce. The definition excludes relocations and expansions in set windows `[10K25 Item 7]`. **"Average net sales per store" ($2.5M FY25, $2.3M FY24) includes only stores open before the start of the fiscal year**, so the newest, lower-volume class is left out by construction.

### 3.2 Store P&L rebuilt two ways [EST], FY25
| Line | Mature store (avg $2.5M) | New store (model $2.0M) | Method |
|---|---|---|---|
| Sales per sq ft | ~$265 (range $260–295 if older stores are 8.5–9.5k sq ft) | ~$210 (80% of mature) | $ per store ÷ model sq ft. Actual chain sq ft **not disclosed** |
| Merchandise margin (before occupancy, DC, buying) | ~51% | ~51% | 36.0% GAAP GM + occupancy ~9.4% + DC/buying/e-com shipping ~5–6% (DC/buying not disclosed; [EST]) |
| Occupancy (rent + CAM + taxes) | ~$225k (9.0%) | ~$225k (11.3%) | Net lease cost $449.9M ÷ ~1,846 avg stores = $244k incl. HQ and the Pedricktown DC; stores ~$225k |
| Store payroll | ~$375–425k (15–17%) | ~$340–380k (17–19%) | §4.2 |
| Other store opex (card fees, supplies, repairs) | ~3% | ~3.5% | Benchmark |
| **Four-wall EBITDA** | **~23% ≈ $575k** | **~18–19% ≈ $370k** | Bottom-up |
| Top-down cross-check | ~24–25% | — | Op. margin 9.6% + D&A 4.0% + corporate/marketing/SBC ~5–6% + DC/buying ~5.5% |

The two routes agree within ~2 pp, which passes technique #1. **On the company's $0.4M, a $370k year-one contribution gives a ~1.1-year payback. That is consistent with "~one year", but only if the $0.4M is right (§3.3).**

### 3.3 Capex per store: the triangulation gap (this run's main L3 finding)
- **Top-down.** FY26 plan: "approximately $100 million of our cash capital expenditure budget … to construct and open approximately 150 net new stores". The plan "exclude[s] the impact of tenant allowances" `[10K25 Item 7]`. That is **~$0.65M gross build-out per store** (≈155 gross openings).
- **Bottom-up of the company's $0.4M:**
  - build-out net of tenant allowances = X;
  - inventory net of payables ≈ $0.14M [EST: store inventory ~$250k × (1 − AP/inventory 43%)];
  - pre-opening ≈ $0.094M [$14.8M ÷ 157 openings `[10K25 n.1(t)]`].
  - So X ≈ $0.17M, which needs **tenant allowances of ~$0.48M per store (~74% of build-out).** That is implausible for a 9,500 sq ft strip-centre box. A 20–35% allowance is the usual range [benchmark, unverified].
- **If tenant allowances are ~$0.15–0.25M, the true cash investment is ~$0.6–0.7M,** and the payback is ~1.6–1.9 years at $370k. That is still excellent retail economics, but **50–75% longer than the headline**.
- **Network capex outside the model:** five ship centres cost ~$270M to buy, build or expand (Forsyth $42M + $21M, Conroe $56M, Buckeye $65M + $26M, Indianapolis $60M) `[10K25 Item 2]` and serve ~1,900 stores. That is **~$0.14M per store of DC capex**, plus systems (ERP, HCM).
- **The gap is the finding** (rule from technique #1, ">30% gap"). Questions for IR or the next transcript: (a) the average tenant allowance per new store; (b) whether the $0.4M is a current-cohort figure or legacy text; (c) the FY24 and FY25 cohort's first-year sales against $2M. Management says "new store productivity again outperformed" `[CC-Q2FY26]`. That is a comparison with their own model, not a number.

### 3.4 Lease economics per store `[10K25 lease note]`
- **FY25 new leases:** 141 new store leases with average ~10-year terms and **$258.0M of minimum payments** → $1.83M per lease → **~$183k a year minimum rent ≈ $19.3/sq ft** at 9,500 sq ft [EST].
- **Feb–Mar 2026:** 27 leases, $48.0M → $178k a year. That is flat, with no rent inflation visible.
- **Variable lease cost** (CAM, taxes, %-rent) is $103.4M, 23% of the $449.9M net lease cost. Gross occupancy is ~$24–26/sq ft [EST].
- **Cash vs expense:** cash lease payments of $316.9M < straight-line operating lease cost of $346.5M, because of free-rent periods and growth.
- **Remaining lease term is 7.0 years.** Leases "typically have ten-year terms with additional five-year renewal options, and many provide us with the option to terminate early" `[10K25 Item 2]`. That is cheap optionality, and a US analogue of the Ind AS 116 lock-in question.

### 3.5 Ship-centre (DC) capacity
- **Five ship centres, 5.19M sq ft:** Buckeye 1.2M, Forsyth 1.1M, Indianapolis 1.03M, Pedricktown 1.0M (leased to 2030 + 2×5-year options), Conroe 0.86M. They serve ~85% of store merchandise; the rest ships direct from vendors. E-commerce is fulfilled from Indianapolis `[10K25]`.
- **Density:** 1,921 stores ÷ 5.19M sq ft = **370 stores per M sq ft** (FY26E ~2,070 → ~400). About **$770 of store sales per DC sq ft** [EST: $4.76B × 85% ÷ 5.19M].
- **History:** DCs were added in 2019–22 at ~900–1,200 stores, and expanded in 2024. No new DC is announced ("evaluate opportunities"). **Open item:** management's stated network capacity in stores. The next DC (~$60–90M) is the lumpy capex the store model omits.

---

## 4. Line-by-line cost drivers in physical terms (L4)

### 4.1 Rank by weight first (v1.1 rule), FY25 % of sales [EST where marked]
| Line | % of sales | Where it sits | Physical driver |
|---|---|---|---|
| Merchandise cost incl. inbound freight & tariffs | ~49% [EST] | COGS | Units × FOB × (1 + duty) + ocean/domestic freight; shrink |
| Store payroll + benefits | ~14–17% [EST] | SG&A | Crew hours × local market wage × (1 + load ~15%) |
| Occupancy (rent, CAM, taxes, utilities) | ~9.4% | COGS | Sq ft × $/sq ft (§3.4) |
| DC, outbound freight, buying, e-com shipping | ~5–6% [EST] | COGS | Cartons × cost per carton; diesel; DC labour |
| D&A | 4.0% | Separate line | Store build-outs over ~10 years |
| Corporate SG&A, incentive comp | ~3–4% [EST] | SG&A | ~600 corporate crew |
| Advertising | 1.6% ($76.2M) | SG&A | Digital/influencer spend; "planned higher marketing investments" in FY26 |
| SBC | 0.73% ($34.7M) | SG&A | §5.2 |

**Top three for security-guard depth:** merchandise, including tariffs and shrink (§4.3); store labour (§4.2); occupancy (§3.4).

### 4.2 Wages (store labour)
- **Headcount** `[10K25 human capital]`: ~7,800 full-time and 16,800 part-time crew (FY24: 7,300 / 15,900). About 600 corporate, ~1,000 at ship centres and **~23,000 in stores** (FY24 21,500). That is **~12.0 crew per store in both years** (23,000/1,921; 21,500/1,771). Each store has a manager plus 1–2 assistant managers. District managers cover 10–15 stores. There is **no union**.
- **Payroll is not disclosed** as a line in the 10-K (the US GAAP gap vs India's employee-benefit note). [EST]: SG&A ex-D&A $1,065M − advertising 76 − SBC 35 − corporate payroll ~80 − other corporate ~150 → store payroll ~$650–800M = **13.6–16.8% of sales**, ~$340–420k per store. Cross-check: at ~$15.5/hour average plus a 15% load ($17.8), that is 19–24k hours per store per year (370–455 hours a week ≈ 9–11 FTE). It fits ~12 crew, most of them part-time. Two routes agree.
- **Sensitivity:**
  - 1% on the store wage rate ≈ $7–8M ≈ **15 bps of sales**.
  - A $1/hour step across all store hours ≈ $42–53M ≈ **90–110 bps** [EST: 36.5–46M hours × $1 × 1.15].
  - On the Q2 call, management "leveraged labor costs year over year" but had "invested more labor in the stores" since 2025 `[CC-Q2FY26]`.
- **The US difference from India:** most US value retailers already pay *above* the statutory minimum in most states. So the binding variable is the **local market wage** (BLS OEWS cashiers / retail salespersons by metro), not the statutory notification. Statutory steps matter where they bind: CA, NY, NJ, WA, IL, MA, MD, and FL's scheduled path to $15 (Sep-2026). [Schedule from memory, unverified. Verify on the DOL state minimum-wage table or the EPI tracker.]
- **Open item:** store count by state. The 10-K map is an image, so no text is extractable. Scrape the store locator, then build state count × (2026–27 legislated step) × hours → bps.

### 4.3 Merchandise margin vs shrink vs freight vs tariffs
- **Sourcing split:** ~40% of purchases are **direct imports** (FIVE is importer of record) and ~60% come from **domestic vendors**. China is the largest source *for both* `[10K25]`. The 10-K gives **no China share** (open item). Calls have not quantified it either `[CC-Q2FY26]`: "not discussed".
- **IEEPA cost revealed by the refund.** The Supreme Court struck down IEEPA tariffs in Feb-2026 `[10K25 subsequent event]`. FIVE recorded **$163.6M of IEEPA refunds in Q2 FY26 COGS** (~$170M pre-tax with interest) `[PR-Q2 FY26]`, `[CC-Q2FY26]`.
  - That is ~3.4% of FY25 sales.
  - It implies an effective IEEPA rate of ~20–22% on direct-import FOB [EST: FY25 merchandise cost ~$2.25–2.35B; 40% direct ≈ $0.9B landed; ≈ $0.75B FOB; $164M ÷ $0.75B].
  - FIVE absorbed most of it through FY25 with a **pricing reset**: ticket +5.3% and "price simplification" `[10K25]`, `[CC-Q2FY26]`.
- **Unmodelled second-order effect (nobody asked):** the **domestic-vendor 60%** carried tariffs inside vendor prices. Refunds go to the importer of record, so *vendors* collect those refunds. Does FIVE get any back, through cost renegotiation or vendor allowances? That is a potential further margin tailwind, and a ground-check and IR question. Replacement tariffs under other statutes: "2027 tariffs may be slightly higher" `[CC-Q2FY26]`.
- **Shrink:** FY25 GM benefited from "lower inventory shrinkage" `[10K25]`. Q2 FY26 had an "improved shrink reserve rate". Q3 FY26 faces "an unfavorable shrink comparison against last year's true-up" `[CC-Q2FY26]`. Shrink is accrued between physical counts, so **the true-up quarter moves**. Read the 10-Q MD&A sentence every quarter.
- **Freight and fuel:** "higher fuel cost was absolutely an offset" in Q2. H2 tariff relief is "largely offset" by fuel `[CC-Q2FY26]`. No freight split is disclosed. Proxies: the EIA weekly on-highway diesel price; Drewry WCI / Freightos FBX for Asia–US ocean rates.
- **Price-point architecture:** "most priced at $5 and below". Since the 2025 simplification the language is "most items priced between $1 and $5 and some extreme value items priced beyond $5" `[PR-HOL25]`. The **FY24 10-K risk factor said "price increases (including beyond $5 per item)". FY25 deleted the parenthesis** `[10K24]` vs `[10K25]`. Five Beyond items were moved back into departments, and an "open-wall" reset costs ~$40–45k capex per store `[CC-Q2FY26]`. **The share of sales above $5 is not disclosed.** It is the ground check's main count (§6).

---

## 5. Governance, ownership, incentives (L5): the US version

### 5.1 Related parties
The proxy has no material Item 404 transactions for new officers and directors (each 8-K states "no transactions … requiring disclosure under Item 404(a)") `[8K-20251002]`, `[8K-20260921]`. The founder **Tom Vellios** left the board on 12-Jun-2025 with a consulting agreement to Dec-2025. It included **reimbursement of private travel of up to $500,000** (plus tax gross-up) and continued RSU vesting `[8K-20250604]`. That is small, but it is the kind of perk the RPT table should log. **The RPT-table equivalent for a widely held US company is the proxy's Item 404 section plus 8-K Item 5.02 exhibits.**

### 5.2 SBC and dilution
- **SBC expense:** FY23 $17.9M, FY24 $15.6M, FY25 $34.7M (0.73% of sales, 9.7% of net income, 8.4% of FCF) `[XBRL]`. FY24 was depressed by forfeitures at the CEO exit ("lapping … a non-recurring stock compensation benefit") `[10K25]`. H1 FY26: $15.0M.
- **Overhang:** 400k RSUs + 311k PSUs unvested = **~1.3% of shares**. $35.3M is unrecognised, over 2.0 years `[10K25 n.8]`.
- **"Adjusted" EPS excludes 2024 retention awards** (cash and equity, vesting through Aug-2026): $1.95M of operating income in H1 FY26 and $5.2M in H1 FY25 `[PR-Q2 FY26]`. Small, but it is pay. **We add it back.**
- **Real dilution cost = the buyback cash** needed to hold shares flat. That was ~$270M since 2018 (~$34M a year), roughly equal to SBC plus ESPP. Q2 FY26: 311k shares bought for $60M. A new **$600M authorisation** with no expiry was approved on 29-Aug-2026 `[PR-Q2 FY26]`. Treat SBC as a cash cost: FY25 FCF after SBC = $377M.

### 5.3 Management turnover (CEO change history) `[8-K Item 5.02 series]`, `[10K25]`
| Date | Event |
|---|---|
| 2015 → Jul-2024 | Joel Anderson CEO. Resigned (8-K 16-Jul-2024). **The securities class period ends 16-Jul-2024** |
| Jul–Dec 2024 | Ken Bull (COO) interim CEO. Co-founder Vellios executive chairman. Cash and equity **retention awards** granted |
| Dec-2024 | **Winnie Park** CEO (8-K 4-Dec-2024) |
| 6-Jun-2025 | CFO Kristy Chipman exits; forfeits retention awards; gets 6 months' salary. Bull interim CFO |
| 12-Jun-2025 | Vellios leaves the board |
| 6-Oct-2025 | **Dan Sullivan** CFO (ex-Edgewell COO, Party City CFO): $850k base, $500k signing bonus, $2M RSUs over 3 years |
| Oct-2025 | Michelle Israel Chief Merchandising Officer (ex-Macy's) |
| 3-Feb-2026 | George Hill exits (severance $700k = 12 months' base; role not in the extract; open) |
| 21-Sep-2026 | Scott Settersten joins the board and audit committee (ex-Ulta CFO, per the press release) |

That is a new CEO, CFO and CMO in 10 months, plus the founder's exit. The current team owns **only the reset period**. The long-range "Triple-Double" promises (§7) belong to the prior team.

### 5.4 Insider Form 4 activity (Mar–Nov 2026, 80 filings) `[F4]`
- **Open-market buys:** 1 (director Robert Lynch, 530 shares at $176.06, $93k, 29-Jun-2026).
- **Open-market sells:** 25 transactions by 7 insiders, **$13.3M**. Cluster after the Q2 print (4–14 Sep 2026, $241–255):
  - COO Bull ~10.5k shares (~$2.6M);
  - director Devine 4,250 (~$1.06M);
  - CAO Specter 5,500 ($1.37M);
  - CHRO Gellerman 1,610 ($0.40M);
  - CMOO Hawkins 818 ($0.20M).
  - After the Q4 print (Mar-2026): director Sargent 20,000 ($4.63M), Bull 10,000 ($2.34M), director Markee 3,000 ($0.70M).
- **CEO Park: no open-market sales.** Only tax-withholding (F) rows.
- **Reading (L14):** our own test found US insider-*buy* clusters had ~0 excess return against matched controls. Sales after a ~+100% rally and a vesting window are weaker still. The tool flagged them "non-10b5-1". **Verify the 10b5-1 checkbox on each Form 4 before calling any sale discretionary** (tool caveat). The signal is weak, recorded as an open-low flag.

### 5.5 13F / 13G ownership changes `[13F]`, `[13G]`
- **BlackRock:** 4.90M (Dec-25) → **5.50M** (Sep-26), ≈10% of shares.
- **FMR:** 1.01M → 1.09M.
- **Vanguard Group:** 13F 5.34M (Dec-25). **Its 13G/A of 26-Mar-2026 shows 0%.** That is a 12-Jan-2026 internal realignment to disaggregated reporting, **not a sale** (a bad-but-benign row).
- **T. Rowe Price Investment Management:** 13G/A **6.6% (Feb-2025) → 0.0% (Nov-2025)**, an exit by a ~3.6M-share holder [EST] during the turnaround year. T. Rowe Associates still held 150,514 shares (13F, Sep-26).
- **D. E. Shaw:** 3.9% (2.18M shares, including 100.9k via calls) at 30-Sep-2025.
- **Tool gotcha:** `holdings13f 80255` printed value 0.0M and a total of $0.99B for T. Rowe Associates, a value-unit misparse. Use share counts.

### 5.6 Litigation, controls and other 8-K items
- **Securities class action** (E.D. Pa., class periods Dec-2022–Jul-2024). The motion to dismiss was **partly denied (25-Aug-2025)**. The class-certification motion was briefed by Apr-2026. Discovery is ongoing. Derivative suits are stayed. The Special Litigation Committee declined to sue `[10K25 Item 3]`.
- **Cyber incident** of 14–15 Jul 2026: one employee laptop, files exfiltrated, "no PII", not material `[8K-20260722]`.
- **ABL amendment** of 14-Oct-2026 (§2.4).

---

## 6. Ground check (L6): three stores, what to count
**Site choice (hypothesis-driven):**
- **(A)** A mature store (opened ≤2015) in the Philadelphia/NJ core. It tests mature productivity and the Five Beyond/open-wall reset.
- **(B)** A 2025–26 opening in one of the two newest states (46 states vs 44 a year ago). It tests the $2M new-store model and new-market awareness.
- **(C)** A store sharing a centre or within 1 mile of a **Dollar Tree and/or an Ollie's**. It tests price overlap and cannibalisation.

Visit each twice: a weekday 3–5 pm (teens after school) and a Saturday midday.

| Count / observe | Why (model line) | How |
|---|---|---|
| **Transactions per hour** | Bills → footfall; checks comps-by-traffic | Receipt numbers at the start and end of 1 hour (buy one cheap item each time) + a queue count every 15 min |
| **Crew on the floor and at registers** by hour | Store labour hours (§4.2: 370–455 hours a week) | Count name-tagged crew 4× per visit; ask nothing confidential |
| **Price-point mix:** % of facings tagged >$5, and the top price seen | Price architecture (§4.3), the share above $5 | Count facings in 3 fixed bays (Tech, Room, Sports) |
| **Fixed 15-item basket** (5 FIVE private/no-name, 5 licensed, 5 branded candy/beverage) vs Dollar Tree ($1.25/$1.50 multi-price) and Ollie's | Value gap; pass-through of tariffs and refunds | Same 15 items every quarter, photographed with date |
| **Locked cases, security tags, guard present, empty pegs (%)** | Shrink (§4.3) and in-stock | Count locked fixtures; out-of-stocks per 100 pegs |
| **Sq ft check** (pace the box) and back-room size | $/sq ft (§3.2); 9,500 model | Pacing plus the landlord/LoopNet listing for the centre |
| **Co-tenants and vacancy in the centre** | Traffic dependence; rent leverage | Count anchors, dark boxes and asking rent on LoopNet/CoStar |
| **Hiring signs and posted pay** | Market wage vs statutory minimum (§4.2) | In-store sign; Indeed listings for the same zip |
| **Country of origin** on 20 random items | China share (not disclosed) | Read the labels; tally China / Vietnam / India / other / USA |

**Ethics:** identify yourself honestly if asked. Never seek non-public sales data from crew. No recordings without consent.
**Output:** a surprises-vs-model list. The rows to mark confirmed / contradicted / no read: $210 vs $265/sq ft; ~12 crew; shrink controls; the >$5 share; the China share.

---

## 7. Promise tracker (last investor day + 5 calls)

### 7.1 Long-range: investor day of 30-Mar-2022, "Triple-Double" (prior CEO) `[WEB: Retail Dive 31-Mar-2022; Motley Fool 2-May-2022]`
| Promise | Target | Delivered by FY25 | Hit rate |
|---|---|---|---|
| Double sales by FY2025 | ~$5.7B (2 × FY21 $2.85B) | $4.76B | **84%** |
| Double EPS by FY2025 | ~$9.90 (2 × $4.95) | $6.47 GAAP / $6.67 adj. | **65–67%** |
| ~1,000 openings FY22–25 (up to 400 in FY22–23, up to 600 in FY24–25) | ~2,190 stores | 1,921 (+731 net) | **73%** |
| Operating margin ~14% by FY25 | single-source `[WEB: Quartr summary]` | 9.6% (FY21: 13.3%) | miss |
| 3,500+ stores **by FY2030** | ~316 net a year needed from FY26 | Plan ~150 a year. **The 10-K now says "more than 3,500 locations over time"** | silently softened |

### 7.2 Near-term: quarterly comp guidance vs delivery (new CEO/CFO era) `[PR-*]`
| Guide date | Period | Comp guide | Actual | Beat vs midpoint |
|---|---|---|---|---|
| 4-Jun-2025 | Q2 FY25 | +7–9% | +12.4% | +4.4 pp |
| 27-Aug-2025 | Q3 FY25 | +5–7% | +14.3% | +8.3 pp |
| 3-Dec-2025 | Q4 FY25 | +6–8% (raised to ~14.5% on 12-Jan) | +15.4% | +8.4 pp |
| 18-Mar-2026 | Q1 FY26 | +14–16% | +22.7% | +7.7 pp |
| 3-Jun-2026 | Q2 FY26 | +7–9% | +14.1% | +6.1 pp |
| 2-Sep-2026 | Q3 FY26 | +8–10% | due ~early Dec-2026 | — |

- **Full-year comp guide path:**
  - FY25: +3–5% (Jun) → +5–7% (Aug) → +9.4–10.1% (Dec) → ~12.5% (Jan) → **12.8% actual**.
  - FY26: +3–5% (Mar) → +6–8% (Jun) → +10–12% (Sep).
- **EPS:** Q4 FY25 GAAP guide $3.34–3.52 → $4.28. Q1 FY26 adjusted $1.57–1.69 → $2.22. Q2 FY26 adjusted $1.17–1.29 → $1.68.
- **Reading:** two different credibility numbers. **Long-range targets were missed (65–84%)** under the prior team. **Near-term guides have been beaten 5 for 5, by 4–8 pp**, under the new CFO's method. The CFO calls the outlook "thoughtful", not conservative `[CC-Q2FY26]`.
- **Method lesson:** a promise tracker must **score long-range and near-term promises separately, and by management team.**

---

## 8. Flag override (L7)

### 8.1 Bad-but-benign / good-but-misleading
| Item | Looks | Why it misleads | Verdict |
|---|---|---|---|
| Vanguard 13G/A = 0% (Mar-2026) | Bad (top holder exits) | Jan-2026 realignment to disaggregated reporting; the 13F still holds 5.34M | Benign. **Closed** |
| $2.03B lease liabilities | Bad (debt-like) | 10-year leases with early-termination options; 7.0 years remaining; covered by store cash flow | Benign, but use lease-adjusted metrics |
| ABL doubled to $450M | Bad? | Seasonal inventory line, undrawn at year-end, maturity extended to 2031 | Benign. **Closed** |
| SBC doubled FY24 → FY25 | Bad | FY24 was depressed by forfeitures at the CEO exit | Mostly benign; treat SBC as cash anyway |
| Zero buybacks in FY25 | Bad? | CEO transition plus tariff uncertainty; $60M in Q2 FY26 and a $600M programme | Benign |
| **Q2 FY26 GAAP EPS $3.99, GAAP GM 48.5%** | Good | $163.6M IEEPA refund in COGS (13% of the quarter's sales) | **Misleading.** Use adjusted figures; flag for 4 quarters |
| **FY25 FCF $412M** (3.9× FY24) | Good | Capex halved (fewer openings) + payables and incentive accrual build | **Misleading as run-rate.** Normalise to ~$250–300M [EST] |
| **"Payback ~1 year"** | Good | Undefined numerator; net of tenant allowances *and* payables; excludes DC/network capex; unchanged text; capex guide implies ~$0.65M gross per store | **Open** (§3.3) |
| **"Average net sales per store $2.5M"** | Good | Includes only stores open before the start of the year (excludes the new, weaker class) | Mildly misleading; use total sales ÷ average stores ($2.58M ≈ similar this year) |
| **Comps +22.7% / +14.1%** | Good | FY25 had +5.3% ticket from pricing; e-commerce is inside comps; 2-year stack; trend/licence spikes | **Open** (durability) |
| "Adjusted" excludes retention awards | Good | It is pay | Add back (small) |
| Flat share count for 10 years | Good | Bought with ~$34M a year of cash | Neutral. SBC is a real cost |

### 8.2 Open soft flags (each with what would change my mind)
1. **New-store investment vs capex gap** (§3.3). *Clears if* the tenant allowance is disclosed at ≥$0.4M per store, or a cohort payback table is published. *Confirms if* the next 10-K raises the $0.4M or quietly drops the payback sentence.
2. **Comp durability** (2-year stack ~+30% in H1 FY26). *Clears if* Q4 FY26 and FY27 comps stay positive against +15–23% comparisons, with transactions positive. *Confirms if* traffic turns negative while ticket carries the comp.
3. **Tariff regime and vendor pass-through.** The refund is one-off; replacement tariffs are possibly higher in 2027; the 60% domestic-vendor channel's refunds are unknown. *Clears if* merchandise margin holds in FY27 with tariffs at the new rates.
4. **Insider cluster selling** (Sep-2026, 5 insiders, $6M+). Low weight (L14). *Changes if* the CEO or CFO sell outside 10b5-1, or an insider buys at scale.
5. **Executive turnover** (CEO, 2 CFOs, CMO and other senior exits in 18 months). *Clears* after 4+ quarters with a stable team.
6. **Class action in discovery.** *Clears* on dismissal or settlement below ~1% of market cap.

**Count of open soft flags: 6** (plus a mechanical normalisation of FCF and GAAP EPS). That is above the 3+ rule, so *no position without a written variant view*. This is a statement about our evidence, not about the company.
**Hard disqualifiers found: none** (no restatement, no auditor change, no going-concern language, no related-party diversion).

---

## 9. Note on the open paper call (not a change to it)
`thesis:paper-call:US-FIVE:fy2026-comps-11pct-plus` (made 2026-11-21, P = 0.58, base 0.50). Facts its reasoning did **not** use, recorded for the post-mortem:
- **What the guide implies.** H1 FY26 comps were +18.3%; Q3 is guided +8–10%. Management says the FY guide of +10–12% **implies Q4 ≈ +3%** `[CC-Q2FY26, single-source]`.
- **My comp-base weighting.** Weights from FY25 quarterly sales: H1 41.6%, Q3 21.8%, Q4 36.3% [EST]. On these, FY ≥ 11.0% needs Q4 ≥ ~4% if Q3 lands at +9%, and **Q4 ≥ ~1% if Q3 repeats the beat pattern (~+14%)**.
- **For YES:** 5 for 5 quarterly beats of +4.4 to +8.4 pp; the Q3 results (~early Dec) arrive before resolution; holiday merchandise newness.
- **For NO:** Q4 laps +15.4%; an "unfavorable shrink comparison" (a margin item, not comps); fuel; consumer softening; and the CFO explicitly calls the guide "thoughtful", not conservative.
- **Net:** the call's main premise (beat-and-raise means a conservative H2) is supported by the promise tracker in §7.2. The weighting shows the threshold is low *if* Q3 beats. **Lesson for the paper-call method:** compute the implied remaining-quarter comp from the FY guide before setting a probability.

---

## 10. What this exercise taught (method, not stock)
1. **US filings move the "boring filings" (L13).** There is no BRSR, so headcount comes from the 10-K *human capital* section. The lease note (Topic 842 tables plus "leases committed but not commenced", with dollar totals) gives **rent per new lease** directly: $258M ÷ 141 leases. The **non-GAAP reconciliation in the 8-K Ex-99.1** is where the one-offs hide (the $163.6M tariff refund).
2. **For a widely held US company, the L16 "money to the parent" question becomes "money to management, and what the KPIs leave out".** The useful documents were the 8-K Item 5.02 exhibits (severance, signing bonuses, founder perks, retention awards), the KPI definitions in Items 1 and 7, and Form 4 plus 13G.
3. **Diff the 10-K text year over year.** Deleting "(including beyond $5 per item)" and replacing "by 2030" with "over time" were the cheapest promise-tracker signals in the set.
4. **Triangulate the company's store model against its own capex guidance.** "$100M for ~150 stores" contradicts "$0.4M investment" unless tenant allowances are huge. That made a 2-minute check into the main L3 finding.
5. **Ownership-filing mechanics create false alarms** (the Vanguard realignment) and tool misparses (13F value units). Read the 13G remarks field before reading a 0%.
6. **Two credibility scores:** long-range vs near-term, and by team.
7. **Time spent:** ~70% primary SEC filings (two 10-Ks, 11 8-Ks/exhibits, 80 Form 4s, 13F/13G), ~15% one call transcript (secondary, automated), ~15% estimates. Broker notes were not needed.

## Open items
- **Tenant allowance per new store** and the FY24/FY25 cohort's first-year sales. Ask IR, or look for a cohort chart at the next investor event.
- **Earlier 10-K store-model text** (FY2019–FY2023): has the $2.0M / $0.4M ever changed?
- **Total chain sq ft** (not disclosed). Estimate from pacing and listings.
- **Store count by state** (locator scrape), for the minimum-wage bps model.
- **China share** of direct and domestic-vendor purchases. Read the full Q4 FY25 and Q1 FY26 transcripts. The Q2 call is single-source and automated; get the Motley Fool or official replay and re-verify the quotes.
- **DEF 14A (1-May-2026):** read the CEO pay mix, PSU metrics (is it EPS? adjusted or GAAP? are tariff refunds excluded?), clawback, and Item 404.
- **Peer COGS definitions** for DG, DLTR and OLLI, before any gross-margin comparison.
- **DC capacity** in stores. When is the next ship centre due?
- **George Hill's role** (Feb-2026 exit).

## Sources
- 10-K FY2025: https://www.sec.gov/Archives/edgar/data/1177609/000117760926000010/five-20260131.htm ; 10-K FY2024: https://www.sec.gov/Archives/edgar/data/1177609/000117760925000009/five-20250201.htm
- Earnings releases (Ex-99.1): Q2 FY26 https://www.sec.gov/Archives/edgar/data/1177609/000117760926000023/q22026fivebelowexhibit991.htm ; Q1 FY26 https://www.sec.gov/Archives/edgar/data/1177609/000117760926000015/q12026fivebelowexhibit991.htm ; Q4 FY25 https://www.sec.gov/Archives/edgar/data/1177609/000117760926000006/q42025fivebelowexhibit991.htm ; holiday 2025 https://www.sec.gov/Archives/edgar/data/1177609/000117760926000003/holiday2025fivebelowex991.htm ; Q3 FY25 https://www.sec.gov/Archives/edgar/data/1177609/000117760925000048/q32025fivebelowexhibit991.htm ; Q2 FY25 https://www.sec.gov/Archives/edgar/data/1177609/000117760925000037/q22025fivebelowexhibit991.htm ; Q1 FY25 https://www.sec.gov/Archives/edgar/data/1177609/000117760925000019/q12025fivebelowexhibit991.htm
- 8-Ks: ABL https://www.sec.gov/Archives/edgar/data/1177609/000117760926000072/five-20261014.htm ; director https://www.sec.gov/Archives/edgar/data/1177609/000117760926000050/five-20260921.htm ; cyber https://www.sec.gov/Archives/edgar/data/1177609/000119312526312573/d19155d8k.htm ; Hill https://www.sec.gov/Archives/edgar/data/1177609/000119312526042901/d25218d8k.htm ; CFO https://www.sec.gov/Archives/edgar/data/1177609/000119312525227293/d18933d8k.htm ; Chipman/Vellios https://www.sec.gov/Archives/edgar/data/1177609/000117760925000019/five-20250604.htm
- 13G/A: Vanguard https://www.sec.gov/Archives/edgar/data/1177609/000010290926001383/xslSCHEDULE_13G_X02/primary_doc.xml ; D. E. Shaw https://www.sec.gov/Archives/edgar/data/1177609/000110465925112499/xslSCHEDULE_13G_X01/primary_doc.xml ; T. Rowe https://www.sec.gov/Archives/edgar/data/1177609/000189761225000532/xslSCHEDULE_13G_X01/primary_doc.xml
- Q2 FY26 call: https://www.webull.com/news/15510981903246336 ; https://www.nasdaq.com/articles/five-below-q2-earnings-call-highlights
- 2022 investor day: https://www.retaildive.com/news/five-below-looks-to-triple-store-count-by-2030/621334/ ; https://www.fool.com/investing/2022/05/02/five-below-plans-to-triple-its-store-count-by-2030 ; https://quartr.com/events/five-below-inc-five-q4-2022-investor-day-2022_QQIH5QT

---

## 11. Protocol v1.2: US adaptations (applied to `deep_dive_protocol.md`)

**What worked unchanged:** rule zero (list the call's questions to find the un-asked variable), technique #1 triangulation (it exposed the capex gap), technique #10 definition audit, the override table including the "looks good" rows, and "rank cost lines by weight".

**What was missing for a US filer:**
1. **No document map by 10-K item and note.** India's equivalents (BRSR, "other expenses" note, RPT note) do not exist. The US depth sits in: Item 1 (store model, sourcing %, human capital headcount), Item 1A (diff year over year), Item 2 (DC sq ft, cost, lease terms), Item 3 (litigation stage), Item 5 (buybacks), Item 7 (KPI definitions, capex plan, contractual obligations, leases signed after year-end), and the notes: leases (Topic 842 cost table, cash vs straight-line, "committed not commenced" $), SBC (unvested units, unrecognised $), PP&E, subsequent events.
2. **No rule for 8-K exhibits.** Item 2.02 Ex-99.1 is the quarterly results and the non-GAAP reconciliation (one-offs). Item 5.02 gives officer pay, severance and founder perks. Item 1.01 covers credit agreements. Item 8.01 covers other events (cyber). Items 4.01 and 4.02 cover auditor change and non-reliance (hard flags).
3. **No SBC handling rule.** Treat SBC as a cash cost; compute FCF − SBC; add back "retention award" exclusions; dilution cost = buyback cash needed to hold the share count flat.
4. **No Form 4 / 13F / 13G reading rules:** codes; 10b5-1 checkbox; clusters vs L14 base rates; 13G remarks; reporting realignments; 13F value units; 45-day lag.
5. **The US wage logic differs.** The market wage, not the statutory minimum, usually binds. Payroll is not disclosed; estimate it by two routes.
6. **The proxy (DEF 14A) replaces the AGM notice** for pay, PSU metrics and Item 404 related parties.
7. **Promise tracker:** split long-range from near-term, and score by team. Diff 10-K text year over year.
8. **Tool notes:** `sec_fetch.py doc --file X --text` for exhibits; `holdings13f` value misparse; the "non-10b5-1" flag needs manual confirmation.
