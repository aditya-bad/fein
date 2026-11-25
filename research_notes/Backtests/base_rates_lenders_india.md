# India LENDER 5-year base-rate class (survivorship-free as far as feasible): 2026-11-25

**Roadmap stage 6 (decision), feeding stage 7 (scorekeeping).** Lesson L41 (4): until now every lender card (UTKARSHBNK,
FEDERALBNK dry run) anchored its tails to the *non-financial* class, which cannot see bank leverage. This adds
`india_lender_1000_20000cr_5y` to `tools/decision/base_rates.json` (v3). Card v1.5 picks it automatically for any firm
marked as a lender. **Unlocks:** honest outside-view tails on lender cards, and a Brier baseline for lender paper calls.
Script: `tools/backtests/base_rates_lenders_india/build.py` (standard library + curl; screener pages and charts
cached in the scratchpad `bt_solv_in/`). Outputs: `base_rates_lenders_india_outputs/{panel.csv,results.json}`.
Research, not SEBI-registered advice.

## Method (same definitions as `base_rates_5y.md`, India class)
| | |
|---|---|
| Frame | **Census of lender candidates** (weight 1.0 each), not a stratified sample: (a) BSE Active, Delisted and Suspended lists, NSE delisted/suspended, IBBI CIRP/liquidation rows (`research_notes/Universe/india_dead_companies_2026-11-22.csv`), equity codes only, whose name matches a lender keyword (bank, financ, fin, housing, credit, leasing, capital, invest, homes, micro, loan ...); (b) every lender in `india_pead_live/industry_map.csv`; (c) every financial page cached by the solvency re-test; (d) explicit cases (REC, IFCI, PFC, HUDCO, Paisalo, the merged PSU banks, LVB, DHFL, SREI, Reliance Capital/Home Finance, GRUH, Capital First, Bharat Financial, SBI associates, Shriram City, Equitas, IDFC). 1,039 candidates → 932 screener pages |
| Lender test | screener labels Banks / NBFC / Housing Finance / Microfinance / Financial Institution. Unlabeled (mostly merged/delisted) pages classified by name; 39 ambiguous names ("capital", "invest") not counted (none was in band). Holding companies of a single lender and NBFC-CICs reviewed by hand and counted: Equitas Holdings, IDFC Ltd, Reliance Capital. Diversified holdcos (Edelweiss, JM Financial), brokers, AMCs, insurers excluded |
| Start dates T | 30-Sep-2016, 30-Sep-2018; FY0 annual column in (T−18m, T−6m]; a weekly price within 31 days before T |
| Size | screener market-cap-to-sales × TTM sales at the last price ≤ T, **₹1,000–20,000 cr**; 2 overrides where the ratio is missing in an IPO month (RBL Aug-2016 ₹11,100 cr, CreditAccess Aug-2018 ₹5,300 cr; shares × screener price, single-source) |
| ≥3x / ≤0.5x | R5 = price at T+5 ÷ price at T (price only). No R5 + failure → ≤0.5x |
| Blow-up | close ≤0.2× the T close at any point within 5 yrs, liquidation, compulsory delisting, **equity write-off** (LVB Nov-2020). Also reported: **permanent blow-up** = blow-up AND (R5 ≤0.5x or no R5) |
| Mergers | Not dropped: the holder's path is chained into the acquirer at the target's last traded price (R = target_last/target_T × acquirer(t)/acquirer(link)), so split adjustments in the acquirer series do not matter. 24 rows chained (8 PSU-bank amalgamations, 3 SBI associates, GRUH, Capital First is not in band, Bharat Financial, Shriram City, Equitas Holdings) |
| Median multiple | median R5 with failed-no-R5 = 0 |
| CI | 2,000 bootstrap draws, companies resampled (a company in both snapshots is one cluster), seed 20261125 |

## Results (n = 107 company-snapshots, 64 companies; 0 rows excluded for missing R5)
| Class | n | P(≥3x) [95% CI] | P(≤0.5x) [95% CI] | P(blow-up) [95% CI] | permanent blow-up | median multiple [CI] |
|---|---|---|---|---|---|---|
| **India lenders ₹1,000–20,000 cr** | 107 | **11.2%** [5.1–18.3] | **25.2%** [17.0–33.3] | **27.1%** [17.9–36.5] | **19.6%** [11.9–28.0] | **1.04x** [0.84–1.62] |
| start 2016 | 52 | 3.8% | 42.3% | 34.6% | 30.8% | 0.60x |
| start 2018 | 55 | 18.2% | 9.1% | 20.0% | 9.1% | 1.73x |
| banks (incl. SFBs) | 56 | 3.6% [0–9.1] | 25.0% | 21.4% | 17.9% | 1.02x |
| — public-sector (incl. merged) | 36 | 5.6% | 30.6% | 25.0% | 19.4% | 1.19x |
| —— 2016 / 2018 start | 19 / 17 | 0% / 11.8% | 57.9% / 0% | 36.8% / 11.8% | 36.8% / 0% | 0.37x / 1.62x |
| — private / SFB | 20 | 0% | 15.0% | 15.0% | 15.0% | 0.79x |
| NBFCs + HFCs + FIs | 51 | 19.6% [8.2–33.3] | 25.5% | 33.3% [18.5–48.2] | 21.6% | 1.04x |
| —— 2016 / 2018 start | 23 / 28 | 8.7% / 28.6% | 39.1% / 14.3% | 39.1% / 28.6% | 30.4% / 14.3% | 0.84x / 1.87x |
| robustness: firms alive today only (what survivors say) | 74 | 14.9% | 18.9% | 20.3% | 13.5% | 1.40x |
| robustness: without the size overrides | 105 | 10.5% | 25.7% | 27.6% | | 1.04x |
| *for comparison: India non-financial (same T, same rules)* | 208 | 21.3% | 11.3% | 15.4% | | |

