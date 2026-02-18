from python_command_runner import Command, CommandRunner

command = Command()
command.executable = "git"
command.subcommands = ["remote"]
command.add_flag("-v")

CommandRunner(command).run()
