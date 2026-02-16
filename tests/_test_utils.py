import time


class DelayedPipe:
    def __init__(self, lines, delay_s=0.02):
        self._lines = [line + "\n" for line in lines]
        self._index = 0
        self._delay_s = delay_s

    def readline(self):
        if self._index == 0:
            time.sleep(self._delay_s)
        if self._index >= len(self._lines):
            return ""
        line = self._lines[self._index]
        self._index += 1
        return line
