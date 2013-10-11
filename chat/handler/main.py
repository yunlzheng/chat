# coding: utf-8
import json
import tornado.web
from tornado.options import options
from chat.util import getAvatar
from chat.handler import BaseHandler
from chat.util.tumblr import Tumblr


class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        tumblr = Tumblr()
        self.back_image = tumblr.get_fullbackground()
        email = self.get_secure_cookie('email')
        nickname = self.get_secure_cookie('nickname')
        params = {
            "avatar": getAvatar(email, name=nickname),
            "email": email,
            "nickname": nickname,
            "clients": [],
            "background": self.back_image
        }
        self.render("index.html", **params)

    @tornado.web.authenticated
    def post(self):
        message = self.get_argument("data")
        to = self.get_argument("to")
        data = {
            "email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname'),
            "avatar": getAvatar(self.get_secure_cookie('email')),
            "message": message,
            "to": to,
            "type": "normal"
        }
        r = self.settings['redis']
        r.publish(options.redis_channel, json.dumps(data))
