# My Memory — everything we've learned and decided

*Your plain-language copy. Claude updates this at the end of every session.*
*Last updated: 19 Nov 2026 (evening).*

---

## 1. Where we are right now

We've finished the **learning phase** and built the **memory**. The knowledge library now holds
**100 case studies** (Indian and global multibaggers, 32 frauds/blow-ups), **19 sector playbooks**,
**32 investor profiles**, **14 Indian market cycles (1992–2026)** and **68 insights** — all searchable.
Claude can now pull filings, transcripts, pledges and insider trades **directly from NSE/BSE**.
Next: build the "promise tracker" (what management said vs what they delivered).
**Action for you:** merge the pull request so new sessions load the memory:
https://github.com/aditya-bad/fein/pull/1

---

## 2. The 10 biggest truths we learned

1. **Almost all stock-market wealth comes from very few stocks.** About 4% of US stocks
   created *all* the market's net wealth over 90 years. Most stocks lose to a bank FD.
   So we're hunting for rare winners, and most of our picks will be ordinary.
2. **F&O is a trap for individuals.** 88–93% of individual F&O traders in India lose
   money every year. In FY26, 82% were losing even *before* costs. Prop firms and
   foreign funds with algorithms took the other side. → **We don't do F&O.**
3. **Every legend had an unfair advantage, not just knowledge.**
   - Buffett: started at 11 in a market nobody studied; later used cheap insurance
     money (about 1.7x leverage); 99% of his wealth came after age 60–65.
   - Lynch: read ~700 annual reports and visited 200+ companies a year. Burned out at 46.
   - Damani: most of his wealth comes from *building* D-Mart, not trading.
   - Jhunjhunwala: started with "₹5,000" but borrowed his brother's clients' money; his
     biggest wealth came from a 1992 bet *against* the market; Titan was ~1/3 of his wealth.
4. **Myths we busted:** Titan wasn't bought at ₹3 (that's split-adjusted; he paid ₹30–50).
   The "Fidelity study of best investors being dead" never existed. Your Radico story
   was off: the 120 → 4,600 move started in **2016–17** (premium brands + debt falling),
   not from a 2008 UBL issue. UBL is a beer company.
5. **Multibaggers have "two engines":** profits grow *and* the market pays a higher P/E.
   Radico ≈ profit ×7.5 × P/E ×5 ≈ 38x.
6. **Winners fall hard along the way.** Amazon −94%, NVIDIA −50% twice, Radico −74%.
   You only get the reward if you can hold through that.
7. **Knowledge isn't the edge.** Millions read the same books. Edge = seeing what others
   don't, plus patience, plus never getting wiped out.
8. **AI doesn't pick winning stocks by itself.** AI trading contests mostly lost money;
   the oldest AI-run ETF trails the S&P 500. AI is great for *reading* and *checking*.
9. **Instant disqualifiers**, no matter how cheap the stock: promoter pledging shares,
   auditor qualifying the accounts, profits jumping with no real reason, growth funded
   by debt while cash flow is negative.
10. **Time and capital matter.** ₹25,000/month at 12% for 30 years ≈ ₹7.7 crore —
    more than ₹10,000/month at 15% (≈ ₹5.6 crore). Saving more beats chasing returns.

---

## 3. What OUR edge will be — "Lynch at scale" (proposed)

| Claude does | You do |
|---|---|
| Reads every annual report, earnings call, rating report and SEBI order for ~1,500 small companies, every quarter | Check things in the real world: shops, dealers, factories, customers, people in the trade |
| Tracks what each management **promised** vs what they **delivered**, over years — a credibility score nobody else keeps for small companies | Bring knowledge from your own work, industry and city |
| Spots changes early: margins jumping, promoters buying, pledges, guidance misses | Make the final call, and hold through bad patches |
| Enforces discipline: kill criteria, "how could this fail?", a decision journal | Stay out of F&O and leverage |

Our advantages over big funds: we can buy small companies they can't, we can wait
years without being fired, and nobody tracks small-company management this closely.

---

## 4. Mistakes Claude made (so it doesn't repeat them)

- **Jumped to a stock list without an edge.** The 13 stocks came from public screens
  thousands of people use. You called it an amateur move — correctly.
- New rule: **edge first, stocks later.** And: answer what you actually asked.

---

## 5. Stocks we've looked at (learning watchlist — NOT buy advice)

Prices from 19 Nov 2026. Each has "kill criteria" — if one triggers, the idea is dead.

- **Looked strongest:** Uniparts (72/100), Sandur Manganese (68), Bajaj Consumer (66), Skipper (now watchlist — see 5a).
  Uniparts, Bajaj Consumer, MPS and IOL: **zero promoter pledge confirmed from NSE**.
