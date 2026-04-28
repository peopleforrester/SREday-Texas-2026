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
- [x] Apply senior-review fixes per `docs/senior-review-fixes.md`
      (items #1, #2, #3, #4, #6 — see "Senior-review fixes" below)
- [x] Populate `abstract/` with as-submitted SREday abstract and bio
      (organizers-only speaker notes captured locally, gitignored)
- [ ] Draft SREday-tuned outline in `outline/` (emphasis: blast-radius,
      reversibility, operational controls)
- [ ] Import / adapt deck from `claude-deleted-my-cluster-2026` into
      `deck/` once the SREday timebox is known
- [ ] Write speaker notes in `speaker-notes/`
- [ ] Rehearse and capture timing notes

## Senior-review fixes

Applied via TDD on `staging` per `docs/senior-review-fixes.md`. Each
item below has at least one consistency test in `tests/` that asserts
the durable state matches reality.

- [x] #1 Owner drift in `PROJECT_STATE.md` — corrected to
      `peopleforrester/SREday-Texas-2026`; canonical remote URL added
      to `MEMORY.md`. Test: `test_project_state_owner_matches_remote`.
- [x] #2 Stale "Next step" framing — rewritten with explicit
      primary/secondary ordering. Test:
      `test_next_step_names_both_unknowns`.
- [x] #3 `.gitignore` extended for slide-tool intermediates, Office /
      Keynote lock files, LaTeX/Beamer artifacts, rehearsal audio,
      and a scoped PDF-export ignore. PDF policy documented in
      README. Tests: `test_deck_asset_patterns_covered` (parametrized),
      `test_pdf_export_policy_documented`.
- [x] #4 README "Repository Layout" split into Layout (present today)
      and Roadmap (planned). Test: `test_layout_dirs_exist_or_are_in_roadmap`.
- [x] #6 LICENSE added (CC BY 4.0); README references it. Tests:
      `test_license_file_present`, `test_readme_references_license`.

Deferred items (with reasons in `docs/senior-review-fixes.md`):

- #5 cross-repo sibling-drift script — premature; no shared content
  to diff yet.
- #7 `CITATION.cff` — premature for a scaffold.
- #8 MEMORY.md path reference — verified valid during planning, no
  fix needed.
- #9 public email address — speaker's call, not a defect.

## Last completed step

Captured the as-submitted SREday abstract and bio under `abstract/`.
README defers to `abstract/abstract.md` as canonical instead of
paraphrasing. Submission's "organizers only" speaker notes captured
locally but gitignored from the public repo. Pytest suite green
(29 tests).

## Next step

With the abstract captured, the next blocking inputs shift one notch
down. Chase in this order.

1. **Primary — event date, timebox, and room.** Blocks the README
   placeholders, the SREday-tuned outline, and any timing-dependent
   deck decisions. Once SREday publishes the schedule, fill in the
   README "Event Details" section and revisit the deck timing.
2. **Secondary — draft the SREday-tuned outline in `outline/`.** The
   abstract is in hand, so the outline work is no longer blocked on
   external inputs (only on having the timebox to plan against).
   Emphasis: blast-radius, reversibility, operational controls.

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

- Event date, timebox, and room — marked TBD in README.
