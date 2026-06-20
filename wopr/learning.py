"""Learning sequence — the cinematic climax of the WOPR experience."""

from __future__ import annotations

import time
from typing import Callable

from .timing import Timing

Writer = Callable[[str], None]

SCENARIOS: list[str] = [
    "U.S. FIRST STRIKE",
    "SOVIET FIRST STRIKE",
    "NATO CONFLICT ESCALATION",
    "MIDDLE EAST ESCALATION",
    "CHINA-SOVIET CONFRONTATION",
    "ACCIDENTAL LAUNCH",
]

COUNTDOWN_TICKS: int = 5


def run_learning_sequence(wopr, writer: Writer) -> None:
    """Run the WOPR learning sequence: scenarios, tic-tac-toe, countdown,
    and the famous punchline.
    """
    writer("\n" + "=" * 50 + "\n")
    writer("INITIATING LEARNING SEQUENCE...\n")
    writer("=" * 50 + "\n\n")
    time.sleep(Timing.LEARNING_HEADER_PAUSE)

    writer("ANALYZING GLOBAL THERMONUCLEAR WAR SCENARIOS...\n\n")
    time.sleep(Timing.LEARNING_AFTER_SCENARIOS_PAUSE)

    for scenario in SCENARIOS:
        writer(f"SIMULATING: {scenario}")
        for _ in range(3):
            writer(".")
            time.sleep(Timing.LEARNING_SCENARIO_DOT_PAUSE)
        writer(" PROJECTED OUTCOME: TOTAL ANNIHILATION\n")
        time.sleep(Timing.LEARNING_SCENARIO_PAUSE)

    # Mid-loop existential question — the film's most chilling line.
    for ch in "\nIS THIS A GAME OR IS IT REAL?\n":
        writer(ch)
        time.sleep(Timing.TELETYPE_SLOW / 4)
    time.sleep(Timing.LEARNING_AFTER_SCENARIOS_PAUSE)

    writer("\nRUNNING TIC-TAC-TOE LEARNING MODULE...\n\n")
    time.sleep(Timing.LEARNING_AFTER_SCENARIOS_PAUSE)

    # Use the WOPR's existing TicTacToe instance, or create a transient one
    # for the autoplay portion. We use a transient one to avoid clobbering
    # state.
    from .tictactoe import TicTacToe
    ttt = TicTacToe(wopr)
    ttt._autoplay(writer, games=10, delay=Timing.TICTACTOE_AUTOPLAY_MOVE_PAUSE / 2)

    writer("\nANALYSIS COMPLETE.\n")
    time.sleep(Timing.LEARNING_AFTER_TTT_PAUSE)

    # The countdown: "5... 4... 3... 2... 1..."
    for n in range(COUNTDOWN_TICKS, 0, -1):
        writer(f"{n}...")
        time.sleep(Timing.LEARNING_COUNTDOWN_TICK)

    writer("\n" + "=" * 50 + "\n")
    # Use per-character output for cinematic pacing.
    for ch in wopr.movie_quotes["learning_complete"]:
        writer(ch)
        time.sleep(Timing.TELETYPE_SLOW / 4)
    writer("\n")
    writer("=" * 50 + "\n\n")
    time.sleep(Timing.LEARNING_AFTER_PUNCHLINE_PAUSE)

    wopr.learning_mode = True
