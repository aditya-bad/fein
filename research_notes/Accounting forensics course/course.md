# Accounting forensics: a practical course (India + US)

*Built 2026-11-20. Teaches how to read financial statements the way a forensic analyst does. Every worked example uses a real filing or a real data aggregator page, cited at the end of each lesson.*

**How to use this.** Do one lesson per sitting. Work each example yourself before you read the answer. The exercises use the same real numbers. Answers are at the end of each lesson.

**What this course adds to memdb.** It builds on records that already exist and does not repeat them:
- `insight:forensic-redflag-checklist` is the 18-flag checklist distilled from about 30 blow-ups.
- `insight:ind-as-accounting-levers` lists where reported profit and owner earnings diverge under Ind AS.
- `insight:beneish-m-score`, `insight:altman-z-score` and `insight:piotroski-f-score` give the definitions and cut-offs.
- `strategy:read-10k-efficiently` and `strategy:us-forensic-screen-workflow` cover the US filing workflow.

This course adds the mechanics: how to compute each test, which thresholds to use, worked numbers from real companies, and exercises.

**Data conventions**
- Indian figures are in ₹ crore, consolidated, from Screener.in (pages read 2026-11-20). Screener is a single aggregator, so every Indian number is **single-source** until you tie it to the annual report.
- US and IFRS figures come from SEC XBRL companyfacts (`tools/sec_fetch.py`), and each one carries its accession number. Those are primary filings.
- Screener folds exceptional items into "Other Income". Its "Free Cash Flow" is CFO minus capex, with no deduction for lease payments. Both conventions matter in the lessons below.
- This is research and self-education, not SEBI-registered advice.

**The one idea behind everything.** Profit is an opinion and cash is a fact, though cash can be managed too. Each technique below asks one of three questions:
1. Did the accrual turn into cash?
2. Was a cost moved somewhere you are not looking, such as the balance sheet, the CFF section, a subsidiary or a footnote?
3. Will this number recur?

---

## Lesson 1: Reading the cash-flow statement

### 1.1 CFO vs PAT: the master test

**Formula.** Take cumulative CFO over N years and divide it by cumulative PAT over the same years. Use N = 5, because single years are noisy.

**Thresholds (practitioner convention; Marcellus-style screens use CFO/EBITDA of at least 70–80%).**

