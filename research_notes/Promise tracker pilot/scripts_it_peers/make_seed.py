"""Assemble memdb/seeds/2026-11-22_promises_it.json for the IT mid-caps peer set:
PERSISTENT + COFORGE + MPHASIS + KPITTECH ledgers (this folder). Copied UNCHANGED from scripts_auto_peers/make_seed.py
except the company list (no pilot company), tags, ids and the insight text. MIN_N, MIN_POOL, MIN_PEERS and SHRINK_K
and the adjustment rule are identical (pre-stated in AUTO_COMPONENTS_peer_comparison.md section 5).
sector medians by category, sector-adjusted credibility (SAC) with the >=5-promises rule, and the leave-one-out base rates
used by the credibility-generated paper calls.
usage: python3 -I make_seed.py <repo_root> <out_seed.json> <out_summary.json>"""
import json, sys, os, statistics as st, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT, OUT, SUMOUT = sys.argv[1], sys.argv[2], sys.argv[3]
sp = importlib.util.spec_from_file_location("ab", os.path.join(HERE, "build_seed.py")); B = importlib.util.module_from_spec(sp); sp.loader.exec_module(B)
SPEC_W, CAT, SCORE = B.SPEC_W, B.CAT, B.SCORE
CATS = ["revenue_growth", "margin", "capacity", "other"]
MIN_N = 5            # L18: quote a category gap only with >= 5 scored promises
MIN_POOL = 8         # base rate for a category needs >= 8 scored peer promises, else all-category peer rate
MIN_PEERS = 2        # a category gap needs >= 2 peers with scored promises in it, else the category is pooled
SHRINK_K = 20        # empirical-Bayes shrink: weight on SAC = N/(N+20)

recs, rows = [], {}   # rows[T] = list of (category_group, specificity, status)
for T in ("PERSISTENT", "COFORGE", "MPHASIS", "KPITTECH"):
    r, s = B.build(B.load(os.path.join(HERE, f"promises_{T}.py"))); recs += r
    rows[T] = [(CAT.get(x["data"]["category"], x["data"]["category"]), x["data"]["specificity"], x["data"]["status"])
               for x in r if x["type"] == "promise" and x["data"]["status"] in SCORE]
for T in rows:
    rows[T] = [(c if c in CATS else "other", s, z) for c, s, z in rows[T]]
TICK = list(rows)

def rate(rs, strict=False):
    w = sum(SPEC_W[s] for _, s, _ in rs)
    if not w: return None
    cr = (lambda z: 1.0 if z == "delivered" else 0.0) if strict else (lambda z: {"delivered": 1.0, "partly": 0.5}.get(z, 0.0))
    return round(100 * sum(cr(z) * SPEC_W[s] for _, s, z in rs) / w, 1)

cat = {T: {c: {"n": sum(1 for x in rows[T] if x[0] == c), "D": rate([x for x in rows[T] if x[0] == c]),
               "S": rate([x for x in rows[T] if x[0] == c], True)} for c in CATS if any(x[0] == c for x in rows[T])} for T in TICK}
overall = {T: {"n": len(rows[T]), "D": rate(rows[T]), "S": rate(rows[T], True)} for T in TICK}

sac = {}
for T in TICK:
    N = len(rows[T])
    big = [c for c in cat[T] if cat[T][c]["n"] >= MIN_N and sum(1 for o in TICK if o != T and c in cat[o]) >= MIN_PEERS]
    small = [c for c in cat[T] if c not in big]
    parts, total = {}, 0.0
    for c in big:
        peers = [cat[o][c]["D"] for o in TICK if o != T and c in cat[o]]
        if not peers: continue
        g = cat[T][c]["D"] - st.median(peers); parts[c] = {"n": cat[T][c]["n"], "own": cat[T][c]["D"], "peer_median": st.median(peers), "gap": round(g, 1)}
        total += cat[T][c]["n"] / N * g
    if small:
        own = rate([x for x in rows[T] if x[0] in small])
        peers = [rate([x for x in rows[o] if x[0] in small]) for o in TICK if o != T]
        peers = [p for p in peers if p is not None]
        n_s = sum(cat[T][c]["n"] for c in small)
        if peers:
            g = own - st.median(peers); parts["pooled:" + "+".join(small)] = {"n": n_s, "own": own, "peer_median": st.median(peers), "gap": round(g, 1)}
            total += n_s / N * g
    sac[T] = {"sac_pts": round(total, 1), "n_scored": N, "shrink_weight": round(N / (N + SHRINK_K), 3), "components": parts}

base = {}
for T in TICK:
    others = [x for o in TICK if o != T for x in rows[o]]
    allr = rate(others, True); b = {"_all": {"n": len(others), "p0_pct": allr}}
    for c in CATS:
        rc = [x for x in others if x[0] == c]
        b[c] = {"n": len(rc), "p0_pct": rate(rc, True) if len(rc) >= MIN_POOL else allr, "fallback_all": len(rc) < MIN_POOL}
    base[T] = b
