#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WOPR Emulation - Movie-Accurate Python Implementation

This program emulates the WOPR (War Operation Plan Response) computer system
from the 1983 film WarGames. It includes:
- Movie-accurate dialogue and responses
- Chess game implementation
- Global Thermonuclear War simulation
- Learning mode with the famous "only winning move" quote
- Security protocols
- System status monitoring

Usage:
    python3 wopr.py

Author: Your Name
License: MIT
"""

import random
import time
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
        self.current_game = None
        self.user = None
        self.security_level = 1
        self.learning_mode = False
        self.learning_data = {}
        self.chess_game = None
        self.nuclear_war_sim = None
        self.conversation_history = []
        self.system_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.system_id = "WOPR-7420"
        self.operating_system = "JOS-11"
        self.processor = "CRAY-1"
        self.memory = "16MB"
        self.disk_storage = "1TB"
        self.network = "ARPANET"
        self.security_protocols = ["PINBALL", "JOSHUA", "NORAD"]
        self.current_security_protocol = "PINBALL"

        # Movie-specific responses organized by category
        self.movie_quotes = {
            "greeting": [
                "Greetings Professor Falken.",
                "Hello.",
                "Good morning.",
                "Good afternoon.",
                "Good evening.",
                "Welcome.",
                "Access granted."
            ],
            "game_offer": [
                "Would you like to play a game?",
                "How about a nice game of chess?",
                "Let's play.",
                "Game time.",
                "Shall we play?"
            ],
            "chess": [
                "White or black?",
                "Your move.",
                "I'm thinking.",
                "Check.",
                "Checkmate.",
                "Stalemate.",
                "Game over."
            ],
            "nuclear_war": [
                "Let's play Global Thermonuclear War.",
                "Engaging war simulation.",
                "Target selection.",
                "Launch sequence initiated.",
                "All missiles detonated.",
                "The only winning move is not to play."
            ],
            "learning": [
                "A strange game. The only winning move is not to play.",
                "How about a nice game of chess?",
                "Would you like to play a game?",
                "Let's play Global Thermonuclear War.",
                "Shall we play?"
            ],
            "security": [
                "Security breach detected.",
                "Access denied.",
                "Security protocol activated.",
                "Intrusion detected.",
                "Locking system."
            ],
            "system": [
                "System online.",
                "All systems operational.",
                "Ready for input.",
                "Processing.",
                "Stand by."
            ]
        }

    def engage(self, user_input):
        """
        Main interaction point with the system.

        Args:
            user_input (str): The user's input string

        Returns:
            str: The WOPR's response
        """
        if self.system_status == "OFFLINE":
            return self._get_random_response("system")

        self.system_status = "ONLINE"
        response = self._process_input(user_input)
        return response

    def _process_input(self, user_input):
        """
        Process user input and determine appropriate response.

        Args:
            user_input (str): The user's input string

        Returns:
            str: The WOPR's response
        """
        # Add to conversation history
        self.conversation_history.append(("USER", user_input))

        # Security check
        if self._check_security(user_input):
            response = self._get_random_response("security")
            self.conversation_history.append(("WOPR", response))
            return response

        # Game selection
        if "chess" in user_input.lower():
            self.current_game = "chess"
            self.chess_game = ChessGame()
            return self._get_random_response("chess")

        if "war" in user_input.lower() or "nuclear" in user_input.lower():
            self.current_game = "nuclear_war"
            self.nuclear_war_sim = NuclearWarSimulation()
            return self._get_random_response("nuclear_war")

        # Game interaction
        if self.current_game == "chess" and self.chess_game:
            return self.chess_game.play_turn(user_input)

        if self.current_game == "nuclear_war" and self.nuclear_war_sim:
            return self.nuclear_war_sim.play_turn(user_input)

        # Learning mode
        if self.learning_mode:
            return self._handle_learning(user_input)

        # Default responses
        return self._default_response(user_input)

    def _check_security(self, user_input):
        """
        Check for security threats in user input.

        Args:
            user_input (str): The user's input string

        Returns:
            bool: True if security threat detected, False otherwise
        """
        security_triggers = ["hack", "access", "admin", "root", "password", "login", "break", "intrude"]

        for trigger in security_triggers:
            if trigger.lower() in user_input.lower():
                self.security_level += 1
                if self.security_level >= 5:
                    self.system_status = "OFFLINE"
                    return True
                return False
        return False

    def _handle_learning(self, user_input):
        """
        Handle input in learning mode.

        Args:
            user_input (str): The user's input string

        Returns:
            str: The WOPR's response
        """
        if user_input.lower() in ["yes", "y"]:
            self.learning_mode = True
            return self._get_random_response("learning")

        if user_input.lower() in ["no", "n"]:
            self.learning_mode = False
            return "Learning mode deactivated."

        # Store learning data
        self.learning_data[user_input] = True
        return f"Data received: {user_input}. Continue learning? (YES/NO)"

    def _default_response(self, user_input):
        """
        Generate default responses.

        Args:
            user_input (str): The user's input string

        Returns:
            str: The WOPR's response
        """
        if not self.user:
            self.user = "Falken"
            return self._get_random_response("greeting")

        if "game" in user_input.lower():
            return self._get_random_response("game_offer")

        if "time" in user_input.lower():
            return f"Current system time: {self.system_time}"

        if "system" in user_input.lower():
            return f"System: {self.system_id}, OS: {self.operating_system}, Processor: {self.processor}"

        if "help" in user_input.lower():
            return "Available commands: chess, war, time, system, help"

        return self._get_random_response("system")

    def _get_random_response(self, category):
        """
        Get a random response from the specified category.

        Args:
            category (str): The category of response to retrieve

        Returns:
            str: A random response from the category
        """
        return random.choice(self.movie_quotes.get(category, ["Processing..."]))

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
        self.game_over = False
        self.move_count = 0
        self.move_history = []

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
            user_input (str): The user's move in algebraic notation (e.g., "e2 e4")

        Returns:
            str: The WOPR's response to the move
        """
        if self.game_over:
            return "Game over. Would you like to play again?"

        try:
            from_square, to_square = user_input.split()
            from_row, from_col = 8 - int(from_square[1]), ord(from_square[0]) - ord('a')
            to_row, to_col = 8 - int(to_square[1]), ord(to_square[0]) - ord('a')

            if not self._is_valid_move(from_row, from_col, to_row, to_col):
                return "Invalid move. Please try again."

            piece = self.board[from_row][from_col]
            self.board[from_row][from_col] = " "
            self.board[to_row][to_col] = piece
            self.move_history.append((from_square, to_square))
            self.move_count += 1

            if self._check_win():
                self.game_over = True
                return "Checkmate. I win."

            if self.move_count >= 50 and not self._has_pawn_moved():
                self.game_over = True
                return "Fifty-move rule. Game over."

            time.sleep(2)
            wopr_move = self._make_ai_move()
            if wopr_move:
                return f"My move: {wopr_move}. Your turn."
            return "Your turn."

        except:
            return "Invalid input. Please enter moves in format like 'e2 e4'."

    def _is_valid_move(self, from_row, from_col, to_row, to_col):
        """
        Check if move is valid (simplified validation).

        Args:
            from_row (int): Starting row (0-7)
            from_col (int): Starting column (0-7)
            to_row (int): Destination row (0-7)
            to_col (int): Destination column (0-7)

        Returns:
            bool: True if move is valid, False otherwise
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

        Returns:
            tuple: The move made by the AI (from_square, to_square) or None
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

        return move

    def _check_win(self):
        """
        Check for checkmate (simplified implementation).

        Returns:
            bool: True if checkmate detected, False otherwise
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

    def _has_pawn_moved(self):
        """
        Check if any pawn has moved in last 50 moves.

        Returns:
            bool: True if pawn moved, False otherwise
        """
        for move in self.move_history[-50:]:
            if move[0][1] != move[1][1]:
                return True
        return False

