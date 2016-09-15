import codecs
import json
import bottle
from bottle import request, response, run
from beaker.middleware import SessionMiddleware

def setJsonContentType():
    response.content_type = 'application/json'

def postBodyToDict():
    reader = codecs.getreader("utf-8")
    obj = json.load(reader(request.body))
    body_dict = json.loads(json.dumps(obj))
    return body_dict

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

def removeSession():
    session = getSession()
    session.delete()

def getSessionUsername():
    session = getSession()