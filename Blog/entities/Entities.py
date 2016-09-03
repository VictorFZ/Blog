import sys
import json
from bson.objectid import ObjectId

class ValidationEntity(object):
	def __init__(self, success, message = ""):
		self.success = success
		self.message = message

	def __iter__(self):
		yield 'success', self.success
		yield 'message', self.message

class BaseEntity(object):
	def __init__(self, ignore_id = 0):
		self.oid = ""
		self.ignore_id = ignore_id

	def fromDictionary(self, dictionary):
		for k, v in dictionary.items():
			setattr(self, k, v)
		if '_id' in dictionary:
			setattr(self, "oid", str(dictionary["_id"]))

	def ignoreIDSerialization(self):
		self.ignore_id = 1

class Category(BaseEntity):
	def __init__(self, value = ""):
		BaseEntity.__init__(self, 1)
		self.value = value

	def __iter__(self):
		if(self.ignore_id == 0):
			yield 'oid', self.oid
		yield 'value', self.value

	def getInstance(dict):
		category = Category()
		category.fromDictionary(dict)
		return category

class Tag(BaseEntity):
	def __init__(self, value = ""):
		BaseEntity.__init__(self, 1)
		self.value = value

	def __iter__(self):
		if(self.ignore_id == 0):
			yield 'oid', self.oid
		yield 'value', self.value

	def getInstance(dict):
		tag = Tag()
		tag.fromDictionary(dict)
		return tag

class User(BaseEntity):
	def __init__(self, name = "", email = ""):
		BaseEntity.__init__(self)
		self.name = name
		self.email = email

	def __iter__(self):
		if(self.ignore_id == 0):
			yield 'oid', self.oid
		yield 'name', self.name
		yield 'email', self.email

	def getInstance(dict):
		user = User()
		user.fromDictionary(dict)
		return user

class Comment(BaseEntity):
	def __init__(self, comment = "", date = "", author = User()):
		BaseEntity.__init__(self, 1)
		self.comment = comment
		self.date = date
		self.author = author

	def __iter__(self):
		if(self.ignore_id == 0):
			yield 'oid', self.oid
		yield 'comment', self.comment
		yield 'date', self.date
		yield 'author', dict(self.author)

	def getInstance(dict):
		comment = Comment()
		comment.fromDictionary(dict)
		return comment

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