- **Watch, wait for a lower price:** MPS, IOL Chemicals, Prudent, Techno Electric.
- **Downgraded to avoid on 19 Nov after checking NSE pledge data:** Transrail (promoter pledged 5.97%,
  even though the company declared "no pledge" in April), Rolex Rings (5.13%), Honasa (4.15%), Birla Cable (6.28%).
- **Avoid:** Indo Tech (promoter pledged 57.9% on 12 Nov), Jayaswal Neco (99.9% pledged),
  Genus Power, Syncom, gold jewellers.
- Next check: **Feb 2027** results.

Full details: `memory/watchlist.md` and the published report.

---

## 5a. The promise tracker works (first real edge, 20 Nov 2026)
We read 10 earnings calls each for Uniparts and Skipper and checked every promise against what happened.
- **Uniparts:** credibility +0.28. Numbers guidance reliable under the new CEO (78% hit), but execution
  promises keep slipping (Mexico plant ~10 months late, promised acquisition never happened). Stays 72/100.
- **Skipper:** only ~41% of promises delivered; capacity date moved 5 times; promised "no more equity"
  then raised ₹433.5 cr. **Downgraded from buy-zone to watchlist (66 → 55).**
- New rule: no stock goes in the buy zone without this credibility check.

Also added: governance history of **43 Indian business groups** (clean → severe), **29 lessons straight
from Buffett's letters and Howard Marks' memos**, and **Indian base rates** (about half of IPOs trade below
issue price; ~3 in 4 active funds lag the index over 10 years; momentum and value factors have worked in
India, small size by itself has not).

## 5c. Tested on real data (Nov 2026) — what holds and what doesn't
- **US insider buying clusters:** no edge vs similar random stocks (12-month excess 0.0%).
- **Indian promoter buying:** not reliable — a few big winners make the average look good; the typical case lags.
- **Indian post-earnings drift: REAL.** Stocks with the biggest earnings surprise beat the biggest disappointments
  by ~4.2% over the next 3 months, and it held in a fresh 2022–25 test. After trading costs, buying only the winners
  is borderline. **The clearest use: don't hold (or don't buy) a stock right after a big earnings miss.**
  **Confirmed again on fresh 2026 data (21 Nov):** big misses kept falling (~−2.7% vs similar stocks over 3 months);
  big beats were only slightly ahead after costs — not reliable. A live tracker starts with the Jan–Feb 2027 results.
- **Blind historical drills don't work for an AI** (it recognised 19/20 companies). So we test skill with
  dated predictions about the future instead: 42+ open, scored from Jan 2027.

## 5b. New things we learned in the knowledge scout
- **Valuation timing matters.** Since 2004, every negative 5-year Nifty return started at P/E ≥ 24.5;
  starting below P/E 12 gave ~29%/yr.
- **Indian winners mostly grew profits;** only ~37% of the median gain came from a higher P/E. Stocks
  that ended their run at P/E 70+ are mostly lower today (median −48%).
- **Small caps fall >20% about every 2 years** and spent 36% of days (2004–26) >30% below their peak.
- **Tone isn't an edge in India** — optimistic concall language moves prices short-term but doesn't
  predict results. Checking promises vs delivery is the edge.
- **Never trust a company's own "no pledge" statement** — check the exchange data.

## 6. Our rules

1. No F&O, no day trading, no borrowed money that could force us to sell.
2. Every number checked against two sources.
3. Write down why we buy and what would make us sell — *before* buying.
4. Small positions, so being wrong never hurts badly. A few big winners pay for the rest.
5. Think in probabilities, never "sure shot".
6. This is research, not SEBI-registered advice.

---

## 7. What Claude needs from you next

1. What's your work or industry? Which businesses do you understand from the inside?
2. Which city, and what can you physically check (markets, dealers, factories, people)?
3. Time horizon, rough capital, and do you have separate income?
4. How many hours a week can you give this?
5. Access you can give: Screener.in login, Zerodha Kite connector, Trendlyne, a YouTube
   transcript API key.

---

## 8. Where everything is

| What | Where |
|---|---|
| This summary | `MY_MEMORY.md` |
| Claude's detailed memory | `memory/` folder (start with `memory/00_index.md`) |
| Claude's auto-loaded instructions | `CLAUDE.md` |
| Report 1: How people pick stocks, A–Z | `reports/AI stock picking playbook.md` |
| Report 2: What separated the real winners | `reports/What separated real market winners.md` |
| Report 3: 13-stock pipeline | `reports/Multibagger idea pipeline.html` · https://claude.ai/artifact/VbL4pGdvUHLEnS4oKskvX3 |
| Raw research with sources | `research_notes/` |
