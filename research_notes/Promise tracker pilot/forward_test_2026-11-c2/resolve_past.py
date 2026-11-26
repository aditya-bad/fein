#!/usr/bin/env python3
"""Cohort-2 past-promise resolver (prereg s2): after run.py (fetch -> turns -> candidates -> llm_extract -> score),
take every chain head (earliest statement of a chain) said 2023-07-01.. with deadline <= 2026-09-30, attach
evidence sentences from LATER calls' management turns (keyword retrieval) + the screener FY/quarter numbers +
score.py's auto verdict, and ask the LLM CLI (claude -p) to assign a status under the pipeline v1.4 thresholds.
Claude (this session) then reviews disagreements with the numbers and a sample of the rest.

  python3 -I resolve_past.py SYM --cache /root/pt_cache_c2 [--cmd "claude -p"] [--batch 14]
Writes <cache>/<SYM>/out/<SYM>_resolved.jsonl (one row per chain head) and raw LLM output in <cache>/<SYM>/resolve/.
Research, not SEBI-registered advice."""
import argparse, json, os, re, shlex, subprocess, sys
PIPE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "tools", "promise_tracker", "pipeline")
sys.path.insert(0, os.path.abspath(PIPE))
import common as C  # noqa: E402
import financials as F  # noqa: E402

SAID_FROM, DUE_BY = "2023-07-01", "2026-09-30"
FINAL = ("delivered", "partly", "missed", "moved-goalpost", "withdrawn")
STOP = set("""the and for with that this from will have been into over under year years quarter quarters which what their there
about would should could also than then them they were your just like more most some such very much going expect expected expecting
target targets guidance around approximately roughly basis level levels business company number numbers growth crore crores cr inr rs
fy fy24 fy25 fy26 fy27 fy28 h1 h2 q1 q2 q3 q4 percent consolidated standalone revenue revenues""".split())

PROMPT = """You are resolving management promises made on Indian company earnings calls (company: {name}, NSE: {sym}).
For EACH promise below decide what actually happened by its deadline, using ONLY the evidence given (later-call
management statements, the screener numbers table, and the automatic numbers check). Rules (pipeline v1.4):
- growth targets: delivered if actual >= target low end minus max(0.5 pp, 5% of the target); partly within max(2 pp, 20%); else missed.
- margin/ratio targets: delivered within 0.3 pp of the low end (or better); partly within 1.5 pp; else missed.
- amounts and days: delivered at >= 95% of the target (ceilings: <= 105%); partly 80-95%; else missed.
- explicit floors/ceilings ("25% plus", "below 4.5%") are strict: delivered only if met.
- dated events (commissioning, launch, approval, closing, hiring, go-live): delivered only if done by the deadline; up to one
  quarter late = partly; later or still not done = missed.
- moved-goalpost: the company later restated a lower target or later date for THIS promise without calling it a revision, and
  the original was not met. withdrawn: the company explicitly acknowledged cutting/dropping it and the original was not met.
- unresolvable: the evidence does not settle it (do NOT guess). Use this whenever no later statement or number decides it.
- Beating a target = delivered. A company-defined metric (segment, order intake, deal wins, EBITDA as the company reports it) is
  decided from management's later statement of the actual figure, not from screener.
- If the automatic numbers check gives a status, accept it unless the evidence shows the company's own reported figure for the
  SAME metric differs (e.g. company EBITDA vs screener OPM); then say why.

Screener numbers (Rs cr; FY = year ending March; OPM = operating profit / sales, excludes other income):
{fin}

Promises (JSON, one per line; "evidence" = later management sentences, dated by call):
{items}

Output ONLY JSON Lines, one per promise, in the same order:
{{"id": "<id>", "status": "delivered|partly|missed|moved-goalpost|withdrawn|unresolvable", "actual": "<the actual figure or event, short>", "evidence": "<call date + short quote or 'screener FY..'>", "confidence": "high|medium|low"}}
"""


def fin_table(root, sym):
    try:
        page, _ = F.fetch_screener(sym, root)
        fin = F.parse_screener(page)
    except Exception as e:  # noqa: BLE001
        return f"(screener unavailable: {e})"
    out = []
    for key, lab in (("FY", "FY"), ("Q", "Quarter")):
        d = fin.get(key) or {}
        per = sorted(d)[-(8 if key == "FY" else 14):]
        for p in per:
            r = d[p]
            vals = {k: r.get(k) for k in ("sales", "op_profit", "net_profit", "other_income", "interest", "depreciation", "cfo",
                                          "debtor_days", "wc_days", "roce_pct") if r.get(k) is not None}
            if r.get("sales") and r.get("op_profit") is not None:
                vals["opm_pct"] = round(100 * r["op_profit"] / r["sales"], 1)
            out.append(f"{lab} {p}: " + ", ".join(f"{k}={v}" for k, v in vals.items()))
    bs = fin.get("BS") or {}
    for p in sorted(bs)[-4:]:
        r = bs[p]
        vals = {k: r.get(k) for k in ("borrowings", "cwip", "fixed_assets", "reserves") if r.get(k) is not None}
        out.append(f"BS {p}: " + ", ".join(f"{k}={v}" for k, v in vals.items()))
    return "\n".join(out)[:6000]


def sentences(root, sym):
    tdir = C.sym_dir(root, sym, "turns")
    rows = []
    for f in sorted(os.listdir(tdir)):
        if not f.endswith(".json"):
            continue
        d = json.load(open(os.path.join(tdir, f)))
        for t in d["turns"]:
            if t.get("role") != "management":
                continue
            for s in re.split(r"(?<=[\.\?!])\s+", t["text"]):
                if 30 <= len(s) <= 600:
                    rows.append((d["call_date"], s))
    return rows


