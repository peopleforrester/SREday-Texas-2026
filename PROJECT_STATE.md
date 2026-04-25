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
- [ ] Populate `abstract/` with as-submitted SREday abstract and bio
- [ ] Draft SREday-tuned outline in `outline/` (emphasis: blast-radius,
      reversibility, operational controls)
- [ ] Import / adapt deck from `claude-deleted-my-cluster-2026` into
      `deck/` once the SREday timebox is known
- [ ] Write speaker notes in `speaker-notes/`
- [ ] Rehearse and capture timing notes

## Last completed step

Repo initialized. Scaffold committed on `staging`, merged to `main`,
and both branches pushed to the new public GitHub repo.

## Next step

Two inputs from Michael are blocking further work; chase them in this
order.

1. **Primary — submitted abstract and bio text.** This blocks talk
   content. Once received, create `abstract/abstract.md` and
   `abstract/bio.md` and lift the paraphrased summary out of the README.
2. **Secondary — event date, timebox, and room.** This blocks only the
   README placeholders and any timing-dependent outline decisions.
   When SREday publishes the schedule, fill in the README "Event
   Details" section.

## Branch and test status

- Branches: `main`, `staging` — both at the same commit.
- Tests: none yet — this is a talk repo, not a code project. Adding a
  test suite is not planned unless deck-generation tooling is added
  later.

## Verification method used

- **Research / manual:** all decisions were drawn from Michael's
  direct instruction and inspection of sibling repo structures.
- **Shell verification:** `git log`, `git branch -vv`, `gh repo view`
  used to confirm commit and remote state. No browser, no external
  APIs.

## Known unverified items

- Event date, timebox, and room — marked TBD in README.
- As-submitted abstract text — README uses a paraphrased summary
  until Michael supplies the exact submitted copy.
