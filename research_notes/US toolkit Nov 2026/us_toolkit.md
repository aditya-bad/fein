# US-market toolkit and knowledge — tested 20-Nov-2026

Research, not SEBI/SEC-registered advice. Everything below was tested live from our cloud session
on 2026-11-20 unless marked otherwise. Seed records: `memdb/seeds/2026-11-20_us_toolkit.json`
(21 records, not yet ingested). Tool: `tools/sec_fetch.py` (standard library only).

## 1. Tested endpoint table

SEC requests used User-Agent `fein-research admin@example.com`; the tool spaces calls at least 0.15 s apart, which keeps it under SEC's 10 req/s limit.

| # | Source / endpoint | Result | Notes |
|---|---|---|---|
| 1 | `data.sec.gov/submissions/CIK0000320193.json` | **200** (164 KB) | Metadata plus about 1,000 recent filings, with form, date, accession, 8-K `items` and primary doc. Older filings are in the paged `files[]`. |
| 2 | `data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json` | **200** (3.9 MB) | Every XBRL fact, with filed date and accession. Both restated and as-first-reported values can be recovered. |
| 3 | `data.sec.gov/api/xbrl/companyconcept/CIK0000320193/us-gaap/NetIncomeLoss.json` | **200** | 341 data points |
| 4 | `data.sec.gov/api/xbrl/frames/us-gaap/Revenues/USD/CY2024.json` | **200** | 2,513 filers. NetIncomeLoss CY2025 has 5,723 filers and includes a $1.157T scaling error, so sanity-check outliers. |
| 5 | `efts.sec.gov/LATEST/search-index?q=...&forms=...&dateRange=custom&startdt=&enddt=` | **200** | 100 hits per page, offset with `from=`. "material weakness" in 8-Ks between 1-Oct and 20-Nov-2026 gave 254 hits. "prepared remarks" in 8-Ks over the same window gave 119. |
| 6 | `www.sec.gov/files/company_tickers.json` | **200** | Ticker-to-CIK map (cached for 7 days by the tool) |
| 7 | `www.sec.gov/Archives/edgar/data/CIK/ACCNODASH/index.json` | **200** | Lists the files in a filing |
| 8 | Form 4 raw XML (`.../form4.xml`) | **200** | The `primaryDocument` in submissions points to the XSL-rendered copy (`xslF345X06/...`). The raw `.xml` sits at the filing root. The `aff10b5One` element carries the 10b5-1 flag. |
| 9 | 13F-HR information table (`.../60471.xml` for Berkshire) | **200** | This is the non-`primary_doc.xml` XML. Berkshire's 30-Sep-2026 filing has 30 positions worth $304.2B. |
| 10 | 10-K / DEF 14A / 8-K HTML docs | **200** | The Apple 10-K text extracted cleanly with `doc --text` |
| 11 | EDGAR atom feed `cgi-bin/browse-edgar?...&output=atom` | **200** | Not needed, because submissions JSON covers it |
| 12 | Motley Fool `fool.com/earnings-call-transcripts/` and transcript pages | **200** | Full call text including Q&A (about 4,750 words in the example). Needs a browser UA. |
| 13 | SEC 8-K EX-99.x prepared remarks / shareholder letters | **200** | Found via full-text search (e.g. Snap EX-99.2). Official text, but no Q&A. |
| 14 | Seeking Alpha transcripts | **403** | PerimeterX captcha, and paywalled anyway |
| 15 | Company IR (investor.apple.com), roic.ai | **403** | Cloudflare challenge |
| 16 | discountingcashflows.com transcripts | **405** | Human verification |
| 17 | nasdaq.com earnings page | **200** | Next-earnings-date API answers but is often empty |
| 18 | Yahoo `query1.finance.yahoo.com/v8/finance/chart/AAPL?period1=0&period2=9999999999&interval=1d&events=div,split` | **200** | Full history (11,578 AAPL bars), with adjclose, dividends and splits. No crumb needed. |
| 19 | Yahoo `v10/finance/quoteSummary` | **401** | "Invalid Crumb", so not usable without cookies |
| 20 | Nasdaq `api.nasdaq.com/api/quote/AAPL/historical?assetclass=stocks&fromdate=&todate=&limit=9999` | **200** with a browser UA | Fails with a curl UA. Limited to 10 years of unadjusted closes. AAPL closed at $349.21 on 19-Nov-2026. |
| 21 | Stooq CSV `stooq.com/q/d/l/?s=aapl.us&i=d` | **blocked** | Now serves a JavaScript browser check |
| 22 | Ken French data library and CSV zips | **200** | Built from CRSP data through Sep-2026 |
| 23 | Jay Ritter `IPO-Statistics.pdf` | **200** | Tables updated Feb-2026. `pdftotext -layout` extracts them cleanly. |
| 24 | spglobal.com SPIVA pages and PDFs | **403** | SPIVA numbers came via web search and a press article |

