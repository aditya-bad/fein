# Technical Trading Systems, Position Sizing & Risk Management (as of Nov 2026)

Source-quality legend used below:
- **[F]** = fetched/searched this session (URL reviewed via search/fetch).
- **[K]** = canonical item from the book or paper (training knowledge); the URL is the publisher/DOI/reference page and was **not** re-fetched this session. The report writer should treat [K] rule details as "per the author's book" and can confirm them against the book.
- Many web summaries of trader rules are third-party (blogs, TradingView scripts). Where sources conflict, it is noted.

---

## 1. Growth/momentum trading systems: exact rules (CAN SLIM, SEPA/Trend Template, VCP, Weinstein, Darvas, Zanger, Qullamaggie, Livermore, RS, volume, bases, MAs, market regime)

### Takeaway
All of the well-known US "momentum-growth" systems share one structure: (1) a market-regime filter (only buy in confirmed uptrends), (2) a leadership universe (strong earnings/sales growth + top-decile/quintile relative strength + price in a Stage 2 uptrend above rising 50/150/200-day MAs and near 52-week highs), (3) a low-risk entry from a tight base or pivot on rising volume, and (4) a hard, small stop (about 7-8% max, often 3-5%) with losses cut quickly and winners held or pyramided. The specific thresholds differ by author and are often misquoted online, so treat exact numbers as the author's heuristics, not tested parameters.

### Cited Findings

