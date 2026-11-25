# Live deep dive #8 — selection rules, written 2026-11-25 BEFORE the frame was built or any in-frame name/ratio was seen

(This folder is renamed to `<TICKER>_selection/` after the draw; the text above the "Frame and walk log" heading is not edited
after it was written. Its sha256 is recorded in the walk log below that heading.)

Task rule (verbatim from caller): Universe = research_notes/Backtests/india_pead_live/universe.csv joined to industry_map.csv; India;
mcap Rs 1,000-20,000 cr at the latest bhavcopy close (date from the bhavcopy's date column). Sector: Information Technology OR Fast
Moving Consumer Goods OR Consumer Durables (state exact map values used; check the map's sector list first). Exclude prior live
subjects (SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA, SHK) and financials. Draw: random.Random(20261205) shuffle of the
alphabetically sorted eligible list; first name passing stage-2 filters (v3), not in the PEAD avoid window, scoreable. Log skips.

Seen before writing (disclosed): the map's sector value counts over the whole map (not by band): Information Technology 86,
Fast Moving Consumer Goods 109, Consumer Durables 90 (of 1,646 mapped rows); the header + first row of both csv files;
SHK_selection/ (dd7's prereg, walk log and its 110-name eligible list, which includes the 38 in-band IT names as of the 23-Nov close,
and dd7's first-15 order under seed 20261204, five of them IT: RSYSTEMS, RAMCOSYS, HAPPSTMNDS, ZENSARTECH, TANLA). No mcaps,
ratios, PEAD values or filings of any FMCG/Consumer Durables name were looked at. The seed is fixed by the caller, so prior
knowledge of names cannot steer the order.

## Operational definitions (fixed now)
1. **Latest bhavcopy close.** Try NSE `sec_bhavdata_full_DDMMYYYY.csv` for 25-Nov-2026, then 24-Nov, then 23-Nov; use the first that
   returns HTTP 200 with data rows. **Frame close date = the DATE1 column value** (not the file name; L42). Series EQ/BE/BZ,
   CLOSE_PRICE. Mcap = universe.csv shares x close / 1e7 (Rs cr). Keep 1,000 <= mcap <= 20,000. Unpriced symbols dropped (counted).
2. **Sector (no hand classification).** Join on symbol. Keep rows whose industry_map `sector` (stripped) is exactly one of
   `Information Technology`, `Fast Moving Consumer Goods`, `Consumer Durables`. Every name with that value is kept as the map
   classifies it. In-band symbols absent from the map are dropped (counted, listed).
3. **Financials exclusion.** Drop any name whose `sector` or `macro` is `Financial Services`.
4. **Exclusions:** SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA, SHK (prior live subjects); also practice/dry-run subjects
   CUMMINSIND, VMM, FEDERALBNK, FIVE if present.
5. **Draw:** eligible list sorted alphabetically by symbol; order = copy; random.Random(20261205).shuffle(order). Walk in that order.
6. **Skip checks per walked name, in order; first failure = skip (logged with reason):**
   a. **scoreability:** the listed entity is not scheduled to cease to exist before 2027-11-30: no sanctioned/pending scheme that
      dissolves the listed entity, no open offer + delisting, no NCLT/IBC admission (a scheme where the listed entity survives as
      transferee is not a skip; a threat to a core asset/licence is not a skip, it goes into the tails). Also an NSE integrated-filing
      XBRL exists for the latest quarter (Q2 FY27, or Q1 FY27 if Q2 not yet due), so structured calls can resolve.
   b. **governance / fraud-judgment flags (v3 hard):** forensic audit; SEBI/ED/SFIO action naming the company or promoters for fraud;
      search & seizure with unexplained outcome; rating default or INC in the last 2 years; qualified/adverse audit opinion or
      mid-term statutory-auditor resignation in the last 2 FYs.
   c. **pledge:** promoter pledge <= 50% of promoter holding (NSE pledge API; SHP XBRL encumbrance fallback). >25% does not skip
      (graded flag). No promoter = pass.
   d. **PEAD avoid window:** latest SUE quintile 1-2 (tools/backtests/india_pead/live_tracker.py sue_for on eps_history.csv + fixed
      sue_cutpoints.json) with the event within 63 trading days before the frame close date. No EPS history -> skip ("unchecked").
   e. **solvency:** tools/detectors/solvency_screen.py India grade not red.
   The first name passing a-e is the subject. Names after it are not checked.

## Frame and walk log (appended 2026-11-25 ~10:50 IST, after the frame and the draw)
Prereg text above this heading: sha256 511f256567089a8a00dc88caea6350bff43a6d74c46ae66cf5f38b66f70e37b0 (written 04:57 UTC = 10:27 IST, before the frame).
Bhavcopy: `sec_bhavdata_full_25112026.csv` -> HTTP 404 (25-Nov in session). `sec_bhavdata_full_24112026.csv` -> HTTP 200, every row
DATE1 = 23-Nov-2026, byte-identical to `sec_bhavdata_full_23112026.csv` -> **frame close = 23-Nov-2026** (DATE1 column, L42).
Frame: 1,547 universe symbols, 0 unpriced; **809** in Rs 1,000-20,000 cr; 0 in-band names missing from industry_map.csv.
Sector values kept (exact): `Information Technology` 38, `Fast Moving Consumer Goods` 53, `Consumer Durables` 58; no Financial Services
rows; no excluded subject present. **Eligible = 149.** random.Random(20261205).shuffle -> first 15: UTTAMSUGAR, INFOBEAN, DOMS, BSOFT,
WHIRLPOOL, BOROLTD, REDTAPE, BOSCH-HCIL, SILVERTUC, BBTC, SIRCA, SONATSOFTW, RENUKA, PARAGMILK, SHAILY. Full order and mcaps in
selection_order.json.

| # | Symbol | Mcap Rs cr | Result | Reason |
|---|---|---|---|---|
| 1 | **UTTAMSUGAR** (Uttam Sugar Mills; map: Fast Moving Consumer Goods / Agricultural Food & other Products) | 1,329.1 | **SUBJECT** | a: no scheme/delisting/open offer/NCLT in 100 NSE (25-Nov-2024 -> 25-Nov-2026, four 6-month windows, union 100) + 118 BSE (scrip 532729) announcements; Q2 FY27 consolidated integrated XBRL filed 31-Oct-2026. Corporate actions: preference-share redemption tranches; subsidiary UDL distillery 40 -> 160 KLPD (Rs 110 cr, by Mar-2027); corporate-office building bought (25-Sep-2026). b: no forensic/SEBI/ED/INC; ratings *upgraded* (CARE A- -> A Stable 17-Sep-2025; India Ratings A- -> A Stable 10-Jun-2026); B.K. Kapur & Co. unmodified FY26 opinion **with an Emphasis of Matter** (interest on a State of Uttarakhand loan not provided) - not a skip, goes to S2/L40; CFO resigned 15/16-Sep-2026 "personal reasons", replaced 18-Sep-2026 (graded, card). c: pledge API 0 rows; SHP XBRL 30-Sep-2026 all promoter encumbrance flags false; promoter 74.71%. d: Q2 FY27 (event 31-Oct-2026) SUE +0.28 -> quintile 3; Q1 FY27 -1.15 -> Q1 (10-Aug-2026, superseded by the later event; latest quintile governs). e: solvency_screen 25-Nov-2026 grade blank (not red), 1 flag S3: ST borrowings 675 > cash 17 + 0.5 x CFO 270 (FY26; seasonal sugar-inventory working-capital debt); ICR 3.6x. |
Names after UTTAMSUGAR were not checked. **Skips: none.**
Rule ambiguity logged: (d) reads "latest SUE quintile"; the prior quarter (Q1 FY27, quintile 1, event 10-Aug-2026) is ~70 trading days (75 weekdays less exchange holidays) before the
23-Nov close, outside the 63-day window anyway, so the reading does not change the result.
