# ABOUTME: Asserts .gitignore covers the asset types this repo will inevitably hold.
# ABOUTME: Also verifies the PDF-export policy is documented in README.

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

# Patterns that must be ignored by `.gitignore`. Each entry pairs a sample
# path that would be created in normal operation with the rationale.
DECK_ASSET_SAMPLES: list[tuple[str, str]] = [
    ("_site/index.html", "static-site builds (e.g. reveal-md, marp)"),
    ("dist/index.html", "generic frontend build output"),
    ("build/foo.html", "generic build output"),
    (".reveal-md/cache.json", "reveal-md cache directory"),
    ("deck/~$slides.pptx", "PowerPoint lock file"),
    ("deck/~$slides.key", "Keynote lock file"),
    ("deck/slides.pptx~", "PowerPoint autosave"),
    ("deck/main.aux", "LaTeX auxiliary"),
    ("deck/main.log", "LaTeX log"),
    ("deck/main.toc", "LaTeX table of contents"),
    ("deck/main.nav", "Beamer nav"),
    ("deck/main.snm", "Beamer snm"),
    ("deck/main.out", "LaTeX hyperref out"),
    ("deck/main.synctex.gz", "LaTeX synctex"),
    ("rehearsal/dryrun.wav", "rehearsal recording"),
    ("rehearsal/dryrun.m4a", "rehearsal recording"),
    ("rehearsal/dryrun.aif", "rehearsal recording"),
    ("rehearsal/dryrun.aiff", "rehearsal recording"),
    ("deck/slides.pdf", "PDF export of the deck (derived artifact)"),
]


def _git_check_ignore(repo_root: Path, sample_path: str) -> bool:
    """Return True if `sample_path` is ignored by .gitignore.

    Uses `git check-ignore` against a *hypothetical* path — the file does
    not need to exist. Exit code 0 means ignored, 1 means not ignored.
    """
    result = subprocess.run(
        ["git", "-C", str(repo_root), "check-ignore", "--no-index", sample_path],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


@pytest.mark.parametrize(
    "sample,reason",
    DECK_ASSET_SAMPLES,
    ids=[s for s, _ in DECK_ASSET_SAMPLES],
)
def test_deck_asset_patterns_covered(repo_root: Path, sample: str, reason: str) -> None:
    """Each predictable deck/talk asset path must be ignored."""
    assert _git_check_ignore(repo_root, sample), (
        f".gitignore does not cover '{sample}' ({reason}). "
        "Add a pattern that catches it."
    )


def test_pdf_export_policy_documented(readme: str) -> None:
    """The README must document the PDF-export policy.

    The senior review flagged that the prior .gitignore was ambiguous
    about PDFs. The policy is: PDF exports are derived and ignored;
    deck source is committed. README must say so for future contributors.
    """
    lower = readme.lower()
    assert "asset policy" in lower or "pdf" in lower, (
        "README does not mention PDFs or an 'Asset policy' section. "
        "Document the PDF-export decision so it doesn't drift."
    )
    # The decision itself must be captured — look for the actual ruling.
    assert "derived" in lower or "ignored" in lower or "not committed" in lower, (
        "README mentions PDF but does not state the policy "
        "(derived / ignored / not committed)."
    )
