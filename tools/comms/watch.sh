#!/usr/bin/env bash
# Watcher for the Pi (or cloud) Claude session. Run it under Claude Code's Monitor tool so each printed line wakes the agent:
#   tools/comms/watch.sh pi 60
# Every N seconds it fetches the branch and lists messages addressed to ME on origin that have no .ack file yet.
# It prints one line per NEW unacked message ("NEW <id>") and nothing otherwise. It never changes the working tree,
# never commits, never runs anything from a message. Cheap: one `git fetch` per poll, no model calls.
set -u
ME="${1:?usage: watch.sh pi|cloud [seconds]}"; EVERY="${2:-60}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; BR="${FEIN_BRANCH:-claude/focused-brahmagupta-g3hraq}"
declare -A seen
warned=0
while true; do
  if git -C "$ROOT" fetch -q origin "$BR" 2>/dev/null; then
    [ "$warned" = 1 ] && { echo "OK fetch back"; warned=0; }
    names="$(git -C "$ROOT" ls-tree --name-only "origin/$BR" comms/msgs/ 2>/dev/null | xargs -n1 basename 2>/dev/null)"
    for f in $(printf '%s\n' "$names" | grep -E '\.md$' | grep -vE '\.(ack|done)\.md$'); do
      id="${f%.md}"
      [ -n "${seen[$id]:-}" ] && continue
      printf '%s\n' "$names" | grep -qx "$id.ack.md" && { seen[$id]=1; continue; }
      to="$(git -C "$ROOT" show "origin/$BR:comms/msgs/$f" 2>/dev/null | sed -n 's/^to: *//p' | head -1)"
      [ "$to" = "$ME" ] && echo "NEW $id"
      seen[$id]=1
    done
  else
    [ "$warned" = 0 ] && { echo "WARN fetch failed (offline?) — will keep retrying quietly"; warned=1; }
  fi
  sleep "$EVERY"
done
