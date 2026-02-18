import os
import subprocess

from pathlib import Path
import threading
from typing import Generator, Optional

from .merge_pipes import merge_pipes
from .output_line import OutputLine
from .output_source import OutputSource


def run_command(
    *args, timeout_seconds: Optional[int] = None, **kwargs
) -> Generator[OutputLine, None, Optional[int]]:
    """
    Wrap subprocess.Popen yielding every output line as an OutputLine object.
    """
    kwargs["stdout"] = subprocess.PIPE
    kwargs["stderr"] = subprocess.PIPE
    kwargs["text"] = True

    if "stdin" not in kwargs:
        kwargs["stdin"] = subprocess.DEVNULL

    cwd = str(Path(kwargs.pop("cwd", os.getcwd())).resolve())
    process = subprocess.Popen(*args, cwd=cwd, **kwargs)

    def on_timeout() -> None:
        if process.poll() is None:
            process.terminate()

    timer = (
        threading.Timer(timeout_seconds, on_timeout)
        if timeout_seconds is not None
        else None
    )
    if timer:
        timer.start()

    current_line_index = 0
    try:
        for pipe_name, line in merge_pipes(STDOUT=process.stdout, STDERR=process.stderr):
            yield OutputLine(line, current_line_index, OutputSource[pipe_name])
            current_line_index += 1
    finally:
        if timer:
            timer.cancel()
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
        returncode = process.wait()

    return returncode
