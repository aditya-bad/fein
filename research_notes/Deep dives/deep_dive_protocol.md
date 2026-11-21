# Deep-dive protocol (sector-agnostic) at "security-guard depth"

**Version 1.1 · 2026-11-21.** Built from the Vishal Mega Mart practice run (`VMM_practice.md`, a retailer). Revised after the Cummins India practice run (`CUMMINSIND_practice.md`, a manufacturer and MNC subsidiary). Links: `insight:flag-override-template`, `strategy:fisher-scuttlebutt`, lessons L9, L10, L12, L13. The changelog is at the bottom.

**What "security-guard depth" means:** you can rebuild the business's economics from its smallest operating unit (a store, a plant, a branch, a truck, a salesperson). You can express every major cost line in physical terms: people × wage, square feet × rent, kWh × tariff, tonnes × freight. And you can name the one or two micro-drivers (a wage notification, a tariff order, a commodity, a related-party contract) that move margins before the P&L shows it.

It is **not** collecting trivia. Each deep fact must end in a number that (a) changes a model line, or (b) can be checked on the ground.

---

## Rule zero: edge before depth
Before starting, write 3 lines:
1. What does the market already know (consensus numbers, the 5 most-asked questions on the last call)?
2. Which variable, if we knew it better than consensus, would change the value most?
3. Which layer below is most likely to reveal it?
Depth without a question is a hobby. A deep dive done to test a method produces **no verdict** (L9).
Tip (v1.1): list the 5 most-asked questions from the last call's Q&A. The variable that *nobody* asks about is often where the edge is. At Cummins it was the parent's cost take.

## Choose the unit by business type (v1.1)
"Smallest operating unit" differs by model. Pick the unit(s) before L3.
| Business type | Units to rebuild | Typical micro-drivers to test first |
|---|---|---|
| Retailer / consumer service | Store (sq ft, bills, staff) | Rent, minimum wages, outsourced security/housekeeping, shrinkage |
| **Manufacturer** | **(1) Plant** (capacity × utilisation), **(2) product node/platform** (price, mix, competition), **(3) channel account** (OEM, dealer, distributor concentration) | Materials basket and pass-through lag, plant utilisation, regulatory product transitions, warranty |
| **MNC subsidiary / group company** | All of the above plus the **parent relationship** | Royalty, support/cost allocations, transfer-pricing formulas, purchases from and sales to group companies, dividends to the parent, renewal dates |
| Lender | Branch / loan cohort | Cost of funds, credit cost by vintage, collection staff |
| Platform / software | Cohort / account | CAC, retention, take rate |

---

## The 7 layers (and the time budget for a ~3–4 day dive)

| # | Layer | Question it answers | Time share | Stop when |
|---|---|---|---|---|
| L1 | **Map**: business model, segments, history, peers | What is the unit, and who else runs the same unit? | 5% | You can draw the value chain and name 2–3 peers with comparable units |
| L2 | **Reported financials, re-derived** | Do the numbers add up after accounting adjustments? | 15% | 10-year P&L, BS and CF re-derived; leases, goodwill, ESOP, one-offs separated |
| L3 | **Unit economics** | What does one unit earn, cost and return? | 20% | Revenue per unit and per sq ft or capacity; unit P&L; capex per unit; payback, triangulated two ways |
| L4 | **Line-by-line cost drivers in physical terms** | What *physically* drives each cost, and what is the elasticity to an external input? | 20% | **First rank cost lines by weight** (v1.1). Each line ≥3% of sales mapped to quantity × price, with a sensitivity in bps. Do security-guard depth on the top 3 lines, not on habit (wages were 3.8% of sales at VMM; minimum-wage labour was 0.3% at Cummins, where materials were 63%) |
| L5 | **Governance, ownership, incentives, related parties** | Who gets paid before minority shareholders? | 10% (**15% for MNC subsidiaries/group companies**, taken from L3) | RPT table by year and share of each cost line; promoter/PE supply; KMP incentives and strike prices; **for MNC subs, the parent-take table** (see below) |
| L6 | **Customer, competitor, supplier ground truth** | Does reality match the disclosures? | 20% | Scuttlebutt list executed or scheduled; each observation tied to a model number |
| L7 | **Flag override and synthesis** | Which numbers mislead, in either direction? | 10% | Override table filled; open-flag count; "what would change my mind" per flag |

