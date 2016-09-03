import sys
import json

class BaseEntity(object):
	def __init__(self, ignore_id = False):
		self.oid = ""
		self.ignore_id = ignore_id

	def fromDictionary(self, dictionary):
		for k, v in dictionary.items():
			setattr(self, k, v)
		if '_id' in dictionary:
			setattr(self, "oid", str(dictionary["_id"]))

	def ignoreIDSerialization(self):
		self.ignore_id = True