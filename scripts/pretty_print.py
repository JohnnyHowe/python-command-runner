try:
    from python_pretty_print import pretty_print as _pretty_print
except ModuleNotFoundError:
    def _pretty_print(message: str) -> None:
        print(message)


def pretty_print(message: str) -> None:
    _pretty_print(message)


__all__ = ["pretty_print"]
