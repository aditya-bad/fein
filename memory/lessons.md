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

## L13 (2026-11-21) — Depth lives in the boring filings
VMM practice deep dive: the sustainability report (BRSR: 66% of staff at minimum wage, 84% attrition),
the "other expenses" note (security charges ₹87.65 cr → ~5.5–6 guards/store) and related-party notes
(promoter-PE vehicle as transporter, 28% of transport cost) revealed cost drivers no broker note had.
**Rule:** for any deep dive read BRSR, other-expense breakdowns, RPT notes and every company-defined
metric's footnote (payback, LFL, "loyalty customers", pre-Ind AS 116 EBITDA). Protocol:
research_notes/Deep dives/deep_dive_protocol.md.

## L14 (2026-11-21) — Famous public signals may not survive an honest test
US insider-buying clusters (849 events, 2021–24) vs size-matched random controls: 12m excess 0.0%
(CI −4.8 to +5.0). The apparent +1.7% vs IWM was a size/survivor effect that random controls also showed.
"Stronger" variants (3+ insiders, CEO/CFO buying) did worse. **Rule:** always test against matched
controls, date signals at filing (not trade), audit survivorship, pre-register subgroup tests.
Next: pre-registered "opportunistic insider" rule (train 2017–20, test 2021–24) and the India SEBI PIT version.

## L15 (2026-11-21) — Historical blind drills don't work for an LLM; forward calls are the test
Set 2 (money scaled, years relabelled) still 9/10 recognised from qualitative details (dual-class family
control, a 74.8% promoter stake, an overseas plant, a common pandemic-era date). Across sets 1–2: 19/20 recognised.
**Decision:** stop treating historical drills as a skill measure. Use them only as analysis *practice*.
Skill is measured by **forward paper calls** (dated probabilities on events nobody knows yet) — make many,
cheaply, every results season. Possible future v3: synthetic composite packets blending 2–3 companies.
D017 (only clean drill): Brier 0.170 vs base-rate 0.230 (n=1 — meaningless alone).

## L16 (2026-11-21) — For subsidiaries of foreign parents, follow the money to the parent
Cummins India practice: royalty + support services to the parent rose from 8.8% to 11.6% of EBITDA; total
cash to parent ≈8.9% of sales; royalty agreement expires 31-Mar-2027; 51% of purchases and most exports are
intra-group at cost-plus — so "weak rupee helps exporters" mostly helps the parent. Best source: the
AGM-notice related-party annex (formulas, rates, sunset dates). Protocol v1.1 adds a parent-take table.

## L17 (2026-11-21) — First positive, out-of-sample finding: Indian post-earnings drift
Pre-registered PEAD test (580 cos, 10,026 events): top-minus-bottom SUE quintile +4.24% over 63 days in the
2022–25 TEST period (t 3.99; train +4.84%, t 4.06). Long-only top quintile vs size-matched controls +2.36%
gross (t 3.23), +1.36% net of 1% costs — misses our pre-committed cost bar by 0.06 pp (reported, not rounded up).
Bottom quintile (big misses) is the strongest leg (≈ −2.1 to −2.7%, t ≈ −4.5). Small-vs-large hypothesis NOT supported.
**Use:** a timing/filter layer, not a multibagger method — avoid/exit after big earnings misses; tilt research
toward top surprises; ~30-name baskets. Exploratory (needs fresh pre-registration): mid-cap tertile strongest;
"price rose on results" filter; 2025 weak (decay or noise). Weakness: standalone EPS, price-only, sample not universe.

## L18 (2026-11-21) — A credibility score means nothing without a peer base rate
T&D/EPC peers scored identically: KPIL 76.7%, Skipper 41.3%, KEC 19.8% weighted delivery. Skipper is the
sector median (sector-adjusted −2.6 pts), so its 20-Nov downgrade "for weak credibility" (L8) over-weighted
an absolute number. Sector-wide: order-inflow shortfalls, 1–2 qtr date slips, silent downward re-statements,
Jal Jeevan payment delays. **Rule:** always report credibility as sector-adjusted (company − peer median, by
category, ≥5 promises per category). Precise ≠ more reliable; volunteered opening-remark guidance delivered
better at KEC/KPIL. n=3 → provisional. Also: KEC Power Grid bribery-inquiry question (Jul-2025) + ~15 months
without PGCIL orders — single-source governance flag, verify independently.

