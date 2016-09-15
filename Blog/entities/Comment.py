import sys
import json
from entities.BaseEntity import BaseEntity
from entities.Validation import Validation
from datetime import datetime, timedelta
from helpers import CollectionHelper

class Comment(BaseEntity):
    def __init__(self, comment = "", publish_date = "", author = ""):
        BaseEntity.__init__(self)
        self.comment = comment
        self.publish_date = publish_date
        self.author = author
        self.author_name = ""
        self.publish_date_formatted = ""

    def __iter__(self):
        if(self.mongo_serialize == False):
            yield 'author_name', self.author_name
            yield 'publish_date_formatted', self.publish_date_formatted
            yield 'oid', self.oid
        yield 'comment', self.comment
        yield 'publish_date', self.publish_date
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

    def format(self, users = []):
        if(self.publish_date != ""):
            self.publish_date_formatted = (self.publish_date - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")

            commentAuthor = CollectionHelper.firstOrDefault(users, {"key":"oid", "value": self.author})
            if(commentAuthor is not None):
                self.author_name = commentAuthor.name