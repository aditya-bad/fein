# Federal Bank (NSE: FEDERALBNK): end-to-end DRY RUN of stages 2→6 on a bank

**2026-11-22 · TEST MATERIAL (L9, L21). No buy/sell/watchlist verdict. The decision card is labelled practice and is not
added to the stage-7 scoreboard.** Research, not SEBI-registered advice.

**Roadmap:** builds stages 2–6 (hard filters → signals → deep dive → valuation → decision) on a new sector type, a
lender, to find what breaks. **Unlocks:** a bank/NBFC branch in every tool (promise tracker, worksheet, card,
protocol v1.3), so the next lender run (an NBFC, a PSU bank) is comparable and faster.

**Files produced**
| What | Path |
|---|---|
| This note | `research_notes/Deep dives/FEDERALBNK_dryrun.md` |
| Worksheet input / output (bank mode) | `tools/valuation/examples/FEDERALBNK.json`, `FEDERALBNK_worksheet.md/.json` |
| Decision card (practice) / paper calls (NOT ingested) | `tools/decision/examples/FEDERALBNK_card.json/.md`, `FEDERALBNK_paper_calls.json` |
| New bank valuation module | `tools/valuation/bank.py` (dispatched from `worksheet.py` when `"mode": "bank"`) |
| New bank KPI extractor | `tools/promise_tracker/pipeline/bank_kpis.py` |
| Promise ledger (29, manual LLM step), bank KPI CSVs, scored file, credibility report | `research_notes/Deep dives/FEDERALBNK_dryrun_outputs/` (promises not seeded into memdb) |
| Protocol | `research_notes/Deep dives/deep_dive_protocol.md` → **v1.3** |
| memdb seed (not ingested) | `memdb/seeds/2026-11-22_dryrun_federalbnk.json` |

**Source discipline.** Every number carries a source. Primary sources: NSE integrated-filing XBRL (Q4 FY25–Q2 FY27),
FBL investor presentations (Q2 FY26–Q2 FY27), Integrated Annual Report FY26 (NSE, 30-Jul-2026, 266 pp), BRSR FY26,
earnings-call transcripts (company website; NSE carries only cover letters), rating letters (CARE, India Ratings,
CRISIL, S&P), Reg-30 filings (NSE + BSE), screener.in, Yahoo chart API. "[EST]" = our estimate with the method shown.
"single-source" = not yet confirmed by a second dated source. Transcripts are company-produced and had two
transcription errors (§4.8), so transcript numbers are treated as single-source.

---

## 0. Rule zero: edge before depth (written first)
1. **What the market knows / asks.** The five most-asked Q2 FY27 call topics: (a) FCNR special-window leverage
   economics, (b) NIM trajectory after the October 2026 repo hike, (c) opex and cost-to-income, (d) loan-growth
   guidance, (e) gold-loan LTV and ECL. Consensus sees a NIM/RoA recovery, the Blackstone capital and M&A optionality.
2. **The variable that moves value most:** *sustainable ROE on fully diluted book* = RoA × leverage. Whether the
   RoA gain (1.09% → 1.32% YoY) is franchise (CASA mix, mid-yield shift, fees) or cycle (rate cycle, FCNR window,
   one-offs, write-offs), and whether costs step up (IBA wage settlement due Nov-2027).
3. **Layer most likely to reveal it:** the deposit franchise (Kerala/NRI concentration, quarter-end vs average
   balances) and the Schedule 16 cost lines. **Nobody asked about:** the 2027 IBA wage revision, the DICGC premium,
   ₹5,298 cr of PSL-shortfall deposits, write-off-driven GNPA, or the 59% Kerala deposit share. That is where depth
   paid off below.

---

## 1. Stage 2: hard and graded filters (disqualifiers v2, bank form)
`decision:adopt-disqualifiers-v2` (hard at entry / hard at exit / graded / questions) plus `insight:lender-blowup-signals`.

