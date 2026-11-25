#!/usr/bin/env python3
"""FEIN news layer: news, rating actions, SEBI/RBI items and sector policy watch for the companies we cover.

Standard library + the system `curl`. Polite: one request at a time, >= 2-3 s between requests to the same
host, back-off on 429/5xx, no logins. Sites behind CAPTCHA / anti-bot challenges are never automated: they
are skipped and logged (see README "Sources").

  python3 news.py                       # default window --since 2d, all of watchlist.csv + policy.csv
  python3 news.py --since 7d            # or --since 2026-11-20 / --since 36h
  python3 news.py --tickers UTTAMSUGAR,US-KEX --sources google,ratings
  python3 news.py --selftest            # offline, fixture RSS/HTML, writes only to a temp dir

Outputs: $FEIN_DATA/news/YYYY-MM-DD.md and .csv (date, ticker, source, headline, url, matched_rule).
Dedup state: $FEIN_DATA/news/news.sqlite (an item is reported once, on the run it is first seen).
Research, not SEBI-registered advice: an item means "go and read it", not "trade".
"""
import argparse, csv, datetime as dt, email.utils, hashlib, html, logging, os, re, sqlite3, subprocess
import sys, tempfile, time, urllib.parse
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "detectors"))
from fein_common import IST, DATA, setup_logging, single_instance  # noqa: E402

log = logging.getLogger("fein")
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
GAP = {"news.google.com": 3.0}          # seconds between requests per host; default below
DEFAULT_GAP = 2.0
_last = {}
SOURCES = ("google", "ratings", "sebi", "rbi", "policy")

SEBI_LISTS = {  # first page (25 newest rows) of each public listing; no login, no captcha on the listing
    "sebi_order": "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=2&ssid=9&smid=0",
    "sebi_press": "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=6&ssid=23&smid=0",
}
RBI_RSS = "https://www.rbi.org.in/pressreleases_rss.xml"
RATING_QUERY = ('(CRISIL OR ICRA OR "CARE Ratings" OR CareEdge OR "India Ratings" OR "Ind-Ra" OR Acuite OR '
                'Brickwork OR Infomerics) (downgrade OR downgrades OR upgrade OR upgrades OR reaffirms OR '
                '"rating watch" OR outlook OR "not cooperating" OR withdraws)')
# Never automated (CAPTCHA / bot challenge / JS-only), listed in every report so the gap stays visible.
SKIPPED = [
    ("NCLT / NCLAT cause lists", "CAPTCHA on case search; never automated"),
    ("ICRA company search", "Barracuda/infisecure bot-protection script; search route returns 404. Rationale PDFs by Id still work by hand"),
    ("CRISIL rating-rationale listing", "page embeds reCAPTCHA; listing JSON not used. Single rationale HTML pages work by hand"),
    ("CARE Ratings", "JS-heavy, no clean public endpoint"),
    ("India Ratings", "JS single-page app; not curl-able"),
    ("SEBI listings beyond page 1", "older rows need the site's AJAX pager; only the 25 newest per list are read"),
]
ANTIBOT = re.compile(r"cf-chl|challenge-platform|Just a moment\.\.\.|Attention Required! \| Cloudflare|"
                     r"/sorry/index|unusual traffic from your computer|g-recaptcha|hcaptcha|infisecure", re.I)

