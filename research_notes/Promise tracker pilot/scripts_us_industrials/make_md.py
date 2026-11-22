"""Write <TICKER>.md ledgers for the US industrials peers from the seed (numbers come from build_seed/make_seed).
usage: python3 -I make_md.py <repo_root>"""
import json, os, sys
ROOT = sys.argv[1]; HERE = os.path.dirname(os.path.abspath(__file__)); OUTD = os.path.dirname(HERE)
recs = json.load(open(os.path.join(ROOT, "memdb/seeds/2026-11-22_promises_us_industrials.json")))
calls = json.load(open(os.path.join(ROOT, "memdb/seeds/2026-11-22_paper_calls_credibility_us.json")))
S = json.load(open(os.path.join(HERE, "us_summary.json")))
NAMES = {"US-WTS": "Watts Water Technologies", "US-AOS": "A. O. Smith", "US-SSD": "Simpson Manufacturing", "US-LECO": "Lincoln Electric"}
EXCH = {"US-WTS": "NYSE: WTS", "US-AOS": "NYSE: AOS", "US-SSD": "NYSE: SSD", "US-LECO": "NASDAQ: LECO"}
METHOD = {
 "US-WTS": "- 6 calls Q2-2025..Q3-2026: 5 Motley Fool transcripts (curl, UA 'Mozilla/5.0', HTML -> text) plus the Q3-2025 8-K Ex 99.1 press release (no Fool transcript found; its 'Full Year 2025 Outlook' paragraph stands in for the call). Fool page dates are publication dates: the Q4-2025 call is dated 12-Feb-2026 (8-K filed 11-Feb), Q2-2026 06-Aug-2026.",
 "US-AOS": "- 6 Motley Fool transcripts Q2-2025..Q3-2026 (the Q2-2026 call is listed twice; the 30-Jul-2026 copy is used). The CFO's outlook section was read in full on every call. CFO changed in Q3-2026 (Charles Lauber -> Carrie Anderson).",
 "US-SSD": "- 6 calls Q2-2025..Q3-2026: 5 Motley Fool transcripts plus the Q2-2026 8-K Ex 99.1 'Business Outlook' section (no Fool transcript found). Call dates from the transcripts' DATE lines (Monday after-close calls), not the fool.com publication dates.",
 "US-LECO": "- 6 calls Q2-2025..Q3-2026: 4 Motley Fool transcripts plus the Q2-2025 and Q2-2026 8-K Ex 99.1 press releases (no Fool transcripts found). Lincoln's releases carry almost no outlook, so those two quarters add only the Alloy Steel closing. **Thinnest read of the four.**"}