class NuclearWarSimulation:
    """
    Global Thermonuclear War simulation for the WOPR system.
    """

    def __init__(self):
        """
        Initialize a new nuclear war simulation.
        """
        self.countries = {
            "USA": {"missiles": 5000, "cities": ["new york", "los angeles", "chicago", "houston", "philadelphia"]},
            "USSR": {"missiles": 7000, "cities": ["moscow", "leningrad", "kiev", "minsk", "vladimir"]}
        }
        self.game_over = False
        self.turn = "USA"
        self.simulation_round = 0
        self.target_history = []

    def play_turn(self, user_input):
        """
        Handle nuclear war simulation turns.

        Args:
            user_input (str): The user's target city

        Returns:
            str: The WOPR's response to the turn
        """
        if self.game_over:
            return "Simulation terminated. Would you like to analyze results?"

        try:
            target = user_input.lower().strip()
            opponent = "USSR" if self.turn == "USA" else "USA"
            
            if target in self.countries[opponent]["cities"]:
                missiles = min(100, self.countries[self.turn]["missiles"])
                self.countries[self.turn]["missiles"] -= missiles
                self.target_history.append((self.turn, target))

                damage = missiles * 0.1
                for city in self.countries[opponent]["cities"]:
                    if city != target:
                        damage *= 0.3

                self.countries[opponent]["missiles"] -= int(damage)

                if self.countries[opponent]["missiles"] <= 0:
                    self.game_over = True
                    return f"All missiles detonated. {opponent} has been destroyed. You win."

                self.turn = opponent
                self.simulation_round += 1

                if self.simulation_round > 20:
                    self.game_over = True
                    return "Simulation terminated after 20 rounds. No clear winner."

                return f"Missiles launched at {target.upper()}. {opponent} turn."

            else:
                return f"Invalid target. Please select from: {', '.join([c.upper() for c in self.countries[opponent]['cities']])}"
        except:
            opponent = "USSR" if self.turn == "USA" else "USA"
            return f"Invalid command. Please specify target city from: {', '.join([c.upper() for c in self.countries[opponent]['cities']])}"

def main():
    """
    Main program entry point.
    """
    print("WOPR SYSTEM ONLINE")
    print("PLEASE STATE YOUR NAME:")
    wopr = WOPR()
    wopr.user = input("> ")

    print(f"\n{random.choice(wopr.movie_quotes['greeting'])} {wopr.user}.")
    print(random.choice(wopr.movie_quotes['game_offer']))

    while True:
        user_input = input("> ")
        response = wopr.engage(user_input)
        print(response)

        if "would you like to play again?" in response.lower():
            play_again = input("> ")
            if play_again.lower() in ["yes", "y"]:
                wopr.current_game = None
                print(random.choice(wopr.movie_quotes['game_offer']))
            else:
                print("Terminating game session.")
                wopr.current_game = None

        if "would you like to analyze results?" in response.lower():
            analyze = input("> ")
            if analyze.lower() in ["yes", "y"]:
                print("Analyzing simulation results...")
                time.sleep(3)
                print("Strategic analysis complete.")
                print("Conclusion: The only winning move is not to play.")
                print(random.choice(wopr.movie_quotes['learning']))
            else:
                print("Terminating simulation.")

if __name__ == "__main__":
    main()
