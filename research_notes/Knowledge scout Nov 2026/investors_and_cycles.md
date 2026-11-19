# Investor playbooks and Indian market cycles (1990-2026)

Knowledge scout, researched 2026-11-19. Seed file: `memdb/seeds/2026-11-19_investors_cycles.json` (45 records). Confidence labels: verified (2+ sources), single-source, unverified (folklore or unchecked). Research notes, not investment advice.

## Library 1 - Investor playbooks (people)

### Stanley Druckenmiller - liquidity-driven macro, concentrated sizing

`person:stanley-druckenmiller` | confidence: **verified** | tags: us, global, process, macro, position-sizing

Duquesne Capital 1981-2010: ~30% average annual return, widely reported as no losing year, though some reports say 2010 (closing year) was down ~5%; returns never publicly audited, so treat as press-reported. Lead PM of Soros's Quantum Fund 1988-2000. Structural edge: in the Soros seat he could deploy multi-billion positions in currencies, bonds and stocks with leverage. Process edge: markets are driven by liquidity (central banks, credit), not earnings; he looks 18-24 months ahead; he sizes very large when conviction and risk/reward line up and cuts fast when wrong ('it's not whether you're right or wrong, but how much you make when right'). Signature trade: Sept 1992 short of sterling before ERM exit (~$1bn, Wikipedia puts Quantum gain at ~$1.8bn for the week). Biggest mistake: 1999-2000 he shorted tech, gave up, then bought ~$6bn of tech near the March 2000 top (unverified figure) and Quantum lost heavily; he left in April 2000. He also says he sold Nvidia too early in 2024. Copyable for an individual: track RBI/Fed liquidity and credit spreads as the master variable; make few large bets, not many small ones; exit as soon as the thesis breaks; when a regime changes, change your mind without ego. Not copyable: leverage, FX/bond access, information flow.

| key | value |
|---|---|
| edge_structural | multi-asset leverage, scale, macro information network |
| edge_process | liquidity first, 18-24m horizon, concentrated sizing, fast cuts |
| signature_trades | GBP short 1992 (~$1bn+); avoided 2008; tech round-trip 2000 (loss) |
| track_record | ~30%/yr 1981/86-2010 (press, unaudited) |
| mistakes | bought tech at 2000 top; sold Nvidia early (2024) |
| copyable | liquidity dashboard, concentration with stop discipline |

Links: strategy:druckenmiller-liquidity (about); strategy:position-sizing (illustrates); person:george-soros (similar_to)

Sources: <https://www.wikipedia.org/wiki/Stanley Druckenmiller> ; <https://moneyweek.com/441992/the-worlds-greatest-investors-stanley-druckenmiller> ; <https://www.businessinsider.in/finance/the-fabulous-life-of-stanley-druckenmiller-the-hedge-funder-who-says-old-people-are-robbing-young-people-blind/slidelist/21292399.cms> ; <https://www.aol.com/finance/stan-druckenmiller-reveals-one-stock-231700663.html>

### George Soros - reflexivity and boom-bust trading

`person:george-soros` | confidence: **verified** | tags: us, global, process, macro, base-rate

Quantum Fund (with Jim Rogers from 1973) compounded roughly ~30% a year from 1969 to 2000 by commonly cited estimates (unaudited, press figures). Structural edge: global macro mandate, leverage, and later Druckenmiller as PM. Process edge: reflexivity - market prices do not just reflect fundamentals, they change them (rising stock prices let firms raise cheap capital, rising collateral values let banks lend more), producing self-reinforcing booms that overshoot and then reverse. He looks for a prevailing bias plus a flaw, invests early in the boom, and shorts when the trend is exhausted; 'invest first, investigate later' with small size, then add. Signature trade: 1992 sterling short with Druckenmiller (~$1bn widely reported; ~$1.8bn for the week per Wikipedia). Mistakes: Oct 1987 he was positioned for a Japan crash and lost heavily selling US futures near the low (~$300m+ in days, figure unverified); 1998 Russia losses (~$2bn, unverified); 2000 tech losses. Copyable: map credit-fuelled feedback loops (India 2007 infra/realty, 2023-24 PSU rerating, 2024 SME IPOs) and ask what breaks the loop (funding, regulation, supply); scale in as evidence confirms. Not copyable: macro leverage and access.

| key | value |
|---|---|
| edge_process | reflexive feedback loops, bias + flaw, probe then scale |
| signature_trades | GBP 1992 |
| mistakes | 1987, 1998 Russia, 2000 tech |
| track_record | ~30%/yr 1969-2000 (press, unaudited) |
| copyable | identify loops and their break points |

Links: strategy:soros-reflexivity (about); person:stanley-druckenmiller (similar_to)

Sources: <https://www.wikipedia.com/wiki/Soros_Fund> ; <https://www.wikiwand.com/en/articles/Quantum_Fund> ; <https://www.pressreader.com/uk/money-week/20220520/282046215707570>

### Ed Thorp - quantified edge and Kelly sizing

`person:ed-thorp` | confidence: **verified** | tags: us, process, quant, position-sizing, base-rate

Mathematician who proved blackjack card counting (Beat the Dealer, 1962) and then applied the same logic to markets: only bet when you can quantify a positive expectation, and size by the Kelly criterion. Princeton Newport Partners (Nov 1969-1988): ~19.1% gross / ~15.1% net annualised (some sources say 20% net), with one source reporting 227 winning months and 3 losing months (all <1%). Structural edge: early mathematical pricing of warrants and options (a Black-Scholes-like formula before 1973), convertible arbitrage, statistical arbitrage - hedged, market-neutral books. The fund closed after the 1988 RICO raid tied to the Drexel investigation; Thorp was never charged. He also spotted Madoff in 1991 by noticing the options volume Madoff claimed to trade did not exist. Mistake: the partnership's structural dependence on a partner's office (the RICO case) ended a great record - operational/counterparty risk, not market risk. Copyable for individuals: (1) half-Kelly or smaller sizing - never bet so big that a loss ends the game; (2) check feasibility of any too-smooth record before trusting it; (3) Thorp himself recommends index funds for most people. Not copyable: arbitrage infrastructure.

| key | value |
|---|---|
| edge_structural | option/convert pricing models, hedged arbitrage |
| edge_process | positive expectation + Kelly sizing |
| track_record | ~19.1% gross, ~15.1% net 1969-1988; 3 losing months of 230 (single-source) |
| mistakes | operational/legal risk via Princeton office |
| copyable | fractional Kelly, fraud feasibility checks, indexing |

Links: strategy:thorp-kelly (about); strategy:position-sizing (illustrates); insight:avoid-ruin (illustrates)

Sources: <https://en.wikipedia.org/wiki/Princeton_Newport_Partners> ; <https://Www.Wikipedia.org/wiki/Edward_Thorp> ; <https://moneyweek.com/461698/edward-thorp-the-worlds-greatest-investors> ; <https://www.fool.com/investing/2017/01/26/the-riveting-story-of-edward-thorp.aspx>

### Jim Simons - Renaissance Medallion (the uncopyable edge)

`person:jim-simons` | confidence: **verified** | tags: us, quant, process, luck-vs-skill, base-rate

Mathematician (codebreaker, Chern-Simons) who founded Renaissance Technologies (1982). Medallion fund, per Zuckerman's The Man Who Solved the Market: ~66% gross / ~39% net a year 1988-2018, ~$104.5bn of trading profits, fees of 5% of assets plus up to 44% of profits. Medallion has been closed to outsiders for decades and capped (~$10bn) because its edge is capacity-limited. Structural edge: decades of cleaned data, hundreds of PhD scientists (not finance people), huge compute, very short holding periods, thousands of small statistically weak but persistent signals, high leverage, and extreme secrecy. Its public funds (e.g., RIEF) did far worse - reportedly lost ~20-30% in 2020 while Medallion gained (figures unverified) - proof the edge does not scale to longer horizons. Mistake/near-death: Medallion's early years (1989) had a large drawdown that led Simons to rebuild the models with Berlekamp (unverified detail). Simons died in May 2024. Lesson for an individual: this is the clearest example of an edge that cannot be copied; anyone selling 'Medallion-like' retail algos is misleading. What can be copied is the attitude: trust data over stories, kill signals that stop working, and let the system (not emotions) execute.

| key | value |
|---|---|
| track_record | 66% gross / 39% net 1988-2018 (Zuckerman; Cornell 2020 paper questions how) |
| edge_structural | data, scientists, compute, short horizon, leverage, capacity cap |
| copyable | systematic rules, data over narrative; NOT the returns |

Links: insight:luck-vs-skill (about); insight:ai-picking-evidence (about); insight:investor-edge-taxonomy (illustrates)

Sources: <https://www.wealthmanagement.com/alternative-investments/jim-simons-built-the-best-hedge-fund-ever> ; <https://www.institutionalinvestor.com/article/b1k2fymby99nj0/Famed-Medallion-Fund-Stretches-Explanation-to-the-Limit-Professor-Claims> ; <https://quartr.com/insights/company-research/renaissance-technologies-and-the-medallion-fund>

### John Templeton - global bargain hunting at maximum pessimism

`person:john-templeton` | confidence: **single-source** | tags: global, us, process, contrarian, base-rate

Pioneer of global investing. Folklore-grade but widely repeated: in Sept 1939, at the outbreak of WWII, he borrowed $10,000 and bought 100 shares of every NYSE stock trading under $1 (~104 companies, ~34 in bankruptcy) and sold ~4 years later for roughly 4x (details unverified in this research). Templeton Growth Fund (1954-1992): $10,000 grew to ~$2m by 1992, ~13.96% annualised per one source (14.5% often quoted, unverified). Structural edge: early access to cheap foreign markets - he bought Japan in the 1960s at P/E ~3-4x when few Westerners did. Process: 'the time of maximum pessimism is the best time to buy'; compare price with value across every country and industry; buy the cheapest relative to long-term earnings power; diversify widely. His cycle line: 'bull markets are born on pessimism, grow on skepticism, mature on optimism and die on euphoria.' Mistakes: exited Japan years before its 1989 peak (early, missed the final leg); a diversified value approach lags in growth-led eras. 1999-2000 he reportedly shorted Nasdaq IPOs around lock-up expiries (unverified). Copyable: keep a global/sector 'cheapest vs own history' list and act when news is worst; diversify bargain baskets rather than betting on one distressed name; use his pessimism-to-euphoria ladder as a cycle checklist.

