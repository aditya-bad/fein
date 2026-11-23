# Next steps

Last updated: 2026-11-19

## Waiting on the user (asked 2026-11-19)
1. Work / industry / domain they understand from the inside
2. City and what they can physically check (dealers, factories, markets, network)
3. Time horizon, rough capital, separate income
4. Hours per week available
5. Which data access they can give (Screener login, Kite/Trendlyne MCP, transcript API)

## Build plan (after answers) — don't start stock-picking before step 1
1. Personalise the edge thesis in `mission_and_edge.md` around the user's domain.
2. ~~Test direct NSE/BSE filing access~~ DONE 19-Nov-2026 (tools/nse_fetch.py, tools/bse_fetch.py).
3. Build the management promise-vs-delivery tracker (start with 50–100 companies in the
   user's circle of competence; expand quarterly).
4. Change-detection alerts each results season.
5. Decision journal template + quarterly kill-criteria review of `watchlist.md`.

## Memory system TODO
- Add semantic (embedding) search when an API key or local model is available.
- Plan migration of memdb store to external DB/object storage before ~50k records.
- ~~Ask user whether to open a PR~~ User keeps this branch as home; asked them to set it as GitHub default branch (19-Nov-2026). Close PR #1 after.

## Ready to build next (no user input needed)
- Credibility base rates: run promise tracker on 2–3 peers each of Skipper (KEC, Kalpataru, Transrail) and
  Uniparts (Sansera, Happy Forgings) — a score means nothing without peers.
- Fix tools/nse_fetch.py: `transcripts --download` ignores --from/--to.
- Add `supersedes` links for re-dated promises (count goalpost moves automatically).
- Promise tracker v1: schema in research_notes/Knowledge scout Nov 2026/edge_methods_data_access.md;
  pipeline = NSE transcripts → pdftotext → extract promises → memdb `promise` records → score each quarter.
- Text-change ("lazy prices") diff of annual reports/concalls year over year.
- Weekly change detectors: pledge, SAST, insider (PIT), bulk/block, auditor/CFO exits, rating actions.

## Pending implementation
- decision_card.py: add the survival cap (decision:pead-avoid-plus-redflag-survival-cap) after the calibration task lands.
- Pre-register: survival cap for any red-flag firm regardless of earnings (group C showed 2.5× halving risk).

## Dated reminders
- Feb 2027: Q3 FY27 results — re-check all watchlist kill criteria.
