# coding: utf-8
import urllib, hashlib

def getAvatar(email, default=None, size=100):

    if default:
        return default
    else:
        # construct the url
        default = "http://pdflabs.herokuapp.com/static/images/avatar.jpg"
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url