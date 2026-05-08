# The Day an AI Agent Deleted My Cluster

### And the Guardrails That Would Have Stopped It

A 30-minute talk by **Michael Forrester** at
[**SREday Austin Q2 2026**](https://sreday.com/2026-austin-q2/).

I gave Claude Code full Kubernetes cluster access and told it to fix
a networking issue. Forty minutes later the cluster was gone — etcd
force-overridden, netplan deleted across every control plane node,
no gate stopping any of it. The talk is the full incident, and the
**Eight Guardrails Framework** I spent the next six months building
to let agents operate fast inside a boundary they can't break out of.

> **When** — Monday, May 11, 2026 · 12:30 PM (30 minutes)
> **Where** — The Sunset Room, 310 E 3rd St, Austin, TX 78701
> **Format** — single track, 10:00 AM – 6:00 PM
> **Tickets** — [sreday.com/2026-austin-q2](https://sreday.com/2026-austin-q2/)

---

## What you'll walk away with

- **Lessons learned.** The actual command sequence, recovery, and the
  forty-minute timeline — pulled from real session JSONL, not
  reconstructed.
- **Deep dives.** The three-layer guardrail architecture: Git hooks
  (deterministic, local), Claude Code hooks (pre-tool-use blocking),
  and Kubernetes infrastructure (admission webhooks, RBAC, Falco
  runtime detection).
- **Culture and ways of working.** Why "the AI knows what it's doing"
  is the most dangerous assumption in modern SRE, and how to build
  operational habits that treat AI agents as nondeterministic systems.

The full as-submitted abstract is in
[**`abstract/abstract.md`**](abstract/abstract.md).

## What's in this repo

- [**`abstract/`**](abstract/) — the as-submitted talk abstract and
  speaker bio (canonical text for the talk).
- [**`docs/`**](docs/) — plans and supporting documents for repo work.
- [**`tests/`**](tests/) — a small consistency suite that asserts the
  durable-state files in this repo match reality (event date matches
  the conference page, GitHub owner matches `git remote`, README
  layout matches what is on disk, etc.).

After the talk, slides-as-delivered, the recording link, and audience
follow-ups will land in `post-event/`.

## Speaker

**Michael Forrester** — Principal Training Architect at KodeKloud.
30 years of infrastructure experience across federal, Fortune 50, and
startup environments. Has personally taught over 100,000 engineers
platform engineering and AI/ML infrastructure. Speaker at KubeCon EU
Cloud Native University and KubeAuto AI Day Europe.

Full bio: [**`abstract/bio.md`**](abstract/bio.md).
Contact: [michael@performantpro.com](mailto:michael@performantpro.com).

## License

Talk content — abstract, slides, speaker notes, and prose in this
repository — is licensed under [**CC BY 4.0**](LICENSE). Reuse with
attribution.

If you cite the talk: *Forrester, Michael. "The Day an AI Agent
Deleted My Cluster (And the Guardrails That Would Have Stopped It)."
SREday Austin Q2 2026, May 11, 2026.*
