"""Shared paths/helpers for the PEAD survivorship check (Roadmap stage 3).
Pre-registration: research_notes/Backtests/india_pead_survivorship.md. Research tool, not SEBI-registered advice.
Reuses tools/backtests/india_pead (v1 NSE fetch/parse code) and tools/backtests/solvency_india (screener charts)."""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SCR = "/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad"
V1 = os.environ.get("BT_PEAD", os.path.join(SCR, "bt_pead"))          # v1 cache (live sample, daily Yahoo)
SOLV = os.environ.get("BT_SOLV_IN", os.path.join(SCR, "bt_solv_in"))   # screener cache (dead firms' charts)
OUT = os.environ.get("BT_PEAD_SURV", os.path.join(SCR, "bt_pead_surv"))
REPORT_OUT = os.path.join(ROOT, "research_notes", "Backtests", "india_pead_survivorship_outputs")
sys.path.insert(0, os.path.join(ROOT, "tools", "backtests", "india_pead"))
sys.path.insert(0, os.path.join(ROOT, "tools"))
GAP = 1.5   # one stream, >= 1.5 s between requests to any host


class _Shared(dict):
    """last-request clock shared by every host key -> one polite stream."""
    t = [0.0]
    def __getitem__(self, k): return self.t[0]
    def __setitem__(self, k, v): self.t[0] = v


def single_stream(mod):
    """Patch a v1/v2 fetch module (GAP/last/locks dicts) so all hosts share one >=1.5 s clock and lock."""
    import threading
    lk = threading.Lock()
    for k in list(mod.GAP): mod.GAP[k] = GAP
    mod.last = _Shared()
    mod.locks = {k: lk for k in mod.GAP}
