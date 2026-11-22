#!/usr/bin/env python3
"""Step 4b: firm-years whose CIK has no current ticker in EDGAR (mostly acquired / delisted firms):
read the trading symbol from the 10-K cover page ("Trading Symbol(s)" table) and write
old_tickers.tsv (acc -> symbol). Then fetch those via s4_prices.py. A recovered ticker is only used
if the market-cap identity check in s5 passes (guards against ticker reuse).
"""
import csv, gzip, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import p

SYM = re.compile(r"^([A-Z]{1,5}(?:[\.\-][A-Z]{1,2})?)\s*$")
BAD = {"NYSE", "LLC", "NONE", "NA", "N", "INC", "THE", "AND", "OTC", "USD", "II", "III", "LP"}


def symbol(text):
    i = text.find("Trading Symbol")
    if i < 0:
        i = text.lower().find("trading symbol")
    if i < 0 or i > 40000:
        return ""
    for line in text[i:i + 3000].split("\n")[1:40]:
        m = SYM.match(line.strip())
        if m and m.group(1) not in BAD:
            return m.group(1)
    return ""


def main():
    out = []
    for r in csv.DictReader(open(p("firmyears.tsv")), delimiter="\t"):
        if r["ticker"]:
            continue
        f = p("docs", r["acc"] + ".txt.gz")
        if not os.path.exists(f):
            continue
        with gzip.open(f, "rt", encoding="utf-8") as g:
            s = symbol(g.read(60000))
        out.append((r["acc"], r["cik"], s))
    with open(p("old_tickers.tsv"), "w") as f:
        f.write("acc\tcik\tsymbol\n")
        for row in out: f.write("\t".join(row) + "\n")
    syms = sorted({s for _, _, s in out if s})
    open(p("old_tickers.txt"), "w").write("\n".join(syms) + "\n")
    print(f"{len(out)} no-ticker firm-years, {sum(1 for x in out if x[2])} symbols found, {len(syms)} unique", file=sys.stderr)


if __name__ == "__main__":
    main()
