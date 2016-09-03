import sys

class Validation(object):
	def __init__(self, success, message = ""):
		self.success = success
		self.message = message

	def __iter__(self):
		yield 'success', self.success
		yield 'message', self.message
