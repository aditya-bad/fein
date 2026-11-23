#!/usr/bin/env python3
"""Regression check: concall-mode outputs are unchanged versus a reference git revision.

    python3 -I regress_concall.py --ref 5c15082 --cache CONCALL_CACHE [--symbols SONACOMS,UNIPARTS] [--work DIR]

Added with AR mode (v1.4). AR mode only ADDS files (ar_fetch.py, ar_sections.py, ar_run.py) and keeps its own
cache root, so the concall pipeline must give byte-identical results. This script proves it on cached data:
  1. extracts the reference pipeline (`git show REF:tools/promise_tracker/pipeline/*`) into <work>/ref/;
  2. for each symbol, copies <cache>/<SYMBOL>/ (manifest, txt, screener page, fin.csv) into two fresh caches;
  3. runs turns.py -> candidates.py -> score.py -> report.py with the reference code and with the current code
     (score: the symbol's promises from memdb/seeds/*promises*.json via --seed, --no-screener plus fin.csv when
     present, so no network is touched and the run is deterministic);
  4. compares every output (turns/*.json, candidates.jsonl, scored.jsonl, seed JSON, summary JSON, markdown).
  5. also compares score.infer_measure / parse_target on every promise in memdb/seeds/*promises*.json.
Exit code 0 = identical; 1 = differences (listed).
"""
import argparse
import filecmp
import glob
import importlib.util
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
REL = "tools/promise_tracker/pipeline"


def extract_ref(ref, dst):
    os.makedirs(dst, exist_ok=True)
    names = subprocess.run(["git", "-C", REPO, "ls-tree", "--name-only", ref, REL + "/"], check=True,
                           capture_output=True, text=True).stdout.split()
    for n in names:
        if n.endswith((".py", ".md")):
            data = subprocess.run(["git", "-C", REPO, "show", f"{ref}:{n}"], check=True, capture_output=True).stdout
            open(os.path.join(dst, os.path.basename(n)), "wb").write(data)
    return dst


def seed_for(sym, out):
    recs = []
    for f in sorted(glob.glob(os.path.join(REPO, "memdb", "seeds", "*promises*.json"))):
        for r in json.load(open(f)):
            if r.get("type") == "promise" and sym in (r.get("tickers") or []):
                recs.append(r)
    json.dump(recs, open(out, "w"))
    return len(recs)


def run_chain(code, cache, sym, out, seed, fin_csv, as_of):
    py = [sys.executable, "-I"]
    co = ["--cache", cache]
    subprocess.run(py + [os.path.join(code, "turns.py"), sym] + co, check=True, capture_output=True)
    subprocess.run(py + [os.path.join(code, "candidates.py"), sym] + co, check=True, capture_output=True)
    sc = [os.path.join(code, "score.py"), sym, "--seed", seed, "--no-screener", "--as-of", as_of,
          "--out", os.path.join(out, "scored.jsonl")] + co + (["--csv", fin_csv] if fin_csv else [])
    subprocess.run(py + sc, check=True, capture_output=True)
    subprocess.run(py + [os.path.join(code, "report.py"), sym, "--scored", os.path.join(out, "scored.jsonl"),
                         "--as-of", as_of, "--candour-auto", "--seed-out", os.path.join(out, "seed.json"),
                         "--json-out", os.path.join(out, "summary.json"), "--md-out", os.path.join(out, "report.md")] + co,
                   check=True, capture_output=True)


def load_mod(path, name):
    sys.path.insert(0, os.path.dirname(path))
    try:
        for m in ("common", "financials", "score"):
            sys.modules.pop(m, None)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        sys.path.pop(0)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", default="HEAD", help="reference git revision (use the last pre-AR-mode commit)")
    ap.add_argument("--cache", required=True, help="an existing concall cache root (read only; it is copied)")
    ap.add_argument("--symbols", help="comma list (default: every symbol in the cache with turns/txt)")
    ap.add_argument("--work", default=None)
    ap.add_argument("--as-of", default="2026-11-22")
    a = ap.parse_args(argv)
    work = a.work or os.path.join(a.cache, "..", "_regress_concall")
    shutil.rmtree(work, ignore_errors=True)
    ref = extract_ref(a.ref, os.path.join(work, "ref"))
    syms = a.symbols.split(",") if a.symbols else sorted(
        d for d in os.listdir(a.cache) if os.path.exists(os.path.join(a.cache, d, "manifest.json")))
    bad = []
    for sym in syms:
        seed = os.path.join(work, f"{sym}_seed_in.json")
        n = seed_for(sym, seed)
        outs = {}
        for tag, code in (("ref", ref), ("new", HERE)):
            cache = os.path.join(work, tag + "_cache")
            dst = os.path.join(cache, sym)
            shutil.copytree(os.path.join(a.cache, sym), dst, ignore=shutil.ignore_patterns("pdf", "turns", "out", "llm"))
            man = json.load(open(os.path.join(dst, "manifest.json")))   # point txt paths at the copy
            for m in man:
                m["txt"] = os.path.join(dst, "txt", os.path.basename(m["txt"]))
            json.dump(man, open(os.path.join(dst, "manifest.json"), "w"))
            out = os.path.join(work, tag + "_out", sym)
            os.makedirs(out, exist_ok=True)
            fin = os.path.join(dst, "fin.csv")
            run_chain(code, cache, sym, out, seed, fin if os.path.exists(fin) else None, a.as_of)
            outs[tag] = (cache, out)
        files = ["candidates.jsonl"] + [os.path.join("turns", os.path.basename(f)) for f in
                                        sorted(glob.glob(os.path.join(outs["new"][0], sym, "turns", "*.json")))]
        diffs = [f for f in files if not filecmp.cmp(os.path.join(outs["ref"][0], sym, f),
                                                     os.path.join(outs["new"][0], sym, f), shallow=False)]
        diffs += [f for f in ("scored.jsonl", "seed.json", "summary.json", "report.md")
                  if not filecmp.cmp(os.path.join(outs["ref"][1], f), os.path.join(outs["new"][1], f), shallow=False)]
        nc = sum(1 for _ in open(os.path.join(outs["new"][0], sym, "candidates.jsonl")))
        print(f"{sym}: {len(files) - 1} calls, {nc} candidates, {n} seed promises scored -> "
              + ("IDENTICAL" if not diffs else "DIFFERENT: " + ", ".join(diffs)))
        bad += [(sym, d) for d in diffs]
    # measure / target parsing on every seeded promise
    old = load_mod(os.path.join(ref, "score.py"), "score_ref")
    new = load_mod(os.path.join(HERE, "score.py"), "score_new")
    n = changed = 0
    for f in sorted(glob.glob(os.path.join(REPO, "memdb", "seeds", "*promises*.json"))):
        for r in json.load(open(f)):
            if r.get("type") != "promise":
                continue
            d = dict(r["data"], id=r["id"], title=r.get("title"))
            n += 1
            if (old.infer_measure(d), old.parse_target(d.get("target")) if d.get("target") else None) != \
                    (new.infer_measure(d), new.parse_target(d.get("target")) if d.get("target") else None):
                changed += 1
    print(f"seed promises: {n}; infer_measure/parse_target changed: {changed}")
    if changed:
        bad.append(("seeds", f"{changed} changed"))
    print("ALL IDENTICAL" if not bad else f"REGRESSION: {bad}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
