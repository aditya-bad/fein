# Live deep dive #5 — selection rules, written 2026-11-24 16:35 IST BEFORE the frame was built or any in-frame name/ratio was seen

(This folder is renamed to `<TICKER>_selection/` after the draw; the text above the "Hand classification" heading is not edited
after it was written. Its sha256 is recorded in the walk log below the heading.)

Task rule (verbatim from caller): universe = research_notes/Backtests/india_pead_live/universe.csv, India, mcap Rs 1,000-20,000 cr at
latest NSE close. Sector: IT/software services OR NBFC/bank (lenders use protocol's bank/NBFC mode and tools/valuation/bank.py). If
research_notes/Backtests/india_pead_live/industry_map.csv exists use it, else classify by hand and record the list in the prereg before
the draw. Exclude INDRAMEDCO and prior live subjects. Draw: random.Random(20261202) shuffle of alphabetically sorted eligible list;
first name passing stage-2 filters (v3 pledge/solvency/governance), not in the PEAD avoid window, and scoreable. Log all skips.

Seen before writing: the CSV header of universe.csv (`sym,shares`); the live-dd4 prereg and selection_order.json (which list the
pharma/healthcare + IT names that were in the Rs 1,000-20,000 cr band at the 23-Nov-2026 close, but no financial names and no
mcaps); tool code (solvency_screen.py excludes lenders as `financial_alm`). industry_map.csv does NOT exist (checked 16:30 IST).

## Operational definitions (fixed now)
1. **Latest NSE close.** Try NSE bhavcopy `sec_bhavdata_full_24112026.csv`; if it is not published when the frame is built, use
   `sec_bhavdata_full_23112026.csv` (23-Nov-2026 close, cached at scratchpad live_dd3/dl/bhav_23112026.csv). Series EQ/BE/BZ,
   CLOSE_PRICE. Mcap = universe.csv shares x close / 1e7 (Rs cr). Keep 1,000 <= mcap <= 20,000.
2. **Sector (no industry_map.csv -> hand classification, written below BEFORE the shuffle).**
   - First pass: NSE index "Industry" column of ind_niftytotalmarket_list.csv + ind_niftymicrocap250_list.csv (the 23-Nov-2026
     downloads used by live dd3/dd4).
   - **IT/software services:** index Industry = "Information Technology" (kept as classified, as in dd4) plus in-range names with no
     index industry that are clearly IT services, software products, ER&D or BPM/IT-enabled services (hand list).
   - **Lenders (bank/NBFC):** every in-range name with index Industry = "Financial Services" and every in-range name with no index
     industry is hand-classified. Lender = a scheduled commercial bank, small finance bank, or an RBI-registered NBFC/HFC/MFI whose main
     revenue is interest on loans it books (incl. housing, gold, vehicle, MSME, microfinance, infra/project finance, NBFC-ICC lenders).
     NOT lenders (excluded): insurers, AMCs, brokers/margin-funding brokers whose main revenue is broking, exchanges, depositories, RTAs,
     rating agencies, wealth/distribution platforms, payments/fintech platforms without a material own loan book, core investment /
     holding companies, investment companies whose income is mainly dividends/gains, ARCs.
   - Unsure -> excluded, listed with a one-word reason. Each hand list is written verbatim below before the shuffle.
3. **Exclusions:** prior live subjects INDRAMEDCO, SUNFLAG, AUTOAXLES (US-KEX is US; not in universe). Also prior practice/dry-run
   subjects if they appear in the band: CUMMINSIND, VMM, FEDERALBNK (expected out of band).
4. **Draw:** eligible list sorted alphabetically by symbol; order = copy; random.Random(20261202).shuffle(order). Walk in that order.
5. **Skip checks per walked name, in order; first failure = skip (logged with reason):**
   a. **scoreability:** the listed entity is not scheduled to cease to exist before 2027-11-30 (one-year call horizon): no
      sanctioned/pending scheme of amalgamation that dissolves it, no open offer + delisting, no NCLT/IBC admission, no RBI
      supersession/moratorium/scheme of amalgamation (lenders). (A risk to a core asset or licence is NOT a skip; it goes into the tails,
      per live dd4 lesson 7.) Also: an NSE integrated-filing XBRL exists for the latest quarter (so structured calls can resolve).
   b. **governance / fraud-judgment flags:** forensic audit; SEBI/ED/SFIO/RBI action naming the company or promoters for fraud;
      search & seizure with unexplained outcome; rating default or non-cooperation; qualified/adverse audit opinion or mid-term
      statutory-auditor resignation in the last 2 FYs; **lenders also:** an RBI direction restricting core business in force (e.g.
      ban on sanctioning/disbursing a loan product, Section 35A business restrictions), RBI PCA framework in force.
   c. **pledge:** promoter pledge <= 50% of promoter holding (NSE pledge API; SHP XBRL encumbrance fallback). No promoter = pass.
   d. **PEAD avoid window:** latest SUE quintile 1-2 (live_tracker.sue_for on eps_history.csv + fixed sue_cutpoints.json, reported
      EPS for all names incl. lenders) with event within 63 trading days before the frame close date. No EPS history -> the avoid gate
      cannot be cleared -> skip ("unchecked").
   e. **solvency:** non-financials: tools/detectors/solvency_screen.py India grade not red. Lenders (screen returns financial_alm):
      latest disclosed CRAR at or above the regulatory minimum (NBFC/HFC 15%, bank 11.5% incl. CCB, SFB 15%) and no rating
      downgrade to below investment grade in the last 12 months.
   The first name passing a-e is the subject. Names after it are not checked.

## Hand classification (appended after the frame was built, BEFORE the shuffle)
(written 2026-11-24 16:34 IST, after `frame.py` and before `draw.py`; prereg text above this heading had sha256
6056895a903cc45e448d805630ca5a9153d5d1be2a0d785bd7cdde19703e6758 at 16:33 IST)

Frame (23-Nov-2026 close; the 24-Nov bhavcopy returned HTTP 404 at 16:33 IST): 1,547 symbols, all priced; 809 in Rs 1,000-20,000 cr;
482 with no index industry; index "Financial Services" 29; index "Information Technology" 18.

- **IT (index, kept as classified, 18):** AURIONPRO BBOX BSOFT CYIENT DATAMATICS E2E HAPPSTMNDS INTELLECT KPITTECH LATENTVIEW MAPMYINDIA
  MASTEK NEWGEN RATEGAIN SONATSOFTW TANLA ZAGGLE ZENSARTECH
- **IT (hand, no index industry; same judgments as dd4, 18):** 63MOONS ACCELYA ALLDIGI DSSL EMUDHRA EXPLEOSOL HGS INFOBEAN IZMO MPSLTD
  NINSYS NUCLEUS ONEPOINT RAMCOSYS RSYSTEMS SAKSOFT SASKEN SUBEXLTD
- **IT unsure -> excluded:** CYIENTDLM (EMS), DLINKINDIA (hardware dist), KERNEX (rail electronics), MATRIMONY (internet consumer), NELCO
  (satcom), AURUM (proptech), EASEMYTRIP (online travel), YATRA (online travel), NIITMTS (corporate training), TEAMLEASE (staffing),
  PANACHE (IT hardware)
- **Lenders from index "Financial Services" (17):** AAVAS APTUS CANFINHOME CREDITACC CSBBANK DCBBANK EQUITASBNK FEDFINA HOMEFIRST J&KBANK
  KTKBANK PAISALO SAMMAANCAP SBFC SOUTHBANK TMB UJJIVANSFB
- **Index "Financial Services" not lenders (10):** BAJAJHLDNG (holdco) CAMS (RTA) CHOICEIN (broker) IEX (exchange) IIFLCAPS (broker)
  KFINTECH (RTA) RELIGARE (holdco/insurance) SHAREINDIA (broker) UTIAMC (AMC); unsure -> excluded: EDELWEISS (holdco), JMFINANCIL
  (diversified), IFCI (stake holdco vs lender unclear) [EDELWEISS/JMFINANCIL/IFCI counted here: 12 non-lender/unsure total]
- **Lenders (hand, no index industry, 17):** ARMANFIN DHANBANK ESAFSFB FUSION INDOSTAR MASFIN MUFIN MUTHOOTMF PFS PSB REPCOHOME SATIN
  SPANDANA SURYODAY TFCILTD UGROCAP UTKARSHBNK
- **No-industry financials not lenders / unsure -> excluded:** 5PAISA GEOJITFSL PRIMESECU SMCGLOBAL MONARCH (brokers); CARERATING ICRA
  (ratings); PRUDENT (distribution); BFINVEST CONSOFINVT JSWHL KICL PILANIINVS SUMMITSEC NSIL MAHSCOOTER BBTC VHL STEL RANEHOLDIN (holdco/
  investment cos); PNBGILTS (primary dealer); AFSL (broking/NBFC mix, unsure); IBULLSLTD (unsure); TSFINV (unsure, holdco?)
- **Exclusions applied:** none of INDRAMEDCO/SUNFLAG/AUTOAXLES/CUMMINSIND/VMM/FEDERALBNK is in the sector lists (AUTOAXLES and INDRAMEDCO
  are in band but not IT/lender).

## Walk log (written 2026-11-24 ~16:55 IST, after the draw; seed 20261202; frame close 23-Nov-2026)
Eligible = 70 (IT 36 = index 18 + hand 18; lenders 34 = index 17 + hand 17). Order (first 15): KPITTECH, UTKARSHBNK, CYIENT, SATIN,
TANLA, MPSLTD, UJJIVANSFB, PSB, INTELLECT, RAMCOSYS, REPCOHOME, ESAFSFB, SAMMAANCAP, ONEPOINT, PAISALO. Full order in selection_order.json.

| # | Symbol | Mcap Rs cr | Result | Reason |
|---|---|---|---|---|
| 1 | KPITTECH | 14,316.7 | skip (d) | a: only subsidiaries merged INTO KPIT (PathPartner 2025, FMS GmbH 2024); b: no flags in 728 NSE announcements (the 22-Nov-2023 "Change in Auditors" is KPIT UK's auditor, not the listed company's); c: promoter 38.6%, SHP XBRL 30-Sep-2026 encumbrance flags all false. **d: Q2 FY27 SUE -0.81 -> quintile 1, event 28-Oct-2026, inside the 63-TD window (from 21-Aug-2026).** |
| 2 | **UTKARSHBNK** | 2,083.8 | **SUBJECT** | a: the pending NCLT scheme amalgamates the promoter holdco Utkarsh CoreInvest Ltd INTO the bank (bank = transferee; RBI NOC 03-Jan-2025, NSE/BSE no-objection Jul-2025, 2nd-motion petition listed 23-Jul-2026) -> the listed entity survives; Q2 FY27 results filed 03-Nov-2026. b: SEBI settlement order 10-Apr-2024 (Rs 1.24 cr, LODR violations, no fraud finding); FY26 joint auditors' opinion unmodified (09-May-2026); no RBI business restriction found; ratings downgraded twice but investment grade. c: promoter 42.67%, SHP XBRL 30-Sep-2026 encumbrance flags all false. d: Q2 FY27 SUE +1.53 -> quintile 5 (event 03-Nov-2026). e: solvency screen = financial_alm (lender); CRAR 17.0% vs 15% SFB minimum (30-Sep-2026, press release 03-Nov-2026); ICRA A- (Stable) 02-Jul-2026, CARE A- (Stable) 14-Jul-2026 = investment grade. |
Names after UTKARSHBNK were not checked (PEAD quintiles for the next 13 were printed together with the first two by pead.py before the walk;
they did not affect the walk).
