# India (NSE/BSE) Stock-Picking Toolkit, Red Flags & Forensic Accounting (as of Nov 2026)

Convention: **[VERIFY LIVE]** = number changes over time; re-check before use. **[BACKGROUND, not re-verified this session]** = well-established public fact from prior knowledge, not re-fetched in this research pass; the report writer should treat it as lower-confidence or verify against the named primary source.

---

## Q1. Data sources and how to use them (incl. Screener.in query syntax)

### Takeaway
A practical Indian stack is: Screener.in (screens + 10-yr financials + annual reports/concalls links) for discovery, then primary filings (BSE/NSE announcements, annual reports, credit-rating rationales, shareholding/pledge/SAST disclosures) for verification, with Trendlyne/Tijori/Tickertape/Chartink as supplements and Valuepickr for crowd-sourced deep dives. Screener queries are plain-English field names joined by AND/OR with comparison operators; public screens like "Coffee Can Investing" are good templates.

### Cited Findings
- Screener query pattern from a public user screen: `Debt to equity < 0.25 AND Return on capital employed > 20% AND Net profit > 200 AND Public holding < 30% AND Pledged percentage < 10%` — [Screener screen "334 to 48 companies >1000 cr mcap"](https://www.screener.in/screens/3679793/334-to-48-companies-1000-cr-mcap/) (as summarised by search; community example, not official docs).
- Public "Coffee Can Investing" Screener screen: starts `Market Capitalization > 1000 AND Average return on capital employed 10Years > 14% ...`; requires avg ROCE > 14% over 10/7/5/3 yrs plus current and previous year, the same for ROE, Debt to equity < 1, sales growth > 9% over 10/7/5/3 yrs and current year, Pledged percentage < 15%; returned ~100 results (4 pages) when fetched Nov 2026 [VERIFY LIVE count] — [Screener: Coffee Can Investing](https://www.screener.in/screens/1125448/coffee-can-investing/)
- Other public quality screens to clone: "Clean-balance-sheet compounders" (D/E < 0.5, ROCE > 18, ROE > 12) — [Screener](https://www.screener.in/screens/3103240/clean-balance-sheet-compounders/); "Consistent Compounders" (ROCE > 20% + low debt) — [Screener](https://www.screener.in/screens/3468167/the-consistent-compounders-screener/); "High Quality Long-Term Compounders" — [Screener](https://www.screener.in/screens/3394399/high-quality-long-term-compounders/); "High ROE, Continuous growth, Low PE, Low Debt" — [Screener](https://www.screener.in/screens/141333/High-Quality-Stocks-with-consistent-growth/?order=asc)
- Tickertape also hosts user-built compounder screens (e.g., "Quality compounders at a low EV/EBITDA") — [Tickertape](https://www.tickertape.in/screener/equity/user/quality-compounders-at-a-low-evebitda-auQCO3-ROu6xsOcX)
- Credit-rating "non-cooperation" and downgrades are a practical early-warning feed: Gensol saw credit downgrades around the April 2025 SEBI interim order — [Business Today](https://businesstoday.in/markets/stocks/sebi-interim-order-gensol-fund-diversion-stock-plunge-credit-downgrades-472172-2025-04-16)
- Broker research reading of disclosures can surface issues before regulators: Kotak Institutional Equities flagged mismatches between Kaynes Technology's, Kaynes Electronics Manufacturing's and Iskraemeco's FY25 related-party disclosures (Dec 2025) — [Business Today](https://www.businesstoday.in/markets/stocks/story/kaynes-technologies-shares-fall-related-party-disclosure-inconsistencies-kotak-equities-505053-2025-12-04)

### Inferences
- **Example Screener queries (written by this researcher in Screener's syntax; field names match Screener's standard ratio names but should be pasted and tested before use):**
  - *Quality compounder:* `Market Capitalization > 2000 AND Average return on capital employed 5Years > 20 AND Return on equity > 18 AND Debt to equity < 0.3 AND Sales growth 5Years > 12 AND Profit growth 5Years > 12 AND Pledged percentage < 5 AND Promoter holding > 40`
  - *GARP:* `Profit growth 3Years > 20 AND Sales growth 3Years > 15 AND Return on capital employed > 18 AND PEG Ratio < 1.2 AND Price to Earning < Industry PE AND Debt to equity < 0.5 AND Market Capitalization > 1000`
  - *Turnaround:* `Net profit > 0 AND Net Profit last year < 0 AND Sales growth > 20 AND OPM > OPM last year AND Debt to equity < 1 AND Pledged percentage < 10` (Screener also supports quarterly fields like `Net Profit latest quarter`, `Net Profit preceding year quarter`, `YOY Quarterly sales growth`).
  - *Small-cap multibagger hunt:* `Market Capitalization > 300 AND Market Capitalization < 5000 AND Sales growth 3Years > 20 AND Profit growth 3Years > 25 AND Return on capital employed > 18 AND Debt to equity < 0.5 AND Promoter holding > 50 AND Pledged percentage = 0 AND Cash from operations last year > 0`
  - *Forensic overlay to add to any screen:* `AND Cash from operations 5Years > 0.7 * Net profit 5Years` (approximating cumulative CFO/PAT; check exact field names for cumulative CFO), `AND Debtor days < 90`, `AND Pledged percentage < 5`.
- **Role of each tool [BACKGROUND, not re-verified this session]:** Trendlyne – DVM scores, insider/SAST/bulk-block deal trackers, superstar portfolio tracker, MF holdings changes; Tijori Finance – segment/operational KPIs (capacity, volumes, store counts) and concall summaries; Tickertape – screener + MF/ETF data; Chartink – technical scanners (breakouts, volume); BSE/NSE "Corporate Announcements" – results, concall transcripts, investor presentations, credit-rating intimations, SAST Reg 29 and PIT Reg 7 disclosures, pledge (Reg 31) filings; NSE/BSE bulk & block deal pages; AMFI/AMC monthly portfolio disclosures for MF holdings; CRISIL/ICRA/CARE/India Ratings rationale PDFs (liquidity, contingent liabilities, group support, "Issuer Not Cooperating" status); Valuepickr – long-form stock threads with annual report notes and concall summaries.
- The Kaynes case shows a cheap retail check: compare related-party disclosures across the listed parent, subsidiaries and the promoter's private entities (MCA filings) — mismatches are a signal even when they turn out to be disclosure errors.

### Gaps
- No official Screener.in syntax help page was retrieved; exact field names (e.g., cumulative CFO fields) need testing on the site.
- Did not fetch feature pages for Trendlyne, Tijori, Tickertape, Chartink or Valuepickr; tool descriptions above are background knowledge.

---

## Q2. What to read in an annual report (and Q3 forensic red flags with Indian blow-ups)

### Takeaway
The highest-yield annual-report sections are related-party transactions, auditor's report (qualifications/emphasis of matter/CARO), auditor changes, contingent liabilities, cash flow vs profit, receivables/inventory days, CWIP and capitalised costs, other income, loans to subsidiaries/group cos, and promoter remuneration. Almost every Indian blow-up (Satyam, DHFL, IL&FS, Yes Bank, Manpasand, Vakrangee, Gitanjali, Brightcom, Gensol) showed one or more of these: auditor resignation, related-party/fund diversion, profits not converting to cash, opaque group structures, or promoter pledging/selling.

### Cited Findings
**Gensol Engineering (2025) – fund diversion via related parties**
- SEBI interim order of 15 Apr 2025 barred Gensol and promoters Anmol & Puneet Singh Jaggi from the securities market and from director/KMP roles; case began with a June 2024 complaint about share price manipulation and fund diversion — [Business Today](https://www.businesstoday.in/markets/company-stock/story/sebi-bars-gensol-engineering-its-promoters-from-accessing-markets-in-fund-diversion-case-472151-2025-04-15)
- Gensol took ₹977.75 cr term loans, ₹663.89 cr earmarked for 6,400 EVs (for BluSmart), but only 4,704 vehicles were procured; funds allegedly went to a ₹42.94 cr DLF Camellias apartment and personal spends — [Outlook Business](https://www.outlookbusiness.com/news/blusmart-crisis-gensol-loans-for-procuring-evs-used-to-buy-dlf-camellias-flat-says-sebi); SEBI order described as "personal piggy bank" — [Moneylife](https://www.moneylife.in/article/how-jaggi-brothers-used-gensol-engineering-as-personal-piggybank-sebi-reveals-in-explosive-order/76903.html)
- Order mentions shell companies, circular fund flows and forged documents; stock split put on hold — [Moneylife](https://www.moneylife.in/article/how-jaggi-brothers-used-gensol-engineering-as-personal-piggybank-sebi-reveals-in-explosive-order/76903.html); [Angel One](https://www.angelone.in/news/sebi-cracks-down-on-gensol-engineering-over-funds-misuse-halts-stock-split)
- Jaggi brothers resigned May 2025; SEBI confirmed the interim order 30 Jul 2025 — [The Week](https://www.theweek.in/wire-updates/business/2025/05/12/dcm50-biz-gensol-promoter-resign.html); [The Week](https://www.theweek.in/wire-updates/business/2025/07/30/dcm123-biz-sebi-gensol.html)

**Brightcom Group – inflated profits, impairment delays, preferential-issue irregularities**
- SEBI ordered a forensic audit (FY15–FY20) in March 2022 — [Business Standard](https://www.business-standard.com/amp/article/news-cm/sebi-orders-forensic-audit-of-brightcom-group-122030100275_1.html)
- SEBI found profits artificially inflated by about ₹1,280 cr in FY19–FY20 by delaying impairments; money from preferential allottees did not show up or match bank statements — [BQ Prime](https://www.bqprime.com/business/sebi-unravels-how-brightcom-group-cooked-its-books); [SEBI order PDF (Feb 2025)](https://www.sebi.gov.in/sebi_data/attachdocs/feb-2025/1738846203125_1.pdf)
- Penalties: ~₹34 cr total, including ₹15 cr each on promoters M. Suresh Kumar Reddy and Vijay Kancharla; Oct 2025 order penalised former independent directors (₹35 lakh) for failing fiduciary duties — [Storyboard18](https://www.storyboard18.com/digital/sebi-fines-brightcom-group-%E2%82%B934-crore-for-financial-misrepresentation-56014.htm); [Moneylife](https://www.moneylife.in/article/brightcom-group-sebi-slaps-rs35-lakh-penalty-on-2-exdirectors-for-accounting-irregularities/78509.html); [SEBI order PDF (Oct 2025)](https://www.sebi.gov.in/sebi_data/attachdocs/oct-2025/1759753202973_1.pdf)
- Note: figures across reports differ (₹868 cr vs ~₹1,280–1,300 cr) depending on period/order — verify against the SEBI PDFs.

**Manpasand Beverages – auditor exits + fake invoicing**
- Deloitte resigned in May 2018 citing non-provision of "significant information"; second auditor Mehra Goel & Co quit July 2019 — [Moneylife](https://moneylife.in/article/after-deloitte-mehra-goel-co-resigns-as-manpasands-auditors/57645.html); [Business Standard](https://business-standard.com/amp/article/markets/gst-scam-manpasand-bev-s-auditor-resigns-stock-locked-in-5-lower-circuit-119071000226_1.html)
- MD Abhishek Singh, his brother and CFO arrested May 2019 in a ₹40 cr GST fake-invoice fraud using 30+ bogus units — [Business Standard](https://www.business-standard.com/amp/article/current-affairs/manpasand-beverages-md-officials-arrested-in-rs-40-crore-gst-fraud-119052500241_1.html); [Business Standard explainer](https://business-standard.com/article/companies/how-gst-fraud-worth-rs-40-crore-came-into-light-at-manpasand-beverages-119053100023_1.html)

**Vakrangee – auditor resignation after a parabolic run**
- Stock fell ~84% from ₹515 (24 Jan 2018) to ~₹81.5 by early May 2018 — [Business Standard](https://www.business-standard.com/amp/article/markets/vakrangee-hits-22-month-low-after-auditor-pwc-flags-concerns-118050700332_1.html)
- Price Waterhouse resigned late April 2018, under a year after appointment, citing lack of information on election books, bullion and jewellery businesses; MCA ordered inspection of three years' books (Sep 2018) — [BloombergQuint](https://www.bloombergquint.com/amp/business/election-books-bullion-and-gold-why-vakrangees-auditor-quit); [Business Standard](https://www.business-standard.com/amp/article/companies/vakrangee-ltd-s-accounts-business-face-scrutiny-from-corporate-affairs-min-118092900389_1.html)
- ~30 auditors resigned from listed companies in a year in 2018 — an industry-wide signal — [The Week](https://www.theweek.in/news/biz-tech/2018/06/04/Alarm-bell-for-investors-30-auditors-resigned-in-last-one-year.amp.html)
- Vakrangee later said probes found no irregularity — [BloombergQuint](https://www.bloombergquint.com/business/probe-revealed-no-irregularity-over-auditor-resignation-stock-trading-says-vakrangee) (company claim)

**Kaynes Technology (Dec 2025) – disclosure quality scare in a hot EMS name**
- Kotak flagged ₹180 cr purchases from Kaynes Electronics Manufacturing, ₹320 cr payables / ₹190 cr receivables mismatches, goodwill/reserve treatment in acquisitions, and ₹180 cr capitalised as technical know-how/prototypes — [Business Today](https://www.businesstoday.in/markets/stocks/story/kaynes-tech-shares-extend-fall-sink-8-today-as-kotak-flags-disclosure-gaps-co-issues-clarification-505187-2025-12-05)
- Company said the RPTs were eliminated on consolidation but "inadvertently not disclosed" in standalone statements and since rectified — [Business Standard](https://www.business-standard.com/amp/companies/news/some-related-party-transactions-not-disclosed-inadvertently-kaynes-tech-125120501207_1.html)
- Stock fell ~27% in six sessions from ₹5,411.70 and nearly halved from 52-week high ₹7,824.95; dragged other EMS names — [Business Standard](https://www.business-standard.com/amp/markets/news/kaynes-tech-snaps-30pc-rout-as-stock-soars-7pc-on-positive-reports-125120900324_1.html); [Business Standard](https://www.business-standard.com/markets/news/ems-stocks-slip-as-dixon-tech-amber-ent-drop-up-to-9pc-heres-why-125121000775_1.html)
- No regulator action found; ICICI Securities called them largely disclosure discrepancies — [Business Today](https://www.businesstoday.in/markets/stocks/story/kaynes-tech-shares-extend-fall-sink-8-today-as-kotak-flags-disclosure-gaps-co-issues-clarification-505187-2025-12-05)

**Adani–Hindenburg debate**
- SEBI's two final orders dated 18 Sep 2025 held Hindenburg's allegations (incl. concealed related-party transactions via Milestone Tradelinks, Rehvar Infrastructure) "not established", closing proceedings without directions; group stocks rose up to 13% — [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-clears-adani-group-dismisses-hindenburg-allegations-125091801259_1.html); [Moneylife](https://www.moneylife.in/article/adani-group-gets-clean-chit-in-hindenburg-case-sebi-says-no-evidence-of-concealed-related-party-deals/78318.html); [Business Today](https://www.businesstoday.in/markets/stocks/story/sebi-dismisses-hindenburg-researchs-allegations-against-adani-group-494677-2025-09-18)
- SEBI's reasoning was partly that the impugned transactions did not meet the then RPT definition — [Moneylife](https://www.moneylife.in/article/adani-group-gets-clean-chit-in-hindenburg-case-sebi-says-no-evidence-of-concealed-related-party-deals/78318.html)

**SME IPO manipulation and SEBI response**
- SEBI amended ICDR (4 Mar 2025) after finding diversion of IPO proceeds to promoter shells and revenue inflated via circular RPTs; new rules include a minimum operating-profit (EBITDA) eligibility, limits on use of proceeds, minimum application raised from ~₹1 lakh to >₹2 lakh — [The Legal Quorum](https://thelegalquorum.com/reforming-the-sme-ipo-framework-sebis-2025-regulatory-measures/); [IndiaCorpLaw](https://indiacorplaw.in/2025/04/23/strangling-growth-or-ensuring-stability-sebis-new-regulatory-framework-for-smes/); [Agama Law](https://agamalaw.in/2025/05/16/navigating-sme-ipos-recent-regulatory-changes/)
- Enforcement examples: FOCL barred two years (Oct 2025) over fund diversion across ~20 SME IPOs (>₹100 cr); SecUR Credentials (Sep 2025) post-listing coordinated price manipulation — per [Corporate Professionals](https://www.corporateprofessionals.com/?p=11759) (secondary; verify against SEBI orders)
- Oct 2026 SEBI consultation proposes partial recalibration (only unsubscribed portion needs underwriting; align promoter contribution with mainboard) — [Moneylife](https://www.moneylife.in/article/sebi-proposes-sweeping-overhaul-of-sme-ipo-framework/81956.html); [Bar & Bench](https://www.barandbench.com/law-firms/leading-questions/the-sme-ipo-market-in-2026-stricter-entry-smarter-execution)
- NISM overview of SME IPO lacunae — [NISM](https://www.nism.ac.in/blog/lacunae-in-the-sme-ipo-markets)

**Finfluencer / Telegram pump-and-dump**
- Sadhna Broadcast: paid YouTube videos/ads with false claims (5G licence, Adani acquisition) used to pump the stock; SEBI ordered disgorgement — [exchange4media](https://www.exchange4media.com/influence-zone-news/sadhna-broadcast-case-sebi-tightens-grip-on-finfluencers-143991.html)
- "Baap of Chart" (Md. Nasiruddin Ansari): unregistered advice via X and Telegram; ~₹17.2 cr disgorgement (Oct 2023) — [Inc42](https://inc42.com/buzz/sebi-cracks-down-on-finfluencer-baap-of-chart-orders-inr-17-cr-disgorgement)
- Asmita Patel: ex-parte interim order 6 Feb 2025 barring her and 5 others; tips via private Telegram channels/courses; >₹53 cr impounded — [YourStory](https://yourstory.com/2025/02/sebi-bans-fininfluencer-asmita-patel-5-others-from-mkt-impound-illegal-gains-of-over-rs-53-cr); [law.asia](https://law.asia/sebi-bans-asmita-patel/)

**Forensic models**
- Marcellus's forensic model ("first line of defence") grades companies on accounting quality using ~12 ratios drawn from Schilit's *Financial Shenanigans*, covering P&L manipulation and balance-sheet misstatement; a Level-2 qualitative checklist covers governance issues the ratios miss — [Elearnmarkets summary of *Diamonds in the Dust*](https://www.elearnmarkets.com/school/units/diamonds-in-the-dust/marcellus-s-3-level-check-to-detect-accounting-frauds)

### Inferences
- **Annual-report reading checklist (synthesis):**
  1. *Auditor's report & CARO annexure* – qualifications, emphasis of matter, going-concern, KAMs; CARO comments on loans to related parties, defaults, fraud reporting. *Auditor change mid-term* = top red flag (Manpasand, Vakrangee above).
  2. *Related party transactions (AS/Ind AS 24 note + AOC-2)* – purchases/sales with promoter entities, loans/advances/guarantees to group cos, royalty to promoter entities; cross-check against subsidiaries' and private promoter cos' disclosures (Kaynes, Gensol, Brightcom).
  3. *Contingent liabilities & guarantees* vs net worth (corporate guarantees to group cos).
  4. *Cash flow vs profit* – cumulative 5–10 yr CFO/PAT well below ~0.7–0.8, or FCF persistently negative while reporting profit growth.
  5. *Working capital* – receivable days and inventory days rising faster than sales; "loans and advances" / "other current assets" ballooning.
  6. *CWIP and capitalised expenses* – CWIP stuck for years; R&D/"technical know-how"/interest capitalised (Kaynes ₹180 cr capitalised).
  7. *Other income* as share of PBT; interest income on funds that look idle while company borrows (cash + debt both high = classic Indian red flag).
  8. *Subsidiaries / step-downs / overseas entities* – many small subsidiaries, write-offs, impairments delayed (Brightcom).
  9. *Promoter remuneration* vs PAT and vs peers; commission structures.
  10. *Shareholding* – promoter pledge trend, promoter selling, preferential allotments/warrants to unknown entities, frequent fund-raises (Brightcom preferential issue).
- **Background on older blow-ups [BACKGROUND, not re-verified this session]:** Satyam (Jan 2009) – Ramalinga Raju confessed to ~₹7,000 cr inflation incl. fictitious cash balances; lesson: verify cash vs interest income; PwC later penalised. IL&FS (2018) – AAA-rated group defaulted with ~₹90,000+ cr debt; 300+ subsidiaries; rating agencies penalised; lesson: complex group structure, rating complacency. DHFL (2019) – Cobrapost alleged ~₹31,000 cr diverted via shell companies; later the first NBFC/HFC resolved via IBC (Piramal); lesson: loans to related "builder" entities, ALM mismatch. Yes Bank (2020) – RBI moratorium March 2020, under-reported NPA divergence flagged by RBI in prior years, SBI-led rescue, AT1 bonds written off; founder Rana Kapoor arrested; lesson: NPA divergence disclosures in annual report, rapid corporate-loan growth to stressed groups. Gitanjali Gems (2018) – Mehul Choksi linked to the ~₹13,000+ cr PNB LoU fraud with Nirav Modi; lesson: high receivables/inventory in jewellery, promoter pledging. Each of these should be verified with primary sources before citation.
- **Scoring tools:** Beneish M-score (8 variables; > −1.78 commonly treated as likely manipulator), Altman Z-score (distress; original manufacturing cut-offs 1.81/2.99; EM-variant Z'' for emerging markets), Piotroski F-score (0–9, 8–9 strong). Trendlyne/Screener users often build these manually. [BACKGROUND – thresholds standard in literature; no Indian-specific validation fetched.]
- Pattern across cases: auditor resignation + preferential issues/QIPs + aggressive promoter communication + retail/finfluencer hype + rising pledge → highest-risk combination.

### Gaps
- Satyam, DHFL, IL&FS, Yes Bank, Gitanjali details were not re-fetched this session (stayed within tool budget); need primary-source citations (SEBI orders, RBI press releases, SFIO reports).
- The exact list of Marcellus's 12 forensic ratios was not retrieved (the summary didn't list them).
- No retrieved study on how well M-score/Z-score/F-score work on Indian data.
- Status of Gensol final order/appeal after July 2025 and of Asmita Patel final order not checked.

---

## Q4. Indian themes and cycles 2020–2026, and where valuations stand (Nov 2026)

### Takeaway
2020–2024 rewarded policy-driven capex themes (PLI, China+1, defence, railways, power/capital goods, EMS) and financialisation; by late 2025–2026 valuations compressed in parts of the market. As of mid-Nov 2026 the Nifty 50 trades around 20–21x trailing earnings, midcaps near their 10-yr forward average, and small caps still at a premium to their own history.

### Cited Findings
- Nifty 50 trailing P/E ~20.6 as of 16 Nov 2026 per NSE Indices data [VERIFY LIVE] — as reported in search summary of [Wright Research](https://www.wrightresearch.in/stocks/nifty-pe-ratio/) / [indexpe.in](https://indexpe.in/)
- HDFC MF (6 Nov 2026): Midcap 100 forward P/E 22.8x vs 10-yr avg 23.2x; BSE Smallcap 250 forward P/E 21.9x vs 10-yr avg 18.7x; 41% of Nifty Midcap 150 stocks below 30x forward P/E vs 25% in Sep-24 [VERIFY LIVE] — [HDFC MF](https://www.hdfcfund.com/learn/deep-dives/tuesday-talking-point/equity-valuations-remain-reasonable-despite-market-uptick)
- Trailing basis (Oct 2026): Nifty Smallcap 100 P/E ~33.6 vs Nifty 50 ~19.1 (~77% premium); Nifty Midcap 150 ~26.4 (~39% premium) [VERIFY LIVE] — [Craytheon Smallcap 100](https://craytheon.com/charts/nse-sector-pe/nifty-smallcap-100-pe-ratio/); [Craytheon Midcap 150](https://craytheon.com/charts/nse-sector-pe/nifty-midcap-150-pe-ratio/)
- Note: trailing vs forward and index-universe differences explain the conflicting premium figures.
- EMS sector sentiment hit in Dec 2025: Kaynes, PG Electroplast fell up to 13%; Dixon and Amber also dropped — [Business Standard](https://www.business-standard.com/amp/markets/news/kaynes-pg-electroplast-tank-up-to-13-on-monday-ems-stocks-extend-losses-125120800554_1.html); [Business Standard](https://www.business-standard.com/markets/news/ems-stocks-slip-as-dixon-tech-amber-ent-drop-up-to-9pc-heres-why-125121000775_1.html)

### Inferences
- Theme map [BACKGROUND, not re-verified this session]: PLI schemes (14 sectors announced 2020–21, incl. mobiles/electronics, pharma, autos, specialty steel, textiles, solar modules) underpinned EMS (Dixon, Kaynes, Amber, PG Electroplast, Syrma) and solar manufacturing (Waaree, Premier Energies); China+1 helped specialty chemicals (which de-rated 2022–24) and EMS; defence indigenisation (HAL, BEL, Mazagon Dock, BDL, Data Patterns) and railways (IRFC, RVNL, Titagarh) were 2023–24 PSU re-ratings that corrected in 2025; power/capital goods (Siemens, ABB, CG Power, BHEL, transformers/cables) on transmission & data-centre capex; financialisation (BSE, MCX, CDSL, CAMS, KFin, HDFC AMC, Nippon AMC) on demat/SIP growth — note F&O curbs hit exchange volumes; premiumisation (Radico Khaitan, United Spirits; also jewellery/Titan) vs mass consumption slowdown.
- With large caps near long-run averages and small caps still premium, a stock-picking process should demand earnings delivery rather than re-rating in small caps.

### Gaps
- Did not retrieve sourced performance/valuation data per theme (defence, railways, EMS, AMCs, Radico) for 2026.
- No consensus Nifty EPS forecast for FY27/FY28 retrieved.

---

## Q5. Taxes and F&O rule changes (practical)

### Takeaway
Since 23 Jul 2024, listed equity STCG is 20% and LTCG 12.5% above a ₹1.25 lakh annual exemption (12-month holding). SEBI's F&O curbs (Nov 2024 onward) raised contract sizes, cut weekly expiries to one index per exchange, collected premium upfront and added intraday position monitoring; Budget 2026 raised STT on F&O from 1 Apr 2026, alongside a 50% cash-margin rule.

### Cited Findings
- Budget 2024: STCG (Sec 111A) 15% → 20%; LTCG (Sec 112A) 10% → 12.5%; exemption ₹1 lakh → ₹1.25 lakh; holding period for listed equity unchanged at 12 months — [Business Standard](https://www.business-standard.com/amp/finance/personal-finance/budget-2024-all-the-key-changes-to-capital-gains-tax-explained-124072500330_1.html); [Zerodha Z-Connect](https://zerodha.com/z-connect/business-updates/what-changes-for-investors-after-budget-2024); [Business Today (IT dept FAQs)](https://www.businesstoday.in/amp/personal-finance/tax/story/budget-2024-income-tax-dept-issues-faqs-on-new-capital-gains-tax-regime-check-details-438651-2024-07-24)
- SEBI Oct 1, 2024 six-measure package (effective from 20 Nov 2024 in phases): minimum index-derivative contract value ₹15 lakh at launch; one weekly expiry per exchange (NSE: Nifty 50; BSE: Sensex); 2% extra ELM on short options on expiry day; removal of calendar-spread benefit on expiry day; upfront premium collection (Feb 2025); intraday position-limit monitoring (Apr 2025) — [Business Standard](https://www.business-standard.com/amp/markets/news/sebi-announces-six-key-changes-to-curb-speculation-in-derivatives-trading-124100101316_1.html); [Business Standard](https://www.business-standard.com/amp/markets/news/new-f-o-rule-to-come-into-effect-from-thursday-nov-21-here-s-what-changes-124112000292_1.html); [Motilal Oswal](https://www.motilaloswal.com/learning-centre/2024/10/nse-discontinues-weekly-derivatives-on-bank-nifty-nifty-midcap-select-and-finnifty)
- Lot sizes Nov 2024: Nifty 25→75, Bank Nifty 15→30; revised again Jan 2026 (Nifty 75→65) [VERIFY LIVE]; Nifty weekly expiry Tuesday, Sensex Friday [VERIFY LIVE]; from 1 Apr 2026 ≥50% of F&O margin must be cash/cash-equivalents; Budget 2026 STT: futures 0.02%→0.05%, options premium sell 0.10%→0.15%, options exercise 0.125%→0.15% — [Alice Blue (secondary, internally inconsistent in places)](https://aliceblueonline.com/blog/sebi-new-fo-rules-2024-to-2026); [Zerodha lot-size update](https://zerodha.com/z-connect/updates/revision-in-lot-size-for-nifty-index-fo-contracts); [5paisa](https://www.5paisa.com/news/nse-bse-revise-index-derivatives-framework-lot-sizes-weekly-options)

### Inferences
- For a long-only stock picker, the ₹1.25 lakh exemption and 12.5% LTCG favour holding >12 months; STCG at 20% penalises churn.
- F&O curbs and higher STT likely reduce retail derivative volumes, relevant to exchange/broker stocks (BSE, Angel One, CDSL) in the financialisation theme.

### Gaps
- Budget 2026 STT and Jan 2026 lot sizes come from a broker blog with self-noted inconsistencies; verify against the Finance Act 2026 and NSE circulars.
- Did not verify whether Budget 2025/2026 changed equity capital-gains rates (no evidence found that they did).
- SEBI's own F&O loss studies (e.g., ~9 in 10 individual traders lose money) not fetched this session.

---

## Q6. How Indian multibagger hunters structure their process

### Takeaway
Indian practitioners typically layer: (1) a quant screen for quality/growth (Coffee Can-style 10-yr ROCE/ROE/sales consistency, or growth+low debt for small caps), (2) a forensic/governance filter (CFO/PAT, pledge, auditor, RPTs — Marcellus-style ratio grading then a qualitative checklist), (3) deep reading of annual reports, concalls, rating rationales and Valuepickr threads, and (4) valuation and position sizing.

### Cited Findings
- Coffee Can filter as codified on Screener: 10-yr consistency of ROCE/ROE > 14–15%, revenue growth > 9–10%, low leverage, plus pledge filter — [Screener: Coffee Can Investing](https://www.screener.in/screens/1125448/coffee-can-investing/)
- Marcellus uses a 3-level check: Level 1 quantitative forensic ratios, Level 2 qualitative accounting/governance checklist (issues not captured by data) — [Elearnmarkets](https://www.elearnmarkets.com/school/units/diamonds-in-the-dust/marcellus-s-3-level-check-to-detect-accounting-frauds)
- SEBI orders show the downside of skipping governance checks even in hyped small caps (Gensol rose on EV/solar narrative before collapse) — [Value Research](https://www.valueresearchonline.com/stories/223978/sebi-bars-gensol-founders-over-ev-loan-diversion-tied-to-blusmart/)

### Inferences
- Suggested process for the playbook: Screen → forensic overlay (CFO/PAT, receivable days, pledge, auditor tenure/changes, RPT % of revenue, other income % of PBT) → read 3–5 years of annual reports + last 8 concalls (check guidance vs delivery) → rating rationales → shareholding (promoter, MF/FII trends, bulk deals) → Valuepickr thread for scuttlebutt → valuation (PEG, EV/EBITDA vs history) → sizing with a "kill list" of red flags (auditor resignation, rating non-cooperation, rising pledge, preferential issues to obscure entities, finfluencer/Telegram promotion, SME listing with sharp post-listing run-up).
- Books referenced by Indian investors [BACKGROUND]: *Coffee Can Investing* (Mukherjea, Bajaj, Rao), *The Unusual Billionaires* (Mukherjea), *Diamonds in the Dust* (Mukherjea et al.), *100 Baggers* (Mayer).

### Gaps
- Did not fetch Valuepickr examples or interviews with named Indian multibagger investors (e.g., process write-ups); their methods are summarised from background knowledge only.
