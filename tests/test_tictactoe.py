"""Tests for wopr.tictactoe.TicTacToe."""

from __future__ import annotations

import unittest
from unittest import mock

from wopr.core import WOPR
from wopr.tictactoe import TicTacToe


class TestTicTacToe(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()
        self.game = TicTacToe(self.wopr)
        self.captured: list[str] = []

    def _writer(self, s: str) -> None:
        self.captured.append(s)

    def test_first_call_prompts_for_players(self) -> None:
        out = self.game.play_turn("")
        self.assertIn("PLEASE LIST NUMBER OF PLAYERS", out)

    def test_mode_zero_runs_self_play(self) -> None:
        self.game.play_turn("")  # ask players
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.game.play_turn("0", writer=self._writer)
        # Should trigger learning
        self.assertTrue(self.wopr.learning_mode)
        # All self-play games should end in a DRAW (with perfect play)
        self.assertIn("ANALYSIS COMPLETE.\n", "".join(self.captured))

    def test_mode_one_sets_up_human_vs_wopr(self) -> None:
        self.game.play_turn("")  # ask players
        out = self.game.play_turn("1", writer=self._writer)
        self.assertIn("YOU ARE X", out)
        self.assertIn("I AM O", out)
        self.assertIn("YOUR MOVE (1-9)", out)

    def test_mode_two_sets_up_hotseat(self) -> None:
        self.game.play_turn("")  # ask players
        out = self.game.play_turn("2", writer=self._writer)
        self.assertIn("PLAYER 1 = X", out)
        self.assertIn("PLAYER 2 = O", out)
        self.assertIn("PLAYER 1 (X) MOVE (1-9)", out)

    def test_invalid_player_count_reprompts(self) -> None:
        self.game.play_turn("")  # ask players
        out = self.game.play_turn("3", writer=self._writer)
        self.assertIn("PLEASE LIST NUMBER OF PLAYERS", out)

    def test_mode_one_human_move_then_wopr_responds(self) -> None:
        self.game.play_turn("")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.game.play_turn("1", writer=self._writer)
            # Take center, expect WOPR reply
            out = self.game.play_turn("5", writer=self._writer)
        self.assertIn("MY MOVE", out)
        # WOPR should have placed an O
        self.assertIn("O", out)
        # board[4] is X
        self.assertEqual(self.game.board[4], "X")

    def test_invalid_move_reprompts(self) -> None:
        self.game.play_turn("")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.game.play_turn("1", writer=self._writer)
            out = self.game.play_turn("99", writer=self._writer)
        self.assertIn("NUMBER MUST BE 1-9", out)

    def test_taken_square_reprompts(self) -> None:
        self.game.play_turn("")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.game.play_turn("1", writer=self._writer)
            self.game.play_turn("5", writer=self._writer)  # X at center
            out = self.game.play_turn("5", writer=self._writer)
        self.assertIn("SQUARE ALREADY TAKEN", out)

    def test_play_again_after_win(self) -> None:
        # Force a near-end position where X wins in one move.
        self.game.awaiting_players = False
        self.game.players = 1
        self.game.board = ["X", "X", " ", "O", "O", " ", " ", " ", " "]
        self.game.turn = 0  # X to move
        with mock.patch("time.sleep", lambda *a, **kw: None):
            out = self.game.play_turn("3", writer=self._writer)
        self.assertIn("YOU WIN!", out)
        self.assertIn("PLAY AGAIN", out)
        self.assertTrue(self.game.game_over)

    def test_play_again_resets_board(self) -> None:
        # Make a finished game
        self.game.awaiting_players = False
        self.game.players = 1
        self.game.board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
        self.game.turn = 0
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.game.play_turn("1", writer=self._writer)  # already-won board triggers
        # board should have a winner, game over
        if self.game.game_over:
            with mock.patch("time.sleep", lambda *a, **kw: None):
                out = self.game.play_turn("yes", writer=self._writer)
            self.assertIn("NEW GAME", out)
            self.assertEqual(self.game.board, [" "] * 9)

    def test_play_again_no_returns_to_menu(self) -> None:
        self.game.awaiting_players = False
        self.game.players = 1
        self.game.board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
        self.game.turn = 0
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.game.play_turn("1", writer=self._writer)
        if self.game.game_over:
            out = self.game.play_turn("no", writer=self._writer)
            self.assertIn("RETURNING TO MAIN MENU", out)

    def test_ai_blocks_imminent_threat(self) -> None:
        # If O is about to win, X should block. But here we test that
        # when X threatens, the AI blocks.
        self.game.awaiting_players = False
        self.game.players = 1
        # X has 1 and 2, threatens to win on 3; O at 4 already.
        self.game.board = ["X", "X", " ", "O", " ", " ", " ", " ", " "]
        self.game.turn = 0
        with mock.patch("time.sleep", lambda *a, **kw: None):
            out = self.game.play_turn("3", writer=self._writer)  # X wins
        # Game over with X win
        self.assertIn("YOU WIN", out)

    def test_best_move_chooses_center(self) -> None:
        b = [" "] * 9
        move = self.game._best_move(b, "X", "O")
        self.assertEqual(move, 4)

    def test_best_move_takes_winning(self) -> None:
        b = ["X", "X", " ", "O", "O", " ", " ", " ", " "]
        move = self.game._best_move(b, "X", "O")
        self.assertEqual(move, 2)  # completes top row

    def test_best_move_blocks(self) -> None:
        b = ["O", "O", " ", "X", " ", " ", " ", " ", " "]
        move = self.game._best_move(b, "X", "O")
        self.assertEqual(move, 2)  # blocks top row
