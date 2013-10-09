# coding: utf-8
import json
import tornado.web

from chat.define import _CLIENTS_MAP, _CHANNEL
from chat.util import getAvatar
from chat.handler import BaseHandler


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        email = self.get_secure_cookie('email')
        params = {
            "avatar": getAvatar(self.get_secure_cookie('email')),
            "email": email,
            "nickname": self.get_secure_cookie('nickname'),
            "clients": _CLIENTS_MAP
        }
        self.render("index.html", **params)

    @tornado.web.authenticated
    def post(self):
        message = self.get_argument("data")
        data = {
            "email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname'),
            "avatar": getAvatar(self.get_secure_cookie('email')),
            "message": message,
            "type": "normal"
        }
        r = self.settings['redis']
        r.publish(_CHANNEL, json.dumps(data))
