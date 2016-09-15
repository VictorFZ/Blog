import sys
import json
from entities.BaseEntity import BaseEntity
from datetime import datetime, timedelta

class Comment(BaseEntity):
    def __init__(self, comment = "", date = "", author = ""):
        BaseEntity.__init__(self, True)
        self.comment = comment
        self.date = date
        self.author = author
        self.author_name = ""
        self.publish_date_formatted = ""

    def __iter__(self):
        if(self.mongo_serialize == False):
            yield 'author_name', self.author_name
            yield 'publish_date_formatted', self.publish_date_formatted
            yield 'oid', self.oid
        yield 'comment', self.comment
        yield 'date', self.date
        yield 'author', self.author

    
    def validate(self):
        if(self.comment == ""):
            return Validation(False,"You must write something")

        return Validation(True)

    def setPublishTimeToNow(self):
        self.publish_date = datetime.utcnow()

    def setAuthor(self, user_id):
        self.author = user_id

    def getInstance(dict):
    	comment = Comment()
    	comment.fromDictionary(dict)
    	return comment

    def format(self):
        if(self.publish_date != ""):
            self.publish_date_formatted = (self.publish_date - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")