| key | value |
|---|---|
| signature_trades | 1939 sub-$1 basket (folklore, ~4x); Japan 1960s |
| track_record | TGF ~14%/yr 1954-1992 (single-source) |
| mistakes | left Japan too early |
| copyable | max-pessimism buying, cheap-vs-history global screen |

Links: strategy:templeton-max-pessimism (about); insight:india-cycle-top-bottom-signals (about)

Sources: <https://www.caproasia.com/?p=13086> ; <https://www.oreilly.com/library/view/templetons-way-with/9781118149614/xhtml/Chapter03.html> ; <https://fa-mag.com/news/academia-vs--the-real-world-part-1-42332.html>

### Seth Klarman - margin of safety, cash, and complexity

`person:seth-klarman` | confidence: **verified** | tags: us, process, value, avoid-ruin

Founded Baupost (1982/83). Record varies by window: ~19% net a year vs 11% for the S&P 500 to 2010 (Bloomberg); 'just over 20%' with one losing year (Ivey); 16.4% to end-2015 (CNBC); but only ~4% a year since 2014 per investors, with clients pulling ~$7bn since 2021 (Bloomberg, Jan 2025). Structural edge: patient endowment-style capital (Harvard-type LPs) that let him hold large cash (often 30-50%) and buy illiquid, complex assets others are forced to sell - bankruptcy claims (e.g., Lehman claims after 2008), distressed debt, post-reorganisation equities, real estate. Process: absolute-return mindset; buy at a big discount to conservatively estimated value; focus on downside first; catalysts help; avoid leverage. His 1991 book Margin of Safety is out of print. Mistakes: long cash drag in a decade-long bull market; post-2014 performance shows an edge in distress needs distress to exist. Copyable: write down the downside value first; accept holding cash when nothing is cheap; hunt for forced sellers (index deletions, spin-offs, rights issues, promoters under margin call, MF redemptions in smallcaps) - India's 2018 and 2020 smallcap selloffs were Klarman-style opportunities. Not copyable: buying Lehman claims.

| key | value |
|---|---|
| track_record | ~19-20% net 1983-2010; 16.4% to 2015; ~4%/yr since 2014 (Bloomberg) |
| source_quality | press + LP-reported; Baupost does not publish |
| mistakes | cash drag, post-2014 lag |
| copyable | downside-first, forced-seller hunting, permission to hold cash |

Links: strategy:klarman-margin-of-safety (about); insight:avoid-ruin (illustrates)

Sources: <https://www.bloomberg.com/news/articles/2010-06-17/the-financial-life-seth-klarman> ; <https://ivey.uwo.ca/bengrahaminvesting/resources/interviews-notes/seth-a-klarman> ; <https://www.cnbc.com/2016/08/30/how-to-think-like-value-investing-idol-seth-klarman.html> ; <https://www.bloomberg.com/news/articles/2025-01-22/baupost-clients-pulled-7-billion-since-2021-after-poor-returns>

### Joel Greenblatt - special situations and the Magic Formula

`person:joel-greenblatt` | confidence: **single-source** | tags: us, process, value, special-situations, weak-factor

Gotham Capital (1985): ~50% annualised over its first decade, per Greenblatt's own book You Can Be a Stock Market Genius (1997) - self-reported, not audited (confidence: single-source); outside capital returned in 1994-95. Structural edge (early): small fund size allowed meaningful positions in spin-offs, restructurings, rights offerings, merger securities and LEAPS where institutions are forced or uninterested sellers. Process: find situations where the seller is not price-sensitive (parent shareholders dumping spin-off shares, index deletions), concentrate in 6-8 names. Later the Magic Formula (The Little Book That Beats the Market, 2005): rank by return on capital (EBIT / net working capital + net fixed assets) and earnings yield (EBIT / EV), buy the top 20-30, rebalance yearly; backtest 1988-2004 ~30.8%/yr vs S&P ~12.4% (backtest, not live). Live results of formula funds and many replications were far weaker and long periods of underperformance made most users quit. Mistakes: the public long-short Gotham funds lagged in the 2010s growth era (unverified magnitude). Copyable for an Indian individual: spin-off and demerger watchlist (Indian demergers often sell off as funds exit the new listing), rights-issue and open-offer arbitrage; Magic-Formula-style screen as an idea generator, not a black box.

| key | value |
|---|---|
| track_record | ~50%/yr 1985-1994 (self-reported) |
| magic_formula_backtest | 30.8% vs 12.4% 1988-2004 (backtest) |
| mistakes | live formula lag; quitting behaviour |
| copyable | demerger/spin-off watchlist, ROC + earnings-yield screen |

Links: strategy:greenblatt-special-situations (about); insight:weak-factor-folklore (about)

Sources: <https://www.oreilly.com/library/view/profiting-from-hedge/9781118465172/xhtml/Chapter08.html>

### Michael Burry - primary-document deep value and the Big Short

`person:michael-burry` | confidence: **verified** | tags: us, process, value, contrarian, blowup

Scion Capital (Nov 2000-2008): +489.34% net of fees to June 2008 vs ~2-3% for the S&P 500 incl. dividends; investors made ~$700m+, Burry ~$100m. Early gains came from deep value and shorting dot-com stocks (2001 +55% per a blog, less reliable). Signature trade: from May 2005 bought credit default swaps on subprime mortgage bonds (first $60m from Deutsche Bank) after reading the actual loan pools in prospectuses; investors revolted and he side-pocketed positions during 2006-07 losses before the payoff; he exited CDS by April 2008. Structural edge: a tiny, unconstrained fund able to buy obscure securities; process edge: reads primary documents others skip, EV/EBITDA-style deep value screens, willingness to look wrong for 2+ years. Later: GameStop stake 2019 (sold before most of the 2021 squeeze); public 'crash' warnings repeatedly early (e.g., 2023 'Sell' tweet and index puts); deregistered Scion Asset Management in Nov 2025 after bearish AI-hyperscaler depreciation calls. Mistakes: investor-relations failure in 2006-07; serial premature macro calls. Copyable: read the annual report, notes and loan/collateral disclosures yourself; size contrarian bets so you can survive being early. Do not copy: public doom predictions as a timing tool.

| key | value |
|---|---|
| track_record | +489% net Nov 2000-Jun 2008 vs S&P ~+3% (2+ sources) |
| signature_trades | subprime CDS 2005-08; GME 2019 |
| mistakes | investor revolt 2006-07, early macro calls 2015-2025 |
| copyable | primary-document reading, survivable sizing for early contrarian bets |

Links: strategy:variant-perception (illustrates); insight:avoid-ruin (about)

Sources: <https://en.wikipedia.org/wiki/Michael_Burry> ; <https://en.wikipedia.org/wiki/Scion_Asset_Management> ; <https://moneyweek.com/investments/tech-stocks/big-short-investor-michael-burry-closes-hedge-fund-scion-capital>

### Bill Ackman - concentrated quality activism plus asymmetric hedges

`person:bill-ackman` | confidence: **verified** | tags: us, process, activism, concentration, blowup

Pershing Square (2004). Structural edge: activist stakes large enough to change boards/management; permanent capital via Pershing Square Holdings (listed 2014) so LPs cannot run. Process: 8-12 simple, predictable, free-cash-flow-generative businesses with pricing power and low leverage, bought when temporarily mispriced, plus cheap asymmetric macro hedges. Signature wins: General Growth Properties after its 2009 bankruptcy (~$60m into ~$1.6bn+, unverified); Canadian Pacific turnaround 2011-16 (~$2.6bn profit, unverified); Chipotle and Hilton; Feb-Mar 2020 credit default swap hedge that made ~$2.6bn (premium cost ~$27m widely reported but not confirmed here). Biggest mistakes: Valeant 2015-17 - concentrated bet on a roll-up whose growth came from price gouging and acquisitions; ~$4bn loss (CNBC). Herbalife $1bn short (2012-18, loss), JC Penney (2010-13, loss). PSH had four straight losing years 2015-18 before +58% (2019) and +70% (2020) (unverified exact figures). Copyable: own a small number of high-quality compounders bought on temporary bad news; use cheap options/hedges where payoff is many times premium; never let a roll-up's adjusted earnings substitute for organic growth (Valeant lesson maps to Indian acquisition-led stories). Not copyable: activism.

| key | value |
|---|---|
| signature_trades | GGP 2009, CP 2011-16, COVID CDS 2020 (+$2.6bn) |
| mistakes | Valeant (-$4bn), Herbalife short, JCPenney |
| copyable | quality concentration on bad news; asymmetric hedges; roll-up skepticism |

Links: strategy:ackman-quality-activism (about); insight:disqualifiers (illustrates)

Sources: <https://www.cnbc.com/2017/03/20/hedge-fund-titans-surefire-bet-turns-into-a-4-billion-loss.html> ; <https://fortune.com/2017/03/13/bill-ackman-valeant-exit-loss/> ; <https://moneyweek.com/economy/people/601185/bill-ackman-the-billionaire-who-bet-big-on-viral-doom> ; <https://businessinsider.in/miscellaneous/meet-bill-ackman-the-controversial-hedge-fund-manager-who-made-2-6-billion-off-the-coronavirus-market-crash-in-march/slidelist/75074028.cms>

### Chuck Akre - the three-legged stool compounder approach

`person:chuck-akre` | confidence: **single-source** | tags: us, process, quality, compounding, low-turnover

Akre Capital Management; ran FBR Focus Fund, then the Akre Focus Fund from 2009 (John Neff and Chris Cerrone later took over; Akre stepped back from the strategy around 2020). Returns: compounded over ~13% a year since 2009 (Quartr) and top-third rankings vs peers for years; a Substack figure of 15.44% vs 14.22% for the S&P 500 is unverified; Q4 2024 -0.41% vs +2.41% for the S&P. Process edge: the 'three-legged stool' - (1) an extraordinary business with high returns on owners' capital, (2) talented management with integrity who treat shareholders as partners, (3) a long runway to reinvest free cash flow at high returns. When all three exist it is a 'compounding machine' and the job is to sit still. Signature long holds: American Tower, Mastercard, Moody's, O'Reilly Automotive, later KKR and Constellation Software. Structural edge: patient capital and very low turnover, small team. Mistakes: low turnover means sitting through valuation compression (2022 drawdown) and occasional late exits from businesses whose reinvestment runway faded (unverified specifics). Copyable: the three questions are a direct checklist for Indian compounders (e.g., ROE >20%, honest promoter, reinvestment runway); hold winners; measure in 5-year blocks.

