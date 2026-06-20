"""Output abstractions for the WOPR emulation.

Game modules accept a ``writer`` callable so output is funneled through a
single boundary. In production this is a thin wrapper that calls
``tprint``; in tests it can be a list-collecting stub.
"""

from __future__ import annotations

import os
import sys
import time
from typing import Callable, Optional

from .timing import Timing

FAST = os.environ.get("WOPR_FAST") == "1" or "--fast" in sys.argv

Writer = Callable[[str], None]


def tprint(text: str, end: str = "\n", delay: Optional[float] = None) -> None:
    """Print like a 1983 modem: one character at a time.

    Skipped when ``FAST`` mode is enabled or ``delay`` is explicitly 0.
    """
    if FAST or delay == 0:
        print(text, end=end, flush=True)
        return
    d = Timing.TELETYPE_CHAR if delay is None else delay
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        if ch != " ":
            time.sleep(d)
    if end:
        sys.stdout.write(end)
        sys.stdout.flush()


def bell() -> None:
    """Emit the terminal bell character (for DEFCON escalations)."""
    sys.stdout.write("\a")
    sys.stdout.flush()


def default_writer() -> Writer:
    """Return a writer that just prints without teletype delay."""
    return lambda text: print(text, end="", flush=True)
