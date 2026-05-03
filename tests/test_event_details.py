# ABOUTME: Asserts README "Event Details" reflects the verified SREday Austin Q2 2026 schedule.
# ABOUTME: Source of truth: https://sreday.com/2026-austin-q2/ (verified 2026-04-28).

from __future__ import annotations

import re


# Verified facts pulled from the official event page on 2026-04-28.
# If the schedule moves, update this list and the README together.
VERIFIED_FACTS: list[tuple[str, str]] = [
    ("date", "May 11, 2026"),
    ("venue", "The Sunset Room"),
    ("address", "310 E 3rd St"),
    ("city/state/zip", "Austin, TX 78701"),
    ("timebox", "30 minutes"),
    ("format", "single track"),
    ("session time", "12:30"),
]


def test_readme_has_verified_event_details(readme: str) -> None:
    """Every verified fact must appear somewhere in the README.

    The check is case-insensitive on the fact strings to allow stylistic
    flexibility (e.g. 'Single track' vs 'single track').
    """
    lower = readme.lower()
    missing: list[str] = []
    for label, fact in VERIFIED_FACTS:
        if fact.lower() not in lower:
            missing.append(f"{label}={fact!r}")
    assert not missing, (
        "README is missing verified event facts: "
        + ", ".join(missing)
        + ". Source: https://sreday.com/2026-austin-q2/"
    )


def test_readme_does_not_advertise_tbd_event_details(readme: str) -> None:
    """No TBD marker on the date/timebox/room line — the schedule is known."""
    pattern = re.compile(r"date,?\s*timebox,?\s*and\s*room.*tbd", re.IGNORECASE | re.DOTALL)
    assert not pattern.search(readme), (
        "README still says 'Date, timebox, and room: TBD'. The SREday "
        "Austin Q2 2026 schedule is verified — fill it in."
    )
