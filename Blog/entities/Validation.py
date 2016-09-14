import sys

class Validation(object):
    def __init__(self, success, message = "", id = ""):
        self.success = success
        self.message = message
        self.id = id

    def __iter__(self):
        yield 'success', self.success
        yield 'message', self.message
        yield 'id', self.id
