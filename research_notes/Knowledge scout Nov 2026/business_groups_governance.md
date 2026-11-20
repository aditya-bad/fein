# Indian business groups: governance-history library

*Knowledge scout, Nov 2026. Research date 2026-11-19 and 20. Seed file: `memdb/seeds/2026-11-19_business_groups.json` (49 records: 43 group/promoter `person` records, 6 `insight` records). Not ingested yet.*

This is research, not SEBI-registered advice. Each profile keeps **regulator/court findings**, **interim orders**, **settlements** and **allegations** separate. Allegations are labelled as unproven. Figures marked single-source or 'verify' were not checked against a second dated source.

## Flag scale
- **clean**: no meaningful minority-harm episodes; good capital return
- **mostly-clean**: good listed-company conduct, with holdco/trust disputes, capital-allocation misses or old/unproven allegations
- **mixed**: real minority-relevant concerns (pledges, RPTs, contested regulatory matters) next to good conduct
- **poor**: documented minority harm or regulator findings, but not a total wipe-out
- **severe**: regulator/court findings of diversion or fraud, or equity wiped out by promoter conduct

## Summary table

| Group | Flag | Main listed tickers | Status 2026 | Record id |
|---|---|---|---|---|
| Bajaj group (Rahul Bajaj family: Rajiv & Sanjiv Bajaj) | clean | BAJAJ-AUTO, BAJFINANCE, BAJAJFINSV, BAJAJHLDNG, BAJAJHFL | FY26 dividend Rs150 + Rs5,633cr buyback (May-2026) | `person:group-bajaj` |
| Bharti group (Sunil Bharti Mittal) | clean | BHARTIARTL, BHARTIHEXA, INDUSTOWER | promoter ~50%; Singtel sell-downs | `person:group-bharti` |
| Burman family (Dabur; Eveready, Religare via family office) | clean (Dabur); mostly-clean (Religare/Eveready takeovers) | DABUR, EVEREADY, RELIGARE | Burmans control Religare since Feb-2025 | `person:group-burman-dabur` |
| Godrej family (Godrej Industries Group / Godrej Enterprises Group) | clean | GODREJIND, GODREJCP, GODREJPROP, GODREJAGRO, ASTECLIFE | Pirojsha Godrej GIG chair from Aug-2026 (announced plan) | `person:group-godrej` |
| HCL group (Shiv Nadar, Roshni Nadar Malhotra) | clean | HCLTECH | Roshni Nadar controlling promoter since Mar-2025 | `person:group-hcl-nadar` |
| Infosys founders (Narayana Murthy, Nilekani et al.) | clean | INFY | no open issues | `person:group-infosys-founders` |
| Mahindra group | clean | M&M, M&MFIN, TECHM, MAHLIFE, MHRIL | no open issues found | `person:group-mahindra` |
| Murugappa group | clean | CHOLAFIN, CHOLAHLDNG, TIINDIA, CUMI, COROMANDEL | no open governance issues found | `person:group-murugappa` |
| Wipro / Azim Premji | clean | WIPRO | no open issues found | `person:group-wipro-premji` |
| Aditya Birla Group (Kumar Mangalam Birla) | mostly-clean | GRASIM, HINDALCO, ULTRACEMCO, ABCAPITAL, ABFRL | Vi AGR relief + ABG warrant infusion (single-source amounts) | `person:group-aditya-birla` |
| CK Birla group | mostly-clean | ORIENTELEC, HIL, BSOFT, ORIENTPPR | no open issues found (limited scan) | `person:group-ck-birla` |
| Dalmia Bharat group (Jai Hari & Puneet Dalmia) | mostly-clean | DALBHARAT, DALMIASUG | ED attachment reportedly released Apr-2026 | `person:group-dalmia` |
| OP Jindal family groups (JSW / Sajjan; JSPL / Naveen; Jindal Stainless / Ratan) | mostly-clean (JSW, JSL); mixed (JSPL) | JSWSTEEL, JSWENERGY, JSWINFRA, JSWHL, JSWCEMENT | SC stay on JSPL coal cognisance (Jul-2026); BPSL plan upheld (Sep-2025) | `person:group-jindal` |
| Piramal group (Ajay Piramal family) | mostly-clean | PIRAMALFIN, PPLPHARMA | PEL merged into Piramal Finance (Sep-2025) | `person:group-piramal` |
| Reliance group (Mukesh Ambani) | mostly-clean | RELIANCE, JIOFIN, NETWORK18, TV18BRDCST, HATHWAY | Jio IPO timing reports conflict (Oct-2026 vs H2FY27) | `person:group-reliance-mukesh` |
| TVS group (Venu Srinivasan branch and other TVS families) | mostly-clean | TVSMOTOR, TVSHLTD, SUNDARMFIN, TVSSCS, SUNCLAY | dispute unresolved as of Oct-Nov 2026 | `person:group-tvs` |
| Tata group (Tata Sons / Tata Trusts) | mostly-clean | TCS, TMPV, TATASTEEL, TITAN, TATAPOWER | RBI again told Tata Sons to list (17-Nov-2026); trusts split | `person:group-tata` |
| Adani group (Gautam Adani) | mixed | ADANIENT, ADANIPORTS, ADANIPOWER, ADANIGREEN, ADANIENSOL | FPI-ownership probe continuing after settlements rejected (Aug-2026) | `person:group-adani` |
| Emami group (R.S. Agarwal & R.S. Goenka families) | mixed | EMAMILTD, EMAMIPAP, EMAMIREAL | fresh pledge Jan-2026 (~4.95%); ~16% of promoter holding pledged (aggregator) | `person:group-emami` |
| GMR group (G.M. Rao family) | mixed | GMRAIRPORT, GMRP&UI | no regulator orders found | `person:group-gmr` |
| Hinduja group (Hinduja brothers / IIHL) | mixed | INDUSINDBK, ASHOKLEY, HGS, GULFOILLUB, RELCAPITAL | succession after Gopichand's death unresolved | `person:group-hinduja` |
| KK Birla group (Chambal, Avadh/Magadh Sugar, HT Media) and MP Birla group (Birla Corp; Lodha estate dispute) | mixed (MP Birla); mostly-clean (Chambal/Avadh) | CHAMBLFERT, AVADHSUGAR, MAGADSUGAR, HTMEDIA, BIRLACORPN | Birla-Lodha litigation continuing (latest verified ruling Dec-2023) | `person:group-kk-birla-mp-birla` |
| Kalyani group (Baba Kalyani; Bharat Forge) | mixed | BHARATFORG, KALYANIFRG, KSL, BFINVEST, HIKAL | SC-appointed mediation (Jul-2026) | `person:group-kalyani` |
| Vedanta group (Anil Agarwal) | mixed | VEDL, HINDZINC | demerger effective 1-May-2026 | `person:group-vedanta` |
| Essel group (Subhash Chandra, Punit Goenka) | poor | ZEEL, DISHTV, ZEEMEDIA, SITINET | SEBI 1-yr ban on Chandra/Goenka (Jul-2026), SAT proceedings | `person:group-essel-zee` |
| Future group (Kishore Biyani) | poor | FRETAIL, FLFL, FCONSUMER, FEL, FSC | FRL in liquidation; group equity largely wiped out | `person:group-future` |
| GVK group (G.V. Krishna Reddy family) | poor | GVKPIL | no current status found; MIAL with Adani; GVKPIL penny stock | `person:group-gvk` |
| Kushagra Bajaj group (Bajaj Hindusthan Sugar, Bajaj Consumer Care) | poor (BAJAJHIND); mixed (BAJAJCON) | BAJAJHIND, BAJAJCON | BHSL debt-to-equity/CCPS conversion Mar-2026 | `person:group-bajaj-kushagra` |
| Lanco group (Lagadapati Madhusudhan Rao family) | poor | LITL | under liquidation since 2018 | `person:group-lanco` |
| PC Jeweller (Balram Garg) | poor | PCJEWELLER | bank-debt-free per filings; dilution via preferential warrants | `person:group-pc-jeweller` |
| Rajesh Exports (Rajesh Mehta) | poor | RAJESHEXPO | fresh forensic audit; NFRA probe | `person:group-rajesh-exports` |
| Ruchi Soya (Shahra family) → Patanjali Foods (Patanjali/Ramdev) | poor (Shahra); mixed (Patanjali) | PATANJALI | MPS compliant; RPTs with Patanjali Ayurved continue | `person:group-ruchi-patanjali` |
| Byju's / Think & Learn (Byju Raveendran) | severe | (unlisted) | Think & Learn in insolvency; US damages phase pending | `person:group-byjus-raveendran` |
| Gensol / BluSmart (Anmol & Puneet Singh Jaggi) | severe | GENSOL | Gensol and BluSmart in CIRP; CBI/ED cases pending | `person:group-gensol-jaggi` |
| Jaypee group (Jaiprakash Gaur / Manoj Gaur) | severe | JPASSOCIAT, JPPOWER, JPINFRATEC | JAL to Adani via IBC (NCLAT May-2026); JIL with Suraksha | `person:group-jaypee` |
| Malvinder & Shivinder Singh (Ranbaxy, Fortis, Religare) | severe | FORTIS, RELIGARE | criminal cases pending; new promoters at Fortis/Religare | `person:group-religare-singh` |
| Reliance Anil Dhirubhai Ambani Group (ADAG, Anil Ambani) | severe | RPOWER, RELINFRA, RCOM, RELCAPITAL, RHFL | ED/CBI probes active; aides arrested Apr-2026; personal insolvency admitted | `person:group-reliance-adag` |
| Sandesara family (Sterling Biotech group) | severe | STERLINGBI | SC told SEBI to close proceedings (2026) | `person:group-sterling-sandesara` |
| Srei group (Hemant & Sunil Kanoria) | severe | SREINFRA | under NARCL; equity extinguished | `person:group-srei-kanoria` |
| UB group / Kingfisher (Vijay Mallya) | severe (historical); current UNITDSPR/UBL under MNC control | UNITDSPR, UBL, MCDHOLDING | extradition pending in UK; SBI recoveries ongoing | `person:group-ub-mallya` |
| Videocon group (Venugopal Dhoot family) | severe | VIDEOIND | listed equity worthless in practice; cases pending | `person:group-videocon` |
| Wadhawan family (DHFL; earlier HDIL link) | severe | DHFL | criminal trial ongoing; brothers on bail (Dec-2025) | `person:group-dhfl-wadhawan` |
| Yes Bank / Rana Kapoor | severe | YESBANK | Kapoor on bail; SMBC largest holder | `person:group-yes-bank-rana-kapoor` |

## Pattern insights

### India: group contagion runs through promoter-level leverage and repeats with the credit cycle
`insight:group-contagion-pledge-cycles` · confidence: verified

Across the 43 group profiles reviewed (Nov-2026), the worst minority outcomes (ADAG, Essel, Future, Jaypee, Videocon, Lanco, GVK, Srei, Singh brothers) shared one structure: the promoter borrowed outside the listed company -- against its shares, or through cross-guarantees -- to fund unrelated, capital-hungry ventures (power, infra, real estate, telecom, oil). The trigger is usually an outside credit event, not the business itself: the 2008 crisis, the 2013-14 infra bust, IL&FS (Sep-2018, which froze MF/NBFC loans against shares), and COVID (2020). Pledge cycles repeat even in good groups: Emami pledged, sold ~10% in Feb-2019 to cut group debt, and a fresh ~4.95% pledge appeared in Jan-2026; Bajaj Consumer's promoters had ~70% of their stake pledged in Dec-2018 to support the sugar/power side before cutting it to zero in Oct-2019; JSW and GMR carry long-running encumbrance. Contagion is group-wide: when one company defaults, lenders cut lines to all of them, pledges get invoked, and the stocks fall together regardless of each one's fundamentals (Essel 2019: Zee, Dish, Zee Media, Siti; ADAG 2018-19). Rules: (1) count pledges across all group listed companies plus promoter holdco debt; (2) a rising pledge in a bull market is borrowing against inflated collateral; (3) a pledge cut by selling stake (Emami 2019, BAJAJCON 2019, Adani 2023) helps, but check where the money went; (4) the cycle tends to come back at the next credit tightening. Complements insight:promoter-pledge-group-contagion.

Sources: <https://business-standard.com/article/companies/emami-promoters-sell-10-stake-to-pare-group-debt-pledged-shares-119021801092_1.html> · <https://www.business-standard.com/amp/article/companies/promoters-sell-22-stake-in-bajaj-consumer-care-for-rs-700-crore-119101501423_1.html> · <https://www.moneylife.in/article/sebi-bars-former-zee-executives-subhash-chandra-punit-goenka-from-securities-market-for-1-year/81233.html> · <https://filingreader.com/news-wire/mumbai/2025-11-14/gmr-enterprises-pledges-shares-in-gmr-power-and-urban-infra>

### The cash-rich listed company is often what pays for the promoter's sick sibling
`insight:clean-cash-cow-funds-sick-sibling` · confidence: verified

