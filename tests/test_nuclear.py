"""Tests for wopr.nuclear.NuclearWarSimulation."""

from __future__ import annotations

import unittest
from unittest import mock

from wopr.core import WOPR
from wopr.nuclear import NORAD_LINES, NuclearWarSimulation


class TestNuclearWarSimulation(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()
        self.wopr.authenticate("joshua")
        self.wopr.current_game = None
        self.captured: list[str] = []
        self.writer = lambda s: self.captured.append(s)
        self.sim = NuclearWarSimulation(self.wopr)
        self.sim._writer = self.writer

    def test_side_selection_usa(self) -> None:
        out = self.sim.play_turn("1")
        self.assertIn("AWAITING FIRST STRIKE", out)
        self.assertEqual(self.sim.player_side, "USA")
        self.assertEqual(self.sim.enemy_side, "USSR")

    def test_side_selection_ussr(self) -> None:
        out = self.sim.play_turn("2")
        self.assertIn("AWAITING FIRST STRIKE", out)
        self.assertEqual(self.sim.player_side, "USSR")
        self.assertEqual(self.sim.enemy_side, "USA")

    def test_side_selection_by_name(self) -> None:
        out = self.sim.play_turn("soviet union")
        self.assertEqual(self.sim.player_side, "USSR")

    def test_invalid_side_reprompts(self) -> None:
        out = self.sim.play_turn("athens")
        self.assertIn("WHICH SIDE DO YOU WANT", out)
        self.assertIsNone(self.sim.player_side)

    def test_start_command_acquires_codes(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
        # Should have printed 9 launch codes
        self.assertEqual(self.wopr.launch_codes_found, 9)
        # DEFCON should be at 3
        self.assertEqual(self.wopr.defcon_level, 3)

    def test_valid_strike_sequence(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            out = self.sim.play_turn("moscow")
        self.assertIn("LAUNCHING MISSILES", "".join(self.captured))
        self.assertIn("SELECT NEXT TARGET", out)

    def test_invalid_target_reprompts(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            out = self.sim.play_turn("atlantis")
        self.assertIn("INVALID TARGET", out)

    def test_defcon_escalation(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            self.sim.play_turn("moscow")  # turn 1, DEFCON still 3
            self.assertEqual(self.wopr.defcon_level, 3)
            self.sim.play_turn("leningrad")  # turn 2, DEFCON 2
            self.assertEqual(self.wopr.defcon_level, 2)
        # Note: turn 3 resets DEFCON to 5 via end_current_game
        # after the learning sequence, so we don't assert here.

    def test_third_strike_triggers_learning(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            self.sim.play_turn("moscow")
            self.sim.play_turn("leningrad")
            self.sim.play_turn("kiev")
        self.assertTrue(self.wopr.learning_mode)
        self.assertTrue(self.sim.game_over)

    def test_norad_chatter_present(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            self.sim.play_turn("moscow")
        text = "".join(self.captured)
        self.assertIn("[NORAD]", text)

    def test_casualty_projection(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            self.sim.play_turn("moscow")
        text = "".join(self.captured)
        self.assertIn("CASUALTIES", text)
        self.assertIn("ESTIMATED", text)

    def test_retaliation(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            self.sim.play_turn("moscow")
        text = "".join(self.captured)
        self.assertIn("RETALIATION DETECTED", text)

    def test_extinction_message(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            self.sim.play_turn("moscow")
            self.sim.play_turn("leningrad")
            self.sim.play_turn("kiev")
        text = "".join(self.captured)
        self.assertIn("EXTINCTION", text)

    def test_list_games_mid_war(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            out = self.sim.play_turn("list games")
        self.assertIn("PLEASE CHOOSE ONE OF THE FOLLOWING", out)

    def test_terminate_after_game_over(self) -> None:
        self.sim.play_turn("1")
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.sim.play_turn("")
            self.sim.play_turn("moscow")
            self.sim.play_turn("leningrad")
            self.sim.play_turn("kiev")
        out = self.sim.play_turn("anything")
        self.assertIn("SIMULATION TERMINATED", out)

    def test_norad_lines_pool(self) -> None:
        self.assertGreater(len(NORAD_LINES), 0)
        for line in NORAD_LINES:
            self.assertTrue(line.startswith("[NORAD]"))
