# PROJECT_STATE.md — SREday Texas 2026

Durable project state. Read this first at the start of any session.
Reconcile against `git log`, `git status`, and `gh repo view` before
trusting it — this file is updated by hand and can drift.

## Current plan

Initialize a venue-specific talk repo for SREday Austin / Texas 2026.
Mirror the lightweight structure used for other venue-specific repos
(DevOpsDays-Atlanta-2026, LLMday-Texas-2026) and keep the analytical
substance in `claude-deleted-my-cluster-2026`.

## Task checklist

- [x] Create `staging` branch from `main`
- [x] Write README.md with talk metadata, abstract, and pointers to
      source-of-truth repos
- [x] Write CLAUDE.md with project-specific instructions
- [x] Write MEMORY.md and PROJECT_STATE.md (state persistence)
- [x] Write .gitignore
- [x] Commit scaffold to `staging`
- [x] Create public GitHub repo `peopleforrester/SREday-Texas-2026`
- [x] Push `staging`, then fast-forward `main` and push
- [x] Apply senior-review fixes (TDD remediation series)
- [x] Populate `abstract/` with as-submitted SREday abstract and bio
      (organizers-only speaker notes captured locally, gitignored)
- [x] Verify event date / venue / timebox and lift TBD from README
      (May 11, 2026 at The Sunset Room, single track, 30-minute slot)
- [x] Confirm session time (12:30 on May 11) and revise bio for the
      talk page
- [x] Polish the public-facing repo: visitor-focused README,
      GitHub description / topics / homepage URL, asset policy
      relocated to CLAUDE.md
- [ ] Draft SREday-tuned outline in `outline/` (emphasis: blast-radius,
      reversibility, operational controls)
- [x] Adapt deck into `presentations/` (PPTX in place)
- [ ] Write speaker notes in `speaker-notes/`
- [ ] Rehearse and capture timing notes

## Last completed step

Pre-show cleanup: removed internal-process files (MEMORY.md,
historical TDD plan) from git tracking so the published repo reads
cleanly for students arriving from slide 20. Email contact updated
from the prior `performantpro.com` address to the gmail and Accenture
addresses. Pytest suite green (32 tests).

## Next step

After the talk, capture in `post-event/`:
- Recording link once SREday publishes
- Slides-as-delivered PDF if shared with attendees
- Audience reaction notes, Q&A surprises, anything worth folding
  back into the analysis repo

## Branch and test status

- Branches: `main`, `staging` — `staging` is ahead pending the FF
  merge in the senior-review-fix series.
- Tests: pytest consistency suite under `tests/`. Run with
  `uv sync && uv run pytest`. The suite asserts that durable state
  files match the actual repo and remote — exactly the class of bug
  the senior review surfaced.

## Verification method used

- **Automated:** pytest consistency suite (`tests/`) — covers GitHub
  owner, "Next step" framing, `.gitignore` coverage, README layout
  vs. on-disk dirs, and LICENSE presence.
- **Shell verification:** `git log`, `git branch -vv`, `gh repo view`
  used to confirm commit and remote state. No browser, no external
  APIs.

## Known unverified items

_None at the moment._ All external blockers (abstract, schedule,
session time, bio) are now closed. Remaining work is content
authoring: outline, deck, speaker notes, rehearsal.
