"""Shared helpers for the FEIN change detectors (standard library only).

Paths:   FEIN_DATA env var (default ~/fein-data) -> raw/, alerts/, logs/, fein.sqlite
HTTP:    NSE via urllib (short browser UA + JSON headers, >=1.5 s gap, back-off on 403/429/503)
         BSE via the system `curl --http2` (BSE's Akamai front rejects HTTP/1.1 urllib).
"""
import csv, datetime as dt, gzip, io, json, logging, os, re, sqlite3, subprocess, sys, time
import urllib.error, urllib.parse, urllib.request

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
DATA = os.path.expanduser(os.environ.get("FEIN_DATA", "~/fein-data"))
DB_PATH = os.path.join(DATA, "fein.sqlite")

NSE = "https://www.nseindia.in/api/"
NSE_ARCH = "https://nsearchives.nseindia.com/"
NSE_HDRS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9", "Accept-Encoding": "gzip",
            "Referer": "https://www.nseindia.in/"}
BSE = "https://api.bseindia.com/BseIndiaAPI/api/"
BSE_HDRS = ["Accept: application/json, text/plain, */*", "Accept-Language: en-US,en;q=0.9",
            "Sec-Fetch-Mode: cors", "Sec-Fetch-Site: same-site", "Sec-Fetch-Dest: empty",
            "Referer: https://www.bseindia.com/"]
BSE_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
MIN_GAP = 1.5
_last = {"nse": 0.0, "bse": 0.0}
log = logging.getLogger("fein")


def today_ist():
    return dt.datetime.now(IST).date()


def setup_logging(name):
    os.makedirs(os.path.join(DATA, "logs"), exist_ok=True)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    log.setLevel(logging.INFO)
    log.handlers.clear()
    # WatchedFileHandler reopens the file after logrotate moves it (see README)
    from logging.handlers import WatchedFileHandler
    fh = WatchedFileHandler(os.path.join(DATA, "logs", f"{name}.log"))
    fh.setFormatter(fmt)
    sh = logging.StreamHandler(sys.stderr)
    sh.setFormatter(fmt)
    log.addHandler(fh)
    log.addHandler(sh)


def _pace(host):
    wait = MIN_GAP - (time.time() - _last[host])
    if wait > 0:
        time.sleep(wait)
    _last[host] = time.time()


def http_get(url, tries=4, as_text=False):
    """GET an NSE URL. Returns parsed JSON (or text if as_text). Raises after retries."""
    err = None
    for i in range(tries):
        _pace("nse")
        try:
            req = urllib.request.Request(url, headers=NSE_HDRS)
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    body = gzip.decompress(body)
            txt = body.decode("utf-8-sig", "replace")
            if as_text:
                return txt
            if txt.lstrip().startswith("<"):
                raise ValueError("HTML instead of JSON (endpoint changed or blocked)")
            return json.loads(txt)
        except urllib.error.HTTPError as e:
            err = e
            if e.code not in (403, 429, 500, 502, 503, 504):
                raise
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
            err = e
        if i < tries - 1:
            back = 5 * 2 ** i
            log.warning("NSE %s failed (%s); retry in %ss", url[:120], err, back)
            time.sleep(back)
    raise RuntimeError(f"NSE fetch failed after {tries} tries: {url} ({err})")


def nse_api(path, **params):
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v not in (None, "")})
    url = NSE + path + ("?" + q if q else "")
    return http_get(url), url


def bse_api(path, tries=4, **params):
    url = BSE + path + "?" + urllib.parse.urlencode(params, safe="")
    err = None
    for i in range(tries):
        _pace("bse")
        cmd = ["curl", "-sS", "-m", "60", "--http2", "--compressed", "-L", "-A", BSE_UA,
               "-w", "\n%{http_code}"]
        for h in BSE_HDRS:
            cmd += ["-H", h]
        cmd.append(url)
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=90)
            body, _, code = r.stdout.rpartition(b"\n")
            code = code.decode().strip()
            if code == "200":
                txt = body.decode("utf-8", "replace")
                if txt.lstrip().startswith("<"):
                    raise ValueError("HTML instead of JSON")
                data = json.loads(txt)
                if isinstance(data, str):
                    data = json.loads(data)
                return data, url
            err = f"HTTP {code} {r.stderr.decode()[:150]}"
        except (subprocess.TimeoutExpired, ValueError, OSError) as e:
            err = e
        if i < tries - 1:
            time.sleep(5 * 2 ** i)
    raise RuntimeError(f"BSE fetch failed: {url} ({err})")


# ---------- parsing helpers ----------
def num(x):
    """'1,23,456.7' / ' 45.04 ' / '-' / None -> float or None."""
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip().replace(",", "")
    if s in ("", "-", "NA", "N.A.", "nil", "Nil"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


_MON = {m: i for i, m in enumerate(
    ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"], 1)}


def parse_date(s):
    """Parse NSE/BSE date strings to ISO 'YYYY-MM-DD[ HH:MM:SS]'. Returns None on failure."""
    if not s:
        return None
    s = str(s).strip().replace(",", "")
    m = re.match(r"(\d{1,2})-([A-Za-z]{3})-(\d{4})(?:\s+(\d{1,2})[:\-](\d{2})(?::(\d{2}))?)?", s)
    if m:
        d, mon, y, hh, mm, ss = m.groups()
        mo = _MON.get(mon.upper())
        if not mo:
            return None
        out = f"{y}-{mo:02d}-{int(d):02d}"
        if hh:
            out += f" {int(hh):02d}:{mm}:{ss or '00'}"
        return out
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2}):(\d{2}))?", s)
    if m:
        y, mo, d, hh, mm, ss = m.groups()
        return f"{y}-{mo}-{d}" + (f" {hh}:{mm}:{ss}" if hh else "")
    m = re.match(r"(\d{2})-(\d{2})-(\d{4})", s)
    if m:
        d, mo, y = m.groups()
        return f"{y}-{mo}-{d}"
    return None


