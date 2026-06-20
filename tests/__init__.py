"""Shared test utilities."""

from __future__ import annotations

import os
import sys
import unittest

# Force fast mode for the entire test run before any wopr module is
# imported — the io module reads this at import time.
os.environ["WOPR_FAST"] = "1"

# Ensure the project root is on the path so `import wopr` works when the
# tests are run from the project root.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main() -> None:
    """Run the test suite with stdout suppressed for cleaner output."""
    import contextlib
    import io

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=os.path.dirname(__file__))
    runner = unittest.TextTestRunner(verbosity=2)
    with contextlib.redirect_stdout(io.StringIO()):
        result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
