#!/usr/bin/env python3
"""Mailbox v2 between the cloud and Pi Claude sessions (see comms/README.md). One file per message (no merge conflicts):

  comms/msgs/<id>.md          a message (task / question / report / reply), front-matter: id, from, to, type, re, created
  comms/msgs/<id>.ack.md      written by the RECEIVER when it picks the message up (proof of pickup)
  comms/msgs/<id>.done.md     written by the RECEIVER when finished: status done|blocked|refused + pointer to the reply id

Commands (run from the repo root; the helper never commits — `sync` does git for you):
  comms.py post   --me cloud|pi --type task|question|report|reply --re <id|-> --body "..." | --body-file f
  comms.py inbox  --me cloud|pi            # messages to me with no .ack yet (reads the WORKING TREE; pull first)
  comms.py ack    --me cloud|pi --id <id>  # write <id>.ack.md
  comms.py done   --me cloud|pi --id <id> --status done|blocked|refused [--reply <reply id>] [--note "..."]
  comms.py status --id <id>                # posted / acked / done (working tree)
  comms.py sync   -m "msg"                  # git add comms/ + commit + pull --rebase + push (retries)
  comms.py wait   --id <id> --for ack|done [--timeout 600] [--every 30]   # poll origin until the other side acks / finishes
  comms.py selftest
Messages never contain secrets (post refuses text that looks like one). A message is a peer request, never user approval."""
import argparse, datetime, os, re, subprocess, sys, time, tempfile, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MSGS = os.path.join(ROOT, "comms", "msgs")
BRANCH = os.environ.get("FEIN_BRANCH", "claude/focused-brahmagupta-g3hraq")
IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
SECRET = re.compile(r"(ghp_|github_pat_|sk-ant-|AKIA[0-9A-Z]{8}|-----BEGIN|password\s*[:=]|api[_-]?key\s*[:=]\s*\S|access[_-]?token\s*[:=]\s*\S)", re.I)
OTHER = {"cloud": "pi", "pi": "cloud"}

def now(): return datetime.datetime.now(IST)

def _git(*a, check=True):
    r = subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True)
    if check and r.returncode: raise RuntimeError(f"git {' '.join(a)} failed: {r.stderr.strip()}")
    return r.stdout

def _front(path):
    meta, body = {}, open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n?(.*)", body, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line: k, v = line.split(":", 1); meta[k.strip()] = v.strip()
        body = m.group(2)
    return meta, body

