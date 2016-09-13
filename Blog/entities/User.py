import sys
import json
from entities.BaseEntity import BaseEntity
from entities.Validation import Validation

class User(BaseEntity):
    def __init__(self, name = "", email = "", password = ""):
        BaseEntity.__init__(self)
        self.name = name
        self.email = email
        self.password = password

    def __iter__(self):
        if(self.mongo_serialize == False):
            yield 'oid', self.oid
        yield 'name', self.name
        yield 'email', self.email
        yield 'password', self.password

    def validate(self):
        if(self.password == ""):
            return Validation(False,"Password is required")
        if(self.email == ""):
            return Validation(False,"Email is required")

        return Validation(True)

    def getInstance(dict):
        user = User()
        user.fromDictionary(dict)
        return user