# Antigravity vs our gold study — comparison (28-Nov-2026)

Antigravity (Gemini 4 Neon, effort high, run on the user's Pi, blind to our work) vs `research_notes/Gold/gold_study_2026-11/`
(Claude, pre-registered). Spot checks done against our Yahoo GC=F daily file (fetched 28-Nov-2026).

## Spot checks of Antigravity's numbers
| Item | Antigravity | Our data | Verdict |
|---|---|---|---|
| 27-Nov close | $3,654.58 spot (Investing/Kitco/Myfxbook) | $3,639.6 futures (GC=F) | ✅ consistent (spot vs futures basis) |
| Intraday record | $5,595.47 (29-Jan) | $5,586.2 futures high | ✅ |
| Closing record | $5,405 (LBMA PM) | $5,318.4 futures close | ✅ different benchmark, both valid |
| Recent low | $3,426.48 intraday 24-Nov | $3,425.2 futures low (Yahoo dates it 25-Nov) | ✅ — **we missed this**: we only used closes ($3,515) |
| Real yield / DXY / USD-INR | 2.78% / 103.99 / 92.98 | 2.73–2.79% / 104.0 / 92.45–92.99 | ✅ |
| 30-Jan-2026 close | $4,865 (StatMuse, single-source) | $4,745 futures | ⚠️ ~2.5% off; single-source as it flagged |
| India duty history | Feb-2026 Budget cut to 5%, then 15% from 13-May-2026 | our study: Feb Budget left it at 6% | ❌ **conflict — unresolved; check the CBIC notifications** |
| RBI repo | 5.50%, hiked +25 bp in Oct-2026 | we had "hike undated" (L51) | ➕ fills our gap (single-source; verify) |
No obvious invented numbers found in the spot checks. Its own "unsure" list was honest and specific.

## Where Antigravity was better
- **Breadth of current drivers:** Oct-2026 FOMC 10–2 hold with hawkish dissents, core PCE 3.3%, Q3 GDP 4.3%, weekly ETF outflows
  (−20.7 t), CFTC hedge-fund selling, Indian dealer premium ($19/oz), RBI gold reserves. We had fewer of these.
- **The Indian buyer's real price:** it priced gold **landed in India** (duty + rupee). Its point: in rupees with duty, gold is
  roughly flat over 1 year, because the duty jump to 15% and the weaker rupee offset the dollar fall. Combining both studies:
  from the January peak an Indian buyer is down ≈ −25%, not −31% (−31% world price × 1.15/1.06 duty change).
- **More complete history:** it lists the 1983–85, 1987–93 and 1996–99 falls separately (10 episodes); our monthly-average
  method folded them into one 1980–99 episode. Its median fall (~39–44%) agrees with ours (−39%).

## Where our study was better
- **Auditability:** every Antigravity source is a temporary Google "grounding redirect" link — not a real URL, may expire, can't
  be re-checked later. Its history comes from aggregators (TaxFreeGold, StatMuse), not primary series. No code, so it can't be rerun.
- **Probabilities:** its scenario odds (best 15 / base 45 / bad 28 / worst 12) are narrative judgment. Ours are derived from
  conditional base rates (real-yield regime, run-up size), pre-registered, with a sensitivity check.
- **Tested relationships:** we measured that real yields, not the Fed's hike/cut label, explain gold (correlation −0.4; every
  recovery began with real yields falling). Antigravity *states* real yields matter but doesn't test it.

## Where the two disagree on the outlook (both get scored)
| Next 12 months from ~$3,650 | Antigravity | Our study |
|---|---|---|
| Strong rebound (> +25%) | 15% | 9% |
| Base | 45% (to ~$4,100, +12%) | 52% (−5% to +25%) |
| Bad (−5% to −25%) | 28% | 34% |
| Worst (< −25%) | 12% | 5% |
Antigravity is more two-sided (more upside *and* more crash). Ours is more "flat-to-down for a while".

## Verdict on Antigravity as a worker
**Good first-pass researcher; not a final authority.** It is fast and broad at gathering current facts and was honest about
uncertainty. It cannot yet be trusted for (a) auditable sourcing, (b) derived probabilities, (c) reproducible data. Use it for:
news/driver sweeps, filling gaps, and as an independent second opinion we score. Every number it gives gets checked by us.

**Next prompt changes for Antigravity:** require real article URLs (no redirect links) + saving each source page as text;
require primary series (LBMA/FRED/RBI) downloaded to data/ with as_of; ask it to show how each probability was derived.