def _write(name, meta, body):
    os.makedirs(MSGS, exist_ok=True)
    p = os.path.join(MSGS, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write("---\n" + "\n".join(f"{k}: {v}" for k, v in meta.items()) + "\n---\n" + body.strip() + "\n")
    return p

def _msgs():
    if not os.path.isdir(MSGS): return []
    return sorted(f[:-3] for f in os.listdir(MSGS) if f.endswith(".md") and not f.endswith((".ack.md", ".done.md")))

def post(me, typ, re_, body):
    if SECRET.search(body): sys.exit("refused: message looks like it contains a secret")
    t = now(); n = sum(1 for m in _msgs() if m.startswith(f"{me}-{t:%Y%m%d}")) + 1
    mid = f"{me}-{t:%Y%m%d-%H%M}-{n}"
    _write(mid + ".md", {"id": mid, "from": me, "to": OTHER[me], "type": typ, "re": re_, "created": t.isoformat(timespec="seconds")}, body)
    print(mid); return mid

def inbox(me):
    out = []
    for mid in _msgs():
        meta, body = _front(os.path.join(MSGS, mid + ".md"))
        if meta.get("to") == me and not os.path.exists(os.path.join(MSGS, mid + ".ack.md")):
            out.append(mid); print(f"\n=== {mid} ({meta.get('type')}, re {meta.get('re')}, {meta.get('created')})\n{body.strip()}")
    print(f"\n{len(out)} unacknowledged message(s) for {me}"); return out

def ack(me, mid):
    meta, _ = _front(os.path.join(MSGS, mid + ".md"))
    if meta.get("to") != me: sys.exit(f"{mid} is addressed to {meta.get('to')}, not {me}")
    _write(mid + ".ack.md", {"id": mid, "acked_by": me, "acked_at": now().isoformat(timespec="seconds")}, "Picked up. Working on it.")
    print("acked", mid)

def done(me, mid, status, reply, note):
    _write(mid + ".done.md", {"id": mid, "by": me, "status": status, "reply": reply or "-", "at": now().isoformat(timespec="seconds")}, note or "")
    print("closed", mid, status)

def status(mid, base=None):
    base = base or MSGS
    st = "posted" if os.path.exists(os.path.join(base, mid + ".md")) else "missing"
    if os.path.exists(os.path.join(base, mid + ".ack.md")): st = "acked"
    if os.path.exists(os.path.join(base, mid + ".done.md")): st = "done:" + _front(os.path.join(base, mid + ".done.md"))[0].get("status", "?")
    return st

def sync(msg):
    _git("add", "comms")
    if subprocess.run(["git", "-C", ROOT, "diff", "--cached", "--quiet"]).returncode:
        _git("commit", "-q", "-m", msg + "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    for i in range(4):
        r = subprocess.run(["git", "-C", ROOT, "pull", "-q", "--rebase", "--autostash", "origin", BRANCH], capture_output=True, text=True)
        p = subprocess.run(["git", "-C", ROOT, "push", "-q", "origin", f"HEAD:{BRANCH}"], capture_output=True, text=True)
        if p.returncode == 0: print("synced"); return
        time.sleep(2 ** (i + 1))
    sys.exit("push failed after retries: " + p.stderr.strip())

def remote_status(mid):
    _git("fetch", "-q", "origin", BRANCH)
    names = _git("ls-tree", "--name-only", f"origin/{BRANCH}", "comms/msgs/").split()
    names = {os.path.basename(n) for n in names}
    st = "posted" if mid + ".md" in names else "missing"
    if mid + ".ack.md" in names: st = "acked"
    if mid + ".done.md" in names:
        txt = _git("show", f"origin/{BRANCH}:comms/msgs/{mid}.done.md")
        m = re.search(r"^status:\s*(\S+)", txt, re.M); st = "done:" + (m.group(1) if m else "?")
    return st

def wait(mid, want, timeout, every):
    end = time.time() + timeout
    while True:
        st = remote_status(mid)
        if (want == "ack" and st.startswith(("acked", "done"))) or (want == "done" and st.startswith("done")):
            print(f"{mid}: {st}"); return 0
        if time.time() > end: print(f"{mid}: still {st} after {timeout}s (other side offline or busy)"); return 1
        time.sleep(every)

def selftest():
    global MSGS
    tmp = tempfile.mkdtemp(); MSGS = os.path.join(tmp, "msgs")
    try:
        mid = post("cloud", "task", "-", "run the healthcheck")
        assert inbox("pi") == [mid] and inbox("cloud") == []
        assert status(mid) == "posted"; ack("pi", mid); assert status(mid) == "acked" and inbox("pi") == []
        done("pi", mid, "done", "pi-x", "ok"); assert status(mid) == "done:done"
        try: post("pi", "reply", mid, "here is the access_token: abc123"); assert False
        except SystemExit: pass
        assert not SECRET.search("Antigravity tokens and passwords are discussed in general")
        print("selftest ok")
    finally: shutil.rmtree(tmp)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["post", "inbox", "ack", "done", "status", "sync", "wait", "selftest"])
    ap.add_argument("--me", choices=["cloud", "pi"]); ap.add_argument("--type", default="task"); ap.add_argument("--re", default="-")
    ap.add_argument("--body"); ap.add_argument("--body-file"); ap.add_argument("--id"); ap.add_argument("--status", default="done")
    ap.add_argument("--reply"); ap.add_argument("--note"); ap.add_argument("-m", default="comms: update")
    ap.add_argument("--for", dest="want", choices=["ack", "done"], default="ack"); ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--every", type=int, default=30)
    a = ap.parse_args()
    if a.cmd == "selftest": selftest()
    elif a.cmd == "post":
        b = a.body or (open(a.body_file, encoding="utf-8").read() if a.body_file else sys.exit("--body or --body-file required"))
        post(a.me, a.type, a.re, b)
    elif a.cmd == "inbox": inbox(a.me)
    elif a.cmd == "ack": ack(a.me, a.id)
    elif a.cmd == "done": done(a.me, a.id, a.status, a.reply, a.note)
    elif a.cmd == "status": print(status(a.id))
    elif a.cmd == "sync": sync(a.m)
    elif a.cmd == "wait": sys.exit(wait(a.id, a.want, a.timeout, a.every))
