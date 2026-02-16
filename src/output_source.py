from enum import Enum


class OutputSource(Enum):
	STDOUT = 0
	STDERR = 1
	OTHER = 2

	def __str__(self):
		return self.name

