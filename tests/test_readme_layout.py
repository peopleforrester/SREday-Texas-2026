# ABOUTME: Asserts every directory listed in README "Repository Layout" exists on disk.
# ABOUTME: Forward-looking ('expected', 'planned') items belong in a separate Roadmap section.

from __future__ import annotations

import re
from pathlib import Path


# Several heading wordings are acceptable for the section that lists
# what is on disk. The test does not care about the wording — only
# that whatever section plays that role lists directories that exist.
_LAYOUT_HEADINGS = (
    "Repository Layout",
    "Repository contents",
    "What's in this repo",
    "What's in this repository",
)
_LAYOUT_HEADING = re.compile(
    r"^##\s+(?:" + "|".join(re.escape(h) for h in _LAYOUT_HEADINGS) + r")\s*$",
    re.MULTILINE,
)
_NEXT_HEADING = re.compile(r"^##\s+", re.MULTILINE)
# Match a list line that contains a backtick-wrapped path-with-slash.
# Allows arbitrary non-backtick prefix between the bullet and the
# backtick so markdown link / bold / emoji wrappers are tolerated:
#   - `abstract/` — caption
#   - **`abstract/`** — caption
#   - [**`abstract/`**](abstract/) — caption
_DIR_ENTRY = re.compile(r"^[-*]\s+[^`\n]*`([^`]+/)`")


def _extract_layout_section(readme: str) -> str:
    """Return the body of the layout H2 section, or '' if not present."""
    m = _LAYOUT_HEADING.search(readme)
    if not m:
        return ""
    start = m.end()
    next_h2 = _NEXT_HEADING.search(readme, start)
    end = next_h2.start() if next_h2 else len(readme)
    return readme[start:end]


def test_layout_dirs_exist_or_are_in_roadmap(repo_root: Path, readme: str) -> None:
    """Every directory listed in 'Repository Layout' must currently exist.

    Planned-but-not-yet-created dirs belong in a separate 'Roadmap' (or
    similarly-named) section so a first-time reader is not misled.
    """
    section = _extract_layout_section(readme)
    assert section, (
        "README is missing the layout section. Expected one of these "
        f"H2 headings: {_LAYOUT_HEADINGS}."
    )

    listed_dirs: list[str] = []
    for line in section.splitlines():
        match = _DIR_ENTRY.match(line.strip())
        if match:
            listed_dirs.append(match.group(1).rstrip("/"))

    missing: list[str] = []
    for d in listed_dirs:
        if not (repo_root / d).is_dir():
            missing.append(d)

    assert not missing, (
        "README 'Repository Layout' lists directories that do not exist on "
        f"disk: {missing}. Move them to a 'Roadmap' (or 'Planned') section."
    )
