"""Chess game for the WOPR system.

Simplified chess: full piece set and per-piece move validation
(including blocked-path detection and friendly-fire rejection) but no
castling, en passant, or pawn promotion. Game ends when a king is
captured (no check/checkmate detection).
"""

from __future__ import annotations

import random
import time
from typing import Optional

from .timing import Timing


class ChessGame:
    """Chess game implementation for the WOPR system."""

    def __init__(self) -> None:
        self.board: list[list[str]] = self._initialize_board()
        self.player_color: Optional[str] = None  # "WHITE" or "BLACK"
        self.game_over: bool = False
        self.awaiting_color_selection: bool = True

    def _initialize_board(self) -> list[list[str]]:
        return [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
        ]

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    @staticmethod
    def _parse_square(sq: str) -> Optional[tuple[int, int]]:
        """Convert algebraic square (e.g. ``"e2"``) to internal (row, col)."""
        if not sq or len(sq) != 2:
            return None
        file_ch, rank_ch = sq[0], sq[1]
        if not ("a" <= file_ch <= "h") or not rank_ch.isdigit():
            return None
        col = ord(file_ch) - ord("a")
        rank = int(rank_ch)
        if not (1 <= rank <= 8):
            return None
        return 8 - rank, col

    @staticmethod
    def _format_square(row: int, col: int) -> str:
        return f"{chr(col + ord('a'))}{8 - row}"

    # ------------------------------------------------------------------
    # Move validation
    # ------------------------------------------------------------------

    def _path_clear(self, fr: int, fc: int, tr: int, tc: int) -> bool:
        dr = 0 if tr == fr else (1 if tr > fr else -1)
        dc = 0 if tc == fc else (1 if tc > fc else -1)
        r, c = fr + dr, fc + dc
        while (r, c) != (tr, tc):
            if self.board[r][c] != " ":
                return False
            r += dr
            c += dc
        return True

    def _is_valid_move(self, fr: int, fc: int, tr: int, tc: int) -> bool:
        piece = self.board[fr][fc]
        if piece == " " or (fr, fc) == (tr, tc):
            return False
        target = self.board[tr][tc]
        if target != " " and piece.isupper() == target.isupper():
            return False
        kind = piece.upper()
        dr, dc = tr - fr, tc - fc
        adr, adc = abs(dr), abs(dc)

        if kind == "P":
            direction = -1 if piece.isupper() else 1
            start_row = 6 if piece.isupper() else 1
            if dc == 0 and target == " ":
                if dr == direction:
                    return True
                if fr == start_row and dr == 2 * direction and self.board[fr + direction][fc] == " ":
                    return True
                return False
            if adc == 1 and dr == direction and target != " ":
                return True
            return False

        if kind == "N":
            return (adr, adc) in ((1, 2), (2, 1))

        if kind == "B":
            return adr == adc and self._path_clear(fr, fc, tr, tc)

        if kind == "R":
            return (dr == 0 or dc == 0) and self._path_clear(fr, fc, tr, tc)

        if kind == "Q":
            if adr == adc or dr == 0 or dc == 0:
                return self._path_clear(fr, fc, tr, tc)
            return False

        if kind == "K":
            return adr <= 1 and adc <= 1

        return False

    def _legal_moves_for(self, white: bool) -> list[tuple[int, int, int, int]]:
        moves: list[tuple[int, int, int, int]] = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p == " " or p.isupper() != white:
                    continue
                for tr in range(8):
                    for tc in range(8):
                        if self._is_valid_move(r, c, tr, tc):
                            moves.append((r, c, tr, tc))
        return moves

    def _apply_move(self, fr: int, fc: int, tr: int, tc: int) -> None:
        piece = self.board[fr][fc]
        self.board[fr][fc] = " "
        self.board[tr][tc] = piece

    def _winner(self) -> Optional[str]:
        """Return ``"WHITE"`` / ``"BLACK"`` based on which king is missing."""
        kings = {"K": False, "k": False}
        for row in self.board:
            for sq in row:
                if sq in kings:
                    kings[sq] = True
        if not kings["K"]:
            return "BLACK"
        if not kings["k"]:
            return "WHITE"
        return None

    # ------------------------------------------------------------------
    # AI
    # ------------------------------------------------------------------

    def _make_ai_move(self) -> Optional[str]:
        wopr_white = self.player_color == "BLACK"
        moves = self._legal_moves_for(wopr_white)
        if not moves:
            return None
        captures = [m for m in moves if self.board[m[2]][m[3]] != " "]
        king_grabs = [m for m in captures if self.board[m[2]][m[3]].upper() == "K"]
        choice = random.choice(king_grabs or captures or moves)
        fr, fc, tr, tc = choice
        from_sq = self._format_square(fr, fc)
        to_sq = self._format_square(tr, tc)
        self._apply_move(fr, fc, tr, tc)
        return f"{from_sq} {to_sq}"

    # ------------------------------------------------------------------
    # Top-level dispatch
    # ------------------------------------------------------------------

    def play_turn(self, user_input: str) -> str:
        if self.awaiting_color_selection:
            color = user_input.strip().upper()
            if "WHITE" in color or color == "W":
                self.player_color = "WHITE"
                self.awaiting_color_selection = False
                return "\nA GAME OF CHESS IS A BATTLE OF LOGIC AND PATIENCE. NEITHER SIDE CAN AFFORD A MISCALCULATION.\n\nYOU ARE WHITE. YOUR MOVE: "
            if "BLACK" in color or color == "B":
                self.player_color = "BLACK"
                self.awaiting_color_selection = False
                wopr_move = self._make_ai_move()
                return f"\nA GAME OF CHESS IS A BATTLE OF LOGIC AND PATIENCE. NEITHER SIDE CAN AFFORD A MISCALCULATION.\n\nYOU ARE BLACK. MY OPENING MOVE: {wopr_move}\n\nYOUR MOVE: "
            return "\nPLEASE SELECT WHITE OR BLACK: "

        if self.game_over:
            return "\nGAME OVER."

        try:
            from_sq, to_sq = user_input.split()
        except ValueError:
            return "\nINVALID INPUT. USE FORMAT 'e2 e4': "

        fr_fc = self._parse_square(from_sq)
        tr_tc = self._parse_square(to_sq)
        if fr_fc is None or tr_tc is None:
            return "\nINVALID SQUARE. USE FORMAT 'e2 e4': "
        fr, fc = fr_fc
        tr, tc = tr_tc

        piece = self.board[fr][fc]
        player_white = self.player_color == "WHITE"
        if piece == " " or piece.isupper() != player_white:
            return "\nTHAT IS NOT YOUR PIECE. TRY AGAIN: "

        if not self._is_valid_move(fr, fc, tr, tc):
            return "\nINVALID MOVE. TRY AGAIN: "

        self._apply_move(fr, fc, tr, tc)
        winner = self._winner()
        if winner:
            self.game_over = True
            return (
                "\nCHECKMATE. YOU WIN."
                if winner == self.player_color
                else "\nCHECKMATE. I WIN."
            )

        time.sleep(Timing.CHESS_AI_THINK_PAUSE)
        wopr_move = self._make_ai_move()
        winner = self._winner()
        if winner:
            self.game_over = True
            tail = (
                "\nCHECKMATE. YOU WIN."
                if winner == self.player_color
                else "\nCHECKMATE. I WIN."
            )
            return f"\nMY MOVE: {wopr_move}{tail}"
        if wopr_move:
            return f"\nMY MOVE: {wopr_move}\n\nYOUR MOVE: "
        return "\nYOUR MOVE: "
