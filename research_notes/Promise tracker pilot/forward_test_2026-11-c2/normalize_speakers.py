#!/usr/bin/env python3
"""Pre-turns text fix for transcripts whose speaker names stand alone on a line (no colon), which turns.py
cannot split (e.g. INTELLECT FY24 calls). For each cached txt with < 6 'Name:' labels, a line is turned into
'Name:' if it is 1-5 capitalised words, no end punctuation, <= 40 chars, preceded by a blank line and the same
string stands alone >= 2 times in the file (or is 'Moderator'). The original is kept as <file>.orig.
Usage: python3 -I normalize_speakers.py <cache>/<SYM>/txt   (then re-run run.py --no-llm)"""
import os, re, sys
from collections import Counter

NAME = re.compile(r"^(?:(?:Mr|Ms|Mrs|Dr)\.?\s+)?[A-Z][A-Za-z\.'’\-]*(?:\s+[A-Z][A-Za-z\.'’\-]*){0,4}$")
LABEL = re.compile(r"^\s{0,8}([A-Z][A-Za-z\.\'’\-]*(?:\s+[A-Z][A-Za-z\.\'’\-]*){0,4})\s*:\s?(.*)$")
STOP = {"Thank You", "Thank you", "Thanks", "Okay", "Yes", "No", "Disclaimer", "Note", "Sub", "Page"}

def fix(path):
    src = path + ".orig" if os.path.exists(path + ".orig") else path
    lines = open(src, encoding="utf-8", errors="replace").read().split("\n")
    if sum(1 for l in lines if LABEL.match(l)) >= 6:
        return 0
    st = [l.strip() for l in lines]
    cand = Counter(s for i, s in enumerate(st) if s and len(s) <= 40 and NAME.match(s) and s not in STOP
                   and (i == 0 or st[i - 1] == ""))
    names = {s for s, n in cand.items() if n >= 2 or s.lower() == "moderator"}
    n = 0
    for i, s in enumerate(st):
        if s in names and (i == 0 or st[i - 1] == ""):
            lines[i] = s + ":"; n += 1
    if n:
        if not os.path.exists(path + ".orig"):
            os.rename(path, path + ".orig")
        open(path, "w", encoding="utf-8").write("\n".join(lines))
    return n

if __name__ == "__main__":
    d = sys.argv[1]
    for f in sorted(os.listdir(d)):
        if f.endswith(".txt"):
            k = fix(os.path.join(d, f))
            if k: print(f, "labels added:", k)
