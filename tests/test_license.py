# ABOUTME: Asserts the repo has a LICENSE file and the README references it.
# ABOUTME: Public talk repos without a license leave reuse rights ambiguous.

from __future__ import annotations

from pathlib import Path


def test_license_file_present(repo_root: Path) -> None:
    """A LICENSE file must exist at repo root.

    The repo is public; without a license, default copyright applies and
    reuse rights are murky. The senior review flagged this directly.
    """
    license_path = repo_root / "LICENSE"
    assert license_path.is_file(), (
        "LICENSE file missing at repo root. The repo is public, so reuse "
        "rights need to be explicit."
    )
    contents = license_path.read_text(encoding="utf-8")
    assert contents.strip(), "LICENSE file exists but is empty."


def test_readme_references_license(readme: str) -> None:
    """README must mention the license so readers know what applies."""
    lower = readme.lower()
    assert "license" in lower, (
        "README does not mention the license. Add a short License section."
    )
