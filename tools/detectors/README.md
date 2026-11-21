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

- **Insider (PIT) data is stale at the source.** NSE's PIT feed has no records dated after
  30-Apr-2026, both the all-market query and per-symbol queries (checked 21-Nov-2026), and BSE's
  insider endpoint returned nothing. So `insider_buy`, `insider_sell` and the PIT half of
  `insider_cluster` cannot fire until NSE resumes; `collect.py` logs a warning every day while it is
  stale. Promoter open-market trades still arrive through SAST Reg 29 (`sast_promoter_open_market`,
  and clusters built from SAST rows), but SAST has no rupee value, covers promoters only (not
  directors or KMP), and only applies to trades above the SAST reporting thresholds. The code keeps
  calling PIT (all-market, then per-symbol for up to 25 companies a day) so it recovers by itself.
- About 80 of about 1,500 companies in the pledge snapshot are not matched to an NSE symbol (mostly
  BSE-only or delisted names). They are logged and skipped.
- Announcement rules are keyword rules on the exchange's one-line text. They catch most events,
  with some false positives (read the filing) and misses where the detail is only inside the PDF.
- Bulk/block deal percentages need a share count: from the pledge snapshot, otherwise from the
  latest shareholding-pattern XBRL (cached for 100 days).
- NSE moved its host to `www.nseindia.in` in 2026 and changes endpoints without notice. If a
  selftest line fails, the endpoint has probably changed; the raw files show what came back.

## Test run and sample alerts

Live run on 21-Nov-2026 for events dated 2026-11-18 to 2026-11-20, with `FEIN_DATA` in a scratch folder:

```
collect.py --from 2026-11-18 --to 2026-11-20   16/16 steps ok, 358 s, peak memory 39.5 MB
  NSE announcements 517 / 540 / 479, BSE announcements 693 / 635 / 630,
  SAST 20 / 35 / 21, bulk+block deals 118 / 125 / 113,
  pledge snapshot 1,474 companies (81 names not matched to an NSE symbol)
detect.py  -> 72 alerts: pledge_cross_50 1, pledge_up 1, auditor_resignation 4, rating_not_cooperating 1,
  insolvency_new 2, kmp_resignation 13, insider_cluster 2, sast_promoter_open_market 23,
  large_deal 17, auditor_change 7, pledge_release 1
```

**Pledge rule check, Indo Tech Transformers (INDOTECH).** The live NSE snapshot (broadcast
20-Nov-2026, shareholding as of 30-Sep-2026) shows 6,152,236 of 10,620,000 shares pledged by
promoters: 57.93% of equity (`percTotShares`) and 82.41% of the promoter holding
(`percPromoterShares`). `percSharesPledged` says 61.97% because it includes non-promoter pledges,
which is why the code never uses it. A real first run has only one snapshot, so the test added a
baseline row dated 2026-11-12 at the level before the 21-Nov-2025 encumbrance disclosed under SAST
Reg 29(2) (+2,761,200 shares, so 3,391,036 shares = 31.93% of equity). The rule then fired
`pledge_cross_50` and `pledge_up`, as expected. `detect.py --selftest` repeats this check live every
time it runs.

Selected alerts from `alerts/2026-11-21.md`:

| date | symbol | rule | details |
|---|---|---|---|
| 2026-11-21 | INDOTECH | pledge_cross_50 | crossed 50% (of equity, of promoter holding); promoter pledge 45.43% -> 82.41% of promoter holding; 31.93% -> 57.93% of equity (snapshots 2026-11-12 vs 2026-11-21, SHP 2026-09-30) |
| 2026-11-21 | INDOTECH | pledge_up | promoter pledge 45.43% -> 82.41% of promoter holding; 31.93% -> 57.93% of equity (snapshots 2026-11-12 vs 2026-11-21, SHP 2026-09-30) |
| 2026-11-18 | KALIND | auditor_resignation | [BSE: Company Update / Resignation of Statutory Auditors] match 'Resignation of Statutory Auditors' - Intimation regarding resignation of M/s. PHHAD & Co LLP (formerly D G K T & Co LLP), Chartered Accountant as Statutory Audito... |
| 2026-11-20 | ICIL | kmp_resignation | [NSE: Resignation] match 'Chief Financial Officer and Key Managerial Personnel, has re' - Indo Count Industries Limited has informed the Exchange regarding Resignation of  Mr. Manish Bhatia as Chief Financial Officer of the com... |
| 2026-11-18 | TIAANC | insolvency_new | [BSE: Company Update / Appointment of Interim Resolution Professional (IRP)] match 'Interim Resolution Professional' - Dear Sir |
| 2026-11-20 | SINCLAIR | insider_cluster | 2 insiders buy in 30d (2026-11-20..2026-11-20): Navin Chand Suchanti; Pramina Suchanti |
| 2026-11-20 | GALLANTT | sast_promoter_open_market | Dinesh R. Agarwal (promoter) Sale 5,000,000 sh (2.07%) on 03-NOV-2026 to 03-NOV-2026; after 3.57% [Reg29(2)] |
| 2026-11-19 | IIFLCAPS | large_deal | bulk net BUY FIH MAURITIUS INVESTMENTS LTD: 44,000,000 sh, Rs 1,540.00 cr = 11.81% of equity |
| 2026-11-20 | GSTL | pledge_release | [NSE: Disclosure under SEBI Takeover Regulations] match 'revocation of Pledge' - Ragavan Rajkumar has submitted to  the Exchange  a copy of Disclosure regarding revocation of Pledge on Share under Regulation 31(2) of SEBI (SAST... |

The same alerts in `alerts/2026-11-21.csv` (first rows):

```csv
date,symbol,rule,details,source_url
2026-11-21,INDOTECH,pledge_cross_50,"crossed 50% (of equity, of promoter holding); promoter pledge 45.43% -> 82.41% of promoter holding; 31.93% -> 57.93% of equity (snapshots 2026-11-12 vs 2026-11-21, SHP 2026-09-30)",https://www.nseindia.in/api/corporate-pledgedata?index=equities&symbol=INDOTECH
2026-11-20,GALLANTT,sast_promoter_open_market,"Dinesh R. Agarwal (promoter) Sale 5,000,000 sh (2.07%) on 03-NOV-2026 to 03-NOV-2026; after 3.57% [Reg29(2)]",https://nsearchives.nseindia.in/corporate/Dis4_11202026154824_54207.zip
2026-11-19,IIFLCAPS,large_deal,"bulk net BUY FIH MAURITIUS INVESTMENTS LTD: 44,000,000 sh, Rs 1,540.00 cr = 11.81% of equity",https://www.nseindia.com/report-detail/display-bulk-and-block-deals
```

Things to know when reading alerts: `kmp_resignation` and `auditor_change` are the noisiest rules
(an appointment of a new auditor after a normal term ending also fires `auditor_change`).
`sast_promoter_open_market` includes trivial top-ups of a few thousand shares. Sort by rule priority,
which the .md file already does, and open the linked filing before drawing any conclusion.
