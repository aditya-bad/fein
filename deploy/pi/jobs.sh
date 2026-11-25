# shellcheck shell=bash
# FEIN Pi job table: one place, sourced by install.sh, run_job.sh, healthcheck.sh and uninstall.sh.
# Fields (|-separated):
#   name | systemd OnCalendar (IST) | cron schedule (system clock must be IST) | max hours between successful runs | timeout | what it does
# Times follow each tool's own README (tools/detectors, tools/scoreboard, tools/news, research_notes/Backtests/india_pead_v2.md).
FEIN_JOBS=(
  "collect|Mon..Sat *-*-* 21:00:00 Asia/Kolkata|0 21 * * 1-6|74|2h|detectors: collect NSE/BSE disclosures into FEIN_DATA"
  "detect|Mon..Sat *-*-* 21:30:00 Asia/Kolkata|30 21 * * 1-6|74|30min|detectors: write alerts/YYYY-MM-DD.md and .csv"
  "pead-update|Mon..Fri *-*-* 20:30:00 Asia/Kolkata|30 20 * * 1-5|98|90min|PEAD live tracker: log new results (update)"
  "pead-weekly|Sat *-*-* 21:30:00 Asia/Kolkata|30 21 * * 6|194|3h|PEAD live tracker: finalize, then score"
  "scoreboard|*-*-* 22:00:00 Asia/Kolkata|0 22 * * *|50|2h|scoreboard: tools/scoreboard/run_daily.sh"
  "news|*-*-* 22:30:00 Asia/Kolkata|30 22 * * *|50|45min|news: tools/news/news.py -> FEIN_DATA/news/YYYY-MM-DD.md/.csv"
  "solvency|Sun *-*-* 06:00:00 Asia/Kolkata|0 6 * * 0|194|5h|detectors: weekly solvency screen (screener.in)"
  "git-sync|Mon *-*-* 07:00:00 Asia/Kolkata|0 7 * * 1|194|20min|git pull --ff-only of the branch (push only if opted in)"
  "logrotate|Sun *-*-* 05:30:00 Asia/Kolkata|30 5 * * 0|194|15min|rotate FEIN_DATA logs, prune old scoreboard run logs"
)
FEIN_BRANCH_DEFAULT="claude/focused-brahmagupta-g3hraq"
FEIN_CRON_BEGIN="# >>> FEIN deploy/pi (managed by install.sh; remove with uninstall.sh) >>>"
FEIN_CRON_END="# <<< FEIN deploy/pi <<<"

# job_field <line> <index 1-6>
job_field() { local IFS='|'; local -a f; read -r -a f <<<"$1"; printf '%s' "${f[$(($2 - 1))]}"; }
