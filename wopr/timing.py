"""Named timing constants for the WOPR emulation.

All ``time.sleep`` durations in the program should reference one of these
named constants so pacing can be tuned in one place and the constants can
be monkey-patched in tests.
"""

from __future__ import annotations


class Timing:
    """Single source of truth for all pause durations in the emulation."""

    # ---- Teletype / dramatic pacing ---------------------------------------
    TELETYPE_CHAR: float = 0.012
    TELETYPE_SLOW: float = 0.04
    TELETYPE_FAST: float = 0.005

    # ---- Authentication / opening conversation ----------------------------
    LOGIN_PAUSE: float = 1.0
    CONVERSATION_PAUSE: float = 1.0
    LOCKOUT_PAUSE: float = 1.5

    # ---- DEFCON banners ----------------------------------------------------
    DEFCON_RING_PAUSE: float = 1.0

    # ---- Launch code acquisition ------------------------------------------
    LAUNCH_CODE_PAUSE: float = 0.5
    LAUNCH_CODE_FINAL_SEARCH_PAUSE: float = 2.0
    LAUNCH_CODE_REVEAL_PAUSE: float = 1.0
    LAUNCH_CODE_DIGIT_PAUSE: float = 0.01
    LAUNCH_CODE_DONE_PAUSE: float = 2.0

    # ---- Global Thermonuclear War -----------------------------------------
    STRIKE_LAUNCH_PAUSE: float = 2.0
    STRIKE_IMPACT_PAUSE: float = 2.0
    RETALIATION_DETECTED_PAUSE: float = 1.0
    CASUALTY_PROJECTION_PAUSE: float = 3.0
    NORAD_LINE_PAUSE: float = 0.4

    # ---- Chess ------------------------------------------------------------
    CHESS_AI_THINK_PAUSE: float = 0.5

    # ---- Tic-tac-toe ------------------------------------------------------
    TICTACTOE_HUMAN_TO_AI_PAUSE: float = 0.6
    TICTACTOE_AUTOPLAY_MOVE_PAUSE: float = 0.2
    TICTACTOE_AUTOPLAY_GAME_PAUSE: float = 0.3
    TICTACTOE_AUTOPLAY_LEAD_IN: float = 1.0

    # ---- Falken's Maze ----------------------------------------------------
    MAZE_MOVE_PAUSE: float = 0.4
    MAZE_GAME_OVER_PAUSE: float = 1.0

    # ---- Learning sequence -----------------------------------------------
    LEARNING_HEADER_PAUSE: float = 2.0
    LEARNING_SCENARIO_PAUSE: float = 0.3
    LEARNING_SCENARIO_DOT_PAUSE: float = 0.3
    LEARNING_AFTER_SCENARIOS_PAUSE: float = 1.0
    LEARNING_AFTER_TTT_PAUSE: float = 2.0
    LEARNING_COUNTDOWN_TICK: float = 1.0
    LEARNING_AFTER_PUNCHLINE_PAUSE: float = 2.0
