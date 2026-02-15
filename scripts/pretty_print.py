"""Utilities for styled terminal output.

This module provides a small wrapper around ``print`` to support optional
ANSI truecolor output and a helper for raising formatted exceptions.
"""

from pathlib import Path
from typing import Type


REGULAR=None
WARNING="#f1c40f"
ERROR="#e06c75"
SUCCESS="#98c379"
TODO="#4F37D7"


def print_with_color_tags(text: str) -> None:
    """
    Print text, colouring sections in <color> tags.
    So "<red>Red Text. </red>White (default) Text. <green>Green Text.</green>" would print in those colors.
    """


def raise_pretty_exception(error: Type[Exception], message: str) -> None:
    """Print a message using the error color and raise the given exception."""
    pretty_print(message, color=ERROR)
    raise error(message)


def pretty_print(*args, color=None, **kwargs) -> None:
    """Print values as text, optionally with a hex foreground color.

    Args:
        *args: Values converted to strings and joined by spaces.
        color: Optional RGB hex string (for example ``"#98c379"``).
        **kwargs: Additional keyword arguments forwarded to ``print``.
    """
    text = " ".join(str(a) for a in args)  # join everything manually
    if not color:
        print(text, **kwargs)
        return

    color = color.lstrip("#")
    r, g, b = (int(color[i:i+2], 16) for i in (0, 2, 4))
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m", **kwargs)