A recurring Indian pattern: a high-quality, cash-generative listed company sits in the same group as a loss-making, capital-hungry sibling, and value moves from the first to the second through ICDs, guarantees, letters of comfort, collateral or forced promoter selling. Cases: United Spirits -> Kingfisher (SEBI 2017: ~Rs 1,880 cr diverted to UB-group entities); Zee -> Essel infra (SEBI 2023: letter-of-comfort FD adjustments; SEBI 31-Jul-2026: ZEEL's Hyderabad land mortgaged for four Essel entities' loans without authority); Jaypee Infratech -> Jaiprakash Associates (SC 2020: ~858 acres mortgaged for the parent's debt held to be preferential transactions); MIAL -> GVK group (CBI FIR 2020 alleges ~Rs 705 cr); Bajaj Consumer -> Bajaj Hindusthan/Lalitpur Power (2018-19 pledges, stake sales to fund the power business); Emami -> cement/power (2019 stake sale to repay group debt). Things to check every year: (1) RPT notes listing loans, guarantees or security given to group firms; (2) 'other financial assets' and capital advances to related parties; (3) charge filings on MCA showing listed-company assets securing other entities' loans; (4) the promoter's other businesses and their debt; (5) whether a strategic partner or buyer (Diageo at USL) later finds diversions, since they often do. Rule: the safety of a great franchise is capped by the weakest balance sheet the promoter controls.

Sources: <https://www.business-standard.com/article/pti-stories/sebi-bans-mallya-6-others-in-usl-fund-diversion-case-117012501425_1.html> · <https://www.moneylife.in/article/sebi-bars-former-zee-executives-subhash-chandra-punit-goenka-from-securities-market-for-1-year/81233.html> · <https://theprint.in/india/cbi-books-gvk-group-chairman-gvk-reddy-son-over-alleged-rs-705-crore-mumbai-airport-scam/452805> · <https://www.business-standard.com/amp/article/companies/promoters-sell-22-stake-in-bajaj-consumer-care-for-rs-700-crore-119101501423_1.html>

### Indian holding companies trade at deep, persistent discounts, and the discount rarely closes on its own
`insight:group-holdco-discount` · confidence: single-source

Listed holdcos in good groups (Bajaj Holdings, Tata Investment, Godrej Industries, Cholamandalam Financial Holdings, TVS Holdings, BF Investment/Kalyani Investment, and Grasim with its stakes in UltraTech and ABCL) usually trade well below the market value of their listed stakes. Commonly cited gaps are 40-70%, but that range was not re-derived here, so compute it yourself for each name. The reasons are structural: tax leakage on dividends and exits, no promoter intent to distribute or unwind, the holdco being used to fund new ventures (Grasim -> paints and B2B e-commerce), illiquidity, and control premia that accrue to the promoter, not to minorities. What actually closed gaps in this sample was a corporate event: a demerger or mirror listing (Bajaj 2008, Vedanta 2026, Piramal 2022), a regulator forcing a listing (RBI's upper-layer rule for Tata Sons, reiterated 17-Nov-2026, which matters for Tata Investment and SP group), a merger of holdco into opco (Piramal Enterprises into Piramal Finance, Sep-2025; GMR 2024), or a buyback/dividend policy change. Rules: (1) 'cheap vs NAV' is not a thesis without a named catalyst and its probability; (2) family disputes (TVS 2026, Kalyani 2023-26) can widen the discount; (3) holdco debt (Vedanta Resources, Bharti Telecom's planned stake build) changes everything, because the discount then reflects a claim ahead of minorities. Mark the 40-70% range unverified until computed.

Sources: <https://www.businesstoday.in/latest/corporate/story/tata-sons-listing-rbi-makes-its-stand-clear-again-asks-the-company-to-comply-567742-2026-11-17> · <https://www.angelone.in/news/market-updates/piramal-enterprises-shares-to-be-delisted-on-sep-23-shareholders-to-receive-1-1-allotment-in-piramal-finance> · <https://www.moneylife.in/article/vedanta-sets-1-may-2026-as-demerger-record-date-shareholders-to-receive-11-shares-in-four-new-entities/80266.html>

### How governance problems typically surface first in India (the order of signals)
`insight:governance-surfacing-sequence` · confidence: verified

In the severe/poor cases reviewed, outside parties found the problem years before the regulator ruled on it, and the signals tended to arrive in this order. (1) Financing and structure: promoter pledges rising, ICDs or 'general purpose corporate loans' to opaque entities (RHFL to ADAG shells, SEBI 2024; DHFL's 'Bandra Book', SEBI 2025: ~Rs 14,040 cr; Fortis ICDs 2017-18), listed assets securing group debt (Zee, Jaypee), thin float after relisting (Ruchi/Patanjali 2020). (2) Credit market: rating downgrades, CP/NCD rollovers failing, lender 'fraud' tags (SBI on RCom 2025; PNB on Srei 2022), or forged no-default letters (Gensol, 2025). (3) Gatekeepers: auditor qualifications or resignations, delayed accounts (Byju's FY21 ~18 months late; Deloitte quit Jun-2023), independent directors leaving, a forensic auditor reporting non-cooperation (Rajesh Exports, per SEBI's 3-Jun-2026 interim order). (4) Bank regulator signals: RBI divergences and refusal of a CEO's term (Yes Bank 2016-18), RBI special audits (Srei), supersession. (5) Outsiders: whistleblowers (Videocon 2016), investigative media (Cobrapost on DHFL 2019), short sellers (Hindenburg on Adani 2023, Viceroy on Vedanta 2025). The short-seller claims were largely not upheld by SEBI in Adani's case, so on their own they are prompts for diligence, not verdicts. (6) Regulators and agencies act last: SEBI interim orders, then ED/CBI, often 2-7 years later. Counter-example: Infosys (2019 whistleblower allegations not substantiated after an independent probe; stock recovered). Process rule: any one of items 1-3 means a deeper check; two together means exit or don't enter.

Sources: <https://www.moneylife.in/article/dhfls-bandra-book-scam-sebi-slaps-rs120-crore-fine-bans-4-wadhawans-2-others-for-diverting-rs14000-crore-loan/77969.html> · <https://www.business-standard.com/companies/news/rhfl-fund-diversion-case-5-year-market-ban-for-anil-ambani-24-others-124082300983_1.html> · <https://www.businesstoday.in/markets/stocks/story/bt-explainer-what-sebis-interim-order-against-rajesh-exports-and-its-promoter-reveals-534811-2026-06-04> · <https://business-standard.com/markets/news/sebi-bars-gensol-engineering-promoters-for-alleged-fund-diversion-125041501266_1.html> · <https://www.business-standard.com/markets/news/sebi-clears-adani-group-dismisses-hindenburg-allegations-125091801259_1.html>

### Family succession disputes: frequent, slow, and mostly a holdco-level risk if the listed companies are ring-fenced
`insight:succession-disputes-governance` · confidence: verified

Of the 43 group profiles reviewed, at least 10 had a public family or control dispute: Ambani (2002-05 split), Tata (Mistry ouster 2016, SC 2021; trustee split 2025-26), Birla-Lodha (Priyamvada will, 2004 onwards; Calcutta HC Dec-2023), Murugappa (2019-23, settled), Godrej (amicable split 2024), TVS (2020 partition; Venu Srinivasan family dispute open in Oct-2026), Kalyani (Hikal and Sulochana Kalyani will; SC mediator Jul-2026), Hinduja (2014 letter litigation; Gopichand died Nov-2025), Bajaj (old branch splits), and the Singh brothers vs. their spiritual-guru lenders. Pattern: disputes that stayed at the family holdco level and left listed companies' cash alone (Godrej, Murugappa, Tata) did little lasting harm to minorities. Where the dispute froze strategy or control (Birla-Lodha: ~20 years of litigation over Birla Corp and others) or touched listed boards (Tata-Mistry 2016; Kalyani-Hikal), it raised uncertainty and holdco discounts. Settlements take 3-20 years. A pre-announced split with listed companies untouched and a non-compete (Godrej 2024) is the good template. Signals: deaths of patriarchs without a public will, 'family arrangement' documents of disputed legal status (Hikal 1993-94; Hinduja 2014), trust structures with vague beneficiaries (TVS Holdings' VS Trust at 66.55%), and women heirs excluded from holdco boards (Murugappa). Investor read: price the dispute as a governance discount, not a business impairment, unless listed-company cash, board control or a forced stake sale is in play.

Sources: <https://www.businesstoday.in/latest/corporate/story/family-assets-dont-belong-to-one-individual-venu-srinivasans-family-says-no-settlement-has-been-reached-561153-2026-10-13> · <https://moneylife.in/article/kalyani-family-feud-sc-pushes-baba-kalyani-sister-sugandha-hiremath-towards-mediation-appoints-justice-l-nageswara-rao-as-mediator/81050.html> · <https://businesstoday.in/latest/corporate/story/127-year-old-godrej-empire-splits-adi-nadir-to-keep-listed-firms-jamshyd-smita-get-unlisted-cos-land-bank-427735-2024-05-01> · <https://business-standard.com/amp/companies/news/birla-lodha-battle-calcutta-hc-shrinks-priyamvada-birla-estate-s-reach-123121401093_1.html> · <https://gulfnews.com/business/markets/who-will-succeed-gopichand-hinduja-inside-the-battle-for-a-15-billion-empire-1.500333305>

### Judge governance history on conduct, not on final legal outcomes: Indian orders are often quashed, settled or delayed
`insight:regulator-outcomes-vs-conduct` · confidence: verified

Legal outcomes are poor proxies for how a promoter behaved, in both directions. Penalties quashed on appeal: SAT set aside SEBI's 2021 RPL manipulation penalty on Mukesh Ambani (Dec-2023) and a Rs 25 cr takeover penalty on the Ambani family (Jul-2023), citing SEBI's long delay; SAT quashed SEBI's 2021 insider-trading ban on Kishore Biyani (Dec-2023), even as Future Retail went into liquidation; the Supreme Court (Apr-2022) set aside insider-trading orders against PC Jeweller relatives. Settlements: Adani's MPS case was settled for ~Rs 1.48 cr (Sep-2026, no admission); the Sandesaras' criminal cases were quashed on a Rs 5,100 cr deposit (SC, Nov-2025), and the SC then told SEBI to close its case (2026). Dismissals: US DOJ charges against the Adanis were dismissed with prejudice (Aug-2026); SEBI found no violation on Hindenburg's related-party allegations (Sep-2025). Delay: Videocon-ICICI (FIR 2019), DHFL (CBI 2022), Yes Bank (2020) and Religare (2019) had no final criminal verdicts by Nov-2026; promoters got bail citing trial delay. Meanwhile, conduct is often visible directly in filings: ICDs to shells, collateral given for group debt, pledge cycles, auditor exits. Rules: (1) record regulator findings, interim orders, settlements and allegations as separate categories, which this library does; (2) a quashed penalty is not proof of good conduct, and an allegation is not proof of bad conduct; (3) for investing, the question is whether minority value was transferred, which filings can usually answer before the courts do.

Sources: <https://www.taxmann.com/post/blog/sat-quashes-sebis-order-imposing-penalty-on-mukesh-ambani-2-others-in-case-related-to-manipulative-trading/> · <https://www.outlookbusiness.com/news/sat-quashes-sebis-order-against-kishore-biyani-others-in-insider-trading-case> · <https://www.taxmann.com/post/blog/sc-sets-aside-insider-trading-orders-against-p-chand-jeweller/> · <https://www.moneylife.in/article/sebi-clears-vinod-adani-in-mps-case-gautam-adani-4-group-companies-settle-for-148-crore/81785.html> · <https://www.businesstoday.in/latest/economy/story/supreme-court-agrees-to-drop-criminal-proceedings-against-fugitive-sandesara-brothers-if-they-paid-rs-5100-crore-503463-2025-11-24>

## Group profiles

### Bajaj group (Rahul Bajaj family: Rajiv & Sanjiv Bajaj) — governance history
`person:group-bajaj` · flag: **clean** · confidence: verified · tickers: BAJAJ-AUTO, BAJFINANCE, BAJAJFINSV, BAJAJHLDNG, BAJAJHFL

Flag: CLEAN. The Rahul Bajaj branch (d. Feb-2022) runs Bajaj Auto (Rajiv) and Bajaj Finserv/Bajaj Finance/Bajaj Housing Finance (Sanjiv), with Bajaj Holdings & Investment as holdco. The 2007-08 demerger of old Bajaj Auto into Bajaj Auto, Bajaj Finserv and Bajaj Holdings is a textbook value-unlocking split (Bajaj Finance later a 100x+ compounder). No promoter pledging, high payouts: Bajaj Auto paid Rs 210/share for FY25 and Rs 150/share for FY26 plus a buyback of up to Rs 5,633 cr announced May-2026 (its second in two years), together ~100% of FY26 standalone PAT per one analysis. Bajaj Auto closed control of KTM AG (via Pierer Bajaj AG, ~74.9%) in Nov-2025 after KTM's insolvency -- a capital-allocation bet to monitor, not a governance breach. Regulatory blemish: RBI barred Bajaj Finance from lending under its eCOM and Insta EMI card products (Nov-2023) for KFS disclosure lapses; lifted May-2024. Bajaj Holdings trades at a large holdco discount despite dividends. Note: the Kamalnayan/Shekhar branch (Bajaj Electricals) and the Shishir/Kushagra branch (Bajaj Hindusthan, Bajaj Consumer) are separate groups with different records -- do not transfer this flag to them.

- **red flags:** RBI product ban Bajaj Finance 2023-24 (lifted); KTM rescue risk
- **good conduct:** 2008 demerger, buybacks (Bajaj Auto), no pledges

Sources:
- <https://www.businesstoday.in/amp/markets/stocks/story/bajaj-auto-q4-profit-jumps-34-announces-up-to-rs-5633-crore-buyback-rs-150-dividend-530164-2026-05-06>
- <https://www.kotakneo.com/news/market-news/bajaj-auto-q4-profit-buyback-dividend-fy26-share-rises/>
- <https://www.equentis.com/blog/bajaj-auto-strategic-continuity-and-shareholder-value/>
- <https://investors.bajajauto.com/ar25/wp-content/uploads/2025/07/BAL_Annual_Report_2025.pdf>

### Bharti group (Sunil Bharti Mittal) — governance history
`person:group-bharti` · flag: **clean** · confidence: verified · tickers: BHARTIARTL, BHARTIHEXA, INDUSTOWER

Flag: CLEAN (mostly-clean on structure). Bharti Airtel is controlled through Bharti Telecom (Bharti Enterprises ~50.56%, Singtel ~49.44%), which held ~40.47% of Airtel in Sep-2025; total promoter group ~50.3%. Minority record: no promoter pledging at Airtel; rights issues (2019 Rs 25,000 cr; 2021 Rs 21,000 cr partly paid) offered to all at the same price; AGR dues paid/managed without seeking a bail-out conversion; Bharti Hexacom IPO (2024) was an OFS by the government's TCIL, not the promoter. Singtel and promoter entity Indian Continent Investment have sold blocks (2025: ICIL ~3.43 cr shares for ~Rs 7,189 cr; Singtel ~0.8% for ~Rs 10,353 cr) -- secondary sales, not pledges. Legal record: the 2G spectrum case -- the Supreme Court (2015) quashed summons against Sunil Mittal; the special court acquitted all accused in Dec-2017. Airtel acquired control of Indus Towers (2024) after Vodafone's sell-down. Watch: Mittal's stated plan (2025-26) for Bharti Telecom to regain 51% of Airtel over a decade (~Rs 1 lakh cr at current prices) implies holdco leverage at Bharti Telecom; a 10-year leadership succession plan has been outlined publicly. Status Nov-2026: no regulator actions against promoters found.

- **red flags:** holdco leverage at Bharti Telecom to raise stake (future)
- **good conduct:** rights issues to all; no pledges; transparent block sales

Sources:
- <https://www.outlookbusiness.com/corporate/sunil-bharti-mittal-eyes-majority-control-comeback-at-bharti-airtel>
- <https://www.business-standard.com/companies/news/bharti-airtel-promoter-entity-icil-sells-3-43-cr-shares-for-7-189-cr-125112600215_1.html>
- <https://www.outlookbusiness.com/news/singtel-offloads-08-stake-in-bharti-airtel-for-10353-cr>
- <https://www.angelone.in/news/stocks/sunil-bharti-mittal-outlines-10-year-succession-plan-for-airtel-leadership>

### Burman family (Dabur; Eveready, Religare via family office) — governance history
`person:group-burman-dabur` · flag: **clean (Dabur); mostly-clean (Religare/Eveready takeovers)** · confidence: verified · tickers: DABUR, EVEREADY, RELIGARE

Flag: CLEAN (Dabur) / MOSTLY-CLEAN (family-office takeovers). Dabur India is professionally managed (family separated ownership from management in 1998), with no promoter pledging, consistent dividends and no regulator findings of diversion. The Burmans deploy family capital via Puran Associates/VIC Enterprises etc. into turnarounds: Eveready Industries (creeping acquisition and open offer in 2022 after the Khaitan group's lenders sold shares) and Religare Enterprises. Religare: after open-market purchases (Sep-2023, +5.27% on a 21.54% base) triggered an open offer for 26% at Rs 235/share (~Rs 2,116 cr), a prolonged fight followed with chairperson Rashmi Saluja (who opposed the offer; independent directors called the price low) and a counter-offer at Rs 275 by US investor Digvijay (Danny) Gaekwad that SEBI rejected; the open offer finally ran 27-Jan to 7-Feb-2025 with only ~0.07% tendered, Burmans gained control and Saluja was voted off (97% against, Feb-2025). An allegation: a Nov-2023 Mumbai police FIR in the Mahadev betting-app case reportedly named Gaurav Burman (and reports said Mohit Burman); Dabur stated they had no connection -- unproven, no charge found in this scan. Investor read: a disciplined promoter at the flagship; takeovers have been by open offer at regulated prices (minorities could exit).

- **allegations:** Mahadev FIR naming (denied, unproven)
- **good conduct:** professional management; open offers at SEBI price

Sources:
- <https://www.business-standard.com/amp/companies/news/burmans-rs-2-116-crore-open-offer-for-religare-gets-tepid-response-125021901159_1.html>
- <https://www.business-standard.com/markets/capital-market-news/religare-enterprises-surges-after-burman-family-secures-majority-control-125022100685_1.html>
- <https://www.business-standard.com/companies/news/religare-independent-directors-say-burmans-open-offer-price-is-low-125012300587_1.html>
- <https://www.angelone.in/news/others/rashmi-saluja-removed-director-religare-enterprises-after-shareholder-rejection>

### Godrej family (Godrej Industries Group / Godrej Enterprises Group) — governance history
`person:group-godrej` · flag: **clean** · confidence: verified · tickers: GODREJIND, GODREJCP, GODREJPROP, GODREJAGRO, ASTECLIFE

Flag: CLEAN. 127-year-old group; the family split amicably by a Family Settlement Agreement (30-Apr-2024, completed 18-Jul-2024): Adi and Nadir Godrej's side kept the listed Godrej Industries Group (Godrej Industries, Godrej Consumer Products, Godrej Properties, Godrej Agrovet, Astec Lifesciences); Jamshyd Godrej and Smita Godrej Crishna took unlisted Godrej & Boyce and the Vikhroli land bank, with a non-compete and brand-sharing arrangement. Promoters took 64.66% of Godrej Industries under the settlement. No promoter pledging; listed companies have not been used to fund family entities; succession was pre-announced (Pirojsha Godrej to succeed Nadir as GIG chair in Aug-2026). Points to watch: Godrej Industries is a holdco trading at a deep discount to its listed stakes; Godrej Properties raises equity often (QIPs) -- dilution, but at market prices; Astec Lifesciences losses. Lesson: a peaceful, pre-planned split with listed cos untouched is the good template versus litigated feuds (Ambani 2005, Birla-Lodha, TVS 2026). Status Nov-2026: no regulator orders found.

- **red flags:** holdco discount; frequent GPL equity raises
- **good conduct:** amicable 2024 split, no listed-entity value transfer

Sources:
- <https://businesstoday.in/latest/corporate/story/127-year-old-godrej-empire-splits-adi-nadir-to-keep-listed-firms-jamshyd-smita-get-unlisted-cos-land-bank-427735-2024-05-01>
- <https://www.dtnext.in/amp/story/news/business/realignment-of-share-in-godrej-entities-following-split-completed-statement-795683>
- <https://www.deccanherald.com/business/companies/godrej-family-split-who-gets-what-3002904>

### HCL group (Shiv Nadar, Roshni Nadar Malhotra) — governance history
`person:group-hcl-nadar` · flag: **clean** · confidence: verified · tickers: HCLTECH

Flag: CLEAN (HCL Tech) with a legacy blemish (HCL Infosystems). HCL Technologies (promoter ~60%) has been a high-payout company: quarterly dividends with a stated ~75%+ payout policy and occasional buybacks; no promoter pledging; no SEBI findings against promoters. Succession was handled in steps: Roshni Nadar Malhotra became chair of HCL Tech (2020), and by gift deeds of 6-Mar-2025 Shiv Nadar gave her 47% of promoter vehicles Vama Sundari Investments (Delhi) and HCL Corp (his stake 51% -> 4%; hers 10.33% -> ~57.3%), giving her voting control of ~44.3% of HCL Tech; SEBI exempted the open offer and total promoter holding stayed ~60.8%. Legacy blemish: HCL Infosystems (hardware/distribution) shrank into heavy losses through the 2010s, eroding its minority shareholders' value; it was eventually wound into the group (details unverified). HCL Tech's large IBM software IP purchase (2019, $1.8bn) was a capital-allocation debate, not a governance breach. Investor read: one of the cleaner promoter-led IT names; the payout policy is the key minority protection.

- **red flags:** HCL Infosystems value erosion (legacy)
- **good conduct:** high dividend payout; clean succession

Sources:
- <https://businesstoday.in/latest/corporate/story/hcl-succession-shiv-nadar-gifts-47-stake-roshni-nadar-malhotra-takes-majority-control-467282-2025-03-08>
- <https://www.freepressjournal.in/business/shiv-nadar-reshapes-hcls-future-with-major-stake-transfer-to-daughter>
- <https://www.angelone.in/news/market-updates/shiv-nadar-transfers-47-stake-in-hcl-group-to-roshni-nadar-malhotra>

### Infosys founders (Narayana Murthy, Nilekani et al.) — governance history
`person:group-infosys-founders` · flag: **clean** · confidence: verified · tickers: INFY

Flag: CLEAN. Infosys is the reference case for disclosure and minority treatment in Indian IT: founders/promoter group own only ~13%; no pledging; capital-allocation policy returns ~85% of free cash flow over 5 years via dividends and buybacks. Buybacks: 2017 (Rs 13,000 cr), 2019, 2021, 2022 and the Rs 18,000 cr tender at Rs 1,800/share approved 11-Sep-2025, in which the promoters chose not to participate (their stake rising slightly to ~13.4% as shares are extinguished). Governance episodes: (1) 2016-17 founder-board conflict over CEO Vishal Sikka, the Panaya acquisition and severance pay to ex-CFO Rajiv Bansal; Sikka resigned (Aug-2017); Nilekani returned as chairman; an external probe found no wrongdoing in Panaya. (2) Oct-2019 anonymous 'ethical employees' whistleblower letter alleged accounting manipulation by CEO Salil Parekh/CFO; the audit committee's independent probe (with law firm) found no evidence; the US SEC closed its inquiry (2020); stock fell ~16% in a day then recovered -- a whistleblower allegation not upheld. (3) SEBI settled insider-trading proceedings involving some employees (no promoter wrongdoing). Status Nov-2026: no open promoter governance issues; GST demand disputes are tax matters. Investor read: buyback decisions where promoters abstain are a strong signal of alignment.

- **allegations:** 2019 whistleblower (not substantiated)
- **good conduct:** 85% FCF return policy; buybacks; promoters skipped 2025 buyback

Sources:
- <https://www.business-standard.com/amp/markets/news/infosys-founders-skip-share-buyback-rs18000-crore-plan-125102200636_1.html>
- <https://www.businesstoday.in/markets/stocks/story/infosys-stock-in-focus-as-narayana-murthy-promoters-skip-rs-18000-crore-share-buyback-499241-2025-10-23>
- <https://www.indmoney.com/blog/stocks/infosys-buyback-promoters-not-participating>

### Mahindra group — governance history
`person:group-mahindra` · flag: **clean** · confidence: verified · tickers: M&M, M&MFIN, TECHM, MAHLIFE, MHRIL, MAHLOG, SWARAJENG

Flag: CLEAN. Promoter Mahindra family (Anand Mahindra, chairman) with professional management; Anish Shah became the first non-family group CEO/MD (2021). Listed: Mahindra & Mahindra, Mahindra & Mahindra Financial Services, Tech Mahindra, Mahindra Lifespace, Mahindra Holidays, Mahindra Logistics, Swaraj Engines (and others). No promoter pledging; dividends regular. The defining governance positive is the 2020-21 capital-allocation reset: the board rejected a ~$406 m fresh equity infusion into loss-making SsangYong (Apr-2020), and the group exited or shut SsangYong (sold to KG group 2022-23), GenZe, GippsAero and others -- ~15 underperforming businesses per a 2026 report (single-source). Tech Mahindra's 2009 rescue of fraud-hit Satyam is a legacy positive. Blemishes: past value destruction from the 2010 SsangYong purchase and international ventures; Mahindra Finance faced an RBI bar on outsourced recovery (Sep-2022, lifted Dec-2022) and a ~Rs 150 cr fraud at a Mizoram branch (2023, unverified magnitude). Status Nov-2026: no open governance issues found; the group is a reference case for 'killing losers' discipline.

- **red flags:** legacy international losses; M&M Finance operational lapses
- **good conduct:** refused to throw good money after bad (SsangYong); exits of ~15 businesses

Sources:
- <https://www.businesstoday.in/latest/corporate/story/from-capital-allocation-discipline-to-bold-bets-how-anish-shah-steered-mahindra-group-over-last-5-years-523945-2026-04-03>
- <https://www.business-standard.com/article/automobile/m-m-board-rejects-plan-to-pump-in-fresh-equity-in-ssangyong-motor-120040400054_1.html>
- <https://business-standard.com/article/companies/mahindra-resets-its-playbook-for-international-business-ventures-120071901016_1.html>

### Murugappa group — governance history
`person:group-murugappa` · flag: **clean** · confidence: verified · tickers: CHOLAFIN, CHOLAHLDNG, TIINDIA, CUMI, COROMANDEL, EIDPARRY, CGPOWER, SHANTIGEAR, WENDT

Flag: CLEAN. 120-year-old Chennai family group run through Ambadi Investments (unlisted holdco) and professional CEOs. Listed: Cholamandalam Investment & Finance, Cholamandalam Financial Holdings, Tube Investments of India, Carborundum Universal, Coromandel International, EID Parry, CG Power (acquired by TII in 2020 after the Thapar-era fraud there), Shanthi Gears, Wendt. Minority record: no meaningful promoter pledging, conservative leverage, consistent dividends; the CG Power rescue (TII infused capital, cleaned up books after the previous management's undisclosed liabilities and RPTs) is a positive governance case that created large value for TII holders. Main blemish: a 2019-2023 family dispute -- Valli Arunachalam (daughter of late chairman M.V. Murugappan) sought an Ambadi board seat; family policy of no women on the holdco board drew criticism. Settled out of court Aug-2023; the family said the settlement did not involve the listed companies. Holdco structure (Cholamandalam Financial Holdings) trades at a discount. Status Nov-2026: no regulator orders found; a group widely regarded as a governance benchmark among Indian family groups.

- **red flags:** 2019-23 family dispute (settled, outside listed cos); holdco discount
- **good conduct:** CG Power cleanup; conservative leverage; professional management

Sources:
- <https://business-standard.com/companies/news/murugappa-group-resolves-longstanding-family-dispute-strikes-deal-123082000331_1.html>
- <https://www.deccanherald.com/india/tamil-nadu/murugappa-family-reaches-agreement-with-valli-arunachalam-2654253>
- <https://businesstoday.in/latest/corporate/story/murugappa-family-valli-arunachalam-end-dispute-envisaged-to-bring-amity-maintain-goodwill-394852-2023-08-21>

### Wipro / Azim Premji — governance history
`person:group-wipro-premji` · flag: **clean** · confidence: single-source · tickers: WIPRO

Flag: CLEAN. Wipro (promoter group ~72-73%, much of it held for the Azim Premji Foundation's endowment) has a long record of repeated buybacks (2016-2023; the 2023 one ~Rs 12,000 cr -- figures single-source from memory, verify) and dividends, no promoter pledging and no SEBI findings against promoters. The high promoter holding means tender-offer buybacks largely return cash to the promoter/foundation, and Wipro has occasionally been near the 75% MPS ceiling -- a structural, not ethical, issue. Allegations dismissed: an NGO ('India Awake for Transparency') filed multiple complaints alleging Premji transferred assets of three group companies improperly; the Karnataka High Court dismissed a petition under the RBI Act as 'abuse of process' (18-Jan-2021), quashed two private complaints against Premji and his wife, imposed Rs 10 lakh costs for repetitive petitions (Feb-2021), and later convicted two NGO representatives of contempt -- a case where allegations against a promoter failed. Capital-allocation debates: Capco acquisition (2021, $1.45bn) and long underperformance vs. TCS/Infosys; CEO turnover. Premji's philanthropy (pledged equity worth ~$21bn to the foundation, 2019) separated economic interest from the family. Status Nov-2026: Rishad Premji chairman; no open governance issues found.

- **allegations:** NGO complaints quashed by Karnataka HC
- **good conduct:** repeated buybacks; dividends; foundation ownership

Sources:
- <https://www.livelaw.in/news-updates/karnataka-high-court-10-lakh-cost-for-multiple-petitions-against-azim-premjit-170255>
- <https://www.livelaw.in/news-updates/karnataka-high-court-rbi-azim-premji-private-complaint-india-awake-for-transparency-168664>
- <https://www.thenewsminute.com/article/karnataka-hc-convicts-two-filing-repeated-cases-against-wipro-azim-premji-159917>

### Aditya Birla Group (Kumar Mangalam Birla) — governance history
`person:group-aditya-birla` · flag: **mostly-clean** · confidence: verified · tickers: GRASIM, HINDALCO, ULTRACEMCO, ABCAPITAL, ABFRL, ABLBL, IDEA, ABSLAMC, CENTURYPLY

Flag: MOSTLY-CLEAN (governance) with poor capital-allocation episodes. Listed: Grasim (holdco + VSF/chemicals + Birla Opus paints), UltraTech, Hindalco (Novelis), Aditya Birla Capital, ABFRL and demerged Aditya Birla Lifestyle Brands (2025), ABSL AMC, Vodafone Idea (co-promoter). No fraud findings or promoter pledging; dividends regular. Concerns are about capital allocation: (1) Vodafone Idea (2018 merger) destroyed enormous value; after AGR dues ruling, KM Birla offered (2021) to hand his stake to government rather than infuse more; government converted dues to become largest holder; ABG holds ~9.5%. In late 2025/2026 the Cabinet froze ~Rs 87,695 cr AGR dues with repayment from FY32 (later reassessed lower), and ABG committed ~Rs 4,730 cr via warrants (May-2026; Rs 1,183 cr received Jun-2026, single-source). (2) Grasim deploys cash from cyclical businesses into new ventures (paints, B2B e-commerce) -- shareholders bear a conglomerate/holdco discount. (3) Hindalco's big leveraged Novelis buys (2007, Aleris 2020). Good conduct: clean ABCL-ABFL merger (2024), ABFRL demerger, UltraTech's acquisitions largely accretive. Status Nov-2026: no regulator actions found; key risk is Vi funding calls.

- **red flags:** Vi value destruction; cross-subsidy from Grasim cash to new bets; holdco discount
- **good conduct:** no pledges; clean mergers/demergers

Sources:
- <https://www.outlookbusiness.com/corporate/vodafone-idea-gets-new-agr-relief-as-cabinet-freezes-87695-cr-dues-till-fy32>
- <https://www.outlookbusiness.com/corporate/agr-relief-a-turning-point-for-vodafone-idea-says-kumar-mangalam-birla>
- <https://www.business-standard.com/companies/news/govt-freezes-vodafone-idea-agr-dues-repayment-from-fy32-125123101064_1.html>

### CK Birla group — governance history
`person:group-ck-birla` · flag: **mostly-clean** · confidence: single-source · tickers: ORIENTELEC, HIL, BSOFT, ORIENTPPR

Flag: MOSTLY-CLEAN. Chandrakant Birla's group (an older branch of the Birla family). Listed: Orient Electric, HIL (Birla Aerocon, roofing), Birlasoft, Orient Paper & Industries, and formerly Orient Cement. Orient Cement sale (Oct-2024): Ambuja Cements (Adani) agreed to buy 46.8% at Rs 395.40/share (~Rs 8,100 cr, ~12% premium to prior close), triggering a mandatory 26% open offer to public shareholders at the same price; the letter of offer was delayed to May-2025 pending approvals -- minorities received the same price as promoters (good conduct). No regulator enforcement findings against the group were found in this scan; group companies are mid-caps with moderate leverage and no notable promoter pledges. Birlasoft has had CEO churn and the group has faced questions on sub-scale businesses (Orient Paper), but not on value transfers. Confidence: single-source for most items beyond the Orient Cement deal; verify SAST pledges and RPT notes before relying.

- **red flags:** none major found; sub-scale businesses
- **good conduct:** Orient Cement exit with open offer at same price

Sources:
- <https://business-standard.com/companies/news/adani-backed-ambuja-to-acquire-46-8-stake-in-orient-cement-for-rs-8-100-cr-124102200224_1.html>
- <https://orientcement.com/wp-content/uploads/2024/10/October-22-2024-Public-Announcement.pdf>
- <https://orientcement.com/wp-content/uploads/2025/05/May-20-2025-Letter-of-Offer.pdf>

### Dalmia Bharat group (Jai Hari & Puneet Dalmia) — governance history
`person:group-dalmia` · flag: **mostly-clean** · confidence: verified · tickers: DALBHARAT, DALMIASUG

Flag: MOSTLY-CLEAN (one long-running quid-pro-quo allegation). Dalmia Bharat (cement; consolidated subsidiaries Dalmia Cement (Bharat) and earlier OCL India) and Dalmia Bharat Sugar. Listed-company record: periodic simplification (2018-19 merger of Odisha Cement and the holdco into Dalmia Bharat), buybacks/dividends, no promoter pledging; aggressive capacity expansion via IBC bids (lost Jaiprakash Associates to Adani, 2025-26; acquired Murli Industries and parts of Binani). Allegation: the 2011 CBI case in the Y.S. Jagan Mohan Reddy disproportionate-assets matter alleges Dalmia Cement invested ~Rs 95 cr in Bharathi Cement in return for limestone leases from the Andhra Pradesh government; ED provisionally attached Reddy's shares (~Rs 27.5 cr) and Dalmia Cement land (ED value ~Rs 377 cr; DCBL said ~Rs 793 cr) on 31-Mar-2025; the PMLA Appellate Tribunal partly allowed DCBL's appeal, cutting attributable proceeds of crime from ~Rs 793 cr to ~Rs 92.5 cr; ED reportedly released attached land on 21-Apr-2026 (secondary source). This is an unproven criminal allegation 15 years old; no conviction. Older Dalmia family history (Ramkrishna Dalmia's 1950s conviction; the separate Sanjay Dalmia/GHCL and Vishnu Hari Dalmia branches) should not be conflated with this group. Investor read: operating governance acceptable; political-licensing risk in mining-heavy businesses.

- **allegations:** CBI 2011 / ED 2025 Jagan Reddy quid-pro-quo (pending; proceeds reduced by tribunal)
- **good conduct:** structure simplification; no pledges

Sources:
- <https://www.businesstoday.in/india/story/ed-attaches-jagan-reddys-shares-worth-rs-275-crore-land-in-14-year-old-money-laundering-case-472535-2025-04-18>
- <https://www.thestatesman.com/india/ed-attaches-assets-of-jagan-mohan-reddy-dalmia-cements-in-14-year-old-money-laundering-case-1503421910.html>
- <https://www.livelawbiz.com/pmla/pmla-tribunal-reduces-alleged-proceeds-of-crime-from-793-crore-to-9252-crore-in-dalmia-cement-case-linked-to-ys-jagan-mohan-reddy-526277>
- <https://www.angelone.in/news/stocks/dalmia-bharat-share-price-in-focus-as-ed-releases-attached-properties-of-subsidiary-dcbl>

### OP Jindal family groups (JSW / Sajjan; JSPL / Naveen; Jindal Stainless / Ratan) — governance history
`person:group-jindal` · flag: **mostly-clean (JSW, JSL); mixed (JSPL)** · confidence: single-source · tickers: JSWSTEEL, JSWENERGY, JSWINFRA, JSWHL, JSWCEMENT, JINDALSTEL, JSL, JINDALSAW

Flag: MOSTLY-CLEAN (JSW, Jindal Stainless) / MIXED (JSPL). OP Jindal's sons run separate groups. JSW (Sajjan Jindal): JSW Steel, JSW Energy, JSW Infrastructure (IPO 2023), JSW Cement (IPO 2025), JSW Holdings. Record: aggressive debt-funded growth incl. IBC buys (Bhushan Power & Steel -- the Supreme Court ordered liquidation in May-2025, recalled it, then upheld JSW's Rs 19,700 cr plan on 26-Sep-2025); recurring material RPTs with promoter-group firms (JSW Energy, BMM Ispat) put to shareholder vote; historic promoter pledges at JSW Steel (pledge releases ~Rs 1,150 cr in 2019; ~11.7% of promoter holding pledged per a dated aggregator snapshot); a 2017 controversy over JSW group loans to a loss-making entity co-owned by Sajjan Jindal's wife (single-source). JSPL (Naveen Jindal): coal-block allocation cases -- a special CBI court took cognisance and summoned Naveen Jindal and ex-coal secretary P.C. Parakh (Jun-2026) in the Gare Palma IV/1 case; the Supreme Court stayed that cognisance order (Jul-2026); separate ED PMLA case over Amarkonda Murgadangal block pending. JSPL deleveraged sharply 2017-2022 via asset sales (Oman plant, Jindal Power to promoter entity -- a related-party sale that drew valuation questions). Jindal Stainless (Ratan/Abhyuday Jindal): JSL-JSHL merger (2023) simplified structure; turned around after a 2014-17 debt crisis. Allegations are not convictions.

- **red flags:** material RPTs with promoter cos; past pledges; JSPL coal cases; Jindal Power sale to promoter
- **good conduct:** JSPL deleveraging; JSL structure simplification

Sources:
- <https://www.businesstoday.in/latest/corporate/story/supreme-court-reverses-order-allows-jsw-steel-to-acquire-bhushan-steel-in-rs-20000-cr-deal-495844-2025-09-26>
- <https://www.livelawbiz.com/top-stories/coal-block-allocation-case-supreme-court-stays-cognizance-order-against-former-coal-secretary-pc-parakh-jindal-steel-542246>
- <https://www.businesstoday.in/amp/india/story/delhi-court-summons-naveen-jindal-former-coal-secretary-pc-parekh-534651-2026-06-03>
- <https://business-standard.com/article/companies/jsw-steel-promoter-companies-release-pledged-shares-worth-rs-1-150-crore-119091901010_1.html>
- <https://www.business-standard.com/article/companies/jsw-loans-to-loss-making-entity-co-owned-by-sajjan-jindal-s-wife-draw-ire-117062800255_1.html>
- <https://nsearchives.nseindia.com/corporate/amartiwari_03072025233952_Notice_of_AGM.pdf>

### Piramal group (Ajay Piramal family) — governance history
`person:group-piramal` · flag: **mostly-clean** · confidence: verified · tickers: PIRAMALFIN, PPLPHARMA

Flag: MOSTLY-CLEAN (governance) with an aggressive deal/capital-allocation record. Ajay Piramal is a serial asset trader: sold the domestic formulations business to Abbott (2010, ~$3.7bn), traded a Vodafone India stake (2011-14), took and exited a Shriram group stake, then pivoted Piramal Enterprises (PEL) into real-estate wholesale lending (2014-2019) -- a concentrated book that hurt after IL&FS (2018-19). PEL acquired DHFL via IBC (2021, ~Rs 34,250 cr plan), giving a large retail book plus legacy recoveries. Structure changes: pharma vertically demerged into Piramal Pharma (2022; 4 PPL shares per PEL share); PEL merged into wholly owned Piramal Finance effective 16-Sep-2025 (1:1 swap; PEL delisted, Piramal Finance listed), with Anand Piramal as chair. No promoter pledging; no SEBI/ED findings against promoters found. Points to watch: frequent restructurings (each one resets comparables), legacy wholesale write-downs, alternate-investment-fund (AIF) structures flagged by RBI in 2023 (evergreening rules), and promoter-group real-estate (Piramal Realty, unlisted) interactions with the lender. Good conduct: demergers gave mirror shareholding; buybacks/dividends from PEL historically; rights issues offered to all. Status Nov-2026: Piramal Finance is the listed lending entity; no open governance actions found.

- **red flags:** concentrated wholesale RE lending; frequent restructurings; AIF exposure (RBI 2023)
- **good conduct:** mirror demergers; no pledges

Sources:
- <https://www.business-standard.com/companies/news/anand-piramal-appointed-chairman-piramal-finance-125092401236_1.html>
- <https://www.angelone.in/news/market-updates/piramal-enterprises-shares-to-be-delisted-on-sep-23-shareholders-to-receive-1-1-allotment-in-piramal-finance>
- <https://bsppd.business-standard.com/article/companies/nclt-approves-the-demerger-of-piramal-enterprises-pharma-business-122081300024_1.html>

### Reliance group (Mukesh Ambani) — governance history
`person:group-reliance-mukesh` · flag: **mostly-clean** · confidence: verified · tickers: RELIANCE, JIOFIN, NETWORK18, TV18BRDCST, HATHWAY, DEN, JUSTDIAL, ALOKINDS

Flag: MOSTLY-CLEAN. Reliance Industries (promoter ~50%) is the core; subsidiaries Jio Platforms and Reliance Retail were funded with ~$25bn+ of strategic/PE equity (2020) and a Rs 53,124 cr rights issue (2020). No promoter pledging; Jio Financial Services was demerged 1:1 (2023), a clean value-distribution. Regulatory record: SEBI's 2007 RPL share-sale case -- SEBI ordered disgorgement (2017) and in Jan-2021 fined RIL Rs 25 cr and Mukesh Ambani Rs 15 cr for manipulative trading; SAT quashed the 2021 penalty order (Dec-2023) and separately set aside a Rs 25 cr takeover-code penalty on the Ambani family (Jul-2023) citing SEBI's inordinate delay; a report says the Supreme Court later dismissed SEBI's appeal (date unverified). Other concerns: decades of 'opaque structure' criticism (layers of promoter entities), large RPT flows between RIL and subsidiaries, minority buy-outs at subsidiary level (Reliance Retail capital-reduction exit for minorities, 2023), KG-D6 cost-recovery dispute with the government (unresolved; figures not verified here), and the Network18/media group's long losses. Positives: consistent dividends, bonus issues, debt-reduction promises largely met (net-debt-free claim 2020, later re-levered). Status Nov-2026: Jio Platforms IPO reported for Oct-2026 with an RIL-shareholder reservation (one source lists a 21-23 Oct issue at Rs 1,065-1,119; others say H2FY27 -- unconfirmed); watch whether IPO pricing and listing of Reliance Retail treat RIL holders fairly (holdco discount risk).

- **red flags:** 2007 RPL case (penalties later quashed by SAT); opaque promoter layers; subsidiary-level value capture
- **good conduct:** JFS demerger; rights issue at discount to all; no pledges; shareholder reservation in Jio IPO

Sources:
- <https://www.moneylife.in/article/sat-sets-aside-sebi-order-imposing-rs25-crore-on-ambani-family-and-reliance-promoter-entities/71523.html>
- <https://www.taxmann.com/post/blog/sat-quashes-sebis-order-imposing-penalty-on-mukesh-ambani-2-others-in-case-related-to-manipulative-trading/>
- <https://www.devdiscourse.com/article/law-order/3153245-supreme-court-upholds-sat-order-in-ril-trading-case>
- <https://www.kotakneo.com/ipo/jio-ipo/>
- <https://www.mstock.com/articles/reliance-jio-ipo>

### TVS group (Venu Srinivasan branch and other TVS families) — governance history
`person:group-tvs` · flag: **mostly-clean** · confidence: verified · tickers: TVSMOTOR, TVSHLTD, SUNDARMFIN, TVSSCS, SUNCLAY

Flag: MOSTLY-CLEAN. The wider TVS family divided the group in 2020 (TVS Motor, Sundaram-Clayton and holdco TVS Holdings to Venu Srinivasan's branch; Sundaram Finance, Lucas-TVS, Sundram Fasteners etc. to other branches) -- an orderly partition with no listed-company value transfer reported. TVS Motor has been a strong compounder with low promoter pledging and steady dividends; Sundaram Finance is a conservative lender with a long clean record. Capital allocation debates: TVS Motor's overseas bets (Norton, Swiss e-bike brands) and Sundaram-Clayton/TVS Holdings restructuring that created a holdco layer. New 2026 risk: an open ownership dispute inside Venu Srinivasan's family. Venu and son Sudarshan Venu say a March-2024 MoU split the businesses; wife Mallika Srinivasan (TAFE chair) and daughter Lakshmi Venu said on 13-Oct-2026 that 'no economic settlement has been reached', and Lakshmi sent a partition notice. TVS Holdings disclosed Sudarshan as a significant beneficial owner via trust structures; the VS Trust holds 66.55% of TVS Holdings. No regulator findings of wrongdoing. Investor read: governance of operating companies is good; the dispute is a control/succession overhang at the holdco level that could affect board stability or force stake monetisation.

- **red flags:** 2026 father-daughter ownership dispute; holdco layering
- **good conduct:** orderly 2020 partition; no pledges

Sources:
- <https://www.businesstoday.in/latest/corporate/story/family-assets-dont-belong-to-one-individual-venu-srinivasans-family-says-no-settlement-has-been-reached-561153-2026-10-13>
- <https://www.businesstoday.in/latest/corporate/story/tvs-succession-a-question-of-who-gets-what-565459-2026-11-03>
- <https://www.outlookbusiness.com/corporate/tvs-groups-ownership-question-is-far-from-settled>
- <https://business-standard.com/article/companies/family-owned-tvs-group-changes-ownership-model-splits-businesses-120121001117_1.html>

### Tata group (Tata Sons / Tata Trusts) — governance history
`person:group-tata` · flag: **mostly-clean** · confidence: verified · tickers: TCS, TMPV, TATASTEEL, TITAN, TATAPOWER, TATACONSUM, TRENT, INDHOTEL, VOLTAS, TATACOMM, TATAELXSI, TATACHEM, TATAINVEST, TATATECH

Flag: MOSTLY-CLEAN. Tata Sons (unlisted holdco; Tata Trusts ~66%, Shapoorji Pallonji ~18%) controls ~25+ listed firms. Minority record is broadly good: no promoter pledging at listed cos, arm's-length intra-group mergers (Tata Steel absorbing listed subsidiaries; Tata Consumer/Tata Coffee, Tata Motors-TML DVR schemes), and TCS has run repeated buybacks plus high dividend payouts. Tata Motors demerged into passenger (TMPV) and commercial (TMCV) entities in late 2025 with 1:1 mirror shareholding. Blemishes: (1) the Oct-2016 ouster of chairman Cyrus Mistry; NCLAT reinstated him (Dec-2019) but the Supreme Court upheld Tata Sons (Mar-2021) -- legally clean but exposed concentrated trust control; (2) capital allocation misses -- Corus (2007), Tata Teleservices losses and the DoCoMo arbitration, Air India (2022) and its AI171 crash (Jun-2025); (3) 2025-26 trustee infighting: Mehli Mistry not reappointed as trustee (Oct-2025) after a split; Noel Tata vs Venu Srinivasan/Vijay Singh disagreements in 2026. Current status (Nov-2026): RBI classified Tata Sons as an upper-layer NBFC (2022), missed the Sep-30-2025 listing deadline, and on 17-Nov-2026 RBI reiterated it must comply (list); Noel Tata-led trusts resist, SP group pushes for an IPO. A listing would expose the holdco discount at Tata Investment Corp and give SP group an exit. Investor read: listed-company minority treatment strong; holdco/trust politics are the key risk, not fraud.

- **red flags:** trust-level disputes, Mistry ouster, legacy capital misallocation
- **good conduct:** TCS buybacks, no pledges, clean demergers
- **watch:** Tata Sons listing decision; SP group exit; trust board composition

Sources:
- <https://www.businesstoday.in/latest/corporate/story/tata-sons-listing-rbi-makes-its-stand-clear-again-asks-the-company-to-comply-567742-2026-11-17>
- <https://www.moneylife.in/article/rbi-tells-tata-sons-to-comply-with-listing-rules-putting-public-float-back-at-centre-of-board-dispute-reports/82199.html>
- <https://www.businesstoday.in/latest/corporate/story/tata-sons-listing-explained-why-the-holding-company-was-required-to-go-public-556273-2026-09-18>
- <https://www.freepressjournal.in/business/power-shift-in-tata-trusts-noel-tata-led-faction-ousts-ratan-tatas-confidant-mehli-mistry-amid-internal-rift>
- <https://www.outlookbusiness.com/in-depth/another-mistry-fallout-at-tata-what-mehlis-ouster-means-for-the-trusts>

### Adani group (Gautam Adani) — governance history
`person:group-adani` · flag: **mixed** · confidence: verified · tickers: ADANIENT, ADANIPORTS, ADANIPOWER, ADANIGREEN, ADANIENSOL, ATGL, AMBUJACEM, ACC, NDTV, AWL

Flag: MIXED. Ports-to-power conglomerate built with heavy debt and concentrated promoter holdings (60-75%). Hindenburg (24-Jan-2023) alleged stock manipulation via Mauritius-linked FPIs and undisclosed related parties; ~$150bn market cap fell, the Rs 20,000 cr FPO was withdrawn. Regulator record: the Supreme Court (Jan-2024) declined an SIT/CBI probe and left it to SEBI; SEBI (Sep-2025) dismissed the Hindenburg related-party/fund-routing allegations (Adicorp, Milestone, Rehvar loans) finding no violation; SEBI's minimum-public-shareholding case ended (Sep-2026) with Vinod Adani cleared and Gautam Adani plus four group companies settling for ~Rs 1.48 cr (settlement = no admission). Still open: SEBI's probe of whether 13 overseas FPIs were genuine public holders -- SEBI rejected all 13 settlement applications (Aug-2026). US: DOJ bribery indictment (Nov-2024) dismissed with prejudice (Aug-2026); SEC civil case moved to proposed final judgments with ~$18 m penalties (May-2026, verify final). Good conduct post-2023: promoters prepaid ~$2.15bn of share-backed loans (pledges in Adani Ports to ~0, Adani Power ~25% -> ~1%), GQG and other long-only investors came in, Adani exited Adani Wilmar (2025). Growth continues via acquisitions (Ambuja/ACC, Orient Cement, Jaiprakash Associates via IBC 2026). Risks: high capex and debt, related-party flows among group cos, valuation, political-proximity perception. Investor read: the worst allegations were not upheld by Indian or US authorities, but disclosure/ownership opacity remains the core issue.

- **regulator findings:** SEBI Sep-2025: no violation on Hindenburg RPT allegations; MPS case settled Sep-2026; FPI probe open
- **allegations:** Hindenburg 2023 (largely not upheld); US DOJ (dismissed 2026)
- **good conduct:** pledge prepayment 2023; promoter stake increases

Sources:
- <https://www.business-standard.com/markets/news/sebi-clears-adani-group-dismisses-hindenburg-allegations-125091801259_1.html>
- <https://www.moneylife.in/article/sebi-clears-vinod-adani-in-mps-case-gautam-adani-4-group-companies-settle-for-148-crore/81785.html>
- <https://businesstoday.in/markets/stocks/story/adani-linked-funds-sebi-rejects-settlement-bids-says-report-550823-2026-08-24>
- <https://www.moneylife.in/article/us-court-dismisses-criminal-fraud-charges-against-gautam-adani-sagar-adani-and-vneet-jaain/81308.html>
- <https://www.businesstoday.in/latest/corporate/story/us-authorities-moving-to-end-fraud-prosecution-against-gautam-adani-report-531585-2026-05-14>
- <https://www.outlookbusiness.com/news/adani-says-2-15-billion-share-backed-loans-paid-off-only-operating-co-liabilities-remain-news-274298>

### Emami group (R.S. Agarwal & R.S. Goenka families) — governance history
`person:group-emami` · flag: **mixed** · confidence: verified · tickers: EMAMILTD, EMAMIPAP, EMAMIREAL

Flag: MIXED. Kolkata group whose cash-rich FMCG company Emami Ltd (Navratna, Boroplus, Zandu) has been the collateral behind diversification into cement, power, paper, real estate, edible oils and hospitals. Pledge cycle: promoter pledges on Emami Ltd shares rose through 2016-2018; in Feb-2019 the Agarwal and Goenka families sold ~10% of Emami for ~Rs 1,600 cr explicitly to pare debt of other group companies (Emami Cement, Emami Power) and release pledges; Emami Cement was later sold to Nuvoco (2020, ~Rs 5,500 cr) to deleverage the group. Pledges have not gone away: an aggregator shows ~16% of promoter holdings pledged in 2026, and a BSE disclosure records a fresh pledge of ~2.16 cr shares (~4.95% of equity) by promoter entity Diwakar Finvest on 9-Jan-2026 (verify lender on SAST). At the listed-company level Emami has paid steady dividends and run buybacks (2022, 2023) and no regulator findings of diversion were found. Emami Realty (listed) is loss-making and leveraged. Investor read: Emami Ltd's own operations and minority treatment are acceptable; the risk channel is promoter-level borrowing against Emami shares to fund unlisted/other ventures -- a repeating pattern (2018-19, again 2026). Track pledge % quarterly.

- **red flags:** recurring promoter pledges for group ventures; 2019 stake sale to repay group debt
- **good conduct:** buybacks, dividends; deleveraging via Emami Cement sale

Sources:
- <https://business-standard.com/article/companies/emami-promoters-sell-10-stake-to-pare-group-debt-pledged-shares-119021801092_1.html>
- <https://bsmedia.business-standard.com/_media/bs/data/announcements/bse/16012026/1C7FB2CA_9A60_418E_B357_3F9DBACD4EED_102322.pdf>
- <https://trendlyne.com/equity/share-holding/374/EMAMILTD/latest/emami-ltd>
- <https://www.emamiltd.in/wp-content/uploads/2026/01/13233708/shp-as-on-31dec2025.pdf>

### GMR group (G.M. Rao family) — governance history
`person:group-gmr` · flag: **mixed** · confidence: single-source · tickers: GMRAIRPORT, GMRP&UI

Flag: MIXED. Airports-energy-infrastructure group (Delhi and Hyderabad airports; Goa, overseas airports). Survived a 2013-2020 leverage crisis via asset sales and strategic equity (Tata-GIC-SSG 2019 deal, Groupe ADP buying 49% of GMR Airports Ltd for ~Rs 10,780 cr in 2020). Restructuring: 2021 demerger of non-airport businesses (energy, urban infra, EPC) into GMR Power & Urban Infra (GPUIL), leaving GMR Airports Infrastructure (GIL) as an airport pure-play; 2024 merger of GIL with unlisted GMR Airports Ltd to simplify the structure and settle most GPUIL-related contingent liabilities. Minority concerns: long history of the listed holdco supporting loss-making energy subsidiaries through loans/guarantees; complex multi-layer structure with holdco discount; persistently high promoter encumbrance -- an aggregator summary of a Nov-2025 filing put ~50.6% of promoter shares in GPUIL as encumbered (verify on NSE SAST). No SEBI/ED fraud findings against the promoters were found in this scan; the Maldives airport cancellation (2012) and Indonesian coal assets were capital-allocation losses. Positives: airport-business value has been preserved and grown; strategic partners came in at arm's length prices; promoter has not been accused of siphoning. Status Nov-2026: GIL is the main listed vehicle; watch encumbrance, RPT approvals between GPUIL and GIL, and dilution via preferential/ convertible issues to partners.

- **red flags:** high encumbrance at GPUIL; inter-group support for energy losses; layered holdcos
- **good conduct:** demerger 2021; merger 2024 simplification; strategic equity at arm's length

Sources:
- <https://www.business-standard.com/article/companies/gmr-infra-to-demerge-energy-transport-businesses-list-airports-separately-120082701491_1.html>
- <https://www.constructionworld.in/transport-infrastructure/aviation-and-airport-infra/gmr-airports-infrastructure-merger-streamlines-corporate-structure/59773>
- <https://filingreader.com/news-wire/mumbai/2025-11-14/gmr-enterprises-pledges-shares-in-gmr-power-and-urban-infra>
- <https://www.businessinsider.in/gmr-ropes-in-tata-group-gic-ssg-capital-as-investors-in-its-airports-business-in-a-restructuring-deal-valued-at-3-2-billion/articleshow/68594334.cms>

### Hinduja group (Hinduja brothers / IIHL) — governance history
`person:group-hinduja` · flag: **mixed** · confidence: verified · tickers: INDUSINDBK, ASHOKLEY, HGS, GULFOILLUB, RELCAPITAL

Flag: MIXED. London/Geneva-based family controlling Ashok Leyland, Gulf Oil Lubricants, Hinduja Global Solutions (HGS) and, through IndusInd International Holdings (IIHL, Mauritius), IndusInd Bank; IIHL also won Reliance Capital in IBC (Rs 9,650 cr plan, 2024-25). Family: a 2014 letter said assets in any brother's name belonged to all four; Srichand Hinduja's side sued (UK High Court, 2020) to declare it void; a truce was announced (2022); Srichand died May-2023 and chairman Gopichand died 4-Nov-2025, with succession reports conflicting (Prakash/Ashok vs. third-generation Dheeraj/Sanjay). A Geneva court (Jun-2024) convicted four family members of exploiting domestic staff (acquitted of trafficking) -- personal, not listed-company, conduct. Listed-company issues: IndusInd Bank's derivatives-accounting discrepancy (~Rs 1,960 cr, disclosed Mar-2025), plus ~Rs 172.6 cr microfinance interest wrongly booked as fee income; CEO Sumant Kathpalia and deputy CEO resigned (Apr-2025); first quarterly loss in ~two decades (Q4FY25, ~Rs 2,328 cr); SEBI's ex-parte interim order (28-May-2025) barred the two ex-executives for alleged insider trading -- findings against executives, not the promoter; IIHL said it remained committed to support. Earlier, the 2018-19 IL&FS-linked and loan-quality divergences at IndusInd drew RBI scrutiny. HGS: how the ~Rs 8,000 cr healthcare-BPO sale proceeds (2021) were deployed (NXTDIGITAL merger, treasury) drew minority questions (unverified detail). Ashok Leyland is professionally run with no promoter pledging. Status Nov-2026: promoter control intact; watch IIHL leverage for Reliance Capital and any family realignment after Gopichand's death.

- **regulator findings:** SEBI interim order 2025 vs IndusInd ex-CEO/deputy (insider trading)
- **red flags:** IndusInd accounting lapse 2025; family litigation; offshore promoter vehicle leverage

Sources:
- <https://news.bloomberglaw.com/daily-labor-report/indusind-bank-ceo-quits-over-230-million-accounting-lapse-1>
- <https://www.business-standard.com/companies/news/indusind-bank-board-focus-sebi-ex-parte-order-2025-125060501198_1.html>
- <https://www.business-standard.com/india-news/gopichand-hinduja-passes-away-hinduja-group-chairman-london-125110401793_1.html>
- <https://gulfnews.com/business/markets/who-will-succeed-gopichand-hinduja-inside-the-battle-for-a-15-billion-empire-1.500333305>
- <https://theprint.in/economy/hinduja-brothers-are-fighting-over-a-letter-that-divides-the-familys-11-billion-fortune/447519>

### KK Birla group (Chambal, Avadh/Magadh Sugar, HT Media) and MP Birla group (Birla Corp; Lodha estate dispute) — governance history
`person:group-kk-birla-mp-birla` · flag: **mixed (MP Birla); mostly-clean (Chambal/Avadh)** · confidence: single-source · tickers: CHAMBLFERT, AVADHSUGAR, MAGADSUGAR, HTMEDIA, BIRLACORPN, UNIVCABLES, VINDHYATEL, ZUARI

Flag: MIXED (MP Birla, litigation overhang) / MOSTLY-CLEAN (KK Birla companies). KK Birla group (after K.K. Birla d. 2008, split among daughters): Chambal Fertilisers (Saroj Poddar side; also Zuari Agro via Adventz), Avadh Sugar & Energy and Magadh Sugar (Nandini Nopany side; Upper Ganges/Oudh demerged 2015), HT Media (Shobhana Bhartia). Chambal is a cash-generative, dividend-paying fertiliser company; its 2025 buyback is a positive (unverified detail). HT Media has had persistent losses and complex RPTs with promoter-linked digital/radio entities -- minority value has eroded (unverified specifics). MP Birla group: Priyamvada Birla (d. Jul-2004) willed her estate, which controls Birla Corp, Universal Cables, Vindhya Telelinks, Birla Cable, to her CA R.S. Lodha; the Birla family (KK, BK, GP, SK, KM, Yashovardhan Birla) challenged the will. 20+ years of litigation: court-appointed administrators pendente lite (2012); a Calcutta HC division bench (Dec-2023) held that the estate is limited to shares she held, not controlling interests in companies -- appeal to the Supreme Court expected. Harsh Lodha has continued to run the companies. Lesson: a contested will over control can freeze strategic decisions and invite boardroom litigation for decades. Confidence: single-source for most KK Birla details.

- **red flags:** two-decade will dispute; HT Media losses/RPTs (unverified)

Sources:
- <https://business-standard.com/amp/companies/news/birla-lodha-battle-calcutta-hc-shrinks-priyamvada-birla-estate-s-reach-123121401093_1.html>
- <https://www.angelone.in/news/share-market/mp-birla-group-boardroom-battle-inside-the-latest-courtroom-drama>
- <https://www.livelaw.in/amp/high-court/calcutta-high-court/calcutta-high-court-birla-lodha-battle-testamentary-court-cannot-decide-issues-of-title-conclusively-such-power-lies-purely-within-the-domain-of-civil-courts-244587>

### Kalyani group (Baba Kalyani; Bharat Forge) — governance history
`person:group-kalyani` · flag: **mixed** · confidence: verified · tickers: BHARATFORG, KALYANIFRG, KSL, BFINVEST, HIKAL, BFUTILITIE

Flag: MIXED (operations strong; family/holdco governance contested). Bharat Forge is a global forging leader with defence/aero growth and long dividend record; no promoter pledging noted. Governance concerns are about the family and holding structure: (1) Hikal ownership dispute -- the Kalyani and Hiremath families each own ~34% of Hikal; Baba Kalyani's sister Sugandha Hiremath (Bombay HC, Mar-2023) claims a 1993-94 family arrangement obliges Baba to sell his Hikal stake to her family; Baba calls it a non-binding 'note'. (2) Brother Gaurishankar Kalyani disputes their mother Sulochana Kalyani's will (2024); nephews/nieces filed a Pune civil suit (2024) claiming shares of group assets. (3) The Supreme Court appointed former judge L. Nageswara Rao as mediator (Jul-2026), listing the matter for 3-Aug-2026 -- outcome not found. (4) Holdco structure (Kalyani Investment, BF Investment, Kalyani Steels) trades at deep holdco discounts; Bharat Forge has invested in group companies and new ventures (EVs, defence, US aluminium plants) whose returns lagged. Earlier, a 2024 news report of an alleged conspiracy complaint by Hiremath's side was denied by the Baba Kalyani group (allegation). No SEBI/ED findings against the promoters found. Investor read: discount the holdcos; watch board stability and any forced stake sale at Hikal.

- **red flags:** multi-front family disputes; holdco discount; capital spread into ventures
- **good conduct:** no pledges; dividends; operational quality

Sources:
- <https://moneylife.in/article/kalyani-family-feud-sc-pushes-baba-kalyani-sister-sugandha-hiremath-towards-mediation-appoints-justice-l-nageswara-rao-as-mediator/81050.html>
- <https://business-standard.com/companies/news/hikal-ownership-dispute-kalyani-family-spar-over-1993-agreement-123040400805_1.html>
- <https://businesstoday.in/latest/corporate/story/brothers-grim-inside-the-high-stakes-fight-between-baba-and-gaurishankar-kalyani-over-their-mothers-will-446597-2024-09-19>
- <https://www.business-standard.com/industry/news/hikal-promoters-baba-kalyani-faction-clash-over-family-wealth-disclosures-125011601275_1.html>

### Vedanta group (Anil Agarwal) — governance history
`person:group-vedanta` · flag: **mixed** · confidence: single-source · tickers: VEDL, HINDZINC

Flag: MIXED (leaning poor on minority treatment). UK-based Vedanta Resources (VRL, promoter holdco) carries large debt serviced largely by dividends and brand fees from listed Vedanta Ltd (VEDL), which in turn controls Hindustan Zinc (~61%). Pattern: very high dividend payouts upstream (good for VEDL minorities' cash yield but driven by holdco debt needs), plus brand and strategic-service fees -- Viceroy Research (Jul-2025) alleged VEDL and subsidiaries paid ~$361 m (Rs 3,085 cr) in brand fees to VRL in FY25 and called the structure a 'parasite' holdco; Vedanta rejected the report as 'selective misinformation'. A shareholder PIL on brand fees was reported (undated). History of contested minority actions: Cairn India merger (2017) with preference-share consideration; failed delisting of Vedanta Ltd (2020) when promoters sought to buy out minorities near lows; Vedanta lending to/receiving from group entities; Sterlite Copper Tuticorin closure (2018, after police firing on protesters). Hindustan Zinc's government (~28%) stake gives some check on cash moves. Status Nov-2026: VEDL's demerger into Vedanta Aluminium, Oil & Gas, Power, Iron & Steel plus residual Vedanta Ltd (with HZL) became effective 1-May-2026 (record date, 1:1 shares); VEDL revised dividend policy to drop mandatory HZL dividend up-streaming; lost Jaiprakash Associates to Adani at NCLAT (May-2026). Watch: brand-fee agreements at each demerged entity, ICDs to VRL, promoter pledges (historically ~99% of VEDL promoter shares encumbered -- verify current SAST). (Tickers of the four demerged entities were not verified here; check NSE.)

- **allegations:** Viceroy Jul-2025 (denied, no regulator finding)
- **red flags:** brand fees to holdco; holdco debt dependence; 2020 delisting attempt at lows; high encumbrance
- **good conduct:** high dividends; demerger with 1:1 mirror shares

Sources:
- <https://www.business-standard.com/companies/news/vedanta-resources-viceroy-ed-action-brand-fee-vedl-vrl-125073000697_1.html>
- <https://www.business-standard.com/companies/news/vedanta-s-anil-agarwal-vows-transparency-after-viceroy-s-allegations-125071001391_1.html>
- <https://www.moneylife.in/article/vedanta-sets-1-may-2026-as-demerger-record-date-shareholders-to-receive-11-shares-in-four-new-entities/80266.html>
- <https://www.businesstoday.in/latest/corporate/story/nclat-clears-adanis-rs14500-crore-jaiprakash-deal-rejects-vedanta-appeal-529548-2026-05-04>

### Essel group (Subhash Chandra, Punit Goenka) — governance history
`person:group-essel-zee` · flag: **poor** · confidence: verified · tickers: ZEEL, DISHTV, ZEEMEDIA, SITINET

Flag: POOR. Zee Entertainment (ZEEL) is a good franchise run for the benefit of a levered promoter group. Promoter Essel borrowed against Zee shares for infrastructure/power ventures; pledges rose to ~90% of promoter holding, invocations from Jan-2019 cut the promoter stake from ~42% to ~4%. Regulator findings: SEBI's interim order (Jun-2023) found Chandra and Goenka 'misused their position' to siphon ZEEL funds for associate entities via a sham 'adjustment' of Yes Bank FD-backed letters of comfort; barred them from board posts; SAT set aside the Goenka restriction (Oct-2023) while SEBI's probe continued. Invesco's 2021 requisition to remove Goenka and the collapsed Sony merger (Jan-2024) compounded value loss. New finding: SEBI order of 31-Jul-2026 held ZEEL's Hyderabad land was mortgaged as security for loans to four Essel entities without board/shareholder authorisation; barred ZEEL for two months and Chandra/Goenka for 12 months, with fines (ZEEL Rs 30 lakh, Goenka Rs 58 lakh, Chandra Rs 60 lakh); stock fell ~13%; SAT reserved interim-relief orders and partially relaxed ZEEL's restriction to allow a ~Rs 3,000 cr+ fundraise. Dish TV, Zee Media and Siti have had their own board fights, defaults and lender control. Lesson: a low promoter stake does not end promoter extraction while the family controls management; listed-company assets used as collateral for group debt is a severe signal.

- **regulator findings:** SEBI 2023 interim (fund diversion via LoCs); SEBI 31-Jul-2026 (unauthorised land mortgage)
- **red flags:** pledges ~90%; letters of comfort; listed assets securing promoter debt

Sources:
- <https://www.moneylife.in/article/sebi-bars-former-zee-executives-subhash-chandra-punit-goenka-from-securities-market-for-1-year/81233.html>
- <https://www.medianews4u.com/sat-questions-sebis-rationale-for-zees-two-month-market-ban-interim-relief-order-reserved/>
- <https://theprint.in/economy/zee-entertainment-case-sat-sets-aside-sebi-order-against-punit-goenka/1824791/>
- <https://www.business-standard.com/companies/news/subhash-chandra-zeel-md-ceo-move-sat-against-sebi-order-123061300857_1.html>
- <https://businesstoday.in/markets/stocks/story/zee-entertainment-shares-tank-13-amid-sebi-order-on-subhash-chandra-punit-goenka-546759-2026-08-03>

### Future group (Kishore Biyani) — governance history
`person:group-future` · flag: **poor** · confidence: verified · tickers: FRETAIL, FLFL, FCONSUMER, FEL, FSC

Flag: POOR. India's retail pioneer (Big Bazaar, Pantaloons -- sold to ABG 2012) ran a web of listed companies (Future Retail, Future Lifestyle Fashions, Future Consumer, Future Enterprises, Future Supply Chain) with heavy promoter pledging, frequent demergers/re-mergers, asset-light sale-and-leaseback structures and cross-holdings. COVID (2020) broke the model: lenders invoked pledges (FRL promoter stake ~47% -> ~14%), the Rs 24,713 cr asset sale to Reliance (Aug-2020) was fought by Amazon via Singapore arbitration and Indian courts and was called off by lenders (Apr-2022); Reliance had meanwhile taken over many FRL store leases. FRL went into IBC (2022); NCLT later allowed liquidation after the CIRP period lapsed without a plan (date unverified). Regulator record: SEBI (Feb-2021) barred Kishore Biyani and others for one year over insider trading in FRL shares (2017); SAT quashed that order (Dec-2023). SEBI (12-May-2026) imposed a consolidated Rs 50 lakh penalty on Kishore Biyani, Rakesh Biyani and FRL's ex-CFO over related-party-transaction disclosure lapses. Minority shareholders of FRL/FEL/FLFL have been largely wiped out. Early signals: pledges >50%, repeated restructurings that moved assets between listed vehicles, negative operating cash flow masked by working-capital financing, low ROCE. Lesson: frequent restructurings across listed entities are a red flag in themselves.

- **regulator findings:** SEBI 2021 insider trading (quashed by SAT 2023); SEBI May-2026 RPT disclosure penalty
- **red flags:** pledges; restructurings; sale-leasebacks; cross-holdings

Sources:
- <https://www.outlookbusiness.com/news/sat-quashes-sebis-order-against-kishore-biyani-others-in-insider-trading-case>
- <https://business-standard.com/article/companies/sebi-bars-future-ceo-kishore-biyani-from-capital-markets-for-one-year-121020301673_1.html>
- <https://www.livelawbiz.com/securities-law/sebi/securities-and-exchange-board-of-india-penalises-kishore-biyani-rakesh-biyani-cfo-related-party-transaction-disclosure-violations-533961>
- <https://www.business-standard.com/article/companies/future-group-shareholders-stare-at-possible-wipeout-of-investments-122042400555_1.html>

### GVK group (G.V. Krishna Reddy family) — governance history
`person:group-gvk` · flag: **poor** · confidence: verified · tickers: GVKPIL

Flag: POOR. Hyderabad infrastructure group that controlled Mumbai International Airport (MIAL, 50.5%) and Bangalore airport, plus power and roads, carrying group debt reported around Rs 32,000 cr (mid-2010s). Sold Bangalore airport stakes to Fairfax (33% in 2016, residual 10% for ~Rs 1,290 cr in 2017) to service debt -- the crown jewels went to lenders' needs rather than to shareholders. Allegations: CBI registered a case (27-Jun-2020) against chairman GVK Reddy, son G.V. Sanjay Reddy, MIAL and others alleging ~Rs 705 cr siphoned from MIAL -- ~Rs 310 cr via bogus works contracts with nine companies (2017-18) and ~Rs 395 cr of MIAL's surplus funds used for group companies (2012-2017); ED followed with a PMLA case. These are FIR allegations; no conviction or final finding was found in this scan. In 2020-21 Adani took control of MIAL by acquiring GVK's stake and debt; GVK Power & Infrastructure's listed shares became a penny stock. Early signals: holdco debt far above holdco cash flow, airport SPV surpluses moving to group companies, stake sales of the best assets, auditor qualifications on going concern. Lesson: when a group's only cash-generating asset is a regulated SPV with outside partners (AAI, ACSA, Bidvest), watch the SPV's related-party contracts.

- **allegations:** CBI FIR 2020 ~Rs 705 cr MIAL siphoning (pending)

Sources:
- <https://theprint.in/india/cbi-books-gvk-group-chairman-gvk-reddy-son-over-alleged-rs-705-crore-mumbai-airport-scam/452805>
- <https://theprint.in/india/bogus-contracts-undue-advantage-to-family-members-cbi-case-against-gvk-group-promoters/453008>
- <https://www.deccanherald.com/business/business-news/ed-files-money-laundering-case-against-gvk-group-mial-858094.html>
- <https://business-standard.com/article/companies/gvk-completes-residual-stake-sale-in-bangalore-airport-to-fairfax-india-117071301056_1.html>
- <https://www.business-standard.com/article/companies/challenges-weigh-on-gvk-s-debt-recovery-plan-116042000750_1.html>

### Kushagra Bajaj group (Bajaj Hindusthan Sugar, Bajaj Consumer Care) — governance history
`person:group-bajaj-kushagra` · flag: **poor (BAJAJHIND); mixed (BAJAJCON)** · confidence: verified · tickers: BAJAJHIND, BAJAJCON

Flag: POOR (Bajaj Hindusthan) / MIXED (Bajaj Consumer). Shishir Bajaj-Kushagra Bajaj branch, separate from the Rahul Bajaj group. Bajaj Hindusthan Sugar (BHSL) levered up for capacity in the late 2000s and plus promoter power venture Lalitpur Power; debt recast approved 2017 (~Rs 8,285 cr, SBI-led; promoter stake to fall 26% -> ~15% via sales to lenders); tagged NPA by lenders (2022); Feb-Mar 2026 a fresh RBI-framework restructuring converts several thousand crore of loans into equity/CCPS for lenders (~Rs 2,712 cr Series A CCPS allotted Mar-2026; totals reported between ~Rs 3,400 cr and ~Rs 6,155 cr -- unreconciled), heavily diluting minorities. Bajaj Consumer Care (cash-rich hair-oil FMCG) was used as the family's collateral: Dec-2018 ~70% of promoter Bajaj Resources' 66.9% stake was pledged; promoters sold 6.85% (Mar-2019) and ~22% (Oct-2019, ~Rs 700 cr, to MFs) taking pledges to zero, and proceeds were routed via Bajaj Energy to buy Lalitpur Power stakes from Bajaj Power Ventures and BHSL (~Rs 4,972 cr transaction). Bajaj Consumer later approved buybacks (2023, Jul-2025) and acquired Vishal Personal Care (Banjaras). Lesson: the clean, debt-free company's value can be drawn on for the sick sibling's debts. Status Nov-2026: BHSL under lender-led conversion; BAJAJCON debt-free; check SAST pledge data each quarter (watchlist kill criterion: any pledge).

- **red flags:** pledge of FMCG stake to fund sugar/power debt; RPT routing via Bajaj Energy/Lalitpur; repeated recasts; equity dilution to lenders
- **good conduct:** pledge cleared 2019; BAJAJCON buybacks
- **watch:** promoter pledge at BAJAJCON; any inter-corporate loans to group

Sources:
- <https://www.business-standard.com/amp/article/companies/promoters-sell-22-stake-in-bajaj-consumer-care-for-rs-700-crore-119101501423_1.html>
- <https://www.business-standard.com/article/pti-stories/bajaj-consumer-care-promoters-sell-6-85-pc-stake-for-rs-320-crore-119031300737_1.html>
- <https://www.business-standard.com/article/companies/panel-approves-bajaj-hindusthan-sugar-s-debt-recast-117120300001_1.html>
- <https://www.business-standard.com/article/companies/lenders-tag-bajaj-hindusthan-as-npa-debt-recast-plan-under-discussion-122070500995_1.html>
- <https://www.whalesbook.com/corporate-news/English/agriculture/Bajaj-Hindusthan-Sugar-Swaps-indian-rupee2711-Cr-Debt-for-Equity/69c640c163d6db8f4b531069>
- <https://www.business-standard.com/markets/capital-market-news/bajaj-consumer-drops-after-board-approves-share-buyback-125072500271_1.html>

### Lanco group (Lagadapati Madhusudhan Rao family) — governance history
`person:group-lanco` · flag: **poor** · confidence: single-source · tickers: LITL

Flag: POOR (leverage-driven wipe-out; no regulator fraud finding located). Hyderabad power-EPC group whose Lanco Infratech was among RBI's first 12 IBC referrals (2017) with group debt reported ~Rs 40,000 cr+; after creditors rejected Thriveni Earthmovers' revised bid, NCLT Hyderabad ordered liquidation (27-Aug-2018) -- equity effectively zero; IBBI records show liquidation still in process with a May-2026 stakeholder list. Lenders also pursued promoter Madhusudhan Rao as personal guarantor (NCLT personal-guarantee insolvency matter, 2021). Governance pattern: listed holdco funded multiple SPVs (Amarkantak, Udupi -- sold to Adani 2015, Teesta, Babandh, Vidarbha) and an Australian coal acquisition (Griffin, 2011) with corporate guarantees; EPC revenue booked from own group SPVs (related-party revenue inflating the holdco P&L); multiple CDR rounds (2013-2014) before IBC. A Business Standard analysis used Lanco to illustrate how a failed group-level resolution destroys value when each SPV is resolved separately. No CBI/SEBI fraud finding against the promoter was found in this scan -- do not describe it as fraud. Lesson: EPC 'order book' from captive SPVs is not third-party revenue; group guarantees convert one project's failure into holdco failure.

- **red flags:** related-party EPC revenue; group guarantees; CDR then IBC

Sources:
- <https://www.business-standard.com/article/pti-stories/nclt-orders-liquidation-of-lanco-infratech-118082701098_1.html>
- <https://www.bloombergquint.com/insolvency/lanco-infratech-headed-for-liquidation-after-thriveni-earthmovers-bid-is-rejected>
- <https://business-standard.com/article/companies/lanco-infratech-and-lessons-from-a-failed-group-resolution-of-troubled-debt-120102300735_1.html>
- <https://ibbi.gov.in/claims/order-process/L45200TG1993PLC015545>

### PC Jeweller (Balram Garg) — governance history
`person:group-pc-jeweller` · flag: **poor** · confidence: verified · tickers: PCJEWELLER

Flag: POOR (history) with an in-progress balance-sheet repair. 2018: the stock fell ~70%+ after a proposed buyback was withdrawn, promoters' related selling surfaced and questions arose on inventory, export receivables and a promoter-family 'gift' of shares. SEBI's final order (May-2021) fined four individuals and an entity Rs 1 cr in total and barred them for one year for insider trading around the 2018 buyback/capital announcements, including Rs 20 lakh on MD Balram Garg for communicating UPSI; the Supreme Court (Apr-2022) set aside SEBI/SAT orders against Garg's relatives (and, per reports, related findings) on the 'connected person' presumption -- regulator findings did not survive appeal. 2019-2023: export receivables and inventory problems, lender defaults; SBI-led consortium of 14 banks moved recovery/insolvency proceedings. Sep-2024 one-time settlement with the consortium; by 2026 filings the company reported repaying all 14 banks and receiving no-dues and release of mortgaged assets (verify against exchange filings). Funding of the turnaround included large preferential warrant issues to promoter/investors, heavy equity dilution, and a stock that rose many-fold from 2023 lows on the settlement narrative. Investor read: debt repaired, but history of insider-trading allegations, receivable write-offs and dilution means the governance record is not repaired by debt repayment alone; watch receivables recovery, inventory audit and promoter allotment pricing.

- **regulator findings:** SEBI 2021 insider-trading order (partly set aside by SC 2022)
- **good conduct:** bank debt OTS repaid by 2026 (company filings)

Sources:
- <https://www.sebi.gov.in/enforcement/orders/may-2021/final-order-in-the-matter-of-insider-trading-in-the-scrip-of-pc-jeweller-ltd-_50111.html>
- <https://www.taxmann.com/post/blog/sc-sets-aside-insider-trading-orders-against-p-chand-jeweller/>
- <https://www.outlookbusiness.com/spotlight/news-wire/pc-jeweller-receives-no-dues-release-letters-from-all-14-consortium-banks>
- <https://www.outlookbusiness.com/spotlight/news-wire/pc-jeweller-completes-debt-clearance-secures-release-of-mortgaged-assets>

### Rajesh Exports (Rajesh Mehta) — governance history
`person:group-rajesh-exports` · flag: **poor** · confidence: verified · tickers: RAJESHEXPO

Flag: POOR (pending SEBI case; interim findings, not final). Bengaluru gold refiner/jeweller reporting very large revenues (often Rs 2-3 lakh cr+ consolidated, largely via Swiss refiner Valcambi, bought 2015) at razor-thin margins, with limited segment/geography disclosure and a promoter holding ~54%. Long-standing analyst concerns: revenue quality, cash conversion, related-party trading, and frequent auditor changes; a 2023-24 PLI-linked battery venture (Elest/ACC Energy Storage) whose own auditor later resigned citing regulatory reasons. Regulator action: SEBI appointed BDO India as forensic auditor (Dec-2024); per SEBI's 109-page ex-parte interim order (3-Jun-2026), the forensic auditor was denied access to key records, ERP systems and journal data, and SEBI alleged standalone revenue was overstated by ~Rs 12,557 cr over FY21-FY24 (headlines cite a far larger cumulative 'misrepresentation' figure); promoter Rajesh Mehta was barred from dealing in the company's securities; SEBI ordered a fresh forensic audit and referred statutory auditors' conduct to NFRA (which reportedly opened a probe). The company said it would cooperate and not challenge the interim order, while disputing the allegations. SEBI confirmed its interim directions (Oct-2026). Early signals (visible for years): revenue far out of proportion to assets/employees, non-cooperation with information requests, opaque overseas subsidiary, low dividend relative to reported profits, and turnover-vs-cash-flow gaps. Lesson: when a forensic auditor reports non-cooperation, treat it as a stronger signal than any single number.

- **regulator findings:** SEBI interim Jun-2026 (confirmed Oct-2026): alleged Rs 12,557 cr revenue overstatement; forensic non-cooperation

Sources:
- <https://www.businesstoday.in/markets/stocks/story/bt-explainer-what-sebis-interim-order-against-rajesh-exports-and-its-promoter-reveals-534811-2026-06-04>
- <https://www.moneylife.in/article/sebi-confirms-interim-directions-on-rajesh-exports-retains-trading-ban-on-promoter-rajesh-mehta/81948.html>
- <https://www.valueresearchonline.com/stories/228727/rajesh-exports-sebi-forensic-audit-revenue-fraud-order/>
- <https://www.freepressjournal.in/business/rajesh-exports-audit-under-scrutiny-over-rs-15-lakh-crore-misreporting>

### Ruchi Soya (Shahra family) → Patanjali Foods (Patanjali/Ramdev) — governance history
`person:group-ruchi-patanjali` · flag: **poor (Shahra); mixed (Patanjali)** · confidence: verified · tickers: PATANJALI

Flag: POOR (Shahra era) / MIXED (Patanjali era). Ruchi Soya, an edible-oil major run by the Shahra family, over-borrowed and lost money on commodity bets and was admitted to IBC (Dec-2017; ~Rs 12,000 cr debt). Patanjali Ayurved won with a ~Rs 4,350 cr plan (2019); after relisting in Jan-2020 only ~1.1% of shares were public, and the stock rose from ~Rs 17 to over Rs 1,500 within months -- a thin-float price not reflecting fundamentals (market cap briefly exceeding many FMCG majors). The Mar-2022 FPO (Rs 4,300 cr) saw SEBI ask the company to let investors withdraw bids after unsolicited SMS messages promoting the issue circulated. Public float stayed below 25% (19.18% after FPO), so NSE/BSE froze 29.25 cr promoter shares (80.82% of equity) in Mar-2023 for MPS non-compliance; Patanjali Ayurved sold ~2.53 cr shares by OFS (Jul-2024) to reach 73.82% promoter holding. Renamed Patanjali Foods; absorbed Patanjali Ayurved's food business (2022, Rs 690 cr) and later its home & personal care business -- related-party acquisitions from the promoter that need independent valuation scrutiny. Patanjali Ayurved separately faced Supreme Court contempt proceedings over misleading ads (2024). Status Nov-2026: MPS compliant; watch further RPT acquisitions from the unlisted Patanjali Ayurved and the pricing of those deals.

- **red flags:** thin float post-IBC; FPO SMS episode; MPS freeze; RPT business transfers from promoter
- **good conduct:** MPS met via OFS 2024

Sources:
- <https://business-standard.com/article/markets/stock-exchanges-freeze-promoter-shareholding-of-patanjali-foods-123031501217_1.html>
- <https://www.outlookbusiness.com/news/explainer-why-patanjali-food-s-promoter-shares-are-frozen-and-how-is-it-affecting-the-baba-ramdev-led-company-s-stock--news-270594>
- <https://www.dtnext.in/amp/story/news/business/promoters-stake-falls-to-7382-in-patanjali-foods-after-share-sale-724736>

### Byju's / Think & Learn (Byju Raveendran) — governance history (unlisted)
`person:group-byjus-raveendran` · flag: **severe** · confidence: verified · tickers: none (unlisted)

Flag: SEVERE (unlisted; included as a governance pattern for future IPO candidates). Think & Learn peaked at a ~$22bn private valuation (2022) after debt-funded acquisitions (Aakash ~$950m, WhiteHat Jr, Great Learning, Epic). Signals: FY21 accounts filed ~18 months late; auditor Deloitte resigned (Jun-2023) citing delays, and three board members (Peak XV, Prosus, Chan Zuckerberg nominees) quit the same week; $1.2bn term-loan B default and lender litigation in the US; ~$533m from Byju's Alpha (the TLB borrower) moved to a small US hedge fund (Camshaft Capital) and onward offshore, per lenders; ED alleged FEMA violations of ~Rs 9,000 cr (Nov-2023 notice). BCCI's petition put Think & Learn into Indian insolvency (2024); a settlement with BCCI was set aside by the Supreme Court route (the SC dismissed Raveendran's plea on the BCCI settlement). A Delaware bankruptcy court entered a >$1bn default judgment against Raveendran personally (Nov-2025) for failing discovery; it was later corrected to say damages had not been determined, with a damages phase set for Jan-2026 (outcome not found). Aakash, now separately controlled by Manipal's Ranjan Pai, blocked transactions with Think & Learn. Raveendran denies wrongdoing. Lesson: late audited accounts, auditor exit plus investor-director exits in the same week are near-certain distress signals; debt at an offshore SPV with founder control of cash is a severe risk.

- **regulator findings:** US court default judgment (Nov-2025, later corrected); ED FEMA notice (allegation)

Sources:
- <https://www.outlookbusiness.com/corporate/us-court-orders-byju-to-pay-over-usd-1-bn-on-petition-of-byjus-alpha-glas-trust>
- <https://www.outlookbusiness.com/start-up/us-bankruptcy-court-reverses-1-bn-damages-against-byju-raveendran-statement>
- <https://gulfnews.com/business/markets/byjus-founder-liable-for-over-1-billion-default-judgment-plans-appeal-1.500356751>
- <https://www.business-standard.com/topic/byju-raveendran>

### Gensol / BluSmart (Anmol & Puneet Singh Jaggi) — governance history
`person:group-gensol-jaggi` · flag: **severe** · confidence: verified · tickers: GENSOL

Flag: SEVERE. Gensol Engineering (solar EPC; EV leasing to sister company BluSmart, both promoted by the Jaggi brothers) was a 2022-24 smallcap multibagger. SEBI's interim order (15-Apr-2025) found prima facie that of ~Rs 978 cr borrowed from IREDA and PFC to buy 6,400 EVs for BluSmart, only ~4,704 were bought (~Rs 568 cr); funds were round-tripped via the vehicle supplier and related entities to promoters' uses (incl. a luxury DLF Camellias apartment and personal spending); promoters treated the listed company 'like a personal piggy bank'; letters purportedly from lenders submitted to rating agencies (CARE, ICRA) were allegedly forged; SEBI barred the Jaggis from the market and from director roles and halted a stock split. SEBI confirmed the interim directions (Jul-2025); the Jaggis resigned from the board. IREDA's petition admitted Gensol into insolvency (Jun-2025, ~Rs 510 cr default); NCLT Ahmedabad admitted BluSmart (Jul-2025). CBI registered an FIR (31-Jul-2025) over alleged misappropriation of IREDA loans (~Rs 672 cr cited); ED searches/forex probe; MCA examination. Criminal cases are pending. Early signals visible in 2024: rating-agency downgrades to default after 'forged' no-default letters were questioned, related-party leasing to the sponsor's unlisted startup, preferential allotments and a stock split proposal amid soaring price, and rapid debt growth versus cash flow.

- **regulator findings:** SEBI interim Apr-2025, confirmed Jul-2025 (fund diversion)

Sources:
- <https://business-standard.com/markets/news/sebi-bars-gensol-engineering-promoters-for-alleged-fund-diversion-125041501266_1.html>
- <https://www.businesstoday.in/latest/corporate/story/sebi-upholds-ban-on-gensol-and-jaggi-brothers-in-fund-diversion-case-487120-2025-07-30>
- <https://www.business-standard.com/companies/news/nclt-admits-gensol-insolvency-plea-ireda-125061301025_1.html>
- <https://inc42.com/buzz/from-loan-diversion-to-forged-letters-cbi-books-blusmart-founders-in-%e2%82%b9672-cr-ireda-case/>
- <https://www.barandbench.com/amp/story/news/litigation/gensol-promoters-treated-company-funds-like-their-piggybank-sebi-bars-anmol-puneet-singh-jaggi-from-market>

### Jaypee group (Jaiprakash Gaur / Manoj Gaur) — governance history
`person:group-jaypee` · flag: **severe** · confidence: verified · tickers: JPASSOCIAT, JPPOWER, JPINFRATEC

Flag: SEVERE. Cement-hydro-real-estate-expressway group that borrowed heavily in 2007-2012. Jaypee Infratech (JIL, Yamuna Expressway + ~20,000+ unfinished Noida flats) was among RBI's first 12 IBC referrals (2017, IDBI-led); its listed equity was extinguished; NCLT approved Suraksha group's plan (Mar-2023). Key finding: the Supreme Court (Feb-2020, Anuj Jain v Axis Bank) upheld that JIL's mortgage of ~858 acres to secure the parent Jaiprakash Associates' (JAL) loans were preferential transactions to be avoided -- a listed subsidiary's assets pledged for the parent's debt. Homebuyer funds: ED arrested MD Manoj Gaur (13-Nov-2025) alleging ~Rs 12,000 cr of homebuyer money was diverted/siphoned, partly to Jaypee Sewa Sansthan (a trust he heads); he reportedly surrendered in Feb-2026 after bail rejection (single-source). Charges are allegations pending trial. JAL itself went into IBC; CoC approved Adani Enterprises' ~Rs 14,535 cr plan with 93.8% votes (Nov-2025), NCLT approved (17-Mar-2026), NCLAT dismissed Vedanta's challenge (4-May-2026) -- JAL equity holders expected to get little or nothing. Jaiprakash Power Ventures went through lender-led debt-for-equity conversion and remains listed. Early signals (visible by 2012-14): customer advances funding other businesses, inter-group guarantees and mortgages, repeated asset sales to service debt, rising promoter pledges. Lesson: in real-estate groups, homebuyer advances are the first pot of money diverted.

- **regulator findings:** SC 2020: JIL mortgages for JAL = preferential transactions
- **allegations:** ED 2025: Rs 12,000 cr homebuyer-fund diversion (pending trial)

Sources:
- <https://www.outlookbusiness.com/corporate/ed-arrests-jaypee-infratech-md-manoj-gaur-for-cheating-homebuyers>
- <https://www.businesstoday.in/latest/corporate/story/manoj-gaur-arrest-years-of-tumult-at-jaypee-group-502082-2025-11-13>
- <https://www.businesstoday.in/latest/corporate/story/nclat-clears-adanis-rs14500-crore-jaiprakash-deal-rejects-vedanta-appeal-529548-2026-05-04>
- <https://www.outlookbusiness.com/corporate/adani-enterprises-wins-nclt-nod-for-jaiprakash-associates-resolution-plan>
- <https://en.wikipedia.org/wiki/Jaypee_Infratech_homebuyers_fraud>

### Malvinder & Shivinder Singh (Ranbaxy, Fortis, Religare) — governance history
`person:group-religare-singh` · flag: **severe** · confidence: verified · tickers: FORTIS, RELIGARE

Flag: SEVERE (Singh era); Fortis (IHH-controlled since 2018) and Religare (Burman-controlled since 2025) have new promoters. The Singh brothers sold Ranbaxy to Daiichi Sankyo (2008, ~$4.6bn); Daiichi later won a ~Rs 3,500 cr Singapore arbitration award (2016) for concealment of US FDA issues. They then extracted value from Fortis Healthcare and Religare: Fortis disclosed ~Rs 473-500 cr of inter-corporate deposits routed to promoter-linked entities (2017-18), auditor Deloitte qualified results, and the board was overhauled; RBI (2018) found Religare Finvest (RFL) had placed ~Rs 2,300 cr+ of corporate loans with promoter-linked shells; Delhi Police EOW arrested both brothers (Oct-2019) in the ~Rs 2,397 cr RFL misappropriation case; ED followed under PMLA. The Supreme Court held the brothers guilty of contempt (Nov-2019) for selling Fortis shares in violation of its order and sentenced them to six months (Sep-2022). The Delhi HC granted Malvinder bail in the EOW case (2023); a Delhi court framed conspiracy/cheating charges; Shivinder filed for personal insolvency (2025). No final criminal verdict found as of 2026. Early signals: promoter pledges near 100% at Fortis/Religare, ICDs to promoter entities, auditor qualifications, spiritual-guru (RSSB) related borrowings reported, and an unexplained cash gap after selling Ranbaxy.

- **regulator findings:** RBI 2018 RFL inspection; SC contempt (2019, sentence 2022)

Sources:
- <https://theprint.in/india/religare-case-court-frames-conspiracy-cheating-charges-against-singh-brothers/2450977/>
- <https://business-standard.com/india-news/eow-s-rfl-case-hc-grants-bail-to-malvinder-singh-and-three-others-123060200837_1.html>
- <https://theprint.in/india/cases-malvinder-shivinder-singh-forbes-billionaires-police-custody/305824/>
- <https://www.business-standard.com/topic/fortis-healthcare-case>

### Reliance Anil Dhirubhai Ambani Group (ADAG, Anil Ambani) — governance history
`person:group-reliance-adag` · flag: **severe** · confidence: verified · tickers: RPOWER, RELINFRA, RCOM, RELCAPITAL, RHFL, RNAVAL

Flag: SEVERE. After the 2005 Ambani split Anil took telecom (RCom), power, infra, financial services (Reliance Capital, Reliance Home Finance, Reliance Commercial Finance) -- then a ~$40bn+ market-cap group. Over 2008-2020 it destroyed most of that value: debt-funded expansion, near-100% promoter pledges, insolvency of RCom (2019), Reliance Capital (RBI-supersession 2021, sold to IndusInd International/Hinduja 2024-25), Reliance Naval, and RHFL (resolution 2022). Regulator findings: SEBI (Aug-2024) banned Anil Ambani and 24 entities for 5 years and fined him Rs 25 cr for diverting RHFL funds via 'general purpose corporate loans' to promoter-linked shells (order dated 22-Aug-2024; total penalties ~Rs 624 cr on 27 parties; appeal status not verified). SBI classified RCom/Anil Ambani accounts as 'fraud' (Jun-2025); CBI registered a case on an alleged Rs 2,929 cr SBI loss (Aug-2025); ED opened PMLA cases, arrested the Reliance Power CFO (Oct-2025) over an alleged Rs 68 cr fake bank guarantee to SECI, arrested aides Amitabh Jhunjhunwala and Amit Bapna (Apr-2026) and says it has attached ~Rs 17,000 cr of assets in an alleged Rs 40,000 cr laundering case -- these are agency allegations, not court findings; a further CBI FIR (Apr-2026) alleges Rs 3,750 cr loss to LIC. NCLT admitted SBI's personal-insolvency plea against him as guarantor. Anil Ambani denies wrongdoing; he had not been arrested per reports found. Status Nov-2026: Reliance Power and Reliance Infra remain listed and have raised fresh equity via preferential allotments to promoter/investors -- treat any revival narrative with extreme caution.

- **red flags:** ICDs to shells (SEBI finding 2024); 'fraud' tags by banks; near-total pledges; repeated insolvencies; fake BG allegation

Sources:
- <https://www.business-standard.com/companies/news/rhfl-fund-diversion-case-5-year-market-ban-for-anil-ambani-24-others-124082300983_1.html>
- <https://www.businesstoday.in/markets/top-story/story/anil-ambani-24-others-barred-from-securities-market-for-5-years-fined-rs-25-crore-for-diversion-of-funds-442716-2024-08-23>
- <https://www.businesstoday.in/latest/corporate/story/ed-arrests-amitabh-jhunjhunwala-amit-bapna-close-aides-of-anil-ambani-in-rhfl-rcfl-loan-fraud-case-525865-2026-04-15>
- <https://www.businesstoday.in/amp/india/story/after-cbi-raids-ed-slaps-fresh-money-laundering-case-on-anil-ambani-rcom-493304-2025-09-10>
- <https://www.businesstoday.in/latest/corporate/story/ed-arrests-reliance-power-cfo-in-money-laundering-case-linked-to-anil-ambani-group-497808-2025-10-11>
- <https://www.moneylife.in/article/ed-arrests-anil-ambanis-top-aides-amitabh-jhunjhunwala-amit-bapna-in-40000-crore-loan-fraud-assets-worth-17000-crore-attached/80221.html>
- <https://www.ibtimes.co.in/ed-arrests-anil-ambanis-top-aides-amitabh-jhunjhunwala-amit-bapna-rhfl-case-901160>

### Sandesara family (Sterling Biotech group) — governance history
`person:group-sterling-sandesara` · flag: **severe** · confidence: verified · tickers: STERLINGBI

Flag: SEVERE. Gujarat gelatin/pharma group (Sterling Biotech, also oil & gas via Nigerian blocks) whose promoters Nitin and Chetan Sandesara (and Deepti Sandesara) left India in 2017 as CBI and ED pursued alleged bank fraud on an Andhra Bank-led consortium (agency figures ranged from ~Rs 5,000 cr to ~Rs 14,500 cr+ including overseas lenders). Sterling Biotech's listed equity was effectively wiped out in insolvency/liquidation. ED attached assets including Nigerian oil assets. Resolution: in Nov-2025 the Supreme Court accepted a government-placed sealed-cover proposal and ordered that all criminal proceedings (CBI, ED, SFIO) would be quashed once Rs 5,100 cr was deposited by 17-Dec-2025 -- stressing it is not a precedent (OTS amounts for Indian and foreign-guarantor companies were cited as Rs 3,826 cr and Rs 2,935 cr). In 2026 the Supreme Court questioned SEBI for continuing its proceedings and later told it to close the case or face action (Apr-2026); lenders sought release of funds from the court registry. Investor read: settlement extinguishes criminal exposure for promoters, not losses of minority shareholders. Early signals at the time: aggressive capacity expansion in a niche product (gelatin), large overseas subsidiaries, related-party transactions with promoter-owned firms, and a diary/ITs raid (2011) naming payments. Lesson: 'settlement' outcomes in India can let promoters exit cases -- governance history must be judged on conduct, not on criminal outcomes.

- **regulator findings:** criminal cases quashed by SC on Rs 5,100 cr deposit (Nov-2025)

Sources:
- <https://www.businesstoday.in/latest/economy/story/supreme-court-agrees-to-drop-criminal-proceedings-against-fugitive-sandesara-brothers-if-they-paid-rs-5100-crore-503463-2025-11-24>
- <https://www.livelaw.in/amp/top-stories/sandesarasterling-group-loan-fraud-supreme-court-quashes-criminal-cases-after-accused-agree-to-pay-rs-5100-crore-to-banks-311087>
- <https://www.moneylife.in/article/sterling-biotech-case-sc-questions-sebi-over-continued-probe-into-sandesara-brothers-despite-5100-crore-settlement/79966.html>
- <https://www.business-standard.com/india-news/supreme-court-asks-sebi-to-close-case-against-sandesaras-or-face-action-126040200852_1.html>

### Srei group (Hemant & Sunil Kanoria) — governance history
`person:group-srei-kanoria` · flag: **severe** · confidence: verified · tickers: SREINFRA

Flag: SEVERE. Kolkata infrastructure/equipment financier: Srei Infrastructure Finance (SIFL, listed) and Srei Equipment Finance (SEFL). After the IL&FS shock (2018) and COVID, Srei sought a one-shot debt restructuring via a scheme of arrangement (2020-21) that lenders rejected. RBI superseded both boards (4-Oct-2021) citing governance concerns and payment defaults -- one of the first NBFCs sent to IBC by RBI; an RBI special audit had flagged related-party transactions and under-provisioning. A lender-commissioned KPMG forensic audit flagged transactions; Hemant Kanoria challenged its methodology (NCLT Kolkata dismissed his application); a separate BDO transaction audit was commissioned by the administrator to identify avoidance transactions. PNB reported an alleged Rs 2,434 cr loan fraud by the former promoters to RBI (2022); the Kanorias deny wrongdoing and call the matter sub judice; they also made a late offer to take Srei out of insolvency (2023), which was not accepted. NCLT Kolkata approved National ARC (NARCL)'s plan (CoC vote 89.2%), and NARCL took control; existing equity effectively wiped out. Early signals: high exposure to promoter-linked/infra SPVs, evergreening via group entities, auditor emphasis matters, and wholesale funding dependence. Lesson: in lenders, related-party exposure and regulatory special audits are the first reliable signal; the equity goes to near zero when the regulator supersedes the board.

- **regulator findings:** RBI supersession Oct-2021; RBI special audit RPT flags
- **allegations:** PNB fraud report Rs 2,434 cr (denied)

Sources:
- <https://www.business-standard.com/article/companies/srei-infrastructure-finance-shocked-by-rbi-move-to-supersede-its-boards-121100401554_1.html>
- <https://www.zeebiz.com/personal-finance/banking/news-rs-2434-crore-fraud-pnb-flags-srei-equipment-infra-promoters-to-rbi-after-forensic-audit-386601>
- <https://bsppd.business-standard.com/article/companies/srei-s-hemant-kanoria-to-challenge-report-alleging-fraud-at-group-firm-122061401354_1.html>
- <https://www.business-standard.com/article/companies/kanorias-make-an-offer-to-take-srei-out-of-insolvency-123021001839_1.html>

### UB group / Kingfisher (Vijay Mallya) — governance history
`person:group-ub-mallya` · flag: **severe (historical); current UNITDSPR/UBL under MNC control** · confidence: verified · tickers: UNITDSPR, UBL, MCDHOLDING

Flag: SEVERE (Mallya era); the current listed companies are now controlled by multinationals (United Spirits by Diageo, United Breweries by Heineken) and their recent governance is materially better. Mallya's Kingfisher Airlines (listed, grounded 2012) borrowed ~Rs 9,000 cr from a 17-bank SBI-led consortium backed by Mallya's personal guarantee and UB Holdings' corporate guarantee; he left India in Mar-2016 and was declared a fugitive economic offender (Jan-2019). Regulator findings: SEBI (Jan-2017) barred Mallya and six former United Spirits officials for diverting ~Rs 1,880 cr from USL to UB-group entities including Kingfisher; Diageo's internal inquiry (2015) had flagged the diversions; SEBI (Jul-2024) further barred him for 3 years for secretly trading group shares via FII Matterhorn Ventures. UK courts approved extradition (2020), but he remained in the UK per Aug-2026 reports; the Bombay HC in Aug-2026 urged parties to 'move on' as SBI's recovery of ~Rs 15,000 cr (incl. asset sales) took centre stage. Lesson: cross-guarantees and fund transfers from a cash-rich listed company (USL) to a loss-making sibling (Kingfisher) are the classic transmission channel; a strategic buyer (Diageo) later found and disclosed the diversions. Mallya denies wrongdoing.

- **regulator findings:** SEBI 2017 (USL diversion), SEBI 2024 (Matterhorn trading)

Sources:
- <https://www.business-standard.com/article/pti-stories/sebi-bans-mallya-6-others-in-usl-fund-diversion-case-117012501425_1.html>
- <https://www.businesstoday.in/markets/story/vijay-mallya-barred-from-accessing-securities-markets-for-3-years-sebi-issues-order-439000-2024-07-26>
- <https://www.businesstoday.in/india/story/time-to-move-on-bombay-high-court-to-vijay-mallya-sbi-as-rs15000-crore-recovery-takes-centre-stage-549138-2026-08-14>
- <https://www.thedrinksbusiness.com/2025/09/britain-eyes-new-delhi-in-mallya-extradition-case/>

### Videocon group (Venugopal Dhoot family) — governance history
`person:group-videocon` · flag: **severe** · confidence: verified · tickers: VIDEOIND

Flag: SEVERE. Consumer-durables maker that diversified into oil & gas (Mozambique Rovuma stake, Brazil), DTH (d2h) and telecom with consortium bank debt of ~Rs 40,000 cr+ across 13+ group companies. Collapsed into insolvency (2018); the NCLT-approved Twin Star (Vedanta-group) plan for Videocon Industries (2021) implied a ~95%+ haircut and was later set aside by NCLAT -- outcome remains unresolved per this scan; listed shares effectively wiped out. ICICI Bank quid-pro-quo case: CBI FIR (2019) and chargesheet allege that ICICI's sanction of Videocon loans while Chanda Kochhar was CEO was linked to Dhoot's investment in NuPower Renewables (Deepak Kochhar's firm); CBI arrested the Kochhars and Dhoot (Dec-2022) -- the Bombay HC later held the Kochhars' arrest illegal (Feb-2024); the PMLA Appellate Tribunal (Jul-2025) upheld ED attachments, reportedly calling the Rs 64 cr transfer a bribe. Trial continues; no final criminal verdict found. ED also chargesheeted a UK-resident (Sachin Duggal) for alleged siphoning. Early signals: rising debt in unrelated ventures, complex cross-holdings, related-party flows, and a whistleblower (Arvind Gupta, 2016) letter. Lesson: when a consumer company's promoter bets on upstream oil with bank debt, minority equity is an option on that bet.

- **regulator findings:** PMLA Appellate Tribunal 2025 on attachments; criminal trial ongoing
- **red flags:** unrelated diversification on debt; whistleblower; lender-borrower conflicts

Sources:
- <https://www.outlookbusiness.com/news/icici-bank-loan-fraud-cbi-files-charge-sheet-against-kochhars-dhoot-news-276864>
- <https://www.business-standard.com/topic/icici-videocon-loan-case>
- <https://www.business-standard.com/article/finance/money-trail-a-timeline-of-cbi-s-probe-into-icici-bank-videocon-case-119012501495_1.html>
- <https://dailypioneer.com/news/videocon-bank-scam-ed-chargesheets-uk-resident-sachin-duggal-for-siphoning>

### Wadhawan family (DHFL; earlier HDIL link) — governance history
`person:group-dhfl-wadhawan` · flag: **severe** · confidence: verified · tickers: DHFL

Flag: SEVERE. Dewan Housing Finance (DHFL), once India's third-largest housing financier, collapsed in 2019 after the IL&FS-triggered funding freeze and a Cobrapost exposé (Jan-2019) alleging ~Rs 31,000 cr routed to shell companies. RBI superseded the board (Nov-2019); first NBFC resolved under IBC -- Piramal acquired it (Sep-2021); public equity was extinguished. Findings: SEBI's final order (12-Aug-2025, 181 pages) held that from 2006 to Mar-2019 DHFL promoters/executives diverted ~Rs 14,040 cr to 'Bandra Book Entities' (Wadhawan-linked firms) disguised as retail housing loans in a hidden branch-level book; it barred Kapil and Dheeraj Wadhawan for 5 years (Rs 27 cr fine each) and Rakesh and Sarang Wadhawan for 4 years (Rs 20.75 cr each), ~Rs 120 cr fines in all. CBI's ~Rs 34,926 cr bank-consortium fraud case (2022; UBI-led 17 banks) is in trial; the Supreme Court granted the brothers bail (Dec-2025) citing trial delay; a Delhi court refused CBI's plea to add charges (Oct-2026, single-source). The Yes Bank link: Yes Bank invested ~Rs 3,700 cr in DHFL debt in 2018 allegedly in return for ~Rs 600 cr loan to a Rana Kapoor family firm (CBI allegation). Wadhawans were earlier tied to HDIL/PMC Bank fraud. Early signals: loan growth far above peers with thin disclosure, large 'project loans' to opaque builders, wholesale funding mismatch, and an auditor/whistleblower trail.

- **regulator findings:** SEBI Aug-2025: Rs 14,040 cr diverted; bans and Rs ~120 cr fines

Sources:
- <https://www.moneylife.in/article/dhfls-bandra-book-scam-sebi-slaps-rs120-crore-fine-bans-4-wadhawans-2-others-for-diverting-rs14000-crore-loan/77969.html>
- <https://www.business-standard.com/companies/news/sebi-bars-wadhawan-brothers-five-years-dhfl-fund-diversion-case-125081300117_1.html>
- <https://livelaw.in/top-stories/supreme-court-grants-bail-kapil-wadhawan-dheeraj-wadhawan-dhfl-bank-fraud-case-513514>
- <https://www.devdiscourse.com/article/headlines/3999387-dhfl-case-delhi-court-rejects-cbi-plea-for-additional-charges-against-wadhawan-brothers-says-it-cannot-review-charge-order>

### Yes Bank / Rana Kapoor — governance history
`person:group-yes-bank-rana-kapoor` · flag: **severe** · confidence: verified · tickers: YESBANK

Flag: SEVERE (Kapoor era); Yes Bank today is controlled by institutional holders (SBI-led rescue 2020; Japan's SMBC became the largest shareholder in 2025 -- stake size ~20-25%, verify). Kapoor built Yes Bank (2004) into a top-5 private lender via fast corporate lending to stressed groups (ADAG, Essel, DHFL, IL&FS, Cox & Kings, CG Power). Early signals: RBI asset-quality divergences (FY16-17 ~Rs 4,200 cr; FY17 ~Rs 6,355 cr); RBI refused Kapoor a further term (Sep-2018); promoter pledges on Yes Bank shares; founder-family dispute with the Madhu Kapur side; frequent auditor and board exits (2018-19). RBI imposed a moratorium (5-Mar-2020) and an SBI-led reconstruction; Rs 8,415 cr of AT1 bonds were written off (the Bombay HC quashed the write-off in Jan-2023; Supreme Court stayed that ruling -- litigation ongoing). SEBI fined Kapoor Rs 2 cr for mis-selling AT1 bonds to retail investors (2021). CBI/ED allege Yes Bank invested ~Rs 3,983 cr in DHFL debentures in 2018 in exchange for ~Rs 600 cr in kickbacks to Kapoor family firms (DoIT Urban Ventures); Kapoor was arrested in Mar-2020 and released on bail in all cases after four years (Apr-2024); trials pending; no final conviction found. Lesson: for banks, RBI divergence disclosures and regulator refusals of CEO tenure are the decisive early signals; minority equity in a rescued bank is massively diluted (rescue at Rs 10/share vs ~Rs 400 peak).

- **regulator findings:** RBI divergences; SEBI AT1 mis-selling penalty; RBI moratorium 2020
- **allegations:** CBI/ED DHFL kickback case (pending)

Sources:
- <https://www.business-standard.com/about/who-is-rana-kapoor>
- <https://www.freepressjournal.in/mumbai/mumbai-court-grants-bail-to-yes-bank-founder-rana-kapoor-after-spending-4-years-in-jail>
- <https://theprint.in/judiciary/kept-behind-bars-over-2-yrs-without-trial-court-order-granting-bail-to-yes-bank-founder-rana-kapoor/1516930>
- <https://www.business-standard.com/topic/rana-kapoor>

## Caveats and gaps
- The search tool returned mainly secondary news, and many page dates were crawl dates. Dates were taken from article URLs or the body text where possible.
- Open items to verify: current SAST pledge % for Emami, GMR Power & Urban Infra, JSW Steel and Vedanta; Jio IPO timing (sources conflict: Oct-2026 vs H2FY27); the KK Birla/HT Media details; HGS cash-use concerns; SMBC's exact Yes Bank stake; Future Retail's liquidation date; Videocon's resolution status; the outcome of the Byju's US damages phase; any SAT appeal by Anil Ambani of SEBI's Aug-2024 order.
- 'BHL' in the brief was read as Bajaj Hindusthan (Kushagra Bajaj). The KK Birla group is covered with the MP Birla/Lodha dispute.
- Byju's is unlisted. It is included as a pattern for future IPO candidates.
