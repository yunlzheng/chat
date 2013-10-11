# coding: utf-8
import urllib
import hashlib
import re

def getAvatar(email, name='majia', default=None, size=100):

    if default:
        return default
    else:
        zhPattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = zhPattern.search(name)
        if match:
            name = email.replace("@", "").replace(".", "").strip()
        # construct the url
        name = name[0:4]
        default = "https://identicons.github.com/"+name+".png"
        print default
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
        return gravatar_url