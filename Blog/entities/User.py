import sys
import json
from entities.BaseEntity import BaseEntity

class User(BaseEntity):
	def __init__(self, name = "", email = ""):
		BaseEntity.__init__(self)
		self.name = name
		self.email = email

	def __iter__(self):
		if(self.mongo_serialize == False):
			yield 'oid', self.oid
		yield 'name', self.name
		yield 'email', self.email

	def getInstance(dict):
		user = User()
		user.fromDictionary(dict)
		return user