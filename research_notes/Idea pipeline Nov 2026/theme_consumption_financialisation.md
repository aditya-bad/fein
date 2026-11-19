# Theme: Domestic consumption revival + financialisation of savings

*Research date: 19 Nov 2026. This is research, not investment advice. Process: stock-research-analyst skill (5 stages, verification gate).*

Raw data: screener.in **consolidated** pages fetched 19 Nov 2026 (price stamp on every page: "19 Nov 3:32 p.m.", i.e. today's close). Exceptions, both called out below: Campus and Thangamayil, where the consolidated view is stale or empty, so the **standalone** view was used. Downloads are in `/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/consumption/raw/`, with the parser in `.../scratchpad/scripts/parse.py`.

---

## Stage 1: Macro thesis, checked against dated sources

| Claim in the brief | What I found | Status |
|---|---|---|
| Record SIP flows of ~₹31–32k cr/month | Sep 2026 SIP flows set a record at ₹32,490 cr. Oct 2026 was **₹32,160 cr (−1% MoM)**. Equity MF inflows fell **14% MoM** to ₹32,994 cr in Oct. SIP AUM ₹17.68 lakh cr; ~10 cr contributing accounts (AMFI data via Kotak Neo / 5paisa, 11 Nov 2026) | **Confirmed, but momentum has plateaued** |
| RBI rate cuts in 2025 | 125 bp of cuts in 2025 (Feb, Apr, Jun 50 bp, Dec). Repo held at **5.25%** at the Feb, Apr, Jun and Aug 2026 meetings. RBI flagged an oil shock / West Asia conflict and rupee weakness. I could not confirm the Oct 2026 decision | Confirmed. **No further easing in 2026, and the inflation risk now points up** |
| GST 2.0 (22 Sep 2025) | FMCG volumes were *soft* right after the change: NIQ Oct–Dec 2025 value +7.8%, volume +2.6%, held back by transition and a high base. ICRA says sales growth improved in Q3 FY26. Q2 FY27 (Sep-26 qtr) prints are strong at Nestle, Honasa, Bajaj Consumer, Radico and Mrs Bectors | Confirmed with a lag. The demand revival is showing up in FY27 numbers |
| Income-tax cut, Budget 2025 | ₹12 lakh zero-tax threshold, effective FY26. Taken from prior knowledge; **not re-verified this session** | Assumed |
| STT hike on F&O from 1 Apr 2026 | Futures 0.02%→0.05%, options 0.10%→0.15% of premium (Business Today, 26–27 Mar 2026). Forecasts ranged from −20–30% volumes to "limited impact". **I found no clean post-April volume data** | Confirmed as policy. The impact is unquantified |

**Thesis in two sentences.** Household savings are still moving into equities through SIPs at about ₹32k cr a month, but that flow has stopped accelerating. The money is in companies whose earnings grow with the *AUM stock* rather than with *trading turnover*. On consumption, real income relief (tax cuts plus GST 2.0) began showing up in volumes from mid-2026, so the best setups are companies where revenue growth comes *together with* a mix or operating-leverage margin step-change, not ones where price is doing all the work.

**Second-order check on the "F&O losers".** The loser trade looks **already played out in the reported numbers**. Angel One's Sep-26 quarter PAT was ₹335 cr vs ₹212 cr YoY, with OPM at 45%. CDSL's Sep-26 quarter PAT was ₹173 cr vs ₹140 cr. A short or avoid call based purely on the STT hike is stale. Angel One is still avoided, for its balance sheet: borrowings ₹7,632 cr and CFO of −₹4,142 cr in FY26.

---

## Stage 2 and 4: Universe and pattern recognition (26 names fetched)

The test was a sustained OPM step-change over the last 4–8 quarters with an identifiable cause, ROCE >15%, clean cash conversion, and market cap of ₹500–25,000 cr.

| Name | Mcap ₹cr | P/E | ROCE | OPM trend, last 8 qtrs | Cash/debt | Outcome |
|---|---|---|---|---|---|---|
| **Bajaj Consumer Care** | 5,355 | 21.4 | 30% | **11–15% → 23–25%** for 3 quarters | Debt-free; FY26 CFO/PAT 1.04 | **FINALIST** |
| **Prudent Corporate Advisory** | 12,098 | 45.9 | 37.5% | **23% → 26%** for 3 quarters | Debt ~₹40 cr (leases); CFO/PAT 0.98 | **FINALIST** |
| **Honasa Consumer** | 17,257 | 60.3 | 19% | **5% → 12–15%** for 4 quarters | ₹129 cr (leases); CFO/PAT 0.70 | **FINALIST** |
| KFin Tech | 16,184 | 45.2 | 29% | 45% → 34–40%, *falling* | Clean | Rejected |
| CAMS | 17,738 | 34.7 | 47% | Flat at 43–46% | Clean | Rejected |
| Piccadily Agro (Indri) | 5,362 | 39.2 | 18% | 26–28% peak → 17–21% | Debt 154→550; debtor days 32→89 | Watchlist |
| Associated Alcohols | 1,112 | 14.5 | 18% | 16.9% (Mar-26) → **6.5%** (Sep-26) | OK | Watchlist |
| Radico Khaitan | 62,336 | 77.6 | 24% | 13% → 20–21% (the template case) | OK | Out of band |
| Others | | | | | | See the rejected list |

---

## FINALIST 1: Bajaj Consumer Care (NSE: BAJAJCON)

**Verified price block**
- Screener.in: **₹410**, stamped 19 Nov 2026 3:32 pm. Mcap ₹5,355 cr.
- Bajaj Finserv: ₹414.65 (16 Nov, 3:30 pm). Ventura: NSE ₹415.00 / BSE ₹412.80 (16 Nov). ICICI Direct: ₹423.90 (17 Nov, 9:18 am; labelled a close, but the timing makes that doubtful).
- **Price used: ~₹410.** The sources sit within 3% of each other, which fits normal day-to-day moves.
- Re-derived P/E: ₹5,355 cr / TTM PAT ₹251 cr = **21.3×**, which matches the 21.4× shown on screener.
- 52-week range ~₹243–692. The stock rallied about 150% in H1 2026, then fell ~41% from its high. It dropped 11% on Q1 results (Jul) and 8–10% on Q2 results (15 Oct), despite PAT growth of 66–80% in both quarters.

**Financials (consolidated, ₹cr)**

| FY | Sales | OPM | PAT | ROCE |
|---|---|---|---|---|
| FY22 | 880 | 20% | 170 | 38% |
| FY23 | 961 | 15% | 139 | 26% |
| FY24 | 984 | 16% | 155 | 21% |
| FY25 | 965 | 13% | 125 | 23% |
| FY26 | 1,165 | 19% | 190 | 19% |
| TTM | 1,307 | 23% | 251 | 30% (latest) |

| Qtr | Mar-25 | Jun-25 | Sep-25 | Dec-25 | Mar-26 | Jun-26 | Sep-26 |
|---|---|---|---|---|---|---|---|
| Sales | 250 | 273 | 265 | 306 | 327 | 342 | 333 |
| OPM | 13% | 15% | 18% | 18% | 23% | 24% | 25% |
| PAT | 31 | 38 | 42 | 46 | 64 | 71 | 70 |

There is no loss quarter, and the margin rise holds across 7 consecutive quarters rather than resting on one spike. Other income is steady at ₹5–9 cr a quarter and the tax rate at 17–19%, so the PAT jump is operating, not driven by other income.

**Balance sheet and holders.** Borrowings ₹4–16 cr over FY23–Sep-26 (debt-free). Debtor days rose from 8 (FY22) to 24–27 (FY25–26). That needs watching, but it is still low.

Shareholding, Dec-24 → Sep-26:
- Promoter: 40.95% → 42.97%. The step came from the Sep 2025 buyback (₹290/sh, ₹187 cr, promoters did not tender). It was the second buyback at ₹290 in two years.
- FII: 10.5% → **16.4%**, rising, with a step-up in Mar-26.
- DII: 20.2% → 14.9%, falling.

Pledge: none was flagged on screener and none came up in searches. The promoter family cleared a pledge in 2019 by selling ~22%. That history, and the group's Bajaj Hindusthan links, are a governance memory to keep in mind. **I could not confirm the current pledge figure from an NSE filing.**

**Structural story and named cause.** The margin went from 13% to 25%, which is a return toward the company's FY18–19 level of ~30%. Q2 FY27 sales were +25% and EBITDA +71% to ₹83.3 cr, at a 25.0% margin vs 18.6% (JM Financial). The company cites three drivers:
1. Double-digit **unit volume** growth in Almond Drops (10%+), with domestic Almond Drops revenue up >30% in H1.
2. Coconut-portfolio volumes ahead of value, because coconut prices deflated.
3. Price-point packs growing faster than the rest of the portfolio, plus distribution expansion.

The premium angle is Natyv Soul, but it is small. **Bluntly, this is operating leverage plus input-cost relief on a revived core brand, not a pure premiumisation mix shift.** Management guides to "low-to-mid 20s" EBITDA margins and declines to predict the margin path, citing input volatility. LLP (light liquid paraffin) is crude-linked, and RBI is flagging an oil shock.

**Reverse DCF.** At 21×, with a 12% cost of equity, 10 years, exit at 20–25× and 50% payout, the price implies **~8–10% EPS CAGR**. FMCG peers trade at 40–50×. This is the only name in the theme that is *not* priced for perfection.

**Bull case (FY29).**
- Sales ₹1,730 cr (12% CAGR from TTM), OPM 24%, giving EBITDA ~₹415 cr plus other income of ₹30 cr.
- PAT ~₹350 cr. At 28× that is ~₹9,800 cr, **about 1.8× in ~2.5 years**.

**Bear case.** OPM reverts to 17% and PAT goes to ~₹190 cr. At 18× that is ~₹3,400 cr, **−36%**.

**Risks**
1. The margin is partly input-driven (coconut, LLP and crude). An oil spike could take 300–500 bp off.
2. Almond Drops concentration in a structurally slow category: the 5-year sales CAGR is only 4.8%.
3. A history of post-results selling. A broker downgrade to Reduce after Q1 shows the market already treats the margin as peak.
4. Promoter-group financial history.
5. No dividend. Capital is returned through buybacks only.

**Kill criteria**
- OPM below 19% for two consecutive quarters.
- Almond Drops volume growth below 5%.
- Any promoter pledge reappearing.
- Debtor days above 40.

**Conviction: 66/100. Verdict: BUY-ZONE** (research view). The market is pricing a peak margin. If margins hold in the low 20s, the current valuation offers re-rating plus EPS growth. Of the three finalists, this is the closest to a multibagger setup, and it is a *re-rating plus recovery* bet, not a long compounder.

---

## FINALIST 2: Prudent Corporate Advisory Services (NSE: PRUDENT)

**Verified price block**
- Screener.in: **₹2,922**, stamped 19 Nov 2026 3:32 pm. Mcap ₹12,098 cr.
- 5paisa: ~₹2,908 (16 Nov, 2:16 pm; mcap ₹12,042 cr, P/E 45.8). Investing.com: ₹2,904.30 (16 Nov).
- **Price used: ~₹2,920.** The sources agree within 1%.
- Re-derived P/E: ₹12,098 / ₹263 cr TTM = **46.0×**. That is about 11.9× book.
- 52-week range ₹1,955–4,106 on screener; 5paisa shows a ₹2,121 low. The stock is **29% below its high**.
- Brokers: Citi Buy, target ₹3,300 (May-26). ICICI Securities Hold, target ₹2,800 (Jun-26).

**Financials (consolidated, ₹cr)**

| FY | Revenue | OPM | PAT | ROCE |
|---|---|---|---|---|
| FY22 | 458 | 27% | 80 | 52% |
| FY23 | 617 | 29% | 117 | 51% |
| FY24 | 823 | 26% | 139 | 43% |
| FY25 | 1,133 | 26% | 196 | 44% |
| FY26 | 1,341 | 25% | 222 | 37% |
| TTM | 1,440 | 25% | 263 | 37.5% |

| Qtr | Mar-25 | Jun-25 | Sep-25 | Dec-25 | Mar-26 | Jun-26 | Sep-26 |
|---|---|---|---|---|---|---|---|
| Revenue | 283 | 294 | 320 | 343 | 361 | 348 | 389 |
| OPM | 24% | 23% | 23% | 23% | 26% | 26% | 26% |
| PAT | 52 | 52 | 54 | 58 | 59 | 75 | 72 |

There is no loss quarter. The Sep-26 PAT fell 4% QoQ because of an MTM loss on treasury income, which was ₹4 cr in other income vs ₹21 cr in Jun-26. The core operating profit was ₹102.8 cr, **up 42% YoY**.

**Balance sheet and holders.** Debt is ~₹40 cr, which is leases. CFO/PAT is 0.98 in FY26 and above 0.7 every year. Debtor days are 45–49, improving from 61–85. Equity is undiluted at ₹21 cr capital since FY22.

Shareholding:
- Promoter: flat at 55.31%. It fell 3.1% over 3 years from the Wargus/TA exit at listing.
- FII: 14.8% → 14.6%, flat.
- DII: 23.6% → 22.9%, flat.
- Retail shareholders jumped from 30.8k to 44.8k in Sep-26, so retail is chasing the dip. No pledge was found.

**Structural story and named cause.** Prudent is a B2B2C mutual fund distribution platform for ~30k+ sub-brokers in tier-2 and tier-3 towns. It is a direct way to own the *stock* of SIP savings rather than trading turnover, and its broking arm is small.
- Q2 FY27: quarterly average AUM **₹1.43 lakh cr**, up 21% YoY and 8% QoQ. Monthly SIP book ₹1,272 cr, up 17% YoY. Market share 3.7% vs 3.5%.
- OPM 26.4% vs 22.6% YoY. Management talks of "30%+ over time" from operating leverage.
- The step-change is real but modest, at 300 bp. It comes from **operating leverage and lower payout leakage, not mix**.
- SEBI's MF Regulations 2026 (TER restructuring, from 1 Apr 2026) were a headwind. A third-party estimate (Finology) puts the trail impact at ~2–3 bp, partly passed on to sub-brokers. Margins still expanded after the change, which is the evidence it was absorbed.

**Reverse DCF.** At 46×, the price implies **17–20% EPS CAGR for 10 years**. The 5-year PAT CAGR was 37% and the current YoY rate is ~34%, but SIP book growth is now only ~17% and industry SIP flows are flat MoM. **This is priced for continued excellence. It is not cheap.**

**Bull case.** PAT grows at 22% CAGR to ~₹710 cr in FY31. At 35× that is ~₹25,000 cr, **about 2× in 5 years** (~15% IRR). A multibagger is only possible with a bull market, which lifts AUM via MTM, plus margins reaching 30%.

**Bear case.** A market correction gives 2 flat years of PAT, and the multiple compresses to 30×. That is ~₹7,900 cr, **−35%**.

**Risks**
1. Beta to equity markets: an AUM MTM shock hits revenue directly.
2. Further SEBI commission caps.
3. AMCs shifting to direct plans and fintech platforms.
4. Retail crowding (the shareholder-count spike).
5. Insurance-broking diversification diluting returns.

**Kill criteria**
- SIP book growth below 10% YoY.
- OPM back below 23%.
- Net equity sales falling YoY for two quarters.
- Any adverse SEBI action on distributor trail.

**Conviction: 63/100. Verdict: WATCHLIST.** It is a high-quality compounder. Accumulation makes sense below ~₹2,500 (~39× TTM, implied CAGR ~15%) or after FY27 earnings catch up. It is a 2× in 5 years, not a 5× setup.

---

## FINALIST 3: Honasa Consumer (NSE: HONASA)

**Verified price block, with a discrepancy disclosed**
- Screener.in: **₹529**, stamped 19 Nov 2026 3:32 pm. 52-week high ₹535, so it is trading at the high. Mcap ₹17,257 cr.
- Upstox: ₹481.65 (5 Nov 2026). Kotak Neo: 52-week high ₹509.8 (as of 21 Oct).
- **I found no second source for 18–19 Nov.** The ~10% gap vs 5 Nov fits the post-Q2 rally (Inc42: "jumps over 8% on strong Q2 growth outlook"), but it is **single-source for today**.
- Re-derived P/E: ₹17,257 / ₹283 cr TTM = **61×**.

**Financials (consolidated, ₹cr)**

| FY | Sales | OPM | PAT |
|---|---|---|---|
| FY23 | 1,493 | 1.5% | −151 |
| FY24 | 1,920 | 7% | 111 |
| FY25 | 2,067 | 3.4% | 73 |
| FY26 | 2,392 | 10% | 200 |
| TTM | 2,746 | 13% | 283 |

ROCE was 8% in FY25 and 19% in FY26.

| Qtr | Sep-24 | Dec-24 | Mar-25 | Jun-25 | Sep-25 | Dec-25 | Mar-26 | Jun-26 | Sep-26 |
|---|---|---|---|---|---|---|---|---|---|
| Sales | 462 | 518 | 534 | 595 | 538 | 602 | 657 | 756 | 731 |
| OPM | −7% | 5% | 5% | 8% | 9% | 11% | 12% | 15% | 13% |
| PAT | −19 | 26 | 25 | 41 | 39 | 50 | 69 | 90 | 73 |

There was a loss quarter in Sep-24, during the distributor inventory clean-up. The margin has risen for 7 quarters since. Other income of ₹16–24 cr a quarter is **~25–30% of PAT**, so the core is weaker than the headline. The tax rate swings (12–27%).

**Balance sheet and holders.** CFO/PAT was 0.70 in FY26 and 1.4 in FY25, which is mediocre. Debt is leases only.

Shareholding:
- Promoter: steady at 35.5%.
- DII: 18.5% → **23.4%**, rising.
- FII: 15.4% → 14.9%.
- No pledge was found.

**Structural story and named cause.** Project Neev, the offline general-trade overhaul from late 2024, moved the company off super-stockists onto direct distribution. GT secondary sales are growing 30%+ and MT offtake 40%+, with ~3.2 lakh GT outlets. Gross margin is ~70%. Younger brands (Derma Co, Aqualogica, Dr Sheth's) grew >45% at better margins, which is the **mix-shift element**. Q2 FY27 revenue was +36% and EBITDA +93%, at a 12.7% margin. Management's own target is only a "15% EBITDA margin profile" within four years, and Q1 already printed 15%.

**Reverse DCF.** At 61×, the price implies **~21–23% EPS CAGR for 10 years**. **It is priced for perfection**, and management's own margin ceiling caps the operating leverage left.

**Bull case (FY29).** Sales ~₹4,600 cr (25% CAGR), EBITDA margin 15% plus other income, giving PAT ~₹570 cr. At 50× that is ~₹28,500 cr, **+65%**.

**Bear case.** Growth slows to 15% and the margin stays at 11%, giving PAT ~₹350 cr. At 35× that is ~₹12,250 cr, **−29%**.

**Risks**
1. History of channel inventory stuffing (2024).
2. Intense D2C and beauty competition (HUL/Minimalist, Nykaa private labels, Reliance).
3. Other-income dependence.
4. A Q2 sequential decline in both revenue and PAT.

**Kill criteria**
- Revenue growth below 20%.
- OPM below 10%.
- Any sign of channel inventory build-up (receivable days above 35, or a fall in GT secondaries).

**Conviction: 55/100. Verdict: WATCHLIST.** The turnaround is real and the cause is named, but the stock sits at its 52-week high and 61× earnings. Wait for a 20–25% pullback.

---

## Rejected names and reasons

All figures in this section are single-source, from screener consolidated on 19 Nov 2026.

- **KFin Tech** (₹936, 45× P/E): OPM fell from 45% to 34–40% because of investment and acquisitions. Promoter General Atlantic sold down from 32.9% to 14.1%, and DIIs absorbed it (19% → 37.5%). There is no margin step-change. The price implies ~17% CAGR. Revisit if OPM gets back above 42%.
- **CAMS** (₹714, 35×): Best-in-class quality, ROCE 47%, CFO above PAT. But growth is ~10–15%, and FIIs fell from 57.6% to 45.6%. It is fairly priced at ~14% implied growth, not a multibagger.
- **Anand Rathi Wealth**: Mcap of ₹39k cr is outside the band. P/E 86×, and the Sep-26 quarter OPM dropped from 46% to 34%.
- **Nuvama**: Mcap ₹34k cr. Borrowings of ₹13.2k cr and persistently negative CFO make it a balance-sheet business.
- **UTI AMC**: A loss quarter in Mar-26 (−₹51 cr). Earnings are MTM-heavy and ROE is 10%.
- **CDSL** (59×) and **Angel One**: The F&O damage is already reflected in the numbers, and the Sep-26 quarters recovered. CDSL is too expensive. Angel One has ₹7.6k cr of debt and CFO of −₹4.1k cr.
- **Radico Khaitan**: The pattern proof (OPM 13% → 21%), but mcap is ₹62k cr and the price implies ~24% CAGR at 78×.
- **Tilaknagar**: The Imperial Blue acquisition took borrowings from ₹44 cr to ₹2,301 cr. There were loss quarters in Dec-25 and Mar-26, CFO of −₹445 cr, ROCE 11%, and debtor days of 198. It is a special situation, not a clean step-change.
- **Sula Vineyards**: OPM collapsed from 31% to 18%, ROCE is 8%, and FIIs went from 9.6% to 0.35%. A broken premiumisation story.
- **Piccadily Agro (Indri)**: The premiumisation brand is real, but the margin peaked (26–28% → 17–21%). Sep-26 PAT was −15% YoY, debt rose from ₹154 cr to ₹550 cr, debtor days from 32 to 89, and the ENA capex dilutes the mix. **Watchlist.**
- **Associated Alcohols**: Cheap at 14.5× and near its 52-week low, but Sep-26 OPM collapsed to 6.5% with no explained cause. **Watchlist** until the cause is known.
- **Globus Spirits**: ROCE 11% and erratic margins.
- **Jewellery (Senco, PN Gadgil, Thangamayil [standalone], Sky Gold)**: Gold-price inventory gains inflate margins and make P/Es look cheap (Senco 8.75×). CFO is deeply negative (Senco −₹789 cr, PNG −₹717 cr) and borrowings are ballooning. Sky Gold has the best growth (Sep-26 qtr PAT ₹129 cr vs ₹67 cr) but negative CFO every year. These are not mix stories, and they reverse if gold corrects.
- **Metro Brands**: P/E 54, OPM flat at 30%, FIIs falling. No step-change.
- **Campus** (standalone; the consolidated page is stale at 2022): OPM flat at 13–19%, P/E 44.
- **Mrs Bectors**: Steady 13% OPM, P/E 42, FIIs 15.6% → 6.0%.
- **V2 Retail**: Growth is debt-funded (₹525 cr → ₹1,379 cr) and FY26 CFO was −₹103 cr.
- **Jyothy Labs**: Screener consolidated data stops at Mar-25, so it could not be verified. Excluded.
- **Devyani**: P/E 1,304× and ROCE 4.75%. The QSR recovery has not shown up.

## Bottom line

- The theme is real, but **most of the obvious beneficiaries are priced for it**: AMCs, RTAs, Radico and Honasa all trade at prices implying 17–24% CAGRs.
- The only finalist with a valuation margin of safety is **Bajaj Consumer Care**: 21×, debt-free, OPM tripled-ish over 7 quarters. But its step-change is partly input-cost-driven, so it has to keep showing margins in the low 20s through an oil-price shock.
- **Prudent** is the cleanest financialisation compounder, and it is a buy-on-dips name.
- The "F&O loser" short thesis is stale.

Sources: Kotak Neo/5paisa (AMFI SIP, Nov 2026); Business Today (STT, 26–27 Mar 2026); Outlook Money/Moneylife (RBI holds 2026); NIQ/ICRA (FMCG volumes); JM Financial, Quartr, Sovrenn, Upstox (BAJAJCON Q2 FY27); Business Standard, Angel One (buyback 2025); Bajaj Finserv, Ventura, ICICI Direct (BAJAJCON price, 16–17 Nov); Free Press Journal, Investywise, Multibagg (PRUDENT Q2 FY27); 5paisa, Investing.com (PRUDENT price, 16 Nov); Finology, Business Today (SEBI MF Regs 2026); Exchange4media, Inc42, Arthneeti, NewsBytes (Honasa Q2 FY27); Upstox, Kotak Neo (Honasa price); Arthneeti, Sovrenn (Piccadily Q2 FY27).
