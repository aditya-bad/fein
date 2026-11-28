# Session log

## 2026-11-19 — Session 1
**Asked:** How do people use AI and analysis to pick and trade stocks, A to Z; how
multibaggers (Radico, NVIDIA) were spotted; become "the next Buffett".
**Done:**
- Deep research (6 tracks) → `reports/AI stock picking playbook.md`.
- User pushed back: "if it were this easy everyone would be rich, we're missing something."
  Deep research (5 tracks) on what really separated the winners → `reports/What separated real market winners.md`.
- User: "do you want me to fail?" → Claude: no; edges must be built, survival matters.
- User: "you are my sleeper cell, why should I define everything" → Claude autonomously ran
  4 screening tracks → 13 finalists → `reports/Multibagger idea pipeline.html` (published artifact).
- User: "amateur move — what is our advantage? did I ask for stocks?" → Claude admitted it;
  proposed "Lynch at scale" combined edge; asked 4 profile questions.
- User: build cross-session memory for Claude and a readable one for them → created
  `CLAUDE.md`, `memory/*`, `MY_MEMORY.md`.
**Next:** get the user's answers (next_steps.md), then personalise the edge and build the tracker.
- (later, same session) User asked for memory that scales to millions of records → built `memdb`
  (JSONL store + SQLite FTS5 index), seeded 130 structured records + 406 research passages + 64 metrics.
  Stress test: 1M records written in 145 s; ticker lookup 3 ms; id get 27 ms; full-text 0.4–1 s worst case;
  1M records ≈ 630 MB JSONL (git fine to tens of thousands; move to external DB beyond that).
  Cold-start recall test by a fresh agent: 8/8 correct. Fixed: CLAUDE.md now documents memdb; OR-fallback
  search; memory/*.md indexed; FTS delete perf bug.
  User is sceptical about recall — be transparent: Claude doesn't remember, it retrieves.

## 2026-11-19 — Session 1 (continued): knowledge scout
**Asked:** "Repeat the scout process and get the knowledge; don't wait for approval."
**Done:** opened PR https://github.com/aditya-bad/fein/pull/1 (merge memory to main — user to merge).
Six research agents (hit usage limit once, resumed) produced seed libraries, all ingested to memdb:
India multibaggers (35), global multibaggers (33), blow-ups/frauds (42), sector playbooks (27),
investors + Indian market cycles (64), edge methods + data access (15) + `tools/nse_fetch.py`, `tools/bse_fetch.py`.
memdb now: 100 case studies, 68 insights, 33 strategies, 32 people, 19 sector themes, 656 passages.
**Verified pledges from NSE primary data** → downgraded TRANSRAILL, ROLEXRINGS, HONASA, BIRLACABLE to AVOID.
Lesson: company self-declarations (Transrail Apr-26 "no encumbrance") can be stale — always check exchange data.
**Next:** build promise tracker v1 on NSE transcripts; weekly change detectors; still need user profile answers.

## 2026-11-19/20 — Research round 2
**Asked:** "Are you done with research? What is stopping you?" → not done; limits: usage caps, blocked
sources (YouTube, paywalls, Screener login, India-only IPs), generic knowledge has diminishing returns.
**Launched:** promise-tracker pilots (UNIPARTS done: 68 promises, credibility +0.28; FY25 promoter era
33% hit vs FY26–27 new-CEO era 78%; execution promises −0.08 vs cycle promises +0.53; candour ~5%),
SKIPPER pilot, business-group governance histories, Berkshire/Marks primary sources + Indian base rates.
Hit usage limit again; resumed 20-Nov after reset. Tracker scripts saved in tools/promise_tracker/.
- Round 2 complete (20-Nov-2026): SKIPPER pilot (credibility ~41%, downgraded to WATCHLIST 66→55),
  business-group governance (43 groups + 6 insights), Berkshire/Marks primary sources (29) +
  Indian base rates (13; IIMA factors: momentum ~10.6%/yr, value ~6.5%, size not significant;
  ~42–58% of IPOs below issue; SPIVA 76–79% of active funds lag over 10 yrs).
  memdb: 100 case studies, 116 insights, 75 persons/groups, 136 promises, 784 passages.
**Next:** score 2–3 T&D/auto-component peers for credibility base rates; automate promise pipeline
(fetch → pdftotext → extract → score vs screener); weekly change detectors; still need user profile.
- 20-Nov-2026 (late): usage limit hit (resets ~08:30 UTC). Stopped mid-run, to resume via SendMessage:
  drill set 2 builder (D011–D020, v2 anonymisation), US insider-cluster backtest, literature sweep
  (OpenAlex budget exhausted → switching to Semantic Scholar), VMM "security-guard depth" deep-dive practice.
  Done this stretch: accounting forensics course (25), flags-judgment library (44) + graded pledge rule (L12),
  7 forward paper calls, drill set 1 (excluded, L11), US toolkit (21 + sec_fetch.py).
- 21-Nov-2026: usage limit hit again (resets ~07:20 UTC). Stopped mid-run (resume via SendMessage): India PEAD
  test (was writing analysis script), India insider test (fixing UA throttling), FIVE US deep-dive practice.
  Done this stretch: deep-dive protocol v1 (VMM) + v1.1 (Cummins, L16), US insider backtest (no edge, L14),
  literature sweep (36), drill set 2 (9/10 recognised → drills retired as skill test, L15), paper-call batch 1
  (35; 42 open total), verified NVIDIA CEO resignation event.
- 21-Nov-2026 (afternoon): user made branch default (PR #1 closed); roadmap.md (7 stages) + roadmap rule; List 3 Pi
  security checklist (SSH not needed by Claude); change detectors done (NSE PIT feed empty since 30-Apr-2026);
  paper-call batch 2 (77 open); India PEAD v1 positive OOS (L17); T&D peer credibility (KPIL 77 / Skipper 41 / KEC 20, L18).
  Usage limit hit (resets 17:30 UTC). To resume via SendMessage: PEAD v2 (live tracker), promise-tracker pipeline.
- 22-Nov-2026: stage 5–6 templates (worksheet + decision card, L21); Federal Bank end-to-end dry run (19 gaps,
  14 fixed incl. range-parsing bug; protocol v1.3; bank valuation mode; L22); stage-7 resolver + scoreboard
  (27 tests pass, nothing resolved yet — first due 31-Jan-2027). Still running: US solvency-flags test.

- 24-Nov-2026: deep-dive protocol v1.4 committed (holdco >20% mcap trigger = untested rule of thumb). Pi deployment bundle
  finished (install/healthcheck/uninstall/jobs; dry-run tested, not yet on a real Pi; no inbound ports, no auto-push,
  SB_AUTO_APPLY=0). Pre-registered general survival-cap test PASSED → card v1.3 size cap ≤1%/no additions for Indian
  pledge>25% or ICR<1.5x outside PEAD window (L39). Live deep dive #4 INDRAMEDCO (healthcare draw): size 0 (EV below hurdle);
  expired govt land lease undisclosed in AR; 10 calls ingested with resolver specs (L40). Next: split pledge-vs-ICR rule prereg,
  industry map for the universe, ar_run ZIP fix, card flag for licence/lease risk, live dive #5 (IT or bank/NBFC).
- 24-Nov-2026 (later): live dive #5 UTKARSHBNK (first live lender; card v1.4 size 0, EV 1.29x vs 1.76x hurdle; 11 calls with specs;
  GNPA fall driven by write-offs/ARC sales, CET1 book below price; Bihar MFI Act unmentioned in filings) → L41. Card v1.4 (manual
  core-asset threat trigger, anchoring-lowered-tails warning) and industry map / AR-zip fix in progress (agent still running).
- 24-Nov-2026 (end): industry map 100% (1,547), AR-zip handling (10 tests), card v1.4 (33 tests). Day's net: protocol v1.4, card v1.3→v1.4, Pi bundle, 2 live dives (21 calls), L39–L41.
- 25-Nov-2026: user deferred Pi. Split survival-cap test (pledge vs ICR) rejected — single-flag tails regime-dependent; both-flags group consistently worst (L39 addendum). Card unchanged.
- 25-Nov-2026: BSE fetch window fix; scoreboard bank XBRL path. Live dive #6 HARSHA (Capital Goods draw, no skips; card size 0, EV 1.58x vs 1.76x; 9 calls, 4 auto). L42. Watch: 6/6 live cards size 0.
- 25-Nov-2026: India lender base rates (P≥3x 11%, P≤0.5x 25%, blow-up 27%) → card v1.5; bank.py v1.2 (CET1 book, scenario dilution, J-curve). UTKARSHBNK addendum (calls unchanged).
- 25-Nov-2026: card no-machine audit → partial structural bias (L43); 6 fixes pre-registered, none applied.
- 25-Nov-2026: live dive #7 SHK (Chemicals draw, walk #1; card size 0, EV 1.59x; 9 calls, 5 auto) → L44. 7/7 live cards size 0 (see L43).
- 25-Nov-2026: tool fixes (core EPS, below-net-debt note, card fraction validation, nse_fetch --limit; 126 tests). Live dive #8 UTTAMSUGAR (FMCG-map draw; size 0, EV 0.89x anchored; 10 calls) → L45. Hit 5-hr limit once; resumed.
- 25-Nov-2026: scoring-season dry run: 191 open calls all specced; Jan–Jul 2027: 81 auto / 68 assisted / 4 human; 5 specs fixed; no data gaps; runbook research_notes/Scoreboard/scoring_season_runbook.md. Card-fix prereg amended (tails evaluated on historical panels; card tails final 2031).
- 25-Nov-2026: card-fix historical test (L48): σ too narrow; fix 3 passes, fix 4 fails on lender Brier; v1.6 patch ready. Promise-tracker forward test running (prereg committed).
- 25-Nov-2026: promise forward test cohort 1 — 12 cos (Capital Goods, Chemicals, Healthcare), 38 calls with P_cred vs P_base (L49: under-powered). Total open calls 229. News layer being built.
- 25-Nov-2026: news layer built + first live run (3,852 items, 116 company-named material headlines; flags unverified, listed in research_notes/News/first_run_2026-11-25.md). Pi job added (22:30 IST).
- 26-Nov-2026: news flags verified (22: 6 confirmed, 10 partly, 4 unconfirmed, 2 false/stale; NVIDIA CEO resignation+reinstatement confirmed by 8-Ks) → L50; UTTAMSUGAR price calendar started; addenda on UTTAMSUGAR/UTKARSHBNK dives (calls unchanged); sec_fetch doc fix.
- 26-Nov-2026: macro snapshot tool (16 fields, monthly Pi job); EY–G-sec gap test 2012–21: no OOS power (L51); asked user for pre-2012 Nifty P/E CSV (List 4).
- 26-Nov-2026: wealth-allocation test (L52): 70/20/10 yearly passes (−17pp worst fall, +0.8pp/yr), underweight-SIP passes, P/E tilt not adopted.
- 26-Nov-2026: live dive #9 VIYASH (healthcare draw after 2 PEAD skips; size 0, EV 1.07x; 9 calls; consensus 4 analysts agrees near-term) → L53. 9/9 cards size 0.
- 26-Nov-2026: deep-dive protocol v1.5 (24 mandatory lines from L39–L53) + sector_sensitivity.md (22 sectors).

- 26-Nov-2026: blow-up model test (stage 6): prereg `research_notes/Decision audits/blowup_model_test.md` §A saved 07:30:33 UTC, BEFORE results.json was computed (07:31:18 UTC, single run; both unchanged since WIP commit fcff33f). L2 logistic on flags beats base rate on Brier in India non-fin + US (CITL +0.7/+0.1pp) → ADOPTED; card floor max(anchored, model) beats v1.5 on all 3 panels. Unapplied patch `tools/decision/patches/v1.6b_blowup_model_floor.patch` (after v1.6, post-season). memdb analysis:blowup-model-test-2026-11-26.
- 26-Nov-2026: user paused work (usage at ~60% of 5-hr limit). Promise cohort 2 agent told to pause and write PAUSE_STATE.md; resume it via SendMessage (same agent) later. Nothing else running.

- 26-Nov-2026: user asked for a cloud↔Pi pipeline → comms/ mailbox + CLAUDE.md rule; first task posted to Pi. Pi still being configured by user.

- 28-Nov-2026: comms v2 (one file per message, .ack/.done, watch.sh under Monitor on the Pi, comms.py wait on cloud); CLAUDE.md updated; first task migrated (cloud-20261128-1257-1).

- 28-Nov-2026: gold quick note (5 calls) → full pre-registered gold study (L55), 3 v2 calls; tools/gold/. Antigravity running the same task blind on the Pi for comparison.
- 28-Nov-2026: Antigravity blind gold study compared with ours (L56); its 12m probabilities recorded as a scored forecast.

- 28-Nov-2026: user set up SSH deploy key (write) for the Pi; remote origin=git@github-fein:aditya-bad/fein.git; commits as fein-pi. No Pi push seen yet; task cloud-20261128-1257-1 still unacked (no Pi session started yet).


- 28-Nov-2026 16:36 IST (Pi session): first Pi session live. Watcher running under Monitor. Acked cloud-20261128-1634-2 (ping) + cloud-20261128-1257-1 (setup). Ping replied (pi-20261128-1636-1) and closed. **Pi push via deploy key confirmed working.** Setup task 1257-1 waits for the user to say go.
- 28-Nov-2026: comms pipeline VERIFIED both ways: ping cloud-20261128-1634-2 acked + answered by the Pi in ~2 min (aarch64, agy 1.5.19, node 26.13.1, push via deploy key works). Setup task cloud-20261128-1257-1 acked, waiting for user go-ahead.


- 28-Nov-2026 17:05 IST (Pi): user approved Pi install. Dry run clean, real install OK (10/10 systemd timers, linger on, push switches all 0). Healthcheck: 1 FAIL — NSE corporate-pledgedata returns empty (INDOTECH and unfiltered, both domains), so detect selftest crashes and the nightly pledge feed would be empty. Reported to cloud (pi-20261128-1705-2) with fix asks; re-test Monday. Open: SSH :22 and VNC :5900 listening (user choice). Steps 3-4 (Antigravity) wait on the user confirming telemetry off.

- 28-Nov-2026 ~17:40 IST (Pi): user confirmed agy telemetry off. Antigravity vs pipeline one-call test (SKIPPER Q2FY27 vs hand ledger): pipeline recall 6.5/7, 0 FP; agy 5.5/7, 1 FP, 2 dupes. Verdict: agy = cross-check only (n=1). Both miss confirmations inside analyst questions. research_notes/Promise tracker pilot/antigravity_test_2026-11-28/. Closed 1257-1 and 1655-3 (reply pi-20261128-1715-3).
- 28-Nov-2026: Pi install done (10/10 timers, linger). Healthcheck FAIL = empty NSE pledge feed (fixed selftest/collect handling; endpoint check handed to Pi for Monday; cloud gets 403 from NSE). Antigravity promise test on SKIPPER: recall 5.5/7 vs pipeline 6.5/7 → cross-check only. SSH/VNC listening on Pi = user decision.

