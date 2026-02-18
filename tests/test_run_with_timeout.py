import sys
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from python_command_runner.run_with_timeout import run_with_timeout


class TestRunWithTimeout(unittest.TestCase):
    def test_returns_function_result(self):
        result = run_with_timeout(lambda: 123, timeout_seconds=0.5)
        self.assertEqual(result, 123)

    def test_propagates_function_exception(self):
        def boom():
            raise RuntimeError("boom")

        with self.assertRaisesRegex(RuntimeError, "boom"):
            run_with_timeout(boom, timeout_seconds=0.5)

    def test_raises_timeout_error_when_function_takes_too_long(self):
        def sleepy():
            time.sleep(0.2)
            return "done"

        with self.assertRaises(TimeoutError):
            run_with_timeout(sleepy, timeout_seconds=0.01)

    def test_returns_none_when_function_returns_none(self):
        def returns_none():
            return None

        result = run_with_timeout(returns_none, timeout_seconds=0.5)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
