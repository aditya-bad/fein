#!/usr/bin/env python3
"""Step 2: download each needed 10-K primary document (current + prior year), strip HTML/iXBRL,
save plain text gzipped under docs/<acc>.txt.gz. Raw HTML is not kept. ~4 req/s total to SEC.
Failures logged in docs_fail.tsv. Usage: python3 s2_docs.py [--workers 3]
"""
import csv, gzip, os, sys, threading
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(__file__))
from common import p, sec_raw
from textutil import html_to_text

lock = threading.Lock()


def job(cik, acc, doc, fail):
    out = p("docs", acc + ".txt.gz")
    if os.path.exists(out):
        return 0
    url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/{doc}"
    try:
        b = sec_raw(url)
    except Exception as e:
        b = None; why = str(e)[:60]
    else:
        why = "404"
    if not b:
        with lock:
            fail.write(f"{cik}\t{acc}\t{doc}\t{why}\n"); fail.flush()
        return 1
    t = html_to_text(b)
    with gzip.open(out + ".tmp", "wt", encoding="utf-8") as f:
        f.write(t)
    os.replace(out + ".tmp", out)
    return 0


def main():
    os.makedirs(p("docs"), exist_ok=True)
    need = {}
    for r in csv.DictReader(open(p("firmyears.tsv")), delimiter="\t"):
        need[r["acc"]] = (r["cik"], r["doc"]); need[r["prev_acc"]] = (r["cik"], r["prev_doc"])
    print("docs needed", len(need), file=sys.stderr, flush=True)
    fail = open(p("docs_fail.tsv"), "a")
    w = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 3
    done = [0]
    def run(item):
        acc, (cik, doc) = item
        job(cik, acc, doc, fail)
        done[0] += 1
        if done[0] % 250 == 0:
            print(done[0], file=sys.stderr, flush=True)
    with ThreadPoolExecutor(w) as ex:
        list(ex.map(run, sorted(need.items())))
    print("done", file=sys.stderr)


if __name__ == "__main__":
    main()
