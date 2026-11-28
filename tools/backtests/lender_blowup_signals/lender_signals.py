"""Lender blow-up signals vs the lender base rate. Pre-registration: research_notes/Backtests/lender_blowup_signals.md §A.
Run from repo root:  python3 tools/backtests/lender_blowup_signals/lender_signals.py --phase cache|run
cache: copies the screener public pages (cached by the base-rate build) into outputs/data/ as gzip + extracted annual
tables with as_of. run: computes flags, LOCO M1 vs B, writes outputs/{flags.csv,results.json}. Research, not SEBI advice."""
import csv, gzip, json, os, re, sys, random, math, datetime
sys.path.insert(0, 'tools/backtests/blowup_model')
import blowup_model as BM   # fit_logit, predict, auc (L54 code, unchanged)

BT = 'research_notes/Backtests/'
PANEL = BT + 'base_rates_lenders_india_outputs/panel.csv'
OUT = BT + 'lender_blowup_signals_outputs/'
DATA = OUT + 'data/'
SRC = os.environ.get('SC_CACHE', '/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_solv_in/sc')
FEATS = ['GROW', 'WEAKPROF', 'THINCAP', 'WHOLESALE']
SEC = ['HIGHYIELD', 'COSTUP', 'CAPFALL', 'COUNT2']

def clean(s): return re.sub(r'<.*?>|&nbsp;|\+', ' ', s, flags=re.S).strip()
def num(s):
    s = clean(s).replace(',', '').replace('%', '').strip()
    try: return float(s)
    except ValueError: return None

def tables(html):
    out = {}
    for sec in ('profit-loss', 'balance-sheet'):
        m = re.search(r'<section id="%s".*?</section>' % sec, html, re.S)
        if not m: continue
        s = m.group(0)
        t = re.search(r'<table.*?</table>', s, re.S).group(0)
        hdr = [clean(h) for h in re.findall(r'<th[^>]*>(.*?)</th>', t, re.S)]
        rows = {}
        for tr in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S):
            tds = re.findall(r'<td[^>]*>(.*?)</td>', tr, re.S)
            if not tds: continue
            rows[re.sub(r'\s+', ' ', clean(tds[0]))] = {hdr[i]: num(v) for i, v in enumerate(tds[1:], 1) if i < len(hdr)}
        out[sec] = rows
    return out

def cache():
    slugs = sorted({r['slug'] for r in csv.DictReader(open(PANEL))})
    os.makedirs(DATA, exist_ok=True)
    idx = {}
    for s in slugs:
        p = os.path.join(SRC, s, 'page.html')
        html = open(p, encoding='utf-8', errors='replace').read()
        as_of = datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
        with gzip.open(DATA + s + '.page.html.gz', 'wt', encoding='utf-8') as g: g.write(html)
        idx[s] = dict(as_of=as_of, url='https://www.screener.in/company/%s/' % s, tables=tables(html))
    json.dump(idx, open(DATA + 'annual_tables.json', 'w'), indent=0, sort_keys=True)
    print('cached', len(idx))

ALIAS = {'Revenue': ('Revenue', 'Sales'), 'Borrowing': ('Borrowing', 'Borrowings')}
def g(t, sec, row, col):
    # extraction fix (see §B0): older screener pages (mostly merged/dead firms) use 'Sales' and 'Borrowings'
    for r in ALIAS.get(row, (row,)):
        v = (t.get(sec, {}).get(r) or {}).get(col)
        if v is not None: return v
    return None

