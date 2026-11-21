"""Shared helpers for the promise-tracker pipeline (standard library only).

Paths: every stage reads/writes under a cache root:
    <cache>/<SYMBOL>/announcements.json   NSE announcement list (raw)
    <cache>/<SYMBOL>/pdf/*.pdf            transcript PDFs (untrusted data)
    <cache>/<SYMBOL>/txt/*.txt            pdftotext -layout output
    <cache>/<SYMBOL>/manifest.json        one row per call (filing date, call date, quarter, files)
    <cache>/<SYMBOL>/turns/<call>.json    speaker turns (turns.py)
    <cache>/<SYMBOL>/candidates.jsonl     candidate promise sentences (candidates.py)
    <cache>/<SYMBOL>/screener.html        screener.in consolidated page (score.py)
The cache root is --cache, else $PT_CACHE, else ~/.cache/fein_promise_tracker.
"""
import datetime as dt
import json
import os
import re

MONTHS = {m: i + 1 for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"])}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
MONTHS["sept"] = 9


def cache_root(arg=None):
    root = arg or os.environ.get("PT_CACHE") or os.path.expanduser("~/.cache/fein_promise_tracker")
    os.makedirs(root, exist_ok=True)
    return root


def sym_dir(root, symbol, *sub):
    d = os.path.join(root, symbol.upper(), *sub)
    os.makedirs(d, exist_ok=True)
    return d


def load_json(path, default=None):
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def read_jsonl(path):
    out = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def write_jsonl(path, rows):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


# ---------------------------------------------------------------- dates / fiscal calendar
# Indian fiscal year FYyy runs 1-Apr-(yy-1) .. 31-Mar-yy. Q1 = Apr-Jun ... Q4 = Jan-Mar.

def fy_end(fy):
    """FY number (2026 or 26) -> date(2026,3,31)."""
    fy = int(fy)
    if fy < 100:
        fy += 2000
    return dt.date(fy, 3, 31)


def quarter_end(q, fy):
    """Q1..Q4 of FYyy -> quarter end date."""
    fy = int(fy)
    if fy < 100:
        fy += 2000
    return {1: dt.date(fy - 1, 6, 30), 2: dt.date(fy - 1, 9, 30),
            3: dt.date(fy - 1, 12, 31), 4: dt.date(fy, 3, 31)}[int(q)]


def fy_of(d):
    """date -> fiscal year number it falls in (2026 for 2025-04-01..2026-03-31)."""
    return d.year + 1 if d.month >= 4 else d.year


def fq_of(d):
    """date -> (quarter, fy)."""
    q = {4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3, 1: 4, 2: 4, 3: 4}[d.month]
    return q, fy_of(d)


def quarter_end_of(d):
    q, fy = fq_of(d)
    return quarter_end(q, fy)


def reported_quarter_for_call(call_date):
    """Earnings call held in month m discusses the quarter that ended before it."""
    # the latest quarter that ended at least ~20 days before the call
    d = call_date - dt.timedelta(days=20)
    qe = quarter_end_of(d)
    if qe > d:
        qe = quarter_end_of(qe - dt.timedelta(days=92))
    return fq_of(qe)


def qlabel(q, fy):
    return f"Q{q}FY{int(fy) % 100:02d}"


def quarters_between(a, b):
    return (b - a).days / 91.3


DATE_PATTERNS = [
    # November 07, 2025 / Nov 7 2025
    (re.compile(r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|"
                r"Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d\d)\b", re.I),
     lambda m: (m.group(3), m.group(1), m.group(2))),
    # 7th November, 2025 / 07 Nov 2025
    (re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|"
                r"July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?),?\s+(20\d\d)\b", re.I),
     lambda m: (m.group(3), m.group(2), m.group(1))),
]


def find_dates(text):
    out = []
    for rx, f in DATE_PATTERNS:
        for m in rx.finditer(text):
            y, mon, d = f(m)
            mon = MONTHS.get(mon.lower().rstrip("."))
            try:
                out.append((m.start(), dt.date(int(y), mon, int(d))))
            except (TypeError, ValueError):
                pass
    return sorted(out)


def parse_nse_date(s):
    """'05-Nov-2026 16:51:36' -> date."""
    return dt.datetime.strptime(s.split()[0], "%d-%b-%Y").date()


def slugify(s, n=48):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n].rstrip("-") or "x"
