# Tools and access

Last updated: 2026-11-19

## Works
- screener.in company pages without login: `curl -sL https://www.screener.in/company/TICKER/consolidated/`
  (also standalone without `/consolidated/`). Price-chart API usable for closes.
- screener.in public screens (25 rows/page, `?page=N`): /screens/126864/debt-reduction/,
  /screens/226712/growth-without-dilution/, /screens/97687/capacity-expansion/,
  /screens/343087/fii-buying/, /screens/86/quarterly-growers/, /screens/57601/coffee-can-portfolio/,
  /screens/49/loss-to-profit-companies/, /screens/2/piotroski-scan/, /screens/59/magic-formula/
- Google Finance, Upstox, Kotak Neo, 5paisa, Value Research for second-source prices (via web search).
- WebSearch tool (load via ToolSearch). Subagents for parallel research.
- GitHub push to aditya-bad/fein works (it failed with 403 early in session 1, then was fixed).
- Skills: deep-research, stock-research-analyst (verification gate), barak-report-design
  (light editorial theme), contra-miltibagger-1 (turnaround screening), artifact publishing.

## NSE/BSE direct access (tested 19-Nov-2026) — see research_notes/Knowledge scout Nov 2026/edge_methods_data_access.md
- `tools/nse_fetch.py` (www.nseindia.in API, browser headers, no cookie): announcements, transcripts
  (--download), shareholding, pledge, sast, insider, results, bulk, block. Live quotes 403.
- `tools/bse_fetch.py` (api.bseindia.com, needs curl --http2): announcements, transcripts, header,
  price, results, shareholding, actions, calendar.
- Concall transcript PDFs → `pdftotext` works (KPIT Q2FY27: 8,530 words).
- Credit ratings: ICRA and CRISIL fetchable; India Ratings / CARE not (use exchange filings).
- Alt data reachable: FADA, SIAM, npp.gov.in, CEA, PPAC, tradestat, Play Store buckets, Trends RSS.
  Blocked from foreign IP: Grid-India, e-way bill, IPA ports, JPC steel, data.gov.in.
- Pledge field gotcha: use `percPromoterShares`, not `percSharesPledged`.

## US access (tested 20-Nov-2026) — see research_notes/US toolkit Nov 2026/us_toolkit.md
- `tools/sec_fetch.py`: facts (≈19 line items + forensic checks), concept, frames, filings (form/8-K item
  filter e.g. 4.01/4.02), doc, search (EDGAR full-text), insider (Form 4, 10b5-1 flag, clusters),
  holdings13f, selftest. UA "fein-research admin@example.com", ≥0.15 s between requests.
- Frames API has filer scaling errors → sanity-check outliers.
- Transcripts: Motley Fool pages + SEC 8-K exhibits work; Seeking Alpha 403.
- Prices: Yahoo v8 chart API (adjusted) works; Nasdaq API (browser UA, 10y, unadjusted); Stooq blocked.
- Scheduled tasks (create_trigger) blocked by auto-mode classifier — user must add a permission rule.

## Blocked / missing
- screener.in custom raw queries need login → ask user for a Screener account (paid w/ export ideal).
- YouTube: yt-dlp blocked ("confirm you're not a bot"); youtubetotranscript 403 → need a
  transcript API key (e.g. Supadata) or browser cookies.
- businessinsider.in blocked by network; some Business Standard / ET pages 403.
- No live market data feed. Options: Zerodha Kite MCP (user account), Trendlyne MCP.

## Wanted (user offered to provide)
Screener login, Kite MCP or Trendlyne MCP, US data API (Financial Datasets/Polygon),
transcript API.
