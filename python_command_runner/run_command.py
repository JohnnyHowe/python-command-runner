import os
import subprocess

from enum import Enum
from pathlib import Path
from typing import Iterator

from .merge_pipes import merge_pipes


class OutputSource(Enum):
	STDOUT = 0
	STDERR = 1
	OTHER = 2

	def __str__(self):
		return self.name


class OutputLine:
	source: OutputSource
	test: str

	def __init__(self, text: str, source: OutputSource = OutputSource.OTHER) -> None:
		self.text = text
		self.source = source

	def __repr__(self):
		return str(self)

	def __str__(self):
		return f"[{str(self.source)}] {self.text}"

	def __iter__(self):
		yield self.text
		yield self.source


def run_command(*args, **kwargs) -> Iterator[OutputLine]:
	"""
	Wrap subprocess.Popen yielding every output line as an OutputLine object.
	"""

	kwargs["stdout"] = subprocess.PIPE
	kwargs["stderr"] = subprocess.PIPE
	kwargs["text"] = True

	if "stdin" not in kwargs:
		kwargs["stdin"] = subprocess.DEVNULL

	cwd = str(Path(kwargs.pop("cwd", os.getcwd())).resolve())

	p = subprocess.Popen(*args, cwd=cwd, **kwargs)
	try:
		for pipe_name, line in merge_pipes(STDOUT=p.stdout, STDERR=p.stderr):
			yield OutputLine(line, OutputSource[pipe_name])
	finally:
		if p.stdout:
			p.stdout.close()
		if p.stderr:
			p.stderr.close()
		p.wait()
