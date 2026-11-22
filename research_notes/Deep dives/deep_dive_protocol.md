# Deep-dive protocol (sector-agnostic) at "security-guard depth"

**Version 1.3 · 2026-11-22.** Built from the Vishal Mega Mart practice run (`VMM_practice.md`, a retailer). Revised after the Cummins India practice run (`CUMMINSIND_practice.md`, a manufacturer and MNC subsidiary), then after the Five Below practice run (`FIVE_practice.md`, the first US filer), then after the Federal Bank end-to-end dry run (`FEDERALBNK_dryrun.md`, the first lender; stages 2→6). Links: `insight:flag-override-template`, `strategy:fisher-scuttlebutt`, `insight:lender-blowup-signals`, `decision:adopt-disqualifiers-v2`, `research_notes/Templates/valuation_and_decision.md`, lessons L9, L10, L12, L13, L18, L19, L21. The changelog is at the bottom.

**Where a deep dive sits in the machine (v1.3).** Run in this order: **S2 checklist** (below) → stage-3 signals (PEAD quintile, credibility vs peers) → layers L1–L7 → **L8 valuation and decision** → paper calls. A deep dive is not finished until L8 has produced a worksheet and a card.

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
| **Lender (bank / NBFC; v1.3, see the adaptation section)** | **(1) Branch** (deposits, CASA, sourcing per outlet), **(2) loan segment/cohort** (yield, slippage, LGD), **(3) liability pool** (CASA, retail TD, NRI/FCNR, bulk), **(4) balance-sheet "cost lines"** (CRR, PSL shortfall, DICGC) | IBA wage settlement, deposit repricing lag vs EBLR share, DICGC premium, CRR/PSL rules, special funding windows, write-offs vs slippage, collateral price (gold LTV) |
| Platform / software | Cohort / account | CAC, retention, take rate |
| **US widely held company (v1.2)** | Same unit as its business type, plus **management as the "related party"** | KPI definitions (payback, comps, "adjusted"), SBC and retention awards, 8-K Item 5.02 pay and perks, Form 4 clusters, guidance-beat pattern |

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
| **L8** | **Valuation and decision (v1.3)** | What does the price imply, and what does the written rule do with it? | **~20 min (outside the 3–4 day budget)** | `tools/valuation/worksheet.py` run (bank mode for lenders) and `tools/decision/decision_card.py` run; card shows every gate; paper calls written (practice: not ingested) |

For a 1-day screen, do L1–L2 plus the L4 top-3 costs plus the L5 RPT table only. **L5's RPT table is never skipped.**

**L2 additions (v1.1), always:**
- **Customer concentration** from the Ind AS 108 footnote ("sales of ₹X derived from N external customers", each ≥10% of revenue). Track N and the share by year. At Cummins it went from 2 customers/21% to 3 customers/31%.
- **Other-income decomposition:** treasury interest, MF gains, group rent, JV/associate dividends. Compute **core PBT = PBT − other income** and use it for multiples. At Cummins, other income was 23% of PBT.
- Screener nets exceptional items into "Other income". Read the AR P&L.

**L5 parent-take table (v1.1), for MNC subsidiaries and group companies.** By year: royalty (rate × eligible base); technical, support and cost-allocation fees; reimbursements paid and received; purchases from group companies (share of purchases) with the pricing formula; sales to group companies (share of revenue, share of exports) with the pricing formula; dividends to the parent; and stock-based pay in *parent* shares. Total it as % of sales and % of EBITDA. List every **agreement renewal date** (royalty agreements often run for 3 years) as a dated watch item. Read the **AGM/postal-ballot RPT annex**: SEBI's Jun-2025 "minimum information" standard makes companies disclose pricing formulas (e.g. "cost plus at least 11%"), royalty rates, uniform-rate confirmations and sunset clauses.

