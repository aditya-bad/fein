# Promise-tracker calibration: Indian auto components (Uniparts, Sona BLW, Sansera, Happy Forgings, Endurance)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This compares how reliably managements' own forward statements came true, to build a sector base rate and test whether credibility predicts future delivery. It is not a stock ranking and carries no buy/sell view.*

**Roadmap:** stage 3 (is promise credibility a signal?) + stage 7 (rule-generated, dated, scoreable calls). **Unlocks:** when these 16 calls resolve (Feb–Jul 2027), the scoreboard can compare Brier(ours) with Brier(base) for *one method with no judgment in it*. That answers "does the credibility adjustment add skill?" The IT mid-cap sector (Persistent, Coforge, Mphasis, KPIT) is deferred. Its transcripts are already fetched. Coforge files only scanned cover letters on NSE, so its transcripts must come from the company site via `--local`.

Inputs: `SONACOMS.md`, `SANSERA.md`, `HAPPYFORGE.md`, `ENDURANCE.md` (new, last 6 calls each) and `UNIPARTS.md` (19-Nov pilot, 10 calls, statuses as scored then). Scripts: `scripts_auto_peers/` (`promises_*.py` ledgers → `build_seed.py` (the T&D scorer, unchanged except AS_OF and a wider category map) → `make_seed.py` (medians, SAC, base rates; writes `auto_summary.json`) → `make_calls.py` (calls + specs) → `make_md.py`). Seeds: `memdb/seeds/2026-11-22_promises_sectors.json` (74 promises, 4 analyses, 1 insight), `memdb/seeds/2026-11-22_paper_calls_credibility.json` (16 theses).

## 1. Answer in one paragraph
Revenue and margin guidance in this sector is usually met: pooled delivery is 69% on revenue (n=28) and 81% on margin (n=10). **Dates are not.** Capacity, SOP and commissioning promises deliver 43% pooled (n=21), and 1–5-quarter slips occur at four of the five companies. That is the same pattern as T&D (L18), so "dates slip" looks like an Indian-industrial base rate, not a company flaw. Company spread on the credit basis: Sona 83%, Uniparts 65%, Sansera 60%, Happy Forgings 50%, Endurance 26%. **But the four new companies have only 6–9 scored promises each.** Most of their FY27 guidance is still pending, and two of them (Sona, Endurance) refuse to guide revenue at all. So the company-level numbers are weak evidence, and the call rule shrinks them heavily.

## 2. Scores (same formula as the pilots)
| | UNIPARTS | SONACOMS | SANSERA | HAPPYFORGE | ENDURANCE |
|---|---|---|---|---|---|
| Calls read | 10 (pilot) | 6 | 6 | 6 | 6 |
| Promises logged / scored | 68 / 47 | 16 / 6 | 19 / 8 | 19 / 7 | 20 / 9 |
| Delivery, credit basis (specificity-weighted) | 64.8% | 83.3% | 60.0% | 50.0% | 26.1% |
| Strict delivery (partly = 0) | 57.1% | 77.8% | 60.0% | 42.1% | 26.1% |
| MCS (−1.5..+1) | +0.28 (pilot) | +0.70 | +0.33 | +0.08 | −0.81 |
| Candour (shortfalls admitted unprompted) | ~5% | 1/2 | 1/3 | 1/4 | 4/7 |
| What they guide on | revenue, margin, WC, dates | margin band, mix | revenue, ADS segment, capex | margin, volume, capex, dates | SOP dates, capex, order wins |
| **SAC (pts vs leave-one-out peers)** | **−8.1** | **+50.0** | **−4.8** | **+3.6** | **−43.0** |
| Shrink weight N/(N+20) | 0.70 | 0.23 | 0.29 | 0.26 | 0.31 |
| Effective adjustment to call probability | −5.7 pts | +11.6 | −1.4 | +0.9 | −13.3 |

### By category (credit basis, n in brackets)
| Category | UNIPARTS | SONACOMS | SANSERA | HAPPYFORGE | ENDURANCE | Median of companies | Pooled (credit / strict) |
|---|---|---|---|---|---|---|---|
| Revenue growth (group + segment) | 63% (23) | – | 100% (5) | – | – | 81% | 69% / 64% (28) |
| Margin | 85% (5) | 75% (3) | – | 100% (1) | 0% (1) | 80% | 81% / 72% (10) |
| Capacity / capex / SOP dates | 71% (6) | – | 0% (3) | 65% (4) | 27% (8) | 46% | 43% / 39% (21) |
| Other (mix, orders, M&A, returns, WC) | 57% (13) | 90% (3) | – | 0% (2) | – | 57% | 53% / 45% (18) |

**The L18 rule (≥5 per category) is rarely met.** Uniparts meets it in all four categories, Sansera in revenue and Endurance in capacity. Everything else is pooled (section 5). Uniparts supplies 47 of the 77 scored promises, so it dominates the peer pools for the other four. That is a real limitation, not a rounding issue.

