# Valuation worksheet and decision card: how to use them, worked examples, design choices, known limits

**Version 1.1 · 2026-11-23** (changelog in §6; v1.0 2026-11-21). Roadmap stages **5 (valuation)** and **6 (decision)**, with the hand-off to
**stage 7 (scorekeeping)**. Each future deep dive (stage 4) ends by filling these two templates, so every company
comes out with the same comparable fields.
**What it unlocks next:** stage 7 gets one dated, mechanically resolvable set of probabilities per decision
(3 paper calls per card), and stage 1 data (Pi/Kite/Screener) can feed the inputs automatically.
**Not stock picking.** The three companies below are **test material (L9). No verdict, no buy/sell/watchlist
call.** Their scenario inputs are illustrative estimates, chosen to exercise the tools. Research, not
SEBI-registered advice.

| Tool | Path |
|---|---|
| Valuation worksheet | `tools/valuation/worksheet.py` (+ `README.md`, `examples/`) |
| Decision card | `tools/decision/decision_card.py`, template `tools/decision/decision_card.md`, `base_rates.json` (+ `README.md`, `examples/`) |
| memdb seed | `memdb/seeds/2026-11-21_templates.json` (strategy records; not yet ingested) |

Both tools use only the standard library (Python 3.7+), so they run on the Raspberry Pi.

---

