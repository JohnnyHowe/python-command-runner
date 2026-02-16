from typing import Optional


class CommandOutput:
    stdout_lines: list = []
    success: Optional[bool] = None
    result: Optional[str]