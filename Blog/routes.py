import os
import json
import bottle
from bottle import Bottle, request, response, run, route, view, static_file
from datetime import datetime
from beaker.middleware import SessionMiddleware
from bson import Binary, Code
from bson.json_util import dumps
from entities import Article, User, Validation, Comment
from providers import MongoProvider
from helpers import CollectionHelper, HttpHelper, EncryptionHelper
from operator import attrgetter

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

@route('/')
@route('/home')
def home():
    return static_file("index.html", root=dir_path+'/'+'views/')

def getAllUsers():
    usercall = MongoProvider.UserCall()
    mongoUsers = usercall.get()
    users = list(map(lambda x: User.User.getInstance(x), mongoUsers))

    return users

@bottle.route('/Articles', method=['GET'])
def getArticles():
    HttpHelper.setJsonContentType()

    users = getAllUsers()
    call = MongoProvider.ArticleCall()

    mongoArticles = list(call.get())
    articles = list(map(lambda x: Article.Article.getInstance(x, True, users), mongoArticles))
    
    articles_sorted = sorted(articles, key=attrgetter('publish_date'), reverse=True)
    dicts = map(lambda x: dict(x), articles_sorted)

    return dumps(dicts)

@bottle.route('/Articles/<object_id>', method=['GET'])
def getArticle(object_id):
    HttpHelper.setJsonContentType()

    users = getAllUsers()

    call = MongoProvider.ArticleCall()

    mongoArticles = call.getByID(object_id)
    mongoArticle = CollectionHelper.firstOrDefault(mongoArticles)
    if(mongoArticle is None):
        return dumps(None)
    else:
        article = Article.Article.getInstance(mongoArticle, True, users)
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
        article.setAuthor(user["oid"])

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

@bottle.route('/Articles/<object_id>', method=['PUT'])
def createArticle(object_id):
    HttpHelper.setJsonContentType()

    article_dict = HttpHelper.postBodyToDict()
    article = Article.Article.getInstance(article_dict)

    validation = article.validate()
    if(validation.success == True):
        article.mongoSerialization(True)
        article_edit_dict =  dict(article)
        call = MongoProvider.ArticleCall()
        ret = call.updateEntireDocument(object_id, article_edit_dict)

    return dumps(dict(validation))

@bottle.route('/Articles/<object_id>/Comment', method=['POST'])
def createArticle(object_id):
    HttpHelper.setJsonContentType()

    user = HttpHelper.getSessionKey("logged_user")

    if(user is None):
        return dumps(dict(Validation.Validation(False, "You are not logged in")))

    comment_dict = HttpHelper.postBodyToDict()
    comment = Comment.Comment.getInstance(comment_dict)
    
    validation = comment.validate()
    if(validation.success == True):
        comment.setPublishTimeToNow()
        comment.setAuthor(user["oid"])
        comment.mongoSerialization(True)

        call = MongoProvider.ArticleCall()

        mongoArticles = call.getByID(object_id)
        mongoArticle = CollectionHelper.firstOrDefault(mongoArticles)
        if(mongoArticle is not None):
            article = Article.Article.getInstance(mongoArticle, True)
            article_comments = article.comments

            if(article_comments is None):
                article_comments = []

            article_comments.append(comment)
            article_comments_dicts = list(map(lambda x: dict(x), article_comments))

            call = MongoProvider.ArticleCall()
            ret = call.updateEntireDocument(object_id, {"comments": article_comments_dicts})

    return dumps(dict(validation))

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
        d = dict(User.User.getInstance(mongoUser))
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