For a 1-day screen, do L1–L2 plus the L4 top-3 costs plus the L5 RPT table only. **L5's RPT table is never skipped.**

**L2 additions (v1.1), always:**
- **Customer concentration** from the Ind AS 108 footnote ("sales of ₹X derived from N external customers", each ≥10% of revenue). Track N and the share by year. At Cummins it went from 2 customers/21% to 3 customers/31%.
- **Other-income decomposition:** treasury interest, MF gains, group rent, JV/associate dividends. Compute **core PBT = PBT − other income** and use it for multiples. At Cummins, other income was 23% of PBT.
- Screener nets exceptional items into "Other income". Read the AR P&L.

**L5 parent-take table (v1.1), for MNC subsidiaries and group companies.** By year: royalty (rate × eligible base); technical, support and cost-allocation fees; reimbursements paid and received; purchases from group companies (share of purchases) with the pricing formula; sales to group companies (share of revenue, share of exports) with the pricing formula; dividends to the parent; and stock-based pay in *parent* shares. Total it as % of sales and % of EBITDA. List every **agreement renewal date** (royalty agreements often run for 3 years) as a dated watch item. Read the **AGM/postal-ballot RPT annex**: SEBI's Jun-2025 "minimum information" standard makes companies disclose pricing formulas (e.g. "cost plus at least 11%"), royalty rates, uniform-rate confirmations and sunset clauses.

---

## Data sources by layer

### India
| Layer | Primary sources (in order of value per hour) |
|---|---|
| L1 | DRHP/RHP "Industry overview" (commissioned research such as RedSeer or CRISIL: biased but detailed); "Our Business" chapter; peer DRHPs |
| L2 | Annual-report notes (not the front half); screener.in (re-derive, never trust "Borrowings" or "ROCE" blindly); quarterly results; `tools/nse_fetch.py results` |
| L3 | DRHP KPIs (stores, area, payback, cohort data); investor presentations; call transcripts (`nse_fetch.py transcripts`); broker *analyst-meet* notes (they relay closed-door numbers) |
| L4 | **AR note "Other expenses"** (security, manpower, housekeeping, power, freight lines); **BRSR** (headcount, *% of employees at minimum wage*, median pay, attrition, energy GJ, water); state labour-department wage notifications; SERC tariff orders (power); freight indices; commodity prices |
| L5 | AR related-party note (Ind AS 24) by year; **AGM-notice and postal-ballot material-RPT annexes (pricing formulas, royalty rate, sunset clause; v1.1)**; Form AOC-2; DRHP risk factors ("our Promoters provide us services…"); shareholding pattern; SAST/insider/pledge (`nse_fetch.py sast/insider/pledge`); block/bulk deals; ESOP grant intimations (Reg 30); AGM/postal-ballot notices (pay, strike prices); MCA filings of promoter entities |
| L4 (manufacturers, v1.1) | Materials ratio by quarter from results; commodity series (BigMint, SteelOrbis, Mysteel for pig iron and steel; LME for Cu/Al; freight indices); BRSR energy, water and waste plus *physical-output intensity*; regulatory notifications (CPCB, CAQM, NGT, BIS/QCO orders); SPCB consent-to-operate orders (permitted capacity) |
| L6 | Store/plant visits; B2B channel checks (OEM/dealer price sheets by product node, lead times, parts prices); GeM/railway/defence tender results; MCA filings of private channel partners and sister companies; job portals (AmbitionBox, Indeed, Naukri) for pay and attrition reviews; Google Maps (reviews, competitor distances); landlord/broker rent quotes; dealer and supplier calls; app-store reviews; quick-commerce price checks by PIN code |
| L7 | memdb `insight:flag-override-template`; our false-alarm case base (`--tag false-alarm`) |

