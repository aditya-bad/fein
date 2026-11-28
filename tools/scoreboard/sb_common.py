"""Shared helpers for the paper-call scoreboard (standard library only; runs on a Raspberry Pi).

Stage 7 (scorekeeping) of memory/roadmap.md. Used by calls.py, resolve.py and scoreboard.py.
Research tooling, not SEBI-registered advice.
"""
from __future__ import annotations

import datetime as dt
import glob
import hashlib
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import gzip

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT_DIR = os.path.join(REPO, "research_notes", "Scoreboard")
SEEDS_DIR = os.path.join(REPO, "memdb", "seeds")
CURRICULUM = os.path.join(REPO, "memory", "curriculum.md")
SPECS_FILE = os.path.join(HERE, "specs.json")
STATE_DIR = os.path.join(HERE, "state")
SEED_GLOB = "*_scoreboard_resolutions*.json"
CACHE = os.environ.get("SB_CACHE") or os.path.join(
    os.environ.get("XDG_CACHE_HOME", os.path.expanduser("~/.cache")), "fein_scoreboard")
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
VERSION = "scoreboard v1 (2026-11-22)"

METHOD_MAP = {
    "promise-tracker credibility": "promise-tracker", "promise-tracker": "promise-tracker",
    "management-tone-vs-delivery": "mgmt-tone", "mgmt-tone": "mgmt-tone",
    "sector cycle/lead indicator": "sector-cycle", "sector-cycle": "sector-cycle",
    "base rate": "base-rate", "base-rate": "base-rate",
    "flags-judgment context": "flags-judgment", "flags-judgment": "flags-judgment",
    "valuation-temperature": "valuation-temperature",
    "deep-dive protocol v1.3 (live #1)": "deep-dive", "deep-dive": "deep-dive",
    "decision-card-v1": "decision-card",
}
# tags that look like sectors but are method names
NOT_SECTOR = {"sector-cycle"}
# the 7 pilot calls (20-Nov-2026) carry no sector tag
SECTOR_FALLBACK = {"SKIPPER": "power-td", "UNIPARTS": "auto-components"}


def today() -> dt.date:
    """Today's date in IST (the cron runs at 22:00 IST). SB_TODAY=YYYY-MM-DD overrides (tests, replays)."""
    o = os.environ.get("SB_TODAY")
    return dt.date.fromisoformat(o) if o else dt.datetime.now(IST).date()


def d(s) -> dt.date | None:
    if not s:
        return None
    if isinstance(s, dt.date):
        return s
    return dt.date.fromisoformat(str(s)[:10])


# ----------------------------------------------------------------- memdb access
def memdb_core():
    if REPO not in sys.path:
        sys.path.insert(0, REPO)
    from memdb import core  # noqa: E402
    return core


def load_call_records(include_closed=True) -> list[dict]:
    """All paper-call thesis records (full records, newest version) from memdb."""
    core = memdb_core()
    con = core.connect()
    rows = core.search(con, "", rtype="thesis", tag="paper-call", limit=1_000_000)
    out = []
    for r in rows:
        if not include_closed and (r.get("status") or "open") != "open":
            continue
        out.append(r)
    out.sort(key=lambda r: r["id"])
    return out


def normalise(rec: dict) -> dict:
    """memdb record -> flat call dict used everywhere else."""
    x = rec.get("data") or {}
    tags = rec.get("tags") or []
    tick = (rec.get("tickers") or [""])[0]
    market = "us" if tick.startswith("US-") or "us" in tags else "india"
    sym = tick[3:] if tick.startswith("US-") else tick
    sector = next((t[7:] for t in tags if t.startswith("sector-") and t not in NOT_SECTOR), "")
    sector = sector or SECTOR_FALLBACK.get(sym, "unknown")
    batch = next((t for t in tags if re.fullmatch(r"batch\d+", t)), "pilot")
    title = re.sub(r"^Paper call:\s*", "", rec.get("title") or "")
    base = x.get("base_rate_probability")
    prob = x.get("probability", x.get("p"))   # 'p' = short form used by gold/macro calls (28-Nov-2026)
    if isinstance(prob, bool) or not isinstance(prob, (int, float, str)):
        raise NotBinaryCall(f"{rec['id']}: no single probability (multi-outcome scenario set or missing)")
    return {
        "id": rec["id"], "ticker": tick, "symbol": sym, "market": market,
        "method": METHOD_MAP.get(x.get("method") or "", x.get("method") or "unknown"),
        "probability": float(prob),
        "base_rate_probability": float(base) if base is not None else None,
        "made_on": x.get("made_on") or x.get("made") or rec.get("date"), "resolve_by": x.get("resolve_by"),
        "resolution_rule": x.get("resolution_rule") or ("(no written rule; from title) " + title),
        "resolution_source": x.get("resolution_source") or "",
        "sector": sector, "batch": batch, "title": title, "status": rec.get("status") or "open",
        "outcome": x.get("outcome"), "data": x, "version": rec.get("version"),
    }