READ = {
 "US-WTS": ["Every scored promise was met or beaten (12 of 12): FY2025 organic flat to +3% (Aug) -> +5%; reported +2-5% -> +8.4% (XBRL); adjusted operating margin +50-110 bp -> +190 bp; FCF conversion >=100% -> 104.5% (XBRL re-derived); every next-quarter organic and margin band beaten (Q3-25 organic +9% vs 2-5%; Q1-26 +12% vs 4-8%; Q2-26 +12.2% vs 4-8%).",
            "This is the profile of a **systematic sandbagger**: guidance was raised at every call in 2025-26 (FY2026 organic 2-6% -> 8-11% -> 11-12%). A 100% delivery record is evidence of conservative guiding, not of foresight. Data-centre demand (now high-single-digit % of sales) drove most of the 2026 beats.",
            "Pending FY2026: organic 11-12%, reported 17-18%, adjusted operating margin 20.3-20.4%, FCF conversion >=90%, Q4 organic 9-12%. These are now one-quarter-ahead guides, so delivery should be high again.",
            "The rule still gives WTS only P = 0.47 on its two FY2026 growth calls, because the peers' strict revenue/growth delivery is low (41%, dragged by A. O. Smith's China and water-treatment misses) and the shrink weight is 0.375. This is the case where 'company credibility' (very high) and 'sector base rate' (low) disagree most: a good test of the shrink."],
 "US-AOS": ["FY2025 company-level guidance was met: EPS $3.85 in a $3.70-3.90 band (narrowed to $3.70-3.85 in Oct), FCF $546 mn vs $500-525 mn, North America margin 24.4% in 24-24.5%, Rest of World 8.7% in 8-9%, buybacks $401 mn vs ~$400 mn (all XBRL-checked where tagged).",
            "The misses are China and sub-lines: FY2025 China -5..-8% (Jul) -> 'down 10%' (Oct) -> -12%; FY2025 capex $70.8 mn vs ~$75 mn.",
            "**FY2026 guidance was cut three times.** EPS $3.85-4.15 (Jan) -> $3.70-4.00 adjusted (Apr) -> $3.70-3.85 (Jul) -> $3.42-3.52 ex-China, continuing operations (Oct). Rest of World margin 8-9% -> 6-7%; water-treatment growth 10-12% -> 5-6% -> 3-4%; China 'mid-single-digit decline, growth in H2' -> 'low double digits' -> sold. Each cut was explicit and explained more than two quarters before the deadline, so clarification A scores them **withdrawn** (-0.5), not missed. Candour is high (7 of 8 shortfalls admitted unprompted).",
            "Leonard Valve: '~$70 mn of 2026 sales' (Jan, Jul) cut to $55 mn in Oct (final quarter: scored on outcome when FY2026 reports; 9M = $47 mn).",
            "The China sale (81% to CPE, $400 mn, close 'first half of 2027') is one of the calls. It changes the measurement basis of every FY2026 total-company promise: the calls use the ex-China, continuing-operations figures the company now guides."],
 "US-SSD": ["Simpson guides only a GAAP consolidated operating-margin band (2 pts wide in Jul-2025 and Feb-2026), capex and tax rate: no sales or EPS guidance. Wide bands are easy to hit: FY2025 19.66% (XBRL re-derived) sat inside both 18.5-20.5% and 19-20%. The bands include one-off property-sale gains ($12.9 mn in 2025; ~$11 mn land sale planned for Q4-2026).",
            "Near misses on capacity and capex: FY2025 capex $161.0 mn vs $140-160 mn and $150-160 mn (0.6% over: partly). The Gallatin fastener plant opened on time in Q3-2025 but was still ramping in Q1-2026 (~100 bp gross-margin headwind), against 'fully operational by the end of this year': partly.",
            "Delivered: >=35% of FCF returned (56%); the 2025 price actions were worth ~$130 mn annualised vs ~$100 mn guided.",
            "Pending FY2026: margin band (narrowed to 20.0-20.5%), capex $80-90 mn (raised from $75-85 mn in Jul), the >=$30 mn cost programme and an opex cut of $10-15 mn. With only 7 scored promises, the SAC (-7.0) is mostly the capex/plant near-misses."],
 "US-LECO": ["Lincoln guides in words ('mid single digit', 'modest improvement') plus segment EBIT-margin bands, incremental margin, capex and cash conversion - few hard numbers.",
             "Near-term Q4-2025 statements were met: automation +20% QoQ vs '15-20%'; adjusted operating margin 18.0% vs Q3's 17.4% ('modest sequential improvement'); Americas Welding ~20% vs '18-19%'; International 11.8% inside '11-12%'.",
             "The one miss: in Oct-2025 the FY2025 cash-conversion range was **raised** to 'above 100%'; the year came in at 97% (FCF $534.2 mn / adjusted net income $551.3 mn, Q4-2025 release table) and the Q4 call did not mention it.",
             "FY2026: sales growth guide raised twice (mid single digit -> high single digit -> low teens); capex raised from $110-130 mn to $140-150 mn in the final quarter (scored on outcome). 2030 targets (19% average margin, >$6 bn sales) are logged pending.",
             "Only 6 scored promises and two of six calls read from press releases only: treat the score as a placeholder."]}

