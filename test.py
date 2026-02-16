from src import *

command = Command()
command.executable = "git"
command.subcommands = ["remote"]
command.add_flag("-v")

CommandRunner(command).run()