## 3. Sector-wide vs company-specific

### Sector-wide (don't penalise one company for these)
1. **Start-of-production and plant dates slip 1–2 quarters.** Endurance: dual-channel ABS 13 months, ABS lines about 2 quarters, Chennai brakes 2 quarters. Sansera: ADS hangar 1 quarter. Happy Forgings: 4,000-t press 1 quarter. Uniparts: Mexico and the fire rebuild (pilot). OEM validation and customer clearance are the usual stated reasons. **Base case for any auto-component SOP date: about one quarter late.** Note that 46% is the median capacity delivery here; T&D's was 36%.
2. **The government's ABS-mandate guidelines** (not yet notified in Nov-26) delayed brake-capacity timing. This hit Endurance directly and is a sector-level factor.
3. **Margin pressure in H1 FY27 from West Asia–linked steel, copper and aluminium prices and freight** was named by Sona, Endurance, Happy Forgings and Uniparts. Margin *bands* were mostly held. Sona openly lowered its band to 23%.
4. **Capex forecasts are revised upward mid-year** at Sansera (FY26 400 → 510 cr; FY27 510 → 800), Endurance (FY27 "much below 800" → 1,100) and Happy Forgings (FY26 ~300 → 460). This is growth capex for new orders. Score it as a forecasting miss, but don't read it as distress.

### Company-specific (these drive the spread)
- **Endurance: date reliability.** About half its SOP re-dates were not explained (Chennai, Bajaj, Chinese OEM). FY26 revenue still grew 26%, so this is a forecasting-discipline issue that has not yet shown up in the P&L.
- **Happy Forgings: the INR 650 cr heavy-component plant.** It went from "finished by Q2–Q3 FY27" (Aug-25) to "commence operation in Q4 FY2028" (Nov-26), while each call said "as per schedule". This is the one clearly silent goalpost move on a core project in the set. Its margin promises, by contrast, are the most reliable in the set.
- **Sansera: delivers revenue, misses capacity forecasts.** Group and ADS revenue were met or beaten; capex and the hangar date were not.
- **Sona: few hard promises, delivered or openly revised.** The +50 SAC rests on six records, partly mechanical (non-auto share rose because railways were consolidated). That is why the shrink weight matters.
- **Uniparts (pilot): revenue guidance below peers.** 63% vs Sansera's 100% in the only other revenue ledger. Its capacity and margin records are above peers. With 10 calls and a cycle trough in its window, it is the only company with a full sample.

## 4. Splits
- **Volunteered vs prompted** (new four; small n): Happy Forgings volunteered 86% vs prompted 0% (n 4/3); Sansera 67% vs 58%; Endurance 20% vs 38%; Sona 79% vs 100%. There is no consistent sign. The T&D finding (volunteered guidance is more reliable) is not confirmed here, and the n is too small to reject it.
- **Precise vs vague:** again no monotonic pattern. Keep specificity as a weight (informativeness), not as an odds signal (same conclusion as T&D).
- **Guidance refusers** (Sona, Endurance) cannot be scored on revenue. A credibility score for them is really a score on mix or date statements. Flag this in any future use.

## 5. Pre-stated rule for credibility-generated calls (fixed before any call was written)
The rule was coded in `make_seed.py` (`adjustment_rule` in `auto_summary.json`) and run before `make_calls.py` wrote any call. Each call's probability is computed by the code from that file. No probability was typed by hand.

