#!/usr/bin/env python3
"""One-shot / quarterly runner: fetch -> turns -> candidates -> LLM -> score -> report.

    python3 -I run.py SYMBOL --since 2024-07-01 [--cache DIR] [--llm-cmd "claude -p"] [--no-llm]
                      [--as-of YYYY-MM-DD] [--out DIR] [--roster "Name A,Name B"] [--tags sector-x]

Quarterly update: re-run the same command with --refresh-list; cached PDFs, text, turns and LLM
outputs are reused, so only the new call is downloaded and sent to the LLM. Human corrections go
in <out>/<SYMBOL>_overrides.jsonl as {"id": ..., "human_status": ..., "admitted_unprompted": ...}
lines; they are merged before scoring and always win.
With --no-llm the run stops after candidates.jsonl (and writes the prompts for manual LLM use).
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C  # noqa: E402
import fetch  # noqa: E402
import turns  # noqa: E402
import candidates  # noqa: E402
import llm_extract  # noqa: E402
import score  # noqa: E402
import report  # noqa: E402


def merge_overrides(promises_path, overrides_path):
    if not os.path.exists(overrides_path):
        return promises_path
    ov = {o["id"]: o for o in C.read_jsonl(overrides_path)}
    rows = C.read_jsonl(promises_path)
    for r in rows:
        if r["id"] in ov:
            r.update({k: v for k, v in ov[r["id"]].items() if k != "id"})
    merged = promises_path.replace(".jsonl", ".merged.jsonl")
    C.write_jsonl(merged, rows)
    return merged


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("symbol")
    ap.add_argument("--since", required=True)
    ap.add_argument("--cache")
    ap.add_argument("--out")
    ap.add_argument("--llm-cmd", default="claude -p")
    ap.add_argument("--no-llm", action="store_true")
    ap.add_argument("--refresh-list", action="store_true")
    ap.add_argument("--as-of")
    ap.add_argument("--roster")
    ap.add_argument("--tags", default="")
    a = ap.parse_args(argv)
    sym = a.symbol.upper()
    cache = C.cache_root(a.cache)
    out = a.out or C.sym_dir(cache, sym, "out")
    os.makedirs(out, exist_ok=True)
    co = ["--cache", cache]
    fetch.main([sym, "--since", a.since] + co + (["--refresh"] if a.refresh_list else []))
    turns.main([sym] + co + (["--roster", a.roster] if a.roster else []))
    candidates.main([sym] + co + ["--emit-prompts", os.path.join(out, "prompts")])
    if a.no_llm:
        print("stopped before the LLM step; prompts in", os.path.join(out, "prompts"))
        return
    prom = os.path.join(C.sym_dir(cache, sym), "promises.jsonl")
    llm_extract.main([sym, "--cmd", a.llm_cmd, "--out", prom] + co)
    prom = merge_overrides(prom, os.path.join(out, f"{sym}_overrides.jsonl"))
    scored = os.path.join(out, f"{sym}_scored.jsonl")
    asof = ["--as-of", a.as_of] if a.as_of else []
    score.main([sym, "--promises", prom, "--out", scored] + co + asof)
    report.main([sym, "--scored", scored, "--candour-auto", "--seed-out", os.path.join(out, f"{sym}_seed.json"),
                 "--md-out", os.path.join(out, f"{sym}_credibility.md"), "--json-out",
                 os.path.join(out, f"{sym}_summary.json"), "--company-tags", a.tags] + co + asof)


if __name__ == "__main__":
    main()
