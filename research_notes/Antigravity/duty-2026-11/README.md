# India gold customs duty, Jul-2024 to Nov-2026: Antigravity task + Pi verification (28-Nov-2026)

Task cloud-20261128-1819-7 (B). Stage 1/5 input (gold allocation, macro). Research, not SEBI-registered advice.

## Verified timeline (gold bars, HS 7108; BCD + AIDC; GST 3% extra)
| Change | Notification | Dated | Effective | Gold bar | Gold doré | Verified how |
|---|---|---|---|---|---|---|
| Before Jul-2024 | 50/2017 + 11/2021-Customs | – | – | 10% + 5% = **15%** | 14.35% | primary: Budget 2024-25 memo ("From 15%") |
| Budget 2024-25 cut | **30/2024-Customs** (BCD 5%, S.No. 356/357 of 50/2017) + **32/2024-Customs** (AIDC Sl. 15D 1%, 15B/15C 0.35%) | 23-Jul-2024 | **24-Jul-2024** | 5% + 1% = **6%** | 5.35% | primary: notification texts + memo |
| Budget 2025-26 | none for the rate (new tariff lines for >=99.5% gold, from 1-May-2025) | 1-Feb-2025 | – | **6%** unchanged | – | primary: 2025-26 memo |
| Consolidation | 45/2025-Customs replaces 50/2017 (gold = S.No. 192-196) | 24-Oct-2025 | 1-Nov-2025 | 6% (per agy) | – | secondary only (agy); 02/2026 confirms 45/2025 and its S.Nos exist |
| Budget 2026-27 | **02/2026-Customs** only adds a sunset proviso (31-Mar-2027) to S.No. 192-195 | 1-Feb-2026 | – | **6% unchanged, NOT cut to 5%** | – | primary: 02/2026 text + 2026-27 memo (sunset table only; no gold rate in speech or memo) |
| Mid-year hike | 15/2026-Customs (BCD 10%) + 16/2026-Customs (AIDC 5% / 4.35%), per agy | 12-May-2026 | **13-May-2026** | 10% + 5% = **15%** | 14.35% | **Text of 15/2026 seen in two independent SECONDARY reproductions** (worldtradescanner, taxguru; they match word for word: G.S.R. 358(E), 12-May-2026, TABLE I S.No. 192-197 of 45/2025 '5%' -> '10%', in force 13-May-2026). AIDC 1% -> 5% (16/2026) seen only in a news report (LiveLaw: 'overall effective levy to 15%', Nos. 15-18/2026). Market check: IBJA 999 ~16% above spot x INR in Nov-2026. The Gazette PDF itself was not found (egazette 273940.pdf = 22/2026, unrelated) |

Note: "15/2026-Customs (N.T.)" dated 1-Feb-2026 (baggage regulations) is a different series from the tariff notification 15/2026-Customs, so it does not contradict agy.

## Who was right
- **Our study was right:** the Feb-2026 Budget kept 6% (primary), and 15% applies from 13-May-2026 (BCD text via two matching secondary reproductions; AIDC via news; Gazette PDF still not seen).
- **Antigravity's earlier gold study was wrong** ("Feb Budget cut it to 5%"). In this run agy itself reports the 5% claim as an unsupported secondary claim (iifl/coinswitch) and sides with 6%.

## How Antigravity behaved
- It had only `search_web`, with no page-reading tool, and was told not to run shell commands (the Pi session's permission rules
  blocked letting it run commands). So it **saved no source files** and gave **no URLs at all**. It did not fabricate any and
  said so plainly. "No redirect links" was obeyed only in the sense that it gave none.
- First attempt (shell allowed only by prompt): print mode auto-denied its first Bash call, and it produced nothing.
- Its notification numbers and dates for 2024 matched the primary texts exactly (30/2024, 32/2024, 23-Jul / 24-Jul-2024,
  AIDC 1% / 0.35%). Its Feb-2025 and Feb-2026 "no change" calls also match the primary documents.
- To use it as a research worker it needs a page-reading tool (or a pre-approved fetch tool) in headless mode. Decide with the user.

Files: `answer.md`, `agy_stdout.md`, `prompt.txt` (agy); `primary_excerpts/*.txt` (URL on line 1, verbatim extracts; PDFs from
indiabudget.gov.in, fetched 28-Nov-2026 on the Pi).
