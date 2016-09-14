import os
import json
import bottle
from bottle import Bottle, request, response, run, route, view, static_file
from datetime import datetime
from beaker.middleware import SessionMiddleware
from bson import Binary, Code
from bson.json_util import dumps
from entities import Article, User, Validation
from providers import MongoProvider
from helpers import CollectionHelper, HttpHelper, EncryptionHelper

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
    articles = map(lambda x: Article.Article.getInstance(x, True), mongoArticles)
    
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
        article = Article.Article.getInstance(mongoArticle, True)
        article.format()
        return dumps(dict(article))

@bottle.route('/Articles', method=['POST'])
def createArticle():
    HttpHelper.setJsonContentType()

    user = HttpHelper.getSessionKey("logged_user")

    if(user is None):
        return dumps(dict(Validation.Validation(False, "You are not logged in")))

    article_dict = HttpHelper.postBodyToDict()
    article = Article.Article.getInstance(article_dict)

    validation = article.validate()
    if(validation.success == True):
        article.mongoSerialization()
        article.setPublishTimeToNow()
        article.setAuthor(str(user["_id"]))

        call = MongoProvider.ArticleCall()
        ret = call.insert(dict(article))
        validation.id = str(ret.inserted_id)

    return dumps(dict(validation))

@bottle.route('/Articles/<object_id>', method=['DELETE'])
def createArticle(object_id):
    HttpHelper.setJsonContentType()

    call = MongoProvider.ArticleCall()
    ret = call.delete(object_id)

    return dumps(True)

@bottle.route('/Users', method=['GET'])
def getUsers():
    HttpHelper.setJsonContentType()

    call = MongoProvider.UserCall()

    mongoUsers = call.get()
    users = map(lambda x: Entities.User.getInstance(x), mongoUsers)
    dicts = map(lambda x: dict(x), users)

    return dumps(dicts)

@bottle.route('/Users/Login', method=['GET'])
def getLoggedUser():
    HttpHelper.setJsonContentType()
    user = HttpHelper.getSessionKey("logged_user")

    if(user is None):
        return None
    else:
        return dumps(user)

@bottle.route('/Users/Login', method=['POST'])
def logUser():
    HttpHelper.setJsonContentType()
    login_dict = HttpHelper.postBodyToDict()
    call = MongoProvider.UserCall()

    mongoUsers = call.getByQuery({"$and": [{"email": login_dict["email"]}, {"password": login_dict["password"]}]})
    mongoUser = CollectionHelper.firstOrDefault(mongoUsers)
    if(mongoUser is None):
        return dumps(None)
    else:
        d = dict(mongoUser)
        HttpHelper.setSessionKey("logged_user", d)
        return dumps(d)

@bottle.route('/Users/Logout', method=['GET'])
def logOutUser():
    HttpHelper.setJsonContentType()
    HttpHelper.removeSession()
    return dumps(True)

@bottle.route('/Users/Sigin', method=['POST'])
def signinUser():
    HttpHelper.setJsonContentType()
    signin_dict = HttpHelper.postBodyToDict()
    call = MongoProvider.UserCall()

    mongoUsers = call.getByQuery({"email": signin_dict["email"]})
    mongoUser = CollectionHelper.firstOrDefault(mongoUsers)
    if(mongoUser is not None):
        return dumps(dict(Validation.Validation(False, "A user with the same email already exists!")))
    else:
        user = User.User.getInstance(signin_dict)
        validation = user.validate()
        if(validation.success == True):
            user.mongoSerialization()
            ret = call.insert(dict(user))

        return dumps(dict(validation))

