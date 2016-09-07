import sys
import json

class BaseEntity(object):
    def __init__(self, mongo_serialize = False, propertiesToCustomDict = []):
        self.oid = ""
        self.mongo_serialize = mongo_serialize
        self.propertiesToCustomDict = propertiesToCustomDict

    def fromDictionary(self, dictionary):
        for k, v in dictionary.items():
        	setattr(self, k, v)
        if '_id' in dictionary:
        	setattr(self, "oid", str(dictionary["_id"]))

    def mongoSerialization(self):
        self.mongo_serialize = True