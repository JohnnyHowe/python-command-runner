import subprocess
import time
from typing import Optional

from .command import Command
from .command_output import CommandOutput


class CommandRunner:
    timeout_seconds: float = 60 * 5
    start_time: Optional[float] = None
    process = None
    terminated = False

    def __init__(self, command: Command) -> None:
        self.command = command
        self.output = CommandOutput()

    def run(self):
        self.start_time = time.time()

        self.process = subprocess.Popen(
            self.command.as_list(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        assert self.process.stdout is not None
        for line in self.process.stdout:
            self._recieved_stdout_line(line)
            if self.terminated:
                return

    def _recieved_stdout_line(self, line: str) -> None:
        print(line, end="")
        self.output.stdout_lines.append(line)

        assert self.start_time
        if self.start_time + self.timeout_seconds <= time.time():
            self.output.result = "timeout"
            self.output.success = False
            self.terminate()

    def terminate(self) -> None:
        if self.process is None:
            return
        self.terminated = True
        self.process.terminate()
        if self.process.stdout:
            self.process.stdout.close()
