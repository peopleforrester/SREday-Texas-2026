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
- **Event page:** <https://sreday.com/2026-austin-q2/> — source of truth
  for date, venue, format, and (eventually) the session schedule.
- **CFP / submission page:** <https://www.papercall.io/sreday-2026-austin-q2>.

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
- **Bio versions:** `abstract/bio.md` is the talk-page bio Michael
  sent on 2026-05-03 (KodeKloud-affiliated, 30 years experience,
  100K+ engineers taught, KCD Texas / KubeCon EU / KubeAuto AI Day
  references, with the personal closing "This is for both of them.
  This is for SRE Day"). The earlier as-submitted CFP bio is in git
  history; check `git log -- abstract/bio.md` if anyone asks for it.

## Where we left off

Talk-page submission captured (2026-05-03): **session time 12:30 on
May 11, 2026**, and the revised speaker bio. README surfaces the
12:30 slot in Event Details; `abstract/bio.md` now holds the
talk-page version of the bio (the earlier as-submitted CFP bio
remains in git history if needed). Pytest suite green (31 tests).

All external blockers (abstract, schedule, session time, bio) are
closed. Remaining work is content authoring: SREday-tuned outline
in `outline/`, then deck adaptation in `deck/`. The April 21, 2026
DevOpsDays Atlanta Ignite cut is the most recent rehearsal of the
substance — see "Rehearsal signal — DevOpsDays Atlanta Ignite" below
for the implication for the 30-minute cut.

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

## Rehearsal signal — DevOpsDays Atlanta Ignite (2026-04-21)

The 5-minute Ignite cut at DevOpsDays Atlanta on 2026-04-21 was a
strong rehearsal of the shared substance. Per Michael's report:
audience laughed at almost every beat and gave a standing ovation
at the end.

Implication for the 30-minute SREday cut on 2026-05-11:

- Comedic beats are validated — keep the same tone and timing in
  the longer cut. Don't over-formalize.
- A standing ovation off a 5-minute version means the through-line
  works compressed; the 30-minute version's risk is energy sag in
  the middle, not a weak premise. Pace the guardrails section
  deliberately so it does not become a lecture.
- The April 21 cut is the most recent live timing reference for any
  shared material. Until a longer rehearsal exists, treat Atlanta
  pacing data as authoritative for the segments that overlap.
