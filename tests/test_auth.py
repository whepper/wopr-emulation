"""Tests for wopr.core.WOPR.authenticate."""

from __future__ import annotations

import unittest

from wopr.core import WOPR


class TestAuthenticate(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()

    def test_correct_password_returns_success(self) -> None:
        success, msg = self.wopr.authenticate("joshua")
        self.assertTrue(success)
        self.assertIn("GREETINGS PROFESSOR FALKEN", msg)
        self.assertTrue(self.wopr.authenticated)

    def test_password_is_case_insensitive(self) -> None:
        success, _ = self.wopr.authenticate("JOSHUA")
        self.assertTrue(success)

    def test_wrong_password_returns_failure_with_prompt(self) -> None:
        success, msg = self.wopr.authenticate("wrong")
        self.assertFalse(success)
        self.assertIn("ACCESS DENIED", msg)
        self.assertIn("LOGON", msg)
        self.assertFalse(self.wopr.authenticated)

    def test_login_attempts_increments(self) -> None:
        self.assertEqual(self.wopr.login_attempts, 0)
        self.wopr.authenticate("wrong")
        self.assertEqual(self.wopr.login_attempts, 1)
        self.wopr.authenticate("wrong")
        self.assertEqual(self.wopr.login_attempts, 2)

    def test_three_failures_locks_out(self) -> None:
        for _ in range(3):
            success, msg = self.wopr.authenticate("wrong")
        self.assertFalse(success)
        self.assertIn("CHANGES LOCKED OUT", msg)
        self.assertEqual(self.wopr.login_attempts, 3)

    def test_attempts_continue_after_lockout(self) -> None:
        for _ in range(5):
            self.wopr.authenticate("wrong")
        self.assertEqual(self.wopr.login_attempts, 5)

    def test_success_message_appears_only_for_correct_password(self) -> None:
        # The greeting must not be revealed for wrong attempts.
        _, wrong_msg = self.wopr.authenticate("bad")
        self.assertNotIn("GREETINGS PROFESSOR FALKEN", wrong_msg)
