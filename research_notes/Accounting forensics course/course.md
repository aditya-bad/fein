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
