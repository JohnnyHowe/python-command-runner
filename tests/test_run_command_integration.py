import sys
import unittest
from pathlib import Path
from tempfile import NamedTemporaryFile

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from python_command_runner import OutputLine, OutputSource, run_command


class TestRunCommandIntegration(unittest.TestCase):
    def _consume_generator_with_return_code(self, generator):
        lines = []
        while True:
            try:
                lines.append(next(generator))
            except StopIteration as stop:
                return lines, stop.value

    def test_collects_stdout_and_stderr_with_correct_source(self):
        code = "import sys; print('out'); print('err', file=sys.stderr)"
        lines = list(run_command(["python3", "-c", code]))

        self.assertEqual(len(lines), 2)
        self.assertTrue(all(isinstance(line, OutputLine) for line in lines))

        by_source = {OutputSource.STDOUT: [], OutputSource.STDERR: []}
        for line in lines:
            by_source[line.source].append(line.text)

        self.assertEqual(by_source[OutputSource.STDOUT], ["out"])
        self.assertEqual(by_source[OutputSource.STDERR], ["err"])

    def test_defaults_stdin_to_devnull_and_process_does_not_hang(self):
        code = "import sys; data = sys.stdin.read(); print('stdin:' + data)"
        lines = list(run_command(["python3", "-c", code]))

        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].source, OutputSource.STDOUT)
        self.assertEqual(lines[0].text, "stdin:")

    def test_accepts_custom_stdin(self):
        code = "import sys; print(sys.stdin.read())"
        with NamedTemporaryFile(mode="w+", encoding="utf-8") as temp_stdin:
            temp_stdin.write("abc")
            temp_stdin.seek(0)
            lines = list(run_command(["python3", "-c", code], stdin=temp_stdin))

        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].source, OutputSource.STDOUT)
        self.assertEqual(lines[0].text, "abc")

    def test_resolves_cwd_and_runs_command_in_target_directory(self):
        temp_dir = Path(__file__).resolve().parent
        code = "import os; print(os.getcwd())"
        lines = list(run_command(["python3", "-c", code], cwd=str(temp_dir / ".." / "tests")))

        self.assertEqual(len(lines), 1)
        self.assertEqual(Path(lines[0].text), temp_dir.resolve())

    def test_returns_nonzero_exit_code(self):
        code = "import sys; print('bad', file=sys.stderr); sys.exit(4)"
        lines, return_code = self._consume_generator_with_return_code(run_command(["python3", "-c", code]))

        self.assertEqual(return_code, 4)
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].source, OutputSource.STDERR)
        self.assertEqual(lines[0].text, "bad")


if __name__ == "__main__":
    unittest.main(verbosity=2)
