# coding: utf-8
import json
import tornado.web

from chat.util import getAvatar
from chat.handler.base import BaseHandler
from chat.chat import _CLIENTS_MAP, _CHANNEL


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        email = self.get_secure_cookie('email')
        self.render("index.html", clients = _CLIENTS_MAP, email=email)

    @tornado.web.authenticated
    def post(self):
        message = self.get_argument("data")
        data = {
            "email":self.get_secure_cookie('email'),
            "nickname":self.get_secure_cookie('nickname'),
            "avatar":getAvatar(self.get_secure_cookie('email')),
            "message":message,
            "type":"normal"
        }
        r = self.settings['redis']
        r.publish(_CHANNEL, json.dumps(data))