| key | value |
|---|---|
| track_record | >13%/yr since 2009 (Quartr; single-source) |
| copyable | three-legged-stool checklist, low turnover |
| mistakes | valuation compression drawdowns |

Links: strategy:akre-three-legged-stool (about); strategy:marcellus-cc (similar_to)

Sources: <https://quartr.com/insights/investment-strategy/chuck-akre-above-average-returns-and-a-legendary-framework> ; <https://www.akrefund.com/?p=3457> ; <https://www.gurufocus.com/news/1009011> ; <https://seekingalpha.com/article/4749930-akre-focus-fund-q4-2024-commentary>

### Nick Sleep - Nomad and 'scale economies shared'

`person:nick-sleep` | confidence: **verified** | tags: global, process, quality, compounding, low-turnover

Nomad Investment Partnership with Qais Zakaria (2001-2013/14): ~921% cumulative vs ~117% for MSCI World; ~20.8% a year net per one source vs ~6.5% for the index. Closed and returned capital in 2014 because they felt the work was done; partnership letters are public and widely studied. Early book: deep value in Asia/UK small caps; it evolved into a very concentrated portfolio of Amazon, Costco and Berkshire Hathaway (a German source says ~3 stocks at the end; uncorroborated). Process edge: 'destination analysis' - what will this business look like in 10-20 years - and the 'scale economies shared' model: firms that pass scale savings back to customers (Costco's low markups, Amazon's prices and free shipping) grow volume, which creates more scale savings, a flywheel competitors cannot match. Structural edge: an LP base and fee structure (performance fee over a hurdle, with deferral/clawback features - details unverified) that let them hold for a decade. Mistakes: Sleep wrote about errors of commission in early deep-value holdings and errors of omission (not sizing winners up sooner) - specifics unverified. Copyable: look for Indian companies that deliberately price low to widen the moat (DMart-style retail, low-cost brokers, platform businesses), judge them on customer value per rupee, and hold through quarterly noise.

| key | value |
|---|---|
| track_record | +921% vs +117% MSCI World 2001-2013/14 (2+ sources) |
| signature_trades | Costco, Amazon, Berkshire |
| copyable | destination analysis, scale-economies-shared test |

Links: strategy:sleep-scale-economies-shared (about); person:chuck-akre (similar_to)

Sources: <https://massivemoats.substack.com/p/a-deep-dive-analysis-into-the-nomad> ; <https://quartr.com/insights/investment-strategy/investing-mastery-with-nick-sleep-nomad-s-costco-investment> ; <https://www.morningstar.com.au/insights/personal-finance/254055/my-favourite-lessons-from-nick-sleeps-famous-investing-letters>

### Terry Smith - Fundsmith quality: buy good companies, don't overpay, do nothing

`person:terry-smith` | confidence: **verified** | tags: global, process, quality, low-turnover, base-rate

Fundsmith Equity launched 1 Nov 2010. To 31 Dec 2025: +612.9% cumulative, 13.8% annualised vs MSCI World +467.6% / 12.1% (fund's annual letter). But 2025 returned only +0.8% vs +12.8% for MSCI World - the fifth consecutive calendar year of underperformance (2021-2025) and the weakest year since inception; the since-inception annualised figure fell from 14.8% at end-2024. Process: three rules - buy good companies (high ROCE, high gross margins, cash conversion, low leverage, resilient demand, no banks or heavy cyclicals), don't overpay (free-cash-flow yield vs bonds), do nothing (very low turnover). ~25-30 holdings. Structural edge: low-fee, transparent fund with a long-horizon UK retail base. Smith blamed 2025 on index concentration in a few mega-caps, passive flows and dollar weakness. Mistakes: owning quality at 30-40x earnings left the fund exposed to de-rating (e.g., Novo Nordisk's 2024-25 collapse; earlier PayPal exit; unverified magnitudes). Lesson: even a sound quality process can lag for five years when style or valuation turns; 'don't overpay' is the rule most often broken. Copyable for Indians: the quality checklist maps well to India's consumer/financial compounders, but valuation discipline (FCF yield vs 10-year G-sec) matters most when quality trades at 60-80x.

| key | value |
|---|---|
| track_record | 13.8%/yr vs 12.1% MSCI World, Nov 2010-Dec 2025 (fund letter) |
| underperformance | 2021-2025 five straight years; 2025 +0.8% vs +12.8% |
| copyable | quality checklist + FCF-yield valuation guardrail |

Links: strategy:smith-quality-do-nothing (about); strategy:marcellus-cc (similar_to)

Sources: <https://www.fundsmith.co.uk/media/4hcfd1pg/2025-fef-annual-letter-web.pdf> ; <https://www.ajbell.co.uk/group/news/fundsmith-underperforms-fifth-calendar-year-row> ; <https://www.investmentweek.co.uk/investment-week/news/3069660/terry-smith-defends-weakest-returns-since-inception-for-fundsmith-equity> ; <https://www.ii.co.uk/analysis-commentary/terry-smith-blames-these-three-factors-2025s-underperformance-ii537765>

### Mohnish Pabrai - Dhandho, cloning, and concentrated India/commodity bets

`person:mohnish-pabrai` | confidence: **single-source** | tags: us, india, process, cloning, concentration, cyclical

Pabrai Investment Funds since 1999. Long-run record is murky: an app-store bio claims >28% net since inception (unreliable); a profile says $100,000 at inception became $1.207m by 30 Jun 2017 (~14.8% annualised) - the more checkable figure. The funds reportedly fell ~60-70% peak-to-trough in 2008-09 (unverified). Process: 'heads I win, tails I don't lose much'; a few concentrated bets in simple businesses in distress; openly clone other great investors' positions (13Fs, Indian superstar filings); checklists built from past errors. Signature trades: Fiat Chrysler (~2012-18, large gain), Rain Industries (India; bought ~2015 at ~$0.60/share, i.e., about Rs 40, rose roughly 10x by early 2018 - it and Fiat were his most concentrated positions in Jan 2018 - then gave back most of the gain), US coal miners in 2021-22 (large gains, unverified). India book later: Edelweiss Financial (7-8% stake 2023-24, under 1% by Sep 2025), Sunteck Realty (~6.7%). Mistakes: Horsehead Holdings (zinc recycler, bankrupt 2016 - near total loss); round-trips in cyclical commodity names (Rain) when he did not sell near peak margins. Copyable: cloning as idea sourcing, a written checklist, few bets; but in cyclicals sell when margins and P/B are peak, not when P/E looks low.

| key | value |
|---|---|
| track_record | ~14.8%/yr 1999-2017 (single profile); 2008 drawdown ~-60%+ (unverified) |
| signature_trades | Fiat Chrysler, Rain Industries (~10x then round-trip), coal 2021-22 |
| mistakes | Horsehead bankruptcy; cyclical round-trips |
| copyable | cloning, checklist; cyclical exit rule |

Links: strategy:pabrai-dhandho (about); insight:cloning-indian-superstars (about)

Sources: <https://www.5paisa.com/news/an-insight-into-the-investing-style-of-mohnish-pabrai> ; <https://trendlyne.com/portfolio/superstar-shareholders/69664/Q3-2025/mohnish-pabrai-portfolio> ; <https://en.wikipedia.com/wiki/Mohnish_Pabrai> ; <https://tekinvestor.s3.dualstack.eu-west-1.amazonaws.com/original/3X/c/c/cc5e33b3da0c71e7f81e56da46be5532b90d75de.pdf>

### Howard Marks - cycle positioning and second-level thinking

`person:howard-marks` | confidence: **verified** | tags: us, global, process, credit, base-rate, avoid-ruin

Co-founder of Oaktree Capital (1995); memos since 1990 (the Jan 2000 'bubble.com' memo called the tech top); books The Most Important Thing (2011) and Mastering the Market Cycle (2018). Structural edge: a credit/distressed-debt franchise with locked-up capital that can deploy when others must sell. Signature trade: in 2008 Oaktree raised $10.9bn for OCM Opportunities Fund VIIb - its largest distressed fund, 3x the previous one - began investing in May 2008 and deployed most of it between Lehman's bankruptcy and year-end 2008 (reportedly ~$500m a week), targeting 25-30%+ gross; by 2011 it had returned $3bn to LPs (final realised IRR not found). Process: 'second-level thinking' (what is priced in, not just what is good); 'you can't predict, you can prepare' - take the market's temperature (credit spreads, issuance quality, investor attitudes, 'too good to be true' deals) and lean aggressive when fear is high and defensive when risk appetite is high; winning by avoiding losers. Mistakes: his cautious memos were early in several long bull runs (e.g., 2017-2021) - temperature reading gives direction, not timing. Copyable: build a simple 'market temperature' checklist for India (smallcap-to-Nifty P/E premium, IPO/SME subscription multiples, F&O retail volumes, market cap/GDP, credit spreads) and adjust equity allocation in steps rather than going all-in or all-out.

| key | value |
|---|---|
| signature_trades | 2008 $10.9bn distressed fund |
| copyable | temperature checklist, stepwise allocation |
| mistakes | early caution in long bull runs |

Links: strategy:marks-cycle-temperature (about); insight:india-cycle-top-bottom-signals (about)

Sources: <https://www.privatedebtinvestor.com/oaktree-raises-10-9bn-distressed-fund/> ; <https://www.privatefundscfo.com/print-editions/2011-03/oaktree-hands-back-3bn-from-2008-fund/> ; <https://labusinessjournal.com/finance/firm-banked-distressed-debt/>

### Charlie Munger - mental models, inversion, and patience for few great bets

`person:charlie-munger` | confidence: **verified** | tags: us, process, quality, behavior, concentration

Wheeler, Munger & Co. partnership 1962-1975: ~19.8% a year vs ~5% for the Dow (Buffett's 1984 'Superinvestors' article), but with -31.9% in 1973 and -31.5% in 1974 (figures from that article; not re-checked here) - proof that concentration brings deep drawdowns. Berkshire vice-chairman from 1978; he pushed Buffett from Graham cigar butts to 'wonderful companies at fair prices' (See's Candies 1972). Signature trades: BYD - Berkshire's 2008 stake (~225m shares, ~$230-270m depending on source) became worth ~$8-9bn by 2023 per Munger, ~39x over 17 years per later reports, mostly sold 2022-25; Daily Journal sold part of its BYD holding in late 2021 at ~15x cost. Process edge: a 'latticework' of models from psychology, economics, biology and engineering; inversion ('tell me where I'll die so I never go there'); his 1995 'Psychology of Human Misjudgment' list of biases; extreme patience ('sit on your ass investing') and very few bets. Mistakes: Alibaba bought at Daily Journal in 2021 - he later called it one of his worst mistakes; early partnership drawdowns. Died Nov 2023 aged 99. Copyable: a pre-mortem/inversion checklist before every buy, a written bias list, and the willingness to hold cash until a rare fat pitch appears.

| key | value |
|---|---|
| track_record | ~19.8%/yr 1962-75 with -31.9%/-31.5% in 1973/74 (Buffett 1984, not re-checked) |
| signature_trades | See's 1972, BYD 2008 (~39x), Costco |
| mistakes | Alibaba 2021 |
| copyable | inversion, bias checklist, patience |

Links: strategy:munger-inversion (about); strategy:buffett-munger (part_of); person:warren-buffett (similar_to)

Sources: <https://www.cnbc.com/2023/02/15/charlie-munger-says-byd-is-far-ahead-of-tesla-in-china.html> ; <https://fortune.com/2023/02/16/charlie-munger-byd-stake-warren-buffett-berkshire-hathaway-china-tesla/> ; <https://finviz.com/news/327877/charlie-mungers-2008-investment-into-this-company-made-39x-returns-over-17-years-but-berkshires-timely-exit-may-have-cemented-the-profits>

### Philip Fisher - scuttlebutt growth investing

`person:philip-fisher` | confidence: **unverified** | tags: us, process, growth, scuttlebutt, low-turnover

Founded Fisher & Co. in 1931; author of Common Stocks and Uncommon Profits (1958), whose 15 points (sales growth runway, R&D effectiveness, margins, labour relations, management depth and integrity, long-range outlook) and 'scuttlebutt' method (interview customers, suppliers, competitors and ex-employees) shaped Buffett's shift towards quality growth. Signature trade: bought Motorola in 1955 when it was a car-radio maker and held it until his death in 2004 (folklore-grade; held ~5 decades); also Texas Instruments and Dow Chemical. Track record: never audited or published as a fund series - treat any CAGR claim as unverified. Process: very few holdings, held for decades; sell only if the original analysis was wrong, the company no longer meets the 15 points, or a far better opportunity appears - not because the stock looks expensive. Mistakes he described (Developing an Investment Philosophy): early in his career he tried to time the market and bought weak businesses on cheapness; also, never-sell can mean riding a fading leader (Motorola's long decline after the 1990s). Copyable for Indians: scuttlebutt is very doable - dealer checks, distributor calls, LinkedIn hiring trends, product reviews - and is a genuine individual edge in small/mid caps under-covered by analysts.

