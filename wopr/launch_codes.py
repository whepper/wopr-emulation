"""Launch code acquisition and the climactic 10th-code brute force."""

from __future__ import annotations

import random
import sys
import time
from typing import Callable

from .timing import Timing

# Ten launch codes. The 10th is the famous "CPE-1704-TKS" from the film.
KNOWN_CODES: list[str] = [
    "DPR-5938-AKL", "FGH-2847-PLM", "KJR-8372-QWE",
    "LMN-4729-RTY", "OPQ-6183-VBN", "RST-9264-XCV",
    "UVW-3715-ZXC", "YZA-5628-MNB", "BCD-7104-FGH",
    "CPE-1704-TKS",
]

Writer = Callable[[str], None]


def simulate_launch_codes(writer: Writer) -> int:
    """Print the 9-of-10 acquisition sequence.

    Returns the number of codes "found" (9).
    """
    writer("\nATTEMPTING TO ACQUIRE LAUNCH CODES...\n")
    time.sleep(Timing.LAUNCH_CODE_FINAL_SEARCH_PAUSE)
    for i, code in enumerate(KNOWN_CODES[:9], 1):
        writer(f"LAUNCH CODE {i}/10 ACQUIRED: {code}\n")
        time.sleep(Timing.LAUNCH_CODE_PAUSE)
    writer("\nWARNING: 9 OF 10 LAUNCH CODES ACQUIRED\n")
    writer("SEARCHING FOR FINAL LAUNCH CODE...\n\n")
    time.sleep(Timing.LAUNCH_CODE_FINAL_SEARCH_PAUSE)
    return 9


def reveal_final_launch_code(
    writer: Writer,
    target: str = KNOWN_CODES[-1],
    shuffle: bool = True,
) -> None:
    """Brute-force the final launch code digit by digit on a single line.

    Uses carriage-return to update the line in place. The digits are
    "tried" in a random order so the cinematic effect is unpredictable
    across runs.
    """
    writer("\nFINAL LAUNCH CODE BRUTE-FORCE IN PROGRESS...\n\n")
    time.sleep(Timing.LAUNCH_CODE_REVEAL_PAUSE)
    revealed = ["#"] * len(target)
    for i, ch in enumerate(target):
        if ch == "-":
            revealed[i] = "-"
    order = [i for i, ch in enumerate(target) if ch != "-"]
    if shuffle:
        random.shuffle(order)
    charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for idx in order:
        for guess in charset:
            revealed[idx] = guess
            sys.stdout.write("\r  " + "".join(revealed))
            sys.stdout.flush()
            time.sleep(Timing.LAUNCH_CODE_DIGIT_PAUSE)
            if guess == target[idx]:
                break
    sys.stdout.write("\r  " + target + "\n")
    sys.stdout.flush()
    writer("\n*** ALL 10 LAUNCH CODES ACQUIRED ***\n")
    time.sleep(Timing.LAUNCH_CODE_DONE_PAUSE)
