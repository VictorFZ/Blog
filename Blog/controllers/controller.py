import os
import json
import codecs
import pprint
import bottle
from bottle import Bottle, request, response, run
from beaker.middleware import SessionMiddleware
from bson import Binary, Code
from bson.json_util import dumps
import Entities
import MongoProvider
import CollectionHelper

session_opts = {
    'session.type': 'memory',
    'session.cookie_expires': 300,
    'session.auto': True
}

app = SessionMiddleware(bottle.app(), session_opts)
pp = pprint.PrettyPrinter(indent=4)

@bottle.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

def setJsonContentType():
    response.content_type = 'application/json'

@bottle.route('/Articles', method=['GET'])
def getArticles():
    setJsonContentType()

    call = MongoProvider.ArticleCall()

    mongoArticles = call.get()
    articles = map(lambda x: Entities.Article.getInstance(x), mongoArticles)
    dicts = map(lambda x: dict(x), articles)

    return dumps(dicts)

@bottle.route('/Articles/<object_id>', method=['GET'])
def getArticle(object_id):
    setJsonContentType()

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
    setJsonContentType()
    article_dict = postBodyToDict()

    article = Entities.Article()
    article.fromDictionary(article_dict)
    article.ignoreIDSerialization()

    call = MongoProvider.ArticleCall()
    call.insert(dict(article))

    return dumps("true")

@bottle.route('/Users', method=['GET'])
def getUsers():
    setJsonContentType()

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

if __name__ == '__main__':
    bottle.run(
    app=app,
    host='localhost',
    port=8080,
    debug=True,
    reloader=True
)
