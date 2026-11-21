#!/usr/bin/env python3
"""Validation harness: compare pipeline output with a manual pilot ledger.

    python3 -I validate.py SYMBOL --manual memdb/seeds/2026-11-19_promises_SYMBOL.json [--cache DIR]
                          [--scored scored.jsonl] [--out validation.json] [--show-misses]

1. Candidate extraction (candidates.jsonl vs manual promise quotes):
   * locatable  = the manual quote can be found in that call's transcript text at all
   * in_mgmt    = ... inside a management turn (tests turns.py attribution)
   * recall     = located promises covered by >= 1 candidate sentence (tier A, and A+B)
   * precision  = candidates that match a manual promise / all candidates (a LOWER BOUND:
                  the pilots logged only material promises, not every forward-looking line)
   A candidate covers a quote when they share enough word 4-grams (>= 50% of the quote's
   4-grams, or >= 3), or the candidate sentence is contained in the quote.
2. Auto-scoring agreement (scored.jsonl from score.py run on the manual ledger's own
   metric/target/deadline fields): auto status vs manual status for promises the scorer
   judged auto-scorable.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def toks(s):
    s = s.lower().replace("’", "'").replace("--", " ")
    s = re.sub(r"(inr|rs\.?)\s?(\d)", r"inr \2", s)
    s = re.sub(r"(\d),(\d)", r"\1\2", s)
    return re.findall(r"[a-z0-9\.%]+", s)


def grams(t, n=4):
    return {tuple(t[i:i + n]) for i in range(len(t) - n + 1)} if len(t) >= n else {tuple(t)}


def covers(quote, sent):
    qt, st = toks(quote), toks(sent)
    if not qt or not st:
        return False
    qg, sg = grams(qt), grams(st)
    hit = len(qg & sg)
    if hit >= 3 or (qg and hit / len(qg) >= 0.5):
        return True
    # short sentence wholly inside the quote
    return len(st) >= 6 and " ".join(st) in " ".join(qt)


def quote_parts(q):
    # pilot quotes sometimes join fragments with '...'
    return [p.strip() for p in re.split(r"\.\.\.|…| -- ", q) if len(p.split()) >= 4] or [q]


def load_manual(path):
    R = [r for r in json.load(open(path)) if r["type"] == "promise"]
    return R


def nearest_call(said_on, calls):
    d = C.dt.date.fromisoformat(said_on)
    best = min(calls, key=lambda c: abs((C.dt.date.fromisoformat(c) - d).days))
    return best if abs((C.dt.date.fromisoformat(best) - d).days) <= 5 else None


def _fy_or_none(d):
    try:
        return C.fy_of(C.dt.date.fromisoformat(str(d)[:10]))
    except ValueError:
        return None


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol")
    p.add_argument("--manual", required=True)
    p.add_argument("--cache")
    p.add_argument("--scored")
    p.add_argument("--out")
    p.add_argument("--show-misses", action="store_true")
    p.add_argument("--llm", help="scored.jsonl produced from the LLM promises (score.py --promises)")
    a = p.parse_args(argv)
    sym = a.symbol.upper()
    root = C.cache_root(a.cache)
    man = load_manual(a.manual)
    cands = C.read_jsonl(os.path.join(root, sym, "candidates.jsonl"))
    turns = {os.path.basename(f)[:-5]: C.load_json(f) for f in glob.glob(os.path.join(root, sym, "turns", "*.json"))}
    by_call = {}
    for c in cands:
        by_call.setdefault(c["call_date"], []).append(c)

    res = {"symbol": sym, "n_manual": len(man), "n_candidates": len(cands),
           "n_candidates_A": sum(c["tier"] == "A" for c in cands), "calls": len(turns)}
    located = in_mgmt = 0
    rec_a = rec_ab = 0
    matched_cands = set()
    misses = []
    per_promise = []
    for r in man:
        d = r["data"]
        call = nearest_call(d["said_on"], list(turns))
        parts = quote_parts(d["quote"])
        loc = mg = False
        if call:
            for t in turns[call]["turns"]:
                for s in re.split(r"(?<=[\.\?!])\s+", t["text"]):
                    if any(covers(q, s) for q in parts):
                        loc = True
                        mg = mg or t["role"] == "management"
        hits = [c for c in by_call.get(call, []) if any(covers(q, c["sentence"]) for q in parts)]
        for c in hits:
            matched_cands.add(c["id"])
        ha = any(c["tier"] == "A" for c in hits)
        located += loc
        in_mgmt += mg
        if loc:
            rec_ab += bool(hits)
            rec_a += ha
        if loc and not hits:
            misses.append((r["id"], d["quote"][:200]))
        per_promise.append({"id": r["id"], "located": loc, "in_mgmt_turn": mg, "hit_A": ha, "hit_any": bool(hits),
                            "volunteered_manual": d.get("volunteered") in (True, "volunteered"),
                            "volunteered_auto": (hits[0]["volunteered"] if hits else None),
                            "category": d.get("category")})
    res.update({
        "located_in_transcript": located, "located_in_management_turn": in_mgmt,
        "recall_A": round(rec_a / located, 3) if located else None,
        "recall_AB": round(rec_ab / located, 3) if located else None,
        "precision_lower_bound_AB": round(len(matched_cands) / len(cands), 3) if cands else None,
        "precision_lower_bound_A": round(len({c["id"] for c in cands if c["tier"] == "A"} & matched_cands)
                                         / max(1, res["n_candidates_A"]), 3),
        "candidates_per_call": round(len(cands) / max(1, len(turns)), 1),
        "manual_promises_per_call": round(len(man) / max(1, len(turns)), 1),
    })
    vv = [x for x in per_promise if x["hit_any"]]
    res["volunteered_flag_agreement"] = round(sum(x["volunteered_manual"] == x["volunteered_auto"] for x in vv)
                                              / len(vv), 3) if vv else None
    cats = Counter()
    hitc = Counter()
    for x in per_promise:
        if x["located"]:
            cats[x["category"]] += 1
            hitc[x["category"]] += x["hit_any"]
    res["recall_by_category"] = {k: f"{hitc[k]}/{v}" for k, v in sorted(cats.items())}
    res["unlocated_ids"] = [x["id"] for x in per_promise if not x["located"]]

    if a.scored:
        sc = {r["id"]: r for r in C.read_jsonl(a.scored)}
        mstat = {r["id"]: r["data"]["status"] for r in man}
        rows = []
        for pid, r in sc.items():
            au = r.get("auto")
            if not au or au.get("status") in (None, "not-auto-scorable"):
                continue
            rows.append((pid, mstat.get(pid), r.get("auto_status_final") or au["status"], au.get("actual"),
                         au.get("measure")))
        def norm(s):
            return {"partially_delivered": "partly", "moved_goalpost": "moved-goalpost"}.get(s, s)
        exact = sum(norm(m) == norm(x) for _, m, x, _, _ in rows)
        pos = {"delivered": 1, "partly": 0.5, "missed": -1, "moved-goalpost": -1, "silently-dropped": -1,
               "withdrawn": -1, "pending": None, "unverifiable": None}
        direction = sum((pos.get(norm(m)) is not None and pos.get(norm(x)) is not None
                         and (pos[norm(m)] > 0) == (pos[norm(x)] > 0)) or norm(m) == norm(x) for _, m, x, _, _ in rows)
        resolved = [x for x in rows if norm(x[1]) not in ("pending", "unverifiable") and norm(x[2]) not in ("pending", "awaiting-data")]
        ex_res = sum(norm(m) == norm(x) for _, m, x, _, _ in resolved)
        dir_res = sum((pos.get(norm(m)) or 0) > 0 and (pos.get(norm(x)) or 0) > 0 or
                      (pos.get(norm(m)) or 0) <= 0 and (pos.get(norm(x)) or 0) <= 0 for _, m, x, _, _ in resolved)
        # goalpost detection over ALL promises (chain rule works for non-financial ones too)
        mg = {pid for pid, s_ in mstat.items() if s_ == "moved-goalpost"}
        ag = {pid for pid, r in sc.items() if r.get("auto_status_final") == "moved-goalpost"}
        res["goalposts"] = {"manual_moved_goalpost": len(mg), "auto_moved_goalpost": len(ag),
                            "both": len(mg & ag), "auto_only": sorted(ag - mg), "manual_only": sorted(mg - ag),
                            "goalpost_moves_counted": sum(1 for r in sc.values() if r.get("chain", {}).get("goalpost_move")),
                            "restatements_linked": sum(1 for r in sc.values() if r.get("chain", {}).get("restates"))}
        num_rows = [(pid, mstat.get(pid), sc[pid]["auto"]["status"]) for pid, *_ in rows]
        num_res = [x for x in num_rows if norm(x[1]) not in ("pending", "unverifiable") and x[2] not in ("pending", "awaiting-data")]
        res["autoscore_numbers_only"] = {
            "resolved_both": len(num_res),
            "exact": f"{sum(norm(m) == x for _, m, x in num_res)}/{len(num_res)}",
            "confusion": Counter(f"{norm(m)} -> {x}" for _, m, x in num_res).most_common()}
        res["autoscore"] = {
            "resolved_both": len(resolved), "resolved_exact_agreement": f"{ex_res}/{len(resolved)}",
            "resolved_direction_agreement": f"{dir_res}/{len(resolved)}",
            "n_manual_promises": len(man), "n_auto_scorable": len(rows),
            "coverage": round(len(rows) / len(man), 3),
            "exact_status_agreement": f"{exact}/{len(rows)}",
            "direction_agreement": f"{direction}/{len(rows)}",
            "confusion": Counter(f"{norm(m)} -> {norm(x)}" for _, m, x, _, _ in rows).most_common(),
            "disagreements": [{"id": pid, "manual": m, "auto": x, "actual": act, "measure": me}
                              for pid, m, x, act, me in rows if norm(m) != norm(x)],
        }
    if a.llm:
        L = C.read_jsonl(a.llm)
        mstat = {r["id"]: r["data"]["status"] for r in man}
        used = set()
        pairs = []
        for r in man:
            d = r["data"]
            parts = quote_parts(d["quote"])
            hit = [x for x in L if abs((C.dt.date.fromisoformat(x["said_on"]) - C.dt.date.fromisoformat(d["said_on"])).days) <= 5
                   and any(covers(q, x["quote"]) or covers(x["quote"], q) for q in parts)]
            if hit:
                pairs.append((r, hit[0]))
                used.update(h["id"] for h in hit)
        def norm(s):
            return {"partially_delivered": "partly", "moved_goalpost": "moved-goalpost"}.get(s, s)
        agree = [(r["id"], norm(mstat[r["id"]]), x.get("auto_status_final")) for r, x in pairs
                 if x.get("auto_status_final") not in (None, "not-auto-scorable")]
        res_ag = [t for t in agree if t[1] not in ("pending", "unverifiable") and t[2] not in ("pending", "awaiting-data")]
        fields = Counter()
        for r, x in pairs:
            d = r["data"]
            fields["category"] += d.get("category") == x.get("category")
            fields["deadline_same_fy"] += bool(_fy_or_none(d.get("deadline")) is not None and
                                               _fy_or_none(d.get("deadline")) == _fy_or_none(x.get("deadline")))
            fields["volunteered"] += (d.get("volunteered") in (True, "volunteered")) == bool(x.get("volunteered"))
            fields["specificity"] += bool(d.get("specificity") == x.get("specificity") or
                                          {3: "precise", 2: "range", 1: "vague"}.get(d.get("specificity_score")) == x.get("specificity"))
        res["llm"] = {
            "n_llm_promises": len(L), "manual_matched": len(pairs),
            "recall_vs_manual": round(len(pairs) / len(man), 3),
            "precision_lower_bound": round(len(used) / max(1, len(L)), 3),
            "field_agreement_on_matched": {k: f"{v}/{len(pairs)}" for k, v in fields.items()},
            "auto_scored_matched": len(agree),
            "auto_resolved_both": len(res_ag),
            "auto_exact_agreement": f"{sum(m == x for _, m, x in res_ag)}/{len(res_ag)}",
            "auto_confusion": Counter(f"{m} -> {x}" for _, m, x in res_ag).most_common(),
            "auto_disagreements": [t for t in res_ag if t[1] != t[2]],
            "llm_unmatched_sample": [x["title"] for x in L if x["id"] not in used][:25],
        }
    print(json.dumps({k: v for k, v in res.items() if k != "unlocated_ids"}, indent=1, ensure_ascii=False))
    if a.show_misses:
        print("\nMISSED (located but no candidate):")
        for pid, q in misses:
            print(" ", pid, "|", q)
        print("\nUNLOCATED:", res["unlocated_ids"])
    if a.out:
        res["per_promise"] = per_promise
        res["missed"] = misses
        C.save_json(a.out, res)


if __name__ == "__main__":
    main()
