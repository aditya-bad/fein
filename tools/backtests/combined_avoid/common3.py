"""Shared paths/helpers for the combined PEAD-avoid x stage-2 red-flag test (Roadmap stages 2+3).
Pre-registration: research_notes/Backtests/combined_avoid_india.md. Research tool, not SEBI-registered advice.
Reuses: india_pead_survivorship (events_w.tsv, groups/boot), hard_filters_v2 (pledge_from), solvency_india (cut),
tools/detectors/solvency_screen (inputs/flags/fetch), tools/bse_fetch (BSE API)."""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SCR = "/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad"
SURV = os.path.join(SCR, "bt_pead_surv")
SOLV = os.path.join(SCR, "bt_solv_in")
HF2 = os.path.join(SCR, "bt_hf2")
OUT = os.environ.get("BT_COMB", os.path.join(SCR, "bt_comb"))
REPORT_OUT = os.path.join(ROOT, "research_notes", "Backtests", "combined_avoid_outputs")
for p in ("tools", "tools/detectors", "tools/backtests/india_pead_survivorship", "tools/backtests/hard_filters_v2",
          "tools/backtests/solvency_india"):
    sys.path.insert(0, os.path.join(ROOT, p))


def jl(p, d=None):
    try: return json.load(open(p))
    except Exception: return d


def js(p, o):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(o, open(p + ".tmp", "w"), default=str); os.replace(p + ".tmp", p)


def event_symbols():
    syms = []
    for r in csv.DictReader(open(os.path.join(SURV, "events_w.tsv")), delimiter="\t"):
        if r["sym"] not in syms: syms.append(r["sym"])
    return syms


def id_maps():
    """symbol -> {isin, bse_code, slug, cid} from caches only (no network)."""
    out = {}
    isin = {r["SYMBOL"]: r[" ISIN NUMBER"].strip() for r in csv.DictReader(open(os.path.join(SOLV, "nse_equity_l.csv")))}
    bse_by_isin = {x["ISIN_NUMBER"]: x["SCRIP_CD"] for x in jl(os.path.join(SOLV, "bse_active.json"), []) if x.get("ISIN_NUMBER")}
    frame = list(csv.DictReader(open(os.path.join(SOLV, "frame.csv"))))
    st = jl(os.path.join(SOLV, "fetch_status.json"), {})
    by = {}
    for r in frame:
        s = st.get(r["key"], {})
        rec = {"bse_code": r["bse_code"], "isin": r["isin"]}
        if s.get("page") == "ok" and s.get("cid"): rec.update(slug=s["slug"], cid=s["cid"], dir=os.path.join(SOLV, "sc", s["slug"]))
        for k in (r["nse_symbol"], r["isin"], r["bse_code"]):
            if k: by.setdefault(k, rec)
    miss = {r["symbol"]: r for r in csv.DictReader(open(os.path.join(SURV, "missing.csv")))}
    ss = jl(os.path.join(SURV, "status_screener.json"), {})
    for sym in event_symbols():
        m = miss.get(sym, {})
        i = isin.get(sym) or m.get("isin") or ""
        rec = dict(by.get(sym) or by.get(i) or {})
        rec["isin"] = i or rec.get("isin", "")
        rec["bse_code"] = rec.get("bse_code") or m.get("bse_code") or bse_by_isin.get(i, "")
        if sym in ss and ss[sym].get("cid") and "cid" not in rec:
            src = ss[sym]; d = os.path.join(SOLV if src.get("src") == "solv_cache" else SURV, "sc", src["slug"])
            rec.update(slug=src["slug"], cid=src["cid"], dir=d)
        out[sym] = rec
    return out


def _pin_solvency_common():
    """solvency_india / hard_filters_v2 modules do `import common as K` and expect solvency_india/common.py;
    pin that module under the name 'common' so other same-named modules on sys.path cannot shadow it."""
    import importlib.util
    if "common" in sys.modules and hasattr(sys.modules["common"], "SS"): return
    sp = importlib.util.spec_from_file_location("common", os.path.join(ROOT, "tools", "backtests", "solvency_india", "common.py"))
    m = importlib.util.module_from_spec(sp); sys.modules["common"] = m; sp.loader.exec_module(m)


_pin_solvency_common()
