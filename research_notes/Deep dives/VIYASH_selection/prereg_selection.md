# Live deep dive #9 — selection rules, written 2026-11-26 BEFORE the frame was built or any in-frame name/ratio was seen

(This folder is renamed to `<TICKER>_selection/` after the draw; the text above the "Frame and walk log" heading is not edited
after it was written. Its sha256 is recorded in the walk log below that heading.)

Task rule (verbatim from caller): Universe = research_notes/Backtests/india_pead_live/universe.csv joined to industry_map.csv; India;
mcap Rs 1,000-20,000 cr at the latest bhavcopy close (date from the bhavcopy's date column). Sector: `Information Technology` OR
`Healthcare` (exact map values; check). Exclude prior live subjects (SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA, SHK,
UTTAMSUGAR), the 12 promise-forward-test companies and financials. Draw: random.Random(20261206) shuffle of the alphabetically sorted
eligible list; first name passing stage-2 filters (v3), not in the PEAD avoid window, scoreable. Log skips.

Seen before writing (disclosed): the map's sector value counts over the whole map (not by band): Information Technology 86,
Healthcare 113 (of 1,547 mapped rows) — both exact values exist; the header + first row of both csv files; UTTAMSUGAR_selection/
(dd8's prereg, walk log and 149-name eligible list incl. 38 in-band IT names as of the 23-Nov close, and dd8's first-80 order under
seed 20261205); the promise forward-test README's 12 names (4 Healthcare: KRSNAA, ORCHPHARMA, SYNGENE, SHILPAMED). No mcaps, ratios,
PEAD values or filings of any in-frame Healthcare name were looked at. The seed is fixed by the caller, so prior knowledge of names
cannot steer the order.

## Operational definitions (fixed now)
1. **Latest bhavcopy close.** Try NSE `sec_bhavdata_full_DDMMYYYY.csv` for 26-Nov-2026, then 25-Nov, then 24-Nov; use the first that
   returns HTTP 200 with data rows. **Frame close date = the DATE1 column value** (not the file name; L42). Series EQ/BE/BZ,
   CLOSE_PRICE. Mcap = universe.csv shares x close / 1e7 (Rs cr). Keep 1,000 <= mcap <= 20,000. Unpriced symbols dropped (counted).
2. **Sector (no hand classification).** Join on symbol. Keep rows whose industry_map `sector` (stripped) is exactly
   `Information Technology` or `Healthcare`. In-band symbols absent from the map are dropped (counted, listed).
3. **Financials exclusion.** Drop any name whose `sector` or `macro` is `Financial Services`.
4. **Exclusions:** SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA, SHK, UTTAMSUGAR (prior live subjects); the 12 forward-test
   companies JASH, KIRLOSBROS, RISHABH, ANUP, NEOGEN, GALAXYSURF, YASHO, TATVA, KRSNAA, ORCHPHARMA, SYNGENE, SHILPAMED; also
   practice/dry-run subjects CUMMINSIND, VMM, FEDERALBNK, FIVE if present.
5. **Draw:** eligible list sorted alphabetically by symbol; order = copy; random.Random(20261206).shuffle(order). Walk in that order.
6. **Skip checks per walked name, in order; first failure = skip (logged with reason):**
   a. **scoreability:** the listed entity is not scheduled to cease to exist before 2027-11-30: no sanctioned/pending scheme that
      dissolves the listed entity, no open offer + delisting, no NCLT/IBC admission (a scheme where the listed entity survives as
      transferee is not a skip; a threat to a core asset/licence is not a skip, it goes into the tails). Also an NSE integrated-filing
      XBRL exists for the latest quarter (Q2 FY27), so structured calls can resolve.
   b. **governance / fraud-judgment flags (v3 hard):** forensic audit; SEBI/ED/SFIO action naming the company or promoters for fraud;
      search & seizure with unexplained outcome; rating default or INC in the last 2 years; qualified/adverse audit opinion or
      mid-term statutory-auditor resignation in the last 2 FYs.
   c. **pledge:** promoter pledge <= 50% of promoter holding (NSE pledge API; SHP XBRL encumbrance fallback). >25% does not skip
      (graded flag). No promoter = pass.
   d. **PEAD avoid window:** latest SUE quintile 1-2 (tools/backtests/india_pead/live_tracker.py sue_for on eps_history.csv + fixed
      sue_cutpoints.json) with the event within 63 trading days before the frame close date. No EPS history -> skip ("unchecked").
   e. **solvency:** tools/detectors/solvency_screen.py India grade not red.
   The first name passing a-e is the subject. Names after it are not checked.
   A USFDA warning letter / import alert is NOT a skip (it is an operating risk for the tails), unless it meets rule b.

## Frame and walk log
(appended 2026-11-26 ~12:50 IST, after the frame and the draw)
Prereg text above, up to and including the "## Frame and walk log" heading: sha256 882f9b3b3cb05ae2c8ff6488db1d758b32f8d06eff8756ad45b5bc5a6e21d4c4 (written 07:06 UTC = 12:36 IST, before the frame).
Bhavcopy: `sec_bhavdata_full_26112026.csv` -> HTTP 404 (26-Nov in session). `sec_bhavdata_full_25112026.csv` -> HTTP 200, every row DATE1 = 25-Nov-2026
-> **frame close = 25-Nov-2026** (DATE1 column, L42).
Frame: 1,547 universe symbols, 0 unpriced; **806** in Rs 1,000-20,000 cr; 0 in-band names missing from industry_map.csv.
Sector values kept (exact): `Information Technology` 38, `Healthcare` 67; no Financial Services rows. Excluded names present: INDRAMEDCO, KRSNAA,
ORCHPHARMA, SHILPAMED, SYNGENE. **Eligible = 100.** random.Random(20261206).shuffle -> first 15: DCAL, ZOTA, VIYASH, INFOBEAN, SAKAR, DATAMATICS,
CONCORDBIO, WINDLAS, VIJAYA, NATCOPHARM, BBOX, INDOCO, SILVERTUC, METROPOLIS, BLUEJET. Full order and mcaps in selection_order.json.

| # | Symbol | Mcap Rs cr | Result | Reason |
|---|---|---|---|---|
| 1 | DCAL (Dishman Carbogen Amcis) | 1,760 | skip (d) | a: 160 NSE announcements 26-Nov-2024 -> 26-Nov-2026: only an intra-group Swiss step-down merger (listed entity unaffected); Q2 FY27 XBRL filed 13-Nov-2026 -> pass. b: India Ratings downgrade IND A+ -> IND A/Negative (18-Feb-2026) - a downgrade, not default/INC -> pass; "Change in Auditors" 29-Sep-2025 = secretarial-auditor appointment -> pass. c: promoter pledge 7.8 m of 93.0 m shares = 8.4% -> pass. **d: Q2 FY27 SUE -1.94 -> quintile 1, event 13-Nov-2026 (8 trading days before close) -> SKIP (PEAD avoid window).** |
| 2 | ZOTA (Zota Healthcare) | 4,575 | skip (d) | **d: Q2 FY27 SUE -0.75 -> quintile 1, event 28-Oct-2026 (< 63 trading days) -> SKIP.** a-c were not checked one by one before d; any earlier failure would also be a skip, so the subject is unchanged. |
| 3 | **VIYASH** (Viyash Scientific Ltd, formerly SeQuent Scientific; map: Healthcare / Pharmaceuticals & Biotechnology / Pharmaceuticals; BSE 512529) | 9,999 | **SUBJECT** | a: composite scheme (SeQuent + Viyash Life Sciences + Symed Labs) sanctioned by NCLT Hyderabad 18-Nov-2025, record date 08-Dec-2025, name change 09-Jan-2026 - the listed entity is the surviving transferee -> not a skip; no pending scheme/delisting/open offer/IBC in 209 NSE + 224 BSE announcements (26-Nov-2024 -> 26-Nov-2026); Q2 FY27 consolidated integrated XBRL filed 13-Nov-2026. b: no forensic/SEBI/ED/SFIO/search; ratings withdrawn at the company's request (Crisil on Symed 17-Jan-2026; Ind-Ra 22-May-2026) - not INC; XBRL "Declaration of unmodified opinion" in Q4 FY25 and Q4 FY26 filings; no statutory-auditor resignation found -> pass. c: NSE pledge API (SHP 30-Sep-2026): promoter shares pledged 0 of 217.9 m (0.00%); promoter 49.34% (CA Hull Investments / Carlyle group) -> pass. d: Q2 FY27 (event 13-Nov-2026) SUE +3.23 -> quintile 5 -> pass. e: solvency_screen 26-Nov-2026 (FY26 consolidated): grade blank, 0 flags, ICR 6.1x -> pass. |
Names after VIYASH were not checked. **Skips: 2 (DCAL, ZOTA; both PEAD avoid window).**
Rule ambiguity logged: VIYASH's SUE compares the post-merger Q2 FY27 EPS with the pre-merger SeQuent Q2 FY26 EPS (share count 249 m -> 437 m;
different business). The mechanical rule passes it; the comparability problem goes into stage 3 of the dive, not the selection.
