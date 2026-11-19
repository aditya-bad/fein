import json,datetime as dt,collections,sys
R=[r for r in json.load(open("/home/user/fein/memdb/seeds/2026-11-19_promises_UNIPARTS.json")) if r["type"]=="promise"]
asof=dt.date(2026,11,19)
EXEC={"capacity_commissioning","customer_win","m&a","new_product"}
def w(d,drop_spec=False):
    q=(asof-dt.date.fromisoformat(d["said_on"])).days/91.3
    return (1 if drop_spec else d["specificity_score"])*d["materiality"]*0.5**(q/8)
def mcs(rs,**k):
    rs=[r for r in rs if r["data"]["score"] is not None]
    W=sum(w(r["data"],**k) for r in rs); 
    return (sum(w(r["data"],**k)*r["data"]["score"] for r in rs)/W if W else None), len(rs)
def summary(rs,label):
    res=[r for r in rs if r["data"]["status"]!="pending"]
    c=collections.Counter(r["data"]["status"] for r in rs)
    m,n=mcs(rs); m2,_=mcs(rs,drop_spec=True)
    hit=sum(r["data"]["status"]=="delivered" for r in res)/len(res) if res else None
    drs=[r["data"]["delivery_ratio"] for r in res if r["data"]["delivery_ratio"] is not None]
    bad=[r for r in res if r["data"]["status"] in("missed","moved-goalpost","silently-dropped","partly")]
    cand=[r["data"]["admitted_unprompted"] for r in bad]
    ci=sum(1 for x in cand if x)/len(bad) if bad else None
    print(f"{label}: n={len(rs)} resolved={len(res)} {dict(c)} MCS={m:+.2f} (unweighted-spec {m2:+.2f}) hit={(hit or 0):.0%} avgDR={(sum(drs)/len(drs) if drs else 0):.2f} (n={len(drs)}) candour={(ci or 0):.0%} of {len(bad)} shortfalls")
    return m
summary(R,"ALL")
summary([r for r in R if r["data"]["status"]!="silently-dropped" or r["data"]["category"]!="revenue_growth" or "small-ag" not in r["id"]],"ALL ex small-ag")
summary([r for r in R if r["data"]["said_on"]<"2025-05-01"],"FY25 calls (promoter-led)")
summary([r for r in R if r["data"]["said_on"]>="2025-05-01"],"FY26-27 calls (COO/CEO-led)")
summary([r for r in R if r["data"]["driver"]=="execution"],"Execution/strategic")
summary([r for r in R if r["data"]["driver"]!="execution"],"Cycle/financial")
summary([r for r in R if r["data"]["volunteered"]=="volunteered"],"Volunteered")
summary([r for r in R if r["data"]["volunteered"]=="prompted"],"Prompted")
for s in ["precise","range","vague"]: summary([r for r in R if r["data"]["specificity"]==s],s)
