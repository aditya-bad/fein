#!/usr/bin/env bash
# Runs one FEIN job for systemd or cron:  run_job.sh <job>
# - loads $FEIN_DATA/fein.env, takes a per-job lock, appends output to $FEIN_DATA/logs/<job>.out.log
# - records the result in $FEIN_DATA/logs/status/<job>.last  ("<epoch> <exit code> <start ISO> <seconds>")
# It only calls the tools as their READMEs document; it never changes their logic.
set -uo pipefail

JOB="${1:-}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=jobs.sh
. "$HERE/jobs.sh"

FEIN_DATA="${FEIN_DATA:-$HOME/fein-data}"
if [ -f "$FEIN_DATA/fein.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$FEIN_DATA/fein.env"
  set +a
fi
export FEIN_DATA
FEIN_REPO="${FEIN_REPO:-$(cd "$HERE/../.." && pwd)}"
FEIN_BRANCH="${FEIN_BRANCH:-$FEIN_BRANCH_DEFAULT}"
PY="${FEIN_PYTHON:-python3}"
export TZ="${TZ:-Asia/Kolkata}"
umask 077

known=0
for j in "${FEIN_JOBS[@]}"; do [ "$(job_field "$j" 1)" = "$JOB" ] && known=1; done
if [ "$known" != 1 ]; then
  echo "usage: run_job.sh <job>   jobs: $(for j in "${FEIN_JOBS[@]}"; do printf '%s ' "$(job_field "$j" 1)"; done)" >&2
  exit 2
fi

LOGS="$FEIN_DATA/logs"
mkdir -p "$LOGS/status"
OUT="$LOGS/$JOB.out.log"
STATUS="$LOGS/status/$JOB.last"

exec 9>"$LOGS/.job-$JOB.lock"
if ! flock -n 9; then
  echo "$(date -Iseconds) $JOB: previous run still going; skipped" >>"$OUT"
  exit 0
fi

# ------------------------------------------------------------------ jobs
git_sync() {
  cd "$FEIN_REPO" || return 1
  local cur
  cur="$(git rev-parse --abbrev-ref HEAD)" || return 1
  if [ "$cur" != "$FEIN_BRANCH" ]; then
    echo "ERROR: repo is on '$cur', expected '$FEIN_BRANCH'. Not pulling."
    return 1
  fi
  if [ "${FEIN_GIT_PUSH:-0}" = "1" ]; then
    # Opt-in only (see deploy/pi/README.md): commit the Pi-owned output folders, rebase onto the remote, push.
    local paths="${FEIN_PUSH_PATHS:-research_notes/Backtests/india_pead_live}"
    # shellcheck disable=SC2086
    git add -- $paths 2>/dev/null
    if ! git diff --cached --quiet; then
      git commit -q -m "Pi: scheduled results $(date +%Y-%m-%d)" || { echo "ERROR: commit failed (git user.name/email set?)"; return 1; }
    fi
    if ! git pull --rebase --autostash -q origin "$FEIN_BRANCH"; then
      git rebase --abort 2>/dev/null
      echo "ERROR: pull --rebase failed; nothing pushed. Local commits are intact."
      return 1
    fi
    git push -q origin "HEAD:$FEIN_BRANCH" || { echo "ERROR: push failed (credentials?)"; return 1; }
    echo "pulled and pushed $(git rev-parse --short HEAD)"
    return 0
  fi
  # Default: pull only. Local results (uncommitted tracked changes) are stashed, the branch is
  # fast-forwarded, and the results are put back. Nothing is ever pushed.
  git fetch -q origin "$FEIN_BRANCH" || { echo "ERROR: git fetch failed (network or credentials)"; return 1; }
  if git merge-base --is-ancestor "origin/$FEIN_BRANCH" HEAD; then
    echo "already up to date ($(git rev-parse --short HEAD))"; return 0
  fi
  local tag stashed=0 rc=0
  tag="fein-autopull-$(date +%Y%m%d-%H%M%S)"
  if [ -n "$(git status --porcelain --untracked-files=no)" ]; then
    git stash push -q -m "$tag" && stashed=1
  fi
  if git merge --ff-only -q "origin/$FEIN_BRANCH"; then
    echo "fast-forwarded to $(git rev-parse --short HEAD)"
  else
    echo "ERROR: cannot fast-forward (local commits on the Pi?). Nothing changed."; rc=1
  fi
  if [ "$stashed" = 1 ] && ! git stash pop -q; then
    if git stash list | grep -q "$tag"; then
      git reset -q --hard HEAD   # tracked files only; the local results stay safe in the stash
      echo "ERROR: local results clash with the pulled version. They are kept in 'git stash list' as $tag."
      echo "$tag" >"$LOGS/git-sync.CONFLICT"
    else
      echo "ERROR: stash pop failed and stash $tag was not found; check 'git status' by hand."
    fi
    rc=1
  fi
  return "$rc"
}

rotate_logs() {
  local conf="$FEIN_DATA/logrotate.conf"
  if command -v logrotate >/dev/null && [ -f "$conf" ]; then
    logrotate -s "$LOGS/.logrotate.state" "$conf" || return 1
  else
    echo "WARN: logrotate or $conf missing; skipped"
  fi
  # scoreboard writes one log per day inside the repo (gitignored); keep 90 days
  find "$FEIN_REPO/tools/scoreboard/state" -maxdepth 1 -name 'run_*.log' -mtime +90 -delete 2>/dev/null
  return 0
}

run() {
  case "$JOB" in
    collect)     cd "$FEIN_REPO/tools/detectors" && "$PY" collect.py ;;
    detect)      cd "$FEIN_REPO/tools/detectors" && "$PY" detect.py ;;
    solvency)    cd "$FEIN_REPO/tools/detectors" && "$PY" solvency_screen.py ;;
    pead-update) cd "$FEIN_REPO" && "$PY" tools/backtests/india_pead/live_tracker.py update ;;
    pead-weekly) cd "$FEIN_REPO" && "$PY" tools/backtests/india_pead/live_tracker.py finalize &&
                   "$PY" tools/backtests/india_pead/live_tracker.py score ;;
    scoreboard)  cd "$FEIN_REPO" && tools/scoreboard/run_daily.sh ;;
    news)        cd "$FEIN_REPO/tools/news" && "$PY" news.py ;;
    macro)       cd "$FEIN_REPO" && "$PY" tools/macro/snapshot.py --out-dir "$FEIN_DATA/macro" ;;
    git-sync)    git_sync ;;
    logrotate)   rotate_logs ;;
  esac
}

start=$(date +%s)
{
  echo "=== $(date -Iseconds) $JOB start"
  run
  rc=$?
  echo "=== $(date -Iseconds) $JOB end rc=$rc ($(( $(date +%s) - start ))s)"
} >>"$OUT" 2>&1   # a { } group runs in this shell, so rc is visible below
echo "$(date +%s) $rc $(date -d "@$start" -Iseconds) $(( $(date +%s) - start ))" >"$STATUS"
exit "$rc"
