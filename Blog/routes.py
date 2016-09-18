import os
import json
import bottle
from bottle import Bottle, request, response, run, route, view, static_file
from datetime import datetime
from beaker.middleware import SessionMiddleware
from bson import Binary, Code
from bson.json_util import dumps
from entities import Article, User, Validation, Comment, Category
from providers import MongoProvider
from helpers import CollectionHelper, HttpHelper, EncryptionHelper
from operator import attrgetter
import cgi
import re

path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)

@route('/')
@route('/home')
def home():
    return static_file("index.html", root=dir_path+'/'+'views/')

@route('/posts/<slug>')
def post_by_id(slug):
    return static_file("index.html", root=dir_path+'/'+'views/')

def getAllUsers():
    usercall = MongoProvider.UserCall()
    mongoUsers = usercall.get()
    users = list(map(lambda x: User.User.getInstance(x), mongoUsers))

    return users

@bottle.route('/Articles', method=['GET'])
def getArticles():
    HttpHelper.setJsonContentType()

    tag = request.query['tags']
    category  = request.query['categories']

    hasTags = tag.strip() != ""
    hasCategories = category.strip() != ""

    users = getAllUsers()
    call = MongoProvider.ArticleCall()

    mongoArticles = []
    if hasTags == False and hasCategories == False:
        mongoArticles = list(call.get())
    else:
        tagQuery = "true"
        categoryQuery = "true"

        if hasTags == True:
            tagQuery = 'this.tags.map(function(t) {  return t.value; }).indexOf("' + tag + '") != -1'
        if hasCategories == True:
            categoryQuery = 'this.categories.map(function(t) {  return t.value; }).indexOf("' + category + '") != -1'

        mongoArticles = call.getByQuery({"$where": tagQuery + ' && ' + categoryQuery})

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

@bottle.route('/Articles/BySlug/<slug>', method=['GET'])
def getArticleBySlug(slug):
    HttpHelper.setJsonContentType()

    users = getAllUsers()
    call = MongoProvider.ArticleCall()

    mongoArticles = call.getByQuery({"slug": slug})
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

    call = MongoProvider.ArticleCall()
    mongoArticles = call.getByQuery({"slug": article.slug})
    mongoArticle = CollectionHelper.firstOrDefault(mongoArticles)
    if(mongoArticle is not None):
            return dumps(dict(Validation.Validation(False, "There is an article with same slug already")))

    validation = article.validate()
    if(validation.success == True):
        article.mongoSerialization()
        article.setPublishTimeToNow()
        article.setAuthor(user["oid"])
        article.text = formatTextHtml(article.text)
        ret = call.insert(dict(article))
        validation.id = str(ret.inserted_id)

    return dumps(dict(validation))

def formatTextHtml(text):
    escaped_text = cgi.escape(text, quote=True)
    newLine = re.compile('\r?\n')
    return newLine.sub("<p>", escaped_text)

@bottle.route('/Articles/<object_id>', method=['DELETE'])
def deleteArticle(object_id):
    HttpHelper.setJsonContentType()

    call = MongoProvider.ArticleCall()
    ret = call.delete(object_id)

    return dumps(True)

@bottle.route('/Articles/<object_id>', method=['POST'])
def updateArticle(object_id):
    HttpHelper.setJsonContentType()

    article_dict = HttpHelper.postBodyToDict()
    article = Article.Article.getInstance(article_dict)

    validation = article.validate()
    if(validation.success == True):
        article.mongoSerialization(True)
        article_edit_dict =  dict(article)
        call = MongoProvider.ArticleCall()
        article_edit_dict["text"] = formatTextHtml(article_edit_dict["text"])
        ret = call.updateEntireDocument(object_id, article_edit_dict)

    return dumps(dict(validation))

@bottle.route('/Articles/<object_id>/Comment', method=['POST'])
def createComment(object_id):
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

@bottle.route('/Categories', method=['GET'])
def getCategories():
    HttpHelper.setJsonContentType()

    call = MongoProvider.CategoryCall()

    mongoCategories = list(call.get())

    categories = list(map(lambda x: Category.Category.getInstance(x), mongoCategories))

    dicts = map(lambda x: dict(x), categories)

    return dumps(dicts)

@bottle.route('/Categories', method=['POST'])
def createCategory():
    HttpHelper.setJsonContentType()

    user = HttpHelper.getSessionKey("logged_user")

    if(user is None):
        return dumps(dict(Validation.Validation(False, "You are not logged in")))

    category_dict = HttpHelper.postBodyToDict()
    category = Category.Category.getInstance(category_dict)

    validation = category.validate()
    if(validation.success == True):
        category.mongoSerialization()

        call = MongoProvider.CategoryCall()
        ret = call.insert(dict(category))
        validation.id = str(ret.inserted_id)

    return dumps(dict(validation))

@bottle.route('/Categories/<object_id>', method=['DELETE'])
def deleteArticle(object_id):
    HttpHelper.setJsonContentType()

    call = MongoProvider.CategoryCall()
    ret = call.delete(object_id)

    return dumps(True)

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
