#!/usr/bin/env bash
# FEIN Raspberry Pi installer. Safe to run again: it only adds what is missing and rewrites its own units.
#   deploy/pi/install.sh              install (asks for sudo once for apt, timezone and "linger")
#   deploy/pi/install.sh --dry-run    print every action, change nothing
# Options:
#   --cron        use crontab instead of systemd user timers
#   --no-sudo     skip apt, timezone and linger (prints what to run by hand)
#   --data DIR    data folder (default ~/fein-data); must be outside the repo
#   --force       continue on a non-ARM64 / non-Debian system
# It never stores secrets in the repo, never opens a port, and never pushes to git.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
# shellcheck source=jobs.sh
. "$HERE/jobs.sh"

DRY=0; MODE=auto; SUDO_OK=1; FORCE=0
DATA="${FEIN_DATA:-$HOME/fein-data}"
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;;
    --cron) MODE=cron ;;
    --systemd) MODE=systemd ;;
    --no-sudo) SUDO_OK=0 ;;
    --data) DATA="$2"; shift ;;
    --force) FORCE=1 ;;
    -h|--help) sed -n '2,10p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done
DATA="$(realpath -m "$DATA")"
UNIT_DIR="$HOME/.config/systemd/user"
APT_PKGS=(git python3 python3-venv poppler-utils sqlite3 curl util-linux logrotate ca-certificates)

