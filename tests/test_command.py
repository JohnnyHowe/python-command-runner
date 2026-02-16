from pathlib import Path
import sys
import unittest

# import os
# cwd = Path(os.getcwd()).resolve()
# print("cwd=" + str(cwd))
# for item in cwd.iterdir():
#     print(f"\t{item.relative_to(cwd)}")

sys.path.insert(0, str(Path(__file__).parent.parent))

from __init__ import run_command


class TestCommand(unittest.TestCase):
    # Test method names must start with `test_` so unittest discovery can find
    # and execute them automatically.
    def test_junk(self):
        lines = list(run_command(["python3", "--version"]))
        self.assertTrue(len(lines) == 1, f"Expected one line! Got: {lines}") 
        print(lines[0])
        print(lines[0].text)
        self.assertTrue(lines[0].text.startswith("Python"), f"Expected line to start with \"python\". Got: {lines[0].text}") 


# This allows running this file directly:
# `python3 tests/test_command.py`
# It is optional for discovery mode (`python3 -m unittest discover ...`) but
# useful when starting out.
if __name__ == "__main__":
    unittest.main()
