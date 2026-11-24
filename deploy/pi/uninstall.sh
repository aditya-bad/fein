#!/usr/bin/env bash
# Remove the FEIN schedules. Keeps all data unless --purge.
#   deploy/pi/uninstall.sh                 remove systemd user timers/units and the FEIN cron block
#   deploy/pi/uninstall.sh --systemd-only  remove only the systemd units (after switching to cron)
#   deploy/pi/uninstall.sh --purge         ALSO delete the data folder (asks to type 'delete'; --yes skips the question)
#   deploy/pi/uninstall.sh --dry-run       print what would happen
# Never touches the repo, the apt packages, the timezone or linger.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=jobs.sh
. "$HERE/jobs.sh"
DRY=0; PURGE=0; YES=0; SYSD_ONLY=0
DATA="${FEIN_DATA:-$HOME/fein-data}"
while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run) DRY=1 ;; --purge) PURGE=1 ;; --yes) YES=1 ;; --systemd-only) SYSD_ONLY=1 ;;
    --data) DATA="$2"; shift ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done
do_() { if [ "$DRY" = 1 ]; then printf '   [dry-run] %s\n' "$*"; else "$@"; fi; }
UNIT_DIR="$HOME/.config/systemd/user"

echo "==> systemd user timers"
found=0
for j in "${FEIN_JOBS[@]}"; do
  n="fein-$(job_field "$j" 1)"
  [ -e "$UNIT_DIR/$n.timer" ] || [ -e "$UNIT_DIR/$n.service" ] || continue
  found=1
  systemctl --user show-environment >/dev/null 2>&1 && do_ systemctl --user disable --now "$n.timer" || true
  do_ rm -f "$UNIT_DIR/$n.timer" "$UNIT_DIR/$n.service"
done
if [ "$found" = 1 ]; then
  systemctl --user show-environment >/dev/null 2>&1 && do_ systemctl --user daemon-reload || true
else echo "   none installed"; fi

if [ "$SYSD_ONLY" = 0 ]; then
  echo "==> crontab"
  if crontab -l 2>/dev/null | grep -qF "$FEIN_CRON_BEGIN"; then
    new="$(crontab -l | awk -v b="$FEIN_CRON_BEGIN" -v e="$FEIN_CRON_END" '$0==b{s=1;next} $0==e{s=0;next} !s')"
    if [ "$DRY" = 1 ]; then echo "   [dry-run] remove the FEIN block from crontab"
    elif [ -z "$(printf '%s' "$new" | tr -d '[:space:]')" ]; then crontab -r; echo "   removed (crontab now empty)"
    else printf '%s\n' "$new" | crontab -; echo "   removed FEIN block, other entries kept"; fi
  else echo "   no FEIN block"; fi
fi

if [ "$PURGE" = 1 ]; then
  echo "==> purge $DATA"
  DATA="$(realpath -m "$DATA")"
  case "$DATA" in "$HOME"|/|"") echo "refusing to delete '$DATA'" >&2; exit 1 ;; esac
  if [ ! -d "$DATA" ]; then echo "   not there"
  else
    if [ "$YES" = 0 ] && [ "$DRY" = 0 ]; then
      echo "   This deletes ALL collected data, alerts, logs and secrets in $DATA ($(du -sh "$DATA" | cut -f1))."
      read -r -p "   Type 'delete' to confirm: " ans
      [ "$ans" = delete ] || { echo "   kept"; exit 0; }
    fi
    do_ rm -rf -- "$DATA"
  fi
else
  echo "==> data kept in $DATA (use --purge to delete it)"
fi
echo "Done. The repo, packages, timezone and linger setting are unchanged."
