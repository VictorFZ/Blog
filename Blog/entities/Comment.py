import sys
import json
from entities.BaseEntity import BaseEntity

class Comment(BaseEntity):
	def __init__(self, comment = "", date = "", author = User()):
		BaseEntity.__init__(self, True)
		self.comment = comment
		self.date = date
		self.author = author

	def __iter__(self):
		if(self.ignore_id == False):
			yield 'oid', self.oid
		yield 'comment', self.comment
		yield 'date', self.date
		yield 'author', dict(self.author)

	def getInstance(dict):
		comment = Comment()
		comment.fromDictionary(dict)
		return comment