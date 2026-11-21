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
   pumps (circular). Leverage blow-ups (Jet, IL&FS, DHFL, Future, Zee, Suzlon-2008, Unitech, SVB, Lehman, Evergrande,
   GE…) pass the hard set every time: **no hard rule addresses solvency**.
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