def flags_for(t, fy, kind):
    c0, c1 = 'Mar %d' % fy, 'Mar %d' % (fy - 1)
    v = {}
    for c, k in ((c0, 0), (c1, 1)):
        ta = g(t, 'balance-sheet', 'Total Assets', c)
        inv = g(t, 'balance-sheet', 'Investments', c) or 0
        fa = g(t, 'balance-sheet', 'Fixed Assets', c) or 0
        cw = g(t, 'balance-sheet', 'CWIP', c) or 0
        nw = None
        if g(t, 'balance-sheet', 'Equity Capital', c) is not None and g(t, 'balance-sheet', 'Reserves', c) is not None:
            nw = g(t, 'balance-sheet', 'Equity Capital', c) + g(t, 'balance-sheet', 'Reserves', c)
        v[k] = dict(ta=ta, L=(ta - inv - fa - cw) if ta else None, nw=nw,
                    dep=g(t, 'balance-sheet', 'Deposits', c) or 0, bor=g(t, 'balance-sheet', 'Borrowing', c) or 0,
                    np=g(t, 'profit-loss', 'Net Profit', c), rev=g(t, 'profit-loss', 'Revenue', c),
                    exp=g(t, 'profit-loss', 'Expenses', c))
    a, p = v[0], v[1]
    old_bank = kind == 'bank' and 'Deposits' not in t.get('balance-sheet', {})  # deposits folded into 'Borrowings'
    def ok(*x): return all(y is not None for y in x)
    avg = (a['ta'] + p['ta']) / 2 if ok(a['ta'], p['ta']) else a['ta']
    m = {}
    m['loan_growth'] = a['L'] / p['L'] - 1 if ok(a['L'], p['L']) and p['L'] > 0 else None
    m['roa'] = a['np'] / avg if ok(a['np'], avg) and avg else None
    m['nw_ta'] = a['nw'] / a['ta'] if ok(a['nw'], a['ta']) and a['ta'] else None
    m['wholesale'] = (a['bor'] / (a['dep'] + a['bor']) if ok(a['ta']) and (a['dep'] + a['bor']) > 0 and not old_bank
                      else None)
    m['yield'] = a['rev'] / avg if ok(a['rev'], avg) and avg else None
    pavg = p['ta']
    m['cost_chg'] = (a['exp'] / avg - p['exp'] / pavg) if ok(a['exp'], p['exp'], avg, pavg) and avg and pavg else None
    m['nw_ta_chg'] = (m['nw_ta'] - p['nw'] / p['ta']) if m['nw_ta'] is not None and ok(p['nw'], p['ta']) and p['ta'] else None
    th = 0.065 if kind == 'bank' else 0.125
    F = dict(GROW=m['loan_growth'] is not None and m['loan_growth'] > 0.30,
             WEAKPROF=m['roa'] is not None and m['roa'] < 0.004,
             THINCAP=m['nw_ta'] is not None and m['nw_ta'] < th,
             WHOLESALE=m['wholesale'] is not None and m['wholesale'] > 0.50,
             HIGHYIELD=m['yield'] is not None and m['yield'] >= 0.13,
             COSTUP=m['cost_chg'] is not None and m['cost_chg'] >= 0.005,
             CAPFALL=m['nw_ta_chg'] is not None and m['nw_ta_chg'] <= -0.005)
    F = {k: int(x) for k, x in F.items()}
    F['COUNT2'] = int(sum(F[k] for k in FEATS) >= 2)
    known = dict(GROW=m['loan_growth'] is not None, WEAKPROF=m['roa'] is not None, THINCAP=m['nw_ta'] is not None,
                 WHOLESALE=m['wholesale'] is not None or (not old_bank and ok(a['ta'])), HIGHYIELD=m['yield'] is not None,
                 COSTUP=m['cost_chg'] is not None, CAPFALL=m['nw_ta_chg'] is not None)
    return F, m, known

def brier(p, y): return sum((a - b) ** 2 for a, b in zip(p, y)) / len(y)
def logs(p, y): return sum(math.log(a if b else 1 - a) for a, b in zip(p, y)) / len(y)
def auc(p, y): return BM.auc(p, y, [1.0] * len(y))

def fit(rows, feats):
    X = [[1.0] + [r['x'][k] for k in feats] for r in rows]
    return BM.fit_logit(X, [r['y'] for r in rows], [1.0] * len(rows))

def pred(beta, rows, feats): return BM.predict(beta, [[1.0] + [r['x'][k] for k in feats] for r in rows])

def m2(train, test):
    hi = [r['y'] for r in train if r['x']['COUNT2']]; lo = [r['y'] for r in train if not r['x']['COUNT2']]
    ph = sum(hi) / len(hi) if hi else sum(r['y'] for r in train) / len(train)
    pl = sum(lo) / len(lo) if lo else ph
    return [min(max(ph if r['x']['COUNT2'] else pl, 0.02), 0.60) for r in test]

def loco(rows):
    res, pooled = {}, dict(y=[], M1=[], B=[], M2=[], comp=[])
    for c in ('FY2016', 'FY2018'):
        tr = [r for r in rows if r['c'] != c]; te = [r for r in rows if r['c'] == c]
        beta = fit(tr, FEATS)
        P = dict(M1=pred(beta, te, FEATS), B=[sum(r['y'] for r in tr) / len(tr)] * len(te), M2=m2(tr, te))
        y = [r['y'] for r in te]
        res[c] = dict(n=len(te), events=sum(y), realised=round(sum(y) / len(y), 4),
                      coef=dict(zip(['const'] + FEATS, [round(b, 3) for b in beta])),
                      **{k: dict(brier=round(brier(p, y), 4), log=round(logs(p, y), 4),
                                 mean_pred=round(sum(p) / len(p), 4), citl=round(sum(p) / len(p) - sum(y) / len(y), 4),
                                 auc=(round(auc(p, y), 3) if k != 'B' else None)) for k, p in P.items()})
        pooled['y'] += y; pooled['comp'] += [r['comp'] for r in te]
        for k in P: pooled[k] += P[k]
    return res, pooled

