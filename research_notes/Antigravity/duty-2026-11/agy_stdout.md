I am **blocked from completing the primary-source URL verification and verbatim source-file parts of this task** under the current toolset, and have recorded the preliminary findings and the exact blockage in [answer.md](file:///home/aditya/Desktop/money/agy-work/duty-2026-11/answer.md).

### Why this is blocked
1. **No built-in web page reading tool is available** in this environment (only `search_web` is available), and shell/terminal commands are prohibited by your instructions.
2. `search_web` returns synthesized search summaries rather than raw page/PDF text, and every source link it exposes is a `vertexaisearch.cloud.google.com/grounding-api-redirect/...` redirect URL that cannot be resolved without fetching it.
3. Because I cannot open any primary source page or PDF on `cbic.gov.in`, `egazette.gov.in`, `pib.gov.in`, or `indiabudget.gov.in`, I **did not create per-source verbatim `.txt` files** and **did not include redirect links or unverified/guessed direct document URLs**.

### Summary of Preliminary Findings (from `search_web` only — unverified against fetched primary PDFs)

| Change | Gold Category | CBIC Notifications (G.S.R.) | Notification Date | Effective Date | BCD | AIDC | Effective Rate |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Pre-Budget baseline | Gold bars (HS 7108) / Gold doré | Pre-existing 50/2017-Customs & 11/2021-Customs | Prior to 23 Jul 2024 | Through 23 Jul 2024 | 10% | 5% (bars) / 4.35% (doré) | **15%** (bars) / **14.35%** (doré) |
| Union Budget 2024–25 cut | Gold bars (HS 7108) / Gold doré | **30/2024-Customs** (`G.S.R. 433(E)`) & **32/2024-Customs** (`G.S.R. 435(E)`) *(plus companion 31/2024 & 33/2024)* | 23 Jul 2024 | 24 Jul 2024 | 5% | 1% (bars) / 0.35% (doré) | **6%** (bars) / **5.35%** (doré) |
| Exemption consolidation (rate unchanged) | Gold bars & doré (Table I S. Nos. 192, 194, 196) | **45/2025-Customs** (`G.S.R. 781(E)`, superseding 50/2017-Customs) & **44/2025-Customs** | 24 Oct 2025 | 1 Nov 2025 | 5% | 1% (bars) / 0.35% (doré) | **6%** (bars) / **5.35%** (doré) |
| Mid-year hike (May 2026) | Gold bars (HS 7108) / Gold doré | **15/2026-Customs** (`G.S.R. 358(E)`) & **16/2026-Customs** (`G.S.R. 359(E)`) *(plus companion 17/2026 & 18/2026)* | 12 May 2026 | 13 May 2026 | 10% | 5% (bars) / 4.35% (doré) | **15%** (bars) / **14.35%** (doré) |
| Post-May 2026 – 28 Nov 2026 | Gold bars / Gold doré | No further BCD/AIDC tariff-rate change found *(only periodic Section 14(2) N.T. USD tariff-value updates)* | — | In force on 28 Nov 2026 | 10% | 5% (bars) / 4.35% (doré) | **15%** (bars) / **14.35%** (doré) |

Discrepancies found across secondary search summaries (such as a conflicting report claiming 11% in July 2024 and another claiming a cut to 5% in Union Budget 2026) are documented in [answer.md](file:///home/aditya/Desktop/money/agy-work/duty-2026-11/answer.md).

If you would like me to directly open the official primary pages on `cbic.gov.in`, `egazette.gov.in`, `pib.gov.in`, and `indiabudget.gov.in`, verify the live non-redirect URLs, and save verbatim `.txt` files for each source, you can use the `/browser` command to enable web-page reading in this session.
