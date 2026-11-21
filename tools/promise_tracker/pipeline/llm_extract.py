#!/usr/bin/env python3
"""Stage 3b: run the LLM confirmation step over candidates.jsonl, call by call.

    python3 -I llm_extract.py SYMBOL [--cmd "claude -p"] [--calls 2025-11-07,2026-01-29]
                              [--cache DIR] [--out promises.jsonl] [--workdir DIR] [--timeout 900]

* Builds the prompt for each call from llm_extract_prompt.md (+ that call's candidates).
* Calls are processed oldest first; chain_keys produced so far are fed into the next prompt
  so the same target keeps the same key across calls (this is what makes the supersedes-chain
  reliable for non-financial promises like commissioning dates).
* The command gets the prompt on STDIN and must print JSON Lines. Tested with `claude -p`;
  `gemini -p ""` (Gemini CLI, non-interactive) should work the same way on the Pi.
* Raw model output is kept in <cache>/<SYMBOL>/llm/<call>.raw.txt; parsed promises are validated,
  given ids (promise:SYMBOL:<said_on>:<slug>) and appended to --out (default
  <cache>/<SYMBOL>/promises.jsonl), replacing earlier output for the same call.
* Run from a neutral --workdir (default: the cache dir) so the CLI does not pick up repo instructions.
"""
import argparse
import json
import os
import re
import shlex
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402
import candidates as K  # noqa: E402

REQUIRED = ("quote", "category", "metric", "deadline_precision", "specificity")
CATS = {"revenue_growth", "margin", "capex", "capacity_commissioning", "order_inflow", "order_book", "debt_reduction",
        "working_capital", "new_product", "approval_regulatory", "customer_win", "m&a", "dividend_payout",
        "fundraise", "other"}


def parse_output(txt):
    out, bad = [], 0
    for line in txt.splitlines():
        line = line.strip().strip(",")
        if not line.startswith("{"):
            continue
        try:
            out.append(json.loads(line))
        except ValueError:
            bad += 1
    if not out:  # model returned a JSON array instead of JSONL
        m = re.search(r"\[\s*\{.*\}\s*\]", txt, re.S)
        if m:
            try:
                out = json.loads(m.group(0))
            except ValueError:
                pass
    return out, bad


def clean(p, sym, call, cands_by_id):
    for k in REQUIRED:
        if not p.get(k):
            return None
    p["said_on"] = call
    if p.get("category") not in CATS:
        p["category"] = "other"
    if p.get("specificity") not in ("precise", "range", "vague"):
        p["specificity"] = "vague"
    try:
        p["materiality"] = max(1, min(3, int(p.get("materiality") or 2)))
    except (TypeError, ValueError):
        p["materiality"] = 2
    ids = [i for i in (p.get("source_candidate_ids") or []) if i in cands_by_id]
    if ids:
        c = cands_by_id[ids[0]]
        p.setdefault("speaker", c["speaker"])
        p["source_url"] = c.get("source_url")
        if "volunteered" not in p or p["volunteered"] is None:
            p["volunteered"] = c["volunteered"]
    p["volunteered"] = bool(p.get("volunteered"))
    p["extracted_by"] = "rules+llm"
    p["status"] = p.get("status")  # left for human / score.py
    return p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--cmd", default="claude -p")
    ap.add_argument("--calls")
    ap.add_argument("--cache")
    ap.add_argument("--out")
    ap.add_argument("--workdir")
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args(argv)
    sym = a.symbol.upper()
    root = C.cache_root(a.cache)
    sdir = C.sym_dir(root, sym)
    ldir = C.sym_dir(root, sym, "llm")
    cands = C.read_jsonl(os.path.join(sdir, "candidates.jsonl"))
    by_id = {c["id"]: c for c in cands}
    by_call = {}
    for c in cands:
        by_call.setdefault(c["call_date"], []).append(c)
    calls = sorted(by_call)
    if a.calls:
        want = set(a.calls.split(","))
        calls = [c for c in calls if c in want]
    out_path = a.out or os.path.join(sdir, "promises.jsonl")
    existing = C.read_jsonl(out_path) if os.path.exists(out_path) else []
    known = {p["chain_key"]: p.get("title", "") for p in existing if p.get("chain_key")}
    for call in calls:
        prompt = K.build_prompt(sym, call, by_call[call], known)
        raw_path = os.path.join(ldir, f"{call}.raw.txt")
        if os.path.exists(raw_path) and os.path.getsize(raw_path) > 0:
            raw = open(raw_path).read()
            print(call, "cached LLM output")
        else:
            r = subprocess.run(shlex.split(a.cmd), input=prompt, capture_output=True, text=True,
                               timeout=a.timeout, cwd=a.workdir or ldir)
            raw = r.stdout
            if r.returncode != 0 or not raw.strip():
                print(call, "LLM command failed:", r.returncode, r.stderr[:300])
                continue
            open(raw_path, "w").write(raw)
        ps, bad = parse_output(raw)
        got = []
        seen = set()
        for p in ps:
            p = clean(p, sym, call, by_id)
            if not p:
                bad += 1
                continue
            slug = C.slugify(p.get("title") or p["metric"], 40)
            pid = f"promise:{sym}:{call}:{slug}"
            n = 2
            while pid in seen:
                pid = f"promise:{sym}:{call}:{slug}-{n}"
                n += 1
            seen.add(pid)
            p["id"] = pid
            got.append(p)
            if p.get("chain_key"):
                known.setdefault(p["chain_key"], p.get("title", ""))
        existing = [e for e in existing if e["said_on"] != call] + got
        C.write_jsonl(out_path, sorted(existing, key=lambda x: (x["said_on"], x["id"])))
        print(f"{call}: {len(by_call[call])} candidates -> {len(got)} promises ({bad} unparsable/invalid)")
    print("wrote", out_path)


if __name__ == "__main__":
    main()
