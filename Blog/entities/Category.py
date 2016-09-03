import sys
import json
from entities.BaseEntity import BaseEntity

class Category(BaseEntity):
	def __init__(self, value = ""):
		BaseEntity.__init__(self, True)
		self.value = value

	def __iter__(self):
		if(self.ignore_id == False):
			yield 'oid', self.oid
		yield 'value', self.value

	def getInstance(dict):
		category = Category()
		category.fromDictionary(dict)
		return category