"""Tests for wopr.launch_codes."""

from __future__ import annotations

import unittest
from unittest import mock

from wopr.core import WOPR
from wopr.launch_codes import KNOWN_CODES, reveal_final_launch_code, simulate_launch_codes


class TestLaunchCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()
        self.captured: list[str] = []

    def writer(self, s: str) -> None:
        self.captured.append(s)

    def test_known_codes_count(self) -> None:
        self.assertEqual(len(KNOWN_CODES), 10)

    def test_known_codes_format(self) -> None:
        for code in KNOWN_CODES:
            parts = code.split("-")
            self.assertEqual(len(parts), 3, msg=f"bad format: {code!r}")
            self.assertEqual(len(parts[0]), 3)
            self.assertEqual(len(parts[1]), 4)
            self.assertEqual(len(parts[2]), 3)

    def test_final_code_is_famous(self) -> None:
        self.assertEqual(KNOWN_CODES[-1], "CPE-1704-TKS")

    def test_simulate_prints_nine_codes(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            count = simulate_launch_codes(self.writer)
        self.assertEqual(count, 9)
        text = "".join(self.captured)
        for i in range(1, 10):
            self.assertIn(f"LAUNCH CODE {i}/10 ACQUIRED", text)
        self.assertIn("WARNING: 9 OF 10 LAUNCH CODES", text)
        self.assertIn("SEARCHING FOR FINAL LAUNCH CODE", text)

    def test_reveal_final_brute_forces(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None), \
             mock.patch("sys.stdout.write") as mock_write:
            reveal_final_launch_code(self.writer, target="ABC-1234-XYZ", shuffle=False)
        # The brute force should write the target as the final line
        # Check that the mock was called with the target
        all_writes = "".join(
            call.args[0] if call.args else "" for call in mock_write.call_args_list
        )
        self.assertIn("ABC-1234-XYZ", all_writes)
        self.assertIn("ALL 10 LAUNCH CODES ACQUIRED", "".join(self.captured))

    def test_reveal_works_with_default_target(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None), \
             mock.patch("sys.stdout.write") as mock_write:
            reveal_final_launch_code(self.writer)
        all_writes = "".join(
            call.args[0] if call.args else "" for call in mock_write.call_args_list
        )
        self.assertIn("CPE-1704-TKS", all_writes)


class TestWOPRLaunchCodes(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()
        self.captured: list[str] = []

    def writer(self, s: str) -> None:
        self.captured.append(s)

    def test_simulate_updates_wopr_state(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.wopr.simulate_launch_codes(self.writer)
        self.assertEqual(self.wopr.launch_codes_found, 9)

    def test_reveal_updates_wopr_state(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None), \
             mock.patch("sys.stdout.write"):
            self.wopr.reveal_final_launch_code(self.writer)
        self.assertEqual(self.wopr.launch_codes_found, 10)
