# Hooks — install this on your own machine

Working artifacts from the SREday talk, as presented May 11, 2026.
These are the actual scripts referenced in
[`docs/the-framework.md`](../docs/the-framework.md) and on stage. The
deck calls out eight Claude Code lifecycle hooks, two git hooks, one
GitHub Actions workflow, and one systemd timer. The first three are
in this directory and the next one over (`../workflows/`); the timer
is documented in the framework doc.

You already know CI. The "extra" for AI agents lives here.

## Layout

```
hooks/
├── claude-code/   8 lifecycle hooks (SessionStart → SessionEnd)
└── git/           pre-commit + pre-push (tiered local enforcement)
../workflows/      ci.yml (defense-in-depth for anyone without local hooks)
```

## 1. Claude Code lifecycle hooks → `~/.claude/hooks/`

These run inside the Claude Code agent session. They wire into the
agent's lifecycle so the agent can be redirected, blocked, lint-
checked, re-anchored, and journalled without prompting it to "be
careful."

| Script | Event | Purpose | Bypass |
|---|---|---|---|
| `session-start.sh` | SessionStart | Detect pending work in `PROJECT_STATE.md` + uncommitted changes; output a directive to read state and reconcile before new edits | Advisory; model can ignore the directive |
| `check-commit-message.sh` | PreToolUse (Bash) | Block `git commit` if message contains AI/Claude attribution (case-insensitive regex) | `--no-verify`; non-`git` shell out |
| `block-sensitive-files.sh` | PreToolUse (Edit\|Write) | Exit 2 (BLOCK) on writes to `.env`, `*.pem`, `*.key`, `id_*`, `*credential*`, `*secret*`, etc. | Write via Bash redirect; pattern evasion |
| `validate-file.sh` | PostToolUse (Edit\|Write) | Ruff (Python) and yamllint on every write | Post-hoc, catches not prevents; non-Py/YAML skipped |
| `check-aboutme.sh` | PostToolUse (Edit\|Write) | Warn when a `.py` file is missing the `ABOUTME:` header | Warn-only; trivially ignored |
| `auto-reanchor.sh` | PostCompact | Re-anchor context after compaction: re-read `CLAUDE.md`, `PROJECT_STATE.md`, git state, surface orientation block | Reorientation, not enforcement |
| `auto-test-on-stop.sh` | Stop | Run project tests after Claude finishes a turn if a runner is detected (pytest / npm test / cargo test) | Non-blocking; failures do not roll back |
| `harvest-journal.sh` | SessionEnd | Trigger an engineering-journal harvest in the background | Capture only; no enforcement. **Edit the `TASKS_SCRIPT` and `HARVESTER` paths at the top of the file before using** |

### Install

```bash
mkdir -p ~/.claude/hooks
cp hooks/claude-code/*.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

Then add the hooks block to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart":  [{"hooks": [{"type": "command", "command": "~/.claude/hooks/session-start.sh"}]}],
    "PreToolUse":  [
      {"matcher": "Bash",       "hooks": [{"type": "command", "command": "~/.claude/hooks/check-commit-message.sh"}]},
      {"matcher": "Edit|Write", "hooks": [{"type": "command", "command": "~/.claude/hooks/block-sensitive-files.sh"}]}
    ],
    "PostToolUse": [
      {"matcher": "Edit|Write", "hooks": [
        {"type": "command", "command": "~/.claude/hooks/validate-file.sh"},
        {"type": "command", "command": "~/.claude/hooks/check-aboutme.sh"}
      ]}
    ],
    "PostCompact": [{"hooks": [{"type": "command", "command": "~/.claude/hooks/auto-reanchor.sh"}]}],
    "Stop":        [{"hooks": [{"type": "command", "command": "~/.claude/hooks/auto-test-on-stop.sh"}]}],
    "SessionEnd":  [{"hooks": [{"type": "command", "command": "~/.claude/hooks/harvest-journal.sh"}]}]
  }
}
```

Restart Claude Code. The next session will fire `session-start.sh`
on entry and the rest will fire as their events occur.

## 2. Git hooks → `<repo>/.git/hooks/`

Tiered enforcement, fail-fast, language-aware. Detects Python /
Node / Rust / Go by config files at the repo root and runs the
appropriate linters and tests.

| Hook | Tier | Runs | Bypass |
|---|---|---|---|
| `pre-commit` | 1 | Fast lint + type check on **staged files only** (<5s target). Docs-only commits skip lint entirely. Per-repo opt-outs: `.skip-lint`, `.skip-typecheck` | `git commit --no-verify` |
| `pre-push` (any branch) | 2 | Secret scan (AKIA, ghp_*, sk-*, BEGIN PRIVATE KEY) + unit tests. `.skip-unit-tests` opts out | `git push --no-verify` |
| `pre-push` (main only) | 3 | e2e gate — Python `tests/e2e/`, Node `test:e2e` script, or `scripts/e2e-test.sh`. `.skip-e2e` opts out. `.direct-push-allowed` skips all pre-push checks | Admin force-push on a protected branch |

### Install (per repo)

```bash
cp hooks/git/pre-commit  /path/to/your-repo/.git/hooks/
cp hooks/git/pre-push    /path/to/your-repo/.git/hooks/
chmod +x /path/to/your-repo/.git/hooks/pre-{commit,push}
```

`.git/hooks/` is per-clone and not under version control. Re-install
after every `git clone`. Pair with `core.hooksPath` set to a tracked
directory if you want them versioned across the team.

## 3. GitHub Actions workflow → `<repo>/.github/workflows/`

Defense-in-depth for anyone who pushes without the local hooks
installed. See [`../workflows/ci.yml`](../workflows/ci.yml). Drop it
into your repo's `.github/workflows/` and adapt the test command to
your runner.

## What gets past all of this

Read [`../docs/the-framework.md`](../docs/the-framework.md) for the
full bypass column per artifact. Stacking layers is the point —
no single hook is unbypassable, but compromising the whole stack
requires multiple distinct moves at once.

## License

These scripts are MIT-licensed for free reuse (the talk repo
overall is CC BY 4.0 for prose; code artifacts are MIT). Steal
them, adapt them, ship them.
