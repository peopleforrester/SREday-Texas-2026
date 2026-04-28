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
- **License:** CC BY 4.0 for talk content (prose, slides, speaker
  notes). Standard for public talk repos; permits reuse with
  attribution.
- **PDF policy:** deck source is committed; PDF exports are derived
  and gitignored under `deck/` and `outline/`. Publishable PDFs (e.g.
  slides-as-delivered) belong in `post-event/`, which is not
  blanket-ignored.
- **Test framework:** pytest, resolved by uv. Suite is a *consistency
  suite* — it asserts durable-state files match the actual repo and
  remote. Plan and rationale: `docs/senior-review-fixes.md`.
- **Organizers-only speaker notes:** the submission form's "visible
  to organizers only" section is captured locally at
  `abstract/speaker-notes-organizers.md` but gitignored. The content
  is not sensitive, but the original framing was private, so the
  conservative default is no-publish. To publish, remove the entry
  from `.gitignore` deliberately.

## Where we left off

As-submitted SREday abstract and bio captured under `abstract/`.
README replaced its paraphrased Talk Summary with a short intro plus
a link to `abstract/abstract.md` (canonical). Organizers-only speaker
notes from the submission form captured locally as
`abstract/speaker-notes-organizers.md` but gitignored — the form
labelled them "visible to organizers only" so they stay out of the
public repo. Pytest suite green (29 tests).

Next blocking input is the event date, timebox, and room (was
secondary, now primary). The outline draft can begin once the
timebox is known. See `PROJECT_STATE.md` "Next step".

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

Senior-review fixes were applied via TDD: a pytest consistency suite
was wired up first, failing tests were committed to record the red
state, then each fix was driven to green one phase at a time with a
commit per phase. Plan in `docs/senior-review-fixes.md`.
