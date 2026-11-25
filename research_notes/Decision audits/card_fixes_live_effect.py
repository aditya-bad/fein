"""Effect of candidate fixes on the 8 live cards, in memory only (no card re-issued, nothing written).
Run from the repo root: python3 "research_notes/Decision audits/card_fixes_live_effect.py"
V0 = card v1.5 as is; V1 = sigma -> class robust log-SD; V2 = two-sided anchoring; V3 = both.
Also shows fix (1) (EV = mean of the anchored outcome distribution, i.e. mult5 read as a median) for each variant."""
import sys, math, copy, io, contextlib
sys.path.insert(0, 'tools/decision'); sys.path.insert(0, 'tools/valuation')
import decision_card as dc
ws = dc.ws
SIG_CLASS = {'india_nonfin': 0.682, 'india_lender': 0.981, 'us': 0.700}   # pooled, card_fixes_historical_test.py
WIN_FALLBACK = 4.0
_orig_load, _orig_anchor = ws.load_input, dc.anchor_outcomes
STATE = {}

def load_override(path):
    d = _orig_load(path)
    if STATE.get('sigma'): d['dispersion'] = STATE['sigma']
    return d

def anchor_two_sided(outs, pa, pl):
    res, pl_eff = _orig_anchor(outs, pa, pl)
    pr = STATE.get('pr')
    if pr is None: return res, pl_eff
    D = sum(p for p, m in res if m >= 3.0); C = sum(p for p, m in res if 0.5 < m < 3.0)
    tot = C + D
    tgt = min(pr, tot)
    out = []
    for p, m in res:
        if m >= 3.0: out.append((p * tgt / D, m) if D > 0 else None)
        elif m > 0.5: out.append((p * (tot - tgt) / C, m))
        else: out.append((p, m))
    out = [x for x in out if x]
    if D <= 0 and tgt > 0: out.append((tgt, WIN_FALLBACK))
    return out, pl_eff

def run(t, sigma=None, two=False):
    p = 'tools/decision/live/%s_card.json' % t
    card = dc._load_json(p)
    STATE.clear(); STATE['sigma'] = sigma
    ws.load_input = load_override
    try:
        # pre-pass for the model P(>=3x) and class
        with contextlib.redirect_stderr(io.StringIO()):
            F, rec, wres = dc.build(card, p)
        rates = dc._load_json('tools/decision/base_rates.json')
        cn, _ = dc.resolve_base_rate_class(card, wres['input'], wres, rates)
        cls = rates['classes'].get(cn) or rates['classes'].get(str(cn) + '_deprecated') or {}
        aw, _ = dc.anchor_weight(card.get('tail_anchor'))
        p3m = wres['scenarios'].get('p_ge_3x'); b3 = cls.get('p_ge_3x')
        if two and b3 is not None and (cls.get('p_blowup') is not None or cls.get('p_le_half') is not None):
            STATE['pr'] = dc.anchor_p(p3m, b3, aw)
            dc.anchor_outcomes = anchor_two_sided
            with contextlib.redirect_stderr(io.StringIO()):
                F, rec, wres = dc.build(card, p)
    finally:
        ws.load_input = _orig_load; dc.anchor_outcomes = _orig_anchor
    dec = rec[-1]['data']; sc = wres['scenarios']
    # reconstruct anchored outcomes for the fix-(1) mean and P(>=3x)
    touts = dc._outcomes_tagged(sc, wres['input']['dispersion'])
    outs_raw = [(q, m) for q, m, _ in touts]
    if dec['anchor_weight'] is not None:
        pa = dec['p_blowup_anchored'] if cls.get('p_blowup') is not None else (sc.get('p_blowup') or 0.0)
        pl = dec['p_le_half_anchored'] if cls.get('p_le_half') is not None else (sc.get('p_le_half') or 0.0)
        outs, _ = (anchor_two_sided if STATE.get('pr') is not None else _orig_anchor)(touts, pa, pl)
    else:
        outs = outs_raw
    ev_med = sum(q * m for q, m in outs)
    p3 = sum(q for q, m in outs if m >= 3.0)
    hurdle = sc['hurdle_mult5']
    blocked_other = [g['gate'] for g in dec['gates'] if g['blocks'] and g['gate'] != 'Expected value vs hurdle']
    f1, _ = dc._kelly(outs, hurdle)
    kf = (card.get('sizing') or {}).get('kelly_fraction', 0.25)
    cap = (card.get('sizing') or {}).get('max_pct_at_cost') or dc.TIER_CAPS.get((card.get('sizing') or {}).get('tier', 'satellite'))
    size_fix1 = 0.0 if (ev_med < hurdle or blocked_other) else min(kf * f1, cap)
    if (dec.get('survival_cap') or {}).get('mode') == 'cap':
        size_fix1 = min(size_fix1, dc.SURVIVAL_MIN_SIZE)
    return dict(cls=cn, sigma=wres['input']['dispersion'], ev=dec['ev_mult5_anchored'], hurdle=hurdle, f=dec['kelly_f_star'],
                rule=dec['rule_size'], size=dec['size_after_gates'], ev_fix1=ev_med, size_fix1=size_fix1, p3_dist=p3,
                p3_model=sc.get('p_ge_3x'), other_blocks=blocked_other)

def cls_sigma(cn, market):
    if cn and 'lender' in cn: return SIG_CLASS['india_lender']
    return SIG_CLASS['india_nonfin'] if market == 'india' else SIG_CLASS['us']

if __name__ == '__main__':
    for t in ['AUTOAXLES', 'HARSHA', 'INDRAMEDCO', 'SHK', 'SUNFLAG', 'UTKARSHBNK', 'UTTAMSUGAR', 'US-KEX']:
        r0 = run(t)
        mkt = 'us' if t.startswith('US-') else 'india'
        s = cls_sigma(r0['cls'], mkt)
        rows = {'V0': r0, 'V1': run(t, s), 'V2': run(t, None, True), 'V3': run(t, s, True)}
        print('==', t, r0['cls'], 'hurdle %.3f' % r0['hurdle'], 'other blocking gates:', r0['other_blocks'])
        for v, r in rows.items():
            print('  %s sig=%.2f P3(model)=%.3f P3(anch dist)=%.3f | EV(card conv)=%.3f f*=%.3f rule=%.3f size=%.3f | EV(fix1)=%.3f size(fix1)=%.3f'
                  % (v, r['sigma'], r['p3_model'] or 0, r['p3_dist'], r['ev'], r['f'] or 0, r['rule'], r['size'], r['ev_fix1'], r['size_fix1']))
