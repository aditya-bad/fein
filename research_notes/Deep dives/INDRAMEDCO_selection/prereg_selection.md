# Live deep dive #4 — selection rules, written 2026-11-24 16:15 IST BEFORE the frame was built or any in-frame name/ratio was seen

Task rule (verbatim from caller): universe = research_notes/Backtests/india_pead_live/universe.csv, India, market cap Rs 1,000-20,000 cr
at latest NSE close; sector type not yet covered by live dives: restrict to pharma/healthcare OR IT/software services (NSE industry
classification), non-financial. Draw with random.Random(20261201) over the alphabetically sorted eligible list; first company passing
stage-2 filters (v3: pledge, solvency, governance) AND scoreability is the subject. Log every skip with its reason.

(Seen before writing: only the column headers of universe.csv and of the NSE index lists, and the count of index constituents per
industry. No in-frame name, market cap or ratio.)

Operational definitions (fixed now):
1. Latest NSE close = bhavcopy sec_bhavdata_full_23112026.csv (23-Nov-2026 close; the 24-Nov file is not published at 16:15 IST),
   series EQ/BE/BZ, CLOSE_PRICE. Mcap = universe.csv shares x close / 1e7 (Rs cr). Keep 1,000 <= mcap <= 20,000.
2. Sector = NSE index "Industry" (macro-sector) column of ind_niftytotalmarket_list.csv + ind_niftymicrocap250_list.csv (same files
   as live dd3, downloaded 23-Nov-2026). Keep Industry in {"Healthcare", "Information Technology"}. These macro-sectors are
   non-financial by construction.
   In-range names with no index industry: classified by hand from the company name/known business, each listed verbatim in the log
   with its class BEFORE the shuffle; included only if clearly pharma/healthcare (drugs, API, CDMO, hospitals, diagnostics, devices)
   or IT/software services (IT services, software products, ER&D, BPM/IT-enabled). Unsure -> excluded (logged).
3. Eligible list sorted alphabetically by symbol; order = list copy, random.Random(20261201).shuffle(order). Walk in that order.
4. Skip checks per walked name, first failure = skip (logged with reason):
   a. scoreability: listed entity not scheduled to cease to exist before 2027-11-30 (one-year call horizon): sanctioned/pending
      scheme dissolving it, open offer + delisting, NCLT/IBC (NSE+BSE announcements)
   b. governance / fraud-judgment flags: forensic audit, SEBI/ED/SFIO action naming the company or promoters for fraud, search &
      seizure with unexplained outcome, rating default/non-cooperation; qualified/adverse audit opinion or mid-term statutory
      auditor resignation in the last 2 FYs
   c. promoter pledge <= 50% of promoter holding (NSE pledge API; SHP XBRL encumbrance fallback)
   d. PEAD avoid window: latest SUE quintile 1-2 (live_tracker.sue_for + fixed sue_cutpoints.json) with event within 63 trading days
      before 23-Nov-2026 (protocol S0 skip check)
   e. solvency screen (tools/detectors/solvency_screen.py) India grade not red
   The first name passing a-e is the subject. Names after it are not checked.

## Hand classification of in-range names without an index industry (written 2026-11-24 ~16:25 IST, before the shuffle)
482 in-range names lack an index industry. Classified from name/known business:
- Healthcare (40): AARTIDRUGS ALIVUS APLLTD ARTEMISMED ASTRAZEN BAFNAPH BAJAJHCARE BLISSGVS DCAL FDC GUFICBIO HESTERBIO HIKAL INDOCO INDRAMEDCO INDSWFTLAB INNOVACAP IOLCP JAGSNPHARM KOPRAN KRSNAA LINCOLN MOREPENLAB NGLFINE ORCHPHARMA PANACEABIO RPGLIFE SAKAR SANOFI SHALBY SIGACHI SMSPHARMA SOLARA SYNCOMF TARSONS UNICHEMLAB VENUSREM VIMTALABS WINDLAS ZOTA
- IT / software services (18): 63MOONS ACCELYA ALLDIGI DSSL EMUDHRA EXPLEOSOL HGS INFOBEAN IZMO MPSLTD NINSYS NUCLEUS ONEPOINT RAMCOSYS RSYSTEMS SAKSOFT SASKEN SUBEXLTD
- Unsure -> excluded: ALEMBICLTD (holdco/realty), TTKHLTCARE (diversified consumer), AMRUTANJAN (OTC/FMCG), CYIENTDLM (EMS), DLINKINDIA (hardware distribution), KERNEX (rail electronics), MATRIMONY (internet consumer), NELCO (satcom), AURUM (proptech), RPSGVENT (holdco)
