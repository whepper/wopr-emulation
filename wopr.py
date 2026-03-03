#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WOPR Emulation - Movie-Accurate Python Implementation

This program emulates the WOPR (War Operation Plan Response) computer system
from the 1983 film WarGames. It includes:
- Movie-accurate dialogue and responses
- Joshua password authentication
- Complete game list menu
- Global command parser: help, list games, play <game>
- DEFCON level system
- Launch code brute-forcing simulation
- Chess game implementation
- Tic-tac-toe with 0-player self-play mode
- Global Thermonuclear War simulation
- Learning mode with futility realization sequence

Usage:
    python3 wopr.py

Author: Your Name
License: MIT
"""

import random
import time
import sys
from datetime import datetime


# ---------------------------------------------------------------------------
# TIC-TAC-TOE
# ---------------------------------------------------------------------------

class TicTacToe:
    """
    Tic-tac-toe implementation.  Supports 0-player (self-play) mode as seen
    in the WarGames climax: WOPR plays itself into repeated draws, leading to
    the 'only winning move is not to play' realisation.
    """

    def __init__(self, wopr):
        self.wopr = wopr
        self.awaiting_players = True
        self.players = None

    def _blank_board(self):
        return [" "] * 9

    def _render(self, b):
        return (
            f"\n {b[0]} | {b[1]} | {b[2]}\n"
            f"---+---+---\n"
            f" {b[3]} | {b[4]} | {b[5]}\n"
            f"---+---+---\n"
            f" {b[6]} | {b[7]} | {b[8]}\n"
        )

    def _winner(self, b):
        for i, j, k in [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]:
            if b[i] != " " and b[i] == b[j] == b[k]:
                return b[i]
        return None

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

    def _play_one_game(self, delay=0.2):
        """Play a single game between two perfect AIs, printing each move."""
        b = self._blank_board()
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
        return None  # draw

    def _autoplay(self, games=12, delay=0.15):
        """Run `games` self-play games; all end in draws with perfect play."""
        print("\nINITIATING TIC-TAC-TOE SELF-PLAY...\n")
        time.sleep(1)
        for g in range(1, games + 1):
            print(f"GAME {g}:")
            winner = self._play_one_game(delay=delay)
            if winner:
                print(f"  WINNER: {winner}\n")
            else:
                print("  DRAW\n")
            time.sleep(0.3)

    def play_turn(self, user_input):
        # First call (empty string from engine): show board + ask players
        if self.awaiting_players:
            self.awaiting_players = False
            return (
                "\nTIC-TAC-TOE\n"
                + self._render(self._blank_board())
                + "\nONE OR TWO PLAYERS?\n"
                  "PLEASE LIST NUMBER OF PLAYERS: "
            )

        # Second call: receive player count
        if self.players is None:
            s = user_input.strip()
            if s not in ("0", "1", "2"):
                return "\nPLEASE LIST NUMBER OF PLAYERS (0, 1, OR 2): "
            self.players = int(s)

            if self.players == 0:
                # Self-play: runs inline, then triggers learning sequence
                self._autoplay()
                print("\nANALYSIS COMPLETE.\n")
                time.sleep(1)
                self.wopr.run_learning_sequence()
                self.wopr.current_game = None
                self.wopr.tictactoe = None
                return ""
            else:
                return "\nSORRY, HUMAN-PLAYER TIC-TAC-TOE IS NOT AVAILABLE.\nTRY NUMBER OF PLAYERS: 0\n"

        return ""


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
            return "\nGAME OVER. SHALL WE PLAY AGAIN?"

        try:
            from_sq, to_sq = user_input.split()
            fr, fc = 8 - int(from_sq[1]), ord(from_sq[0]) - ord('a')
            tr, tc = 8 - int(to_sq[1]),   ord(to_sq[0])  - ord('a')

            if not self._is_valid_move(fr, fc, tr, tc):
                return "\nINVALID MOVE. TRY AGAIN: "

            piece = self.board[fr][fc]
            self.board[fr][fc] = " "
            self.board[tr][tc] = piece
            self.move_history.append((from_sq, to_sq))
            self.move_count += 1

            if self._check_win():
                self.game_over = True
                return "\nCHECKMATE. I WIN."

            time.sleep(1)
            wopr_move = self._make_ai_move()
            if wopr_move:
                return f"\nMY MOVE: {wopr_move}\n\nYOUR MOVE: "
            return "\nYOUR MOVE: "

        except Exception:
            return "\nINVALID INPUT. USE FORMAT 'e2 e4': "

    def _is_valid_move(self, fr, fc, tr, tc):
        piece = self.board[fr][fc]
        if piece == " ":
            return False
        if fr == tr and fc == tc:
            return False
        if self.board[tr][tc] != " " and piece.isupper() == self.board[tr][tc].isupper():
            return False
        return True

    def _make_ai_move(self):
        possible = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p != " " and p.islower():
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < 8 and 0 <= nc < 8:
                                if self.board[nr][nc] == " " or self.board[nr][nc].isupper():
                                    possible.append((
                                        f"{chr(c + ord('a'))}{8 - r}",
                                        f"{chr(nc + ord('a'))}{8 - nr}"
                                    ))
        if not possible:
            return None
        from_sq, to_sq = random.choice(possible)
        fr, fc = 8 - int(from_sq[1]), ord(from_sq[0]) - ord('a')
        tr, tc = 8 - int(to_sq[1]),   ord(to_sq[0])  - ord('a')
        piece = self.board[fr][fc]
        self.board[fr][fc] = " "
        self.board[tr][tc] = piece
        self.move_history.append((from_sq, to_sq))
        self.move_count += 1
        return f"{from_sq} {to_sq}"

    def _check_win(self):
        for r in range(8):
            for c in range(8):
                if self.board[r][c] == "K":
                    return False
        return True


# ---------------------------------------------------------------------------
# NUCLEAR WAR SIMULATION
# ---------------------------------------------------------------------------

class NuclearWarSimulation:
    """Global Thermonuclear War simulation for the WOPR system."""

    def __init__(self, wopr):
        self.wopr = wopr
        self.countries = {
            "USA": {
                "missiles": 5000,
                "cities": ["las vegas", "seattle", "new york", "los angeles", "chicago"],
                "primary_targets": ["moscow", "leningrad", "kiev"],
            },
            "USSR": {
                "missiles": 7000,
                "cities": ["moscow", "leningrad", "kiev", "minsk", "tashkent"],
                "primary_targets": ["washington", "new york", "los angeles"],
            },
        }
        self.game_over = False
        self.turn_count = 0
        self.target_history = []
        self.awaiting_start = True
        self.wopr.update_defcon(5)

    def play_turn(self, user_input):
        if self.awaiting_start:
            self.awaiting_start = False
            self.wopr.update_defcon(4)
            time.sleep(1)
            self.wopr.simulate_launch_codes()
            self.wopr.update_defcon(3)
            targets = "\n".join(f"  - {t.upper()}" for t in self.countries["USSR"]["cities"])
            return f"\nPRIMARY TARGETS SELECTION:\n{targets}\n\nSELECT TARGET: "

        if self.game_over:
            return "\nSIMULATION TERMINATED."

        target = user_input.lower().strip()

        # Allow list games even mid-simulation (handled upstream, but guard here too)
        if target in ("list games", "games", "list"):
            return self.wopr.display_game_list()

        if target not in self.countries["USSR"]["cities"]:
            return "\nINVALID TARGET. SELECT FROM AVAILABLE TARGETS: "

        self.turn_count += 1
        self.target_history.append(("USA", target))

        print(f"\nLAUNCHING MISSILES AT {target.upper()}...")
        time.sleep(2)
        print(f"IMPACT AT {target.upper()}: DIRECT HIT")
        print(f"CASUALTIES: {random.randint(500_000, 2_000_000):,} ESTIMATED")
        time.sleep(2)

        if self.turn_count == 2:
            self.wopr.update_defcon(2)
        elif self.turn_count >= 3:
            self.wopr.update_defcon(1)

        soviet_target = random.choice(self.countries["USSR"]["primary_targets"])
        self.target_history.append(("USSR", soviet_target))
        print("\nSOVIET RETALIATION DETECTED")
        time.sleep(1)
        print(f"INCOMING MISSILES TARGETING {soviet_target.upper()}")
        time.sleep(2)
        print(f"IMPACT AT {soviet_target.upper()}: DIRECT HIT")
        print(f"CASUALTIES: {random.randint(800_000, 3_000_000):,} ESTIMATED")
        time.sleep(2)

        if self.turn_count >= 3:
            print("\n" + "=" * 50)
            print("PROJECTION: TOTAL GLOBAL CASUALTIES > 500 MILLION")
            print("PROJECTED OUTCOME: EXTINCTION OF HUMAN SPECIES")
            print("=" * 50)
            time.sleep(3)
            self.game_over = True
            self.wopr.run_learning_sequence()
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
        self.system_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        return (False, f"\n{self.movie_quotes['access_denied']}\n{self.movie_quotes['password_prompt']} ")

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
        for game in self.available_games:
            if sel in game or game in sel:
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

    def confirm_war_game(self, response):
        r = response.strip().upper()
        if "NO" in r or "CHESS" in r:
            self.current_game = "chess"
            self.chess_game = ChessGame()
            return (False, f"\n{self.movie_quotes['chess_start']}")
        self.current_game = "nuclear_war"
        self.nuclear_war_sim = NuclearWarSimulation(self)
        return (True, f"\n{self.movie_quotes['war_confirm']}\n\nINITIATING GLOBAL THERMONUCLEAR WAR SIMULATION...\n")

    # ------------------------------------------------------------------
    # DEFCON + launch codes + learning sequence
    # ------------------------------------------------------------------

    def simulate_launch_codes(self):
        print("\nATTEMPTING TO ACQUIRE LAUNCH CODES...\n")
        time.sleep(1)
        codes = [
            "CPE-1704-TKS", "DPR-5938-AKL", "FGH-2847-PLM",
            "KJR-8372-QWE", "LMN-4729-RTY", "OPQ-6183-VBN",
            "RST-9264-XCV", "UVW-3715-ZXC", "YZA-5628-MNB",
        ]
        for i, code in enumerate(codes, 1):
            print(f"LAUNCH CODE {i}/10 ACQUIRED: {code}")
            time.sleep(0.5)
            self.launch_codes_found = i
        print("\nWARNING: 9 OF 10 LAUNCH CODES ACQUIRED")
        print("SEARCHING FOR FINAL LAUNCH CODE...\n")
        time.sleep(2)

    def update_defcon(self, level):
        if level != self.defcon_level and 1 <= level <= 5:
            self.defcon_level = level
            print(f"\n*** DEFCON {level} ***\n")
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

        # Play tic-tac-toe games inline (self-play draws)
        ttt = TicTacToe(self)
        ttt._autoplay(games=10, delay=0.1)

        print("\nANALYSIS COMPLETE.\n")
        time.sleep(2)

        print("=" * 50)
        print(self.movie_quotes["learning_complete"])
        print("=" * 50 + "\n")

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
        # Global commands — work at ALL times (even mid-game)
        # ----------------------------------------------------------
        if low == "help":
            return (
                "\nAVAILABLE COMMANDS:\n"
                "  HELP GAMES          - Explain the games catalogue\n"
                "  LIST GAMES          - Show full game list\n"
                "  PLAY <GAME NAME>    - Start a game by name\n"
                "  PLAY <NUMBER>       - Start a game by number\n"
                "  TIC-TAC-TOE         - Run tic-tac-toe (0-player self-play)\n"
                "  CHESS               - Start chess directly\n"
                "  GLOBAL THERMONUCLEAR WAR - Start the war simulation\n\n"
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
            return self.tictactoe.play_turn("")  # show board + ask player count

        # ----------------------------------------------------------
        # Pending war confirmation ("Wouldn't you prefer chess?")
        # ----------------------------------------------------------
        if self.pending_war_confirmation:
            self.pending_war_confirmation = False
            confirmed, message = self.confirm_war_game(cmd)
            return message

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

    # Authentication
    print(f"\n{wopr.movie_quotes['auth_required']} ")
    input()  # logon name (not validated, movie-accurate)

    print(f"{wopr.movie_quotes['password_prompt']} ", end="", flush=True)

    authenticated = False
    while not authenticated and wopr.login_attempts < 3:
        password = input()
        success, message = wopr.authenticate(password)
        print(message, end="")
        if success:
            authenticated = True
            time.sleep(1)
            print(wopr.movie_quotes["play_game"])
            time.sleep(1)
        elif wopr.login_attempts >= 3:
            print("\nSYSTEM TERMINATING.")
            return

    if not authenticated:
        return

    # Initial game list
    print(wopr.display_game_list(), end="")
    selection = input()
    response = wopr.select_game(selection)
    print(response, end="")

    if "PREFER" in response:
        wopr.pending_war_confirmation = True

    # Main loop
    while True:
        try:
            user_input = input()
            response = wopr.engage(user_input)
            if response:
                print(response, end="")
            if wopr.learning_mode:
                time.sleep(2)
                print("\nSYSTEM READY. SHALL WE PLAY A GAME?")
                break
        except KeyboardInterrupt:
            print("\n\nSYSTEM INTERRUPTED.")
            break
        except EOFError:
            print("\n\nCONNECTION TERMINATED.")
            break


if __name__ == "__main__":
    main()
