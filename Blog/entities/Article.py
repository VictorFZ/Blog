import sys
import json
from bson.objectid import ObjectId
from entities.BaseEntity import BaseEntity
from entities.Tag import Tag
from entities.Comment import Comment
from entities.Category import Category
from entities.Validation import Validation
from datetime import datetime

class Article(BaseEntity):
    def __init__(self, name = "", publish_date = "", slug = "", text = "", author = "", comments = [], tags = [], categories = []):
        BaseEntity.__init__(self, propertiesToCustomDict=[{'c':'Tag','p':'tags'}, {'c':'Comment', 'p':'comments'}, {'c':'Category', 'p':'categories'}])
        self.name = name
        self.slug = slug
        self.publish_date = publish_date
        self.text = text
        self.author = author
        self.comments = comments
        self.tags = tags
        self.categories = categories

    def __iter__(self):
        if(self.ignore_id == False):
        	yield 'oid', self.oid
        yield 'name', self.name
        yield 'slug', self.slug
        yield 'publish_date', self.publish_date
        yield 'text', self.text
        yield 'author', self.author
        yield 'comments', list(map(lambda x: dict(x), self.comments))
        yield 'tags', list(map(lambda x: dict(x), self.tags))
        yield 'categories', list(map(lambda x: dict(x), self.categories))

    def validate(self):
        return Validation("true","OK")

    def setPublishTimeToNow(self):
        self.publish_date = datetime.utcnow()

    def fromDictionary(self, dictionary):
        for k, v in dictionary.items():
            found = next((x for x in self.propertiesToCustomDict if x['p'] == k), None)
            if (found is not None and v is not None):
                setattr(self, k, list(map(lambda x: eval(found['c']).getInstance(x), v)))
            else:
                if(v is not None):
                    setattr(self, k, v)
        if '_id' in dictionary:
            setattr(self, "oid", str(dictionary["_id"]))

    def getInstance(dict):
        article = Article()
        article.fromDictionary(dict)
        return article
