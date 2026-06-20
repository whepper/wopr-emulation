"""Tests for wopr.defcon."""

from __future__ import annotations

import unittest
from unittest import mock

from wopr.core import WOPR
from wopr.defcon import (
    BANNER_WIDTH,
    DEFCON_DESCRIPTIONS,
    render_banner,
)


class TestDefconBanner(unittest.TestCase):
    def test_all_rows_same_width(self) -> None:
        for level in (1, 2, 3, 4, 5):
            banner = render_banner(level)
            for line in banner.split("\n"):
                if not line:
                    continue
                self.assertEqual(
                    len(line), BANNER_WIDTH, msg=f"line width mismatch at level {level}: {line!r}"
                )

    def test_borders_have_correct_width(self) -> None:
        for level in (1, 2, 3, 4, 5):
            banner = render_banner(level)
            lines = [l for l in banner.split("\n") if l]
            self.assertEqual(len(lines), 5)  # border, head, bar, desc, border
            for border_line in (lines[0], lines[-1]):
                self.assertTrue(border_line.startswith("+"))
                self.assertTrue(border_line.endswith("+"))
                self.assertEqual(len(border_line), BANNER_WIDTH)

    def test_invalid_level_raises(self) -> None:
        with self.assertRaises(ValueError):
            render_banner(0)
        with self.assertRaises(ValueError):
            render_banner(6)

    def test_descriptions_present(self) -> None:
        for level in (1, 2, 3, 4, 5):
            banner = render_banner(level)
            self.assertIn(DEFCON_DESCRIPTIONS[level], banner)


class TestWOPRDefconUpdates(unittest.TestCase):
    def setUp(self) -> None:
        self.wopr = WOPR()

    def test_initial_defcon_is_5(self) -> None:
        self.assertEqual(self.wopr.defcon_level, 5)

    def test_update_changes_level(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.wopr.update_defcon(3)
        self.assertEqual(self.wopr.defcon_level, 3)

    def test_update_same_level_is_noop(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.wopr.update_defcon(5)
        # Defcon shouldn't change and no banner should be printed
        self.assertEqual(self.wopr.defcon_level, 5)

    def test_update_out_of_range_is_noop(self) -> None:
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.wopr.update_defcon(0)
        self.assertEqual(self.wopr.defcon_level, 5)
        with mock.patch("time.sleep", lambda *a, **kw: None):
            self.wopr.update_defcon(6)
        self.assertEqual(self.wopr.defcon_level, 5)

    def test_reset_post_war(self) -> None:
        self.wopr.defcon_level = 1
        self.wopr.reset_post_war()
        self.assertEqual(self.wopr.defcon_level, 5)