| Rule (v2) | Bank adaptation used | Status | Evidence (source) |
|---|---|---|---|
| H1a fake cash | Cash/RBI balances and investments verifiable; audited | **PASS** | Cash + RBI ₹16,801 cr, investments ₹84,045 cr (Q2 FY27 XBRL); FY26 opinion unmodified (AR FY26 auditor's report) |
| H1b implausible economics | NIM/RoA/C-I vs peer band, yield − CoD re-derived | **PASS** | NIM 3.32%, yield 8.70%, CoD 5.18%, RoA 1.32% (Q2 FY27 deck); spread 3.52 pp re-derived |
| H1c unverifiable profits | One-offs traced to external documents | **PASS** | ₹456 cr interest on IT refund (Q4 FY26) traced to IT orders filed on NSE 19-Feb/26-Mar/27-Mar-2026 (refunds ₹686 + ₹490 + ₹323 = ₹1,499 cr incl. interest) |
| H2 auditor exit / qualification | Rotation vs resignation | **PASS** | 15-May-2026: RBI-approved rotation on term completion (Suri & Co + MSKA → Price Waterhouse LLP + K S Aiyar) (NSE Reg-30) |
| H3 rating "not cooperating" | All agencies | **PASS** | CARE AA+/Stable 9-Oct-2026; IND AA+/Stable 22-Sep-2026; CRISIL AAA (FD) 30-Dec-2025; S&P BBB-/Stable (first) 9-Jul-2026 |
| H4 pump | — | **PASS** | Nifty constituent, 100% public (NSE SHP 30-Sep-2026) |
| H5 related-party leakage | Connected lending (AS-18) | **PASS** | No promoter. FY26 AS-18: advances ₹1,126 cr + NCDs ₹235 cr to subsidiary Fedbank Financial (60.64%, itself listed); KMP-relative deposits ~₹1 cr (AR FY26 n.2.3) |
| EXIT: RBI NPA divergence | AR note "Divergence in asset classification" | **PASS** | AR FY26 n.1.4.5: FY25 and FY24 divergence below the disclosure threshold |
| EXIT: restatement / delayed results / 8-K 4.02 analogue | — | **PASS** | No restatement filings Jan-2025..Nov-2026; results filed 16 days after quarter-end |
| Graded: pledge | — | **CLEAR (n/a)** | Promoter 0%; NSE pledge API 0 rows |
| Graded: accounting-trouble events 5y | Regulator penalties | **CLEAR** | RBI penalty ₹27.3 lakh, 7-Feb-2025 (Interest Rate on Deposits Directions); GST penalty ₹15 lakh set aside 13-Nov-2026 (BSE only) |
| Graded: solvency — capital | CET1 vs floor; leverage | **CLEAR** | CET1 15.76% (Sep-26 XBRL; no AT1), floor 12% (Ind-Ra); leverage ratio 8.42% FY26 (AR) |
| Graded: solvency — funding | Concentration, bulk share, CD ratio | **FIRED (question)** | Kerala 58.8% of deposits (Ind-Ra, Q1 FY27); NR deposits ₹1,19,056 cr = 34.7% of deposits; FCNR(B) +239% YoY; "<₹3 cr" granular share fell 85% → 81% QoQ; CD ratio 298,226/342,694 = 87.0% |
| Graded: frauds | AR n.1.4.9 | **FIRED (question)** | Amount ₹207 cr FY26 vs ₹79 cr FY25 (count 510 vs 3,803); 100% provided |
| Lender signal 7: window-dressing | Period-end vs average balances | **question** | Period-end CASA ₹1,09,803 cr vs average CASA ₹1,01,791 cr (+7.9%); CA +14% QoQ in Q2 (deck slides 4, 12) |

**Stage-2 result: all hard rules PASS (9/9 checked, 0 unknown). Two graded flags fired (funding concentration, fraud
value) and one lender question (quarter-end CA bump).** The lender rule "two+ signals + discount to book = avoid"
does not apply (P/B premium).

---

## 2. Stage 3: signals
### 2.1 Earnings surprise (PEAD, tools/backtests/india_pead logic)
`live_tracker.sue_for()` on `eps_history.csv` (consolidated EPS, 8 prior seasonal changes), fixed v2 cut-points
`[-0.62, -0.001, 0.42, 1.24]`:

| Quarter | Consolidated EPS (yr-ago) | SUE | Quintile |
|---|---|---|---|
| Q2 FY26 | 4.04 (4.48) | −1.11 | 1 (an avoid flag would have been active to ~Jan-2026) |
| Q3 FY26 | 4.45 (3.85) | +1.54 | 5 |
| Q4 FY26 | 5.44 (4.44) | +2.23 | 5 (includes the ₹456 cr one-off) |
| Q1 FY27 | 5.09 (3.74) | +2.48 | 5 |
| **Q2 FY27 (event 16-Oct-2026)** | **6.07 (4.04)** | **+2.91** | **5 (provisional)** |

Avoid flag not active. Per L19 a top-quintile surprise is **not** a buy reason. Bank caveat: reported EPS mixes
treasury gains (Q2 ₹238 cr vs ₹113 cr) and provision buffers; normalised Q2 EPS (~₹5.2 basic [EST]) is still a
large beat, so the quintile is robust here, but see §6 gap G6.

### 2.2 Promise tracker (tools/promise_tracker/pipeline, rules + Claude as the LLM step)
**Calls used (6):** Q4 FY25 (30-Apr-2025), Q1 FY26 (2-Aug-2025), Q3 FY26 (16-Jan-2026), Q4 FY26 (29-Apr-2026),
Q1 FY27 (17-Jul-2026), Q2 FY27 (16-Oct-2026). Q2 FY26's transcript could not be fetched (website bot block).
Pipeline: 412 rule candidates → 29 promises (manual LLM step) → scored on a bank KPI CSV (XBRL + deck).

| Result | Value |
|---|---|
| Promises / resolved | 29 / 9 (20 pending, mostly FY27–FY28) |
| MCS / weighted delivery / hit rate | **+0.93 / 92.9% / 77.8%** (grade A on paper) |
| Goalpost changes (unacknowledged) | 3 flagged (C/I ceiling 53.5% → 55% → 56%, then "around 52%"; CASA 36% "in 3 years" → "at some point") |
| Usable as a signal? | **No (L18):** no bank peer base; <5 resolved per category; guidance is conservative (NIM guided −5–10 bps for Q2 FY26, delivered +12 bps; credit cost guided 50–60 bps, running 31–41 bps) |

Resolved promises:
| Said | Promise | Actual | Status |
|---|---|---|---|
| 30-Apr-25 | FY26 C/I 52.5–53.5% | 53.90% excl one-off (52.27% reported) | partly |
| 30-Apr-25 | FY26 loan growth >12% | net advances +12.7% (XBRL Mar-26 vs Mar-25) | delivered |
| 2-Aug-25 | FY26 credit cost ~55 bps (50–60) | 54 bps excl one-off (73 reported) | delivered |
| 2-Aug-25 | Q2 FY26 NIM down 5–10 bps from 2.94% | 3.06% | delivered (beat) |
| 2-Aug-25 | RoA bottomed (1.00%), sustain and rise | 1.24% Q4 FY26 excl one-off | delivered |
| 2-Aug-25 | Detailed strategy review in Jan-2026 | brand/strategy update on the Jan call only | partly (judgment) |
| 16-Jan-26 | FY26 credit cost 52–53 bps | 54 bps excl one-off | delivered (within 5 bps) |
| 16-Jan-26 | Q4 FY26 NIM ~3.18% | 3.20% excl one-off | delivered |
| 16-Jan-26 | Blackstone money by Q4 FY26 | CET1 13.89% → 15.93% Mar-26; ₹1,549 cr warrant money on books | delivered (inference) |

Key pending: NIM +5–6 bps/qtr to ≥3.40% by Q4 FY27 (tracking 3.32%); RoA +3–4 bps/qtr to ≥1.36% (tracking 1.32%);
FY27 credit cost "lower end of 50–60 bps"; ~100 branches in FY27 (+22 in H1); SCB card portfolio integrated by
31-Dec-2026; ECL one-time hit 1.5–2% of net worth (Apr-2027); CASA 36%; loan growth "mid-teens" (H1 +21.7%
reported, ~18% ex-FCNR loans).
**Traceability finding:** management twice cited "the guidance we gave" (NIM +5–6 bps/qtr, RoA +3–4 bps/qtr) that
appears in none of the 5 earlier transcripts we hold. The first traceable date is 17-Jul-2026. A promise tracker
must date a promise from its first traceable statement, not from management's recollection.

**How the pipeline handled bank metrics (before the fixes in §6):** no bank vocabulary at all. NIM, credit cost,
GNPA, CASA, loan growth were "no financial measure recognised"; worse, "net interest margin ~3.2%" matched the
finance-cost rule (`interest` + `%`) and would have been scored as interest ÷ revenue (~59%) → a false "missed".
Screener's bank page has no NIM/CASA/credit-cost rows, so even a correct measure had no data. All fixed or
documented in §6.

---

## 3. Stage 4: deep dive at "security-guard depth" (bank adaptation)
Units for a lender: **(1) the branch** (deposit gathering and sourcing), **(2) the loan cohort/segment** (yield,
slippage, LGD), **(3) the liability pool** (CASA, retail TD, NRI/FCNR, bulk), **(4) the cost line in physical terms**
(people × IBA wage, deposits × DICGC premium, NDTL × CRR, PSL shortfall × RIDF rate).

### 3.1 Map
Old private bank (Aluva, Kerala; 1931), 1,662 outlets (Sep-26; 1,640 at Mar-26: 310 metro, 316 urban, 780
semi-urban, 234 rural, AR FY26), 2,145 ATMs/recyclers, 17,681 employees (BRSR FY26; 16,111 FY25). Subsidiaries:
Fedbank Financial Services (60.64%, listed NBFC), FedServ (100%, ops/tech), Ageas Federal Life (30%). Strategic
investor: Blackstone (Asia II Topco XIII) via 27.3 cr warrants at ₹227 (≈9.95% post-issue). MD & CEO KVS Manian
since Sep-2024 (3-year term). Peers with the same units: City Union, Karur Vysya, South Indian Bank (Kerala), CSB
(Kerala), plus AU/IDFC First/RBL for mid-size private.

### 3.2 Reported financials, re-derived (₹ cr; standalone)
| | Q2 FY26 | Q3 FY26 | Q4 FY26 | Q1 FY27 | Q2 FY27 | Source |
|---|---|---|---|---|---|---|
| NII | 2,495 | 2,653 | 3,173 (2,717 excl) | 2,946 | 3,153 | deck slide 6, XBRL |
| Fee income | 886 | 896 | 991 | 957 | 1,168 | deck slide 20 |
| Treasury income | 113 | 126 | 12 | 22 | 238 | deck slide 20 |
| Opex | 1,933 | — | — | 2,097 | 2,418 | deck slide 31 |
| PAT | 955 | 1,041 | 1,259 (1,145 excl) | 1,177 | 1,386 | XBRL/screener |
| NIM % | 3.06 | 3.18 | 3.74 (3.20 excl) | 3.33 | 3.32 | deck |
| C/I % | 54.04 | 53.92 | 47.28 (52.86 excl) | 52.50 | 52.08 | deck; XBRL-derived 54.0/53.9/47.3/52.5/52.1 agree |
| Credit cost % | 0.50 | 0.47 | 1.18 (0.47 excl) | 0.41 | 0.31 | deck / transcripts |
| GNPA / NNPA % | 1.83/0.48 | 1.72/0.42 | 1.62/0.20 | 1.52/0.18 | 1.32/0.17 | XBRL = deck |
| CET1 % | 14.37 | 13.89 | 15.93 | 15.89 | 15.76 | XBRL (AR FY26 15.93) |
| RoA % (ann.) | 1.09 | 1.15 | 1.36 (1.24 excl) | 1.22 | 1.32 | deck; XBRL 0.33%/qtr ×4 = 1.32 |

Re-derivations: Q2 FY27 PPOP = 3,153 + 1,490 − 2,418 = 2,225 ✓ (XBRL 2,225.4). Provisions 342 = loan loss 218 +
investment 13 + standard 107 + other 4 (deck slide 9) ✓. **Q4 FY26 one-off:** interest on IT refund ₹456 cr in NII and
tax reversal ₹115 cr, offset by a ~₹470 cr buffer provision [EST: (1.18 − 0.47)% × avg advances ~₹2.65 lakh cr ÷ 4]
kept for the ECL transition (Q4 FY26 call). **Diluted EPS** Q2 FY27 ₹5.38 vs basic ₹5.61 (XBRL): warrants already dilute.

### 3.3 Branch and employee economics (unit 1) [EST unless sourced]
| Per outlet (FY26; avg outlets ~1,615 [EST: (1,589 + 1,640)/2, Mar-25 count inferred]) | Value | Method |
|---|---|---|
| Deposits / CASA / net advances per outlet (Sep-26) | ₹206 cr / ₹66 cr / ₹179 cr | deck slide 30 ÷ 1,662 |
| Employees per outlet (incl. HO, hubs) | 10.6 | 17,681 ÷ 1,662 |
| Revenue (NII + other income) per outlet | ₹9.3 cr | (10,657 + 4,440) ÷ 1,615; NII = 27,695 − 17,038 (screener FY26) |
| Opex / staff cost / rent per outlet | ₹4.9 cr / ₹2.0 cr / ₹0.22 cr (₹1.8 lakh a month) | Schedule 16 FY26 ÷ 1,615 |
| PAT per outlet | ₹2.5 cr | 4,117 ÷ 1,615 |
| Loaded cost per employee vs BRSR median pay | ₹19.1 lakh vs ₹15.8 lakh median | 3,225 cr ÷ 16,896 avg staff; BRSR median (M ₹16.3 L, F ₹15.1 L) |
| Attrition | 5.05% (voluntary 4.14%) | BRSR FY26 — very low (unionised, Kerala) |
| Liability value of a mature branch | CASA ₹66 cr × ~4.5 pp saving vs wholesale ≈ ₹3.0 cr/yr vs direct cost ~₹2.4 cr | [EST] SA rate 2.5% (cut 15-Jun-2025, Q1 FY26 call), CA 0%, CD/bulk ~6.5–7%; direct cost = 8 staff × ₹19 L + rent + ₹0.7 cr other |
Implication: a mature branch roughly pays for itself on CASA alone; a new branch needs ~₹50–60 cr of CASA
(2–4 years, peer proxy, unverified) before it does. The 100-branch FY27 plan is therefore a 2–3 year drag on C/I.

### 3.4 Cost-to-income by component (FY26, Schedule 16; % of NII + other income ₹15,097 cr)
| Line (₹ cr) | FY26 | FY25 | YoY | % of income | Physical driver / sensitivity |
|---|---|---|---|---|---|
| Employees | 3,225 | 3,088 | +4% | 21.4% | Headcount × IBA scale. **Bipartite settlement applies** (AR "provisions of Bipartite"). The 12th settlement (Nov-2022–Oct-2027) gave ~17% [general knowledge, unverified]; if the 13th is similar on ~60% of staff cost [EST]: +₹330 cr pre-tax/yr ≈ 5% of PAT ≈ −50 bps ROE from FY28. Also actuarial pension/gratuity swings with G-sec yields (Q2 FY27 call) |
| Other expenditure | 3,069 | 2,665 | +15% | 20.3% | incl. service charges to providers ₹1,019 cr (+17%; sourcing/ops outsourcing) and card-network charges ₹510 cr (+18%; scales with card spends) (AR n.1.12.9) |
| Insurance (mostly DICGC) | 380 | 350 | +8% | 2.5% | ≈ 12 paise per ₹100 of assessable deposits: 380 ÷ 0.0012 ≈ ₹3.2 lakh cr ≈ deposits ✓. Each 1 paise change ≈ ₹32 cr |
| Rent, taxes, lighting | 354 | 334 | +6% | 2.3% | outlets × ₹1.8 lakh/month |
| Depreciation | 282 | 267 | +6% | 1.9% | tech + branch fit-outs |
| Postage, telecom | 253 | 187 | +35% | 1.7% | digital transaction volumes, SMS/OTP |
| Repairs | 141 | 129 | +9% | 0.9% | |
| Advertisement | 81 | 51 | +60% | 0.5% | brand refresh (Vidya Balan campaign) |
| Other small lines | 107 | 97 | | 0.7% | printing, law, auditors, directors |
| **Total** | **7,892** | **7,168** | **+10%** | **52.3%** | Q2 FY27 opex +25% YoY: ESOP fair-value switch ₹32.7 cr, branches, new sales channel, tech, actuarial |
**Balance-sheet "costs" that sit in NIM, not opex:** PSL-shortfall deposits (RIDF etc.) ₹5,298 cr (₹8,457 cr FY25)
earning well below the 8.7% loan yield → drag ~₹200–250 cr/yr ≈ 6 bps NIM [EST, rate gap 4–5 pp]; CRR at 3% of
NDTL [RBI 2025, unverified here] → each 1 pp ≈ ₹3,200 cr idle ≈ 5 bps NIM.

### 3.5 Deposit franchise (unit 3)
| Metric (Sep-26) | Value | Source / note |
|---|---|---|
| Deposits / CASA / CASA ratio | ₹3,42,694 cr / ₹1,09,803 cr / 32.04% | deck; average CASA ₹1,01,791 cr (period-end +7.9% above average) |
| Retail granularity (CASA + TD < ₹3 cr, per LCR) | 81% (85% a quarter earlier) | deck slide 32 — fell because of FCNR |
| NR deposits / NRE | ₹1,19,056 cr (34.7%) / ₹1,09,162 cr | press release; FCNR(B) ₹23,548 cr (+239%), ₹14,922 cr mobilised in the special window |
| Kerala share of deposits | 58.8% (Q1 FY27) | Ind-Ra 22-Sep-2026 (single-source) |
| Cost of deposits / funds | 5.18% / 5.21% (−39 / −40 bps YoY) | deck |
| Inward-remittance market share | 21.67% (Q1 FY27) | **company-computed** from its data ÷ RBI BoP preliminary data (deck footnote) |
| Top-20 depositors | ~4.5% of deposits | deck slide 35 (pdftotext garbled; read as the lower series) |
**NRI/Gulf sensitivity [EST]:** if NR deposit growth stalls for a year (0% vs ~15%), ~₹18,000 cr must come from TDs
at ~100 bps more → ~₹180 cr ≈ 5 bps NIM; the bigger risk is CASA mix (NRE SB is cheap). The West Asia conflict of
2026 is already in the transcripts (Q4 FY26, Q1 FY27).

### 3.6 Loan book composition and yield (unit 2)
Net customer assets ₹3,00,875 cr (Sep-26): retail book ₹1,63,429 cr (54%) of which gold ₹44,242 cr (+37% YoY),
BuB ₹21,419 cr, agri ₹8,065 cr, CV/CE ₹6,081 cr, micro ₹3,908 cr, "retail" ₹79,714 cr (housing ₹35,233 cr −1% YoY,
LAP ₹9,400 cr +32%, auto ₹8,777 cr +3%, cards ₹4,801 cr +28%, **other ₹17,541 cr incl. ₹9,438 cr loans against FCNR
deposits**); commercial ₹32,780 cr (11%, +25%); corporate ₹1,04,666 cr (35%, +17%). Rate type: 45% EBLR, 33% fixed,
~22% MCLR (Q2 call). Yield on advances 8.70% (8.99% a year ago).
**Re-derived core growth:** retail "retail" ex-FCNR loans ₹70,276 cr vs ₹67,600 cr = **+4% YoY** (headline +18%).
Total net customer assets ex-FCNR loans +16% (headline +20%); gross advances ex-FCNR ~+18% (analyst on the call)
vs +21.7% headline. **Rate-cycle effect:** the 7-Oct-2026 repo hike (+25 bps to 5.5%, Q2 call) reprices the 45% EBLR
book at once: ≈ ₹3 lakh cr × 45% × 0.25% ≈ ₹340 cr/yr ≈ +9 bps NIM before deposits reprice (~1 year lag) [EST].
Part of the promised "+5–6 bps a quarter" is therefore cyclical.

### 3.7 Asset quality, vintage and provisioning
| | Value | Source |
|---|---|---|
| Q2 FY27 NPA walk | 4,282 + slippage 420 + 6 − recoveries/upgrades 220 − **write-offs 498** = 3,990 | deck slide 9 |
| GNPA by vertical (Q2 FY27, ₹ cr; ÷ vertical book [EST]) | retail 1,401 (1.8%), agri/MFI 1,271 (~10.6% of ₹11,973 cr), BuB 642 (3.0%), CV/CE 155 (2.5%, rising 113→139→155), CoB 440 (1.3%), corporate 81 (0.1%) | deck slide 33 |
| Slippage ratio (ann.) | 0.59% (0.94% a year ago); fresh slippage 420 (579 a year ago) | deck |
| Restructured standard | ₹1,389.55 cr (0.46%) | press release |
| PCR excl / incl TWO | 86.78% / 94.49% (73.45% a year ago; 76.55% Q4 FY26 excl one-off) | deck Q4 FY26 slide 4 |
| Net stressed book / net worth | 3.8% (Q1 FY27) | Ind-Ra |
| ECL transition | 1.5–2% of net worth, effective 1-Apr-2027 | Q1 FY27 call |
**Vintage:** the bank discloses no origination-cohort data; slippage by segment is the only proxy. Gold-loan LTV
rose from ~55% to ~60–61% in one quarter (Q2 call), with PSU competition below 9% vs the bank's ~10.4% yield.
Without Q2's write-offs GNPA would be ~4,488 cr ≈ 1.49% [EST], not 1.32%.

### 3.8 Fee income, capital, digital partnerships
- **Fees** ₹1,168 cr Q2 (1.11% of average earning assets; FY26 1.21% of assets per Ind-Ra): other service charges
  568 (49%), loan processing 246, insurance 146 (Ageas associate), forex/derivatives 104, commissions 104. The CFO
  said some FCNR-related fee is inside but "not significant". Card spends rank 9 among private banks (1.90% spend
  share; 3.13% of cards outstanding, deck slide 28, company calculation).
- **Capital:** CET1 15.76%, RWA ₹2,50,722 cr (density 58.7% of assets). On warrant exercise (+₹4,647 cr) CET1 rises
  ~1.85 pp to ~17.6% [EST] — ROE on diluted book ~10% until deployed. The ₹10,000 cr bond enabling resolution
  (17-Jul-2026) and a USD 500 mn MTN programme (17-Sep-2026) add funding options. M&A rumours: Jana SFB
  (25-Sep-2026) and "open to deals" (19-Oct-2026), both answered "no material event".
- **Digital partnerships risk:** the deck lists partner channels for deposits, loans, cards, merchant payments and
  remittance; the AR notes "resumption of business with a key fintech partner" (i.e. it had paused). Partner names,
  the share of cards/deposits sourced through partners and any RBI direction are **not disclosed** → ground check.

### 3.9 Governance and incentives (L5)
No promoter; board of 10 (7 independent). Postal ballot 18-Nov-2026: MD & CEO fixed pay ₹4.54 cr p.a.; variable pay
capped at 300% of fixed (RBI rule); ESOPs. CFO change (Manikandan M from 1-May-2026). CEO term ends ~Sep-2027 (Ind-Ra:
3 years from Sep-2024). RPT table: §1 H5 (subsidiary lending only).

### 3.10 Bad-but-benign vs good-but-misleading
| Looks bad, is (mostly) benign | Why | Looks good, may mislead | Why |
|---|---|---|---|
| Q4 FY26 credit cost 118 bps | a ₹470 cr ECL buffer funded by a tax windfall | Retail book +18% YoY / +15% QoQ | ₹9,438 cr FCNR-backed loans; core retail +4% |
| CET1 13.89% at Dec-25 | before Blackstone's ₹1,549 cr | Deposits +18.6%, NR +27% | FCNR special window (₹14,922 cr) |
| Agri/MFI GNPA ~10% | ~4% of loans, provided; growth deliberately slowed | GNPA "decadal low" 1.32% | write-offs ₹498 cr > slippage ₹420 cr |
| C/I 52% vs top peers' ~40% | IBA wages, Kerala network, investment phase | PCR 87% | one-time buffer (76.6% excl) |
| Frauds ₹207 cr FY26 | count down 86%; fully provided | PAT +45% YoY | weak base (MFI provisions) + treasury ₹238 cr |
| Opex +25% YoY | ESOP switch, branches, actuarial | NIM +26 bps YoY | rate cycle (CoD −39 bps; Oct-26 repo hike on 45% EBLR), not only mix |
| | | RoE 13.6% | on undiluted book; ~10% on diluted book |
| | | BVPS +17.5% | includes ₹1,549 cr warrant money |
| | | Credibility +0.93 | conservative guidance; no peer base |
| | | "21.7% remittance share" | company-computed ratio |

### 3.11 Ground-check list (L6 for a bank)
1. **Three branches:** Aluva/Kochi (mature), a 2025–26 metro opening (Mumbai/Bengaluru), a semi-urban TN branch.
   Count counters, gold-loan desk queue, RMs; photograph the SA/TD rate boards and the gold-loan rate card; ask LTV.
2. **Gold-loan price check** (quarterly, fixed basket): FBL vs SBI/Canara/IOB vs Muthoot/Manappuram at 3 PIN codes.
3. **Gold auction notices** in Kerala newspapers (public, dated): count per quarter as a leading stress series.
4. **NRI channel:** two Gulf exchange houses and NRI depositors — FCNR leverage terms (deposit vs loan rate), stickiness after maturity.
5. **RBI data:** BSR state-wise deposits/credit (Kerala share); RBI monthly card statistics (verify 3.13%/1.90%); NPCI
   UPI bank performance; RBI Ombudsman annual complaints by bank.
6. **Fintech partners:** list them (app T&Cs, co-brand card pages), check app status and any RBI direction.
7. **Labour:** AIBEA/AIBOC notices on the 13th bipartite settlement; job-portal reviews for RM targets/attrition.
8. **Subsidiaries:** Fedbank Financial quarterly results (listed); FedServ MCA filings (outsourced ops cost).
9. **Bureau:** CRIF/TransUnion reports for gold, MFI, CV delinquency by lender type.
Each observation must change a number in §3.3–3.7 (rule of the protocol).

### 3.12 Override table (summary; full list in the card)
Open soft flags 9 (FCNR inflation, write-off-driven GNPA, Kerala/NRI concentration, cost drift, gold LTV,
capital + M&A appetite, valuation HOT, fintech dependence, ESOP "one-time") + 2 graded stage-2 flags = **11 open**,
2 adjusted (Q4 one-offs, Q2 treasury), 2 watch (CEO term Sep-2027, ECL Apr-2027). No variant view written.

---

## 4. Stage 5: valuation (bank mode, new)
`python3 tools/valuation/worksheet.py tools/valuation/examples/FEDERALBNK.json` (full output in `FEDERALBNK_worksheet.md`).
Price ₹373.5 (NSE close 20-Nov-2026, Yahoo; screener ₹374; BSE LTP ₹373.00 — three sources). Fully diluted for the
Blackstone warrants: BVPS ₹160.44 → ₹167.06; P/B 2.33x → **2.24x**.

| Output | Value | Reading |
|---|---|---|
| ROE needed forever at CoE 12.5%, g 5% | **21.8%** | vs ~10% today on diluted book, 13.6% reported on undiluted book |
| CoE the market is using if today's ROE is permanent | **7.3%** | the price assumes a big ROE expansion or a very low discount rate |
| Justified P/B on base long-run ROE 14% | 1.20x | |
| IRR the price offers if the base case happens | 10.0% | vs 12% hurdle |
| Scenarios (bear / base / bull; probs 35/45/18 + 2% blow-up) | 5-yr multiples 0.95x / 1.41x / 2.17x | EV 1.36x (6.4%/yr) vs hurdle 1.76x |
| Exit P/B used vs residual-income-consistent P/B at yr 5 | 1.3 vs 0.75; 1.8 vs 1.25; 2.6 vs 1.64 | exit multiple is again the hidden bet (L21) |
| P(≥3x) / P(≤0.5x) / P(blow-up) | 3% / 3% / 2% | base class (non-bank) 44% / 2% / n.a. |
| Temperature | P/B 2.24x = **1.63x own 10-yr median (1.38x) → HOT**; 1.51x peer median (1.48x, 8 mid-size banks) → HOT | P/E 22.1 on normalised diluted EPS vs own median ~11 |
| Book stress | leverage 9.3x; +2% loan loss = −10% of book; +5% = −24% | |
These are practice inputs; the point is that the tool now speaks a bank's language. **Method lesson:** at an Indian
12.5% CoE almost every listed private bank above ~1.6x book "needs" ROE > 17%; the useful outputs are the implied
CoE, the base-case IRR and the own-history P/B band, not "RIM value −50%" (the same conclusion as L21 for P/E names).

## 5. Stage 6: decision card (PRACTICE, no verdict)
`python3 tools/decision/decision_card.py tools/decision/examples/FEDERALBNK_card.json -o …_card.md --calls …_paper_calls.json`

| Gate | Result |
|---|---|
| Stage 2 hard filters | passed (9) |
| Stage 3 PEAD avoid flag | clear (quintile 5) |
| Stage 4 soft flags | **11 open, no variant view → blocks** |
| Outside-view check | P(≥3x) 0.06x base rate → shrink (note) |
| Expected value vs hurdle | **1.36x vs 1.76x → blocks** |
| Rule output | **size 0 (practice; mechanical, no verdict)** |
Paper calls written to `tools/decision/examples/FEDERALBNK_paper_calls.json`, tagged `practice-example`, **not
ingested and not on the scoreboard** (L21).

---

## 6. What broke (and what was fixed)
| # | Stage | What broke | Fix |
|---|---|---|---|
| G1 | 3 | `fetch.py`: banks file only a **cover letter** on NSE ("transcript made available on the Bank's website"); it was flagged "scanned, needs OCR" and its letterhead became junk speaker turns ("Re", "Sub") | **Fixed:** cover-letter detector (whitespace-normalised, curly apostrophes), `skip` flag, turns.py skips them; new `--local PDF@DATE` in fetch.py/run.py adds website copies and replaces the cover letter |
| G2 | 3 | Quarter label: a 16-Oct call was labelled Q1 FY27 (20-day lag rule; banks report in 12–20 days) | **Fixed:** 7-day lag + quarter named in the transcript text wins (`common.quarter_from_text`) |
| G3 | 3 | **No bank measures**; "net interest margin 3.2%" was mapped to the finance-cost rule (false "missed") | **Fixed:** 20 bank measures (NIM, credit cost, GNPA/NNPA, slippage, PCR, C/I, CoD/CoF, yield, CASA, RoA/RoE, CET1/CRAR, CD ratio, loan/deposit/CASA/fee growth); bank rules run before the finance-cost rule; bps parsing; tight 5-bp tolerance for ratios; segment and multi-year-CAGR guards |
| G4 | 3 | **Pre-existing range bug:** "18–20%" / "3.2–3.3%" parsed as (−20, −20) because the dash was read as a minus sign; affected SKIPPER (9 targets, e.g. "20–25%" read as −25%) | **Fixed** in `parse_target`; SKIPPER statuses unchanged on 19-Nov data, but pending targets would have resolved as easy "delivered" |
| G5 | 3 | Chain logic compared floors, so a **raised ceiling on a lower-is-better metric** (C/I 53.5 → 55 → 56) was "same"; "3 years" → "at some point" was not a re-date; tolerance 0.5 pp too wide for bps metrics | **Fixed:** ceilings for lower-better measures, `deadline_dropped`, bank tolerances (2 bps / 25 bps) |
| G6 | 3 | Chain rule marked a **pending** original target "moved-goalpost" before its deadline | **Fixed:** stays pending with `goalpost_flag`; resolve at the original deadline (SKIPPER auto moved-goalposts 12 → 9; human statuses still win) |
| G7 | 3 | Data: screener bank page has no NIM/CASA/credit cost; `nse_fetch.py results` stops at Dec-2024 | **Fixed:** `nse_fetch.py integrated` + `bank_kpis.py` (XBRL: GNPA/NNPA %, CET1, RoA, NII, opex, provisions, diluted EPS; deck KPIs via `--manual`). Note: Q1/Q3 integrated filings carry **no balance sheet** for banks |
| G8 | 3 | Candour heuristic treated "slippages" as an admission word; categories had no bank labels (176 of 412 candidates = "other") | **Fixed** regex; bank categories added to the LLM prompt and `EXEC_CATS` |
| G9 | 3 | PEAD on reported EPS mixes treasury gains, provision buffers and one-offs; consolidated EPS also includes a 60.6%-owned NBFC | **Documented** (protocol v1.3): for lenders also compute SUE on PPOP-less-normal-credit-cost per share as a robustness check before acting on quintiles 1–2 |
| G10 | 3 | Credibility from conservative guidance looks excellent; MCS rewards sandbagging; card prints MCS as a % | **Documented/proposed:** add a "guidance bias" metric (actual − guide midpoint, in bps) and require a bank peer base (CUB, KVB, SIB, CSB, AU) before use |
| G11 | 3 | Management cites "guidance we gave" that is not in any earlier transcript | **Documented:** date promises from first traceable statement |
| G12 | 5 | Worksheet had no bank mode (revenue/EBIT/ROIIC meaningless for lenders) | **Fixed:** `tools/valuation/bank.py` (justified P/B, implied ROE, implied CoE, residual-income scenarios, RIM-consistent exit P/B, twin engine on book, P/B temperature, book stress, CoE×ROE grid), dilution for warrants; `worksheet.py --template --mode bank`; P/E examples unchanged (regression checked) |
| G13 | 6 | Decision card's stage-5 text assumed P/E-mode keys (crashed on bank results) | **Fixed:** `_bank_stage5_lines`; the four existing cards re-render identically except the version line. Remaining: §6 wording still says "exit P/E/DCF" (cosmetic) |
| G14 | 6 | No bank base-rate class (only an all-sector 2020–25 survivor class, bull-biased) | **Proposed:** stage-1 task: 5-yr outcome distribution of Nifty Bank/BSE Bankex members from several start dates, incl. Yes Bank, LVB, PMC-type failures |
| G15 | 2 | v2 hard rules are written for operating companies (fake cash, debtor days); lender checks lived only in `insight:lender-blowup-signals` | **Fixed in protocol v1.3:** a bank stage-2 checklist (divergence, AS-18 connected lending, frauds note, CET1/leverage, funding concentration, quarter-end vs average, ratings) |
| G16 | 2/4 | Basel III Pillar 3 and the bank website are behind a Radware bot wall; the Q2 FY26 transcript could not be fetched | **Documented:** use AR capital/LCR notes + XBRL CET1; fetch website PDFs manually (`--local`) |
| G17 | 4 | Protocol v1.2 had one line for lenders; no unit/cost/disclosure list for banks | **Fixed:** v1.3 bank/NBFC adaptation section |
| G18 | 4 | Data conflicts: transcript "personal loans +32.21%" vs press release "LAP +32.21%"; transcript BVPS "₹266.32" vs ₹166.32; Ind-Ra "FY26 Tier 1 13.9%" vs AR CET1 15.93% (13.89% was Dec-25); Ind-Ra credit cost 67 bp vs company 41 bp (definitions) | **Documented:** company filings > rating rationale > transcript; record definition differences |
| G19 | 4 | pdftotext scrambles multi-series deck charts (yield buckets, retail mix, top-20 concentration) | **Documented:** read the XBRL/press release first; mark chart-derived numbers single-source; next: pdfplumber-free table parse or manual entry |

## 7. What the method taught (for curriculum)
1. **For a bank, the "good" numbers mislead more than the bad ones** (10 good-but-misleading rows vs 6 bad-but-benign).
   The disciplined move is re-deriving growth ex the special window and GNPA ex write-offs.
2. **The cost of equity decides everything again.** At 12.5% the price needs ~22% ROE; the market's implied CoE is ~7%.
   Report implied CoE and the own-history P/B band; treat "RIM value" as a hurdle check (L21 generalises to P/B).
3. **Dilution must be in the denominator before any P/B.** Warrants at ₹227 cut ROE on book by ~1.5–2 pp until deployed.
4. **Credibility needs a sector-adjusted, bias-aware score.** Conservative guidance → A grade; meaningless without peers.
5. **Depth lived in the boring notes again (L13):** Schedule 16 (DICGC, card-network, outsourcing), the PSL-shortfall
   line, the divergence note, the fraud note and the AS-18 table were not mentioned by any analyst on six calls.
