#!/usr/bin/env bash
# ABOUTME: SessionEnd hook — triggers engineering journal session harvesting in background.
# ABOUTME: Runs harvest-sessions.sh if it exists, non-blocking.

set -euo pipefail

# Point these at your own paths. Defaults shown are the author's
# layout under ~/repos/mrf/ and will not exist on your machine —
# override via env vars or edit in place.
TASKS_SCRIPT="${TASKS_SCRIPT:-$HOME/repos/mrf/llm-coding-workflow/scripts/tasks.sh}"
HARVESTER="${HARVESTER:-$HOME/repos/mrf/Engineering_Journal/scripts/harvest-sessions.sh}"

# Mark interrupted tasks before session teardown
if [ -f "tasks.yaml" ] && [ -x "$TASKS_SCRIPT" ]; then
    "$TASKS_SCRIPT" interrupt 2>/dev/null || true
fi

if [ ! -x "$HARVESTER" ]; then
    # Harvester not installed — skip silently
    exit 0
fi

# Run in background so it doesn't block session teardown
nohup "$HARVESTER" > /dev/null 2>&1 &

exit 0
