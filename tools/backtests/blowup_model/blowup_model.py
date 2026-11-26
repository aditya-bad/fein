"""Blow-up probability model: out-of-sample test. Pre-registration: research_notes/Decision audits/blowup_model_test.md §A.
Run from repo root: python3 tools/backtests/blowup_model/blowup_model.py. Read-only on inputs; writes
research_notes/Backtests/blowup_model_outputs/results.json."""
import csv, math, json, collections
BT = 'research_notes/Backtests/'
OUT = BT + 'blowup_model_outputs/results.json'
def f(x):
    try: return float(x)
    except Exception: return None
def b(x): return 1 if str(x).strip() in ('1', '1.0') else 0

def keep(Rraw, fail):
    R = f(Rraw)
    if R is None:
        if not fail: return None
        R = 0.0
    return R

def load():
    P = {}
    rows = []
    for r in csv.DictReader(open(BT + 'hard_filters_india_v2_outputs/panel_v2.csv')):
        m = f(r['mcap'])
        if m is None or not (1000 <= m <= 20000): continue
        fail = r['o_fail'] == '1'
        if keep(r['r5'], fail) is None: continue
        B25, S2 = b(r['B25']), b(r['s2'])
        rows.append(dict(w=float(r['weight']), c=r['snap'], y=int(fail), size=m, name=r['name'],
                         x=dict(B25=B25, S2=S2, BOTH=B25 * S2, S15=max(b(r['s1']), b(r['s5'])),
                                S1=b(r['s1']), S5=b(r['s5']))))
    P['india_nonfin'] = (rows, ['B25', 'S2', 'BOTH', 'S15'])
    rows = []
    for r in csv.DictReader(open(BT + 'base_rates_lenders_india_outputs/panel.csv')):
        fail = r['o_fail'] == '1'
        if keep(r['r5'], fail) is None: continue
        rows.append(dict(w=1.0, c=r['snap'], y=int(fail), size=f(r['mcap']), name=r['name'], x={}))
    P['india_lender'] = (rows, ['SMALL'])
    rows = []
    for r in csv.DictReader(open(BT + 'solvency_us_outputs/panel.csv')):
        fl = f(r['float'])
        if fl is None or not (5e8 <= fl <= 1e10): continue
        fail = r['O_fail'] == '1'
        if keep(r['R5'], fail) is None: continue
        rows.append(dict(w=1.0, c=r['T'][:4], y=int(fail), size=fl, name=r['name'],
                         x=dict(S1=b(r['S1']), S2=b(r['S2']), S5=b(r['S5']))))
    P['us_float'] = (rows, ['S1', 'S2', 'S5', 'SMALL'])
    return P

def load_events():
    rows = []
    ev = list(csv.DictReader(open(BT + 'survival_cap_general_outputs/events_out.tsv'), delimiter='\t'))
    byq = collections.defaultdict(list)
    for r in ev:
        if f(r['sue']) is not None: byq[r['qe']].append(f(r['sue']))
    cut = {q: sorted(v)[int(len(v) * 0.2)] if len(v) >= 5 else None for q, v in byq.items()}
    for r in ev:
        m = f(r['mcap_cr'])
        if r['fin'] == '1' or m is None or not (1000 <= m <= 20000) or r['fail3'] == '': continue
        s = f(r['sue']); c = cut.get(r['qe'])
        rows.append(dict(w=1.0, c=r['entry'][:4], y=int(r['fail3'] == '1'), size=m, name=r['sym'],
                         x=dict(PEADQ1=int(s is not None and c is not None and s < c), B25=b(r['B25']), S2=b(r['S2']))))
    return rows, ['PEADQ1', 'B25', 'S2', 'SMALL']

def wq(rows, q, key):
    s = sorted(rows, key=key); W = sum(r['w'] for r in s); acc = 0
    for r in s:
        acc += r['w']
        if acc >= q * W: return key(r)

def design(rows, feats, small_cut):
    X = []
    for r in rows:
        v = [1.0]
        for k in feats:
            v.append(float(r['size'] < small_cut) if k == 'SMALL' else float(r['x'][k]))
        X.append(v)
    return X

def solve(A, g):
    n = len(g); M = [A[i][:] + [g[i]] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda k: abs(M[k][i])); M[i], M[p] = M[p], M[i]
        for k in range(n):
            if k != i:
                fct = M[k][i] / M[i][i]
                for j in range(i, n + 1): M[k][j] -= fct * M[i][j]
    return [M[i][n] / M[i][i] for i in range(n)]

def sig(z): return 1 / (1 + math.exp(-max(min(z, 30), -30)))

