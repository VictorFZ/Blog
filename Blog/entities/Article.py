import sys
import json
from bson.objectid import ObjectId
from entities.BaseEntity import BaseEntity
from entities.Validation import Validation

class Article(BaseEntity):
	def __init__(self, name = "", publish_date = "", slug = "", text = "", author = "", comments = [], tags = [], categories = []):
		BaseEntity.__init__(self)
		self.name = name
		self.slug = slug
		self.publish_date = publish_date
		self.text = text
		self.author = author
		self.comments = comments
		self.tags = tags
		self.categories = categories

	def __iter__(self):
		if(self.ignore_id == 0):
			yield 'oid', self.oid
		yield 'name', self.name
		yield 'slug', self.slug
		yield 'publish_date', self.publish_date
		yield 'text', self.text
		yield 'author', self.author
		yield 'comments', self.comments
		yield 'tags', self.tags
		yield 'categories', self.categories

	def validate(self):
		return ValidationEntity("true","OK")

	def getInstance(dict):
		article = Article()
		article.fromDictionary(dict)
		return article
