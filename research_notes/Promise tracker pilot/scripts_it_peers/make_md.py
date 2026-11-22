"""Write <TICKER>.md ledgers for the IT mid-cap peers from the seed (numbers come from build_seed/make_seed).
usage: python3 -I make_md.py <repo_root>"""
import json, os, sys
ROOT = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.dirname(HERE)
recs = json.load(open(os.path.join(ROOT, "memdb/seeds/2026-11-22_promises_it.json")))
calls = json.load(open(os.path.join(ROOT, "memdb/seeds/2026-11-22_paper_calls_credibility_it.json")))
S = json.load(open(os.path.join(HERE, "it_summary.json")))
NAMES = {"PERSISTENT": "Persistent Systems", "COFORGE": "Coforge", "MPHASIS": "Mphasis", "KPITTECH": "KPIT Technologies"}
METHOD = {
 "PERSISTENT": "- 6 calls: Q1FY26, Q2FY26, Q3FY26, Q4FY26 (company-website PDF via `fetch.py --local`; the NSE filing is a cover letter), the 28-Jun-2026 Nagarro acquisition call, Q2FY27. Persistent held no Q1FY27 earnings call (results 02-Aug-2026, during the Nagarro offer). `turns.py` needed `--roster`.",
 "COFORGE": "- 6 calls Q1FY26-Q2FY27, all downloaded from investors.coforge.com and passed with `fetch.py --local PDF@FILED`: Coforge's NSE transcript filings are one-page cover letters with a link.",
 "MPHASIS": "- 6 NSE calls Q1FY26-Q2FY27. `turns.py` could not split the Mphasis layout into speaker turns (0-3 management turns in 4 calls even with `--roster`), so the reading was done on the raw `pdftotext` output. `fetch.py` mis-dated the Q1FY26 call (2025-07-01); the header date 25-Jul-2025 is used.",
 "KPITTECH": "- 6 NSE calls Q1FY26-Q2FY27 (590 rule candidates). The Q4FY26 file is a long outlook call with run-together text."}
READ = {
 "PERSISTENT": ["Persistent says 'we don't give forward-looking guidance' on every call. Its scoreable near-term statements were all met: FY26 tax rate 22.6% (22.5-23.5% guided), FY26 EBIT +90 bp (~+100 bp guided), the Q3FY26 wage-hike walk (beaten ex the one-time labour-code charge, clarification C) and the deferred wage hike.",
                "Its two big aspirations are pending and both were quietly re-framed. 'Reach USD 2 billion by FY27' (Jul-2025, 'we need a CAGR of 19-20%') became, in Apr-2026, 'that's a run rate ... Q4 exit ... in the range of $500 million or so, plus minus a quarter at worst'. '+200-300 bp from 14.7% by FY27' (i.e. 16.7-17.7%) became 'our aspiration continues to be in the 16 to 17% range' and 'we have achieved whatever we had said'. Neither change was acknowledged as a change. Under pipeline v1.1 they stay pending with a goalpost flag and are resolved at the deadline.",
                "Nagarro (announced 27-Jun-2026; 94% tendered by Oct; closing expected Dec-2026/Jan-2027) will blur both FY27 tests: it lifts reported revenue and its ~13.9% EBITDA margin dilutes EBIT. The revenue call therefore uses ex-Nagarro revenue and voids if that is not disclosed.",
                "Only 4 scored promises: the 100% delivery rate says little. The shrink weight (0.17) keeps it from moving the calls much."],
 "COFORGE": ["Coforge is the only explicit guider in the set: EBIT, EBITDA, FCF/PAT and ETR numbers, raised or restated almost every call, with a CEO script that cites its own past promises ('made sure they came true').",
             "Hard financial guidance was met or beaten: FY26 EBIT 14.4% vs 14%; Q4FY26 16.6% vs 15%; FCF/PAT 110% vs 70-80%; Encora closed inside the Mar-Apr 2026 window.",
             "The misses are softer statements: 'H2 should be robust' then a 2.0% CC Q4; a Q3 wage hit described as 'very, very limited' that cost 150 bp; the Cigniti merger ~2-3 months after 'December, January' (NCLT timetable, acknowledged); normalised ETR 23% vs 23.5-24%.",
             "FY27 is pending: EBITDA 20.5-21% (H1 20.5%), EBIT raised 15.5% -> 16% (H1 16.0%), FCF/PAT 100% (H1 92%), no EPS dilution from Encora. Reported growth is inflated by Encora from May-2026, so 'industry growth leader' needs an organic read."],
 "MPHASIS": ["Company-level guidance was met: FY26 '~2x industry growth' (6.7% CC; 'industry' is Mphasis's own benchmark, single-source) and the 14.75-15.75% EBIT band (15.3%, every quarter inside).",
             "Vertical and working-capital promises were not. Logistics & Transportation: 'recover through the remainder of the year' (Jul-25) -> 'sequential growth from Q3' (Oct-25) -> 'gradually recover through FY27' (Apr-26) -> -12% QoQ in Q2FY27. The FY26 version is scored moved-goalpost (re-dated without acknowledgement).",
             "DSO 'normalise over the next three to four quarters' (Oct-25, 89 days) went to 105 days (Q2FY27, company-normalised). The miss was explained (remittance timing, fixed-price mix) and a new promise made: double digits in Q3FY27 - one of the calls.",
             "FY27 guidance was raised in Nov-2026 to low-double-digit CC growth (acquisitions included); the EBIT band is held but sits near its 14.75% floor (H1 ~14.7-14.8% on both company and screener-derived bases)."],
 "KPITTECH": ["Every FY26 statement resolved delivered or partly: EBITDA 'maintain 21%' -> 20.8%; H2 > H1; Q3 'marginal' growth (+1.5% CC); Q4 'highest growth quarter' (+1.8% CC, barely; 'meaningful' growth was implied, scored partly).",
              "The record breaks in FY27, but the score cannot show it yet because nothing has resolved. In Jan-2026 KPIT said FY27 growth would 'for sure' beat FY26, and on 7-May-2026 it guided FY27 EBITDA 20.5-21.2%. Weeks later Q1FY27 came in at 17.2% EBITDA and -3.6% CC QoQ (two largest SDV programmes ended). Recovery has slid from 'by Q4' (Jul-26) to 'early next year when we get there' (Oct-26).",
              "This is the clearest example in the IT set of a good scored record next to a probable large miss on the most important current guidance. The credibility rule (P = 0.75 for the FY27 EBITDA call) will look badly wrong on it, and that is part of what the test measures: the rule ignores in-year progress by design.",
              "Company EBITDA and screener OPM differ by ~2 pp for KPIT (FY26 20.8% vs 18.9%), so the EBITDA call is assisted, not structured."]}

