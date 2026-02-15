"""Manual visual sanity check for pretty_print output.

Run from this repository root:
    python3 tests/visual_check_pretty_print.py
"""

import sys
from pathlib import Path

# Support direct execution (for example VS Code "Run Python File") by ensuring
# the package parent directory is importable.
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT.parent))

from python_command_runner.scripts.pretty_print import *


def main() -> None:
    print("=== pretty_print visual sanity check ===")
    print("If ANSI colors are supported, lines below should be colorized.\n")

    pretty_print("Regular message (no color)")
    pretty_print("Warning message", color=WARNING)
    pretty_print("Error message", color=ERROR)
    pretty_print("Success message", color=SUCCESS)
    pretty_print("TODO message", color=TODO)
    pretty_print("Custom hex color message", color="#00bcd4")

    print("\n=== raise_pretty_exception demo ===")
    try:
        raise_pretty_exception(RuntimeError, "This is an expected demo exception.")
    except RuntimeError as exc:
        print(f"Caught exception as expected: {exc}")

    print("\nVisual check complete.")


if __name__ == "__main__":
    main()
