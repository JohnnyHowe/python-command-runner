import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from __init__ import OutputLine, OutputSource


class TestOutputLine(unittest.TestCase):
    def test_defaults_to_other_source(self):
        line = OutputLine("hello")
        self.assertEqual(line.text, "hello")
        self.assertEqual(line.source, OutputSource.OTHER)

    def test_str_and_repr_include_source_and_text(self):
        line = OutputLine("message", OutputSource.STDERR)
        self.assertEqual(str(line), "[STDERR] message")
        self.assertEqual(repr(line), "[STDERR] message")

    def test_iter_yields_text_then_source(self):
        line = OutputLine("payload", OutputSource.STDOUT)
        items = list(iter(line))
        self.assertEqual(items, ["payload", OutputSource.STDOUT])


if __name__ == "__main__":
    unittest.main(verbosity=2)
