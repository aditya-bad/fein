"""Dump every sentence with a broad forward marker from an AR's front half (before the CG report/auditor's report),
for a HAND read. Independent of ar_sections' zone/boilerplate rules (only the column splitter is shared)."""
import re, sys
sys.path.insert(0, "/home/user/fein/tools/promise_tracker/pipeline")
import ar_sections as A
txt, stop = sys.argv[1], sys.argv[2]
t = open(txt).read()
lines = []
for pg in t.split("\f"):
    lines += A.split_columns(pg)
end = next(i for i, l in enumerate(lines) if re.search(stop, l))
text = re.sub(r"\s+", " ", " ".join(lines[:end]))
FW = re.compile(r"\b(will|shall|expect\w*|plan\w*|aim\w*|target\w*|going forward|outlook|propos\w*|intend\w*|likely|"
                r"next|future|upcoming|commission\w*|expan\w*|launch\w*|anticipat\w*|envisag\w*|endeavou?r|strive|"
                r"poised|road ?map|vision|goal|by FY|by 20\d\d|coming)\b", re.I)
n = 0
for s in re.split(r"(?<=[\.\?!])\s+(?=[A-Z“\"'(•])", text):
    if FW.search(s) and 6 <= len(s.split()) <= 120:
        n += 1
        print(f"[{n}] {s}")
