# S H Kelkar and Company (NSE: SHK) — LIVE deep dive #7 (method test, protocol v1.4, stages 2→7; first Chemicals/IT-frame draw)

**Date:** 2026-11-25 · **Analyst:** Claude · **Status:** live (not practice). Its paper calls are scored.
**Purpose:** test the deep-dive method on a new sector frame (Chemicals + Information Technology only) with a company **drawn at
random**. Test material (L9, L21): **no buy/sell verdict**. Outputs: decision card v1.5 and dated probabilistic calls scored later
against naive base rates.
**Roadmap:** stage 2 (filters) → 3 (signals) → 4 (deep dive) → 5 (valuation) → 6 (decision) → 7 (scoreboard). It unlocks the first
live test of a **consumer-ingredient compounder that screens cheap on reported earnings but whose reported earnings carry one-off
insurance gains**, and the first chemicals name for the China-price-cycle and pollution-board checks.
Research, not SEBI-registered advice.

Source tags: `[AR26]` annual report FY2025-26 (NSE, filed 01-Jul-2026; consolidated notes unless marked); `[XBRL]` NSE integrated-filing
XBRL, consolidated (Q2 FY27 filed 02-Nov-2026; Q1 FY27, FY26/Q4, Q3 FY26, FY25/Q4); `[DECK]` Q2 FY27 press release + presentation
(02-Nov-2026); `[CALL]` earnings-call transcripts on NSE (Q2 FY27 = 06-Nov-2026; also Nov-2024, May-2025, Nov-2025, May-2026, Aug-2026);
`[NSE]` announcements (178, 25-Nov-2024 → 25-Nov-2026) / bhavcopy / SHP XBRL / pledge API; `[BSE]` BSE announcements (scrip 539450, 188
items, two ≤1-year windows); `[AGM]` Reg-44 voting results (31-Jul-2026; 2025 AGM 13-Aug-2025); `[SCR]` screener.in fetched 25-Nov-2026;
`[YH]` Yahoo v8 daily closes; `[WEB]` web search 25-Nov-2026 (single-source); `[EST]` my estimate (method shown). Money in ₹ crore.
"Two sources" for P&L lines = XBRL and screener agree (checked for every quarter and year used).

---

