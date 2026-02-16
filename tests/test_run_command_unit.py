import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from __init__ import OutputSource, run_command
import run_command as run_command_module


class TestRunCommandUnit(unittest.TestCase):
    def test_passes_expected_popen_kwargs_and_closes_pipes(self):
        stdout_pipe = mock.Mock()
        stderr_pipe = mock.Mock()

        process = mock.Mock()
        process.stdout = stdout_pipe
        process.stderr = stderr_pipe
        process.wait = mock.Mock()

        with mock.patch.object(run_command_module.subprocess, "Popen", return_value=process) as popen_mock:
            with mock.patch.object(run_command_module, "merge_pipes", return_value=iter([("STDOUT", "a")])):
                lines = list(run_command(["echo", "x"]))

        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0].text, "a")
        self.assertEqual(lines[0].source, OutputSource.STDOUT)

        popen_mock.assert_called_once()
        called_args, called_kwargs = popen_mock.call_args
        self.assertEqual(called_args[0], ["echo", "x"])
        self.assertEqual(called_kwargs["stdout"], run_command_module.subprocess.PIPE)
        self.assertEqual(called_kwargs["stderr"], run_command_module.subprocess.PIPE)
        self.assertTrue(called_kwargs["text"])
        self.assertEqual(called_kwargs["stdin"], run_command_module.subprocess.DEVNULL)
        self.assertTrue(Path(called_kwargs["cwd"]).is_absolute())

        stdout_pipe.close.assert_called_once()
        stderr_pipe.close.assert_called_once()
        process.wait.assert_called_once()

    def test_preserves_user_supplied_stdin(self):
        process = mock.Mock()
        process.stdout = mock.Mock()
        process.stderr = mock.Mock()

        custom_stdin = object()

        with mock.patch.object(run_command_module.subprocess, "Popen", return_value=process) as popen_mock:
            with mock.patch.object(run_command_module, "merge_pipes", return_value=iter([])):
                list(run_command(["echo", "x"], stdin=custom_stdin))

        called_kwargs = popen_mock.call_args.kwargs
        self.assertIs(called_kwargs["stdin"], custom_stdin)

    def test_waits_and_closes_pipes_when_merge_raises(self):
        process = mock.Mock()
        process.stdout = mock.Mock()
        process.stderr = mock.Mock()

        with mock.patch.object(run_command_module.subprocess, "Popen", return_value=process):
            with mock.patch.object(run_command_module, "merge_pipes", side_effect=RuntimeError("boom")):
                with self.assertRaises(RuntimeError):
                    list(run_command(["echo", "x"]))

        process.stdout.close.assert_called_once()
        process.stderr.close.assert_called_once()
        process.wait.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
