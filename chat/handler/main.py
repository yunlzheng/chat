# coding: utf-8
import json
import tornado.web
from tornado.options import options
from chat.util.gavatar import Gavatar
from chat.handler import BaseHandler


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        email = self.get_secure_cookie('email')
        nickname = self.get_secure_cookie('nickname')
        gavatar = Gavatar(email=email)
        params = {
            "avatar": gavatar.get_default_avatar(size=200),
            "email": email,
            "nickname": nickname,
            "clients": []
        }
        self.render("index.html", **params)

    @tornado.web.authenticated
    def post(self):
        message = self.get_argument("data")
        to_email = self.get_argument("to_mail")
        gavatar = Gavatar(email=self.get_secure_cookie('email'))
        data = {
            "from_email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname'),
            "avatar": gavatar.get_default_avatar(size=200),
            "message": message,
            "to_email": to_email,
            "type": "normal"
        }
        r = self.settings['redis']
        r.publish(options.redis_channel, json.dumps(data))
