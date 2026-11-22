"""Shared paths for the v2 hard-filter back-test on the survivorship-free Indian panel (Roadmap stage 2).
Reuses the solvency_india panel (panel.csv), its screener cache, and its weighted bootstrap (s4_analyze.stats).
Research tool, not SEBI-registered advice."""
import calendar, datetime as dt, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools", "backtests", "solvency_india"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import common as K  # noqa: E402  (solvency_india common: CACHE, SNAPS, read_csv, write_csv, jload, jsave)

CACHE2 = os.environ.get("BT_HF2", "/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_hf2")
PANEL = os.path.join(K.OUTDIR, "panel.csv")
OUT = os.path.join(ROOT, "research_notes", "Backtests", "hard_filters_india_v2_outputs")
MONTHS = {m: i for i, m in enumerate(calendar.month_name) if m}


def qtr_end(q):
    """'June 2016' -> 2016-06-30"""
    try:
        m, y = q.split()
        mi, yi = MONTHS[m], int(y)
        return dt.date(yi, mi, calendar.monthrange(yi, mi)[1])
    except (ValueError, KeyError, AttributeError):
        return None
