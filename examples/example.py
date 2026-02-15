import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT / "src"))

from python_command_runner import Command, CommandRunner

command = Command()
command.executable = "python3"
command.subcommands = ["-c"]
command.positional_args = ['print("hello from python_command_runner")']

runner = CommandRunner(command)
runner.run()

print("captured lines:", len(runner.output.stdout_lines))
