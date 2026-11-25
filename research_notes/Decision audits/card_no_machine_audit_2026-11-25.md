# Is the decision card a "no machine"? Stage-6 design audit (2026-11-25)

**Stage:** 6 (decision). **Unlocks:** a pre-registered card change (or none) to evaluate at the first scoring season
(Jan–Feb 2027), so stage 7 tests a gate that can open. **Nothing in the card was changed by this audit.**
Question from `memory/strategy_review.md` §4 and L42: 6/6 live cards are size 0 because the anchored EV of the 5-year
multiple is below the 1.76x hurdle. Is that the market being fair on random draws, or can the card not say yes?

Scripts (run from the repo root, read-only, write nothing): `card_no_machine_audit_2026-11-25_cards.py` (re-runs the six
live cards through card v1.5 in memory and solves for break-evens, plus synthetic firms) and
`card_no_machine_audit_2026-11-25_baserates.py` (multiples in the base-rate panels).

## Short answer
**Partial.** The card *can* say yes to a good company: a firm whose base case earns CoE + 5pp (17.5%/yr in India) gets
anchored EV ≈ 2.0x and the full 4% satellite cap. It cannot say yes to a *fairly priced* firm (base IRR = CoE 12.5%):
anchored EV 1.63–1.66x, size 0. The pass line sits at a **base-case IRR of ~13.8–14.3% (India)**, about 1.3–1.8pp
above CoE — roughly a 6–8% discount to fair value. That is a deliberate-looking margin of safety, but it is not
written anywhere: it comes from two mechanical effects (below), not from a stated rule.
The six live cards are **not** near that line: their *own base cases* return 3–11%/yr, below CoE and below the index,
so the "no" comes mainly from inputs (price vs our base case), not from the mechanics. The closest is HARSHA.
But because the card says no to a fairly priced firm *by construction*, 6/6 zeros carry no evidence either way about
whether the market is fair — the forward scores (stage 7) are the only real test.

## 1. Where 1.76x comes from
- Hurdle = (1 + index CAGR)^5 with India `hurdle` = 12% → **1.12^5 = 1.7623x** (US 8% → 1.4693x;
  `tools/valuation/worksheet.py` `MARKET_DEFAULTS`). It is the index alternative only: **not** the cost of equity
  (12.5%, which would give 1.802x) and **no explicit margin of safety**. Horizon 5 years.
- Card multiples include dividends (`cum_dist_ps_5y`) and the hurdle is meant as index total return — consistent. The
  base-rate R5 for India is price only (dividends ~1–2%/yr excluded), so the class rows below *understate* pass rates a little.

Share of each base-rate class that actually reached the hurdle over 5 years (survivorship-free panels; failed-and-unpriced
rows counted as 0x, not-failed-unpriced excluded; India non-fin stratum-weighted as in `base_rates_5y.md`):

| Class | n | Median | Mean | P(≥1.76x) | P(≥1.47x) | P(≥1x) |
|---|---|---|---|---|---|---|
| India non-fin ₹1k–20k cr, both starts | 205 | 1.69x | 2.24x | **49.6%** | 57.8% | 77.0% |
| — 2016 start | 105 | 1.47x | 1.97x | 39.2% | 48.3% | 70.6% |
| — 2018 start | 100 | 2.02x | 2.48x | 59.1% | 66.4% | 82.8% |
| India lenders ₹1k–20k cr | 107 | 1.04x | 1.49x | **33.6%** | 43.0% | 51.4% |
| US float $0.5–10B (unpriced acquisitions excluded) | 2,226 | 1.16x | 1.49x | 28.4% | **38.2%** | 58.2% |

So the hurdle is **consistent with the classes**: India non-fin median 1.69x sits just under 1.76x (a random draw is a
coin flip to beat it), lenders (median 1.04x) mostly fail it, US (vs its own 1.47x hurdle) mostly fails it. The hurdle is
not set too high. Note the class **mean** (2.24x India non-fin) is well above the hurdle — the realised distribution is
right-skewed (median 1.69x, log-SD ~0.68 robust / ~1.0 raw). Caveat: two start dates in a strong small-cap window;
read the mean as history, not a forecast.

## 2. Mechanics: what pulls EV down
Re-derived from `decision_card.py` v1.5 (`_outcomes_tagged`, `anchor_outcomes`, `_kelly`) and `worksheet.py`
`scenario_analysis`.

