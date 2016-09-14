import sys
import json

class BaseEntity(object):
    def __init__(self, mongo_serialize = False, mongo_serialize_is_edit = False, propertiesToCustomDict = []):
        self.oid = ""
        self.mongo_serialize = mongo_serialize
        self.mongo_serialize_is_edit = mongo_serialize_is_edit
        self.propertiesToCustomDict = propertiesToCustomDict

    def fromDictionary(self, dictionary):
        for k, v in dictionary.items():
        	setattr(self, k, v)
        if '_id' in dictionary:
        	setattr(self, "oid", str(dictionary["_id"]))

    def mongoSerialization(self, is_edit = False):
        self.mongo_serialize = True
        self.mongo_serialize_is_edit = is_edit