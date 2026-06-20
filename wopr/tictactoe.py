"""Tic-tac-toe with WOPR — three modes: 0-player self-play, 1-player vs
WOPR, 2-player hotseat.
"""

from __future__ import annotations

import time
from typing import Callable, Optional

from .timing import Timing

Writer = Callable[[str], None]


class TicTacToe:
    """Tic-tac-toe implementation.

    Modes:
      0 players  - WOPR self-play, ends in draws, triggers learning sequence
      1 player   - Human (X) vs WOPR (O); WOPR plays optimally
      2 players  - Human X vs Human O, alternating turns
    """

    def __init__(self, wopr) -> None:
        self.wopr = wopr
        self.awaiting_players: bool = True
        self.players: Optional[int] = None
        self.board: list[str] = [" "] * 9
        self.turn: int = 0
        self.game_over: bool = False

    # ------------------------------------------------------------------
    # Board helpers
    # ------------------------------------------------------------------

    def _render(self, b: Optional[list[str]] = None) -> str:
        b = b if b is not None else self.board

        def cell(i: int) -> str:
            return b[i] if b[i] != " " else str(i + 1)

        return (
            f"\n {cell(0)} | {cell(1)} | {cell(2)}\n"
            f"---+---+---\n"
            f" {cell(3)} | {cell(4)} | {cell(5)}\n"
            f"---+---+---\n"
            f" {cell(6)} | {cell(7)} | {cell(8)}\n"
        )

    def _winner(self, b: Optional[list[str]] = None) -> Optional[str]:
        b = b if b is not None else self.board
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        for i, j, k in lines:
            if b[i] != " " and b[i] == b[j] == b[k]:
                return b[i]
        return None

    def _is_full(self, b: Optional[list[str]] = None) -> bool:
        b = b if b is not None else self.board
        return " " not in b

    def _best_move(self, b: list[str], me: str, opp: str) -> Optional[int]:
        """Minimax-lite: win, block, center, corner, side."""
        for idx in range(9):
            if b[idx] == " ":
                b[idx] = me
                if self._winner(b) == me:
                    b[idx] = " "
                    return idx
                b[idx] = " "
        for idx in range(9):
            if b[idx] == " ":
                b[idx] = opp
                if self._winner(b) == opp:
                    b[idx] = " "
                    return idx
                b[idx] = " "
        if b[4] == " ":
            return 4
        for idx in (0, 2, 6, 8):
            if b[idx] == " ":
                return idx
        for idx in (1, 3, 5, 7):
            if b[idx] == " ":
                return idx
        return None

    # ------------------------------------------------------------------
    # 0-player autoplay
    # ------------------------------------------------------------------

    def _play_one_game(
        self,
        b: list[str],
        writer: Writer,
        delay: float = Timing.TICTACTOE_AUTOPLAY_MOVE_PAUSE,
    ) -> Optional[str]:
        """Play a single 0-player game on a fresh board; returns winner or None."""
        symbols = ["X", "O"]
        turn = 0
        while True:
            me = symbols[turn % 2]
            opp = symbols[(turn + 1) % 2]
            mv = self._best_move(b, me, opp)
            if mv is None:
                break
            b[mv] = me
            writer(self._render(b))
            time.sleep(delay)
            w = self._winner(b)
            if w:
                return w
            if " " not in b:
                break
            turn += 1
        return None

    def _autoplay(
        self,
        writer: Writer,
        games: int = 12,
        delay: float = Timing.TICTACTOE_AUTOPLAY_MOVE_PAUSE,
    ) -> None:
        """Run ``games`` self-play games; all end in draws with perfect play."""
        writer("\nINITIATING TIC-TAC-TOE SELF-PLAY...\n")
        time.sleep(Timing.TICTACTOE_AUTOPLAY_LEAD_IN)
        for g in range(1, games + 1):
            writer(f"GAME {g}:\n")
            b = [" "] * 9
            winner = self._play_one_game(b, writer, delay=delay)
            if winner:
                writer(f"  WINNER: {winner}\n")
            else:
                writer("  DRAW\n")
            time.sleep(Timing.TICTACTOE_AUTOPLAY_GAME_PAUSE)

    # ------------------------------------------------------------------
    # Human-game helpers
    # ------------------------------------------------------------------

    def _current_symbol(self) -> str:
        return "X" if self.turn % 2 == 0 else "O"

    def _prompt_move(self) -> str:
        sym = self._current_symbol()
        if self.players == 1:
            label = "YOUR" if sym == "X" else "MY"
        else:
            label = f"PLAYER {1 if sym == 'X' else 2} ({sym})"
        return f"{label} MOVE (1-9): "

    def _apply_move(self, cell_str: str) -> Optional[str]:
        """Validate and apply a human move. Returns error string or None."""
        try:
            idx = int(cell_str.strip()) - 1
        except ValueError:
            return "INVALID INPUT. ENTER A NUMBER 1-9: "
        if not 0 <= idx <= 8:
            return "NUMBER MUST BE 1-9: "
        if self.board[idx] != " ":
            return "SQUARE ALREADY TAKEN. CHOOSE ANOTHER: "
        self.board[idx] = self._current_symbol()
        return None

    def _reset(self) -> None:
        self.board = [" "] * 9
        self.turn = 0
        self.game_over = False

    # ------------------------------------------------------------------
    # Step handlers (decomposed)
    # ------------------------------------------------------------------

    def _ask_player_count(self) -> str:
        """First call: prompt for player count."""
        self.awaiting_players = False
        return (
            "\nTIC-TAC-TOE\n"
            + self._render([" "] * 9)
            + "\n  1  2  3\n  4  5  6\n  7  8  9\n\n"
            "ONE OR TWO PLAYERS? (0 = WOPR SELF-PLAY)\n"
            "PLEASE LIST NUMBER OF PLAYERS: "
        )

    def _receive_player_count(self, user_input: str, writer: Writer) -> Optional[str]:
        """Second call: parse the count, dispatch into the chosen mode."""
        s = user_input.strip()
        if s not in ("0", "1", "2"):
            return "\nPLEASE LIST NUMBER OF PLAYERS (0, 1, OR 2): "
        self.players = int(s)

        if self.players == 0:
            self._autoplay(writer)
            writer("\nANALYSIS COMPLETE.\n")
            time.sleep(1)
            self.wopr.run_learning_sequence()
            self.wopr.end_current_game()
            return ""

        if self.players == 1:
            return (
                "\nYOU ARE X. I AM O.\n"
                + self._render()
                + "\n" + self._prompt_move()
            )
        return (
            "\nPLAYER 1 = X  |  PLAYER 2 = O\n"
            + self._render()
            + "\n" + self._prompt_move()
        )

    def _handle_game_over(self, user_input: str) -> str:
        """Return ``PLAY AGAIN?`` prompt or exit to main menu."""
        s = user_input.strip().upper()
        if "YES" in s or s in ("Y", "1"):
            self._reset()
            return "\nNEW GAME.\n" + self._render() + "\n" + self._prompt_move()
        self.wopr.end_current_game()
        return "\nRETURNING TO MAIN MENU.\n"

    def _apply_human_move(self, user_input: str) -> Optional[str]:
        """Validate input, place piece, advance turn. Returns response or None."""
        err = self._apply_move(user_input)
        if err:
            return "\n" + err
        self.turn += 1
        winner = self._winner()
        if winner:
            self.game_over = True
            if self.players == 1:
                result = "YOU WIN!" if winner == "X" else "I WIN."
            else:
                player_no = 1 if winner == "X" else 2
                result = f"PLAYER {player_no} ({winner}) WINS!"
            return self._render() + f"\n{result}\n\nPLAY AGAIN? (YES/NO): "
        if self._is_full():
            self.game_over = True
            return self._render() + "\nDRAW.\n\nPLAY AGAIN? (YES/NO): "
        return None

    def _wopr_responds(self) -> str:
        """In 1-player mode, compute WOPR's move and return formatted reply."""
        time.sleep(Timing.TICTACTOE_HUMAN_TO_AI_PAUSE)
        mv = self._best_move(self.board, "O", "X")
        if mv is None:
            return self._render() + "\n" + self._prompt_move()
        self.board[mv] = "O"
        self.turn += 1
        winner = self._winner()
        wopr_cell = mv + 1
        if winner:
            self.game_over = True
            return (
                self._render()
                + f"\nMY MOVE: {wopr_cell}\nI WIN.\n\nPLAY AGAIN? (YES/NO): "
            )
        if self._is_full():
            self.game_over = True
            return (
                self._render()
                + f"\nMY MOVE: {wopr_cell}\nDRAW.\n\nPLAY AGAIN? (YES/NO): "
            )
        return self._render() + f"\nMY MOVE: {wopr_cell}\n\n" + self._prompt_move()

    # ------------------------------------------------------------------
    # Main dispatch
    # ------------------------------------------------------------------

    def play_turn(self, user_input: str, writer: Optional[Writer] = None) -> str:
        """Called by the WOPR engine for each user input."""
        if writer is None:
            writer = lambda s: print(s, end="", flush=True)

        if self.awaiting_players:
            return self._ask_player_count()

        if self.players is None:
            return self._receive_player_count(user_input, writer)

        if self.game_over:
            return self._handle_game_over(user_input)

        result = self._apply_human_move(user_input)
        if result is not None:
            return result

        if self.players == 1:
            return self._wopr_responds()

        return self._render() + "\n" + self._prompt_move()
