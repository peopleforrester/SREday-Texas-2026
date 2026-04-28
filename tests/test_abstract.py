# ABOUTME: Asserts the as-submitted SREday abstract and bio are captured under abstract/.
# ABOUTME: Also enforces the README links to the canonical abstract file.

from __future__ import annotations

from pathlib import Path


# The full talk title as submitted to SREday. If the abstract diverges from
# this verbatim title, the test should catch it — talk metadata is the kind
# of thing that drifts when copied between repos.
SUBMITTED_TITLE = (
    "The Day an AI Agent Deleted My Cluster "
    "(And the Guardrails That Would Have Stopped It)"
)


def test_abstract_dir_exists(repo_root: Path) -> None:
    assert (repo_root / "abstract").is_dir(), (
        "abstract/ directory missing. Capture the as-submitted SREday "
        "abstract and bio there."
    )


def test_abstract_md_has_submitted_metadata(repo_root: Path) -> None:
    """abstract/abstract.md must contain the submitted title, format, duration, level."""
    path = repo_root / "abstract" / "abstract.md"
    assert path.is_file(), f"{path} missing."
    text = path.read_text(encoding="utf-8")

    assert SUBMITTED_TITLE in text, (
        f"abstract.md is missing the verbatim submitted title:\n  {SUBMITTED_TITLE!r}"
    )
    # The submission form fields are the durable record — keep them visible.
    for required in ("Talk", "30 minutes", "Intermediate", "Accepted"):
        assert required in text, (
            f"abstract.md is missing the submission field '{required}'."
        )


def test_bio_md_has_speaker(repo_root: Path) -> None:
    """abstract/bio.md must identify the speaker."""
    path = repo_root / "abstract" / "bio.md"
    assert path.is_file(), f"{path} missing."
    text = path.read_text(encoding="utf-8")
    assert "Michael" in text and "Forrester" in text, (
        "bio.md is missing the speaker name."
    )


def test_readme_links_to_abstract(readme: str) -> None:
    """The README must link to abstract/abstract.md.

    Once a real submitted abstract is captured, the README should defer to
    it as the canonical source rather than carrying its own paraphrase.
    """
    assert "abstract/abstract.md" in readme, (
        "README does not link to abstract/abstract.md. Replace the "
        "paraphrased Talk Summary with a short intro plus a link to the "
        "as-submitted text."
    )
