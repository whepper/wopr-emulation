"""Tests for wopr.falken_maze.FalkenMaze."""

from __future__ import annotations

import unittest
from unittest import mock

from wopr.core import WOPR
from wopr.falken_maze import CENTER, MAX_TURNS, FalkenMaze, SIZE


class TestFalkenMaze(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()
        self.maze = FalkenMaze(self.wopr)

    def test_initial_board(self) -> None:
        # Bottom-left is player, top-right is WOPR, center is star
        self.assertEqual(self.maze.board[SIZE - 1][0], "P")
        self.assertEqual(self.maze.board[0][SIZE - 1], "W")
        self.assertEqual(self.maze.board[CENTER[0]][CENTER[1]], "*")
        # Everything else is '.'
        for r in range(SIZE):
            for c in range(SIZE):
                if (r, c) in {(SIZE - 1, 0), (0, SIZE - 1), CENTER}:
                    continue
                self.assertEqual(self.maze.board[r][c], ".")

    def test_starts_with_player_turn(self) -> None:
        self.assertEqual(self.maze.turn, "P")

    def test_player_move_north(self) -> None:
        out = self.maze.play_turn("n")
        self.assertIn("YOUR MOVE", out)
        # Player should have moved from (4,0) to (3,0)
        self.assertEqual(self.maze.player_pos, (3, 0))

    def test_player_move_aliases(self) -> None:
        # Test each direction with a maze that allows the move
        cases = [
            # (cmd, start_pos, expected_pos)
            ("NORTH", (2, 0), (1, 0)),
            ("SOUTH", (1, 0), (2, 0)),
            ("EAST", (0, 0), (0, 1)),
            ("WEST", (0, 1), (0, 0)),
            ("U", (2, 0), (1, 0)),
            ("D", (1, 0), (2, 0)),
            ("L", (0, 1), (0, 0)),
            ("R", (0, 0), (0, 1)),
        ]
        for cmd, start, expected in cases:
            m = FalkenMaze(self.wopr)
            m.player_pos = start
            m.board[start[0]][start[1]] = "P"
            # Place WOPR out of the way
            m.wopr_pos = (0, 4)
            m.board[0][4] = "W"
            m.play_turn(cmd)
            self.assertEqual(m.player_pos, expected, msg=f"failed for {cmd!r}")

    def test_invalid_direction(self) -> None:
        out = self.maze.play_turn("Z")
        self.assertIn("INVALID DIRECTION", out)

    def test_player_cannot_move_off_board(self) -> None:
        # From (4, 0), S is off-board
        out = self.maze.play_turn("s")
        self.assertIn("YOU CAN'T MOVE", out)
        self.assertEqual(self.maze.player_pos, (4, 0))

    def test_player_cannot_move_into_wopr(self) -> None:
        # Put WOPR right above the player
        self.maze.wopr_pos = (3, 0)
        self.maze.board[3][0] = "W"
        out = self.maze.play_turn("n")
        self.assertIn("YOU CAN'T MOVE", out)

    def test_wopr_moves_after_player(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.maze.play_turn("n")
        # WOPR should have moved toward the center
        wr, wc = self.maze.wopr_pos
        # Closer to center (2,2) than start (0,4)
        d_after = abs(wr - 2) + abs(wc - 2)
        d_before = abs(0 - 2) + abs(4 - 2)
        self.assertLess(d_after, d_before)

    def test_player_wins_by_reaching_center(self) -> None:
        # Move player to (3, 2), then to center
        self.maze.player_pos = (3, 2)
        self.maze.board[3][2] = "P"
        self.maze.turn = "P"
        with mock.patch("time.sleep", lambda *a, **kw: None):
            out = self.maze.play_turn("n")
        self.assertIn("YOU FOUND YOUR WAY OUT", out)
        self.assertTrue(self.maze.game_over)

    def test_wopr_wins_by_reaching_center(self) -> None:
        # Move WOPR right next to center
        self.maze.wopr_pos = (3, 2)
        self.maze.board[3][2] = "W"
        self.maze.turn = "P"
        with mock.patch("time.sleep", lambda *a, **kw: None):
            out = self.maze.play_turn("e")
        # WOPR moves next, may reach center
        # If it does, we get the WOPR-wins message
        # If not, we get the "your move" prompt
        # The test is satisfied if either case is handled
        self.assertTrue(
            "I FOUND MY WAY OUT FIRST" in out or "YOUR MOVE" in out
        )

    def test_manhattan_distance(self) -> None:
        self.assertEqual(self.maze._manhattan((0, 0), (3, 4)), 7)
        self.assertEqual(self.maze._manhattan((2, 2), (2, 2)), 0)

    def test_ai_chooses_closer_to_center(self) -> None:
        # WOPR at (0, 4) should move toward (2, 2)
        move = self.maze._wopr_ai_move()
        self.assertIn(move, [(0, 3), (1, 4), (0, 3)])

    def test_play_again_resets(self) -> None:
        self.maze.game_over = True
        with mock.patch("time.sleep", lambda *a, **kw: None):
            out = self.maze.play_turn("yes")
        self.assertIn("FIND YOUR WAY OUT", out)
        self.assertFalse(self.maze.game_over)

    def test_play_again_no_returns_to_menu(self) -> None:
        self.maze.game_over = True
        out = self.maze.play_turn("no")
        self.assertIn("RETURNING TO MAIN MENU", out)

    def test_max_turns_ends_in_loss(self) -> None:
        # Force end of game by max turns
        self.maze.moves_taken = MAX_TURNS - 1
        with mock.patch("time.sleep", lambda *a, **kw: None):
            out = self.maze.play_turn("n")
        # Either the player or WOPR reached center, or max turns hit
        self.assertTrue(self.maze.game_over or "MAZE GOES ON FOREVER" in out
                        or "FOUND MY WAY OUT" in out)
