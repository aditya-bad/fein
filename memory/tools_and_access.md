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

## Change detectors (21-Nov-2026) — tools/detectors/ (ready for the Raspberry Pi)
- collect.py (NSE+BSE announcements, PIT, SAST, pledge snapshot, bulk/block → SQLite WAL) and detect.py
  (pledge changes/crossings, invocations, insider buy/sell & clusters, auditor/CFO/CEO/CS exits, rating
  downgrades/non-cooperation, default keywords, insolvency, big deals) → $FEIN_DATA/alerts/. --selftest passes.
- Live test 18–20 Nov: 72 alerts; peak memory 39.5 MB. Pledge rules need ≥2 daily snapshots.
- **NSE PIT insider feed has no records after 30-Apr-2026** (BSE insider endpoint empty too) — insider rules
  dormant until it resumes; SAST promoter trades still captured.

## Promise-tracker pipeline (21-Nov-2026) — tools/promise_tracker/pipeline/ (Pi-ready, stdlib + pdftotext/curl)
fetch → turns → candidates (rules) → llm_extract (`claude -p` or Gemini CLI) → score (vs screener) → report; run.py
runs all with a human-override file. Validation vs manual pilots (SKIPPER/UNIPARTS): formula reproduces pilot scores
exactly; rules+LLM recall 85–87%, precision ≥36–40% (lower bound; LLM over-extracts ~3×); auto-scorable vs
screener only ~30% of promises (segment/order-book/capex need results-PDF CSVs next); judgment items (status of
non-financial promises, goalpost vs missed, candour) still need human/LLM review.

## Scoreboard (22-Nov-2026) — tools/scoreboard/ (Pi-ready)
calls.py (export + classify), resolve.py (only on real data; India needs 2 sources same side of threshold;
event NO/text numbers = proposals for review), scoreboard.py (Brier/log-loss vs base rates, calibration bins →
research_notes/Scoreboard/scoreboard.md + curriculum.md SCOREBOARD block), apply.sh, run_daily.sh (cron 22:00 IST).
Calendar: research_notes/Scoreboard/calendar.md/.ics. First due 31-Jan-2027.

- `tools/nse_fetch.py annual_reports SYMBOL [--download DIR]` (NSE api/annual-reports; pre-FY24 dates from file-name stamp) — added 23-Nov-2026.

## Blocked / missing
- screener.in custom raw queries need login → ask user for a Screener account (paid w/ export ideal).
- YouTube: yt-dlp blocked ("confirm you're not a bot"); youtubetotranscript 403 → need a
  transcript API key (e.g. Supadata) or browser cookies.
- businessinsider.in blocked by network; some Business Standard / ET pages 403.
- No live market data feed. Options: Zerodha Kite MCP (user account), Trendlyne MCP.

## Wanted (user offered to provide)
Screener login, Kite MCP or Trendlyne MCP, US data API (Financial Datasets/Polygon),
transcript API.

## 25-Nov-2026 fixes
- **BSE announcements:** HTTP 400 was the date window, not pagination — with a scrip code the range must be ≤1 calendar year;
  without a scrip code, >1 day silently returns 0 rows. bse_fetch.py now splits windows, pages fully, dedupes NEWSID (`selftest [--live]`).
- **Bank XBRL (IFBanking taxonomy):** scoreboard reads InterestEarned, ProfitLossForThePeriod, GNPA/NNPA, CET1/AT1, ROA, advances,
  deposits. No total CRAR, loan portfolio, NIM or credit-cost tag → those calls stay assisted. NBFC filings have no GNPA tag.

## 26-Nov-2026: Gemini CLI personal login is dead → use Antigravity CLI (`agy`)
Google stopped serving Gemini CLI for individual / AI Pro / AI Ultra accounts on 18-Jun-2026 (Code Assist release notes);
the CLI shows "This client is no longer supported for Gemini Code Assist for individuals". Successor: Antigravity CLI,
`curl -fsSL https://antigravity.google/cli/install.sh | bash` → `~/.local/bin/agy`; non-interactive `agy -p "..."` (unverified flags,
from secondary guides). Gemini CLI still works with a paid Gemini API key / Vertex. User's Pi: user `aditya`, Node 26 at /usr/bin
(nvm default set to system). Reported issue: agy may segfault on CPUs without AES instructions (Pi 4's Cortex-A72 lacks the ARMv8
crypto extension; Pi 5 has it) — unverified for Pi.
