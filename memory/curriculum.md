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
- Mix: ~1/3 later multibaggers, ~1/3 frauds/blow-ups, ~1/3 ordinary/mediocre (base-rate realistic).

## Forward paper calls (live, out-of-sample)
Method-driven predictions on current companies (e.g., "credibility score < X ⇒ guidance miss next qtr"),
dated, with probabilities, scored when the outcome arrives. Stored as memdb `thesis` tag `paper-call`.
These are tests of methods, not recommendations.

## Gate to phase B (bring the user ideas)
All of: ≥60 scored blind drills with Brier clearly better than a naive base-rate forecaster; ≥30 forward
paper calls resolved with positive skill; promise-tracker signal shown to predict something on ≥20
companies; written post-mortems on misses. Until then: no idea-pitching (except "great stock spotted" notes).

## Scoreboard
| Date | Drills scored | Brier (ours) | Brier (base rate) | Paper calls resolved | Notes |
|---|---|---|---|---|---|
| 2026-11-20 | 0 | – | – | 0 | loop started |

## Knowledge backlog (top = next)
1. US toolkit: SEC EDGAR access (10-K/10-Q/8-K/Form 4/13F), US transcripts sources, US factor & IPO base rates, US red flags.
2. Blind drill packets set 1 (India + US).
3. Accounting deep-dive: reading cash-flow statements, working-capital games, Ind AS vs US GAAP differences.
4. Valuation craft: reverse DCF practice, sector multiples history, when cheap stays cheap.
5. Capital allocation scorecards (buybacks, M&A, dilution) — India & US examples.
6. Behavioural finance applied: our own bias checklist; pre-mortem templates.
7. Macro → markets transmission: rates, liquidity, FX, commodity cycles (India & US).
8. Books distilled from primary text where legally accessible (public letters, memos, speeches, papers).
9. YouTube/podcast learning — blocked until a transcript API key is provided.
10. Promise tracker automation + peer base rates (method calibration, not picks).
11. "Lazy prices" text-change detector on Indian annual reports.

## Done
- 19–20 Nov 2026: playbook, winners' edges, 100 case studies, 19 sectors, 75 investors/groups, cycles,
  frauds, primary sources, base rates, NSE/BSE tools, promise tracker pilots (2).
