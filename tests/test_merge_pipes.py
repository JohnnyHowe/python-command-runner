import sys
import unittest
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from python_command_runner.merge_pipes import merge_pipes
from tests._test_utils import DelayedPipe


class TestMergePipes(unittest.TestCase):
    def test_single_pipe_yields_trimmed_lines(self):
        pipe = StringIO("alpha\nbeta\n")
        output = list(merge_pipes(STDOUT=pipe))
        self.assertEqual(output, [("STDOUT", "alpha"), ("STDOUT", "beta")])

    def test_multiple_pipes_emit_all_lines_with_source_name(self):
        stdout = DelayedPipe(["one", "two"])
        stderr = DelayedPipe(["errA", "errB"])

        output = list(merge_pipes(STDOUT=stdout, STDERR=stderr))

        self.assertEqual(len(output), 4)
        self.assertEqual({name for name, _ in output}, {"STDOUT", "STDERR"})
        grouped = {"STDOUT": [], "STDERR": []}
        for name, line in output:
            grouped[name].append(line)
        self.assertEqual(grouped["STDOUT"], ["one", "two"])
        self.assertEqual(grouped["STDERR"], ["errA", "errB"])

    def test_pipe_closure_does_not_drop_other_pipe_output(self):
        stdout = DelayedPipe(["out1", "out2", "out3"])
        stderr = DelayedPipe(["err1"])

        output = list(merge_pipes(STDOUT=stdout, STDERR=stderr))
        grouped = {"STDOUT": [], "STDERR": []}
        for name, line in output:
            grouped[name].append(line)

        self.assertEqual(grouped["STDERR"], ["err1"])
        self.assertEqual(grouped["STDOUT"], ["out1", "out2", "out3"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
