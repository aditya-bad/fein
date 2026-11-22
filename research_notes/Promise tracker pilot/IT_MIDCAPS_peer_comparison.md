# Promise-tracker calibration: Indian IT mid-caps (Persistent, Coforge, Mphasis, KPIT)

*As of 22-Nov-2026. Research, not SEBI-registered advice. This compares how reliably managements' own forward statements came true, to build a sector base rate and test whether credibility predicts future delivery. It is not a stock ranking and carries no buy/sell view.*

**Roadmap:** stage 3 (is promise credibility a signal?) + stage 7 (rule-generated, dated, scoreable calls). This is the second sector of the credibility-generated forward-call test, after auto components. **Unlocks:** 11 more calls that resolve Feb–Jun 2027 under the *same* rule, so the method's Brier(ours) vs Brier(base) is measured across two sectors (27 calls), not one. LTTS was not added (budget); it is the next IT company to run.

Inputs: `PERSISTENT.md`, `COFORGE.md`, `MPHASIS.md`, `KPITTECH.md` (last 6 calls each). Scripts: `scripts_it_peers/` (`promises_*.py` ledgers → `build_seed.py` (the auto-components scorer; only the tags and the category map change) → `make_seed.py` (medians, SAC, base rates; writes `it_summary.json`; same constants and rule) → `make_calls.py` (calls + specs) → `make_md.py`). Seeds: `memdb/seeds/2026-11-22_promises_it.json` (63 promises, 4 analyses, 1 insight), `memdb/seeds/2026-11-22_paper_calls_credibility_it.json` (11 theses). Pipeline: v1.2 IT vocabulary (CC growth, TCV, EBIT band; see `tools/promise_tracker/pipeline/README.md`).