def norm_name(name):
    s = (name or "").lower().replace("&", " and ")
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    s = re.sub(r"\b(limited|ltd|the|co|company|corp|corporation|india|private|pvt)\b", " ", s)
    return re.sub(r"\s+", "", s)


def read_csv_text(txt):
    rows = list(csv.reader(io.StringIO(txt)))
    if not rows:
        return []
    head = [h.strip() for h in rows[0]]
    return [dict(zip(head, [c.strip() for c in r])) for r in rows[1:] if r and any(c.strip() for c in r)]


# ---------- storage ----------
SCHEMA = """
CREATE TABLE IF NOT EXISTS announcements(
  source TEXT, id TEXT, dt TEXT, date TEXT, symbol TEXT, bse_code TEXT, company TEXT,
  category TEXT, subject TEXT, text TEXT, url TEXT, PRIMARY KEY(source, id));
CREATE INDEX IF NOT EXISTS ix_ann_date ON announcements(date);
CREATE TABLE IF NOT EXISTS insider_trades(
  id TEXT PRIMARY KEY, dt TEXT, date TEXT, symbol TEXT, company TEXT, person TEXT, category TEXT,
  mode TEXT, tx_type TEXT, sec_type TEXT, qty REAL, value REAL, before_pct REAL, after_pct REAL,
  trade_from TEXT, trade_to TEXT, url TEXT);
CREATE INDEX IF NOT EXISTS ix_pit_sym ON insider_trades(symbol, date);
CREATE TABLE IF NOT EXISTS sast(
  id TEXT PRIMARY KEY, dt TEXT, date TEXT, symbol TEXT, company TEXT, acquirer TEXT, promoter TEXT,
  reg_type TEXT, mode TEXT, side TEXT, shares_acq REAL, shares_sale REAL, shares_after REAL,
  pct_acq REAL, pct_sale REAL, pct_after REAL, period TEXT, url TEXT);
CREATE INDEX IF NOT EXISTS ix_sast_sym ON sast(symbol, date);
CREATE TABLE IF NOT EXISTS pledges(
  snapshot_date TEXT, symbol TEXT, company TEXT, shp_date TEXT, promoter_holding_pct REAL,
  pledged_pct_of_promoter REAL, pledged_pct_of_equity REAL, promoter_pledged_shares REAL,
  promoter_shares REAL, total_shares REAL, all_pledged_pct REAL, broadcast_dt TEXT,
  PRIMARY KEY(snapshot_date, symbol));
CREATE TABLE IF NOT EXISTS deals(
  date TEXT, kind TEXT, symbol TEXT, company TEXT, client TEXT, side TEXT, qty REAL, price REAL,
  value_cr REAL, remarks TEXT, PRIMARY KEY(date, kind, symbol, client, side, qty, price));
CREATE TABLE IF NOT EXISTS shares(symbol TEXT PRIMARY KEY, as_of TEXT, shares REAL, source TEXT, fetched TEXT);
CREATE TABLE IF NOT EXISTS symbols(symbol TEXT PRIMARY KEY, name TEXT, isin TEXT, norm TEXT);
CREATE INDEX IF NOT EXISTS ix_sym_norm ON symbols(norm);
CREATE TABLE IF NOT EXISTS runs(run_at TEXT, dataset TEXT, day TEXT, rows INTEGER, status TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS alerts(
  key TEXT PRIMARY KEY, first_seen TEXT, date TEXT, symbol TEXT, rule TEXT, details TEXT, url TEXT);
"""

# Column meanings (lesson L6): pledged_pct_of_promoter = NSE percPromoterShares (promoter shares
# pledged / promoter holding); pledged_pct_of_equity = percTotShares (promoter shares pledged /
# total shares). all_pledged_pct = percSharesPledged includes NON-promoter pledges: do not use it
# as "promoter pledge".


def db(path=None):
    p = path or DB_PATH
    if p != ":memory:":
        os.makedirs(os.path.dirname(p), exist_ok=True)
    con = sqlite3.connect(p, timeout=60)
    con.row_factory = sqlite3.Row
    if p != ":memory:":
        # SD-card friendly: WAL = sequential appends, fewer fsyncs; NORMAL sync is safe with WAL.
        con.execute("PRAGMA journal_mode=WAL")
        con.execute("PRAGMA synchronous=NORMAL")
        con.execute("PRAGMA wal_autocheckpoint=2000")
    con.execute("PRAGMA cache_size=-8000")      # ~8 MB page cache cap (low memory)
    con.execute("PRAGMA temp_store=FILE")
    con.executescript(SCHEMA)
    return con


def upsert(con, table, rows):
    if not rows:
        return 0
    cols = list(rows[0].keys())
    sql = (f"INSERT OR REPLACE INTO {table}({','.join(cols)}) "
           f"VALUES({','.join('?' * len(cols))})")
    con.executemany(sql, [tuple(r.get(c) for c in cols) for r in rows])
    return len(rows)   # no commit here: callers commit once per dataset/day (batched writes)


def single_instance(name):
    """Take an exclusive lock so cron/systemd never runs two copies at once. Returns the handle
    (keep it referenced) or None if another copy is running."""
    import fcntl
    os.makedirs(os.path.join(DATA, "logs"), exist_ok=True)
    fh = open(os.path.join(DATA, "logs", f".{name}.lock"), "w")
    try:
        fcntl.flock(fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return None
    return fh
