"""Tests for wopr.learning.run_learning_sequence."""

from __future__ import annotations

import unittest
from unittest import mock

from wopr.core import WOPR
from wopr.learning import COUNTDOWN_TICKS, SCENARIOS, run_learning_sequence


class TestLearningSequence(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()
        self.captured: list[str] = []

    def writer(self, s: str) -> None:
        self.captured.append(s)

    def test_runs_all_scenarios(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            run_learning_sequence(self.wopr, self.writer)
        text = "".join(self.captured)
        for scenario in SCENARIOS:
            self.assertIn(scenario, text)
        self.assertIn("TOTAL ANNIHILATION", text)

    def test_runs_tictactoe_module(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            run_learning_sequence(self.wopr, self.writer)
        text = "".join(self.captured)
        self.assertIn("TIC-TAC-TOE LEARNING MODULE", text)
        self.assertIn("DRAW", text)

    def test_includes_countdown(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            run_learning_sequence(self.wopr, self.writer)
        text = "".join(self.captured)
        for n in range(COUNTDOWN_TICKS, 0, -1):
            self.assertIn(f"{n}...", text)

    def test_includes_is_this_a_game_line(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            run_learning_sequence(self.wopr, self.writer)
        text = "".join(self.captured)
        self.assertIn("IS THIS A GAME OR IS IT REAL?", text)

    def test_punchline_present(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            run_learning_sequence(self.wopr, self.writer)
        text = "".join(self.captured)
        self.assertIn("THE ONLY WINNING MOVE IS NOT TO PLAY", text)
        self.assertIn("HOW ABOUT A NICE GAME OF CHESS?", text)

    def test_sets_learning_mode(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            run_learning_sequence(self.wopr, self.writer)
        self.assertTrue(self.wopr.learning_mode)

    def test_tictactoe_self_play_ends_in_draws(self) -> None:
        # The autoplay portion must end in all draws (with perfect play)
        with mock.patch("time.sleep", lambda *a, **kw: None):
            run_learning_sequence(self.wopr, self.writer)
        # All games should be DRAW (no WINNER lines in the learning output)
        game_blocks = [s for s in self.captured if s.startswith("GAME ")]
        self.assertGreater(len(game_blocks), 0)
        # No winner announced
        self.assertNotIn("  WINNER:", "".join(self.captured))
