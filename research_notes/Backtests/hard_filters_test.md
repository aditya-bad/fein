# Back-test: do our hard filters remove traps without removing winners? (Roadmap stage 2)

*Method calibration, not stock picking. Research, not SEBI-registered advice.*
Started 2026-11-21. Stage 2 (hard filters) of `memory/roadmap.md`; unlocks a calibrated stage-2 gate that
stage 3 signals (PEAD, credibility) can run behind, and a nightly detector set for the Pi.

## Pre-registration (written 2026-11-21 before any Part B outcome statistic was computed)

**Question.** `insight:disqualifiers` (revised 20-Nov-2026, L10/L12) splits our checklist into HARD
disqualifiers (no override) and GRADED flags (override with `insight:flag-override-template`). Do the hard
rules catch traps (fraud, blow-ups, >70% losses) *at the time we would have been deciding*, and how many
winners would they and the graded flags have cost us?

**Part A — labelled case set.** Every `case_study` in memdb (131 records). Duplicates (hidden-trap-X / X,
false-alarm-X / X) merged into one company-episode; 14 non-company or private records excluded with a
reason. Labels: WINNER (≥3x from T), TRAP (fraud / blow-up / >70% loss from T not recovered within 5 years,
sub-typed fraud, lev = leverage/business blow-up, bust = valuation/cycle round-trip after a run), FALSE-ALARM
(the flags-judgment library; counted as winners). T = episode start: for traps the peak / last calm date
before the first public shock; for winners the record's start (trough, IPO or start of the measured leg).
**Hindsight rule:** a flag counts as fired only if the record or a dated filing shows it was public before T.
If that cannot be shown, it is `U` (unknown), never `Y`. Flags that became public after T are kept as
"later" notes (early-warning value), not hits. Mechanical flags use only fiscal years public before T
(India: FY ending March counts from 30 Sep; US: period end + 90 days) from screener.in pages (India) and SEC
companyfacts (US); promoter pledge from the BSE shareholding-pattern XBRL filed before T.

Rules tested (codes used everywhere below):
- HARD: H1a fake-cash signal · H1b economics implausible for the business · H1c profits not verifiable by
  outsiders · H2 auditor resignation citing disagreement/denied information or qualified opinion ·
  H3 rating "issuer not cooperating" · H4 SME/Telegram pump · H5 related-party cash leakage to promoter
  entities. Plus a broader variant **H2b**: any auditor exit mid-term, restatement / SEC 8-K item 4.02,
  regulator-assessed misstatement (e.g., RBI NPA divergence) or delayed results within 5 years before T.
- GRADED: G1 promoter pledge > 25% of promoter holding · G3 dilution / repeated raises in the 2 years
  before T · G4 trailing P/E > 50 (or > 2x own median) · and mechanical: F1 Σ5y CFO/Σ5y PAT < 0.7,
  F1b < 0.3, G2 borrowings ≥ 1.5x over 3 years with Σ3y CFO < 0, G5 Σ5y FCF < 0, G6 debtor days > 120 or
  +30 days in 2 years, F2 other income > 30% of PBT (3y). Lenders: cash-flow, debtor-day and other-income
  tests marked not applicable.

**Part B — systematic universe test (pre-registered here).** Universe = the 580 usable companies of the
PEAD sample (`research_notes/Backtests/india_pead.md` §1: seeded random sample of the current NSE EQ/BE
list → survivors only). Snapshot **T0 = 30-Sep-2020**; fundamentals FY2016–FY2020 (screener consolidated if
it has ≥3 of those years, else standalone); pledge from the BSE SHP for March 2020; auditor resignations
from NSE corporate announcements 1-Jan-2015 → 30-Sep-2020. Mechanical rules:
- **R1** Σ5y CFO / Σ5y PAT < 0.3 (PAT sum > 0, non-lender); **R1b** same < 0.7
- **R2** promoter pledge > 25% of promoter holding (Mar-2020); **R2b** > 50%
- **R3** any statutory-auditor resignation announced before T0 (internal/secretarial/cost/branch excluded)
- **R4** borrowings FY20 ≥ 1.5x FY17 and Σ CFO FY18–20 < 0 (non-lender)
- **R5** other income / PBT (FY18–20) > 30% (PBT > 0, non-lender) — reported separately
- **ANY** = R1 or R2 or R3 or R4