**S2 checklist (v1.3, before L1; ~1 hour).** Fill every disqualifier-v2 rule as pass / fail / unknown with a dated
source *before* starting the layers, so the card never shows "incomplete" (H3 was never checked in the first three
practice runs). Hard at entry: H1a, H1b, H1c, H2, H3, H4, H5. Hard at exit: auditor exit on denied information,
RBI divergence, US 8-K 4.02, results delayed past the deadline. Graded: pledge (>25%, escalate >50% or rising),
accounting-trouble events in 5 years, dilution (price × purpose × buyer), debtor days by counterparty, solvency set.
Questions only: CFO/PAT, negative FCF, other-income share. Sources: `nse_fetch.py announcements/pledge/shareholding/
integrated`, `bse_fetch.py announcements` (catches Reg-30 items the NSE description hides), rating letters, the AR
auditor's report and notes. Lenders: use the bank form of each rule (adaptation section).

**L8 valuation and decision (v1.3; from `research_notes/Templates/valuation_and_decision.md` §5).**
1. Collect the extra inputs the templates need: a **dated close from two sources**, **10 FY-end P/Es (P/B for
   lenders)** for the own-history band, **3+ peer P/Es (P/Bs)**, **6-month ADV**, net cash/debt or (lenders) book
   and pending dilution, and the explicit S2 statuses.
2. Write the scenarios (growth/margin/ROIIC/exit P/E, or ROE path/exit P/B) and probabilities **before** reading the
   price outputs; anchor on the base-rate class first.
3. Run the worksheet; read (a) implied growth or ROE and the base-case IRR, (b) exit multiple vs the DCF/RIM-consistent
   multiple (the hidden bet, L21), (c) re-rating share, (d) temperature vs own history and peers, (e) sensitivity.
4. Fill the card from the deep dive: S2 statuses, PEAD quintile and event date, credibility **with peer median**,
   detector alerts, the L7 override table, base-rate class, sizing tier, dated kill criteria, pre-mortem, review date.
5. Run the card with `--calls`. Practice runs: paper calls tagged `practice-example`, **not ingested** (L21).
6. Write the variant view or accept size 0: ≥3 open soft flags without one blocks the card.

---

## Bank / NBFC adaptation (v1.3, from the Federal Bank dry run)
A lender's revenue, EBITDA, FCF and ROIIC are not meaningful (debt is raw material). Keep the 7 layers but swap the
content as follows.