def fit_logit(X, y, w, prior_var=1.0, offset=None):
    n, k = len(X), len(X[0]); wm = sum(w) / n; w = [wi / wm for wi in w]
    beta = [0.0] * k
    pb = sum(wi * yi for wi, yi in zip(w, y)) / sum(w); beta[0] = math.log(pb / (1 - pb))
    for _ in range(50):
        g = [0.0] * k; H = [[0.0] * k for _ in range(k)]
        for xi, yi, wi in zip(X, y, w):
            p = sig(sum(a * c for a, c in zip(beta, xi)))
            for a in range(k):
                g[a] += wi * (yi - p) * xi[a]
                for c in range(k): H[a][c] += wi * p * (1 - p) * xi[a] * xi[c]
        for a in range(1, k):
            g[a] -= beta[a] / prior_var; H[a][a] += 1 / prior_var
        step = solve(H, g); beta = [a + s for a, s in zip(beta, step)]
        if max(abs(s) for s in step) < 1e-9: break
    return beta

def predict(beta, X): return [min(max(sig(sum(a * c for a, c in zip(beta, xi))), 0.02), 0.60) for xi in X]

def auc(p, y, w):
    pos = [(pi, wi) for pi, yi, wi in zip(p, y, w) if yi]; neg = [(pi, wi) for pi, yi, wi in zip(p, y, w) if not yi]
    num = sum(wp * wn * (1.0 if a > c else 0.5 if a == c else 0.0) for a, wp in pos for c, wn in neg)
    return num / (sum(x for _, x in pos) * sum(x for _, x in neg))

def metrics(p, y, w, nb):
    W = sum(w)
    br = sum(wi * (pi - yi) ** 2 for pi, yi, wi in zip(p, y, w)) / W
    ls = sum(wi * math.log(pi if yi else 1 - pi) for pi, yi, wi in zip(p, y, w)) / W
    mp = sum(wi * pi for pi, wi in zip(p, w)) / W; my = sum(wi * yi for yi, wi in zip(y, w)) / W
    order = sorted(range(len(p)), key=lambda i: p[i]); rel = []; acc = 0; cur = []
    tgt = W / nb
    for i in order:
        cur.append(i); acc += w[i]
        if acc >= tgt * (len(rel) + 1) - 1e-9 or i == order[-1]:
            ww = sum(w[j] for j in cur)
            rel.append(dict(n=len(cur), pred=round(sum(w[j] * p[j] for j in cur) / ww, 4),
                            real=round(sum(w[j] * y[j] for j in cur) / ww, 4))); cur = []
    a = auc(p, y, w) if len(set(p)) > 1 else 0.5
    return dict(brier=round(br, 5), logscore=round(ls, 5), mean_pred=round(mp, 4), realised=round(my, 4),
                citl=round(mp - my, 4), auc=round(a, 3), reliability=rel)

def run_panel(rows, feats, nb, folds_key='c'):
    cohorts = sorted(set(r[folds_key] for r in rows))
    preds = {k: [None] * len(rows) for k in ('M1', 'B', 'C0', 'C1a', 'C1b', 'C2')}
    fold_info = {}
    for c in cohorts:
        tr = [r for r in rows if r[folds_key] != c]; te_idx = [i for i, r in enumerate(rows) if r[folds_key] == c]
        cut = wq(tr, 1 / 3, key=lambda r: r['size'])
        X = design(tr, feats, cut); y = [r['y'] for r in tr]; w = [r['w'] for r in tr]
        beta = fit_logit(X, y, w)
        B = sum(wi * yi for wi, yi in zip(w, y)) / sum(w)
        te = [rows[i] for i in te_idx]
        pm = predict(beta, design(te, feats, cut))
        C0 = 0.5 * B + 0.5 * 0.05
        for i, p in zip(te_idx, pm):
            preds['M1'][i] = p; preds['B'][i] = B; preds['C0'][i] = C0
            preds['C1a'][i] = 0.5 * B + 0.5 * max(0.05, p); preds['C1b'][i] = max(C0, p); preds['C2'][i] = max(C0, B)
        # univariate flag prevalence / rates in training fold
        uni = {}
        for k in feats + (['S1', 'S5'] if 'S15' in feats else []) + (['SMALL'] if 'SMALL' not in feats else []):
            if k != 'SMALL' and k not in tr[0]['x']: continue
            fl = lambda r: (r['size'] < cut) if k == 'SMALL' else r['x'][k]
            w1 = sum(r['w'] for r in tr if fl(r)); w0 = sum(r['w'] for r in tr if not fl(r))
            r1 = sum(r['w'] * r['y'] for r in tr if fl(r)) / w1 if w1 else None
            r0 = sum(r['w'] * r['y'] for r in tr if not fl(r)) / w0 if w0 else None
            uni[k] = dict(n1=sum(1 for r in tr if fl(r)), rate1=r1 and round(r1, 3), rate0=r0 and round(r0, 3))
        fold_info[c] = dict(n_train=len(tr), n_test=len(te), base=round(B, 4), small_cut=cut,
                            beta=dict(zip(['const'] + feats, [round(v, 3) for v in beta])), univariate=uni)
    y = [r['y'] for r in rows]; w = [r['w'] for r in rows]
    res = {k: metrics(v, y, w, nb) for k, v in preds.items()}
    return dict(n=len(rows), events=sum(y), folds=fold_info, metrics=res), preds