**(a) Mean/median inconsistency (≈ −σ²/2 ≈ −4.5% to −8%).** The worksheet's P(≥3x), P(≤0.5x), the outcome
distribution and Kelly all centre each scenario's lognormal on `mult5` (i.e. `mult5` is the *median*, mean = `mult5`·e^{σ²/2},
+6.3% at σ=0.35, +8.3% at σ=0.40). The EV gate treats `mult5` as the *mean* (`ev_mult5 = Σ p·mult5`). Consequence: on every
card Kelly turns positive *before* the EV gate passes (below), i.e. the card's own outcome distribution says "beats the
index" in a zone where the gate says no. Fair firm, card-shaped: Kelly opens at base IRR 12.8% (≥1% size at 13.1%), EV gate
at 14.3%.

**(b) One-sided anchoring (≈ −0.09 to −0.14x on a clean firm).** Anchoring imports the class *left* tails (blow-up 15.4%,
≤0.5x 11.3%, at w = 0.5) and takes the mass proportionally from everything above 0.5x — including the right tail. P(≥3x)
is not anchored. The class whose left tail we import has a fat right tail (P(≥3x) 21%, mean 2.24x); we do not import that.
Model P(≥3x) on the live cards is 0.4–10% vs the 21% base (0.02–0.48× the base rate). On a single-scenario fair firm with
no model blow-up, anchoring alone moves EV 1.80x → 1.66x.

**(c) Scenario shape (analyst input, not code).** All six cards put more probability on bear than bull (bear 0.20–0.35,
bull 0.15–0.20), plus a blow-up, so the scenario mean sits *below* the base case. Real 5-year outcomes are right-skewed.
This is a judgement pattern worth tracking, not a bug.

σ itself (0.30–0.40) does not lower the EV gate (EV uses `mult5` as the mean) but it is about half the class's realised
dispersion, which keeps the model's P(≥3x) far below base and lowers Kelly.

**Survival rules** (PEAD gate, survival cap) do not touch EV; they only cap or zero size after the gate. None of the six
is blocked by them except INDRAMEDCO, where the v1.4 core-asset trigger would cap size at ≤1% even if EV passed.

Synthetic firms (India, hurdle 1.762x, base-rate class india_nonfin, w = 0.5, Kelly fraction 0.25, satellite cap 4%):

| Firm | Shape | Base IRR | Raw EV | Anchored EV | Full Kelly f* | Size | Min base IRR to pass EV gate |
|---|---|---|---|---|---|---|---|
| Index-like | card-shaped (bear .25 @0.65×base, base .5, bull .2 @1.45×, blow-up 5% @0.1x) | 12.0% | 1.68x | 1.60x | 0 | 0 | 14.3% |
| Fairly priced | card-shaped | 12.5% (=CoE) | 1.72x | **1.63x** | 0 | **0** | 14.3% |
| Fairly priced | single scenario, σ 0.35, no model blow-up | 12.5% | 1.80x | 1.66x | 3.7% | 0 (EV gate) | 13.8% |
| Fairly priced | same, no anchoring | 12.5% | 1.80x | 1.80x | 68.6% | 4% | 12.0% (= hurdle) |
| Good (CoE+5pp) | card-shaped | 17.5% | 2.14x | **2.02x** | 48.7% | **4% (cap)** | 14.3% |
| Good (CoE+5pp) | single scenario | 17.5% | 2.24x | 2.06x | 65.9% | 4% (cap) | 13.8% |

Reading: without anchoring the gate is exactly "base IRR ≥ index 12%". Anchoring + the mean/median convention + card
shape add ~1.8–2.3pp, putting the line at ~14% — above CoE. A good firm clears it easily; a fair one never does.

## 3. The six live cards — what would have flipped them
Re-run in memory under card v1.5 (no files written). Break-even = scale all scenario multiples by k (equivalently the
price falls by 1 − 1/k), anchoring recomputed at each k.

| Card | Class used | Anchored EV vs hurdle | Our base-case IRR | Base IRR needed for EV gate | Price fall for EV gate | Price fall for ≥1% Kelly size | Gap |
|---|---|---|---|---|---|---|---|
| HARSHA | india_nonfin | 1.58x vs 1.76x | 10.4% | 13.9% | −14% | −8% | **smallest** |
| SUNFLAG* | survivors (deprecated) | 1.44x vs 1.76x | 9.0% | 14.6% | −22% | −13% | large |
| INDRAMEDCO | india_nonfin, w 0.3 | 1.39x vs 1.76x | 11.2% | 16.1% | −19% | −18% | large (and survival cap ≤1%) |
| AUTOAXLES | india_nonfin, w 0.6 | 1.40x vs 1.76x | 9.9% | 15.2% | −21% | −17% | large |
| US-KEX* | us_seasoned (deprecated, all null → no anchoring) | 1.12x vs 1.47x | 3.0% | 8.8% | −24% | −21% | large |
| UTKARSHBNK* | india_lender (v1.5) | 1.23x vs 1.76x | 7.9% | 16.8% | −33% | −30% | very large |

