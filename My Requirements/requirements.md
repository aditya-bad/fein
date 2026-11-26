# What Claude needs from you

*Last updated: 20 Nov 2026. I keep working without any of these. Each one removes a specific limit.*
*Ordered by how much it would help. Tick an item off (`[x]`) when you've done it, and tell me.*

## High impact

- [x] **1. Make our branch the GitHub default branch.** ✅ Done by user 21-Nov-2026; PR #1 closed.
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


---

# List 2 — update (21 Nov 2026): Raspberry Pi, your own Kite MCP wrapper, Screener step by step

*Replaces sections A, C and D of List 2 above where they differ. Everything else stands.*

## A2. Raspberry Pi setup (step by step)
1. **OS:** Raspberry Pi OS **64-bit** (Bookworm or newer). Pi 4/5 with ≥4 GB RAM. Use an SSD over USB if you can,
   because SD cards wear out with constant database writes. Set timezone: `sudo timedatectl set-timezone Asia/Kolkata`.
2. **Packages:**
   `sudo apt update && sudo apt install -y git python3 python3-venv poppler-utils sqlite3 curl nodejs npm`
3. **Repo:** `mkdir -p ~/fein-lab && cd ~/fein-lab && git clone https://github.com/aditya-bad/fein.git && cd fein && git checkout claude/focused-brahmagupta-g3hraq`
   (needs a GitHub login with access to the repo, for example a fine-grained token with access to this one repo only.)
4. **Data folder:** `mkdir -p ~/fein-data` (the nightly collectors write here).
5. **Connecting it to me (Remote Control).** The Claude desktop app doesn't run on a Pi, so use Claude Code in a terminal:
   - Install Claude Code on the Pi (`curl -fsSL https://claude.ai/install.sh | bash`), then run `claude` once and log in with **your** account.
   - In the folder to share, run: `cd ~/fein-lab && claude remote-control`. Keep it running (for example in `tmux`, or as a systemd service).
   - Tell me when it's running. I'll check whether this cloud session can see the folder and request access; you approve on the Pi.
   - Honest caveat: using a computer's folder from a cloud session isn't available on every account yet. If I can't see it,
     you can still run a Claude session **on the Pi itself**, which reads this same repo, memory and all.
