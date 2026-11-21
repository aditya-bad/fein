# FEIN change detectors

Two plain Python 3 scripts (standard library only, plus the system `curl` for BSE) that run
unattended on a Raspberry Pi, collect Indian exchange disclosures every evening and flag changes
worth a human look. No Claude, no pip packages, no API keys.

| File | Job |
|---|---|
| `collect.py` | Pulls NSE corporate announcements (main board + SME), PIT insider disclosures, SAST Reg 29, bulk and block deals, the all-company NSE promoter-pledge snapshot, and BSE announcements as a backup feed. Raw responses are kept gzipped under `$FEIN_DATA/raw/YYYY-MM-DD/`; normalised rows go into `$FEIN_DATA/fein.sqlite`. |
| `detect.py` | Runs the rules below over the database and writes `$FEIN_DATA/alerts/YYYY-MM-DD.md` and `.csv` (columns: date, symbol, rule, details, source_url). An alert is reported once, on the day it is first seen. |
| `fein_common.py` | Shared code: HTTP with pacing and back-off, date/number parsing, SQLite schema. |

`FEIN_DATA` defaults to `~/fein-data`. Logs go to `$FEIN_DATA/logs/collect.log` and `detect.log`.

This is a research tool, not SEBI-registered advice. An alert means "open the filing", not "trade".

## Rules