## 1. How to use (the 20-minute end of every deep dive)
1. **Copy the inputs.** Run `python3 tools/valuation/worksheet.py --template > <T>.json` and fill it from the deep dive.
   - Every figure gets a source tag, and every estimate gets `[EST]` with its method, in `notes`. The two-source rule still applies (stock-research-analyst skill).
   - **Use the economic margin, not the reported one.** That means the pre-Ind AS 116 margin for lease-heavy Indian retailers, the core margin (ex other income) for cash-rich companies, margins after SBC for US filers, and adjusted EPS where a one-off sits in COGS (FIVE's tariff refund).
   - Leave lease liabilities out of `net_debt` when rent is already inside the margin you use. Put treasury income in `treasury_income_post_tax` so the EPS path does not grow it.
2. **Write the scenarios before you look at the price outputs.**
   - Bear/base/bull need growth (year 1 → year N), end margin, ROIIC, exit P/E and a probability. Add a blow-up probability with a one-line story for how it would happen.
   - Anchor the probabilities on the base-rate class first (outside view), then adjust (inside view).
3. **Run the worksheet:** `worksheet.py <T>.json -o <T>_worksheet.md --json <T>_worksheet.json`. Read the blocks in this order:
   1. **(a)** What growth does the price need, is that path self-fundable (feasibility flag), and what IRR does the price offer on the base case?
   2. **(b)** Does the exit P/E used agree with the DCF-consistent P/E at year 5? If not, which one are you betting on?
   3. **(c)** How much of a 3x has to come from re-rating?
   4. **(d)** Where is the P/E against its own history and its peers?
   5. **(e)** Which input moves value the most?
4. **Fill the card input** (`decision_card.py --template`):
   - stage 2: each hard rule pass, fail or unknown, with evidence;
   - stage 3: PEAD quintile and event date, credibility score *and peer median*, detector alerts;
   - stage 4: soft flags and override log, copied from the deep dive's override table;
   - the base-rate class;
   - sizing tier, ADV and portfolio value;
   - dated kill criteria, the pre-mortem and the review date.
5. **Run the card:** `decision_card.py <T>_card.json -o <T>_card.md --calls <T>_calls.json`.
6. **Live (non-practice) cards:** ingest the calls with `python3 -m memdb add --json-file <T>_calls.json` the same day. Rules forbid editing a call after it is made. At the review date, re-run the card with new inputs as a *new* dated card. Never overwrite the old one.

---

## 2. Worked examples (TEST MATERIAL, no verdict)
Inputs: `tools/valuation/examples/{VMM,CUMMINSIND,FIVE}.json` (figures from `research_notes/Deep dives/*_practice.md`).
Cards: `tools/decision/examples/*_card.md`. Paper-call files: `*_paper_calls.json` (**not ingested**).

### 2.1 Stage 5 outputs side by side
| | Vishal Mega Mart | Cummins India | Five Below |
|---|---|---|---|
| Price used | ₹91.5 (20-Nov-2026, screener) | ₹4,100 (21-Nov-2026, screener) | **$220, an estimate from a 13F, not a quote** |
| Trailing P/E | 47.7 | 52.0 | 34.0 (GAAP FY25); 21.8 on the FY26 adjusted-EPS guide midpoint |
| CoE / TG / ROIIC | 12.5% / 5% / 30% | 12.5% / 5% / 40% | 9.5% / 3% / 20% |
| (a) Revenue CAGR the price implies, 10 yrs, margin to base end | **30.0%** | **31.2%** | **17.1%** |
| (a) Year-1 growth fading to TG | 53.7% | 56.2% | 29.9% |
| (a) Margin needed on the base growth path | 20.5% NOPAT (today 6.2%) | none ≤ 60% | 12.4% NOPAT (today 7.2%) |
| (a) IRR the price offers if the base case happens | 8.2% | 7.3% | 7.9% |
| (a) Feasibility flag (reinvestment > 100% of NOPAT) | yes, peak 179% | yes, peak 141% | yes, peak 149% |
| (b) Probability-weighted DCF value vs price | −65% | −69% | −30% |
| (b) DCF-consistent P/E at year 5 (bear/base/bull) | 12 / 15 / 17 | 12 / 13 / 15 | 16 / 18 / 20 |
| (b) Exit P/E used (bear/base/bull) | 25 / 35 / 45 | 30 / 40 / 50 | 14 / 20 / 26 |
| (b) P(≥3x in 5 yrs) / P(≤0.5x) / P(blow-up) | 6% / 5% / 2% | 2% / 2% / 1% | 4% / 14% / 2% |
| (b) EV of 5-yr multiple (EV CAGR) vs hurdle | 1.46x (7.9%) vs 1.76x | 1.33x (5.8%) vs 1.76x | 1.19x (3.6%) vs 1.47x |
| (c) EPS CAGR for 3x at today's P/E | 25% | 25% | 25% |
| (d) Own-history band | insufficient (n=2) | insufficient (no history in file) | insufficient (no history in file) |
| (d) Sector band | cool (0.87x of DMart/V2 median) | normal (0.90x of KOEL) | no peers in file |

### 2.2 Stage 6 cards: mechanical rule outputs (practice, no verdict)
| | VMM | CUMMINSIND | US-FIVE |
|---|---|---|---|
| Stage 2 hard filters | incomplete: H3 and H5 unchecked (H5 = Samayat logistics RPT) | incomplete: H3 unchecked; graded R5 (other income > 30% PBT in FY18–20) fired | passed (7) |
| Stage 3 | no live PEAD quintile; credibility not scored; PE supply detector | no live quintile (Q2 FY27 margin miss is likely bottom-quintile; not computed) | PEAD n/a (India-only test); credibility 75% absolute, **no peer base, so not usable (L18)** |
| Open soft flags | 8 | 7 + 1 graded = 8 (+1 dated watch: royalty renewal 31-Mar-2027) | 6 |
| Variant view written | no | no | no |
| Base-rate class | India 2020–25, mcap ≥ ₹400 cr | same | US IPO 3-yr (a rough left-tail anchor only) |
| P(≥3x): model vs base | 6% vs 44% | 2% vs 44% | 4% vs 7.8% |
| P(≤0.5x): model vs base | 5% vs 2.0% | 2% vs 2.0% | 14% vs 38.5% |
| Full Kelly f* | 0 | 0 | 0 |
| Rule output | size 0 (stage 2 incomplete; 8 open flags without a variant view; EV below hurdle) | size 0 (same three gates) | size 0 (6 open flags without a variant view; EV below hurdle) |

The fictional `SYNTHETIC` card shows the gates-clear path: f* 92%, ¼-Kelly 23%, satellite cap 4%, so the rule size is 4%. A hard-rule fail or a PEAD quintile-1 event forced it to 0 in the code check.

### 2.3 What the examples taught (about the method, not the companies)
1. **At an Indian cost of equity of 12–13%, the DCF calls almost every quality compounder 60–70% overvalued.**
   - The terminal value on these settings is worth ~11–15x NOPAT (`(1 − tg/ROIC)/(r − tg)` = 0.8/0.075 ≈ 10.7x at 25% ROIC), while these stocks trade at 48–52x.
   - So for Indian high-P/E names the **"IRR the price offers"** line (7–8% here, against a 12.5% hurdle) and the reverse-DCF growth line are the useful outputs, not "value −65%".
   - The decision gate uses the 5-year multiple against the index hurdle, not DCF value against price, so the strict CoE alone does not decide the card.
2. **The exit multiple is the hidden bet.** Every Indian scenario's exit P/E (25–50) was 2–3x its DCF-consistent P/E (12–17). The worksheet now prints both and flags the gap. A 5-year multiple that needs the market to keep paying 40x is a bet on market behaviour, and the card should say so.
3. **The base-rate class can be badly biased.** Our only 5-year Indian class (random NSE survivors from Sep-2020, x3 = 44%) started six months after a crash low and ran through a small/mid-cap bull market. Every model probability looked "0.05–0.14x the base rate", and the card flags that departure. Part of the gap is the class's bias, part is the starting P/E (≥35x; `insight:india-mb-starting-pe`). We need a delisting-inclusive, multi-start-date class from stage 1 (see §4).
4. **The soft-flag gate binds first.** All three practice deep dives ended with 6–8 open flags and no variant view. That is consistent with what the deep dives themselves said ("no position without a variant view"). The card makes the rule mechanical.
5. **Unknown hard rules are common.** H3 (rating non-cooperation) was never checked in any practice run, and H5 stayed unresolved at VMM. The protocol needs an explicit stage-2 checklist step before the card (add it to protocol v1.3).
6. **Missing inputs show up.** None of the practice files had an own 10-year P/E history, ADV or a usable FIVE price. A deep dive must now collect: 10 FY-end P/Es, 3+ peer P/Es, 6-month ADV, and a dated close.

---

## 3. Design choices (and why)
| Choice | Why | Alternative rejected |
|---|---|---|
| Value-driver DCF: FCF = NOPAT × (1 − g/ROIIC) | Growth has to be paid for. It links the implied growth to reinvestment × ROIC, which is our high-P/E test (`insight:flag-high-pe-context`). Every number can be re-derived by hand | A full 3-statement model: too many inputs per company, not comparable |
| Equity-level discounting at the cost of equity | Most of our names are low-debt or net cash. One rate keeps it simple; net debt is subtracted | WACC: adds a debt/beta layer we cannot verify per company |
| Margins and growth fade linearly | Readable; a reverse DCF needs one free parameter | S-curves: more parameters, false precision |
| Exit P/E is stated per scenario, next to the DCF-consistent P/E | Twin engine: the multiple *is* half the bet (`insight:twin-engine`, `insight:india-mb-twin-engine-base-rate`); showing both stops the exit multiple hiding | Exit at the DCF value only: ignores how markets actually pay |
| Lognormal spread (σ) around each scenario, blow-up as a point mass | Three point scenarios give lumpy probabilities. A smooth distribution gives P(≥3x) and P(≤0.5x) that can be scored with Brier | Monte Carlo: needs a random seed, is harder to audit, and is not more truthful given opinion inputs |
| Base rates in a separate, versioned file, `null` when unknown | The outside view must be visible next to every probability, and an honest "n/a" beats a borrowed number | Hard-coding numbers inside the card |
| Gates block, notes inform | Hard filters, the PEAD avoid leg, ≥3 open flags without a variant view, EV < hurdle and undated kill criteria each block. The outside-view check only informs (it needs judgment) | One composite score: hides which rule did the work |
| Kelly against the index hurdle, ¼ fraction, then caps | Measures the bet against the real alternative. Full Kelly is absurd with opinion inputs (the synthetic case gives f* 92%), so caps from `strategy:position-sizing` bind | Fixed 2% for everything: ignores the asymmetry and the downside |
| Three 5-year paper calls per card | Makes each decision scoreable without judgment at resolution | One "was it a good decision" grade: unscoreable |
| Practice mode in both tools | L9: test material must never read as a verdict | Separate tools for practice: the templates would drift apart |

---

## 4. Known limits (read before trusting any output)
1. **Garbage in.** Scenario probabilities, ROIIC and exit P/E are opinions. The tool makes them explicit and scoreable; it does not make them right.
2. **The cost-of-equity convention dominates the DCF for Indian stocks** (§2.3.1). Treat DCF value as "what the cash flows justify at our hurdle", not as a price target. The sensitivity table shows the spread: at 10.5% CoE, VMM's base value rises by ~45%.
3. **The EPS path is approximate.** EPS scales with NOPAT + recurring other income, and treasury income is held flat. Buybacks, dilution and changes in interest are not modelled; SBC dilution must be inside the margin.
4. **One growth path per scenario**, with linear fades. Cyclicals (Cummins' margin cycle) need a cycle-aware base year. Use a normalised margin as `nopat_margin`, not the peak.
5. ~~**Base rates are weak.** The India class is survivors-only and bull-biased, the US class is IPOs over 3 years, and blow-up rates are unknown everywhere.~~ *(Superseded 2026-11-23: see §6.)* **Now:** two survivorship-free 5-year classes exist, India non-financial ₹1,000–20,000 cr and US float $0.5–10B (`research_notes/Backtests/base_rates_5y.md`). Their limits are few start dates (2 and 3), no class for banks/NBFCs or large caps, and blow-up without fraud findings. Still to do in **stage 1:** more start dates and starting-P/E buckets.
6. **The 5-year paper calls resolve slowly** (first in Nov-2031). Stage 7 also needs faster feedback, so each live card should add one or two 6–12 month calls (for example on a kill criterion or a reverse-DCF growth check). The v1 card does not generate those automatically.
7. **The PEAD gate is India-only** (card v1.1). US quintiles are shown but never block, because US cut-points are uncalibrated and no US PEAD test exists. **It also depends on the live tracker** (`research_notes/Backtests/india_pead_live/`). Until a company has a computed SUE quintile, the gate reads "unknown, does not block". It is not wired to the tracker's CSV yet.
8. **The credibility gate needs ≥5 promises per category and a peer median (L18).** Without both, it is shown and ignored.
9. **Liquidity cap** needs ADV and portfolio value in the same money units. If they are not supplied, it is skipped (shown as n/a).
10. **US temperature has no market-level base rate on file.** The Nifty bands come from `insight:india-valuation-forward-returns` (data mostly before 2015).
11. **Not wired to memdb metrics yet.** Inputs are typed by hand. Next: a `--from-memdb TICKER` loader once stage-1 snapshots land in `memdb metric`.
12. **Cash tax and incremental ROIC are hand inputs** (v1.3). The annual deferral is not modelled from capex vs tax depreciation; fade it unless persistence is shown. For cyclicals the incremental ROIC needs a full-cycle window with impairments added back.
13. **The exit-multiple bet table is display only.** The EV gate still uses the stated exit P/E, so the scenario author's exit choice remains the single most influential judgment on the card.

---

## 5. Next steps this unlocks
- Protocol v1.3: add an "L8 valuation and decision" step that requires the worksheet, the card, and the extra inputs from §2.3.6 (10-yr P/E, peer P/Es, ADV, dated close, explicit stage-2 H1–H5 statuses).
- Stage 1: compute the base-rate classes in §4.5 and replace the placeholders in `tools/decision/base_rates.json`.
- Stage 7: decide whether practice-card calls enter the scoreboard (recommendation: no; only live cards), and extend the resolver to read `resolution_rule` from `decision-card-v1` calls.
- Wire the PEAD live tracker and the promise-tracker peer medians directly into the card input.

---

## 6. Changelog
**2026-11-23: worksheet v1.3, card v1.1, base rates v2 (lesson L34: every card so far said size 0).**
Goal: fix genuine model gaps without loosening the hurdle or any threshold.
- **Worksheet v1.3**
  - Optional cash tax (`cash_tax_rate` / `deferred_tax_share` / `cash_tax_rate_end`).
  - Reinvestment-realism check (`incremental_roic_5y` or `roic_history`; flags a gap of more than 5 pts, and solves the ROIIC the price implies).
  - An always-on **exit-multiple bet** table: exit P/E used vs DCF-consistent vs own median, and the EV of the 5-year multiple at each.
  - Regression: all 9 example and live inputs give identical numbers when the new inputs are absent.
- **Base rates v2** (`research_notes/Backtests/base_rates_5y.md`) from the survivorship-free stage-2 panels:
  - India ₹1,000–20,000 cr: P(≥3x) **21.3%** [14.1–28.7], P(≤0.5x) **11.3%** [7.0–16.1], P(blow-up) **15.4%** [10.2–21.4], n=208.
  - US float $0.5–10B: **7.0%** [6.0–8.1], **14.2%** [12.7–15.7], **10.9%** [9.6–12.3], n=3,125. Bounds under the other missing-price assumption: 9.8% / 19.9% / 15.3%.
  - The old classes are kept with a `_deprecated` suffix.
- **Card v1.1**
  - PEAD gate: India = bottom two quintiles (L19/L31). US = no gate (uncalibrated; quintile shown).
  - New outputs: base-rate CIs, a size-outside-class warning, and the v1.3 stage-5 lines.
- **Re-run of all 6 cards** (`tools/decision/calibration_2026-11-23/README.md`; no calls written): **all still size 0.**
  - The live cards are blocked only by EV vs hurdle.
  - Kirby's cash tax lifts the probability-weighted DCF from $58.6 to $70–84, but its EV only from 1.12x to 1.16–1.17x (hurdle 1.47x). The binding choice is the exit P/E: the card would clear only at its noisy own-median P/E of 21.5x.
  - Method lesson: every card's P(blow-up) is 0.07–0.18x the new base rate, so our scenario sets under-weight the left tail compared with the outside view.
