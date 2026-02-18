# python_command_runner

Small Python utility for running subprocess commands and streaming output lines with source metadata (`STDOUT` or `STDERR`).

## What It Provides

- `run_command(...)`: wraps `subprocess.Popen` and yields output lines.
- `OutputLine`: value object containing `text`, `index`, and `source`.
- `OutputSource`: enum for output stream source labels.

## Installation

### From GitHub

```bash
pip install "python-command-runner @ git+https://github.com/OWNER/REPO.git"
```

### Session-only virtualenv workflow

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install "python-command-runner @ git+https://github.com/OWNER/REPO.git"

python3 path/to/your_script.py

deactivate
```

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## Quick Example

```python
from python_command_runner import run_command

for line in run_command(["python3", "-c", "print('hello')"]):
    print(line)
```

## API Notes

### `run_command(*args, timeout_seconds=None, **kwargs)`

- Passes arguments to `subprocess.Popen`.
- Always configures `stdout=subprocess.PIPE`, `stderr=subprocess.PIPE`, and `text=True`.
- Defaults `stdin=subprocess.DEVNULL` if not provided.
- Resolves `cwd` to an absolute path (defaults to current working directory).
- Yields `OutputLine` objects until process output is exhausted.
- Returns the subprocess exit code when the generator completes.
- Ensures pipes are closed and the process is waited for, even on errors while reading output.
- If `timeout_seconds` is set, the subprocess is terminated when the timeout elapses.

To read the exit code, consume the generator manually and inspect `StopIteration.value`:

```python
iterator = run_command(["python3", "-c", "import sys; sys.exit(3)"])
while True:
    try:
        line = next(iterator)
        print(line)
    except StopIteration as stop:
        print("exit code:", stop.value)
        break
```

### `OutputLine`

- Constructor: `OutputLine(text, index, source=OutputSource.OTHER)`
- `str(line)` / `repr(line)` format: `[index][SOURCE] text`
- Iterable form yields: `text`, then `source`
