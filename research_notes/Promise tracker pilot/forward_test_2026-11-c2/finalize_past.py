#!/usr/bin/env python3
"""Turn <cache>/<SYM>/out/<SYM>_resolved.jsonl into past_c2.json rows (prereg s2), applying:
  * scoreable only: target not direction-only AND (specificity precise/range, or a number in the target, or a dated
    discrete-event category: new_product, capacity_commissioning, capex, approval_regulatory, m&a, customer_win);
    'vague' direction-only statements are excluded (no measurable target);
  * status: Claude's review (OVERRIDES below, id -> status or 'exclude') > LLM resolver > score.py numbers; unresolvable = excluded;
  * strict y = 1 only if delivered.
  python3 -I finalize_past.py SYM [SYM ...] --cache /root/pt_cache_c2   (rewrites past_c2.json for those symbols, keeps others)"""
import argparse, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
FINAL = ("delivered", "partly", "missed", "moved-goalpost", "withdrawn", "silently-dropped")
EVENT = {"new_product", "capacity_commissioning", "capex", "approval_regulatory", "m&a", "customer_win"}
DIRECTION = ("direction only", "direction-only", "(direction", "higher", "improve", "do well", "possible", "may ")
# Claude's review decisions (2026-11-27): id -> new status, or "exclude" (not a measurable promise / mis-extracted)
OVERRIDES = json.load(open(os.path.join(HERE, "review_overrides.json"))) if os.path.exists(os.path.join(HERE, "review_overrides.json")) else {}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("syms", nargs="+"); ap.add_argument("--cache", required=True)
    a = ap.parse_args()
    path = os.path.join(HERE, "past_c2.json")
    keep = [r for r in (json.load(open(path)) if os.path.exists(path) else []) if r["sym"] not in a.syms]
    for sym in a.syms:
        spec = {}
        for l in open(os.path.join(a.cache, sym, "out", f"{sym}_scored.jsonl")):
            p = json.loads(l); spec[p["id"]] = p.get("specificity")
        n_in = n_ex = 0
        for r in map(json.loads, open(os.path.join(a.cache, sym, "out", f"{sym}_resolved.jsonl"))):
            n_in += 1
            ov = OVERRIDES.get(r["id"])
            if ov == "exclude":
                n_ex += 1; continue
            sp = spec.get(r["id"]); tgt = (r.get("target") or "").lower()
            directional = any(d in tgt for d in DIRECTION)
            measurable = not directional and (sp in ("precise", "range") or any(ch.isdigit() for ch in tgt) or r["category"] in EVENT)
            if not measurable and not ov:
                n_ex += 1; continue
            st = ov or (r["llm_status"] if r["llm_status"] in FINAL else None)
            if st is None:
                continue
            keep.append({"sym": sym, "id": r["id"], "said_on": r["said_on"], "deadline": r["deadline"], "category": r["category"],
                         "status": st, "y": 1 if st == "delivered" else 0, "title": r["title"], "target": r["target"],
                         "evidence": (r.get("actual") or "")[:240], "basis": "claude-review" if ov else ("llm-resolver" if st == r["llm_status"] else "numbers"),
                         "auto_numbers": r["auto"], "materiality": r.get("materiality"), "volunteered": r.get("volunteered")})
        k = [x for x in keep if x["sym"] == sym]
        print(f"{sym}: chain heads {n_in}, excluded not-measurable {n_ex}, scored {len(k)}, delivered {sum(x['y'] for x in k)}")
    keep.sort(key=lambda x: (x["sym"], x["said_on"], x["id"]))
    json.dump(keep, open(path, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
