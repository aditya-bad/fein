# What Claude needs from you

*Last updated: 20 Nov 2026. I keep working without any of these. Each one removes a specific limit.*
*Ordered by how much it would help. Tick an item off (`[x]`) when you've done it, and tell me.*

## High impact

- [ ] **1. Make our branch the GitHub default branch.**
  GitHub → `aditya-bad/fein` → Settings → General → Default branch → `claude/focused-brahmagupta-g3hraq`.
  *Why:* new sessions then load the memory automatically. Without this, a new session starts blank.
  After this I'll close PR #1.

- [ ] **2. YouTube / podcast transcript access.**
  For example a **Supadata** API key (supadata.ai) or a similar YouTube-transcript API.
  Add it as a credential in this environment's settings for that API's host (I'll ask for it with a secure form when you're ready, so never paste a key in chat).
  *Why:* YouTube blocks automated access from here. This unlocks investor interviews, AGM recordings,
  concall audio, Valuepickr meetups, US podcasts (Invest Like the Best, Acquired, etc.).

- [ ] **3. Screener.in account** (premium with export is ideal).
  *Why:* custom screens, full 10-year history exports, and concall AI summaries need a login.
  Option: create a separate account for research.

- [ ] **4. A connection to an Indian internet location** (your computer via Claude's Remote Control, or an India-based machine).
  *Why:* Grid-India power data, e-way bills, ports, steel and data.gov.in block foreign IP addresses.
  These are leading indicators for whole sectors.

## Medium impact

- [ ] **5. Books you own as PDFs/EPUBs**, put in a folder in the repo (e.g. `library/`), only ones you legally own.
  Examples that would help: *Common Stocks and Uncommon Profits*, *One Up on Wall Street*, *100 Baggers*,
  *The Most Important Thing*, *Margin of Safety*, *Financial Shenanigans*, *Expectations Investing*,
  *Coffee Can Investing*, *Diary of a Professional Commodity Trader*, *Valuation (McKinsey)*.
  *Why:* right now I learn from summaries. Reading the original text gives deeper and more accurate learning.

- [ ] **6. Zerodha Kite connector** (official, free) or the **Trendlyne** connector.
  *Why:* live prices, historical prices, and (Trendlyne) broker and fundamental data. These would strengthen our verification.

- [ ] **7. An embedding API key** (e.g. Voyage AI or OpenAI embeddings).
  *Why:* lets memory search by meaning, not only by exact words. That will matter as we pass thousands of records.

- [ ] **8. Your ground-level help, later.** When a deep dive needs a physical check (visiting a store, asking a
  dealer, checking a product's shelf presence or prices), I'll write you a short, specific task list.
  *Why:* this is our "security-guard depth" edge. I can't walk into a shop. Nothing needed now.

## Later / optional

- [ ] **9. A hosted database** (e.g. Supabase/Postgres) when memory passes ~50,000 records (not soon).
- [ ] **10. Permission for scheduled tasks** (`mcp__claude-code-remote__create_trigger`). You said skip this for now.
- [ ] **11. Google Scholar is blocked for bots.** I'll use OpenAlex and Semantic Scholar (free) instead. Only needed
  if those prove insufficient: a SerpAPI key.

## Never send me
Passwords, broker login PINs, bank details, or keys pasted into chat. Use the environment's credential settings instead.

---

# List 2 — the user's proposal (21 Nov 2026) and what Claude needs for it

*The user offered a remote device, Gemini CLI, Kite data and a Screener login. Below is exactly what I'd like
for each. List 1 above still stands.*

## A. Remote device (highest value)
- [ ] **Connect it to this session with Claude's Remote Control.** In the Claude desktop app on that machine: Settings → Claude Code → Remote Control → share a working folder. A dedicated folder is ideal (e.g. `~/fein-lab`). Then tell me, and I'll request access. You approve it on the device.
- [ ] **Clone this repo there** on branch `claude/focused-brahmagupta-g3hraq`, so scripts and memory stay in sync.
- [ ] **Python 3.11+** plus `poppler-utils` (for `pdftotext`) and `sqlite3`. Optional: `pip install pandas numpy`.
- [ ] **Keep it on as long as practical** (24/7 is ideal). I'll schedule *plain scripts* there, such as nightly NSE/BSE disclosure collectors and long backtests. These run without using my Claude usage, so data collection never stops.
- [ ] **Tell me if the device is in India.** An Indian IP unblocks Grid-India, the e-way bill portal, ports, JPC steel and data.gov.in.
- [ ] **Disk:** ~50 GB free for price/filing archives.

## B. Gemini CLI (extra hands)
- [ ] **Install and log in to Gemini CLI** on the device, so `gemini -p "…"` works non-interactively in a terminal. Antigravity (the IDE) is optional, because I can only drive the CLI.
- How I'll use it: bulk extraction (promises from transcripts, tables from PDFs), first-pass summaries, and an independent second opinion.
- Rules I'll follow: its output is untrusted until verified, every number is re-checked against the source, and it never makes the final judgment.
  It has also read market history, so it does **not** fix the hindsight problem in blind drills.

## C. Kite (Indian market data)
- [ ] **Preferred: a small READ-ONLY REST API on the device** (localhost, or LAN-only, never the public internet) that wraps Kite Connect:
  - `GET /instruments?exchange=NSE` → full instrument master (instrument_token, tradingsymbol, name, segment, lot size).
  - `GET /historical?token=…&from=YYYY-MM-DD&to=…&interval=day|minute|15minute` → OHLCV candles. Please tell me whether prices are adjusted for splits/bonuses.
  - `GET /quote?symbols=NSE:INFY,…` → last price, OHLC, volume (for verification).
  - Respect Kite's rate limit (~3 historical calls/second). Caching on your side is a bonus.
  - **No order, position, funds or holdings endpoints. Read-only only.** Keep the access token on the device and never send it to me.
- [ ] **Optional extra:** the official Zerodha Kite MCP connector, for quick ad-hoc questions in chat.
- Why the API is preferred: backtests need thousands of calls from Python scripts, which is cheap through an API and expensive through chat tool calls.

## D. Screener.in (free login)
- [ ] **Create a separate research account** and log in on the device's browser or in a cookie file there. Never paste the password in chat.
- Plan for it:
  1. **Universe builder:** custom screens to list every NSE/BSE company with market cap, sector and key ratios, so backtests use a complete, documented universe instead of guesses.
  2. **Point-in-time snapshots:** save screen results weekly, building our own history of fundamentals over time.
  3. **Concall/transcript links** per company for the promise tracker.
- Export is a premium feature. If free screens can't be paged fully, I'll tell you before we consider premium.

## E. US data
- Already working: SEC EDGAR (`tools/sec_fetch.py`) and Yahoo chart API. Nothing needed now.
- If Yahoo starts blocking, a free Tiingo or Alpha Vantage key would be the backup (add it as an environment credential, never in chat).

## F. Anything else
- [ ] When the device is connected, tell me its OS, CPU/RAM and timezone, so I size jobs correctly.
- [ ] Decide who gets notified when a nightly job fails (I can write failures to a `logs/` file in the repo).
