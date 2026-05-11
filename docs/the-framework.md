# The Framework

The mental model from the SREday Austin Q2 2026 talk "The Day an AI
Agent Deleted My Cluster (And the Guardrails That Would Have Stopped
It)," with the **bypass column filled in** for every enforcement
artifact. The structure is the speaker's; the bypass material is
added here so the reference is honest about what each layer does
and does not catch.

## The Eight Guardrails

The talk's named framework. Deck slide 17 (Level 5 :: The Eight)
lists them; the abstract calls out "Eight Guardrails Framework"
explicitly. Each guardrail is a principle. The four-layer mental
model below is **how the principles get enforced** in practice —
think of the eight as the *what*, and the four layers as the *where*.

| # | Guardrail | Primarily enforced at | Concrete artifacts in this repo |
|---|---|---|---|
| 1 | **Treat agent as untrusted workload** | Principle — pervades all four layers | `docs/the-framework.md` (this doc), `hooks/README.md` |
| 2 | **Sandbox by default** | Agent / host | None in this repo (host sandbox is a deck-acknowledged gap); see slide 19 for "OS-level isolation is currently the strongest line" |
| 3 | **Never give agent your permissions** | Server / target | Not enforced via repo artifacts — server-side RBAC and IAM scope; see the "Identity" and "Authorization" rows of the bypass matrix below |
| 4 | **Tiered approval** | Client + server | `hooks/git/pre-commit` (T1), `hooks/git/pre-push` (T2 secret-scan + units, T3 e2e on main) |
| 5 | **Cluster-level policy** | Server / target | Not enforced via repo artifacts — Kyverno / OPA admission policies on the target cluster |
| 6 | **IaC behind a gate** | Server / git+ci | `workflows/ci.yml` and `workflows/e2e.yml` (plan-and-apply split lives in the IaC pipeline, not here) |
| 7 | **Audit the MCP attack surface** | Agent / framework | `hooks/claude-code/block-sensitive-files.sh` (operator-owned deny-list); MCP server allowlist lives in `~/.claude/settings.json` per operator |
| 8 | **Monitor agents like production** | Cross-cutting (Detect / Respond) | `hooks/claude-code/harvest-journal.sh` (session capture for retrospective); production Detect / Respond / Recover live in separate matrices |

Slide 18 calls out **#3 and the identity-half of #1** as "the two
most-skipped — where the headlines come from." Pull your audit log
on Tuesday: *who's the actor, what's the scope.*

The rest of this document is the four-layer enforcement model —
how the eight above get made real in code and policy.

## Mental model

Four layers, top to bottom:

| Layer | What it owns | Where it lives |
|---|---|---|
| **PRD (planning / governance)** | What we're going to build and why | `prds/`, `claude-config/skills/prd/` |
| **Tasks (decomposition)** | The orderable, claimable units that satisfy a PRD | `tasks.yaml`, `scripts/tasks.sh`, `claude-config/skills/task/` |
| **Skills (agent hands)** | What the agent runs to *do* the work | `claude-config/skills/<name>/SKILL.md` |
| **Hooks / CI / timers (enforcement)** | What guarantees correctness while the work happens | `claude-config/hooks/`, `.github/workflows/`, `claude-config/systemd/`, each clone's `.git/hooks/` |

Hooks don't know about PRDs. PRDs don't run hooks. The two meet
through the skill layer and the human/agent operator who drives them.

## 1. Client side — Claude Code session lifecycle

Wired in `claude-config/settings.json` under the `"hooks"` key.
Scripts live in `claude-config/hooks/` and are symlinked into
`~/.claude/hooks/` so any edit is live immediately.

