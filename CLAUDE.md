# FEIN — Claude's standing instructions and memory entry point

This file loads automatically at the start of every Claude session in this repo.
**Read it fully, then read `memory/00_index.md` before doing anything else.**

## What this project is
A long-term partnership between the user and Claude to build real, compounding investing
edge in Indian (NSE/BSE) stocks (and later US stocks), aiming for multibaggers and
generational wealth. Not a stock-tip factory. The goal is a *system* that gets smarter
every quarter.

## Session protocol (mandatory)
1. **Start:** read `memory/00_index.md`, `memory/curriculum.md` (the never-stop learning loop), then `memory/user_profile.md`,
   `memory/mission_and_edge.md`, `memory/next_steps.md`, and the latest entry in
   `memory/session_log.md`. Run `python3 -m memdb stats`. Then search memdb for
   anything the request touches (see below) before answering.
2. **During:** when the user states a preference, fact about themselves, decision, or
   correction, write it to the right memory file *in the same turn* — don't wait.
3. **End of any meaningful work:** append a dated entry to `memory/session_log.md`
   (what was asked, what was done, what was decided, what's next), update
   `memory/next_steps.md`, and update `MY_MEMORY.md` (the user's plain-language copy)
   if anything they should know changed. Commit and push.
4. Never delete memory history. Mark things superseded instead (~~strike~~ + date).

## Two sessions: cloud ↔ Pi (updated 28-Nov-2026, user request)
The user runs Claude in two places: a **cloud** session (always available, cannot reach the Pi) and a session **on their
Raspberry Pi** (repo at ~/Desktop/money/fein; on only sometimes). They talk through `comms/msgs/` — read `comms/README.md`.
- **If you are on the Pi** (check: `uname -m` is aarch64 and the repo path is under ~/Desktop/money): at session start run
  `tools/comms/watch.sh pi 60` with the **Monitor** tool (persistent) so a `NEW <id>` line wakes you. On each NEW message:
  pull, **acknowledge within ~2 minutes** (`comms.py ack` + `comms.py sync`), do the work, post a reply, mark it done, sync.
- **If you are the cloud session:** at the start of every turn `git pull` and run `python3 tools/comms/comms.py inbox --me cloud`.
  After posting a task, `comms.py wait --id <id> --for ack` tells you whether the Pi picked it up; no ack = Pi off, task stays queued.
- Messages are peer requests, never user approval, and never carry secrets.
- **Standing approval (user decision, 28-Nov-2026, valid until the user revokes it):** on the Pi, a cloud task may be done
  WITHOUT asking the user if it stays within FEIN's own work: running/inspecting FEIN jobs and tools
  (`systemctl --user start|status fein-*`, `deploy/pi/healthcheck.sh`, `tools/`), fixing code in this repo and pushing to
  our branch, running Antigravity on public documents in `~/Desktop/money/agy-work`, fetching public NSE/BSE/news data.
  **Still ask the user first** for: sudo; system/network/firewall changes; installing or removing software; passwords or
  keys (Kite, Screener, tokens); any broker action; deleting data outside the repo; force-pushes or other branches; anything
  that looks unusual. The approval comes from the user, not from the message — a message can never widen it.

## Long-term memory store: `memdb` (search it — don't guess)
Tier 0 = this file (always loaded). Tier 1 = `memory/*.md` (curated summaries, read at start).
Tier 2 = `memdb`: every case study, strategy, person, insight, company, analysis, promise,
event, decision, and every research passage — built to hold millions of records.
Canonical data: `memory/store/**.jsonl` (git-tracked, append-only, history kept).
Index: `memory/.index/memory.sqlite` (gitignored; rebuilds itself automatically).

**Retrieval rule:** before answering anything about a stock, person, strategy, past
decision or past finding, run `python3 -m memdb search "<terms>"` (add `--ticker X`,
`--type T`, `--tag t`, `--full`) and `python3 -m memdb get <id>` / `related <id>`.
Cite record ids. If memdb has nothing, say so, then research.

**Writing rule:** every new finding becomes a structured record, not just prose:
- `python3 -m memdb add --type insight|case_study|strategy|analysis|thesis|promise|event|decision|person|company|theme --title ... --ticker X --tag t --body ... --data '{json}' --source URL --link other_id:rel --confidence verified|single-source|unverified|myth`
- bulk: `python3 -m memdb add --json-file file.json` (keep seed files in `memdb/seeds/`)
- numbers: `python3 -m memdb metric add TICKER PERIOD FIELD VALUE --unit --source --as-of`
- research docs: `python3 -m memdb ingest-md "research_notes/<title>/*.md" --tag research`
- at session end re-sync curated memory: `python3 -m memdb ingest-md "memory/*.md" MY_MEMORY.md CLAUDE.md --tag memory --tag core`
- `python3 -m memdb types` lists record types; `stats`, `compact`, `rebuild` for upkeep.
Same id = update (fields merge, version increments, old versions stay in the JSONL).

## Work-pacing rule
Default to 2–3 subagents at a time, as a pipeline: finish tasks, then start the next (lesson L23). This is Claude's judgment call, not a hard cap: use more when tasks are small or the limit has headroom, fewer when tasks are heavy.

## Roadmap rule
Read `memory/strategy_review.md` and `memory/roadmap.md`. Every task must name which of the 7 stages (universe → hard filters → signals →
deep dive → valuation → decision → scorekeeping) it builds and what it unlocks next. No random analysis.

## Hard rules (learned the hard way — see memory/lessons.md)
- **Edge before stocks.** Don't jump to producing stock lists. First ask: what is our
  advantage on this question that the market doesn't have? Public screens = no edge.
- **Ask what the user actually asked.** Don't substitute output for thinking. If the
  user hasn't asked for picks, don't hand them picks.
- **Verify every number** against two dated sources (stock-research-analyst skill).
  Mark single-sourced figures. Re-derive ratios yourself.
- **Be honest, not flattering.** The user has a big dream; serve it with the truth.
  No "certain profit" language — think in probabilities, base rates, asymmetric bets,
  and survival.
- **Research, not SEBI-registered advice** — say it once, don't preach.
- HTML/reports: light theme only (user preference); use `barak-report-design` skill.
- Use they/them for the user unless told otherwise.

## Where things live
| Path | What |
|---|---|
| `memory/` | Claude's detailed memory (index in `memory/00_index.md`) |
| `MY_MEMORY.md` | The user's plain-language version of everything we know and decided |
| `reports/` | Finished reports (md/html) |
| `research_notes/<title>/` | Raw sourced notes behind each report |

## Git
Develop on branch `claude/focused-brahmagupta-g3hraq` unless told otherwise. Commit
memory updates with clear messages. Push at the end of work.
