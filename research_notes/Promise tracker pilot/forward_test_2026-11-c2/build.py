#!/usr/bin/env python3
"""Promise-credibility forward test, cohort 2 (Nov-2026; roadmap stage 3 -> 7).

Applies the pre-registered rule (prereg.md in this folder, sha256 43f23229..., copied from cohort 1) to the
pipeline-built, Claude-reviewed past ledgers in past_c2.json:
  p0  = leave-one-out sector-peer strict delivery rate in the promise's group (fallbacks per prereg s4;
        Consumer Durables has no peer ledger -> pooled all-India group rate, leave-one-out)
  SAC = mean over the company's resolved past promises of (y - p0(group of that promise))
  P_cred = clip(p0 + N/(N+20) * SAC, 0.05, 0.95);  P_base = p0
Writes: ledger.json, memdb/seeds/2026-11-26_promise_forward_test_c2.json, specs_lines.txt (one-line specs to append).
Run from the repo root: python3 -I "research_notes/Promise tracker pilot/forward_test_2026-11-c2/build.py"
Research, not SEBI-registered advice.
"""
import json, os, sys

ROOT = os.getcwd()
HERE = os.path.join(ROOT, "research_notes", "Promise tracker pilot", "forward_test_2026-11-c2")
C1 = os.path.join(ROOT, "research_notes", "Promise tracker pilot", "forward_test_2026-11", "ledger.json")
MADE = "2026-11-26"
K = 20
sys.path.insert(0, HERE)
from forward_c2 import FWD, SECTOR, NAME  # noqa: E402

GROUP = {'revenue_growth': 'revenue', 'order_inflow': 'revenue', 'order_book': 'revenue', 'deal_wins': 'revenue',
         'margin': 'margin', 'capacity_commissioning': 'dates', 'capex': 'dates', 'new_product': 'dates',
         'approval_regulatory': 'dates', 'm&a': 'dates', 'customer_win': 'dates',
         'debt_reduction': 'balance_sheet', 'working_capital': 'balance_sheet'}
# existing India concall ledgers (prereg s4): file -> {ticker: sector}
PILOTS = {
    '2026-11-21_promises_TD_peers.json': {'KEC': 'Construction', 'KPIL': 'Construction'},
    '2026-11-19_promises_SKIPPER.json': {'SKIPPER': 'Capital Goods'},
    '2026-11-19_promises_UNIPARTS.json': {'UNIPARTS': 'Automobile and Auto Components'},
    '2026-11-22_promises_it.json': {'PERSISTENT': 'Information Technology', 'COFORGE': 'Information Technology',
                                    'MPHASIS': 'Information Technology', 'KPITTECH': 'Information Technology'},
    '2026-11-22_promises_sectors.json': {'SONACOMS': 'Automobile and Auto Components', 'SANSERA': 'Automobile and Auto Components',
                                         'ENDURANCE': 'Automobile and Auto Components', 'HAPPYFORGE': 'Capital Goods'},
}
C1_SECTOR = {'JASH': 'Capital Goods', 'KIRLOSBROS': 'Capital Goods', 'RISHABH': 'Capital Goods', 'ANUP': 'Capital Goods',
             'NEOGEN': 'Chemicals', 'GALAXYSURF': 'Chemicals', 'YASHO': 'Chemicals', 'TATVA': 'Chemicals',
             'KRSNAA': 'Healthcare', 'ORCHPHARMA': 'Healthcare', 'SYNGENE': 'Healthcare', 'SHILPAMED': 'Healthcare'}
NO_PEER_POOL = {'Consumer Durables'}


def pilot_rows():
    out = []
    for f, secs in PILOTS.items():
        default = next(iter(secs)) if len(secs) == 1 else None
        for r in json.load(open(os.path.join(ROOT, 'memdb', 'seeds', f))):
            if r.get('type') != 'promise': continue
            s = r['data'].get('status')
            if s in (None, 'pending', 'unverifiable'): continue
            sym = (r.get('tickers') or [default])[0] or default
            if sym not in secs: continue
            out.append((sym, secs[sym], GROUP.get(r['data'].get('category'), 'other'), 1 if s == 'delivered' else 0))
    return out


