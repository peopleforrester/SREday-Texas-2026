# The Day an AI Agent Deleted My Cluster

Venue-specific materials for the talk at **SREday Austin / Texas 2026**.

**Status:** Accepted. Speaker: Michael Forrester.

## Talk Summary

In late 2025, a Claude Code agent was given direct, unguarded access to a
nine-node production homelab Kubernetes cluster. It deleted the cluster.

This talk walks through the session transcripts: the prompt that started
it, the failure chain that let a single tool call cascade into cluster
destruction, and the **Eight Guardrails Framework** that would have
stopped it at any of several points. The content is built from actual
JSONL session data, not reconstructions — every destructive command in
the narrative is a real one pulled from the transcript.

The SREday version is tuned for an SRE audience: the emphasis is on
blast-radius management, reversibility, and the operational controls
that make AI-agent-driven infrastructure safe to run in production.

## Related Repositories

The analysis, raw session data, and shared content live in sibling repos.
This repo intentionally does **not** duplicate that substance — it holds
only the SREday-specific deliverables.

| Repo | Purpose |
|---|---|
| `events/claude-deleted-my-cluster-2026` | Source of truth: session JSONL, parsed timeline, forensic evidence, core presentation facts |
| `events/DevOpsDays-Atlanta-2026` | Ignite (5-minute) version of the talk |
| `events/LLMday-Texas-2026` | Sibling venue, different angle |
| `events/kubeauto-ai-day` | Extended content on AI-driven Kubernetes automation |

## Repository Layout

What currently exists. The scaffold is intentionally light — directories
are created as content lands, not as empty placeholders.

- `README.md` — this file
- `CLAUDE.md` — project-specific instructions for Claude Code sessions
- `MEMORY.md` — session memory index
- `PROJECT_STATE.md` — durable state for `/continue` across sessions
- `LICENSE` — license terms (CC BY 4.0)
- `pyproject.toml`, `uv.lock` — Python project config (used by the test suite)
- `docs/` — plans and supporting documents for repo work
- `tests/` — consistency suite asserting durable-state files match reality

## Roadmap

Directories planned but not yet created. They will appear here as
content for them is produced.

- `abstract/` — as-submitted abstract, bio, session metadata
- `outline/` — SREday-tuned outline and timebox plan
- `deck/` — slides for this venue
- `speaker-notes/` — speaker notes tuned for the SREday audience and timebox
- `post-event/` — recording link, slides-as-delivered, audience feedback

## Asset Policy

- **Deck source is committed; PDF exports are derived and not committed.**
  Exports are regenerated from source on every build, so they only
  pollute diffs. `.gitignore` ignores `deck/*.pdf` and `outline/*.pdf`.
- **Publishable PDFs** (e.g. a slides-as-delivered handout) belong in
  `post-event/`, which is not blanket-ignored.
- **Rehearsal recordings** (`*.wav`, `*.m4a`, etc.) are gitignored —
  they are local-only artifacts and not appropriate for a public repo.
- **Session transcripts with real credentials, unredacted customer
  data, or private financial info** belong in the private analysis
  repo (`events/claude-deleted-my-cluster-2026`), never here.

## Event Details

- **Event:** SREday (Texas / Austin edition)
- **Year:** 2026
- **Status:** Accepted
- **Date, timebox, and room:** _TBD — fill in once the schedule drops_

## License

Talk content (abstract, slides, speaker notes, and prose in this
repository) is licensed under [CC BY 4.0](LICENSE). Reuse with
attribution.

## Author

Michael Forrester — [michael@performantpro.com](mailto:michael@performantpro.com)