## L19 (2026-11-21) — Indian PEAD replicated on fresh 2026 data: the edge is the AVOID leg
PEAD v2 (pre-registered; 1,555 cos, 4,272 fresh events, 79% consolidated EPS): bottom SUE quintile −2.73% vs
size-matched controls at 63d (t −3.6, CI excludes 0) — confirmed in two independent periods; quintile 2 equally
weak. Long-only top quintile +2.41% gross / +1.41% net (CI touches 0) — not proven, again. "Positive
announcement-day reaction" filter did not replicate; v1's "mid-cap strongest" reversed (noise).
**Rule (stage 2/3):** treat the bottom two earnings-surprise quintiles as an avoid/exit flag for at least
63 trading days. Don't treat a positive surprise alone as a buy reason. Exploratory subgroups don't survive
fresh data — only pre-registered results count. Live tracker logs from Q3 FY27; verdict after 4 live quarters.

## L20 (2026-11-21) — Our hard filters catch frauds, not leverage blow-ups; mechanical cash-flow rules hit winners too
Stage-2 test (106 case episodes, in-sample + 495-firm 2020 snapshot): current hard set caught 8/39 known traps,
rejected 0/62 winners — all 8 were frauds caught by *judgment* signals (fake cash, unverifiable profits, implausible
economics). Leverage blow-ups caught 0/15; post-run crashes 0/9. Auditor exit never fired before a peak (0/41) → it's
an EXIT trigger, not an entry screen. CFO/PAT<0.7 and negative FCF fired on winners as often as traps (HAL, BSE,
Trent, Netflix). Pledge >25% of promoter holding = best graded flag (8/20 traps vs 2/13 winners). P/E>50 belongs
in valuation. Universe test is survivorship-biased (no delisted firms) → can't see losers well.
**Adopted (provisional):** insight:disqualifiers-v2-proposal as the working rule set; solvency flags (negative
net worth, interest cover <1.5x, short-term funding of long assets, payouts > FCF while borrowing) are UNTESTED.

## L21 (2026-11-22) — In India, the exit multiple is the hidden bet
Valuation worksheet on 3 practice names: at 12–13% cost of equity a DCF can justify only ~12–17x P/E in year 5, so
48–52x compounders look 65–70% overvalued and need ~30%/yr growth for 10 years. Scenario exit P/Es (25–50x) were
2–3× what the DCF justifies. **Rule:** judge Indian compounders on the return the price offers in the base case vs
the index hurdle, and state the exit multiple explicitly as a bet. Practice paper calls from templates are NOT
added to the stage-7 scoreboard (live cards only).

## L22 (2026-11-22) — End-to-end dry runs find real bugs; for banks the flattering numbers mislead most
Federal Bank dry run (stages 2→6, practice, no verdict): 19 gaps found, 14 fixed. Biggest: range parsing read
"18–20%" as −20% (affected SKIPPER pending targets; re-scored: no status changed, goalpost moves 12→10);
NIM scored as cost/revenue; bank transcripts on NSE are cover letters only; no bank valuation mode (added P/B–ROE).
Good-but-misleading rows outnumbered bad-but-benign 10 to 6: retail loan growth 18% → 4% ex special FCNR window;
GNPA "10-year low" helped by write-offs > slippages; PCR 87% → 76.6% ex one-off; ROE 13.6% → ~10% after warrants.
**Rule:** run a full dry run whenever a new sector type enters the pipeline; for banks always strip special
windows, write-offs and one-offs before trusting headline asset-quality and growth numbers.

## L23 (2026-11-22) — Run work as a pipeline, not a swarm (user observation, confirmed)
Running 4–6 agents in parallel hit the 5-hour usage limit roughly daily, leaving several tasks half-done;
each resume re-reads large transcripts/files, wasting budget. **Rule:** max 2 concurrent agents (prefer 1 heavy +
1 light); size each task to finish within one usage window; save in stages; start the next task only when one
finishes; give agents precise file paths so they read less.
