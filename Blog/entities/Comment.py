import sys
import json
from entities.BaseEntity import BaseEntity
from datetime import datetime

class Comment(BaseEntity):
    def __init__(self, comment = "", date = "", author = ""):
    	BaseEntity.__init__(self, True)
    	self.comment = comment
    	self.date = date
    	self.author = author

    def __iter__(self):
    	if(self.mongo_serialize == False):
    		yield 'oid', self.oid
    	yield 'comment', self.comment
    	yield 'date', self.date
    	yield 'author', self.author

    def setPublishTimeToNow(self):
        self.publish_date = datetime.utcnow()

    def getInstance(dict):
    	comment = Comment()
    	comment.fromDictionary(dict)
    	return comment