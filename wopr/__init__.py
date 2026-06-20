"""WOPR Emulation - Movie-Accurate Python Implementation.

A faithful recreation of the WOPR computer system from the 1983 film
*WarGames*.

Usage:
    python3 wopr.py
    python3 -m wopr
"""

from .core import QUIT, WOPR
from .main import main

__all__ = ["WOPR", "QUIT", "main"]