6. **Cron jobs** (I'll give the exact lines when the detector scripts are ready in `tools/detectors/README.md`). They run without
   Claude, so they cost none of my usage.
7. **Gemini CLI:** `sudo npm install -g @google/gemini-cli`, then run `gemini` once and log in. Check `gemini -p "say ok"` prints a reply.
8. **Pi deployment (added 24 Nov 2026): one command.** After step 3, run `deploy/pi/install.sh --dry-run`, then
   `deploy/pi/install.sh`, then `deploy/pi/healthcheck.sh`. It installs the packages, creates `~/fein-data` (with
   `secrets/` at `chmod 700`), and schedules every unattended job (detectors, solvency, PEAD live tracker,
   scoreboard, weekly `git pull`, log rotation). Nothing is pushed to GitHub unless you opt in. Step by step, outputs,
   sharing alerts with me and troubleshooting: `deploy/pi/README.md`. This replaces the hand-written cron lines in step 6.

## C2. Kite: your own MCP wrapper (not the official one). Tools I'd like it to expose
All **read-only**. No order, position, funds, holdings or profile tools. The access token stays on the Pi.
| Tool | Inputs | Returns |
|---|---|---|
| `instruments` | exchange (NSE/BSE/NFO), optional search text | instrument_token, tradingsymbol, name, segment, lot size, tick size |
| `historical` | symbol or token, from, to, interval (day/60minute/15minute/minute), `continuous` (for futures), `oi` | OHLCV (+OI) candles. **Say whether prices are adjusted for splits/bonuses.** |
| `historical_bulk` | list of symbols, from, to, interval=day | same, for many symbols in one call (saves my usage). Do the paging and rate-limit sleeps inside your wrapper. |
| `quote` / `ltp` | up to ~200 symbols | last price, OHLC, volume (for verifying prices) |
| `index_history` | index name (NIFTY 50, NIFTY 500, NIFTY SMALLCAP 250, sector indices) | daily closes (benchmarks for backtests) |
| `health` | none | token valid? last refresh time? |
Nice to have:
- Results as **CSV/JSON files written to a shared folder** (e.g. `~/fein-data/kite/`) for big pulls, with the tool returning just the file path.
  That keeps large data out of my context.
- Your wrapper handling the daily Kite login/token refresh.

Also tell me how I'll reach the wrapper: over Remote Control on the Pi (simplest), or as a remote MCP URL added to this environment.

## D2. Screener.in: exactly what to do
1. Create a **new free account** at screener.in with a **separate email** used only for research (not your main one).
2. On the Pi, install a browser-cookie export or simply log in once with a script. Simplest:
   - Log in on any browser, open DevTools → Application → Cookies → `www.screener.in`, and copy the `sessionid` and `csrftoken` values.
   - On the Pi, save them in `~/fein-data/secrets/screener_cookies.txt` (`chmod 600`) as two lines: `sessionid=…` and `csrftoken=…`.
   - **Never paste them in chat.** I'll read the file only from scripts on the Pi.
3. Tell me it's done. I'll then:
   - run custom screens to build a complete NSE/BSE universe (every company: market cap, sector, P/E, ROCE, growth, pledge %) for backtests;
   - save a snapshot every week, building our own point-in-time history;
   - collect concall/transcript links for the promise tracker.
4. Sessions expire every few weeks. When a script reports "login expired", repeat step 2.
5. If free screens turn out to be capped (no paging/export), I'll tell you before suggesting premium.


---

# List 3 — network & security checklist for the Raspberry Pi (21 Nov 2026)

*You said you're setting up the network and security. This is what I'd recommend, ordered by importance.*

## Must do
- [ ] **No inbound ports open to the internet.** Nothing on the Pi needs to accept connections from outside.
  Remote Control and git work over outbound connections only. Keep the router's port forwarding off for the Pi.
- [ ] **Separate user account** on the Pi for this work (e.g. `fein`), not `pi`/root. Run cron jobs and Claude as that user.
- [ ] **SSH: Claude does NOT need it.** Remote Control connects outward from the Pi. SSH is only for *you* to manage the Pi
  from another computer. If you don't need that, turn it off (`sudo systemctl disable --now ssh`), which is safest. If you do,
  allow keys only (`PasswordAuthentication no` in `/etc/ssh/sshd_config`).
- [ ] **Firewall:** `sudo apt install ufw && sudo ufw default deny incoming && sudo ufw default allow outgoing && sudo ufw enable`
  (add `sudo ufw allow from <your-LAN-subnet> to any port 22` only if you keep SSH for yourself on the LAN).
- [ ] **Kite wrapper binds to `127.0.0.1` only** (not `0.0.0.0`), and is read-only (no order/funds/holdings endpoints).
  If you want it reachable from your laptop, use a private network like Tailscale rather than opening ports.
- [ ] **Secrets in files with `chmod 600`** under `~/fein-data/secrets/`, owned by the `fein` user. That covers the Kite API key/secret/access
  token, Screener cookies and the GitHub token. **Never commit them.** I'll add `secrets/` to `.gitignore` patterns.
- [ ] **GitHub access:** a *fine-grained* token limited to `aditya-bad/fein`, with contents read/write only and an expiry date.
- [ ] **Automatic security updates:** `sudo apt install unattended-upgrades && sudo dpkg-reconfigure unattended-upgrades`.

## Should do
- [ ] **Remote Control folder scope:** share only `~/fein-lab`, never your home folder. Claude can only act inside what you share.
- [ ] **Back up `~/fein-data`** (SQLite DB, raw filings) weekly to another drive or cloud. The repo holds code and memory, but not the raw data.
- [ ] **Kite token refresh:** Kite access tokens expire daily, so your wrapper should refresh them on the Pi. If you do that by hand, tell me what time it's ready.
- [ ] **Gemini CLI account:** use an account without sensitive email/drive data, since it will process public filings only.
- [ ] **Monitoring:** I'll write job failures to `~/fein-data/logs/`. Optionally set up an email or Telegram alert on failure, which you'd configure yourself.

## Nice to have
- [ ] UPS or stable power. SD cards corrupt on power loss, which is another reason to prefer an SSD.
- [ ] Tailscale (or similar) if you want to reach the Pi from your phone or laptop without exposing it.

## List 4 (added 26-Nov-2026) — small one-off asks
- [ ] **Nifty P/E history before 2012** (5 minutes, optional): open https://www.niftyindices.com/reports/historical-data →
  "P/E, P/B & Div. Yield" → Nifty 50 → from 01-Jan-1999 to today → download CSV, and drop it into `My Requirements/uploads/`.
  The site only serves this to a browser, and I won't work around that. It lets me re-run the valuation-timing test on 25+ years
  (2000 and 2008 peaks included) instead of 2012–26 only.
