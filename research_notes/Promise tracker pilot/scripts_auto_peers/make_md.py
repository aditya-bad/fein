"""Write <TICKER>.md ledgers for the auto-components peers from the seed (numbers come from build_seed/make_seed).
usage: python3 -I make_md.py <repo_root>"""
import json, os, sys
ROOT = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.dirname(HERE)
recs = json.load(open(os.path.join(ROOT, "memdb/seeds/2026-11-22_promises_sectors.json")))
calls = json.load(open(os.path.join(ROOT, "memdb/seeds/2026-11-22_paper_calls_credibility.json")))
S = json.load(open(os.path.join(HERE, "auto_summary.json")))
NAMES = {"SONACOMS": "Sona BLW Precision Forgings", "SANSERA": "Sansera Engineering", "HAPPYFORGE": "Happy Forgings", "ENDURANCE": "Endurance Technologies"}
READ = {
 "SONACOMS": ["Sona does not guide revenue ('we don't give forward growth guidance'). Its scoreable statements are mix targets (BEV share, non-auto share), a margin band and return ratios, so n is small (6 scored).",
              "The margin band drifted down in the open: 24-25% (Oct-25, met for FY26 at 24.7%) -> 23-25% (Apr-26) -> 'around 23%' (Oct-26). Each change was said out loud with a reason (railway consolidation, traction-motor mix, commodity lag). That is candour, not a goalpost move under the pilot rule.",
              "The one clear miss: 'recovery measures ... visible from quarter 2' (Jul-26) - Q2FY27 margin was flat at ~23% and management said so in the opening remarks.",
              "The non-auto >25% delivery is mostly mechanical (railway acquisition consolidated), so it says little about execution. Discount the +50 SAC accordingly - the shrink weight (0.23) already does most of that."],
 "SANSERA": ["Group revenue guidance was met: FY26 +15.9% vs 'at least the teens' / 'teens to mid-teens'. The start-of-year 'mid-to-high teens' was trimmed openly in Feb-26 (outside the 6-call window, not scored).",
             "ADS (aerospace/defence/semicon) guidance was met: INR 315 cr vs 280-300, run-rate ~38 cr/month vs 38-40.",
             "Capacity forecasts are the weak spot: FY26 capex INR 510 cr vs 375-400 guided seven weeks before year-end; the new ADS hangar re-dated Jun-Jul -> Jul-Aug -> 'towards October' 2026 without an explanation (moved-goalpost).",
             "The FY27 capex step-up (510 -> 800 cr) was announced openly with its reason (new ADS orders) and is scored withdrawn (-0.5), per clarification A."],
 "HAPPYFORGE": ["Margin promises are reliable: 'sustain ~28.6%' (Aug-25) -> FY26 30.4%; every quarter since is >=30.5% on screener.",
                "Near-term capacity was nearly on time (10,000-t press Q4FY26 as promised; 4,000-t press one quarter late, acknowledged).",
                "Big-project dates are not: the INR 650 cr heavy-component plant went from 'finished by Q2-Q3 FY27' (Aug-25) to 'commence operation in Q4 FY2028' (Nov-26) while every call in between said it was on schedule. That is the clearest silent goalpost move in this peer set.",
                "Also missed: a US PV programme ramp promised for Nov-Dec 2025 began in Q1-Q2 FY27; a hoped-for acquisition 'in 6-8 months' never came up again."],
 "ENDURANCE": ["Endurance gives no revenue or margin guidance. It gives many dated SOP (start-of-production) promises, and those slip: dual-channel ABS by 13 months, new ABS lines by about two quarters, Chennai brakes Q2FY27 -> March 2027, Bajaj and a Chinese OEM by 2 quarters each.",
               "About half the slips were explained (OEM clearance, the government's ABS-mandate guidelines, which hit every brake maker); the Chennai, Bajaj and Chinese-OEM re-dates were not.",
               "The P&L has not suffered yet (FY26 revenue +26%, OPM flat at 13.5%), so the low score is about date reliability, not business quality. Read SOP dates from this management with a 1-2 quarter haircut.",
               "Q2FY27 margin was guided up on the bigger Q1 base and fell instead (12.4% -> 11.7% on screener); new-plant drag and metal prices were admitted in the next opening remarks."]}

