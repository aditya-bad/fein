"""memdb core: append-only JSONL store (git-tracked) + rebuildable SQLite/FTS5 index.

Canonical data : memory/store/<type>/<shard>.jsonl   (one JSON record per line, last version wins)
Metrics        : memory/store/metric/<TICKER>.jsonl  (numeric time series)
Index          : memory/.index/memory.sqlite         (gitignored, rebuilt automatically)
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("MEMDB_ROOT", Path(__file__).resolve().parent.parent))
STORE = ROOT / "memory" / "store"
INDEX_DIR = ROOT / "memory" / ".index"
INDEX = INDEX_DIR / "memory.sqlite"

TYPES = {
    "company": "A listed company (one per ticker); data: exchange, sector, mcap band, etc.",
    "case_study": "Historical episode (multibagger, blow-up, fraud) with lessons",
    "strategy": "Investing/trading framework or an investor's method",
    "analysis": "A dated analysis of a stock/theme: verdict, score, kill criteria",
    "thesis": "A live investment thesis we hold or watch, with kill criteria",
    "promise": "Management guidance/promise: said_on, target_period, metric, outcome, status",
    "event": "Dated corporate/market/regulatory event (pledge, order win, SEBI order...)",
    "insight": "Principle, base rate, lesson, or corrected myth",
    "decision": "A dated decision and its reasoning",
    "person": "Investor, promoter, manager",
    "theme": "Sector/macro theme with beneficiary map",
    "source": "A document/URL we relied on",
    "note": "A chunk of a longer research document (auto from ingest-md)",
}

SCHEMA = """
CREATE TABLE IF NOT EXISTS records(
  id TEXT PRIMARY KEY, type TEXT, title TEXT, tickers TEXT, tags TEXT, date TEXT,
  body TEXT, data TEXT, sources TEXT, confidence TEXT, status TEXT,
  created TEXT, updated TEXT, version INTEGER);
CREATE INDEX IF NOT EXISTS ix_type ON records(type);
CREATE INDEX IF NOT EXISTS ix_date ON records(date);
CREATE TABLE IF NOT EXISTS rec_tickers(id TEXT, ticker TEXT);
CREATE INDEX IF NOT EXISTS ix_rt ON rec_tickers(ticker);
CREATE INDEX IF NOT EXISTS ix_rt_id ON rec_tickers(id);
CREATE TABLE IF NOT EXISTS rec_tags(id TEXT, tag TEXT);
CREATE INDEX IF NOT EXISTS ix_tag ON rec_tags(tag);
CREATE INDEX IF NOT EXISTS ix_tag_id ON rec_tags(id);
CREATE TABLE IF NOT EXISTS links(src TEXT, dst TEXT, rel TEXT);
CREATE INDEX IF NOT EXISTS ix_ls ON links(src);
CREATE INDEX IF NOT EXISTS ix_ld ON links(dst);
CREATE TABLE IF NOT EXISTS metrics(
  ticker TEXT, period TEXT, field TEXT, value REAL, unit TEXT, source TEXT, as_of TEXT,
  PRIMARY KEY(ticker, period, field));
CREATE VIRTUAL TABLE IF NOT EXISTS fts USING fts5(
  id UNINDEXED, title, tags, tickers, body, tokenize='porter unicode61');
CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT);
"""


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slug(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:80] or hashlib.sha1(str(time.time()).encode()).hexdigest()[:10]


def shard_path(rtype: str, rid: str) -> Path:
    return STORE / rtype / (hashlib.sha1(rid.encode()).hexdigest()[:2] + ".jsonl")


def _fingerprint() -> str:
    """Cheap fingerprint of the canonical store (paths+sizes+mtimes)."""
    h = hashlib.sha1()
    if STORE.exists():
        for p in sorted(STORE.rglob("*.jsonl")):
            st = p.stat()
            h.update(f"{p.relative_to(STORE)}:{st.st_size}:{int(st.st_mtime)};".encode())
    return h.hexdigest()


def connect(auto_rebuild: bool = True) -> sqlite3.Connection:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(INDEX)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    if auto_rebuild:
        row = con.execute("SELECT v FROM meta WHERE k='fp'").fetchone()
        if not row or row[0] != _fingerprint():
            rebuild(con)
    return con


def _index_record(con: sqlite3.Connection, r: dict) -> None:
    rid = r["id"]
    prev = con.execute("SELECT rowid FROM records WHERE id=?", (rid,)).fetchone()
    if prev:  # FTS rows are keyed by the records rowid -> O(log n) delete
        con.execute("DELETE FROM fts WHERE rowid=?", (prev[0],))
        for t in ("records", "rec_tickers", "rec_tags"):
            con.execute(f"DELETE FROM {t} WHERE id=?", (rid,))
        con.execute("DELETE FROM links WHERE src=?", (rid,))
    if r.get("deleted"):
        return
    tick = r.get("tickers") or []
    tags = r.get("tags") or []
    cur = con.execute(
        "INSERT INTO records VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (rid, r["type"], r.get("title", ""), json.dumps(tick), json.dumps(tags),
         r.get("date", ""), r.get("body", ""), json.dumps(r.get("data") or {}),
         json.dumps(r.get("sources") or []), r.get("confidence", ""), r.get("status", ""),
         r.get("created", ""), r.get("updated", ""), r.get("version", 1)))
    con.executemany("INSERT INTO rec_tickers VALUES(?,?)", [(rid, t.upper()) for t in tick])
    con.executemany("INSERT INTO rec_tags VALUES(?,?)", [(rid, t.lower()) for t in tags])
    links = []
    for l in r.get("links") or []:
        if isinstance(l, str):
            to, _, rel = l.rpartition(":") if l.count(":") >= 2 else (l, "", "related")
            links.append((rid, to or l, rel or "related"))
        else:
            links.append((rid, l["to"], l.get("rel", "related")))
    con.executemany("INSERT INTO links VALUES(?,?,?)", links)
    data_txt = " ".join(f"{k} {v}" for k, v in (r.get("data") or {}).items())
    con.execute("INSERT INTO fts(rowid, id, title, tags, tickers, body) VALUES(?,?,?,?,?,?)",
                (cur.lastrowid, rid, r.get("title", ""), " ".join(tags), " ".join(tick),
                 (r.get("body", "") + " " + data_txt)))


def _index_metric(con, m: dict) -> None:
    con.execute("INSERT OR REPLACE INTO metrics VALUES(?,?,?,?,?,?,?)",
                (m["ticker"].upper(), m["period"], m["field"], m["value"],
                 m.get("unit", ""), m.get("source", ""), m.get("as_of", "")))


def rebuild(con: sqlite3.Connection | None = None) -> int:
    own = con is None
    if own:
        con = connect(auto_rebuild=False)
    for t in ("records", "rec_tickers", "rec_tags", "links", "metrics", "fts"):
        con.execute(f"DELETE FROM {t}")
    n = 0
    if STORE.exists():
        for p in sorted(STORE.rglob("*.jsonl")):
            is_metric = p.parent.name == "metric"
            latest: dict[str, dict] = {}
            with p.open(encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    obj = json.loads(line)
                    if is_metric:
                        _index_metric(con, obj)
                        n += 1
                    else:
                        latest[obj["id"]] = obj
            for r in latest.values():
                _index_record(con, r)
                n += 1
    con.execute("INSERT OR REPLACE INTO meta VALUES('fp',?)", (_fingerprint(),))
    con.commit()
    if own:
        con.close()
    return n


def touch(con) -> None:
    """Record the store fingerprint and commit (call once after bulk writes)."""
    con.execute("INSERT OR REPLACE INTO meta VALUES('fp',?)", (_fingerprint(),))
    con.commit()


def compact() -> int:
    """Rewrite every shard keeping only the latest version of each record
    (drops history + tombstones). Metrics: keep last value per (period, field)."""
    kept = 0
    for p in sorted(STORE.rglob("*.jsonl")):
        latest: dict = {}
        for line in p.open(encoding="utf-8"):
            if line.strip():
                o = json.loads(line)
                key = (o["period"], o["field"]) if p.parent.name == "metric" else o["id"]
                latest[key] = o
        rows = [o for o in latest.values() if not o.get("deleted")]
        p.write_text("".join(json.dumps(o, ensure_ascii=False, sort_keys=True) + "\n" for o in rows),
                     encoding="utf-8")
        kept += len(rows)
    rebuild()
    return kept


def _append(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, sort_keys=True) + "\n")


def get(con, rid: str) -> dict | None:
    row = con.execute("SELECT * FROM records WHERE id=?", (rid,)).fetchone()
    return _row(row) if row else None


def _row(row) -> dict:
    d = dict(row)
    for k in ("tickers", "tags", "data", "sources"):
        d[k] = json.loads(d[k] or "null")
    return d


def put(con, rec: dict, merge: bool = True, commit: bool = True) -> dict:
    """Create or update a record. With merge, unspecified fields keep old values;
    list fields (tickers/tags/sources/links) are unioned; data dict is merged."""
    # accept links as "target_id:rel" strings as well as {"to","rel"} dicts
    norm = []
    for l in rec.get("links") or []:
        if isinstance(l, str):
            to, _, rel = l.rpartition(":") if l.count(":") >= 2 else (l, "", "related")
            norm.append({"to": to or l, "rel": rel or "related"})
        else:
            norm.append(l)
    if norm:
        rec["links"] = norm
    if rec.get("type") not in TYPES:
        raise ValueError(f"type must be one of {sorted(TYPES)}")
    rid = rec.get("id") or f"{rec['type']}:{slug(rec.get('title', ''))}"
    rec["id"] = rid
    old = get(con, rid)
    if old and merge:
        old_links = [{"to": d, "rel": r} for d, r in con.execute(
            "SELECT dst, rel FROM links WHERE src=?", (rid,))]
        out = {**old, **{k: v for k, v in rec.items() if v not in (None, "", [], {})}}
        for k in ("tickers", "tags", "sources"):
            out[k] = list(dict.fromkeys((old.get(k) or []) + (rec.get(k) or [])))
        out["data"] = {**(old.get("data") or {}), **(rec.get("data") or {})}
        seen = {(l["to"], l["rel"]) for l in old_links}
        out["links"] = old_links + [l for l in rec.get("links") or []
                                    if (l["to"], l.get("rel", "related")) not in seen]
        out["version"] = int(old.get("version") or 1) + 1
        out["created"] = old.get("created") or now()
    else:
        out = dict(rec)
        out["version"] = 1
        out["created"] = now()
    out["updated"] = now()
    out = {k: v for k, v in out.items() if v not in (None, "", [], {}) or k == "data"}
    _append(shard_path(out["type"], rid), out)
    _index_record(con, out)
    if commit:
        touch(con)
    return out


def delete(con, rid: str) -> None:
    old = get(con, rid)
    if not old:
        raise KeyError(rid)
    tomb = {"id": rid, "type": old["type"], "deleted": True, "updated": now()}
    _append(shard_path(old["type"], rid), tomb)
    _index_record(con, tomb)
    touch(con)


def history(rid: str, rtype: str) -> list[dict]:
    p = shard_path(rtype, rid)
    if not p.exists():
        return []
    return [o for o in (json.loads(l) for l in p.open(encoding="utf-8") if l.strip())
            if o.get("id") == rid]


def add_metric(con, ticker, period, field, value, unit="", source="", as_of="", commit=True) -> dict:
    m = {"ticker": ticker.upper(), "period": period, "field": field, "value": float(value),
         "unit": unit, "source": source, "as_of": as_of or now()[:10]}
    _append(STORE / "metric" / f"{m['ticker']}.jsonl", m)
    _index_metric(con, m)
    if commit:
        touch(con)
    return m


def _fts_query(q: str) -> str:
    # Quote each term so punctuation (& - : /) can't break FTS syntax; keep OR/AND/NOT.
    out = []
    for tok in re.findall(r'"[^"]+"|\S+', q):
        if tok.upper() in ("OR", "AND", "NOT"):
            out.append(tok.upper())
        elif tok.startswith('"'):
            out.append(tok)
        elif tok.endswith("*"):
            out.append('"' + tok[:-1].replace('"', '') + '"*')
        else:
            out.append('"' + tok.replace('"', '') + '"')
    return " ".join(out)


def search(con, q: str = "", rtype=None, ticker=None, tag=None, since=None,
           limit: int = 20) -> list[dict]:
    where, args = [], []
    if q:
        sql = ("SELECT r.*, bm25(fts, 0, 5.0, 2.0, 3.0, 1.0) AS score, "
               "snippet(fts, 4, '[', ']', ' … ', 18) AS snip FROM fts "
               "JOIN records r ON r.rowid = fts.rowid WHERE fts MATCH ?")
        args.append(_fts_query(q))
    else:
        sql = "SELECT r.*, 0 AS score, substr(r.body,1,160) AS snip FROM records r WHERE 1=1"
    if rtype:
        where.append("r.type = ?"); args.append(rtype)
    if ticker:
        where.append("r.id IN (SELECT id FROM rec_tickers WHERE ticker=?)"); args.append(ticker.upper())
    if tag:
        where.append("r.id IN (SELECT id FROM rec_tags WHERE tag=?)"); args.append(tag.lower())
    if since:
        where.append("r.date >= ?"); args.append(since)
    if where:
        sql += " AND " + " AND ".join(where)
    sql += " ORDER BY score, r.date DESC LIMIT ?" if q else " ORDER BY r.date DESC, r.updated DESC LIMIT ?"
    args.append(limit)
    out = [_row(row) for row in con.execute(sql, args)]
    # Recall fallback: if an all-terms (AND) query finds little, widen to any-term (OR).
    terms = [t for t in re.findall(r'"[^"]+"|\S+', q) if t.upper() not in ("OR", "AND", "NOT")]
    if q and len(terms) > 1 and len(out) < max(3, limit // 3) and " OR " not in q.upper():
        seen = {r["id"] for r in out}
        for r in search(con, " OR ".join(terms), rtype, ticker, tag, since, limit):
            if r["id"] not in seen and len(out) < limit:
                r["fallback"] = True
                out.append(r)
    return out


def related(con, rid: str) -> list[dict]:
    rows = con.execute(
        "SELECT 'out' AS dir, rel, dst AS other FROM links WHERE src=? "
        "UNION ALL SELECT 'in', rel, src FROM links WHERE dst=?", (rid, rid)).fetchall()
    res = []
    for r in rows:
        o = get(con, r["other"])
        res.append({"dir": r["dir"], "rel": r["rel"], "id": r["other"],
                    "title": o["title"] if o else "(missing)", "type": o["type"] if o else ""})
    # also records sharing a ticker
    return res


def stats(con) -> dict:
    d = {r[0]: r[1] for r in con.execute("SELECT type, count(*) FROM records GROUP BY type")}
    d["_metrics"] = con.execute("SELECT count(*) FROM metrics").fetchone()[0]
    d["_tickers"] = con.execute("SELECT count(DISTINCT ticker) FROM rec_tickers").fetchone()[0]
    d["_links"] = con.execute("SELECT count(*) FROM links").fetchone()[0]
    return d


def ingest_markdown(con, path: Path, tags=None, tickers=None, date="") -> int:
    """Split a markdown file by headings into `note` records (searchable passages),
    each linked to a parent `source` record for the file."""
    text = path.read_text(encoding="utf-8")
    rel = str(path.resolve().relative_to(ROOT)) if path.resolve().is_relative_to(ROOT) else str(path)
    parent_id = f"source:{slug(rel)}"
    title_m = re.search(r"^#\s+(.+)$", text, re.M)
    put(con, {"id": parent_id, "type": "source", "title": title_m.group(1) if title_m else path.stem,
              "body": f"File: {rel}", "tags": tags or [], "tickers": tickers or [], "date": date,
              "data": {"path": rel}}, merge=True, commit=False)
    parts = re.split(r"(?m)^(#{1,4}\s+.+)$", text)
    chunks, head = [], path.stem
    if parts[0].strip():
        chunks.append((head, parts[0]))
    for i in range(1, len(parts), 2):
        chunks.append((parts[i].lstrip("# ").strip(), parts[i + 1] if i + 1 < len(parts) else ""))
    n, written = 0, set()
    stale = {row[0] for row in con.execute("SELECT src FROM links WHERE dst=? AND rel='part_of'", (parent_id,))}
    for j, (h, body) in enumerate(chunks):
        body = body.strip()
        if len(body) < 40:
            continue
        # split very long sections into ~3,000-char pieces on paragraph boundaries
        pieces, buf = [], ""
        for para in re.split(r"\n\s*\n", body):
            if len(buf) + len(para) > 3000 and buf:
                pieces.append(buf); buf = ""
            buf += para + "\n\n"
        if buf.strip():
            pieces.append(buf)
        for k, piece in enumerate(pieces):
            put(con, {"id": f"note:{slug(rel)}:{j:03d}{'-' + str(k) if k else ''}", "type": "note",
                      "title": f"{path.stem} › {h}", "body": piece.strip(), "tags": tags or [],
                      "tickers": tickers or [], "date": date, "data": {"path": rel, "section": h},
                      "links": [{"to": parent_id, "rel": "part_of"}]}, merge=False, commit=False)
            written.add(f"note:{slug(rel)}:{j:03d}{'-' + str(k) if k else ''}")
            n += 1
    for rid in stale - written:  # sections that no longer exist in the file
        tomb = {"id": rid, "type": "note", "deleted": True, "updated": now()}
        _append(shard_path("note", rid), tomb)
        _index_record(con, tomb)
    touch(con)
    return n
