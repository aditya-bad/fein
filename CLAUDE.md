# FEIN — Claude's standing instructions and memory entry point

This file loads automatically at the start of every Claude session in this repo.
**Read it fully, then read `memory/00_index.md` before doing anything else.**

## What this project is
A long-term partnership between the user and Claude to build real, compounding investing
edge in Indian (NSE/BSE) stocks (and later US stocks), aiming for multibaggers and
generational wealth. Not a stock-tip factory. The goal is a *system* that gets smarter
every quarter.

## Session protocol (mandatory)
1. **Start:** read `memory/00_index.md`, then `memory/user_profile.md`,
   `memory/mission_and_edge.md`, `memory/next_steps.md`, and the latest entry in
   `memory/session_log.md`. Skim others as relevant to the request.
2. **During:** when the user states a preference, fact about themselves, decision, or
   correction, write it to the right memory file *in the same turn* — don't wait.
3. **End of any meaningful work:** append a dated entry to `memory/session_log.md`
   (what was asked, what was done, what was decided, what's next), update
   `memory/next_steps.md`, and update `MY_MEMORY.md` (the user's plain-language copy)
   if anything they should know changed. Commit and push.
4. Never delete memory history. Mark things superseded instead (~~strike~~ + date).

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