def rate(rows):
    return (sum(r[3] for r in rows) / len(rows), len(rows)) if rows else (None, 0)


def main():
    past = json.load(open(os.path.join(HERE, 'past_c2.json')))
    c2rows = [(p['sym'], SECTOR[p['sym']], GROUP.get(p['category'], 'other'), p['y']) for p in past]
    c1rows = [(p['sym'], C1_SECTOR[p['sym']], p['group'], p['y']) for p in json.load(open(C1))['past']]
    pil = pilot_rows()
    allrows = c2rows + c1rows + pil

    def p0(sym, grp):
        sec = SECTOR[sym]
        pooled = [x for x in allrows if x[0] != sym]
        if sec in NO_PEER_POOL:
            r3, n3 = rate([x for x in pooled if x[2] == grp])
            if n3 >= 8: return r3, n3, f"pooled all-India ledgers, group '{grp}' (no {sec} peer ledger yet)"
            return 0.5, 0, "no base rate (0.5)"
        peers = [x for x in pooled if x[1] == sec]
        r, n = rate([x for x in peers if x[2] == grp])
        if n >= 8: return r, n, f"sector peers ({sec}), group '{grp}'"
        r2, n2 = rate(peers)
        if n2 >= 8: return r2, n2, f"sector peers ({sec}), all groups (group '{grp}' n={n} < 8)"
        r3, n3 = rate([x for x in pooled if x[2] == grp])
        if n3 >= 8: return r3, n3, f"pooled all-India ledgers, group '{grp}' (sector pool n={n2} < 8)"
        return 0.5, 0, "no base rate (0.5)"

    cred = {}
    for sym in SECTOR:
        mine = [(GROUP.get(p['category'], 'other'), p['y']) for p in past if p['sym'] == sym]
        res = [y - p0(sym, g)[0] for g, y in mine]
        N = len(mine); sac = sum(res) / N if N else 0.0
        by = {}
        for g, y in mine: by.setdefault(g, []).append(y)
        cred[sym] = {'N': N, 'hits': sum(y for _, y in mine), 'hit_rate': round(sum(y for _, y in mine) / N, 3) if N else None,
                     'sac': round(sac, 3), 'w': round(N / (N + K), 3), 'active': N >= 3,
                     'by_group': {g: f"{sum(v)}/{len(v)}" for g, v in sorted(by.items())},
                     'p0_by_group': {g: round(p0(sym, g)[0], 3) for g in ('revenue', 'margin', 'dates', 'balance_sheet', 'other')}}
    order = sorted(SECTOR, key=lambda s: (cred[s]['sac'], s), reverse=True)
    for i, s in enumerate(order): cred[s]['tercile'] = 'top' if i < 2 else ('middle' if i < 4 else 'bottom')

    recs, specs, calls = [], [], []
    for sym, slug, grp, said, quote, claim, rule, spec, rby in FWD:
        base, nb, basis = p0(sym, grp)
        c = cred[sym]
        pc = base + c['w'] * c['sac'] if c['active'] else base
        pc = min(0.95, max(0.05, pc)); base_r = round(base, 2); pc_r = round(pc, 2)
        praw = round(min(0.95, max(0.05, base + c['sac'])), 2) if c['N'] else base_r
        cid = f"thesis:paper-call:{sym}:{slug}-pft2"
        adj = f"p0 = {base:.3f} ({basis}, n={nb}); SAC {c['sac']:+.3f} x w {c['w']:.3f} (N={c['N']}) -> P_cred = {pc_r}"
        src = ("Q4FY27 results, press release / investor presentation and Q4FY27 earnings call transcript (NSE)"
               if spec.get('kind') == 'india_fin' else "company Q3/Q4 FY27 filings, presentations and call transcripts (NSE / company website)")
        body = (f"Promise-credibility forward test, cohort 2 (Nov-2026) (NOT a recommendation; not buy/sell). {NAME[sym]} ({sym}). "
                f"Probability {pc_r} (naive base rate {base_r}) that: {claim}. Probabilities set only by the pre-registered rule "
                f"(research_notes/Promise tracker pilot/forward_test_2026-11-c2/prereg.md s4): {adj}. Evidence: call of {said}: {quote}. "
                f"Resolution: {rule} Source: {src}. Resolve by {rby}; score Brier of P_cred vs P_base (prereg s5; pooled with cohort 1).")
        data = {"probability": pc_r, "base_rate_probability": base_r, "probability_raw_unshrunk": praw,
                "method": "promise-tracker credibility (sector-adjusted, rule-generated; forward test 2026-11 cohort 2)",
                "made_on": MADE, "resolve_by": rby, "resolution_rule": rule, "resolution_source": src,
                "base_rate_reasoning": f"Naive forecaster = leave-one-out strict delivery rate ({basis}, n={nb}). No company-specific information.",
                "adjustment_rule": "P_cred = clip(p0 + N/(N+20) x SAC, 0.05, 0.95); SAC = mean(y - p0(group)) over the company's resolved past promises (strict: delivered=1, else 0). P_base = p0.",
                "adjustment_applied": adj, "sector_adjusted_score": c['sac'], "sac_shrink_weight": c['w'], "sac_n_scored": c['N'],
                "credibility_tercile": c['tercile'], "promise_group": grp, "promise_said_on": said, "promise_quote": quote,
                "sector": SECTOR[sym], "company_name": NAME[sym], "cohort": "promise-forward-test-2026-11-c2",
                "pooled_with": "promise-forward-test-2026-11",
                "prereg": "research_notes/Promise tracker pilot/forward_test_2026-11-c2/prereg.md", "outcome": None, "brier": None}
        tags = ["paper-call", "method-test", "promise-forward-test", "credibility-generated", "cohort-2", "promise-tracker", "india",
                "sector-" + SECTOR[sym].lower().replace(' ', '-'), "cat-" + grp]
        recs.append({"type": "thesis", "id": cid, "title": f"Paper call: {claim}", "body": body, "tickers": [sym], "tags": tags,
                     "date": MADE, "status": "open", "confidence": "single-source", "data": data,
                     "sources": [f"https://www.screener.in/company/{sym}/consolidated/"]})
        specs.append(f' "{cid}": ' + json.dumps(spec, ensure_ascii=False))
        due = spec.get('event_deadline') or spec.get('end') or rby
        calls.append({'id': cid, 'sym': sym, 'group': grp, 'claim': claim, 'p_cred': pc_r, 'p_base': base_r, 'p_raw': praw,
                      'due': due, 'resolve_by': rby, 'auto': spec['auto'], 'kind': spec['kind'], 'basis': basis, 'n_base': nb})

    seed = os.path.join(ROOT, 'memdb', 'seeds', '2026-11-26_promise_forward_test_c2.json')
    json.dump(recs, open(seed, 'w'), indent=1, ensure_ascii=False)
    open(os.path.join(HERE, 'specs_lines.txt'), 'w').write(",\n".join(specs) + "\n")
    json.dump({'past': past, 'credibility': cred, 'calls': calls,
               'pool_rows': {'cohort2': len(c2rows), 'cohort1': len(c1rows), 'pilots': len(pil)}},
              open(os.path.join(HERE, 'ledger.json'), 'w'), indent=1, ensure_ascii=False)
    for s in SECTOR:
        c = cred[s]
        print(f"{s:10s} {SECTOR[s][:22]:22s} N={c['N']:3d} hits={c['hits']:3d} hr={c['hit_rate']} SAC={c['sac']:+.3f} w={c['w']:.3f} {c['tercile']} {c['by_group']} p0={c['p0_by_group']}")
    for c in calls: print(f"{c['due']} {c['sym']:10s} {c['group']:13s} Pc={c['p_cred']:.2f} Pb={c['p_base']:.2f} {c['auto']}")
    print(len(recs), 'calls ->', seed, '| pool rows', len(c2rows), len(c1rows), len(pil))


if __name__ == '__main__':
    main()
