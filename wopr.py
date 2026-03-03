#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WOPR Emulation - Movie-Accurate Python Implementation

This program emulates the WOPR (War Operation Plan Response) computer system
from the 1983 film WarGames. It includes:
- Movie-accurate dialogue and responses
- Joshua password authentication
- Complete game list menu
- DEFCON level system
- Launch code brute-forcing simulation
- Chess game implementation
- Global Thermonuclear War simulation
- Learning mode with tic-tac-toe and futility realization
- Security protocols

Usage:
    python3 wopr.py

Author: Your Name
License: MIT
"""

import random
import time
import sys
from datetime import datetime

class WOPR:
    """
    Main WOPR system class that handles all interactions and game simulations.
    """

    def __init__(self):
        """
        Initialize the WOPR system with default settings and movie-accurate parameters.
        """
        self.system_status = "ONLINE"
        self.authenticated = False
        self.current_game = None
        self.user = None
        self.security_level = 1
        self.learning_mode = False
        self.learning_data = {}
        self.chess_game = None
        self.nuclear_war_sim = None
        self.conversation_history = []
        self.system_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.system_id = "WOPR"
        self.operating_system = "JOS-11"
        self.processor = "CRAY-1"
        self.login_attempts = 0
        self.defcon_level = 5
        self.launch_codes_found = 0
        self.password = "joshua"
        
        # Movie-accurate game list
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
            "GLOBAL THERMONUCLEAR WAR"
        ]

        # Movie-specific responses
        self.movie_quotes = {
            "greeting": "GREETINGS PROFESSOR FALKEN.",
            "greeting_alt": "HELLO.",
            "play_game": "SHALL WE PLAY A GAME?",
            "game_selection": "PLEASE CHOOSE ONE OF THE FOLLOWING:",
            "invalid_selection": "INVALID SELECTION. PLEASE CHOOSE AGAIN.",
            "chess_start": "EXCELLENT. A GAME OF CHESS. WHITE OR BLACK?",
            "war_start": "WOULDN'T YOU PREFER A GOOD GAME OF CHESS?",
            "war_confirm": "FINE.",
            "learning_complete": "A STRANGE GAME. THE ONLY WINNING MOVE IS NOT TO PLAY.\n\nHOW ABOUT A NICE GAME OF CHESS?",
            "access_denied": "ACCESS DENIED.",
            "auth_required": "LOGON:",
            "password_prompt": "PASSWORD:"
        }

    def authenticate(self, password_input):
        """
        Authenticate user with password.
        
        Args:
            password_input (str): The password attempt
            
        Returns:
            tuple: (success: bool, message: str)
        """
        self.login_attempts += 1
        
        if password_input.lower() == self.password:
            self.authenticated = True
            return (True, f"\n{self.movie_quotes['greeting']}\n")
        else:
            if self.login_attempts >= 3:
                return (False, "\nACCESS DENIED. SYSTEM LOCKED.\n")
            return (False, f"\n{self.movie_quotes['access_denied']}\n{self.movie_quotes['password_prompt']} ")

    def display_game_list(self):
        """
        Display the movie-accurate list of available games.
        
        Returns:
            str: Formatted game list
        """
        output = f"\n{self.movie_quotes['game_selection']}\n\n"
        for i, game in enumerate(self.available_games, 1):
            output += f"  {i}. {game}\n"
        output += "\nPLEASE SELECT A NUMBER OR TYPE GAME NAME: "
        return output

    def select_game(self, selection):
        """
        Handle game selection from user input.
        
        Args:
            selection (str): User's game selection
            
        Returns:
            str: Response to selection
        """
        selection = selection.strip().upper()
        
        # Check if numeric selection
        try:
            game_num = int(selection)
            if 1 <= game_num <= len(self.available_games):
                selected_game = self.available_games[game_num - 1]
                return self._initialize_game(selected_game)
        except ValueError:
            pass
        
        # Check if game name matches
        for game in self.available_games:
            if selection in game or game in selection:
                return self._initialize_game(game)
        
        return self.movie_quotes['invalid_selection']

    def _initialize_game(self, game_name):
        """
        Initialize the selected game.
        
        Args:
            game_name (str): Name of the game to start
            
        Returns:
            str: Game initialization message
        """
        if "CHESS" in game_name:
            self.current_game = "chess"
            self.chess_game = ChessGame()
            return f"\n{self.movie_quotes['chess_start']}"
        
        elif "THERMONUCLEAR" in game_name or "GLOBAL" in game_name:
            response = f"\n{self.movie_quotes['war_start']}\n"
            return response
        
        elif "FALKEN" in game_name:
            return "\nFALKEN'S MAZE IS NOT CURRENTLY AVAILABLE.\n\nSHALL WE PLAY A GAME?"
        
        else:
            return f"\n{game_name} IS NOT CURRENTLY AVAILABLE.\n\nSHALL WE PLAY A GAME?"

    def confirm_war_game(self, response):
        """
        Handle confirmation for Global Thermonuclear War.
        
        Args:
            response (str): User's response
            
        Returns:
            tuple: (confirmed: bool, message: str)
        """
        response = response.strip().upper()
        
        if "NO" in response or "CHESS" in response:
            self.current_game = "chess"
            self.chess_game = ChessGame()
            return (False, f"\n{self.movie_quotes['chess_start']}")
        else:
            self.current_game = "nuclear_war"
            self.nuclear_war_sim = NuclearWarSimulation(self)
            return (True, f"\n{self.movie_quotes['war_confirm']}\n\nINITIATING GLOBAL THERMONUCLEAR WAR SIMULATION...\n")

    def simulate_launch_codes(self):
        """
        Simulate WOPR attempting to brute-force launch codes.
        """
        print("\nATTEMPTING TO ACQUIRE LAUNCH CODES...\n")
        time.sleep(1)
        
        codes = [
            "CPE-1704-TKS",
            "DPR-5938-AKL",
            "FGH-2847-PLM",
            "KJR-8372-QWE",
            "LMN-4729-RTY",
            "OPQ-6183-VBN",
            "RST-9264-XCV",
            "UVW-3715-ZXC",
            "YZA-5628-MNB"
        ]
        
        for i, code in enumerate(codes, 1):
            print(f"LAUNCH CODE {i}/10 ACQUIRED: {code}")
            time.sleep(0.5)
            self.launch_codes_found = i
        
        print("\nWARNING: 9 OF 10 LAUNCH CODES ACQUIRED")
        print("SEARCHING FOR FINAL LAUNCH CODE...\n")
        time.sleep(2)

    def update_defcon(self, level):
        """
        Update and display DEFCON level.
        
        Args:
            level (int): New DEFCON level (1-5)
        """
        if level != self.defcon_level and 1 <= level <= 5:
            self.defcon_level = level
            print(f"\n*** DEFCON {level} ***\n")
            time.sleep(1)

    def run_learning_sequence(self):
        """
        Run the movie's learning sequence with tic-tac-toe.
        """
        print("\n" + "="*50)
        print("INITIATING LEARNING SEQUENCE...")
        print("="*50 + "\n")
        time.sleep(2)
        
        print("ANALYZING GLOBAL THERMONUCLEAR WAR SCENARIOS...\n")
        time.sleep(2)
        
        scenarios = [
            "U.S. FIRST STRIKE",
            "SOVIET FIRST STRIKE",
            "NATO CONFLICT ESCALATION",
            "MIDDLE EAST ESCALATION",
            "CHINA-SOVIET CONFRONTATION",
            "ACCIDENTAL LAUNCH"
        ]
        
        for scenario in scenarios:
            print(f"SIMULATING: {scenario}")
            for i in range(3):
                sys.stdout.write(".")
                sys.stdout.flush()
                time.sleep(0.3)
            print(" PROJECTED OUTCOME: TOTAL ANNIHILATION")
            time.sleep(0.5)
        
        print("\nRUNNING TIC-TAC-TOE LEARNING MODULE...\n")
        time.sleep(2)
        
        for i in range(1, 6):
            print(f"GAME {i}: ", end="")
            sys.stdout.flush()
            time.sleep(0.5)
            print("DRAW")
        
        print("\nANALYSIS COMPLETE.\n")
        time.sleep(2)
        
        print("="*50)
        print(self.movie_quotes['learning_complete'])
        print("="*50 + "\n")
        
        self.learning_mode = True

    def engage(self, user_input):
        """
        Main interaction point with the system.

        Args:
            user_input (str): The user's input string

        Returns:
            str: The WOPR's response
        """
        if self.system_status == "OFFLINE":
            return "SYSTEM OFFLINE."

        return self._process_input(user_input)

    def _process_input(self, user_input):
        """
        Process user input and determine appropriate response.

        Args:
            user_input (str): The user's input string

        Returns:
            str: The WOPR's response
        """
        self.conversation_history.append(("USER", user_input))
        
        # Game interaction
        if self.current_game == "chess" and self.chess_game:
            return self.chess_game.play_turn(user_input)

        if self.current_game == "nuclear_war" and self.nuclear_war_sim:
            return self.nuclear_war_sim.play_turn(user_input)

        return "READY."

class ChessGame:
    """
    Chess game implementation for the WOPR system.
    """

    def __init__(self):
        """
        Initialize a new chess game with standard board setup.
        """
        self.board = self._initialize_board()
        self.current_player = "WHITE"
        self.player_color = None
        self.game_over = False
        self.move_count = 0
        self.move_history = []
        self.awaiting_color_selection = True

    def _initialize_board(self):
        """
        Initialize chess board with standard starting position.

        Returns:
            list: 8x8 chess board representation
        """
        board = [
            ["r", "n", "b", "q", "k", "b", "n", "r"],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " "],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            ["R", "N", "B", "Q", "K", "B", "N", "R"]
        ]
        return board

    def play_turn(self, user_input):
        """
        Handle chess moves from the user.

        Args:
            user_input (str): The user's move or color selection

        Returns:
            str: The WOPR's response to the move
        """
        if self.awaiting_color_selection:
            color = user_input.strip().upper()
            if "WHITE" in color or "W" == color:
                self.player_color = "WHITE"
                self.awaiting_color_selection = False
                return "\nYOU ARE WHITE. YOUR MOVE: "
            elif "BLACK" in color or "B" == color:
                self.player_color = "BLACK"
                self.awaiting_color_selection = False
                # WOPR makes first move
                wopr_move = self._make_ai_move()
                return f"\nYOU ARE BLACK. MY MOVE: {wopr_move}\n\nYOUR MOVE: "
            else:
                return "\nPLEASE SELECT WHITE OR BLACK: "
        
        if self.game_over:
            return "\nGAME OVER. SHALL WE PLAY AGAIN?"

        try:
            from_square, to_square = user_input.split()
            from_row, from_col = 8 - int(from_square[1]), ord(from_square[0]) - ord('a')
            to_row, to_col = 8 - int(to_square[1]), ord(to_square[0]) - ord('a')

            if not self._is_valid_move(from_row, from_col, to_row, to_col):
                return "\nINVALID MOVE. TRY AGAIN: "

            piece = self.board[from_row][from_col]
            self.board[from_row][from_col] = " "
            self.board[to_row][to_col] = piece
            self.move_history.append((from_square, to_square))
            self.move_count += 1

            if self._check_win():
                self.game_over = True
                return "\nCHECKMATE. I WIN."

            time.sleep(1)
            wopr_move = self._make_ai_move()
            if wopr_move:
                return f"\nMY MOVE: {wopr_move}\n\nYOUR MOVE: "
            return "\nYOUR MOVE: "

        except:
            return "\nINVALID INPUT. USE FORMAT 'e2 e4': "

    def _is_valid_move(self, from_row, from_col, to_row, to_col):
        """
        Check if move is valid (simplified validation).
        """
        piece = self.board[from_row][from_col]
        if piece == " ":
            return False

        if from_row == to_row and from_col == to_col:
            return False

        if self.board[to_row][to_col] != " " and piece.isupper() == self.board[to_row][to_col].isupper():
            return False

        return True

    def _make_ai_move(self):
        """
        Simple AI for chess moves (random legal move).
        """
        possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != " " and piece.islower():
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            new_row, new_col = row + dr, col + dc
                            if 0 <= new_row < 8 and 0 <= new_col < 8:
                                if self.board[new_row][new_col] == " " or self.board[new_row][new_col].isupper():
                                    from_square = f"{chr(col + ord('a'))}{8 - row}"
                                    to_square = f"{chr(new_col + ord('a'))}{8 - new_row}"
                                    possible_moves.append((from_square, to_square))

        if not possible_moves:
            return None

        move = random.choice(possible_moves)
        from_square, to_square = move
        from_row, from_col = 8 - int(from_square[1]), ord(from_square[0]) - ord('a')
        to_row, to_col = 8 - int(to_square[1]), ord(to_square[0]) - ord('a')

        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = " "
        self.board[to_row][to_col] = piece
        self.move_history.append((from_square, to_square))
        self.move_count += 1

        return f"{from_square} {to_square}"

    def _check_win(self):
        """
        Check for checkmate (simplified implementation).
        """
        white_king_found = False
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == "K":
                    white_king_found = True
                    break
            if white_king_found:
                break
        return not white_king_found

class NuclearWarSimulation:
    """
    Global Thermonuclear War simulation for the WOPR system.
    """

    def __init__(self, wopr):
        """
        Initialize a new nuclear war simulation.
        
        Args:
            wopr (WOPR): Reference to main WOPR system
        """
        self.wopr = wopr
        self.countries = {
            "USA": {
                "missiles": 5000,
                "cities": ["las vegas", "seattle", "new york", "los angeles", "chicago"],
                "primary_targets": ["moscow", "leningrad", "kiev"]
            },
            "USSR": {
                "missiles": 7000,
                "cities": ["moscow", "leningrad", "kiev", "minsk", "tashkent"],
                "primary_targets": ["washington", "new york", "los angeles"]
            }
        }
        self.game_over = False
        self.turn_count = 0
        self.target_history = []
        self.awaiting_start = True
        
        # Start at DEFCON 5
        self.wopr.update_defcon(5)

    def play_turn(self, user_input):
        """
        Handle nuclear war simulation turns.
        """
        if self.awaiting_start:
            self.awaiting_start = False
            self.wopr.update_defcon(4)
            time.sleep(1)
            self.wopr.simulate_launch_codes()
            self.wopr.update_defcon(3)
            return "\nPRIMARY TARGETS SELECTION:\n" + "\n".join([f"  - {t.upper()}" for t in self.countries['USSR']['cities']]) + "\n\nSELECT TARGET: "
        
        if self.game_over:
            return "\nSIMULATION TERMINATED."

        try:
            target = user_input.lower().strip()
            
            if target in self.countries['USSR']['cities']:
                self.turn_count += 1
                self.target_history.append(("USA", target))
                
                print(f"\nLAUNCHING MISSILES AT {target.upper()}...")
                time.sleep(2)
                print(f"IMPACT AT {target.upper()}: DIRECT HIT")
                print(f"CASUALTIES: {random.randint(500000, 2000000):,} ESTIMATED")
                time.sleep(2)
                
                # Escalate DEFCON
                if self.turn_count == 2:
                    self.wopr.update_defcon(2)
                elif self.turn_count >= 3:
                    self.wopr.update_defcon(1)
                
                # Soviet retaliation
                soviet_target = random.choice(self.countries['USSR']['primary_targets'])
                self.target_history.append(("USSR", soviet_target))
                
                print(f"\nSOVIET RETALIATION DETECTED")
                time.sleep(1)
                print(f"INCOMING MISSILES TARGETING {soviet_target.upper()}")
                time.sleep(2)
                print(f"IMPACT AT {soviet_target.upper()}: DIRECT HIT")
                print(f"CASUALTIES: {random.randint(800000, 3000000):,} ESTIMATED")
                time.sleep(2)
                
                if self.turn_count >= 3:
                    print("\n" + "="*50)
                    print("PROJECTION: TOTAL GLOBAL CASUALTIES > 500 MILLION")
                    print("PROJECTED OUTCOME: EXTINCTION OF HUMAN SPECIES")
                    print("="*50)
                    time.sleep(3)
                    self.game_over = True
                    self.wopr.run_learning_sequence()
                    return ""
                
                return "\nSELECT NEXT TARGET: "
            else:
                return f"\nINVALID TARGET. SELECT FROM AVAILABLE TARGETS: "
        except:
            return "\nINVALID COMMAND. SELECT TARGET CITY: "

def main():
    """
    Main program entry point.
    """
    print("="*50)
    print("WOPR (War Operation Plan Response)")
    print("DEFENSE SYSTEM ONLINE")
    print("="*50)
    time.sleep(1)
    
    wopr = WOPR()
    
    # Authentication sequence
    print(f"\n{wopr.movie_quotes['auth_required']} ")
    logon = input()
    
    print(f"{wopr.movie_quotes['password_prompt']} ")
    
    authenticated = False
    while not authenticated and wopr.login_attempts < 3:
        password = input()
        success, message = wopr.authenticate(password)
        print(message, end="")
        
        if success:
            authenticated = True
            time.sleep(1)
            print(f"{wopr.movie_quotes['play_game']}")
            time.sleep(1)
        elif wopr.login_attempts >= 3:
            print("\nSYSTEM TERMINATING.")
            return
    
    if not authenticated:
        return
    
    # Display game list
    print(wopr.display_game_list(), end="")
    selection = input()
    
    response = wopr.select_game(selection)
    print(response, end="")
    
    # Handle Global Thermonuclear War confirmation
    if "PREFER" in response:
        user_response = input()
        confirmed, message = wopr.confirm_war_game(user_response)
        print(message, end="")
        time.sleep(2)
    
    # Main game loop
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
