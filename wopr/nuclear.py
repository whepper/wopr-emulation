"""Global Thermonuclear War simulation for the WOPR system."""

from __future__ import annotations

import random
import time
from typing import Optional

from .timing import Timing

NORAD_LINES: list[str] = [
    "[NORAD] GENERAL, WE HAVE MULTIPLE LAUNCH DETECTIONS.",
    "[NORAD] TRACKING 14 INCOMING \u2014 IMPACT IN 90 SECONDS.",
    "[NORAD] SECOND-STRIKE AUTHORIZATION REQUESTS INCOMING.",
    "[NORAD] ALL COMMUNICATIONS WITHIN SECTOR 7 ARE DOWN.",
    "[NORAD] EARLY-WARNING SATELLITES CONFIRM SUBMARINE LAUNCHES.",
    "[NORAD] COMMAND, OUR OWN CODES ARE BEING CRACKED IN REALTIME.",
    "[NORAD] RECOMMEND IMMEDIATE RETALIATORY STRIKE.",
]


class NuclearWarSimulation:
    """Global Thermonuclear War simulation for the WOPR system."""

    COUNTRIES: dict[str, dict[str, list[str]]] = {
        "USA": {
            "cities": ["washington", "new york", "los angeles", "las vegas", "seattle"],
        },
        "USSR": {
            "cities": ["moscow", "leningrad", "kiev", "minsk", "tashkent"],
        },
    }

    def __init__(self, wopr) -> None:
        self.wopr = wopr
        self.player_side: Optional[str] = None
        self.enemy_side: Optional[str] = None
        self.game_over: bool = False
        self.turn_count: int = 0
        self.awaiting_side: bool = True
        self.awaiting_start: bool = False
        self._writer = lambda s: print(s, end="", flush=True)

    def _norad_chatter(self) -> None:
        """Insert a 1-2 line NORAD interjection for flavor."""
        line = random.choice(NORAD_LINES)
        self._writer(f"\n{line}\n")
        time.sleep(Timing.NORAD_LINE_PAUSE)

    def play_turn(self, user_input: str) -> str:
        if self.awaiting_side:
            s = user_input.strip().upper()
            if s in ("1", "USA", "UNITED STATES", "US", "AMERICA"):
                self.player_side = "USA"
                self.enemy_side = "USSR"
            elif s in ("2", "USSR", "SOVIET UNION", "SOVIET", "RUSSIA"):
                self.player_side = "USSR"
                self.enemy_side = "USA"
            else:
                return (
                    "\nWHICH SIDE DO YOU WANT?\n"
                    "  1. UNITED STATES\n"
                    "  2. SOVIET UNION\n\n"
                    "PLEASE SELECT: "
                )
            self.awaiting_side = False
            self.awaiting_start = True
            return f"\nAWAITING FIRST STRIKE COMMAND. PRESS ENTER TO PROCEED: "

        if self.awaiting_start:
            self.awaiting_start = False
            self.wopr.update_defcon(4)
            time.sleep(Timing.DEFCON_RING_PAUSE)
            self.wopr.simulate_launch_codes(self._writer)
            self.wopr.update_defcon(3)
            targets = "\n".join(
                f"  - {t.upper()}"
                for t in self.COUNTRIES[self.enemy_side]["cities"]
            )
            return (
                f"\nYOU ARE {self.player_side}. ENEMY: {self.enemy_side}.\n"
                f"\nPRIMARY TARGETS SELECTION:\n{targets}\n\nSELECT TARGET: "
            )

        if self.game_over:
            return "\nSIMULATION TERMINATED."

        target = user_input.lower().strip()
        if target in ("list games", "games", "list"):
            return self.wopr.display_game_list()
        enemy_cities = self.COUNTRIES[self.enemy_side]["cities"]
        if target not in enemy_cities:
            return "\nINVALID TARGET. SELECT FROM AVAILABLE TARGETS: "

        self.turn_count += 1
        self._norad_chatter()

        self._writer(f"\nLAUNCHING MISSILES AT {target.upper()}...\n")
        time.sleep(Timing.STRIKE_LAUNCH_PAUSE)
        self._writer(f"IMPACT AT {target.upper()}: DIRECT HIT\n")
        self._writer(
            f"CASUALTIES: {random.randint(500_000, 2_000_000):,} ESTIMATED\n"
        )
        time.sleep(Timing.STRIKE_IMPACT_PAUSE)

        if self.turn_count == 2:
            self.wopr.update_defcon(2)
        elif self.turn_count >= 3:
            self.wopr.update_defcon(1)

        retaliation_pool = self.COUNTRIES[self.player_side]["cities"]
        retaliation_target = random.choice(retaliation_pool)
        self._writer(f"\n{self.enemy_side} RETALIATION DETECTED\n")
        time.sleep(Timing.RETALIATION_DETECTED_PAUSE)
        self._writer(f"INCOMING MISSILES TARGETING {retaliation_target.upper()}\n")
        time.sleep(Timing.STRIKE_LAUNCH_PAUSE)
        self._writer(f"IMPACT AT {retaliation_target.upper()}: DIRECT HIT\n")
        self._writer(
            f"CASUALTIES: {random.randint(800_000, 3_000_000):,} ESTIMATED\n"
        )
        time.sleep(Timing.STRIKE_IMPACT_PAUSE)

        if self.turn_count >= 3:
            self.wopr.reveal_final_launch_code(self._writer)
            self._writer("\n" + "=" * 50 + "\n")
            self._writer("PROJECTION: TOTAL GLOBAL CASUALTIES > 500 MILLION\n")
            self._writer("PROJECTED OUTCOME: EXTINCTION OF HUMAN SPECIES\n")
            self._writer("=" * 50 + "\n")
            time.sleep(Timing.CASUALTY_PROJECTION_PAUSE)
            self.game_over = True
            self.wopr.run_learning_sequence()
            self.wopr.end_current_game()
            return ""

        return "\nSELECT NEXT TARGET: "
