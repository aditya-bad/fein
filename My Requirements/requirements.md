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
