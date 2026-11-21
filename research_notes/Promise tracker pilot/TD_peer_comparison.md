# Promise-tracker calibration: Skipper vs KEC vs KPIL (power T&D / EPC)

*As of 21-Nov-2026. Research, not SEBI-registered advice. This compares management credibility scores to calibrate the method. It is not a stock ranking and carries no buy/sell view.*
Inputs: `SKIPPER.md` (19-Nov), `KEC.md`, `KPIL.md`. Seed: `memdb/seeds/2026-11-21_promises_TD_peers.json`, including `insight:td-epc-promise-credibility-base-rate`. Numbers below come from `scripts_TD_peers/build_seed.py` and `make_seed.py`, which run the Skipper formula unchanged.

## 1. Answer: is Skipper's ~41% low for the sector?
**No. On this small sample it is the middle of the range.**

| | KPIL | **SKIPPER** | KEC |
|---|---|---|---|
| Weighted delivery ratio | 76.7% | **41.3%** | 19.8% |
| Specificity-only delivery | 69.2% | 41.2% | 26.9% |
| Raw hit rate | 61.9% | 33.3% | 22.4% |
| MCS (-1.5 .. +1) | +0.63 | -0.18 | -0.60 |
| Candour index | 8% (2/24) | 12.5% (4/32) | 31% (14/45) |
| Moved goalposts / scored | 1 / 63 | 9 / 48 | 9 / 58 |
| Core (materiality-3) delivery | 83% | 52% | 9% |
| FY25-call vs FY26-call promises | 73% -> 67% | 56% -> 25% | 53% -> 20% |
| Grade | B+ | C- | D+ |

- **Median of the three = 41.3%, which is Skipper.** Against the other two (mean 48%), Skipper is about 7 points lower. On the sector-adjusted measure below, it scores **-2.6 points**, roughly neutral.
- **The spread is very wide (20% to 77%).** "T&D company" is not a meaningful base rate on its own. Credibility here is mostly company-specific, so the useful comparison is by promise category (section 3).
- **Skipper's score is robust to the one rule change these peers needed.** Under the ceiling-target rule (clarification B, section 5), its FY25 finance-cost miss (4.63% vs <4.5%) becomes "partly" and the score moves from 41.3% to 42.2%.
- **Caveat: n = 3**, the windows differ, and the peers were read less deeply than Skipper (section 6). Treat 41% as "typical, not good". That is a better reading than "C-, bad", but it is not yet a base rate.

## 2. What is sector-wide vs company-specific

### Sector-wide (all three, so do not penalise one company for it)
1. **FY26 domestic T&D order inflow fell short everywhere.**
   - Skipper's FY26 inflow was 87% of the first guide and 95% of the restated one; it cited CEA holding back bids, ROW, and transformer and HVDC shortages.
   - KPIL's T&D inflow was 90% of FY25's level, and India T&D fell from ~INR 7,000 cr to ~4,500 cr as L1s slipped into FY27.
   - KEC's India T&D intake was ~-11% against +20% guided. That was worsened by a **company-specific** 15-month gap in PGCIL awards, after an analyst raised a bribery inquiry involving Power Grid officials (single-source; see KEC.md).
   - **Group-level inflow misses were partial (84-100% of guide), not collapses.** Order-inflow promises cluster in "partly" (median category delivery 50%). The user's hypothesis is confirmed, but the effect is modest: expect ~85-95% of a T&D inflow guide in a slow-tendering year, not a blow-out.
2. **Dates slip one to two quarters everywhere.**
   - Skipper: second 75k t block, five dates.
   - KEC: E-Beam plant, five dates; Karnataka solar, three dates; Afghanistan receipt, three quarters late.
   - KPIL: VEPL sale, two quarters late against the first date; Indore collections, two quarters late; JJM recovery.

   The capacity/capex category is the weakest for the sector (median 36%). A one-quarter haircut on any T&D date is the base case, not a red flag.
