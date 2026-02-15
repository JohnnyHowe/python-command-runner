import sys
import unittest
from pathlib import Path

# Ensure the package parent directory is importable for test discovery.
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT.parent))

from python_command_runner import OutputSource, run_command


class TestRunCommand(unittest.TestCase):
    def test_run_command_captures_stdout(self):
        # Execute a real subprocess with the same Python used for the test run.
        output_lines = list(
            run_command([sys.executable, "-c", "print('hello from test')"])
        )

        # Verify command produced output and that stdout line content is correct.
        self.assertTrue(output_lines)
        self.assertEqual("hello from test", output_lines[0].text)
        self.assertEqual(OutputSource.STDOUT, output_lines[0].source)


if __name__ == "__main__":
    unittest.main()
