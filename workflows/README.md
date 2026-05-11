# Workflows — GitHub Actions backstop

`ci.yml` is the defense-in-depth that fires for anyone who pushes
without the local `pre-commit` / `pre-push` hooks from
`../hooks/git/` installed. Runs on push to staging/main and on PRs
to either.

Right now `ci.yml` runs the consistency test suite for this talk
repo (uv + pytest). For your own repo, adapt the test command at the
bottom of the file — drop in whatever runs the suite you care about.

### Install

```bash
mkdir -p /path/to/your-repo/.github/workflows
cp workflows/ci.yml /path/to/your-repo/.github/workflows/
```

Commit and push. The workflow fires on the next push or PR.

### What it does not cover

`ci.yml` is a **client-side-equivalent** check moved to the remote.
It does not replace branch protection, CODEOWNERS, admission
policies, or any other server-side enforcement on the target.
See [`../docs/the-framework.md`](../docs/the-framework.md) section 2
("Server side — Git, CI, systemd") for what a complete remote-side
posture looks like.

### Bypass

Admin merge override on branch protection. Code that passes the
linters but is wrong. UI-skipped checks. Same as any CI gate.
