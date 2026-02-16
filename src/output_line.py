from src.output_source import OutputSource


class OutputLine:
	source: OutputSource
	text: str
	index: int

	def __init__(self, text: str, index: int, source: OutputSource = OutputSource.OTHER) -> None:
		self.text = text
		self.source = source
		self.index = index

	def __repr__(self):
		return str(self)

	def __str__(self):
		return f"[{str(self.source)}] {self.text}"

	def __iter__(self):
		yield self.text
		yield self.source