| Event | Hook | Purpose | Known bypass |
|---|---|---|---|
| **SessionStart** | `session-start.sh` | Detect pending work + uncommitted changes; direct Claude to read `PROJECT_STATE.md` and reconcile before new edits | Advisory only. The agent can fail to read or fail to reconcile correctly. Model error or intentional non-compliance defeats it. |
| **PreToolUse** (Bash) | `check-commit-message.sh` | Block `git commit` if the message contains AI/Claude attribution patterns | `git commit --no-verify`; `git -c core.hooksPath=/dev/null commit`; editing the hook script if the hooks dir is writable by the agent; committing via direct filesystem writes rather than the `git` CLI. |
| **PreToolUse** (Edit\|Write) | `block-sensitive-files.sh` | Block writes to `.env`, credentials, keys, secrets — exit 2 (BLOCK) | Writing via `Bash` (`>` redirect, `cat <<EOF > .env`) bypasses Edit/Write entirely; pattern evasion (filename not in the deny-list); agent editing the deny-list if the hooks dir is writable. |
| **PostToolUse** (Edit\|Write) | `validate-file.sh` | Lint Python (ruff) and YAML (yamllint) on every write | **Post-hoc**: the write already happened. Catches violations but does not prevent them. Non-Python / non-YAML files skip entirely. Linter false negatives let bad code through. |
| **PostToolUse** (Edit\|Write) | `check-aboutme.sh` | Warn when a `.py` file is missing the `ABOUTME:` header | Warn-only, non-blocking. Trivially ignored. |
| **PostCompact** | `auto-reanchor.sh` | Re-anchor context after compaction — re-read `CLAUDE.md`, `PROJECT_STATE.md`, git state, surface orientation block | Re-orientation, not enforcement. Agent can drift again after the re-read. |
| **Stop** | `auto-test-on-stop.sh` | Run project tests after Claude finishes a response if a test runner is detected | Non-blocking. Test failures do not roll back the work that just happened. |
| **SessionEnd** | `harvest-journal.sh` | Trigger `harvest-sessions.sh` in the engineering journal repo to capture the session for retrospective | Capture only, no enforcement. Harvest-script errors mean a session goes unrecorded. |

## 2. Server side — Git, CI, systemd

### Git hooks — tiered local enforcement

`.git/hooks/` in every clone. The skill at
`claude-config/skills/review-hooks/` deploys and audits them.

| Hook | Tier | Runs | Known bypass |
|---|---|---|---|
| `pre-commit` | 1 | Fast lint + type check on staged files only (<5s target) | `git commit --no-verify`; `git -c core.hooksPath=/dev/null commit`; `rm .git/hooks/*` if filesystem write is allowed. |
| `pre-push` | 2 (any branch) | Secret scan + unit tests | `git push --no-verify`; bypassing the local hook by pushing from a different clone or CI environment. |
| `pre-push` | 3 (main only) | e2e gate | Same as Tier 2; also any operator with admin override on branch protection can force-push to `main` directly. |

### GitHub Actions — defense in depth for anyone without local hooks

The remote checks are the backstop for two failure modes: contributors
who never installed the local hooks, and agents that found a way
around them.

| Workflow | Triggers | Steps | Known bypass |
|---|---|---|---|
| `.github/workflows/ci.yml` | PR to main/staging, push to staging | ruff lint → mypy strict → README rules-table sync check → unit tests (`-m "not e2e"`) | Admin merge override on branch protection. Code that passes the linter but is wrong. UI-skipped checks. |
| `.github/workflows/e2e.yml` | PR to main | e2e tests requiring network access | Same as `ci.yml`; also flaky tests that pass on retry; tests that mock the real surface instead of hitting it. |

### systemd user timer

| Unit | Schedule | Action | Known bypass |
|---|---|---|---|
| `repo-backup.timer` | Daily at 03:00 | Fire `repo-backup.service` which mirrors gitignored content (env, configs, keys) from every `~/repos/` git repo to a private backup repo | Disabled timer. User account not logged in (user timers do not run without an active session). Backup destination compromise. Source filesystem failure between backups. |

## 3. Blocks — what the hooks refuse

Two explicit deny-lists, both source-controlled:

| Block | Defined in | Triggered by | Known bypass |
|---|---|---|---|
| Sensitive-file writes | `claude-config/hooks/block-sensitive-files.sh` | PreToolUse Edit\|Write on `.env*`, `credentials*`, `*.key`, `*.pem`, `id_*`, `*secret*` | Bash redirect (write the file with `>` instead of through Edit/Write). New file pattern not in the deny-list. Agent editing the deny-list. |
| AI/Claude attribution in commit messages | `claude-config/hooks/check-commit-message.sh` | PreToolUse Bash when the command is `git commit` | `--no-verify`; using a different shell tool to invoke git; committing via filesystem writes instead of the git CLI. |

