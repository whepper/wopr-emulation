"""FALKEN'S MAZE — WOPR's first game on the list, canonically offered to
Professor Falken in the film.

A simple 5x5 grid where the player and WOPR both try to reach the center
cell. WOPR uses Manhattan-distance heuristic and always moves first
(inside the bounds of the maze). The first to reach the center wins;
running out of moves without reaching it is a loss.
"""

from __future__ import annotations

import time
from typing import Optional

from .timing import Timing

SIZE: int = 5
CENTER: tuple[int, int] = (SIZE // 2, SIZE // 2)
MAX_TURNS: int = SIZE * SIZE  # 25 moves each is plenty

PLAYER: str = "P"
WOPR: str = "W"


class FalkenMaze:
    """Falken's Maze: race to the center."""

    def __init__(self, wopr) -> None:
        self.wopr = wopr
        self.board: list[list[str]] = self._init_board()
        self.player_pos: tuple[int, int] = (SIZE - 1, 0)  # bottom-left
        self.wopr_pos: tuple[int, int] = (0, SIZE - 1)    # top-right
        self.turn: str = PLAYER  # PLAYER moves first
        self.game_over: bool = False
        self.wopr_won: bool = False
        self.moves_taken: int = 0

    def _init_board(self) -> list[list[str]]:
        board = [["." for _ in range(SIZE)] for _ in range(SIZE)]
        board[SIZE - 1][0] = PLAYER
        board[0][SIZE - 1] = WOPR
        board[CENTER[0]][CENTER[1]] = "*"
        return board

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _render(self) -> str:
        rows = []
        rows.append("  " + " ".join(str(i) for i in range(SIZE)))
        rows.append(" +" + "-" * (SIZE * 2 - 1) + "+")
        for i, row in enumerate(self.board):
            rows.append(f"{i}|" + " ".join(row) + f"|{i}")
        rows.append(" +" + "-" * (SIZE * 2 - 1) + "+")
        rows.append("  " + " ".join(str(i) for i in range(SIZE)))
        return "\n" + "\n".join(rows) + "\n"

    @staticmethod
    def _manhattan(p: tuple[int, int], q: tuple[int, int]) -> int:
        return abs(p[0] - q[0]) + abs(p[1] - q[1])

    def _wopr_ai_move(self) -> tuple[int, int]:
        """WOPR moves one step toward the center using Manhattan heuristic.

        On ties, prefers a step that is also closer to the player (so WOPR
        plays aggressively and "catches" the player if they get in the
        way). This is intentionally simple but produces a competent
        opponent.
        """
        cr, cc = CENTER
        pr, pc = self.wopr_pos
        plr = self.player_pos
        best: Optional[tuple[int, tuple[int, int]]] = None
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = pr + dr, pc + dc
            if not (0 <= nr < SIZE and 0 <= nc < SIZE):
                continue
            if (nr, nc) == plr:
                continue  # can't share a square
            d_to_center = self._manhattan((nr, nc), CENTER)
            d_to_player = self._manhattan((nr, nc), plr)
            score = (d_to_center, d_to_player)
            if best is None or score < best[0]:
                best = (score, (nr, nc))
        if best is None:
            return self.wopr_pos
        return best[1]

    def _parse_dir(self, s: str) -> Optional[tuple[int, int]]:
        s = s.strip().upper()
        mapping = {
            "N": (-1, 0), "S": (1, 0), "E": (0, 1), "W": (0, -1),
            "U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1),
            "NORTH": (-1, 0), "SOUTH": (1, 0), "EAST": (0, 1), "WEST": (0, -1),
        }
        return mapping.get(s)

    def _apply_player_move(self, dr: int, dc: int) -> bool:
        pr, pc = self.player_pos
        nr, nc = pr + dr, pc + dc
        if not (0 <= nr < SIZE and 0 <= nc < SIZE):
            return False
        if (nr, nc) == self.wopr_pos:
            return False
        # Clear old position
        self.board[pr][pc] = "."
        self.player_pos = (nr, nc)
        if (nr, nc) != CENTER:
            self.board[nr][nc] = PLAYER
        return True

    def _apply_wopr_move(self) -> None:
        nr, nc = self._wopr_ai_move()
        pr, pc = self.wopr_pos
        self.board[pr][pc] = "."
        self.wopr_pos = (nr, nc)
        if (nr, nc) != CENTER:
            self.board[nr][nc] = WOPR

    def _is_center_reached(self) -> bool:
        return self.player_pos == CENTER or self.wopr_pos == CENTER

    def _winner(self) -> Optional[str]:
        if self.player_pos == CENTER:
            return "PLAYER"
        if self.wopr_pos == CENTER:
            return "WOPR"
        return None

    # ------------------------------------------------------------------
    # Main dispatch
    # ------------------------------------------------------------------

    def play_turn(self, user_input: str) -> str:
        if self.game_over:
            s = user_input.strip().upper()
            if s in ("YES", "Y", "1"):
                self._reset()
                return "\nFALKEN'S MAZE. FIND YOUR WAY OUT.\n" + self._render() + "\nYOUR MOVE (N/S/E/W): "
            self.wopr.end_current_game()
            return "\nRETURNING TO MAIN MENU.\n"

        if self.turn == PLAYER:
            d = self._parse_dir(user_input)
            if d is None:
                return (
                    self._render()
                    + "\nINVALID DIRECTION. USE N (NORTH), S (SOUTH), E (EAST), W (WEST): "
                )
            if not self._apply_player_move(*d):
                return self._render() + "\nYOU CAN'T MOVE THERE. TRY AGAIN: "
            self.moves_taken += 1
            if self._winner() == "PLAYER":
                self.game_over = True
                return (
                    self._render()
                    + "\nYOU FOUND YOUR WAY OUT.\n\nPLAY AGAIN? (YES/NO): "
                )
            if self.moves_taken >= MAX_TURNS:
                self.game_over = True
                return (
                    self._render()
                    + "\nTHE MAZE GOES ON FOREVER.\n\nPLAY AGAIN? (YES/NO): "
                )
            self.turn = WOPR

        # WOPR's turn
        time.sleep(Timing.MAZE_MOVE_PAUSE)
        self._apply_wopr_move()
        self.moves_taken += 1
        if self._winner() == "WOPR":
            self.game_over = True
            return (
                self._render()
                + "\nI FOUND MY WAY OUT FIRST.\n\nPLAY AGAIN? (YES/NO): "
            )
        if self.moves_taken >= MAX_TURNS:
            self.game_over = True
            return (
                self._render()
                + "\nTHE MAZE GOES ON FOREVER.\n\nPLAY AGAIN? (YES/NO): "
            )
        self.turn = PLAYER
        return self._render() + "\nYOUR MOVE (N/S/E/W): "

    def _reset(self) -> None:
        self.board = self._init_board()
        self.player_pos = (SIZE - 1, 0)
        self.wopr_pos = (0, SIZE - 1)
        self.turn = PLAYER
        self.game_over = False
        self.moves_taken = 0
