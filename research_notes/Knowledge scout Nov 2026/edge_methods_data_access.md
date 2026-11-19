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
