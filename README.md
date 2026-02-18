# python_command_runner
Small Python wrapper around `subprocess` for building and running commands.

## Installation
From this repository root:

```bash
python3 -m pip install -e .
```

## Basic Example
```python
from python_command_runner import Command, CommandRunner

command = Command()
command.executable = "python3"
command.subcommands = ["-c"]
command.positional_args = ['print("hello from python_command_runner")']

runner = CommandRunner(command)
runner.run()
print("captured lines:", len(runner.output.stdout_lines))
```

## Local Development
From this repository root:

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
```
