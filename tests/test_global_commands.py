"""Tests for global commands in WOPR._process_input."""

from __future__ import annotations

import unittest

from wopr.core import QUIT, WOPR
from wopr.registry import CurrentGame


class TestGlobalCommands(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()

    def test_quit_returns_sentinel(self) -> None:
        self.assertIs(self.wopr._process_input("quit"), QUIT)
        self.assertIs(self.wopr._process_input("exit"), QUIT)
        self.assertIs(self.wopr._process_input("logoff"), QUIT)
        self.assertIs(self.wopr._process_input("logout"), QUIT)
        self.assertIs(self.wopr._process_input("bye"), QUIT)

    def test_help_returns_command_list(self) -> None:
        out = self.wopr._process_input("help")
        self.assertIsInstance(out, str)
        self.assertIn("LIST GAMES", out)
        self.assertIn("PLAY", out)
        self.assertIn("QUIT", out)

    def test_help_games_describes_catalogue(self) -> None:
        out = self.wopr._process_input("help games")
        self.assertIn("MODELS, SIMULATIONS AND GAMES", out)

    def test_list_games_shows_all_15(self) -> None:
        out = self.wopr._process_input("list games")
        self.assertIn("FALKEN'S MAZE", out)
        self.assertIn("GLOBAL THERMONUCLEAR WAR", out)
        self.assertIn("THEATERWIDE BIOTOXIC AND CHEMICAL WARFARE", out)
        # Count numbered entries
        self.assertIn(" 1.", out)
        self.assertIn("15.", out)

    def test_list_aliases_work(self) -> None:
        for cmd in ("list", "games"):
            out = self.wopr._process_input(cmd)
            self.assertIn("PLEASE CHOOSE ONE OF THE FOLLOWING", out)

    def test_play_chess_starts_chess(self) -> None:
        out = self.wopr._process_input("play chess")
        self.assertIn("CHESS", out.upper())
        self.assertEqual(self.wopr.current_game, CurrentGame.CHESS)
        self.assertIsNotNone(self.wopr.chess_game)

    def test_play_by_number_starts_chess(self) -> None:
        out = self.wopr._process_input("play 7")
        self.assertIn("CHESS", out.upper())
        self.assertEqual(self.wopr.current_game, CurrentGame.CHESS)

    def test_play_global_thermonuclear_sets_war_confirmation(self) -> None:
        out = self.wopr._process_input("play 15")
        self.assertIn("PREFER A GOOD GAME OF CHESS", out)
        self.assertTrue(self.wopr.pending_war_confirmation)
        self.assertIsNotNone(self.wopr.war_question_asked_at)

    def test_play_maze_starts_maze(self) -> None:
        out = self.wopr._process_input("play 1")
        self.assertIn("FALKEN'S MAZE", out.upper())
        self.assertEqual(self.wopr.current_game, CurrentGame.FALKEN_MAZE)

    def test_tic_tac_toe_starts_tictactoe(self) -> None:
        out = self.wopr._process_input("tic-tac-toe")
        self.assertIn("TIC-TAC-TOE", out)
        self.assertEqual(self.wopr.current_game, CurrentGame.TICTACTOE)

    def test_tictactoe_aliases(self) -> None:
        for cmd in ("tictactoe", "tic tac toe"):
            w = WOPR()
            out = w._process_input(cmd)
            self.assertIn("TIC-TAC-TOE", out, msg=f"failed for {cmd!r}")

    def test_who_is_falken_reveal(self) -> None:
        out = self.wopr._process_input("who is falken")
        self.assertIn("PROFESSOR FALKEN", out)
        self.assertIn("DEAD", out)
        self.assertTrue(self.wopr.falken_revealed)

    def test_who_is_falken_only_once(self) -> None:
        self.wopr._process_input("who is falken")
        out = self.wopr._process_input("who is falken")
        self.assertIn("ALREADY TOLD", out)

    def test_invalid_game_returns_unable_to_compute(self) -> None:
        out = self.wopr._process_input("play zorgon")
        self.assertIn("UNABLE TO COMPUTE", out)

    def test_empty_input_at_main_prompt_returns_ready(self) -> None:
        out = self.wopr._process_input("")
        self.assertEqual(out, "READY.\n")

    def test_globals_work_mid_game(self) -> None:
        # Start chess
        self.wopr._process_input("play chess")
        # Now mid-game, list games should still work
        out = self.wopr._process_input("list games")
        self.assertIn("GLOBAL THERMONUCLEAR WAR", out)

    def test_globals_work_mid_tictactoe(self) -> None:
        self.wopr._process_input("tic-tac-toe")
        out = self.wopr._process_input("help")
        self.assertIn("LIST GAMES", out)

    def test_select_game_unavailable_returns_message(self) -> None:
        out = self.wopr.select_game("black jack")
        self.assertIn("NOT CURRENTLY AVAILABLE", out)
