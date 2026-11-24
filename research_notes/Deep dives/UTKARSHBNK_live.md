# Utkarsh Small Finance Bank (NSE: UTKARSHBNK) — LIVE deep dive #5 (method test, protocol v1.4 bank mode, stages 2→7; first live lender)

**Date:** 2026-11-24 · **Analyst:** Claude · **Status:** live (not practice). Its paper calls are scored.
**Purpose:** test the deep-dive method on a lender, the first live use of the protocol's bank/NBFC adaptation (until now used only in the
Federal Bank dry run). The frame was IT/software services + banks/NBFCs; the company was **drawn at random**. This is test material (L9, L21):
**no buy/sell verdict**. Outputs: a decision card (**v1.4**, the `CARD_VERSION` in `tools/decision/decision_card.py` at run time) and dated
probabilistic calls, each scored later against a naive base rate.
**Roadmap:** stage 2 (filters) → 3 (signals) → 4 (deep dive) → 5 (valuation, bank mode) → 6 (decision) → 7 (scoreboard). It unlocks the first
live test of the method on a **levered balance sheet coming out of a credit cycle**, and exposes three tool gaps (no lender base-rate class,
no banking-XBRL resolver, linear ROE paths in `bank.py`).
Research, not SEBI-registered advice.

Source tags: `[AR26]` annual report FY2025-26 (NSE, filed 10-Jul-2026; Schedule 18 notes, DF-11); `[XBRL]` NSE integrated-filing banking XBRL,
seven quarters Q4 FY25–Q2 FY27 (latest filed 03-Nov-2026); `[DECK]` investor presentation Q2 FY27 (03-Nov-2026) and Q1 FY27 (01-Aug-2026);
`[PR]` press release 03-Nov-2026; `[CALL]` earnings-call transcripts (May-2025, Nov-2025, May-2026, Aug-2026, 04-Nov-2026); `[P3]` Basel III Pillar 3
as on 30-Sep-2026 (utkarsh.bank.in); `[NSE]` announcements (417), SHP XBRL, bhavcopy; `[SCR]` screener.in fetched 24-Nov-2026; `[YH]` Yahoo v8
daily closes; `[RATING]` ICRA/CARE letters filed on NSE; `[EXT]` external (Bihar gazette via PRS, press). `[EST]` = my estimate (method shown).
Money in ₹ crore unless stated. Numbers with one source are marked *(1 src)*.

---

## 0. Selection (S0; rules fixed before drawing)

**Rules** were written to `research_notes/Deep dives/UTKARSHBNK_selection/prereg_selection.md` at **2026-11-24 16:33 IST, before the frame was
built** (sha256 of the rule text recorded in the file). Seen before writing: universe.csv header; the live-dd4 prereg/selection lists (healthcare
+ IT names, no financials, no mcaps); `industry_map.csv` checked and **absent**, so lenders were hand-classified.
- Close: the 24-Nov bhavcopy returned HTTP 404 at 16:33 IST → 23-Nov-2026 close (rule 1). Mcap = universe shares × close.
- Frame: 1,547 symbols, all priced; **809** in ₹1,000–20,000 cr; 482 with no index industry.
- Sector lists (written into the prereg **before the shuffle**): IT 36 (index 18 + hand 18, same judgments as dd4); lenders 34 (17 from index
  "Financial Services" + 17 hand-classified from unindexed names). Excluded as non-lenders or unsure: holdcos (BAJAJHLDNG, EDELWEISS, JMFINANCIL,
  IFCI, BFINVEST…), brokers, RTAs, AMC, exchange, ratings, primary dealer. **Eligible = 70.**
- Draw: `random.Random(20261202).shuffle` of the sorted list. First 15: KPITTECH, **UTKARSHBNK**, CYIENT, SATIN, TANLA, MPSLTD, UJJIVANSFB, PSB,
  INTELLECT, RAMCOSYS, REPCOHOME, ESAFSFB, SAMMAANCAP, ONEPOINT, PAISALO.