**CAN SLIM (William O'Neil, *How to Make Money in Stocks*)**
- C = Current quarterly EPS up at least 25% year over year (O'Neil preferred 40%+); accelerating growth is a positive. — [AAII: O'Neil's CAN SLIM approach](https://www.aaii.com/journal/article/william-oneil-can-slim-approach-to-selecting-growth-stocks) [F]; [Wikipedia: CAN SLIM](https://en.wikipedia.org/wiki/CAN_SLIM) [F]
- A = Annual EPS growth of 25%+ in each of the last 3 years (some sources say 3-5 years); ROE of at least 17% (O'Neil's studies of the biggest winners). Some screens add sales growth of 25%+ as confirmation. — [AAII](https://www.aaii.com/journal/article/how-to-use-the-can-slim-approach-to-screen-for-growth-stocks) [F]; [Liberated Stock Trader: What is CANSLIM](https://www.liberatedstocktrader.com/what-is-canslim/) [F]
- N = Something New: new product/service, new management, or new industry conditions, and the stock emerging from a proper base to new price highs. — [Wikipedia: CAN SLIM](https://en.wikipedia.org/wiki/CAN_SLIM) [K]
- S = Supply and demand: shares outstanding/float, and price advances on volume well above average (accumulation). — [Wikipedia: CAN SLIM](https://en.wikipedia.org/wiki/CAN_SLIM) [K]
- L = Leader or laggard: buy leaders in leading industry groups; IBD Relative Strength Rating of 80+ (O'Neil). — [AAII](https://www.aaii.com/journal/article/william-oneil-can-slim-approach-to-selecting-growth-stocks) [K]
- I = Institutional sponsorship: increasing number of quality institutional owners in recent quarters. — [Wikipedia: CAN SLIM](https://en.wikipedia.org/wiki/CAN_SLIM) [K]
- M = Market direction: roughly 3 of 4 stocks follow the general market, so buy only in a confirmed uptrend (follow-through day), and cut exposure as distribution days pile up. — [Wikipedia: CAN SLIM](https://en.wikipedia.org/wiki/CAN_SLIM) [K]
- Sell rule: cut every loss at 7-8% below purchase price, no exceptions; O'Neil's typical profit-taking zone is 20-25% gains (with an exception to hold for 8 weeks a stock that gains 20%+ within 3 weeks of breakout). — [Liberated Stock Trader](https://www.liberatedstocktrader.com/what-is-canslim/) [F] for the 7-8% stop; 20-25%/8-week rule is [K] from the book.
- Cup-with-handle: online sources disagree on parameters. One guide lists 7-65 weeks duration and 15-35% depth; O'Neil's book describes bases of at least 7 weeks and cups typically 12-33% deep (up to ~40-50% in bear markets), handle drifting down in the upper half of the base, ideally on light volume, buy point = handle high + $0.10, breakout volume 40-50%+ above average. — [AAII screening guide](https://www.aaii.com/journal/article/how-to-use-the-can-slim-approach-to-screen-for-growth-stocks) [F] (conflict noted); book parameters [K].
- Flat base: per O'Neil, a ~5+ week sideways base correcting no more than ~10-15%, often forming after a breakout from a cup. [K] — [Wikipedia: CAN SLIM](https://en.wikipedia.org/wiki/CAN_SLIM)
- AAII's long-running CAN SLIM screen has been one of its better-performing screens historically (AAII publishes the track record), but this is a screen backtest, not an audited live record. — [AAII](https://www.aaii.com/journal/article/how-to-use-the-can-slim-approach-to-screen-for-growth-stocks) [K]

**Market regime filter: follow-through day (FTD) and distribution days (IBD)**
- FTD: on Day 4 or later of a rally attempt (Day 1 = first up close after a new low), a major index (Nasdaq or S&P 500) gains a minimum percentage on volume higher than the prior session; strongest FTDs come on days 4-7. Threshold has changed over time: ~1% in the original rule, ~1.7% in IBD's 2000s rule, ~1.25% in recent descriptions (not confirmed against an IBD primary document). The FTD fails if the index undercuts the rally-attempt low. — [LuxAlgo: Follow-through Day](https://www.luxalgo.com/library/concept/follow-through-day/) [F]
- Distribution day: index closes down at least 0.2% on volume higher than the prior session; each counts for 25 sessions, and drops off early if the index rallies 5% above that day's close. Clusters of ~5-6 distribution days within 25 sessions are IBD's warning that the uptrend is "under pressure." — [LuxAlgo: Distribution Days](https://www.luxalgo.com/library/concept/distribution-days/) [F] (third-party; not IBD primary)

**Minervini SEPA and the Trend Template (*Trade Like a Stock Market Wizard*, 2013)**
- The Trend Template (as published by Minervini; online lists vary slightly):
  1. Price above both the 150-day and 200-day MA.
  2. 150-day MA above the 200-day MA.
  3. 200-day MA trending up for at least 1 month (preferably 4-5 months).
  4. 50-day MA above both the 150-day and 200-day MA.
  5. Price above the 50-day MA.
  6. Price at least 30% above its 52-week low (some lists say 25%).
  7. Price within 25% of its 52-week high (closer is better).
  8. IBD RS rating at least 70 (preferably 80s-90s).
  — [Chartmill: SEPA explained](https://www.chartmill.com/documentation/trading-and-investing/methodologies/523-SEPA-Explained-Mark-Minervinis-Specific-Entry-Point-Analysis-System) [F]; [Sharpely: Minervini trend template for Stage 2 stocks](https://sharpely.in/blogs/minervini-trend-template-for-stage-2-stocks/) [F]; [Deepvue: Trend Template](https://deepvue.com/?p=3926) [F]. Discrepancy: some implementations use 25% vs 30% above the low, or drop the 52-week-low check; one scanner counts 7 criteria. The template is a universe filter, not an entry signal.
- SEPA's 5 elements (per Minervini): Trend (Stage 2 via Trend Template), Fundamentals (earnings/sales growth, ideally accelerating; earnings surprises/estimate revisions), Catalyst, Entry points (low-risk pivot, usually VCP), Exits (predefined stop and sell rules). — [Chartmill SEPA](https://www.chartmill.com/documentation/trading-and-investing/methodologies/523-SEPA-Explained-Mark-Minervinis-Specific-Entry-Point-Analysis-System) [F]
- Volatility Contraction Pattern (VCP): a base with 2-6 successive pullbacks ("T"s), each roughly half the depth of the prior (e.g., 25% -> 12% -> 6% -> 3%), volume drying up into the right side; buy the pivot (high of the final tight contraction) on expanding volume. Stop typically just below the last contraction low; Minervini's maximum stop is 10%, average loss targeted around 5-6% or less, and he says to keep average win larger than average loss by about 2-3x. [K] — book; summarized at [Chartmill SEPA](https://www.chartmill.com/documentation/trading-and-investing/methodologies/523-SEPA-Explained-Mark-Minervinis-Specific-Entry-Point-Analysis-System)
- Minervini's verified US Investing Championship record: he won the 1997 USIC with a 155% return and has competed since. — [USIC press (BusinessWire, 2023)](https://businesswire.com/news/home/20230125005300/en/United-States-Investing-Championship-2022-Final-Standings) [F] for participation; 155%/1997 is [K].

**Stan Weinstein Stage Analysis (*Secrets for Profiting in Bull and Bear Markets*, 1988)**
- Uses weekly charts and the 30-week moving average (~150-day). Stage 1 basing (flat 30-week MA, price whipsawing around it); Stage 2 advancing (price breaks out above resistance and the 30-week MA turns up, on volume at least ~2x average on the breakout week); Stage 3 topping (MA flattens, price chops around it); Stage 4 declining (price below a falling 30-week MA). Buy only Stage 2 breakouts (or the first pullback to the breakout level); never hold in Stage 4. Uses Mansfield relative strength (stock vs. index, zero line) — RS should be positive/rising. Market and sector also must be in Stage 2 ("forest to trees"). Stop: below the prior base/support, then trail under the 30-week MA. — [MarketInOut Stage 2 screen (India)](https://www.marketinout.com/stock-screener/stage-2-uptrend/india) [F] for framework; detailed rules [K] from book.

**Nicolas Darvas box (*How I Made $2,000,000 in the Stock Market*, 1960)**
- Combined "techno-fundamental": stocks in growing industries with rising earnings, making new highs on unusual volume. A "box" forms when price makes a high not exceeded for ~3 days (top) and a low not broken for ~3 days (bottom). Buy-stop just above the box top; stop-loss just below the box bottom (or the new box's bottom as price stacks new boxes higher). — [Wikipedia: Nicolas Darvas](https://en.wikipedia.org/wiki/Nicolas_Darvas) [K]

**Jesse Livermore pivotal points (*How to Trade in Stocks*, 1940; *Reminiscences of a Stock Operator*)**
- Buy when price breaks through a "pivotal point" (a key prior high/resistance, or a round number) with confirming volume; "probe" with a small position, add only if the first is profitable (pyramid up, never average down); if the stock doesn't act right quickly after crossing the pivot, exit. Also: follow the leaders of leading groups ("tandem trading"). — [Wikipedia: Jesse Livermore](https://en.wikipedia.org/wiki/Jesse_Livermore) [K]

**Dan Zanger**
- Chart-pattern breakout trader (cup-with-handle, flags, pennants, ascending triangles) in high-volume leaders; requires breakout volume well above average; tight stops near the breakout point and fast exits if the breakout fails. Reportedly turned ~$10,775 into $18M+ in 1998-99 (widely cited; I found no independently audited record this session). [K] — gap: not verified this session.

**Qullamaggie (Kristjan Kullamägi) — three setups**
- Breakout: a stock that already made a big move (e.g., top 1-2% performers over 1/3/6 months), then consolidates in a tightening range ("higher lows," surfing the 10/20-day MAs) for ~2 weeks to 2 months; buy the opening-range high breakout (1-min/5-min ORH) on the daily-chart breakout; stop at the low of the day (stop size should not exceed the stock's ADR, average daily range); sell 1/3-1/2 after 3-5 days, move stop to breakeven, and trail the remainder with the 10- or 20-day MA (close below). Don't anticipate breakouts. — [Tikamalma: Qullamaggie swing trading setups](https://tikamalma.substack.com/p/qullamaggie-swing-trading-setups) [F]; [Retail Traders Repository stream notes](https://retailtradersrepository.substack.com/p/kristjan-kullamagi-qullamaggie-stream-092) [F]
- Episodic Pivot (EP): a news catalyst (earnings blowout, FDA, contract) causing a gap of ~10%+ on very heavy volume, ideally in a stock that has not already run up (neglected); entry on the opening range high; stop at low of the day. In a 2023 stream he reportedly said he now mainly trades EPs. — [Financial Wisdom: Episodic Pivot](https://www.financialwisdomtv.com/post/the-episodic-pivot-strategy-qullamaggie-s-high-momentum-setup-explained) [F]; [Stockbsessed: Episodic pivot](https://stockbsessed.substack.com/p/episodic-pivot-1) [F]
- Parabolic short: stock up several hundred % (large caps ~50-100%+) in days/weeks; short the opening-range low or the first crack/failure at VWAP; targets the 10- and 20-day MAs; higher win rate than his long setups. — [Tikamalma](https://tikamalma.substack.com/p/qullamaggie-swing-trading-setups) [F]; [Stonks Capital: systemizing the parabolic short](https://stonkscapital.substack.com/p/systemizing-kullamagis-parabolic?r=5igdr) [F]
- Risk/expectancy: risk per trade typically 0.25-0.5%, 1% max; win rate only ~25-30% by his own estimate; profits come from rare 10-20R winners. Position size often up to 10-25% of account per position because stops are tight. — [CTE research sheet on Kullamägi](https://completetradersedge.com/wp-content/uploads/2026/09/CTE-Research-Sheet-Kristjan-Kullamagi-market-wizards-next-generation.pdf) [F]
- His claimed growth (roughly $5k to $100M+) is self-reported; a 2026 profile describes a ~$105M figure that "lasted a few days." — [Complete Trader's Edge profile](https://completetradersedge.com/kristjan-kullamagi-qullamaggie/) [F]

**Relative Strength (IBD RS rating)**
- IBD RS Rating = 1-99 percentile rank of a stock's price performance over the last 12 months vs. all stocks, with the most recent quarter double-weighted (common replication: RS = 0.4×ROC(63) + 0.2×ROC(126) + 0.2×ROC(189) + 0.2×ROC(252), then percentile-ranked). O'Neil: buy 80+; Minervini: 70+ minimum. — [TradingView Minervini Scanner (MarketSmith-style RS)](https://www.tradingview.com/script/y43c2PL9-Minervini-Scanner-MarketSmith-RS-up-to-40-tickers) [F]; formula weights [K] (common public replication, not an IBD disclosure).

**Volume and moving averages**
- Breakout volume should be at least 40-50% above the 50-day average (O'Neil); dry-up of volume in the handle/final contraction signals supply exhaustion; distribution = heavy-volume down days. [K]
- 50/150/200-DMA stack is the core of the Trend Template above; Weinstein's 30-week MA ≈ 150-day MA. — [Chartmill SEPA](https://www.chartmill.com/documentation/trading-and-investing/methodologies/523-SEPA-Explained-Mark-Minervinis-Specific-Entry-Point-Analysis-System) [F]

### Inferences
- A consolidated, codable rulebook (common denominator): (a) regime ON when index > rising 50/200-DMA and an FTD has occurred with < ~5 distribution days in 25 sessions; (b) universe = Trend Template pass + RS ≥ 80 + EPS/sales growth ≥ 25% (fundamental filter optional for Qullamaggie-style pure momentum); (c) entry = breakout above a ≥5-7 week base or VCP pivot, volume ≥ 1.5× 50-day average; (d) initial stop = min(7-8%, below base low, ~1 ADR); (e) trail with 10/20/50-DMA depending on holding period.
- These systems are all variants of documented academic momentum + 52-week-high + PEAD effects (Section 3) wrapped in strict loss-cutting; the risk rules, not the patterns, are what the practitioners themselves credit.

### Gaps
- Exact current IBD thresholds (FTD % gain, distribution-day count that triggers "under pressure") not confirmed from an IBD primary source this session.
- Dan Zanger's record and rules are not independently verified; no primary source fetched.
- No peer-reviewed backtest of the full CAN SLIM, VCP, or Qullamaggie systems was found; evidence is author track records + screen backtests.

---

## 2. Indian adaptations: traders, screeners, momentum indices, competitions

### Takeaway
In India, the Minervini/Weinstein framework is widely replicated on Chartink, Screener.in, MarketInOut, Sharpely and MarketSmith India; the most rule-based, investable implementation is the NSE Nifty200 Momentum 30 index (volatility-adjusted 6- and 12-month returns, semi-annual rebalance) and its ETFs/index funds. Indian traders have featured in the US Investing Championship (USIC), but India-specific competition data is thin.

### Cited Findings
- Nifty200 Momentum 30: top 30 of the Nifty 200 by Normalised Momentum Score from 6-month and 12-month price returns adjusted for volatility; weights = free-float mcap × momentum score; stock cap = lower of 5% or 5× its free-float weight; must be F&O-eligible with ≥1 year listing; rebalanced semi-annually (last working day of June and December). — [NSE factsheet](https://www.niftyindices.com/Factsheet/Factsheet_Nifty200_Momentum30.pdf) [F]; [NSE index page](https://niftyindices.com/indices/equity/strategy-indices/nifty200-momentum-30) [F]; [NSE rebalancing calendar](https://niftyindices.com/resources/index-rebalancing-schedule) [F]
- Score mechanics (per freefincal's reading of NSE methodology): momentum ratio = return ÷ std. dev. of daily returns over the past year, computed for 6 and 12 months; each converted to a cross-sectional z-score; weighted average z = 50%/50%; then normalized. — [Freefincal](https://freefincal.com/nifty200-momentum-30-index-a-new-strategy-index-from-the-nse/) [F]
- Volatility: NSE whitepaper reports annualized volatility of ~23.4% vs 22.3% for the Nifty 200 since inception. — [NSE momentum whitepaper 2026](https://www.niftyindices.com/docs/default-source/indices/nifty200-momentum-30/momentum-strategy-whitepaper_2026.pdf) [F]
- High turnover: the December 2025 rebalance replaced 19 of 30 constituents (effective Dec 31, 2025), churning ~₹16,000 crore; June 2025 rebalance saw ~20 changes. — [Business Standard, Dec 2025](https://www.business-standard.com/markets/news/nifty200-momentum30-a-flip-of-index-switch-jolts-16k-cr-across-the-grid-125121400388_1.html) [F, headline/snippet; page 403 on fetch]; [Business Standard June 2025](https://www.business-standard.com/amp/markets/stock-market-news/nifty200-momentum-30-index-to-see-20-stock-changes-on-june-27-125062600872_1.html) [F]; [NSE press release 11 Dec 2025](https://www.niftyindices.com/Press_Release/ind_prs11122025.pdf) [F]
- Value Research notes about two-thirds of momentum index changes can happen on a single rebalance day (illustrating front-running/impact cost risk). — [Value Research](https://www.valueresearchonline.com/stories/225617/two-thirds-momentum-index-changes-just-one-day/) [F]
- Screeners: Chartink (free custom technical scans incl. intraday 5-min; delayed data on free plan; Premium ~₹780/30 days as of Oct 2026) is the most-used India technical screener; ready-made Minervini/Stage-2 screens exist on MarketInOut (India), Sharpely and Screener.in user screens. — [Tapetide comparison](https://tapetide.com/compare/best-stock-screener-for-swing-trading-india) [F]; [MarketInOut Trend Template India](https://www.marketinout.com/stock-screener/minervini-trend-template/india) [F]; [Sharpely Stage 2 blog](https://sharpely.in/blogs/minervini-trend-template-for-stage-2-stocks/) [F]; [Screener.in "Mark minervini" screen](https://www.screener.in/screens/672150/mark-minervini) [F]
- MarketSmith India (O'Neil's platform localized) publishes CAN SLIM education for Indian stocks. — [MarketSmith India blog](https://blog.marketsmithindia.com/?p=14301) [F]
- Indian traders in USIC: Tanmay Khandelwal is described as the first Indian champion (2023 Money Manager Verified division); Goverdhan Gajjala reported ~805% in USIC 2023; Vibha Jha is described as a USIC champion investor (Elearnmarkets interview); Aryan Khandelwal led the $1M+ division at the 9-month mark of 2024 (interim only). The 2025 MMVR winner was J Law (Hong Kong, 252.3%). — [TraderLion 2023 USIC champion](https://traderlion.com/investing-champions/2023-us-investing-champion/) [F]; [Retail Traders Repository: Goverdhan Gajjala](https://retailtradersrepository.substack.com/t/goverdhan-gajjala) [F]; [Elearnmarkets: Vibha Jha](https://www.elearnmarkets.com/face2face/details/profitable-trading-portfolio-management-tips-from-a-champion-investor-with-vibha-jha) [F]; [The Week, Feb 2026](https://www.theweek.in/wire-updates/business/2026/02/27/j-law-sets-two-year-record-with-1-499-return-in-u.s.-investing-championship.html) [F]
- Indian academic evidence: momentum profits exist in India (Ansari & Khan 1995-2006, not explained by CAPM/FF3); profits concentrated in winners (long side), not explained by size/value/illiquidity; strongest after "up" markets; no January seasonality. — [Ansari & Khan, Managerial Finance 2012](https://emerald.com/insight/content/doi/10.1108/03074351211193730/full/html) [F]; [Maheshwari & Dhankar, JAMR 2017](https://econpapers.repec.org/RePEc:eme:jamrpp:jamr-11-2015-0081) [F]; [Maheshwari & Dhankar, IIMK 2018](https://econpapers.repec.org/RePEc:sae:iimkoz:v:7:y:2018:i:2:p:154-170) [F]; [Seasonality in Indian momentum, JCAR](https://publishingindia.com/archive/jcar/seasonality-in-momentum-profits-evidence-from-the-indian-stock-market) [F]

### Inferences
- An Indian rulebook adaptation: use Nifty 500 (or Nifty 200 for liquidity) as universe; apply Trend Template on daily closes; replace IBD RS with percentile of the Nifty-200-Momentum-style volatility-adjusted 6/12m score; require minimum daily traded value (e.g., ₹5-10 crore) to avoid illiquid small caps and circuit-limit (upper/lower circuit) traps where stops cannot execute; use Nifty 50/Nifty 500 above rising 50/200-DMA as regime filter.
- Long-only cash equity (not F&O) is the realistic implementation for retail given SEBI's F&O loss data (Section 4). Because Indian momentum profits come from the long leg, long-only loses little of the edge.
- Momentum index turnover (19/30 names in one rebalance) means impact cost and STT erode returns; the index fund route trades predictably and can be front-run.

### Gaps
- Could not verify specific named Indian swing traders' published systems (search found no reliable source on, e.g., Vijay Thakkar or Siddharth Bhanushali's rules); India-specific trading competitions with audited results not found.
- No IIM Ahmedabad momentum paper retrieved (IIMA publishes Indian Fama-French + momentum factor data, not fetched).
- Long-run net-of-cost performance of Nifty200 Momentum 30 vs Nifty 200 not fetched as a figure (check NSE factsheet).

---

## 3. Position sizing and risk management (the part that makes systems work)

### Takeaway
Size every position from the stop: shares = (account × risk%) ÷ (entry − stop). Keep risk per trade at 0.25-1% (2% hard ceiling), total open risk ("portfolio heat") ≤ ~6-10%, cut losses fast (7-8% max per O'Neil; 3-5% typical for VCP/Qullamaggie), and only add to winners. Positive expectancy with small, uniform R is what lets low-win-rate breakout systems (25-50% win rate) survive.

### Cited Findings
- O'Neil: sell any stock that falls 7-8% below purchase price, no exceptions. — [Liberated Stock Trader: CANSLIM](https://www.liberatedstocktrader.com/what-is-canslim/) [F]
- Qullamaggie: risk ≤0.5% per trade typically, 1% max; win rate ~25-30%. — [CTE research sheet](https://completetradersedge.com/wp-content/uploads/2026/09/CTE-Research-Sheet-Kristjan-Kullamagi-market-wizards-next-generation.pdf) [F]
- Minervini (*Trade Like a Stock Market Wizard*, *Think & Trade Like a Champion*): max stop 10%, average loss target ~5-6%; risk per trade ~1.25-2.5% of equity; 4-6 positions typical when fully invested (concentration), up to 10-12 max; "progressive exposure" — start small after losses and raise size only as trades work; never let a good-sized gain turn into a loss. [K] — summarized at [Chartmill SEPA](https://www.chartmill.com/documentation/trading-and-investing/methodologies/523-SEPA-Explained-Mark-Minervinis-Specific-Entry-Point-Analysis-System)
- Van Tharp (*Trade Your Way to Financial Freedom*): R = initial risk per share (entry − stop); every outcome measured as an R-multiple; expectancy = mean R-multiple across trades; "position sizing" is the key to meeting objectives; SQN (system quality number) = √N × mean(R)/stdev(R). [K] — [Van Tharp Institute](https://www.vantharp.com/) (not fetched)
- Expectancy formula: E = (Win% × Avg Win) − (Loss% × Avg Loss). Example: 30% win rate, avg win 5R, avg loss 1R → E = 0.30×5 − 0.70×1 = +0.8R per trade. [arithmetic]
- Kelly criterion: f* = W − (1 − W)/R, where W = win probability and R = avg win/avg loss (payoff ratio); full Kelly maximizes long-run log growth but has very large drawdowns and is highly sensitive to estimation error, so practitioners use fractional Kelly (¼-½). Half Kelly gives ~75% of the growth rate with roughly half the volatility. — [Wikipedia: Kelly criterion](https://en.wikipedia.org/wiki/Kelly_criterion) [K]. Worked example: W = 0.30, R = 5 → f* = 0.30 − 0.70/5 = 0.16 (16% of capital *at risk* per bet — far above the 0.5-1% practitioners use, showing how fractional/conservative real sizing is).
- Pyramiding (Livermore/O'Neil/Darvas): add only after the initial position shows a profit, in decreasing size (e.g., O'Neil: initial buy, then add ~2-3% higher, total buys within ~5% of the pivot); never average down. — [Wikipedia: Jesse Livermore](https://en.wikipedia.org/wiki/Jesse_Livermore) [K]
- Drawdown math (required gain to recover = 1/(1−d) − 1): −10% → +11.1%; −20% → +25%; −25% → +33.3%; −33% → +50%; −50% → +100%; −75% → +300%; −90% → +900%. [arithmetic]
- Losing streaks: with a 30% win rate, probability of 10 straight losers = 0.7^10 ≈ 2.8%; over 500 trades, such streaks are near-certain. At 1% risk, 10 losses ≈ −9.6% drawdown; at 5% risk, ≈ −40%. [arithmetic]

### Inferences
- Practical rulebook defaults: risk 0.5% per trade while learning or in choppy regimes, 1% in confirmed uptrends; max 1.5-2%. Max position size 20-25% of equity (liquidity permitting). Portfolio heat ≤ 6% (sum of open R). Cut exposure (halve risk) after a 3-5 loss streak or a 7-10% equity drawdown; stop trading new setups at −15% to −20% equity drawdown and review.
- Concentration: momentum traders run 4-12 positions; academic momentum portfolios run deciles (dozens to hundreds of stocks). Concentration raises variance and drawdown far beyond the academic factor, so stop discipline must substitute for diversification.
- Gap risk: stops do not protect against overnight gaps (earnings, Indian circuit limits); size so that a gap of 2-3× the stop distance on any one name is survivable.

### Gaps
- No independent, audited study confirming Minervini's or Qullamaggie's exact position-size rules; these are self-reported.
- Kelly figures above are formula-based; I did not fetch an empirical study of fractional Kelly in equity swing trading.

---

## 4. Evidence: what academic research supports, and base rates of retail trader success

### Takeaway
The core ingredients (cross-sectional momentum, time-series momentum/trend following, the 52-week-high effect, and post-earnings-announcement drift) are among the most robust anomalies in finance, including in India. Chart patterns and indicator rules have much weaker, era- and data-snooping-sensitive evidence. Meanwhile, base rates for active retail traders are grim: ~88-93% of Indian F&O traders lose money each year, 97% of persistent Brazilian day traders lost money, and <1% of Taiwanese day traders are predictably profitable.

### Cited Findings

**Momentum and related anomalies**
- Jegadeesh & Titman (1993): buying past 3-12-month winners and selling losers earned ~1% per month over the following 3-12 months (US, 1965-1989); profits partly reverse after 1-2 years. — [Journal of Finance, DOI 10.1111/j.1540-6261.1993.tb04702.x](https://doi.org/10.1111/j.1540-6261.1993.tb04702.x) [K]
- Moskowitz, Ooi & Pedersen (2012), "Time series momentum": a security's own past 12-month return predicts its future return across futures/forwards in equity indices, currencies, commodities and bonds; partial reversal at longer horizons; diversified TSMOM performs best in extreme markets. — [JFE 104(2):228-250](https://doi.org/10.1016/j.jfineco.2011.11.003) [F for citation; 58-instrument count not verified]
- George & Hwang (2004): nearness of price to the 52-week high explains a large portion of momentum profits and dominates past-return-based momentum in forecasting; returns do not reverse in the long run. Later work finds 52-week-high profits in 18 of 20 international markets. — [Journal of Finance 59(5):2145-2176](https://doi.org/10.1111/j.1540-6261.2004.00695.x) [F]; [CXO Advisory summary](https://www.cxoadvisory.com/1284/technical-trading/the-52-week-high-as-a-momentum-indicator-for-individual-stocks/) [F]
- Post-earnings-announcement drift (Bernard & Thomas 1989): stocks with the most positive earnings surprises continue to drift up for ~60 trading days after the announcement (and negative surprises drift down) — supports CAN SLIM "C" and Qullamaggie EPs. — [Journal of Accounting Research 27, DOI 10.2307/2491062](https://doi.org/10.2307/2491062) [K]
- Momentum crashes (Daniel & Moskowitz 2016): momentum suffers rare, severe crashes, typically in "panic states" right after market declines when the market rebounds sharply — the risk practitioners' market-regime filters try to manage. — [JFE 122(2), DOI 10.1016/j.jfineco.2015.12.002](https://doi.org/10.1016/j.jfineco.2015.12.002) [K]
- India: momentum profits documented and not explained by CAPM/FF3, concentrated in winners. — [Ansari & Khan 2012](https://emerald.com/insight/content/doi/10.1108/03074351211193730/full/html) [F]; [Maheshwari & Dhankar 2017](https://econpapers.repec.org/RePEc:eme:jamrpp:jamr-11-2015-0081) [F]

**Technical analysis more broadly**
- Brock, Lakonishok & LeBaron (1992): simple moving-average and trading-range-breakout rules on the DJIA (1897-1986) had predictive power; later work (Sullivan, Timmermann & White 1999) shows much of this weakens after correcting for data snooping and in later samples. — [JF, DOI 10.1111/j.1540-6261.1992.tb04681.x](https://doi.org/10.1111/j.1540-6261.1992.tb04681.x) [K]
- Lo, Mamaysky & Wang (2000): automated pattern recognition finds several technical patterns (e.g., head-and-shoulders) provide incremental information on Nasdaq stocks, though not necessarily exploitable profits. — [JF, DOI 10.1111/0022-1082.00265](https://doi.org/10.1111/0022-1082.00265) [K]
- Park & Irwin (2007) survey: of 95 "modern" studies, 56 found positive TA profits, 20 negative, 19 mixed — but many suffer data snooping, ex-post rule selection and cost-estimation problems; evidence is stronger in older samples and futures/FX than recent equities. — [Journal of Economic Surveys, DOI 10.1111/j.1467-6419.2007.00519.x](https://doi.org/10.1111/j.1467-6419.2007.00519.x) [K]

**Retail trader base rates**
- SEBI FY22-FY24 study (Sept 2024): 93% of ~1.13 crore individual F&O traders lost money over FY22-24; aggregate losses > ₹1.8 lakh crore. — [News On Air (Govt.)](https://www.newsonair.gov.in/sebi-study-reveals-individual-traders-face-severe-losses-in-equity-fo-segment) [F]; [Business Standard](https://www.business-standard.com/markets/capital-market-news/sebi-study-exposes-massive-losses-for-individual-f-o-traders-in-india-124092400948_1.html) [F]
- SEBI FY22 study (Jan 2023): 89% (9 in 10) of individual F&O traders lost money in FY22. — [Business Standard, Jan 2023](https://www.business-standard.com/article/finance/9-out-of-10-individual-traders-in-f-o-segment-making-losses-123012600435_1.html) [F]
- SEBI FY25 study (July 2025): 91% of individual F&O traders lost money; net losses rose 41% to ₹1,05,603 crore from ₹74,812 crore in FY24. — [Business Standard, July 2025](https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html) [F]
- SEBI FY25-FY26 study ("Profitability of Individual Traders in the Equity Derivatives Segment (FY25-FY26)", Aug 2026): 87.7% of individual traders lost money in FY26 (vs 90.9% in FY25); 82.1% lost even before costs; aggregate losses ₹91,685 crore in FY26 (FY25 revised to ~₹1,11,788 crore); average loss per trader ~₹1.17 lakh; active traders fell ~18% to 87.5 lakh (one outlet says 78.6 lakh — conflict); options ~92% of losses, futures loss rate ~66%; 43% of traders under 30; transaction costs ~₹25,000 crore in FY26 (brokerage ~44%, STT ~27%). — [SEBI on X](https://x.com/SEBI_updates/status/2090451964626894921) [F]; [Finnovate summary](https://www.finnovate.in/learn/blog/sebi-fno-trader-losses-fy26-individual-derivatives) [F]; [Coinswitch](https://coinswitch.co/switch/personal-finance/sebi-profitability-report/) [F]; [Open Magazine](https://openthemagazine.com/business/sebi-fo-loss-study-explained-why-9-in-10-retail-traders-lost-91685-crore-in-fy26) [F]. (Figures via secondary sources; SEBI PDF not opened.)
- Brazil (Chague, De-Losso & Giovannetti, 2019/2020): of individuals who began day trading mini-Ibovespa futures in 2013-2015 and persisted ≥300 days, 97% lost money, only 0.4% earned more than a bank teller's wage (top individual ~US$310/day), and no evidence of learning. — [RePEc/IDEAS](https://ideas.repec.org/p/fgv/eesptd/525.html) [F]; [Quantpedia summary](https://quantpedia.com/retail-day-trading-is-an-uphill-battle/) [F]
- Taiwan (Barber, Lee, Liu & Odean 2014): using complete TSE data 1992-2006, less than 1% of day traders are able to predictably earn positive abnormal returns net of fees; past top performers do continue to earn ~38 bps/day while the rest lose. — [JFM 18:1-24 (IDEAS)](https://ideas.repec.org/a/eee/finmar/v18y2014icp1-24.html) [F]; [Working paper PDF](https://faculty.haas.berkeley.edu/odean/papers/day%20traders/Day%20Trading%20Skill%20110523.pdf) [F]
- Barber & Odean (2000): US households that traded most earned 11.4% annually vs 17.9% for the market (1991-96) — overtrading destroys returns. — [JF, DOI 10.1111/0022-1082.00226](https://doi.org/10.1111/0022-1082.00226) [K]

### Inferences
- The defensible core of these systems is "buy strength near highs, after strong earnings, in uptrending markets, and cut losers" — this maps directly to momentum, 52-week-high and PEAD evidence. Specific chart-pattern shapes (exact cup depth, handle length) have little independent evidence and should be treated as entry-timing/risk-definition tools, not alpha sources.
- The SEBI and Brazil/Taiwan data imply that a retail trader's prior should be that they will lose money net of costs; the burden is on a documented, cost-inclusive, out-of-sample track record before scaling size. Short-dated options and intraday trading are the worst-evidenced venues.

### Gaps
- SEBI PDFs not opened directly (sebi.gov.in not fetched); FY26 trader count conflict (87.5 lakh vs 78.6 lakh) unresolved.
- No academic study found evaluating SEPA/VCP, CAN SLIM or Qullamaggie setups out of sample with costs.

---

## 5. Combining fundamentals with technicals

### Takeaway
The best-known systems are explicitly "techno-fundamental": fundamentals (EPS/sales growth, ROE, catalysts) pick *what* to buy; Stage 2/Trend Template and pivots decide *when*; and the stop decides *how much*. A practical rule: only buy fundamentally strong stocks when they are in Stage 2, and ignore (or exit) fundamentally strong stocks in Stage 4.

### Cited Findings
- CAN SLIM combines C/A/N/I (fundamental and ownership) with S/L/M (supply-demand, relative strength, market trend). — [AAII CAN SLIM](https://www.aaii.com/journal/article/william-oneil-can-slim-approach-to-selecting-growth-stocks) [F]
- Minervini's SEPA requires both Trend Template (Stage 2) and fundamental criteria (earnings/sales growth, surprises) plus a catalyst before a VCP entry. — [Chartmill SEPA](https://www.chartmill.com/documentation/trading-and-investing/methodologies/523-SEPA-Explained-Mark-Minervinis-Specific-Entry-Point-Analysis-System) [F]
- Minervini buys only Stage 2 (Weinstein's advancing stage). — [MarketInOut Stage 2 (India)](https://www.marketinout.com/stock-screener/stage-2-uptrend/india) [F]
- Darvas called his method "techno-fundamentalist": industry/earnings growth for selection, boxes for timing. — [Wikipedia: Nicolas Darvas](https://en.wikipedia.org/wiki/Nicolas_Darvas) [K]
- PEAD (earnings surprise drift) and price momentum are distinct but complementary signals; Qullamaggie's EP is an implementation of trading the surprise gap. — [Bernard & Thomas 1989](https://doi.org/10.2307/2491062) [K]; [Financial Wisdom: EP](https://www.financialwisdomtv.com/post/the-episodic-pivot-strategy-qullamaggie-s-high-momentum-setup-explained) [F]

### Inferences
- Pipeline for an AI stock-picking playbook (India): Step 1 fundamental screen (latest quarter EPS & sales growth ≥ 25% YoY, 3-yr EPS CAGR ≥ 20-25%, ROE ≥ 15-17%, low pledge, adequate liquidity) → Step 2 technical gate (Trend Template pass, RS percentile ≥ 80, within 25% of 52-week high) → Step 3 market regime (Nifty 500 above rising 50/200-DMA; no distribution cluster) → Step 4 entry on base/VCP pivot with volume ≥1.5× average or on an earnings-gap EP → Step 5 risk: 0.5-1% equity risk, stop ≤ 8%, portfolio heat ≤ 6%, trail with 20/50-DMA, sell partial at 2-3R.
- Pure-momentum (Qullamaggie, Nifty200 Momentum 30) works without fundamentals but with higher turnover and crash risk; adding the fundamental filter mainly reduces "junk" momentum and pump-driven small-caps, a particular risk in Indian SME/small-cap segments.

### Gaps
- No rigorous comparative study (fundamental + Stage 2 vs Stage 2 alone) found for Indian equities.
