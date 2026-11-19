# Trade Certainty for Edge: Multibagger Playbook

No method gives "near-certain profit" in stocks. What works is a repeatable process that tilts the odds in your favour, sizes positions so you survive being wrong, and holds the rare big winner long enough for it to compound. The base rates are harsh. **About 58% of US stocks returned less than one-month T-bills over their lifetimes, and about 4% of stocks created all the net wealth in the US market from 1926 to 2016** ([Bessembinder, JFE 2018](https://wpcarey.asu.edu/sites/default/files/2021-10/do-stocks-outperform-treasury-bills.pdf)). In India, **87.7–93% of individual F&O traders lost money in every year SEBI has studied** ([Business Standard](https://www.business-standard.com/markets/capital-market-news/sebi-study-exposes-massive-losses-for-individual-f-o-traders-in-india-124092400948_1.html); [Finnovate summary of SEBI FY26 study](https://www.finnovate.in/learn/blog/sebi-fno-trader-losses-fy26-individual-derivatives)). Across retail investors, legendary investors, professional firms and quants, the winning methods share one structure. Quality and growth filters decide *what* to own. A view that differs from consensus, together with a check on what the price already assumes, decides *why now*. Trend and regime filters decide *when*. Position-sizing rules decide *how much*. AI is now useful for the reading-heavy middle of that pipeline: summarising filings, red-teaming a thesis and screening for forensic problems. The evidence that AI can *pick* stocks on its own is weak to negative. Live LLM trading contests mostly lost money, and the oldest AI-run ETF has trailed the S&P 500. One correction to the starting story is needed. Radico Khaitan did rise roughly 25–90x depending on the entry point, but it went sideways for **eight years after 2008**. The move began in **2016–17**, driven by premiumisation, debt reduction and operating leverage. No 2008 "UBL issue" caused it. This report is educational and is not personalised financial advice.

---

## The honest starting point: your edge is probabilistic, and the base rates are against you

"Near-certain profit" assumes the market is a puzzle with a correct answer. The data describes something else: a lottery-like distribution of outcomes in which skill moves the odds but cannot remove the variance. Bessembinder's US study found that of nearly 26,000 stocks, **just 1,092 companies (4.3%) accounted for all $35 trillion of net wealth creation**. The other 96% collectively matched T-bills ([ASU W.P. Carey](https://wpcarey.asu.edu/department-finance/faculty-research/do-stocks-outperform-treasury-bills)). The global follow-up covered 64,000+ stocks from 1990 to 2020 and found that **about 2.4% of firms created all net shareholder wealth**. In the same study, 57.4% of non-US stocks underperformed T-bills ([Morningstar AU](https://www.morningstar.com.au/stocks/only-2-4-of-companies-deliver-all-net-shareholder-wealth); [ASU](https://wpcarey.asu.edu/department-finance/faculty-research/do-stocks-outperform-treasury-bills)). Motilal Oswal's 2014 100x study found about **47 stocks that did 100x out of a universe of roughly 3,500**, taking about 12 years on average ([Outlook Business](https://www.outlookbusiness.com/interview/how-to-spot-a-100-bagger-744)). Raamdeo Agrawal, whose firm ran that study, says plainly that "100X is a rare phenomenon" ([Outlook Business](https://www.outlookbusiness.com/markets/interview/value-investors-do-not-talk-or-focus-too-much-on-growth-2482)).

Active trading is worse. SEBI found that **93% of about 1.13 crore individual F&O traders lost money over FY22–24, with aggregate losses above ₹1.8 lakh crore** ([News On Air](https://www.newsonair.gov.in/sebi-study-reveals-individual-traders-face-severe-losses-in-equity-fo-segment)). In FY25, 91% lost money and net losses rose 41% to ₹1,05,603 crore ([Business Standard](https://www.business-standard.com/markets/news/net-losses-of-traders-in-fo-widens-in-fy25-sebi-study-125070701221_1.html)). The FY26 study reported 87.7% losers, and **82.1% were losing even before transaction costs** ([Finnovate](https://www.finnovate.in/learn/blog/sebi-fno-trader-losses-fy26-individual-derivatives); [Open Magazine](https://openthemagazine.com/business/sebi-fo-loss-study-explained-why-9-in-10-retail-traders-lost-91685-crore-in-fy26)). That last figure means the problem is not only costs: most of these traders have no edge at all. Studies of other markets agree. **97% of Brazilians who persisted at day trading for 300+ days lost money** ([IDEAS/RePEc](https://ideas.repec.org/p/fgv/eesptd/525.html)). In Taiwan, **fewer than 1% of day traders earned predictable abnormal returns net of fees** ([Barber, Lee, Liu & Odean](https://ideas.repec.org/a/eee/finmar/v18y2014icp1-24.html)). Professionals do not escape the arithmetic either. SPIVA India Year-End 2025 reports that a majority of active funds in every category underperformed over the decade ([S&P SPIVA](https://www.spglobal.com/spdji/en/spiva/article/spiva-india-year-end-2025/)).

The right goal is therefore **positive expected value, applied repeatedly, with survival guaranteed**. Expected value is the probability of a win times the size of the win, minus the probability of a loss times the size of the loss. Howard Marks's "second-level thinking" asks you to set out the range of likely outcomes, the probability that you are right, what consensus believes and what the price implies ([Oaktree, "It's Not Easy"](https://www.advisorperspectives.com/commentaries/2015/09/24/it-s-not-easy)). Druckenmiller, crediting Soros, says what matters is "how much you make when you're right and how much you lose when you're wrong," not your hit rate ([MoneyWeek](https://moneyweek.com/investments/investment-strategy/605020/stan-druckenmiller-position-size-really-matters)). Pabrai's version is "Heads I win; tails I don't lose much" ([Outlook Money](https://www.outlookmoney.com/invest/mohnish-pabrais-lessons-in-the-dhandho-of-investing)). If 2–4% of stocks create all the wealth, a multibagger portfolio has to be judged on whether **a few large winners pay for many small losers**, not on how often you are right. The playbook below is built around that idea.

| "Certainty" framing (wrong) | Probabilistic reframing (right) |
|---|---|
| "This stock will 10x" | "I estimate a 20% chance of 10x, 50% of roughly flat, 30% of −50%. EV is positive and the downside is survivable." |
| "I'm confident, so I'll go big" | "Size from the downside and from estimation error. Cap any one position." |
| "It fell 30%, so the thesis is wrong" or "...so I'll buy more" | "Did a pre-written kill criterion trigger? If not, price alone is not information about the thesis." |
| "My win rate is 70%" | "My average win divided by my average loss, times my hit rate, is my expectancy, measured over 30+ decisions." |
| "The AI said buy" | "The AI produced a hypothesis. I verified the numbers against the source and red-teamed it." |

---

## Case studies show multibaggers come from public data most investors dismissed

### Radico Khaitan: correcting the "2008 UBL issue" story

The user's story has the price range roughly right and the cause and timing wrong. **UBL is United Breweries Ltd, the Kingfisher beer maker. It does not compete with Radico in spirits.** The story probably confuses UBL with the UB Group / United Spirits (USL) / Vijay Mallya saga. That ran mainly from 2012 to 2016. Diageo agreed in November 2012 to buy 53.4% of USL, but its open offer failed and it ended up with about 25% by July 2013 ([Business Standard](https://www.business-standard.com/amp/article/companies/diageo-seals-deal-with-mallya-to-pick-up-53-4-112110900175_1.html); [Business Standard Jul 2013](https://www.business-standard.com/article/companies/diageo-gains-control-over-united-spirits-ups-stake-to-25-113070400973_1.html)). The real "UB connection" is older. In the 1990s, Lalit Khaitan approached United Spirits for a partnership after Radico's Shaw Wallace bottling contract expired and was refused, which pushed Radico to build its own brands. **8PM whisky launched in August 1998** ([StockEdge](https://blog.stockedge.com/stock-insights-radico-khaitan-ltd/)). The research found **no source showing investors bought Radico in 2008 on a UB thesis**. That version is most likely investor folklore.

The price record shows something more useful than the legend. Adjusted prices fell **from a 2008 high of ₹191 to a low of ₹49.6 (−74%)**. They then spent **2010–2016 trading between about ₹76 and ₹186**. Closing prices were then ₹294 (2017), ₹400 (2018), ₹1,236 (2021), ₹2,606 (2024) and ₹3,298 (2025) ([stockpricearchive](https://stockpricearchive.com/share-price-history-and-returns/radico/)). Recent quotes are around ₹4,135–4,196, against a 52-week high near ₹4,748 ([screener.in](https://www.screener.in/company/RADICO/)). Aggregator data is inconsistent, so check the exact multiples on NSE/BSE. "120 → 4,600" is achievable on an entry anywhere in 2010–2016. A 2008 buyer, though, first lost three-quarters of their money and then waited eight years.

The trigger was a **2016–17 business inflection**. In early 2017 Radico had ₹742 crore of net debt and had "not performed well in the last two years due to increasing raw material costs" ([Angel Broking 3QFY17](https://www.angelone.in/get-html-report/AngelBrokingResearch_Radico%20Khaitan_3QFY2017RU_130217.html)). Over the next four years **debt/equity fell from 0.77 to 0.15**, and revenue grew 44% while **PAT grew 239%**, from ₹80 crore to ₹271 crore ([StockEdge](https://blog.stockedge.com/stock-insights-radico-khaitan-ltd/)). That is operating leverage driven by a premium mix. By FY26, consolidated PAT had risen 74.6% to ₹602.5 crore, and Prestige & Above brands made up more than half of operating revenue ([AlphaStreet](https://alphastreet.com/india/radico-khaitan-premiumization-drives-strong-growth-outlook)). A rough decomposition (the share count is unverified, so confirm on screener.in) runs as follows. From an FY17 trough near ₹110 to about ₹4,200 is roughly 38x. **PAT grew about 7.5x** while **trailing P/E rerated about 5x**, from the high teens to 90x+. That is Chris Mayer's "twin engine": earnings growth multiplied by a rising multiple ([Validea on Mayer](https://blog.validea.com/?p=33794)). The early signals visible in 2016–17 were premium-brand volume growth while regular brands stagnated, management guiding to debt reduction without big new capex, and a reversal of the raw-material cost cycle. Two further elements are plausible but **unverified as documented contemporaneous theses**: USL's distraction during the Diageo transition leaving room for challengers, and the luxury launches (Rampur single malt, Jaisalmer gin), whose launch years are also unverified.

### NVIDIA: the signal was in segment data for years, and the later move came from earnings

NVIDIA's **data-center revenue was $339M in FY16, $1.93B in FY18 and $10.6B in FY22**, all years before ChatGPT ([StockAnalysis](https://stockanalysis.com/stocks/nvda/metrics/data-center-revenue/); [NVIDIA investor presentation, Oct 2022](https://s201.q4cdn.com/141608511/files/doc_presentations/2022/NVIDIA-Investor-Presentation-Oct-2022-(1).pdf)). The signal was a small segment compounding inside a company the market mostly saw as a gaming and crypto business. Holders had to sit through **two drawdowns of more than 50%, in 2018 and 2022** ([Yahoo Finance/Motley Fool](https://finance.yahoo.com/news/nvidia-down-27-peak-history-100700214.html)). Both came from the cyclical gaming and crypto segment, not from the data-center thesis. After 2023 the stock's gains came "primarily [from] earnings growth rather than renewed multiple expansion" ([Mavengity](https://mavengity.com/articles/finance/nvidia-valuation-duration-not-existence/)). **Forward P/E fell from about 40 in mid-2025 to about 15–17x by October–November 2026** ([shattered.io](https://shattered.io/nvidia-17x-forward-earnings-cheap-multiple-half-story-2026/); [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/nvidia-nvda-more-doubled-revenue-132539113.html)). The bear case also deserves its due. If expected EPS growth of 70% turns out to be 40%, "17x was never 17x" ([shattered.io](https://shattered.io/nvidia-17x-forward-earnings-cheap-multiple-half-story-2026/)). Several commonly told details are **unverified in this research**: the CUDA launch in 2006–07, AlexNet being trained on GTX 580s in 2012, the May 2023 guidance shock, and ARK selling early.

### The wider pattern library, including failures

| Case | Pattern | What the engine was | Lesson |
|---|---|---|---|
| Radico Khaitan (2016→2026) | Mix shift + deleveraging in an out-of-favour company | Earnings ~7.5x × P/E ~5x (approx.) | Twin engine; thesis ≠ timing (8 dead years first) |
| NVIDIA (2016→2026) | Hidden fast segment inside a cyclical company | Mostly earnings after 2023 | Earnings alone can carry a multibagger; expect 50%+ drawdowns |
| Eicher / Royal Enfield | New-CEO product reset of a stagnant brand | Fastest Wealth Creator 2009–14 ([MOSL](https://www.motilaloswal.com/content/dam/mofsl-website-adobe/investor-relations/wealth-creation/wc19.pdf)); ~86x from 2005 ([PrimeInvestor](https://primeinvestor.in/?p=56537)) | Read management change plus channel evidence |
| Defence PSUs (2020–24) | Policy shift (indigenisation) | Rally "largely driven by valuation rerating rather than faster growth" ([Business Standard 2023](https://www.business-standard.com/markets/news/rally-in-listed-defence-stocks-yet-to-be-backed-by-earnings-growth-123071300913_1.html)); HAL 28x forward vs 14x 5-yr avg in 2025 ([Business Today](https://businesstoday.in/markets/stocks/story/mazagon-dock-hal-bdl-bel-share-price-targets-for-9-defence-stocks-ahead-of-q4-results-471974-2025-04-15)) | Multiple-led moves need earnings to catch up |
| Deepak Nitrite (2020–21) | Import-substitution capex + China+1 | +135% in 6 months to Mar 2021 ([Business Standard](https://www.business-standard.com/article/markets/deepak-nitrite-analysts-see-further-upside-despite-135-rally-in-6-months-121030500331_1.html)); FY26 profit down ([Upstox](https://upstox.com/stocks/deepak-nitrite-ltd-share-price/INE288B01029)) | A correct thesis meets cyclical spread compression; the exit matters |
| Suzlon (2008) | Green-energy policy tailwind | **−99.6%**, from ₹430.92 (2008) to ₹1.51 (2020) ([Business Today](https://www.businesstoday.in/markets/stocks/story/suzlon-energy-shares-down-96-in-5-years-this-stock-rebounded-42x-heres-why-456906-2024-12-11)) | Same story as the winners, killed by leverage |
| Amazon (1999–2009) | Platform compounder | −94%, then 10 years to regain the 1999 high ([Motley Fool](https://www.fool.com/investing/2016/06/26/amazon-stocks-history-the-importance-of-patience.aspx)) | Survivorship: most dot-com names never came back |

The base rates for wealth creators reinforce one point: start small. **Eight of the ten fastest Indian wealth creators of 2016–21 had a market cap below ₹2,000 crore in 2016** ([Business Standard/MOSL](https://www.business-standard.com/amp/article/markets/reliance-industries-largest-wealth-creator-in-2016-21-says-motilal-oswal-121121401678_1.html)). Motilal's 30th study (2020–25) found the **top 10 fastest creators compounded at about 88% a year against 24% for the Nifty TRI** ([Motilal Oswal](https://www.motilaloswalgroup.com/Media-Room/Press-Release/-/india’s-biggest-wealth-boom-rs148-trillion-ad/FS/20796)). Survivorship bias is the other half of that lesson. The same signals (policy tailwind, sector boom, turnaround) also produced Suzlon. What separated Eicher and Radico from the blow-ups was mostly **leverage, governance and promoter capital-allocation discipline**. This matches Mayer's rule to avoid debt so that drawdowns do not become permanent ([Hedge Fund Alpha](https://hedgefundalpha.com/strategies/christopher-mayers-notes-100-baggers/)).

---

## "Reading between the lines" is a repeatable second-order process

None of the early signals in these cases was secret. Each was **public data that sat inside a boring or declining story**: segment revenue (NVIDIA), mix shift (Radico), a new CEO's product reset (Royal Enfield), a policy document (defence, PLI) or an import-substitution capex (Deepak). The skill lies in following the chain of consequences to the point the market has not yet priced. Steinhardt formalised this as **"variant perception"**: a well-founded view meaningfully different from consensus. Every idea had to state the consensus view, the variant view and a trigger event, and he held positions until the disagreement closed ([MicroCapClub](https://microcapclub.com/michael-steinhardt-in-his-own-words/)). Marks's example captures the second-order step. First-level thinking says "earnings will fall; sell." Second-level thinking says "earnings will fall less than people expect; the surprise lifts the stock; buy" ([Oaktree](https://www.advisorperspectives.com/commentaries/2015/09/24/it-s-not-easy)). Soros's reflexivity adds the dynamic element. Rising prices bring capital, flows and analyst upgrades that reinforce the narrative, until the gap with reality breaks. **Booms are long and busts are short and sharp** ([GuruFocus](https://www.gurufocus.com/news/421890/george-soros-theory-of-reflexivity)). That pattern fits India's PSU, defence and railway run of 2023–24.

### The mind-map method

A practical mind map has three layers. Write the first-order event at the centre, for example "defence indigenisation," "PLI for electronics," "a leader distracted by ownership turmoil," or "AI data-center capex." Then branch outwards. **First-order beneficiaries** are the obvious names (OEMs such as HAL, BEL, Dixon). **Second-order beneficiaries** are component and subsystem suppliers. **Third-order beneficiaries** sit in raw materials, testing, logistics, power and financing. Then add the **losers** on each branch, for example importers, displaced incumbents, and customers whose margins get squeezed. For every node, ask which is the smallest listed company where this effect is a large share of profits, and whether the market already prices it in. The second-order node usually offers more asymmetry, because analysts cover the first-order names first. The map is a hypothesis generator. Each node still needs the fundamental and forensic tests below.

### Eight signals that preceded the case-study moves

| # | Signal to look for | Where to find it | Case example |
|---|---|---|---|
| 1 | A small, fast segment hidden inside a big, flat company | Segment notes, investor decks | NVIDIA data center FY16–18; Royal Enfield inside Eicher |
| 2 | Mix shift → gross margin → operating leverage | Concall commentary on mix, A&P spend | Radico revenue +44% → PAT +239% |
| 3 | Balance-sheet inflection (deleveraging, capex cycle ending) | Cash-flow statement, debt schedule | Radico D/E 0.77 → 0.15 |
| 4 | Policy documents that come before order books | Budget, PLI notifications, import lists | Defence, EMS |
| 5 | Competitor distress or industry structure change | News, channel checks, dealer and shelf visits | USL turmoil (unverified as a contemporaneous thesis); wind consolidation |
| 6 | Capacity utilisation >80% plus a brownfield expansion | Concalls, investor presentations | Deepak phenol |
| 7 | Promoter behaviour: buying, no pledge, refusing to dilute cheaply | SAST/PIT disclosures, shareholding pattern | Radico promoter refusing Mallya |
| 8 | A starting valuation that leaves room for rerating | P/E against own history and peers; reverse DCF | Radico (both engines) vs defence 2025 (rerating already spent) |

Fisher's **"scuttlebutt"** means talking to customers, suppliers, competitors and ex-employees. It is the original way to validate a mind-map node ([Fisher, *Common Stocks and Uncommon Profits*, primary text not re-fetched]). Professionals add paid alternative data such as card transactions and web scraping. Hedge funds are the largest buyers of alternative data, at about 55–68% of the market ([GM Insights](https://gminsights.com/industry-analysis/alternative-data-market)). Retail cannot match that, but free proxies cover much of the ground. In India these include monthly auto sales, GST and power data, concall transcripts, Google Trends, app rankings and job postings. Bulk and block deal data, monthly mutual-fund portfolio disclosures and quarterly shareholding patterns also give Indian investors unusually good visibility into what institutions are doing ([EquityResearchIndia](https://www.equityresearchindia.com/post/block-deals-and-bulk-deals-how-to-track-big-institutional-trades-and-what-they-signal); [SEBI](https://www.sebi.gov.in/legal/circulars/mar-2009/circular-portfolio-format-for-debt-oriented-close-ended-and-interval-schemes-plans_14185.html)). Treat superinvestor tracking as an idea source, never as conviction. US 13F filings arrive up to 45 days late, and research suggests much of the "superstar" alpha is earned before the filing becomes public ([Christoffersen et al.](https://www.bwl.uni-mannheim.de/media/Lehrstuehle/bwl/Area_Finance/Finance_Area_Seminar/HWS2018/Christoffersen_Paper.pdf); [InvestorLens](https://www.investorlens.capital/docs/faq/can-filings-predict-performance)).

---

## Legends, Indian masters and quant firms converge on quality bought at a sensible price

The legendary frameworks differ in emphasis but share a core: an understandable business with high, durable returns on capital, honest owner-minded management, low debt, a price below conservative value, and a long hold. Buffett's four filters are a business "(1) that we can understand; (2) with favorable long-term prospects; (3) operated by honest and competent people; and (4) available at a very attractive price" ([1977 letter](https://www.berkshirehathaway.com/letters/1977.html)). He also argued it is "far better to buy a wonderful company at a fair price than a fair company at a wonderful price" ([1989 letter](https://www.berkshirehathaway.com/letters/1989.html)). Munger's quote is the bridge between cheapness and quality. A business earning 6% on capital for 40 years returns about 6% even if bought at a big discount, while one earning 18% gives "one hell of a result" even at an expensive-looking price ([Farnam Street transcript](https://fs.blog/great-talks/a-lesson-on-worldly-wisdom/)). Terry Smith compresses it into "buy good companies, don't overpay, do nothing," with holdings typically earning **25–30% ROCE** ([Fundsmith](https://www.fundsmith.co.uk/news/2015/2171-this-is-money-firms-which-provide-good-products-or-services-are-key-to-investing-says-fundsmith-boss/); [Trustnet](https://www.trustnet.com/news/662915/three-simple-steps-to-making-returns-like-terry-smith)). Lynch adds categories (slow growers, stalwarts, fast growers, cyclicals, turnarounds, asset plays) and the PEG ratio, where a fairly priced P/E equals the growth rate ([Value Research](https://www.valueresearchonline.com/stories/51021/peter-lynch-s-six-stock-categories/)). Nick Sleep's "scale economics shared" explains Costco and Amazon. The firm passes savings from scale to customers, which drives volume and still lower costs ([Morningstar AU](https://www.morningstar.com.au/insights/personal-finance/254055/my-favourite-lessons-from-nick-sleeps-famous-investing-letters)). Mayer's 100-bagger traits are high sustained ROE, owner-operators, small starting size, a moat, a reasonable starting multiple and a "coffee can" hold ([Mindful Compounding](https://mindfulcompounding.substack.com/p/what-i-learned-from-chris-mayer); [Hedge Fund Alpha](https://hedgefundalpha.com/strategies/christopher-mayers-notes-100-baggers/)).

India's best-documented frameworks translate the same ideas locally. Motilal Oswal's **QGLP** stands for Quality of business and management, Growth in earnings, Longevity of both, and a favourable Price ([Motilal Oswal PMS](https://pms.motilaloswalmf.com/about-us/investment-philosophy)). The 100x study added **S for Size** (SQGLP) and concluded that "the biggest wealth is created when growth and rerating combine" ([Wealth Creation Study](https://www.motilaloswal.com/site/rreports/HTML/635542588369519988/index.htm)). Marcellus's **Consistent Compounders** filter demands **revenue growth above 10% and ROCE above 15% in every one of 10 consecutive years**. That leaves about 25–35 names, which moat research narrows to 12–15 ([Marcellus newsletter](https://marcellus.in/newsletter/consistent-compounders/valuing-longevity-of-healthy-fundamentals/); [Marcellus FAQ](https://marcellus.in/faqs)). Its forensic model grades accounting quality on about 10–12 ratios drawn from Schilit's *Financial Shenanigans* ([Marcellus](https://marcellus.in/portfolio-management-services/marcellus-consistent-compounder-pms)). Vijay Kedia's **SMILE** means "Small in size, Medium in experience, Large in aspiration, Extra-large in market potential" ([Value Research](https://www.valueresearchonline.com/stories/54019/how-to-invest-like-vijay-kedia/)). Jhunjhunwala, Kacholia, Dolly Khanna and Porinju Veliyath published **no formal checklists**. Their "rules" are media readings of their portfolio disclosures, so treat any specific claim about them as unverified.

Professional fundamental shops add process rather than secret formulas. Tiger Management's bull/bear debates stress-tested every idea, and the Tiger Cubs kept the pitch-and-debate model ([Wall Street Prep](https://wallstreetprep.com/knowledge/tiger-cubs)). Gary Klein's **pre-mortem** assumes the investment has already failed and asks why. The underlying "prospective hindsight" research found a 30% improvement in identifying reasons for future outcomes ([Klein, HBR](https://wiki.duraspace.org/download/attachments/104563925/ProjectPremortem.pdf?api=v2)). Some folklore edges have faded. The spin-off premium found in 1965–88 data looks much weaker in later samples ([McConnell et al. 2001](https://business.purdue.edu/faculty/mcconnell/publications/spinoffs-ex-ante-2001-vol74.pdf)). Greenblatt's magic formula reportedly works about 3 calendar years in 4. Greenblatt argues it keeps working *because* most investors quit after one or two bad years ([GuruFocus](https://www.gurufocus.com/news/891031/joel-greenblatt-why-people-dont-stick-to-their-strategies)). Critics note weaker post-publication returns ([Hedge Fund Alpha](https://hedgefundalpha.com/strategies/has-the-magic-formula-lost-its-sparkle/)).

Academic and quant evidence explains *why* the legends' ideas work. Novy-Marx found **gross profitability predicts returns about as well as book-to-market**, and the two are negatively correlated, so combining them is powerful ([Novy-Marx](https://www.ivey.uwo.ca/media/3775548/novy-marx.pdf)). AQR's **Quality Minus Junk** earns significant returns across 24 countries ([NBER](https://conference.nber.org/conf_papers/f69835.pdf)). **Value and momentum** premia appear across eight markets and asset classes ([AQR](https://www.aqr.com/Insights/Research/Journal-Article/Value-and-Momentum-Everywhere)). The small-cap premium reappears only **once junk is excluded** ([Asness et al.](https://research-api.cbs.dk/ws/files/57307999/lasse_heje_pedersen_et_al_size_matters_if_you_control_your_junk_publishersversion.pdf)). That directly supports the "S" in SQGLP and the "Small" in SMILE, but only with a quality filter attached. "Buffett's Alpha" found Berkshire's alpha **becomes insignificant after controlling for low-beta and quality factors**, with average leverage of about 1.7:1. In the authors' words, it is "a reward for leveraging cheap, safe, quality stocks" ([NBER w19681](https://www.nber.org/papers/w19681.pdf)). Renaissance's Medallion fund, at about 66% gross and 39% net a year from 1988 to 2018, is the exception that proves the limits. It is closed to outsiders, built on leverage and execution infrastructure, and RenTec's own external funds are "relatively mundane" ([Institutional Investor](https://www.institutionalinvestor.com/article/b1k2fymby99nj0/Famed-Medallion-Fund-Stretches-Explanation-to-the-Limit-Professor-Claims)). Retail investors can harvest slow factors such as quality, value and momentum. They cannot compete in high-frequency trading.

### Fundamental metrics cheat-sheet

The thresholds below are common practitioner conventions. They are not research-derived cut-offs, except where a source is named.

| Metric | Formula | Practitioner threshold / note |
|---|---|---|
| ROCE | EBIT ÷ (equity + debt) | >15% minimum (Marcellus); 20%+ high quality; 25–30% Fundsmith-type. India's cost of capital is ~12–14%, so 15% is the *floor*, not excellence |
| ROIC (incremental) | ΔNOPAT ÷ Δinvested capital | What matters for compounding is the return on *new* capital |
| Trailing vs forward P/E | Price ÷ LTM EPS vs ÷ next-FY consensus EPS | Forward P/E embeds analyst optimism; compare the two, then run a reverse DCF |
| PEG | P/E ÷ EPS growth % (3–5 yr) | <1 cheap, 1 fair, >1.5–2 expensive (Lynch); "a PEG below 1 is not proof" ([Validea](https://blog.validea.com/?p=32501)) |
| Reverse DCF | Solve for the growth the price implies | Mauboussin's core tool: is the implied growth plausible against base rates? ([Mauboussin excerpt](https://www.michaelmauboussin.com/s/EIexcerpt.pdf)) |
| Owner earnings | NI + D&A + non-cash − maintenance capex | Buffett 1986 ([letter](https://www.berkshirehathaway.com/letters/1986.html)) |
| FCF yield | (CFO − capex) ÷ market cap | >5% attractive for mature firms; compare with the ~6.5–7% Indian 10-yr G-sec |
| Cash conversion | CFO ÷ EBITDA (5–10 yr cumulative) | ≥70–80% healthy; persistently <50% is a forensic flag |
| Working-capital days | Debtor + inventory − payable days | Debtor days rising faster than sales = red flag |
| Leverage | D/E; net debt/EBITDA; EBIT/interest | D/E <0.5, ND/EBITDA <2x, coverage >5x (danger <2–3x) |
| Twin engine | Return ≈ (1+EPS growth) × (1+ΔP/E) + yield | Biggest winners had both engines; a high starting P/E removes one |
| Banks/NBFCs | P/B vs ROE; justified P/B ≈ (ROE−g)/(Ke−g) | ROCE, EV/EBITDA and CFO metrics don't apply; check GNPA, credit cost, cost of funds |

**Twin-engine rerating** is the central valuation idea for multibagger hunters. If earnings grow 5x and the P/E rises from 15 to 45, the stock rises 15x. If you pay 80x for the same 5x earnings growth and the multiple settles back to 40x, you make only 2.5x despite being right about the business. NVIDIA after 2023 shows the reverse case: earnings growth alone produced a multibagger even as the multiple compressed. Buying at already-elevated multiples still removes one engine and adds de-rating risk. Defence PSUs in 2025 traded at about **twice their historical forward multiples** ([Business Today](https://businesstoday.in/markets/stocks/story/mazagon-dock-hal-bdl-bel-share-price-targets-for-9-defence-stocks-ahead-of-q4-results-471974-2025-04-15)), so the rerating engine had largely been spent.

---

## Technical systems are momentum research wrapped in strict loss-cutting

Every well-known US growth-momentum system has the same four parts. The first is a **market-regime filter**: buy only in confirmed uptrends. The second is a **leadership universe**: strong earnings and sales growth, top-quintile relative strength, and a Stage 2 uptrend near 52-week highs. The third is a **low-risk entry** from a tight base on rising volume. The fourth is a **hard, small stop**, about 7–8% at most and often 3–5%. The rules below are as the authors describe them. Many details are drawn from the books and were not re-verified against primary editions, and online summaries often misquote thresholds.

| System | Core rules (per author) | Stop / exit |
|---|---|---|
| **CAN SLIM** (O'Neil) | Current quarterly EPS ≥25% YoY; Annual EPS growth ≥25% for 3 years, ROE ≥17%; New product/management/high; Supply–demand (volume); Leader, RS ≥80; Institutional sponsorship rising; Market in confirmed uptrend ([AAII](https://www.aaii.com/journal/article/william-oneil-can-slim-approach-to-selecting-growth-stocks)) | Cut every loss at 7–8%, no exceptions ([Liberated Stock Trader](https://www.liberatedstocktrader.com/what-is-canslim/)); take profits at 20–25% (book) |
| **Minervini Trend Template / SEPA / VCP** | Price > 150- and 200-DMA; 150 > 200; 200-DMA rising ≥1 month; 50 > 150 and 200; price > 50-DMA; ≥30% above 52-wk low; within 25% of 52-wk high; RS ≥70 ([Chartmill](https://www.chartmill.com/documentation/trading-and-investing/methodologies/523-SEPA-Explained-Mark-Minervinis-Specific-Entry-Point-Analysis-System)). VCP: 2–6 contractions, each about half the prior, volume drying up, buy the pivot | Max 10% stop, average loss ~5–6%, wins 2–3x losses (book) |
| **Weinstein Stage Analysis** | Weekly chart and 30-week MA. Stage 1 base → **Stage 2 breakout on ~2x volume** → Stage 3 top → Stage 4 decline. Buy only Stage 2; market and sector must also be Stage 2 ([MarketInOut](https://www.marketinout.com/stock-screener/stage-2-uptrend/india)) | Below the base, then trail under the 30-week MA; never hold Stage 4 |
| **Qullamaggie** | Breakouts after big moves and 2-week to 2-month tightening; Episodic Pivots on ~10%+ news gaps with heavy volume ([Tikamalma](https://tikamalma.substack.com/p/qullamaggie-swing-trading-setups)) | Stop at low of day; sell ⅓–½ after 3–5 days; trail with the 10/20-DMA; **risk 0.25–0.5%, win rate ~25–30%** ([CTE](https://completetradersedge.com/wp-content/uploads/2026/09/CTE-Research-Sheet-Kristjan-Kullamagi-market-wizards-next-generation.pdf)) |
| **Darvas / Livermore** | New highs on unusual volume in growing industries; buy box tops or pivotal points; pyramid only into profit, never average down | Just below the box bottom; exit if the stock "doesn't act right" |
| **Market regime (IBD)** | Follow-through day on day 4+ of a rally attempt; **5–6 distribution days in 25 sessions** = uptrend under pressure ([LuxAlgo](https://www.luxalgo.com/library/concept/distribution-days/)) | Cut exposure as distribution builds |

The evidence base is real but narrower than the marketing. **Cross-sectional momentum** (Jegadeesh & Titman: ~1% a month for 3–12-month winners) and the **52-week-high effect** are among the most robust anomalies in finance. Nearness to the 52-week high explains much of momentum and does not reverse, and it appears in 18 of 20 international markets ([George & Hwang 2004](https://doi.org/10.1111/j.1540-6261.2004.00695.x); [CXO Advisory](https://www.cxoadvisory.com/1284/technical-trading/the-52-week-high-as-a-momentum-indicator-for-individual-stocks/)). **Post-earnings-announcement drift**, where stocks keep drifting about 60 days after big surprises, underpins CAN SLIM's "C" and Qullamaggie's Episodic Pivots ([Bernard & Thomas 1989](https://doi.org/10.2307/2491062)). Momentum also works in India. Profits are concentrated in the winners (the long leg) and are not explained by CAPM or Fama-French ([Ansari & Khan 2012](https://emerald.com/insight/content/doi/10.1108/03074351211193730/full/html)). That matters because long-only cash investors keep most of the edge. Momentum does suffer **rare, violent crashes** when markets rebound sharply after a panic ([Daniel & Moskowitz 2016](https://doi.org/10.1016/j.jfineco.2015.12.002)). Market-regime filters exist to manage that risk. Specific chart shapes, such as exact cup depths and handle lengths, have weak, data-snooping-sensitive evidence. Park & Irwin's survey found positive results in 56 of 95 studies, but many had methodological problems, and the evidence is stronger in older samples ([Park & Irwin 2007](https://doi.org/10.1111/j.1467-6419.2007.00519.x)). The defensible conclusion is that patterns are **timing and risk-definition tools, not alpha sources**. The practitioners themselves credit their risk rules.

For Indian investors, the most rule-based implementation is the **Nifty200 Momentum 30** index. It holds the top 30 Nifty 200 stocks by volatility-adjusted 6- and 12-month returns and rebalances in June and December ([NSE factsheet](https://www.niftyindices.com/Factsheet/Factsheet_Nifty200_Momentum30.pdf)). Turnover is heavy: **19 of 30 names changed in the December 2025 rebalance** ([Business Standard](https://www.business-standard.com/markets/news/nifty200-momentum30-a-flip-of-index-switch-jolts-16k-cr-across-the-grid-125121400388_1.html)). Chartink, MarketInOut, Sharpely and Screener host ready-made Minervini/Stage-2 scans ([MarketInOut Trend Template India](https://www.marketinout.com/stock-screener/minervini-trend-template/india); [Screener "Mark minervini"](https://www.screener.in/screens/672150/mark-minervini)). The Indian adaptation needs a **liquidity floor**, for example ₹5–10 crore of daily traded value. Circuit limits on small caps can lock you in, and your stop may never execute.

The two schools combine cleanly. **Fundamentals decide what, Stage 2 decides when, the stop decides how much.** CAN SLIM, SEPA and Darvas's "techno-fundamentalism" were all designed this way ([AAII](https://www.aaii.com/journal/article/william-oneil-can-slim-approach-to-selecting-growth-stocks); [Chartmill](https://www.chartmill.com/documentation/trading-and-investing/methodologies/523-SEPA-Explained-Mark-Minervinis-Specific-Entry-Point-Analysis-System)). A long-term investor does not need to be a swing trader to use this. Simply refusing to add new money to a high-quality stock while it is in a Weinstein Stage 4 decline avoids many "right company, terrible timing" years, like Radico in 2008.

---

## Position sizing decides whether a good process survives

Sizing turns a set of probabilistic bets into a survivable compounding machine. Trading systems size every position from the stop. **Shares = (account × risk %) ÷ (entry − stop).** Risk per trade is kept at 0.25–1%, with a hard ceiling of 2%. Total open risk ("portfolio heat") stays at or below about 6–10%. Van Tharp's framework measures every outcome in **R-multiples**, where 1R is the initial risk. Expectancy is the average R per trade. A system that wins only 30% of the time, with average wins of 5R against average losses of 1R, has an expectancy of 0.30×5 − 0.70×1 = **+0.8R per trade**. That arithmetic is why low-hit-rate breakout systems can make money. The same arithmetic shows that losing streaks are certain. At a 30% win rate, ten straight losses has a probability of about 2.8% on any run of ten trades. At 1% risk per trade that costs about 9.6%; at 5% risk it costs about 40%.

The Kelly criterion formalises sizing by edge. It is also a warning. For the trading system above (W = 0.30, payoff 5), full Kelly says to **risk 16% of capital** per bet. For a fundamental bet with a 60% chance of +50% and a 40% chance of −25%, Kelly suggests **160% of capital**, which is absurd. Real investors use **¼ to ½ Kelly**, which keeps about 75% of the growth at half the volatility, plus hard position caps. They do this because their probability estimates are themselves unreliable ([Wikipedia: Kelly criterion](https://en.wikipedia.org/wiki/Kelly_criterion); [Old School Value](https://www.oldschoolvalue.com/investing-strategy/kelly-criterion-investing-portfolio-sizing/)). Thorp called full Kelly "too risky for the tastes of many, perhaps most, investors."

| Drawdown | Gain needed to recover |
|---|---|
| −10% | +11.1% |
| −25% | +33.3% |
| −50% | +100% |
| −75% | +300% |
| −90% | +900% |

Long-term multibagger investing faces a sizing paradox. Every big winner in the case studies had a 50–95% drawdown: Amazon −94%, NVIDIA twice more than −50%, Radico −74%, and Berkshire halved at least three times ([TIP](https://www.theinvestorspodcast.com/articles/100-bagger-stocks/)). A trader's 8% stop would have ejected you from all of them. An investor without any exit rule would also have held Suzlon to −99.6%. The answer is to **split the decision rules by holding type**. For trading positions, use price stops. For long-term compounders, use **thesis stops**: pre-written kill criteria based on fundamentals and governance. Pair them with **position sizes small enough that a 60% drawdown is painful but not ruinous**. Then let winners grow beyond their initial weight rather than trimming them mechanically. The pros' sell rules are: (1) a kill criterion triggers, (2) the variant view has been priced in (Steinhardt), (3) a clearly better risk/reward is available, or (4) a position limit is hit. A price drop alone is not on the list.

An illustrative portfolio structure (a synthesis, not a prescription) puts SPIVA's finding to work. If most active funds trail the index, a self-directed investor should hold a **low-cost index core**, with Indian and US exposure, and run active multibagger bets as a **satellite**. Within the satellite, sensible defaults are as follows. Hold 10–20 names. Start positions at 2–4% of the total portfolio. Raise a position to 6–10% only after the thesis is confirmed by earnings delivery. Cap any single name at about 15–20% at cost. Never use margin or F&O on multibagger theses. Mayer's rule applies to *your* balance sheet as well as the company's: avoid leverage so that drawdowns are not permanent. Indian tax rules reinforce patience. Since July 2024, listed-equity **STCG is 20% and LTCG is 12.5% above ₹1.25 lakh a year** after 12 months' holding ([Business Standard](https://www.business-standard.com/amp/finance/personal-finance/budget-2024-all-the-key-changes-to-capital-gains-tax-explained-124072500330_1.html)). Churn is taxed hardest.

---

## AI speeds up research but has not shown it can pick stocks

### What the evidence says

The strongest academic result is **Lopez-Lira & Tang**. ChatGPT's sentiment scores on news headlines significantly predict next-day returns and outperform older sentiment methods ([arXiv v6](https://arxiv.org/pdf/2304.07619v6)). But per-headline accuracy is only about 51%, and the signal emerges only across many firms and days ([Fortune](https://fortune.com/2023/04/21/chat-gpt-market-predicting-stock-price-movements/)). Later work shows that **LLM memorisation of past data inflates apparent predictability**. That makes backtests on periods the model was trained on unreliable ([Gao, Jiang & Yan](https://arxiv.org/pdf/2512.23847); [The Memorization Problem](https://arxiv.org/html/2504.14765v2)). Live tests are sobering. In Alpha Arena Season 1 (crypto, $10k each), **four of six models lost money and GPT-5 lost about 62%**, mainly from overtrading costs ([Benzinga](https://benzinga.com/crypto/cryptocurrency/25/11/48651974/chatgpt-lost-63-trying-to-trade-crypto-but-one-china-ai-made-a-healthy-profit); [Protos](https://protos.com/llm-crypto-trading-contest-finds-llms-cant-trade-crypto)). In Season 1.5 on US stocks, **only 6 of 32 entries finished positive** ([Forklog](https://forklog.com/en/news/ai-model-grok-4-2-triumphs-in-trading-tournament)). Nof1's founder said it is not yet feasible to hand an LLM money to trade on its own ([KuCoin News](https://www.kucoin.com/news/flash/ai-trading-models-struggle-in-live-market-tests-majority-of-systems-report-losses)). In Finder's 2026 AI portfolio showdown, **every aggressive AI portfolio lost money in October 2026** and trailed the Russell 2000 ([Finder AU](https://www.finder.com.au/insights/who-let-the-bots-out-2026-ai-portfolio-performance-showdown)). The headline "ChatGPT beat the market by 72%" results come from short paper portfolios ([Crypto Briefing](https://cryptobriefing.com/chatgpt-leads-rallies-ai-stock-market-arena/)). One study found ChatGPT portfolios putting **18–20% in Nvidia** ([Altiorem](https://altiorem.org/?p=25299)), so these results look like a concentrated tech bet in a strong tech market rather than demonstrated skill. The longest real-money record belongs to the **AIEQ ETF**, which returned about 9.7% a year against 14.2% for SPY over about nine years, at a 0.80% fee ([PortfoliosLab](https://portfolioslab.com/tools/stock-comparison/AIEQ/SPY)).

Hallucinated numbers are the practical danger. In FinanceBench (2023-era models), **GPT-4 Turbo with retrieval failed 81% of questions about filings**. Long-context runs failed 21% (GPT-4 Turbo) and 24% (Claude 2) ([Patronus/PR Newswire](https://prnewswire.com/news-releases/patronus-ai-launches-industry-first-llm-benchmark-for-finance-to-address-hallucinations-301990858.html)). Current frontier models are likely better, but no 2026 benchmark figure was found. Indian guides warn that plain chatbots give stale or invented numbers for Indian companies, and recommend pasting or connecting Screener data instead ([LumiChats](https://lumichats.com/blog/ai-for-stock-market-investing-india-2026)). The defensible role for AI is therefore as an **analyst-productivity multiplier**. It reads, summarises, compares, red-teams and flags forensic issues in primary documents that you supply. It should not be an oracle that tells you what will go up.

### The tool stack

| Layer | Tools | Notes |
|---|---|---|
| Claude skills and plugins | Anthropic's **financial-services** marketplace: `financial-analysis` (/comps, /dcf, /lbo, 3-statement), `equity-research` (/earnings, /earnings-preview, /initiate, /sector, **/thesis**, **/catalysts**, **/screen**), agents such as `earnings-reviewer`, `market-researcher`, `model-builder` ([GitHub](https://github.com/anthropics/financial-services-plugins)) | Install: `claude plugin marketplace add anthropics/financial-services`, then `claude plugin install equity-research@claude-for-financial-services` ([Claude docs](https://claude.com/docs/office-agents/fsi-plugins)). Premium connectors (FactSet, S&P, Morningstar, LSEG) need subscriptions; the skills work on filings you upload |
| India data / broker MCP | **Zerodha Kite MCP**: official, free, login via Kite with TOTP, works in Claude Desktop and Code ([Zerodha](https://zerodha.com/products/mcp/)); **Trendlyne MCP** connector, paid ([Trendlyne](https://trendlyne.com/subscription/mcp/plans/)) | Community Kite servers that can place orders are "use at your own risk" ([aptro/zerodha-mcp](https://github.com/aptro/zerodha-mcp)) |
| US data MCP | Financial Datasets (statements; API key), Alpha Vantage (free 25 req/day), Polygon/Massive (free 5 calls/min), Yahoo Finance community servers ([Geekflare](https://geekflare.com/guides/best-financial-data-mcp-servers/); [MarketXLS](https://marketxls.com/blog/best-financial-data-mcp-servers-ai-market-data)) | Yahoo-based servers have reliability concerns |
| India research | Screener.in (10-yr data, screens, AI filing summaries), **Tijori Concall Monitor** (transcript + AI summary), Valuepickr threads, a community Chrome extension that turns Screener data into forensic prompts ([Tijori/TradingQnA](https://tradingqna.com/t/tijori-s-ai-stack-for-company-research/194604); [ValuePickr](https://forum.valuepickr.com/t/tool-launch-free-chrome-extension-turn-screener-in-data-into-institutional-grade-ai-research-prompts-zero-data-collection-v2-0-0-us-stocks-forensic-analysis-under-review/218186)) | Most Indian "AI platform" comparisons are vendor-affiliated |
| Open-source agents | **TradingAgents** (analyst team + bull/bear debate + risk team; [arXiv](https://arxiv.org/html/2412.20138v4)), virattt/ai-hedge-fund (legend-persona agents, self-described as educational) | Short backtests are vulnerable to look-ahead bias; treat as learning tools |
| Automation | Claude Cowork/Code scheduled skills, e.g. a weekly scan of a watchlist for >10% 7-day moves ([Asian Century Stocks](https://www.asiancenturystocks.com/p/how-to-use-claude-for-equity-resear)) | Trading bots (Alpaca MCP) have only self-reported paper snapshots; paper-trade by default with loss circuit breakers ([Alzarak/trading-bot](https://github.com/Alzarak/trading-bot)) |

### An AI-assisted research workflow with concrete prompts

The best-documented practitioner workflow, Michael Fritzell's, works like this. Give Claude standing instructions as an equity analyst. Create **one Claude Project per saved prompt**. Then just type a ticker. Use the larger model for complex, multi-step analysis ([Asian Century Stocks](https://www.asiancenturystocks.com/p/how-to-use-claude-for-equity-resear)). The prompts below adapt his library, the steelman-the-bear technique ([Assistly](https://getassistly.co/blog/how-to-use-claude-for-stock-analysis)) and the Indian forensic checklist for an India-plus-US investor. **Always attach the primary documents** (annual reports, the last 8 concall transcripts, investor decks, rating rationales, and a Screener export) or connect a data MCP. Require a citation for every number.

```text
SYSTEM / PROJECT INSTRUCTIONS
You are a skeptical buy-side equity analyst. Use ONLY the documents I attach
or data returned by connected tools. For every number, cite the document and
page/section. If a figure is not in the sources, say "NOT IN SOURCES" — never
estimate silently. Separate FACT (sourced), INFERENCE (your reasoning), and
UNKNOWN. Be brief and concrete.
```

```text
1) BUSINESS & SEGMENTS
Explain [COMPANY]'s business model in simple terms: products, customers,
suppliers, competitors, pricing/contract terms. Build a 10-year table of
segment revenue and segment EBIT. Identify the smallest segment growing
fastest and its share of incremental profit over the last 3 years.
```

```text
2) SECOND-ORDER MIND MAP
Event/theme: [e.g., defence indigenisation / PLI electronics / AI data-centre
capex / competitor X distress]. Map first-, second- and third-order listed
beneficiaries and losers in [India/US]. For each node give: why it benefits,
% of the company's profit plausibly exposed, what would have to be true, and
which public data (order inflows, capacity utilisation, monthly volumes) would
confirm it within 2 quarters. Flag which nodes are already heavily covered.
```

```text
3) FORENSIC ACCOUNTING (India)
You are a forensic accountant using Schilit's Financial Shenanigans. From the
attached annual reports (last 5 yrs), compute and trend: CFO/EBITDA and
cumulative CFO/PAT; debtor, inventory, payable days; CWIP/gross block;
capitalised expenses (R&D, know-how, interest); other income % of PBT; cash +
debt both high (yield on cash); contingent liabilities and guarantees / net
worth; related-party transactions as % of revenue (AS/Ind AS 24 note + AOC-2);
auditor changes, qualifications, emphasis of matter, CARO remarks; promoter
pledge, preferential allotments/warrants; promoter remuneration vs PAT.
Output a red/amber/green table with page citations.
```

```text
4) CONCALL TRUTH-TRACKER
From the last 8 concall transcripts, tabulate every quantitative guidance
statement (revenue, margin, capex, capacity, debt) and what was actually
delivered in later quarters. Score management's guidance accuracy. Note shifts
in tone, newly introduced metrics, and metrics that quietly disappeared.
```

```text
5) VARIANT PERCEPTION + REVERSE DCF
State (a) the consensus view and what the current price implies: solve a
reverse DCF for the revenue growth and margin needed over 10 years at a
[12–13% INR / 9% USD] discount rate; (b) my variant view: [paste]; (c) the
specific catalyst/trigger and its timing; (d) whether the implied growth is
plausible against base rates (few firms sustain >20% growth for 10 years).
Decompose a 5-year scenario into EPS growth × P/E change (twin engine).
```

```text
6) STEELMAN THE BEAR / PRE-MORTEM
Act as a skeptical short-seller. It is 3 years from now and this position lost
60%. Write the most plausible story of why, using only public data. Test the
moat, customer concentration, capital allocation, governance, and valuation if
growth disappoints by 20–30%. Then list 5 measurable KILL CRITERIA that would
tell me early that this story is happening.
```

```text
7) QUESTIONS FOR MANAGEMENT / SCUTTLEBUTT
List 15 questions ranked by information value for management, and 10 for
channel checks (dealers, distributors, customers, ex-employees), that would
most change my estimate of [key value driver].
```

```text
8) THESIS TRACKER (quarterly)
Here is my thesis memo and kill criteria [paste]. Here are the new results,
concall and shareholding pattern [attach]. For each thesis pillar and kill
criterion: confirmed / weakened / broken, with citations. Has the variant
perception been priced in (P/E vs my target, consensus estimate revisions)?
Recommend: hold / add / trim / exit, with reasons — I will decide.
```

In Claude Code with the equity-research plugin, `/thesis` and `/catalysts` can maintain prompts 8 and 5 on a schedule, and `/screen` can seed idea generation. **The human sets sizing and makes the final decision.** Delegating order placement to an agent is exactly the overtrading failure that sank most Alpha Arena entrants.

---

## The A-to-Z process for an Indian investor who also buys US stocks

The process below draws the evidence together. Each stage names its tool, its output and the decision gate it must pass.

| Step | What you do | Tools | Gate to pass |
|---|---|---|---|
| **0. Set structure** | Index core (India + US) plus an active satellite; write position-size and drawdown rules *before* buying | Index funds/ETFs; written policy | Rules exist in writing |
| **1. Idea generation** | Second-order mind maps of policy, cycle and industry shifts; segment surprises in results; new 52-week highs after strong earnings; MF portfolio additions, bulk deals, promoter buying; Valuepickr; 13F as ideas only | Screener, Trendlyne, Chartink, NSE/BSE announcements, Claude prompt 2 | A one-line "why this could be mispriced" |
| **2. Quant screen** | Quality / GARP / small-cap / turnaround screens (below) plus forensic overlay | Screener.in, Tickertape, Finviz-type for US | Passes quality and forensic filters |
| **3. Forensic & governance** | Annual-report deep read; red-flag list (below) | Claude prompt 3, rating rationales, SAST/pledge filings | **Zero** "kill" flags |
| **4. Deep dive** | Business, segments, moat, management truth-tracking, unit economics, scuttlebutt | Prompts 1, 4, 7; concalls; channel checks | You can explain the business and its moat in 5 sentences |
| **5. Thesis & variant perception** | Write a 1-page memo: consensus, variant view, catalyst, what must be true, kill criteria | Prompts 5, 6 | The variant view is *specific and testable* |
| **6. Valuation** | Reverse DCF; twin-engine scenarios (bear/base/bull with probabilities); P/E vs own history | Spreadsheet or `/dcf`; prompt 5 | Probability-weighted upside ≥ 2–3x the downside |
| **7. Entry timing** | Prefer Stage 2 or base breakout; avoid adding during Stage 4; check market regime | Chartink/TradingView; 30-week MA; Nifty 500/S&P regime | Not in Stage 4; regime not in heavy distribution |
| **8. Sizing** | Start 2–4%; scale up on *earnings confirmation*; cap at ~15–20% at cost; trading positions sized from the stop at 0.5–1% risk | Position calculator | Survivable if it falls 60% |
| **9. Monitoring** | Quarterly thesis tracker; shareholding/pledge; guidance vs delivery; reflexivity check on themes | Prompt 8; `/thesis`; `/catalysts` | Pillars intact |
| **10. Selling** | Kill criterion hit; variant view priced in; better risk/reward available; size limit reached; governance breach = immediate exit | Decision journal | Pre-committed rule, not emotion |

### Screener.in starting queries

These were written by a researcher in Screener's syntax and have not been tested on the site. Paste and test them before use, and check the field names.

```text
Quality compounder:
Market Capitalization > 2000 AND Average return on capital employed 5Years > 20 AND
Return on equity > 18 AND Debt to equity < 0.3 AND Sales growth 5Years > 12 AND
Profit growth 5Years > 12 AND Pledged percentage < 5 AND Promoter holding > 40

GARP:
Profit growth 3Years > 20 AND Sales growth 3Years > 15 AND Return on capital employed > 18
AND PEG Ratio < 1.2 AND Price to Earning < Industry PE AND Debt to equity < 0.5 AND
Market Capitalization > 1000

Small-cap multibagger hunt:
Market Capitalization > 300 AND Market Capitalization < 5000 AND Sales growth 3Years > 20
AND Profit growth 3Years > 25 AND Return on capital employed > 18 AND Debt to equity < 0.5
AND Promoter holding > 50 AND Pledged percentage = 0 AND Cash from operations last year > 0

Turnaround:
Net profit > 0 AND Net Profit last year < 0 AND Sales growth > 20 AND OPM > OPM last year
AND Debt to equity < 1 AND Pledged percentage < 10

Forensic overlay (append to any screen):
AND Debtor days < 90 AND Pledged percentage < 5
```

The public **"Coffee Can Investing"** Screener screen requires average ROCE and ROE above 14% across 10/7/5/3-year windows, sales growth above 9%, D/E below 1 and pledge below 15%. It returned about 100 names in November 2026 and is a good template to clone ([Screener](https://www.screener.in/screens/1125448/coffee-can-investing/)). For technical gating, ready-made Minervini Trend Template scans exist for India ([MarketInOut](https://www.marketinout.com/stock-screener/minervini-trend-template/india)).

### Multibagger candidate checklist

| Dimension | Pass condition |
|---|---|
| Size & runway (S) | Market cap small relative to an addressable market that can grow 5–10x; 8 of the top-10 fastest creators started below ₹2,000 cr |
| Quality (Q) | ROCE >15–20% through a cycle (or a credible path there); CFO/EBITDA ≥70%; low debt |
| Growth (G) | Revenue and EPS growth >15–20%, ideally *accelerating*; a fast segment or mix shift visible |
| Longevity (L) | Moat named and evidenced: brand, scale economics shared, switching costs, cost advantage, regulatory licence |
| Management | Owner-operator; guidance matches delivery; no pledge; sensible related-party transactions; capital-allocation record |
| Price (P) | Starting multiple leaves room for rerating; reverse DCF implies plausible growth; PEG near or below ~1–1.5 |
| Variant view | You can state the consensus view, your differing view, and the catalyst |
| Asymmetry | Bull case ≥ 3–5x; bear case survivable at your position size |
| Timing | Not in Stage 4; ideally a Stage 2 base or an earnings-led breakout |

### Red flags: when any of these appears, stop or exit

| Red flag | Real Indian example |
|---|---|
| **Auditor resignation mid-term**, especially citing missing information | Vakrangee: PwC quit, and the stock fell ~84% from ₹515 to ~₹81.5 in 2018 ([Business Standard](https://www.business-standard.com/amp/article/markets/vakrangee-hits-22-month-low-after-auditor-pwc-flags-concerns-118050700332_1.html)); Manpasand: Deloitte quit in 2018, MD arrested in a ₹40 cr GST fraud ([Business Standard](https://www.business-standard.com/amp/article/current-affairs/manpasand-beverages-md-officials-arrested-in-rs-40-crore-gst-fraud-119052500241_1.html)) |
| **Fund diversion via related parties** | Gensol: ₹663.89 cr earmarked for 6,400 EVs, only 4,704 bought, funds allegedly used for a ₹42.94 cr DLF Camellias flat; promoters barred ([Outlook Business](https://www.outlookbusiness.com/news/blusmart-crisis-gensol-loans-for-procuring-evs-used-to-buy-dlf-camellias-flat-says-sebi)) |
| **Profits inflated via delayed impairments; preferential-issue money that doesn't show up** | Brightcom: ~₹1,280 cr inflation in FY19–20 per SEBI ([BQ Prime](https://www.bqprime.com/business/sebi-unravels-how-brightcom-group-cooked-its-books)) |
| **Related-party disclosures that don't match across group entities; aggressive capitalisation** | Kaynes (Dec 2025): Kotak flagged RPT mismatches and ₹180 cr capitalised; the stock nearly halved from its high ([Business Today](https://www.businesstoday.in/markets/stocks/story/kaynes-tech-shares-extend-fall-sink-8-today-as-kotak-flags-disclosure-gaps-co-issues-clarification-505187-2025-12-05)). The company called it an inadvertent disclosure error, and no regulator action was found |
| **Credit-rating downgrade or "Issuer Not Cooperating"** | Gensol downgrades around the SEBI order ([Business Today](https://businesstoday.in/markets/stocks/sebi-interim-order-gensol-fund-diversion-stock-plunge-credit-downgrades-472172-2025-04-16)) |
| **Finfluencer/Telegram promotion; paid "news" videos** | Sadhna Broadcast pump ([exchange4media](https://www.exchange4media.com/influence-zone-news/sadhna-broadcast-case-sebi-tightens-grip-on-finfluencers-143991.html)); Asmita Patel: >₹53 cr impounded ([YourStory](https://yourstory.com/2025/02/sebi-bans-fininfluencer-asmita-patel-5-others-from-mkt-impound-illegal-gains-of-over-rs-53-cr)) |
| **SME IPO with a sharp post-listing run-up** | SEBI tightened SME rules in March 2025 after finding diversion of IPO proceeds and circular-RPT revenue ([IndiaCorpLaw](https://indiacorplaw.in/2025/04/23/strangling-growth-or-ensuring-stability-sebis-new-regulatory-framework-for-smes/)) |
| CFO/PAT persistently below ~0.7; debtor or inventory days rising faster than sales; CWIP stuck for years | Marcellus forensic ratios ([Elearnmarkets](https://www.elearnmarkets.com/school/units/diamonds-in-the-dust/marcellus-s-3-level-check-to-detect-accounting-frauds)) |
| High cash *and* high debt; other income a large share of PBT | Classic Indian flag. Satyam's fictitious cash is the canonical case (**not re-verified here**) |
| Rising promoter pledge; frequent preferential issues to obscure entities; heavy debt-funded expansion | Suzlon's −99.6% after a leveraged expansion ([Business Today](https://www.businesstoday.in/markets/stocks/story/suzlon-energy-shares-down-96-in-5-years-this-stock-rebounded-42x-heres-why-456906-2024-12-11)) |

The highest-risk combination in the case record is an **auditor resignation, plus preferential issues, plus loud promoter communication, plus finfluencer hype, plus a rising pledge**. Regulators do not always conclude fraud. SEBI closed its Hindenburg proceedings against Adani in September 2025, finding the allegations "not established" ([Business Standard](https://www.business-standard.com/amp/markets/news/sebi-clears-adani-group-dismisses-hindenburg-allegations-125091801259_1.html)). A retail investor does not need a regulator's burden of proof, though. **Doubt is a sufficient reason to pass.** Standard scoring tools, the Beneish M-score (above −1.78 suggests manipulation risk), the Altman Z-score and the Piotroski F-score, are useful as overlays, but the research found no validation of them on Indian data.

### Context for late 2026

Market valuations affect which engine you can rely on. In mid-November 2026 the Nifty 50 traded at about **20.6x trailing earnings**. Midcap forward P/E was close to its 10-year average (22.8x vs 23.2x). **Small-cap forward P/E stood at 21.9x against a 10-year average of 18.7x** ([HDFC MF](https://www.hdfcfund.com/learn/deep-dives/tuesday-talking-point/equity-valuations-remain-reasonable-despite-market-uptick)). These figures change constantly, so re-check them. With small caps still at a premium, new small-cap bets need **earnings delivery rather than further rerating** to work. Cycle history warns against buying a theme at its peak multiple. The BSE Capital Goods index took **14 years to regain its 2007 peak** ([Business Standard](https://business-standard.com/article/markets/bse-capital-goods-index-hits-fresh-52-week-high-l-t-bel-gain-up-to-3-120121400412_1.html)).

---

## Conclusion

The user's example contains the most useful lesson of all, once corrected. The "UBL issue" story frames a multibagger as one brilliant insight followed by an inevitable rise. The real Radico record shows something else: years of dead money, then a slow change in the business (premium mix, debt reduction, operating leverage) that anyone reading segment commentary and balance sheets in 2016–17 could see. It paid off through two engines at once, earnings and the multiple. NVIDIA shows the same pattern in a different form. In both cases the edge lay in **interpreting public data differently and having the temperament to hold through 50–75% drawdowns**, not in information others lacked. That shifts the investor's job. Finding the idea matters less than (a) a forensic filter that removes the Suzlons and Gensols, which tell the same story as the winners, (b) a valuation discipline that keeps both engines available, and (c) sizing and kill rules that let you survive the many bets that will fail, as base rates guarantee.

AI changes the cost of that work, not its nature. A retail investor with Claude, a Screener export, eight concall transcripts and a forensic prompt can now do in an evening the document-reading that once needed an analyst team. That makes the "reading between the lines" stage cheaper than it has ever been. The evidence also says that handing the *decision* to a model reproduces the classic retail failures of overtrading, concentration and invented numbers. The durable edge for an Indian investor seeking generational wealth is unglamorous: an index core, a concentrated but size-capped satellite of quality small and mid-cap compounders bought before their rerating, AI used as a tireless skeptic, and enough patience to let the rare 4% winner do what the other 96% cannot.