3. **JJM water receivables broke every recovery promise** at both companies with water exposure (KEC: dues ~INR 800-900 cr broadly unchanged from Mar-25 to Nov-26; KPIL: INR 1,427 -> 1,551 -> ~1,600 cr). Skipper's polymer segment was hit by the same JJM cuts. This is a government-payment problem, so promises that depend on it should be scored but discounted when comparing managements.
4. **The FY26-27 operating environment hurt everyone:** labour shortages (elections, LPG), the Middle East war in Q4FY26-Q2FY27 (KEC ~INR 300-400 cr of revenue deferred per quarter; KPIL ~200-250 cr in Q4FY26; Skipper export orders) and freight costs.
5. **Restating a target downward without saying so happens at all three.** Skipper and KEC did it nine times each; KPIL three times, but its outcomes still cleared the original bar. It is industry-normal. What differs is how far the outcome falls short.

### Company-specific (these drive the spread)
- **KEC: margins, debt and NWC.** These are near zero (10%, 18%, 11%), while the other two companies' medians are 70%, 79% and 69%. The cause is internal: legacy civil, metro and railway closures, JJM exposure, Saudi 20% retentions, and growth funded with debt. Every FY26 debt or NWC number was missed and then re-set.
- **KPIL: group P&L and balance-sheet guidance** (revenue 80%, debt 100%). Its guidance is conservative, volunteered and repeated. Misses are in subsidiaries (Fasttel write-off of INR 515 cr), asset-sale timing and capex discipline.
- **Skipper: capacity dates, segment targets and exports.** Group margin and finance cost were good (margin 70%).
- **Group revenue guidance** separates the three: KPIL 80%, Skipper 35%, KEC 16%.

## 3. Proposed sector-adjusted credibility (SAC)
**Definition.** For company *i* and promise category *c*:
- `D_ic` = specificity-weighted delivery % (credit: delivered 1, partly 0.5);
- `M_-i,c` = median `D` in category *c* across the **other** peers;
- `SAC_i = sum over c of (n_ic / N_i) x (D_ic - M_-i,c)`, where `n_ic` is the number of scored promises in the category.

Report `SAC_i` (in points) next to the raw weighted delivery ratio, and always show the category row. Leave-one-out medians stop a company from benchmarking against itself. Weighting by the company's own promise mix means the score asks: "on the kinds of promise this management makes, does it deliver more or less than peers?"

| Category | SKIPPER (n) | KEC (n) | KPIL (n) | Median of 3 |
|---|---|---|---|---|
| Revenue growth | 35% (15) | 16% (18) | 80% (16) | 35% |
| Margin | 70% (4) | 10% (8) | 69% (11) | 69% |
| Order inflow / book | 32% (6) | 50% (5) | 65% (5) | 50% |
| Debt / finance cost | 57% (3) | 18% (8) | 100% (6) | 57% |
| Working capital | 75% (2) | 11% (7) | 62% (10) | 62% |
| Capacity / capex / dates | 36% (13) | 50% (8) | 0% (3) | 36% |
| Other | 50% (5) | 75% (4) | 67% (11) | 67% |

| | SKIPPER | KEC | KPIL |
|---|---|---|---|
| **SAC (points vs peers)** | **-2.6** | **-30.3** | **+28.8** |
| Raw ratio minus the other two's median | -6.9 | -39.2 | +46.2 |
| Biggest positive category | working capital +39, margin +30 | capacity +32 | debt +62, revenue +54 |
| Biggest negative category | order inflow -26, other -21, revenue -13 | debt -60, margin -59, WC -57 | capacity -43 |

**Reading Skipper with SAC.** It is roughly at peer level overall. It is better than peers on margin and working-capital promises, though Skipper's own debtor-day jump argues the WC credit is partly luck of timing; only two records are in that category. It is worse on order inflow and segment/"other" targets. Its weakest raw category (capacity dates, 36%) is exactly the sector median, so the five-date 75k t saga is bad but not unusual for the industry.

**Caveats on SAC.** The categories with n < 5 (Skipper margin 4, WC 2, debt 3; KPIL capacity 3) swing the score. Pool the categories or require n >= 5 before quoting a category gap. Merging Skipper's "order_book" into order inflow uses an n-weighted average of the two ratios.

