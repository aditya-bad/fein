#!/usr/bin/env python3
"""Mailbox helper for the cloud <-> Pi Claude sessions (see comms/README.md).

  python3 tools/comms/comms.py inbox --me cloud|pi          # show messages addressed to me that are new since last read
  python3 tools/comms/comms.py post --me cloud|pi --type task|reply|report|question --re <id|-> --status open|done|blocked \
        --body "text"   (or --body-file f.md)                  # append a message to the other side's file
  python3 tools/comms/comms.py ack --me cloud|pi                # mark everything currently in my inbox as read
Run `git pull` before and commit+push after (the helper never touches git). Never put secrets in a message."""
import argparse, datetime, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(ROOT, "comms")
INBOX = {"cloud": "to_cloud.md", "pi": "to_pi.md"}
OUTBOX = {"cloud": "to_pi.md", "pi": "to_cloud.md"}
HDR = re.compile(r"^## MSG (\S+) · ", re.M)
SECRET = re.compile(r"(ghp_|github_pat_|sk-ant-|AKIA|-----BEGIN|password\s*[:=]|api[_-]?key\s*[:=]|token\s*[:=])", re.I)

def _state(me):
    p = os.path.join(C, f"state_{me}.json")
    try: return p, json.load(open(p))
    except Exception: return p, {}

def _msgs(fname):
    txt = open(os.path.join(C, fname), encoding="utf-8").read()
    parts = HDR.split(txt)
    return [(parts[i], "## MSG " + parts[i] + " · " + parts[i + 1].rstrip()) for i in range(1, len(parts), 2)]

def inbox(me):
    p, st = _state(me); key = f"last_read_in_{INBOX[me][:-3]}"
    msgs = _msgs(INBOX[me]); last = st.get(key)
    ids = [m[0] for m in msgs]; start = ids.index(last) + 1 if last in ids else 0
    new = msgs[start:]
    print(f"{len(new)} new message(s) in comms/{INBOX[me]} (last read: {last})")
    for _, body in new: print("\n" + body)
    return new

def ack(me):
    p, st = _state(me); key = f"last_read_in_{INBOX[me][:-3]}"
    msgs = _msgs(INBOX[me])
    if msgs: st[key] = msgs[-1][0]
    st["updated"] = datetime.date.today().isoformat()
    json.dump(st, open(p, "w")); print("marked read up to", st.get(key))

def post(me, typ, re_, status, body):
    if SECRET.search(body): sys.exit("refused: message looks like it contains a secret")
    out = os.path.join(C, OUTBOX[me]); n = len(_msgs(OUTBOX[me])) + 1
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
    mid = f"{me}-{now:%Y%m%d}-{n}"
    with open(out, "a", encoding="utf-8") as f:
        f.write(f"\n## MSG {mid} · {now.isoformat(timespec='minutes')} · type: {typ} · re: {re_}\nStatus: {status}\n{body.strip()}\n")
    print("posted", mid, "to comms/" + OUTBOX[me])

def selftest():
    s = "x\n## MSG a-1 · t · type: task · re: -\nStatus: open\nhi\n## MSG a-2 · t · type: task · re: -\nStatus: open\nyo\n"
    parts = HDR.split(s); assert [parts[i] for i in range(1, len(parts), 2)] == ["a-1", "a-2"]
    assert SECRET.search("token: abc") and not SECRET.search("Antigravity tokens are not discussed")
    print("selftest ok")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd", choices=["inbox", "post", "ack", "selftest"])
    ap.add_argument("--me", choices=["cloud", "pi"]); ap.add_argument("--type", default="reply")
    ap.add_argument("--re", default="-"); ap.add_argument("--status", default="open")
    ap.add_argument("--body"); ap.add_argument("--body-file")
    a = ap.parse_args()
    if a.cmd == "selftest": selftest()
    elif a.cmd == "inbox": inbox(a.me)
    elif a.cmd == "ack": ack(a.me)
    else:
        b = a.body or (open(a.body_file).read() if a.body_file else sys.exit("--body or --body-file required"))
        post(a.me, a.type, a.re, a.status, b)
