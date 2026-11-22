#!/usr/bin/env bash
# Apply scoreboard resolution seeds to memdb (python3 -m memdb add --json-file ...), then refresh the scoreboard.
#   tools/scoreboard/apply.sh            # every memdb/seeds/*_scoreboard_resolutions*.json not yet applied
#   tools/scoreboard/apply.sh FILE.json  # just this seed
# "Applied" is decided from memdb itself (stateless): a seed is skipped when every id in it already has the
# seed's status and resolved_on. Same id = update; old versions stay in memory/store/*.jsonl.
set -euo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO"
if [ "$#" -gt 0 ]; then seeds=("$@"); else shopt -s nullglob; seeds=(memdb/seeds/*_scoreboard_resolutions*.json); fi
applied=0
for f in "${seeds[@]}"; do
  python3 -c "import json,sys; d=json.load(open(sys.argv[1])); assert isinstance(d, list) and all(r.get('id') and r.get('type')=='thesis' for r in d)" "$f" \
    || { echo "apply.sh: $f is not a valid resolution seed, skipped" >&2; continue; }
  if python3 - "$f" <<'PY'
import json, sys
sys.path.insert(0, ".")
from memdb import core
con = core.connect()
for r in json.load(open(sys.argv[1])):
    cur = core.get(con, r["id"]) or {}
    if cur.get("status") != r.get("status") or (cur.get("data") or {}).get("resolved_on") != r["data"].get("resolved_on"):
        sys.exit(1)          # something still to apply
sys.exit(0)
PY
  then echo "apply.sh: $f already applied"; continue; fi
  python3 -m memdb add --json-file "$f"
  applied=$((applied + 1))
done
echo "apply.sh: applied $applied seed file(s)"
python3 tools/scoreboard/scoreboard.py
