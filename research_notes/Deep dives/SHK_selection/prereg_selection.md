# Live deep dive #7 — selection rules, written 2026-11-25 10:10 IST BEFORE the frame was built or any in-frame name/ratio was seen

(This folder is renamed to `<TICKER>_selection/` after the draw; the text above the "Frame and walk log" heading is not edited
after it was written. Its sha256 is recorded in the walk log below that heading.)

Task rule (verbatim from caller): Universe = research_notes/Backtests/india_pead_live/universe.csv joined to industry_map.csv (same
folder); India; mcap Rs 1,000-20,000 cr at the latest bhavcopy close (take the date from the bhavcopy's date column, L42). Sector:
Chemicals OR Information Technology (exact map values: `Chemicals`, `Information Technology`). Exclude prior live subjects (SUNFLAG,
AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA) and financials. Draw: random.Random(20261204) shuffle of the alphabetically sorted eligible
list; first name passing stage-2 filters (v3), not in the PEAD avoid window, and scoreable. Log all skips.

Seen before writing (disclosed): the header and first row of industry_map.csv and universe.csv; HARSHA_selection/ (dd6's
prereg, its walk log and the first ~110 alphabetical names of dd6's 262-name eligible list, which mixes Capital Goods, Chemicals and
IT names in the 23-Nov band, and dd6's first-15 shuffle order under seed 20261203: HARSHA, HPL, RATEGAIN, GHCL, DEEPAKFERT, BAJEL,
JINDALSAW, IZMO, MODISONLTD, EXPLEOSOL, HARIOMPIPE, APOLLO, HEGAM, GNFC, PRINCEPIPE). No mcaps, ratios or filings of any name were looked
at. The seed is fixed by the caller, so prior knowledge of names cannot steer the order.

## Operational definitions (fixed now)
1. **Latest bhavcopy close.** Try NSE `sec_bhavdata_full_DDMMYYYY.csv` for 25-Nov-2026, then 24-Nov, then 23-Nov; use the first that
   returns HTTP 200 with data rows. **Frame close date = the DATE1 column value** (not the file name; L42). 25-Nov is in session at
   writing, so a 25-Nov file is not expected. Series EQ/BE/BZ, CLOSE_PRICE. Mcap = universe.csv shares x close / 1e7 (Rs cr).
   Keep 1,000 <= mcap <= 20,000. Unpriced symbols are dropped (counted).
2. **Sector (no hand classification).** Join on `symbol`. Keep rows whose industry_map `sector` (stripped) is exactly `Chemicals` or
   `Information Technology`. Every name with that value is kept as the map classifies it (incl. agro-chemicals, fertiliser, IT-hardware
   names if the map puts them there). In-band symbols absent from the map are dropped (counted, listed).
3. **Financials exclusion.** Drop any name whose `sector` or `macro` is `Financial Services` (none expected given rule 2).
4. **Exclusions:** SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA (prior live subjects); also practice/dry-run subjects CUMMINSIND,
   VMM, FEDERALBNK if present.
5. **Draw:** eligible list sorted alphabetically by symbol; order = copy; random.Random(20261204).shuffle(order). Walk in that order.
6. **Skip checks per walked name, in order; first failure = skip (logged with reason):**
   a. **scoreability:** the listed entity is not scheduled to cease to exist before 2027-11-30 (one-year call horizon): no
      sanctioned/pending scheme of amalgamation/arrangement that dissolves the listed entity, no open offer + delisting, no NCLT/IBC
      admission. (A risk to a core asset, licence or lease is NOT a skip; it goes into the tails.) A scheme in which the listed entity is
      the surviving transferee is not a skip. Also: an NSE integrated-filing XBRL exists for the latest quarter (Q2 FY27, or Q1 FY27 if
      Q2 is not yet due), so structured calls can resolve.
   b. **governance / fraud-judgment flags:** forensic audit; SEBI/ED/SFIO action naming the company or promoters for fraud;
      search & seizure with unexplained outcome; rating default or non-cooperation (INC) in the last 2 years; qualified/adverse
      audit opinion or mid-term statutory-auditor resignation in the last 2 FYs.
   c. **pledge:** promoter pledge <= 50% of promoter holding (NSE pledge API; SHP XBRL encumbrance fallback). >25% does not skip
      (graded flag for the card). No promoter = pass.
   d. **PEAD avoid window:** latest SUE quintile 1-2 (tools/backtests/india_pead/live_tracker.py sue_for on eps_history.csv + fixed
      sue_cutpoints.json) with the event within 63 trading days before the frame close date. No EPS history -> the avoid gate cannot be
      cleared -> skip ("unchecked").
   e. **solvency:** tools/detectors/solvency_screen.py India grade not red.
   The first name passing a-e is the subject. Names after it are not checked.

## Frame and walk log (appended 2026-11-25 ~10:25 IST, after the frame and the draw)
Prereg text above this heading: sha256 25927bb950aeee2df728e66110946571a4fd5fbc48de5ceb0c5a9822bad0351a (10:10 IST, before the frame).
Bhavcopy: `sec_bhavdata_full_25112026.csv` -> HTTP 404 (25-Nov in session). `sec_bhavdata_full_24112026.csv` -> HTTP 200, every row
DATE1 = 23-Nov-2026, byte-identical to `sec_bhavdata_full_23112026.csv` -> **frame close = 23-Nov-2026** (DATE1 column, L42).
Frame: 1,547 universe symbols, 0 unpriced; **809** in Rs 1,000-20,000 cr; 0 in-band names missing from industry_map.csv.
Sector values kept (exact): `Chemicals` 72, `Information Technology` 38; no Financial Services rows; no excluded subject in these sectors
(HARSHA is Capital Goods). **Eligible = 110.** random.Random(20261204).shuffle -> first 15: SHK, SWANCORP, GALAXYSURF, DHANUKA, RSYSTEMS,
TATACHEM, RAMCOSYS, RCF, HAPPSTMNDS, ZENSARTECH, IPL, FINEORG, TANLA, LXCHEM, NEOGEN. Full order and mcaps in selection_order.json.

| # | Symbol | Mcap Rs cr | Result | Reason |
|---|---|---|---|---|
| 1 | **SHK** (S H Kelkar & Co; map: Chemicals / Specialty Chemicals) | 1,765.3 | **SUBJECT** | a: no scheme/delisting/open offer/NCLT in 178 NSE (25-Nov-2024 -> 25-Nov-2026) + 188 BSE (scrip 539450, two <=1-yr windows) announcements; restructurings are subsidiary-level (Keva Ventures WOS divested 28-Jul-2026; 17% CFF Keva Italy stake sold to Keva Italy Srl 13-Mar-2026); Q2 FY27 consolidated integrated XBRL filed 02-Nov-2026. b: no fraud/forensic/INC; exchange *cautionary* letters 27-Oct-2026 for late intimation of an analyst meet (03-Mar-2025) = procedural, not a skip; Deloitte Haskins & Sells unmodified FY25 + FY26 and "will complete their term" at the 70th AGM (31-Jul-2026), BSR & Co appointed 5 yrs = rotation; CRISIL AA- reaffirmed 28-Sep-2026, outlook **Stable -> Negative** (graded, card). c: pledge API 0 rows; SHP XBRL 30-Sep-2026: promoter 75,945,564 sh (54.87%), pledged 6,300,000 = **8.3% of promoter holding** (<= 50%: pass; < 25%: not a graded flag). d: Q2 FY27 SUE +0.08 -> quintile 3 (event 02-Nov-2026); Q1 FY27 +0.26 -> Q3. e: solvency_screen 25-Nov-2026 grade blank (not red), 2 flags: interest cover 2.29x (EBIT 128 / interest 56, FY26); ST borrowings 639 > cash 65 + 0.5 x CFO 263. |
Names after SHK were not checked (PEAD for SWANCORP..ZENSARTECH was printed in the same pead.py call as SHK; it did not affect the walk).
**Skips: none.**
