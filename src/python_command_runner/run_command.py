import os
import subprocess

from pathlib import Path
import threading
from typing import Generator, Optional, Tuple

from .merge_pipes import merge_pipes
from .output_line import OutputLine
from .output_source import OutputSource
from .run_with_timeout import run_with_timeout


def _prepare_popen_kwargs(kwargs: dict) -> Tuple[str, dict]:
    popen_kwargs = dict(kwargs)
    popen_kwargs["stdout"] = subprocess.PIPE
    popen_kwargs["stderr"] = subprocess.PIPE
    popen_kwargs["text"] = True

    cwd = str(Path(popen_kwargs.pop("cwd", os.getcwd())).resolve())
    return cwd, popen_kwargs


def _start_timeout_supervisor(
    process: subprocess.Popen, timeout_seconds: Optional[int]
) -> Optional[threading.Thread]:
    if timeout_seconds is None:
        return None

    def watch_timeout() -> None:
        try:
            run_with_timeout(process.wait, timeout_seconds)
        except TimeoutError:
            if process.poll() is None:
                process.terminate()

    timeout_supervisor = threading.Thread(target=watch_timeout, daemon=True)
    timeout_supervisor.start()
    return timeout_supervisor


def _yield_output_lines(process: subprocess.Popen) -> Generator[OutputLine, None, None]:
    current_line_index = 0
    for pipe_name, line in merge_pipes(STDOUT=process.stdout, STDERR=process.stderr):
        yield OutputLine(line, current_line_index, OutputSource[pipe_name])
        current_line_index += 1


def _cleanup_process(
    process: subprocess.Popen, timeout_supervisor: Optional[threading.Thread]
) -> int:
    if process.stdout:
        process.stdout.close()
    if process.stderr:
        process.stderr.close()

    returncode = process.wait()

    if timeout_supervisor and timeout_supervisor.is_alive():
        timeout_supervisor.join(timeout=0.01)

    return returncode


def run_command(
    *args, timeout_seconds: Optional[int] = None, **kwargs
) -> Generator[OutputLine, None, Optional[int]]:
    """
    Wrap subprocess.Popen yielding every output line as an OutputLine object.
    """
    cwd, popen_kwargs = _prepare_popen_kwargs(kwargs)
    process = subprocess.Popen(*args, cwd=cwd, **popen_kwargs)
    timeout_supervisor = _start_timeout_supervisor(process, timeout_seconds)

    try:
        yield from _yield_output_lines(process)
    finally:
        returncode = _cleanup_process(process, timeout_supervisor)

    return returncode
