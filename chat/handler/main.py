# coding: utf-8
import json
import tornado.web
from tornado.options import options
from chat.util import getAvatar
from chat.handler import BaseHandler


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):

        email = self.get_secure_cookie('email')
        nickname = self.get_secure_cookie('nickname')
        params = {
            "avatar": getAvatar(email, name=nickname),
            "email": email,
            "nickname": nickname,
            "clients": []
        }
        self.render("index.html", **params)

    @tornado.web.authenticated
    def post(self):
        message = self.get_argument("data")
        to = self.get_argument("to")
        to_email = self.get_argument("to_mail")
        data = {
            "email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname'),
            "avatar": getAvatar(self.get_secure_cookie('email')),
            "message": message,
            "to": to,
            "to_email": to_email,
            "type": "normal"
        }
        r = self.settings['redis']
        r.publish(options.redis_channel, json.dumps(data))
