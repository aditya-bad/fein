"""Historical test of card fixes (3) two-sided anchoring and (4) sigma. Pre-registration: card_fixes_historical_test.md §A.
Run from the repo root: python3 "research_notes/Decision audits/card_fixes_historical_test.py". Read-only; prints results."""
import csv, math, json
BT = 'research_notes/Backtests/'
SQ2 = math.sqrt(2)
def Phi(x): return 0.5 * (1 + math.erf(x / SQ2))
def f(x):
    try: return float(x)
    except Exception: return None

def load():
    P = {}
    rows = []
    for r in csv.DictReader(open(BT + 'solvency_india_outputs/panel.csv')):
        m = f(r['mcap'])
        if m is None or not (1000 <= m <= 20000): continue
        R = f(r['r5']); fail = r['o_fail'] == '1'
        if R is None:
            if not fail: continue
            R = 0.0
        rows.append(dict(w=float(r['weight']), c=r['snap'], R=R, bl=fail))
    P['india_nonfin'] = (rows, 1.7623)
    rows = []
    for r in csv.DictReader(open(BT + 'base_rates_lenders_india_outputs/panel.csv')):
        R = f(r['r5']); fail = r['o_fail'] == '1'
        if R is None:
            if not fail: continue
            R = 0.0
        rows.append(dict(w=1.0, c=r['snap'], R=R, bl=fail))
    P['india_lender'] = (rows, 1.7623)
    rows = []
    for r in csv.DictReader(open(BT + 'solvency_us_outputs/panel.csv')):
        fl = f(r['float'])
        if fl is None or not (5e8 <= fl <= 1e10): continue
        R = f(r['R5']); fail = r['O_fail'] == '1'
        if R is None:
            if not fail: continue
            R = 0.0
        rows.append(dict(w=1.0, c=r['T'][:4], R=R, bl=fail))
    P['us_float'] = (rows, 1.4693)
    return P

def wq(rows, q, key=lambda r: r['R']):
    s = sorted(rows, key=key); W = sum(r['w'] for r in s); acc = 0
    for r in s:
        acc += r['w']
        if acc >= q * W: return key(r)
def wfrac(rows, c):
    W = sum(r['w'] for r in rows); return sum(r['w'] for r in rows if c(r)) / W

def fit(rows):
    pr = [r for r in rows if r['R'] > 0]
    lq = lambda q: wq(pr, q, key=lambda r: math.log(r['R']))
    return dict(M=wq(rows, 0.5), sig=(lq(0.75) - lq(0.25)) / 1.349,
                p3=wfrac(rows, lambda r: r['R'] >= 3), ph=wfrac(rows, lambda r: r['R'] <= 0.5),
                pb=wfrac(rows, lambda r: r['bl']))

SCEN = [(0.25, 0.65), (0.50, 1.0), (0.20, 1.45)]; BLP, BLM = 0.05, 0.10; W_ANC = 0.5

class Dist:
    """Card-shaped forecast: lognormal scenario mixture + blow-up point, anchored by region rescaling."""
    def __init__(s, M, sig, base, two_sided):
        s.sc = [(p, k * M) for p, k in SCEN]; s.sig = sig
        cont = lambda x: sum(p * Phi((math.log(x) - math.log(m)) / sig) for p, m in s.sc)  # mass 0.95
        s.cont = cont
        mh = cont(0.5); m3 = sum(p for p, _ in s.sc) - cont(3.0)
        model_ph = mh + BLP; model_p3 = m3
        pa = W_ANC * base['pb'] + (1 - W_ANC) * BLP
        pl = max(W_ANC * base['ph'] + (1 - W_ANC) * model_ph, pa)
        pr = (W_ANC * base['p3'] + (1 - W_ANC) * model_p3) if two_sided else None
        tot_c = sum(p for p, _ in s.sc)
        if two_sided:
            s.kB = (pl - pa) / mh; s.kD = pr / m3; s.kC = (1 - pl - pr) / (tot_c - mh - m3); s.kD_on = True
        else:
            s.kB = (pl - pa) / mh; s.kC = s.kD = (1 - pl) / (tot_c - mh); s.kD_on = False
        s.pa = pa; s.mh = mh; s.m3 = m3
        s.p_le_half = pl; s.p_ge3 = s.kD * m3; s.p_blow = pa
    def cdf(s, x):
        if x <= 0: return 0.0
        v = s.pa if x >= BLM else 0.0
        c = s.cont(x)
        if x <= 0.5: return v + s.kB * c
        v += s.kB * s.mh
        if x < 3.0: return v + s.kC * (c - s.mh)
        return v + s.kC * (s.cont(3.0) - s.mh) + s.kD * (c - s.cont(3.0))
    def quant(s, q):
        lo, hi = 1e-4, 1e3
        for _ in range(80):
            mid = math.sqrt(lo * hi)
            if s.cdf(mid) < q: lo = mid
            else: hi = mid
        return hi
    def mean(s, n=4000):
        # numeric: E[R] = sum over regions of k * partial lognormal means
        def pm(m, a, b):  # E[X 1{a<X<=b}] for lognormal median m, sigma sig
            mu, sg = math.log(m), s.sig
            F = lambda x: 0.0 if x <= 0 else (1.0 if x == math.inf else Phi((math.log(x) - mu - sg * sg) / sg))
            return m * math.exp(sg * sg / 2) * (F(b) - F(a))
        e = s.pa * BLM
        for p, m in s.sc:
            e += p * (s.kB * pm(m, 0, 0.5) + s.kC * pm(m, 0.5, 3.0) + s.kD * pm(m, 3.0, math.inf))
        return e

