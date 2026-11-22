"""Shared helpers for the US solvency-flag back-test (stage 2). Standard library + numpy only."""
import gzip, json, os, threading, time, urllib.request, urllib.error

BASE = os.environ.get("BT_DIR", "/tmp/claude-0/-home-user-fein/5b06430f-c120-564f-b9b0-6102d4d6d193/scratchpad/bt_solvency")
UA = os.environ.get("SEC_UA", "fein-research admin@example.com")
SNAPS = ["2015-06-30", "2017-06-30", "2019-06-30"]
_last = [0.0]
_lock = threading.Lock()


def sec_get(url, path=None, gap=0.13, tries=6):
    """GET JSON from SEC with polite spacing; cache to path if given. Returns dict or None on 404."""
    if path and os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    for i in range(tries):
        with _lock:  # reserve a global slot: total rate <= 1/gap across threads
            slot = max(time.time(), _last[0] + gap)
            _last[0] = slot
        w = slot - time.time()
        if w > 0:
            time.sleep(w)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    data = gzip.decompress(data)
            d = json.loads(data)
            break
        except urllib.error.HTTPError as e:
            if e.code == 404:
                d = None; break
            if i < tries - 1:
                time.sleep(2 ** i); continue
            raise
        except Exception:
            if i < tries - 1:
                time.sleep(2 ** i); continue
            raise
    if path:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(d, f)
    return d


def p(*a):
    return os.path.join(BASE, *a)
