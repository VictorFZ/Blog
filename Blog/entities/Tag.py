import sys
import json
from entities.BaseEntity import BaseEntity

class Tag(BaseEntity):
	def __init__(self, value = ""):
		BaseEntity.__init__(self, True)
		self.value = value

	def __iter__(self):
		if(self.mongo_serialize == False):
			yield 'oid', self.oid
		yield 'value', self.value

	def getInstance(dict):
		tag = Tag()
		tag.fromDictionary(dict)
		return tag
