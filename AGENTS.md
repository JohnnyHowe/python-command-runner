# Repository Guidelines

## Project Structure & Module Organization
This package lives at `python_command_runner/` and is organized as a small Python library:
- `__init__.py`: public package exports.
- `scripts/`: implementation modules (`command.py`, `run_command.py`, `command_runner.py`, `pretty_print.py`, `command_output.py`).
- `tests/`: unit tests (`test_*.py`).
- `README.md`: high-level notes.

Keep core logic in `scripts/` and expose stable APIs through `__init__.py`.

## Build, Test, and Development Commands
No build step is required; this is a pure Python package.

Use these commands from `python_command_runner/`:
- `python3 -m unittest discover -s tests -v` - run all tests.
- `python3 -m unittest tests.test_command -v` - run one test module.
- `python3 -m unittest tests.test_run_command.TestRunCommand -v` - run one test class.

If you use `pytest` locally, install it separately; `unittest` is the canonical runner in this repo.

## Coding Style & Naming Conventions
- Follow PEP 8 with 4-space indentation.
- Use `snake_case` for functions/variables/modules, `PascalCase` for classes, and `UPPER_SNAKE_CASE` for constants.
- Prefer explicit relative imports inside the package (for example, `from .pretty_print import pretty_print`).
- Avoid `sys.path` manipulation in library code; keep imports package-safe.
- Add type hints for public functions and class methods when practical.

## Testing Guidelines
- Framework: Python `unittest`.
- Place tests in `tests/` and name files `test_*.py`.
- Name test methods `test_*` and keep each test focused on one behavior.
- Cover both normal and edge cases (for example, subprocess output parsing and command argument construction).

## Commit & Pull Request Guidelines
Git history currently uses short, imperative commit messages (for example, `Create pretty_print.py`, `Copied scripts`). Keep that style:
- First line under ~72 characters.
- Describe what changed, not how you felt.

For pull requests, include:
- Clear summary of behavior changes.
- Test evidence (exact command + result).
- Any import/API changes called out explicitly.