# Material rules, checked on the headline, in priority order (first hit = rule name; all hits listed).
MATERIAL = [
    ("court", r"supreme court|high court|\bcourt\b|\bnclt\b|\bnclat\b|tribunal|\bsc\b (?:order|verdict|ruling)"),
    ("sebi", r"\bsebi\b"), ("rbi", r"\brbi\b|reserve bank"),
    ("usfda", r"usfda|\bfda\b|warning letter|import alert|form 483|\bcgmp\b"),
    ("fraud", r"\bfraud|forensic|siphon|money.laundering|\bed\b (?:raid|probe|searches)|whistleblower"),
    ("raid", r"\braids?\b|income.tax (?:search|survey)|\bsearch(?:es)? at\b"),
    ("default", r"\bdefault|insolvency|bankrupt|chapter 11|\bcirp\b|non.payment|missed (?:interest|payment)"),
    ("downgrade", r"downgrad|negative outlook|rating watch|not cooperating|\bcut to\b"),
    ("resignation", r"resign|steps down|quits|sacked|ousted|\bexits?\b as"),
    ("lease_licence", r"\blease\b|licen[cs]e|concession|land allot"),
    ("tender", r"\btender\b|\bbid\b|\bauction\b"),
    ("gazette", r"gazette|notification|ordinance|ministry|cabinet approves"),
    ("plant_shutdown", r"shut ?down|plant closure|halts? (?:production|operations)|suspends? (?:production|operations)|lockout"),
    ("fire", r"\bfire\b|\bblaze\b|explosion|\bblast\b"),
    ("strike", r"\bstrike\b|\bprotest|agitation"),
    ("penalty", r"penalt|\bfine[ds]?\b|show.cause|\bprobe\b|investigation|subpoena|lawsuit|class action"),
]
MATERIAL_RX = [(n, re.compile(p, re.I)) for n, p in MATERIAL]
AGENCY_RX = re.compile(r"crisil|\bicra\b|\bcare ?(?:ratings|edge)\b|india ratings|ind-ra|acuit[eé]|brickwork|infomerics", re.I)


# ---------------------------------------------------------------- HTTP
def fetch(url):
    """GET via curl with per-host pacing and back-off. Returns (status, text, note). Never raises."""
    host = urllib.parse.urlparse(url).hostname or ""
    err = ""
    for i in range(3):
        wait = GAP.get(host, DEFAULT_GAP) - (time.time() - _last.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        _last[host] = time.time()
        cmd = ["curl", "-sS", "-m", "45", "--compressed", "-L", "-A", UA, "-H", "Accept-Language: en-IN,en;q=0.9",
               "-w", "\n%{http_code}", url]
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=70)
            body, _, code = r.stdout.rpartition(b"\n")
            code = int(code.decode().strip() or 0)
            txt = body.decode("utf-8-sig", "replace")
        except (subprocess.TimeoutExpired, OSError, ValueError) as e:
            code, txt, err = 0, "", str(e)
        if code == 200 and ANTIBOT.search(txt[:20000]) and "sebi.gov.in" not in host:
            return code, "", "anti-bot challenge: skipped"
        if code == 200:
            return code, txt, ""
        if code in (403,) and ANTIBOT.search(txt[:20000]):
            return code, "", "anti-bot challenge: skipped"
        err = err or f"HTTP {code}"
        if code not in (0, 429, 500, 502, 503, 504):
            break
        if i < 2:
            back = 10 * 2 ** i
            log.warning("%s failed (%s); retry in %ss", url[:110], err, back)
            time.sleep(back)
    return code, "", err


# ---------------------------------------------------------------- parsing
def parse_rss(txt):
    """RSS 2.0 -> [{title, link, pub (aware dt or None), publisher}]"""
    out = []
    try:
        root = ET.fromstring(txt.lstrip("﻿").strip())
    except ET.ParseError as e:
        log.warning("RSS parse error: %s", e)
        return out
    for it in root.iter("item"):
        title = html.unescape((it.findtext("title") or "").strip())
        pub = None
        try:
            pub = email.utils.parsedate_to_datetime(it.findtext("pubDate") or "")
            if pub and pub.tzinfo is None:
                pub = pub.replace(tzinfo=dt.timezone.utc)
        except (TypeError, ValueError):
            pass
        src = (it.findtext("source") or "").strip()
        if src and title.endswith(" - " + src):
            title = title[: -len(src) - 3]
        out.append({"title": title, "link": (it.findtext("link") or "").strip(), "pub": pub, "publisher": src})
    return out