GitHub Secrets / Dependabot vulnerability alerts add a third
deny-list layer on the remote side. Bypass: the alert exists but no
one acts on it (alert fatigue is the documented failure mode for
this category — see the BYPASSES doc in the covenants repo).

## 4. App agent — skills and rules

Skills are slash commands. Each is a directory under
`claude-config/skills/<name>/` with a `SKILL.md` prompt template
and an optional `scripts/` subdirectory for deterministic shell.

Skills are agent-side. They are **not enforcement** — the agent
can choose not to invoke them. They are how common workflows get
made repeatable and visible to the operator; the hooks layer is
what catches the agent when a workflow goes wrong.

| Skill | Triggered when | What it does |
|---|---|---|
| `/post-compact` | After a compaction event | Re-anchor context (manual mirror of the `auto-reanchor.sh` hook) |
| `/continue` | Resuming a session | Read `PROJECT_STATE.md`, task list, git log; pick next step |
| `/remediate` | After `/review-senior` | Convert review findings into phased TDD plan and ship them |
| `/task` | Any task operation | Manage `tasks.yaml` with dependency tracking and crash recovery |
| `/syncallthings` | Before any cross-repo work | Verify staging vs main drift, local vs remote sync |
| `/init-state` | New repo onboarding | Deploy `PROJECT_STATE.md` + state-persistence rule so `/continue` works |
| `/prd` | Any PRD lifecycle operation | Create / list / amend / close PRDs and keep markdown + GitHub issue in sync |

A `claude-config/rules/` tree (57 markdown files) loads
automatically based on file globs in YAML frontmatter — context
injection rather than hooks, but still part of the agent's runtime
surface.

## 5. PRD process — the planning layer above all of this

PRDs decide what gets built; hooks/CI/timers enforce correctness
while it happens; tasks decompose the PRD into orderable units;
skills are the agent's hands.

| Piece | Path |
|---|---|
| Markdown PRD files | `prds/<number>-<slug>.md` |
| GitHub issues (one per PRD) | labelled `prd:draft`, `prd:active`, `prd:done` |
| Skill that drives the lifecycle | `claude-config/skills/prd/SKILL.md` |
| Backing script | `claude-config/skills/prd/scripts/prd.sh` |

### Lifecycle

1. **`/prd new "<title>"`** → markdown file in `prds/` + matching
   GitHub issue with label `prd:draft`.
2. **`/prd status N active`** → label flips to `prd:active`; the
   signal to start work.
3. **Decompose** with `/task new ...` → `tasks.yaml` entries with
   `blocks` / `blocked_by` edges that mirror the PRD's milestones.
4. **Hooks fire as you work** — `validate-file.sh`,
   `check-commit-message.sh`, `block-sensitive-files.sh`, CI, etc.
   None of them know about PRDs; they just enforce correctness.
5. **`/prd status N done`** → issue closed; markdown stays as
   historical record.

The triangle pattern — issue + markdown + (eventual) PR — is
intentional: the issue gives a stable URL, the markdown survives
any repo loss because it's also in `repo-backups/`, and the PR
connects the work back to the discussion.

## One-line summary

> 8 Claude Code lifecycle hooks (SessionStart → SessionEnd), 2 git
> hooks (pre-commit + pre-push), 2 GitHub Actions workflows (ci +
> e2e), 1 systemd daily timer (repo-backup), a skill layer that
> turns common workflows into slash commands, and a PRD → tasks →
> skills → hooks pipeline that sits above all of it.

## What to read next

- **The matrix this fits into:** the three-column prevention matrix
  (in-agent < client-side < server-side) maps each layer above to
  one of the three columns. Client-side hooks dominate this
  document; server-side enforcement (CI, branch protection,
  Kubernetes admission) is where the matrix gets its strongest
  guarantees.
- **The bypasses in depth:** the talk's premise is that
  *every layer has a bypass and stacking them is the point.* The
  detailed bypass surface per control is the kind of thing you write
  down so you do not pretend a single layer is enough.
- **The incident itself:** what happened to a nine-node Kubernetes
  cluster in forty minutes, told from the session JSONL. That is
  what motivated this entire stack.

The talk recording and slides-as-delivered will land in `post-event/`
after May 11.
