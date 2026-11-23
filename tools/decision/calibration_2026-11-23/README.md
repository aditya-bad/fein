# Gate calibration re-run, 2026-11-23 (lesson L34; roadmap stages 5–6)

All 6 cards (4 practice, 2 live) were re-run with worksheet v1.3, card v1.1 and base_rates v2. **Nothing here is a new
decision:** no paper-call files were written (`decision_card.py` was run without `--calls`). The live SUNFLAG and
US-KEX cards and their 18 calls stand as made, and the practice cards stay out of the scoreboard. The hurdle and every
gate threshold are unchanged.

Inputs: each `*_card.json` here is a copy of the original card with only `base_rate_class` (and the worksheet path)
changed. `US-KEX_v13.json` adds the v1.3 inputs to Kirby's worksheet: cash tax and incremental ROIC, both added after
the outputs and documented in its notes. `US-KEX_v13_persistent.json` is the upper bound (cash tax at 7.9% forever).

| Card | Base-rate class: old → new | Base P(≥3x) / P(≤0.5x) / P(blow-up) | Model | EV vs hurdle | EV if every scenario exited at the DCF P/E / own-median P/E | Size | Blocked by |
|---|---|---|---|---|---|---|---|
| VMM (practice) | India survivors 2020–25 → India ₹1,000–20,000 cr (**size outside class**, ₹42,849 cr) | 21% / 11% / 15% (was 44% / 2% / n/a) | 6% / 5% / 2% | 1.46x vs 1.76x | 0.62x / n/a | 0 | H3+H5 unchecked; 8 open flags, no variant view; EV |
| CUMMINSIND (practice) | same (**size outside class**, ₹113,652 cr) | 21% / 11% / 15% | 2% / 2% / 1% | 1.33x vs 1.76x | 0.49x / n/a | 0 | H3 unchecked; 8 open flags; EV |
| FIVE (practice) | US IPO 3-yr → US float $0.5–10B (**size outside class**, $12.2B) | 7.0% / 14.2% / 10.9% (was 7.8% / 38.5% / n/a, 3-yr IPOs) | 4% / 14% / 2% | 1.19x vs 1.47x | 1.04x / n/a | 0 | 6 open flags; EV |
| FEDERALBNK (practice) | India survivors → **none** (no bank class) | n/a | 3% / 3% / 2% | 1.36x vs 1.76x | (bank mode: no P/E bet table) | 0 | 11 open flags; EV |
| SUNFLAG (live) | India survivors → India ₹1,000–20,000 cr | 21% / 11% / 15% | 6% / 8% / 2% | 1.38x vs 1.76x | 1.42x / 1.30x | 0 | EV only |
| US-KEX (live) | US placeholder (n/a) → US float $0.5–10B | 7.0% / 14.2% / 10.9% | 1% / 3% / 2% | **1.12x → 1.16x** (cash tax fading) / 1.17x (persistent) vs 1.47x | 0.94x (1.12x persistent) / **1.50x** | 0 | EV only |

## What changed and why
1. **Base rates are honest now, and the model's departures are clearer.** India P(≥3x) falls from 44% to 21%, so the
   Indian cards' "0.05–0.14x the base rate" becomes 0.10–0.30x. Loss tails now exist: P(≤0.5x) is 11% in India and
   14% in the US. Blow-up base rates of 15% and 11% sit far above the 1–2% every card assumed. **That is the
   biggest calibration finding:** our scenario sets consistently under-weight the left tail compared with the
   outside view (P(blow-up) 0.07–0.18x the base rate on every card). For the live cards the calls are already made,
   and Brier scoring will show whether that confidence was earned.
2. **Cash tax (Kirby) closes most of the DCF gap but not the EV gap.** With the deferral fading, the probability-weighted
   DCF value goes from $58.6 to $70.4/share, and to $84.4 if the deferral persists. The DCF-consistent P/E rises from
   8.6/10.8/12.7 to 10.0/12.3/14.4 (12.3/15.1/17.7 persistent), and the margin the price needs falls from 21.7% to
   18.7% (15.6%). The EV gate barely moves (1.12x → 1.16–1.17x), because the 5-year multiple is book EPS × exit P/E
   plus 75% of FCF paid out, and the cash-tax benefit only enters through that payout. So the gap that blocked Kirby
   was never the DCF. It was the pre-registered exit P/Es of 13/16/19 on 4–9% EPS growth.
3. **The exit-multiple bet line makes the remaining choice visible.** At Kirby's own 10-year median P/E (21.5, a noisy
   series) the EV would be 1.50x, just above the 1.47x hurdle. Opening the card would need a bet that the market pays
   about 21x for a business earning roughly its cost of capital near a cyclical peak. The deep dive said no to that
   before seeing any output, so the card stays closed. At SUNFLAG the bet is small: the DCF-consistent and own-median
   exits give 1.42x and 1.30x, both below the 1.76x hurdle. For VMM and CUMMINSIND, EV at the DCF exit is 0.5–0.6x: their
   stated EVs rest entirely on the market keeping 35–50x multiples.
4. **Reinvestment realism (Kirby):** cross-cycle incremental ROIC is 11.7%, and the scenario ROIICs (7/10/13%) are
   within 5 pts, so no flag. No ROIIC up to 300% reproduces the price on the base growth/margin path, so the price
   rests on margin or the exit multiple, not on capital efficiency. The 2022→25 window alone would say 128% (cycle
   recovery on flat capital), so the window has to span a full cycle.
5. **PEAD:** no card changes. Kirby's US quintile 5 is now labelled "not gated (US uncalibrated)" and does not block.
   India keeps the bottom-two-quintile gate.

## Does any card open?
**No. All 6 stay at size 0.** The two live cards are blocked only by the EV hurdle, and no genuine model gap remains
that would move them above it. The practice cards are also blocked by incomplete stage-2 checks and by ≥3 open flags
without a variant view. A gate that never opens on these 6 is not proof that the gate is miscalibrated: 5 of the 6
trade at or above what their own cash flows justify, and the sixth (SUNFLAG) has a real discount with verified causes
(L33). The next informative test is a card on a stock that screens cheap (low starting P/E, within the class size
band). That is a selection question for stage 1/4, not a reason to change the gate.
