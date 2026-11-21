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


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("symbol")
    p.add_argument("--manual", required=True)
    p.add_argument("--cache")
    p.add_argument("--scored")
    p.add_argument("--out")
    p.add_argument("--show-misses", action="store_true")
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
            rows.append((pid, mstat.get(pid), au["status"], au.get("actual"), au.get("measure")))
        def norm(s):
            return {"partially_delivered": "partly", "moved_goalpost": "moved-goalpost"}.get(s, s)
        exact = sum(norm(m) == norm(x) for _, m, x, _, _ in rows)
        pos = {"delivered": 1, "partly": 0.5, "missed": -1, "moved-goalpost": -1, "silently-dropped": -1,
               "withdrawn": -1, "pending": None, "unverifiable": None}
        direction = sum((pos.get(norm(m)) is not None and pos.get(norm(x)) is not None
                         and (pos[norm(m)] > 0) == (pos[norm(x)] > 0)) or norm(m) == norm(x) for _, m, x, _, _ in rows)
        res["autoscore"] = {
            "n_manual_promises": len(man), "n_auto_scorable": len(rows),
            "coverage": round(len(rows) / len(man), 3),
            "exact_status_agreement": f"{exact}/{len(rows)}",
            "direction_agreement": f"{direction}/{len(rows)}",
            "confusion": Counter(f"{norm(m)} -> {norm(x)}" for _, m, x, _, _ in rows).most_common(),
            "disagreements": [{"id": pid, "manual": m, "auto": x, "actual": act, "measure": me}
                              for pid, m, x, act, me in rows if norm(m) != norm(x)],
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
