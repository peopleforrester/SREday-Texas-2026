# Plan: Apply Senior-Review Fixes

This plan addresses the senior developer review of the initial scaffold.
It is executed phase by phase on the `staging` branch with TDD: each
fix is preceded by a failing test that goes green when the fix lands.

## Approach

The repository is documentation-only, so the test suite is a
**consistency suite**: it asserts that the durable state files
(`PROJECT_STATE.md`, `MEMORY.md`, `README.md`, `.gitignore`) reflect
the actual state of the repository and remote.

This catches the exact class of bug the review surfaced — a stale
GitHub owner in `PROJECT_STATE.md` that drifted from `git remote`
reality — and prevents recurrence.

Tests are written in pytest. Python is the project language default
and pytest's assertion output is the right shape for documentation
consistency checks.

## Scope

**In scope (this plan):**

- Review item #1 — fix `PROJECT_STATE.md` GitHub owner drift
- Review item #2 — fix stale "Next step" framing
- Review item #3 — extend `.gitignore` for deck/talk asset types and
  pin a PDF-export policy
- Review item #4 — reword README "Repository Layout" so planned
  directories are not listed alongside present ones
- Review item #6 — add a LICENSE file
- Wrap durable state (`PROJECT_STATE.md`, `MEMORY.md`) around the new
  reality

**Out of scope (deferred, with reasons):**

- Review item #5 (cross-repo sibling-drift script) — premature with
  no shared content yet to diff. Revisit once `outline/` or `deck/`
  has substance.
- Review item #7 (`CITATION.cff`) — premature for a scaffold.
- Review item #8 (MEMORY.md path reference) — verified during
  planning; the path exists on this machine, no fix needed.
- Review item #9 (public email address) — speaker's call, not a
  defect.

## Phases

Each phase ends with a commit on `staging`. The full pytest suite must
be green before moving to the next phase. The final phase merges
`staging` to `main` and pushes both.

### Phase 1 — Test infrastructure

Create the test harness so the rest of the work can be TDD'd.

- `pyproject.toml` declaring pytest as a dev dependency
- `tests/__init__.py`
- `tests/conftest.py` exposing fixtures: `repo_root`, file readers
  for each durable doc, `git_remote_url`
- `tests/README.md` explaining the consistency-test philosophy

Exit condition: `pytest tests/` runs cleanly with zero collected
tests (framework wired, no assertions yet).

### Phase 2 — Write failing tests (TDD red)

One test module per review item, each asserting the desired post-fix
state. All five must fail at this point.

- `tests/test_state_consistency.py::test_project_state_owner_matches_remote`
- `tests/test_state_consistency.py::test_next_step_names_both_unknowns`
- `tests/test_gitignore_coverage.py::test_deck_asset_patterns_covered`
- `tests/test_gitignore_coverage.py::test_pdf_export_policy_documented`
- `tests/test_readme_layout.py::test_layout_dirs_exist_or_are_in_roadmap`
- `tests/test_license.py::test_license_file_present`

Exit condition: `pytest tests/` reports the expected number of
failures and zero unexpected errors. Commit the failing tests so the
red state is recorded.

### Phase 3 — Fix #1: PROJECT_STATE.md owner drift

- Replace `michaelrishiforrester/SREday-Texas-2026` with
  `peopleforrester/SREday-Texas-2026` in `PROJECT_STATE.md`
- Add the canonical remote URL near the top of `MEMORY.md` so it is
  not derivable only from `git remote -v`

Exit condition: `test_project_state_owner_matches_remote` passes.

### Phase 4 — Fix #2: stale "Next step"

Rewrite the "Next step" section of `PROJECT_STATE.md` to name both
blocking inputs explicitly:

1. Submitted abstract and bio text — primary, since talk content
   blocks on it
2. Event date, timebox, and room — secondary, blocks logistics

Exit condition: `test_next_step_names_both_unknowns` passes.

### Phase 5 — Fix #3: .gitignore extensions + PDF policy

Pin policy: **PDF exports are derived artifacts and are gitignored;
deck source is committed.** The rationale is that PDF exports are
re-generated from source on every run and pollute diffs. If the talk
ever produces a "publishable PDF" deliverable, it goes in
`post-event/` with an explicit override.

Patterns to add:

- Slide-tool intermediates: `.reveal-md/`, `_site/`, `dist/`, `build/`
- Lock files: `~$*.pptx`, `~$*.key`, `*.pptx~`
- LaTeX/Beamer: `*.aux`, `*.log`, `*.toc`, `*.nav`, `*.snm`,
  `*.out`, `*.synctex.gz`
- Audio (rehearsal recordings): `*.wav`, `*.m4a`, `*.aif`, `*.aiff`
- PDF exports: `deck/*.pdf`, `outline/*.pdf` (scoped, not global)

Document the PDF policy in a short "Asset policy" section of
`README.md`.

Exit condition: `test_deck_asset_patterns_covered` and
`test_pdf_export_policy_documented` pass.

### Phase 6 — Fix #4: README Repository Layout wording

Split the README "Repository Layout" section into two:

- **Repository Layout** lists only what currently exists.
- A new **Roadmap** section lists planned directories.

This removes the ambiguity the review flagged (a first-time reader
expecting `abstract/`, `outline/`, etc., to be present).

Exit condition: `test_layout_dirs_exist_or_are_in_roadmap` passes.

### Phase 7 — Fix #6: Add LICENSE

Add a `LICENSE` file using `CC-BY-4.0`. Rationale: standard for talk
content (prose, slides, speaker notes); allows reuse with attribution;
matches what most public-talk repos use.

If helper scripts ever land, dual-license becomes worth a follow-up;
for now, single-license is simpler and accurate.

Reference the license in `README.md`.

Exit condition: `test_license_file_present` passes.

### Phase 8 — Update durable state

- `PROJECT_STATE.md` task checklist: tick the senior-review items;
  add a "Verification: pytest suite green" line
- `MEMORY.md`: add a "Senior-review fixes" entry under decisions
- Confirm full `pytest tests/` is green

Exit condition: full suite green; durable state matches reality.

### Phase 9 — Merge to main

- Verify `staging` is clean and pytest passes
- `git checkout main && git merge --ff-only staging`
- Push `staging`, then push `main`
- Verify both remote refs are aligned

Exit condition: `gh repo view` shows both branches at the same
commit; `pytest tests/` is green on both branches.

## Decisions Made

These are choices the plan locks in so future readers don't have to
reverse-engineer them:

| Decision | Choice | Why |
|---|---|---|
| Test framework | pytest | Project language default; assertion output is well-suited to consistency checks |
| PDF policy | Ignore exports, commit source | Exports are derived; they pollute diffs |
| LICENSE | CC-BY-4.0 | Standard for talk content; permits reuse with attribution |
| Sibling-drift enforcement | Defer | No shared content to diff yet |
| `CITATION.cff` | Defer | Premature for a scaffold |

## Verification Method

- **Automated:** pytest consistency suite. Run with `pytest tests/`.
- **Manual:** `git remote -v`, `gh repo view`, `git log --oneline`
  for any state that is not yet covered by a test.
- **Out of scope:** browser/Puppeteer. There is nothing to render.
