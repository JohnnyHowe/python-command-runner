# python_command_runner

Small Python utility for running subprocess commands and streaming output lines with source metadata (`STDOUT` or `STDERR`).

## What It Provides

- `run_command(...)`: wraps `subprocess.Popen` and yields output as lines.
- `OutputLine`: value object containing:
  - `text`: output line text
  - `source`: `OutputSource.STDOUT`, `OutputSource.STDERR`, or `OutputSource.OTHER`
- `OutputSource`: enum for output stream source labels.

## Installation

From this repository root:

```bash
python3 -m pip install -e .
```

## API Notes

### `run_command(*args, **kwargs)`

- Passes arguments to `subprocess.Popen`.
- Always configures:
  - `stdout=subprocess.PIPE`
  - `stderr=subprocess.PIPE`
  - `text=True`
- Defaults `stdin=subprocess.DEVNULL` if not provided.
- Resolves `cwd` to an absolute path (defaults to current working directory).
- Yields `OutputLine` objects until process output is exhausted.
- Ensures pipes are closed and the process is waited for, even on errors while reading output.

### `OutputLine`

- `str(line)` / `repr(line)` format: `[SOURCE] text`
- Iterable form yields: `text`, then `source`
