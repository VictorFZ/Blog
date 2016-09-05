import os
import json
import bottle
from bottle import Bottle, request, response, run, route, view, static_file
from datetime import datetime
from beaker.middleware import SessionMiddleware
from bson import Binary, Code
from bson.json_util import dumps
from entities import Article
from providers import MongoProvider
from helpers import CollectionHelper, HttpHelper

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

@route('/')
@route('/home')
def home():
    return static_file("index.html", root=dir_path+'/'+'views/')

@bottle.route('/Articles', method=['GET'])
def getArticles():
    HttpHelper.setJsonContentType()

    call = MongoProvider.ArticleCall()

    mongoArticles = call.get()
    articles = map(lambda x: Article.Article.getInstance(x), mongoArticles)
    dicts = map(lambda x: dict(x), articles)

    return dumps(dicts)

@bottle.route('/Articles/<object_id>', method=['GET'])
def getArticle(object_id):
    HttpHelper.setJsonContentType()

    call = MongoProvider.ArticleCall()

    mongoArticles = call.getByID(object_id)
    mongoArticle = CollectionHelper.firstOrDefault(mongoArticles)
    if(mongoArticle is None):
        return dumps(None)
    else:
        article = Article.Article.getInstance(mongoArticle)

        return dumps(dict(article))

@bottle.route('/Articles', method=['POST'])
def createArticle():
    HttpHelper.setJsonContentType()
    article_dict = HttpHelper.postBodyToDict()
    article = Article.Article.getInstance(article_dict)

    article.ignoreIDSerialization()
    article.setPublishTimeToNow()

    call = MongoProvider.ArticleCall()
    ret = call.insert(dict(article))

    return dumps(str(ret.inserted_id))

@bottle.route('/Users', method=['GET'])
def getUsers():
    HttpHelper.setJsonContentType()

    call = MongoProvider.UserCall()

    mongoUsers = call.get()
    users = map(lambda x: Entities.User.getInstance(x), mongoUsers)
    dicts = map(lambda x: dict(x), users)

    return dumps(dicts)