\* Re-run differs from the dated card: SUNFLAG card (v1.1) printed 1.38x (no anchoring; the deprecated class's thin 2% ≤0.5x
tail *raises* EV under v1.2+); UTKARSHBNK card printed 1.29x (non-fin class; the v1.5 lender class lowers it); US-KEX names a
null deprecated class although `us_float_500m_10b_5y` exists. Per L41 follow-up the dated cards are not re-issued.

Scenario levers: at each firm's **own historical median exit P/E** (worksheet exit-bet table, raw, pre-anchoring) AUTOAXLES
would be 1.73x and US-KEX 1.45x — within ~2% of their hurdles; the exit multiple is again the binding bet (L21). At the
DCF-consistent exit P/E every card falls further (0.73–1.42x).

Every live base case is below CoE (3–11%/yr), i.e. even if our base case happens these stocks lag the index. The gaps are
14–33% of price for the gate — not a rounding issue. Mechanics explain ~2pp of required IRR; the cards are 3.5–9pp short.

## 4. Conclusion
**Structural bias: partial.**
- *Not* a no-machine: a good firm (CoE+5pp) passes at full cap; the hurdle matches the class (≈ class median).
- *But* the effective pass line is ~14% base IRR, not the stated 12% hurdle, because of (a) an internal mean/median
  inconsistency and (b) left-tail-only anchoring — neither is a declared margin of safety. A fairly priced name always gets 0.
- The six zeros are mostly **genuine** on our own inputs (base cases below CoE; gaps 14–33% of price). The mechanics do not
  explain them. HARSHA is the only one where the mechanics are a large share of the gap.
- Because fair = 0 by construction, "6/6 zeros" cannot discriminate "market fair" from "card biased". Only stage-7 scoring can.
  Also note the sample is not random: these were chosen as candidates, several from expensive sectors.

## 5. Candidate fixes — NOT applied; pre-register before the Jan–Feb 2027 scoring season
Any change must be written down (prereg) before that season and judged on the scored calls, not on these 6 names.
1. **Make the EV convention consistent** (pick one): treat `mult5` as the median everywhere (EV gate uses the GH mean, as
   Kelly does) or as the mean everywhere (shift the lognormal by −σ²/2). Pure correctness fix; it moves the pass line ~0.5–1pp.
2. **State the margin of safety explicitly** if we want one (e.g. hurdle = CoE^5 or index + Xpp) instead of getting it by
   accident from the mechanics.
3. **Two-sided anchoring**: anchor P(≥3x) toward the class too (or anchor the whole distribution to the class quantiles),
   so we do not import the left tail alone. Paper calls already keep raw vs anchored, so Brier can judge this.
4. **Widen σ toward the class dispersion** (realised log-SD ~0.68 robust) unless the deep dive argues for less — affects
   P(≥3x) and Kelly, not the EV gate.
5. **Scenario-shape check**: flag when bear-prob > bull-prob *and* the scenario mean is below the base case, asking for the
   evidence (track as a stage-7 calibration question: are our bear weights too high?).
6. **Housekeeping (no threshold change)**: cards that name a deprecated class with null tails (US-KEX) should warn; the
   default for new US cards is `us_float_500m_10b_5y`.

Test to pre-register (suggested): on calls scored Jan–Feb 2027 and later, compare realised 5-yr outcomes (when available) and
interim Brier of raw vs anchored vs two-sided-anchored tails; adopt 1 only as a correctness fix (no data needed), adopt 2–4
only if they improve Brier/log-score on the scored set. Never change the hurdle to make cards open (L34).

_Research, not SEBI-registered advice._ Sources: `tools/decision/decision_card.py` v1.5, `tools/valuation/worksheet.py`,
`tools/decision/base_rates.json` v3, `research_notes/Backtests/solvency_india_outputs/panel.csv`,
`research_notes/Backtests/base_rates_lenders_india_outputs/panel.csv`, `research_notes/Backtests/solvency_us_outputs/panel.csv`,
`tools/decision/live/*_card.json`.
