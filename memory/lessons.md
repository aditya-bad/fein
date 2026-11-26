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
each resume re-reads large transcripts/files, wasting budget. **Rule (user: "not a hard rule, your decision"):** default 2–3 concurrent agents (prefer heavy + light mix), adjust to task size and remaining budget; size each task to finish within one usage window; save in stages; start the next task only when one
finishes; give agents precise file paths so they read less.

## L24 (2026-11-22) — Solvency flags double failure odds but catch few failures
US pre-registered test (survivorship-free): negative equity (excluding buyback-driven cases with positive FCF) lift
2.31 and "≥2 solvency flags" lift 2.37 → graded red; interest cover <1.5x mostly flags loss-makers and would cut 27%
of later >3x winners; payouts > FCF while borrowing had no signal. Recall only 8–16% of failures — most 2015–16
energy and COVID failures looked solvent a year earlier. **Use:** look harder and size smaller; not protection, not a short signal.

## L25 (2026-11-22) — US rules don't transfer to India as-is; admission ≠ death
India solvency screen: the US short-term-funding-gap rule (S3) fired on half of Indian firms because working
capital runs on short-term bank lines and spare cash sits in liquid funds → excluded from India S5 (decision:
india-solvency-s3-excluded). Dead-company probe: IBBI CIRP export (9,263 admissions, 673 listed), IBBI liquidations
(3,023), NSE delisted.csv (stale to 2020), BSE delisted/suspended (no dates) are reachable; NCLT site is behind a
CAPTCHA (don't automate). An insolvency *admission* is not a failure (Inox Wind, VA Tech Wabag survived) — use
liquidation, delisting or confirmed price collapse as the failure outcome.

## L26 (2026-11-22) — Credibility across 3 sectors and 2 markets: numbers get met, dates slip
Auto components (India), IT mid-caps (India), US industrials: margin guidance met 81–98%, revenue/growth ~69–71%,
capacity/plant/production dates weakest (43–50%) everywhere — the same as T&D (L18). Much "delivery" is
conservative guiding (Watts raised at every call). US peer medians sit near 100%, so sector-adjusted scores are
noisier there. **Rule:** weight a company's *execution-date* record most; treat beating its own soft guide as weak
evidence of skill. 38 credibility-generated calls (India 27, US 11) will test whether the adjustment adds skill.

## L27 (2026-11-22) — Indian survivorship-free test: same direction as US, too few cases to prove
Screener still serves 87% of dead Indian companies (prices + annual tables) → survivorship-free Indian tests are
feasible now. Weighted 5-year failure base rate 19.7% in India vs 9.5% US. S1/S5-India ≈2× lift but CIs wide;
interest cover <1.5x is a genuine signal in India (2.87× for liquidation/compulsory exit). Dead banks with unlabeled
pages leaked past the financial filter (fixed in the test; live screen has the same small gap).
**Rule:** asymmetric costs justify keeping cheap "look harder" flags on consistent-but-unproven evidence; never
promote them to hard rules without proof.

## L28 (2026-11-22) — Survivorship bias flipped a conclusion
Survivors-only Part B (L20) said pledged firms tripled MORE often (69% vs 51%). With dead firms included, pledged
firms tripled about half as often (15% vs 28%) and lost >50% three times as often (31% vs 11%); pledge >50% lift 2.43,
5.19× for liquidation/compulsory exit. The earlier result came from a COVID-low snapshot and a "later grew past
₹400 cr" sample. **Rule:** never draw a stage-2 conclusion from a survivors-only sample; promoter pledge is our
strongest mechanical red flag (decision:adopt-disqualifiers-v3), partly because it tracks leverage.

## L29 (2026-11-22) — Lazy Prices: right direction, not proven; watch for mechanical confounds
US 10-K text-change test (3,164 firm-years, 2021–23): biggest changers −7.3% vs size-matched controls at 12m
(t −2.53, CI touches 0) — NOT PROVEN by our bar; drift built slowly as in the paper (−0.6/−1.3/−7.3% at 3/6/12m).
About half came from first 10-Ks after a de-SPAC (shell → new business); biotech mix distorted controls; mostly
2022 filings. Risk-factor section ran backwards ("stale risk factors" did worst — new hypothesis, not a finding).
**Use:** judgment flags only — first 10-K after de-SPAC/major change = look harder; big text change = read what
changed. Next: pre-registered v2 on 2024–25 filings (Jaccard, ex de-SPAC, sector-matched controls).

## L30 (2026-11-22) — Lazy Prices v2 on fresh 2024–25 data: retired as a rule
Pre-registered, sector-and-size-matched, de-SPACs excluded (1,971 firm-years): big changers −1.4% (t −0.25) → not
proven; "stale risk factors" +0.5% → rejected (v1's −11.5% was a biotech/sector-mix artefact). Changers show a
lottery profile (median −10%, hit rate ~40%, a few +500–970% winners), not a slow drift.
**Rule:** plain text-change is retired as a mechanical rule in the US; keep only judgment cues (first 10-K after a
de-SPAC/transformation = look harder; big change = read the diff). Next text test: the Indian annual-report pilot.
Meta-lesson: 1 of 6 signal tests so far survived fresh data (Indian PEAD avoid leg) — base rate for "published
anomaly works for us" is low, as McLean–Pontiff predicted.

## L31 (2026-11-23) — Our one proven signal survives the survivorship check
PEAD avoid leg with dead firms included (2018–25, weekly closes, pre-registered): bottom quintile −2.43% vs
size-matched controls at 13 weeks (t −6.2) vs −2.08% live-only → bias small and in the predicted direction
(live-only understated the avoid leg). Long leg +1.00% net — not proven for the third time. Descriptive: distress-
listed firms after a bottom-two-quintile result lagged controls by −16.6% → combine the PEAD avoid flag with
pledge/solvency flags (stage 2 + 3 together). Status of the avoid leg: confirmed in 3 independent checks.

## L32 (2026-11-23) — Text change fails in India too; signal-test scorecard 1 of 7
Indian annual-report pilot (pre-registered, 200 firms incl. later-dead, FY22→23/FY23→24): MD&A and auditor+CARO
big-change quintiles −2.1% / −0.8% vs sector-size controls (t ≈ −0.3/−0.1); new adverse auditor item +7.7% (wrong
sign, n=21) → NO-GO for a full run. Plain text-change has now failed 3 times (US v1, US v2, India).
Useful by-product: NSE annual_reports fetch works (tools/nse_fetch.py annual_reports); reading the auditor's report
+ CARO vs last year stays a deep-dive judgment cue (worst cases −42% to −77%, but big winners too).
**Scorecard of signal tests (honest):** survived = Indian PEAD avoid leg; failed/not proven = US insider clusters,
Indian promoter buying, PEAD long leg, Lazy Prices US v1/v2, India AR text. Edge is likelier in human-depth work
(promise tracking, deep dives) combined with the few proven filters than in mechanical text/flow signals.

## L33 (2026-11-23) — First live deep dive: depth finds the real story, but "hidden value" isn't automatically mispricing
SUNFLAG (random draw): the key fact was a 10.66% stake in Lloyds Metals worth ~₹9,016 cr post-tax vs ₹6,643 cr market
cap — but the implied 45–61% holding-company discount has verified causes (no plan to monetise, pledged shares,
no concalls, mining milestones that never arrive, 1% institutional ownership), so it's not a claimable mispricing.
Card: size 0 (EV below hurdle). 6 live calls + 3 card calls now test whether deep-dive probabilities beat base rates.
Tools: worksheet v1.2 handles non-operating stakes; promise tracker needs an annual-report-status mode for firms
without concalls; NSE pledge API sometimes returns empty → XBRL fallback.

## L34 (2026-11-23) — Every decision card so far says "size 0": the gate itself needs calibrating
6 of 6 cards (4 practice + SUNFLAG + Kirby) returned size 0, mostly from the expected-value hurdle. Some of that is
right (no claimable mispricing), but Kirby exposed a model gap: the worksheet ignores deferred cash taxes from
accelerated depreciation (FCF $406M vs NOPAT $374M), and India's 12–13% cost of equity makes compounders look
overvalued (L21). A gate that never opens can't be tested. **Next:** add cash-tax and reinvestment-realism inputs,
build real US/India 5-year base-rate classes from the survivorship-free panels, reconcile the PEAD avoid rule
(bottom-two quintiles for India; US uncalibrated), then re-run all 6 cards to see which, if any, open — without
changing the hurdle just to make cards open.

## L35 (2026-11-23) — Red flags carry the tail risk; earnings misses carry the drift
Pre-registered combined test (10,242 PEAD events, 2018–25, incl. dead firms): an earnings miss + red flag did NOT drift
more than a miss alone (H1 not supported), but halved within 12 months 17.6% of the time vs 6.1% for clean firms
(2.9×, H2 supported). Most of that comes from the flag itself (flag without miss: 2.5×); pledge >50% is strongest
(3.9×); S5-India alone showed nothing. **Rule:** keep the PEAD WAIT gate; add a survival cap — bottom-two result plus
pledge >25% or interest cover <1.5x → no new money / minimum size and a balance-sheet question
(decision:pead-avoid-plus-redflag-survival-cap). Proposal to test: cap any red-flag firm regardless of results.

## L36 (2026-11-23) — Our scenarios under-weight the left tail; the outside view says blow-ups are common
Real 5-year base rates (survivorship-free): India non-fin ₹1,000–20,000 cr: P(≥3x) 21%, P(≤0.5x) 11%, P(blow-up) 15%;
US $0.5–10B float: 7% / 14% / 11%. (Old India placeholder said 44% / 2% — badly wrong.) On every card our P(blow-up)
was only 0.07–0.18× the base rate → systematic overconfidence about survival. Calibration (cash tax, ROIIC realism,
exit-multiple bet table) didn't open any card; the binding choice is the exit multiple, as it should be.
**Rule:** anchor tail probabilities to the class base rate and move away only with written evidence; Brier scoring
of live calls will measure this. Next useful card: a stock cheap at entry and inside a base-rate size band.

## L37 (2026-11-23) — For no-concall companies, disclosure flags beat credibility scores
Promise tracker v1.4 annual-report mode (validated on SUNFLAG, GULFPETRO, REPRO): too few dated promises to score
(n ≤ 5), but cheap *disclosure-quality flags* are informative: "planned" dates already past at filing (REPRO ×3),
the same "commissioned during the year" sentence in consecutive reports (SUNFLAG), outlook text copied year to year
(GULFPETRO), unchanged reserve quantities. **Use:** for companies without calls, report the asset×year status table
and disclosure flags in the deep dive; don't compare AR-mode scores with concall scores.

## L38 (2026-11-23) — "Cheap" usually means peak-cycle earnings; follow fees to related parties
Live deep dive #3 (AUTOAXLES, random draw from the cheapest EV/EBITDA tercile): 12.9× trailing but 25.8× on 10-yr
average EPS, at a truck-cycle peak (last cycle: revenue −53%, EPS −81%, price −80%). After minorities voted 79.5%
against a ₹2,500 cr related-party deal, a technical fee to the Cummins-group entity appeared (41% of core EBITDA,
renewed annually below the vote threshold); a switch to direct OEM pricing inflated revenue ~5% (visible in the
materials ratio). Credibility 43% vs 60% sector median. Card size 0 (EV 1.40× anchored vs 1.76× hurdle).
**Rules:** for cheap-tercile names, value on normalised (cycle-average) earnings; read vote *results*, not just
notices; when a related-party channel changes, check growth against the materials ratio.

## L39 (2026-11-24) — Red-flag firms are high-variance, not just bad: cap size, don't veto
Pre-registered test (`research_notes/Backtests/survival_cap_general_india.md`, prereg committed before results). Indian non-financials
with pledge >25% or interest cover <1.5x, regardless of earnings surprise: 12-month halving 17.8% vs 7.1% (RR 2.49×, CI 1.96–3.13);
5-year failure, survivorship-free panel 2.36× (CI 1.58–3.66); 3-year failure 5.2×. But they also produced more 3× winners in 2018–21
(1.37×; 1.07× in 2022–25), and the cap would have flagged ~31% of eventual triplers. **Rule (card v1.3):** outside the PEAD window,
red-flag firm = starter size (≤1%) and no additions; inside the PEAD window, 0 new money (v1.2). Pledge is bad on both tails
(fewer winners too); weak interest cover mostly widens the spread — a split rule needs its own pre-registered test.
S1/S5 alone add nothing (too few events, ~1.0–1.2×). Caveat: event sample not blind; only the snapshot panel is a true replication.

## L40 (2026-11-24) — Very high ROIC can be a government concession, not a moat (INDRAMEDCO live dive #4)
IMCL's ~54% ROIC rests on land leased at ₹1/month; the lease expired Jul-2023 and the government counterparty opposes renewal
in the Supreme Court — yet the FY26 annual report never mentions the expiry. **Rule:** for any government-granted input (land,
lease, licence, PPP), record expiry, the obligation given in return and compliance with it, and the counterparty's own filings;
treat the stock as an option on renewal. Add "material external fact absent from the AR" as a disclosure flag. Read vote results
as promoter shares held vs votes polled (a co-promoter abstaining revealed the broken JV). Card v1.3's survival cap cannot see
legal/licence risk → candidate manual trigger. Tail anchoring can *lower* well-documented tails; flag when it does.
Process: sector frames need a full industry map (NSE index lists left 60% of the band unclassified).

## L41 (2026-11-24) — Lenders: read capital-adequacy book and the bad-loan walk, not reported GNPA (UTKARSHBNK live dive #5)
Utkarsh SFB's GNPA "improvement" 12.4%→5.9% came mostly from write-offs + ARC sales (₹1,743 cr removed vs ₹1,724 cr new bad loans;
one ARC sale at 13.6% of face). Tier-1 fell 15.1%→12.8% in one quarter on DTA + capitalised-software deductions — CET1 book ₹10.71
vs reported ₹15.04/share; nobody asked on the call. **Rules:** (1) value lenders on CET1 book (Pillar 3 deductions) beside reported
book; (2) always build the GNPA walk (new NPAs, recoveries, upgrades, write-offs, ARC sales) before crediting asset-quality gains;
(3) generalise L40 to state law — any state >~15% of the book → search that state's gazette; (4) we have no India lender base-rate
class yet, so lender tails are anchored to the wrong class — build one before trusting lender cards.

### L39 addendum (2026-11-25) — splitting the cap by flag type REJECTED
Pre-registered split test (`research_notes/Backtests/survival_cap_split_india.md`; note: prereg was written first but committed together
with results, so the git timestamp doesn't prove order — the stage log does). Pledge-only does NOT cut the upside in the event sample
(3x-winner RR 1.27 [0.77, 1.88]); single-flag tails swap by regime (pledge bad 2018–21, weak ICR bad 2022–25). Only **both flags**
is consistently bad: 12m halving 4.2×, 3y failure 9.4×, stable across periods and the survivorship-free panel — yet still 23.5% triple.
Card unchanged. Judgement rule until tested: when both flags fire, answer the balance-sheet question before even a starter position.
Next: pre-register "both flags → 0 new money" on fresh 2026+ events.

## L42 (2026-11-25) — A strong segment margin can hide a sub-par group ROIC; read dissent net of promoter votes (HARSHA live dive #6)
Harsha's India engineering segment earns 22–24% EBITDA, but group ROIC ~11.5% and ROIIC ~11% (< 12.5% cost of equity) while
₹600 cr of capex goes in at ~54% subsidiary utilisation. **Rules:** compute group ROIC and ROIIC before reading segment margins;
rebuild capex payback two ways (current utilisation vs management's asset-turn claim). Report AGM dissent as
votes against ÷ (votes cast − promoter shares): a "14%" against was ~92% of non-promoter votes. L40 for manufacturers: the
government input is often subsidised financing or a dated rule (e.g. solar relaxations), possibly absent from the AR.
Process: take the frame close from the bhavcopy's date column, not the file name; card input validation (credibility as fraction).
**Pattern to watch:** 6 of 6 live cards = size 0 (EV below the 1.76x hurdle). Either the market is roughly fair on random draws
(expected) or the hurdle/tails make the card structurally say no. Check at the first scoring season before changing anything.

### L41 follow-up (2026-11-25) — India lender base rates exist now
`india_lender_1000_20000cr_5y` (n=107 company-starts, survivorship-aware): P(≥3x) 11% vs 21% for non-financials; P(≤0.5x) 25% vs 11%;
P(blow-up) 27% (permanent 20%) vs 15%; median 1.04x. No private bank tripled. Start years disagree hugely (2016 vs 2018 = the credit
cycle), so treat as a cycle-average. Card v1.5 auto-selects it for Indian lenders. Never re-issue a dated card when a better base rate
arrives — add an addendum; scoring must test what we actually said.

## L43 (2026-11-25) — A card that scores a fairly priced stock 0 can't tell us the market is fair
Audit: the 1.76x hurdle = 12% index CAGR over 5 yrs ≈ the India class median (49.6% of firms cleared it) — not too high. But the
mechanics add an undeclared ~2pp margin (EV treats scenario multiples as means while probabilities treat them as medians; only the
left tail is anchored), so a base IRR ≈ cost of equity scores 0 and the pass point is ~14%. All 6 live zeros were large gaps
(price falls of 14–33% needed) driven by our own base cases below the cost of equity. **Rule:** read size-0 as "not cheap enough
by our inputs", not "market fair"; only stage-7 scoring answers fairness. Fixes are pre-registered (decision:card-audit-fixes-prereg-2026-11-25), none applied before the Jan–Feb 2027 season.

## L44 (2026-11-25) — Strip exceptional gains before any "cheap" read; "numbers met, dates slip" is not universal (SHK live dive #7)
S H Kelkar's 18.7x trailing P/E included ₹63 cr of fire-insurance gains in ₹159 cr PBT — core P/E ~33–37x. The v1.4 normalised-EPS
check missed it because the 10-yr average happened to agree. **Rules:** compute core EPS (ex-exceptionals, ex-other income, after
interest) before valuation temperature. When ROIIC < cost of equity and net debt is large, DCF value can be below net debt — the
whole EV above 1x is an exit-multiple bet (L21). L42 again: 2/2 draws in this frame family had group ROIC < CoE. SHK missed both
margin numbers and dates → L26's pattern is a tendency, not a law. Check whether promoters vote on their own relatives' re-appointment.
Open: pollution-board scraper (no structured source); chemicals/F&F peer credibility ledger.

## L45 (2026-11-25) — When the government sets every price, track the price calendar (UTTAMSUGAR live dive #8)
Uttam Sugar: the UP cane price alone ≈ the sugar realisation; each ₹10/qtl moves EBITDA 15–19%. The Oct-2026 OMC ethanol tender
excludes cane-juice/B-heavy ethanol (the company's distillery feedstock) — absent from its Oct-31 results deck. **Rules:** for any
business with administered prices, keep a dated table (last value, next decision date, whether the company's filings mention it).
Seasonal balance sheets need average capital (net debt ₹30 cr Sep vs ₹712 cr Mar). When core EPS = reported, valuation temperature
(15.2x vs own 10-yr median 8.0x) can be the binding read. Card can't express *partial* loss of a government input (core-asset trigger
is yes/no). Cyclical upside tail (model 0.8% ≥3x vs a stock that did 12.7x in 2020–23) is likely too thin → covered by pre-registered fix (3).
Frame hygiene: industry_map's FMCG includes agri-commodity processors. 8/8 live cards size 0; 3/3 recent draws ROIC < CoE.

## L46 (2026-11-25) — Always name the ticker; same-group companies get confused (Kalpataru)
User read "Kalpataru 77" as Kalpataru Ltd (KALPATARU, real-estate, listed mid-2025 ~₹397 → ₹240 on 25-Nov-2026, Yahoo).
Our score 77 was Kalpataru Projects International (KPIL, T&D/EPC: ~₹375 Nov-2021 → ₹1,310 Nov-2026, Yahoo). **Rule:** in every
message to the user, give company name + NSE ticker. Also: KPIL's past price rise does NOT validate the score (score built in 2026
on past promises = hindsight); only forward calls test it.

## L47 (2026-11-25) — Forward P/E IS freely available (user correction); consensus coverage on small caps is thin
I told the user forward P/E needs paid data. Wrong: Yahoo/stockanalysis show it. New tool `tools/valuation/consensus.py` (Yahoo
quoteSummary with session crumb; stockanalysis.com is behind a Cloudflare challenge — not bypassed). Snapshot 25-Nov-2026
(`research_notes/Consensus/snapshot_2026-11-25.json`): analysts on next FY — RELIANCE 25, AVGO 50, KPIL 11, HARSHA 4, UTKARSHBNK 2,
SHK/INDRAMEDCO/AUTOAXLES 1, UTTAMSUGAR/SUNFLAG 0. **Rules:** show consensus forward P/E + analyst count beside our scenarios as a
cross-check; analyst count = coverage (fewer → more room for depth edge); forward EPS is often adjusted/non-GAAP (AVGO 37x trailing
vs 14.9x forward) so the P/Es aren't like-for-like. SHK: 1 analyst implies ~₹9.9 forward EPS (12.9x) vs our core ₹3.4–3.9 — a dated
disagreement we can score (our FY27 PAT ≥₹120 cr call at P=0.15). Before claiming data is unavailable, check.

## L48 (2026-11-25) — Card σ=0.35 is too narrow; two-sided anchoring passes history; blow-ups still under-predicted
Pre-registered leave-one-cohort-out test (`research_notes/Decision audits/card_fixes_historical_test.md`): the card's 50/80%
intervals caught only 35/60% (India), 12/53% (lenders), 33/65% (US) of real 5-yr outcomes. Fix (4) wider σ improved log score on all
panels but FAILED the pre-set Brier check on lenders (P(≤0.5x) 28.9% vs 25.2% real) → not adopted (re-test needs a new prereg).
Fix (3) two-sided anchoring PASSED (historical half; live half pending to Sep-2027). Every variant under-predicts blow-ups
(India 10.5% vs 15.5%, lenders 16% vs 27%, US 10% vs 15%) → next prereg. With fix (3), HARSHA's dated card would have opened
(EV 1.58x → 1.87x) — dated cards are never re-issued. v1.6 patch (fix 1 mean/median + fix 5 shape warning) ready, apply after season.

## L49 (2026-11-25) — The credibility forward test is under-powered: too few past promises per company
Promise forward test (12 cos, 38 calls, `research_notes/Promise tracker pilot/forward_test_2026-11/`): only 1–6 scored past
promises per company (36 total), so P_cred moves ≤ ±0.10 from the sector base rate and not at all for 4 companies → a single-season
verdict will most likely be INCONCLUSIVE. Pooled with the 22-Nov cohort (38 calls) it is ~76 calls. **Rules:** next cohorts need
≥10 scored past promises per company (read ≥12 calls, full pipeline, not tier-A shortcuts) — the bottleneck is reading volume
(Gemini CLI + Pi). Again: margins met 8/10, revenue/orders 6/15, dates 1/6 (L18/L26 pattern holds).

## L50 (2026-11-26) — Verify news before using it: headline verbs overstate, feeds resurface stale items
News verification (`research_notes/News/verification_2026-11-26.md`): of 22 flags, 6 confirmed, 10 partly, 4 unconfirmed, 2
false/stale. The most surprising one was TRUE (NVIDIA 8-Ks: board accepted Huang's resignation 11-Nov-2026, reinstated 22-Nov) —
so surprise ≠ false; primary filings settle it. "Justice Department closes probe" was really an HSR waiting-period expiry;
"Polycab NCLAT reserves order" was a month-old story already resolved; the "steel duty relief" plea was from 2025. **Rule:** a news
item becomes an event record only after a primary source or two reputable outlets; record the verb the primary source uses.

## L51 (2026-11-26) — Valuation-gap timing: no out-of-sample power in 2012–21 data; fix the rule, not the verdict
Pre-registered test (`research_notes/Macro/ey_gsec_gap_test.md`): with NSE P/E only from Feb-2012 (older history is browser-only),
neither Nifty P/E nor the earnings-yield − 10-yr G-sec gap beat the historical mean out of sample (all OOS R² negative). The literal
rule passed the gap (less wrong than P/E) but was overridden: a rule must also require OOS R² > 0 — recorded for future runs. Only
~3–5 independent windows: this neither confirms nor refutes the P/E ≥ 24.5 base rate (which rests on the 2000/2008 peaks). Gap stays
as snapshot context, not a card input. Data conflicts to resolve: repo 5.50% (RBI site) vs memdb 5.25% (Jun-2025) — hike undated;
gold-api $3,568/oz vs Yahoo GC=F ~$4,187 (Sep) vs IBJA ₹122,982/10g — gold source unreliable this month.