| rule | fires when |
|---|---|
| `pledge_up` | promoter pledge is up 2 points or more between the two latest snapshots, on either basis: % of promoter holding (NSE `percPromoterShares`) or % of total equity (`percTotShares`). `percSharesPledged` is never used, because it includes non-promoter pledges (lesson L6). |
| `pledge_cross_10/25/50` | either basis crosses 10%, 25% or 50% (the highest level crossed is reported) |
| `pledge_down` | pledge down 2 points or more (low priority, listed last) |
| `pledge_invocation` / `pledge_release` | PIT rows with mode "Invocation of pledge" / "Revokation of pledge", or announcement text about pledge or encumbrance invocation or release |
| `insider_buy` / `insider_sell` | promoter, promoter group, director or KMP open-market buy of Rs 1 cr or more / sale of Rs 5 cr or more (PIT Reg 7) |
| `sast_promoter_open_market` | promoter open-market buy or sale filed under SAST Reg 29 (stand-in while NSE's all-market PIT feed is empty, see Known limits) |
| `insider_cluster` | 2 or more different insiders in the same stock and direction, open market, within 30 days |
| `auditor_resignation` / `auditor_change` | statutory auditor resigns / is changed (internal, secretarial and cost auditors are ignored) |
| `kmp_resignation` | CFO, CEO, company secretary or compliance officer resigns |
| `rating_downgrade` / `rating_not_cooperating` | rating downgrade, negative watch or outlook / "issuer not cooperating" |
| `default_delay` | "default", "delay in payment", "non-payment of interest" and similar (filings saying "no default" are skipped) |
| `insolvency_new` | insolvency (CIRP) admitted or initiated |
| `large_deal` | a client's net bulk/block deal in a stock on one day is 1% of equity or more (Rs 50 cr or more if the share count is unknown). Same-day buy-and-sell round trips net to zero and drop out. |

Thresholds are constants at the top of `detect.py`.

## Raspberry Pi setup (Raspberry Pi OS, ARM64)

```bash
sudo apt update
sudo apt install -y python3 poppler-utils sqlite3 git curl
sudo timedatectl set-timezone Asia/Kolkata      # so cron times below are IST
git clone https://github.com/aditya-bad/fein.git ~/fein   # private repo: use a GitHub token or deploy key,
                                                          # or just copy tools/detectors/ onto the Pi
mkdir -p ~/fein-data
echo 'export FEIN_DATA=$HOME/fein-data' >> ~/.bashrc
```

`poppler-utils` (`pdftotext`) is not needed by the detectors; it is there for reading the filing
PDFs that alerts link to. `curl` is preinstalled on Raspberry Pi OS; BSE only answers over HTTP/2,
which Python's urllib cannot do, so `collect.py` calls `curl --http2` for BSE.

Check that everything works, then build a first baseline:

```bash
cd ~/fein/tools/detectors
python3 collect.py --selftest      # live, tiny fetch of every source, writes nothing
python3 detect.py --selftest       # live Indo Tech pledge check + offline rule tests
python3 collect.py                 # yesterday -> today
python3 detect.py
```

The pledge rules compare two snapshots, so they only start firing from the second evening.

Useful options:

```bash
python3 collect.py --from 2026-11-18 --to 2026-11-20   # backfill a range
python3 collect.py --only pledges,deals                # subset: announcements,bse,insider,sast,deals,pledges
python3 collect.py --no-bse                            # skip the BSE backup feed
python3 detect.py --from 2026-11-18 --to 2026-11-20 --all   # re-list alerts already seen
```

Exit codes: `collect.py` returns 1 only if every step failed (each step is logged and recorded in
the `runs` table); `detect.py` returns 0 unless it crashes. Only one copy of `collect.py` runs at a
time (lock file in `logs/`).

## Schedule: cron

`crontab -e` (Pi timezone set to Asia/Kolkata as above):

```cron
FEIN_DATA=/home/pi/fein-data
# collect at 21:00 IST, Monday to Saturday (Saturday picks up Friday-night filings)
0 21 * * 1-6  cd /home/pi/fein/tools/detectors && /usr/bin/python3 collect.py >> /home/pi/fein-data/logs/cron.log 2>&1
# detect at 21:30 IST
30 21 * * 1-6 cd /home/pi/fein/tools/detectors && /usr/bin/python3 detect.py >> /home/pi/fein-data/logs/cron.log 2>&1
# optional: keep one year of raw files
15 3 * * 0    find /home/pi/fein-data/raw -mindepth 1 -maxdepth 1 -type d -mtime +365 -exec rm -rf {} +
```

If the Pi stays on UTC instead, use `30 15` and `0 16` (21:00 and 21:30 IST). Replace `pi` with
your user name.

## Schedule: systemd timer (alternative)

systemd can use IST directly and catches up a run missed while the Pi was off (`Persistent=true`).

`/etc/systemd/system/fein-collect.service`:

```ini
[Unit]
Description=FEIN collect exchange disclosures
Wants=network-online.target
After=network-online.target

[Service]
Type=oneshot
User=pi
Environment=FEIN_DATA=/home/pi/fein-data
WorkingDirectory=/home/pi/fein/tools/detectors
ExecStart=/usr/bin/python3 collect.py
ExecStartPost=/usr/bin/python3 detect.py
Nice=10
IOSchedulingClass=idle
MemoryMax=300M
TimeoutStartSec=2h
```

`/etc/systemd/system/fein-collect.timer`:

```ini
[Unit]
Description=FEIN collect at 21:00 IST

[Timer]
OnCalendar=Mon..Sat 21:00 Asia/Kolkata
Persistent=true
RandomizedDelaySec=120

[Install]
WantedBy=timers.target
```

Here `detect.py` runs right after `collect.py` finishes instead of at a fixed 21:30. If you want
them separate, make a `fein-detect.service` plus timer with `OnCalendar=Mon..Sat 21:30 Asia/Kolkata`.

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now fein-collect.timer
systemctl list-timers fein-*
journalctl -u fein-collect.service -n 50
```

## Log rotation

The scripts reopen their log file if it is moved, so plain logrotate works.
`/etc/logrotate.d/fein`:

```
/home/pi/fein-data/logs/*.log {
    weekly
    rotate 8
    compress
    missingok
    notifempty
}
```

## SD-card and memory notes

- SQLite runs in WAL mode with `synchronous=NORMAL`, an 8 MB page cache and one commit per
  dataset per day, so each evening is a handful of sequential writes. The WAL is checkpointed at
  the end of `collect.py`.
- Raw files are gzipped JSON, roughly 0.3 to 0.5 MB per trading day.
- The heaviest step, the all-company pledge snapshot, holds one JSON response of about 1,500 rows in
  memory. Peak memory of a full run is measured below.
- A full evening run makes roughly 100 to 150 HTTP requests spaced at least 1.5 s apart, so it takes
  a few minutes. 403/429/5xx get exponential back-off (5, 10, 20 s), then the step is logged as
  failed and the run moves on.
- To look at the data: `sqlite3 ~/fein-data/fein.sqlite "select * from alerts order by first_seen desc limit 20"`.

## Known limits (checked November 2026)

- NSE's all-market PIT feed (`corporates-pit` with dates) has returned nothing since about
  May 2026. `collect.py` falls back to per-symbol PIT calls for up to 25 companies a day that filed
  promoter SAST disclosures or insider-trading announcements, and `sast_promoter_open_market` covers
  promoter trades from SAST. Insider coverage is therefore partial: smaller insiders in companies
  without a same-day SAST filing can be missed.
- About 80 of about 1,500 companies in the pledge snapshot are not matched to an NSE symbol (mostly
  BSE-only or delisted names). They are logged and skipped.
- Announcement rules are keyword rules on the exchange's one-line text. They catch most events,
  with some false positives (read the filing) and misses where the detail is only inside the PDF.
- Bulk/block deal percentages need a share count: from the pledge snapshot, otherwise from the
  latest shareholding-pattern XBRL (cached for 100 days).
- NSE moved its host to `www.nseindia.in` in 2026 and changes endpoints without notice. If a
  selftest line fails, the endpoint has probably changed; the raw files show what came back.

## Test run and sample alerts

SAMPLE_PLACEHOLDER