def boot(rows, draws=2000, seed=20261128):
    rnd = random.Random(seed)
    comps = sorted({r['comp'] for r in rows}); by = {}
    for r in rows: by.setdefault(r['comp'], []).append(r)
    d = []
    for _ in range(draws):
        s = [r for c in (rnd.choice(comps) for _ in comps) for r in by[c]]
        if len({r['c'] for r in s}) < 2: continue
        _, P = loco(s)
        d.append(brier(P['M1'], P['y']) - brier(P['B'], P['y']))
    d.sort(); return [round(d[int(0.025 * len(d))], 4), round(d[int(0.975 * len(d))], 4), len(d)]

def run():
    T = json.load(open(DATA + 'annual_tables.json'))
    rows, out_rows = [], []
    for r in csv.DictReader(open(PANEL)):
        fy = int(r['snap'][2:]); F, m, known = flags_for(T[r['slug']]['tables'], fy, r['kind'])
        r5 = BM.f(r['r5'])
        rows.append(dict(c=r['snap'], y=int(r['o_fail'] == '1'), x=F, known=known, comp=r['key'], name=r['name'],
                         kind=r['kind'], perm=int(r['o_fail'] == '1' and (r5 is None or r5 <= 0.5))))
        out_rows.append(dict(key=r['key'], name=r['name'], kind=r['kind'], snap=r['snap'], o_fail=r['o_fail'],
                             as_of=T[r['slug']]['as_of'], **{k: (round(v, 4) if v is not None else '') for k, v in m.items()}, **F))
    with open(OUT + 'flags.csv', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0])); w.writeheader(); w.writerows(out_rows)
    R = dict(prereg='research_notes/Backtests/lender_blowup_signals.md §A', n=len(rows), events=sum(r['y'] for r in rows))
    R['coverage'] = {k: round(sum(r['known'][k] for r in rows) / len(rows), 3) for k in FEATS + SEC[:-1]}
    R['univariate'] = {}
    for k in FEATS + SEC:
        on = [r for r in rows if r['x'][k]]; off = [r for r in rows if not r['x'][k]]
        R['univariate'][k] = dict(n_on=len(on), rate_on=round(sum(r['y'] for r in on) / len(on), 3) if on else None,
                                  rate_off=round(sum(r['y'] for r in off) / len(off), 3) if off else None,
                                  perm_on=round(sum(r['perm'] for r in on) / len(on), 3) if on else None,
                                  by_cohort={c: [sum(1 for r in on if r['c'] == c), sum(r['y'] for r in on if r['c'] == c)]
                                             for c in ('FY2016', 'FY2018')})
    res, P = loco(rows)
    R['loco'] = res
    y = P['y']
    R['pooled'] = {k: dict(brier=round(brier(P[k], y), 4), log=round(logs(P[k], y), 4),
                           citl=round(sum(P[k]) / len(y) - sum(y) / len(y), 4)) for k in ('M1', 'B', 'M2')}
    R['pooled']['M1']['auc_pooled'] = round(auc(P['M1'], y), 3)
    aucs = [res[c]['M1']['auc'] for c in res]
    R['mean_within_cohort_auc_M1'] = round(sum(aucs) / 2, 3)
    order = sorted(range(len(y)), key=lambda i: P['M1'][i]); k3 = len(y) // 3
    R['reliability_tertiles_M1'] = [[round(sum(P['M1'][i] for i in g) / len(g), 3), round(sum(y[i] for i in g) / len(g), 3), len(g)]
                                    for g in (order[:k3], order[k3:2 * k3], order[2 * k3:])]
    R['boot_brier_diff_M1_minus_B_ci95'] = boot(rows)
    beta = fit(rows, FEATS); R['full_fit'] = dict(zip(['const'] + FEATS, [round(b, 3) for b in beta]))
    # secondary: permanent blow-up outcome, same LOCO
    rp = [dict(r, y=r['perm']) for r in rows]; resp, Pp = loco(rp)
    R['secondary_permanent'] = dict(M1=round(brier(Pp['M1'], Pp['y']), 4), B=round(brier(Pp['B'], Pp['y']), 4),
                                    within_auc={c: resp[c]['M1']['auc'] for c in resp},
                                    cohort_brier={c: [resp[c]['M1']['brier'], resp[c]['B']['brier']] for c in resp})
    a = all(res[c]['M1']['brier'] < res[c]['B']['brier'] for c in res); b_ = R['mean_within_cohort_auc_M1'] >= 0.65
    R['verdict'] = dict(brier_beats_B_both_cohorts=a, mean_within_auc_ge_065=b_, adopted=a and b_)
    json.dump(R, open(OUT + 'results.json', 'w'), indent=1)
    print(json.dumps(R, indent=1))

if __name__ == '__main__':
    ph = sys.argv[sys.argv.index('--phase') + 1] if '--phase' in sys.argv else 'run'
    cache() if ph == 'cache' else run()
