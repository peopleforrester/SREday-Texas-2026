# ABOUTME: Asserts PROJECT_STATE.md reflects actual repository and remote state.
# ABOUTME: Catches the class of state-drift bug the senior review surfaced.

from __future__ import annotations


def test_project_state_owner_matches_remote(
    project_state: str, github_owner_repo: tuple[str, str]
) -> None:
    """The GitHub owner mentioned in PROJECT_STATE.md must match `git remote`.

    The senior review caught the owner drifted from `michaelrishiforrester`
    (a stale guess) to the real `peopleforrester`. This test prevents the
    same class of bug from recurring on any future state file edit.
    """
    owner, repo = github_owner_repo
    canonical = f"{owner}/{repo}"
    assert canonical in project_state, (
        f"PROJECT_STATE.md does not mention the canonical "
        f"owner/repo '{canonical}' from `git remote get-url origin`."
    )

    # No incorrect owner should remain anywhere in the file.
    wrong_owner = "michaelrishiforrester"
    assert wrong_owner not in project_state, (
        f"PROJECT_STATE.md still references the wrong owner "
        f"'{wrong_owner}'. The real owner is '{owner}'."
    )


def test_next_step_names_both_unknowns(project_state: str) -> None:
    """The 'Next step' section must call out both blocking inputs.

    The senior review noted the prior 'Next step' only mentioned the
    abstract/bio. Schedule details (date, timebox) are equally blocking
    for the README placeholders, so both must be named explicitly.
    """
    # Find the "## Next step" section and read until the next heading.
    lower = project_state.lower()
    marker = "## next step"
    start = lower.find(marker)
    assert start != -1, "PROJECT_STATE.md is missing a '## Next step' section."

    # Section runs to the next H2 (or EOF).
    rest = project_state[start + len(marker) :]
    next_h2 = rest.find("\n## ")
    section = rest if next_h2 == -1 else rest[:next_h2]
    section_lower = section.lower()

    assert "abstract" in section_lower, (
        "Next step section must reference the submitted abstract "
        "(blocking input #1 for talk content)."
    )
    schedule_terms = ("date", "timebox", "schedule")
    assert any(term in section_lower for term in schedule_terms), (
        "Next step section must reference event date / timebox / schedule "
        "(blocking input #2 for README placeholders). Looked for any of: "
        f"{schedule_terms}."
    )