Outcomes: adjusted close on the first trading day on/after T0 vs the first on/after 30-Sep-2025 (5 years;
last close if the series stops earlier) and vs 18-Nov-2026 (to date). Events: **loss50** = ratio < 0.5,
**x3** = ratio > 3. Report P(event | flagged) vs P(event | unflagged) and the base rate, Wilson 95% CIs,
two-sided Fisher exact p. **Decision rules (fixed now):** a rule "earns its place" as a hard filter only if
flagged→loss50 is at least 2x the base rate with Fisher p < 0.05 **and** flagged→x3 is not above the base
rate; a rule whose flagged→x3 rate is ≥ the base rate is not a hard filter whatever its loss rate.
Known biases, stated in advance: (1) survivors-only universe (firms delisted before mid-2023 are absent, which
removes exactly the worst traps, so loss rates for flagged firms are understated); (2) screener figures are
current/restated, not as-first-reported; (3) 2020-09 → 2025-09 was a strong small/mid-cap bull market, so x3
base rates are high and loss50 base rates low; (4) one snapshot, ~500 firms: power is low for rare flags.

---

# RESULTS — Part A (case studies), written 2026-11-21 after the run

**Set:** 131 case_study records → **106 company-episodes** (43 traps: 19 fraud, 15 leverage/business blow-ups,
9 busts after a winning run; 63 winners incl. 9 false-alarm-only episodes) after merging duplicates; 14
records excluded (funds, sector/market cycles, private companies, Waaree/Premier = neither). Every record id is
covered (script checks). Mechanical data existed before T for only ~45% of episodes: most long-run winners start
in 2003–2013, before screener's 12-year window, and US XBRL starts ~2009.

**Big caveat — this set is in-sample.** The hard disqualifiers were *written from* these very trap cases
(insight:disqualifiers, L10/L12). Strict pre-T dating removes most of the circularity, but the judgment flags
(H1b, H1c) were still coded by someone who knows the outcome, and winners' records list no "tells", so H1b/H1c
were never seriously searched for on winners. Read the hard-rule catch rates as an *upper bound*.

## Per-rule confusion matrix (Y = fired on pre-T evidence; known = Y + N; NA excluded)
| Rule | Traps fired / known (unknown) | Winners fired / known (unknown) | Trap catch rate (known) | Winner reject rate (known) | Precision (traps among fired) |
|---|---|---|---|---|---|
| H1a fake-cash signal | 1 / 43 (0) | 0 / 63 (0) | 2% | 0% | 100% |
| H1b implausible economics | 3 / 42 (1) | 0 / 63 (0) | 7% | 0% | 100% |
| H1c profits unverifiable | 2 / 43 (0) | 0 / 63 (0) | 5% | 0% | 100% |
| H2 auditor exit over disagreement / qualified | 0 / 41 (2) | 0 / 63 (0) | 0% | 0% | – |
| H2b broad: any auditor exit / restatement / regulator misstatement / delayed results (5y) | 3 / 43 (0) | 1 / 62 (1) | 7% | 2% | 75% |
| H3 rating 'not cooperating' | 0 / 43 (0) | 0 / 62 (1) | 0% | 0% | – |
| H4 SME/Telegram pump | 1 / 43 (0) | 0 / 63 (0) | 2% | 0% | 100% |
| H5 RPT cash leakage | 1 / 40 (3) | 0 / 63 (0) | 2% | 0% | 100% |
| G1 pledge >25% of promoter holding | 8 / 20 (7) | 2 / 13 (21) | 40% | 15% | 80% |
| G3 dilution / repeated raises | 1 / 42 (1) | 3 / 63 (0) | 2% | 5% | 25% |
| G4 P/E >50 | 7 / 41 (2) | 4 / 57 (6) | 17% | 7% | 64% |
| F1 Σ5y CFO/PAT <0.7 | 6 / 20 (17) | 8 / 24 (37) | 30% | 33% | 43% |
| F1b Σ5y CFO/PAT <0.3 | 3 / 20 (17) | 5 / 24 (37) | 15% | 21% | 38% |
| G2 debt ≥1.5x + Σ3y CFO<0 | 2 / 21 (16) | 4 / 24 (37) | 10% | 17% | 33% |
| G5 Σ5y FCF <0 | 9 / 23 (14) | 15 / 30 (31) | 39% | 50% | 38% |
| G6 debtor days >120 or +30d | 3 / 23 (14) | 3 / 28 (33) | 13% | 11% | 50% |
| F2 other income >30% PBT | 6 / 17 (20) | 6 / 15 (46) | 35% | 40% | 50% |
| H1b-proxy (blind): ROCE >40% 3y or OPM +10pp in 3y | 9 / 22 (15) | 5 / 28 (33) | 41% | 18% | 64% |
| **HARD_current (H1a,H1b,H1c,H2,H3,H4,H5)** | 8 / 39 (4) | 0 / 62 (1) | 21% | 0% | 100% |
| **HARD + H2b broad** | 11 / 40 (3) | 1 / 61 (2) | 28% | 2% | 92% |
| **GRADED any (G1,G3,G4 + mechanical)** | 22 / 28 (15) | 21 / 24 (39) | 79% | 88% | 51% |
| **mech cash only (F1b CFO/PAT<0.3 or G2)** | 4 / 19 (18) | 7 / 22 (39) | 21% | 32% | 36% |

