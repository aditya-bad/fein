"""Shared paths and helpers for the Indian solvency back-test (Roadmap stage 2).
Reuses the screener fetcher, parser and flag functions of tools/detectors/solvency_screen.py.
Research tool, not SEBI-registered advice."""
import csv, datetime as dt, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "detectors"))
import solvency_screen as SS  # noqa: E402  (curl, cached, labels, is_financial, inputs, flags, ebit_core)
F = SS.F                      # screener table parser

CACHE = os.environ.get("BT_SOLV_IN", "/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_solv_in")
OUTDIR = os.path.join(ROOT, "research_notes", "Backtests", "solvency_india_outputs")
DEAD_CSV = os.path.join(ROOT, "research_notes", "Universe", "india_dead_companies_2026-11-22.csv")
SCREENER = "https://www.screener.in"

# pre-registered snapshots: T = 30-Sep of the year; FY0 = latest annual column ending in (T-18m, T-6m]
SNAPS = {"FY2016": dt.date(2016, 9, 30), "FY2018": dt.date(2018, 9, 30)}
MCAP_LO, MCAP_HI = 200.0, 20000.0      # Rs crore at T
WIN_YEARS = 5


def addy(d, y):
    try:
        return d.replace(year=d.year + y)
    except ValueError:
        return d.replace(year=d.year + y, day=28)


def read_csv(p):
    with open(p, newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(p, rows, cols=None):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    cols = cols or list(dict.fromkeys(k for r in rows for k in r))
    with open(p, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in cols})


def jload(p, default=None):
    try:
        with open(p) as fh:
            return json.load(fh)
    except (OSError, ValueError):
        return default


def jsave(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, default=str)
    os.replace(tmp, p)
