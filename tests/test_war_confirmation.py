"""Tests for war confirmation logic — particularly the YESTERDAY regression.

This file exists to lock in the fix for the original bug where input
starting with "yes" (e.g. "YESTERDAY") would launch a chess game
because the war confirmation used ``startswith`` instead of tokenization.
"""

from __future__ import annotations

import unittest

from wopr.core import _WAR_AFFIRM, _WAR_DECLINE, WOPR


class TestWarConfirmation(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()
        self.wopr.pending_war_confirmation = True

    def test_yes_launches_chess(self) -> None:
        consumed, msg = self.wopr.confirm_war_game("yes")
        self.assertTrue(consumed)
        self.assertIn("CHESS", msg.upper())
        # confirm_war_game itself doesn't clear the flag; _process_input does

    def test_y_alias(self) -> None:
        consumed, _ = self.wopr.confirm_war_game("y")
        self.assertTrue(consumed)
        self.assertIn("CHESS", self.wopr.chess_game.__class__.__name__.upper() if self.wopr.chess_game else "")

    def test_chess_word_launches_chess(self) -> None:
        consumed, _ = self.wopr.confirm_war_game("chess")
        self.assertTrue(consumed)

    def test_no_launches_war(self) -> None:
        consumed, msg = self.wopr.confirm_war_game("no")
        self.assertTrue(consumed)
        self.assertIn("THERMONUCLEAR WAR", msg.upper())

    def test_n_alias(self) -> None:
        consumed, _ = self.wopr.confirm_war_game("n")
        self.assertTrue(consumed)

    def test_regression_yesterday_does_not_consume(self) -> None:
        """'YESTERDAY' must NOT be treated as a yes-answer."""
        consumed, _ = self.wopr.confirm_war_game("YESTERDAY")
        self.assertFalse(consumed)

    def test_regression_northern_does_not_consume(self) -> None:
        """'NORTHERN' starts with 'N' but should not be a no-answer."""
        consumed, _ = self.wopr.confirm_war_game("NORTHERN")
        self.assertFalse(consumed)

    def test_later_is_decline(self) -> None:
        consumed, _ = self.wopr.confirm_war_game("later")
        self.assertTrue(consumed)
        # Declining means war game is initialized
        self.assertIsNotNone(self.wopr.nuclear_war_sim)

    def test_garbage_does_not_consume(self) -> None:
        consumed, _ = self.wopr.confirm_war_game("zxcvbnm")
        self.assertFalse(consumed)

    def test_set_contents_lowercase(self) -> None:
        # The tokenized sets must be lowercase (because shlex splits and
        # lower() the input).
        for word in _WAR_AFFIRM:
            self.assertEqual(word, word.lower())
        for word in _WAR_DECLINE:
            self.assertEqual(word, word.lower())

    def test_mixed_case_works(self) -> None:
        # Uppercase input is lowered by the tokenizer.
        consumed, _ = self.wopr.confirm_war_game("YES")
        self.assertTrue(consumed)

    def test_extra_words_still_match(self) -> None:
        # "yes please" should still count
        consumed, _ = self.wopr.confirm_war_game("yes please")
        self.assertTrue(consumed)