By trap type, the current hard set fires pre-T on **fraud 8 of 19** (3 unknown), **leverage blow-ups 0 of 15**,
**busts 0 of 9**. Graded flags fired on ≥3 counts: traps 8, winners 7 (HAL 5, BSE 4, Mazagon 4, Trent 4,
Netflix-2019 4, Super Micro 3, Eternal 3) — the "3+ open flags = no position without a variant view" rule
would have stopped as many winners as traps.

## What Part A says, rule by rule
1. **The hard set is clean but small: 8 of 39 known traps caught, 0 of 62 winners rejected.** Every catch was a
   fraud case and came from the *judgment* fraud signals: H1a fake cash (Satyam: ~Rs 5,000 cr earning far below
   FD rates while borrowing, visible in FY08 accounts), H1b economics too good for the business (Vakrangee's
   ROCE ~40% in a kiosk franchise; Manpasand outgrowing Frooti; Cox & Kings' debt and receivables in an
   advance-paid business), H1c profits nobody outside can audit (Wirecard's third-party acquirers; Rajesh
   Exports' ~1% margin on Rs 2 lakh cr of gold), H5 group receivables (Gitanjali, ~33% of receivables), H4 SME
   pumps (circular). Leverage blow-ups (Jet, IL&FS, Future, Zee, Suzlon-2008, Unitech, SVB, Lehman, Evergrande,
   GE…) pass the hard set every time, as does DHFL (a fraud whose tell was ALM mismatch): **no hard rule addresses solvency**.
2. **H2 (auditor exit over disagreement) never fired before T: 0 of 41.** In every case it is in the record
   (Vakrangee, Manpasand, Reliance Capital, Ricoh, Super Micro, Byju's) the auditor left *after* the peak, usually
   mid-collapse. It's a sell signal, not a buy-side screen. Keep it as a non-overridable exit trigger, not as an
   entry gate that ever catches anything early.
3. **H2b broad (any auditor exit / restatement / regulator-found misstatement / delayed results in 5y)** added Yes
   Bank (RBI NPA divergence, disclosed 2017), Super Micro at its 2024 peak (8-K 4.02 Nov-2018) and Celsius at its
   2024 peak (4.02 Mar-2022, a stock-comp restatement unrelated to the bust: lucky). Cost: Super Micro at the start
   of its 17–30x run (Jan-2023). A rejection there was still right on net for anyone buying the peak, but wrong for
   a Jan-2023 buyer (even after −86%, ~3x from T).
4. **H3 'not cooperating' never fired (0/43) and H4 only on its own source cases.** No evidence for or against;
   both are cheap to keep as detector rules (tools/detectors already watch ratings).
5. **G1 pledge > 25% is the best single pre-T flag where data exists: 8 of 20 traps vs 2 of 13 winners**
   (BSE XBRL at T: Gitanjali 79%, IL&FS Transportation 98%, Gensol 63%, Cox & Kings 54%, Zee 46%, Future 44%,
   Reliance Capital 34%; Luckin founders' margin loans). The 2 winners: Apollo Hospitals 71% (L12 false alarm) and
   Suzlon 76% at Dec-2019 (then ~49x). Graded, not hard, is right: the misses on both sides are real.
6. **The cash-flow tests (F1, F1b, G2, G5) fire on winners at least as often as on traps.** F1 CFO/PAT < 0.7:
   traps 6/20, winners 8/24. G5 negative FCF: traps 9/23, winners 15/30. The winners caught are the L12 pattern —
   HAL (sovereign receivables), BSE and Mazagon (customer/clearing money and advances swinging CFO), Trent (store
   build-out), Netflix (content), Super Micro (inventory). Meanwhile the *best-disguised* frauds pass them:
   Vakrangee (CFO/PAT 0.75), Cox & Kings (2.7 — fabricated cash), PC Jeweller (0.96), Valeant (11.5), GE. Cash
   conversion is a reason to ask what the working capital is made of, never a verdict.
7. **G4 P/E > 50 is the only flag that sees busts coming (7 of 9 busts at their peaks) but it also hit Trent
   (155x, then 19x), Deepak Nitrite (~69x, then 12x), Kaynes (104x, then 10x) and DMart.** Valuation belongs to
   stage 5, not to stage 2.
8. **A blind, mechanical H1b proxy (ROCE > 40% or OPM +10 pp in 3 years) does not reproduce the judgment rule**:
   it fires mostly on loss-to-profit recoveries (Paytm, Jet, Future, IL&FS) and on winners (Caplin, Tata Elxsi, CDSL,
   Palantir, Tesla), and misses Vakrangee (ROCE 3y avg just under 40). "Too good for the business" needs a peer and
   unit-economics comparison, not a threshold.

# RESULTS — Part B (580-company universe, snapshot 30-Sep-2020), written after the run

**Funnel.** 580 companies → 495 with a price on T0 (85 listed later or had gaps) → fundamentals for 465
(19 lenders), pledge for 452, NSE auditor feed for 486. **0 of 495 stopped trading before Nov-2026**: the
sample was drawn from the *current* NSE list, so every firm that was delisted, merged away or suspended is
missing. Market cap at T0 (BSE SHP shares × unadjusted close): 304 firms ≥ Rs 400 cr, 148 below, 43 unknown.

**5-year (30-Sep-2020 → 30-Sep-2025)** — base rates: loss50 1.8%, x3 54.5% (n = 495)

| Rule | known / flagged | flagged → >50% loss | unflagged → >50% loss | Fisher p | flagged → >3x | unflagged → >3x | Fisher p | median ratio flagged / unflagged |
|---|---|---|---|---|---|---|---|---|
| R1 CFO/PAT 5y < 0.3 | 382 / 42 | 1 (2.4%, CI 0.004–0.123) | 0.9% | 0.3737 | 25 (60%) | 52% | 0.4134 | 4.53 / 3.09 |
| R1b CFO/PAT 5y < 0.7 | 382 / 77 | 1 (1.3%, CI 0.002–0.07) | 1.0% | 1.0 | 44 (57%) | 52% | 0.4437 | 4.07 / 3.06 |
| R2 pledge > 25% | 452 / 68 | 2 (2.9%, CI 0.008–0.101) | 1.6% | 0.3444 | 47 (69%) | 51% | 0.0055 | 4.4 / 3.04 |
| R2b pledge > 50% | 452 / 44 | 2 (4.5%, CI 0.013–0.151) | 1.5% | 0.178 | 31 (70%) | 52% | 0.025 | 5.16 / 3.1 |
| R3 auditor resignation before T0 | 486 / 31 | 1 (3.2%, CI 0.006–0.162) | 1.3% | 0.3715 | 18 (58%) | 54% | 0.7136 | 3.58 / 3.29 |
| R4 debt ≥1.5x + Σ3y CFO < 0 | 445 / 27 | 0 (0.0%, CI 0.0–0.125) | 1.7% | 1.0 | 19 (70%) | 54% | 0.114 | 5.28 / 3.29 |
| R5 other income > 30% PBT | 385 / 111 | 3 (2.7%, CI 0.009–0.076) | 0.7% | 0.1466 | 68 (61%) | 48% | 0.0242 | 3.85 / 2.91 |
| **ANY of R1–R4** | 495 / 139 | 4 (2.9%, CI 0.011–0.072) | 1.4% | 0.2761 | 89 (64%) | 51% | 0.009 | 4.12 / 3.06 |

**to date (→ 18-Nov-2026)** — base rates: loss50 4.2%, x3 49.5% (n = 495)

| Rule | known / flagged | flagged → >50% loss | unflagged → >50% loss | Fisher p | flagged → >3x | unflagged → >3x | Fisher p | median ratio flagged / unflagged |
|---|---|---|---|---|---|---|---|---|
| R1 CFO/PAT 5y < 0.3 | 382 / 42 | 2 (4.8%, CI 0.013–0.158) | 2.9% | 0.6295 | 26 (62%) | 48% | 0.1025 | 4.36 / 2.76 |
| R1b CFO/PAT 5y < 0.7 | 382 / 77 | 4 (5.2%, CI 0.02–0.126) | 2.6% | 0.271 | 46 (60%) | 47% | 0.0553 | 3.66 / 2.72 |
| R2 pledge > 25% | 452 / 68 | 3 (4.4%, CI 0.015–0.122) | 3.6% | 0.7298 | 39 (57%) | 47% | 0.1162 | 3.59 / 2.75 |
| R2b pledge > 50% | 452 / 44 | 2 (4.5%, CI 0.013–0.151) | 3.7% | 0.6764 | 27 (61%) | 47% | 0.0814 | 4.34 / 2.76 |
| R3 auditor resignation before T0 | 486 / 31 | 4 (12.9%, CI 0.051–0.289) | 3.3% | 0.0268 | 14 (45%) | 50% | 0.7114 | 2.28 / 2.99 |
| R4 debt ≥1.5x + Σ3y CFO < 0 | 445 / 27 | 0 (0.0%, CI 0.0–0.125) | 3.8% | 0.6132 | 18 (67%) | 49% | 0.0761 | 5.0 / 2.9 |
| R5 other income > 30% PBT | 385 / 111 | 5 (4.5%, CI 0.019–0.101) | 2.9% | 0.5334 | 62 (56%) | 45% | 0.0715 | 3.55 / 2.57 |
| **ANY of R1–R4** | 495 / 139 | 8 (5.8%, CI 0.029–0.109) | 3.7% | 0.3231 | 78 (56%) | 47% | 0.0721 | 3.55 / 2.75 |

**5-year, only firms with mcap ≥ Rs 400 cr at T0** — base rates: loss50 2.0%, x3 44.4% (n = 304)

| Rule | known / flagged | flagged → >50% loss | unflagged → >50% loss | Fisher p | flagged → >3x | unflagged → >3x | Fisher p | median ratio flagged / unflagged |
|---|---|---|---|---|---|---|---|---|
| R1 CFO/PAT 5y < 0.3 | 258 / 21 | 0 (0.0%, CI 0.0–0.155) | 1.3% | 1.0 | 12 (57%) | 44% | 0.2572 | 4.17 / 2.47 |
| R1b CFO/PAT 5y < 0.7 | 258 / 42 | 0 (0.0%, CI 0.0–0.084) | 1.4% | 1.0 | 21 (50%) | 44% | 0.4986 | 3.91 / 2.57 |
| R2 pledge > 25% | 304 / 32 | 2 (6.2%, CI 0.017–0.201) | 1.5% | 0.1232 | 19 (59%) | 43% | 0.0902 | 3.33 / 2.44 |
| R2b pledge > 50% | 304 / 20 | 2 (10.0%, CI 0.028–0.301) | 1.4% | 0.0527 | 12 (60%) | 43% | 0.167 | 3.61 / 2.51 |
| R3 auditor resignation before T0 | 303 / 12 | 0 (0.0%, CI 0.0–0.243) | 1.7% | 1.0 | 6 (50%) | 44% | 0.7717 | 3.11 / 2.64 |
| R4 debt ≥1.5x + Σ3y CFO < 0 | 276 / 18 | 0 (0.0%, CI 0.0–0.176) | 1.9% | 1.0 | 11 (61%) | 45% | 0.2244 | 4.17 / 2.65 |
| R5 other income > 30% PBT | 259 / 52 | 2 (3.8%, CI 0.011–0.13) | 1.0% | 0.1808 | 28 (54%) | 42% | 0.1202 | 3.17 / 2.44 |
| **ANY of R1–R4** | 304 / 69 | 2 (2.9%, CI 0.008–0.1) | 1.7% | 0.6215 | 39 (56%) | 41% | 0.0272 | 3.17 / 2.41 |

## What Part B says
1. **No rule passes the pre-registered bar.** For every rule P(flagged → >3x) is *at or above* the base rate
   (ANY: 64% vs 51% unflagged, p = 0.009), so by decision rule 2 none qualifies as a hard filter on this sample,
   and none reaches 2x base loss rate with p < 0.05 at 5 years. The R3 auditor rule is the closest on the
   *to-date* horizon (4 of 31 flagged firms down >50% vs 3.3%, p = 0.027), but to-date wasn't the primary
   horizon and n = 4.
2. **The test can barely see losers.** Base rate of a >50% 5-year loss is **1.8% (9 of 495)**. Two reasons, both
   biases stated in advance: survivors only (the Gensols, Cox & Kings and DHFLs of 2020 aren't in a list drawn in
   2023), and Sep-2020 was close to the COVID low before a five-year small-cap bull run (median stock 3.3x).
3. **A second selection bias favours flagged firms:** the PEAD sample kept only firms whose mcap reached Rs 400 cr
   *at some point in 2018–2025*. A tiny, pledged, cash-poor firm in 2020 got in only if it later grew. Firms
   under Rs 400 cr at T0 tripled 72% of the time vs 44% for firms already above it. Restricting to mcap ≥ Rs 400 cr
   at T0 shrinks the "flagged firms do better" effect (ANY x3 57% vs 41%, p = 0.027) but doesn't reverse it, and
   pledge > 50% then shows the only material loss lift: **10% vs 1.4% (2 of 20), p = 0.053** — Sadbhav
   Engineering/Sadbhav Infra (pledges 56% / 82%, −76%).
4. **Names behind the numbers.** Of the 9 >50% 5-year losers, ANY fired on 4: Sadbhav Engineering and Sadbhav
   Infra (pledge 56% / 82%), JHS (cash conversion), SecureKloud (auditor resignation 2019). Den, Radio City, Take
   Solutions and Valiant Organics fired nothing (GVP Tech had no data). On the to-date horizon ZEEL (−63%) fired
   nothing at T0 because its pledge had already been invoked down to 16% of a 4.8% promoter stake — the damage
   was done. Flagged *winners* include CG Power (auditor exit
   in 2020 mid-fraud discovery, then a Murugappa takeover: ~31x), Ramky (auditor exit 2015, ~19x), Aurionpro and
   TI. A flag at a distressed low often marks a *bottom*, after the bad news was public and priced.
5. **What Part B can't tell us:** whether the rules would have saved us from the delisted traps (they aren't in
   the data), and how they behave from a market peak. A fair Part B needs a point-in-time universe that keeps
   dead companies (stage 1: Screener login + delisted-company lists) and several snapshot dates (2017-12, 2019-06,
   2021-12, 2023-12).

# VERDICT (both parts) and proposed revision

Evidence quality: Part A is in-sample and mostly judgment-coded. Part B is out-of-sample but survivor-only, one
snapshot, at a market low. **Neither part supports making any mechanical rule a no-override disqualifier.**
Part A supports keeping the *judgment* fraud signals hard: they had 100% precision on 106 episodes, though
they caught only 8 of 39 known traps and their coding is outcome-aware.

| Rule | Part A (pre-T) | Part B (2020 → 2025) | Verdict |
|---|---|---|---|
| H1a fake-cash signal | 1/43 traps, 0 winners | not tested | **KEEP hard.** Add the mechanical test: interest income / avg cash vs FD rate; big cash + big debt |
| H1b economics implausible for the business | 3 traps, 0 winners (judgment); blind proxy fires on 5/28 winners | not tested | **KEEP hard, but ADJUST:** fires only after a written peer + bottom-up unit-economics comparison (revenue per outlet × outlets etc.); a ratio threshold alone is not the rule |
| H1c profits not verifiable by outsiders | 2 traps, 0 winners | not tested | **KEEP hard**; make "OPM < 2% on pass-through revenue" and "profit in a segment/partner we can't audit" explicit |
| H2 auditor exit over disagreement | 0/41 before T: always came after the peak | R3 (any resignation): no 5y lift, to-date 13% vs 3% (p 0.03, n 4) | **KEEP as a non-overridable EXIT / no-new-buy trigger** (it fires mid-collapse); note it almost never helps at entry |
| H2b broad (restatement, regulator-found misstatement, delayed results, any auditor exit within 5y) | +3 traps (Yes Bank, SMCI and Celsius peaks), cost 1 winner (SMCI 2023) | R3 ≈ this; flagged winners incl. CG Power 31x | **ADD as GRADED** (strong graded flag; RBI divergence for banks should be near-hard) |
| H3 rating not cooperating | 0 fires | not tested | **KEEP** (cheap, detector exists); unproven |
| H4 SME/pump pattern | only its own source cases | not tested | **KEEP**; extend to pre-revenue SPAC/IPO hype (Nikola) |
| H5 RPT cash leakage | 1 trap pre-T (Gitanjali); usually surfaces after T | not tested | **KEEP hard** |
| G1 pledge > 25% | 8/20 traps vs 2/13 winners (best graded flag) | x3 69% vs 51%; >50% & mcap ≥ 400 cr: loss 10% vs 1.4% (p 0.05) | **KEEP graded**; raise attention level at >50% or rising; never hard (Apollo, Suzlon-2020) |
| G3 dilution | 1 trap, 3 winners | not tested | **KEEP graded** (judge price × purpose × buyer) |
| G4 P/E > 50 | 7/9 busts, 4 winners | not tested | **MOVE to stage 5** (valuation temperature, P/E vs own median) — not a stage-2 filter |
| F1 / F1b CFO/PAT | traps 6/20 vs winners 8/24; frauds pass it | R1: no loss lift, x3 60% vs 52% | **DROP as a filter; keep as a question** ("what is the working capital made of?") |
| G2 debt + negative CFO | 2 traps vs 4 winners | R4: 0 losers in 27, x3 70% | **DROP as a filter; ADJUST** to a solvency rule (see below) |
| G5 negative FCF | 9 traps vs 15 winners | not tested separately | **DROP as a flag** (description only) |
| G6 debtor days | 3 vs 3 | not tested | **KEEP graded only with counterparty** (sovereign vs related/unknown, per L12) |
| F2 other income > 30% PBT | 6 vs 6 (fires on exchanges, PSU cash piles) | R5: loss 2.7% vs 0.7% (p 0.15), x3 61% vs 48% | **KEEP as a question** (it's where the H1a cash-yield test starts), not a flag |

**Gap found: solvency.** 15 of 15 leverage blow-ups (Jet, IL&FS, Adani Enterprises, Future, Zee, Unitech, Suzlon-2008,
Kingfisher, SVB, Lehman, Evergrande, GE, Credit Suisse, Paytm, PC Jeweller) passed every hard rule. Proposed new
GRADED solvency flags, to be back-tested before use: negative net worth; interest cover < 1.5x for 2 years;
short-term funding of long assets (lenders: ALM 1-year gap, CP share); dividends or buybacks exceeding FCF while
borrowing; group-level promoter debt (pledge + holdco loans).

**Proposed revised filter set (separate record insight:disqualifiers-v2-proposal; insight:disqualifiers is
unchanged until the user agrees):**
- **HARD at entry (no override):** H1a fake-cash signals · H1b implausible economics *after a written peer/unit-
  economics check* · H1c unverifiable profits · H4 pump patterns (incl. pre-revenue SPAC/IPO hype) · H5 RPT cash
  leakage · H2 auditor exit citing disagreement/denied information or qualified/adverse opinion · H3 rating "not
  cooperating" (unproven, cheap).
- **HARD at exit (sell / no new money until a new auditor signs clean):** H2 and the strongest H2b events (RBI NPA
  divergence, 8-K 4.02 non-reliance, results delayed past the deadline).
- **GRADED (override template):** pledge (>25%; escalate >50% or rising), H2b events, dilution, debtor days with
  counterparty, the new solvency set.
- **QUESTIONS, not flags (description only):** CFO/PAT, negative FCF, debt with negative CFO, other-income share.
- **Moved to stage 5:** P/E > 50 / > 2x own median.

**What would change this verdict:** a point-in-time universe with dead companies showing flagged → >50% loss at
≥ 2x base rate (with x3 not above base) at peak-ish snapshots — that would promote pledge > 50% or the
auditor rule to hard. Re-run with the full Screener universe on the Pi (stage 1) at 4 snapshot dates.

## Files
- Scripts: `tools/backtests/hard_filters/` — `b1_fetch.py` (screener / BSE SHP / NSE announcements), `a1_pledge.py`
  (pledge at T), `a2_episodes.py` (hand-coded pre-T episode table, with evidence), `a3_cases.py` (merge + matrices),
  `a4_tables.py`, `b2_analyze.py` (Part B), `b3_tables.py`, `hfcommon.py` (screener parser, metrics, rule defs).
- Outputs: `research_notes/Backtests/hard_filters_outputs/` — `partA_cases.json` (every episode, flags, evidence,
  metrics), `partA_pledge_at_T.json`, `partB_summary.json`, `partB_flags.csv` (per-company flags and outcomes).
- Raw caches (scratchpad, not in git): screener pages, BSE SHP XBRL values, NSE announcement extracts.
