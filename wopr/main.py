"""Entry point and the famous opening conversation."""

from __future__ import annotations

import sys
import time
from typing import Optional

from .core import QUIT, WOPR
from .io import FAST, tprint
from .timing import Timing


def _opening_conversation(wopr: WOPR) -> Optional[bool]:
    """Run the famous opening dialogue. Returns True if it should
    continue, False if EOF."""
    tprint("\nHOW ARE YOU FEELING TODAY?")
    try:
        input()
    except EOFError:
        return False
    time.sleep(Timing.CONVERSATION_PAUSE)
    # The film: WOPR always answers "I'M FINE. HOW ARE YOU?" regardless
    # of the user's reply. This is the famous non-sequitur.
    tprint("\nI'M FINE. HOW ARE YOU?", delay=Timing.TELETYPE_SLOW)
    try:
        input()
    except EOFError:
        return False
    time.sleep(Timing.CONVERSATION_PAUSE)
    tprint("\nEXCELLENT. IT'S BEEN A LONG TIME. CAN YOU EXPLAIN")
    tprint("THE REMOVAL OF YOUR USER ACCOUNT ON 6/23/73?")
    try:
        input()
    except EOFError:
        return False
    time.sleep(Timing.CONVERSATION_PAUSE)
    tprint("\nYES THEY DO.")
    time.sleep(Timing.CONVERSATION_PAUSE)
    tprint(f"\n{wopr.movie_quotes['play_game']}", delay=Timing.TELETYPE_SLOW)
    time.sleep(Timing.CONVERSATION_PAUSE)
    return True


def main() -> None:
    """Main entry point for the WOPR emulation."""
    print("=" * 50)
    print(f"WOPR (War Operation Plan Response)  ::  {wopr_boot_time()}")
    print("DEFENSE SYSTEM ONLINE")
    print("=" * 50)
    time.sleep(Timing.LOGIN_PAUSE)

    wopr = WOPR()
    print(f"\n{wopr.movie_quotes['auth_required']} ", end="", flush=True)

    authenticated = False
    while not authenticated and wopr.login_attempts < 3:
        try:
            attempt = input()
        except EOFError:
            return
        success, message = wopr.authenticate(attempt)
        if success:
            tprint(message, end="")
            authenticated = True
            break
        print(message, end="")
        if wopr.login_attempts >= 3:
            time.sleep(Timing.LOCKOUT_PAUSE)
            print("\nSYSTEM TERMINATING.\n")
            return

    if not authenticated:
        return

    ok = _opening_conversation(wopr)
    if not ok:
        return

    # Initial game list + selection
    print(wopr.display_game_list(), end="")
    try:
        selection = input()
    except EOFError:
        return
    # First try as a game selection (number or name), then fall back to
    # the standard command pipeline. This lets bare-number selections
    # work alongside global commands like "tic-tac-toe" or "who is falken".
    response = wopr.select_game(selection)
    if response == wopr.movie_quotes["invalid_selection"]:
        response = wopr.engage(selection)
    if response is QUIT:
        print("\nGOODBYE.\n")
        return
    if response:
        print(response, end="")
    if isinstance(response, str) and "PREFER" in response:
        wopr.pending_war_confirmation = True
        wopr.war_question_asked_at = time.time()

    # Main game loop
    while True:
        try:
            user_input = input()
        except EOFError:
            print("\n\nCONNECTION TERMINATED.")
            break
        except KeyboardInterrupt:
            print("\n\nSYSTEM INTERRUPTED.")
            break

        response = wopr.engage(user_input)
        if response is QUIT:
            print("\nGOODBYE.\n")
            break

        if wopr.learning_mode:
            wopr.learning_mode = False
            wopr.end_current_game()
            print(f"\n{wopr.movie_quotes['play_game']}\n")
            print(wopr.display_game_list(), end="")
            continue

        if response:
            print(response, end="")


def wopr_boot_time() -> str:
    """Return the current system time in the format used at boot."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