| key | value |
|---|---|
| signature_trades | Motorola 1955-2004 (folklore-grade) |
| track_record | none published (unverified) |
| copyable | scuttlebutt channel checks, 15-point checklist |

Links: strategy:fisher-scuttlebutt (about); person:warren-buffett (about)

Sources: <https://www.oreilly.com/library/view/templetons-way-with/9781118149614/xhtml/Chapter03.html>

### Sanjay Bakshi - moats, behavioural finance, 'bad news' investing (India)

`person:sanjay-bakshi` | confidence: **unverified** | tags: india, process, quality, behavior

Managing partner of ValueQuest Capital LLP (New Delhi), adviser to the ValueQuest India Moat Fund; long-time adjunct professor at MDI Gurgaon (behavioural finance and business valuation courses; course details not re-verified here); LSE economics; practising value investor in India for 25+ years. His blog (fundooprofessor) and lectures are among the best Indian writing on moats, Munger-style mental models, 'Lollapalooza' effects and the evolution from Graham-style cheapness to quality. Process edge (as he describes it): buy durable-moat businesses when temporary 'bad news' - regulatory scare, one-off loss, sector panic - pushes the price down, and hold; look for 'clean surprises' (businesses whose hidden strengths show up later in numbers); watch for incentive-caused bias in promoters. Track record: ValueQuest's fund returns are not public in this research - treat any number as unverified. Holdings: specific stock attributions circulating online (e.g., chemical or footwear names) could not be verified and are excluded. Mistakes: he has written about selling great businesses too early and owning cheap-but-poor businesses early in his career (characterisation). Copyable: his framework is entirely public - read the lectures, build a moat checklist (pricing power, switching costs, network effects, cost advantage), and use bad-news events as entry points only when the moat is intact.

| key | value |
|---|---|
| track_record | not public (unverified) |
| copyable | moat checklist + bad-news entries; behavioural bias list |

Links: strategy:bakshi-bad-news-moats (about); person:charlie-munger (similar_to)

Sources: <https://www.safalniveshak.com/fundoo-professor-sanjay-bakshi/> ; <https://www.safalniveshak.com/one-percent-show-prof-sanjay-bakshi-transcript/> ; <https://uk.marketscreener.com/insider/SANJAY-BAKSHI-A1Y2BN/experience>

### Raamdeo Agrawal - QGLP and the Wealth Creation Study (India)

`person:raamdeo-agrawal` | confidence: **single-source** | tags: india, process, quality, growth, base-rate

Co-founder (1987, with Motilal Oswal) of Motilal Oswal Financial Services; author of the annual Motilal Oswal Wealth Creation Study since 1996 - the longest-running Indian dataset on which stocks created wealth and why. Early notable investments: Hero Honda, Infosys and Eicher Motors; his personal portfolio reportedly grew to ~Rs 100 crore by 2000 (Wikipedia; single-source). Hero Honda ranked first among the most consistent wealth creators in the 12th study (2002-07); Infosys, Hero Honda and Ranbaxy appeared in ten straight studies. Folklore (unverified): a ~Rs 10 lakh Hero Honda investment in the early 1990s grew to many crores. Process: QGLP - Quality (business and management), Growth (earnings growth runway), Longevity (how long growth and returns last), Price (reasonable vs growth) - plus 'Size' (small at the start, per the 100x study). The studies' core finding: big wealth comes from earnings growth plus P/E rerating, and buying at low P/E relative to future growth. Mistakes: Motilal Oswal's flagship MF schemes lagged badly in 2018-2021 when their quality-growth holdings de-rated and they missed cyclicals/PSUs (characterisation; check fund data). Copyable: the study PDFs are free - use their stock-level tables as a base-rate library (what % of wealth creators were small, at what P/E they started).

| key | value |
|---|---|
| signature_trades | Hero Honda, Infosys, Eicher (1990s) |
| track_record | ~Rs100cr portfolio by 2000 (single-source) |
| copyable | QGLP filter, Wealth Creation Study base rates |

Links: strategy:qglp (about); insight:multibagger-patterns (about)

Sources: <https://en.wikipedia.org/wiki/Raamdeo_Agrawal> ; <https://www.motilaloswal.com/wealth-creation-study> ; <https://www.motilaloswal.com/content/dam/mofsl-website-adobe/investor-relations/wealth-creation/wc12.pdf>

### Ashish Kacholia - diversified early-stage smallcap bets (India)

`person:ashish-kacholia` | confidence: **single-source** | tags: india, process, smallcap, multibagger, cloning

Mumbai-based investor, sometimes called a 'big whale' of Indian small caps (nickname not verified in sources found), a past business associate of Rakesh Jhunjhunwala (folklore-grade details). Public portfolio (holdings >1% disclosed quarterly): ~45-49 stocks worth roughly Rs 2,900-3,000 crore in 2025-26 data, with Shaily Engineering Plastics among top holdings; past widely cited winners include Atul Auto, Polycab, KPIT, Majesco and Safari Industries (returns not verified here). Edge (structural): sizable capital, willingness to take 1-3% stakes in tiny companies (including SME-platform and pre-IPO deals) and hold through illiquidity; network access to managements. Process (as described in media): many small bets on early-growth, often niche-manufacturing or tech-services small caps, letting winners run while losers stay small - a venture-style portfolio. Mistakes: several holdings have fallen 50%+ in smallcap drawdowns (2018-19, 2025) and some SME/micro positions lacked governance quality (characterisation, unverified). Copying risk: disclosures appear 2-6 weeks after quarter-end, only above 1%, and news of 'Kacholia buys' often causes 5-20% jumps - so followers buy after the price moves and never see his exits in time. Copyable: the portfolio construction idea (many small, equal-risk bets in early growth stories, add only on proof) rather than the tickers.

| key | value |
|---|---|
| portfolio | ~45-49 stocks, ~Rs2,900-3,000cr (2025-26, aggregator data) |
| copyable | venture-style many-small-bets construction; not ticker cloning |

Links: insight:cloning-indian-superstars (about); insight:hidden-segment (about)

Sources: <https://www.smallcase.com/star-investors/ashish-kacholia-stocks-portfolio/> ; <https://equitymaster.com/timeless-reading/ashish-kacholia-portfolio> ; <https://aliceblueonline.com/dolly-khanna-portfolio-vs-ashish-kacholia-portfolio>

### Dolly Khanna (Rajiv Khanna) - unloved old-economy cyclicals (India)

`person:dolly-khanna` | confidence: **single-source** | tags: india, process, smallcap, cyclical, cloning

