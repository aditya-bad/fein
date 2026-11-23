"""Recall of AR mode vs hand reads (one report per company) and vs the SUNFLAG hand ledger (section 5.4)."""
import json, re, sys
ARC = "/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/ar_mode"
HAND = {
 ("GULFPETRO", "2025-08-22"): [
  ("G1 PCMO: launch new products, expand passenger-car motor oil segment", r"PCMO|passenger car motor"),
  ("G2 Repsol alliance into Bangladesh/Nepal via exclusive distributors", r"Bangladesh|Nepal"),
  ("G3 bitumen: expand presence, HPCL supply, explore public/private opportunities", r"bitumen"),
  ("G4 explore lubricant opportunities beyond Indian borders", r"beyond Indian borders|international footprint"),
  ("G5 automotive: channel partners in unrepresented territories / LAKSHYA / market coverage", r"unrepresented|LAKSHYA|market coverage"),
  ("G6 Amron Oil Resources: SPA 07-Jun-2025 to acquire 50% (JV) - completion pending", r"Amron"),
  ("G7 tyre process oils: GPPL 'going to be one of the key beneficiaries'", r"key beneficiar"),
 ],
 ("REPRO", "2025-07-22"): [
  ("R1 content monetisation to play an increasingly significant role in turnover", r"increasingly significant role"),
  ("R2 content monetisation remains the key growth driver (3 pillars)", r"content monetisation will remain|key driver of growth"),
  ("R3 new Bindwel binding capacity planned to be installed", r"Bindwel"),
  ("R4 marketing priorities: global accessibility, GMV, reader engagement", r"boosting GMV|expanding global accessibility"),
  ("R5 expand sales and marketing teams across segments", r"expanding sales and marketing teams"),
  ("R6 BRSR target: top-5 online book seller ranking", r"top ?5 sel+ers|topnotch seller"),
  ("R7 BRSR: Phase-1 of data analytics platform", r"Phase-1 of data analytic"),
  ("R8 BRSR: plant assessments' corrective actions to complete next year", r"expected to be completed in the next year"),
 ],
}
SUN = [  # hand ledger cells (research_notes/Deep dives/SUNFLAG_live.md section 5.4): asset x report
 ("lohardongri", ["ARFY24", "ARFY25", "ARFY26"]), ("bhivkund", ["ARFY24", "ARFY25", "ARFY26"]),
 ("bajna", ["ARFY24", "ARFY25", "ARFY26"]), ("surjagad", ["ARFY24", "ARFY25", "ARFY26"]),
 ("belgaon", ["ARFY24", "ARFY25", "ARFY26"]), ("tambia", ["ARFY26"]), ("surajpura", ["ARFY26"])]


def jl(p):
    return [json.loads(l) for l in open(p)]


out = {}
for (sym, d), items in HAND.items():
    turns = json.load(open(f"{ARC}/{sym}/turns/{d}.json"))["turns"]
    zone = " ".join(t["text"] for t in turns)
    cands = [c for c in jl(f"{ARC}/{sym}/candidates.jsonl") if c["call_date"] == d]
    proms = [p for p in jl(f"{ARC}/{sym}/out/{sym}_scored.jsonl") if p["said_on"] == d]
    rows = []
    for name, rx in items:
        z = bool(re.search(rx, zone, re.I))
        c = any(re.search(rx, x["context"] + " " + x["sentence"], re.I) for x in cands)
        pr = [p for p in proms if re.search(rx, (p.get("context") or "") + " " + p["quote"], re.I)]
        rows.append({"item": name, "zone": z, "candidate": c, "promise": bool(pr),
                     "status": pr[0].get("auto_status_final") if pr and pr[0].get("auto_status_final") in
                     ("delivered", "partly", "missed", "moved-goalpost", "withdrawn") else (pr[0]["status"] if pr else None)})
    n = len(items)
    summ = {k: f"{sum(r[k] for r in rows)}/{n}" for k in ("zone", "candidate", "promise")}
    extra = [p["quote"][:160] for p in proms if not any(re.search(rx, (p.get("context") or "") + " " + p["quote"], re.I)
                                                       for _, rx in items)]
    out[sym] = {"report": d, "rows": rows, "recall": summ, "pipeline_promises_in_report": len(proms),
                "pipeline_promises_not_in_hand_list": extra, "candidates_in_report": len(cands)}
    print(sym, d, summ, "pipeline promises:", len(proms), "unmatched:", len(extra))
    for r in rows:
        print("  ", r)
    for e in extra:
        print("   EXTRA:", e)
# SUNFLAG ledger
a = json.load(open(f"{ARC}/SUNFLAG/out/SUNFLAG_assets.json"))
cells = [(k, q) for k, qs in SUN for q in qs]
hit = [(k, q) for k, q in cells if q in a["assets"].get(k, {})]
miss = sorted(set(cells) - set(hit))
proms = jl(f"{ARC}/SUNFLAG/out/SUNFLAG_scored.jsonl")
bajna = [p for p in proms if p.get("asset") == "bajna"]
flags = a["flags"]
print("SUNFLAG ledger cells covered by tracker:", f"{len(hit)}/{len(cells)}", "missing:", miss)
print("Bajna dated promise:", [(p["quote"], p["deadline"], p["status"]) for p in bajna])
print("Belgaon unchanged flag:", [f for f in flags if f["asset"] == "belgaon"])
out["SUNFLAG"] = {"ledger_cells": f"{len(hit)}/{len(cells)}", "missing": miss,
                  "bajna": [(p["quote"], p["deadline"], p["status"]) for p in bajna],
                  "belgaon_flags": [f for f in flags if f["asset"] == "belgaon"]}
json.dump(out, open(f"{ARC}/recall.json", "w"), indent=1)