### US
| Layer | Primary sources |
|---|---|
| L1–L2 | 10-K (Item 1 Business, Item 7 MD&A, notes); S-1 for IPOs; 10-Q |
| L3 | Investor-day decks; earnings transcripts; S-1 "Key metrics" and cohort charts; franchise disclosure documents (FDD Item 19 gives unit-level sales for franchise systems) |
| L4 | BLS OES wage data by occupation and metro; state minimum-wage schedules (DOL, EPI tracker); EIA electricity prices by state; CoStar/LoopNet rent comps; 10-K headcount and "human capital" section; EEO-1 if published |
| L5 | DEF 14A proxy (pay, related-party transactions, PSU metrics); Form 4 (insider); 13D/13G; Form 144 (planned sales); lock-up expiry from S-1 |
| L6 | Glassdoor/Indeed reviews; Placer.ai/SafeGraph-type foot traffic (paid); app downloads; Google Trends; channel checks; court records (PACER) |

---

## Estimation techniques when data is missing
Always show the method next to the number, give a range, and mark it `[EST]` with confidence `unverified` until a second method or a ground check agrees.

1. **Triangulation (two independent routes or it doesn't count).**
   - Top-down: company total ÷ units, e.g. capex ÷ gross openings = upper bound on capex per store.
   - Bottom-up: physical quantity × benchmark price, e.g. sq ft × fit-out ₹/sq ft + net working capital per store.
   - If the routes differ by >30%, the gap is the finding: find out why.
2. **Cost line ÷ statutory wage = headcount.**
   - Outsourced cost (security, housekeeping, manpower) ÷ (state minimum wage × statutory load ~1.29 × agency margin ~1.10) = full-time equivalents.
   - Statutory load in India ≈ PF 12–13% + ESI 3.25% + bonus 8.33% + leave/gratuity ~4–5%.
   - VMM: ₹98k/store/month ÷ ₹16–17.5k ≈ 5.5–6 guards per store.
3. **Minimum-wage exposure from BRSR.** % of employees "equal to minimum wage" × headcount × CTC gives the wage pool indexed to notifications. Add outsourced lines, apply each state's notified step, and convert to bps of margin. The notifications are dated, public and *leading*: April and October variable-DA revisions plus ad-hoc revisions.
4. **Median vs mean pay.** Mean = (employee cost ex-ESOP) ÷ average headcount. The BRSR median is an *annual* figure, so with high attrition it understates the monthly wage. Divide by (1 − attrition/2) as a rough tenure correction before calling anything underpayment.
5. **Rent benchmarks.** Lease cash outflow (Ind AS 116 principal + interest, the cash-flow note) + short-term rent, ÷ average area ÷ 12 = ₹/sq ft/month. Compare with local broker quotes. Lease maturity buckets give the average remaining lock-in.
6. **Capacity × utilisation** (plants, hospitals, hotels, telecom, logistics). Installed capacity (DRHP, environmental clearance, CPCB/SPCB consent orders, which state permitted tonnage) × utilisation (power or fuel consumption ÷ specific consumption; BRSR energy GJ and water kL are proxies) = volume. Volume × realisation (price surveys) gives revenue to check against the reported figure.
7. **Density accounting.** Revenue per sq ft (or per bed or per ton) × gross margin = gross profit per unit of capacity. Compare with peers. A high margin % at low density can earn less than a low margin % at high density (VMM vs DMart).
8. **Bills and footfall from ticket size.** Revenue per store ÷ average bill = bills. Bills ÷ conversion (benchmark) = footfall. A count at the counter confirms it.
9. **Related-party share by line.** For each RPT, compute RPT ÷ the matching expense line, by year. A rising share or a near-monopoly (more than 50% of a line) gets a row in the override table.
10. **Definition audit.** For every company-defined KPI (SSSG/LFL, payback, "operating EBITDA", "customers", "ARR", "order book"): copy the footnote verbatim, list what is excluded, ask how the excluded count moved.
11. **Peer as instrument.** A peer running the same unit with different choices (owned vs leased, fast vs slow rollout) is a natural experiment. Lift its disclosed metric to fill your gap, and mark it as a peer proxy.
12. **Sanity-check claims against physics.** "₹23 cr capex per 18k sq ft leased store" = ₹12,800/sq ft, which is impossible for a value fit-out. Reject. Every third-party number gets a 10-second physical-plausibility check. It also works on **demand**: at Cummins, India's DC IT MW × PUE × redundancy × ₹/MW of gensets bounded the whole DC genset market, and the company's DC revenue sat at the top of that band. The gap became a question for the ground check.
13. **BRSR intensity → physical volume (v1.1).** Total energy (GJ) ÷ "energy intensity per unit of physical output" = units. Cross-foot with water (kL ÷ kL/unit) and waste (t ÷ t/unit). Then revenue ÷ units = realisation, which splits growth into volume vs price/mix. Caveat: "equivalent units" is a company weighting. It confirms arithmetic, not definition. (Cummins FY26: ~147.9k units, +7% volume, ~+10% price/mix.)
14. **Commodity pass-through lag (v1.1).**
   - (a) Materials ÷ revenue by quarter, for at least 8 quarters.
   - (b) Classify input contracts: cost-plus or index-linked (pass-in at once) vs spot.
   - (c) Classify output contracts: order book or tender at fixed prices (pass-out with a lag) vs list price.
   - (d) Inventory build at high cost means the next quarter's COGS carries it.
   - (e) Lag from the last cycle's OPM recovery.
   - (f) Sensitivity: metal-linked share of material cost × % move = bps.
   - (g) Leading series: weekly metal prices turn before the P&L.
   - **Ask who carries the mismatch.** In a group, it is often the listed minority entity.
15. **Transfer-pricing bounds on line margins (v1.1).** When segment margins are not disclosed, use the RPT pricing formulas. A sale to a group company at "cost + 11%" earns ~10% of sales. Back-solve the rest of the business as (EBITDA − group-sales margin) ÷ other revenue. A weak currency does not help exports that are priced at cost-plus.
16. **Regulatory-transition template (v1.1)** for emission norms, BIS/QCOs and labour codes. Date each phase: notification → pre-buy spike → price step (%) → volume trough → competitor catch-up → volume recovery (Cummins CPCB IV+: ~15 months) → **aftermarket tail** after warranty expiry. Each phase is a dated, checkable number.
17. **Own capacity vs group/supplier capacity (v1.1).** "70% utilisation" at own plants is irrelevant if the bottleneck product is made by a sister company or allocated by the parent. Find where the constrained product is physically built.
18. **Customer concentration → channel map (v1.1).** Match the number of ≥10% customers to the channel structure (e.g. 3 genset OEMs). Concentration in channel partners is a different risk from end-customer concentration. Check the partners' health through MCA filings.

---

## Scuttlebutt (L6) design rules
- **Choose sites to test hypotheses.** Use a mature unit, a new unit in a new geography, and a different format or near-cannibalising unit. Visit off-peak and peak.
- **Count before you talk:** queues, bills per hour, footfall, staff and guards, facings, prices of a fixed basket. Numbers first, opinions second.
- **Talk to five constituencies:** staff, store or plant manager, customers, neighbours/competitors, and a supplier, landlord or driver. Ask about pay, tenure, rent, trips, and switching.
- **Ethics:** identify yourself honestly if asked. Never pay for or solicit confidential or unpublished price-sensitive information (that is insider-information risk). No recordings without consent.
- **Repeat the fixed price basket quarterly.** It is a cheap time series nobody else has.
- **B2B version (v1.1).** Use three visits: (A) an OEM or channel partner and two competitor dealers in the same city, (B) the company's dealer workshop or parts counter, (C) end-users and installers.
  - Count: price sheets *by product node* (same nodes every quarter), price-hike dates and percentages by component, lead times by platform, service bays and jobs, and a fixed basket of 5 spare parts (genuine vs will-fit).
  - Ask end-users the engineering ratio that sizes demand (e.g. DG MW per IT MW).
- **Output:** a "surprises vs model" list. Each model estimate is marked confirmed, contradicted or no read.

---

## Synthesis (L7): the override table
For every flag, good or bad, fill: flag | context questions | clearing evidence (external) | confirming evidence | verdict | what changes my mind | review date. Rules from `insight:flag-override-template`:
- A management explanation alone keeps a flag OPEN.
- Three or more open soft flags means no position without a written variant view.
- Hard disqualifiers (fraud signals, auditor exit on denied information, related-party diversion, fake cash) cannot be overridden.
- Include **"looks good" flags**. Inflated KPIs and definitional flattery mislead more often than ugly numbers.

---

## Deliverables checklist
- [ ] Edge question (3 lines) written first
- [ ] Source tag on every number; `[EST]` with the method on every estimate; a second source or route for every key number
- [ ] Unit P&L table (fully loaded and, if possible, four-wall)
- [ ] Physical cost-driver table with at least one external-input sensitivity (wage, tariff, commodity) in bps, with lines ranked by weight first
- [ ] RPT table by year with share of each cost line
- [ ] **Parent-take table** (MNC subs/group cos): royalty, fees, TP formulas, dividends, renewal dates, as % of sales and EBITDA (v1.1)
- [ ] **Price-vs-cost lag table** (manufacturers): materials ratio by quarter, price-action dates, inventory layer, leading commodity series (v1.1)
- [ ] Core PBT (ex other income) and customer-concentration line (v1.1)
- [ ] Ownership and supply table (who sold, at what price, to whom; what is left; incentives and strike prices)
- [ ] Scuttlebutt list (sites, counts, questions, ethics) tied to model numbers
- [ ] Override table and open-flag count
- [ ] "What the method taught" (for curriculum) plus open items
- [ ] memdb seed: an analysis record (no verdict if practice), insight records for new techniques

## Common traps seen so far
- Screener's "Borrowings" includes lease liabilities, so asset-light retailers look indebted.
- Goodwill from a PE buyout crushes reported ROE and ROCE. Use return on tangible equity.
- Ind AS 116 EBITDA overstates margins of rent-heavy models by 4–6 pp. Always find the pre-Ind AS number (company presentation, or EBITDA − lease cash outflow).
- Viral social-media "ground data" can be fake (the VMM guard-recruitment meme was disowned by the company).
- Payback and SSSG are company-defined. Read the definition before quoting them.
- (v1.1) **Cost-plus transfer pricing caps margins.** Exports sold to the parent at cost + x% do not gain from a weak rupee. The parent captures it.
- (v1.1) **High ROCE can be borrowed from the group's balance sheet.** If the constrained product is made by a sister company, the listed entity's capital looks small.
- (v1.1) **Cost allocations from the parent can step up without notice** (Cummins: support services ₹111 → ₹223 cr in a year, then a further Q2 "true-up"). Read the other-expenses note every year, and the call's "one-offs" answer every quarter.
- (v1.1) **Company "ranges" can hide the number.** "DC = 30–40% of power gen" is ±₹130 cr a quarter, wide enough to hide a slowdown in the rest of the business.
- (v1.1) **Tool note:** `tools/nse_fetch.py transcripts SYMBOL --download DIR` ignores `--from/--to` and downloads everything. List first, then fetch only the URLs you need.

---

## Changelog
- **v1 · 2026-11-20.** First version, from the Vishal Mega Mart practice run (retailer).
- **v1.1 · 2026-11-21.** From the Cummins India practice run (manufacturer, 51% MNC subsidiary):
  - Added the unit-by-business-type table.
  - L4 now ranks cost lines by weight before going deep.
  - L5 time share is 15% for MNC subsidiaries, with a parent-take table and the AGM-notice RPT annex as a source.
  - L2 additions: customer concentration, other-income decomposition and the screener exceptional-item trap.
  - New techniques #13–18: BRSR intensity → units; commodity pass-through lag; transfer-pricing bounds; regulatory-transition template; own vs group capacity; concentration → channel map. Demand-side physics check added under #12.
  - Added manufacturer data sources and B2B scuttlebutt rules.
  - Two new deliverables, four new traps and a tool note.
