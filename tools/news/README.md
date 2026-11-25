# FEIN news layer (`tools/news/`)

Stage 3 (signals), feeding stage 4 (deep dive) and 7 (scorekeeping): a nightly list of news, rating actions,
SEBI/RBI items and sector-policy headlines for the companies we cover, with "material" items ranked first.
It answers one question: *did something happen to a name we hold a view on that the filings may not show yet?*
(lessons L40 and L45: the land lease and the ethanol tender were both missing from the company's own documents).

Standard library plus the system `curl`. No logins, no API keys, no Claude. Runs by hand in a cloud session or
nightly on the Pi (`news` job, 22:30 IST, `deploy/pi/jobs.sh`). Research, not SEBI-registered advice: an item
means "read the source", not "trade".

```
python3 news.py                       # window --since 2d (default), whole watchlist + policy list
python3 news.py --since 7d            # also 36h or 2026-11-20
python3 news.py --tickers UTTAMSUGAR,US-KEX --sources google,ratings,sebi,rbi,policy
python3 news.py --selftest            # offline: fixture RSS/HTML, temp dir only (21 checks)
```

| File | What |
|---|---|
| `news.py` | fetch, match, rank, write |
| `watchlist.csv` | `ticker,name,sector,keywords,aliases,tier`. Seeded 25-Nov-2026 with the 8 live-dive tickers (`tier=live`) and every other memdb `paper-call` ticker (Indian and `US-` prefixed). `aliases` (`;`-separated) are extra search and match terms, `keywords` are company-specific watch words (tagged `watch_keyword`). |
| `policy.csv` | `sector,label,query`: Google News keyword queries per sector (sugar cane SAP/FRP, ethanol tender/OMC, microfinance, power tariff, USFDA actions, ...). A query runs only if a watchlist row has that sector. |

Outputs, in `$FEIN_DATA/news/` (default `~/fein-data/news/`):
- `YYYY-MM-DD.csv`: `date, ticker, source, headline, url, matched_rule`. `date` is the publish time (IST). The file is
  named for the run date (IST), so a run after midnight writes the next day's file.
- `YYYY-MM-DD.md`: four sections (material with the company named in the headline; material keyword, but the headline
  does not name the company; policy watch; other company news, at most 4 per ticker) plus a per-source status table and
  the list of sources that are never automated.
- `news.sqlite`: `seen` (dedup keys), `items` (every item reported, with rules) and `runs` (per-source counts).
  **Each item is reported once**: on the run that first sees it. Dedup keys are the canonical URL and the
  normalised headline plus ticker. A story found by two queries in one run is merged, and its tickers and rules are combined.
- Log: `$FEIN_DATA/logs/news.log`.

## Sources

| source | how | status (tested 25-Nov-2026 from a cloud IP) |
|---|---|---|
| `google_news` | Google News RSS search, one query per company: `"name" OR "alias" OR TICKER when:Nd`. India edition (`hl=en-IN&gl=IN`) for Indian names, US edition for `US-` names | **works**. 90 queries, 3,912 rows over 7 days. One HTTP 429 cleared after the 10 s back-off |
| `ratings_news` | one Google News query: agency names (CRISIL, ICRA, CARE/CareEdge, India Ratings, Acuite, Brickwork, Infomerics) AND action words. Kept only when the headline names a watchlist company. Company items with an agency name in the headline are also tagged `rating` | **works** (50 to 100 rows, 0 matched our names on the first run) |
| `sebi_order`, `sebi_press` | public listing HTML on sebi.gov.in (Enforcement > Orders, `sid=2&ssid=9`; Press releases, `sid=6&ssid=23`), first page of 25 rows each, matched by company name | **works**. The page has a CAPTCHA for the *login* widget only; the listing itself is open. `sebirss.xml` is empty (323 bytes) |
| `rbi_press` | `rbi.org.in/pressreleases_rss.xml`. Items that name a watchlist company go to that company. Lender-policy titles (SFB, microfinance, NBFC, risk weight, monetary penalty, directions) go to every `sector=lender` ticker as `policy:lender` | **works** |
| `policy_news` | Google News, one query per `policy.csv` row (India edition unless the sector starts with `us`) | **works**, but noisy (foreign items, loosely related headlines). The queries are the place to tune |

**Not automated, by rule or because they cannot be fetched politely.** These are listed in every report:
- NCLT/NCLAT: CAPTCHA. Never automated.
- ICRA company search: the page loads a Barracuda/infisecure bot-protection script, and the search route returns 404.
  Single rationale PDFs (`icra.in/Rating/ShowRationalReportFilePdfViewer/<Id>`) still work when fetched by hand.
- CRISIL rating-rationale listing: the page embeds reCAPTCHA, so its listing JSON is not used. Single rationale HTML pages still work by hand.
- CARE Ratings (JS-heavy, no clean endpoint) and India Ratings (JS single-page app).
- SEBI rows beyond the newest 25 per list: older rows need the site's AJAX pager. A `--since` window longer than about a
  week can therefore miss SEBI rows.
- Exchange "Credit Rating" announcements are already covered by `tools/detectors` (`rating_downgrade`, `rating_not_cooperating`).

Anti-bot handling: a response with a Cloudflare challenge, a Google "unusual traffic" page, reCAPTCHA or hCaptcha
markers is treated as blocked. That host is then skipped for the rest of the run and noted in the report. The CAPTCHA is
never solved or bypassed. A 429 that persists after the back-off also stops that host for the run.

Politeness: one request at a time, at least 3 s between Google requests and 2 s for other hosts, and a 10 s then 20 s
back-off on 429/5xx. A full run is about 110 requests and takes about 5.5 min.

## Relevance rules (headline only; first hit = primary rule, all hits listed)

`court` (Supreme Court, High Court, court, NCLT/NCLAT, tribunal; "food court" excluded), `sebi`, `rbi`, `usfda` (warning letter,
import alert, Form 483, OAI, cGMP; **FDA approvals are tagged `usfda_nod` and are not material**), `fraud`, `raid`, `default`
(includes insolvency, Chapter 11), `downgrade`, `resignation`, `lease_licence`, `tender`, `gazette` (gazette, ordinance,
cabinet approves, notifies), `plant_shutdown`, `fire`, `strike` (also protest, agitation), `penalty` (fine, probe, investigation,
lawsuit, class action).

Other tags: `name` (the headline names the company), `query_only` (the company search matched but the headline does not name it;
mostly noise), `watch_keyword`, `rating`, `policy:<sector>:<label>`.

Ranking: material and named in the headline → material, not named → policy (material first) → other. Within each group,
live-dive names come first, then the newest.

## Known limits

- Rules read headlines only. They are keyword rules, so false positives are common ("too big to fire", a "tender offer" for
  bonds). The report is a reading list.
- Google News caps a query at about 100 items. For mega caps (`US-AAPL`, `US-NVDA`, `NTPC`) a 7-day window is truncated, while the 2-day default fits.
- Generic names need hand-picked aliases. "Kirby Corporation" must not become "Kirby", which matched a college-football coach.
  NSE codes of 8+ letters are added as search terms automatically, unless the code is a word in the name. Shorter
  codes such as HARSHA, which pulled in cricket and politics, are not.
- Google redirect URLs (`news.google.com/rss/articles/...`) are stored as-is; they open the publisher's page in a browser.
- Policy queries can return foreign or off-topic items. Add `-term` exclusions to `policy.csv` (the sugar rows exclude Pakistan).

## Adding a company

Add one row to `watchlist.csv` with the name as the press writes it, a ticker (L46: always name + ticker), the sector
(reuse a `policy.csv` sector to get its policy queries) and aliases for brand or group names (for example `Indraprastha Apollo`).
