import sysimport jsonfrom bson.objectid import ObjectIdfrom pymongo import MongoClientclass MongoCall(object):    def __init__(self, table):        self.connection = MongoClient("localhost",27017)        self.table = table    def get(self):        documents = self.connection.m101[self.table].find()        return documents    def getByID(self, object_id):        documents = self.connection.m101[self.table].find({"_id": ObjectId(object_id)})        return documents    def insert(self, article):        self.connection.m101[self.table].insert_one(article)class ArticleCall(MongoCall):    def __init__(self):        MongoCall.__init__(self, "articles")class UserCall(MongoCall):    def __init__(self):        MongoCall.__init__(self, "users")