def md(T):
    a = next(r for r in recs if r["type"] == "analysis" and r["tickers"][0] == T); d = a["data"]
    ps = [r for r in recs if r["type"] == "promise" and r["tickers"][0] == T]
    sac = S["sac"][T]; base = S["base_rates_leave_one_out"][T]
    L = [f"# Promise tracker: {NAMES[T]} (NSE: {T})", "",
         f"*As of 22-Nov-2026. Research, not SEBI-registered advice. This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*",
         f"Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `IT_MIDCAPS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_it.json` (`{a['id']}`). Ledger source: `scripts_it_peers/promises_{T}.py`.", "",
         "## 1. Method", "",
         METHOD[T], "- Pipeline v1.2 (`fetch.py --since 2025-07-01`, `turns.py`, `candidates.py` with the new IT vocabulary: deal_wins / people / client_concentration categories; CC growth, TCV, EBIT band measures in `score.py`).",
         "- LLM step done by Claude by hand: full opening remarks, every tier-A or volunteered guidance sentence, and targeted greps of later calls for outcomes. Restatements are folded into the first promise (`later_restatements`), not double-counted.",
         "- Outcomes: IT KPIs (CC growth, EBIT/EBITDA margin as the company defines it, TCV, DSO, large deals) from the company's own later calls (single-source); INR revenue and screener-derived margins re-computed from screener's quarterly table as a cross-check (they differ from company EBIT/EBITDA for Persistent, Coforge and KPIT).",
         "- Scoring: pilot formula unchanged (`scripts_TD_peers/build_seed.py`; T&D clarifications A-D apply). Credit delivered 1 / partly 0.5; MCS weights specificity x materiality x recency.", "",
         "## 2. Scores", "",
         "| Measure | Value |", "|---|---|",
         f"| Promises logged / scored | {d['n_promises']} / {d['n_scored']} |",
         f"| Status counts | {', '.join(f'{k} {v}' for k, v in sorted(d['status_counts'].items()))} |",
         f"| Weighted delivery ratio | {d['weighted_delivery_ratio_pct']}% |",
         f"| Specificity-only delivery | {d['specificity_weighted_delivery_ratio_pct']}% |",
         f"| Raw hit rate | {d['raw_hit_rate_pct']}% |",
         f"| MCS (-1.5 .. +1) | {d['mcs_schema_scale']:+.2f} |",
         f"| Candour index (shortfalls admitted unprompted) | " + (f"{d['candour_index_pct']}% ({d['n_shortfalls_admitted_unprompted']}/{d['n_shortfalls']})" if d["n_shortfalls"] else "n/a (no shortfalls scored)") + " |",
         f"| **Sector-adjusted credibility (SAC)** | **{sac['sac_pts']:+.1f} pts** (shrink weight {sac['shrink_weight']} at N={sac['n_scored']}) |", "",
         "By category (credit basis): " + "; ".join(f"{c} {v['delivery_ratio_pct']}% (n={v['n']})" for c, v in d["by_category"].items()) + ".",
         "SAC components: " + "; ".join(f"{k}: own {v['own']}% vs peer median {v['peer_median']}% (n={v['n']}, gap {v['gap']:+})" for k, v in sac["components"].items()) + ".", "",
         "**Caveat: n is small** (6 calls; 4-10 scored promises; most FY27 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.", "",
         "## 3. Reading", ""] + [f"- {x}" for x in READ[T]] + ["",
         "## 4. Ledger", "", "| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(ps, key=lambda r: r["date"]):
        x = r["data"]; ev = (x.get("evidence") or "").replace("|", "/")
        L.append(f"| {x['said_on']} | {r['title'].replace('|','/')} | {x['category']} | {x['specificity']} | {'V' if x['volunteered'] else 'P'} | {x['deadline']} | **{x['status']}** | {ev[:260]}{'...' if len(ev) > 260 else ''} |")
    L += ["", "## 5. Credibility-generated forward calls (rule-set probabilities)", "",
          "Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `IT_MIDCAPS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.", "",
          "| Call | Category | P(ours) | P(base) | Resolve by | Resolver |", "|---|---|---|---|---|---|"]
    for c in calls:
        if c["tickers"][0] != T: continue
        x = c["data"]; L.append(f"| `{c['id']}` - {c['title'][len('Paper call: '):]} | {x['promise_category']} | {x['probability']:.2f} | {x['base_rate_probability']:.2f} | {x['resolve_by']} | see specs.json |")
    L += ["", "## Sources", ""] + [f"- {r} " for r in sorted({u for p in ps for u in p['sources']})]
    return "\n".join(L) + "\n"

for T in NAMES:
    open(os.path.join(OUTD, f"{T}.md"), "w").write(md(T)); print("wrote", T)
