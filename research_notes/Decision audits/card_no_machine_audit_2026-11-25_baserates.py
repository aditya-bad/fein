import csv,math
BT='research_notes/Backtests/'
def f(x):
    try: return float(x)
    except: return None
def stats(rows,label):
    # rows (w, r5 or 0.0 for failed-no-r5)
    rows=[r for r in rows if r[1] is not None]
    W=sum(w for w,_ in rows)
    def frac(c): return sum(w for w,m in rows if c(m))/W
    srt=sorted(rows,key=lambda r:r[1]); acc=0; med=None
    for w,m in srt:
        acc+=w
        if acc>=W/2: med=m;break
    mean=sum(w*m for w,m in rows)/W
    cap=sum(w*min(m,10) for w,m in rows)/W
    gm=math.exp(sum(w*math.log(max(m,0.01)) for w,m in rows)/W)
    print(f"{label}: n={len(rows)} median={med:.2f} mean={mean:.2f} mean(cap10x)={cap:.2f} geo={gm:.2f} P>=1.762={frac(lambda m:m>=1.7623):.3f} P>=1.469={frac(lambda m:m>=1.4693):.3f} P>=1.802(CoE12.5)={frac(lambda m:m>=1.802):.3f} P>=1.0={frac(lambda m:m>=1):.3f}")
for snap in (None,'FY2016','FY2018'):
    rows=[]
    for r in csv.DictReader(open(BT+'solvency_india_outputs/panel.csv')):
        m=f(r['mcap'])
        if m is None or not(1000<=m<=20000): continue
        if snap and r['snap']!=snap: continue
        r5=f(r['r5'])
        if r5 is None: r5 = 0.0 if r['o_fail']=='1' else None
        rows.append((float(r['weight']),r5))
    stats(rows,'india_nonfin '+str(snap))
for snap in (None,'FY2016','FY2018'):
    rows=[]
    for r in csv.DictReader(open(BT+'base_rates_lenders_india_outputs/panel.csv')):
        if snap and r['snap']!=snap: continue
        r5=f(r['r5'])
        if r5 is None: r5 = 0.0 if r['o_fail']=='1' else None
        rows.append((1.0,r5))
    stats(rows,'india_lender '+str(snap))
rows=[]
for r in csv.DictReader(open(BT+'solvency_us_outputs/panel.csv')):
    fl=f(r['float'])
    if fl is None or not(5e8<=fl<=1e10): continue
    r5=f(r['R5'])
    if r5 is None: r5 = 0.0 if r['O_fail']=='1' else None
    rows.append((1.0,r5))
stats(rows,'us_float (priced+failed; unpriced acquired excluded)')
