import json, glob, os, importlib.util, sys
B=os.path.dirname(os.path.abspath(__file__))
OUT='/home/user/fein/memdb/seeds/2026-11-21_paper_calls_batch2.json'
MD='/home/user/fein/research_notes/Paper calls/batch2.md'
METHODS={'promise-tracker':'promise-tracker credibility','base-rate':'base rate','flags-judgment':'flags-judgment context',
 'sector-cycle':'sector cycle/lead indicator','valuation-temperature':'valuation-temperature','mgmt-tone':'management-tone-vs-delivery'}
calls=[]
for f in sorted(glob.glob(os.path.join(B,'stage*.py'))):
    spec=importlib.util.spec_from_file_location(os.path.basename(f)[:-3],f); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    calls+=m.CALLS
recs=[]
for c in calls:
    tk=c['ticker']; idt=('US-'+tk) if c['market']=='us' else tk
    p=c['p']; b=c['base']; assert 0.05<=p<=0.95 and p!=0.5, (tk,p)
    assert '2027-01-15'<=c['resolve_by']<='2027-06-30', (tk,c['resolve_by'])
    ml=METHODS[c['method']]
    body=(f"Forward test of the {ml} method (NOT a recommendation; not buy/sell). Probability {p:.2f} (naive base rate {b:.2f}) that: {c['event']}. "
          f"Evidence: {c['evidence']} Reasoning: {c['why']} Resolution: {c['rule']} Source: {c['source']}. Resolve by {c['resolve_by']}; score with Brier vs base rate.")
    r={'type':'thesis','id':f"thesis:paper-call:{idt}:{c['slug']}",'title':'Paper call: '+c['event'],'body':body,'tickers':[idt],
       'tags':['paper-call','method-test','batch2',c['method'],c['market']]+c.get('tags',[]),'date':'2026-11-21','status':'open',
       'data':{'probability':p,'base_rate_probability':b,'base_rate_reasoning':c['base_reasoning'],'method':ml,'made_on':'2026-11-21',
               'resolve_by':c['resolve_by'],'resolution_rule':c['rule'],'resolution_source':c['source'],'outcome':None,'brier':None},
       'sources':c['sources'],'confidence':c.get('confidence','single-source')}
    if c.get('links'): r['links']=c['links']
    recs.append(r)
ids=[r['id'] for r in recs]; assert len(ids)==len(set(ids))
json.dump(recs,open(OUT,'w'),indent=1,ensure_ascii=False)
json.load(open(OUT))
# markdown
from collections import Counter
mk=Counter(c['market'] for c in calls); me=Counter(c['method'] for c in calls)
L=[]
L.append('# Paper calls — batch 2 (made 2026-11-21)\n')
L.append('Forward, dated, probabilistic predictions about measurable events, used to **test methods** (lessons L11, L15).\nThey are **not recommendations** — no call says or implies buy/sell. Each is scored with Brier score against\na naive base-rate forecaster when it resolves (Jan–Jun 2027). Seed file: `memdb/seeds/2026-11-21_paper_calls_batch2.json`.\nCompanion to batch 1 (`research_notes/Paper calls/batch1.md`); no company or event from batch 1 or the 7 pilot calls is repeated.\n')
L.append(open(os.path.join(B,'context.md')).read())
L.append(f"**Count:** {len(calls)} calls — india: {mk['india']}, us: {mk['us']}. By method: "+', '.join(f'{k}: {v}' for k,v in me.most_common())+'.\n')
L.append('## Summary table\n\n| # | Market | Ticker | Call (event) | Method | P(ours) | P(base) | Resolve by |\n|---|---|---|---|---|---|---|---|')
for i,c in enumerate(calls,1):
    L.append(f"| {i} | {c['market']} | {c['ticker']} | {c['event']} | {c['method']} | {c['p']:.2f} | {c['base']:.2f} | {c['resolve_by']} |")
L.append('\n## Evidence and resolution rules\n')
for i,(c,r) in enumerate(zip(calls,recs),1):
    L.append(f"### {i}. {c['ticker']} — {c['event']}\n- **id:** `{r['id']}`\n- **Method:** {METHODS[c['method']]} · **P(ours)** {c['p']:.2f} · **P(base)** {c['base']:.2f} · resolve by {c['resolve_by']}\n- **Evidence:** {c['evidence']}\n- **Why our number differs from base:** {c['why']}\n- **Base-rate reasoning:** {c['base_reasoning']}\n- **Resolution rule:** {c['rule']}\n- **Resolution source:** {c['source']}\n- **Sources used:** {'; '.join(c['sources'])}\n- **Confidence of evidence:** {c.get('confidence','single-source')}\n")
L.append(open(os.path.join(B,'tail.md')).read())
open(MD,'w').write('\n'.join(L))
print('ok',len(recs),dict(mk),dict(me))
