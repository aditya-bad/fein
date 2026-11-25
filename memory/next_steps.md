# Next steps

Last updated: 2026-11-24

## Waiting on the user
- ~~Q1–4 (work, city, horizon/capital, hours)~~ superseded 20-Nov-2026: user said capital/job don't matter; proceed without.
- Infra (user will provide later, see `My Requirements/requirements.md` List 2): Raspberry Pi + Remote Control,
  own read-only Kite MCP wrapper, Screener.in credentials (stored on Pi only).

- **25-Nov-2026: user deferred the Pi setup** ("will take a bit more time"); proceed with non-Pi work; remind before late-Jan 2027 results season.

## In flight (25-Nov-2026)
- ~~Lender base rates + bank.py CET1 book~~ DONE 25-Nov (card v1.5, bank.py v1.2).
- ~~BSE pagination + resolver bank XBRL~~ DONE 25-Nov (3 UTKARSHBNK calls now auto; 59 structured / 38 assisted of 163 open).
- ~~Pledge-vs-ICR split test~~ DONE 25-Nov: rejected (L39 addendum). Follow-up: pre-register "both flags → 0 new money" on fresh 2026+ events (collect events from Q3 FY27 onward).

## Done 24-Nov-2026
- ~~Pi bundle, live dive #4, survival-cap test~~ DONE 24-Nov (see session_log).
- Next queue: ~~(1) industry map~~ DONE 24-Nov (1547/1547, BSE+screener; NSE industryInfo 403); ~~(2) AR zip fix~~ DONE;
  ~~(3) card v1.4 core-asset threat + anchoring warning~~ DONE (India-only for now; decide whether US cards apply it);
  (4) prereg split rule pledge vs ICR (L39); ~~(5) live dive #5~~ DONE (UTKARSHBNK).
- From L41: ~~lender class, cet1_book, bank XBRL, bse_fetch~~ DONE 25-Nov. Still open: prereg test of insight:lender-blowup-signals;
  US lender base-rate class; card input validation (credibility as fraction, L42); extend core-asset threat to US cards.
- Live dives: next #7 (Chemicals or IT draw), keep ~1–2/week. Watch 6/6 size-0 pattern (strategy_review §4).
- Deep-dive protocol v1.4 committed; ">20% of mcap" holdco trigger is an untested rule of thumb (insight:holdco-stake-20pct-trigger).

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
- ~~decision_card.py: add the survival cap~~ DONE 23-Nov (card v1.2: survival cap + tail anchoring to base rates, 20 tests).
- ~~Pre-register: survival cap for any red-flag firm~~ DONE 24-Nov: adopted as size cap (card v1.3, L39). Follow-up: pre-register split rule (pledge stricter than interest cover).

## Dated reminders
- Feb 2027: Q3 FY27 results — re-check all watchlist kill criteria.
