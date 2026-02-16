import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from __init__ import OutputSource


class TestOutputSource(unittest.TestCase):
    def test_str_returns_enum_name(self):
        self.assertEqual(str(OutputSource.STDOUT), "STDOUT")
        self.assertEqual(str(OutputSource.STDERR), "STDERR")
        self.assertEqual(str(OutputSource.OTHER), "OTHER")


if __name__ == "__main__":
    unittest.main(verbosity=2)
