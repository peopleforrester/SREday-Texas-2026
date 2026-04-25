# MEMORY.md — SREday Texas 2026

Durable session notes for this repo. Survives `/clear` and compaction.
For global user-level memory, see `~/.claude/projects/*/memory/`.

## Canonical references

- **GitHub remote:** `git@github.com:peopleforrester/SREday-Texas-2026.git`
  (web: <https://github.com/peopleforrester/SREday-Texas-2026>).
  Note: `gh auth status` displays the account as `michaelrishiforrester`,
  but the actual login (and the only valid `gh repo create` namespace) is
  `peopleforrester`. Verify with `git remote get-url origin` rather than
  trusting any stored summary.

## Current work-in-progress

Repo initialization only. No talk content has been written yet —
outline, deck, and speaker notes are all TBD.

## Decisions so far

- **Repo scope:** venue-specific only. Substance lives in
  `claude-deleted-my-cluster-2026`; this repo does not duplicate it.
- **Visibility:** public on GitHub from day one (confirmed by Michael
  at initialization). Session JSONL and any sensitive forensic data
  stay in the private analysis repo.
- **Branch model:** staging-first per the global rule. `main` tracks
  only verified content.
- **Structure:** flat at the root for now. Directories (`abstract/`,
  `outline/`, `deck/`, etc.) are created when there is content to put
  in them — no empty placeholders with `.gitkeep`.

## Where we left off

Initial scaffold committed to `staging` and pushed. GitHub repo
created as public. `main` fast-forwarded from `staging` and pushed.
Next step is to populate `abstract/` with the as-submitted SREday
abstract and bio once Michael provides them.

## What is verified vs. asserted

- **Verified:** scaffold files exist, git log is clean, remote exists
  and has both branches. (Confirm via `git log`, `git branch -vv`,
  and `gh repo view`.)
- **Asserted but not verified:** event date, timebox, and room. These
  are marked TBD in the README pending the SREday schedule release.

## How work has been done

Initialization was done manually by Claude Code via the shell tools
(git, gh) and Write. No browser automation. No session JSONL was
copied from the analysis repo — that stays siloed until Michael
decides which excerpts (if any) should be published with the deck.