sector_med = {c: (st.median([cat[T][c]["D"] for T in TICK if c in cat[T]]) if any(c in cat[T] for T in TICK) else None) for c in CATS}  # IT has no capacity promises
sector_pool = {c: {"n": sum(cat[T].get(c, {"n": 0})["n"] for T in TICK), "D": rate([x for T in TICK for x in rows[T] if x[0] == c]),
                   "S": rate([x for T in TICK for x in rows[T] if x[0] == c], True)} for c in CATS}

def adjusted(T, c):
    p0 = base[T][c]["p0_pct"] / 100; w = sac[T]["shrink_weight"]
    return round(min(0.95, max(0.05, p0 + w * sac[T]["sac_pts"] / 100)), 2), round(p0, 2)

summary = {"as_of": "2026-11-22", "companies": TICK, "category_map": CAT, "categories": CATS,
           "overall": overall, "by_category": cat, "sector_median_D_pct": sector_med, "sector_pooled": sector_pool,
           "sac": sac, "base_rates_leave_one_out": base,
           "adjustment_rule": "p0 = leave-one-out pooled STRICT delivery rate (specificity-weighted share 'delivered'; partly=0) of the other 3 peers in the promise's category (all-category peer rate if <8 peer promises in that category). p = clip(p0 + N/(N+20) x SAC/100, 0.05, 0.95), N = company's scored promises, SAC in points (credit basis: delivered 1, partly 0.5; categories with n<5, or with <2 peers having data, pooled). P(base) = p0.",
           "example_p": {T: {c: adjusted(T, c) for c in CATS} for T in TICK}}
json.dump(summary, open(SUMOUT, "w"), indent=1)

head = {T: overall[T]["D"] for T in TICK}
body = ("Same-method promise scores for four Indian IT mid-caps (last 6 calls each, Jul-2025 to Nov-2026; Persistent held no Q1FY27 call, its Jun-2026 Nagarro call is used). "
        f"Weighted delivery (credit, specificity-weighted): " + ", ".join(f"{T} {head[T]}% (n={overall[T]['n']})" for T in TICK) + ". "
        "Sector pattern: near-term company-level margin guidance (EBIT/EBITDA bands, quarter-ahead margin walks) is almost always met (pooled margin " + str(sector_pool['margin']['D']) + "%); "
        "growth-shape, vertical and timing statements are the weak part (pooled revenue/growth " + str(sector_pool['revenue_growth']['D']) + "%, other " + str(sector_pool['other']['D']) + "%). "
        "Most FY27 guidance is still pending and n is small (4-10 scored per company), so the big tests - KPIT's FY27 20.5-21.2% EBITDA guide against a 17.2-17.8% H1, Persistent's USD 2 bn and 16-17% EBIT aspirations, Coforge's raised 16% EBIT, Mphasis's low-double-digit growth - are not yet in the scores. "
        "SAC (pts vs leave-one-out peer medians): " + ", ".join(f"{T} {sac[T]['sac_pts']:+}" for T in TICK) + ". "
        "Use: base rates for credibility-generated paper calls (thesis tag credibility-generated, it). Provisional. Research, not advice.")
recs.append({"type": "insight", "id": "insight:it-midcaps-promise-credibility-base-rate",
             "title": "Base rate for management promise delivery in Indian IT mid-caps (PERSISTENT, COFORGE, MPHASIS, KPITTECH; Nov 2026)",
             "body": body, "tickers": TICK, "tags": ["india", "promise-tracker", "sector-it", "it", "governance", "base-rate", "process", "it-peer-calibration"],
             "date": "2026-11-22", "data": {k: summary[k] for k in ("as_of", "companies", "overall", "by_category", "sector_median_D_pct", "sector_pooled", "sac", "base_rates_leave_one_out", "adjustment_rule")},
             "sources": sorted({u for r in recs if r["type"] == "analysis" for u in r["sources"]}),
             "confidence": "single-source",
             "links": [{"to": f"analysis:{T}:credibility-2026-11", "rel": "about"} for T in TICK] +
                      [{"to": "insight:auto-components-promise-credibility-base-rate", "rel": "similar_to"},
                       {"to": "insight:td-epc-promise-credibility-base-rate", "rel": "similar_to"}]})
# put SAC into each new company's analysis record
for r in recs:
    if r["type"] == "analysis":
        T = r["tickers"][0]; r["data"]["sector_adjusted_credibility_pts"] = sac[T]["sac_pts"]; r["data"]["sac_components"] = sac[T]["components"]
        r["data"]["peer_set"] = TICK
json.dump(recs, open(OUT, "w"), indent=1, ensure_ascii=False); json.load(open(OUT))
print(len(recs), "records"); print(json.dumps({"overall": overall, "sac": {T: (sac[T]['sac_pts'], sac[T]['components']) for T in TICK}, "pool": sector_pool, "med": sector_med, "base": base, "ex": summary["example_p"]}, indent=0))