| # | Symbol | Mcap ₹ cr | Result | Reason |
|---|---|---|---|---|
| 1 | KPITTECH | 14,317 | **skip (d)** | Passed a–c (only subsidiaries merged into it; the Nov-2023 "change in auditors" is KPIT UK's; pledge flags false). **PEAD Q2 FY27 SUE −0.81 → quintile 1, event 28-Oct-2026, inside the 63-trading-day window.** |
| 2 | **UTKARSHBNK** | 2,084 | **SUBJECT** | a: the pending scheme merges the promoter holdco Utkarsh CoreInvest (UCL) **into** the bank — the listed bank survives. b: SEBI settlement Apr-2024 (₹1.24 cr, LODR) is not a fraud finding; FY26 audit unmodified; no RBI restriction. c: pledge flags false. d: SUE +1.53 → Q5. e: lender form — CRAR 17.0% ≥ 15%, ratings A- (investment grade). |

Note on the industry map: `industry_map.csv` was absent at 16:30 IST; another agent's WIP commit def3230 (16:37 IST) added a partial map (676 rows, in progress; it contains neither KPITTECH nor UTKARSHBNK). The pre-registered rule (hand classification) stands; the same commit also snapshots this selection folder, which timestamps the prereg.
Notes: the defensive layer again removed the first name (as in dd3/dd4). The subject entered via the **hand-classified** lender list (no index
industry), as INDRAMEDCO did — the missing industry map keeps mattering. PEAD quintiles for the first 15 were printed together before the walk;
the walk order was not changed.

## 0b. Rule zero: edge before depth
1. **What the market knows.** A microfinance-born SFB hit by the 2024–26 MFI over-leveraging cycle: FY26 loss ₹1,151 cr, rights issue ₹950 cr at
   ₹14 (Nov-2025), price ₹64.5 (2024 high) → ₹11.71. Management says the worst is over: PPOP back to +₹85 cr/quarter, GNPA 12.4% → 5.9%, FY27 loan
   growth 25–30%, FY28 ROE ~15%. **The 5 most-asked questions on the 04-Nov-2026 call:** why provisions rose QoQ; slippage breakup; equity-raise
   plans; why branch throughput/growth is low; NIM path if repo rises (others: write-off recoveries, CGFMU coverage, headcount).
2. **The variable that moves value most:** the **credit cost path** (each 1 pp on a ₹20,000 cr book = ₹200 cr ≈ 70% of annualised H1 PPOP) and,
   through it, **the price of the next equity raise**. Nobody asked about **Tier-1 falling 235 bp in one quarter**, the **personnel-cost drop**, the
   **DTA**, or the **Bihar microfinance law**.
3. **Layers most likely to reveal it:** L2 (NPA walk with write-offs, capital deductions), L4 (credit cost and CGFMU in physical terms), L5
   (ownership supply after the reverse merger). Honest limit: we have **no edge on the microfinance cycle itself**.

---

## 1. S2 checklist, bank form (filled before L1; every rule dated)
| Rule | Status | Evidence |
|---|---|---|
| H1a fake cash / investments | **pass** | Cash + RBI ₹1,368 cr, bank balances ₹485 cr, investments ₹6,263 cr `[XBRL = DECK]`; LCR 177%, surplus liquidity ~₹2,540 cr `[CALL]`; security receipts ₹102.9 cr fully provided `[AR26 18.4.8]`. No HTM/AFS loss issue (G-sec book small vs equity). |
| H1b NIM/yield/RoA/C-I in peer band | **pass** | Q2 FY27 yield 15.9%, CoF 7.5%, NIM 6.3%, C/I 84% `[DECK]`; NII re-derived 909.26 − 473.95 = 435.3 `[XBRL]` = deck 435. |
| H1c unverifiable | **pass** | 5.21 m customers; DICGC premium ₹23.28 cr incl. GST ÷ 1.18 ÷ 0.12% ≈ ₹16,400 cr assessable deposits vs ₹21,654 cr total (76%) `[AR26 18.14.7]` — consistent (institutional/interbank excluded). |
| H2 auditor exit / opinion | **pass** | FY26 joint auditors (MM Nissim & Co, KKC & Associates) unmodified opinion `[NSE 09-May-2026]`; they replaced Deloitte + Kirtane & Pandit (FY25); no resignation filing → RBI rotation *(reason 1 src)*. |
| H3 rating non-cooperation | **pass** | ICRA A- (Stable) 02-Jul-2026; CARE A- (Stable) 14-Jul-2026, reaffirmed 03-Sep-2026 `[RATING]`. Downgraded twice: A+ → A (Aug-2025) → A- (Jul-2026); CD A1+ → A1. |
| H4 pump | **pass** | IPO Jul-2023; 276,844 holders `[SCR]`; ADV 6 m ₹12.0 cr mean / ₹6.3 cr median `[YH]`. |
| H5 connected lending (AS-18) | **pass** | Related parties: UCL (deposits ₹60.5 cr, rent ₹0.08 cr), Utkarsh Welfare Foundation (CSR ₹8.16 cr), KMP (MD ₹2.64 cr) `[AR26 18.19]`; no loans to related parties. |
| Exit triggers | **none** | RBI divergence: none reportable for FY24 inspection / FY25 SRA `[AR26 18.4.5]`; no restatement; results on time. RBI penalties: none FY25–26 `[AR26 18.12]` (₹10,000 ATM cash-out fine, Jun-2025). |
| G pledge | **clear** | SHP XBRL 30-Sep-2026: three encumbrance flags false; promoter UCL 42.67%. |
| G accounting trouble (5 y) | **clear** | SEBI settlement 10-Apr-2024 (₹1.24 cr; LODR, SCN 16-Mar-2023); SEBI ₹1 lakh debt-listing fine (2023). Compliance, not misstatement. |
| G dilution | **fired** | Rights 8:13 at ₹14 (record date 14-Oct-2025; 67.79 cr shares, +62%) to repair capital after losses; UCL did not subscribe (69% → 42.7%); specific investors took the shares `[NSE 24-Oct-2025]`. |
| G solvency set (bank) | **clear but thin** | CRAR 17.05% vs 15% SFB floor (**cushion ₹306 cr** on RWA ₹14,915 cr); Tier-1 12.78% vs 7.5%; leverage ratio 6.71% `[P3]`; LCR 177%; CD 80.9% (76% ex refinance). |
| Lender signals | **fired** | Discount to book + two-notch downgrade + write-off-driven GNPA fall + state concentration: the memdb rule in `insight:lender-blowup-signals` ("two+ flags + discount to book = avoid") fires. Recorded, not a card gate. |

**Stage-3 signals.** PEAD: Q2 FY27 SUE **+1.53 → quintile 5** (event 03-Nov-2026); Q1 +1.47 → Q5 — not in the avoid zone. Lender caveat: reported EPS
here mixes provision timing (Q1 FY27 had a ₹75 cr CGFMU provision credit and a ₹65 cr ARC gain `[CALL]`); not recomputed because the gate is not
triggered. Survival cap (v1.3/1.4): pledge 0; interest cover not applied to lenders; no core-asset threat (section 6.4).

**Credibility (bank, no peer median → no score; L18).** Guidance-bias table from six calls:
| Said (date) | Target | Outcome | Verdict |
|---|---|---|---|
| May-2025 | "Material improvement in profitability" after H1 FY26 stress | H2 FY26 loss ₹563 cr (Q3 −375, Q4 −188) | missed (date) |
| May-2025 | SMA book to normalise by Q1 FY26 | SMA (MB) 4.9% at Sep-25 → 1.3% at Mar-26 | late (2–3 qtrs) |
| Nov-2025 | Asset quality to improve "meaningfully from Q3 onwards" | Credit cost Q3 FY26 9.6% (vs 9.7%), Q4 5.3% | late (1 qtr) |
| Nov-2025 | Loan growth ~25% a year for 2–3 years | FY26 GLP −1.7% (19,666 → 19,332) | missed |
| May/Aug/Nov-2026 | FY27 GLP growth 25–30%; double-digit ROE exit FY27; FY28 ROE ~15%, NIM ~8%; C/I 70–75% FY27 | H1 FY27 GLP +3.8%; ROE −8% annualised; NIM 6.3%; C/I 84% | open (calls 1, 3) |
| Nov-2026 | Cost of funds down, NIM up | CoF 8.0% → 7.5%, NIM 5.1% → 6.3% over 4 quarters | met (direction) |
Pattern: **direction met, dates and growth quantities missed** — the L26 pattern, stronger here.

---

## 2. Map (L1): units and peers
**Business.** SFB since 23-Jan-2017 (UCL's microfinance business transferred in); 1,110 outlets (779 micro-banking, 331 general banking), 27
states, 18,300 staff, 5.21 m customers `[DECK]`. Gross loan portfolio ₹20,062 cr: JLG ₹5,146 cr (26% incl. BC), MBBL ₹2,586 cr, MSME (LAP) ₹4,489 cr,
housing ₹984 cr, CV/CE ₹988 cr, wholesale (FI + business banking) ₹3,085 cr, gold ~₹400 cr; secured 52% `[DECK, CALL]`. Deposits ₹23,869 cr: CASA
21.4%, retail TD ₹14,442 cr, institutional TD ₹4,309 cr (18.1%) `[PR]`.
**Units (bank form):** (1) the **outlet** (MB vs GB), (2) the **loan segment** (JLG, MBBL, LAP, CV, wholesale), (3) the **liability pool** (CASA,
retail TD, institutional TD, refinance), (4) **balance-sheet cost lines** (CRR, DICGC, CGFMU premium).
**Geography (the concentration).** JLG: Bihar 44%, UP 27%, Jharkhand 9%; MBBL: Bihar 48%, UP 28% `[DECK]` *(1 src)*. Micro-banking in Bihar ≈
0.44 × 4,747 + 0.48 × 2,586 ≈ **₹3,330 cr = 17% of GLP** `[EST]`.
**Holdco/non-operating flag:** none (no subsidiaries). **Cyclicality flag: yes** — microfinance credit cycles (FY17 demonetisation, FY21 COVID,
FY25–26 over-leveraging) — so the normalised-earnings test applies (3.1).
**Peers (P/B, screener 24-Nov-2026, 1 src):** Ujjivan SFB 1.59x, Equitas 1.01x, ESAF 1.08x, Suryoday 0.69x, Jana 0.91x, Capital SFB 0.85x, AU 3.44x;
**median 1.01x**. ESAF and Suryoday went through the same MFI cycle and are back to quarterly profit.

### 2.1 Ownership and the reverse merger
| Date | Event | Source |
|---|---|---|
| 20-Sep-2024 | Board approves amalgamation of UCL (promoter CIC, 69.0% then) into the bank; **699 bank shares per 100 UCL shares**; rationale: SFB promoter-dilution rules; after it, "none of the shareholders of the Transferor Company will qualify as a promoter" (public 100%) | `[NSE]` |
| 03-Jan-2025 | RBI no-objection | `[NSE]` |
| Jul-2025 | BSE/NSE no adverse observations | `[NSE]` |
| Nov-2025 | Rights issue; UCL does not subscribe → 42.67% | `[NSE, SCR]` |
| 28-Mar-2026 | NCLT-convened shareholder/creditor meetings approve | `[NSE]` |
| 05-Apr-2026 | Second-motion petition filed; hearings 23-Jul, 22-Oct, 19-Nov-2026 | `[NSE, CALL]` |
UCL's top holders (31-Mar-2026, % of UCL): British International Investment 13.81, RBL Bank 8.63, NMI Frontier 7.75, Faering II 7.71, Hero Enterprise
4.88, responsAbility 4.88 `[AR26 p.11]`. If the swap is roughly share-neutral `[EST]`, these become direct holders of ~5.9%, 3.7%, 3.3%, 3.3%, 2.1%,
2.1% of the bank — DFIs and PE funds that invested 2010–2018. **Supply overhang** (watch item): lock-in terms not found.

---

## 3. Financials, re-derived (L2) `[SCR; XBRL for FY25–H1 FY27]`
| FY | Total interest earned | Interest exp. | NII | Other inc. | Opex | PPOP | Provisions | PAT | Net worth | GNPA % |
|---|---|---|---|---|---|---|---|---|---|---|
| FY19 | 881 | 382 | 499 | 58 | — | — | — | 94 | 773 | — |
| FY20 | 1,308 | 579 | 729 | 99 | — | — | — | 187 | 1,019 | — |
| FY21 | 1,581 | 742 | 839 | 125 | — | — | — | 112 | 1,368 | — |
| FY22 | 1,849 | 788 | 1,061 | 185 | — | — | — | 61 | 1,573 | — |
| FY23 | 2,505 | 976 | 1,529 | 299 | — | — | — | 404 | 2,000 | — |
| FY24 | 3,178 | 1,293 | 1,885 | 400 | — | — | — | 498 | 2,973 | 2.5 |
| FY25 | 3,764.9 | 1,742.1 | 2,022.9 | 599.8 | 1,615.8 | 1,006.9 | 979.3 | 23.7 | 2,974.5 | 9.4 |
| FY26 | 3,378.8 | 1,902.0 | 1,476.7 | 431.0 | 1,851.4 | 56.4 | 1,563.0 | **−1,151.0** | 2,775.6 | 7.7 |
| H1 FY27 | 1,792.8 | 935.4 | 857.4 | 211.8 | 920.4 | 148.8 | 274.9 | −103.8 | 2,676.3 | 6.0 |
FY19–24 NII = screener revenue − interest; PPOP/provisions not split on screener for those years. FY25–H1 FY27 from XBRL; PAT and GNPA match screener ✓.
FY26 tax was a **credit of ₹355.6 cr**: the bank recognised a DTA on losses "backed by independent expert's opinion" `[AR26 18.21b]`; pre-tax loss
₹1,506.6 cr.

**Re-derivations.**
- **The NPA walk (FY26)** `[AR26 18.4.1]`: opening 1,854 + additions **1,724** − upgrades 252 − recoveries 123 − **technical write-offs 1,013** − **ARC
  sale 654** − other write-offs 76 = closing 1,460. **Write-offs + ARC (1,743) exceeded fresh slippage (1,724).** ARC sale: ₹1,515 cr principal
  (428,864 accounts) for **₹207 cr consideration (13.6%)** `[AR26 18.4.6]`. Quarterly `[DECK]`: Q1 FY27 additions 195, w/o 57, ARC 365; Q2 additions
  239 (MB 66, MSME 64, wholesale 33, CV/CE 30 `[CALL]`), upgrades+recoveries 65, w/o 98, ARC 51. **The stress is migrating to the secured books**
  (72% of Q2 additions were non-MB). GNPA 12.4% → 5.9% is mostly removal, not cure (`insight:mfi-gnpa-writeoff-arc-walk`).
- **Capital deductions** `[P3 DF-11]`: CET1 before adjustments ₹2,674 cr − intangibles **₹245.7 cr** (₹53.2 cr at Mar-26 `[AR26 DF-11]`) − DTA
  **₹495.5 cr** (₹473.2 cr at Mar-26) = **CET1 ₹1,906.7 cr** (deck Tier-1 ₹1,907 ✓). Tier-1 15.13% (Jun) → 12.78% (Sep) while net worth fell only
  ₹69 cr: the new core banking system went live in Q2 (CWIP ₹125 cr at Mar-26 → 0) and became a deducted intangible. **CET1 book = ₹10.71/share**
  vs reported BVPS ₹15.04 (`insight:lender-book-quality-cet1-deductions`).
- **Q2 PPOP quality.** Personnel cost ₹241 cr (Q1) → **₹202 cr** (Q2), −16% QoQ, while headcount rose 18,136 → 18,300 `[XBRL; DECK]`. At Q1's
  per-head cost Q2 PPOP would be ~₹45–50 cr, not ₹85 cr `[EST]`. Not explained in the deck or call; not asked.
- **Other income FY26** ₹431 cr: commission 119, investment gains 41, miscellaneous 273 incl. **PSLC income ₹87 cr** `[AR26 Sch 14; MD&A]` — PSLC
  surplus comes from microfinance loans; as JLG shrinks (88% → 26% of book since 2020) so does this income.
- **Ratios on average balances (FY26):** NII / avg assets 5.2%; opex / avg assets 6.5% (company 6.67% on monthly averages); credit cost ~8.5% of
  avg advances `[EST]`.
- Screener shows Sep-2026 reserves ₹846 cr vs XBRL ₹896.81 cr (₹50 cr gap, unexplained); XBRL/deck used.

### 3.1 Cyclical lender: normalised earnings and the last down-cycle (v1.4 rule)
- **Normalised PAT** FY19–26 (8 years as an SFB) = ₹229 cr total → ₹28.6 cr/yr → ₹0.16/share on today's count → **73x** price; mean ROE 6.8%
  (16, 21, 9, 4, 23, 20, 1, −40%). Justified P/B at a 6.8% through-cycle ROE (CoE 12.5%, g 5%) ≈ **0.23x**.
- **Peak vs now:** FY23–24 ROE 20–23% at the microfinance peak (JLG 61–65% of book); now 26%.
- **Last down-cycle:** PAT ₹498 cr (FY24) → −₹1,151 cr (FY26); GNPA 2.5% → 12.4%; price ₹64.5 (high) → ₹10.22 (30-Mar-2026 low) = **−84%** `[YH]`.
- Reading: the price (0.78x book) is far above the through-cycle value and below a "back to FY24" value. The bet is that the book mix change (52%
  secured) lifts the through-cycle ROE. That is what the scenarios test.

## 4. Unit economics (L3) — outlet, segment, employee (Q2 FY27 annualised) `[DECK, XBRL; EST]`
| Per outlet (1,110) | Value | Note |
|---|---|---|
| Deposits | ₹21.5 cr | CASA ₹4.6 cr |
| Gross loans | ₹18.1 cr | MB outlet: micro-banking book ₹9.4 cr (7,333 ÷ 779) |
| Staff | 16.5 | |
| Operating income (NII + other) | ₹1.90 cr/yr | 528 × 4 ÷ 1,110 |
| Opex | ₹1.60 cr/yr | 443 × 4; rent ₹8.3 lakh/outlet/yr (FY26 rent ₹91.8 cr) |
| PPOP | ₹0.31 cr/yr | |
| Provisions | ₹0.60 cr/yr | 166 × 4 |
| **PBT** | **−₹0.29 cr/yr** | the average outlet still loses money after credit cost |
| Break-even credit cost | ~1.7% of loans | PPOP 341 annualised ÷ GLP 20,062 |
Per employee: loaded cost ₹5.3 lakh/yr at Q1's run-rate (₹4.4 lakh at Q2's) — low-wage field staff; 1,400+ collection staff for JLG/MBBL `[CALL]`.
No new outlets for 18+ months `[CALL]`: growth must come from throughput (GLP per outlet ₹18 cr vs peers' higher — question asked on the call).
Segment yields (disbursement, Q2 FY27 `[CALL]`): micro-LAP ~18%, MSME 13%, housing 11%, CV/CE 12.2%, wholesale 10.9–11%, PL 16%, gold 12%. Against CoF
7.5% and opex ~6.4% of assets, **secured books at 11–13% earn little after opex** — the "secured mix" story lowers risk and also lowers
through-cycle ROE unless opex falls.

## 5. Cost drivers in physical terms (L4), ranked by weight (FY26; % of avg assets ₹28,498 cr)
| Line | ₹ cr | % avg assets | Physical driver | Sensitivity |
|---|---|---|---|---|
| Interest on deposits | 1,707 | 6.0% | ₹23,869 cr deposits, 80% term; retail TD 8.1%, CASA 4.5% `[DECK]` | +25 bp on cost of deposits = ₹60 cr/yr = −21 bp RoA; TD repricing lag ~1 yr; ~50% of loans floating `[CALL]` |
| **Provisions (credit cost)** | 1,563 | 5.5% | Slippage × (1 − recovery); ARC recovery 13.6%; write-off pool ₹1,093 cr recovering ~₹20 cr in H1 `[AR26; CALL]` | **±1 pp credit cost on ₹20,000 cr = ₹200 cr** ≈ 70% of annualised H1 PPOP |
| Staff | 948 | 3.3% | 18,300 people × ₹5.3 lakh | +10% wages = ₹95 cr = −33 bp RoA; state minimum-wage notifications (Bihar/UP) hit field staff |
| Other expenditure | 530 | 1.9% | Core banking service charges, professional fees, travel `[AR26 Sch 16]` | New CBS: capitalised (CET1 deduction) + amortisation |
| Rent, taxes, lighting | 92 | 0.3% | 1,110 outlets × ₹8.3 lakh/yr | — |
| Depreciation | 77 | 0.3% | rises as the ₹246 cr intangible amortises | +₹40–60 cr/yr `[EST]` |
| **Insurance** | 66 | 0.2% | **DICGC ₹23.3 cr** (12 paise/₹100 of assessable deposits) + **CGFMU guarantee fee** (1% of covered MFI disbursements) ~₹40 cr `[EST]`; +223% YoY | Fee is a cost now; benefit = ~73% provision credit on covered loans + claims |
| Law charges | 38 | 0.1% | +28% YoY: recovery litigation, SARFAESI | rises with the secured-book NPAs |
| CRR (in NIM) | — | — | NDTL ~₹24,000 cr × CRR 3% `[EST; rate unverified]` × ~7% opportunity rate | ~₹50 cr/yr ≈ 17 bp |
**The micro-driver:** microfinance credit cost, and through 2026–27 two government inputs (L40): **CGFMU** (NCGTC guarantee: covered book ~₹6,500
cr; NPAs in it ₹209 cr; claims ₹80 cr submitted; window closed for new guarantees in Q2 FY27 pending the next phase `[CALL]`; the Union Cabinet
approved CGFMU's extension to 31-Mar-2031 in Nov-2026 `[EXT, press, 1 src]`) and the **Bihar Micro Finance Institutions Act 2026** (6.4).

## 6. Governance, ownership, incentives (L5)
### 6.1 Related parties (AS-18) `[AR26 18.19]`
| Party | Transaction FY26 | ₹ cr | Note |
|---|---|---|---|
| UCL (holding co) | Deposits outstanding / interest paid | 60.54 / 4.75 | sub-lease to UCL; ESOP cross-charge (0.37) |
| Utkarsh Welfare Foundation (KMP influence) | CSR contribution | 8.16 | 0.4% of FY26 opex |
| RAAG Family Private Trust (KMP influence) | none material | — | — |
| MD & CEO Govind Singh | Remuneration / ESOP granted | 2.64 / 1.31 | ex-MD of UCL |
No connected lending; no parent fees or royalties (no parent-take table needed: UCL is a pure holding company).
### 6.2 Vote results
Shareholder/creditor meetings on the scheme (28-Mar-2026) passed with the required majorities `[NSE]`; AGM 04-Aug-2026 scrutinizer report filed
(not extracted — scanned PDF; open item). L40 check "promoter votes held vs polled": UCL is the only promoter and an interested party on the scheme;
nothing abnormal found in what was read.
### 6.3 People and incentives
MD & CEO Govind Singh (since SFB start; ex-UCL MD); ED Sarju Simaria (ex-CFO, WTD from 22-Jun-2026); new CFO Manmohan Shetty (19-Sep-2026); WTD
Pramod Dubey left 31-Dec-2025; head of micro-banking resigned Sep-2024 `[NSE, AR26]`. **Three senior finance/business changes in 15 months during
the stress** (watch). Management targets (ROE 15% FY28) are not tied to disclosed pay metrics.
### 6.4 Government and external inputs (L40)
| Input | Counterparty | Term / status | Obligation | In AR FY26? |
|---|---|---|---|---|
| SFB licence | RBI | perpetual; promoter dilution plan acknowledged 09-Feb-2024; reverse merger NOC 03-Jan-2025 | SFB norms (75% PSL, 50% loans ≤ ₹25 lakh, promoter dilution) | yes |
| CGFMU guarantee | NCGTC (GoI) | scheme extended to Mar-2031 (Cabinet, Nov-2026, press); bank's window closed in Q2 FY27 | 1% fee; MFIN guardrails | partly (fee in insurance line) |
| **Bihar MFI Act 2026** | Govt of Bihar | Act 11 of 2026, gazette 11-May-2026 `[EXT: PRS]` | Banks exempt from registration (s.2(2)(a)) but **coercive-recovery and borrower-protection provisions apply** (s.2(3)) | **no — and not on the May/Aug/Nov-2026 calls** |
The Bihar Act is a **material external fact absent from the AR** (L40 flag): Bihar is ~17% of GLP and its passage moved the stock (−5 to −11% for
listed MFI lenders on 26/27-Feb-2026, press). It is **not** a licence/lease threat to the core asset (scheduled banks are exempt from its lending
rules), so the card's v1.4 `core_asset_threat` was not set (override log).

## 7. Ground truth (L6): scuttlebutt plan (not executed; the user's ground checks)
1. **Bihar field check** (two MB outlets, e.g., Patna rural + Muzaffarpur): centre-meeting attendance, X-bucket collections vs the 99.5% claim,
   whether borrowers have ≥3 lenders (MFIN guardrail), agents' recovery behaviour under the new Act.
2. **CGFMU claims:** NCGTC claim-settlement data / RTI on payout time for SFB claims (₹80 cr submitted).
3. **Write-off recoveries:** ARC (ARCIL, Paras, Shriram) SR NAVs and redemptions for the 2025–26 pools.
4. **Liability side:** retail TD rate board vs Ujjivan/Equitas/AU (fixed basket of 1-, 2-, 3-year rates, quarterly).
5. **Staff:** AmbitionBox/Naukri reviews on field-staff pay, incentives and the Q2 cost drop (bonus reversal? attrition?).
Ethics: no unpublished price-sensitive information; identify ourselves if asked.

---

## 8. Flag override (L7) and valuation (L8)
### 8.1 Bad-but-benign vs good-but-misleading (mandatory for lenders)
| Good-but-misleading | Why | Bad-but-benign | Why |
|---|---|---|---|
| GNPA 12.4% → 5.9% | write-offs + ARC > slippage | Net NPA 2.7% is 20% of CET1 | PCR 55.5%; MFI PCR 67.7% incl. CGFMU |
| Q2 PPOP +34% QoQ | staff cost −16% unexplained | Provisions up QoQ (109 → 166) | Q1 had ₹140 cr one-offs (CGFMU credit + ARC) `[CALL]` |
| Book value ₹15.04 | 28% of it is DTA + intangibles | Tier-1 down 235 bp | mostly a software capitalisation, not a loss |
| P/B 0.78x "cheap" | 1.09x CET1 book; 73x normalised earnings | Rights issue below 2024 prices | done at ₹14 > today's price; capital repaired |
| Secured share 47% → 52% | secured books now 72% of slippage; yields 11–13% | JLG book −32% YoY | deliberate run-off; MBBL grows |
| Credit cost 9.7% → 3.3% | Q1 2.3% was flattered; CGFMU window closed | LCR 177%, CD 81% | liquidity is not the problem |
### 8.2 Override table
| Flag | Type | Verdict | What changes my mind |
|---|---|---|---|
| GNPA fall via write-offs/ARC | looks-good | **OPEN** | Two quarters of net slippage < ₹120 cr and write-offs < ₹60 cr |
| DTA ₹495 cr + intangibles ₹246 cr in book | looks-good | **OPEN** | DTA starts being used (taxable profit) by FY28 |
| Q2 staff-cost drop | looks-good | **OPEN** | Q3 personnel cost ≤ ₹215 cr or explained |
| Capital cushion ₹306 cr vs 25–30% growth | bad | **OPEN** | Raise at ≥ book, or CRAR ≥ 16% with ≥ 15% growth |
| Bihar/UP concentration + undisclosed Bihar Act | bad (disclosure) | **OPEN** | Impact disclosed; Bihar CE ≥ 99% through FY27 |
| Guidance misses on growth and profit dates | bad | **OPEN** | FY27 GLP growth ≥ 20% |
| Post-merger PE/DFI supply | bad | watch | Lock-in disclosed or holders stay |
| CGFMU dependence | external input | watch | Claims paid in cash; window reopened |
| NIM/CoF/liquidity/no divergence | good | confirmed | — |
Open soft flags: **6** (+2 graded stage-2 flags fired) → a written variant view is required (8.4).

### 8.3 What the price implies (worksheet `tools/valuation/live/UTKARSHBNK_worksheet.md`, bank mode v1.1)
**Inputs (L8 step 1):** close ₹11.71 on 23-Nov-2026 (NSE bhavcopy = Yahoo; screener ₹11.7 — 3 sources); shares 177.95 cr; net worth ₹2,676 cr
(XBRL = deck); assumed **₹500 cr equity raise at ₹11** in FY28 (45.45 cr shares) `[EST]`; FY-end P/Bs only 3 (listed Jul-2023): Mar-24 1.74x,
Mar-25 0.82x, Mar-26 0.66x `[YH ÷ SCR; Yahoo pre-Nov-2025 closes are rights-adjusted; 1 src]`; peers median 1.01x; 6-month ADV ₹12.0 cr mean / ₹6.3 cr
median; CoE 12.5% (India default, for comparability), g 5%, σ 0.35.
**Scenarios (written before the outputs; 10-year linear ROE paths):** bear 30% (prolonged stress, second cycle: ROE −4% → 8%, exit 0.6x); base 40%
(slow recovery: 4% → 13%, exit 0.9x); bull 15% (guidance broadly met: 10% → 15%, exit 1.4x); blow-up 15% at 0.15x (a second cycle loss on CET1 book
₹1,907 cr at 10.9x leverage forces a deeply discounted raise or an RBI-led merger).
**Outputs:** P/B 0.78x (0.82x diluted); **ROE needed forever 11.2%** (13.2% on CET1 book, `UTKARSHBNK_cet1book_worksheet.md`); base-case IRR **12.0%**
= the 12% hurdle; 5-year multiples bear 0.68x / base 1.46x / bull 2.85x / blow-up 0.15x; **EV 1.24x raw** vs hurdle 1.76x; P(≥2x) 20%, P(≥3x) 7%,
P(≤0.5x) 21%, P(blow-up) 15%; probability-weighted RIM value ₹7.9 (−32%). Book stress: an extra 2% loan loss (post-tax) = 9% of book; 5% = 23%.
**Exit-multiple bet:** RIM-consistent P/B at year 5: bear 0.29x vs 0.60x used (the bear exit is *generous* — flagged by the tool), base 1.00x vs
0.90x, bull 1.41x vs 1.40x. As in every card (L21, L36), the exit multiple and the ROE path are the binding choices; here the bear exit is the
optimistic assumption, which means the true left tail is, if anything, fatter.
**Temperature:** own history insufficient (n = 3); **COOL vs SFB peers (0.82x of median)**; on CET1 book it is at the peer median.
**CET1-book sensitivity** (same scenarios, CET1 book; harsh because the exit P/Bs are then applied to CET1 book): EV 0.94x, base IRR 10.9%.

### 8.3b Value-trap test (why is it cheap?)
| Question | Evidence | Answer |
|---|---|---|
| Peak-cycle earnings? | Losses now; through-cycle ROE 6.8%; peak ROE 20–23% | **Trough**, not peak — cheap vs book, dear vs through-cycle earnings |
| Dated catalyst? | Return to profit (guided Q4 FY27); reverse merger (2027); equity raise (FY28) | Yes — two of three are dilutive/supply events |
| Business deteriorating? | NIM up, CoF down, SMA down; but secured-book slippage rising, GLP flat | Mixed |
| Capital allocation | Rights at ₹14 below 2024 book; next raise likely below book | Book per share is being diluted, not compounded |
| Who takes value before minorities? | Depositors (10.9x leverage), future equity buyers at a discount, ex-UCL PE holders selling | The minority's book is the first loss |
| Fraud / solvency trap? | Clean audit, no divergence, CRAR 17% | No fraud; solvency is thin, not breached |
**Conclusion:** a **recovery is already priced on the honest book** (1.09x CET1 book); the discount to reported book has verified causes (DTA and
software in book, below-book raise ahead, cycle risk). Not a claimable mispricing (as SUNFLAG L33, INDRAMEDCO L40).

### 8.4 Variant perception
- **Market:** a recovery to ~11–13% ROE (Gordon read) — a haircut version of management's FY28 15%.
- **Ours:** no claimable mispricing; evidence leans **negative** versus the company's framing (8.1–8.2), with real positives (NIM, funding,
  liquidity, peers' recoveries).
- **Proves us wrong (upside):** two consecutive profitable quarters with credit cost < 2.5% and an equity raise at or above book.
- **Proves us wrong (downside):** another quarterly loss > ₹150 cr or CRAR < 16% before the raise.
- **Base-class departure:** P(≥3x) 7% vs 21%; P(≤0.5x) 21% vs 11%; P(blow-up) 15% vs 15%. Tails anchored at **w = 0.3** with an evidence note:
  the class is **non-financial** (no lender class on file) and cannot see 10.9x leverage; anchoring at 0.5 would have pulled P(≤0.5x) to 16%. Even at
  0.3 the card's v1.4 warning fires ("anchoring lowered documented tails") — correctly.

### 8.5 Decision card (`tools/decision/live/UTKARSHBNK_card.md`, **card v1.4**)
**Rule output: size 0**, blocked by *Expected value vs hurdle* (anchored EV **1.29x**, raw 1.24x vs 1.76x). Stage 2 passed (7 hard rules); PEAD
quintile 5 (clear); survival cap clear (pledge 0; interest cover not applied to lenders; no core-asset threat); 8 open soft flags with a written
variant view (not blocking); tier speculative. Review **2027-02-15**.
Card calls (live, 5-year to 2031-11-23): P(≥3x) 0.074 (base 0.213); P(≤0.5x) 0.207 raw / 0.179 anchored (base 0.113); P(blow-up) 0.150 raw / 0.151
anchored (base 0.154).

---

## 9. Forward calls (live; tags paper-call, deepdive-generated, live, india, sector-banks; specs in `tools/scoreboard/specs.json`)
| # | Call (YES if…) | Resolve by | Our P | Naive base | Reasoning |
|---|---|---|---|---|---|
| 1 | FY27 gross loan portfolio **≥ ₹24,165 cr** (+25%, the bottom of guidance) | 2027-05-31 | **0.05** | 0.50 | Naive: numeric guidance mostly met (L26) [EST]. Ours: H1 +3.8%; H2 needs +20% in 6 months vs +3.6% in H2 FY26; the Nov-2025 "25%" became −1.7% |
| 2 | Q3 FY27 net profit **> 0** | 2027-02-28 | **0.20** | 0.14 | Naive: 0 of last 5 quarters profitable (Laplace). Ours: normal PPOP ~70–100 vs provisions ~130–160 |
| 3 | Q4 FY27 net profit **≥ ₹67 cr** (~10% annualised ROE, the "double-digit exit") | 2027-05-31 | **0.10** | 0.50 | Naive: guidance met [EST]. Ours: needs a ₹137 cr swing from Q2 in two quarters |
| 4 | GNPA **≤ 5.0%** at 31-Mar-2027 | 2027-05-31 | **0.45** | 0.50 | Naive: trend coin [EST]. Ours: habitual Q4 write-offs/ARC vs rising secured slippage |
| 5 | Total CRAR **≥ 16.0%** at 31-Mar-2027 | 2027-05-31 | **0.80** | 0.86 | Naive: 5 of 5 recent quarter-ends ≥ 16% (Laplace). Ours: ₹200 cr Tier 2 planned; slow growth; small losses |
| 6 | Board approves an **equity raise** (QIP/rights/preferential) by 30-Nov-2027 | 2027-11-30 | **0.45** | 0.30 | Naive [EST]: ~1 in 3 small-cap lenders per year. Ours: guided "next FY", ₹306 cr cushion |
| 7 | **Reverse merger effective** by 30-Jun-2027 | 2027-06-30 | **0.60** | 0.65 | Naive [EST]: NCLT sanction 3–12 months after second motion. Ours: NOCs in hand; NCLT calendar slips |
| 8 | UTKARSHBNK price **beats Nifty 500** from 23-Nov-2026 (₹11.71; 23,748.15) to 30-Sep-2027 | 2027-09-30 | **0.40** | 0.44 | Naive [EST, as live #1/#3/#4]. Ours: recovery partly priced; raise and PE overhang vs return to profit |
Calls 1–5 are **assisted** doc-scan specs (the resolver's `india_fin` parser cannot read banking XBRL — see 10.3); 6–7 assisted (Reg-30 scan,
human confirmation); 8 structured (price relative); card calls human (total return, rights/merger-adjusted).

---

## 10. What this run taught the method (curriculum)
1. **No lender base-rate class.** The card anchored a 10.9x-levered bank to the India *non-financial* class. Build an India lender class
   (survivorship-free banks/NBFCs/HFCs, ₹1,000–20,000 cr, 5-year) before the next lender card; until then use w ≤ 0.3 with a note for lenders.
2. **Value lenders on CET1 book beside reported book.** DTA on losses (recognised on an expert opinion) and capitalised software were 28% of net
   worth and moved Tier-1 by 235 bp in a quarter with no loss. Proposal: `bank.py` input `cet1_book` (Pillar 3 DF-11 rows 9–10) and a P/CET1 line;
   protocol S2 bank form adds "DF-11 deductions vs net worth" (`insight:lender-book-quality-cet1-deductions`).
3. **The resolver cannot read banking XBRL** (`InterestEarned`, `ProfitLossForThePeriod`, `PercentageOfGrossNpa`, `CET1Ratio`): every lender metric
   call is "assisted". Add a banking branch to `sources.xbrl_period_values` so lender calls resolve structurally (S0 rule (a) "XBRL exists" was
   satisfied but useless for this reason).
4. **`bank.py` ROE paths are linear over 10 years** and dilution applies to every scenario: it cannot draw a recovery J-curve or a bear-only
   below-book raise. Add an explicit year-by-year ROE list and per-scenario dilution.
5. **L40 generalises to state law.** The single most decision-relevant external fact (Bihar MFI Act; ~17% of GLP in Bihar) was absent from the AR
   and three calls. Rule: for any geographic concentration > 15% of the book, search that state's gazette/assembly for laws on the activity.
6. **"The question nobody asks" worked again** (Tier-1 drop, staff-cost drop, DTA, Bihar Act — none raised by analysts on the call).
7. **The anchoring-lowered warning fires structurally for lenders** while the only class is non-financial; it did its job here, but note it as
   expected until a lender class exists.
8. **`insight:lender-blowup-signals` fired but is not a card gate.** Candidate: pre-register a test of "discount to book + ≥2 lender signals" on the
   survivorship-free lender panel (item 1) before making it a gate.
9. **S0:** 34 of 70 eligible names were lenders, half hand-classified; holdco-vs-lender calls (IFCI, EDELWEISS, JMFINANCIL) needed judgment. The
   industry map (L40 process point) is still the fix.
10. **Tool notes:** `bse_fetch.py announcements` returns HTTP 400 for page 2+ (only 20 rows per range); screener Sep-2026 reserves ₹846 cr vs XBRL
    ₹896.81 cr (unexplained); Yahoo closes before Nov-2025 are rights-adjusted (non-round), so the FY-end P/B history mixes adjusted prices with
    unadjusted books; the bank's own site serves Pillar 3 PDFs without a bot wall (contrary to the Federal Bank note).

## 11. Open items
Reason for the Q2 FY27 personnel-cost drop; CGFMU claim payouts and the bank's window status; Bihar collection efficiency after the Act; AGM 04-Aug-2026
vote results (scanned); UCL share count and the exact post-merger share change (swap 699:100; assumed ~neutral); lock-in on shares to UCL holders;
segment GNPA for MSME/CV/housing (promised on the call); CRR rate and PSL achievement for FY26 (not extracted); FY23–24 PPOP split.

## Sources
- AR FY2025-26: https://nsearchives.nseindia.in/annual_reports/AR_29715_UTKARSHBNK_2025_2026_A_7865039_10072026171622.pdf
- Q2 FY27 banking XBRL: https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_BANKING_1752247_03112026084750_WEB.xml (and six earlier quarters listed by `nse_fetch.py integrated UTKARSHBNK`)
- Investor presentation Q2 FY27: https://nsearchives.nseindia.in/corporate/UTKARSHBANK_03112026204030_InvestorPresentationQ2Sept26.pdf ; press release: https://nsearchives.nseindia.in/corporate/UTKARSHBANK_03112026203644_PressreleaseQ2Sep26.pdf
- Q2 FY27 call transcript: https://nsearchives.nseindia.in/corporate/UTKARSHBANK_11112026151543_intimationtranscriptofearningscall.pdf (earlier: 09-May-2025, 19-Nov-2025, 15-May-2026, 07-Aug-2026 filings)
- Pillar 3 30-Sep-2026: https://www.utkarsh.bank.in/uploads/pdf/our-policy/template_ten/Basel_III_Pillar_3_Disclosures_as_on_September_30_2026.pdf
- Scheme of amalgamation (board outcome 20-Sep-2024): https://nsearchives.nseindia.in/corporate/UTKARSHBNK_20092024220752_Outcome.pdf ; NCLT orders 13-Feb-2026, 20-May-2026 (NSE)
- Rights issue: https://nsearchives.nseindia.in/corporate/UTKARSHBANK_08102025122500_Outcome.pdf ; specific investors: https://nsearchives.nseindia.in/corporate/UTKARSHBANK_24102025114020_rev1.pdf
- Ratings: ICRA 02-Jul-2026, CARE 14-Jul-2026 / 03-Sep-2026, CARE 05-Jan-2026, ICRA/CARE Aug-2025 (NSE filings)
- SEBI settlement 10-Apr-2024: https://nsearchives.nseindia.in/corporate/UTKARSHBNK_10042024204737_Intimation.pdf
- Bihar Micro Finance Institutions Act 2026: https://prsindia.org/files/bills_acts/acts_states/bihar/2026/Act11of2026BR.pdf ; market reaction: https://www.angelone.in/news/stocks/bihar-mfi-bill-2026-triggers-up-to-11-share-price-drop-in-l-t-finance-utkarsh-small-finance-bank-and-fusion-finance
- CGFMU extension (press, 1 src): https://www.manoramayearbook.in/current-affairs/india/2026/11/12/cabinet-credit-guarantee-fund-for-micro-units.html
- NSE bhavcopy 23-Nov-2026; SHP XBRL 30-Sep-2026; Yahoo v8 UTKARSHBNK.NS, ^CRSLDX; screener.in UTKARSHBNK, UJJIVANSFB, EQUITASBNK, ESAFSFB, SURYODAY, JSFB, CAPITALSFB, AUBANK (24-Nov-2026)
- Selection: `research_notes/Deep dives/UTKARSHBNK_selection/` (prereg_selection.md, selection_order.json); scripts in scratchpad `live_dd5/scripts/` (frame.py, draw.py, pead.py, s2check.sh, bankx.py)
