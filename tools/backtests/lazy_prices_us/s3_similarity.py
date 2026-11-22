#!/usr/bin/env python3
"""Step 3: similarity of each firm-year's 10-K vs the prior-year 10-K.
Measures: cosine (term frequency) and Jaccard (word sets) on full text, Item 1A, Item 7.
Output: sims.tsv (one row per firm-year; blank = missing). Usage: python3 s3_similarity.py [--procs 4]
"""
import csv, gzip, os, sys
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from common import p
from textutil import section, tf, cosine, jaccard

KEYS = ["cik", "year", "fd", "acc", "prev_acc", "float", "shares", "sic", "ticker"]


def load(acc):
    f = p("docs", acc + ".txt.gz")
    if not os.path.exists(f):
        return None
    with gzip.open(f, "rt", encoding="utf-8") as g:
        return g.read()


def work(r):
    a, b = load(r["acc"]), load(r["prev_acc"])
    out = {k: r[k] for k in KEYS}
    if not a or not b:
        out["status"] = "nodoc"; return out
    out["status"] = "ok"; out["len"] = len(a); out["prev_len"] = len(b)
    for name, ta, tb in [("full", a, b), ("1a", section(a, "1a"), section(b, "1a")), ("7", section(a, "7"), section(b, "7"))]:
        if len(ta) < 1500 or len(tb) < 1500:
            out[f"cos_{name}"] = out[f"jac_{name}"] = ""; out[f"len_{name}"] = ""
            continue
        fa, fb = tf(ta), tf(tb)
        out[f"cos_{name}"] = round(cosine(fa, fb), 6); out[f"jac_{name}"] = round(jaccard(fa, fb), 6)
        out[f"len_{name}"] = len(ta)
    return out


def main():
    rows = list(csv.DictReader(open(p("firmyears.tsv")), delimiter="\t"))
    n = int(sys.argv[sys.argv.index("--procs") + 1]) if "--procs" in sys.argv else 4
    with Pool(n) as pool:
        res = pool.map(work, rows, chunksize=8)
    cols = KEYS + ["status", "len", "prev_len"] + [f"{m}_{s}" for s in ("full", "1a", "7") for m in ("cos", "jac", "len")]
    with open(p("sims.tsv"), "w") as f:
        w = csv.DictWriter(f, cols, delimiter="\t", extrasaction="ignore"); w.writeheader()
        for r in res: w.writerow(r)
    ok = sum(r["status"] == "ok" for r in res)
    print(f"{ok}/{len(res)} firm-years with both docs", file=sys.stderr)


if __name__ == "__main__":
    main()
