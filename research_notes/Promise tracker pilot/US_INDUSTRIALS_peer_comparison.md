# Promise-tracker calibration: US mid-cap industrials / building products (Watts Water, A. O. Smith, Simpson, Lincoln Electric)

*As of 22-Nov-2026. Research, not investment advice. This compares how reliably managements' own forward statements came true, to build a sector base rate and test whether credibility predicts future delivery. It is not a stock ranking and carries no buy/sell view.*

**Roadmap:** stage 3 (is promise credibility a signal?) + stage 7 (rule-generated, dated, scoreable calls). This is the third sector of the credibility-generated forward-call test, and the **first US sector**, after auto components (16 calls) and IT mid-caps (11). **Unlocks:** 11 more calls under the *same* rule, resolving Mar–Jul 2027. 8 of them are machine-resolvable from SEC data (5 structured XBRL, 3 assisted 8-K scans), so the method's Brier(ours) vs Brier(base) can be measured across 38 calls in two markets. Graco, Middleby and Donaldson were not used: Graco guides almost nothing numeric, Middleby is mid-spin-off, and Donaldson's July fiscal year resolves after Jul-2027.

Inputs: `US-WTS.md`, `US-AOS.md`, `US-SSD.md`, `US-LECO.md` (last 6 calls each, Jul-2025 to Nov-2026). Scripts: `scripts_us_industrials/` (`promises_US-*.py` ledgers → `build_seed.py` (the IT/auto scorer; only the tags, the calendar-year label and the category map change) → `make_seed.py` (medians, SAC, base rates; writes `us_summary.json`; same constants and rule) → `make_calls.py` (calls + specs) → `make_md.py`). Seeds: `memdb/seeds/2026-11-22_promises_us_industrials.json` (82 promises, 4 analyses, 1 insight) and `memdb/seeds/2026-11-22_paper_calls_credibility_us.json` (11 theses). Pipeline: v1.3 US vocabulary (`tools/promise_tracker/pipeline/README.md`). Scoreboard: `sec_fact` now also resolves `op_margin_pct` and `capex`.

## 1. Answer in one paragraph
US industrial managements **meet or beat their explicit company-level ranges** almost every time: pooled margin delivery is 93% (n=14) and revenue/growth 71% (n=14). Without A. O. Smith, revenue/growth is 100%. The reason is not foresight. These companies **guide conservatively and raise**: Watts raised at every call (FY2026 organic 2–6% → 8–11% → 11–12%), and Lincoln raised its sales guide twice (mid-single digit → high single digit → low teens). The misses sit in three places. (1) **One company's bad year**: A. O. Smith cut its FY2026 guide three times and sold China. Its Jan-2026 items score *withdrawn*. (2) **International and China sub-lines**: A. O. Smith's China was −12% against −5..−8%. (3) **Capex and plant dates**: pooled capacity delivery is 50% credit and 0% strict (n=4). Simpson's capex came in 0.6% over its range, its Gallatin plant was still ramping after its "fully operational by year-end" date, and A. O. Smith's capex was 6% under. That third pattern is the same one seen in India (T&D, auto components). **But the company scores rest on 6–18 scored promises each, and nearly all FY2026 guidance is pending**, so the rule shrinks hard.

## 2. Scores (same formula as the pilots, auto components and IT)
| | US-WTS | US-AOS | US-SSD | US-LECO |
|---|---|---|---|---|
| Calls read | 6 (5 Fool + Q3-25 release) | 6 (Fool) | 6 (5 Fool + Q2-26 release) | 6 (4 Fool + 2 releases) |
| Promises logged / scored | 22 / 12 | 28 / 18 | 14 / 7 | 18 / 6 |
| Delivery, credit basis (specificity-weighted) | 100% | 65.9% | 79.4% | 88.5% |
| Strict delivery (partly = 0) | 100% | 58.5% | 58.8% | 76.9% |
| MCS (−1.5..+1) | +1.00 | +0.40 | +0.82 | +0.92 |
| Candour (shortfalls admitted unprompted) | n/a (0 shortfalls) | 7/8 | 1/3 | 0/1 |
| What they guide on | organic + reported growth, adj. op/EBITDA margin (bp), next-quarter bands, FCF conversion | EPS range, segment margins, sub-line growth, FCF, buybacks | GAAP op-margin band, capex, tax rate | sales growth in words, segment EBIT bands, capex, cash conversion |
| **SAC (pts vs leave-one-out peers)** | **+15.3** | **−35.3** | **−7.0** | **−11.5** |
| Shrink weight N/(N+20) | 0.375 | 0.474 | 0.259 | 0.231 |
| Effective adjustment to call probability | +5.7 pts | −16.7 | −1.8 | −2.7 |