Chennai-based; portfolio in Dolly Khanna's name has been run by her husband Rajiv Khanna and active since 1996. Style: bottom-up, small/micro-cap, small stakes, frequent churn, in unglamorous 'old economy' sectors - textiles, sugar, chemicals, manufacturing, petro/refining, aquaculture. Past holdings cited in media include Rain Industries (stake trimmed 2022), Nilkamal, Thirumalai Chemicals and Avanti Feeds (not verified holding-by-holding here); in the March 2026 quarter she added Chennai Petroleum and Sharda Cropchem. Portfolio value estimates conflict: ~Rs 226.6 crore (5paisa, Jan 2026) vs >Rs 485 crore across 12 stocks (Business Today, Apr 2026) - different dates and methods. Edge: process - buying cyclicals when they are unloved (low P/B, trough margins, sector pessimism) and exiting as the cycle matures; small size lets her trade micro caps. No audited track record; 'multibagger' claims in media are anecdotal. Mistakes: holdings in commodity names can give back gains in the down-cycle; the high churn makes static cloning dangerous. Copyable: a cyclical playbook - buy when industry capacity is shutting, margins are at trough and P/B is near historic lows; sell into peak margins and capacity announcements - not her disclosed tickers.

| key | value |
|---|---|
| style | cyclical, unloved, small stakes, churn |
| portfolio_value | Rs226-485cr (conflicting, 2026) |
| copyable | cycle-based entry/exit rules |

Links: insight:cloning-indian-superstars (about); insight:winners-drawdowns (about)

Sources: <https://www.businesstoday.in/markets/stocks/story/dolly-khanna-portfolio-review-these-2-stocks-added-in-q4-should-you-buy-sell-or-hold-524387-2026-04-07> ; <https://5paisa.com/blog/dolly-khanna-portfolio-and-shareholding> ; <https://equitymaster.com/timeless-reading/dolly-khanna-portfolio> ; <https://zeenews.india.com/markets/dolly-khanna-portfolio-stocks-check-share-recommendations-for-long-and-small-term-2375138.html>

### Mukul Agrawal - Param Capital, active multi-stock smallcap book (India)

`person:mukul-agrawal` | confidence: **single-source** | tags: india, process, smallcap, cloning

Mumbai investor behind Param Capital. Public holdings (>1% stakes): ~72-73 stocks as of early 2026; portfolio value estimates range from ~Rs 6,163 crore to ~Rs 7,373 crore depending on date and source. Largest disclosed holdings in Dec 2025 data: Neuland Laboratories (~Rs 496.5 crore) and Radico Khaitan (~Rs 379.4 crore). Q1 FY26 fresh buys included Valor Estate (6.5m shares, ~Rs 120.6 crore), J&K Bank, Wendt India, Tatva Chintan and Yatharth Hospital. Sector spread: pharma/CDMO, infrastructure, chemicals, textiles, alcobev. Edge: structural - large capital spread across many mid/small names, ability to take block and pre-IPO/QIP allocations; process (as reported) - blends earnings-growth/turnaround picks with momentum, actively adds and exits. Track record: no published return series; net-worth figures in media are aggregator estimates (single-source). Mistakes: specific losses are not documented in sources found; like other superstar books, many small positions have suffered 40-60% falls in smallcap drawdowns. Copyable: his top holdings illustrate a useful pattern - turnarounds that became re-rated compounders (Neuland's CDMO shift, Radico's premiumisation) - but the quarterly-lagged, >1%-only disclosure makes ticker-cloning unreliable.

| key | value |
|---|---|
| portfolio | 72-73 stocks, ~Rs6.2-7.4k cr (2025-26) |
| top_holdings | Neuland Labs, Radico Khaitan (Dec 2025) |

Links: case_study:radico-khaitan (about); insight:cloning-indian-superstars (about)

Sources: <https://www.5paisa.com/blog/mukul-agrawal-portfolio-and-shareholding> ; <https://aliceblueonline.com/news/6-stocks-in-which-mukul-agrawal-bought-fresh-stake-in-q1-fy26-do-you-hold-any> ; <https://trendlyne.com/equity/insider-trading-sast/53774/mukul-agrawal-portfolio>

### Kenneth Andrade - supply-side contrarian, 'last man standing' (India)

`person:kenneth-andrade` | confidence: **single-source** | tags: india, process, contrarian, cyclical, midcap

Ran IDFC Premier Equity from Oct 2005 to Sept 2015 (earlier Kotak Mahindra AMC); a FLAME University bio cites ~22.3% CAGR over ten years for the flagship (promotional, unverified end date). The fund became so popular that inflows were restricted (characterisation); after his 2015 exit it struggled. Founded Old Bridge Capital in 2015 (PMS, ~Rs 8,000 crore AUM per a Mint interview); launched the Old Bridge Focused Equity MF in Jan 2024. Process edge: supply-side, capital-cycle analysis - buy into industries where capacity additions have stopped, weak players are exiting and the survivors ('last man standing') gain pricing power; favour high asset-turnover, capital-light businesses; go where earnings are depressed and nobody is looking. Mistakes: his contrarian, commodity/cyclical-leaning PMS lagged in 2016-2020 when quality-growth dominated (characterisation; check data); the mid-cap-heavy IDFC fund suffered as it grew large. Copyable: track industry capex and capacity utilisation (cement, paper, sugar, chemicals) - consolidation plus no new capacity is an early signal that tends to precede margin recovery by 1-2 years; avoid sectors where everyone is announcing capacity.

| key | value |
|---|---|
| track_record | IDFC Premier Equity ~22.3% CAGR over 10 yrs (promotional bio, unverified) |
| copyable | capital-cycle/supply-side screen |

Links: strategy:andrade-capital-cycle (about); case_study:capital-goods-2007 (about)

Sources: <https://www.flame.edu.in/academics/flame-investment-lab/speakers-repository/kenneth-andrade> ; <https://www.morningstar.in/posts/42387/idfc-premier-equity-gets-a-bronze.aspx> ; <https://magzter.com/de/stories/newspaper/Mint-Mumbai/INDIA-HAS-ROBUST-FINANCIALS-IS-ON-EVERY-INVESTORS-RADAR> ; <https://groww.in/mutual-funds/old-bridge-focused-fund-direct-idcw>

### Prashant Jain - valuation-disciplined large-cap contrarian (India)

`person:prashant-jain` | confidence: **verified** | tags: india, process, contrarian, value, sector-psu

Managed HDFC Equity (from Zurich India days, ~1994) and HDFC Top 100 until July 2022 (~28 years). HDFC Equity: ~19.3% CAGR since launch and beat its benchmark in 18 of 21 years; ~20% 20-year CAGR vs ~9.7% for the Nifty (Outlook). Process: valuation discipline, low turnover, willingness to look wrong for years; avoided the 2000 tech bubble and the 2007 realty mania at peak multiples, and leaned into unloved large caps (PSU banks, power, oil, capital goods). His line: 'If there is no pain, why should valuations be attractive?' Structural edge: very large AUM in an era when Indian MF competition was thin; later, size became a constraint (Business Standard 2013). Biggest mistake: 2018-2020 underperformance from an outsized bet on PSUs (SBI, NTPC, Coal India, BPCL etc.) whose value did not turn into growth, causing heavy redemptions and Morningstar downgrades; the PSU bets finally paid off in the last ~18 months of his HDFC stint. Founded 3P Investment Managers (May 2023), >Rs 15,000 crore AUM in two funds. Copyable: valuation discipline in large caps and the stamina to hold an underweight in bubbles; but recognise that cheap PSUs can stay cheap for years without a catalyst (capex cycle, NPA clean-up).

| key | value |
|---|---|
| track_record | ~19-20% CAGR ~20 yrs vs Nifty ~9.7% (2+ sources) |
| mistakes | 2018-2020 PSU drag |
| copyable | valuation discipline, patience, avoid bubble multiples |

Links: strategy:jain-valuation-contrarian (about); case_study:india-psu-rally-2023-24 (about)

Sources: <https://www.outlookbusiness.com/specials/indias-best-fund-managers/prashant-jain-vs-mr-market-2604> ; <https://morningstar.in/posts/58782/2-hdfc-funds-downgraded.aspx> ; <https://primeinvestor.in/reports/the-rise-and-fall-of-hdfc-top-100/> ; <https://www.magzter.com/en/stories/newspaper/Mint-New-Delhi/HOW-THIS-VETERAN-FUND-MANAGER-IS-ADAPTING-TO-NEW-MARKET-REALITIES> ; <https://www.business-standard.com/article/markets/when-size-becomes-a-constraint-113070100835_1.html>

### S. Naren - contrarian asset allocation at ICICI Prudential (India)

`person:s-naren` | confidence: **verified** | tags: india, process, contrarian, asset-allocation, smallcap

Sankaran Naren, CIO (equity) of ICICI Prudential AMC, India's best-known institutional contrarian. Process: buy what has underperformed and is out of favour; shift between equity, debt and gold based on valuation (the house Balanced Advantage approach raises equity when valuations are low and cuts it when high - characterisation of the model); stress-test with history (the 1994-2004 'lost decade' in Indian mid/small caps). Documented calls: Feb 2025 (IFA Galaxy) - said median P/E of mid/small caps at ~43x was 'absurd' and unsustainable, more expensive than 2008, and questioned SIPs/fresh money in those categories; by then the Smallcap 250 had already fallen ~24% from its Sept 2024 peak, and it lagged through 2025. Aug 2025 - warned of 1990s-like risk. Feb 2026 - 'mega gains are unlikely now', large caps not meaningfully overvalued, small/mid caps significantly overvalued. Mistake/limitation: his caution on small caps started in 2023, and small caps rallied hard through Sept 2024 before falling - valuation-based calls are directionally useful but early (characterisation). Copyable: a rule-based allocation that lowers equity (especially small caps) as median P/E and IPO froth rise, and adds after 1-2 years of underperformance; pair with lump-sum deployment into large caps when they are unloved.

| key | value |
|---|---|
| documented_calls | Feb 2025 smallcap 'absurd' 43x; Aug 2025 1990s risk; Feb 2026 moderate returns |
| copyable | valuation-based asset allocation, buy underperformers |

Links: strategy:naren-contrarian-allocation (about); insight:india-valuation-forward-returns (about)