def cross_market(P):
    """US-fitted S1/S2/S5 coefficients applied to India non-fin, intercept re-set to the India training-fold base."""
    us, _ = P['us_float']; ind, _ = P['india_nonfin']; feats = ['S1', 'S2', 'S5']
    beta = fit_logit(design(us, feats, 0), [r['y'] for r in us], [1.0] * len(us))
    p = [None] * len(ind)
    for c in sorted(set(r['c'] for r in ind)):
        tr = [r for r in ind if r['c'] != c]; Xtr = design(tr, feats, 0)
        B = sum(r['w'] * r['y'] for r in tr) / sum(r['w'] for r in tr)
        lo, hi = -10.0, 10.0
        for _ in range(100):
            a = (lo + hi) / 2
            mp = sum(r['w'] * sig(a + sum(bb * xx for bb, xx in zip(beta[1:], x[1:]))) for r, x in zip(tr, Xtr)) / sum(r['w'] for r in tr)
            lo, hi = (a, hi) if mp < B else (lo, a)
        bt = [a] + beta[1:]
        for i, r in enumerate(ind):
            if r['c'] == c: p[i] = predict(bt, design([r], feats, 0))[0]
    return dict(us_beta=dict(zip(['const'] + feats, [round(v, 3) for v in beta])),
                metrics=metrics(p, [r['y'] for r in ind], [r['w'] for r in ind], 5))

def main():
    P = load(); out = {}
    for name, (rows, feats) in P.items():
        nb = 10 if len(rows) >= 500 else 5
        out[name], _ = run_panel(rows, feats, nb)
    out['cross_market_us_to_india'] = cross_market(P)
    ev, ef = load_events()
    out['secondary_events_fail3'], _ = run_panel(ev, ef, 10)
    # adoption
    core = ['india_nonfin', 'india_lender', 'us_float']
    wins = [p for p in core if out[p]['metrics']['M1']['brier'] < out[p]['metrics']['B']['brier']]
    wins_cal = [p for p in wins if abs(out[p]['metrics']['M1']['citl']) <= 0.03]
    adopt = len(wins) >= 2 and len(wins_cal) == len(wins)
    mb = {k: sum(out[p]['metrics'][k]['brier'] for p in core) / 3 for k in ('C1a', 'C1b')}
    pick = 'C1a' if mb['C1a'] < mb['C1b'] else 'C1b'
    pick_beats = [p for p in core if out[p]['metrics'][pick]['brier'] < out[p]['metrics']['C0']['brier']]
    c2w = [p for p in core if out[p]['metrics']['C2']['brier'] < out[p]['metrics']['C0']['brier']]
    c2cal = [p for p in c2w if abs(out[p]['metrics']['C2']['citl']) <= 0.03]
    out['decision'] = dict(M1_brier_wins=wins, M1_wins_with_citl_ok=wins_cal, M1_adopted=adopt,
                           card_variant_mean_brier=mb, card_pick=pick, card_pick_beats_C0=pick_beats,
                           ruleB_C2_wins=c2w, ruleB_C2_wins_citl_ok=c2cal,
                           ruleB_C2_passes=(not adopt) and len(c2w) >= 2 and len(c2cal) == len(c2w))
    json.dump(out, open(OUT, 'w'), indent=1)
    for p in core + ['secondary_events_fail3']:
        o = out[p]; print('\n==', p, 'n', o['n'], 'events', o['events'])
        for c, fi in o['folds'].items(): print('  fold', c, 'base', fi['base'], 'beta', fi['beta'], 'uni', fi['univariate'])
        for k, m in o['metrics'].items():
            print('  %-4s brier %.4f ls %.4f pred %.3f real %.3f citl %+.3f auc %.3f' % (k, m['brier'], m['logscore'], m['mean_pred'], m['realised'], m['citl'], m['auc']))
        print('  rel M1', [(x['n'], x['pred'], x['real']) for x in o['metrics']['M1']['reliability']])
    cm = out['cross_market_us_to_india']; m = cm['metrics']
    print('\n== cross-market', cm['us_beta'], 'brier %.4f citl %+.3f auc %.3f' % (m['brier'], m['citl'], m['auc']))
    print('\nDECISION', json.dumps(out['decision'], indent=1))

if __name__ == '__main__':
    main()