## 2. `tools/sec_fetch.py`

```
python3 tools/sec_fetch.py selftest                       # 8 live checks — ALL PASS on 2026-11-20
python3 tools/sec_fetch.py facts AAPL [--quarterly] [--years N] [--csv f] [--raw]
python3 tools/sec_fetch.py concept AAPL us-gaap NetIncomeLoss
python3 tools/sec_fetch.py frames Revenues CY2024 --top 20
python3 tools/sec_fetch.py filings AAPL --form 10-K,10-Q,8-K,"DEF 14A",S-1,4 [--items 4.01,4.02] [--all]
python3 tools/sec_fetch.py doc AAPL <accession> --list | --out f [--file name] [--text]
python3 tools/sec_fetch.py insider AAPL --limit 40 [--since YYYY-MM-DD] [--out f.json]
python3 tools/sec_fetch.py holdings13f 1067983 [--accession X] [--top 30]
python3 tools/sec_fetch.py search '"going concern"' --forms 10-K --from 2026-01-01 --to 2026-11-20 [--ciks AAPL] [--page 2]
```

What `facts` covers: it merges fallback XBRL tags for revenue, gross profit, operating income, net
income, diluted EPS, CFO, capex, FCF (derived), SBC, buybacks, dividends, diluted shares, shares
outstanding, cash, long-term debt, equity, goodwill, receivables and inventory. Where a value was
amended, the latest filing wins. It also prints automatic checks: SBC/FCF, CFO/NI, change in
diluted shares, and receivables growth vs revenue growth.

What `insider` covers: it parses the raw Form 4 XML into transaction code, shares, price, value
and the 10b5-1 flag. It sums open-market buys and sells separately from off-plan sells, and it
flags clusters of three or more distinct insiders trading within 30 days.

What `holdings13f` covers: it finds the info-table XML, aggregates by issuer/CUSIP/put-call and
corrects for the units change (thousands of dollars before 2023-01-03, whole dollars after).

Gotchas:
- 10-Q cash flows are year-to-date, so `--quarterly` CFO is mostly blank.
- Fiscal Q4 is not filed as a standalone quarter. Derive it as FY minus 9M.
- Form 4 codes M and A carry a price of 0.

Sample outputs (XBRL as filed):

| | Apple FY to 26-Sep-2026 | Snowflake FY to 31-Jan-2026 |
|---|---|---|
| Revenue | $478.83B | $4.68B |
| Net income | $132.18B | –$1.33B |
| CFO | $145.10B | $1.22B |
| FCF | $136.06B | $1.12B |
| SBC | $13.79B (10% of FCF) | $1.60B (143% of FCF) |
| Diluted share count, YoY | –1.9% | +1.4% (after $873.5M of buybacks) |

These are single-source figures from SEC XBRL. Cross-check them before using any of them in a report.

## 3. Base rates (computed by us from primary data where possible)

### IPOs: Ritter, 9,253 US IPOs 1980–2024, 3-year buy-and-hold measured from the first close

| Group | Raw | vs market | vs style |
|---|---|---|---|
| All IPOs | +19.1% | –20.5% | –8.9% |
| Unprofitable | –0.5% | –30.7% | –23.4% |
| Profitable | +33.6% | –13.0% | +1.8% |
| Sales < $10m | –16.2% | –52.3% | –34.0% |
| Sales $100–500m | +39.1% | –2.6% | +5.4% |

Distribution of 3-year returns (1975–2021):

| Outcome | Share of IPOs |
|---|---|
| Lost more than half | 38.5% |
| Lost money (any amount) | 60.0% |
| Gained more than 1,000% (11x+) | 0.5% |
| Lost more than half, IPOs with sales ≥ $100m | 25.9% |

The mean 3-year return is 38.1% but the median is only 2.6%.

### Size: Ken French value-weighted deciles, compounded annual return

| Period | Smallest 10% | Largest 10% |
|---|---|---|
| 1926–Sep 2026 | 12.1% | 10.1% |
| 1926–1979 | 13.6% | 8.2% |
| 1980–2026 | 10.4% | 12.3% |
| 1980–1999 | 11.9% | 18.2% |
| 2000–09 | 8.9% | –2.3% |
| 2010–19 | 8.6% | 13.6% |
| 2020–Sep 2026 | 10.4% | 16.5% |
| Max drawdown | –89% | –82% |

### Factors: compounded annual long-short return, % (2026 runs to September)