Sources: <https://www.businesstoday.in/personal-finance/investment/story/all-the-risk-is-being-borne-by-you-top-fund-manager-s-narens-caution-on-sips-thats-got-everyone-talking-464019-2025-02-10> ; <https://www.businesstoday.in/markets/stocks/story/icici-prudentials-s-naren-warns-1990s-like-risk-as-indian-stock-market-hits-frothy-valuations-489673-2025-08-16> ; <https://www.businesstoday.in/personal-finance/story/mega-gains-are-unlikely-now-icici-prudentials-naren-urges-investors-to-rethink-expectations-517439-2026-02-22> ; <https://finshots.in/archive/what-did-mr-s-naren-actually-say/>

### Samir Arora - avoid-lists and cutting losers (India)

`person:samir-arora` | confidence: **single-source** | tags: india, process, growth, risk-management

CIO of Alliance Capital's Indian MF business 1993-Aug 2003 (funds won 15+ awards); founded Helios Capital (Singapore) in 2005; Helios MF in India launched 2023-24 (its flexi-cap fund has posted strong early returns per Value Research). A Morningstar/PMS-AIF profile claims ~25% a year (219x) since 1996 vs ~12.2% (16x) for the Indian market in INR - combining Alliance and Helios records (single-source, unaudited). His 2003 departure from Alliance followed a SEBI order that was later overturned on appeal (details not re-verified here). Process edge: (1) an 'avoid list' - he excludes whole sectors with poor long-run shareholder returns or governance (PSUs, many commodities, utilities, real estate) to cut error rates; (2) sell losers early rather than average down; (3) diversified 30-40 stock portfolios in growth sectors (private financials, consumer, tech); (4) he argues fewer than 5% of stocks are worth holding long term, so 'buy and hold' alone is not enough. Mistakes: the avoid list made Helios miss the 2021-24 PSU/defence/railway rally (characterisation); he cut equity sharply in early 2020 on COVID (reported; unverified) and had to re-enter. Copyable: write your own avoid list (sectors with chronic capital destruction), set a sell rule for thesis-broken losers, and accept missing some rallies as the price of fewer blow-ups.

| key | value |
|---|---|
| track_record | ~25%/yr since 1996 combined (single-source) |
| copyable | avoid list, sell losers, diversified growth |

Links: strategy:arora-avoid-list (about); insight:disqualifiers (similar_to)

Sources: <https://www.pmsaifworld.com/team_mf/samir-arora/> ; <https://www.businesstoday.in/personal-finance/story/helios-capitals-samir-arora-breaks-the-myth-long-term-holding-not-enough-to-succeed-in-equities-482325-2025-06-29> ; <https://www.morningstar.in/posts/75352/samir-arora-passionate-about-investing,-but-dispassionate-as-an-investor.aspx> ; <https://5paisa.com/news/meet-the-ace-fund-manager-and-investor-samir-arora>

### Vijay Kedia - SMILE small-cap growth investing (India)

`person:vijay-kedia` | confidence: **unverified** | tags: india, process, smallcap, multibagger

Mumbai investor from a Kolkata broking family (Kedia Securities); began as a trader and has spoken publicly about early-career losses in the 1990s before shifting to long-term holding. Framework: SMILE - Small in size, Medium in experience, Large in aspiration, Extra-large market potential. Widely cited past winners (media lists; entry prices and multiples not verified here): Atul Auto (three-wheelers, held for over a decade), Aegis Logistics, Cera Sanitaryware, Vaibhav Global, Elecon Engineering, Tejas Networks, Sudarshan Chemical, Precision Camshafts. Folklore: claims that a small early stake in Atul Auto or Aegis turned 1 lakh into crores circulate widely but have no documented entry dates/prices - treat as unverified. Edge: process - concentrated holdings in small companies with ambitious, hungry promoters and a large addressable market, held for years; he meets managements and stresses promoter integrity and 'hunger'. Mistakes: like all small-cap concentrators, several holdings have halved in drawdowns; some later bets (turnaround infra/engineering names) took years to work. Copyable: the SMILE checklist is a reasonable small-cap screen when paired with balance-sheet and governance filters; size each idea so one failure does not matter.

| key | value |
|---|---|
| copyable | SMILE checklist + governance filter |
| track_record | no published series (unverified) |

Links: strategy:kedia-smile (about); insight:cloning-indian-superstars (about)

Sources: <https://equitymaster.com/timeless-reading/vijay-kedia-portfolio> ; <https://www.angelone.in/news/share-market/unveiling-vijay-kedia-multibagger-picks-stocks-under-rs-500-revealed> ; <https://www.equentis.com/blog/explore-vijay-kedia-portfolio-top-holdings-investment-strategy-and-more/>

## Library 1 - Strategies

### Druckenmiller: liquidity-first, concentrated macro

`strategy:druckenmiller-liquidity` | confidence: **single-source** | tags: global, process, macro, position-sizing

Rules as described by Druckenmiller in interviews: (1) Earnings don't move the overall market; central banks and liquidity do - focus on the Fed (for India: RBI stance, system liquidity, FPI flows, the rupee and US real yields). (2) Look 18-24 months ahead; price action today reflects what investors expect then. (3) When several signals line up (liquidity, valuation, technicals/price confirmation), bet big - concentration, not diversification, is where returns come from. (4) Use price as information: if the market doesn't confirm the thesis, cut fast; preservation of capital comes first. (5) Change your mind without ego when the regime changes. Individual adaptation: a quarterly liquidity checklist (RBI repo direction, banking-system liquidity surplus/deficit, credit growth, FPI and DII flows, USD/INR trend) to tilt equity exposure; fewer, larger positions with explicit exit conditions. Failure mode: overconfidence and chasing at the top (his own 2000 tech buy). Evidence: his record is press-reported, not audited; treat this as a process template, not a proven formula for individuals.

Links: person:stanley-druckenmiller (about); strategy:position-sizing (similar_to)

Sources: <https://moneyweek.com/441992/the-worlds-greatest-investors-stanley-druckenmiller> ; <https://moiglobal.com/latticework-stanley-druckenmiller-202503>

### Soros: reflexivity and boom-bust sequences

`strategy:soros-reflexivity` | confidence: **single-source** | tags: global, process, macro, cyclical

Reflexivity: participants' beliefs change the fundamentals they are trying to price. Typical boom-bust sequence (Soros, Alchemy of Finance): (1) an unrecognised trend begins; (2) a prevailing bias forms and reinforces it - rising prices ease financing (equity issuance, collateral-backed credit), which lifts reported growth; (3) tests survive, conviction grows; (4) a divergence opens between belief and reality; (5) a twilight period where the trend continues on momentum but doubts grow; (6) a crossover and accelerating reversal. Indian examples: 2003-08 infra/realty (rising land values -> bigger loans -> more projects -> higher valuations -> QIPs), 2023-24 PSU rerating (rising prices -> retail and MF inflows -> more buying), 2024 SME IPOs (oversubscription -> listing gains -> more applicants). Rules for individuals: identify the feedback loop and its fuel (credit, IPO funding, retail flows); ride early only with small size; watch the fuel - when financing tightens (RBI/SEBI action, funding costs, lock-up expiries, promoter selling) the loop breaks. Risk: timing is hard; many 'bubbles' run far longer than expected.

Links: person:george-soros (about); case_study:india-bull-2003-08 (illustrates)

Sources: <https://www.wikipedia.com/wiki/Soros_Fund> ; <https://www.wikiwand.com/en/articles/Quantum_Fund>

### Thorp: quantified edge and fractional Kelly sizing

`strategy:thorp-kelly` | confidence: **verified** | tags: global, process, quant, position-sizing, avoid-ruin