def md(T):
    a = next(r for r in recs if r["type"] == "analysis" and r["tickers"][0] == T); d = a["data"]
    ps = [r for r in recs if r["type"] == "promise" and r["tickers"][0] == T]
    sac = S["sac"][T]; base = S["base_rates_leave_one_out"][T]
    L = [f"# Promise tracker: {NAMES[T]} (NSE: {T})", "",
         f"*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*",
         f"Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `AUTO_COMPONENTS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_sectors.json` (`{a['id']}`). Ledger source: `scripts_auto_peers/promises_{T}.py`.", "",
         "## 1. Method", "",
         "- Last 6 earnings calls on NSE (Q1FY26 to Q2FY27), fetched with `tools/promise_tracker/pipeline/fetch.py --since 2025-01-01`; `turns.py` + `candidates.py` (rules) produced the candidate sentences.",
         "- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.",
         "- Outcomes: group numbers from screener.in consolidated (re-derived: growth and OPM computed from the quarterly table); segment, SOP and order figures from the company's own later calls (single-source).",
         "- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.", "",
         "## 2. Scores", "",
         "| Measure | Value |", "|---|---|",
         f"| Promises logged / scored | {d['n_promises']} / {d['n_scored']} |",
         f"| Status counts | {', '.join(f'{k} {v}' for k, v in sorted(d['status_counts'].items()))} |",
         f"| Weighted delivery ratio | {d['weighted_delivery_ratio_pct']}% |",
         f"| Specificity-only delivery | {d['specificity_weighted_delivery_ratio_pct']}% |",
         f"| Raw hit rate | {d['raw_hit_rate_pct']}% |",
         f"| MCS (-1.5 .. +1) | {d['mcs_schema_scale']:+.2f} |",
         f"| Candour index (shortfalls admitted unprompted) | {d['candour_index_pct']}% ({d['n_shortfalls_admitted_unprompted']}/{d['n_shortfalls']}) |",
         f"| **Sector-adjusted credibility (SAC)** | **{sac['sac_pts']:+.1f} pts** (shrink weight {sac['shrink_weight']} at N={sac['n_scored']}) |", "",
         "By category (credit basis): " + "; ".join(f"{c} {v['delivery_ratio_pct']}% (n={v['n']})" for c, v in d["by_category"].items()) + ".",
         "SAC components: " + "; ".join(f"{k}: own {v['own']}% vs peer median {v['peer_median']}% (n={v['n']}, gap {v['gap']:+})" for k, v in sac["components"].items()) + ".", "",
         "**Caveat: n is small** (6 calls; few hard numbers). No category reaches the L18 threshold of 5 scored promises with 2+ peers, except as noted, so SAC is computed on pooled categories and shrunk toward zero when used.", "",
         "## 3. Reading", ""] + [f"- {x}" for x in READ[T]] + ["",
         "## 4. Ledger", "", "| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(ps, key=lambda r: r["date"]):
        x = r["data"]; ev = (x.get("evidence") or "").replace("|", "/")
        L.append(f"| {x['said_on']} | {r['title'].replace('|','/')} | {x['category']} | {x['specificity']} | {'V' if x['volunteered'] else 'P'} | {x['deadline']} | **{x['status']}** | {ev[:260]}{'...' if len(ev) > 260 else ''} |")
    L += ["", "## 5. Credibility-generated forward calls (rule-set probabilities)", "",
          "Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5: P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.", "",
          "| Call | Category | P(ours) | P(base) | Resolve by | Resolver |", "|---|---|---|---|---|---|"]
    for c in calls:
        if c["tickers"][0] != T: continue
        x = c["data"]; L.append(f"| `{c['id']}` - {c['title'][len('Paper call: '):]} | {x['promise_category']} | {x['probability']:.2f} | {x['base_rate_probability']:.2f} | {x['resolve_by']} | see specs.json |")
    L += ["", "## Sources", ""] + [f"- {r} " for r in sorted({u for p in ps for u in p['sources']})]
    return "\n".join(L) + "\n"

for T in NAMES:
    open(os.path.join(OUTD, f"{T}.md"), "w").write(md(T)); print("wrote", T)