## 0. Selection (rules fixed before drawing; full log in `SHK_selection/`)
**Task rule:** universe.csv joined to industry_map.csv; India; mcap ₹1,000–20,000 cr at the latest bhavcopy close (date from the DATE1
column, L42); sector ∈ {`Chemicals`, `Information Technology`}; exclude SUNFLAG, AUTOAXLES, INDRAMEDCO, UTKARSHBNK, HARSHA and
financials; `random.Random(20261204)` shuffle of the sorted eligible list; first name passing stage-2 filters, outside the PEAD avoid
window, and scoreable.
**Pre-registration:** `SHK_selection/prereg_selection.md`, written **10:10 IST 25-Nov-2026 before the frame was built** (sha256
`25927bb9…0351a`, recorded in the walk log). What I had seen before writing is disclosed there (dd6's selection files).
**How it ran:** the 25-Nov file → 404; the 24-Nov file holds DATE1 = 23-Nov-2026 on every row (byte-identical to the 23-Nov file) → frame
close **23-Nov-2026**. 1,547 symbols, all priced; **809** in band; 0 in-band names unmapped. In band: Chemicals 72, IT 38; no excluded
subject in these sectors. **Eligible 110.**
**Walk:** #1 **SHK** (₹1,765 cr) passed all five checks → subject. **Skips: none.** Next (not checked): SWANCORP, GALAXYSURF, DHANUKA,
RSYSTEMS. Two random live draws in a row landed on walk #1 (HARSHA, SHK): the skip rules rarely bind on the first name — expected for a
filter that removes ~10–20% of names, but worth tracking (lesson candidate 7).

## 0b. Rule zero: edge before depth
1. **What the market knows.** India's largest Indian-origin fragrance & flavour (F&F) house (Keva/SHK/Cobra brands), 5,000+ clients,
   FY26 revenue ₹2,368 cr; FY27 talk: revenue +12–13%/yr, EBITDA 13% "the lower side", 15%+ in 12–18 months, debt to fall from Mar-2027
   `[CALL Q2 FY27]`. Reported trailing P/E 18.7x. Q2 FY27 questions: capex timelines (×2), creative-centre traction (×3), margins/15%
   target (×3), domestic volume vs price (×2), **"eight years of ROCE under your cost of capital"** (×1, Discovery Capital), interest and
   D&A run-rate (×1).
2. **The variable that matters:** the **return on ~₹2,330 cr of invested capital**, of which 55% of non-current assets now sit in Europe
   (₹709 cr), while ₹~80 cr/yr of creative-centre opex earns almost nothing yet — and how much of the "cheap" reported P/E is one-off
   insurance money. The ROCE question *was* asked, but nobody asked about **core earnings ex insurance** or the **balance sheet**
   (CRISIL outlook cut to Negative 28-Sep-2026; net debt ₹911 cr at a "peak").
3. **Layers:** L2 (core vs reported EPS; group ROIC/ROIIC first, L42), L3 (creative-centre payback two ways), L5 (votes net of promoter,
   RPTs with promoter companies). Honest limit: no information edge on client briefs won at the new centres.

---

## 1. S2 checklist (disqualifiers v3; filled before L1, every rule dated)
| Rule | Status | Evidence (source, date) |
|---|---|---|
| H1a fake cash | **pass** | Cash ₹62.1 cr vs borrowings ₹972.8 cr at 30-Sep-2026 `[XBRL Q2]`; bank interest income ₹0.09 cr FY26 `[AR26 n.29]` — no idle cash beside debt. |
| H1b implausible economics | **pass** | Gross margin 42–43%, EBITDA 9–18% FY15–H1 FY27 `[SCR; DECK]`; global majors earn more (Givaudan/Symrise ~20%+ EBITDA `[WEB]`, single-source). |
| H1c unverifiable profits | **pass** | No customer ≥10% of revenue FY25/FY26 `[AR26 n.45 D]`; FMCG clients; Deloitte audit with component auditors. |
| H2 auditor | **pass** | Deloitte Haskins & Sells unmodified FY25 `[NSE 16-May-2025]` and FY26 `[NSE 15-May-2026]`; Deloitte "will complete their term" at the 70th AGM; BSR & Co appointed 5 years (AGM 99.91% for) — rotation, flagged a year ahead `[NSE 08-Aug-2025]`. |
| H3 rating | **pass (outlook Negative)** | CRISIL AA- reaffirmed on ₹372 cr bank lines, outlook Stable → **Negative** `[NSE Reg-30 28-Sep-2026]`; rationale not retrieved (`[WEB]` search found no CRISIL page) — single-source. |
| H4 pump | **pass** | Main board since 2015; 6-month ADV ₹8.7 cr mean / ₹3.9 cr median `[YH]`; exchange *cautionary* letters 27-Oct-2026 for a late analyst-meet intimation (03-Mar-2025) — procedural `[NSE]`. |
| H5 RPT leakage | **pass (watch)** | 6.1. |
| Exit triggers | **none** | Results on time; no restatement. |
| G pledge | **clear** | Pledge API 0 rows; SHP XBRL 30-Sep-2026: 6,300,000 of 75,945,564 promoter shares pledged = **8.3% of promoter holding** (4.55% of equity), mostly one promoter-group holder (85% of its 7.39 m shares). |
| G accounting trouble | **watch** | FY25 AGM approved a **waiver of recovery of excess remuneration** paid to the CEO (item 7; 9.0% of institutional votes against) `[AGM 2025]`; exceptional items every year FY25–FY27. |
| G dilution | **clear** | No issue since IPO; buybacks FY20/FY22 (capital 145 → 138). |
| G solvency (S1/S5) | **watch** | `solvency_screen.py` 25-Nov-2026: grade blank, 2 flags (ICR 2.29x FY26; ST borrowings 639 > cash 65 + 0.5×CFO 263). TTM ICR **2.4x** (EBIT ex OI 145.2 / finance 60.9) `[XBRL]`. |
| Q CFO/PAT | ok | FY22–26 CFO 633 vs PAT 478 = 1.32x `[SCR]`; FY25 CFO only 16. |
| Q negative FCF | watch | FCF FY25 −80, FY26 +60 `[SCR]`; H1 FY27 inventory build. |
| Q other-income share | **watch** | TTM other income 12.1 + **exceptional 63.0** = 47% of PBT 159.4 `[XBRL]`. |

**Survival cap / L39 addendum.** Pledge 8.3% (< 25%) and ICR 2.4x (> 1.5x): **neither flag fires**; both-flags rule not triggered. The
balance sheet is still the second open flag (8.1).

**Stage-3 signals.** PEAD: Q2 FY27 SUE **+0.08 → quintile 3** (event 02-Nov-2026); Q1 FY27 +0.26 → Q3. Caveat: SUE on reported EPS is
noisy here (exceptional items of ₹30–60 cr in a quarter). **Credibility (concall mode, hand ledger, n=8): 31% vs auto-components peer
median 60%** (no chemicals/F&F peer set on file; L18). Ledger:

| Said (date) | Promise | Outcome | Score |
|---|---|---|---|
| Nov-2024 | H2 FY25 stronger than H1 | H2 1,110 vs H1 1,012 `[SCR]` | met |
| Nov-2024 | FY25 revenue growth "well in excess of our 12% target" | +10.0% reported (2,123.4 vs 1,930) `[XBRL; SCR]`; May-2025 call called it "15%" | missed |
| May-2025 | Vashivali rebuild commissioned within FY26 | "put to use Q4 FY27", second factory Q4 FY28 `[CALL Nov-2026]` | missed |
| May-2025 | Vanavate commissioning "later this calendar year" (2025) | AR (Jul-2026): Q2 FY27 → Aug-2026: Q3 → Nov-2026: Q4 FY27 | missed |
| May-2025 | FY26 EBITDA "15% remains, may get a little better" | 10.2% (resolver basis) | missed |
| Nov-2025 | H2 FY26 EBITDA "14%, 15% we should be able to achieve" | 9.4% (Q3 9.6, Q4 9.2) `[XBRL]` | missed |
| Nov-2025 | Netherlands brownfield commissioned by end-FY26 | early Q1 FY27 `[AR26]` | ½ |
| May-2026 | Almere factory "in a couple of months" | in use since May-2026 `[CALL Nov-2026]` | met |
Pending: FY27 double-digit growth (H1 +14.5%); "15% EBITDA plus" in 12–18 months (Nov-2026); net debt down by Mar-2027.
**Pattern: dates slip AND margin numbers miss** — worse than the L26 sector pattern ("numbers met, dates slip").

---

## 2. Map (L1)
**Business.** F&F compounder: buys aroma chemicals, essential oils (orange, patchouli, vetiver ≈15% of the purchase basket `[CALL
Nov-2024]`) and solvents, and formulates fragrance/flavour blends for soaps, detergents, personal care, fine fragrance, food and beverage.
A small own-ingredients arm ("Global Ingredients": H1 FY27 revenue ₹20 cr vs ₹32 cr, EBITDA −₹5 cr vs +₹1 cr `[DECK]`; Anhui Ruibang
Aroma, China, 90%) competes with Chinese aroma-chemical makers.
**Segments FY26** `[AR26 n.45]`: Fragrance revenue ₹2,126.9 cr, segment result (after D&A) ₹152.6 cr, segment assets ₹2,524.7 cr;
Flavours ₹241.4 cr, ₹57.7 cr, ₹210.6 cr. H1 FY27: Fragrance ₹1,088 cr (+11.9%; like-for-like ~14% after exiting ~₹50 cr/yr of low-margin
business), EBITDA ₹121 cr; Flavours ₹184 cr (+47%), EBITDA ₹52 cr `[DECK]`.
**Geography:** revenue FY26 India ₹1,236 cr; AR "Europe ₹186.6 cr (FY25 ₹497.6 cr), Others ₹945.2 cr (₹399.7 cr)" `[AR26 n.45 C]` —
**inconsistent with the deck** (Europe H1 FY27 ₹265 cr, +18.8%; H1 FY26 ~₹224 cr) → reclassification, unexplained (disclosure flag).
Non-current assets: India ₹464 cr, **Europe ₹709 cr (55%)**, Others ₹106 cr.
**Subsidiaries:** Keva Europe B.V. → Provier Beheer/Holland Aromatics (NL; Almere brownfield commissioned May-2026), Keva Italy Srl → CFF
Keva Italy, Keva UK, Keva Germany (2024); Keva USA; Keva Fragrance Industries (Singapore) → PT SHK Keva Indonesia, Anhui Ruibang (China);
Keva Middle East FZE (Sep-2025); Keva Ventures (divested 28-Jul-2026) `[AR26 n.46; BSE]`.
**Ownership (Sep-2026):** promoters (Vaze family) 54.87% (58.95% Dec-2023), FIIs 5.27%, DIIs 6.35%, public 33.50%; 56,790 holders `[SCR]`.
Chairman Ramesh Vaze died 15-Sep-2026 `[BSE]`; promoter-group SAST 29(2) filings (Keva Constructions & PACs) 17/21-Oct-2026.
**Peers (P/E `[SCR]` 25-Nov-2026):** Privi Speciality 37.2 (aroma chemicals, ROCE 22%), Galaxy Surfactants 29.9 (same FMCG clients),
Oriental Aromatics 170 (depressed earnings). No listed Indian pure F&F compounder; global majors (Givaudan, Symrise, IFF) are the real
competitors.
**Flags (v1.4):** holdco — none (investments ₹11 cr). **Cyclical — input-cost cycle, not volume:** revenue fell in no year FY15–FY26, but
EPS fell 61% FY18→FY20 and the price fell **−84%** (2018 high 310 → 2020 low 48.9) `[SCR; YH]`. Screens COOL/COLD → cyclicals rule
applied (3).

## 3. Financials re-derived (L2) `[SCR consolidated; XBRL checks]`
| FY | Revenue | OPM % | Op. profit | Other inc.* | PAT | EPS | FY-end close `[YH]` | FY-end P/E |
|---|---|---|---|---|---|---|---|---|
| FY17 | 981 | 17 | 167 | 12 | 105 | 7.25 | 296.45 | 40.9 |
| FY18 | 1,021 | 16 | 159 | 13 | 94 | 6.49 | 259.05 | 39.9 |
| FY19 | 1,048 | 13 | 141 | 21 | 88 | 6.12 | 150.85 | 24.6 |
| FY20 | 1,114 | 14 | 160 | −28 | 36 | 2.53 | 76.10 | 30.1 |
| FY21 | 1,322 | 18 | 239 | 36 | 144 | 10.24 | 111.45 | 10.9 |
| FY22 | 1,564 | 14 | 215 | 6 | 149 | 10.73 | 143.55 | 13.4 |
| FY23 | 1,687 | 13 | 217 | −8 | 63 | 4.42 | 99.50 | 22.5 |
| FY24 | 1,930 | 16 | 308 | 5 | 124 | 8.84 | 205.50 | 23.2 |
| FY25 | 2,123 | 14 | 296 | −38 | 73 | 5.29 | 176.60 | 33.4 |
| FY26 | 2,368 | 10 | 242 | 45 | 69 | 5.00 | 112.34 | 22.5 |
| **TTM Sep-26** | **2,532** | **11** | **284** | **76** | **94** | **6.82** | 127.53 | **18.7** |
\*Screener nets exceptional items into "Other income" (FY25 −38 = OI 23.85 − fire loss 60.55; FY26 45 = 9.53 + insurance 35.92).
FY26 from XBRL = AR: revenue 2,368.26; materials 1,347.76 − inventory change 27.99 (+ contract-manufacturing COGS 60.30, tagged inside
"OtherExpenses" in FY26/FY27 XBRL but inside materials in FY25 — a tagging change); employees 360.56; other expenses 385.83; finance 55.51;
D&A 119.37; PBT before exceptional 76.49; exceptional +35.92; PAT 69.15; EPS 5.00 — = screener ✓.
- **Core vs reported (the key L2 finding).** TTM PBT 159.4 includes **exceptional +63.0** (fire-insurance realisations: 33.07 in Q3
  FY26, 29.95 in Q1 FY27) and other income 12.1 → **core PBT ~₹84 cr** `[XBRL]`. Core EPS **₹3.4–3.9** by three routes (EBIT 145.2 ×
  0.65 − post-tax interest 45.8 = ₹3.51; PBT ex-exceptional less tax = ₹3.42; screener's ex-exceptional P/E 32.5 ⇒ ₹3.9) → **P/E ~33–37x,
  not 18.7x**. Effective tax is high (38% FY26; ~51% on TTM core) because European/US losses carry no tax shield.
- **Fire (23-Apr-2024, Vashivali, Raigad):** loss ₹60.55 cr net of an interim insurance relief of ₹95 cr (FY25 exceptional); FY26
  realised ₹35.46 cr more; Q1 FY27 ₹30 cr more `[AR26 n.48; CALL Aug-2026]`. Insurance premium 6.1 → 20.8 cr (+0.6 pp of sales) since.
- **Group ROIC/ROIIC first (L42) [EST].** Invested capital Sep-2026 = equity 1,420.7 + net debt 910.7 = **₹2,331 cr** (incl. goodwill
  360 + other intangibles 162). TTM NOPAT 145.2 × 0.70 = 101.6 → **ROIC 4.4%**; adding back management's ₹80 cr creative-centre opex
  ("deduct Rs.80 crore and add it to the profitability" `[CALL Q2]`) → 6.8%. **Full-cycle window** FY17–19 → FY24–26 (no trough-to-peak):
  avg EBIT ex OI 131 → 181 on avg IC ~1,040 → ~2,124 (equity + screener borrowings) → ROIC 8.8% → 6.0%, **ROIIC ~3%**. Segment view: Flavours
  27% pre-tax on segment assets, Fragrance 6.0% — the Fragrance segment carries the European acquisitions and centres. CEO: India ROCE
  "in 20% range"; centres need "three to four years before we are breakeven… seven, eight years… a good return" `[CALL Q2]`.
- **Normalised EPS (v1.4):** mean EPS FY17–26 = **₹6.69 → 19.1x** vs 18.7x reported trailing and ~36x core. Here trailing and normalised
  agree, and the misleading number is the *trailing* one (inflated by insurance) — the cyclicals rule alone would have missed this.
- **Ten-year compounding:** EPS FY16 ₹5.05 → FY26 ₹5.00 (≈0%/yr) while revenue grew 9.9%/yr and invested capital ~2.6x.
- **Customer concentration:** none ≥10% (FY25, FY26).
- **Other income FY26** `[AR26 n.29]`: 9.53 (write-backs 3.00, misc 5.27); FY25 23.85 incl. ₹19.93 cr profit on sale of investment.
- **Cash and working capital:** inventory ₹799 cr + receivables ₹615 cr at Sep-2026 `[XBRL]`; inventory days 182–252 FY15–26 `[SCR]`;
  CFO FY22–26 50/197/107/16/263. H1 FY27 inventory build "to ensure uninterrupted supplies" lifted net debt to ₹911 cr (deck = XBRL).

## 4. Unit economics (L3) — the creative centre and the plant
| Item | Value | Source / route |
|---|---|---|
| Creative/development centres (Germany, UK/Manchester, US) | "roughly Rs.80 crore of spend… not generating any meaningful revenue yet"; first sales in all three; "first half is indicative of all cost in" | `[CALL Q2]` |
| Management's payback | breakeven in "three to four years", good return in "seven, eight years" | `[CALL Q2; CALL May-2026: "after three years in term of breakeven"]` |
| New-product growth | "new products and new categories… growing at 25%"; legacy 5–6% | `[CALL Q2]` |
| Capex | segment capex FY25 ₹102 cr, FY26 ₹183 cr `[AR26 n.45]`; Vashivali reinstatement ~₹100 cr (insured) `[CALL Nov-2024]`; D&A guided ₹145–150 cr/yr | `[CALL Q2]` |
**Payback two ways (L42) [EST].** (a) Management route: breakeven in 3–4 years. (b) Revenue route: at a 42.6% gross margin less ~5% variable
selling/freight, contribution ≈38%, so covering ₹80 cr of fixed opex needs **~₹210 cr** of centre revenue. "The numbers are small" today;
from ₹20–40 cr/yr at the 25% growth management gives new business, ₹210 cr takes **7.4–10.5 years** (ln(210/40)/ln 1.25 = 7.4; from
₹20 cr = 10.5). The two routes differ ~2–3x; the revenue route agrees with management's own "seven, eight years" for a return, not with
"three to four" for breakeven. **Plants:** Vanavate greenfield + Vashivali rebuild (India fragrance), then the Mulund factories move out
(FY27–FY28) — "would conclude our large capex expansion… for the next few decades" `[CALL Q2]`. No capacity/utilisation figures are
disclosed (open item), so the plant payback cannot be rebuilt.

## 5. Cost drivers (L4), ranked by weight (FY26 consolidated, % of revenue ₹2,368.3 cr) `[AR26 n.30–35]`
| Line | ₹ cr | % | Physical driver | Sensitivity |
|---|---|---|---|---|
| **Materials (net, incl. contract mfg)** | 1,380.1 | **58.3%** | Aroma chemicals (petrochemical/terpene derived), essential oils (~15% of basket), solvents; ~10% of value bought "exclusively from China" `[CALL Nov-2024]` | 10% move on an assumed 60% crude/petrochemical-linked share [EST] ≈ 350 bp before pass-through; pass-through by "pricing actions" with a lag |
| Employees | 360.6 | 15.2% | Perfumers/flavourists, creative-centre hires in DE/UK/US; India plants (BRSR permanent employees 484 + 166 workers in the parent's table) | +10% = −152 bp; FY26 +24% vs revenue +12% |
| Legal & professional | 69.9 | 3.0% | Not broken down (consultants, European advisors?) | open item |
| Works operation & other | 66.5 | 2.8% | Plant overheads | — |
| Freight & forwarding | 35.8 | 1.5% | Exports, inbound oils | +20% = −30 bp |
| Power & fuel | 32.9 | 1.4% | Maharashtra/Gujarat industrial tariff | +10% = −14 bp |
| Insurance | 20.8 | 0.9% | Post-fire premium (FY25 6.1) | — |
| Contract labour | 18.7 | 0.8% | Maharashtra minimum-wage-linked | +10% = −8 bp |
| FX loss | 13.9 | 0.6% | Euro/US$ exposure | — |
| Pollution control | 3.8 | 0.2% | MPCB/GPCB compliance (Vapi co-processing "GPCB-approved") | — |
**Materials ratio by quarter (XBRL, materials + inventory change, ex contract mfg from FY26):** Q3 FY26 57.5% · Q4 FY26 57.9% · Q1 FY27
55.1% · Q2 FY27 54.9%. Deck basis (incl. contract mfg): gross margin H1 FY27 42.6% vs H1 FY26 42.3%; CEO expects "43% range", +0.5 pt if
inputs ease. The FY24 → FY26 margin fall was **below gross margin** (employees, insurance, FX, centres), not a materials squeeze.
**China-price cycle (chemicals rule).** SHK is a net *buyer* of aroma chemicals: Chinese aroma-chemical deflation (2023–25) is an input
tailwind for the compounding business and a headwind for its own small ingredients arm (Global Ingredients loss-making; China subsidiary).
The 2026 input spike is described as Middle-East/crude-driven ("Middle East oil crisis") `[CALL Q2]`. Leading series to track monthly:
crude/benzene/toluene, Chinese export quotes for key aroma chemicals (linalool, citral, musks), orange/patchouli/vetiver oil prices.

## 6. Governance, ownership, related parties (L5)
### 6.1 RPT table `[AR26 consolidated n.46]` (₹ cr)
| Item | FY25 | FY26 | Share |
|---|---|---|---|
| Purchases from Keva Aromatics Pvt Ltd (promoter-controlled) | 62.07 | 51.29 | 3.8% of materials |
| Sales to Keva Aromatics | 11.22 | 3.52 | 0.1% of revenue |
| Rent to Keva Constructions Pvt Ltd (promoter-controlled) | 6.13 | 7.93 | 55% of the ₹14.5 cr rent line |
| Security deposit to Keva Constructions (balance) | 0.00 | 3.97 | new |
| KMP short-term pay | 2.88 | 7.32 | 10.6% of FY26 PAT |
| Commission to directors (Kedar Vaze 0.78, Ramesh Vaze 0.44) | — | 1.22 | — |
| Dividends to promoter trusts/companies/family | 6.74 | 14.89 | — |
No royalty/parent fee (Indian promoter group). Pricing basis of Keva Aromatics purchases not disclosed (open item). **Verdict: no leakage
pattern, but promoter entities sit inside both materials and rent** (watch).
### 6.2 Vote results — dissent net of promoter votes (L42; the scrutiniser reports split by category)
| Meeting / resolution | Inst. against | Against ÷ non-promoter votes cast | Headline against |
|---|---|---|---|
| AGM 31-Jul-2026, item 3: re-appoint chairman **Ramesh Vaze** | 15.21% | 1.54 m ÷ 10.60 m = **14.5%** | 1.77% |
| AGM 2026 items 1–2, 4–7 (accounts, dividend, BSR auditor, chairman commission, cost auditor) | ≤0.45% | ≤0.7% | ≤0.09% |
| AGM 13-Aug-2025, item 3: re-appoint **Prabha Vaze** | 41.95% | 4.52 m ÷ 10.88 m = **41.6%** | 5.21% |
| AGM 2025, item 7: **waive recovery of excess remuneration paid to CEO Kedar Vaze** | 9.04% | ~8.9% | 1.12% |
| AGM 2025, items 5, 8 (chairman commission; FY25 commission/pay) | ~9.0% | ~9% | ~1.1% |
**Promoter shares held vs votes polled (L40):** promoters hold 75,945,564 and polled 75,943,814 (99.998%) — all promoter blocks voted,
including on their own family members' re-appointment ("promoter interested: No" on the form). Non-promoter turnout: institutions 65.8%
of their 15.3 m shares; non-institutions 1.1% of 47.1 m → non-promoter turnout ~17%. Headline percentages understate dissent ~8–10x.
### 6.3 People and incentives
CEO Kedar Vaze (promoter; re-appointed 2025); Group CFO Jagdish Agarwal since 02-Dec-2025 (previous CFO Rohit Saraogi resigned Jul-2025;
company secretary was interim CFO Oct–Nov 2025); EVP Ingredients resigned 30-Sep-2026. Chairman died 15-Sep-2026; four independent
directors' re-appointments are on a postal ballot (notice 06-Nov-2026). No ESOP overhang (trust sold its shares FY24; closure pending tax
assessments).
### 6.4 L40 — government/licence inputs and external facts missing from the AR
| Input | Dependence | In AR26? | Status |
|---|---|---|---|
| MPCB/GPCB consent-to-operate for Vashivali (rebuilt after the fire), Vanavate (new), Mahad, Vapi | Every plant | Generic BRSR text only | No order retrieved; no closure direction in NSE/BSE filings or a `[WEB]` search (one MPCB minute mentions "a fire incident… Directions were issued" without naming the unit — unresolved). **Open.** |
| Mulund factories (Mumbai) to be vacated FY27–FY28 | Two plants | Not discussed | **Who owns the Mulund land is not stated** (freehold land on the books only ₹32 cr; rent to promoter company ₹7.9 cr). External fact missing → open. |
| Fire-insurance claim | ₹160 cr received so far (95 + 35.46 + ~30) | Yes (n.48) | Total claim and remaining amount not disclosed. |
| State incentives (Maharashtra PSI etc.) | Possible for Vanavate | No grant note found | None claimed. |
**L41 state-law check:** Indian manufacturing is concentrated in Maharashtra (Mulund, Vashivali, Vanavate, Mahad; Vapi in Gujarat) and
India is ~52% of revenue → concentration applies. Items: MPCB consent cycles, Maharashtra minimum-wage VDA (contract labour 0.8% of sales),
Mumbai land-use rules for the Mulund exit. **No gazette search done this run** (open); none is existential on current evidence.

## 7. Scuttlebutt plan (L6; not executed — user's ground checks)
1. **Vanavate/Vashivali (Raigad):** construction status, trucks, MPCB consent board at the gate → tests the Q4 FY27 date (call 5).
2. **Mulund (LBS Marg):** plant activity, any redevelopment hoarding or land notice → who owns the land (6.4).
3. **FMCG buyers / blenders in Mumbai:** price-hike letters from F&F suppliers in 2026, share of briefs going to Keva vs Givaudan/Firmenich.
4. **Essential-oil and aroma-chemical traders (Mumbai, Kannauj):** monthly price basket (orange, patchouli, vetiver; linalool, citral).
5. **LinkedIn/job portals:** headcount at Keva Germany/UK/USA — tests "all cost in" (no further hiring).
Ethics: public sources only; no unpublished price-sensitive information.

---

## 8. Override (L7) and valuation (L8)
### 8.1 Override table
| Flag | Type | Verdict | What changes my mind |
|---|---|---|---|
| ROIC 4.4% (6.8% adj.), full-cycle ROIIC ~3% vs CoE 12.5%; EPS flat 10 yrs; 55% of NCA in Europe | bad (capital allocation) | **OPEN** | ROIC ≥ 9% on FY28; centres at EBITDA breakeven |
| Net debt ₹911 cr, ICR 2.4x, inventory ₹799 cr, CRISIL Negative | bad (balance sheet) | **OPEN** | Net debt < ₹800 cr and ICR > 3.5x by Mar-2027 |
| Margin guidance missed twice; plant dates slip ~1 yr; credibility 31% vs 60% | bad (credibility) | **OPEN** | H2 FY27 EBITDA ≥ 14%; Vanavate commissioned by Mar-2027 |
| ~42% / ~15% of non-promoter votes against family directors; excess CEO pay waived; chairman's death | bad (governance) | **OPEN** | Succession plan; no more waivers |
| Promoter companies in materials (3.8%) and rent (55% of the line); Mulund land ownership unknown | watch | watch | AR FY27 disclosure |
| AR geography table vs deck (Europe 187 vs ~450); "15%" FY25 growth claim vs 10% | disclosure | watch | AR FY27 reconciliation |
| **Reported P/E 18.7x includes ₹63 cr insurance gains; core ~36x** | **good-but-misleading** | explained | — |
| Flavours 27% pre-tax on assets, +47%; gross margin steady | good | confirmed | — |
**Open soft flags: 4** (+ credibility −29 pts counted by the card = 5) → variant view written (card §2).
### 8.2 What the price implies (`tools/valuation/live/SHK_worksheet.md`, worksheet v1.3)
**Inputs:** close **₹127.53** on 23-Nov-2026 (NSE bhavcopy = Yahoo; screener 25-Nov ₹126); 10 FY-end P/Es FY17–26 (median **23.9**);
peers 29.9 / 37.2 / 170 (median 37.2); 6-month ADV ₹8.7 cr mean; net debt ₹911 cr (XBRL = deck); base = **core** TTM (EBIT 145.2, EPS 3.51),
normalised EPS 6.69; tax 35%; post-tax interest −45.8 held flat; ROIIC history 3%.
**Scenarios (written before outputs):** blow-up 8% raw (0.25x); bear 30% (+6% → +5%, NOPAT margin 3.5%, ROIIC 4%, exit 14x); base 47%
(+12% → +8%, 5.5%, 8%, 22x); bull 15% (+14% → +11%, 7.0%, 12%, 28x).
**Outputs:** 5-year multiples bear 0.60x / base 1.89x / bull 3.30x / blow-up 0.25x; **EV 1.59x** (raw = anchored) vs hurdle 1.76x; P(≥2x)
34%, P(≥3x) 14%, P(≤0.5x) 17%, blow-up 8%. Base IRR **7.3%** vs CoE 12.5%.
**Reverse DCF:** no growth path reproduces the price; the base path needs a **year-10 NOPAT margin of 33.4%** (today 3.7%). **The scenario
DCF value per share is negative in every scenario (prob-weighted −₹38)**: at ROIIC 4–12% < CoE 12.5%, growth consumes more cash than it
creates, and the operating value lands below the ₹911 cr of net debt. The DCF-consistent exit P/E is therefore negative (−11.5 / −1.7 /
+3.5). **Reading:** on a strict cost-of-capital view the equity is an option on returns improving; the whole 1.59x EV is the exit-multiple
bet (EV at DCF exits −0.13x; at the own median 1.72x). Bull ROIIC 12% is flagged (>5 pts above history) — the bull case *is* the claim that
the European capital starts earning.
**Temperature:** COOL vs own history (0.78x), COLD vs peers (0.50x) on reported EPS; on core EPS (~36x) it would be WARM vs own history.
### 8.2b Why is it not cheaper / is it a trap?
| Question | Evidence | Answer |
|---|---|---|
| Peak-cycle earnings? | Margin at a trough (10–13%), not a peak; reported EPS inflated by insurance | **No peak — but reported EPS is not core** |
| Capital allocation | ROIIC ~3% over 8 yrs; Europe 55% of NCA | **Question** |
| Who takes value before minorities? | Promoter companies in materials/rent; CEO excess pay waived | Low-to-moderate leakage |
| Fraud/solvency trap? | Clean Deloitte audits, AA- (Negative), pledge 8%, ICR 2.4x | **No fraud signal; balance sheet is the watch** |
### 8.3 Variant perception
Market: a COOL-priced F&F franchise at ~19x with margins recovering. Our view: **no claimable mispricing**; reported cheapness is insurance
money plus a ten-year ROIC problem. The trackable questions are H2 FY27 margin (calls 3–4), Vanavate timing (call 5) and net debt by
Mar-2027 (kill criterion). Tails: raw P(≤0.5x) 17% is *above* the class 11% and raw blow-up 8% *below* 15%; default w=0.5 moves them to
14.2% and 11.7% (anchoring lowers one tail — flagged, L40).
### 8.4 Decision card (`tools/decision/live/SHK_card.md`, **card v1.5**)
**Rule output: size 0**, blocked by *Expected value vs hurdle* (EV 1.59x anchored = raw vs 1.76x). Stage 2 passed (7 hard rules); PEAD Q3;
survival cap clear (pledge 8.3%, ICR 2.4x); 5 open soft flags with a variant view (not blocking); tier satellite; review **2027-02-15**.
Card calls (5-year to 2031-11-23): P(≥3x) 0.137 (base 0.213); P(≤0.5x) 0.170 raw / 0.142 anchored (base 0.113); P(blow-up) 0.080 raw /
0.117 anchored (base 0.154).

---

## 9. Forward calls (live; tags paper-call, deepdive-generated, live, india, sector-chemicals; specs in `tools/scoreboard/specs.json`)
| # | Call (YES if…) | Resolve by | Our P | Naive base | Reasoning |
|---|---|---|---|---|---|
| 1 | Q3 FY27 consolidated revenue **≥ ₹650 cr** (+11.3% YoY vs ₹583.8 cr) | 2027-02-28 | **0.55** | 0.54 | Naive: 7 of 13 quarters (Q2 FY24–Q2 FY27) grew ≥11.3% YoY `[SCR]`. Ours: Q3/Q2 ratio 1.04/1.00/1.054 (FY24–26) on ₹636 cr → ₹636–670 cr, central ~₹655; the ₹25 cr/yr exited business costs ~1 pt; price pass-through helps |
| 2 | FY27 consolidated revenue **≥ ₹2,700 cr** (+14.0%) | 2027-05-31 | **0.50** | 0.31 | Naive: 3 of 11 FYs (FY16–26) grew ≥14% (Laplace 4/13). Ours: H1 ₹1,298.6 cr (+14.5%); H2 needs ₹1,401 cr = +13.6% vs H2 FY26 ₹1,233.7 cr; inflation pricing continues; CEO expects "strong demand in the second half" but his growth numbers have missed before |
| 3 | FY27 consolidated OPM (resolver definition) **≥ 13.0%** | 2027-05-31 | **0.35** | 0.79 | Naive: 10 of 12 FYs (FY15–26) ≥13% (Laplace 11/14). Ours: H1 12.90%; H2 needs ≥13.1% but H2 was weaker than H1 in FY25 (12.3 vs 15.6) and FY26 (9.4 vs 11.1); new-plant costs arrive in Q4; management's margin promises missed twice |
| 4 | FY27 consolidated net profit **≥ ₹120 cr** (as reported, incl. exceptional) | 2027-05-31 | **0.15** | 0.29 | Naive: 3 of 12 FYs ≥ ₹120 cr (Laplace 4/14). Ours: H1 ₹60.0 cr incl. ₹29.95 cr insurance; H2 needs ₹60 cr vs Q2 run-rate ~₹15 cr/quarter; little insurance left; central ~₹95–105 cr |
| 5 | A company document dated by 31-May-2027 states **Vanavate was commissioned / put to use by 31-Mar-2027** | 2027-05-31 | **0.30** | 0.50 | Naive [EST]: coin-flip for a "next quarter" plant date. Ours: the Vanavate date moved in four successive documents (CY2025 → Q2 → Q3 → Q4 FY27); our ledger has 4 of 5 dated plant promises late |
| 6 | SHK **beats the Nifty 500** from 23-Nov-2026 (₹127.53; 23,748.15) to 30-Sep-2027 | 2027-09-30 | **0.42** | 0.44 | Naive [EST, as live #1/#3/#4/#6]. Ours: PEAD Q3 (no drift signal); reported-EPS cheapness unwinds as insurance gains drop out; leverage + negative outlook; upside if margins hit 14% |
Card calls (5-year) are in 8.4. Calls 1–4 and 6 resolve automatically (consolidated XBRL + screener; Yahoo); 5 is assisted (Reg-30/deck
scan, human confirmation); the card calls are human (total-return series).

---

## 10. What this run taught the method (lesson candidates)
1. **Reported trailing EPS can be "cheap" because of one-off gains, not cycle position.** SHK's 18.7x reported P/E is ~36x on core
   earnings (₹63 cr of insurance realisations in TTM PBT of ₹159 cr). The v1.4 cyclicals rule (normalised 10-yr EPS) did not catch it —
   normalised 19.1x agreed with the inflated trailing number. Proposed L2 rule: before any temperature read, compute **core EPS = (EBIT ex
   other income × (1 − tax) − post-tax interest) / shares** and show trailing reported, core and normalised side by side; treat
   exceptional + other income > 25% of PBT as a "good-but-misleading" flag.
2. **When ROIIC < CoE and net debt is large, the worksheet DCF goes negative and the DCF-consistent exit P/E becomes meaningless**
   (−11.5 / −1.7 / +3.5). That is a correct reading (growth at sub-CoE returns destroys value), but the card's exit-bet table prints "n/a"
   ratios. Candidate tool change: print "DCF value below net debt → equity is an option on ROIC improving" and use the own-median column
   as the reference.
3. **L42 held a second time:** group ROIC (4.4%) first exposed what the 27% Flavours segment return hides; full-cycle ROIIC ~3% over eight
   years is the core fact. Two of two random live draws in this frame family (HARSHA, SHK) have ROIC below CoE.
4. **Category-split vote results make L42's dissent rule exact.** SHK's scrutiniser report splits promoter / institutional / non-institutional
   votes, so dissent net of promoter votes needs no assumption (~42% of non-promoter votes against a family director in 2025; headline
   5.2%). Also check whether promoters voted on their own family's re-appointment.
5. **Dates slip AND numbers miss can coexist.** Credibility 31% (−29 pts vs peers): margin guidance missed by 4–5 pts twice. L26's
   "numbers met" is a sector pattern, not a law — keep scoring numbers and dates separately.
6. **Chemicals checks (new): the China-price cycle cuts both ways inside one company** (compounder = buyer of Chinese aroma chemicals;
   ingredients arm = competitor). Pollution-board check: no structured public source; NSE/BSE keyword scans + AR found nothing, and a web
   search could not tie an MPCB "fire incident… directions" minute to the company. Candidate tool: an MPCB/GPCB/CPCB directions scraper
   keyed by unit address.
7. **S0 observation:** two consecutive draws were walk #1 with no skips. The skip rules (scheme, fraud, pledge > 50%, PEAD Q1–Q2, red
   solvency) remove a minority of names; the method is getting "typical" companies, which is the point. Keep counting.
8. **Tool notes:** `nse_fetch.py announcements` prints only 15 rows in summary mode — use `--raw`/`--out` for the full list (178 here);
   XBRL tagging moved contract-manufacturing COGS from materials (FY25) to other expenses (FY26+), which breaks a naive materials ratio;
   the AR geography table contradicts the deck; `decision_card.py` still does not validate fraction inputs (validated by hand, L42); a
   single tail-anchor weight cannot express "raise one tail, keep the other" (lesson candidate for card v1.6).

## 11. Open items
CRISIL rationale for the Negative outlook; total insurance claim and remaining receivable; MPCB consent status for Vashivali/Vanavate;
Mulund land ownership and plan; pricing basis of Keva Aromatics purchases; legal & professional fees (₹70 cr) breakdown; creative-centre
revenue by country; AR geography reclassification; FY25 "15% growth" claim; capacity/utilisation of Indian plants; Maharashtra gazette
check (L41); succession after the chairman's death and the inter-se promoter transfers; postal-ballot results (four IDs, Dec-2026).

## Sources
- AR FY2025-26: https://nsearchives.nseindia.in/annual_reports/AR_29522_SHK_2025_2026_A_9351211_01072026182209.pdf
- Q2 FY27 consolidated XBRL: https://nsearchives.nseindia.in/corporate/xbrl/INTEGRATED_FILING_INDAS_1751494_02112026084816_WEB.xml ; Q1 FY27 1703450; FY26 1668119; Q3 FY26 1620764; FY25 1441723 (same path pattern)
- Q2 FY27 press release + deck: https://nsearchives.nseindia.in/corporate/9152077850_02112026204826_SHKPressReleaseInvestorPPTSigned.pdf
- Q2 FY27 transcript: https://nsearchives.nseindia.in/corporate/aditya_joshi_keva_co_in_06112026112611_SHKConcallTranscriptIntimationQ2FY27FinalSigned.pdf ; Q1 FY27 https://nsearchives.nseindia.in/corporate/9152077850_04082026142658_SHKCONCALLtranscriptQ1.pdf ; Q4 FY26 https://nsearchives.nseindia.in/corporate/aditya_joshi_keva_co_in_21052026180647_SHKQ4FY26ConcallTranscriptFinalSigned.pdf ; Q2 FY26 https://nsearchives.nseindia.in/corporate/9152077850_14112025195823_Concall_Transcript_Q2H26.pdf ; Q4 FY25 https://nsearchives.nseindia.in/corporate/9152077850_27052025141201_SHKQ4FY2025Transcript.pdf ; Q2 FY25 https://nsearchives.nseindia.in/corporate/SHK_26112024114013_TranscriptofInvestorCallQ2FY2025.pdf
- AGM 2026 voting results: https://nsearchives.nseindia.in/corporate/9152077850_01082026165135_SHKVotingResults2026Final.pdf ; AGM 2025: https://nsearchives.nseindia.in/corporate/9152077850_13082025195609_SHKSEINTIMATIONREG44.pdf
- CRISIL reaffirmation (Reg-30 28-Sep-2026): https://nsearchives.nseindia.in/corporate/9152077850_28092026161723_SHKCRISILCreditRatingIntimationFinalSigned.pdf
- Auditor: https://nsearchives.nseindia.in/corporate/9152077850_15052026204720_SHKBMOutcome15052026FinalSigned.pdf ; https://nsearchives.nseindia.in/corporate/9152077850_08082025194012_SHK_-_SE_Intention_of_Appointment_of_Auditor.pdf ; https://nsearchives.nseindia.in/corporate/9152077850_16052025203923_BMOutcomeMay2025.pdf
- Exchange cautionary letters: https://nsearchives.nseindia.in/corporate/ankita_bhanushali_keva_co_in_27102026184546_ExchangeLettersIntimation27102026Final.pdf
- Postal ballot notice 06-Nov-2026: https://nsearchives.nseindia.in/corporate/aditya_joshi_keva_co_in_06112026162546_PostalBallotIntimationFinalSigned.pdf
- SHP XBRL 30-Sep-2026: https://nsearchives.nseindia.in/corporate/xbrl/SHP_1734483_08102026060110_WEB.xml ; pledge API 25-Nov-2026; NSE bhavcopy sec_bhavdata_full_24112026.csv (DATE1 23-Nov-2026); Yahoo v8 SHK.NS, ^CRSLDX
- screener.in SHK (consolidated), PRIVISCL, OAL, GALAXYSURF (25-Nov-2026)
- [WEB] searches 25-Nov-2026 (no CRISIL rationale page; no MPCB order naming the company): crisil.com rating-rationale index; mpcb.gov.in minutes (1st CAC meeting Part II)
- Selection: `research_notes/Deep dives/SHK_selection/` (prereg_selection.md, selection_order.json)