SEBI_ROW = re.compile(r"<td>\s*(\w{3} \d{1,2}, \d{4})\s*</td>.*?<a href=\"([^\"]+)\"[^>]*title=\"([^\"]*)\"", re.S)


def parse_sebi(txt):
    out = []
    for d, link, title in SEBI_ROW.findall(txt):
        try:
            pub = dt.datetime.strptime(d, "%b %d, %Y").replace(tzinfo=IST)
        except ValueError:
            pub = None
        out.append({"title": html.unescape(title).strip(), "link": link, "pub": pub, "publisher": "SEBI"})
    return out


def gnews_url(q, days, market):
    q = f"{q} when:{max(1, days)}d"
    ed = {"hl": "en-US", "gl": "US", "ceid": "US:en"} if market == "US" else {"hl": "en-IN", "gl": "IN", "ceid": "IN:en"}
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q, **ed})


# ---------------------------------------------------------------- watchlist + matching
def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f) if (r.get("ticker") or r.get("sector"))]


def split(s):
    return [x.strip() for x in (s or "").split(";") if x.strip()]


def prep_watchlist(rows):
    for r in rows:
        r["market"] = "US" if r["ticker"].startswith("US-") else "IN"
        base = re.sub(r"\s+(Ltd|Limited|Inc|Corp|Corporation)\.?$", "", r["name"], flags=re.I)
        # the name without Ltd/Inc is only used when still 2+ words ("Kirby Corporation" must not become "Kirby")
        terms = [r["name"]] + ([base] if " " in base.strip() else []) + split(r.get("aliases"))
        # India tickers of 5+ letters are distinctive enough to search and match on (NSE codes)
        if r["market"] == "IN" and len(r["ticker"]) >= 5:
            terms.append(r["ticker"])
        seen, uniq = set(), []
        for t in terms:
            if t and t.lower() not in seen:
                seen.add(t.lower())
                uniq.append(t)
        r["terms"] = uniq
        r["rx"] = re.compile(r"(?<![A-Za-z0-9])(?:" + "|".join(re.escape(t) for t in uniq) + r")(?![A-Za-z0-9])", re.I)
        r["kw_rx"] = (re.compile("|".join(re.escape(k) for k in split(r.get("keywords"))), re.I)
                      if split(r.get("keywords")) else None)
    return rows


def company_query(r):
    return " OR ".join(f'"{t}"' if " " in t or not t.isalnum() or r["market"] == "US" else t for t in r["terms"])


def material_rules(title):
    return [n for n, rx in MATERIAL_RX if rx.search(title)]


def norm_title(t):
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def canon_url(u):
    p = urllib.parse.urlsplit(u)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query) if not k.lower().startswith(("utm_", "oc", "hl", "gl", "ceid"))]
    return urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), p.path.rstrip("/"), urllib.parse.urlencode(q), ""))