def kw(p):
    txt = " ".join(str(p.get(k) or "") for k in ("title", "metric", "target", "quote"))
    ck = str((p.get("chain") or {}).get("chain_key") or p.get("chain_key") or "")
    toks = re.findall(r"[A-Za-z][A-Za-z\-]{3,}", txt + " " + ck.replace(":", " ").replace("_", " "))
    out = []
    for t in toks:
        t = t.lower().strip("-")
        if t not in STOP and t not in out:
            out.append(t)
    return out[:14]


def evidence(p, sents, n=10):
    ks = kw(p)
    said = p["said_on"]
    scored = []
    for d, s in sents:
        if d <= said:
            continue
        sl = s.lower()
        h = sum(1 for k in ks if k in sl)
        if h >= 2 or (h >= 1 and re.search(r"\d", s) and len(ks) <= 3):
            scored.append((h, d, s))
    scored.sort(key=lambda x: (-x[0], x[1]))
    top = sorted(scored[:n], key=lambda x: x[1])
    return [f"[{d}] {s[:420]}" for _, d, s in top]


def heads(rows):
    by = {}
    for p in rows:
        k = (p.get("chain") or {}).get("chain_key") or p.get("chain_key") or p["id"]
        by.setdefault(k, []).append(p)
    out = []
    for k, ps in by.items():
        ps.sort(key=lambda x: x["said_on"])
        h = ps[0]
        h["_chain"] = k
        h["_n_statements"] = len(ps)
        h["_later"] = [{"said_on": x["said_on"], "target": x.get("target"), "deadline": x.get("deadline"),
                        "ack": x.get("acknowledges_revision")} for x in ps[1:]][:4]
        out.append(h)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("symbol"); ap.add_argument("--cache", required=True); ap.add_argument("--cmd", default="claude -p")
    ap.add_argument("--batch", type=int, default=14); ap.add_argument("--name", default="")
    a = ap.parse_args()
    sym, root = a.symbol.upper(), a.cache
    out_dir = C.sym_dir(root, sym, "out")
    scored = C.read_jsonl(os.path.join(out_dir, f"{sym}_scored.jsonl"))
    past = [p for p in scored if p["said_on"] >= SAID_FROM and (p.get("deadline") or "9999") <= DUE_BY]
    hs = heads(past)
    sents = sentences(root, sym)
    fin = fin_table(root, sym)
    rdir = C.sym_dir(root, sym, "resolve"); os.makedirs(rdir, exist_ok=True)
    items = []
    for h in hs:
        au = h.get("auto") or {}
        items.append({"id": h["id"], "said_on": h["said_on"], "speaker": h.get("speaker"), "quote": (h.get("quote") or "")[:400],
                      "title": h.get("title"), "metric": h.get("metric"), "target": h.get("target"), "comparator": h.get("comparator"),
                      "deadline": h.get("deadline"), "category": h.get("category"),
                      "auto_numbers_check": {"status": h.get("auto_status_final"), "basis": (h.get("auto_status_basis") or "")[:160],
                                             "actual": au.get("actual"), "measure": au.get("measure")},
                      "later_restatements": h["_later"], "evidence": evidence(h, sents)})
    res = {}
    for i in range(0, len(items), a.batch):
        chunk = items[i:i + a.batch]
        raw_path = os.path.join(rdir, f"batch_{i // a.batch:02d}.raw.txt")
        if os.path.exists(raw_path) and os.path.getsize(raw_path) > 0:
            raw = open(raw_path).read()
        else:
            prompt = PROMPT.format(name=a.name or sym, sym=sym, fin=fin,
                                   items="\n".join(json.dumps(x, ensure_ascii=False, default=str) for x in chunk))
            r = subprocess.run(shlex.split(a.cmd), input=prompt, capture_output=True, text=True, timeout=1200, cwd=rdir)
            raw = r.stdout
            if r.returncode != 0 or not raw.strip():
                print("batch", i, "failed", r.returncode, r.stderr[:200]); continue
            open(raw_path, "w").write(raw)
        for line in raw.splitlines():
            line = line.strip().strip(",")
            if line.startswith("{"):
                try:
                    o = json.loads(line); res[o["id"]] = o
                except (ValueError, KeyError):
                    pass
    rows = []
    for h, it in zip(hs, items):
        o = res.get(h["id"], {})
        rows.append({"id": h["id"], "sym": sym, "said_on": h["said_on"], "deadline": h.get("deadline"), "category": h.get("category"),
                     "title": h.get("title"), "target": h.get("target"), "quote": (h.get("quote") or "")[:300],
                     "chain": h["_chain"], "n_statements": h["_n_statements"], "auto": h.get("auto_status_final"),
                     "auto_basis": (h.get("auto_status_basis") or "")[:160], "llm_status": o.get("status"),
                     "actual": o.get("actual"), "evidence": o.get("evidence"), "confidence": o.get("confidence"),
                     "materiality": h.get("materiality"), "volunteered": h.get("volunteered")})
    C.write_jsonl(os.path.join(out_dir, f"{sym}_resolved.jsonl"), rows)
    from collections import Counter
    print(sym, "chain heads", len(rows), "llm", dict(Counter(r["llm_status"] for r in rows)),
          "auto", dict(Counter(r["auto"] for r in rows)))


if __name__ == "__main__":
    main()
