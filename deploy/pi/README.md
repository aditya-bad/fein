# FEIN on a Raspberry Pi: one-command setup

This folder turns a Raspberry Pi into the always-on machine that runs FEIN's unattended jobs every evening.
Claude is not involved in these jobs, so they cost none of your Claude usage. It covers roadmap stages
1 (universe), 2 (hard filters: solvency), 3 (signals: detectors, PEAD) and 7 (scorekeeping: scoreboard).
This is research tooling, not SEBI-registered advice.

| File | What it does |
|---|---|
| `install.sh` | Checks the Pi, installs packages, creates `~/fein-data`, writes `~/fein-data/fein.env`, installs the schedule. Safe to re-run. `--dry-run` shows every action and changes nothing. |
| `healthcheck.sh` | One-screen status: setup, schedule, last run of every job, log errors, disk, open ports, the tools' self-tests. Exit code 1 means something needs fixing. |
| `uninstall.sh` | Removes the schedule. Keeps your data unless you add `--purge`. |
| `run_job.sh` | What the schedule calls (`run_job.sh collect`, etc.). You can run it by hand too. |
| `jobs.sh` | The job table: names, times, how stale is "too old". |

## What runs, and when (India time)

| Job | When | Runs | Output |
|---|---|---|---|
| `pead-update` | Mon–Fri 20:30 | `live_tracker.py update` | `research_notes/Backtests/india_pead_live/` (in the repo) |
| `collect` | Mon–Sat 21:00 | `tools/detectors/collect.py` | `~/fein-data/fein.sqlite`, `~/fein-data/raw/` |
| `detect` | Mon–Sat 21:30 | `tools/detectors/detect.py` | `~/fein-data/alerts/YYYY-MM-DD.md` and `.csv` |
| `pead-weekly` | Sat 21:30 | `live_tracker.py finalize`, then `score` | `india_pead_live/scorecard.md` |
| `scoreboard` | daily 22:00 | `tools/scoreboard/run_daily.sh` | `tools/scoreboard/state/`, seeds in `memdb/seeds/` |
| `solvency` | Sun 06:00 | `tools/detectors/solvency_screen.py` (about 2.5 h) | `~/fein-data/solvency/` |
| `logrotate` | Sun 05:30 | rotates `~/fein-data/logs/*.log` (8 weeks kept) | |
| `git-sync` | Mon 07:00 | `git pull --ff-only` of the branch. **Never pushes** unless you opt in (below). | |

`collect` skips Sunday, as the detectors README recommends (Saturday picks up Friday-night filings).
The times follow each tool's own README. If the Pi was off at a scheduled time, systemd runs the missed
job once when it is back on.

The promise tracker (`tools/promise_tracker/pipeline/`) is **not** scheduled. It needs an LLM step and is run
on request in a Claude session.

## Step by step

### 0. Before you start
- Raspberry Pi 4 or 5, Raspberry Pi OS **64-bit** (Bookworm or newer, which has Python 3.11), ideally on a USB SSD.
- A separate user for this work, for example `fein` (List 3). Log in as that user for every step below.
  ```bash
  sudo adduser fein && sudo usermod -aG sudo fein     # once, as your admin user; then log in as fein
  ```
- The repo cloned **on the branch `claude/focused-brahmagupta-g3hraq`**:
  ```bash
  mkdir -p ~/fein-lab && cd ~/fein-lab
  git clone https://github.com/aditya-bad/fein.git && cd fein
  git checkout claude/focused-brahmagupta-g3hraq
  ```
  The repo is private, so git asks for a login. Use a *fine-grained* GitHub token limited to this one repo,
  contents **read-only** is enough unless you opt in to pushing (then read/write), with an expiry date.

### 1. Preview, then install
```bash
cd ~/fein-lab/fein
deploy/pi/install.sh --dry-run     # shows every action, changes nothing
deploy/pi/install.sh               # asks for your password once (sudo) for apt, timezone and "linger"
```
What it does:
1. Checks: Linux, ARM64, Debian/Raspberry Pi OS, Python 3.11+, not running as root, right repo and branch.
2. Installs any missing packages: `git python3 python3-venv poppler-utils sqlite3 curl util-linux logrotate ca-certificates`.
   (The tools use only the Python standard library, so no `pip install` is needed.)
