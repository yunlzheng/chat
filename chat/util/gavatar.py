# coding: utf-8
import urllib
import hashlib
__author__ = 'zheng'


class Gavatar(object):

    def __init__(self, email):
        self.email = email;

    def get_default_avatar(self, size=200):
        name = self.email.replace("@", "").replace(".", "").strip()[0:1]
        default = "https://identicons.github.com/z{0}.png".format(name)
        gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d': default, 's': str(size)})
        return gravatar_url