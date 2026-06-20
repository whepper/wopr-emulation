"""Tests for wopr.chess.ChessGame."""

from __future__ import annotations

import unittest
from unittest import mock

from wopr.chess import ChessGame


class TestChessGame(unittest.TestCase):
    def setUp(self) -> None:
        self.game = ChessGame()

    def test_initial_board_has_correct_pieces(self) -> None:
        self.assertEqual(self.game.board[0], ["r", "n", "b", "q", "k", "b", "n", "r"])
        self.assertEqual(self.game.board[1], ["p"] * 8)
        self.assertEqual(self.game.board[6], ["P"] * 8)
        self.assertEqual(self.game.board[7], ["R", "N", "B", "Q", "K", "B", "N", "R"])

    def test_white_selection(self) -> None:
        out = self.game.play_turn("white")
        self.assertIn("YOU ARE WHITE", out)
        self.assertEqual(self.game.player_color, "WHITE")

    def test_black_selection_triggers_ai_move(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            out = self.game.play_turn("black")
        self.assertIn("YOU ARE BLACK", out)
        self.assertEqual(self.game.player_color, "BLACK")
        self.assertIn("MY OPENING MOVE", out)

    def test_w_alias_for_white(self) -> None:
        self.game.play_turn("w")
        self.assertEqual(self.game.player_color, "WHITE")

    def test_invalid_color_reprompts(self) -> None:
        out = self.game.play_turn("purple")
        self.assertIn("PLEASE SELECT WHITE OR BLACK", out)
        self.assertTrue(self.game.awaiting_color_selection)

    def test_pawn_forward_one(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.assertTrue(self.game._is_valid_move(6, 4, 5, 4))  # e2 to e3

    def test_pawn_forward_two_from_start(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.assertTrue(self.game._is_valid_move(6, 4, 4, 4))  # e2 to e4

    def test_pawn_double_advance_blocked(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.game.board[5][4] = "P"  # block e3
        self.assertFalse(self.game._is_valid_move(6, 4, 4, 4))

    def test_pawn_cannot_move_backward(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.assertFalse(self.game._is_valid_move(6, 4, 7, 4))  # try e2 to e1

    def test_pawn_diagonal_capture(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.game.board[5][5] = "p"  # black pawn on f3
        self.assertTrue(self.game._is_valid_move(6, 4, 5, 5))  # e2 captures f3

    def test_pawn_cannot_move_diagonal_without_capture(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        # Diagonal to empty square is not a valid pawn move
        self.assertFalse(self.game._is_valid_move(6, 4, 5, 5))

    def test_knight_moves(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        # b1 to a3 (knight move)
        self.assertTrue(self.game._is_valid_move(7, 1, 5, 0))
        # b1 to c3 (knight move)
        self.assertTrue(self.game._is_valid_move(7, 1, 5, 2))

    def test_knight_cannot_move_like_king(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.assertFalse(self.game._is_valid_move(7, 1, 6, 1))  # straight ahead is not knight

    def test_bishop_diagonal(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        # Clear e2 and place bishop there
        self.game.board[6][4] = " "
        self.game.board[4][4] = "B"
        self.assertTrue(self.game._is_valid_move(4, 4, 2, 2))  # diagonal

    def test_bishop_blocked(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.game.board[6][4] = " "  # clear e2
        self.game.board[4][4] = "B"
        self.game.board[3][3] = "P"  # block
        self.assertFalse(self.game._is_valid_move(4, 4, 2, 2))

    def test_rook_horizontal(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.game.board[4][4] = "R"
        self.assertTrue(self.game._is_valid_move(4, 4, 4, 7))

    def test_rook_cannot_move_diagonal(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.game.board[4][4] = "R"
        self.assertFalse(self.game._is_valid_move(4, 4, 5, 5))

    def test_queen_combined_moves(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.game.board[3][3] = "Q"
        # Clear path for rook-like move (row 3, cols 4-7)
        for c in range(4, 8):
            self.game.board[3][c] = " "
        self.assertTrue(self.game._is_valid_move(3, 3, 3, 7))  # rook-like
        # Clear path for bishop-like move to (0, 0): (2, 2) and (1, 1) have pawns
        self.game.board[1][1] = " "
        self.game.board[2][2] = " "
        self.assertTrue(self.game._is_valid_move(3, 3, 0, 0))  # bishop-like
        # A move that's neither rook nor bishop pattern
        self.assertFalse(self.game._is_valid_move(3, 3, 4, 5))  # not a queen move

    def test_king_one_square(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        self.game.board[4][4] = "K"
        self.assertTrue(self.game._is_valid_move(4, 4, 5, 4))
        self.assertFalse(self.game._is_valid_move(4, 4, 6, 4))  # two squares

    def test_cannot_capture_own_piece(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        # White bishop at c1 trying to take white queen at d1 (rook-style?)
        # Actually, try white knight at b1 taking white pawn at b2
        self.assertFalse(self.game._is_valid_move(7, 1, 6, 1))

    def test_invalid_input_format(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        out = self.game.play_turn("garbage")
        self.assertIn("INVALID INPUT", out)

    def test_off_board_square(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        out = self.game.play_turn("z9 e4")
        self.assertIn("INVALID SQUARE", out)

    def test_not_your_piece(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        out = self.game.play_turn("a7 a6")  # black pawn
        self.assertIn("NOT YOUR PIECE", out)

    def test_king_capture_ends_game(self) -> None:
        self.game.player_color = "WHITE"
        self.game.awaiting_color_selection = False
        # Place white queen at e6 (row 2, col 4) next to black king at e8 (row 0, col 4)
        self.game.board[0] = [" ", " ", " ", " ", "k", " ", " ", " "]
        self.game.board[1] = [" ", " ", " ", " ", " ", " ", " ", " "]
        self.game.board[2] = [" ", " ", " ", " ", "Q", " ", " ", " "]
        out = self.game.play_turn("e6 e8")
        self.assertIn("CHECKMATE. YOU WIN", out)
        self.assertTrue(self.game.game_over)

    def test_legal_moves_count(self) -> None:
        moves = self.game._legal_moves_for(True)
        # White has 16 pawns + 4 knights (b1, g1 can move) + others depending on blocks
        # Just check it returns a reasonable number
        self.assertGreater(len(moves), 0)
        self.assertLess(len(moves), 100)

    def test_ai_move_returns_algebraic(self) -> None:
        self.game.player_color = "WHITE"
        with mock.patch("time.sleep", lambda *a, **kw: None):
            out = self.game.play_turn("black")
        # The first AI move should be in algebraic format "e2 e4" style
        self.assertIn("MY OPENING MOVE:", out)
        # Extract the move and verify it's a valid algebraic pair
        import re
        match = re.search(r"MY OPENING MOVE: (\w\d) (\w\d)", out)
        self.assertIsNotNone(match)
        from_sq, to_sq = match.group(1), match.group(2)
        self.assertEqual(len(from_sq), 2)
        self.assertEqual(len(to_sq), 2)
        # Verify the board actually changed
        rank_6_changed = any(
            self.game.board[6][c] != "P" for c in range(8)
        )
        rank_7_changed = any(
            self.game.board[7][c] != starting
            for c, starting in enumerate(["R", "N", "B", "Q", "K", "B", "N", "R"])
        )
        self.assertTrue(rank_6_changed or rank_7_changed)
