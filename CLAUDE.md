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
