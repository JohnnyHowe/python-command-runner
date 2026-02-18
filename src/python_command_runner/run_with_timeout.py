
import threading
from typing import Callable


def run_with_timeout(function: Callable, timeout_seconds: float) -> object:
    """Return function result, or raise TimeoutError if it exceeds timeout."""
    result_container = {}
    exception_container = {}

    def target() -> None:
        try:
            result_container["value"] = function()
        except Exception as exc:  # pragma: no cover - behavior validated via tests
            exception_container["value"] = exc

    worker = threading.Thread(target=target, daemon=True)
    worker.start()
    worker.join(timeout_seconds)

    if worker.is_alive():
        raise TimeoutError(f"Function call exceeded timeout of {timeout_seconds} seconds")

    if "value" in exception_container:
        raise exception_container["value"]

    return result_container.get("value")