say()  { printf '\033[1m==>\033[0m %s\n' "$*"; }
warn() { printf 'WARN: %s\n' "$*" >&2; }
die()  { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
# do_ <cmd...>: run, or print in dry-run
do_() { if [ "$DRY" = 1 ]; then printf '   [dry-run] %s\n' "$*"; else "$@"; fi; }
# put_file <path> <mode>: content from stdin; only rewrites when different
put_file() {
  local path="$1" mode="$2" tmp
  tmp="$(mktemp)"; cat >"$tmp"
  if [ -f "$path" ] && cmp -s "$tmp" "$path"; then rm -f "$tmp"; echo "   unchanged: $path"; return 0; fi
  if [ "$DRY" = 1 ]; then
    printf '   [dry-run] write %s (mode %s):\n' "$path" "$mode"; sed 's/^/      | /' "$tmp"; rm -f "$tmp"
  else
    mkdir -p "$(dirname "$path")"; install -m "$mode" "$tmp" "$path"; rm -f "$tmp"; echo "   wrote: $path"
  fi
}
# strip_block: stdin minus the FEIN cron block
strip_block() { awk -v b="$FEIN_CRON_BEGIN" -v e="$FEIN_CRON_END" '$0==b{s=1;next} $0==e{s=0;next} !s'; }
[ "$DRY" = 1 ] && say "DRY RUN: nothing will be changed"

# ------------------------------------------------------------- 1. preflight
say "Checking system"
[ "$(uname -s)" = Linux ] || die "Linux only."
if [ "$(id -u)" = 0 ]; then
  msg="Run as your normal FEIN user (e.g. 'fein'), not root. It asks for sudo itself."
  if [ "$DRY" = 1 ]; then warn "$msg (dry-run continues)"; else die "$msg"; fi
fi
arch="$(uname -m)"; os="unknown"
# shellcheck disable=SC1091
[ -r /etc/os-release ] && os="$(. /etc/os-release; echo "${PRETTY_NAME:-$ID}")"
echo "   OS: $os   arch: $arch   user: $(id -un)"
if [ "$arch" != aarch64 ] && [ "$arch" != arm64 ]; then
  msg="expected ARM64 (Raspberry Pi OS 64-bit), found $arch"
  if [ "$DRY" = 1 ] || [ "$FORCE" = 1 ]; then warn "$msg (continuing)"; else die "$msg. Use --force to continue anyway."; fi
fi
if ! grep -qiE 'debian|raspbian' /etc/os-release 2>/dev/null; then
  msg="not a Debian-based OS; apt steps may fail"
  if [ "$DRY" = 1 ] || [ "$FORCE" = 1 ]; then warn "$msg"; else die "$msg. Use --force to continue anyway."; fi
fi
PY="$(command -v python3 || true)"
[ -n "$PY" ] || die "python3 not found (sudo apt install -y python3)."
"$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' \
  || die "Python 3.11+ needed, found $("$PY" -V 2>&1). Raspberry Pi OS Bookworm ships 3.11."
echo "   python: $PY ($("$PY" -V 2>&1))"

say "Checking repo $REPO"
git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1 || die "$REPO is not a git checkout."
branch="$(git -C "$REPO" rev-parse --abbrev-ref HEAD)"
[ "$branch" = "$FEIN_BRANCH_DEFAULT" ] || warn "repo is on '$branch'; the weekly pull expects '$FEIN_BRANCH_DEFAULT' (git checkout $FEIN_BRANCH_DEFAULT)"
case "$DATA/" in "$REPO"/*) die "data folder $DATA is inside the repo; secrets and data must stay outside it." ;; esac
for f in tools/detectors/collect.py tools/detectors/detect.py tools/detectors/solvency_screen.py \
         tools/backtests/india_pead/live_tracker.py tools/scoreboard/run_daily.sh; do
  [ -e "$REPO/$f" ] || die "missing $f; is this the right branch?"
done

# ------------------------------------------------------------- 2. packages + timezone
SUDO=""; [ "$SUDO_OK" = 1 ] && SUDO="sudo"
missing=()
for p in "${APT_PKGS[@]}"; do dpkg -s "$p" >/dev/null 2>&1 || missing+=("$p"); done
say "Packages"
if [ ${#missing[@]} -eq 0 ]; then echo "   all present: ${APT_PKGS[*]}"
elif [ "$SUDO_OK" = 1 ]; then
  do_ $SUDO apt-get update -q
  do_ $SUDO env DEBIAN_FRONTEND=noninteractive apt-get install -y -q "${missing[@]}"
else warn "missing packages: ${missing[*]}. Run: sudo apt install -y ${missing[*]}"; fi

say "Timezone"
tz="$(timedatectl show -p Timezone --value 2>/dev/null || cat /etc/timezone 2>/dev/null || echo unknown)"
if [ "$tz" = Asia/Kolkata ]; then echo "   already Asia/Kolkata"
elif [ "$SUDO_OK" = 1 ]; then do_ $SUDO timedatectl set-timezone Asia/Kolkata
else warn "clock is $tz; run: sudo timedatectl set-timezone Asia/Kolkata (cron times assume IST)"; fi

# ------------------------------------------------------------- 3. data folders + env file
say "Data folder $DATA"
for d in "$DATA" "$DATA/raw" "$DATA/logs" "$DATA/logs/status" "$DATA/alerts" "$DATA/solvency" "$DATA/secrets"; do
  if [ -d "$d" ]; then echo "   exists: $d"; else do_ mkdir -p "$d"; fi
done
do_ chmod 700 "$DATA" "$DATA/secrets"
if [ -d "$DATA/secrets" ]; then
  while IFS= read -r -d '' f; do do_ chmod 600 "$f"; done < <(find "$DATA/secrets" -type f ! -perm 600 -print0)
fi

ENVF="$DATA/fein.env"
declare -A want=(
  [FEIN_DATA]="$DATA" [FEIN_REPO]="$REPO" [FEIN_BRANCH]="$FEIN_BRANCH_DEFAULT" [FEIN_PYTHON]="$PY"
  [TZ]="Asia/Kolkata" [SB_AUTO_APPLY]="0" [SB_GIT_COMMIT]="0" [FEIN_GIT_PUSH]="0"
)
order=(FEIN_DATA FEIN_REPO FEIN_BRANCH FEIN_PYTHON TZ SB_AUTO_APPLY SB_GIT_COMMIT FEIN_GIT_PUSH)
if [ -f "$ENVF" ]; then
  # keep the user's edits; only the two paths follow this install
  content="$(sed -e "s|^FEIN_DATA=.*|FEIN_DATA=$DATA|" -e "s|^FEIN_REPO=.*|FEIN_REPO=$REPO|" "$ENVF")"
else
  content="# FEIN settings for the scheduled jobs (deploy/pi). KEY=value, no quotes, NO secrets here.
# SB_AUTO_APPLY=0: scoreboard writes seeds + review queue but does not change memdb on the Pi.
# FEIN_GIT_PUSH=1 opts in to a weekly commit+push of FEIN_PUSH_PATHS (see deploy/pi/README.md)."
fi
for k in "${order[@]}"; do
  grep -q "^$k=" <<<"$content" || content+=$'\n'"$k=${want[$k]}"
done
printf '%s\n' "$content" | put_file "$ENVF" 600

put_file "$DATA/logrotate.conf" 600 <<EOF
# FEIN logs; run weekly by the 'logrotate' job as $(id -un) with its own state file.
$DATA/logs/*.log {
    weekly
    rotate 8
    compress
    delaycompress
    missingok
    notifempty
    copytruncate
}
EOF

# ------------------------------------------------------------- 4. scheduler
if [ "$MODE" = auto ]; then
  if command -v systemctl >/dev/null && systemctl --user show-environment >/dev/null 2>&1; then MODE=systemd; else MODE=cron; fi
fi
say "Scheduler: $MODE"
RUN="$REPO/deploy/pi/run_job.sh"

if [ "$MODE" = systemd ]; then
  for j in "${FEIN_JOBS[@]}"; do
    n="$(job_field "$j" 1)"; cal="$(job_field "$j" 2)"; to="$(job_field "$j" 5)"; desc="$(job_field "$j" 6)"
    put_file "$UNIT_DIR/fein-$n.service" 644 <<EOF
[Unit]
Description=FEIN $desc

[Service]
Type=oneshot
Environment=FEIN_DATA=$DATA
ExecStart=/bin/bash "$RUN" $n
Nice=10
IOSchedulingClass=idle
TimeoutStartSec=$to
EOF
    put_file "$UNIT_DIR/fein-$n.timer" 644 <<EOF
[Unit]
Description=FEIN timer: $n

[Timer]
OnCalendar=$cal
Persistent=true
RandomizedDelaySec=60

[Install]
WantedBy=timers.target
EOF
  done
  do_ systemctl --user daemon-reload
  for j in "${FEIN_JOBS[@]}"; do do_ systemctl --user enable --now "fein-$(job_field "$j" 1).timer"; done
  if [ "$(loginctl show-user "$(id -un)" -p Linger --value 2>/dev/null)" = yes ]; then echo "   linger already on"
  elif [ "$SUDO_OK" = 1 ]; then do_ $SUDO loginctl enable-linger "$(id -un)"
  else warn "run: sudo loginctl enable-linger $(id -un)   (so timers run when nobody is logged in)"; fi
  # remove an old cron block if we switched over
  if crontab -l 2>/dev/null | grep -qF "$FEIN_CRON_BEGIN"; then
    say "Removing old FEIN cron block (now using systemd)"
    new="$(crontab -l | strip_block)"
    if [ "$DRY" = 1 ]; then echo "   [dry-run] crontab <(old crontab minus FEIN block)"; else printf '%s\n' "$new" | crontab -; fi
  fi
else
  if ! command -v crontab >/dev/null; then
    msg="crontab not found (sudo apt install -y cron) and systemd user session unavailable."
    if [ "$DRY" = 1 ]; then warn "$msg (dry-run shows the block anyway)"; crontab() { return 1; }; else die "$msg"; fi
  fi
  [ "$tz" = Asia/Kolkata ] || [ "$SUDO_OK" = 1 ] || warn "cron uses the system clock; set it to Asia/Kolkata first."
  block="$FEIN_CRON_BEGIN"$'\n'
  for j in "${FEIN_JOBS[@]}"; do
    block+="$(job_field "$j" 3) FEIN_DATA='$DATA' /bin/bash '$RUN' $(job_field "$j" 1)"$'\n'
  done
  block+="$FEIN_CRON_END"
  old="$(crontab -l 2>/dev/null || true)"
  stripped="$(printf '%s\n' "$old" | strip_block)"
  new="$(printf '%s\n%s\n' "$stripped" "$block" | sed '/./,$!d')"
  if [ "$new" = "$old" ]; then echo "   crontab unchanged"
  elif [ "$DRY" = 1 ]; then echo "   [dry-run] install crontab block:"; printf '%s\n' "$block" | sed 's/^/      | /'
  else printf '%s\n' "$new" | crontab -; echo "   crontab updated"; fi
  # remove systemd units if we switched over
  if ls "$UNIT_DIR"/fein-*.timer >/dev/null 2>&1; then
    warn "systemd FEIN units also exist; run deploy/pi/uninstall.sh --systemd-only to remove them"
  fi
fi

# ------------------------------------------------------------- 5. done
do_ chmod +x "$HERE/run_job.sh" "$HERE/healthcheck.sh" "$HERE/uninstall.sh"
say "Done."
cat <<EOF
   Next:
     1. $HERE/healthcheck.sh            (full check, ~2 min, includes live self-tests)
     2. Optional first run now:  $RUN collect && $RUN detect
   Outputs: $DATA/alerts/  (daily alerts), $DATA/solvency/, $DATA/logs/
   PEAD live state: $REPO/research_notes/Backtests/india_pead_live/  Scoreboard: $REPO/tools/scoreboard/state/
   Nothing is pushed to GitHub unless you set FEIN_GIT_PUSH=1 in $ENVF.
EOF
