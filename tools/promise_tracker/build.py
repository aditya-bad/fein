import json,re,sys
B="https://nsearchives.nseindia.in/corporate/"
DOCS={
 "2024-05-28":("Q4FY24 concall transcript",B+"UNIPARTS_03062024180403_Q4EarningsCallTranscript.pdf"),
 "2024-08-09":("Q1FY25 concall transcript",B+"UNIPARTS_15082024220239_Q1EarningsCallTranscript.pdf"),
 "2024-11-08":("Q2FY25 concall transcript",B+"UNIPARTS_15112024160106_Q2EarningsCallTranscript.pdf"),
 "2025-02-07":("Q3FY25 concall transcript",B+"Earth_2018_13022025113327_Q3EarningsCallTranscript.pdf"),
 "2025-05-28":("Q4FY25 concall transcript",B+"Earth_2018_03062025195354_Q4EarningsCallTranscript.pdf"),
 "2025-08-11":("Q1FY26 concall transcript",B+"Earth_2018_14082025142230_Q125EarningsCallTranscript.pdf"),
 "2025-11-17":("Q2FY26 concall transcript",B+"Earth_2018_21112025180659_Q2_Transcript.pdf"),
 "2026-02-10":("Q3FY26 concall transcript",B+"Earth_2018_17022026111942_Q325EarningsCallTranscript.pdf"),
 "2026-05-26":("Q4FY26 concall transcript",B+"Earth_2018_01062026112803_Q425EarningsCallTranscript.pdf"),
 "2026-08-05":("Q1FY27 concall transcript",B+"Earth_2018_12082026114646_Q126EarningsCallTranscript.pdf"),
 "2026-11-05":("Q2FY27 concall transcript",B+"Earth_2018_12112026160836_Q226EarningsCallTranscript.pdf"),
}
SCR="https://www.screener.in/company/UNIPARTS/consolidated/"
SPEC={"precise":3,"range":2,"vague":1}
SCORE={"PLACEHOLDER":None,"delivered":1,"partly":0.5,"missed":-1,"moved-goalpost":-1.5,"silently-dropped":-1.5,"pending":None}
P=[]
def p(said_on,slug,title,speaker,quote,category,metric,target,deadline,deadline_precision,specificity,volunteered,status,evidence,
      materiality=2,explanation=None,admitted_unprompted=None,delivery_ratio=None,conditionality=None,check_after=None,extra_src=None,target_low=None,target_high=None,unit=None,baseline=None,confidence="verified"):
    P.append(dict(said_on=said_on,slug=slug,title=title,speaker=speaker,quote=quote,category=category,metric=metric,target=target,
      deadline=deadline,deadline_precision=deadline_precision,specificity=specificity,volunteered=volunteered,status=status,evidence=evidence,
      materiality=materiality,explanation=explanation,admitted_unprompted=admitted_unprompted,delivery_ratio=delivery_ratio,
      conditionality=conditionality,check_after=check_after,extra_src=extra_src or [],target_low=target_low,target_high=target_high,unit=unit,baseline=baseline,confidence=confidence))
exec(open(sys.argv[1]).read())
recs=[]
for x in P:
    doc,url=DOCS[x["said_on"]]
    pid=f"promise:UNIPARTS:{x['said_on']}:{x['slug'].replace('.','-')}"
    data={k:x[k] for k in ["said_on","speaker","quote","category","metric","target","target_low","target_high","unit","baseline","deadline","deadline_precision","specificity","volunteered","conditionality","status","evidence","explanation","admitted_unprompted","delivery_ratio","materiality","check_after"]}
    data["source_doc"]=doc; data["source_url"]=url
    data["specificity_score"]=SPEC[x["specificity"]]
    data["unprompted"]=(x["volunteered"]=="volunteered")
    data["score"]=SCORE[x["status"]]
    EX=["mexico","third-platform","fabrication","aftermarket","tariff","fire","3pl-hhp","geo-mix","warehouse-share"]
    data["driver"]="execution" if any(k in x["slug"] for k in EX) else "cycle/financial"
    data["status_history"]=[{"as_of":x["said_on"],"status":"pending","evidence":"stated"}]+([{"as_of":"2026-11-19","status":x["status"],"evidence":x["evidence"]}] if x["status"]!="pending" else [])
    body=(f"{x['speaker']} on the {doc.replace(' concall transcript','')} call ({x['said_on']}), {x['volunteered']}: \"{x['quote']}\" "
          f"Metric: {x['metric']}. Target: {x['target']}. Deadline: {x['deadline']} ({x['deadline_precision']}). Specificity: {x['specificity']}. "
          f"Status as of 2026-11-19: {x['status'].upper()}. Evidence: {x['evidence']}"+(f" Management explanation: {x['explanation']}" if x['explanation'] else ""))
    src=[url]+([SCR] if x["status"]!="pending" else [])+x["extra_src"]
    recs.append({"type":"promise","id":pid,"title":x["title"],"body":body,"tickers":["UNIPARTS"],
      "tags":["india","promise-tracker","management-credibility","sector-auto-ancillary","off-highway",x["category"].replace("_","-")],
      "date":x["said_on"],"data":data,"sources":list(dict.fromkeys(src)),"confidence":x["confidence"],
      "links":[{"to":"company:UNIPARTS","rel":"about"},{"to":"analysis:UNIPARTS:credibility-2026-11","rel":"part_of"}]})
# analysis record
try: exec(open(sys.argv[2]).read())
except (IndexError,FileNotFoundError): pass
out="/home/user/fein/memdb/seeds/2026-11-19_promises_UNIPARTS.json"
json.dump(recs,open(out,"w"),indent=1,ensure_ascii=False)
ids=[r["id"] for r in recs]; assert len(ids)==len(set(ids)),"dup ids"
for r in recs: assert re.match(r'^[a-z_]+:',r['id'])
print(len(recs),"records written")
