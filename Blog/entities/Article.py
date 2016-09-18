import sys
import json
import time
from bson.objectid import ObjectId
from entities.BaseEntity import BaseEntity
from entities.Tag import Tag
from entities.Comment import Comment
from entities.Category import Category
from entities.Validation import Validation
from datetime import datetime, timedelta
from functools import reduce
from helpers import CollectionHelper

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
		self.author_name = ""
		self.publish_date_formatted = ""
		self.tags_joined = ""
		self.categories_joined = ""

	def __iter__(self):
		if(self.mongo_serialize == False):
			yield 'oid', self.oid
			yield 'author_name', self.author_name
			yield 'publish_date_formatted', self.publish_date_formatted
			yield 'tags_joined', self.tags_joined
			yield 'categories_joined', self.categories_joined

		yield 'name', self.name
		yield 'slug', self.slug
		yield 'text', self.text

		if(self.mongo_serialize_is_edit == False):
			yield 'publish_date', self.publish_date
			yield 'author', self.author
			yield 'comments', list(map(lambda x: dict(x), self.comments))

		yield 'tags', list(map(lambda x: dict(x), self.tags))
		yield 'categories', list(map(lambda x: dict(x), self.categories))

	def validate(self):
		if(self.text == ""):
			return Validation(False,"Article body must not be empty")
		if(self.name == ""):
			return Validation(False,"Article must have a title")
		if(self.slug == ""):
			return Validation(False,"Article must have a slug")

		return Validation(True)

	def setPublishTimeToNow(self):
		self.publish_date = datetime.utcnow()

	def setAuthor(self, user_id):
		self.author = user_id

	def fromDictionary(self, dictionary, format, users = []):
		for k, v in dictionary.items():
			found = next((x for x in self.propertiesToCustomDict if x['p'] == k), None)
			if (found is not None and v is not None):
				setattr(self, k, list(map(lambda x: eval(found['c']).getInstance(x), v)))
			else:
				if(v is not None):
					setattr(self, k, v)
		if '_id' in dictionary:
			setattr(self, "oid", str(dictionary["_id"]))

		if(format):
			self.format(users)

	@classmethod
	def getInstance(self, dict, format = False, users = []):
		article = Article()
		article.fromDictionary(dict, format, users)
		return article

	def format(self, users = []):
		if(self.publish_date != ""):
			self.publish_date_formatted = (self.publish_date - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M")
		self.tags_joined = ",".join(list(map(lambda x: x.value,self.tags)))
		self.categories_joined = ",".join(list(map(lambda x: x.value,self.categories)))

		if(users is not None):
			articleAuthor = CollectionHelper.firstOrDefault(users, {"key":"oid", "value": self.author})
			if(articleAuthor is not None):
				self.author_name = articleAuthor.name

			if(self.comments is not None):
				for comment in self.comments:
					comment.format(users)
