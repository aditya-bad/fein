# Live deep dive #6 — selection rules, written 2026-11-25 09:37 IST BEFORE the frame was built or any in-frame name/ratio was seen

(This folder is renamed to `<TICKER>_selection/` after the draw; the text above the "Frame and walk log" heading is not edited
after it was written. Its sha256 is recorded in the walk log below that heading.)

Task rule (verbatim from caller): Universe = research_notes/Backtests/india_pead_live/universe.csv joined to
research_notes/Backtests/india_pead_live/industry_map.csv, India, mcap Rs 1,000-20,000 cr at the latest available NSE bhavcopy close.
Sector: one of IT/software services, Chemicals, or Capital Goods (by the map's sector column; state the exact values). Exclude prior
live subjects (SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK) and financials. Draw: random.Random(20261203) shuffle of the alphabetically
sorted eligible list; first name passing stage-2 filters (v3 pledge/solvency/governance), not in the PEAD avoid window, and scoreable.
Log all skips with reasons.

Seen before writing: the header and first two rows of industry_map.csv; the count of rows per `sector` value over the WHOLE map
(Capital Goods 241, Financial Services 166, Chemicals 127, Information Technology 86, ...) — no per-name mcaps or in-band lists;
the dd5 selection files (which list IT names in the 23-Nov band, but no Chemicals/Capital Goods names); tool code.

## Operational definitions (fixed now)
1. **Latest available NSE close.** NSE bhavcopy `sec_bhavdata_full_24112026.csv` (24-Nov-2026 close; 25-Nov is a trading day still
   in session at writing). If 24-Nov returns 404, fall back to 23-Nov (cached). Series EQ/BE/BZ, CLOSE_PRICE.
   Mcap = universe.csv shares x close / 1e7 (Rs cr). Keep 1,000 <= mcap <= 20,000. Unpriced symbols are dropped (counted).
2. **Sector (no hand classification).** Join on `symbol`. Keep rows whose industry_map `sector` (stripped) is exactly one of:
   `Information Technology`, `Chemicals`, `Capital Goods`. Every name with that sector value is kept as the map classifies it
   (incl. any IT-hardware or EMS names the map puts there). Symbols absent from the map are dropped (counted, listed).
3. **Financials exclusion.** Drop any name whose `sector` or `macro` is `Financial Services` (none expected given rule 2).
4. **Exclusions:** SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK (prior live subjects); also practice/dry-run subjects CUMMINSIND, VMM,
   FEDERALBNK if present.
5. **Draw:** eligible list sorted alphabetically by symbol; order = copy; random.Random(20261203).shuffle(order). Walk in that order.
6. **Skip checks per walked name, in order; first failure = skip (logged with reason):**
   a. **scoreability:** the listed entity is not scheduled to cease to exist before 2027-11-30 (one-year call horizon): no
      sanctioned/pending scheme of amalgamation/arrangement that dissolves the listed entity, no open offer + delisting, no NCLT/IBC
      admission. (A risk to a core asset, licence or lease is NOT a skip; it goes into the tails — dd4 lesson 7.) Also: an NSE
      integrated-filing XBRL exists for the latest quarter (so structured calls can resolve).
   b. **governance / fraud-judgment flags:** forensic audit; SEBI/ED/SFIO action naming the company or promoters for fraud;
      search & seizure with unexplained outcome; rating default or non-cooperation (INC) in the last 2 years; qualified/adverse
      audit opinion or mid-term statutory-auditor resignation in the last 2 FYs.
   c. **pledge:** promoter pledge <= 50% of promoter holding (NSE pledge API; SHP XBRL encumbrance fallback). >25% does not skip
      (it is a graded flag for the card). No promoter = pass.
   d. **PEAD avoid window:** latest SUE quintile 1-2 (live_tracker.sue_for on eps_history.csv + fixed sue_cutpoints.json) with the
      event within 63 trading days before the frame close date. No EPS history -> the avoid gate cannot be cleared -> skip
      ("unchecked").
   e. **solvency:** tools/detectors/solvency_screen.py India grade not red.
   The first name passing a-e is the subject. Names after it are not checked.

## Frame and walk log (appended 2026-11-25 ~10:00 IST, after the frame and the draw)
Prereg text above this heading: sha256 47b2b58eaa0a95cea55b50787d432795b71efe97d1c318ccb30474f9c439deaa (09:37 IST, before `frame.py`).
Bhavcopy: `sec_bhavdata_full_24112026.csv` returned HTTP 200 but every row has DATE1 = 23-Nov-2026 and the file is byte-identical to
`sec_bhavdata_full_23112026.csv` (24-Nov-2026 was not a trading day) -> frame close = **23-Nov-2026** (rule 1 fallback, same data).
Frame: 1,547 universe symbols, 0 unpriced; **809** in Rs 1,000-20,000 cr; 0 in-band names missing from industry_map.csv.
Sector values kept (exact): `Capital Goods` 153, `Chemicals` 72, `Information Technology` 38; no Financial Services rows among them.
Exclusions applied: SUNFLAG (Capital Goods, in band) removed; AUTOAXLES/INDRAMEDCO/UTKARSHBNK not in these sectors. **Eligible = 262**
(Capital Goods 152, Chemicals 72, IT 38). random.Random(20261203).shuffle -> first 15: HARSHA, HPL, RATEGAIN, GHCL, DEEPAKFERT, BAJEL,
JINDALSAW, IZMO, MODISONLTD, EXPLEOSOL, HARIOMPIPE, APOLLO, HEGAM, GNFC, PRINCEPIPE. Full order in selection_order.json.

| # | Symbol | Mcap Rs cr | Result | Reason |
|---|---|---|---|---|
| 1 | **HARSHA** | 3,989.8 | **SUBJECT** | a: only past scheme = WOS Harsha Engineers B.V. merged INTO HARSHA (effective 02-Dec-2022); nothing pending in 290 NSE + 160 BSE announcements; Q2 FY27 integrated XBRL filed 03-Nov-2026. b: no fraud/forensic/INC flags; "Change in Auditors" 23-Jul-2026 = statutory auditor's term completed + new 5-year appointment (rotation); 12-Sep-2025 = secretarial auditor appointment; FY26 opinions unmodified; CARE AA-/A1+ (13-Mar-2024). c: promoter 75.00%, SHP XBRL 30-Sep-2026 encumbrance flags all false (pledge API 0 rows). d: Q2 FY27 SUE +1.81 -> quintile 5 (event 03-Nov-2026); Q1 FY27 SUE -0.10 -> Q2 but event 11-Aug-2026 is before the window start 21-Aug-2026. e: solvency_screen grade blank (not red), 2 flags (short-term debt > cash + 0.5 CFO; dividends > FCF while debt rose). |
Names after HARSHA were not checked (PEAD for HPL/RATEGAIN/GHCL was printed in the same pead.py call as HARSHA; it did not affect the walk).
