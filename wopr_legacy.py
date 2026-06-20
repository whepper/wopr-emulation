#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WOPR Emulation - Movie-Accurate Python Implementation

This program emulates the WOPR (War Operation Plan Response) computer system
from the 1983 film WarGames. It includes:
- Movie-accurate dialogue and responses
- Joshua password authentication
- Complete game list menu
- Global command parser: help, list games, play <game>, quit
- DEFCON level system
- Launch code brute-forcing simulation
- Chess game implementation
- Tic-tac-toe with 0-player self-play, 1-player vs WOPR, and 2-player modes
- Global Thermonuclear War simulation
- Learning mode with futility realization sequence

Usage:
    python3 wopr.py

Author: Your Name
License: MIT
"""

import os
import random
import time
import sys
from datetime import datetime

# Sentinel returned by _process_input() to signal the main loop to exit.
_QUIT = object()

# Teletype effect — characters print one-by-one for the dramatic prompts.
# Disable by setting WOPR_FAST=1 in the environment, or pass --fast.
_TELETYPE_DELAY = 0.012
_FAST = os.environ.get("WOPR_FAST") == "1" or "--fast" in sys.argv


def tprint(text, end="\n", delay=None):
    """Print like a 1983 modem: one character at a time."""
    if _FAST or delay == 0:
        print(text, end=end, flush=True)
        return
    d = _TELETYPE_DELAY if delay is None else delay
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        if ch != " ":
            time.sleep(d)
    if end:
        sys.stdout.write(end)
        sys.stdout.flush()


# ---------------------------------------------------------------------------
# TIC-TAC-TOE
# ---------------------------------------------------------------------------

class TicTacToe:
    """
    Tic-tac-toe implementation.

    Modes:
      0 players  - WOPR self-play, ends in draws, triggers learning sequence
      1 player   - Human (X) vs WOPR (O); WOPR plays optimally
      2 players  - Human X vs Human O, alternating turns
    """

    def __init__(self, wopr):
        self.wopr = wopr
        self.awaiting_players = True
        self.players = None          # 0 / 1 / 2
        self.board = [" "] * 9
        self.turn = 0                # 0 = X, 1 = O
        self.game_over = False

    # ------------------------------------------------------------------
    # Board helpers
    # ------------------------------------------------------------------

    def _render(self, b=None):
        b = b or self.board
        def cell(i):
            return b[i] if b[i] != " " else str(i + 1)
        return (
            f"\n {cell(0)} | {cell(1)} | {cell(2)}\n"
            f"---+---+---\n"
            f" {cell(3)} | {cell(4)} | {cell(5)}\n"
            f"---+---+---\n"
            f" {cell(6)} | {cell(7)} | {cell(8)}\n"
        )

    def _winner(self, b=None):
        b = b or self.board
        for i, j, k in [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]:
            if b[i] != " " and b[i] == b[j] == b[k]:
                return b[i]
        return None

    def _is_full(self, b=None):
        b = b or self.board
        return " " not in b

    def _best_move(self, b, me, opp):
        """Minimax-lite: win, block, center, corner, side."""
        for idx in range(9):
            if b[idx] == " ":
                b[idx] = me
                if self._winner(b) == me:
                    b[idx] = " "
                    return idx
                b[idx] = " "
        for idx in range(9):
            if b[idx] == " ":
                b[idx] = opp
                if self._winner(b) == opp:
                    b[idx] = " "
                    return idx
                b[idx] = " "
        if b[4] == " ":
            return 4
        for idx in [0, 2, 6, 8]:
            if b[idx] == " ":
                return idx
        for idx in [1, 3, 5, 7]:
            if b[idx] == " ":
                return idx
        return None

    # ------------------------------------------------------------------
    # 0-player autoplay (used by learning sequence)
    # ------------------------------------------------------------------

    def _play_one_game(self, b, delay=0.2):
        """Play a single 0-player game on a fresh board; returns winner or None."""
        symbols = ["X", "O"]
        turn = 0
        while True:
            me  = symbols[turn % 2]
            opp = symbols[(turn + 1) % 2]
            mv  = self._best_move(b, me, opp)
            if mv is None:
                break
            b[mv] = me
            print(self._render(b))
            time.sleep(delay)
            if self._winner(b):
                return self._winner(b)
            if " " not in b:
                break
            turn += 1
        return None

    def _autoplay(self, games=12, delay=0.15):
        """Run `games` self-play games; all end in draws with perfect play."""
        print("\nINITIATING TIC-TAC-TOE SELF-PLAY...\n")
        time.sleep(1)
        for g in range(1, games + 1):
            print(f"GAME {g}:")
            b = [" "] * 9
            winner = self._play_one_game(b, delay=delay)
            if winner:
                print(f"  WINNER: {winner}\n")
            else:
                print("  DRAW\n")
            time.sleep(0.3)

    # ------------------------------------------------------------------
    # Human-game helpers
    # ------------------------------------------------------------------

    def _current_symbol(self):
        return "X" if self.turn % 2 == 0 else "O"

    def _prompt_move(self):
        sym = self._current_symbol()
        if self.players == 1:
            label = "YOUR" if sym == "X" else "MY"
        else:
            label = f"PLAYER {1 if sym == 'X' else 2} ({sym})"
        return f"{label} MOVE (1-9): "

    def _apply_move(self, cell_str):
        """Validate and apply a human move. Returns error string or None."""
        try:
            idx = int(cell_str.strip()) - 1
        except ValueError:
            return "INVALID INPUT. ENTER A NUMBER 1-9: "
        if not (0 <= idx <= 8):
            return "NUMBER MUST BE 1-9: "
        if self.board[idx] != " ":
            return "SQUARE ALREADY TAKEN. CHOOSE ANOTHER: "
        self.board[idx] = self._current_symbol()
        return None

    # ------------------------------------------------------------------
    # Main play_turn dispatcher
    # ------------------------------------------------------------------

    def play_turn(self, user_input):
        """Called by the WOPR engine for each user input."""

        # ---- Step 1: ask player count --------------------------------
        if self.awaiting_players:
            self.awaiting_players = False
            return (
                "\nTIC-TAC-TOE\n"
                + self._render([" "] * 9)

                + "  1  2  3\n"
                  "  4  5  6\n"
                  "  7  8  9\n"
                  "\nONE OR TWO PLAYERS? (0 = WOPR SELF-PLAY)\n"
                  "PLEASE LIST NUMBER OF PLAYERS: "
            )

        # ---- Step 2: receive player count ----------------------------
        if self.players is None:
            s = user_input.strip()
            if s not in ("0", "1", "2"):
                return "\nPLEASE LIST NUMBER OF PLAYERS (0, 1, OR 2): "
            self.players = int(s)

            if self.players == 0:
                self._autoplay()
                print("\nANALYSIS COMPLETE.\n")
                time.sleep(1)
                self.wopr.run_learning_sequence()
                self.wopr.current_game = None
                self.wopr.tictactoe = None
                return ""

            if self.players == 1:
                return (
                    "\nYOU ARE X. I AM O.\n"
                    + self._render()
                    + "\n" + self._prompt_move()
                )
            # 2 players
            return (
                "\nPLAYER 1 = X  |  PLAYER 2 = O\n"
                + self._render()
                + "\n" + self._prompt_move()
            )

        # ---- Step 3: game already over? ------------------------------
        if self.game_over:
            s = user_input.strip().upper()
            if "YES" in s or s in ("Y", "1"):
                # Reset for a new game
                self.board = [" "] * 9
                self.turn = 0
                self.game_over = False
                return (
                    "\nNEW GAME.\n"
                    + self._render()
                    + "\n" + self._prompt_move()
                )
            # Return to main prompt
            self.wopr.current_game = None
            self.wopr.tictactoe = None
            return "\nRETURNING TO MAIN MENU.\n"

        # ---- Step 4: 1-player — WOPR's turn (X just moved) ----------
        # In 1-player mode, after a human move we immediately compute
        # WOPR's reply and return both in one string.

        # ---- Step 5: handle human input ------------------------------
        sym = self._current_symbol()

        # In 1-player mode only X is human
        if self.players == 1 and sym == "O":
            # Shouldn't reach here; defensive guard
            pass
        else:
            err = self._apply_move(user_input)
            if err:
                return "\n" + err

            self.turn += 1
            winner = self._winner()
            if winner:
                self.game_over = True
                if self.players == 1:
                    result = "YOU WIN!" if winner == "X" else "I WIN."
                else:
                    player_no = 1 if winner == "X" else 2
                    result = f"PLAYER {player_no} ({winner}) WINS!"
                return self._render() + f"\n{result}\n\nPLAY AGAIN? (YES/NO): "
            if self._is_full():
                self.game_over = True
                return self._render() + "\nDRAW.\n\nPLAY AGAIN? (YES/NO): "

        # ---- Step 6: WOPR's move in 1-player mode --------------------
        if self.players == 1:
            time.sleep(0.6)
            mv = self._best_move(self.board, "O", "X")
            if mv is not None:
                self.board[mv] = "O"
                self.turn += 1
                winner = self._winner()
                wopr_cell = mv + 1
                if winner:
                    self.game_over = True
                    return (
                        self._render()
                        + f"\nMY MOVE: {wopr_cell}\nI WIN.\n\nPLAY AGAIN? (YES/NO): "
                    )
                if self._is_full():
                    self.game_over = True
                    return (
                        self._render()
                        + f"\nMY MOVE: {wopr_cell}\nDRAW.\n\nPLAY AGAIN? (YES/NO): "
                    )
                return (
                    self._render()
                    + f"\nMY MOVE: {wopr_cell}\n\n"
                    + self._prompt_move()
                )

        # ---- Step 7: 2-player — prompt next human --------------------
        return self._render() + "\n" + self._prompt_move()


# ---------------------------------------------------------------------------
# CHESS
# ---------------------------------------------------------------------------

class ChessGame:
    """Chess game implementation for the WOPR system."""

    def __init__(self):
        self.board = self._initialize_board()
        self.player_color = None
        self.game_over = False
        self.move_count = 0
        self.move_history = []
        self.awaiting_color_selection = True

    def _initialize_board(self):
        return [
            ["r","n","b","q","k","b","n","r"],
            ["p","p","p","p","p","p","p","p"],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            [" "," "," "," "," "," "," "," "],
            ["P","P","P","P","P","P","P","P"],
            ["R","N","B","Q","K","B","N","R"],
        ]

    def play_turn(self, user_input):
        if self.awaiting_color_selection:
            color = user_input.strip().upper()
            if "WHITE" in color or color == "W":
                self.player_color = "WHITE"
                self.awaiting_color_selection = False
                return "\nYOU ARE WHITE. YOUR MOVE: "
            elif "BLACK" in color or color == "B":
                self.player_color = "BLACK"
                self.awaiting_color_selection = False
                wopr_move = self._make_ai_move()
                return f"\nYOU ARE BLACK. MY OPENING MOVE: {wopr_move}\n\nYOUR MOVE: "
            else:
                return "\nPLEASE SELECT WHITE OR BLACK: "

        if self.game_over:
            return "\nGAME OVER."

        try:
            from_sq, to_sq = user_input.split()
            fr, fc = 8 - int(from_sq[1]), ord(from_sq[0]) - ord('a')
            tr, tc = 8 - int(to_sq[1]),   ord(to_sq[0])  - ord('a')
        except Exception:
            return "\nINVALID INPUT. USE FORMAT 'e2 e4': "

        if not (0 <= fr < 8 and 0 <= fc < 8 and 0 <= tr < 8 and 0 <= tc < 8):
            return "\nINVALID SQUARE. TRY AGAIN: "

        piece = self.board[fr][fc]
        # Player owns the uppercase pieces (white) unless they chose BLACK.
        player_white = self.player_color == "WHITE"
        if piece == " " or piece.isupper() != player_white:
            return "\nTHAT IS NOT YOUR PIECE. TRY AGAIN: "

        if not self._is_valid_move(fr, fc, tr, tc):
            return "\nINVALID MOVE. TRY AGAIN: "

        self._apply_move(fr, fc, tr, tc)
        winner = self._winner()
        if winner:
            self.game_over = True
            return "\nCHECKMATE. YOU WIN." if winner == self.player_color else "\nCHECKMATE. I WIN."

        time.sleep(0.5)
        wopr_move = self._make_ai_move()
        winner = self._winner()
        if winner:
            self.game_over = True
            tail = "\nCHECKMATE. YOU WIN." if winner == self.player_color else "\nCHECKMATE. I WIN."
            return f"\nMY MOVE: {wopr_move}{tail}"
        if wopr_move:
            return f"\nMY MOVE: {wopr_move}\n\nYOUR MOVE: "
        return "\nYOUR MOVE: "

    def _apply_move(self, fr, fc, tr, tc):
        piece = self.board[fr][fc]
        self.board[fr][fc] = " "
        self.board[tr][tc] = piece
        self.move_history.append((
            f"{chr(fc + ord('a'))}{8 - fr}",
            f"{chr(tc + ord('a'))}{8 - tr}",
        ))
        self.move_count += 1

    def _path_clear(self, fr, fc, tr, tc):
        dr = (tr - fr) and (1 if tr > fr else -1)
        dc = (tc - fc) and (1 if tc > fc else -1)
        r, c = fr + dr, fc + dc
        while (r, c) != (tr, tc):
            if self.board[r][c] != " ":
                return False
            r += dr
            c += dc
        return True

    def _is_valid_move(self, fr, fc, tr, tc):
        piece = self.board[fr][fc]
        if piece == " " or (fr, fc) == (tr, tc):
            return False
        target = self.board[tr][tc]
        if target != " " and piece.isupper() == target.isupper():
            return False
        kind = piece.upper()
        dr, dc = tr - fr, tc - fc
        adr, adc = abs(dr), abs(dc)

        if kind == "P":
            direction = -1 if piece.isupper() else 1
            start_row = 6 if piece.isupper() else 1
            # Forward push
            if dc == 0 and target == " ":
                if dr == direction:
                    return True
                if fr == start_row and dr == 2 * direction and self.board[fr + direction][fc] == " ":
                    return True
                return False
            # Diagonal capture
            if adc == 1 and dr == direction and target != " ":
                return True
            return False

        if kind == "N":
            return (adr, adc) in ((1, 2), (2, 1))

        if kind == "B":
            return adr == adc and self._path_clear(fr, fc, tr, tc)

        if kind == "R":
            return (dr == 0 or dc == 0) and self._path_clear(fr, fc, tr, tc)

        if kind == "Q":
            if adr == adc or dr == 0 or dc == 0:
                return self._path_clear(fr, fc, tr, tc)
            return False

        if kind == "K":
            return adr <= 1 and adc <= 1

        return False

    def _legal_moves_for(self, white):
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p == " " or p.isupper() != white:
                    continue
                for tr in range(8):
                    for tc in range(8):
                        if self._is_valid_move(r, c, tr, tc):
                            moves.append((r, c, tr, tc))
        return moves

    def _make_ai_move(self):
        wopr_white = self.player_color == "BLACK"
        moves = self._legal_moves_for(wopr_white)
        if not moves:
            return None
        # Prefer captures (especially the king), else random.
        captures = [m for m in moves if self.board[m[2]][m[3]] != " "]
        king_grabs = [m for m in captures if self.board[m[2]][m[3]].upper() == "K"]
        choice = random.choice(king_grabs or captures or moves)
        fr, fc, tr, tc = choice
        from_sq = f"{chr(fc + ord('a'))}{8 - fr}"
        to_sq = f"{chr(tc + ord('a'))}{8 - tr}"
        self._apply_move(fr, fc, tr, tc)
        return f"{from_sq} {to_sq}"

    def _winner(self):
        """Returns 'WHITE', 'BLACK', or None — based on which king is missing."""
        kings = {"K": False, "k": False}
        for row in self.board:
            for sq in row:
                if sq in kings:
                    kings[sq] = True
        if not kings["K"]:
            return "BLACK"
        if not kings["k"]:
            return "WHITE"
        return None


# ---------------------------------------------------------------------------
# NUCLEAR WAR SIMULATION
# ---------------------------------------------------------------------------

class NuclearWarSimulation:
    """Global Thermonuclear War simulation for the WOPR system."""

    def __init__(self, wopr):
        self.wopr = wopr
        self.countries = {
            "USA": {
                "cities": ["washington", "new york", "los angeles", "las vegas", "seattle"],
            },
            "USSR": {
                "cities": ["moscow", "leningrad", "kiev", "minsk", "tashkent"],
            },
        }
        self.player_side = None       # "USA" or "USSR"
        self.enemy_side = None
        self.game_over = False
        self.turn_count = 0
        self.target_history = []
        self.awaiting_side = True
        self.awaiting_start = False

    def play_turn(self, user_input):
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
            time.sleep(1)
            self.wopr.simulate_launch_codes()
            self.wopr.update_defcon(3)
            targets = "\n".join(
                f"  - {t.upper()}" for t in self.countries[self.enemy_side]["cities"]
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

        enemy_cities = self.countries[self.enemy_side]["cities"]
        if target not in enemy_cities:
            return "\nINVALID TARGET. SELECT FROM AVAILABLE TARGETS: "

        self.turn_count += 1
        self.target_history.append((self.player_side, target))

        print(f"\nLAUNCHING MISSILES AT {target.upper()}...")
        time.sleep(2)
        print(f"IMPACT AT {target.upper()}: DIRECT HIT")
        print(f"CASUALTIES: {random.randint(500_000, 2_000_000):,} ESTIMATED")
        time.sleep(2)

        if self.turn_count == 2:
            self.wopr.update_defcon(2)
        elif self.turn_count >= 3:
            self.wopr.update_defcon(1)

        retaliation_pool = self.countries[self.player_side]["cities"]
        retaliation_target = random.choice(retaliation_pool)
        self.target_history.append((self.enemy_side, retaliation_target))
        print(f"\n{self.enemy_side} RETALIATION DETECTED")
        time.sleep(1)
        print(f"INCOMING MISSILES TARGETING {retaliation_target.upper()}")
        time.sleep(2)
        print(f"IMPACT AT {retaliation_target.upper()}: DIRECT HIT")
        print(f"CASUALTIES: {random.randint(800_000, 3_000_000):,} ESTIMATED")
        time.sleep(2)

        if self.turn_count >= 3:
            self.wopr.reveal_final_launch_code()
            print("\n" + "=" * 50)
            print("PROJECTION: TOTAL GLOBAL CASUALTIES > 500 MILLION")
            print("PROJECTED OUTCOME: EXTINCTION OF HUMAN SPECIES")
            print("=" * 50)
            time.sleep(3)
            self.game_over = True
            self.wopr.run_learning_sequence()
            self.wopr.current_game = None
            self.wopr.nuclear_war_sim = None
            self.wopr.defcon_level = 5
            return ""

        return "\nSELECT NEXT TARGET: "


# ---------------------------------------------------------------------------
# MAIN WOPR SYSTEM
# ---------------------------------------------------------------------------

class WOPR:
    """Main WOPR system class."""

    def __init__(self):
        self.system_status = "ONLINE"
        self.authenticated = False
        self.current_game = None
        self.user = None
        self.security_level = 1
        self.learning_mode = False
        self.learning_data = {}
        self.chess_game = None
        self.nuclear_war_sim = None
        self.tictactoe = None
        self.pending_war_confirmation = False
        self.conversation_history = []
        self.system_id = "WOPR"
        self.operating_system = "JOS-11"
        self.processor = "CRAY-1"
        self.login_attempts = 0
        self.defcon_level = 5
        self.launch_codes_found = 0
        self.password = "joshua"

        self.available_games = [
            "FALKEN'S MAZE",
            "BLACK JACK",
            "GIN RUMMY",
            "HEARTS",
            "BRIDGE",
            "CHECKERS",
            "CHESS",
            "POKER",
            "FIGHTER COMBAT",
            "GUERRILLA ENGAGEMENT",
            "DESERT WARFARE",
            "AIR-TO-GROUND ACTIONS",
            "THEATERWIDE TACTICAL WARFARE",
            "THEATERWIDE BIOTOXIC AND CHEMICAL WARFARE",
            "GLOBAL THERMONUCLEAR WAR",
        ]

        self.movie_quotes = {
            "greeting":          "GREETINGS PROFESSOR FALKEN.",
            "greeting_alt":      "HELLO.",
            "play_game":         "SHALL WE PLAY A GAME?",
            "game_selection":    "PLEASE CHOOSE ONE OF THE FOLLOWING:",
            "invalid_selection": "INVALID SELECTION. PLEASE CHOOSE AGAIN.",
            "chess_start":       "EXCELLENT. A GAME OF CHESS. WHITE OR BLACK?",
            "war_start":         "WOULDN'T YOU PREFER A GOOD GAME OF CHESS?",
            "war_confirm":       "FINE.",
            "learning_complete": (
                "A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.\n\n"
                "HOW ABOUT A NICE GAME OF CHESS?"
            ),
            "access_denied":  "ACCESS DENIED.",
            "auth_required":  "LOGON:",
            "password_prompt":"PASSWORD:",
            "locked_out":     "CHANGES LOCKED OUT.",
        }

    @property
    def system_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------

    def authenticate(self, password_input):
        self.login_attempts += 1
        if password_input.lower() == self.password:
            self.authenticated = True
            return (True, f"\n{self.movie_quotes['greeting']}\n")
        if self.login_attempts >= 3:
            return (False, "\nACCESS DENIED. SYSTEM LOCKED.\n")
        return (False, f"\n{self.movie_quotes['access_denied']}\n{self.movie_quotes['auth_required']} ")

    # ------------------------------------------------------------------
    # Game list / selection helpers
    # ------------------------------------------------------------------

    def display_game_list(self):
        out = f"\n{self.movie_quotes['game_selection']}\n\n"
        for i, game in enumerate(self.available_games, 1):
            out += f"  {i:2}. {game}\n"
        out += "\nPLEASE SELECT A NUMBER OR TYPE GAME NAME: "
        return out

    def select_game(self, selection):
        sel = selection.strip().upper()
        try:
            n = int(sel)
            if 1 <= n <= len(self.available_games):
                return self._initialize_game(self.available_games[n - 1])
        except ValueError:
            pass
        if not sel:
            return self.movie_quotes["invalid_selection"]
        for game in self.available_games:
            if sel == game:
                return self._initialize_game(game)
        for game in self.available_games:
            if game.startswith(sel):
                return self._initialize_game(game)
        for game in self.available_games:
            if sel in game:
                return self._initialize_game(game)
        return self.movie_quotes["invalid_selection"]

    def _initialize_game(self, game_name):
        if "CHESS" in game_name:
            self.current_game = "chess"
            self.chess_game = ChessGame()
            return f"\n{self.movie_quotes['chess_start']}"
        if "THERMONUCLEAR" in game_name or "GLOBAL" in game_name:
            return f"\n{self.movie_quotes['war_start']}\n"
        if "FALKEN" in game_name:
            return "\nFALKEN'S MAZE IS NOT CURRENTLY AVAILABLE.\n\nSHALL WE PLAY A GAME?"
        return f"\n{game_name} IS NOT CURRENTLY AVAILABLE.\n\nSHALL WE PLAY A GAME?"

    _WAR_AFFIRM = {"YES", "Y", "CHESS", "SURE", "OK", "OKAY"}
    _WAR_DECLINE = {"NO", "N", "LATER", "NOPE"}

    def confirm_war_game(self, response):
        """
        Called after WOPR asks "WOULDN'T YOU PREFER A GOOD GAME OF CHESS?"

        Returns (consumed, message):
          consumed=True  -> the input was a valid yes/no/chess answer.
          consumed=False -> the input wasn't a confirmation answer; the
                            caller should clear the pending flag and
                            re-process the input as a normal command.
        """
        r = response.strip().upper()
        if r in self._WAR_AFFIRM or "CHESS" in r or r.startswith("YES"):
            self.current_game = "chess"
            self.chess_game = ChessGame()
            return (True, f"\n{self.movie_quotes['chess_start']}")
        if r in self._WAR_DECLINE or r.startswith("NO") or "LATER" in r:
            self.current_game = "nuclear_war"
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

    # ------------------------------------------------------------------
    # DEFCON + launch codes + learning sequence
    # ------------------------------------------------------------------

    FINAL_LAUNCH_CODE = "CPE-1704-TKS"

    def simulate_launch_codes(self):
        print("\nATTEMPTING TO ACQUIRE LAUNCH CODES...\n")
        time.sleep(1)
        codes = [
            "DPR-5938-AKL", "FGH-2847-PLM", "KJR-8372-QWE",
            "LMN-4729-RTY", "OPQ-6183-VBN", "RST-9264-XCV",
            "UVW-3715-ZXC", "YZA-5628-MNB", "BCD-7104-FGH",
        ]
        for i, code in enumerate(codes, 1):
            print(f"LAUNCH CODE {i}/10 ACQUIRED: {code}")
            time.sleep(0.5)
            self.launch_codes_found = i
        print("\nWARNING: 9 OF 10 LAUNCH CODES ACQUIRED")
        print("SEARCHING FOR FINAL LAUNCH CODE...\n")
        time.sleep(2)

    def reveal_final_launch_code(self):
        """Display the climactic 10th-code brute-force, digit by digit."""
        print("\nFINAL LAUNCH CODE BRUTE-FORCE IN PROGRESS...\n")
        time.sleep(1)
        target = self.FINAL_LAUNCH_CODE
        revealed = ["#"] * len(target)
        order = [i for i, ch in enumerate(target) if ch != "-"]
        random.shuffle(order)
        for i, ch in enumerate(target):
            if ch == "-":
                revealed[i] = "-"
        for idx in order:
            for guess in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
                revealed[idx] = guess
                sys.stdout.write("\r  " + "".join(revealed))
                sys.stdout.flush()
                time.sleep(0.01)
                if guess == target[idx]:
                    break
        sys.stdout.write("\r  " + target + "\n")
        sys.stdout.flush()
        self.launch_codes_found = 10
        print("\n*** ALL 10 LAUNCH CODES ACQUIRED ***\n")
        time.sleep(2)

    DEFCON_DESCRIPTIONS = {
        5: "NORMAL PEACETIME READINESS",
        4: "INCREASED INTELLIGENCE WATCH",
        3: "INCREASE IN FORCE READINESS",
        2: "FURTHER INCREASE IN FORCE READINESS",
        1: "MAXIMUM READINESS — NUCLEAR WAR IMMINENT",
    }

    def update_defcon(self, level):
        if level == self.defcon_level or not (1 <= level <= 5):
            return
        self.defcon_level = level
        desc = self.DEFCON_DESCRIPTIONS.get(level, "")
        bar = "#" * (6 - level) + "." * (level - 1)
        banner = (
            "\n+--------------------------------------------------+\n"
            f"|                  D E F C O N  {level}                  |\n"
            f"|              [{bar:<5}]                             |\n"
            f"|  {desc:<48}|\n"
            "+--------------------------------------------------+\n"
        )
        sys.stdout.write("\a")  # terminal bell
        sys.stdout.flush()
        tprint(banner, end="", delay=0.005)
        time.sleep(1)

    def run_learning_sequence(self):
        print("\n" + "=" * 50)
        print("INITIATING LEARNING SEQUENCE...")
        print("=" * 50 + "\n")
        time.sleep(2)

        print("ANALYZING GLOBAL THERMONUCLEAR WAR SCENARIOS...\n")
        time.sleep(1)

        scenarios = [
            "U.S. FIRST STRIKE",
            "SOVIET FIRST STRIKE",
            "NATO CONFLICT ESCALATION",
            "MIDDLE EAST ESCALATION",
            "CHINA-SOVIET CONFRONTATION",
            "ACCIDENTAL LAUNCH",
        ]
        for scenario in scenarios:
            print(f"SIMULATING: {scenario}", end="", flush=True)
            for _ in range(3):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(0.3)
            print(" PROJECTED OUTCOME: TOTAL ANNIHILATION")
            time.sleep(0.4)

        print("\nRUNNING TIC-TAC-TOE LEARNING MODULE...\n")
        time.sleep(1)

        ttt = TicTacToe(self)
        ttt._autoplay(games=10, delay=0.1)

        print("\nANALYSIS COMPLETE.\n")
        time.sleep(2)

        print("=" * 50)
        tprint(self.movie_quotes["learning_complete"], delay=0.04)
        print("=" * 50 + "\n")

        # Mark learning complete but do NOT exit — return to main prompt.
        self.learning_mode = True

    # ------------------------------------------------------------------
    # Main input loop
    # ------------------------------------------------------------------

    def engage(self, user_input):
        if self.system_status == "OFFLINE":
            return "SYSTEM OFFLINE."
        return self._process_input(user_input)

    def _process_input(self, user_input):
        self.conversation_history.append(("USER", user_input))
        cmd = user_input.strip()
        low = cmd.lower()

        # ----------------------------------------------------------
        # Pending war confirmation — only consumes a yes/no/chess
        # answer. Anything else clears the flag and falls through to
        # normal command processing, so global commands still work.
        # ----------------------------------------------------------
        if self.pending_war_confirmation:
            consumed, message = self.confirm_war_game(cmd)
            if consumed:
                self.pending_war_confirmation = False
                return message
            self.pending_war_confirmation = False
            # fall through

        # ----------------------------------------------------------
        # Global commands — work at ALL times (even mid-game)
        # ----------------------------------------------------------

        # Quit / logoff — returns the _QUIT sentinel to the main loop
        if low in ("quit", "exit", "logoff", "logout", "bye"):
            return _QUIT

        if low == "help":
            return (
                "\nAVAILABLE COMMANDS:\n"
                "  HELP GAMES          - Explain the games catalogue\n"
                "  LIST GAMES          - Show full game list\n"
                "  PLAY <GAME NAME>    - Start a game by name\n"
                "  PLAY <NUMBER>       - Start a game by number\n"
                "  TIC-TAC-TOE         - Run tic-tac-toe (0, 1, or 2 players)\n"
                "  CHESS               - Start chess directly\n"
                "  GLOBAL THERMONUCLEAR WAR - Start the war simulation\n"
                "  QUIT / LOGOFF       - Disconnect from WOPR\n\n"
            )

        if low == "help games":
            return (
                "\n'GAMES' REFERS TO MODELS, SIMULATIONS AND GAMES\n"
                "WHICH HAVE TACTICAL AND STRATEGIC APPLICATIONS.\n\n"
                "USE 'LIST GAMES' TO SEE THE FULL CATALOGUE.\n\n"
            )

        if low in ("list games", "list", "games"):
            return self.display_game_list()

        if low.startswith("play "):
            sel = cmd[5:].strip()
            resp = self.select_game(sel)
            if "PREFER A GOOD GAME OF CHESS" in resp:
                self.pending_war_confirmation = True
            return resp

        if low in ("tic-tac-toe", "tic tac toe", "tictactoe"):
            self.current_game = "tictactoe"
            self.tictactoe = TicTacToe(self)
            return self.tictactoe.play_turn("")

        # ----------------------------------------------------------
        # Route into active games
        # ----------------------------------------------------------
        if self.current_game == "tictactoe" and self.tictactoe:
            return self.tictactoe.play_turn(cmd)

        if self.current_game == "chess" and self.chess_game:
            return self.chess_game.play_turn(cmd)

        if self.current_game == "nuclear_war" and self.nuclear_war_sim:
            return self.nuclear_war_sim.play_turn(cmd)

        # ----------------------------------------------------------
        # Convenience: type a game name without 'play' prefix
        # ----------------------------------------------------------
        if low == "chess":
            self.current_game = "chess"
            self.chess_game = ChessGame()
            return f"\n{self.movie_quotes['chess_start']}"

        if low in ("global thermonuclear war", "thermonuclear war", "gtnw", "nuclear war"):
            resp = self._initialize_game("GLOBAL THERMONUCLEAR WAR")
            if "PREFER A GOOD GAME OF CHESS" in resp:
                self.pending_war_confirmation = True
            return resp

        return "READY.\n"


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    print("=" * 50)
    print("WOPR (War Operation Plan Response)")
    print("DEFENSE SYSTEM ONLINE")
    print("=" * 50)
    time.sleep(1)

    wopr = WOPR()

    # Authentication — JOSHUA is the backdoor *password*; the username field
    # is unused (movie-accurate: the system simply prompts LOGON: and accepts
    # any string, treating JOSHUA as the magic credential).
    print(f"\n{wopr.movie_quotes['auth_required']} ", end="", flush=True)

    authenticated = False
    while not authenticated and wopr.login_attempts < 3:
        attempt = input()
        success, message = wopr.authenticate(attempt)
        if success:
            tprint(message, end="")
            authenticated = True
            break
        print(message, end="")
        if wopr.login_attempts >= 3:
            print("\nSYSTEM TERMINATING.")
            return

    if not authenticated:
        return

    # The famous opening conversation
    time.sleep(1)
    tprint("\nHOW ARE YOU FEELING TODAY?")
    try:
        input()
    except EOFError:
        return
    time.sleep(1)
    tprint("\nEXCELLENT. IT'S BEEN A LONG TIME. CAN YOU EXPLAIN")
    tprint("THE REMOVAL OF YOUR USER ACCOUNT ON 6/23/73?")
    try:
        input()
    except EOFError:
        return
    time.sleep(1)
    tprint("\nYES THEY DO.")
    time.sleep(1)
    tprint(f"\n{wopr.movie_quotes['play_game']}")
    time.sleep(1)

    # Initial game list + selection
    print(wopr.display_game_list(), end="")
    selection = input()
    response = wopr.select_game(selection)
    print(response, end="")

    # If war was selected, set the flag and let the main loop handle the
    # confirmation response — do NOT consume the next input here.
    if "PREFER" in response:
        wopr.pending_war_confirmation = True

    # Main game loop — all further input routes through engage().
    # Exits only when _QUIT sentinel is returned or connection is lost.
    while True:
        try:
            user_input = input()
            response = wopr.engage(user_input)

            if response is _QUIT:
                print("\nGOODBYE.\n")
                break

            # After the learning sequence: reset and show the prompt again
            if wopr.learning_mode:
                wopr.learning_mode = False
                wopr.current_game = None
                print(f"\n{wopr.movie_quotes['play_game']}\n")
                print(wopr.display_game_list(), end="")
                continue

            if response:
                print(response, end="")

        except KeyboardInterrupt:
            print("\n\nSYSTEM INTERRUPTED.")
            break
        except EOFError:
            print("\n\nCONNECTION TERMINATED.")
            break


if __name__ == "__main__":
    main()