1. **Category of the promise:** revenue_growth, margin, capacity (capex / commissioning / SOP), or other.
2. **P(base) = p0** = the leave-one-out pooled **strict** delivery rate of the other four peers' scored promises in that category. Strict means delivered = 1 and partly = 0, because a call resolves YES/NO. The rate is specificity-weighted. If the peers have fewer than 8 scored promises in the category, the all-category peer rate is used instead. Leave-one-out keeps the company's own record out of its own naive base.
3. **SAC_i** (points, credit basis, as in TD_peer_comparison.md section 3) = Σ_c (n_ic / N_i) × (D_ic − median of the other peers' D_c). A category enters on its own only if n_ic ≥ 5 *and* at least 2 peers have scored promises in it. Otherwise the company's small categories are pooled into one bucket and compared with the peers' pooled rate on the same categories.
4. **P(ours) = clip(p0 + N_i/(N_i+20) × SAC_i/100, 0.05, 0.95).** N_i is the company's scored-promise count. The N/(N+20) factor is an empirical-Bayes shrink: six records move a probability about a quarter as much as SAC says, 47 records about 70%.
5. **No other adjustment.** In-year progress (for example Sansera's H1 FY27 +33%) is deliberately *not* used, so these calls isolate the credibility signal. They will therefore look under-confident on items that are already nearly done, and that is part of what the test measures. Judgment calls on the same companies (batch 1: `thesis:paper-call:SONACOMS:q3fy27-opm-23pct-plus`, the Uniparts pilot calls) stay separate.
6. **Scoring:** Brier(ours) vs Brier(base) over the batch (and later, all credibility-generated calls). The method earns weight only if ours beats base out of sample.

## 6. The 16 calls (made 22-Nov-2026; all due by 30-Jun-2027 or confirmed in the call that follows)
| Ticker | Call (YES if…) | Cat | P(ours) | P(base) | Resolve by | Type / resolver |
|---|---|---|---|---|---|---|
| UNIPARTS | FY27 consol revenue growth ≥24.0% | revenue | 0.40 | 0.46 | 2027-05-31 | a, structured |
| UNIPARTS | FY27 consol OPM >20.0% | margin | 0.40 | 0.46 | 2027-05-31 | a, structured |
| SONACOMS | FY27 consol OPM ≥23.0% | margin | 0.63 | 0.51 | 2027-05-31 | a, structured (straddle → review) |
| SONACOMS | JV1 (Denso 2W/3W) completed by 31-Jan-2027 | other | 0.51 | 0.39 | 2027-02-28 | c, assisted |
| SONACOMS | JV2 (Denso HV) closed by 30-Jun-2027 | other | 0.51 | 0.39 | 2027-07-31 | c, assisted |
| SANSERA | FY27 consol revenue growth ≥17.0% | revenue | 0.56 | 0.57 | 2027-05-31 | a, structured |
| SANSERA | FY27 consol OPM >18.4% (better than FY26) | margin | 0.71 | 0.72 | 2027-05-31 | a, structured |
| SANSERA | Nichidai JV commercial production by 31-Mar-2027 | capacity | 0.42 | 0.43 | 2027-06-15 | c, assisted |
| SANSERA | Defence facility operating by 31-Mar-2027 | capacity | 0.42 | 0.43 | 2027-06-15 | c, assisted |
| HAPPYFORGE | FY27 consol revenue growth ≥17.0% (volume-guide proxy) | revenue | 0.65 | 0.64 | 2027-05-31 | a, structured |
| HAPPYFORGE | FY27 consol OPM ≥30.0% | margin | 0.68 | 0.67 | 2027-05-31 | a, structured |
| HAPPYFORGE | ≥INR 450 cr new orders won 6-Nov-26..31-Mar-27 (target ~500) | other | 0.54 | 0.53 | 2027-06-15 | a, assisted |
| ENDURANCE | Tata 4W driveshaft SOP by 31-Dec-2026 | capacity | 0.33 | 0.47 | 2027-02-28 | c, assisted |
| ENDURANCE | Chennai disc-brake plant SOP by 31-Mar-2027 | capacity | 0.33 | 0.47 | 2027-06-15 | c, assisted |
| ENDURANCE | Fifth aluminium forging press SOP by 31-Mar-2027 | capacity | 0.33 | 0.47 | 2027-06-15 | c, assisted |
| ENDURANCE | FY27 driveshaft revenue >INR 100 cr (company-reported) | revenue | 0.51 | 0.64 | 2027-06-30 | a, assisted |

- 7 calls are structured type a (NSE XBRL + screener, the resolver decides). 2 are assisted type a. 7 are type c events (the resolver gathers documents and proposes; a human confirms).
- `specs.json` entries for doc-scan calls set `deadline` = resolve_by, because the confirming document (the next results call) arrives after the event date, and keep `event_deadline` for the rule date.
- The calls where P(ours) and P(base) differ most are Endurance (−13 to −14 pts) and Sona (+12). Those are where the test has power. The Sansera and Happy Forgings calls differ by about 1 pt, so they contribute almost nothing to the "does the adjustment add skill" question.

## 7. Limits
- **Small n for the new four** (6–9 scored each). Most promises from the last three calls are pending; scores will move a lot when FY27 resolves. Refresh after the Q4 FY27 calls (May 2027) using only new calls plus pending items.
- **Uniparts dominates the pools** (47/77 scored), and its window (10 calls, from Jul-24) differs from the others (6 calls, from Aug-25). Its statuses are as of 19-Nov and were not re-scored here.
- **Reading depth:** the new four were read through rule-filtered candidates plus full opening remarks and targeted greps, not line by line. Vague promises are probably under-counted, as in the T&D peers.
- **Single-source outcomes:** segment, SOP, order and capex outcomes come from the companies' own later calls. Group revenue and OPM were re-derived from screener's quarterly table.
- **The strict vs credit split:** P(base) uses the strict rate (binary resolution) and SAC uses the credit rate (pilot convention). This is stated in the rule, and both are stored on every call.
- **Survivorship:** all five are listed, growing companies.

## Sources
NSE transcript PDFs listed in each company file (nsearchives.nseindia.in, fetched 22-Nov-2026); screener.in consolidated pages for SONACOMS, SANSERA, HAPPYFORGE, ENDURANCE, UNIPARTS (fetched 22-Nov-2026); UNIPARTS pilot seed `memdb/seeds/2026-11-19_promises_UNIPARTS.json`.
