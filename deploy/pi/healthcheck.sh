#!/usr/bin/env bash
# FEIN Pi health check: one screen, exit 0 = OK (warnings allowed), 1 = something needs fixing.
#   deploy/pi/healthcheck.sh           full: includes the tools' live self-tests (NSE calls, ~1-2 min)
#   deploy/pi/healthcheck.sh --quick   offline only (skips collect/detect live self-tests)
#   deploy/pi/healthcheck.sh --strict  warnings also give a non-zero exit (2)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=jobs.sh
. "$HERE/jobs.sh"

QUICK=0; STRICT=0
for a in "$@"; do
  case "$a" in
    --quick) QUICK=1 ;; --strict) STRICT=1 ;;
    -h|--help) sed -n '2,5p' "$0"; exit 0 ;;
    *) echo "unknown option: $a" >&2; exit 2 ;;
  esac
done

FEIN_DATA="${FEIN_DATA:-$HOME/fein-data}"
if [ -f "$FEIN_DATA/fein.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$FEIN_DATA/fein.env"
  set +a
fi
FEIN_REPO="${FEIN_REPO:-$(cd "$HERE/../.." && pwd)}"
FEIN_BRANCH="${FEIN_BRANCH:-$FEIN_BRANCH_DEFAULT}"
PY="${FEIN_PYTHON:-python3}"
export FEIN_DATA TZ="${TZ:-Asia/Kolkata}"
LOGS="$FEIN_DATA/logs"
NFAIL=0; NWARN=0
ok()   { printf '  [ OK ] %s\n' "$*"; }
warn() { printf '  [WARN] %s\n' "$*"; NWARN=$((NWARN + 1)); }
fail() { printf '  [FAIL] %s\n' "$*"; NFAIL=$((NFAIL + 1)); }
hdr()  { printf '%s\n' "$*"; }

hdr "FEIN health  $(date '+%Y-%m-%d %H:%M %Z')  host $(hostname)  data $FEIN_DATA"

# ------------------------------------------------------------------ setup
hdr "Setup"
if "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' 2>/dev/null; then ok "$("$PY" -V 2>&1)"
else fail "Python 3.11+ not found at $PY"; fi
miss=""; for b in git curl pdftotext sqlite3 flock; do command -v "$b" >/dev/null || miss+=" $b"; done
[ -z "$miss" ] && ok "binaries: git curl pdftotext sqlite3 flock" || fail "missing:$miss (run install.sh)"
[ -f "$FEIN_DATA/fein.env" ] && ok "env file fein.env" || warn "no $FEIN_DATA/fein.env (run install.sh)"
if [ -d "$FEIN_DATA/secrets" ]; then
  p="$(stat -c %a "$FEIN_DATA/secrets")"
  [ "$p" = 700 ] && ok "secrets/ is 700" || fail "secrets/ is $p, should be 700 (chmod 700 $FEIN_DATA/secrets)"
  loose="$(find "$FEIN_DATA/secrets" -type f -perm /077 2>/dev/null | wc -l)"
  [ "$loose" = 0 ] || fail "$loose secret file(s) readable by others (chmod 600 $FEIN_DATA/secrets/*)"
else warn "no secrets/ folder"; fi
case "$(realpath -m "$FEIN_DATA")/" in "$(realpath -m "$FEIN_REPO")"/*) fail "data folder is inside the repo" ;; esac
tz="$(timedatectl show -p Timezone --value 2>/dev/null || cat /etc/timezone 2>/dev/null || echo '?')"
[ "$tz" = Asia/Kolkata ] && ok "clock Asia/Kolkata" || warn "system clock is '$tz' (cron mode needs Asia/Kolkata)"

# ------------------------------------------------------------------ repo
hdr "Repo $FEIN_REPO"
if git -C "$FEIN_REPO" rev-parse --git-dir >/dev/null 2>&1; then
  br="$(git -C "$FEIN_REPO" rev-parse --abbrev-ref HEAD)"
  last="$(git -C "$FEIN_REPO" log -1 --format='%h %cd' --date=format:'%Y-%m-%d')"
  [ "$br" = "$FEIN_BRANCH" ] && ok "branch $br at $last" || fail "on branch '$br', expected '$FEIN_BRANCH'"
  n="$(git -C "$FEIN_REPO" status --porcelain --untracked-files=no | wc -l)"
  [ "$n" = 0 ] || ok "$n tracked file(s) changed locally (normal: Pi results stay local)"
else fail "not a git checkout"; fi
[ -f "$LOGS/git-sync.CONFLICT" ] && fail "weekly pull hit a clash; local results are in git stash '$(cat "$LOGS/git-sync.CONFLICT")'"

# ------------------------------------------------------------------ scheduler
hdr "Scheduler"
sched=none
if ls "$HOME/.config/systemd/user"/fein-*.timer >/dev/null 2>&1; then
  sched=systemd
  if systemctl --user show-environment >/dev/null 2>&1; then
    act=0; tot=0
    for j in "${FEIN_JOBS[@]}"; do
      tot=$((tot + 1)); systemctl --user is-active -q "fein-$(job_field "$j" 1).timer" && act=$((act + 1))
    done
    [ "$act" = "$tot" ] && ok "systemd: $act/$tot timers active" || fail "systemd: only $act/$tot timers active (systemctl --user list-timers 'fein-*')"
    [ "$(loginctl show-user "$(id -un)" -p Linger --value 2>/dev/null)" = yes ] \
      || warn "linger is off: timers stop when you log out (sudo loginctl enable-linger $(id -un))"
  else warn "systemd units exist but no user session bus here; cannot check timers"; fi
fi
if crontab -l 2>/dev/null | grep -qF "$FEIN_CRON_BEGIN"; then
  [ "$sched" = systemd ] && warn "both cron and systemd entries exist: jobs may run twice" || ok "cron block installed"
  sched=cron
fi
[ "$sched" = none ] && fail "no FEIN timers or cron entries (run install.sh)"

# ------------------------------------------------------------------ last runs
hdr "Last runs (job  age  exit)"
now="$(date +%s)"
for j in "${FEIN_JOBS[@]}"; do
  n="$(job_field "$j" 1)"; maxh="$(job_field "$j" 4)"; st="$LOGS/status/$n.last"
  if [ ! -f "$st" ]; then warn "$(printf '%-12s never run yet' "$n")"; continue; fi
  read -r ts rc _start secs <"$st"
  age=$(( (now - ts) / 3600 ))
  line="$(printf '%-12s %4sh ago  exit %s  (%ss)' "$n" "$age" "$rc" "$secs")"
  if [ "$rc" != 0 ]; then fail "$line  see logs/$n.out.log"
  elif [ "$age" -gt "$maxh" ]; then fail "$line  older than ${maxh}h"
  else ok "$line"; fi
done

# ------------------------------------------------------------------ logs + outputs
hdr "Logs and outputs"
for f in "$LOGS"/*.log; do
  [ -f "$f" ] || continue
  e="$(tail -n 300 "$f" | grep -cE 'Traceback|ERROR|FAIL')"
  [ "$e" = 0 ] || warn "$(basename "$f"): $e error line(s) in the last 300 lines"
done
sbl="$(ls -1t "$FEIN_REPO"/tools/scoreboard/state/run_*.log 2>/dev/null | head -1)"
if [ -n "$sbl" ]; then
  e="$(grep -c ' failed$' "$sbl")"
  [ "$e" = 0 ] && ok "scoreboard $(basename "$sbl"): no step failed" || fail "scoreboard $(basename "$sbl"): $e step(s) failed"
fi
la="$(ls -1t "$FEIN_DATA"/alerts/*.md 2>/dev/null | head -1)"
[ -n "$la" ] && ok "latest alerts: $(basename "$la")" || warn "no alerts file yet (first one after collect+detect)"
if [ -f "$FEIN_DATA/fein.sqlite" ] && command -v sqlite3 >/dev/null; then
  ic="$(sqlite3 -readonly "$FEIN_DATA/fein.sqlite" 'PRAGMA quick_check;' 2>&1 | head -1)"
  [ "$ic" = ok ] && ok "fein.sqlite quick_check ok ($(du -h "$FEIN_DATA/fein.sqlite" | cut -f1))" || fail "fein.sqlite: $ic"
fi

# ------------------------------------------------------------------ disk + network exposure
hdr "Disk and network"
if df -Pk "$FEIN_DATA" >/dev/null 2>&1; then
  read -r _ _ _ avail pct _ < <(df -Pk "$FEIN_DATA" | tail -1)
  freeg=$((avail / 1048576)); pct="${pct%\%}"
  if [ "$freeg" -lt 1 ] || [ "$pct" -ge 95 ]; then fail "disk: ${freeg} GB free (${pct}% used)"
  elif [ "$freeg" -lt 5 ] || [ "$pct" -ge 85 ]; then warn "disk: ${freeg} GB free (${pct}% used)"
  else ok "disk: ${freeg} GB free (${pct}% used); data $(du -sh "$FEIN_DATA" 2>/dev/null | cut -f1)"; fi
else warn "data folder $FEIN_DATA missing"; fi
if command -v ss >/dev/null; then
  pub="$(ss -Hltn 2>/dev/null | awk '{print $4}' | grep -vE '^(127\.|\[::1\]|::1|\[::ffff:127\.)' | sort -u | tr '\n' ' ')"
  [ -z "$pub" ] && ok "no TCP port listening beyond localhost" \
    || warn "listening on non-local addresses: $pub(FEIN needs none; SSH on :22 is your choice)"
fi

# ------------------------------------------------------------------ self-tests
hdr "Self-tests$([ "$QUICK" = 1 ] && echo ' (quick: offline only)')"
st() { # st <label> <dir> <cmd...>
  local label="$1" dir="$2" out; shift 2
  if out="$(cd "$dir" && timeout 300 "$@" 2>&1)"; then
    if grep -q 'FAIL' <<<"$out"; then warn "$label passed with: $(grep 'FAIL' <<<"$out" | head -2 | tr -s ' ' | tr '\n' ';' | cut -c1-140)"
    else ok "$label"; fi
  else fail "$label: $(printf '%s' "$out" | grep -E 'FAIL|Error|error' | head -2 | tr '\n' ' ' | cut -c1-140)"; fi
}
D="$FEIN_REPO/tools/detectors"
st "solvency_screen --selftest (offline)" "$D" "$PY" solvency_screen.py --selftest
st "scoreboard unit tests (offline)" "$FEIN_REPO" "$PY" -m unittest discover -s tools/scoreboard/tests
st "news --selftest (offline)" "$FEIN_REPO/tools/news" "$PY" news.py --selftest
st "macro snapshot --selftest (offline)" "$FEIN_REPO" "$PY" tools/macro/snapshot.py --selftest
if [ "$QUICK" = 0 ]; then
  st "collect --selftest (live NSE/BSE)" "$D" "$PY" collect.py --selftest
  st "detect --selftest (live + offline rules)" "$D" "$PY" detect.py --selftest
fi
"$PY" -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$FEIN_REPO/tools/backtests/india_pead/live_tracker.py" \
  && ok "live_tracker.py parses (it has no --selftest)" || fail "live_tracker.py does not parse"

# ------------------------------------------------------------------ verdict
echo
if [ "$NFAIL" -gt 0 ]; then echo "RESULT: $NFAIL problem(s), $NWARN warning(s). Logs: $LOGS"; exit 1; fi
if [ "$NWARN" -gt 0 ]; then echo "RESULT: OK with $NWARN warning(s)"; [ "$STRICT" = 1 ] && exit 2; exit 0; fi
echo "RESULT: all OK"
