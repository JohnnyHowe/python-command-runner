from python_command_runner import run_command


for output_line in run_command(["python3", "-c", 'print("hello from python_command_runner")']):
    print(output_line)
