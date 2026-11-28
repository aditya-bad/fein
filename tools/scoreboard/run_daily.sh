#!/usr/bin/env bash
# Nightly paper-call pipeline (cron, 22:00 IST): export -> resolve -> apply -> scoreboard. Logs to state/.
#   SB_AUTO_APPLY=0  write seeds and the review queue but do not touch memdb (look first, then apply.sh)
#   SB_GIT_COMMIT=1  commit memdb/research_notes/curriculum changes locally after a run (never pushes)
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO"
mkdir -p tools/scoreboard/state
LOG="tools/scoreboard/state/run_$(TZ=Asia/Kolkata date +%Y-%m-%d).log"
exec >>"$LOG" 2>&1
echo "=== $(TZ=Asia/Kolkata date -Iseconds) run_daily start"
# one run at a time (a slow NSE night must not overlap the next cron)
exec 9>tools/scoreboard/state/.lock
flock -n 9 || { echo "another run holds the lock; exiting"; exit 0; }
FAIL=0
python3 tools/scoreboard/calls.py || { echo "calls.py failed"; FAIL=1; }
python3 tools/scoreboard/resolve.py || { echo "resolve.py failed"; FAIL=1; }
if [ "${SB_AUTO_APPLY:-1}" = "1" ]; then
  tools/scoreboard/apply.sh || { echo "apply.sh failed"; FAIL=1; }
else
  python3 tools/scoreboard/scoreboard.py || { echo "scoreboard.py failed"; FAIL=1; }
fi
if [ "${SB_GIT_COMMIT:-0}" = "1" ] && ! git diff --quiet -- memory research_notes/Scoreboard memdb/seeds; then
  git add memory/store memory/curriculum.md research_notes/Scoreboard memdb/seeds/*_scoreboard_resolutions*.json 2>/dev/null
  git commit -q -m "scoreboard: nightly resolver run $(TZ=Asia/Kolkata date +%Y-%m-%d)" || true
fi
echo "=== $(TZ=Asia/Kolkata date -Iseconds) run_daily end (fail=$FAIL)"
# non-zero exit so systemd/healthcheck see a failed step (before 28-Nov-2026 failures were swallowed)
exit $FAIL
