"""
Routes and views for the bottle application.
"""


import os
import json
import codecs
import pprint
import bottle
from bottle import Bottle, request, response, run, route, view
from datetime import datetime
from beaker.middleware import SessionMiddleware
from bson import Binary, Code
from bson.json_util import dumps
from entities import Entities
from providers import MongoProvider
from helpers import CollectionHelper, HttpHelper

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/contact')
@view('contact')
def contact():
    """Renders the contact page."""
    return dict(
        title='Contact',
        message='Your contact page.',
        year=datetime.now().year
    )

@route('/about')
@view('about')
def about():
    """Renders the about page."""
    return dict(
        title='About',
        message='Your application description page.',
        year=datetime.now().year
    )

@bottle.route('/Articles', method=['GET'])
def getArticles():
    HttpHelper.setJsonContentType()

    call = MongoProvider.ArticleCall()

    mongoArticles = call.get()
    articles = map(lambda x: Entities.Article.getInstance(x), mongoArticles)
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
        article = Entities.Article.getInstance(mongoArticle)
        return dumps(dict(article))

@bottle.route('/Articles', method=['POST'])
def createArticle():
    HttpHelper.setJsonContentType()
    article_dict = postBodyToDict()

    article = Entities.Article()
    article.fromDictionary(article_dict)
    article.ignoreIDSerialization()

    call = MongoProvider.ArticleCall()
    call.insert(dict(article))

    return dumps("true")

@bottle.route('/Users', method=['GET'])
def getUsers():
    HttpHelper.setJsonContentType()

    call = MongoProvider.UserCall()

    mongoUsers = call.get()
    users = map(lambda x: Entities.User.getInstance(x), mongoUsers)
    dicts = map(lambda x: dict(x), users)

    return dumps(dicts)

def postBodyToDict():
    reader = codecs.getreader("utf-8")
    obj = json.load(reader(request.body))
    body_dict = json.loads(json.dumps(obj))
    return body_dict
	#content = json.loads(body, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

def getSession():
    return bottle.request.environ.get('beaker.session')

def getSessionKey(key):
    session = getSession()
    if key in session.keys():
        return session[key]
    else:
        return None

def setSessionKey(key, value):
    session = getSession()
    session[key] = value