class NotBinaryCall(ValueError):
    """A paper-call record the binary scoreboard cannot score (e.g. a multi-outcome scenario set)."""


def load_calls(include_closed=True) -> list[dict]:
    """Normalised binary calls. Records with no single probability are skipped with a warning
    (one bad record must not stop scoring for every other call)."""
    out, skipped = [], []
    for r in load_call_records(include_closed):
        try:
            out.append(normalise(r))
        except NotBinaryCall as e:
            skipped.append(str(e))
    for msg in skipped:
        print(f"WARNING skipped call {msg}", file=sys.stderr)
    return out


def load_specs(path=SPECS_FILE) -> dict:
    with open(path, encoding="utf-8") as f:
        s = json.load(f)
    return {k: v for k, v in s.items() if not k.startswith("_")}


def pending_seed_ids(seeds_dir=SEEDS_DIR) -> set:
    """ids already written to a scoreboard resolution seed (applied or not) -> never resolve twice."""
    out = set()
    for p in glob.glob(os.path.join(seeds_dir, SEED_GLOB)):
        try:
            for r in read_json(p):
                out.add(r["id"])
        except (ValueError, KeyError, OSError):
            continue
    return out


# ----------------------------------------------------------------- scoring
def brier(p: float, o: int) -> float:
    return (p - o) ** 2


def logloss(p: float, o: int, eps: float = 0.01) -> float:
    """Natural-log loss with probabilities clipped to [eps, 1-eps] (one 0/1 forecast cannot be infinite)."""
    p = min(max(p, eps), 1 - eps)
    return -(o * math.log(p) + (1 - o) * math.log(1 - p))


def score_fields(p: float, base: float | None, o: int) -> dict:
    out = {"brier": round(brier(p, o), 6), "logloss": round(logloss(p, o), 6)}
    if base is not None:
        out["brier_base"] = round(brier(base, o), 6)
        out["logloss_base"] = round(logloss(base, o), 6)
    return out


# ----------------------------------------------------------------- HTTP with polite spacing + disk cache
_last_by_host: dict = {}
GAP = {"www.nseindia.in": 1.6, "nsearchives.nseindia.in": 1.6, "query1.finance.yahoo.com": 1.0,
       "www.screener.in": 2.0}


def http_get(url, headers=None, binary=False, max_age_h=20.0, tries=4, cache=True):
    """GET with per-host spacing, gzip, retry/back-off and an on-disk cache (max_age_h hours)."""
    os.makedirs(os.path.join(CACHE, "http"), exist_ok=True)
    key = hashlib.sha1(url.encode()).hexdigest()
    path = os.path.join(CACHE, "http", key)
    if cache and os.path.exists(path) and time.time() - os.path.getmtime(path) < max_age_h * 3600:
        with open(path, "rb") as f:
            b = f.read()
        return b if binary else b.decode("utf-8", "replace")
    host = urllib.parse.urlparse(url).netloc
    hdrs = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip"}
    hdrs.update(headers or {})
    err = None
    for i in range(tries):
        wait = GAP.get(host, 0.3) - (time.time() - _last_by_host.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        _last_by_host[host] = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=hdrs), timeout=60) as r:
                b = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    b = gzip.decompress(b)
            if cache:
                with open(path, "wb") as f:
                    f.write(b)
            return b if binary else b.decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            err = e
            if e.code in (403, 429, 500, 502, 503, 504) and i < tries - 1:
                time.sleep(3 * 2 ** i)
                continue
            raise
        except urllib.error.URLError as e:
            err = e
            if i < tries - 1:
                time.sleep(2 ** i)
                continue
            raise
    raise RuntimeError(f"GET failed: {url}: {err}")


def read_text(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def drop_cache(url):
    """Forget a cached response (e.g. an empty answer from a flaky endpoint)."""
    p = os.path.join(CACHE, "http", hashlib.sha1(url.encode()).hexdigest())
    if os.path.exists(p):
        os.remove(p)


def slug_uid(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9.-]+", "-", s).strip("-")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(text)
    os.replace(tmp, path)


def write_bytes(path, b):
    with open(path, "wb") as f:
        f.write(b)


def write_json(path, obj):
    write_text(path, json.dumps(obj, indent=1, ensure_ascii=False) + "\n")