# ---------------------------------------------------------------- state
def open_db(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    con = sqlite3.connect(path, timeout=60)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("PRAGMA synchronous=NORMAL")
    con.executescript("""
      CREATE TABLE IF NOT EXISTS seen(key TEXT PRIMARY KEY, first_seen TEXT);
      CREATE TABLE IF NOT EXISTS items(id TEXT PRIMARY KEY, first_seen TEXT, pub TEXT, ticker TEXT, source TEXT,
        headline TEXT, url TEXT, matched_rule TEXT, material INTEGER, direct INTEGER, publisher TEXT);
      CREATE INDEX IF NOT EXISTS ix_items_seen ON items(first_seen);
      CREATE TABLE IF NOT EXISTS runs(run_at TEXT, source TEXT, requests INTEGER, items INTEGER, new INTEGER, note TEXT);""")
    return con


# ---------------------------------------------------------------- collection
class Run:
    def __init__(self, con, since, day):
        self.con, self.since, self.day = con, since, day
        self.items, self.status = {}, {}
        self.keyidx = {}

    def note(self, src, ok=True, n=0, msg=""):
        s = self.status.setdefault(src, {"requests": 0, "fail": 0, "raw": 0, "new": 0, "notes": []})
        s["requests"] += 1
        s["fail"] += 0 if ok else 1
        s["raw"] += n
        if msg and msg not in s["notes"]:
            s["notes"].append(msg)

    def add(self, src, it, tickers, rules, direct):
        if it["pub"] and it["pub"] < self.since:
            return
        if not it["title"] or not it["link"]:
            return
        tk = ";".join(tickers)
        keys = ["u:" + canon_url(it["link"]), "t:" + hashlib.sha1((norm_title(it["title"]) + "|" + tk).encode()).hexdigest()]
        iid = hashlib.sha1(keys[0].encode()).hexdigest()[:16]
        # same story found by two queries in this run: merge tickers/rules into the first copy
        for k in keys:
            prev = self.items.get(self.keyidx.get(k, ""))
            if prev:
                    for t in tickers:
                        if t not in prev["tickers"]:
                            prev["tickers"].append(t)
                    for r_ in rules:
                        if r_ not in prev["rules"]:
                            prev["rules"].append(r_)
                    prev["direct"] = prev["direct"] or direct
                    return
        if any(self.con.execute("SELECT 1 FROM seen WHERE key=?", (k,)).fetchone() for k in keys):
            return  # reported on an earlier run
        mat = material_rules(it["title"])
        for k in keys:
            self.keyidx[k] = iid
        self.items[iid] = {"id": iid, "_keys": keys, "pub": it["pub"], "tickers": list(tickers), "source": src,
                           "headline": it["title"], "url": it["link"], "rules": mat + [r for r in rules if r not in mat],
                           "material": bool(mat), "direct": direct, "publisher": it.get("publisher", "")}
        self.status.setdefault(src, {"requests": 0, "fail": 0, "raw": 0, "new": 0, "notes": []})["new"] += 1


def match_companies(wl, title):
    return [r for r in wl if r["rx"].search(title)]


def collect(run, wl, policy, sources, days, fetcher=fetch):
    blocked = set()

    def get(src, url, host_key):
        if host_key in blocked:
            run.note(src, False, 0, f"{host_key} skipped after anti-bot/rate-limit response")
            return None
        code, txt, note = fetcher(url)
        if note.startswith("anti-bot") or code == 429:
            blocked.add(host_key)
            log.warning("%s: %s (%s) - skipping this host for the rest of the run", src, note or code, url[:100])
        run.note(src, bool(txt), 0, note)
        return txt or None

    if "google" in sources:
        for r in wl:
            txt = get("google_news", gnews_url(company_query(r), days, r["market"]), "google")
            if not txt:
                continue
            items = parse_rss(txt)
            run.status["google_news"]["raw"] += len(items)
            for it in items:
                direct = bool(r["rx"].search(it["title"]))
                rules = ["name"] if direct else ["query_only"]
                if r["kw_rx"] and r["kw_rx"].search(it["title"]):
                    rules.append("watch_keyword")
                if AGENCY_RX.search(it["title"]):
                    rules.append("rating")
                run.add("google_news", it, [r["ticker"]], rules, direct)

    if "ratings" in sources:
        txt = get("ratings_news", gnews_url(RATING_QUERY, days, "IN"), "google")
        if txt:
            items = parse_rss(txt)
            run.status["ratings_news"]["raw"] += len(items)
            for it in items:
                hits = [r["ticker"] for r in match_companies(wl, it["title"]) if r["market"] == "IN"]
                if hits:
                    run.add("ratings_news", it, hits, ["rating"], True)

    if "sebi" in sources:
        for src, url in SEBI_LISTS.items():
            txt = get(src, url, "sebi")
            if not txt:
                continue
            items = parse_sebi(txt)
            run.status[src]["raw"] += len(items)
            if not items:
                run.note(src, False, 0, "0 rows parsed: listing layout changed?")
            for it in items:
                hits = [r["ticker"] for r in match_companies(wl, it["title"]) if r["market"] == "IN"]
                if hits:
                    run.add(src, it, hits, ["sebi"], True)

    lenders = [r["ticker"] for r in wl if r["sector"] == "lender"]
    lender_rx = re.compile(r"small finance bank|microfinance|\bnbfc|risk weight|monetary penalty|"
                           r"directions?,? 20\d\d|payments bank|co-lending|digital lending", re.I)
    if "rbi" in sources:
        txt = get("rbi_press", RBI_RSS, "rbi")
        if txt:
            items = parse_rss(txt)
            run.status["rbi_press"]["raw"] += len(items)
            for it in items:
                hits = [r["ticker"] for r in match_companies(wl, it["title"]) if r["market"] == "IN"]
                if hits:
                    run.add("rbi_press", it, hits, ["rbi"], True)
                elif lenders and lender_rx.search(it["title"]):
                    run.add("rbi_press", it, lenders, ["policy:lender"], False)

    if "policy" in sources:
        sectors_in_wl = {r["sector"] for r in wl}
        for p in policy:
            if p["sector"] not in sectors_in_wl:
                continue
            tick = [r["ticker"] for r in wl if r["sector"] == p["sector"]]
            market = "US" if p["sector"].startswith("us") else "IN"
            txt = get("policy_news", gnews_url(p["query"], days, market), "google")
            if not txt:
                continue
            items = parse_rss(txt)
            run.status["policy_news"]["raw"] += len(items)
            for it in items:
                hits = [r["ticker"] for r in match_companies(wl, it["title"])]
                run.add("policy_news", it, sorted(set(tick + hits)), [f"policy:{p['sector']}:{p['label']}"], bool(hits))


# ---------------------------------------------------------------- output
def rank(it, tiers):
    live = any(tiers.get(t) == "live" for t in it["tickers"])
    policy = any(r.startswith("policy:") for r in it["rules"]) and not it["direct"]
    group = (0 if it["material"] and it["direct"] and not policy else 1 if it["material"] and not policy
             else 2 if policy and it["material"] else 3 if policy else 4 if it["direct"] else 5)
    pub = it["pub"].timestamp() if it["pub"] else 0
    return (group, 0 if live else 1, -pub)


def write_outputs(run, out_dir, wl, max_other=4):
    tiers = {r["ticker"]: r.get("tier", "") for r in wl}
    names = {r["ticker"]: r["name"] for r in wl}
    items = sorted(run.items.values(), key=lambda i: rank(i, tiers))
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, run.day.isoformat())

    def pub_s(i):
        return i["pub"].astimezone(IST).strftime("%Y-%m-%d %H:%M") if i["pub"] else ""

    with open(base + ".csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date", "ticker", "source", "headline", "url", "matched_rule"])
        for i in items:
            w.writerow([pub_s(i), ";".join(i["tickers"]), i["source"], i["headline"], i["url"], ";".join(i["rules"])])

    def line(i):
        tk = ", ".join(f"{names.get(t, t)} ({t})" for t in i["tickers"][:4]) + (" +more" if len(i["tickers"]) > 4 else "")
        pubr = f" ({i['publisher']})" if i["publisher"] else ""
        return f"- {pub_s(i)} | **{tk}** | [{i['headline']}]({i['url']}){pubr} | `{';'.join(i['rules'])}` | {i['source']}"

    md = [f"# FEIN news - {run.day.isoformat()}", "",
          f"Window: items published since {run.since.astimezone(IST).strftime('%Y-%m-%d %H:%M')} IST. "
          f"New items this run: {len(items)} (each item is reported once; earlier ones are in news.sqlite). "
          "Research, not SEBI-registered advice: an item means 'read the source', not 'trade'.", ""]
    pol = lambda i: any(r.startswith("policy:") for r in i["rules"]) and not i["direct"]  # noqa: E731
    groups = [("Material, headline names the company", lambda i: i["material"] and i["direct"] and not pol(i)),
              ("Material keyword, company search hit but headline does not name it (often noise)",
               lambda i: i["material"] and not i["direct"] and not pol(i)),
              ("Policy watch (material-keyword items first)", pol),
              ("Other company news (max %d per ticker here, headline names the company; all rows in the CSV)" % max_other,
               lambda i: not i["material"] and not pol(i))]
    for title, pred in groups:
        sel = [i for i in items if pred(i)]
        md += [f"## {title} ({len(sel)})", ""]
        if "Other" in title:
            per, kept = {}, []
            for i in sel:
                k = i["tickers"][0]
                per[k] = per.get(k, 0) + 1
                if per[k] <= max_other and i["direct"]:
                    kept.append(i)
            sel = kept
        md += [line(i) for i in sel] or ["- none"]
        md.append("")
    md += ["## Sources this run", "", "| source | requests | failed | rows read | new items | notes |", "|---|---|---|---|---|---|"]
    for s, v in sorted(run.status.items()):
        md.append(f"| {s} | {v['requests']} | {v['fail']} | {v['raw']} | {v['new']} | {'; '.join(v['notes'][:3])} |")
    md += ["", "Not automated (by rule or because they cannot be fetched politely):", ""]
    md += [f"- {a}: {b}" for a, b in SKIPPED]
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(md) + "\n")
    return base, items