### By category (credit basis, n in brackets)
| Category | US-WTS | US-AOS | US-SSD | US-LECO | Median of companies | Pooled (credit / strict) |
|---|---|---|---|---|---|---|
| Revenue / growth (group, organic, segment) | 100% (6) | 43% (7) | – | 100% (1) | 100% | 71% / 66% (14) |
| Margin (group + segment) | 100% (5) | 75% (4) | 100% (2) | 100% (3) | 100% | 93% / 93% (14) |
| Capacity (capex, plant dates) | – | 50% (1) | 50% (3) | – | 50% | 50% / 0% (4) |
| Other (EPS, FCF, buybacks, savings, price, M&A) | 100% (1) | 87% (6) | 100% (2) | 75% (2) | 93% | 88% / 83% (11) |

**The L18 rule (≥5 per category, ≥2 peers) is met three times:** WTS revenue and margin, and AOS revenue and other. Everything else is pooled. The peer medians are 100% in most categories, so **any** shortfall produces a negative SAC. That is why Lincoln (88.5%, one partly) gets −11.5. US peer medians are a harder bar than India's.

## 3. Sector-wide vs company-specific

### Sector-wide (don't penalise one company for these)
1. **Conservative ranges, then raises.** Every company except A. O. Smith beat or raised its 2025–26 guidance. A beat is the base case for an explicit US range on a company-level number. **A 100% delivery record here mostly measures how conservative the guide is.** That is the main difference from India, where the same metric mostly measured execution.
2. **Wide bands make "delivered" cheap.** Simpson's 2-point operating-margin band and Lincoln's "mid single digit" words are hard to miss. Specificity weights (range 2, vague 1) only partly correct for this.
3. **Tariffs, steel and price/cost in 2025–26** were named on every call. Price actions held margins (Watts price ~8% in Q1-26; Simpson's 2025 price actions ~$130 mn annualised vs $100 mn; Lincoln "neutral price-cost posture"). A. O. Smith is the exception: steel +15–20% and weak residential volume compressed its North America margin.
4. **Capex and plant timing are the weak point, as in India.** Simpson 2025 capex 0.6% over its range and Gallatin ramp-up late; A. O. Smith 2025 capex 6% under; Lincoln 2026 capex raised from $110–130 mn to $140–150 mn (pending). The sample is small (n=4 scored), but the direction matches T&D and auto components.
5. **Adjusted vs GAAP.** Watts, A. O. Smith and Lincoln guide *adjusted* figures (excluding restructuring and acquisition costs). Simpson guides GAAP (including property-sale gains). The calls resolve each on the basis the company guided: adjusted through an 8-K scan (assisted), GAAP through XBRL (structured).

### Company-specific (these drive the spread)
- **A. O. Smith: delivered 2025, cut 2026 three times.** FY2025 EPS, FCF, segment margins and buybacks all met. FY2026 EPS $3.85–4.15 became $3.70–4.00, then $3.70–3.85, then $3.42–3.52 ex-China. Rest of World margin, water-treatment growth and the China outlook were each cut ≥2 quarters early, so they score *withdrawn*. China missed in both years. Candour is high (cuts explained, 7/8 admitted). The −35 SAC is the only large signal in this set.
- **Watts: the sandbagger.** 12/12 scored promises were beaten, and every next-quarter band was cleared by 3–6 points of organic growth. Data-centre demand did most of the beating in 2026. Under the rule this earns +5.7 points. But Watts's FY2026 growth calls still get only P = 0.47, because the peers' strict revenue rate is 41% (A. O. Smith's misses, with Simpson having no revenue promises).
- **Simpson: few, wide promises.** It met both margin bands. Its capex and the Gallatin plant were near misses (partly). With only 7 scored promises, its score is a placeholder.
- **Lincoln: words, not numbers.** Its near-term Q4-2025 statements were met. It raised the FY2025 cash-conversion floor to ">100%" in Oct-2025, then delivered 97% and did not mention the miss. With 6 scored promises and two of six calls read from press releases only, this is the weakest ledger.

## 4. Splits
- **Volunteered vs prompted:** almost everything is volunteered (US guidance is read from a script). Only A. O. Smith has prompted items (n=2, 50% vs volunteered 68%). Untestable here.
- **Precise vs range vs vague:** A. O. Smith precise 83% / range 55%. Its range-type FY2026 guides were the ones cut. Lincoln is too small to read. There is no monotonic pattern across companies, the same as India. Specificity stays a weight, not a signal.
- **Guidance style:** two companies guide hard numbers (WTS, AOS), one guides a single wide band (SSD), and one guides in words (LECO). Their scores are not directly comparable. The US vocabulary maps "low teens" to 11–13% and "mid single digit" to 4–6% so that the words can be scored.

## 5. Pre-stated rule for credibility-generated calls (REUSED UNCHANGED)
The rule is the one fixed in `AUTO_COMPONENTS_peer_comparison.md` section 5 and reused in `IT_MIDCAPS_peer_comparison.md` section 5. `scripts_us_industrials/make_seed.py` is a copy of `scripts_it_peers/make_seed.py` with the same constants: MIN_N = 5, MIN_POOL = 8, MIN_PEERS = 2, SHRINK_K = 20. It writes the same `adjustment_rule` string to `us_summary.json`. It ran before `make_calls.py` wrote any call, and no probability was typed by hand.

1. Category: revenue_growth, margin, capacity or other. The new US categories map as follows: segment_margin → margin; eps, cash_flow, capital_return, cost_savings and price_cost → other.
2. P(base) = p0 = leave-one-out pooled **strict** delivery of the other three peers in the category, specificity-weighted. If the peers have fewer than 8 scored promises in the category, the all-category peer rate is used. Here this falls back for capacity at every company, and for AOS on revenue and other.
3. SAC_i on the credit basis. Categories with n < 5 or fewer than 2 peers are pooled.
4. P(ours) = clip(p0 + N/(N+20) × SAC/100, 0.05, 0.95).
5. No other adjustment. In-year progress is ignored on purpose. Watts's 9M organic of ~12% and Lincoln's 9M sales of ~+12% are not used.
6. Scoring: Brier(ours) vs Brier(base), for this batch and pooled with the 27 India calls.

Only the category map, the tags and the calendar-year label in `build_seed.py` changed. The scoring constants did not.

## 6. The 11 calls (made 22-Nov-2026; resolve by 15-Mar to 31-Jul-2027)
| Ticker | Call (YES if…) | Cat | P(ours) | P(base) | Resolve by | Type / resolver |
|---|---|---|---|---|---|---|
| US-WTS | FY2026 reported net sales growth ≥17.0% | revenue | 0.47 | 0.41 | 2027-03-15 | a, structured (SEC XBRL revenue_growth_pct) |
| US-WTS | FY2026 adjusted operating margin ≥20.3% | margin | 0.94 | 0.88 | 2027-03-15 | a, assisted (8-K 2.02 scan) |
| US-WTS | FY2026 organic sales growth ≥11.0% | revenue | 0.47 | 0.41 | 2027-03-15 | a, assisted (8-K 2.02 scan) |
| US-AOS | FY2026 adjusted EPS ex-China (continuing ops) ≥$3.42 | other | 0.65 | 0.82 | 2027-03-31 | a, assisted (8-K 2.02 scan) |
| US-AOS | FY2026 net sales growth, continuing ops, ≥3.5% ("≈4%") | revenue | 0.65 | 0.82 | 2027-03-31 | a, structured (XBRL; review if the comparative isn't ex-China) |
| US-AOS | China sale (81% to CPE) closed by 30-Jun-2027 | other | 0.65 | 0.82 | 2027-07-31 | c, assisted (8-K scan) |
| US-SSD | FY2026 GAAP operating margin ≥20.0% | margin | 0.90 | 0.92 | 2027-03-15 | a, structured (XBRL op_margin_pct) |
| US-SSD | FY2026 capex within $80–90 mn | capacity | 0.73 | 0.75 | 2027-03-15 | a, structured (XBRL capex) |
| US-LECO | FY2026 net sales growth ≥11.0% ("low teens") | revenue | 0.60 | 0.63 | 2027-03-15 | a, structured (XBRL revenue_growth_pct) |
| US-LECO | FY2026 capex within $140–150 mn | capacity | 0.69 | 0.71 | 2027-03-15 | a, structured (XBRL capex) |
| US-LECO | FY2026 adjusted operating income margin ≥17.7% (> FY2025 17.6%) | margin | 0.89 | 0.91 | 2027-03-15 | a, assisted (8-K 2.02 scan) |

- 5 structured (SEC XBRL: the resolver decides), 5 assisted type a (8-K Exhibit 99.1 scan proposes a value; a human confirms) and 1 type c event. The three 8-K regexes were tested on the FY2025 Q4 releases with the year swapped. Their first capture was the right full-year figure each time: WTS 19.6% adjusted operating margin, 5% organic; AOS adjusted EPS $3.85; LECO 17.6%.
- **The test has power mainly on A. O. Smith** (−17 pts vs base) **and Watts** (+6). Simpson and Lincoln differ from base by 2–3 pts. Pooled across the three sectors, the power now comes from 5 of 13 companies: Endurance, Sona, Mphasis, A. O. Smith and Watts.
- **Known likely failures of the rule, recorded in advance:** Watts's two FY2026 growth calls (P = 0.47, but the guides are one quarter ahead and 9M organic is ~12%) and Lincoln's sales call (P = 0.60, with 9M ~+12% against an 11% bar). These are the "credibility from past calls vs what has happened this year" cases again. Here, unlike KPIT, in-year data says *more* likely than the rule does. If they resolve YES, Brier(ours) beats Brier(base) on Watts (ours is higher) but loses nothing on Lincoln, where ours is just below base.

## 7. Limits
- **Small n and mostly pending.** 43 of 82 promises are scored, and every FY2026 item is pending. Refresh after the Q4-2026 calls (late Jan–Feb 2027).
- **Reading depth.** The ledgers come from the Motley Fool takeaway lists, the full CFO outlook sections and targeted greps, not a line-by-line read. Quotes marked [Fool summary] are the transcriber's paraphrase. Four of 24 calls were read from 8-K press releases only, because no Fool transcript was found and guessed URLs returned 404. For Lincoln, that leaves two quarters nearly empty.
- **Single-source outcomes.** Organic growth, adjusted margins, segment figures and adjusted EPS come from the companies' own later calls and releases. GAAP revenue, operating income, EPS, capex, FCF, buybacks and dividends were re-derived from SEC XBRL (second source).
- **A. O. Smith's basis change.** China moved to discontinued operations in Q4-2026. Total-company FY2026 promises made before October are scored *withdrawn* or measured ex-China. The structured revenue call checks that the 10-K comparative is ex-China (~$3,155 mn).
- **Peer medians at 100%.** With three peers that rarely miss, one partly-delivered capex promise moves SAC by 5–10 pts. US SAC values are noisier than India's.
- **Survivorship and selection:** four listed, profitable, dividend-paying firms in a 2025–26 data-centre/price upcycle. A downturn sample would look different.

## Sources
Motley Fool call transcripts and SEC 8-K Exhibit 99.1 releases are listed per company in `US-WTS.md`, `US-AOS.md`, `US-SSD.md` and `US-LECO.md` (all fetched 22-Nov-2026). SEC XBRL companyfacts for CIK 795403 (WTS), 91142 (AOS), 920371 (SSD) and 59527 (LECO) were fetched 22-Nov-2026 via `tools/sec_fetch.py facts`.