3. Sets the clock to `Asia/Kolkata`.
4. Creates `~/fein-data/{raw,logs,alerts,solvency,secrets}`. `~/fein-data` and `secrets/` are `chmod 700`.
5. Writes `~/fein-data/fein.env` (`chmod 600`): data path, repo path, branch, `TZ=Asia/Kolkata`, and three switches,
   all off by default (`SB_AUTO_APPLY=0`, `SB_GIT_COMMIT=0`, `FEIN_GIT_PUSH=0`). Re-running keeps your edits.
6. Installs **systemd user timers** (`~/.config/systemd/user/fein-*.timer`) and turns on "linger" so they run
   when nobody is logged in. If systemd user sessions are not available it uses your **crontab** instead
   (force it with `--cron`).

Other options: `--no-sudo` (skip the sudo steps and print them for you), `--data DIR` (another data folder, must
be outside the repo), `--force` (non-ARM64 machine).

### 2. Check it
```bash
deploy/pi/healthcheck.sh           # about 1-2 min; includes live NSE/BSE self-tests
deploy/pi/healthcheck.sh --quick   # offline checks only
```
Right after install, "never run yet" warnings are normal. After the first evening every job should be `OK`.
Exit code: 0 = fine (warnings allowed), 1 = problem. `--strict` also fails on warnings (exit 2).

To build a first baseline tonight instead of waiting:
```bash
deploy/pi/run_job.sh collect && deploy/pi/run_job.sh detect
```
The pledge rules compare two snapshots, so they start firing from the second evening.
The PEAD tracker logs nothing until the Dec-2026 quarter results arrive (about mid-January 2027). That is expected.

### 3. Where the outputs are
| What | Where |
|---|---|
| Daily alerts (the thing to read) | `~/fein-data/alerts/YYYY-MM-DD.md` and `.csv` |
| Solvency screen | `~/fein-data/solvency/latest.csv` and dated `.md` |
| Detector database | `~/fein-data/fein.sqlite` |
| PEAD live log and scorecard | `~/fein-lab/fein/research_notes/Backtests/india_pead_live/` |
| Scoreboard runs and review queue | `~/fein-lab/fein/tools/scoreboard/state/`, seeds in `memdb/seeds/` |
| Job logs | `~/fein-data/logs/<job>.out.log`, plus the tools' own `collect.log`, `detect.log`, `solvency.log` |
| Last result of each job | `~/fein-data/logs/status/<job>.last` |

`SB_AUTO_APPLY=0` means the Pi's scoreboard writes its seed files and review queue but does not change memdb.
Claude applies them in a session (`tools/scoreboard/apply.sh`). This keeps the Pi's copy of `memory/store/`
identical to GitHub's, so the weekly pull never clashes. Set `SB_AUTO_APPLY=1` in `fein.env` to apply on the Pi.

### 4. Sharing alerts with Claude
Results stay on the Pi. To let Claude read them:
- **Remote Control (preferred).** Install Claude Code on the Pi (`curl -fsSL https://claude.ai/install.sh | bash`), log in
  with your account, then `cd ~/fein-lab && claude remote-control` (keep it running in `tmux` or as a service).
  Share **only `~/fein-lab`**, never your home folder. To make the alerts visible inside it without sharing secrets:
  ```bash
  ln -s ~/fein-data/alerts ~/fein-lab/alerts       # alerts only; do NOT link ~/fein-data or secrets/
  ln -s ~/fein-data/solvency ~/fein-lab/solvency
  ```
  Then tell Claude it is running. Caveat: using a computer's folder from a cloud session is not on every account yet.
  If Claude cannot see it, run `claude` **on the Pi** itself in `~/fein-lab/fein`; it reads the same repo and memory.
