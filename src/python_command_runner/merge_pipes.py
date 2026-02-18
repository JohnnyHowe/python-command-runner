# Source - https://stackoverflow.com/a/51668895
# Posted by Marten Jacobs
# Retrieved 2026-02-16, License - CC BY-SA 4.0

import queue
import threading


def merge_pipes(**named_pipes):
    r"""
    Merges multiple pipes from subprocess.Popen (maybe other sources as well).
    The keyword argument keys will be used in the output to identify the source
    of the line.

    Example:
    p = subprocess.Popen(['some', 'call'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    outputs = {'out': log.info, 'err': log.warn}
    for name, line in merge_pipes(out=p.stdout, err=p.stderr):
        outputs[name](line)

    This will output stdout to the info logger, and stderr to the warning logger
    """

    # Constants. Could also be placed outside of the method. I just put them here
    # so the method is fully self-contained
    PIPE_OPENED = 1
    PIPE_OUTPUT = 2
    PIPE_CLOSED = 3

    # Create a queue where the pipes will be read into
    output = queue.Queue()

    # This method is the run body for the threads that are instatiated below
    # This could be easily rewritten to be outside of the merge_pipes method,
    # but to make it fully self-contained I put it here
    def pipe_reader(name, pipe):
        r"""
        reads a single pipe into the queue
        """
        output.put((PIPE_OPENED, name))
        try:
            for line in iter(pipe.readline, ""):
                output.put((PIPE_OUTPUT, name, line.rstrip()))
        finally:
            output.put((PIPE_CLOSED, name))

    # Start a reader for each pipe
    for name, pipe in named_pipes.items():
        t = threading.Thread(target=pipe_reader, args=(name, pipe))
        t.daemon = True
        t.start()

    # Use a counter to determine how many pipes are left open.
    # If all are closed, we can return
    pipe_count = 0

    # Read the queue in order, blocking if there's no data
    for data in iter(output.get, ""):
        code = data[0]
        if code == PIPE_OPENED:
            pipe_count += 1
        elif code == PIPE_CLOSED:
            pipe_count -= 1
        elif code == PIPE_OUTPUT:
            yield data[1:]
        if pipe_count == 0:
            return
