import sys
import json
from entities.BaseEntity import BaseEntity
from entities.Validation import Validation

class Category(BaseEntity):
	def __init__(self, value = ""):
		BaseEntity.__init__(self, False)
		self.value = value

	def __iter__(self):
		if(self.mongo_serialize == False):
			yield 'oid', self.oid
		yield 'value', self.value

	def validate(self):
		if(self.value == ""):
			return Validation(False,"Category name must not be empty")

		return Validation(True)

	@classmethod
	def getInstance(self, dict):
		category = Category()
		category.fromDictionary(dict)
		return category
