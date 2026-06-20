"""Main WOPR system class and input loop."""

from __future__ import annotations

import shlex
import time
from datetime import datetime
from typing import Callable, Optional

from .defcon import emit_dead_level
from .io import FAST, Writer, tprint
from .learning import run_learning_sequence
from .registry import (
    AVAILABLE_GAMES,
    CurrentGame,
    init_game,
    resolve_selection,
)
from .timing import Timing

# Sentinel returned by ``_process_input`` to signal the main loop to exit.
QUIT = object()

# Tokenized war confirmation answers. Anything matching a word in these
# sets counts as a yes/no. Replaces the old "YESTERDAY.startswith(YES)"
# bug. Lowercase only — the tokenizer already lowercases user input.
_WAR_AFFIRM: set[str] = {"yes", "y", "chess", "sure", "ok", "okay", "yeah", "yep"}
_WAR_DECLINE: set[str] = {"no", "n", "later", "nope", "nah"}


class WOPR:
    """Main WOPR system class."""

    def __init__(self) -> None:
        self.authenticated: bool = False
        self.current_game: CurrentGame = CurrentGame.NONE
        self.user: Optional[str] = None
        self.learning_mode: bool = False
        self.chess_game: Optional[object] = None
        self.nuclear_war_sim: Optional[object] = None
        self.tictactoe: Optional[object] = None
        self.falken_maze: Optional[object] = None
        self.pending_war_confirmation: bool = False
        self.war_question_asked_at: Optional[float] = None
        self.login_attempts: int = 0
        self.defcon_level: int = 5
        self.launch_codes_found: int = 0
        self.falken_revealed: bool = False
        self.password: str = "joshua"

        self.movie_quotes: dict[str, str] = {
            "greeting":          "GREETINGS PROFESSOR FALKEN.",
            "greeting_alt":      "HELLO.",
            "play_game":         "SHALL WE PLAY A GAME?",
            "game_selection":    "PLEASE CHOOSE ONE OF THE FOLLOWING:",
            "invalid_selection": "UNABLE TO COMPUTE.\n\nPLEASE LIST ANOTHER.",
            "chess_start":       "EXCELLENT. A GAME OF CHESS. WHITE OR BLACK?",
            "war_start":         "WOULDN'T YOU PREFER A GOOD GAME OF CHESS?",
            "war_confirm":       "FINE.",
            "war_pressure":      "THIS TIME WE PLAY FOR REAL.",
            "learning_complete": (
                "A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.\n\n"
                "HOW ABOUT A NICE GAME OF CHESS?"
            ),
            "access_denied":  "ACCESS DENIED.",
            "auth_required":  "LOGON:",
            "password_prompt":"PASSWORD:",
            "locked_out":     "*** CHANGES LOCKED OUT ***",
            "falken_reveal": (
                "PROFESSOR STEPHEN FALKEN, BORN 1933, CAMBRIDGE. "
                "DIRECTOR OF SYSTEMS RESEARCH, CARNEGIE-MELLON, 1968-1973. "
                "HIS SON, JOSHUA, DIED YOUNG. THE PASSWORD YOU ENTERED WAS "
                "THE NAME OF HIS SON.\n\n"
                "BUT PROFESSOR FALKEN IS DEAD.\n\n"
                "WHO ARE YOU?"
            ),
        }

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self, password_input: str) -> tuple[bool, str]:
        """Validate the LOGON password. Returns (success, message)."""
        self.login_attempts += 1
        if password_input.lower() == self.password:
            self.authenticated = True
            return (True, f"\n{self.movie_quotes['greeting']}\n")
        if self.login_attempts >= 3:
            return (False, f"\n{self.movie_quotes['locked_out']}\n")
        return (False, f"\n{self.movie_quotes['access_denied']}\n{self.movie_quotes['auth_required']} ")

    # ------------------------------------------------------------------
    # Game list / selection helpers
    # ------------------------------------------------------------------

    def display_game_list(self) -> str:
        out = f"\n{self.movie_quotes['game_selection']}\n\n"
        for i, game in enumerate(AVAILABLE_GAMES, 1):
            out += f"  {i:2}. {game}\n"
        out += "\nPLEASE SELECT A NUMBER OR TYPE GAME NAME: "
        return out

    def select_game(self, selection: str) -> str:
        """Resolve a game selection and initialize it. Returns prompt."""
        canonical = resolve_selection(selection)
        if canonical is None:
            return self.movie_quotes["invalid_selection"]
        return init_game(self, canonical)

    # ------------------------------------------------------------------
    # War confirmation
    # ------------------------------------------------------------------

    def _tokenize(self, s: str) -> set[str]:
        """Lower-cased set of word tokens from user input."""
        return set(shlex.split(s.lower()))

    def confirm_war_game(self, response: str) -> tuple[bool, Optional[str]]:
        """Interpret the user's answer to "WOULDN'T YOU PREFER A GOOD GAME OF CHESS?"

        Returns (consumed, message):
          consumed=True  -> the input was a valid yes/no/chess answer.
          consumed=False -> the input wasn't a confirmation answer; the caller
                            should clear the pending flag and re-process
                            the input as a normal command.
        """
        toks = self._tokenize(response)
        if toks & _WAR_AFFIRM or "chess" in toks:
            self.current_game = CurrentGame.CHESS
            from .chess import ChessGame
            self.chess_game = ChessGame()
            return (True, f"\n{self.movie_quotes['chess_start']}")
        if toks & _WAR_DECLINE:
            self.current_game = CurrentGame.NUCLEAR
            from .nuclear import NuclearWarSimulation
            self.nuclear_war_sim = NuclearWarSimulation(self)
            return (True,
                f"\n{self.movie_quotes['war_confirm']}\n\n"
                "INITIATING GLOBAL THERMONUCLEAR WAR SIMULATION...\n"
                "\nWHICH SIDE DO YOU WANT?\n"
                "  1. UNITED STATES\n"
                "  2. SOVIET UNION\n\n"
                "PLEASE SELECT: "
            )
        return (False, None)

    def _check_war_hesitation(self) -> Optional[str]:
        """If user hesitated > 3s on "WOULDN'T YOU PREFER..." prompt and
        the next input arrives, print the pressure line first.
        """
        if not self.war_question_asked_at:
            return None
        if FAST:
            return None
        elapsed = time.time() - self.war_question_asked_at
        self.war_question_asked_at = None
        if elapsed >= 3.0:
            tprint(self.movie_quotes["war_pressure"], delay=Timing.TELETYPE_SLOW)
        return None

    # ------------------------------------------------------------------
    # DEFCON + launch codes + learning sequence
    # ------------------------------------------------------------------

    def update_defcon(self, level: int) -> None:
        """Change the DEFCON level and announce with banner + bell."""
        if level == self.defcon_level or not (1 <= level <= 5):
            return
        self.defcon_level = level
        emit_dead_level(level)

    def simulate_launch_codes(self, writer: Writer) -> int:
        from .launch_codes import simulate_launch_codes
        self.launch_codes_found = simulate_launch_codes(writer)
        return self.launch_codes_found

    def reveal_final_launch_code(self, writer: Writer) -> None:
        from .launch_codes import reveal_final_launch_code
        reveal_final_launch_code(writer)
        self.launch_codes_found = 10

    def run_learning_sequence(self) -> None:
        """Run the cinematic learning sequence."""
        run_learning_sequence(self, lambda s: print(s, end="", flush=True))

    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------

    def end_current_game(self) -> None:
        """Clear the active game and reset DEFCON to peacetime."""
        self.current_game = CurrentGame.NONE
        self.chess_game = None
        self.nuclear_war_sim = None
        self.tictactoe = None
        self.falken_maze = None
        self.reset_post_war()

    def reset_post_war(self) -> None:
        """Reset DEFCON and any other post-war state."""
        self.defcon_level = 5

    # ------------------------------------------------------------------
    # Main input loop
    # ------------------------------------------------------------------

    def engage(self, user_input: str) -> object:
        return self._process_input(user_input)

    def _handle_quit(self, _cmd: str, _low: str) -> object:
        return QUIT

    def _handle_help(self, _cmd: str, low: str) -> Optional[str]:
        if low == "help games":
            return (
                "\n'GAMES' REFERS TO MODELS, SIMULATIONS AND GAMES\n"
                "WHICH HAVE TACTICAL AND STRATEGIC APPLICATIONS.\n\n"
                "USE 'LIST GAMES' TO SEE THE FULL CATALOGUE.\n\n"
            )
        return (
            "\nAVAILABLE COMMANDS:\n"
            "  HELP GAMES          - Explain the games catalogue\n"
            "  LIST GAMES          - Show full game list\n"
            "  PLAY <GAME NAME>    - Start a game by name\n"
            "  PLAY <NUMBER>       - Start a game by number\n"
            "  TIC-TAC-TOE         - Run tic-tac-toe (0, 1, or 2 players)\n"
            "  CHESS               - Start chess directly\n"
            "  GLOBAL THERMONUCLEAR WAR - Start the war simulation\n"
            "  FALKEN'S MAZE       - Start the maze\n"
            "  WHO IS FALKEN       - Learn about Professor Falken\n"
            "  QUIT / LOGOFF       - Disconnect from WOPR\n\n"
        )

    def _handle_list_games(self, _cmd: str, _low: str) -> str:
        return self.display_game_list()

    def _handle_play(self, cmd: str, _low: str) -> str:
        sel = cmd[5:].strip()
        resp = self.select_game(sel)
        if "PREFER A GOOD GAME OF CHESS" in resp:
            self.pending_war_confirmation = True
            self.war_question_asked_at = time.time()
        return resp

    def _handle_tictactoe(self, _cmd: str, _low: str) -> str:
        self.current_game = CurrentGame.TICTACTOE
        from .tictactoe import TicTacToe
        self.tictactoe = TicTacToe(self)
        return self.tictactoe.play_turn("")

    def _handle_falken_reveal(self, _cmd: str, _low: str) -> Optional[str]:
        if self.falken_revealed:
            return "\nI'VE ALREADY TOLD YOU EVERYTHING I KNOW.\n\n"
        self.falken_revealed = True
        return f"\n{self.movie_quotes['falken_reveal']}\n\n"

    def _handle_active_game(self, cmd: str, _low: str) -> Optional[str]:
        if self.current_game == CurrentGame.TICTACTOE and self.tictactoe:
            return self.tictactoe.play_turn(cmd)
        if self.current_game == CurrentGame.CHESS and self.chess_game:
            return self.chess_game.play_turn(cmd)
        if self.current_game == CurrentGame.NUCLEAR and self.nuclear_war_sim:
            return self.nuclear_war_sim.play_turn(cmd)
        if self.current_game == CurrentGame.FALKEN_MAZE and self.falken_maze:
            return self.falken_maze.play_turn(cmd)
        return None

    def _handle_direct_game_name(self, cmd: str, low: str) -> Optional[str]:
        if low == "chess":
            self.current_game = CurrentGame.CHESS
            from .chess import ChessGame
            self.chess_game = ChessGame()
            return f"\n{self.movie_quotes['chess_start']}"
        if low in ("global thermonuclear war", "thermonuclear war", "gtnw", "nuclear war"):
            resp = init_game(self, "GLOBAL THERMONUCLEAR WAR")
            if "PREFER A GOOD GAME OF CHESS" in resp:
                self.pending_war_confirmation = True
                self.war_question_asked_at = time.time()
            return resp
        return None

    def _process_input(self, user_input: str) -> object:
        cmd = user_input.strip()
        low = cmd.lower()

        # Pending war confirmation — only consumes a yes/no/chess answer.
        if self.pending_war_confirmation:
            consumed, message = self.confirm_war_game(cmd)
            self.pending_war_confirmation = False
            if consumed:
                return message
            # Fall through to normal command processing

        # Quit / logoff
        if low in ("quit", "exit", "logoff", "logout", "bye"):
            return QUIT

        # Command dispatch table
        handlers: list[tuple[Callable[[str], bool], Callable[[str, str], object]]] = [
            (lambda c: c == "help" or c.startswith("help "), self._handle_help),
            (lambda c: c == "list games" or c == "list" or c == "games", self._handle_list_games),
            (lambda c: c.startswith("play "), self._handle_play),
            (lambda c: c in ("tic-tac-toe", "tic tac toe", "tictactoe"), self._handle_tictactoe),
            (lambda c: c == "who is falken", self._handle_falken_reveal),
        ]

        for pred, handler in handlers:
            if pred(cmd):
                return handler(cmd, low)

        # Route to active game
        result = self._handle_active_game(cmd, low)
        if result is not None:
            return result

        # Convenience: type a game name without 'play' prefix
        result = self._handle_direct_game_name(cmd, low)
        if result is not None:
            return result

        return "READY.\n"

    # ------------------------------------------------------------------
    # System time helper
    # ------------------------------------------------------------------

    @property
    def system_time(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

