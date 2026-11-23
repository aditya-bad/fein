# 5-year base-rate classes for the decision card (survivorship-free) — 2026-11-23

**Roadmap stage 6 (decision), feeding stage 7 (scorekeeping: every card call is scored with Brier against these
base rates).** These classes replace the survivors-only India class and the missing US class in
`tools/decision/base_rates.json` (lesson L34). **Unlocks:** honest outside-view anchors on every card, and Brier
baselines that do not flatter or punish the model because the class was biased.
Script: `tools/backtests/base_rates_5y/build.py` (standard library, no fetching; ~4 s). Output:
`research_notes/Backtests/base_rates_5y_outputs/results.json`.

## Method (fixed before reading the numbers)
| | India | US |
|---|---|---|
| Panel | `solvency_india_outputs/panel.csv` (identical rows, weights and R5 to `hard_filters_india_v2_outputs/panel_v2.csv`, checked by the script) | `solvency_us_outputs/panel.csv` |
| Frame | BSE active + delisted + suspended, NSE-only, IBBI/NSE dead lists; strata D (distress census, weight 1.0), X (other delisted, 4.264), L (live, 5.633) | Every 10-K filer in the SEC public-float frames (census; EDGAR keeps dead firms) |
| Start dates T | 30-Sep-2016, 30-Sep-2018 | 30-Jun-2015, 2017, 2019 |
| Class filter | Non-financial (panel already excludes financials), **mcap ₹1,000–20,000 cr at T** | Non-financial, non-utility, **public float $500M–$10B** on the T-10-K |
| Weights | Stratum weights (population ÷ sample) | Equal per firm-snapshot |
| ≥3x | R5 ≥ 3 (price only) | R5 ≥ 3 (adjusted close, incl. dividends) |
| ≤0.5x | R5 ≤ 0.5, or no R5 with a failure | same |
| Blow-up | O_fail: close ≤0.2× the T close within 5 yrs, liquidation, compulsory delisting | O_fail: same price rule, 8-K 1.03 bankruptcy, delisting for cause |
| Missing R5 | Pre-registered rule of the source test: failed → counted in the loss tail; not failed → excluded (3 rows) | Unpriced + EDGAR failure → loss tail (152); unpriced acquisition → neither tail (899); unpriced alive / stopped filing / exchange transfer → excluded (566) |
| CI | 2,000 bootstrap draws, companies resampled within stratum | 2,000 draws, CIKs resampled (a firm in 3 snapshots is one cluster) |

Blow-up here is the card's definition minus fraud findings (no panel has a fraud field).

## Results
| Class | n | P(≥3x) [95% CI] | P(≤0.5x) [95% CI] | P(blow-up) [95% CI] | strict exits only |
|---|---|---|---|---|---|
| **India non-fin ₹1,000–20,000 cr** | 208 | **21.3%** [14.1–28.7] | **11.3%** [7.0–16.1] | **15.4%** [10.2–21.4] | 0.9% |
| by start: 2016 | 108 | 15.8% | 15.5% | 21.3% | |
| by start: 2018 | 100 | 26.2% | 7.4% | 10.0% | |
| live stratum only (what survivors say) | 153 | 22.2% | 7.2% | 11.8% | 0.0% |
| **US float $500M–$10B** | 3,125 used (3,691 in band, 1,823 firms) | **7.0%** [6.0–8.1] | **14.2%** [12.7–15.7] | **10.9%** [9.6–12.3] | 5.1% |
| by start: 2015 / 2017 / 2019 | 1,061 / 961 / 1,103 | 5.4 / 5.9 / 9.5% | 17.3 / 9.9 / 14.9% | 12.7 / 8.4 / 11.3% | |
| US bound: acquisitions excluded (priced-or-failed subset) | 2,226 | 9.8% | 19.9% | 15.3% | 7.2% |
| US bound: stopped-filing counted as ≤0.5x | 3,214 | 6.8% | 16.6% | 10.6% | |

## What changed versus the old classes
- India P(≥3x) falls from **44% to 21%** (the old class started six months after the Mar-2020 low and was survivors
  only). P(≤0.5x) rises from **2% to 11%**, and for the first time there is a blow-up rate: **15%**.
- The US had no 5-year class (`us_seasoned_5y` was a placeholder; FIVE used 3-year IPO numbers). It now has one.
- Including dead firms matters most in the loss tail: in India, survivors alone say 7% for ≤0.5x against 11% with dead
  firms included.

## Biases and limits (read before using)
1. **Few start dates.** India 2 and US 3, and they disagree (India 2016 vs 2018: ≥3x 16% vs 26%). The CIs show
   sampling error only, not regime error.
2. **India survivorship leak toward fewer failures:** IBBI firms that were renamed or merged, 221 IBBI rows with no
   identifier, and stratum X (mergers and voluntary delistings) has only 1 row in the band. India R5 is price only, so
   P(≥3x) is understated slightly (about 1%/yr of dividends).
3. **US missing prices:** 44% of in-band rows have no Yahoo history. The primary estimate counts unpriced acquisitions
   as neither tail, which biases both tails slightly low; the bounds row shows the alternative. A firm that fell 80% and
   was then bought cheaply is missed. Float is stale and understates the market cap of controlled firms.
4. **Size bands:** no class covers India mcap above ₹20,000 cr (VMM, CUMMINSIND) or US above $10B (FIVE ≈ $12B), and
   there is none for banks or NBFCs. Card v1.1 prints a "size outside the class" warning when that happens.
5. Recompute when stage 1 (Pi + Kite/bhavcopy + delisting lists) gives more start dates. Add starting-P/E buckets then
   (`insight:india-mb-starting-pe`).
