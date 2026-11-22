"""Shared helpers for the Lazy Prices US replication (stage 3). Standard library only."""
import gzip, json, os, threading, time, urllib.request, urllib.error

BASE = os.environ.get("BT_DIR", "/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_lazy")
UA = os.environ.get("SEC_UA", "fein-research admin@example.com")
GAP = 0.25  # ~4 requests/s to SEC (gentler than the 10/s limit)
_last = [0.0]
_lock = threading.Lock()


def p(*a):
    return os.path.join(BASE, *a)


def sec_raw(url, gap=GAP, tries=6):
    """GET bytes from SEC, polite global spacing. Returns None on 404."""
    for i in range(tries):
        with _lock:
            slot = max(time.time(), _last[0] + gap)
            _last[0] = slot
        w = slot - time.time()
        if w > 0:
            time.sleep(w)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=120) as r:
                data = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if i < tries - 1:
                time.sleep(2 ** i + (10 if e.code in (429, 503) else 0)); continue
            raise
        except Exception:
            if i < tries - 1:
                time.sleep(2 ** i); continue
            raise


def sec_json(url, path=None):
    if path and os.path.exists(path):
        return json.load(open(path))
    b = sec_raw(url)
    d = json.loads(b) if b else None
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json.dump(d, open(path, "w"))
    return d


def excluded_sic(sic):
    try:
        s = int(sic)
    except (TypeError, ValueError):
        return True
    return 6000 <= s <= 6799 or 4900 <= s <= 4999
