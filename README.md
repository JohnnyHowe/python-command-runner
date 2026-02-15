# python_command_runner
Small Python wrapper around `subprocess` for building and running commands.

## Use as a Git Submodule
Add this repository as a submodule in your project:

```bash
git submodule add <repo-url> third_party/python_command_runner
git submodule update --init --recursive
```

Update later:

```bash
git submodule update --remote --merge third_party/python_command_runner
```

## Import from the Submodule
When used as a submodule, import from its `src` directory:

```python
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO_ROOT / "third_party/python_command_runner/src"))

from python_command_runner import Command, CommandRunner
```

## Basic Example
```python
command = Command()
command.executable = "python3"
command.subcommands = ["-c"]
command.positional_args = ['print("hello from python_command_runner")']

runner = CommandRunner(command)
runner.run()
print("captured lines:", len(runner.output.stdout_lines))
```

## Optional: Editable install (local development)
If you want standard Python imports without `sys.path` setup:

```bash
python3 -m pip install -e third_party/python_command_runner
```