- **Fallback.** Copy today's `alerts/YYYY-MM-DD.md` text into the chat.

### 5. Opt in to pushing results to GitHub (off by default)
Nothing is pushed unless you choose to. To push the PEAD live log weekly:
1. Give the Pi's GitHub token **contents read/write** on this repo only.
2. `git config --global user.name "fein-pi"` and `git config --global user.email "<your noreply address>"`.
3. In `~/fein-data/fein.env` set `FEIN_GIT_PUSH=1`. Optionally `FEIN_PUSH_PATHS=research_notes/Backtests/india_pead_live`
   (space-separated repo paths; that folder is the default). Data in `~/fein-data` is never pushed.

The Monday `git-sync` job then commits only those paths, rebases on GitHub and pushes. To turn it off, set it back to `0`.

## Security notes (from List 3 in `My Requirements/requirements.md`)
- **No inbound ports.** Nothing here listens on a port; every job connects outward. Keep router port-forwarding off.
  `healthcheck.sh` warns if anything listens beyond localhost.
- **Firewall:** `sudo apt install -y ufw && sudo ufw default deny incoming && sudo ufw default allow outgoing && sudo ufw enable`.
- **SSH** is for you, not Claude. Turn it off if unused (`sudo systemctl disable --now ssh`), or keys only (`PasswordAuthentication no`).
- **Secrets** (Kite key/secret/token, Screener cookies, GitHub token) live only in `~/fein-data/secrets/`, one file each,
  `chmod 600`, owned by `fein`. Never in the repo, never in `fein.env`, never pasted in chat.
  `install.sh` refuses a data folder inside the repo; `healthcheck.sh` fails if a secret file is readable by others.
- **Kite wrapper** (when you build it): read-only tools only (no orders, funds, holdings or positions), bound to `127.0.0.1`.
  Use Tailscale if you need it from a laptop, never an open port.
- **Automatic security updates:** `sudo apt install -y unattended-upgrades && sudo dpkg-reconfigure unattended-upgrades`.
- **Back up `~/fein-data`** weekly to another drive. The repo has the code and memory but not the raw data.
- **Power:** a UPS or at least an SSD; SD cards corrupt on power loss.

## Troubleshooting
| Symptom | Fix |
|---|---|
| `healthcheck` says a job failed | `tail -50 ~/fein-data/logs/<job>.out.log`. Re-run it by hand: `deploy/pi/run_job.sh <job>`. |
| `collect --selftest` shows `FAIL` for a source | NSE/BSE changed an endpoint or blocked the request. Look at the newest file in `~/fein-data/raw/` and tell Claude. |
| PEAD `update` finds 0 companies on a results-season weekday | Check `tools/nse_fetch.py` first (see `research_notes/Backtests/india_pead_v2.md`). |
| `solvency` fails or finds few names | It reads public screener.in pages (no login). Check `~/fein-data/logs/solvency.log`; screener may be rate-limiting or have changed its pages. Re-runs the same week use the cache. |
| "weekly pull hit a clash" | Your Pi results and GitHub changed the same file. The repo is clean at the new version; your results are in `git stash list` (name in `~/fein-data/logs/git-sync.CONFLICT`). Ask Claude to merge them, then delete that file. |
| "repo is on '...', expected ..." | `cd ~/fein-lab/fein && git checkout claude/focused-brahmagupta-g3hraq` |
| Timers don't run after logout | `sudo loginctl enable-linger fein` |
| See the schedule | `systemctl --user list-timers 'fein-*'` (or `crontab -l`) |
| Job log from systemd | `journalctl --user -u fein-collect.service -n 50` |
| "another run holds the lock" / "skipped" | The previous run is still going (normal on heavy result days). |
| Disk warning | Old raw files: `find ~/fein-data/raw -mindepth 1 -maxdepth 1 -type d -mtime +365 -exec rm -rf {} +` (optional; keeps one year). |
| Start over | `deploy/pi/uninstall.sh` then `deploy/pi/install.sh`. `--purge` also deletes `~/fein-data` (asks first). |