def commit(run, items):
    now = dt.datetime.now(IST).isoformat(timespec="seconds")
    for i in items:
        for k in i["_keys"]:
            run.con.execute("INSERT OR IGNORE INTO seen VALUES(?,?)", (k, now))
        run.con.execute("INSERT OR REPLACE INTO items VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                        (i["id"], now, i["pub"].isoformat() if i["pub"] else "", ";".join(i["tickers"]), i["source"],
                         i["headline"], i["url"], ";".join(i["rules"]), int(i["material"]), int(i["direct"]), i["publisher"]))
    for s, v in run.status.items():
        run.con.execute("INSERT INTO runs VALUES(?,?,?,?,?,?)", (now, s, v["requests"], v["raw"], v["new"], "; ".join(v["notes"])[:500]))
    run.con.commit()


def parse_since(s, now):
    m = re.fullmatch(r"(\d+)([dh])", s.strip())
    if m:
        n = int(m.group(1))
        return now - (dt.timedelta(days=n) if m.group(2) == "d" else dt.timedelta(hours=n))
    return dt.datetime.fromisoformat(s).replace(tzinfo=IST)


def run_all(args, out_dir, db_path, fetcher=fetch, now=None):
    now = now or dt.datetime.now(IST)
    since = parse_since(args.since, now)
    days = max(1, -(-int((now - since).total_seconds()) // 86400))
    wl = prep_watchlist(load_csv(args.watchlist))
    if args.tickers:
        want = {t.strip().upper() for t in args.tickers.split(",")}
        wl = [r for r in wl if r["ticker"].upper() in want]
    policy = load_csv(args.policy)
    sources = set(args.sources.split(",")) if args.sources else set(SOURCES)
    con = open_db(db_path)
    run = Run(con, since, now.astimezone(IST).date())
    collect(run, wl, policy, sources, days, fetcher)
    base, items = write_outputs(run, out_dir, wl)
    commit(run, items)
    return run, base, items


# ---------------------------------------------------------------- selftest (offline)
def _rss(items):
    body = "".join(f"<item><title>{html.escape(t)} - {p}</title><link>{l}</link><pubDate>{d}</pubDate>"
                   f"<source url=\"https://x\">{p}</source></item>" for t, l, d, p in items)
    return f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>t</title>{body}</channel></rss>'


def selftest():
    now = dt.datetime(2026, 11, 25, 22, 30, tzinfo=IST)
    fresh = email.utils.format_datetime(now - dt.timedelta(hours=5))
    old = email.utils.format_datetime(now - dt.timedelta(days=9))
    fx = {
        "Uttam": _rss([("Supreme Court stays UP cane price order; Uttam Sugar Mills shares fall", "https://n/a1", fresh, "ET"),
                       ("Uttam Sugar Mills Q2 results: profit up", "https://n/a2", fresh, "BS"),
                       ("Uttam Sugar old story", "https://n/a3", old, "BS")]),
        "Kirby": _rss([("Kirby Corp to present at conference", "https://n/k1", fresh, "PR"),
                       ("Barge fire on the Houston Ship Channel", "https://n/k2", fresh, "AP")]),
        "CRISIL": _rss([("CRISIL downgrades Utkarsh Small Finance Bank outlook to negative", "https://n/r1", fresh, "Mint"),
                        ("ICRA reaffirms rating of some unrelated company", "https://n/r2", fresh, "Mint")]),
        "ethanol": _rss([("OMCs float ethanol tender for ESY 2026-27; cane juice excluded", "https://n/p1", fresh, "ET"),
                         ("Supreme Court stays UP cane price order; Uttam Sugar Mills shares fall", "https://n/a1", fresh, "ET")]),
        "sebi.gov.in": ("<tr role='row'><td>Nov 25, 2026</td><td>1/2026</td><td><a href=\"https://www.sebi.gov.in/o1.html\" "
                        "target=\"_blank\" title=\"Adjudication order in the matter of Uttam Sugar Mills Limited\">x</a></td></tr>"
                        "<tr role='row'><td>Nov 24, 2026</td><td>2/2026</td><td><a href=\"https://www.sebi.gov.in/o2.html\" "
                        "title=\"Order in the matter of Someone Else\">y</a></td></tr>"),
        "rbi.org.in": _rss([("RBI imposes monetary penalty on Utkarsh Small Finance Bank Limited", "https://rbi/1", fresh, "RBI"),
                            ("RBI issues draft directions on microfinance loans", "https://rbi/2", fresh, "RBI"),
                            ("Money supply for the fortnight", "https://rbi/3", fresh, "RBI")]),
    }

    def fake(url):
        u = urllib.parse.unquote_plus(url)
        if "sebi.gov.in" in u:
            return 200, fx["sebi.gov.in"] if "sid=2" in u else "", ""
        for k in ("rbi.org.in", "CRISIL", "ethanol", "Uttam", "Kirby"):
            if k in u:
                return 200, fx[k], ""
        return 200, _rss([]), ""

    tmp = tempfile.mkdtemp(prefix="fein-news-selftest-")
    wl = os.path.join(tmp, "wl.csv")
    with open(wl, "w") as f:
        f.write("ticker,name,sector,keywords,aliases,tier\nUTTAMSUGAR,Uttam Sugar Mills,sugar,cane price,Uttam Sugar,live\n"
                "UTKARSHBNK,Utkarsh Small Finance Bank,lender,,Utkarsh SFB,live\nUS-KEX,Kirby Corporation,us_marine,,Kirby Corp,live\n")
    pol = os.path.join(tmp, "pol.csv")
    with open(pol, "w") as f:
        f.write("sector,label,query\nsugar,ethanol tender/OMC,ethanol tender OMC\n")
    a = argparse.Namespace(since="2d", watchlist=wl, policy=pol, tickers="", sources="")
    checks = []
    run, base, items = run_all(a, tmp, os.path.join(tmp, "news.sqlite"), fake, now)
    by = {i["headline"]: i for i in items}
    sc = "Supreme Court stays UP cane price order; Uttam Sugar Mills shares fall"
    checks += [("publisher suffix stripped, court rule", sc in by and by[sc]["rules"][0] == "court"),
                ("story found twice is reported once, tickers merged", sum(i["url"] == "https://n/a1" for i in items) == 1),
                ("--since drops 9-day-old item", "Uttam Sugar old story" not in by),
                ("material+direct ranked first", items[0]["headline"] == sc),
                ("rating item matched to UTKARSHBNK", any(i["source"] == "ratings_news" and i["tickers"] == ["UTKARSHBNK"] for i in items)),
                ("unmatched rating item dropped", not any("unrelated" in i["headline"] for i in items)),
                ("SEBI order matched by name", any(i["source"] == "sebi_order" and "UTTAMSUGAR" in i["tickers"] for i in items)),
                ("SEBI other-company order dropped", not any("Someone Else" in i["headline"] for i in items)),
                ("RBI penalty matched to lender", any(i["url"] == "https://rbi/1" and i["tickers"] == ["UTKARSHBNK"] for i in items)),
                ("RBI microfinance item -> policy:lender", any(i["url"] == "https://rbi/2" and "policy:lender" in i["rules"] for i in items)),
                ("RBI routine item dropped", not any(i["url"] == "https://rbi/3" for i in items)),
                ("policy item tagged to sector", any(i["url"] == "https://n/p1" and i["rules"][0] in ("tender", "policy:sugar:ethanol tender/OMC") for i in items)),
                ("Kirby fire item not 'direct'", any(i["url"] == "https://n/k2" and not i["direct"] for i in items)),
                ("csv + md written", os.path.exists(base + ".csv") and os.path.exists(base + ".md"))]
    with open(base + ".csv") as f:
        head = f.readline().strip()
    checks.append(("csv header", head == "date,ticker,source,headline,url,matched_rule"))
    run2, _, items2 = run_all(a, tmp, os.path.join(tmp, "news.sqlite"), fake, now)
    checks.append(("second run reports nothing new", len(items2) == 0))

    def blocked(url):
        return 200, "", "anti-bot challenge: skipped"
    run3, _, items3 = run_all(a, os.path.join(tmp, "b"), os.path.join(tmp, "b.sqlite"), blocked, now)
    checks.append(("anti-bot host skipped after first hit", run3.status["google_news"]["fail"] == 3 and len(items3) == 0))
    checks.append(("material regex: 'fire' not in 'firepower'", "fire" not in material_rules("Firepower boost for defence")))
    for name, ok in checks:
        print(("PASS " if ok else "FAIL ") + name)
    bad = sum(not ok for _, ok in checks)
    print(f"selftest: {len(checks) - bad}/{len(checks)} passed (temp dir {tmp})")
    return 1 if bad else 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--since", default="2d", help="window: Nd, Nh or YYYY-MM-DD (default 2d)")
    p.add_argument("--tickers", default="", help="comma list to limit the watchlist")
    p.add_argument("--sources", default="", help="comma list from " + ",".join(SOURCES))
    p.add_argument("--watchlist", default=os.path.join(HERE, "watchlist.csv"))
    p.add_argument("--policy", default=os.path.join(HERE, "policy.csv"))
    p.add_argument("--out", default=os.path.join(DATA, "news"))
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        logging.basicConfig(level=logging.ERROR)
        return selftest()
    setup_logging("news")
    lock = single_instance("news")
    if lock is None:
        log.error("another news.py is running")
        return 1
    run, base, items = run_all(a, a.out, os.path.join(a.out, "news.sqlite"))
    mat = sum(i["material"] for i in items)
    log.info("news: %d new items (%d material) -> %s.md/.csv", len(items), mat, base)
    for s, v in sorted(run.status.items()):
        log.info("  %-12s requests=%d failed=%d rows=%d new=%d %s", s, v["requests"], v["fail"], v["raw"], v["new"], "; ".join(v["notes"]))
    failed_all = run.status and all(v["fail"] == v["requests"] for v in run.status.values())
    return 2 if failed_all else 0


if __name__ == "__main__":
    sys.exit(main())
