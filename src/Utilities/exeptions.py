from turtle import st


class ArgumentTypeError(Exception):
	def __init__(self, message: str):
		if isinstance(message, str):
			super().__init__(message)
		else:
			super().__init__()

class InvalidPeriodError(Exception):
	def __init__(self, message: str):
		if isinstance(message, str):
			super().__init__(message)
		else:
			super().__init__()