| Decade | Mkt-RF | SMB | HML (value) | MOM | RMW (profit.) | CMA (invest.) |
|---|---|---|---|---|---|---|
| 1927-39 | 2.0 | 3.4 | 1.3 | -0.4 | – | – |
| 1940s | 9.0 | 4.5 | 9.6 | 6.4 | – | – |
| 1950s | 16.2 | -0.9 | 3.3 | 10.9 | – | – |
| 1960s* | 4.2 | 4.5 | 3.2 | 11.1 | 1.3 | -1.2 |
| 1970s | -0.3 | 2.8 | 7.7 | 9.3 | -0.7 | 6.2 |
| 1980s | 7.3 | -0.4 | 5.6 | 8.6 | 4.9 | 5.5 |
| 1990s | 12.5 | -2.1 | -0.4 | 13.7 | 2.2 | -0.1 |
| 2000s | -3.1 | 4.2 | 7.4 | -2.0 | 7.6 | 6.5 |
| 2010s | 13.0 | -0.5 | -2.6 | 2.6 | 1.2 | 0.1 |
| 2020-26 | 11.9 | -2.8 | 0.7 | 2.5 | 1.7 | 0.1 |
| 1964-2006 | 4.6 | 2.3 | 5.4 | 9.1 | 2.7 | 4.1 |
| 2007-2026 | 9.4 | -1.0 | -2.0 | 0.3 | 2.6 | -0.1 |

\*RMW and CMA start in Jul-1963.

What the factor table shows: value and momentum have gone flat for about 20 years. Profitability
(RMW) is the steadiest premium.

### SPIVA US year-end 2025 (verified from two sources)

| Measure | Share that lagged the benchmark |
|---|---|
| Large-cap funds vs S&P 500, 1 year | 79% (65% in 2024) |
| Large-cap funds, 3 years | 67% |
| Large-cap funds, 5 years | 89% |
| Mid-cap funds, 2025 | 55% |
| Small-cap funds, 2025 | 41% |
| Institutional accounts, gross of fees | 67% |

The 15- and 20-year figures for YE2025 could not be fetched because spglobal.com returns 403.

## 4. US red flags in SEC filings (details are in the seed records)

| Flag | Where to look | Tool |
|---|---|---|
| Going concern / "substantial doubt" | Auditor report (Item 8), Note 1, MD&A liquidity | `search '"substantial doubt"'` |
| Material weakness in internal controls (ICFR) | Item 9A; auditor's ICFR opinion (none at non-accelerated filers or EGCs) | `search '"material weakness"'` |
| Auditor change | 8-K Item 4.01, Exhibit 16.1 letter, 10-K Item 9 | `filings --form 8-K --items 4.01` |
| Restatement (non-reliance) | 8-K Item 4.02 | `--items 4.02` |
| Late filing | NT 10-K / NT 10-Q | `filings --form "NT 10-K"` |
| Related parties | Related-party footnote (ASC 850); DEF 14A Item 404 disclosure (>$120k) | `filings --form "DEF 14A"`, `doc --text` |
| Non-GAAP gap | 8-K EX-99.1 reconciliation compared with XBRL GAAP net income | `facts` plus `doc` |
| SBC dilution | SBC/revenue, SBC/FCF, diluted share trend | `facts` (auto-checks) |
| Insider selling clusters | Form 4: off-plan, 3+ insiders within 30 days, CFO/GC sales | `insider` |
| Dilution pipeline | S-1, S-3, 424B5, ATM programs | `filings --form S-3,424B5` |

## 5. Insider and 13F evidence

- **Lakonishok and Lee (RFS 2001):** insider purchases are informative, especially in small firms. Insider sales are not.
- **Cohen, Malloy and Pomorski (JF 2012):** trades by "opportunistic" insiders earn about 82 bp a month (value-weighted). Trades by "routine" insiders earn about 0.
- **13F filings:** they are lagged by up to 45 days and show long positions only. Use them for idea sourcing and crowding checks, not for cloning. The best-ideas and 13D-activism findings have not been verified yet.

## 6. How the US differs from India

- **Control:** the US has no promoter groups or pledge data. Control risk shows up instead as founder dual-class shares and activist 13D stakes.
- **Pay:** SBC is a major cost in the US.
- **Capital return:** buybacks are the main route. They carry a 1% excise tax since 2023.
- **Shorting and options:** short-selling is mainstream and short interest is disclosed. The single-stock options market is deep.
- **Efficiency:** US large caps are very efficient, so any edge is more plausible in under-covered small caps and in forensic filing work.
- **Data:** XBRL coverage, full-text search and coded 8-K items make systematic screening much cheaper than in India.
- **Not yet checked:** taxes and LRS rules for an Indian resident.

## 7. Next steps (suggested)

1. Ingest the seed file: `python3 -m memdb add --json-file memdb/seeds/2026-11-20_us_toolkit.json`.
2. Add to `memory/tools_and_access.md`: sec_fetch.py; the Yahoo chart and Nasdaq historical APIs as US price sources; Fool for transcripts; Seeking Alpha, Stooq and SPIVA site blocked.
3. Back-test the insider-buy filter (opportunistic + cluster + small-cap) on Form 4 history before treating it as edge.
4. Verify the SPIVA 15/20-year figures, plus the 13F best-ideas and 13D evidence.
5. Check LRS, tax and US estate-tax rules for the user before any US allocation.
