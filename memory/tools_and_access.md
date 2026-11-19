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

## Blocked / missing
- screener.in custom raw queries need login → ask user for a Screener account (paid w/ export ideal).
- YouTube: yt-dlp blocked ("confirm you're not a bot"); youtubetotranscript 403 → need a
  transcript API key (e.g. Supadata) or browser cookies.
- businessinsider.in blocked by network; some Business Standard / ET pages 403.
- No live market data feed. Options: Zerodha Kite MCP (user account), Trendlyne MCP.
- NSE/BSE filings direct fetch not yet tested (needed for pledge/SAST and concalls).

## Wanted (user offered to provide)
Screener login, Kite MCP or Trendlyne MCP, US data API (Financial Datasets/Polygon),
transcript API.