Kelly criterion: for a bet with win probability p and payoff odds b, the growth-maximising fraction of capital is f = (bp - q)/b, where q = 1 - p. Thorp's practice: (1) bet only where expectation is demonstrably positive (counted cards, mispriced warrants/convertibles); (2) size at a fraction of Kelly (half or less) because inputs are uncertain and full Kelly produces brutal drawdowns - roughly a 50% chance of halving the bankroll at some point; (3) hedge out risks you are not paid for (market-neutral). Translation for a stock investor: edge estimates are noisy, so practical position caps (e.g., 5-10% at cost for high conviction, 1-3% for speculative) approximate fractional Kelly; never use leverage or F&O sizes that can wipe you out (see SEBI's F&O loss studies). Feasibility test (Thorp's Madoff insight): if a track record is too smooth for the claimed strategy, verify it or walk away. Evidence quality: Kelly is mathematically proven for repeated bets with known odds; real markets violate those assumptions, which is why fractional Kelly is the rule.

Links: person:ed-thorp (about); strategy:position-sizing (similar_to); insight:sebi-fo-losses (about)

Sources: <https://Www.Wikipedia.org/wiki/Edward_Thorp> ; <https://en.wikipedia.org/wiki/Princeton_Newport_Partners>

### Templeton: maximum pessimism, global bargain search

`strategy:templeton-max-pessimism` | confidence: **single-source** | tags: global, process, contrarian, value

Process: (1) Search everywhere - all countries and industries - for the lowest price relative to long-term earnings power (he used P/E vs history, and P/E vs growth). (2) Buy at 'maximum pessimism': when news is worst and selling is indiscriminate. (3) Diversify across many bargains, because some cheap stocks are cheap for good reason. (4) Sell when a holding's price approaches fair value or a much better bargain appears (he typically held ~4-5 years). (5) Use his cycle ladder - pessimism, skepticism, optimism, euphoria - to judge where a market is. Indian application: years of extreme pessimism (2001-03 post-KP crash, Oct 2008-Mar 2009, Aug 2013 rupee crisis, Mar 2020) all offered P/Es near 11-17x and market cap/GDP near or below 60-75%, followed by 15-30%+ annual returns; a staged buying plan keyed to those valuation levels is the individual's version. Risks: value traps; acting at 'maximum pessimism' requires cash and nerves on hand before the crash.

Links: person:john-templeton (about); insight:india-valuation-forward-returns (about)

Sources: <https://www.caproasia.com/?p=13086> ; <https://www.oreilly.com/library/view/templetons-way-with/9781118149614/xhtml/Chapter03.html>

### Klarman: margin of safety, forced sellers, and cash as an option

`strategy:klarman-margin-of-safety` | confidence: **verified** | tags: global, process, value, avoid-ruin

Principles from Margin of Safety (1991) and Baupost letters: (1) Value conservatively (liquidation, private-market or cash-flow value) and buy only at a large discount - the discount is the protection against your own errors. (2) Think about downside first; absolute, not relative, returns. (3) Look where selling is non-economic: forced or constrained sellers (index deletions, spin-offs, bankruptcy, fund redemptions, regulatory rules) and complex/illiquid securities. (4) Catalysts (asset sales, buybacks, restructuring) shorten the wait. (5) Hold cash when nothing qualifies - cash is a call option on future bargains. Indian forced-seller situations: MF scheme recategorisation (2017-18), index exits, promoter pledge invocations, ASM/GSM-listed stocks after rule-driven selling, demerged entities on listing, rights-issue discounts. Evidence: Baupost's strong first 25 years and weak post-2014 decade show the method depends on the opportunity set - it shines after crashes and lags in long, liquidity-driven bulls.

Links: person:seth-klarman (about); insight:avoid-ruin (similar_to)

Sources: <https://ivey.uwo.ca/bengrahaminvesting/resources/interviews-notes/seth-a-klarman> ; <https://www.bloomberg.com/news/articles/2025-01-22/baupost-clients-pulled-7-billion-since-2021-after-poor-returns>

### Greenblatt: special situations plus Magic Formula screen

`strategy:greenblatt-special-situations` | confidence: **single-source** | tags: global, india, process, special-situations, value

Two separate methods. (A) Special situations (You Can Be a Stock Market Genius): spin-offs (parent holders sell the unwanted child regardless of price; insiders often get equity incentives in the new entity), restructurings, merger securities, rights offerings, recapitalisations and LEAPS. Edge comes from non-economic selling and small size. Indian analogues: demergers (e.g., recent conglomerate splits), open offers and buyback arbitrage, rights issues priced at deep discounts. (B) Magic Formula (2005): rank stocks by return on capital = EBIT / (net working capital + net fixed assets) and earnings yield = EBIT / enterprise value, sum ranks, buy top 20-30, hold one year, repeat; exclude financials/utilities. Backtest 1988-2004: ~30.8%/yr vs ~12.4% for the S&P 500; live results were much weaker, and multi-year underperformance led most users to abandon it - Greenblatt's own point is that it works because it is hard to stick with. Use as an idea generator plus a quality/governance check in India, where cheap high-ROC stocks often include cyclicals at peak margins and promoter-governance risks.

Links: person:joel-greenblatt (about); insight:weak-factor-folklore (about)

Sources: <https://www.oreilly.com/library/view/profiting-from-hedge/9781118465172/xhtml/Chapter08.html>

### Ackman: simple, predictable FCF businesses plus asymmetric hedges

`strategy:ackman-quality-activism` | confidence: **verified** | tags: global, process, quality, concentration

Pershing Square's published criteria: simple, predictable, free-cash-flow-generative businesses; formidable barriers to entry; limited exposure to extrinsic factors; strong balance sheet; minimal capital-markets dependence; high-quality management/governance; attractive valuation vs intrinsic value. Typically 8-12 positions. Add-on: cheap, convex hedges (credit default swaps in Feb 2020, rate-related options in 2022) where the payoff can be 50-100x premium. Lessons from failures: Valeant violated 'simple and predictable' (growth was acquisitions plus drug price hikes; reported 'adjusted' EPS masked it) - ~$4bn loss; Herbalife short and JC Penney turnaround failed on timing and execution. For an individual: concentrated quality buys on temporary bad news, plus a small, explicit tail-hedge budget (e.g., deep-OTM index puts) only if you understand options; avoid serial acquirers whose organic growth is unclear.

Links: person:bill-ackman (about); strategy:buffett-munger (similar_to)

Sources: <https://www.cnbc.com/2017/03/20/hedge-fund-titans-surefire-bet-turns-into-a-4-billion-loss.html> ; <https://moneyweek.com/economy/people/601185/bill-ackman-the-billionaire-who-bet-big-on-viral-doom>

### Akre: three-legged stool compounding machines

`strategy:akre-three-legged-stool` | confidence: **verified** | tags: global, india, process, quality, compounding

Three legs, all required: (1) Business - extraordinary economics, measured by high, durable returns on owners' capital (ROE/ROIC) without heavy leverage; (2) People - skilled, honest management that treats shareholders as partners and has a record of good capital allocation; (3) Reinvestment - the ability to reinvest free cash flow at similar high returns for many years (runway). When a 'compounding machine' is found, the default is to hold; turnover is very low and selling happens when a leg breaks (reinvestment runway ends, management changes behaviour), not on valuation alone. Indian checklist translation: ROCE >20% for 7-10 years, low debt, promoters with clean related-party and pledge history, capex funded internally with incremental ROCE staying high, and a TAM that supports a decade of growth. Risk: paying any price for quality (de-rating), and confusing a cyclical peak ROE for a durable one.

Links: person:chuck-akre (about); strategy:marcellus-cc (similar_to); strategy:qglp (similar_to)

Sources: <https://www.akrefund.com/?p=3457> ; <https://quartr.com/insights/investment-strategy/chuck-akre-above-average-returns-and-a-legendary-framework>

### Sleep/Zakaria: scale economies shared and destination analysis

`strategy:sleep-scale-economies-shared` | confidence: **verified** | tags: global, india, process, quality, compounding

Model: a firm that passes its scale savings back to customers (lower prices, better service) grows volume faster, which deepens scale advantages, which allows more sharing - a flywheel competitors without scale cannot match. Costco (low fixed markups, membership fees) and Amazon (prices, free shipping, reinvestment) were Nomad's archetypes. Tools: (1) destination analysis - estimate what the business looks like in 10-20 years and whether today's price reflects it; (2) judge management by whether they sacrifice near-term margin for customer value; (3) concentrate in the best 3-10 ideas and hold through noise; (4) avoid 'scale economies kept' (firms raising prices on captive customers), which invites competition and regulation. Indian candidates for the test: discount retail, low-cost brokers/AMCs, platform businesses, airlines with cost leadership - but verify the customer-value claim with data (prices vs competitors, volume share).

Links: person:nick-sleep (about)

Sources: <https://quartr.com/insights/investment-strategy/investing-mastery-with-nick-sleep-nomad-s-costco-investment> ; <https://massivemoats.substack.com/p/a-deep-dive-analysis-into-the-nomad>

### Terry Smith: buy good companies, don't overpay, do nothing

`strategy:smith-quality-do-nothing` | confidence: **verified** | tags: global, process, quality, low-turnover

Rule 1 - good companies: high ROCE in cash terms, high gross margins (pricing power), high cash conversion, low leverage, growth that can be reinvested, resilience to obsolescence; avoid banks, heavy cyclicals, airlines, conglomerates. Rule 2 - don't overpay: compare free-cash-flow yield with bond yields and the company's growth. Rule 3 - do nothing: minimise turnover and trading costs; let compounding work. Measured over 2010-2025 the approach beat MSCI World (13.8% vs 12.1% a year) but lagged five calendar years in a row (2021-25), when mega-cap tech concentration, passive flows and de-rating of 'quality defensives' hurt. Indian application: the checklist is close to the Marcellus/consistent-compounder template; the binding constraint in India is rule 2 - quality FMCG/consumer names at 60-80x earnings can deliver low single-digit returns for years even as earnings grow.

Links: person:terry-smith (about); strategy:marcellus-cc (similar_to)

Sources: <https://www.fundsmith.co.uk/media/4hcfd1pg/2025-fef-annual-letter-web.pdf> ; <https://moneyweek.com/investments/fundsmith-underperforms-again>

### Marks: market temperature and stepwise risk posture

`strategy:marks-cycle-temperature` | confidence: **single-source** | tags: global, india, process, base-rate, avoid-ruin

You can't predict, but you can prepare: estimate where the market is in its cycle and adjust aggression gradually. Marks's 'temperature' inputs: investor psychology (greed vs fear), credit availability and lending standards, issuance quality (IPOs of loss-making or tiny firms), valuation vs history, and the prevailing narrative ('this time is different'). Indian temperature checklist: smallcap/midcap P/E premium to Nifty; mainboard and SME IPO counts and subscription multiples; retail F&O volumes and new demat additions; market cap/GDP (above ~120% = hot, below ~70% = cold, per 2008/2020/2024 history); NBFC/corporate bond spreads; FPI positioning and the rupee. Posture rule: in hot readings, raise quality, trim small caps, keep dry powder; in cold readings, deploy in steps. Second-level thinking: ask what consensus expects and what is priced, not just whether a company is good. Limitation: temperature readings are early by months or years.

Links: person:howard-marks (about); insight:india-cycle-top-bottom-signals (about)

Sources: <https://www.privatedebtinvestor.com/oaktree-raises-10-9bn-distressed-fund/>

### Munger: inversion, mental-model latticework, and sitting still

`strategy:munger-inversion` | confidence: **single-source** | tags: global, process, behavior, quality

Core practices: (1) Inversion - before buying, list how the investment could fail (pre-mortem) and avoid those paths; 'all I want to know is where I'm going to die, so I'll never go there.' (2) Latticework - check a thesis with models from several disciplines: incentives, scale economics, network effects, compounding, opportunity cost, regression to the mean. (3) A bias checklist from 'The Psychology of Human Misjudgment' (1995): incentive-caused bias, social proof, commitment/consistency, deprival super-reaction, envy, denial, authority, and 'lollapalooza' when several combine (e.g., Indian IPO/SME manias). (4) Few great bets, held long; 'the big money is not in the buying and selling but in the waiting.' (5) Quality over cheapness: wonderful business at a fair price. Evidence: Munger's own partnership showed -30%+ years in 1973-74, so concentration requires capacity to endure drawdowns. Individual use: a written one-page pre-mortem and bias check per stock.

Links: person:charlie-munger (about); strategy:buffett-munger (part_of); insight:behavior-gap (about)

Sources: <https://www.cnbc.com/2023/02/15/charlie-munger-says-byd-is-far-ahead-of-tesla-in-china.html>

### Bakshi: moats bought on temporary bad news

`strategy:bakshi-bad-news-moats` | confidence: **single-source** | tags: india, process, quality, behavior

As taught in Bakshi's public lectures and blog: (1) Identify businesses with durable moats - pricing power, switching costs, network effects, cost advantages, brands, regulatory licences - evidenced by stable high ROCE. (2) Wait for 'bad news' that is temporary or non-structural: a regulatory scare, a one-off loss, an industry panic, a management change misread by the market. (3) Separate temporary from permanent: does the bad news damage the moat, or only this year's earnings? (4) Use behavioural finance to exploit overreaction (loss aversion, recency bias) and to check one's own biases. (5) Prefer 'clean surprises': hidden strengths that later show up in reported numbers. Indian examples of the pattern (not his holdings): high-quality lenders after one-off asset-quality scares, consumer franchises during temporary input-cost spikes. Risk: misjudging a permanent moat break (technology disruption, regulation) as temporary.

Links: person:sanjay-bakshi (about); strategy:buffett-munger (similar_to)

Sources: <https://www.safalniveshak.com/fundoo-professor-sanjay-bakshi/> ; <https://www.safalniveshak.com/one-percent-show-prof-sanjay-bakshi-transcript/>

### Andrade: supply-side capital cycle, last man standing

`strategy:andrade-capital-cycle` | confidence: **single-source** | tags: india, process, contrarian, cyclical

Look at supply, not demand. (1) Find industries where capacity growth has stalled - years of poor returns, no new projects, weak players exiting or being acquired. (2) Own the survivors with the best cost position and balance sheet ('last man standing'); as demand catches up with frozen supply, utilisation and pricing rise and margins expand sharply. (3) Prefer high asset-turnover, capital-light models where incremental growth needs little capex. (4) Exit when the industry starts announcing big capacity additions or new entrants rush in. Indicators for Indian investors: capacity utilisation data (cement, steel, paper), industry capex announcements, consolidation deals, number of listed players and their losses, P/B near cycle lows. Related evidence: the Indian capital goods index took ~2007-2021 to regain its peak after a capacity boom - the inverse of this strategy. Risk: demand may never return (structural decline).

Links: person:kenneth-andrade (about); case_study:capital-goods-2007 (about)

Sources: <https://www.flame.edu.in/academics/flame-investment-lab/resources/kenneth-andrade>

### Prashant Jain: large-cap valuation discipline through bubbles

`strategy:jain-valuation-contrarian` | confidence: **verified** | tags: india, process, contrarian, value

Approach (from interviews and fund behaviour): (1) Stay anchored to normalised earnings and valuations; refuse to pay bubble multiples (tech 1999-2000, realty 2007, quality-consumer at extreme P/Es). (2) Accept underperformance during bubbles - 'when you avoid certain bubbles, the returns take a hit.' (3) Overweight unloved large caps when they trade well below history, typically financials, energy, power and capital goods, and hold for multi-year mean reversion. (4) Low turnover, long horizon. Results: ~20% CAGR over ~20 years vs ~10% for the Nifty, with painful stretches (2013, 2015, 2018-20). Lesson from the PSU-heavy phase: cheapness without a catalyst (earnings upgrade, capex cycle, bad-loan clean-up) can last years and cause investor redemptions; for an individual, size contrarian large-cap bets so you can wait, and define the catalyst you're waiting for.

Links: person:prashant-jain (about)

Sources: <https://www.outlookbusiness.com/specials/indias-best-fund-managers/prashant-jain-vs-mr-market-2604> ; <https://morningstar.in/posts/74713/prashant-jain-on-paying-the-price-for-conviction.aspx>

### Naren: buy underperformers, allocate by valuation

`strategy:naren-contrarian-allocation` | confidence: **verified** | tags: india, process, contrarian, asset-allocation

Two layers. (1) Sector/stock contrarianism: buy what has underperformed for years and is unloved (ICICI Pru describes buying underperformers in mid/small caps when they are cheap), avoid what everyone owns. (2) Valuation-based asset allocation: reduce equity (especially mid/small caps) when broad valuations and froth indicators are high; add when they are low; use debt and gold as ballast. His 2025-26 public warnings cited mid/small-cap median P/E ~43x (Feb 2025) and the 1994-2004 'lost decade' as the risk analogue. Individual version: a written rule, e.g., target equity 50-80% stepping down as Nifty trailing P/E rises above ~24 and smallcap P/E premium widens, stepping up below ~18; rebalance annually. Evidence: Indian studies show 5-year returns are weak from Nifty P/E above ~24 (see insight:india-valuation-forward-returns); timing signals are early, so steps beat all-or-nothing switches.

Links: person:s-naren (about); insight:india-valuation-forward-returns (about)

Sources: <https://www.businesstoday.in/personal-finance/investment/story/all-the-risk-is-being-borne-by-you-top-fund-manager-s-narens-caution-on-sips-thats-got-everyone-talking-464019-2025-02-10> ; <https://cafemutual.com/news/press-news/39040-sankaran-naren-cio-of-icici-prudential-mf-sees-contra-opportunities-in-mid-and-smallcaps-we-will-only-buy-underperformers>

### Samir Arora: avoid-list plus cut-losers discipline

`strategy:arora-avoid-list` | confidence: **single-source** | tags: india, process, risk-management, growth

Rules (from his interviews): (1) Keep a sector avoid list - industries with chronically poor shareholder returns or governance (he has named PSUs, commodities, utilities, real estate among them at various times); excluding them cuts the error rate. (2) Diversify across ~30-40 growth stocks rather than a few bets. (3) Sell losers when the thesis is wrong instead of averaging down - he argues fewer than 5% of stocks are worth holding for the real long term, so long holding by itself is not an edge. (4) Let winners run. (5) Use macro judgment occasionally (raising cash in crises). Trade-off: avoid lists miss sector-wide rerating rallies (e.g., Indian PSUs 2021-24) - the cost of insurance against blow-ups. For an individual: write the avoid list down, define a review trigger for any stock down 25-30% from cost (re-underwrite, don't auto-average), and cap position size.

Links: person:samir-arora (about); insight:disqualifiers (similar_to)

Sources: <https://www.businesstoday.in/personal-finance/story/helios-capitals-samir-arora-breaks-the-myth-long-term-holding-not-enough-to-succeed-in-equities-482325-2025-06-29> ; <https://www.outlookbusiness.com/interview/hedge-fund-manager-samir-arora-on-why-the-lessons-we-have-learnt-from-warren-buffett-are-selective-and-wrong-6041>

## Insights

### Cloning Indian 'superstar' portfolios: why it usually underdelivers

`insight:cloning-indian-superstars` | confidence: **single-source** | tags: india, process, cloning, base-rate, smallcap

Indian shareholding disclosures only show holders with >=1% of a company, filed quarterly (typically within ~3 weeks of quarter-end), so a follower sees entries 1-4 months late, never sees sub-1% holdings, and usually learns of exits only after the next filing. Media 'X buys Y' stories routinely move small caps 5-20% on the news (observed pattern; magnitude unverified), so the follower's entry price is worse than the investor's. Superstar books are large and diversified (Mukul Agrawal ~72 stocks, Kacholia ~45-49, Dolly Khanna ~12-20 frequently churned), so any single disclosed stock may be a 0.5% experiment for them but a 20% bet for you. Survivorship: lists of 'superstar multibaggers' omit the many holdings that fell 50%+ in 2018-19 and 2025. Pabrai's cloning works better because he clones concentrated, long-held positions of investors with published reasoning, and still applies his own checklist. Useful use: treat disclosed stakes as a pre-screened idea list; check the investor's average cost (bulk-deal or filing prices), the stock's governance and valuation now, and size by your conviction, not theirs.

| key | value |
|---|---|
| lesson | use as idea source, not signal; check lag, size and price paid |

Links: person:ashish-kacholia (about); person:dolly-khanna (about); person:mukul-agrawal (about); person:mohnish-pabrai (about); insight:behavior-gap (about)

Sources: <https://trendlyne.com/portfolio/superstar-shareholders/69664/Q3-2025/mohnish-pabrai-portfolio> ; <https://www.5paisa.com/blog/mukul-agrawal-portfolio-and-shareholding> ; <https://www.smallcase.com/star-investors/ashish-kacholia-stocks-portfolio/>

### Investor edges: structural vs process, and what an individual can copy

`insight:investor-edge-taxonomy` | confidence: **single-source** | tags: global, india, process, base-rate, luck-vs-skill

Across this library, edges fall into two buckets. Structural (not copyable): scale and leverage across asset classes (Soros, Druckenmiller), proprietary data/compute/scientists and capacity caps (Simons' Medallion: 39% net 1988-2018, while Renaissance's public funds did far worse), activism and board influence (Ackman), locked-up distressed capital (Marks, Klarman), pre-IPO/block access and network (Indian superstars). Process (largely copyable): Kelly-style sizing (Thorp), downside-first margin of safety (Klarman), special situations driven by non-economic selling (Greenblatt), three-legged stool / scale-economies-shared quality tests (Akre, Sleep, Smith), capital-cycle supply analysis (Andrade), valuation-based allocation (Naren, Jain), avoid-lists and loser-cutting (Arora), scuttlebutt (Fisher), inversion and bias checklists (Munger), cycle temperature (Marks, Templeton). Small size is the individual's one structural advantage: positions in micro/small caps and special situations too small for funds (Greenblatt and Buffett both credit small size early). Common failures across greats: concentration in a broken thesis (Valeant, Horsehead), buying a mania late (Druckenmiller 2000), style droughts of 5+ years (Fundsmith 2021-25, Baupost post-2014, Jain 2018-20). Implication: copy processes, accept multi-year underperformance as normal, and never copy leverage.

| key | value |
|---|---|
| structural | scale, leverage, data, activism, locked capital, deal access |
| process | sizing, MoS, special sits, quality tests, capital cycle, allocation, avoid lists, scuttlebutt, inversion, temperature |

Links: insight:luck-vs-skill (about); insight:winners-drawdowns (about); decision:edge-before-stocks (about)

Sources: <https://www.wealthmanagement.com/alternative-investments/jim-simons-built-the-best-hedge-fund-ever> ; <https://www.fundsmith.co.uk/media/4hcfd1pg/2025-fef-annual-letter-web.pdf> ; <https://www.cnbc.com/2017/03/20/hedge-fund-titans-surefire-bet-turns-into-a-4-billion-loss.html>