| Ratio | Reading |
|---|---|
| ≥ 0.9 | Healthy |
| 0.7–0.9 | Explain it |
| < 0.7 | Red flag (flag #1 in `insight:forensic-redflag-checklist`) |
| < 0 while PAT is positive for 3+ years | Presumptively disqualifying until explained |

**Worked example A: Gensol Engineering (GENSOL), consolidated, FY20–FY24**

| | FY20 | FY21 | FY22 | FY23 | FY24 | Σ |
|---|---|---|---|---|---|---|
| PAT | 2 | 3 | 11 | 23 | 53 | **92** |
| CFO | −18 | 6 | −50 | 115 | −98 | **−45** |
| Capex (CFO − FCF) | 0 | 0 | 51 | 439 | 479 | 969 |
| FCF | −18 | 6 | −101 | −324 | −577 | **−1,014** |
| Borrowings (year-end) | 11 | 11 | 82 | 598 | 1,510 | |

- Cumulative CFO/PAT = −45 / 92 = **−0.49**.
- Reported profit grew 26x over the period, while the business consumed cash every year except one.
- The ₹1,014 cr of FCF burn was funded by borrowings, which rose ₹1,499 cr, and by equity.
- SEBI's interim order of 15-Apr-2025 later found that EV term loans had been diverted to promoter uses (see `insight:ind-as-accounting-levers`).
- **Visible at the time:** CFO was negative in 3 of 5 years while PAT compounded, and debtor days stood at 86 in FY24. The cash test alone would have kept you out.

**Worked example B: Asian Paints (ASIANPAINT), FY22–FY26. A quality company with one bad year.**

| | FY22 | FY23 | FY24 | FY25 | FY26 | Σ |
|---|---|---|---|---|---|---|
| PAT | 3,085 | 4,195 | 5,558 | 3,710 | 4,395 | 20,943 |
| CFO | 986 | 4,193 | 6,104 | 4,424 | 7,088 | 22,795 |

- FY22 CFO/PAT was **0.32**. Inventory was built during the raw-material inflation, and CCC went from 59 days to 94.
- The 5-year ratio is **1.09**.
- **Lesson:** one bad year in a business with a long clean history is a working-capital swing. Several bad years in a young, fast-growing business is a pattern. Always look at the cumulative figure.

### 1.2 Working-capital swings inside CFO

CFO = PAT + non-cash charges ± changes in working capital. A sudden jump in CFO can come from:
- delaying payments to suppliers (a payables stretch)
- selling receivables (factoring)
- collecting customer advances

All three reverse later. **Test:** split CFO into (a) CFO before working-capital changes and (b) the working-capital change. If (b) supplies more than about 30% of CFO two years running, ask which line moved and whether it can repeat.

### 1.3 Factoring and supply-chain (reverse) finance: CFO that is really debt

- **Factoring or receivable discounting without recourse.** The receivable leaves the balance sheet and the cash lands in CFO. Economically it is a loan against your sales.
- **Supplier finance (reverse factoring).** A bank pays your supplier on day 30 and you repay the bank on day 120. Your payables stay "trade payables", and CFO looks better by the stretched amount.
- **Disclosure.** Since FY2023, US GAAP ASU 2022-04 requires companies to disclose supplier-finance obligations. The XBRL tag is `SupplierFinanceProgramObligation`, and 87 filers tagged it at CY2025Q4. IFRS (IAS 7/IFRS 7 amendments, May 2023, effective 2024) now requires similar disclosure. Ind AS has amended Ind AS 7 and 107 to match, so check the "supplier finance arrangements" note in FY26 Indian annual reports.

**Worked example C: Advance Auto Parts (US-AAP). SEC XBRL, 10-K accession 0001193125-26-051305.**

| $ m | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Accounts payable | 3,526 | 3,408 | 2,977 |
| of which supplier-finance obligations | **3,400** | 3,200 | 2,500 |
| COGS (continuing) | 5,349 | 5,685 | 4,868 |
| Payable days (AP/COGS×365) | **241** | 219 | 223 |
| Inventory days | 266 | 232 | 273 |
| CFO (total) | 287 | 85 | **−46** |

- About **96%** of FY23 payables sat in a bank programme.
- AAP funded inventory with roughly 8 months of "trade credit" that was bank credit.
- As the programme shrank by $0.9 bn over two years, CFO fell from +$287 m to −$46 m.
- **Lesson:** add supplier-finance obligations to debt when you compute leverage. Treat a programme that is shrinking as a cash outflow coming your way.

### 1.4 Capitalised costs: moving expenses out of CFO

An expensed cost reduces CFO. A capitalised cost shows up in CFI as capex or "intangible additions", and CFO looks stronger. Common versions:
- capitalised software or development (Ind AS 38)
- capitalised borrowing costs (Ind AS 23)
- "pre-operative expenses" in CWIP
- customer-acquisition costs (ASC 340-40 / Ind AS 115 "costs to obtain a contract")
- the WorldCom pattern: ~$3.8 bn of line costs capitalised in 2001–02 (SEC complaint, 2002)

**Test:** use FCF, not CFO. Compare capex and intangible additions with depreciation, with peers, and with the company's own history. Capex that rises without revenue growth is a warning.

### 1.5 Classification games

| Item | Ind AS 7 / IAS 7 (today) | US GAAP ASC 230 | Effect |
|---|---|---|---|
| Interest paid | Operating **or financing** (policy choice) | Operating | Indian companies that put interest in CFF show higher CFO than a US peer would |
| Interest/dividends received | Operating or investing | Operating | Treasury income can sit in CFI |
| Lease principal (Ind AS 116 / ASC 842 finance) | Financing | Operating-lease cash = operating | Under Ind AS, CFO is inflated by the whole lease bill (see Lesson 4.6) |
| Acquisition of a business | Investing | Investing | Buying growth keeps CFO "clean". Serial acquirers report high CFO and low FCF after M&A |
| Loans made by a lending subsidiary | Operating (for an NBFC) | Operating | Conglomerate CFO gets distorted (below) |

**IFRS 18** (effective 2027 for IFRS reporters) removes the policy choice for most non-financial companies: interest paid goes to financing, and interest and dividends received go to investing. As of this writing India has **not** notified an Ind AS equivalent, so treat Indian-vs-IFRS comparisons with care. Re-check before FY28.

**Worked example D: Larsen & Toubro (LT), consolidated. CFO below PAT for years.**

| | FY15 | FY16 | FY17 | FY18 | FY19 |
|---|---|---|---|---|---|
| PAT | 4,966 | 4,592 | 6,486 | 8,004 | 10,217 |
| CFO | −1,365 | −3,240 | 6,655 | −10,031 | −4,756 |

- L&T is not hiding losses. Consolidated CFO includes the loan-book growth of L&T Finance, its lending subsidiary, which is operating cash for an NBFC.
- From FY21, once the financial-services book stopped growing, CFO turned strongly positive: 23,074 in FY21 and 22,777 in FY23.
- **Lesson:** for conglomerates, read the segment or standalone cash flow, or strip out the financing arm. Use the ratio as a question, not an answer.

### 1.6 FCF definitions (use one consistently)

| Name | Formula | Use |
|---|---|---|
| Simple FCF | CFO − capex | Screener's definition. Misleading for lease-heavy firms and for firms that put interest in CFF |
| FCF to firm (forensic) | CFO − capex − capitalised intangibles − lease payments (principal + interest) − interest paid (if in CFF) | Comparable across Ind AS and US GAAP |
| Owner earnings (Buffett 1986) | PAT + D&A − maintenance capex ± WC needed to hold position | Valuation |
| FCF after SBC (US) | FCF − stock-based compensation | US tech, where SBC is a real cost (see `insight:us-redflag-sbc-dilution`) |
| FCF after acquisitions | FCF − net cash on acquisitions | Serial acquirers |

### Exercises, Lesson 1

1. Using the Gensol table, compute FY23 alone: CFO/PAT and FCF/PAT. What made FY23 look "good"?
2. IndiGo (INDIGO) FY26: PAT −2,394, CFO +23,470, CFF −21,276, and Screener "FCF" +21,767. Explain in two sentences why "FCF 21,767" overstates the cash owners can take out.
3. AAP: if a lender cut the supplier-finance programme to zero overnight, what is the maximum one-time hit to CFO implied by the FY25 numbers, and how does it compare with FY25 CFO?
4. A company reports CFO ₹500 cr. Its notes show ₹180 cr of interest paid classified in CFF and ₹120 cr of lease principal and interest paid in CFF. Restate a US-GAAP-comparable "CFO" (treat the leases as operating leases).

### Answers, Lesson 1

1. FY23 CFO/PAT = 115/23 = **5.0**, and FCF/PAT = −324/23 = **−14.1**. CFO looked strong because of the working-capital release that year: working-capital days went from 132 to −9, consistent with customer advances or payables. Capex of ₹439 cr was being bought with debt.
2. Under Ind AS 116, aircraft lease repayments (principal and interest) sit in CFF, not CFO, so CFO overstates the cash the operations generate. CFF of −21,276 is mostly lease and debt servicing, which is an unavoidable operating cost for an airline. Lease-adjusted FCF is roughly 23,470 − 1,703 − ~20,000 ≈ **near zero**. (Approximate; take the lease-payment line from the annual report's cash-flow note.)
3. $2.5 bn. That is about **54x** FY25 CFO of −$46 m in absolute size, and roughly 29% of FY25 revenue. The programme is existential-scale.
4. 500 − 180 − 120 = **₹200 cr**. The headline CFO was 2.5x the comparable figure.

*Sources, Lesson 1:*
- https://www.screener.in/company/GENSOL/consolidated/
- https://www.screener.in/company/ASIANPAINT/consolidated/
- https://www.screener.in/company/LT/consolidated/
- https://www.screener.in/company/INDIGO/consolidated/ (all read 2026-11-20)
- SEC XBRL AAP companyfacts https://data.sec.gov/api/xbrl/companyfacts/CIK0001158449.json (10-K 0001193125-26-051305)
- SEC frames `SupplierFinanceProgramObligation` CY2025Q4I https://data.sec.gov/api/xbrl/frames/us-gaap/SupplierFinanceProgramObligation/USD/CY2025Q4I.json
- FASB ASU 2022-04 https://www.fasb.org/page/getarticle?uid=fasb_Media_Advisory_09-29-22
- IAS 7 paras 31–34 https://www.ifrs.org/issued-standards/list-of-standards/ias-7-statement-of-cash-flows/
- IFRS 18 https://www.ifrs.org/issued-standards/list-of-standards/ifrs-18-presentation-and-disclosure-in-financial-statements/
- SEC v. WorldCom (2002) https://www.sec.gov/litigation/complaints/complainta.htm
- SEBI Gensol interim order (15-Apr-2025) per `insight:ind-as-accounting-levers`

---

## Lesson 2: Working capital

### 2.1 The day counts

| Metric | Formula | Notes |
|---|---|---|
| Debtor days (DSO) | Trade receivables / Revenue × 365 | Use average receivables if they are seasonal |
| Inventory days (DIO) | Inventory / COGS × 365 | Screener uses sales when COGS is unavailable, so its figures run lower |
| Payable days (DPO) | Trade payables / COGS (or purchases) × 365 | |
| Cash conversion cycle | DSO + DIO − DPO | |
| **Total DSO (IT/EPC)** | (Receivables + unbilled revenue/contract assets) / Revenue × 365 | This is the one that catches front-loaded revenue |

**Thresholds.**
- **Trend:** DSO or DIO rising more than about 15 days a year for 2+ years while revenue grows (flag #5 in `insight:forensic-redflag-checklist`).
- **Level:** compare with peers and with the business model. An FMCG company should run a negative CCC, a jeweller about 150–250 days, an EPC company 60–150 days with advances netted.
- **Divergence:** receivables growth more than 1.5x revenue growth.

**Worked example E: PC Jeweller (PCJEWELLER). A working-capital death spiral.**

| | FY18 | FY19 | FY20 | FY21 | FY22 | FY24 |
|---|---|---|---|---|---|---|
| Sales | 9,610 | 8,672 | 5,206 | 2,825 | 1,605 | 604 |
| PAT | 536 | 1 | 83 | 62 | −391 | −629 |
| CFO | 358 | **−1,931** | 76 | 91 | −719 | 64 |
| Inventory days | 232 | 227 | 434 | 954 | 1,465 | **3,044** |
| Payable days | 160 | **57** | 87 | 150 | 4 | 7 |
| Borrowings | 1,116 | 2,121 | 2,429 | 2,414 | 3,391 | 4,150 |

- In FY19, payable days collapsed from 160 to 57: suppliers (gold-metal-loan lenders) stopped extending credit.
- The ₹1,931 cr CFO outflow was funded with ₹1,005 cr of new borrowings. Inventory never turned back into cash.
- **Signal:** the first year payables fall while inventory stays flat is the moment trade creditors have lost confidence. Creditors often know before shareholders do.

**Worked example F: Hindustan Unilever (HINDUNILVR). What "good" looks like.**
- CCC ran between −50 and −107 days over FY15–FY26 (FY26: −89).
- Suppliers and distributors fund the business, so growth releases cash.
- The test for an FMCG company is whether the CCC is **deteriorating**, not where its level sits.

### 2.2 Channel stuffing: signs
- Receivables grow faster than revenue, especially in Q4. Compare Q4 debtor days with Q2/Q3 in the quarterly balance sheets that Indian companies now file half-yearly.
- Gross margin falls while volume rises, a sign of discounts to push stock.
- Distributor or dealer inventory rises. Read channel checks and listen for the con-call phrase "inventory correction in trade" the following quarter.
- Returns provisions or "refund liabilities" (an Ind AS 115 line) rise, or credit notes are issued after year-end (subsequent-events note).
- The classic US case is Bristol-Myers Squibb, which paid $150 m to settle SEC charges in 2004 over inflated wholesaler inventory of about $1.5 bn in 2000–01.

### 2.3 Unbilled revenue and contract assets (IT services, EPC)

Under Ind AS 115 / ASC 606, revenue recognised before the right to bill becomes a **contract asset**. Under Ind AS presentation it is also called "unbilled revenue". If only the passage of time stands between the company and the cash, it is an unbilled **receivable**. Unbilled revenue is the riskiest receivable: the customer has not yet accepted an invoice.

**Worked example G: Infosys vs Wipro. IFRS 20-F XBRL.**

| | Infosys FY23 | Infosys FY25 | Wipro FY23 | Wipro FY25 |
|---|---|---|---|---|
| Revenue | $18,212 m | $19,277 m | ₹90,488 cr | ₹89,088 cr |
| Trade receivables | 3,094 | 3,645 | 12,635 | 11,775 |
| Accrued income / contract assets | 2,037 | 1,764 | 2,300 | 1,580 |
| Billed DSO | 62 d | 69 d | 51 d | 48 d |
| Unbilled days | 41 d | 33 d | 9 d | 6 d |
| **Total DSO** | **103 d** | **102 d** | **60 d** | **55 d** |

- Infosys carries about a month of revenue as unbilled. That is structural (fixed-price and milestone contracts), and it is stable, so it is not a flag.
- Wipro's unbilled balance fell by a third. Contract assets shrinking while revenue is flat is a sign of **cleaner** quality, not worse.
- **The flag:** unbilled days rising for 2+ years while billed DSO is also rising. In EPC, add "contract assets net of contract liabilities (customer advances)" and track it against the order book.

### 2.4 Business-model change (gross-up) and working capital: Eternal (ETERNAL)
- Blinkit moved to an inventory-led model in FY26. Revenue went from 20,243 to **54,364 (+169%)**, but management reported like-for-like growth at a fraction of that (see Lesson 3.3).
- The working-capital profile flipped. Payable days fell from 101 to 36, CCC went from −54 days to +2, and FCF went from −623 to −1,114.
- **Lesson:** when the revenue definition changes, recompute every per-revenue ratio (margins, DSO, asset turnover) on a like-for-like basis.

### Exercises, Lesson 2
1. Suzlon (SUZLON): inventory days were 355 (FY19) and 400 (FY20), payable days 265 and 253. Compute the CCC for each year and name the funding source that kept Suzlon alive in those years.
2. SMCI FY2026 (US): receivables $6,125 m, revenue $39,063 m, inventory $12,896 m, COGS $34,836 m. Compute DSO and DIO. In FY2025 DSO was 36.6 days. What does the change suggest?
3. A ₹2,000 cr EPC firm has receivables of ₹500 cr, contract assets of ₹700 cr and customer advances of ₹200 cr. Compute total DSO and net-of-advances DSO.

### Answers, Lesson 2
1. FY19: 137 + 355 − 265 = **227 days**. FY20: 168 + 400 − 253 = **315 days** (matches Screener). Vendors carried roughly 250+ days of payables, and lenders rolled over about ₹11,500–13,200 cr of borrowings until the FY21 restructuring (borrowings then fell to 6,925). Survival depended on creditors, not customers.
2. DSO = 6,125/39,063×365 = **57.2 days**. DIO = 12,896/34,836×365 = **135 days**. DSO jumped 21 days in a year while revenue rose 78%, and CFO was −$6.8 bn. Either sales are being made on longer terms to win volume or collections are slipping. In either case, growth is being financed by SMCI's balance sheet. Feed this into Beneish's DSRI in Lesson 5.
3. Total DSO = (500 + 700)/2,000 × 365 = **219 days**. Net of advances: (1,200 − 200)/2,000 × 365 = **183 days**. Contract assets exceed billed receivables, so ask for the ageing of unbilled balances and for any arbitration claims included in them.

*Sources, Lesson 2:*
- https://www.screener.in/company/PCJEWELLER/consolidated/
- https://www.screener.in/company/HINDUNILVR/consolidated/
- https://www.screener.in/company/ETERNAL/consolidated/
- https://www.screener.in/company/SUZLON/consolidated/ (read 2026-11-20)
- SEC XBRL Infosys (20-F 0000950170-25-091925) https://data.sec.gov/api/xbrl/companyfacts/CIK0001067491.json
- Wipro (20-F 0000950170-25-076303) https://data.sec.gov/api/xbrl/companyfacts/CIK0001123799.json
- SMCI (10-K 0001375365-26-000022)
- SEC BMS settlement https://www.sec.gov/news/press/2004-105.htm
- Eternal model shift: https://inc42.com/buzz/eternal-q1-profit-rises-3x-yoy-to-%e2%82%b992-cr-but-declines-47-sequentially/

---
## Lesson 3: Revenue recognition

### 3.1 The five-step model (Ind AS 115 = ASC 606, converged in substance)
1. Identify the contract.
2. Identify the performance obligations (POs).
3. Determine the transaction price, including variable consideration, which is constrained.
4. Allocate the price to the POs.
5. Recognise revenue when or as each PO is satisfied, either **over time** or **at a point in time**.

Every judgement sits in steps 2, 3 and 5. Read the revenue note's "significant judgements" paragraph, and in the US read the auditor's Critical Audit Matter on revenue.

### 3.2 Percentage-of-completion (over-time recognition) in EPC, defence, real estate and software

**Mechanics.**
- Revenue to date = (cost incurred to date / total estimated cost) × contract price.
- If management lowers its estimated total cost, the percentage complete rises, and revenue and margin are front-loaded.
- **Forensic tests:**
  - (a) Contract assets / revenue trend (Lesson 2.3).
  - (b) "Changes in estimates" disclosures, including cumulative catch-up adjustments.
  - (c) Onerous-contract provisions appearing late. Wipro booked a ₹160 cr short-term onerous-contract provision in FY24 and ₹129 cr in FY25 (20-F XBRL).
  - (d) Claims and variations included in revenue before the customer agrees. Look for "claims under arbitration" inside contract assets.

**Worked micro-example (illustrative numbers).**

| | Original estimate | Revised estimate |
|---|---|---|
| Contract price | ₹1,000 cr | ₹1,000 cr |
| Estimated total cost | ₹800 cr | ₹720 cr |
| Cost incurred, year 1 | ₹400 cr | ₹400 cr |
| Percentage complete | 50% | 400/720 = 55.6% |
| Revenue | ₹500 cr | ₹556 cr |
| Year-1 margin | ₹100 cr | ₹156 cr (+56%) |

Revising the estimate changes **no cash**. If the original estimate proves right, the ₹56 cr reverses later.

### 3.3 Gross vs net (principal vs agent)
- A principal books the gross sale price. An agent books only the commission.
- The test is whether the company **controls** the good before transfer: inventory risk, pricing discretion and primary responsibility.
- Gross-up does not change profit, but it inflates revenue, distorts margins, turnover and P/S, and it is a favourite way to "grow" ahead of an IPO.

**Worked example H: Eternal (ETERNAL), FY25 to FY26.**
- Consolidated revenue went from 20,243 to 54,364 (+169%). TTM revenue is 77,956.
- Blinkit moved to an owned-inventory model, so it now books the full value of goods instead of a marketplace commission.
- Like-for-like, management reported Q3 FY26 group growth of about 64–66% YoY against about 173% reported.
- OPM fell from 3.1% to 2.2% mechanically.
- **Lesson:** on any business-model change, value the company on gross order value, net revenue or contribution, not on reported revenue. Never compare P/S across the change.
- Classic US agent-vs-principal disputes: Groupon (2011 S-1 restated to net revenue after SEC comments) and travel OTAs.

### 3.4 Bill-and-hold
- This is revenue recognised while the goods stay in the seller's warehouse.
- Ind AS 115 / ASC 606 (B79–B82) allow it only if all four conditions hold:
  1. The customer requested the arrangement for a substantive reason.
  2. The goods are identified separately as the customer's.
  3. The goods are ready for physical transfer.
  4. The seller cannot use them or redirect them to another customer.
- **Classic case: Sunbeam (1997).** SEC enforcement found that a large share of Sunbeam's 1997 record earnings came from improper bill-and-hold and "early buy" sales. The 1997 net income of $109 m was later restated sharply lower, and Sunbeam filed for bankruptcy in 2001.
- **Signs:**
  - inventory "held for customers" or finished goods rising at quarter-end
  - receivables spiking while shipments (freight costs, e-way bill data in India) do not
  - Q4 revenue share rising year after year

### 3.5 Related-party revenue
- Under Ind AS 24 and SEBI LODR Reg 23, material related-party transactions need prior audit-committee approval, plus shareholder approval above ₹1,000 cr or 10% of turnover. The Companies Act s.188 also applies.
- **Tests:**
  - (a) RPT sales / total revenue. Above 10% needs a reason; rising and above 20% is a flag.
  - (b) Margins on RPT sales against third-party sales.
  - (c) Receivables from related parties against their share of revenue. A slow-paying related party means the cash is circular.
  - (d) Year-end round-tripping: sales to a related party, then a purchase or advance back.
- SEBI's Dec-2024 memo on SME IPOs documented "fraudulent sales and purchases through circular transactions amongst related parties" (see `insight:ind-as-accounting-levers`). Brightcom (`case_study:brightcom`) and Satyam fit the same family.

### Exercises, Lesson 3
1. An EPC firm's revenue grew 25%, but contract assets grew 60% and CFO fell. Which three disclosures do you read first?
2. Platform X books ₹100 cr of GMV as a marketplace (15% take rate), then moves to an inventory model with a 15% gross margin. What happens to revenue, gross profit and gross margin %?
3. A consumer-durables company's Q4 share of annual revenue went 28%, 31%, 35% over three years, and its year-end finished-goods inventory rose. Name the two hypotheses and one data point that separates them.

### Answers, Lesson 3
1. (a) The contract-asset ageing and the movement table: how much was billed out of opening contract assets. (b) Changes in estimates and cumulative catch-ups, plus onerous-contract provisions. (c) Claims and variations included in revenue, arbitration, and liquidated-damages exposure in contingent liabilities.
2. Revenue goes from ₹15 cr to ₹100 cr (6.7x). Gross profit stays about ₹15 cr. Gross margin goes from ~100% (agent revenue) to 15%. Economics are unchanged, but working capital now carries inventory.
3. H1: genuine seasonality or a product-launch shift. H2: channel stuffing or bill-and-hold. The separator is early-next-year evidence: Q1 receivables collection and returns or credit notes (subsequent events), or dealer-inventory channel checks. H2 shows Q1 receivables still high and returns spiking.

*Sources, Lesson 3:*
- Ind AS 115 (MCA) https://www.mca.gov.in/MinistryV2/indianaccountingstandards.html
- ASC 606 https://asc.fasb.org/606
- SEC v. Sunbeam https://www.sec.gov/litigation/litreleases/lr17001.htm
- Wipro 20-F XBRL (0000950170-25-076303)
- Eternal https://inc42.com/buzz/eternal-q2-profit-tanks-63-yoy-to-inr-65-cr-revenue-up-183-yoy/ and https://yourstory.com/2026/04/zomato-parent-eternal-revenue-jumps-blinkit-drives-growth
- https://www.screener.in/company/ETERNAL/consolidated/
- SEBI LODR Reg 23 https://www.sebi.gov.in/legal/regulations/
- SEBI SME memo per `insight:ind-as-accounting-levers`

---

## Lesson 4: Balance-sheet quality

### 4.1 CWIP that never completes
- Capital work-in-progress is not depreciated. Interest on it can be capitalised (Ind AS 23), and "pre-operative" costs can be parked in it.
- A project that never finishes therefore keeps expenses out of the P&L indefinitely.
- Since FY22, Schedule III (MCA amendment of 24-Mar-2021) requires a **CWIP ageing schedule** in four buckets: <1y, 1–2y, 2–3y, >3y. It also requires disclosure of projects that are overdue or over budget.

**Tests.**

| Test | Flag |
|---|---|
| CWIP / (net block + CWIP) | Above 30% for 3+ years in a non-greenfield company |
| CWIP older than 2 years / total CWIP | Above 25% |
| Capitalised borrowing cost / total finance cost | Above 20% (check the Ind AS 23 note) |
| CWIP grows but revenue capacity does not | Ask which project, its start date and its COD date |

**Worked example I (magnitude, legitimate): Reliance Industries.**
- CWIP was 338,855 at FY24 against fixed assets of 779,985, or **30%** of net block plus CWIP.
- It fell to 237,686 by FY26 (17%) as Jio 5G and the new-energy assets were capitalised.
- Interest went from 23,118 to 27,061 and depreciation from 50,832 to 57,688 over FY24–FY26.
- **Lesson:** when a large CWIP balance capitalises, depreciation and interest stop being hidden and EPS growth slows. Model that before it happens.
- The forensic version is a small company whose CWIP keeps rising while gross block does not. Gensol's CWIP went 41 → 88 → 171 (Sep-24) while fixed assets fell from 723 to 257.

### 4.2 Intangibles, goodwill and capitalised R&D
- Under Ind AS 38 / IAS 38, development cost **must** be capitalised once technical feasibility, intent, ability, future benefit and measurability are shown. US GAAP ASC 730 **expenses** R&D, with narrow software exceptions (ASC 350-40, 985-20).
- An Indian auto or pharma company can therefore report higher EBITDA and EPS than a US peer with the same R&D cash.
- **Tests:**
  - capitalised development / total R&D spend over time
  - amortisation period against product life
  - "intangible assets under development" ageing (also a Schedule III requirement)
- Goodwill is not amortised under either system (impairment test only). Watch for impairment tests with high terminal growth or low discount rates, which the auditor's CAM or Key Audit Matter will name.
- **Rule:** if goodwill plus intangibles exceed equity, compute tangible book value and ROCE on tangible capital as well.

### 4.3 Deferred tax
- **A DTA on carry-forward losses** needs "convincing evidence" of future profit (Ind AS 12). Recognising or reversing it moves PAT without cash.

**Worked example J: Suzlon (SUZLON).**

| | FY24 | FY25 | FY26 |
|---|---|---|---|
| PBT | 659 | 1,447 | 2,422 |
| Tax line | ~0 | **−625 (credit)** | **−741 (credit)** |
| PAT | 660 | 2,072 | 3,163 |
| Effective tax rate (Screener) | −0% | −43% | −31% |

- About ₹1,366 cr of PAT across two years is deferred-tax recognition, not operations.
- On normalised PAT (PBT × ~75%), FY26 is about ₹1,800 cr against 3,163 reported. Any P/E built on 3,163 overstates earnings power by ~75%. *(Amounts derived from Screener's PBT and PAT lines. Confirm the DTA note in the FY26 annual report.)*
- **A DTL growing faster than profits** means tax depreciation is running ahead of book depreciation. That is normal for heavy capex but reverses later.

### 4.4 Contingent liabilities
- Under Ind AS 37 a liability is recognised if outflow is *probable* (more than 50%) and can be estimated. Otherwise it is disclosed as a contingent liability unless remote.
- US ASC 450 recognises only when *probable* (interpreted as a higher bar, roughly 70%+), and at the low end of a range when no best estimate exists. US companies therefore disclose more and recognise less.

**Tests.**
1. Contingent liabilities / net worth. Above 25% needs work; above 50% is a flag (Marcellus-style screens use this ratio).
2. Split them into tax demands, which settle for a fraction historically, and **guarantees to group companies**, which are often quasi-debt.
3. Compare year-on-year: "claims not acknowledged as debt" that grow while cash falls.

The Indian telecom AGR dues are the canonical case: a disclosed dispute that became a recognised ₹ tens-of-thousands-of-crore liability after the Supreme Court's October 2019 ruling. Vodafone Idea went from going concern to the government as largest shareholder.

### 4.5 Off-balance-sheet guarantees and structures
- Corporate guarantees given for group companies are disclosed in contingent liabilities and in Companies Act s.186 disclosures. Banks treat them as debt, and so should you.
- The ADAG and IL&FS episodes (see `insight:forensic-redflag-checklist`) show guarantees crystallising.
- Other structures to check:
  - unconsolidated SPVs or "associates" that hold debt
  - inventory sold to an SPV with a buy-back
  - receivables securitised with recourse
  - supplier finance (Lesson 1.3)
  - First Brands (US, 2025): off-balance-sheet receivable and inventory financing (see `insight:ind-as-accounting-levers`)

### 4.6 Leases: Ind AS 116 vs ASC 842 (the biggest comparability break)
- **Ind AS 116 / IFRS 16** use a single lessee model. Almost every lease becomes a right-of-use asset plus a lease liability.
  - The P&L shows **depreciation + interest**, so EBITDA rises because rent disappears from opex.
  - The CFS puts principal and interest in **financing**, so CFO rises.
- **US ASC 842** uses a dual model. **Operating leases** go on the balance sheet, but the P&L shows a single straight-line lease cost inside opex and the cash sits in **CFO**. Finance leases are treated like IFRS.

**Worked example K: IndiGo (INDIGO), the adoption year FY20 (1-Apr-2019).**

| | FY19 (pre) | FY20 (post Ind AS 116) |
|---|---|---|
| Borrowings incl. lease liabilities | 2,429 | **22,719** |
| Depreciation | 760 | **3,974** |
| Interest | 563 | **1,902** |
| Operating profit (EBITDA) | −149 | **4,090** |
| CFO | 3,176 | **6,972** |

- The jump in EBITDA and CFO is mostly accounting.
- By FY26, borrowings (overwhelmingly lease liabilities) were 77,749, depreciation 10,808 and interest 5,944, against PAT of −2,394.
- **Comparable metric:** EBITDAR (EBITDA before rent), or EBITDA minus total lease payments. Lease-adjusted net debt / EBITDAR is the airline-industry standard.
- **Rule:** for any Indian retailer, airline, hospital or QSR, subtract lease payments from both EBITDA and CFO before you compare it with a US peer or with its own pre-FY20 history.

### Exercises, Lesson 4
1. A company has net block ₹600 cr and CWIP ₹400 cr. The ageing shows ₹250 cr older than 3 years. Finance cost in the P&L is ₹30 cr and the Ind AS 23 note shows ₹45 cr capitalised. Compute the three ratios and give a verdict.
2. Restate IndiGo FY20 EBITDA on a "pre-Ind AS 116" basis, assuming the incremental depreciation and interest (FY20 minus FY19) approximate the rent removed. Compare the result with FY19.
3. Net worth ₹2,000 cr. Contingent liabilities: tax demands ₹600 cr and corporate guarantees for promoter-group companies ₹900 cr. How do you treat each?

### Answers, Lesson 4
1. CWIP share = 400/1,000 = **40%**. Aged >3y share = 250/400 = **62.5%**. Capitalised interest / total finance cost = 45/(30 + 45) = **60%**. That is three flags. True finance cost is 2.5x what the P&L shows, and a "project" older than 3 years is a candidate for impairment. Verdict: **disqualifying until explained**. Ask for the project's name, budget, COD date and the auditor's comment.
2. Incremental D&A + interest = (3,974 − 760) + (1,902 − 563) = 3,214 + 1,339 = 4,553. Pre-116 EBITDA ≈ 4,090 − 4,553 = **−463**, against FY19's −149. The business deteriorated, while reported EBITDA swung from −149 to +4,090. (Approximation: lease additions and fleet growth also matter.)
3. Tax demands: haircut by historical settlement rates, then read the nature of the disputes. Perhaps 10–30% is at risk, so treat it as a cash-risk footnote. Guarantees for promoter-group companies: add **₹900 cr to debt**. That is 45% of net worth, a related-party governance flag (flag #8) and a sign that group stress can transmit to this company.

*Sources, Lesson 4:*
- https://www.screener.in/company/RELIANCE/consolidated/
- https://www.screener.in/company/SUZLON/consolidated/
- https://www.screener.in/company/INDIGO/consolidated/
- https://www.screener.in/company/GENSOL/consolidated/ (read 2026-11-20)
- MCA Schedule III amendment G.S.R. 207(E), 24-Mar-2021 https://www.mca.gov.in/Ministry/pdf/ScheduleIIIAmendmentNotification_24032021.pdf
- IFRS 16 https://www.ifrs.org/issued-standards/list-of-standards/ifrs-16-leases/
- ASC 842 https://asc.fasb.org/842
- IAS 12, IAS 37, IAS 38 (ifrs.org)
- Supreme Court AGR judgment, 24-Oct-2019 (Union of India v. Association of Unified Telecom Service Providers)

---
## Lesson 5: Earnings quality

### 5.1 Other-income dependence
**Formula.** Other income / PBT. Also compute **core PBT = PBT − other income**.

**Thresholds.**

| Other income / PBT | Reading |
|---|---|
| < 15% | Fine |
| 15–30% | Explain it |
| > 30% | Flag, unless the company is a cash-rich holding company being valued as such |
| > 100% | The core business loses money |

Remember that Screener puts **exceptional items** inside "Other Income".

**Worked examples, FY26.**

| Company | Other income | PBT | OI/PBT | Core PBT | Note |
|---|---|---|---|---|---|
| Eternal | 1,396 | 615 | **227%** | **−781** | Treasury income on IPO and QIP cash funds the P&L |
| IndiGo | 2,755 | −1,960 | n/m | −4,715 | Interest on cash and forex |
| Hindustan Unilever | 4,923 | 18,219 | **27%** | 13,296 | Includes the Kwality Wall's demerger gain (below) |
| Wipro (FY25, IFRS) | interest ₹2,721 cr | profit ₹13,218 cr | ~21% of PAT | | Large treasury, not a flag at that level but strip it for EV/EBIT |

### 5.2 Exceptional items that recur
- **Rule:** cumulative exceptional charges over 5 years ÷ cumulative PAT. Above 10% means the "one-offs" are operating costs, so deduct their average from normalised earnings.
- One-off gains must also be stripped out.

**Worked example L: HUL FY26.**
- PAT went from 10,671 to **15,059 (+41%)**.
- In Q3 FY26 HUL recognised a one-time, **non-cash** exceptional gain of about ₹4,611 cr (standalone) on demerging its ice-cream business (Kwality Wall's). Under Ind AS 10 Appendix A, a distribution of non-cash assets to owners is measured at fair value. The same quarter carried a ₹576 cr exceptional charge for the new Labour Codes.
- Ex-gain PAT ≈ 15,059 − 4,611 ≈ **10,450**, i.e. **about −2% YoY**, not +41%.
- The effective tax rate fell from 26% to 17% because the gain is largely untaxed.
- *(Approximate: discontinued-operation profit and the consolidated and standalone treatments differ. Reconcile with the FY26 annual report.)*
- **Suzlon FY23** is the same pattern: other income of 2,739 against PBT of 2,892 (95%) in the debt-restructuring year. Without it, PBT is ₹153 cr.

### 5.3 Tax-rate swings
- Compare the effective tax rate with the statutory rate: 25.17% under India's new regime (s.115BAA, from FY20), 21% US federal plus state.
- **Causes:**
  - DTA recognition or reversal (Suzlon, Lesson 4.3)
  - tax-exempt gains (HUL FY26)
  - regime switch (FY20 one-time DTA remeasurement across India Inc.)
  - SEZ or holiday expiry
  - uncertain tax positions
- **Rule:** value on PBT × normalised rate. Treat any year with ETR below 15% or above 35% as non-representative unless it is structural.

### 5.4 Accruals ratio (Sloan 1996)
- Sloan (1996, *The Accounting Review*) showed that the accrual component of earnings is less persistent than the cash component, and that the market over-prices high-accrual firms. A hedge long-low/short-high accrual decile earned about 10% a year in his 1962–1991 sample. The anomaly has weakened since publication.
- **Cash-flow version:** accruals = (PAT − CFO) / average total assets.
  - Thresholds: below −5% is cash-rich, conservative earnings. **Above +10%** is a high-accrual flag. Above 20% is extreme.

| Company / year | PAT | CFO | Avg assets | Accruals |
|---|---|---|---|---|
| SMCI FY2026 ($ m) | 2,230 | −6,810 | 21,982 | **+41.1%** |
| SMCI FY2024 | 1,153 | −2,486 | 6,750 | **+53.9%** |
| PC Jeweller FY19 | 1 | −1,931 | 8,317 | **+23.2%** |
| Gensol FY24 | 53 | −98 | 1,695 | +8.9% |
| Infosys FY2025 ($ m) | 3,162 | 4,351 | 16,971 | **−7.0%** |
| Asian Paints FY26 | 4,395 | 7,088 | 32,437 | **−8.3%** |

### 5.5 Beneish M-score, computed: Super Micro Computer (US-SMCI)
**Data.** SEC XBRL, 10-K FY2026 (0001375365-26-000022) and FY2025 (0001375365-25-000027). $ m, fiscal years ending 30 June.

| Input | FY2023 | FY2024 | FY2025 | FY2026 |
|---|---|---|---|---|
| Revenue | 7,123.5 | 14,989.3 | 21,972.0 | 39,063.1 |
| COGS | 5,840.5 | 12,927.8 | 19,542.1 | 34,835.8 |
| Receivables | 1,148.3 | 2,737.3 | 2,203.9 | 6,125.4 |
| Current assets | 3,179.4 | 8,932.0 | 12,301.7 | 27,726.3 |
| Net PP&E | 290.2 | 414.0 | 504.5 | 625.6 |
| Total assets | 3,674.7 | 9,826.1 | 14,018.4 | 29,945.5 |
| D&A | 26.9 | 30.1 | 41.0 | 53.0 |
| SG&A (S&M + G&A) | 214.6 | 387.1 | 540.4 | 685.5 |
| Total liabilities | 1,702.6 | 4,408.7 | 7,716.6 | 15,465.9 |
| Net income | 640.0 | 1,152.7 | 1,048.9 | 2,230.5 |
| CFO | 663.6 | −2,486.0 | 1,659.5 | −6,809.9 |

**Steps for FY2024 against FY2023** (t = FY24, t−1 = FY23):
1. DSRI = (2,737.3/14,989.3) / (1,148.3/7,123.5) = 0.1826/0.1612 = **1.133**
2. GMI = GM(t−1)/GM(t) = 18.01% / 13.75% = **1.310**
3. AQI = [1 − (8,932.0 + 414.0)/9,826.1] / [1 − (3,179.4 + 290.2)/3,674.7] = 0.0489/0.0558 = **0.876**
4. SGI = 14,989.3/7,123.5 = **2.104**
5. DEPI = [26.9/(26.9 + 290.2)] / [30.1/(30.1 + 414.0)] = 0.0848/0.0678 = **1.252**
6. SGAI = (387.1/14,989.3) / (214.6/7,123.5) = **0.857**
7. LVGI = (4,408.7/9,826.1) / (1,702.6/3,674.7) = **0.968**. This uses total liabilities / total assets, a common simplification; Beneish used (current liabilities + LTD)/TA.
8. TATA = (1,152.7 − (−2,486.0)) / 9,826.1 = **0.370**

M = −4.84 + 0.92(1.133) + 0.528(1.310) + 0.404(0.876) + 0.892(2.104) + 0.115(1.252) − 0.172(0.857) + 4.679(0.370) − 0.327(0.968)
  = −4.84 + 1.042 + 0.692 + 0.354 + 1.877 + 0.144 − 0.147 + 1.733 − 0.317 = **+0.54**. That is far above −1.78, so **flagged**.

**Other years:**

| Period | M-score | Reading |
|---|---|---|
| FY2023 vs FY2022 | −1.94 | Grey |
| FY2025 vs FY2024 | −2.32 | Clean. Receivables fell and CFO was positive |
| FY2026 vs FY2025 | **+0.07** | Flagged again, driven by DSRI 1.56, SGI 1.78 and TATA 0.30 |

**What happened.**
- SMCI had already restated (an 8-K item 4.02 non-reliance on 15-Nov-2018) and paid a $17.5 m SEC penalty in Aug-2020 for improper revenue recognition.
- Hindenburg published a short report on 27-Aug-2024, and the 10-K was delayed.
- EY resigned as auditor (8-K item 4.01, filed 30-Oct-2024) and BDO was appointed (8-K, 18-Nov-2024).
- A board special committee reported finding no evidence of misconduct, and the delayed 10-K was filed in Feb-2025.

**Lessons.**
1. The FY24 M-score was driven by **SGI (hyper-growth)** and **TATA (inventory-funded growth)**. That is a known false-positive mode for fast growers, and Beneish himself warns about it.
2. The *combination* is what mattered: M > −1.78, a prior restatement plus SEC penalty, and then an auditor exit. That is three red-flag families, and `insight:forensic-redflag-checklist`'s rule says do not own it without a variant view.
3. FY26 repeats the cash pattern at larger scale: CFO −$6.8 bn on NI of +$2.2 bn.

### 5.6 Altman Z-score, computed: Intel (US-INTC), FY2024
**Formula (1968, public manufacturers).** Z = 1.2·X1 + 1.4·X2 + 3.3·X3 + 0.6·X4 + 1.0·X5
- X1 = working capital / total assets
- X2 = retained earnings / TA
- X3 = EBIT / TA
- X4 = market value of equity / total liabilities
- X5 = sales / TA

**Zones:**
- above 2.99: safe
- 1.81–2.99: grey
- below 1.81: distress
- For emerging-market or non-manufacturing firms use Z'' = 6.56X1 + 3.26X2 + 6.72X3 + 1.05X4 (book equity/TL). Distress is below 1.1 and safe is above 2.6.

**Data.** 10-K FY2024 (0000050863-25-000009), FY2025 (0000050863-26-000011). $ m.
- Market value is the cover-page public float (dei:EntityPublicFloat) at the end of Q2 of each fiscal year. It is a filing-sourced proxy that slightly understates market cap.
- Total liabilities = total assets − total equity including NCI.

| | FY2023 | FY2024 | FY2025 |
|---|---|---|---|
| Current assets | 43,269 | 47,324 | 63,688 |
| Current liabilities | 28,053 | 35,666 | 31,575 |
| Total assets | 191,572 | 196,485 | 211,429 |
| Retained earnings | 69,156 | 49,032 | 48,983 |
| EBIT (operating income) | 93 | −11,678 | −2,214 |
| Public float (Jun of FY) | 140,000 | 132,400 | 99,300 |
| Total liabilities | 81,607 | 91,453 | 85,069 |
| Revenue | 54,228 | 53,101 | 52,853 |

**Steps for FY2024:**
- X1 = 11,658/196,485 = 0.0593, ×1.2 = 0.071
- X2 = 0.2495, ×1.4 = 0.349
- X3 = −0.0594, ×3.3 = −0.196
- X4 = 1.448, ×0.6 = 0.869
- X5 = 0.2703, ×1.0 = 0.270

Z = **1.36, the distress zone**. FY2023 was 1.91 (grey) and FY2025 was 1.42 (distress).

**What happened.**
- Intel did not default.
- In Aug-2025 the US government converted CHIPS Act grants into about 433 m new shares at $20.47 (a ~9.9% stake). SoftBank bought $2 bn of stock at $23, and Nvidia invested $5 bn.
- Shares outstanding went from 4.33 bn (FY24) to 4.99 bn (Jan-2026) to 5.32 bn (Oct-2026), about +23%.

**Lesson.** Z measures balance-sheet distress, not the outcome. For strategically important firms, "distress" often resolves through **dilution or a bail-in instead of bankruptcy**. Both outcomes are bad for existing equity. Z below 1.81 means "own only with a specific view on the recapitalisation".

### 5.7 Piotroski F-score, computed: Dr. Reddy's Laboratories (DRREDDY, via 20-F IFRS XBRL), FY2025 vs FY2024
**Data.** 20-F FY2025 (0001575872-25-000393), ₹ million. Shares are split-adjusted (1:5 split in 2024).

| Test (1 point each) | Computation | Point |
|---|---|---|
| 1. ROA > 0 | NI 57,245 / opening TA 387,518 = 14.8% | 1 |
| 2. CFO > 0 | 46,428 | 1 |
| 3. ΔROA > 0 | 14.8% vs FY24 55,684/321,854 = 17.3% | 0 |
| 4. CFO/TA > ROA (accrual) | 12.0% < 14.8% | 0 |
| 5. ΔLeverage (LTD/avg TA) falls | 1.79% vs 1.69% | 0 |
| 6. ΔCurrent ratio > 0 | 250,112/130,392 = 1.92 vs 2.58 | 0 |
| 7. No new shares | 832.6 m vs 830.8 m (ESOPs) | 0 |
| 8. ΔGross margin > 0 | 58.50% vs 58.61% | 0 |
| 9. ΔAsset turnover > 0 | 0.840 vs 0.867 | 0 |
| **F-score** | | **2 / 9** |

- **Why a high-quality company scores 2.** In FY25 Dr. Reddy's bought Haleon's Nicotinell NRT portfolio for £458 m upfront (completed 30-Sep-2024). The deal was funded partly with short-term borrowings: proceeds from borrowings were ₹80,646 m against ₹19,366 m the year before.
- Total assets jumped 27%, so asset turnover, the current ratio and ROA all fell mechanically.
- Piotroski designed F for **cheap, high book-to-market** stocks (value traps vs recoveries). On a growth or quality company, in an acquisition year, it misfires.
- **Rules:**
  - (a) Use F only on the cheapest book-to-market quintile, as Piotroski did. His high-F minus low-F spread was about 23% a year in 1976–96.
  - (b) Re-run it excluding acquisitions (pro-forma assets).
  - (c) Treat 8–9 as "improving fundamentals", ≤ 2 as "deteriorating", and check *why* before acting.
- The strict share test (7) fails on tiny ESOP issuance. Some practitioners allow under 1% dilution.

### Exercises, Lesson 5
1. Compute Beneish's DSRI and TATA for SMCI FY2026 vs FY2025 from the table, and say which input moved most.
2. Compute Z'' (emerging-market, book-equity version) for Intel FY2024 using book equity of 105,032. Zone?
3. Eternal FY26: what PBT would you need from food delivery and quick commerce alone to justify ignoring other income? What question do you ask management?
4. A company's ETR went 25%, 25%, 9% and PAT grew 30% in the 9% year, with PBT up 7%. Restate PAT growth at 25% tax.

### Answers, Lesson 5
1. DSRI = (6,125.4/39,063.1) / (2,203.9/21,972.0) = 0.1568/0.1003 = **1.563**. TATA = (2,230.5 + 6,809.9)/29,945.5 = **0.302**. Receivables moved most: up 178% against revenue up 78%.
2. X1 0.0593 × 6.56 = 0.389. X2 0.2495 × 3.26 = 0.813. X3 −0.0594 × 6.72 = −0.399. X4 105,032/91,453 = 1.148 × 1.05 = 1.206. Z'' = **2.01, the grey zone** (1.1–2.6). The book-value version is gentler because Intel's book equity is large relative to its depressed market value. That itself is a signal: the market doubted the book value of fabs.
3. Core PBT must be at least 0 for "the business pays for itself". FY26 core PBT is −781 (615 − 1,396). Ask: "What is segment-level adjusted EBITDA minus the ESOP cost and lease payments, by segment, and when does quick commerce cover its own depreciation?"
4. If PBT is 100 → 107, then reported PAT went 75 → 97.4 (+30%). At 25% tax, PAT is 80.25, so growth is **+7%**. The other 23 points were tax.

*Sources, Lesson 5:*
- SEC XBRL companyfacts: SMCI https://data.sec.gov/api/xbrl/companyfacts/CIK0001375365.json, INTC https://data.sec.gov/api/xbrl/companyfacts/CIK0000050863.json, Dr. Reddy's https://data.sec.gov/api/xbrl/companyfacts/CIK0001135951.json
- SMCI 8-Ks: https://www.sec.gov/Archives/edgar/data/1375365/000137536524000036/smci-20241024.htm and https://www.sec.gov/Archives/edgar/data/1375365/000137536524000040/smci-20241118.htm
- SEC SMCI 2020 order https://www.sec.gov/news/press-release/2020-190
- Hindenburg https://hindenburgresearch.com/smci/
- Intel stake: https://www.npr.org/2025/08/22/nx-s1-5509673/trump-says-us-government-will-take-stake-intel and https://www.nbcnews.com/business/business-news/nvidia-invest-5-billion-intel-develop-chips-one-time-rival-rcna232094
- Dr. Reddy's NRT deal: https://business-standard.com/amp/companies/news/dr-reddy-s-laboratories-completes-acquisition-of-haleon-s-nrt-portfolio-124093000809_1.html
- HUL demerger gain: https://www.outlookbusiness.com/corporate/hul-net-profit-soars-136-in-q3-boosted-by-4611-cr-kwality-walls-demerger-gain and https://www.freepressjournal.in/business/hindustan-unilever-net-profit-soars-121-yoy-to-6603-crore-in-q3-fy26-boosted-by-ice-cream-business-demerger
- Sloan (1996) https://www.jstor.org/stable/248290
- Beneish (1999) https://rpc.cfainstitute.org/research/financial-analysts-journal/1999/the-detection-of-earnings-manipulation
- Altman (1968) https://doi.org/10.1111/j.1540-6261.1968.tb00843.x
- Piotroski (2000) https://doi.org/10.2307/2672906

---
## Lesson 6: Ind AS vs US GAAP, and Indian specifics

### 6.1 Differences that change comparisons

| Area | Ind AS (≈ IFRS) | US GAAP | Adjust by |
|---|---|---|---|
| Leases (lessee) | Single model: depreciation + interest. CFO excludes lease cash | Operating leases: straight-line opex, cash in CFO | Deduct lease payments from Ind AS EBITDA and CFO (Lesson 4.6) |
| Interest paid in CFS | Operating or financing (choice) | Operating | Move interest into CFO |
| Development costs | Capitalised when criteria met (Ind AS 38) | Expensed (ASC 730), except some software | Add back capitalised development to expenses, or compare on cash R&D |
| PP&E revaluation | Allowed (revaluation model) | Prohibited | Check for revaluation reserves inflating book value and depressing ROE |
| Impairment reversal | Allowed (not for goodwill) | Prohibited | Watch "reversal of impairment" in other income |
| Inventory | LIFO prohibited | LIFO allowed | US LIFO firms: add the LIFO reserve to inventory and equity |
| Provisions | Recognise if probable (>50%) | Probable is a higher bar. Low end of range | Indian companies recognise more; US companies disclose more |
| "Exceptional items" | Separate line common (Schedule III) | No extraordinary items (ASU 2015-01). "Unusual or infrequent" in notes | Indian exceptionals deserve the recurrence test (5.2) |
| Bank overdraft | Can be part of cash & equivalents | Financing | Net cash looks higher under Ind AS |
| Componentisation | Required | Permitted, less common | Different depreciation profiles |
| Non-GAAP metrics | Little regulation (SEBI requires no reconciliation for "EBITDA") | Reg G / Item 10(e): reconciliation required | Rebuild Indian "adjusted EBITDA" yourself |
| Goodwill | Impairment only | Impairment only (private companies may amortise) | Same |
| Revenue | Ind AS 115 | ASC 606 | Converged. Ind AS 115 carve-outs are minor (e.g. penalties presentation) |
| Consolidation | Control model (Ind AS 110) | Voting-interest + VIE model | Check for unconsolidated "associates" holding debt |

### 6.2 Indian specifics a US investor never sees

**1. Promoter loans and promoter-related flows.**
- Loans from promoters (often unsecured, interest-free, classified as quasi-equity) prop up weak balance sheets.
- Loans *to* promoter entities are the classic leak (RHFL "general purpose corporate loans", Gensol).
- Companies Act s.185 restricts loans to directors and their interested entities. s.186 caps loans, guarantees and investments at 60% of capital + free reserves or 100% of free reserves, whichever is higher, unless a special resolution is passed.
- **Test:** loans + advances + investments in group entities / net worth. Above 10% needs a reason; above 25% is a flag.

**2. Inter-corporate deposits (ICDs).**
- These are short-term deposits placed with other companies, often group firms or friendly NBFCs, and frequently shown as "cash-like".
- IL&FS and the 2018 NBFC crisis froze many of them.
- **Test:** ICDs placed / cash + investments, and the counterparty names (RPT note).

**3. Related-party approvals.**
- **SEBI LODR Reg 23:** all RPTs need prior audit-committee approval. Material RPTs (above ₹1,000 cr or 10% of consolidated turnover, whichever is lower) need shareholder approval, and related parties cannot vote.
- **Companies Act s.188** applies to non-arm's-length or non-ordinary-course RPTs.
- Read the AGM notice: a resolution approving "material RPTs up to ₹X cr" with a group company is a forward-looking map of where cash may go.
- **Test:** RPT limits sought / revenue, and how they change year over year.

**4. Promoter pledges and encumbrance** (SEBI SAST Reg 31 disclosures; `tools/nse_fetch.py pledge`). Pledge above 25% or rising is flag #11.

**5. CARO 2020 (Companies (Auditor's Report) Order, 2020).** This annexure to the audit report for most unlisted and listed standalone entities is the single best free forensic document in India. Read these clauses:

| Clause | What the auditor must report | Why it matters |
|---|---|---|
| 3(i) | PP&E records, physical verification, title deeds not in company's name, revaluation, **benami** proceedings | Phantom assets |
| 3(ii)(b) | **Quarterly returns/statements filed with banks for working-capital limits vs books**: any material differences | Inflated stock/debtor statements to banks is a fraud precursor |
| 3(iii) | Loans, advances, guarantees to companies, LLPs, firms, **related parties**: terms, overdue amounts, loans repayable on demand | Promoter leakage |
| 3(iv) | Compliance with s.185/186 | Illegal group loans |
| 3(vii) | Undeposited statutory dues (GST, PF, income tax) and disputed dues | Cash stress shows here first |
| 3(viii) | Unrecorded income surrendered in tax assessments | Off-books income |
| 3(ix) | **Defaults on loans**, wilful-defaulter status, short-term funds used for long-term purposes, funds raised to pay subsidiaries' obligations | Covers flag #14 directly |
| 3(x) | Use of IPO/FPO and preferential-allotment money | Diversion |
| 3(xi) | **Fraud** noticed, whistle-blower complaints, s.143(12) reports to Govt | Fraud already occurred |
| 3(xiv) | Internal audit system adequate? | |
| 3(xvi) | NBFC registration / CIC issues | |
| 3(xvii) | **Cash losses** in current and previous year | |
| 3(xviii) | **Resignation of statutory auditors**, and whether outgoing auditor's issues were considered | Flag #9 |
| 3(xix) | **Material uncertainty about meeting liabilities within one year** | India's going-concern lite |
| 3(xxi) | Qualifications/adverse remarks in group companies' CARO reports | Group contagion |

*Tip:* CARO applies to the **standalone** audit report, so read the standalone annual report even when you analyse consolidated numbers. Also read the auditor's **Key Audit Matters**, any **Emphasis of Matter**, the **Internal Financial Controls (IFC) report** (s.143(3)(i)), and **Schedule III "Additional regulatory information"** (CWIP ageing, wilful defaulter, struck-off company dealings, crypto, undisclosed income, and the key ratios with >25% change explanations).

**6. Auditor quality and tenure.** Mandatory rotation applies (s.139: 2 × 5-year terms for audit firms). Watch for mid-term resignation, a small auditor for a large company, and a change from a Big-4/large network to an unknown firm. NFRA orders are public.

### Exercises, Lesson 6
1. An Indian retailer reports EBITDA of ₹1,000 cr. Notes: lease depreciation ₹350 cr, lease interest ₹150 cr, lease principal paid ₹320 cr, capitalised development nil. What is the US-GAAP-comparable EBITDA (treating all leases as operating)?
2. CARO 3(ii)(b) reports that stock statements submitted to banks showed inventory 22% higher than the books in Q2 and Q3. Give two benign and two malign explanations, and one follow-up step.
3. List the five CARO clauses you read first, in order, and say why.

### Answers, Lesson 6
1. The total cash lease cost is principal ₹320 cr + interest ₹150 cr = ₹470 cr, which approximates the straight-line operating-lease expense. Comparable EBITDA ≈ 1,000 − 470 = **₹530 cr**. Lease depreciation and interest are already below EBITDA, so subtract the rent equivalent once.
2. Benign: (a) timing, since bank statements were prepared before quarter-end adjustments; (b) valuation basis, with statements at selling price and books at cost. Malign: (a) inflating drawing power to borrow more; (b) inventory in the books later written down, i.e. phantom stock. Follow-up: read the reconciliation the company must give in its notes, check whether the gap persists in Q4, and compare inventory days against peers.
3. **3(ix)** defaults/fund diversion → **3(xi)** fraud → **3(xviii)** auditor resignation → **3(iii)** related-party loans → **3(xix)** liquidity uncertainty. These five map to the disqualifiers in `insight:forensic-redflag-checklist`: diversion, fraud, auditor exit, related-party leakage, and survival.

*Sources, Lesson 6:*
- MCA CARO 2020 order (G.S.R. 849(E), 25-Feb-2020; amended 24-Mar-2020) https://www.mca.gov.in/Ministry/pdf/CARO_Order_25022020.pdf
- ICAI Guidance Note on CARO 2020 https://www.icai.org/post/guidance-note-on-caro-2020
- Companies Act 2013 ss.139, 143, 185, 186, 188 https://www.mca.gov.in/content/mca/global/en/acts-rules/ebooks/acts.html
- SEBI LODR Reg 23 https://www.sebi.gov.in/legal/regulations/
- Schedule III amendment 24-Mar-2021 (MCA)
- Ind AS (MCA) https://www.mca.gov.in/MinistryV2/indianaccountingstandards.html
- FASB ASC 230, 450, 730, 842
- ASU 2015-01
- SEC Reg G https://www.sec.gov/rules-regulations/2003/01/conditions-use-non-gaap-financial-measures

---

## Lesson 7: The 30-minute "first read" protocol and scoring template

**Goal.** In 30 minutes, decide between three outcomes: (a) **kill**, (b) **needs deep work**, or (c) **passes forensic gate**. This is not a valuation. Run it before any thesis work, which is the "edge before stocks" rule in practice.

### Minute-by-minute (India annual report; US 10-K equivalents in brackets)

| Min | What | Where | Kill if |
|---|---|---|---|
| 0–3 | **Auditor's report**: opinion type, Emphasis of Matter, KAMs [CAMs], auditor name and tenure; IFC report [Item 9A ICFR] | Standalone + consolidated audit reports [Item 8, 9A] | Qualified/adverse/disclaimer; IFC material weakness; auditor changed mid-term |
| 3–7 | **CARO 2020** 3(ix), 3(xi), 3(xviii), 3(iii), 3(xix), 3(ii)(b), 3(vii) [8-K items 4.01/4.02, NT 10-K] | Standalone audit report annexure | Default, fraud, auditor resignation with issues, material uncertainty |
| 7–12 | **Cash test**: 5-yr Σ CFO / Σ PAT; Σ FCF (lease-adjusted); CFO before WC vs WC change | Cash-flow statement (5 yrs from Screener/XBRL) | Σ CFO/PAT < 0.5 with no clear capex/WC reason |
| 12–16 | **Working capital**: DSO incl. unbilled, DIO, DPO trend; supplier-finance/factoring note | Balance sheet + notes | DSO/DIO up >15 days/yr for 2+ yrs without explanation |
| 16–19 | **Other income & exceptionals**: OI/PBT; 5-yr Σ exceptionals / Σ PAT; ETR vs 25.17% [21%+state] | P&L + notes | Core PBT < 0 presented as profitable |
| 19–23 | **Balance sheet**: CWIP ageing; capitalised interest/dev; goodwill+intangibles vs equity; lease liabilities; contingent liabilities / net worth; guarantees | Notes + Schedule III additional info | Guarantees to group > 25% of NW; CWIP >3y > 25% of CWIP |
| 23–27 | **Related parties & promoter**: RPT note (sales, purchases, loans, guarantees, ICDs, royalty); AGM RPT resolutions; pledge %; promoter holding trend [DEF 14A Item 13, Form 4] | RPT note; AGM notice; NSE/BSE filings | Loans to promoter entities; rising pledge >25% |
| 27–30 | **Scores & write-up**: Beneish M (non-financials), Altman Z/Z'', Piotroski F (cheap stocks only), Sloan accruals; fill the template; one-line verdict | Your sheet | ≥3 red flags → no position without variant perception |

**Banks, NBFCs and insurers:** skip Beneish, Altman and Sloan. Use asset-quality (GNPA/NNPA trends, SMA-2, restructured book, write-offs vs provisions), ALM gaps, the CRAR trend, related-party lending, RBI divergence disclosures, and auditor KAMs on ECL.

### Scoring template (copy per company; save as a memdb `analysis` record)

```
Company / ticker:                FY analysed:            Date:           Analyst:
Sources (AR URL, XBRL accession, Screener as-of):

A. GATEKEEPERS (any = KILL)                                         Y/N  Evidence (page/clause)
  A1 Qualified/adverse opinion or disclaimer
  A2 Auditor resigned mid-term / CARO 3(xviii) issues
  A3 CARO 3(xi) fraud / 3(ix) default or diversion
  A4 Loans/guarantees to promoter entities > 25% of NW
  A5 Material uncertainty (CARO 3(xix) / going concern)

B. QUANTITATIVE (score 0 good / 1 watch / 2 red)                     Value  Score
  B1 Σ5y CFO / Σ5y PAT           (>=0.9 =0; 0.7-0.9 =1; <0.7 =2)
  B2 Σ5y lease-adj FCF / Σ5y PAT (>=0.5 =0; 0-0.5 =1; <0 =2)
  B3 Sloan accruals (PAT-CFO)/avg TA   (<0 =0; 0-10% =1; >10% =2)
  B4 DSO incl. unbilled, Δ2y           (<+10d =0; +10-30d =1; >+30d =2)
  B5 DIO Δ2y                           (<+15d =0; +15-45d =1; >+45d =2)
  B6 Other income / PBT                (<15% =0; 15-30% =1; >30% =2)
  B7 Σ5y exceptional charges / Σ5y PAT (<5% =0; 5-10% =1; >10% =2)
  B8 ETR vs statutory, 3y avg          (within ±5pp =0; ±5-10pp =1; beyond =2)
  B9 CWIP >2y / CWIP; capitalised int / finance cost (both <20% =0; one >20% =1; both =2)
  B10 Contingent liab. (ex-tax) / NW   (<10% =0; 10-25% =1; >25% =2)
  B11 RPT sales+purchases / revenue    (<10% =0; 10-20% =1; >20% =2)
  B12 Beneish M (8-var)                (< -2.22 =0; -2.22 to -1.78 =1; > -1.78 =2)
  B13 Altman Z (or Z'')                (>2.99 [2.6] =0; grey =1; <1.81 [1.1] =2)
  B14 Piotroski F (value stocks only)  (>=7 =0; 4-6 =1; <=3 =2)
  B15 Promoter pledge % / Δ            (0 =0; <25% stable =1; >25% or rising =2)
  B16 Supplier finance + factoring / payables  (<10% =0; 10-30% =1; >30% =2)
  TOTAL B (max 32):

C. QUALITATIVE (note each)
  C1 Business-model / revenue-definition change in last 3y? (gross vs net)
  C2 Accounting policy changes (depreciation life, revenue, capitalisation)?
  C3 KAM/CAM topics; changes vs last year
  C4 Management/CFO/independent director exits
  C5 Non-GAAP "adjusted" metrics vs reported gap

VERDICT:  0-6 = passes forensic gate | 7-12 = needs deep work (list questions) | >=13 or any A = KILL
Biggest open question:
Next check date (e.g., next AR / 10-K):
```

**Calibration note.** These thresholds are practitioner conventions, assembled from Beneish, Sloan, Piotroski, Altman and Marcellus-style screens. They have **not yet been back-tested on Indian data by us.** Logging each scored company in memdb and checking the scores against outcomes 2–3 years later is how this becomes edge rather than ritual. That tracking task is in `next_steps`.

### Worked mini-run: Gensol FY24 through the template (from public data only)
- **A:** FY24 audit report not reviewed here. Its later history (SEBI interim order 15-Apr-2025) would trip A3 and A4.
- **B1:** Σ CFO/PAT = −0.49 → 2.
- **B2:** Σ FCF/PAT = −11 → 2.
- **B3:** +8.9% → 1.
- **B4:** DSO went 67 to 86, +19 days → 1.
- **B6:** OI/PBT = 33/78 = 42% → 2.
- **B9:** CWIP rising while fixed assets fell (FY24 to Sep-24) → 1.
- That gives **9 points on the 6 items computable from Screener alone**, before CARO, RPT or pledge data. The verdict is at minimum **needs deep work**, and the cash items alone justify a pass.

### Exercises, Lesson 7
1. Run the B-section on Asian Paints FY22–FY26 for B1, B3 (FY26) and B6 (FY26) using Lesson 1 and Lesson 5 data.
2. Which A-gatekeepers would have been visible for SMCI on 30-Oct-2024?

### Answers, Lesson 7
1. B1 = 22,795/20,943 = 1.09 → 0. B3 = −8.3% → 0. B6 = 728/6,003 = 12% → 0. That is 0 on all three, consistent with a clean compounder. Its open question is valuation and growth, not accounting.
2. A2: the auditor (EY) resigned, by 8-K item 4.01 filed 30-Oct-2024. The 10-K was also late, which in India would be the equivalent of delayed results. Plus the history: the 2018 non-reliance (item 4.02) and the 2020 SEC penalty. The gatekeeper rule says KILL until a new auditor signs a clean opinion. A new auditor did sign in Feb-2025, after which the stock became an "argue the variant view" case, not a forensic pass.

---

## Appendix: formula card

| Technique | Formula | Red-flag threshold |
|---|---|---|
| Cash conversion | Σ5y CFO / Σ5y PAT | < 0.7 |
| FCF conversion | Σ5y (CFO − capex − capitalised intangibles − lease payments) / Σ5y PAT | < 0.5 |
| Sloan accruals | (PAT − CFO) / avg TA | > +10% |
| DSO incl. unbilled | (AR + contract assets) / revenue × 365 | +15d/yr for 2y |
| DIO | Inventory / COGS × 365 | +15d/yr for 2y; vs peers |
| DPO collapse | ΔDPO | −30d in a year = creditor flight |
| Supplier-finance share | SF obligations / trade payables | > 30% |
| Other-income dependence | OI / PBT | > 30% |
| Recurring exceptionals | Σ5y exceptional charges / Σ5y PAT | > 10% |
| ETR anomaly | ETR − statutory | beyond ±10pp |
| CWIP ageing | CWIP > 2y / CWIP | > 25% |
| Capitalised interest | Capitalised borrowing cost / total finance cost | > 20% |
| Contingent liabilities | (CL ex-tax + guarantees) / NW | > 25% |
| Group exposure | Loans + advances + investments + guarantees to group / NW | > 25% |
| RPT intensity | RPT sales + purchases / revenue | > 20% |
| Beneish M (8-var) | −4.84 + .92DSRI + .528GMI + .404AQI + .892SGI + .115DEPI − .172SGAI + 4.679TATA − .327LVGI | > −1.78 |
| Altman Z | 1.2X1 + 1.4X2 + 3.3X3 + 0.6X4 + 1.0X5 | < 1.81 |
| Altman Z'' | 6.56X1 + 3.26X2 + 6.72X3 + 1.05X4(book) | < 1.1 |
| Piotroski F | 9 binary tests | ≤ 3 (value stocks) |
| Lease-adjusted EBITDA (Ind AS) | EBITDA − lease payments | Compare to US peers |
