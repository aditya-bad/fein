import sys,os,json,math,copy
sys.path.insert(0,'tools/decision'); sys.path.insert(0,'tools/valuation')
import decision_card as dc
rates=json.load(open('tools/decision/base_rates.json'))
def anchored(sc,sig,brb,brl,w,k=1.0):
    s=copy.deepcopy(sc)
    for r in s['scenarios']: r['mult5']*=k
    s['ev_mult5']=sum(r['prob']*r['mult5'] for r in s['scenarios'])+s['blowup']['prob']*s['blowup']['multiple']
    touts=dc._outcomes_tagged(s,sig); raw=[(p,m) for p,m,_ in touts]
    pa_m=s['blowup']['prob']
    # model p_le_half
    pl_m=sum(r['prob']*dc.ws.norm_cdf((math.log(.5)-math.log(r['mult5']))/sig) for r in s['scenarios'])+(pa_m if s['blowup']['multiple']<=.5 else 0)
    if brb is None and brl is None: outs=raw; ev=s['ev_mult5']
    else:
        pa=dc.anchor_p(pa_m,brb,w) if brb is not None else pa_m
        pl=dc.anchor_p(pl_m,brl,w) if brl is not None else pl_m
        outs,_=dc.anchor_outcomes(touts,pa,pl)
        ev=s['ev_mult5']+(sum(p*m for p,m in outs)-sum(p*m for p,m in raw))
    return s,ev,outs
def solve(fn,lo=0.3,hi=5):
    for _ in range(60):
        mid=(lo+hi)/2
        if fn(mid): hi=mid
        else: lo=mid
    return hi
def analyse(name,sc,sig,hurdle,brb,brl,w=0.5,kf=0.25,cap=0.04):
    s,ev,outs=anchored(sc,sig,brb,brl,w)
    f,_=dc._kelly(outs,hurdle)
    base=[r for r in s['scenarios'] if r['name']=='base'] or [max(s['scenarios'],key=lambda r:r['prob'])]
    b=base[0]['mult5']
    k_ev=solve(lambda k: anchored(sc,sig,brb,brl,w,k)[1]>=hurdle)
    k_f=solve(lambda k: dc._kelly(anchored(sc,sig,brb,brl,w,k)[2],hurdle)[0]>0)
    k_1=solve(lambda k: dc._kelly(anchored(sc,sig,brb,brl,w,k)[2],hurdle)[0]*kf>=0.01)
    irr=lambda m: m**0.2-1
    return dict(name=name,ev_raw=s['ev_mult5'],ev_anc=ev,f=f,base_mult=b,base_irr=irr(b),
      k_ev=k_ev,base_irr_ev=irr(b*k_ev),price_drop_ev=1-1/k_ev,k_f=k_f,base_irr_f=irr(b*k_f),k_1pct=k_1,base_irr_1pct=irr(b*k_1),price_drop_1pct=1-1/k_1,
      scen=[(r['name'],r['prob'],round(r['mult5'],2)) for r in s['scenarios']],bl=(s['blowup']['prob'],s['blowup']['multiple']))
res=[]
for t in ['AUTOAXLES','HARSHA','INDRAMEDCO','SUNFLAG','US-KEX','UTKARSHBNK']:
    p='tools/decision/live/%s_card.json'%t
    card=dc._load_json(p)
    F,rec,wres=dc.build(card,p)
    wd=wres['input']; sc=wres['scenarios']
    cn,_=dc.resolve_base_rate_class(card,wd,wres,rates)
    cls=rates['classes'].get(cn) or rates['classes'].get(str(cn)+'_deprecated') or {}
    w,_=dc.anchor_weight(card.get('tail_anchor'))
    hurdle=sc['hurdle_mult5']
    cap=(card.get('sizing') or {}).get('max_pct_at_cost') or dc.TIER_CAPS.get((card.get('sizing') or {}).get('tier','satellite'))
    r=analyse(t,sc,wd['dispersion'],hurdle,cls.get('p_blowup'),cls.get('p_le_half'),w,(card.get('sizing') or {}).get('kelly_fraction',0.25))
    r.update(cls=cn,w=w,hurdle=hurdle,coe=wd['coe'],sig=wd['dispersion'],pw_vs_price=sc.get('pw_vs_price'),model_pb=sc.get('p_blowup'),model_pl=sc.get('p_le_half'),gates=[g[0] for g in [x for x in []]])
    # blocking gates from decision record
    dec=[x for x in rec if x.get('type')=='decision'][0]
    r['decision_data']={k:dec.get('data',{}).get(k) for k in ('size','blocked_by','blocking_gates','final_size')}
    res.append(r)
    print(json.dumps(r,default=str))
# synthetic
H=1.12**5
for label,irr in [('fair CoE 12.5%',.125),('good CoE+5pp 17.5%',.175),('index 12%',.12)]:
    b=(1+irr)**5
    # symmetric-ish shape typical of cards: bear 0.25 @0.65b, base 0.5 @b, bull 0.2 @1.45b, blowup 5% @0.1
    sc={'scenarios':[{'name':'bear','prob':.25,'mult5':.65*b},{'name':'base','prob':.5,'mult5':b},{'name':'bull','prob':.2,'mult5':1.45*b}],'blowup':{'prob':.05,'multiple':.1}}
    r=analyse('SYN '+label+' (card-shaped)',sc,.35,H,.1537,.1127)
    print(json.dumps(r,default=str))
    # pure: all mass at base, no blowup, sigma .35 -> isolates anchoring
    sc2={'scenarios':[{'name':'base','prob':1.0,'mult5':b}],'blowup':{'prob':0.0,'multiple':.1}}
    r=analyse('SYN '+label+' (single scenario, no model blowup)',sc2,.35,H,.1537,.1127)
    print(json.dumps(r,default=str))
    r=analyse('SYN '+label+' (single scenario, no anchoring)',sc2,.35,H,None,None)
    print(json.dumps(r,default=str))
print('---extra')
for t in ['AUTOAXLES','HARSHA','INDRAMEDCO','SUNFLAG','US-KEX','UTKARSHBNK']:
    p='tools/decision/live/%s_card.json'%t
    card=dc._load_json(p); F,rec,wres=dc.build(card,p); sc=wres['scenarios']; wd=wres['input']
    eb=sc.get('exit_bet') or {}
    print(t, 'p3x=%.3f'%sc['p_ge_3x'], 'median=%.2f'%sc['median_mult5'], 'exits', [(r['name'],r['exit_pe'],round(r['dcf_pe5'] or 0,1)) for r in sc['scenarios']],
      'ev_stated/dcf/own', [round(eb[k],2) if eb.get(k) else None for k in ('ev_stated','ev_dcf','ev_own')], 'own_median', [r.get('own_median') for r in eb.get('rows',[])][:1] if eb else None, 'mode', wd.get('mode'), 'pe', round(wres['snapshot'].get('pe') or 0,1))