## 1. Answer in one paragraph
IT mid-cap managements almost always hit their **near-term margin guidance**: pooled delivery 98% (n=8). That covers EBIT/EBITDA bands, quarter-ahead margin walks and FY margin targets. These are levers management controls (utilisation, sub-contracting, ESOP cost, hedges). **Growth-shape, vertical and timing statements are much weaker:** 69% on revenue/growth (n=11, the same as auto components' 69%) and 82% on "other" (n=8). The other category covers DSO, tax rate, FCF, M&A dates and deal counts. The misses: Mphasis's Logistics recovery and DSO normalisation, Coforge's "robust H2" and Cigniti date, KPIT's "meaningful" Q4. **But the scores look better than the sector really is, because the big FY27 tests are all pending.** KPIT guided FY27 EBITDA at 20.5–21.2% in May-2026 and printed 17.2% and 17.8% in the next two quarters. Persistent re-cast "USD 2 bn revenue by FY27" as a Q4 exit run rate, and "+200–300 bp" as "16–17%", without saying either had changed. With 4–10 scored promises per company, the call rule shrinks everything hard. Only Mphasis gets a noticeable adjustment (−8 pts).

## 2. Scores (same formula as the pilots and auto components)
| | PERSISTENT | COFORGE | MPHASIS | KPITTECH |
|---|---|---|---|---|
| Calls read | 6 (no Q1FY27 call held; Jun-26 Nagarro call used) | 6 (website PDFs) | 6 | 6 |
| Promises logged / scored | 15 / 4 | 20 / 10 | 16 / 8 | 12 / 5 |
| Delivery, credit basis (specificity-weighted) | 100% | 85.0% | 58.3% | 95.5% |
| Strict delivery (partly = 0) | 100% | 70.0% | 58.3% | 90.9% |
| MCS (−1.5..+1) | +1.00 | +0.88 | +0.20 | +0.96 |
| Candour (shortfalls admitted unprompted) | n/a (0 shortfalls) | 2/4 | 1/3 | 0/1 |
| What they guide on | nothing formally; aspirations, tax rate, margin walk | EBIT, EBITDA, FCF/PAT, ETR, deal counts | CC growth range, EBIT band, OCF/NI | EBITDA, growth shape (H2 > H1, Q4) |
| **SAC (pts vs leave-one-out peers)** | **+13.9** | **+12.6** | **−28.5** | **+6.6** |
| Shrink weight N/(N+20) | 0.17 | 0.33 | 0.29 | 0.20 |
| Effective adjustment to call probability | +2.3 pts | +4.2 | −8.1 | +1.3 |

### By category (credit basis, n in brackets)
| Category | PERSISTENT | COFORGE | MPHASIS | KPITTECH | Median of companies | Pooled (credit / strict) |
|---|---|---|---|---|---|---|
| Revenue / growth (group, CC, vertical, shape) | – | 75% (2) | 56% (6) | 90% (3) | 75% | 69% / 63% (11) |
| Margin (EBIT/EBITDA bands, walks) | 100% (2) | 93% (3) | 100% (1) | 100% (2) | 100% | 98% / 95% (8) |
| Capacity | – | – | – | – | – | none (IT has no capacity promises) |
| Other (DSO, ETR, FCF, M&A, deals, wage timing) | 100% (2) | 82% (5) | 0% (1) | – | 82% | 82% / 71% (8) |

**The L18 rule (≥5 per category) is met twice:** Coforge "other" (n=5) and Mphasis revenue (n=6). Everything else is pooled. That is weaker than auto components, where Uniparts had a full pilot sample. **No company here has a full sample.**

## 3. Sector-wide vs company-specific

### Sector-wide (don't penalise one company for these)
1. **Margin bands are reliable, growth-shape talk is not.** Every company met its FY26 margin guidance: Persistent +90 bp vs ~+100 bp, Coforge 14.4% vs 14%, Mphasis 15.3% in its band, KPIT 20.8% vs 21%. Statements about *when* growth comes back ("robust H2", "meaningful Q4", vertical recoveries) met about two-thirds of the time. **Base case for an IT "growth returns next quarter / in H2" statement: about a coin-flip-plus. For a margin band: near-certain unless revenue falls.**
2. **The New Labour Code one-time charge (Q3FY26)** hit Persistent (230 bp) and Mphasis (INR 355 mn exceptional). Score on the adjusted basis (clarification C).
3. **Wage hikes in Q2/Q3** cost 150–180 bp every year at every company. They are always guided and always roughly as guided.
4. **Company EBIT/EBITDA ≠ screener.** Screener-derived (OP − depreciation)/sales is within 0.1 pp of company EBIT only for Mphasis. Persistent FY26 is 16.2% vs 15.6%, and Q2FY27 is 10.0% vs 15.0% because of Nagarro transaction costs. Coforge FY26 is 13.7% vs 14.4% (hedge reclassification). KPIT EBITDA is 20.8% vs 18.9% OPM. **IT margin calls must be resolved on the company figure (assisted), not the structured screener path.** This is the reason the new `ebit_margin_pct` measure takes a CSV override.
5. **Acquisitions blur growth promises.** Encora (Coforge, from May-26), Nagarro (Persistent, ~Dec-26/Jan-27), TAP/Red Oak (Mphasis) and Caresoft (KPIT) all inflate reported growth. Promises made before a deal have to be scored on an organic basis, or voided.

### Company-specific (these drive the spread)
- **Mphasis: company-level guidance met; vertical and working-capital promises missed.** Logistics was re-dated "rest of FY26" → "from Q3" → "through FY27" and then fell 12% QoQ (moved-goalpost). DSO "normalise in 3–4 quarters" went 89 → 105 days. This is the only company with a negative SAC.
- **Coforge: explicit, frequent, mostly met.** It is the only real guider in the set. Its misses are softer statements and one regulator-driven date (Cigniti). Guidance is raised often (EBIT 15.5% → 16%, FCF/PAT 70–80% → 100%). In the upgrades so far, the raised number was already in hand when it was announced.
- **Persistent: no formal guidance, quiet re-framing of the big aspirations.** Its near-term statements are perfect (n=4). The two FY27 aspirations (USD 2 bn; 200–300 bp) were both re-defined without being acknowledged as changed. If FY27 misses them, the likely statuses are moved-goalpost, not missed.
- **KPIT: the FY26 record is clean; the FY27 guide looks broken.** A 20.5–21.2% EBITDA guide was given just before a two-programme ramp-down took margins to 17.2–17.8%. The CEO now says margin recovery comes "early next year". This is the strongest single test of the rule: P(ours) = 0.75 on a call that in-year data says is unlikely.

## 4. Splits
- **Volunteered vs prompted:** Coforge 100% volunteered (n=2) vs 79% prompted (n=8). Mphasis 50% volunteered (n=6) vs 100% prompted (n=2). There is no consistent sign, as in auto components. Too small to test.
- **Precise vs vague:** Coforge precise 100% / range 75% / vague 67%. KPIT precise 100% / vague 75%. Mphasis's one precise promise (Logistics "from Q3") missed. Weakly in the expected direction for two of three companies; specificity stays a weight, not a signal.
- **Guidance refusers:** Persistent ("we don't give forward-looking guidance") and, since FY25, KPIT on revenue. Their scores rest on aspirations and growth-shape statements, so read their 95–100% scores with that in mind.

## 5. Pre-stated rule for credibility-generated calls (REUSED UNCHANGED)
The rule is the one fixed in `AUTO_COMPONENTS_peer_comparison.md` section 5, coded in `scripts_auto_peers/make_seed.py`. `scripts_it_peers/make_seed.py` is a copy with the same constants: MIN_N = 5, MIN_POOL = 8, MIN_PEERS = 2, SHRINK_K = 20. It writes the same `adjustment_rule` string to `it_summary.json`. It ran before `make_calls.py` wrote any call, and no probability was typed by hand.

1. Category: revenue_growth, margin, capacity, or other. The new IT categories deal_wins, people and client_concentration map to "other".
2. P(base) = p0 = leave-one-out pooled **strict** delivery of the other three peers in that category, specificity-weighted. If the peers have fewer than 8 scored promises in the category, the all-category peer rate is used. In IT this falls back for margin and other at most companies (peer n = 3–8), and for revenue at Mphasis.
3. SAC_i on the credit basis. Categories with n < 5 or fewer than 2 peers are pooled.
4. P(ours) = clip(p0 + N/(N+20) × SAC/100, 0.05, 0.95).
5. No other adjustment. In-year progress is ignored on purpose (KPIT H1 EBITDA, Coforge H1 EBIT).
6. Scoring: Brier(ours) vs Brier(base), for this batch and pooled with the 16 auto-components calls.

The only code change was a `None` guard: IT has no capacity promises, so the capacity median is empty. It does not change any number for a category that has data.

## 6. The 11 calls (made 22-Nov-2026; resolve by 28-Feb to 30-Jun-2027)
| Ticker | Call (YES if…) | Cat | P(ours) | P(base) | Resolve by | Type / resolver |
|---|---|---|---|---|---|---|
| PERSISTENT | FY27 consol EBIT margin (company) ≥16.0% | margin | 0.74 | 0.72 | 2027-05-31 | a, assisted |
| PERSISTENT | Q4FY27 revenue ex-Nagarro ≥USD 500 mn (void if not disclosed when consolidated) | revenue | 0.65 | 0.62 | 2027-06-30 | a, assisted |
| COFORGE | FY27 consol EBIT (company) ≥16.0% | margin | 0.86 | 0.82 | 2027-05-31 | a, assisted |
| COFORGE | FY27 consol EBITDA (company) ≥20.5% | margin | 0.86 | 0.82 | 2027-05-31 | a, assisted |
| COFORGE | ≥8 large deals signed in Q3FY27 | other | 0.86 | 0.82 | 2027-02-28 | a, assisted |
| MPHASIS | FY27 CC revenue growth ≥10.0% | revenue | 0.75 | 0.83 | 2027-05-31 | a, assisted |
| MPHASIS | FY27 EBIT within 14.75–15.75% | margin | 0.75 | 0.83 | 2027-05-31 | a, assisted (between) |
| MPHASIS | Q3FY27 reported DSO ≤99 days | other | 0.75 | 0.83 | 2027-02-28 | a, assisted |
| KPITTECH | FY27 EBITDA (company) ≥20.5% | margin | 0.75 | 0.74 | 2027-05-31 | a, assisted |
| KPITTECH | FY27 consol revenue > INR 6,732 cr (= H2 > H1) | revenue | 0.56 | 0.55 | 2027-05-31 | a, structured |
| KPITTECH | Q4FY27 CC revenue QoQ > 0% | revenue | 0.56 | 0.55 | 2027-05-31 | a, assisted |

- 1 structured (NSE XBRL + screener) and 10 assisted calls. IT KPIs are company-defined, so the resolver proposes and a human confirms. Coforge's transcripts are only on investors.coforge.com, but its results releases and factsheets are on NSE, so `doc_scan` with source `nse` still finds the numbers.
- **The test has power mainly on Mphasis** (−8 pts vs base). Persistent, Coforge and KPIT differ from base by 1–4 pts. Pooled with auto components, the method's power still comes from 3 of 9 companies (Endurance, Sona, Mphasis).
- **Known likely failures of the rule, recorded in advance:** KPIT FY27 EBITDA (P = 0.75 against an H1 of 17.5%). Possibly Mphasis's EBIT band (H1 at the floor; P = 0.75 is *below* base here, so a miss would favour ours). These are exactly the cases where "credibility from past calls" and "what has happened this year" disagree.
- Persistent's Nagarro closing is not duplicated. It has a batch-2 judgment call (`thesis:paper-call:PERSISTENT:nagarro-deal-closes-by-mar27`).

## 7. Limits
- **Small n and mostly pending.** 27 of 63 promises are scored. Every FY27 item is pending. Refresh after the Q4 FY27 calls (Apr–May 2027).
- **Reading depth.** The ledgers come from opening remarks in full plus targeted greps, not a line-by-line read. `turns.py` failed on Mphasis's layout and needed a roster for Persistent. Vague promises are probably under-counted.
- **Single-source outcomes.** CC growth, company EBIT/EBITDA, DSO, deal counts and vertical growth come from the companies' own later calls. INR revenue and screener-derived margins were re-computed as a cross-check only.
- **Persistent has no Q1FY27 call.** Its window includes the Nagarro deal call instead.
- **"Industry growth"** (Mphasis's 2x claim) is the company's own benchmark.
- **Survivorship:** four listed, scaled firms. LTTS is not included.

## Sources
Transcripts listed in each company file: NSE nsearchives for Persistent (except Q4FY26: persistent.com), Mphasis and KPIT; investors.coforge.com for all six Coforge calls. All fetched 22-Nov-2026. Screener.in consolidated pages for PERSISTENT, COFORGE, MPHASIS and KPITTECH were fetched 22-Nov-2026 via `financials.py`.
