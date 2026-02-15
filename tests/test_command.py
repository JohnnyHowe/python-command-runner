import sys
import unittest
from pathlib import Path

# Ensure the package parent directory is importable for test discovery.
PACKAGE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE_ROOT.parent))

# Import the class under test.
from python_command_runner import Command


class TestCommand(unittest.TestCase):
    # Test method names must start with `test_` so unittest discovery can find
    # and execute them automatically.
    def test_as_list_with_only_executable(self):
        # Arrange: create the object and set only the minimum required field.
        cmd = Command()
        cmd.executable = "python3"

        # Act + Assert: call the method and verify exact output.
        # `assertEqual(expected, actual)` fails with a helpful diff if values
        # are different, which makes debugging straightforward.
        self.assertEqual(["python3"], cmd.as_list())


# This allows running this file directly:
# `python3 tests/test_command.py`
# It is optional for discovery mode (`python3 -m unittest discover ...`) but
# useful when starting out.
if __name__ == "__main__":
    unittest.main()