**Reading it.** An Indian lender in the ₹1,000–20,000 cr band was about **half as likely to triple and twice as likely
to halve** as a non-financial of the same size over the same windows, and **one in four to five suffered a permanent
blow-up** (DHFL ×2, Reliance Capital ×2, SREI ×2, Reliance Home Finance, LVB ×2, Satin 2016, Repco 2016, GIC Housing
2016, IFCI 2016, J&K Bank 2016, Central Bank 2016, Union Bank 2016 and five merged PSU banks 2016). The right tail is
almost entirely NBFCs (Capri ×2, Muthoot ×2, Chola, REC, CreditAccess, Poonawalla 2018, Can Fin 2018, IDFC 2018)
plus two PSU banks from the 2018 trough (Bank of Maharashtra, IOB). No private bank tripled. Excluding dead firms
understates the loss tail (18.9% vs 25.2%) and the blow-up rate (20% vs 27%), as in the non-financial class.

## Survivorship gaps and biases (read before using)
1. **Two start dates, one credit cycle.** The 2016 window contains the PSU-bank NPA recognition (AQR), the IL&FS /
   DHFL freeze (2018–19), YES Bank (2020) and the Mar-2020 crash; the 2018 window starts near the PSU trough. The two
   disagree more than their CIs (P(≤0.5x) 42% vs 9%). The pooled number is a cycle average of two points, not a
   stable rate. Recompute when stage 1 gives more start dates (2012, 2014, 2020).
2. **The blow-up price rule counts the Mar-2020 crash** even where the stock recovered (Poonawalla/Magma 2016 and 2018,
   Allahabad 2018, Indian Bank 2018, Bharat Financial 2018, PNB Housing 2018, IDFC 2016, Satin 2018: 8 of 29). The
   "permanent" column (19.6%) is the better anchor for "lost most of the money and never got it back".
3. **Known episodes outside the class:** YES Bank (₹53,500 cr / ₹42,200 cr at T) and Indiabulls Housing (~₹35,000 cr)
   were above the band; PMC Bank and IL&FS Financial Services were never listed (no IL&FS-group listed lender exists);
   Altico, Srei Equipment unlisted. So the class does *not* include the two largest listed lender failures of the period.
4. **Excluded for data:** Syndicate Bank (in band at both T; screener series mis-scaled, ₹30,418 for a ~₹70 stock) —
   its likely outcomes (2016 start poor, 2018 start ~1.3x via Canara) would move nothing much. DHFL has no page of its
   own; screener carries its pre-2021 history on *Piramal Finance Ltd* (bse:544597), so those two rows are DHFL's
   (crash to 0.03x, no price at T+5 → failed). 101 candidates have no page: almost all tiny dead NBFCs plus old codes of
   live banks (Federal, HDFC, ING Vysya); none is a known in-band lender at T.
5. **Name-keyword frame:** a dead lender whose name carries no lender word is missed (live ones are covered by the
   industry map and the explicit list). Size uses rounded market-cap-to-sales (±0.05; 1 row straddles a band edge, plus the 2 overrides).
6. **Price only**: dividends excluded (~1–2%/yr for lenders) → P(≥3x) slightly understated. PSU-bank recapitalisation
   dilution is inside the price, which is correct for a holder.
7. **Classification is today's screener label**, applied backwards (Ujjivan Financial Services, Equitas Holdings and IDFC
   counted as lenders; Edelweiss and JM Financial not).

## How the card uses it (v1.5)
`decision_card.py` uses this class whenever the card marks the firm as a lender (`"is_lender": true`,
`survival.is_financial: true`, or a bank-mode worksheet) and the market is India, unless the card sets
`"base_rate_class_lock": true`. Effect on the live UTKARSHBNK card (re-built, not re-published): base rates move to
P(≥3x) 11.2%, P(≤0.5x) 25.2%, P(blow-up) 27.1%; the model's tails (21%, 15%) are now *below* the class, so the card's
w = 0.3 evidence note ("the class is non-financial, so weight it less") is stale — at w = 0.3 the anchored tails are
22.1% / 18.6%; at the default w = 0.5 they would be 23.1% / 21.1%. Card size stays 0 (EV 1.23x anchored vs 1.76x hurdle).

## Next
- More start dates (stage 1 data), then split by type (PSU bank / private bank / NBFC) only when each cell has n ≥ 30
  per start date.
- Add starting P/B buckets (cheap-to-book lenders: is <1x P/B a value or a trap signal?) — pre-register first.
