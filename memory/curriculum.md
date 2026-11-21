# Curriculum and learning loop (the engine of "never stop")

Last updated: 2026-11-20. Every session/cycle: pick the top unfinished items, do them, ingest to memdb,
update this file, log in session_log.md, commit and push. Respect usage limits: ≤4 parallel agents,
save in stages.

## The loop (each cycle)
1. **Learn** — 1–2 items from the Knowledge backlog.
2. **Drill** — run blind drills (self-teaching) and score them.
3. **Track** — advance a method (promise tracker, change detectors, text diffs) on real filings.
4. **Distil** — fold what was learned into the thinking system (playbook/checklists), with record ids.
5. **Calibrate** — update the scoreboard below. Be honest; bad scores are information.

## Self-teaching: blind drills (how we "teach ourselves to pick" without hindsight)
- A packet-builder agent assembles point-in-time data for a real past situation (financials only up to
  date T, filings/concalls before T, industry context then), **anonymised** (name, ticker, brands, exact
  places removed; numbers kept), with the outcome sealed in a separate file.
- A different analyst agent, seeing only the packet, writes: thesis, variant view, red flags, valuation,
  and **probabilities** (P(>3x in 5y), P(<−50%), P(fraud/blow-up)), plus a decision (own/avoid/watch).
- Unseal → score with Brier score and log-loss; record what was missed. Store packets in
  `drills/packets/`, sealed outcomes in `drills/sealed/`, results as memdb `analysis` records tag `drill`.
- Contamination check: analyst must state if it recognises the company; recognised drills are excluded.
- **v2 anonymisation (after set 1 failed — 10/10 recognised, L11):** generic sector words only; all money ×
  hidden factor (0.3–3); fiscal years shifted; no listing venue, subsidiaries, foreign brands, group events;
  obscure micro/small caps; packet builder runs a "could I identify this?" self-check and rejects if yes.
- Mix: ~1/3 later multibaggers, ~1/3 frauds/blow-ups, ~1/3 ordinary/mediocre (base-rate realistic).

## Forward paper calls (live, out-of-sample)
Method-driven predictions on current companies (e.g., "credibility score < X ⇒ guidance miss next qtr"),
dated, with probabilities, scored when the outcome arrives. Stored as memdb `thesis` tag `paper-call`.
These are tests of methods, not recommendations.

## Gate to phase B (bring the user ideas)
All of: ≥50 forward paper calls resolved with Brier clearly better than a naive base-rate forecaster (the only clean test — L11, L15); ≥30 forward
paper calls resolved with positive skill; promise-tracker signal shown to predict something on ≥20
companies; written post-mortems on misses. Until then: no idea-pitching (except "great stock spotted" notes).

## Scoreboard
| Date | Drills scored | Brier (ours) | Brier (base rate) | Paper calls resolved | Notes |
|---|---|---|---|---|---|
| 2026-11-20 | 0 | – | – | 0 | loop started |
| 2026-11-20 | paper calls: 7 opened (promise tracker, resolve Feb–May 2027) | | | 0 | |
| 2026-11-21 | set 2: 1 of 10 usable (9 recognised); D017 Brier 0.170 vs base 0.230 | 0.170 | 0.230 | 0 | historical drills retired as skill test (L15) |
| 2026-11-20 | set 1: 0 of 10 usable (all recognised) | – | – | 0 | method fixed → v2 anonymisation; forward calls prioritised |

## Forward paper calls = main skill engine (L15)
Target: 20–40 new dated calls each results season across India and US (guidance delivery, margin direction,
capex commissioning, pledge changes, rating actions, earnings vs consensus). Cheap, many, scored.

## Open paper calls
`python3 -m memdb search "" --tag paper-call` — resolve each after Q3/Q4 FY27 results; record outcome + Brier.

## Knowledge backlog (top = next)
0a. **False alarms vs real traps:** cases where our red flags fired but the stock compounded (high P/E,
    negative FCF, high debtor days, pledges, dilution) and where green flags hid disasters — learn the
    distinguishing context. (agent started 20-Nov)
0b. Deep-dive protocol — v1 DONE 21-Nov (VMM practice). Next: practise it on a manufacturer and a US company.
0c. **Academic literature sweep** via OpenAlex/Semantic Scholar (free APIs): top-cited papers on
    anomalies, analyst behaviour, management signals, India-specific market studies.
0d. **Blogs / long-form practitioners:** Valuepickr threads, Marcellus, Safal Niveshak, Fundoo Professor,
    Abhay Lodha, Neckar, Mauboussin, Damodaran, Cliff Asness, Investor letters (Fundsmith, Nalanda?).
0e. **YouTube/podcasts** — blocked until transcript access (see My Requirements).
1. Blind drill packets set 1 (India + US) — packet builder running 20-Nov.
2. ~~Back-test US insider clusters~~ DONE 21-Nov: no edge vs matched controls (L14). Next: pre-registered opportunistic-insider rule; India PIT version.
4. Valuation craft: reverse DCF practice, sector multiples history, when cheap stays cheap.
5. Capital allocation scorecards (buybacks, M&A, dilution) — India & US examples.
6. Behavioural finance applied: our own bias checklist; pre-mortem templates.
7. Macro → markets transmission: rates, liquidity, FX, commodity cycles (India & US).
8. Books distilled from primary text where legally accessible (public letters, memos, speeches, papers).
9. YouTube/podcast learning — blocked until a transcript API key is provided.
10. Promise tracker automation + peer base rates (method calibration, not picks).
11. "Lazy prices" text-change detector on Indian annual reports.

## Market weighting
India slightly > US; both always in scope.

## Done
- 20 Nov 2026: Accounting forensics course (7 lessons, exercises, 30-min first-read protocol + scoring template; 25 records). TODO: log every scored company and check outcomes in 2–3 yrs to calibrate thresholds.
- 20 Nov 2026: US toolkit — tools/sec_fetch.py (EDGAR facts/filings/full-text/Form 4/13F), US base rates & SEC red flags (21 records).
- 19–20 Nov 2026: playbook, winners' edges, 100 case studies, 19 sectors, 75 investors/groups, cycles,
  frauds, primary sources, base rates, NSE/BSE tools, promise tracker pilots (2).
