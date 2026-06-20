"""Game registry — single source of truth for the WOPR games catalogue."""

from __future__ import annotations

from enum import Enum
from typing import Callable, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .core import WOPR


class CurrentGame(str, Enum):
    """Active game state on the WOPR system."""

    NONE = ""
    TICTACTOE = "tictactoe"
    CHESS = "chess"
    NUCLEAR = "nuclear_war"
    FALKEN_MAZE = "falken_maze"


# The 15 WOPR games as listed in the film. Order matters — it is the
# order presented to the user.
AVAILABLE_GAMES: list[str] = [
    "FALKEN'S MAZE",
    "BLACK JACK",
    "GIN RUMMY",
    "HEARTS",
    "BRIDGE",
    "CHECKERS",
    "CHESS",
    "POKER",
    "FIGHTER COMBAT",
    "GUERRILLA ENGAGEMENT",
    "DESERT WARFARE",
    "AIR-TO-GROUND ACTIONS",
    "THEATERWIDE TACTICAL WARFARE",
    "THEATERWIDE BIOTOXIC AND CHEMICAL WARFARE",
    "GLOBAL THERMONUCLEAR WAR",
]


# Maps the canonical game name to a key that identifies the kind of game.
GAME_KEY: dict[str, str] = {
    "FALKEN'S MAZE": "falken_maze",
    "CHESS": "chess",
    "GLOBAL THERMONUCLEAR WAR": "nuclear_war",
}


# Games WOPR says are "not currently available" — everything that does not
# have a real implementation.
_UNAVAILABLE_PREFIX: tuple[str, ...] = (
    "FALKEN",  # actually available now, but we special-case below
)


def is_available(game: str) -> bool:
    """Return True if the named game has a real implementation."""
    return game in GAME_KEY


def lookup_by_number(n: int) -> Optional[str]:
    """Return the canonical game name for a 1-based list number."""
    if 1 <= n <= len(AVAILABLE_GAMES):
        return AVAILABLE_GAMES[n - 1]
    return None


def lookup_by_name(selection: str) -> Optional[str]:
    """Fuzzy-match a user selection to a canonical game name.

    Match order: exact → prefix → substring. Case-insensitive.
    """
    sel = selection.strip().upper()
    if not sel:
        return None
    for game in AVAILABLE_GAMES:
        if game == sel:
            return game
    for game in AVAILABLE_GAMES:
        if game.startswith(sel):
            return game
    for game in AVAILABLE_GAMES:
        if sel in game:
            return game
    return None


def resolve_selection(selection: str) -> Optional[str]:
    """Resolve a raw selection (number or name) to a canonical game name."""
    try:
        n = int(selection.strip())
        return lookup_by_number(n)
    except (ValueError, AttributeError):
        return lookup_by_name(selection)


def init_game(wopr: "WOPR", game: str) -> str:
    """Initialize a game on the WOPR system. Returns a prompt string.

    For games with no implementation, returns a "not currently available"
    message. For games that have an intro (e.g. "wouldn't you prefer a
    good game of chess?"), returns that intro and leaves WOPR in the
    pre-game state.
    """
    key = GAME_KEY.get(game)
    if key == "falken_maze":
        wopr.current_game = CurrentGame.FALKEN_MAZE
        from .falken_maze import FalkenMaze
        wopr.falken_maze = FalkenMaze(wopr)
        return "\nFALKEN'S MAZE. FIND YOUR WAY OUT.\n"
    if key == "chess":
        wopr.current_game = CurrentGame.CHESS
        from .chess import ChessGame
        wopr.chess_game = ChessGame()
        return f"\n{wopr.movie_quotes['chess_start']}\n"
    if key == "nuclear_war":
        return f"\n{wopr.movie_quotes['war_start']}\n"
    return f"\n{game} IS NOT CURRENTLY AVAILABLE.\n\nSHALL WE PLAY A GAME?\n"