**S2 in bank form.**
| Rule | Bank form | Where |
|---|---|---|
| H1a fake cash | Cash/RBI balances and investments audited; HTM/AFS marks vs equity (SVB test) | XBRL balance sheet; AR investment schedule |
| H1b/H1c | NIM, yield − CoD, RoA and C/I inside the peer band; every one-off traced to an external document (tax order, sale deed) | deck, Reg-30 |
| H2 | Rotation (RBI mandates joint-auditor terms) vs resignation | Reg-30 "Change in Auditors" text |
| H5 | AS-18 connected lending: loans/NCDs to group entities, KMP relatives; promoter-group "general purpose" loans | AR AS-18 note |
| Exit triggers | **RBI divergence note** ("Divergence in asset classification and provisioning"), restatement, late results | AR notes (1.4.x in FBL's numbering) |
| Solvency set | CET1 vs management floor and regulatory minimum; leverage ratio; LCR/NSFR; CD ratio; ALM 1-year gap | AR capital note, XBRL CET1 |
| Lender signals | Funding concentration (state, NRI, top-20 depositors, bulk share), period-end vs average balances (window dressing), fraud note trend, restructured + SMA book, growth >30%/yr | `insight:lender-blowup-signals` |

**Layers for a lender.**
- **L2:** re-derive PPOP = NII + other income − opex; split other income into fees / treasury / one-offs; rebuild the
  **NPA walk** (opening + slippage − recoveries − **write-offs** = closing); compute ratios on **average** balances;
  separate company "excl one-off" figures and keep both. Read the integrated-filing XBRL (`nse_fetch.py integrated`;
  Q1/Q3 filings carry no balance sheet for banks).
- **L3 unit economics:** per outlet — deposits, CASA, advances, revenue, opex, staff, rent, PAT; liability value of a
  mature branch (CASA × saving vs wholesale rate) vs its direct cost; new-branch break-even CASA; per employee —
  loaded cost vs BRSR median, attrition.
- **L4 cost lines in physical terms:** staff (headcount × **IBA bipartite scale**; settlement dates are dated,
  public, leading); **DICGC premium** (≈ 12 paise per ₹100 of assessable deposits; cross-foot insurance ÷ 0.0012 ≈
  deposits); outsourcing/service charges and card-network charges (scale with volumes); rent per outlet.
  Balance-sheet cost lines that sit in NIM: **CRR** (NDTL × CRR% × opportunity rate), **PSL-shortfall deposits**
  (RIDF/NABARD/SIDBI balance × (loan yield − RIDF rate)), SLR carry.
- **L4 rate and funding mechanics:** EBLR/MCLR/fixed split × repo move = immediate yield change; deposit repricing lag
  (~1 year for TDs); special windows (FCNR, TLTRO-type) that inflate both sides of the balance sheet — always
  re-derive growth **ex** the window (loans against the new deposits).
- **L4 asset quality:** slippage and GNPA by segment ÷ segment book; collateral price sensitivity (gold LTV, property);
  vintage/cohort data if disclosed (rarely; say so); ECL/regulatory transitions dated with the guided impact.
- **L5:** no promoter often — the related parties are management (pay mix, ESOP, variable-pay caps), the strategic
  investor (warrants, board seat), subsidiaries (connected lending); the **CEO's RBI-approved term end** is a dated
  watch item.
- **L6 scuttlebutt:** branch counts and rate boards; a fixed gold-loan price basket vs PSU banks and NBFCs; gold
  auction notices (public, dated); NRI exchange houses; RBI BSR (state deposits/credit), RBI card statistics, NPCI
  bank performance, RBI Ombudsman complaints; fintech-partner apps and directions; union notices on wage talks.
- **L7:** bad-but-benign vs good-but-misleading table is mandatory (at Federal Bank: 10 misleading-good vs 6 benign-bad).

**Valuation (L8) for lenders:** `worksheet.py` with `"mode": "bank"` (`tools/valuation/bank.py`): P/B fully diluted for
warrants/QIPs; ROE needed forever `g + P/B × (CoE − g)`; **implied CoE at today's ROE** `g + (ROE − g) ÷ P/B`;
residual-income scenarios on an ROE path with an exit P/B and its RIM-consistent P/B; book stress (+1/2/3/5% loan
loss as % of book); own 10-yr P/B band and peer P/Bs. Expect the same CoE dominance as L21: read the implied CoE,
the base-case IRR and the P/B band.

**Signals (stage 3) for lenders:** PEAD on reported EPS mixes treasury gains and provision buffers — before acting on
a quintile 1–2 flag, recompute SUE on (PPOP − normal credit cost) per share. Promise tracker: pass website transcripts
with `--local` (banks often file only a cover letter on NSE); build the KPI CSV with `bank_kpis.py` (+ `--manual` deck
KPIs: NIM, CASA, credit cost, CoD, PCR, slippage); report credibility only against a bank peer median (L18) and add a
guidance-bias column (actual − guide midpoint, bps).

**NBFC differences (to test on the next lender run):** no CASA, so the liability unit is the borrowing mix (bank
lines, NCDs, CP, securitisation, ECB) and its ALM; leverage limits and RBI scale-based regulation layer; co-lending
and DLG/FLDG arrangements as off-balance-sheet risk; collection staff per ₹ cr of book as the physical cost driver.

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

### US (rewritten in v1.2 after the Five Below run)
| Layer | Primary sources (in order of value per hour) | Tool |
|---|---|---|
| L1 | 10-K Item 1 (business, store/plant counts, **sourcing %**, vendor concentration, **human capital headcount**); Item 2 Properties (DC/plant sq ft, purchase cost, lease expiry); S-1 for IPOs; peer 10-Ks | `sec_fetch.py filings T --form 10-K`, `doc ... --text` |
| L2 | XBRL companyfacts (10-year table); 10-K Item 7 MD&A (KPI definitions, capex plan, contractual obligations, leases signed after year-end); notes (leases, SBC, PP&E, income taxes, subsequent events); 10-Q for the latest YTD; **8-K Item 2.02 Ex-99.1 non-GAAP reconciliation** (one-offs live here) | `sec_fetch.py facts T --years 10`, `doc --file ex991.htm --text` |
| L3 | 10-K "new store model"/unit-economics paragraph (copy it verbatim); Item 7 "average sales per unit"; capex guidance per unit; pre-opening cost note; lease-note "leases committed, not commenced" $ ÷ count; investor-day decks; transcripts (Motley Fool, company replay; automated transcripts are single-source); FDD Item 19 for franchisors | — |
| L4 | Lease note (Topic 842: operating vs variable lease cost, cash paid vs straight-line, weighted remaining term and rate, maturity table); 10-K human capital (FT/PT/store/DC/corporate headcount by year); **BLS OEWS** (market wage by occupation and metro); DOL/EPI state minimum-wage schedules; EIA diesel and electricity; Drewry/Freightos ocean freight; USITC DataWeb/HTS duty rates; CBP and court rulings for tariff regimes; CoStar/LoopNet rents | `sec_fetch.py search` for full-text terms |
| L5 | **DEF 14A** (pay mix, PSU metrics and whether they are GAAP or adjusted, clawback, Item 404 related parties, director independence); **8-K Item 5.02 exhibits** (offer letters, severance, consulting/perk agreements, retention awards); 8-K 1.01 (credit agreements), 4.01/4.02 (auditor change/non-reliance: hard flags), 8.01; **Form 4** (codes P/S vs A/F/M/G; the 10b5-1 checkbox); Form 144; **13F** (quarterly, 45-day lag, long-only); **13D/13G** (5%+ holders; read the remarks field); Item 3 litigation stage | `sec_fetch.py insider T`, `holdings13f CIK`, `filings T --form "SCHEDULE 13G/A"`, `filings T --form 8-K --items 5.02` |
| L6 | Store/plant visits; store locator scrape (count by state); Glassdoor/Indeed (pay, staffing); LoopNet listings for the centre; Placer.ai-type foot traffic (paid); app downloads; Google Trends; country-of-origin label counts; court records (PACER/CourtListener) | — |
| L7 | memdb `insight:flag-override-template`; false-alarm base (`--tag false-alarm`); L14 insider-signal base rates | — |

**US 10-K reading list (v1.2): read these first, then diff each against last year's 10-K.**
1. **Item 1:** unit model paragraph; sourcing (% domestic vs import, largest country); vendor concentration; human capital (FT/PT/segment headcount); seasonality.
2. **Item 1A:** diff year over year. Deleted or added words are signals (FIVE dropped "(including beyond $5 per item)").
3. **Item 2:** DCs/plants (sq ft, owned/leased, cost, expiry).
4. **Item 3:** litigation stage (motion to dismiss granted/denied, class certification, discovery).
5. **Item 5:** buybacks by month; remaining authorisation.
6. **Item 7:** KPI definitions (comps, average sales per unit and which units it counts); capex plan by use; liquidity; contractual obligations; leases signed after the balance-sheet date.
7. **Item 9A:** material weaknesses.
8. **Notes:** significant accounting policies (what COGS includes: occupancy? distribution?); leases; SBC (unvested units, unrecognised $, weighted period, withheld shares); PP&E; taxes; subsequent events (tariff rulings, refunds).

**SBC handling rule (v1.2).** (a) Report SBC as % of sales, of net income and of FCF. (b) Use **FCF − SBC** as owner cash flow. (c) Add back "adjusted" exclusions that are pay: retention awards, "one-time" equity grants, CEO transition awards. (d) Dilution cost = **the buyback cash needed to hold diluted shares flat**, over 5–10 years. (e) Overhang = unvested RSU + PSU + options ÷ shares. (f) Read the PSU metric in the proxy: if it is "adjusted EPS", check which one-offs the board lets management exclude.

**Form 4 / 13F / 13G reading rules (v1.2).**
- **Form 4.** Only codes P and S are open-market. A/M/F/G are grants, exercises, tax withholding and gifts. Check the 10b5-1 checkbox on the form itself; the parser flag is not enough. Clusters of sales after a rally or a vesting window are weak (L14). Open-market buys by several insiders are the only Form 4 pattern worth a prior.
- **13F.** Long-only, 45 days late, no shorts. Compare share counts, not values (the tool's value units can misparse).
- **13G/A.** Read the **remarks** before reading a 0%. Vanguard's 12-Jan-2026 realignment made its 13G/As show 0% with no sale.
- **Proxy beneficial-ownership table:** management plus directors as a group.

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
19. **Company store model vs its own capex guidance (v1.2).** Divide the capex budgeted "for new stores" by planned gross openings. Compare it with the "new store investment" in the 10-K, then rebuild that investment (build-out − tenant allowance + inventory net of payables + pre-opening). If the tenant allowance needed to reconcile is implausible (more than ~40% of build-out), the headline payback is stale or narrowly defined. Add network capex (DCs, systems) ÷ stores served. (FIVE: $100M / ~155 = $0.65M gross vs "$0.4M"; DCs ~$0.14M per store.)
20. **Rent per new lease from the lease note (v1.2).** "Committed to N new leases … future minimum payments $X" ÷ N ÷ term = base rent per unit per year; ÷ model sq ft = $/sq ft. Repeat with the post-year-end lease sentence in Item 7 for a fresh read. Variable lease cost ÷ net lease cost = CAM/tax/%-rent share.
21. **Tariff cost from refunds and duty math (v1.2).** A refund booked through COGS reveals the tariff cost actually borne. Divide by direct-import FOB (purchases × import share ÷ (1 + rate)) for the effective rate. Split importer-of-record exposure (refundable) from domestic-vendor exposure (embedded in vendor prices, not refundable to you) and ask who gets the vendors' refunds.
22. **Guidance implied-remainder (v1.2).** From a full-year guide and the year-to-date actual, solve for the implied remaining-quarter figure (weight comps by the prior year's quarterly sales). Compare it with the beat history (actual − guide midpoint, last 4–6 quarters). Score long-range (investor day) and near-term promises separately, and by management team.
23. **US payroll estimate when not disclosed (v1.2).** Route A: SG&A − advertising − SBC − pre-opening − corporate (headcount × loaded salary) = store payroll. Route B: unit-level crew (10-K human capital ÷ units) × hours × market wage (BLS OEWS metro) × 1.15 load. The sensitivity unit is bps per 1% wage and per $1/hour.

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
- [ ] **US filers (v1.2):** 10-K item/note reading list done with a year-over-year text diff; non-GAAP reconciliation table by quarter; SBC table (SBC % of sales/NI/FCF, FCF − SBC, overhang, buyback-to-hold-flat); Form 4 summary (P/S only, 10b5-1 checked); 13F/13G holder changes with remarks read; management-change table from 8-K 5.02; promise tracker split long-range vs near-term
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
- [ ] **S2 checklist (v1.3):** every disqualifier-v2 rule pass/fail/unknown with a dated source, filled before L1
- [ ] **L8 (v1.3):** worksheet run (bank mode for lenders) + decision card + paper calls; extra inputs collected (two-source dated close, 10 FY-end P/Es or P/Bs, 3+ peers, 6-month ADV, pending dilution)
- [ ] **Lenders (v1.3):** NPA walk with write-offs; growth ex special funding windows; per-outlet table; Schedule-16 cost table incl. DICGC and the PSL-shortfall line; funding-concentration table (state, NRI, top-20, bulk, period-end vs average); bad-but-benign / good-but-misleading table

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
- (v1.2) **US GAAP gross margin is not comparable across retailers.** Some put occupancy, distribution and buying in COGS (FIVE); others put them in SG&A. Compare operating margin, or rebuild merchandise margin.
- (v1.2) **One-off credits inside COGS.** FIVE's Q2 FY26 GAAP gross margin of 48.5% included a $163.6M tariff refund. Trailing GAAP EPS screens are wrong for four quarters. Always read the Ex-99.1 reconciliation.
- (v1.2) **Ownership-filing false alarms.** Vanguard's 13G/A shows 0% after its Jan-2026 realignment. The 13F still shows the shares.
- (v1.2) **"Average sales per store" usually counts only stores open the full year.** Also compute total sales ÷ average store count.
- (v1.2) **FCF in a slowdown-of-openings year is flattered** (capex and working-capital timing). Normalise before using it.
- (v1.2) **Tool notes:** use `sec_fetch.py doc T ACC --file NAME --text` for exhibits; `holdings13f` value can misparse (use shares); confirm the insider "non-10b5-1" flag on the form.
- (v1.1) **Tool note:** `tools/nse_fetch.py transcripts SYMBOL --download DIR` ignores `--from/--to` and downloads everything. List first, then fetch only the URLs you need.
- (v1.3) **"Decadal-low GNPA" can be write-off driven.** Rebuild the NPA walk: at Federal Bank Q2 FY27 write-offs (₹498 cr) exceeded fresh slippage (₹420 cr).
- (v1.3) **Special funding windows inflate both sides.** FCNR-backed loans turned +4% core retail growth into +18% headline.
- (v1.3) **PCR can be bought with a windfall.** A one-time tax-refund gain funded a buffer provision; PCR 76.6% → 87%.
- (v1.3) **Undiluted P/B and ROE flatter a bank with warrants outstanding.** Put the dilution in the denominator first.
- (v1.3) **Conservative guidance makes a credibility score look excellent.** Measure guidance bias, and compare with peers.
- (v1.3) **Rating-agency and company KPI definitions differ** (credit cost 67 bp vs 41 bp; "top-20 group" vs "top-20 borrowers"). Copy the definition with the number.
- (v1.3) **Tool notes:** `nse_fetch.py results` is stale after Dec-2024 (use `integrated`); bank websites may be behind a bot wall (Pillar 3, some transcripts) — fetch by hand and pass `--local`; pdftotext scrambles multi-series deck charts (prefer XBRL and press releases).

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
- **v1.2 · 2026-11-21.** From the Five Below practice run (US specialty retailer, first US filer):
  - Rewrote the US data-source table by layer, with tools.
  - Added the US 10-K item/note reading list (with a year-over-year text diff), the SBC handling rule, and Form 4 / 13F / 13G reading rules.
  - Added a "US widely held company" row to the unit table (management as the related party).
  - New techniques #19 (store model vs capex guidance), #20 (rent per new lease from the lease note), #21 (tariff cost from refunds and duty math), #22 (guidance implied-remainder and split promise tracking) and #23 (US payroll estimate).
  - One new deliverable line and six new traps/tool notes.
- **v1.3 · 2026-11-22.** From the Federal Bank end-to-end dry run (stages 2→6; first lender):
  - Added the **S2 checklist** step before L1 (every disqualifier-v2 rule with a dated source), so the card is never "incomplete".
  - Added **L8 valuation and decision** (worksheet + card + paper calls) per `research_notes/Templates/valuation_and_decision.md` §5, with the extra inputs it needs (two-source close, 10 FY-end P/Es or P/Bs, peers, ADV, dilution).
  - Added the **Bank / NBFC adaptation** section: S2 in bank form, lender units (branch, segment, liability pool, balance-sheet cost lines), physical cost drivers (IBA scale, DICGC, CRR, PSL shortfall), rate/funding mechanics, asset-quality walk, valuation in bank mode, signal caveats, NBFC differences to test next.
  - Replaced the one-line "Lender" row in the unit table.
  - Three deliverable lines; seven traps/tool notes.
  - Tools changed with it: `tools/valuation/bank.py` (+ `worksheet.py` dispatch), `tools/decision/decision_card.py` (bank stage-5 text), `tools/promise_tracker/pipeline/` (bank measures, cover-letter handling, `--local`, quarter detection, range-parse and chain fixes, `bank_kpis.py`), `tools/nse_fetch.py integrated`.