## 4. Splits across the three
- **Precise vs vague.** Skipper: precise 33% < range 53% < vague 64%. KEC: 21% / 42% / 25%. KPIL: 72% / 65% / 75%. **Precise promises are not more reliable at any of the three.** Specificity raises a promise's weight but not its odds. The Skipper finding ("precise does worst") holds at KEC (precise is the worst bucket) but not at KPIL, where the buckets are flat. Keep the specificity weight (it measures how informative a promise is), but don't read precision as confidence.
- **Volunteered vs prompted.** Skipper: 39% vs 42% (no difference). KEC: 48% vs 22%. KPIL: 91% vs 58%. At two of three companies, **numbers volunteered in the prepared remarks are far more reliable than numbers given under analyst questioning.** KPIL publishes its guidance in the opening remarks every May; KEC almost never does (64 of 75 KEC promises were prompted). A useful screen is to ask whether the company states its guidance unprompted and repeats it.
- **Candour vs credibility run opposite ways here.** KEC has the highest candour index (31%: misses are explained in the opening remarks) and the lowest delivery. KPIL has the lowest candour (8%) and the highest delivery, but only 24 shortfalls, most of them minor. So candour is not a proxy for credibility. Read it as how a management behaves *after* a miss, and only compare it across companies with a similar number of misses.
- **Credibility decays with the cycle at the weaker two.** FY26-call promises delivered 20-25% at KEC and Skipper, against 53-56% for their FY25-call promises. KPIL barely moved (73% -> 67%). The ratio of FY26-call to FY25-call delivery is a cheap early signal: a management whose newer promises keep missing has not re-based to conditions.

## 5. Rule clarifications adopted (apply to all future companies)
- **A. Late cuts.** A target lowered in the final quarter before its deadline is scored on outcome, not as "withdrawn". "Withdrawn" (-0.5) requires an explicit, explained cut at least two quarters before the deadline (KEC FY27 revenue 12-15% -> 8-10% in Nov-26 qualifies; KEC FY26 margin 8% -> 7-7.5% in Jan-26 does not).
- **B. Ceilings and expansions.** For ceiling targets (interest %, debt, NWC days): delivered if at or below target, partly if the overshoot is <=5%, missed beyond. Margin-expansion targets are scored on the expansion promised in bp from the stated base, not on the margin level, because "89% of an 8% target" otherwise passes a +10 bp result as "partly".
- **C. Adjusted metrics.** When a target is met only on a company-adjusted basis (KPIL standalone PBT 5.9% adjusted vs 4.9% reported), score it delivered but keep it single-source, and show both numbers in `evidence`.
- **D. Silent restatements that are later beaten** (KPIL order inflow 26-28k -> "25k+" -> delivered 26k+) do not change the status, but are logged in `evidence` and counted in the narrative as a candour flag.

## 6. Limits of this calibration
- **Three companies.** Before treating any number here as a base rate, add Transrail Lighting and Techno Electric (and perhaps Bajel / GE Vernova T&D for a product-heavy comparison).
- **Different windows.** Skipper: 10 calls (Jul-24 to Oct-26). KEC: 8 calls (Feb-25 to Nov-26). KPIL: 7 calls (Feb-25 to Aug-26), plus the Nov-26 deck. All three include the FY26 domestic tendering slowdown and the Middle East war, which helps comparability. Skipper's sample includes more FY25 promises (its easier year).
- **Different reading depth.** Skipper was read in full. KEC and KPIL were read as full opening remarks plus keyword-filtered management answers (each answer with >=3 guidance terms, and its question). Vague promises are probably under-counted for the peers, which would, if anything, raise their "vague" buckets. Numeric guidance was unlikely to be missed.
- **Company-reported actuals dominate segment checks.** Group P&L, PBT, finance cost and borrowings direction were cross-checked with screener. Segment, order-inflow and NWC figures are company figures, and some are derived (flagged in `evidence`).
- **Survivorship.** All three are large, listed and still growing. A sector base rate from survivors flatters the sector.

## 7. What to do with this
1. **Re-label Skipper's grade** from "C- in isolation" to "**about sector-median (SAC ~-3)**: above peers on margin, below on order inflow and segment targets". The haircuts in SKIPPER.md section 4 still stand; they are now benchmarked.
2. **Store SAC with every future promise-tracker analysis**, and refresh the peer medians when a new peer is scored (the leave-one-out median changes).
3. **Next scoring targets: Transrail and Techno Electric** (to get n = 5), then refresh all five each quarter using only the new call plus pending items.
4. **Two cheap early-warning signals to automate:** (i) whether FY guidance is volunteered in the prepared remarks (yes/no, each May); (ii) delivery of the latest year's promises vs the year before.

## Sources
See the Sources sections of SKIPPER.md, KEC.md and KPIL.md; all transcripts are company/NSE/BSE PDFs, and screener.in pages were fetched 19-21 Nov 2026.
