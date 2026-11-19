# Edge methods and data access for Indian small caps (tested 2026-11-19)

Purpose: "Lynch at scale" means AI reads every filing and concall, tracks management promise-vs-delivery over years and spots changes early, while the human does real-world scuttlebutt. This note covers what data can actually be pulled from here (tested with curl from a cloud, non-Indian IP, on 2026-11-19), and which methods are backed by research.
Research, not SEBI-registered advice.

## Part A: tested data access

### Key finding: NSE has moved to www.nseindia.in
`https://www.nseindia.com/*` now answers with a **301 to `https://www.nseindia.in/*`**. It only does this if the request carries a full browser header set; with fewer headers Akamai returns 403 "Access Denied". Archives are on `nsearchives.nseindia.in` and attachment URLs point there too. The old `nsearchives.nseindia.com` still serves CSVs.
On `www.nseindia.in`, the `/api/corporate*` endpoints work **without a cookie** if you send a browser User-Agent plus `Accept`, `Accept-Language` and `Referer`. That holds over both HTTP/1.1 (so Python `urllib` works) and HTTP/2. A bare curl UA or `Python-urllib` UA gets an HTTP/2 stream reset. `quote-equity` (live prices) stays 403 even after a homepage cookie visit: it is protected by bot-manager. The old `www1.nseindia.com` gives a TLS failure.

