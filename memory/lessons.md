# Lessons — mistakes and principles

Add new lessons at the bottom with a date. Each has: what happened → rule.

## L1 (2026-11-19) — Output is not edge
**What happened:** User said "you are my sleeper cell, don't make me define everything."
Claude jumped to running public screener.in screens across 4 themes and produced 13
"finalists". User: "amateur move… what is our advantage? Did I ask you for stocks?"
**Rule:** Before any stock work, answer: *what do we know or do that the market
doesn't?* Public screens are what thousands of people open daily — zero edge. Taking
initiative means thinking about strategy, not producing activity.

## L2 (2026-11-19) — Verify the user's premises
User's Radico story (2008 UBL issue → 120 to 4,600) was wrong on cause and timing;
PR Sundar's SEBI date (2023 not 2024); rupee "96–97" was stale (recovered to ~94).
**Rule:** Fact-check the framing of every request; correct it plainly.

## L3 (2026-11-19) — Every number needs two dated sources
From the stock-research-analyst skill: consolidated not standalone; check quarterly,
not just annual; recompute P/E; flag single-sourced figures.

## L4 (2026-11-19) — Honest ambition
User has a huge dream and rejects "excuses". Don't deflate it, and don't flatter it.
Frame structural advantages of winners as a map for building our own edge, not as
reasons it's impossible. Survival (no ruin) is part of winning.

## L5 (2026-11-19) — Memory is files
Claude has no memory between sessions except this repo. Write everything here,
immediately, and keep MY_MEMORY.md in sync for the user.

## Principles (from research)
- Base rates: ~4% of US stocks created all net wealth (Bessembinder); ~2.4% globally.
- Twin engine: multibaggers = EPS growth × P/E rerating (Radico ≈ 7.5x × 5x ≈ 38x).
- Expect deep drawdowns in winners (Amazon −94%, NVIDIA >50% twice, Radico −74% in 2008).
- Size so being wrong is survivable; a few winners pay for many losers.
- Disqualifiers regardless of price: promoter pledge, qualified audit, margin jump with
  no identifiable cause, debt-funded growth with negative CFO.

## L6 (2026-11-19) — Check field meanings before trusting data
First pledge pass used `percSharesPledged` (all pledged shares incl. public) and nearly reported
false promoter pledges. Sanity check (pledge % of total vs of promoter didn't reconcile) caught it.
**Rule:** inspect raw records and reconcile numbers before acting on a new data source.

## L7 (2026-11-19) — Self-declarations go stale
Transrail's Apr-26 no-encumbrance declaration was relied on; NSE data for 30-Sep-2026 shows a
5.97% promoter pledge. **Rule:** verify governance flags from exchange data every quarter.

## L8 (2026-11-20) — Management credibility changes the verdict
Skipper looked BUY-ZONE on numbers (screen). Promise tracker: ~41% weighted delivery, 5 re-dated
capacity deadlines, reversed "no more equity" promise. Downgraded 66 → 55, WATCHLIST.
**Rule:** no BUY-ZONE without a promise-tracker credibility read on the last 6–8 calls.
Also: score 2–3 sector peers before judging a credibility number (no base rate yet).

## L9 (2026-11-20) — Method tests are not recommendations
Ran promise-tracker pilots on UNIPARTS/SKIPPER (chosen only because data was already in memory), then
reported them as verdicts ("downgraded to watchlist", "stays BUY-ZONE"). User: "again you are searching
for stocks?" — same failure as L1.
**Rule:** companies used to test a method are *test material*. Report what the method revealed, not a
buy/sell verdict. No BUY-ZONE/WATCHLIST/score language unless the user explicitly asks about a stock.
Default next steps should be learning/method (playbooks, calibration, teaching), not more stocks.

## L10 (2026-11-20) — Red flags are hypotheses, not verdicts
User: high-P/E names with every number "against" them still multiplied; good numbers can hide traps.
**Rule:** every flag (pledge, P/E, negative FCF, debtor days…) must be interpreted with the business's
real story; record *why* we override or keep a flag. Track our checklist's false alarms and missed traps.
(Note: our hard disqualifiers — fraud signals, governance — stay strict until evidence says otherwise.)

## L11 (2026-11-20) — Claude's training knowledge contaminates historical drills
Drill set 1: the blind analyst recognised all 10 "anonymised" companies (sector hints like a listed radio
subsidiary, African lead plants, SME gate maker + real numbers were enough). Set 1 excluded from scoring.
**Rules:** (a) drill v2: blur sector/geography to generic level, multiply all money by a hidden random
factor, shift fiscal years, prefer obscure micro/small caps, strip group/listing-venue clues;
(b) **forward paper calls are the only truly clean test of our skill** — weight them most in the phase-B gate;
(c) historical drills remain useful as practice, scored only when "not recognised".

## L12 (2026-11-20) — Our own checklist has measurable false alarms
Flags-judgment study: our checklist would have rejected Titan, Apollo Hospitals (76% pledge) and HAL, and
passed Vakrangee (CFO > PAT). Separator: false alarms had a mechanism outsiders could verify without
company-supplied data, cash eventually arrived, governance clean/improving; traps' good numbers were verifiable
only via company data. Also: buying at ~2× a stock's own median P/E gave flat 4–6 yrs even with earnings growth.
**Rule:** hard disqualifiers stay; soft flags are graded with a written override (insight:flag-override-template).
Pledge rule changed to graded; four 19-Nov downgrades (4–6% pledges) reverted to "open question".
