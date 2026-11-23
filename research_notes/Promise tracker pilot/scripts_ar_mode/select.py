"""Seeded random draw of 2 no-concall NSE small caps for the AR-mode validation (2026-11-23)."""
import json, random, re, sys, datetime as dt, os
sys.path.insert(0, "/home/user/fein/tools/promise_tracker/pipeline"); sys.path.insert(0, "/home/user/fein/tools")
import fetch as FE, common as C
SP = "/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad"
rows = json.load(open(SP + "/live_dd1/mcap_rows.json"))
sel = json.load(open(SP + "/live_dd1/selection_order.json"))
fin = set(sel["fin_idx"]) | set(sel["fin_hand"])
elig = sorted(r["sym"] for r in rows if 300 <= r["mcap"] <= 5000 and r["industry"] != "Financial Services"
              and r["sym"] not in fin and r["sym"] != "SUNFLAG")
print("eligible", len(elig))
random.Random(202611232).shuffle(elig)
print("first 15:", elig[:15])
root = SP + "/ar_mode/_select"
CALL_RX = re.compile(r"earnings\s+call|conference\s+call|con-?\s?call|investor[s]?\s+call|analyst[s]?\s+call|"
                     r"analyst\s*/\s*investor\s+meet|analysts?\s+meet", re.I)
log, picked = [], []
for s in elig:
    if len(picked) == 2 or len(log) >= 25:
        break
    ann = FE.list_announcements(s, root)
    recent = [r for r in ann if C.parse_nse_date(r["an_dt"]) >= dt.date(2023, 1, 1)]
    tr = [r for r in recent if FE.is_transcript(r)]
    calls = [r for r in recent if CALL_RX.search((r.get("attchmntText") or "") + " " + (r.get("desc") or ""))]
    mc = next(r["mcap"] for r in rows if r["sym"] == s)
    if tr or calls:
        log.append((s, mc, f"skip: {len(tr)} transcripts, {len(calls)} call/meet intimations since 2023"))
        continue
    import nse_fetch
    ars = nse_fetch.annual_reports(s)
    yrs = sorted({int(r["toYr"]) for r in ars if r.get("toYr")})
    if len([y for y in yrs if y >= 2024]) < 3:
        log.append((s, mc, f"skip: ARs on NSE only for FY {yrs[-4:]}"))
        continue
    log.append((s, mc, f"PICK: 0 transcripts, 0 call intimations in {len(recent)} announcements since 2023; ARs FY{yrs[-5:]}"))
    picked.append(s)
for x in log:
    print(x)
json.dump({"eligible_n": len(elig), "order_first_25": elig[:25], "log": log, "picked": picked},
          open(SP + "/ar_mode/selection.json", "w"), indent=1)
