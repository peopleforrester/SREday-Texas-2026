# CLAUDE.md — SREday Texas 2026

Project-specific instructions for Claude Code sessions in this repo.
Global rules in `~/.claude/CLAUDE.md` still apply — this file only adds
context that is specific to this talk and venue.

## What this repo is

This is a **venue-specific** repo for the SREday Austin talk
"The Day an AI Agent Deleted My Cluster". It holds only the
SREday-specific deliverables (abstract as submitted, final deck for this
event, speaker notes tuned to this audience and timebox, post-event
artifacts). It does **not** own the underlying talk content.

## Source of truth

The analytical substance — session JSONL, parsed timeline, forensic
evidence, the Eight Guardrails Framework, and the shared core deck —
lives in `~/repos/events/claude-deleted-my-cluster-2026/`. Before
editing deck or outline content here, check there first. If the two
diverge, the analysis repo is authoritative.

Sibling venues that share the same substance:

- `~/repos/events/DevOpsDays-Atlanta-2026` — Ignite (5-minute) cut
- `~/repos/events/LLMday-Texas-2026` — different audience angle
- `~/repos/events/kubeauto-ai-day` — extended Kubernetes automation content

When you make a change here that would also apply to those venues
(e.g., a factual correction from the forensic data), flag it so the
change can be propagated — don't silently fork the story.

## Framework evolution — `agentic-covenants`

The next evolution of the framework — beyond the Eight Guardrails —
lives in `~/repos/events/agentic-covenants` (private:
<https://github.com/peopleforrester/agentic-covenants>). It already
has substance: `MATRIX.md`, `matrix.yaml`, `BYPASSES.md`,
`CITATIONS.md`, and `docs/`.

**Contract for this repo and this talk.** The submitted-and-accepted
SREday abstract names "Eight Guardrails Framework" explicitly, so
the main-stage framework on May 11 is the eight guardrails — full
stop. Renaming, renumbering, or replacing them would be a
bait-and-switch on attendees who came for what the abstract
promised.

**Where the covenants material can show up.** The submitted
structure ends with "5 minutes on what I still don't have a good
answer for." That closing is the right place to gesture at the
covenants direction as the next evolution — at that level of
fidelity (a pointer, not a parallel framework). Anything heavier
goes in a follow-on talk or a venue whose abstract was scoped to
the evolution, not this one.

## Workflow in this repo

- Branch rule: work on `staging`, merge to `main` after verification.
  This is a brand-new repo; protections are not yet configured on the
  remote, but the staging-first workflow still applies.
- Commits: professional tone, no AI/Claude attribution in commit
  messages (per global rule).
- Public repo: this repository is public on GitHub. Do not commit
  anything that is not safe to publish — session transcripts with real
  credentials, unredacted customer data, or private financial info go
  in the analysis repo (which is private), not here.

## Asset policy

What goes in the repo and what does not — relocated here from the
visitor-facing README during the polish pass.

- **Deck source is committed; PDF exports are derived and not
  committed.** Exports are regenerated from source on every build,
  so they only pollute diffs. `.gitignore` ignores `deck/*.pdf` and
  `outline/*.pdf`.
- **Publishable PDFs** (e.g. a slides-as-delivered handout) belong
  in `post-event/`, which is not blanket-ignored.
- **Rehearsal recordings** (`*.wav`, `*.m4a`, etc.) are gitignored —
  they are local-only artifacts and not appropriate for a public repo.
- **Session transcripts with real credentials, unredacted customer
  data, or private financial info** belong in the private analysis
  repo (`events/claude-deleted-my-cluster-2026`), never here. (Same
  rule as "Public repo" above; restated here next to the other asset
  decisions so it stays one mental category.)

## When working on deck / outline / speaker-notes

- The SREday audience is SRE-leaning. Tune emphasis toward
  blast-radius, reversibility, rollback, and operational controls —
  not toward the AI-agent novelty angle (that is the LLMday framing).
- The Eight Guardrails Framework is the load-bearing structure. Do not
  rename, renumber, or reorder the guardrails without checking the
  analysis repo — they are referenced externally.
- Quotes and command lines pulled from the incident must match the
  session JSONL exactly. Never paraphrase a destructive command for
  slide polish; if it reads awkwardly, use an annotation, not a rewrite.

## State persistence

Per `~/.claude/rules/state-persistence.md`, keep `PROJECT_STATE.md`
current at every transition, and update `MEMORY.md` with how work was
done, not just that it was done. `/continue` reads from these files.
