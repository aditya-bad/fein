pids=[r["id"] for r in recs]
recs.append({"type":"analysis","id":"analysis:UNIPARTS:credibility-2026-11",
 "title":"Uniparts India: management promise-vs-delivery ledger and credibility score (FY25 Q1 - FY27 Q2)",
 "body":("Pilot of the promise tracker. 10 concalls (2024-08-09 to 2026-11-05) gave 68 forward-looking promises, scored against later calls and screener.in quarterly numbers as of 2026-11-19. "
  "Of 47 resolved: 26 delivered, 7 partly, 6 missed, 6 moved-goalpost, 2 silently-dropped; 21 pending. Hit rate 55%. "
  "Management Credibility Score (MCS; scale -1.5..+1, weight = specificity x materiality x 8-quarter half-life) = +0.28 overall. Two very different regimes: "
  "FY25 calls (promoter Paramjit Soni guiding into a downturn) MCS -0.24, hit rate 33%. FY25 revenue was guided flat to -3% and came in at -15%; 'Q4 highest quarter' was restated, and the restatement was then denied. "
  "FY26-27 calls (COO, later CEO, Tanushree Bagrodia) MCS +0.65, hit rate 78%. Mid-teens FY26 guide vs +21% actual; FY27 raised three times. "
  "The split that matters is cycle vs execution, not the person: cycle/financial promises MCS +0.53, execution/strategic promises (Mexico, acquisition/third platform, fabrication, aftermarket) MCS -0.08. "
  "Mexico slipped about 10 months, with every new date called 'on track'. The acquisition promised 'within the next year or so' (Nov-2024) never happened; two deals fell through. "
  "Aftermarket was guided mid-teens, then single digit, and actually fell ~9% in FY26. "
  "Candour index ~5%: only 1 of 21 shortfalls was admitted unprompted (Hurricane Helene). Explanations came only when analysts asked. "
  "Tone vs delivery: upbeat tone with near-term misses in FY25. In FY26-27 numeric guides were conservative and beaten, but execution items kept an 'on track' tone while they slipped. "
  "Volunteered promises scored worse (MCS -0.29) than prompted ones (+0.43). "
  "Read: trust the revenue/margin guide in an upturn as a floor; discount strategic and timeline promises by ~1-3 quarters and the acquisition story heavily. "
  "Caveats: one scorer, no second-pass review; era is confounded with the cycle; segment data is mostly management-only."),
 "tickers":["UNIPARTS"],"tags":["india","promise-tracker","management-credibility","governance","process","sector-auto-ancillary","off-highway","cyclical"],
 "date":"2026-11-19",
 "data":{"method":"promise-tracker v0 (edge_methods_data_access.md section 2)","as_of":"2026-11-19","calls_covered":["Q1FY25","Q2FY25","Q3FY25","Q4FY25","Q1FY26","Q2FY26","Q3FY26","Q4FY26","Q1FY27","Q2FY27"],
  "n_promises":68,"n_resolved":47,"status_counts":{"delivered":26,"partly":7,"missed":6,"moved-goalpost":6,"silently-dropped":2,"pending":21},
  "mcs":0.28,"mcs_scale":"-1.5..+1 (delivered +1, partly +0.5, missed -1, moved-goalpost -1.5, silently-dropped -1.5)","mcs_ex_disputed_small_ag":0.33,
  "mcs_fy25_calls":-0.24,"mcs_fy26_27_calls":0.65,"mcs_cycle_financial":0.53,"mcs_execution_strategic":-0.08,"mcs_volunteered":-0.29,"mcs_prompted":0.43,
  "mcs_by_specificity":{"precise":0.46,"range":0.15,"vague":0.09},
  "hit_rate":0.55,"hit_rate_fy25":0.33,"hit_rate_fy26_27":0.78,"avg_delivery_ratio":1.07,"candour_index":0.05,"moved_goalposts":6,
  "weights":"specificity_score(1-3) x materiality(1-3) x 0.5^(quarters_since/8)",
  "tone_delivery_gap":"FY25: high optimism, poor near-term delivery (gap large). FY26-27: measured tone, numeric beats (gap small/negative); execution items: persistent 'on track' language while slipping (gap large).",
  "change_detectors":["Promoter Paramjit Soni (main FY25 guidance voice) absent from calls after May-2025","Tanushree Bagrodia joined as Group COO Nov-2024; Group CEO by Feb-2026","CFO change: Rohit Maheshwari -> Sandeep Taneja (by May-2026)","IR head changes (Vivek Maheshwari -> Kumar Sunit -> Himanshu Sharma); call host Go India -> EY (Aug-2026)","Capex band drift: 2.5% -> 2.5-3% -> 2.5-3.5% -> ~INR 60 cr (~4%)","Aftermarket and segment KPIs disclosed inconsistently (no FY26 aftermarket number until asked)"],
  "watch_next":["Q3FY27 revenue ~INR 347 cr","FY27 +24%","Ludhiana finishing shop by 31-Dec-2026","Mexico H2FY27 single-digit USD m","capex ~INR 60 cr","fabrication 8-10% of revenue by ~Nov-2028","acquisition (about half a dozen under evaluation)"],
  "promise_ids":pids},
 "sources":["https://www.screener.in/company/UNIPARTS/consolidated/"]+[u for d,(k,u) in sorted(DOCS.items()) if d>"2024-06-01"] ,
 "confidence":"single-source",
 "links":[{"to":"company:UNIPARTS","rel":"about"},{"to":"analysis:UNIPARTS:2026-11-19","rel":"similar_to"}]})
