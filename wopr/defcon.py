"""DEFCON rendering and state management."""

from __future__ import annotations

import sys
from enum import IntEnum

from .io import bell
from .timing import Timing


class DefconLevel(IntEnum):
    """U.S. military DEFCON readiness levels. 5 is peacetime, 1 is max."""

    MAXIMUM = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    NORMAL = 5


DEFCON_DESCRIPTIONS: dict[int, str] = {
    5: "NORMAL PEACETIME READINESS",
    4: "INCREASED INTELLIGENCE WATCH",
    3: "INCREASE IN FORCE READINESS",
    2: "FURTHER INCREASE IN FORCE READINESS",
    1: "MAXIMUM READINESS \u2014 NUCLEAR WAR IMMINENT",
}

# Total characters between (and including) the two '+' border characters.
# All content rows must be exactly this wide.
BANNER_WIDTH: int = 54


def _row(content: str) -> str:
    """Build a single bordered row from its interior text."""
    assert len(content) == BANNER_WIDTH - 2, (
        f"row content must be {BANNER_WIDTH - 2} chars, got {len(content)}"
    )
    return f"|{content}|"


def render_banner(level: int) -> str:
    """Return a string containing a DEFCON banner for the given level."""
    if level not in DEFCON_DESCRIPTIONS:
        raise ValueError(f"DEFCON level must be 1-5, got {level!r}")
    bar = "#" * (6 - level) + "." * (level - 1)
    desc = DEFCON_DESCRIPTIONS[level]
    interior = BANNER_WIDTH - 2

    border = "+" + "-" * interior + "+"
    head = _row(f"D E F C O N  {level}".center(interior))
    bar_row = _row(f"  [{bar:<5}]" + " " * (interior - 9))
    desc_row = _row(f"  {desc:<{interior - 4}}  ")

    return (
        f"\n{border}\n"
        f"{head}\n"
        f"{bar_row}\n"
        f"{desc_row}\n"
        f"{border}\n"
    )


def ring_bell() -> None:
    """Emit the terminal bell (used when DEFCON changes)."""
    bell()


def emit_dead_level(level: int) -> None:
    """Visually announce a DEFCON change with bell + banner."""
    bell()
    banner = render_banner(level)
    sys.stdout.write(banner)
    sys.stdout.flush()
    import time
    time.sleep(Timing.DEFCON_RING_PAUSE)