def md(T):
    a = next(r for r in recs if r["type"] == "analysis" and r["tickers"][0] == T); d = a["data"]
    ps = [r for r in recs if r["type"] == "promise" and r["tickers"][0] == T]
    sac = S["sac"][T]; base = S["base_rates_leave_one_out"][T]
    L = [f"# Promise tracker: {NAMES[T]} ({EXCH[T]}; memdb ticker {T})", "",
         f"*As of 22-Nov-2026. Research, not investment advice (not SEBI- or SEC-registered). This measures how reliably management's own forward statements came true; it is not a stock view and carries no buy/sell language.*",
         f"Roadmap: stage 3 (credibility signal) feeding stage 7 (credibility-generated paper calls). Peer comparison: `US_INDUSTRIALS_peer_comparison.md`. Seed: `memdb/seeds/2026-11-22_promises_us_industrials.json` (`{a['id']}`). Ledger source: `scripts_us_industrials/promises_{T}.py`.", "",
         "## 1. Method", "",
         METHOD[T], "- Ledger built by hand (fetch.py reads NSE, not US sources): Motley Fool takeaway list + targeted greps of the full text (guidance, outlook, organic, adjusted operating margin, EPS, free cash flow / conversion, capex, savings, price/cost). Quotes marked [Fool summary] are the transcriber's takeaway wording, not management's words. Pipeline v1.3 adds the US measure vocabulary to `score.py` for future runs.",
         "- Restatements are folded into the first promise (`later_restatements`), not double-counted; a cut >= 2 quarters before the deadline is 'withdrawn' (clarification A).",
         "- Outcomes: company-adjusted KPIs (organic growth, adjusted operating margin, adjusted EPS, segment margins) from the company's own later calls/releases (single-source); GAAP revenue, operating income, EPS, capex, FCF, buybacks and dividends re-derived from SEC XBRL companyfacts (`tools/sec_fetch.py facts`) as the second source.",
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
         "**Caveat: n is small** (6 calls; 6-18 scored promises; most FY2026 guidance pending). Categories rarely reach the L18 threshold of 5 scored promises with 2+ peers, so SAC is computed on pooled categories and shrunk toward zero (N/(N+20)) when used.", "",
         "## 3. Reading", ""] + [f"- {x}" for x in READ[T]] + ["",
         "## 4. Ledger", "", "| Said | Promise | Cat | Spec. | Vol. | Deadline | Status | Evidence |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(ps, key=lambda r: r["date"]):
        x = r["data"]; ev = (x.get("evidence") or "").replace("|", "/")
        L.append(f"| {x['said_on']} | {r['title'].replace('|','/')} | {x['category']} | {x['specificity']} | {'V' if x['volunteered'] else 'P'} | {x['deadline']} | **{x['status']}** | {ev[:260]}{'...' if len(ev) > 260 else ''} |")
    L += ["", "## 5. Credibility-generated forward calls (rule-set probabilities)", "",
          "Probabilities come only from the pre-stated rule in `AUTO_COMPONENTS_peer_comparison.md` section 5 (reused unchanged; `US_INDUSTRIALS_peer_comparison.md` section 5): P(base) = leave-one-out peer delivery rate for the category; P(ours) = P(base) + shrink x SAC. No judgment adjustment.", "",
          "| Call | Category | P(ours) | P(base) | Resolve by | Resolver |", "|---|---|---|---|---|---|"]
    for c in calls:
        if c["tickers"][0] != T: continue
        x = c["data"]; L.append(f"| `{c['id']}` - {c['title'][len('Paper call: '):]} | {x['promise_category']} | {x['probability']:.2f} | {x['base_rate_probability']:.2f} | {x['resolve_by']} | see specs.json |")
    L += ["", "## Sources", ""] + [f"- {r} " for r in sorted({u for p in ps for u in p['sources']})]
    return "\n".join(L) + "\n"

for T in NAMES:
    open(os.path.join(OUTD, f"{T}.md"), "w").write(md(T)); print("wrote", T)