def evaluate(rows, H, fc_for):
    bins = [0.5, 1.0, H, 3.0]
    tot = dict(ls=0, b3=0, bh=0, bb=0, c50=0, c80=0, W=0, p3=0, ph=0, pb=0, o3=0, oh=0, ob=0, pmean=0, omean=0)
    for r in rows:
        d = fc_for(r); w = r['w']; R = r['R']
        cuts = [0.0] + [d.cdf(b) for b in bins] + [1.0]
        # bins: (0,.5], (.5,1], (1,H], (H,3), [3,inf)  -> cdf at 3 is P(R<3) since region D starts at 3 (continuous)
        k = 0 if R <= 0.5 else 1 if R <= 1 else 2 if R <= H else 3 if R < 3 else 4
        pbin = max(cuts[k + 1] - cuts[k], 1e-6)
        y3, yh, yb = R >= 3, R <= 0.5, r['bl']
        tot['ls'] += w * math.log(pbin)
        tot['b3'] += w * (d.p_ge3 - y3) ** 2; tot['bh'] += w * (d.p_le_half - yh) ** 2; tot['bb'] += w * (d.p_blow - yb) ** 2
        for q, key in ((0.5, 'c50'), (0.8, 'c80')):
            lo, hi = d.quant((1 - q) / 2), d.quant(1 - (1 - q) / 2)
            tot[key] += w * (lo <= R <= hi)
        tot['p3'] += w * d.p_ge3; tot['ph'] += w * d.p_le_half; tot['pb'] += w * d.p_blow
        tot['o3'] += w * y3; tot['oh'] += w * yh; tot['ob'] += w * yb
        tot['pmean'] += w * d.mean(); tot['omean'] += w * R
        tot['W'] += w
    W = tot.pop('W'); out = {k: v / W for k, v in tot.items()}
    out['brier_sum'] = out['b3'] + out['bh'] + out['bb']
    return out

VARS = {'V0': (False, False), 'V1': (True, False), 'V2': (False, True), 'V3': (True, True)}

def run(mode):
    P = load(); res = {}
    for name, (rows, H) in P.items():
        cohorts = sorted(set(r['c'] for r in rows))
        fits = {c: fit([r for r in rows if r['c'] != c]) for c in cohorts} if mode == 'loco' else None
        pooled = fit(rows)
        res[name] = {'n': len(rows), 'fits': fits or {'pooled': pooled}}
        for v, (use_cls, two) in VARS.items():
            cache = {}
            def fc(r):
                c = r['c'] if mode == 'loco' else 'pooled'
                if c not in cache:
                    b = fits[c] if mode == 'loco' else pooled
                    cache[c] = Dist(b['M'], b['sig'] if use_cls else 0.35, b, two)
                return cache[c]
            res[name][v] = evaluate(rows, H, fc)
    return res

def verdict(res):
    out = {}
    for fix, v in (('fix4_sigma', 'V1'), ('fix3_two_sided', 'V2')):
        d = {p: res[p][v]['ls'] - res[p]['V0']['ls'] for p in res}
        g = {p: res[p][v]['brier_sum'] - res[p]['V0']['brier_sum'] for p in res}
        better = sum(1 for x in d.values() if x >= 0.005); worse = sum(1 for x in d.values() if x < -0.005)
        guard = all(x <= 0.002 for x in g.values())
        out[fix] = dict(d_logscore=d, d_brier_sum=g, n_better=better, n_worse=worse, guard_ok=guard,
                        passes=(better >= 2 and worse == 0 and guard))
    return out

if __name__ == '__main__':
    for mode in ('loco', 'pooled'):
        res = run(mode)
        print('=====', mode)
        for p, R in res.items():
            print('--', p, 'n=%d' % R['n'], {c: {k: round(v, 3) for k, v in b.items()} for c, b in R['fits'].items()})
            for v in VARS:
                x = R[v]
                print('  %s ls=%.4f brier3=%.4f brierH=%.4f brierB=%.4f sum=%.4f | P3 %.3f/%.3f Ph %.3f/%.3f Pb %.3f/%.3f | cov50 %.3f cov80 %.3f | mean %.2f/%.2f'
                      % (v, x['ls'], x['b3'], x['bh'], x['bb'], x['brier_sum'], x['p3'], x['o3'], x['ph'], x['oh'], x['pb'], x['ob'], x['c50'], x['c80'], x['pmean'], x['omean']))
        print(json.dumps(verdict(res), indent=1, default=lambda z: round(z, 4)))
