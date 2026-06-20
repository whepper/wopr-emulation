#!/usr/bin/env python3
"""WOPR Emulation - entry shim.

Run with:
    python3 wopr.py
    python3 wopr.py --fast
"""

import sys

from wopr.main import main

if __name__ == "__main__":
    main()