### Endpoint table (status as tested 2026-11-19)
| # | Source / data | Endpoint (GET) | Headers needed | Result | Sample of output |
|---|---|---|---|---|---|
| 1 | NSE corporate announcements, per symbol | `https://www.nseindia.in/api/corporate-announcements?index=equities&symbol=KPITTECH` | Browser UA, Accept json, Accept-Language, Referer `https://www.nseindia.in/` | **WORKS**, 200, 727 rows back to 2019 in one call (~62 KB gz) | `{"an_dt":"18-Nov-2026 18:34:15","desc":"Analysts/Institutional Investor Meet/Con. Call Updates","attchmntFile":"https://nsearchives.nseindia.in/corporate/KPITTECH_...pdf","attchmntText":"...","sm_isin":"INE04I401011","hasXbrl":true,"voiceSummary":"..."}` |
| 2 | NSE announcements, all companies by date | `.../api/corporate-announcements?index=equities&from_date=18-11-2026&to_date=19-11-2026` | same | **WORKS**, 287 KB for 2 days | same schema |
| 3 | NSE shareholding pattern (history) | `.../api/corporate-share-holdings-master?index=equities&symbol=KPITTECH` | same | **WORKS** | `{"date":"30-SEP-2026","pr_and_prgrp":"38.6","public_val":"60.82","employeeTrusts":"0.58","broadcastDate":"15-OCT-2026 18:07:16",...}` |
| 4 | NSE pledge / encumbrance (Reg 31) | `.../api/corporate-pledgedata?index=equities&symbol=KPITTECH`; omit symbol for all companies (127 KB) | same | **WORKS** | `{"numSharesPledged":"9953935","percPromot...","broadcastDt":"19-Nov-2026 16:31:28"}` |
| 5 | NSE SAST Reg 29 (substantial acquisitions/sales) | `.../api/corporate-sast-reg29?index=equities&symbol=KPITTECH` | same | **WORKS** | `{"acqNameList":[...promoters...],"data":[{"acqSaleType":"Sale",...}]}` |
| 6 | NSE insider trading (PIT Reg 7) | `.../api/corporates-pit?index=equities&symbol=KPITTECH` | same | **WORKS** per symbol. The all-market date-range form (`&from_date=..&to_date=..`) came back **empty** in this test: use per-symbol calls. | `{"acqName":"...","acqMode":"ESOP","befAcqSharesNo":"1919589","afterAcqSharesNo":"1916889","anex":"7(2)"}` |
| 7 | NSE financial results list | `.../api/corporates-financial-results?index=equities&symbol=KPITTECH&period=Quarterly` | same | **WORKS**: list with filing times, audited flag, consolidated flag and XBRL links | `{"audited":"Un-Audited","consolidated":"Non-Consolidated","financialYear":"01-Apr-2024 To 31-Mar-2025",...}` |
| 8 | NSE bulk deals (history) | `.../api/historicalOR/bulk-block-short-deals?optionType=bulk_deals&from=01-11-2026&to=19-11-2026` | same | **WORKS** | `{"BD_DT_DATE":"02-NOV-2026","BD_SYMBOL":"AARTECH","BD_CLIENT_NAME":"...","BD_BUY_SELL":"BUY","BD_QTY_TRD":189020,"BD_TP_WATP":40.92}` |
| 9 | NSE block deals (history) | same with `optionType=block_deals` | same | **WORKS** | `{"BD_SYMBOL":"GALLANTT","BD_CLIENT_NAME":"DINESH R AGARWAL","BD_BUY_SELL":"SELL","BD_QTY_TRD":5000000,"BD_TP_WATP":501}` |
| 10 | NSE today's large deals | `.../api/snapshot-capital-market-largedeal` | same | **WORKS** | `BULK_DEALS_DATA`, `BLOCK_DEALS_DATA` |
| 11 | NSE today's bulk/block CSV | `https://nsearchives.nseindia.com/content/equities/bulk.csv`, `block.csv` | Browser UA | **WORKS** | `Date,Symbol,Security Name,Client Name,Buy/Sell,Quantity Traded,Trade Price / Wght. Avg. Price,Remarks` |
| 12 | NSE equity master list | `https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv` | Browser UA | **WORKS** (62 KB) | symbol, name, ISIN, listing date |
| 13 | NSE market status | `.../api/marketStatus` | same | **WORKS** | NIFTY last 25514.3 on 19-Nov-2026 |
| 14 | NSE live quote | `.../api/quote-equity?symbol=X` | needs a real browser session | **BLOCKED** (403 even with homepage cookies) | use BSE `getScripHeaderData` instead |
| 15 | NSE old endpoints | `historical/bulk-deals`, `www1.nseindia.com` | n/a | **DEAD** (HTML stub / TLS error) | n/a |
| 16 | NSE attachment PDFs | `https://nsearchives.nseindia.in/corporate/<file>.pdf` | Browser UA | **WORKS**: 492 KB transcript; `pdftotext -layout` gave 8,530 words of clean, speaker-labelled text | see transcripts section |
| 17 | BSE announcements per scrip | `https://api.bseindia.com/BseIndiaAPI/api/AnnSubCategoryGetData/w?pageno=1&strCat=-1&strPrevDate=20261101&strScrip=532400&strSearch=P&strToDate=20261119&strType=C&subcategory=-1` | **HTTP/2 required.** Browser UA, `Accept-Language`, `Accept-Encoding: gzip, deflate, br`, `Sec-Fetch-Mode: cors`, `Sec-Fetch-Site: same-site`, `Sec-Fetch-Dest: empty`, `Referer: https://www.bseindia.com/`. Without Sec-Fetch headers, or over HTTP/1.1, you get Akamai 403. | **WORKS** (with headers) | `{"NEWSSUB":"Announcement under Regulation 30 (LODR)-Earnings Call Transcript","ATTACHMENTNAME":"c2af3076-....pdf","CATEGORYNAME":"Company Update","NEWS_DT":"2026-11-04T16:12:14"}` |
| 18 | BSE announcements, all scrips for a day | same URL with `strScrip=` (empty), paged by `pageno` | same | **WORKS** | `Table` + `Table1.ROWCNT` |
| 19 | BSE attachment PDF | `https://www.bseindia.com/xml-data/corpfiling/AttachLive/<ATTACHMENTNAME>` (recent), `/AttachHis/` (older). `stockinfo/AnnPdfOpen.aspx?Pname=` redirects to AttachHis. | same | **WORKS** (558 KB PDF) | n/a |
| 20 | BSE company header (PE, ROE, ISIN, industry) | `.../api/ComHeadernew/w?quotetype=EQ&scripcode=532400&seriesid=` | same | **WORKS** | `{"SecurityId":"BSOFT","PE":"19.34","ROE":"27.87","Industry":"Computers - Software & Consulting"}` |
| 21 | BSE price | `.../api/getScripHeaderData/w?Debtflag=&scripcode=532400&seriesid=` | same | **WORKS** | `{"CurrRate":{"LTP":"298.45","PcChg":"-1.14"}}` |
| 22 | BSE results calendar (upcoming board meetings) | `.../api/Corpforthresults/w` | same | **WORKS** | `{"short_name":"KRRAIL","meeting_date":"19 Nov 2026"}` |
| 23 | BSE quarterly results snapshot | `.../api/TabResults_PAR/w?scripcode=532400&tabtype=RESULTS` | same | **WORKS** (JSON-in-string) | Revenue Sep-26 858.39 Cr, Net Profit 120.46 Cr |
| 24 | BSE shareholding filings list + XBRL | `.../api/SHPQNewFormat/w?scripcode=532400&qtrid=&Type=EQ`; summary `ShpSecSummery_New/w?qtrid=&scripcode=532400` (HTML in JSON) | same | **WORKS** | `{"qtr":"September 2026","XbrlFile":"532400_..._SHP.xml","filing_date_time":"2026-10-20T09:58"}` |
| 25 | BSE corporate actions | `.../api/CorporateAction/w?scripcode=532400` | same | **WORKS** | dividends with dates |
| 26 | BSE bulk/block, `Sharehold_patternN` | `.../api/BulkblockDeal/w...` | n/a | **302 to error page** (wrong params or retired). Use NSE #8–#11. | n/a |
| 27 | screener.in company page | `https://www.screener.in/company/KPITTECH/consolidated/` | Browser UA | **WORKS without login.** The "Concalls" section lists Transcript (BSE AnnPdfOpen link), PPT and REC (company-hosted mp3) per quarter. "AI Summary" and "Notes" are buttons for logged-in users. Credit-rating links are also visible (e.g. ICRA rationale links). | `('...AnnPdfOpen.aspx?Pname=a7331811-...pdf','Transcript')` |
| 28 | ICRA rationale | `https://www.icra.in/Rationale/ShowRationaleReport/?Id=141659` is an HTML shell; the PDF is at `https://www.icra.in/Rating/ShowRationalReportFilePdfViewer/141659` | Browser UA | **WORKS** (9-page PDF, 890 KB) | n/a |
| 29 | CRISIL rationale | `https://www.crisil.com/mnt/winshare/Ratings/RatingList/RatingDocs/<CompanyName>_<Month DD_ YYYY>_RR_<id>.html` (find via web search or the company's exchange filing) | Browser UA | **WORKS**: plain HTML, about 27 K chars of text including "Key Rating Drivers", "Liquidity" and "Outlook" | `Tega Industries Limited Ratings continues on 'Watch Developing'` |
| 30 | CARE Ratings | `https://www.careratings.com/` and its search page | Browser UA | Pages load (JS-heavy); no simple JSON endpoint found. Use the exchange "Credit Rating" filings or screener links. | n/a |
| 31 | India Ratings | `https://www.indiaratings.co.in/` | n/a | **SPA shell only** (7 KB); data is behind JS. Not scriptable with curl; use the exchange "Credit Rating" filings. | n/a |

Rate limits: neither exchange publishes limits and no `X-RateLimit` headers were seen (BSE sends `Cache-Control: max-age=60`). Community experience says Akamai blocks an IP for minutes to hours after bursts. Policy in our helpers: **at least 1.5 s between requests**, back off exponentially on 403/429, cache everything locally, and pull bulk by date range rather than per symbol where the endpoint allows it.

### Concall transcripts: where they live
- **The exchange filing is the canonical source.** SEBI LODR (Reg 46 amendment 2021; Reg 30/Sch III amendment June 2023) requires transcripts on the company website and with the exchanges within 5 working days, and audio/video recordings promptly. The 2023 text says the next trading day or 24 h; secondary sources differ, so check the consolidated regulation. Sources: [Vinod Kothari guide](https://vinodkothari.com/2021/07/step-by-step-guide-for-disclosure-for-analysts-investors-meet/), [Khaitan 2023 note](https://www.khaitanco.com/sites/default/files/2023-06/SEBI%20enhances%20disclosure%20and%20governance%20requirements%20of%20listed%20entities_1.pdf).
- NSE: in the announcements JSON, filter `desc == "Analysts/Institutional Investor Meet/Con. Call Updates"` and `"ranscript" in attchmntText` (this catches typos like "ransacript"). KPITTECH had 17 such filings.
- BSE: `NEWSSUB` contains "Earnings Call Transcript".
- screener.in: the Concalls section is visible **without login**, with Transcript, PPT and REC links per quarter. Transcript links go to BSE `AnnPdfOpen`. AI Summary needs login. Good as a cross-check index of which quarters exist.
- Extraction: `pdftotext` (poppler) **is installed**. `pdftotext -layout` on KPIT Q2FY27 (20 pages) gave 8,530 words with speaker labels ("Kishor Patil:", "Moderator:"). That is enough to split management remarks from Q&A. Micro-cap scanned PDFs need OCR (tesseract, not tested).
- Sample promise found in the KPIT Q2FY27 call (28-Oct-2026), as an example of a tracker item: an analyst asked whether EBITDA margins would return to the 20–21% range. The CEO replied: "it will go up to some extent, every quarter, but, it will be early next year when we get there." Tracker entry: metric = EBITDA margin; target = about 20–21%; deadline = early CY2027; specificity = medium (range given, date vague); check each quarter's result.

### Credit rating rationales
- ICRA: **works**. Use `icra.in/Rating/ShowRationalReportFilePdfViewer/<Id>` for the PDF; the Id comes from the rationale URL.
- CRISIL: **works**. Plain HTML at `crisil.com/mnt/winshare/Ratings/RatingList/RatingDocs/...html`; discover the URLs via web search or the company's exchange "Credit Rating" filing.
- CARE: site loads, JS-heavy, no clean endpoint found. India Ratings: JS SPA, **not curl-able**.
- Best universal route: the Reg 30 "Credit Rating" exchange announcements plus the links on the screener company page.

### Alternative data (tested 2026-11-19 from a non-Indian cloud IP)
Several Indian government hosts **reset connections from foreign IPs**, so they are probably geo-blocked. They should be retested from an Indian residential connection before being written off.

| Data | Endpoint tested | Result | Use |
|---|---|---|---|
| Vahan vehicle registrations (maker, fuel, state) | `analytics.parivahan.gov.in/analytics/publicdashboard/vahan` | **Page loads** (222 KB; total registration counter visible). Maker-wise tables come through JSF/PrimeFaces AJAX postbacks with ViewState, so scripting means replaying the form. The older `vahan.parivahan.gov.in/vahan4dashboard/...reportview.xhtml` gives **connection reset** (geo-block). | Monthly or even daily 2W/PV/CV/tractor/EV share by OEM, for auto, auto-ancillary and EV small caps. The best free real-time India alt-data. |
| FADA monthly retail auto sales | `www.fada.in/press-release-list.php`, with PDFs at `images/press-release/*.pdf` | **WORKS** (Oct-26 PDF linked) | Vahan-based retail by OEM, released monthly about the 5th–7th. |
| SIAM wholesale despatches | `www.siam.in` | **WORKS** (HTML) | Compare wholesale with retail (FADA) to catch channel stuffing. |
| Power generation / coal stocks | `npp.gov.in` (National Power Portal) | **WORKS**: "Daily Generation on 17-Nov-2026", daily coal status | Power demand proxy for industrial activity, plus coal-stock stress. |
| CEA | `cea.nic.in` | **WORKS** (home); report links are `/public/link-report/view?mappingId=...` | Monthly generation and installed capacity. |
| Grid-India (ex-POSOCO) daily PSP report | `grid-india.in`, `report.grid-india.in`, `posoco.in` | **BLOCKED** (reset / CONNECT 502) | Daily peak demand; use NPP instead. |
| Petroleum product consumption | `ppac.gov.in/consumption/products-wise` | **WORKS** (links present) | Diesel, ATF and bitumen are road-construction and freight proxies. |
| GST collections | `www.gst.gov.in/download/gststatistics` | **Partial**: page loads (3.7 KB shell); `www.gst.gov.in` root resets. Monthly figures come out in a press release (PIB/news) on the 1st. | Macro only; little company-level value. |
| e-way bills | `ewaybillgst.gov.in`, `docs.ewaybillgst.gov.in` | **BLOCKED** (reset/403) | Monthly totals get reported in the news. |
| Port traffic | `ipa.nic.in` reset; `shipmin.gov.in` works | **Partial** | Major-port cargo by commodity (monthly); company port data via Adani/JSW disclosures. |
| Core-sector index (cement, steel, coal, power...) | `eaindustry.nic.in` | **TLS chain broken** (server misconfig; not bypassed). Cement/steel monthly YoY also appear via PIB press release. | Cement and steel volumes by month. |
| Steel (JPC) | `jpcindia.nic.in` reset; `steel.gov.in` works | **Partial** | Steel production/consumption. |
| Google Trends | Explore API `trends.google.com/trends/api/explore` returns **429** (cloud IPs throttled); `trends.google.com/trending/rss?geo=IN` **works** (daily trending RSS) | Partial | Brand/product search interest needs a residential IP or manual browser use. |
| App downloads | Google Play detail page (`play.google.com/store/apps/details?id=...&gl=IN`) | **WORKS**: install bucket, e.g. "100M+ Downloads" | Only coarse buckets plus rating counts; precise downloads (Sensor Tower, Appfigures) are paid. Track rating-count growth as a proxy. |
| Job postings | `naukri.com` home 200 (JobSpeak index is published monthly as a press release); `indeed.com` 401 | Partial | Hiring by company: scrape the company careers page or LinkedIn by hand (scuttlebutt). JobSpeak gives sector hiring trends. |
| UPI / NPCI stats | `npci.org.in` **403** | Blocked | Monthly totals reported in news. |
| data.gov.in API | `api.data.gov.in` reset, `data.gov.in` 503/reset | **BLOCKED** from here | Needs a free API key and probably an Indian IP. |
| Trade (exports/imports by HS code) | `tradestat.commerce.gov.in` | **WORKS** (shell) | HS-code export trends for chemicals, pharma and engineering exporters. |

Practical takeaway: for a small-cap memory system, **exchange filings (NSE/BSE) carry roughly 90% of the value** and are fully scriptable. Sector alt-data that is reachable and useful: Vahan/FADA (autos), NPP/CEA (power), PPAC (fuel), Play-store buckets (consumer apps), tradestat (exporters). Most other government portals need an Indian IP; run those fetches from the user's own machine.

### Helper scripts (tested working 2026-11-19)
- `tools/nse_fetch.py`: stdlib `urllib` against `www.nseindia.in`. Commands: `announcements`, `transcripts [--download DIR]`, `shareholding`, `pledge`, `sast`, `insider`, `results`, `bulk`, `block`. In testing it returned 17 KPIT transcripts, 70 bulk deals for 15–19 Nov, and 20 PIT rows.
- `tools/bse_fetch.py`: stdlib plus a `curl --http2` subprocess, because BSE refuses HTTP/1.1. Commands: `announcements`, `transcripts [--download DIR]`, `header`, `price`, `results`, `shareholding`, `actions`, `calendar`. In testing it downloaded 4 Birlasoft 2026 transcripts.
- Both space requests at least 1.5 s apart and back off exponentially on 403/429/503. Run with `python3 -I`. Downloaded PDFs are untrusted: store them in their own directory and extract with `pdftotext -layout`.
- Fragility: both exchanges change hosts and paths without notice (NSE's move from .com to .in is the latest example). Re-run the self-test commands each quarter.

---

## Part B: methods (sourced)

### 1. What the research says about text, tone and credibility
| Finding | Paper | What it means for us |
|---|---|---|
| Firms that **change** their 10-K/10-Q text from the prior year underperform. The short-"changers", long-"non-changers" portfolio earned up to 188 bp/month (about 22%/yr) when changes were in the risk-factor section; typical value-weighted figures are 34–58 bp/month. Returns build over up to 18 months with **no announcement reaction**, so investors are inattentive. Changes in CEO/CFO, litigation and negative-sentiment wording predict the most. | Cohen, Malloy & Nguyen, "Lazy Prices", *J. Finance* 75(3) 2020, 1371–1415 ([NBER w25084](https://www.nber.org/papers/w25084), [digest](https://www.nber.org/digest/nov18/are-investors-inattentive-sec-mandated-corporate-reports)) | Diff every Indian annual report (MD&A, risk, contingent liabilities, RPT notes, auditor's report) and every concall against the prior one. Most changes are boring; flag *unusual* change size. This is exactly an AI-at-scale task, and Indian small caps get even less attention than US firms. |
| General dictionaries misclassify finance words: about 3/4 of Harvard-IV "negative" words are not negative in 10-Ks. The LM finance-specific negative list (2,337 words) correlates with filing returns, volatility, fraud and material weakness. Fog is a poor readability measure in finance; file size is a better proxy. | Loughran & McDonald, *J. Finance* 2011 ([SSRN](https://papers.ssrn.com/abstract=1331573)); L&M readability paper | Use the LM word lists (or an LLM) for tone, never generic sentiment. Track "uncertainty" and "weak modal" word counts over time *within the same company*. |
| Firms with lower earnings write longer, harder-to-read annual reports; easier-to-read reports go with more persistent positive earnings. | Li, "Annual report readability, current earnings, and earnings persistence", *JAE* 45 (2008) 221–247 ([RePEc](https://ideas.repec.org/a/eee/jaecon/v45y2008i2-3p221-247.html)) | A sudden rise in length or complexity of the MD&A or concall answers is a yellow flag. |
| Conference-call tone predicts abnormal returns and volume, and outweighs the earnings surprise over the following 60 days (US). | Price, Doran, Peterson & Bliss, *J. Banking & Finance* 36(4) 2012 ([RePEc](https://ideas.repec.org/a/eee/jbfina/v36y2012i4p992-1011.html)) | Tone carries information in the US... |
| **India:** 8,273 BSE-500 concall transcripts (559 firms, 2004–2019). Optimistic tone lifts short-window returns but **does not predict future operating performance**; retail investors respond most to the tone. | Jain, Khizer & Thirumalai, "Textual Disclosures and Retail Investors" ([NYU Stern PDF](https://www.stern.nyu.edu/sites/default/files/assets/documents/Jain%20Khizer%20Thirumalai%20-%20Textual%20Disclosures%20and%20Retail%20Investors.pdf), [NSE white paper](https://nsearchives.nseindia.com/s3fs-public/inline-files/Retail%20Investors%20and%20Textual%20Disclosures%20-%20Jain%2C%20Khizer%20and%20Thirumalai%20-%20White%20Paper.pdf)) | ...but **in India, cheerful tone is cheap talk.** The edge is not tone scoring. It is **checking what was promised against what was delivered**. Bullish-tone-with-poor-delivery companies may be systematically overpriced. |
| Complex call language is part obfuscation and part genuine information. Analysts' own question complexity can serve as the benchmark for the legitimate part. | Bushee, Gow & Taylor, *JAR* 56(1) 2018 ([RePEc](https://ideas.repec.org/a/bla/joares/v56y2018i1p85-121.html)) | Score management *non-answers*: did the answer address the question? An LLM can judge this directly. |
| Deceptive CEOs/CFOs (later restatements) use more general-knowledge references ("you know", "everybody knows"), fewer shareholder-value references and fewer non-extreme positive words; CEOs use more *extreme* positive words. Models beat random by 6–16%, and the most-deceptive-CFO portfolio had −4% to −11% annual alpha. | Larcker & Zakolyukina, *JAR* 50(2) 2012 ([HLS forum](https://corpgov.law.harvard.edu/2012/03/21/detecting-deceptive-discussions-in-conference-calls/)) | A cheap red-flag feature: superlatives ("tremendous", "fantastic") plus evasion. Weak on its own, so use it only as one input. |
| Negative vocal affect on calls predicts misses of consensus over the next 3 quarters. | Mayew & Venkatachalam, *J. Finance* 67(1) 2012 ([Duke](https://www.fuqua.duke.edu/duke-fuqua-insights/vocal-cues-influence-company-performance)); the LVA software was **criticised as unreliable** (Lacerda) | Interesting but fragile. Indian REC mp3s exist (screener links), but this is low priority. |
| Managers with accurate past forecasts get larger analyst revisions and price reactions to new guidance. Bad-news forecasts are more credible than good-news ones. | Williams (1996, *TAR*); Hutton & Stocken (2009 WP, [Wharton](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/0207.pdf)); Rogers & Stocken (2005, *TAR*) | Credibility is a **measurable track record**, and the market prices it. Few people measure it for Indian small caps, because guidance is informal and lives only in concall text. That is our gap. |

Confidence note: effect sizes come from abstracts and digests, not full texts, apart from where cited. US results may not carry over to India; the one India study points the other way on tone.

### 2. Promise tracker: concrete schema
Unit of record = one **promise** (memdb `type: promise`), extracted from each concall, investor presentation, annual report MD&A, chairman's letter or press release.

```json
{
  "type": "promise",
  "id": "promise:KPITTECH-2026Q2-ebitda-margin-20pct",
  "tickers": ["KPITTECH"],
  "title": "EBITDA margin back to ~20-21% by early CY2027",
  "date": "2026-10-28",
  "data": {
    "source_doc": "Q2FY27 concall transcript", "source_url": "https://nsearchives.nseindia.in/corporate/KPITTECH_03112026220723_KPIT_Q2FY27_Transcript_Signed.pdf",
    "speaker": "Kishor Patil (CEO)", "quote": "it will go up to some extent, every quarter, but, it will be early next year when we get there",
    "category": "margin",            // revenue_growth | margin | capex | capacity_commissioning | order_inflow | order_book | debt_reduction | working_capital | new_product | approval_regulatory | customer_win | m&a | dividend_payout | other
    "metric": "EBITDA margin %", "baseline": null, "target_low": 20, "target_high": 21, "unit": "%",
    "deadline": "2027-03-31", "deadline_precision": "half-year",   // exact-date | quarter | half-year | fiscal-year | vague
    "specificity": 2,                // 0 vague aspiration .. 3 number+date+metric
    "unprompted": false,             // volunteered in opening remarks vs extracted by analyst question
    "conditionality": "growth accelerating in H2",
    "status": "open",                // open | delivered | partially_delivered | missed | moved_goalpost | withdrawn | superseded
    "status_history": [{"as_of":"2026-10-28","status":"open","evidence":"stated"}],
    "check_after": ["Q3FY27 results", "Q4FY27 results"],
    "resolution": null, "resolved_on": null, "delivery_ratio": null   // actual / promised
  }
}
```

**What to extract from each call.** Run an LLM pass with a fixed prompt, then a human spot-check.
1. Revenue/volume growth guidance (FY, multi-year CAGR), by segment.
2. Margin targets (EBITDA, gross, segment) and the stated drivers.
3. Capex: amount, use, **commissioning date**, peak-revenue potential, asset turn claimed.
4. Order inflow/book: targets, book-to-bill, the pipeline figure quoted, L1 positions.
5. Balance sheet: debt reduction targets, working-capital days, receivable resolution, promoter pledge release.
6. Product/approval timelines: USFDA approvals, launches, customer qualifications, PLI disbursement.
7. Capital allocation: dividend policy, buyback, M&A, fundraising.
8. **Explanations** of last quarter's miss (to test later whether the "one-off" really was one-off).
9. Things management **stopped mentioning**. Diff the topic list against prior calls, Lazy Prices style. A KPI dropped from the presentation is a strong signal.

**Scoring each resolved promise:**
- `delivered` (≥ 95% of target, on time) = +1; `partially_delivered` (≥ 70% or ≤ 1 quarter late) = +0.5; `missed` = −1; `moved_goalpost` (deadline pushed or metric redefined *without* acknowledging a miss) = −1.5; `withdrawn` with candid explanation = −0.5. "Silent drop" = −1.5.
- Weight by specificity (0–3) and materiality (share of revenue/EBIT affected).
- Beat-and-raise behaviour: consistent under-promising (delivery_ratio around 1.1–1.3) is *good*.

**Management Credibility Score (MCS)**, rolling 12 quarters:
`MCS = Σ(w_i · score_i) / Σ w_i`, where `w_i = specificity_i × materiality_i × recency_decay` (half-life about 8 quarters).
Report alongside it: hit rate, average delivery ratio, average delay in quarters, count of moved goalposts, and **candour index** (share of misses that management acknowledged unprompted in the next call).
Also track a **guidance-to-tone gap**: optimistic language (LM positive minus negative, or LLM-rated) against MCS. India evidence says the market pays for tone, so high tone with low MCS is the short-side or avoid signal, and low-key tone with high MCS is the under-recognised compounder.

**Change detectors** to run every quarter, from the endpoints above:
- Promoter pledge up, SAST promoter sale, or a PIT sell cluster near results.
- Auditor resignation or qualification; CFO change (Lazy Prices found CEO/CFO text changes predictive).
- Credit rating watch-negative or "issuer not cooperating".
- Bulk deals by known funds versus operators.
- Spike in related-party-transaction approvals in AGM notices.
- Concall topic diff (new risk words, dropped KPIs, sudden length/complexity increase).

### 3. Scuttlebutt for an individual (Fisher, Lynch, Buffett) and its legal limits
- **Fisher**, *Common Stocks and Uncommon Profits* (1958), ch. 2 "What Scuttlebutt Can Do": the business grapevine (competitors, customers, suppliers, ex-employees, research people, trade-association staff) gives an accurate picture of each company's relative strengths in an industry, built from a representative *cross-section* of opinions. It is a cross-section, not one tip. ([elearnmarkets summary](https://elearnmarkets.com/school/units/common-stocks-and-uncommon-profits/what-scuttlebutt-can-do), [TIP summary](https://www.theinvestorspodcast.com/billionaire-book-club-executive-summary/common-stocks-and-uncommon-profits/))
- **Buffett / American Express (1964)**: after the Nov-1963 salad-oil fraud (Allied Crude / De Angelis; about $150M of "collateral oil" was mostly seawater), Buffett spent an evening with the cashier at Ross's Steak House in Omaha, checking whether diners still used Amex cards. He also checked banks and stores on traveler's cheques. He concluded the franchise was intact and put about 40% of the partnership (~$13M) into the stock during 1964. ([Fortune 2012](https://fortune.com/2012/11/21/why-warren-buffetts-betting-big-on-american-express), [Fool](https://www.fool.com/investing/2017/05/27/1-stock-that-was-pivotal-in-billionaire-warren-buf.aspx)) Lesson: scuttlebutt answers *one decisive question* (is the moat damaged?), not "what will next quarter's EPS be".
- **Lynch**, *One Up on Wall Street*: invest in what you see first as a customer (the Hanes L'eggs story); pass the "two-minute drill" (category, why it will grow, what must go right, what could go wrong). ([SuperSummary](https://supersummary.com/one-up-on-wall-street/part-2-chapters-11-15-summary), [Wikipedia](https://en.wikipedia.org/wiki/One_Up_on_Wall_Street))

**Indian scuttlebutt checklist (questions that stay on generally available or observational ground):**
- *Dealers / distributors / retailers:* Which brand is gaining shelf space or counter share? Who gives the best margins and credit terms, and is that changing? Inventory days now versus 6 months ago? Do customers ask for the brand by name? Is the company pushing stock at quarter-end (channel stuffing)? How are payment terms enforced? Do they accept returns?
- *Customers (B2B):* Why did you choose them over the L1 bidder? Would you single-source? What is the switching cost? How is quality and delivery on time? Is your wallet share going up or down?
- *Suppliers:* Does the company pay on time? Are its order volumes rising? Has it asked for longer credit? (A strong early stress signal.)
- *Ex-employees (Glassdoor, LinkedIn, alumni):* Culture; how the promoter treats minority money; capex discipline; attrition in sales and R&D; **never** ask about unreleased numbers.
- *Competitors:* Who do you fear? Who is pricing irrationally? Who is losing people?
- *Physical checks:* plant visit (Is there an AGM plant tour? Is the plant running shifts? Truck queues?), job postings for the new plant, the new plant on satellite imagery (Google Earth timeline), app-store reviews, quick-commerce and e-commerce rank, a mystery-shopper visit to a showroom.
- *Records:* MCA charges register (new borrowings), court cases (eCourts), the factory licence, pollution-board consent-to-operate for the new capacity (state PCB sites list CTO/CTE approvals, which confirm capex timelines independently of management).

**Legal limits (SEBI PIT Regulations 2015):** UPSI = information about a company or its securities, not generally available, that would likely materially affect the price on becoming available [Reg 2(1)(n)]. It includes financial results, dividends, change in capital structure, M&A/delisting/disposals and KMP changes. "Generally available" = accessible to the public on a non-discriminatory basis [Reg 2(1)(e)]. The May-2024 amendment excludes *unverified* media reports from that. An "insider" is anyone in possession of UPSI, *however obtained*, so a channel check that extracts unreleased quarterly sales from a company employee makes the investor an insider. Trading while in possession is prohibited [Reg 4]; procuring or communicating UPSI is prohibited [Reg 3]. Safe practice:
1. Ask about **your own observations and the counter-party's own business** (a dealer's own stock and sales are the dealer's information, not the listed company's UPSI). Never ask an employee about unreleased company numbers, orders, deals or results.
2. If someone volunteers UPSI, **stop, write it down, and do not trade** that stock until the information is public.
3. Don't pay employees for information. Paid expert-network calls with current employees carry high risk.
4. Keep a dated scuttlebutt log of who, what and when (that is part of the memdb record) to show the mosaic was built from public pieces.
Sources: [KPMG on UPSI](https://assets.kpmg.com/content/dam/kpmg/in/pdf/2020/02/Safeguarding-UPSI.pdf), [Vinod Kothari PIT FAQ](https://vinodkothari.com/wp-content/uploads/2024/01/FAQs_Primer-on-PIT-Regulations_ver-20.08.2021.pdf), [Chambers on 2024 amendment](https://chambers.com/articles/amendments-to-the-sebi-prohibition-of-insider-trading-regulations-2015-widening-the-scope-of-un). This is not legal advice; India has no formal "mosaic theory" safe harbour, so treat this conservatively.

---

## Bottom line
- **Works and is scriptable now:** the NSE corporate APIs (announcements, shareholding, pledge, SAST, PIT, results, bulk/block) on `www.nseindia.in` with browser headers and no cookie; the BSE API over HTTP/2 with Sec-Fetch headers; transcript PDFs from both exchanges plus `pdftotext`; the screener.in Concalls index (no login needed); ICRA and CRISIL rationales; FADA, NPP, PPAC, SIAM, the Play-store install bucket, and Google Trends RSS.
- **Doesn't work from here:** NSE live quotes; India Ratings (SPA); clean CARE endpoints; Grid-India, e-way bill, IPA ports, JPC, data.gov.in, NPCI and the Trends explore API (most of these look like geo-blocks or IP throttling, so retry from an Indian IP); eaindustry (broken TLS).
- **Method:** the India evidence says concall *tone* is priced but uninformative, so the durable edge is a **multi-year promise-vs-delivery ledger, filing diffs and ownership-change alerts**, plus *targeted*, PIT-safe scuttlebutt on the few flags that matter.

Seed records: `memdb/seeds/2026-11-19_edge_methods.json` (15 records: 5 source, 7 insight, 3 strategy).
