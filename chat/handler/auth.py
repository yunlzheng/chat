# coding: utf-8
import tornado.web
from chat.handler import BaseHandler
from chat.define import ChatSigletonDefine
from chat.util.tumblr import Tumblr


class AuthHandler(BaseHandler):

    def initialize(self):
        #tumblr = Tumblr()
        #self.back_image = tumblr.get_fullbackground()
        pass

    def get(self):
        self.render("login.html", error=None)

    def post(self):
        nickname = self.get_argument("nickname")
        email = self.get_argument("email")
        clients = ChatSigletonDefine.get_singleton_instance()._CLIENTS_MAP
        for key in clients.keys():
            if clients[key].email == email:
                self.render("login.html", error="邮箱正在使用中...", background = None)
        self.set_secure_cookie('email', email)
        self.set_secure_cookie('nickname', nickname)
        self.redirect("/chat")


class LogoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        """
        退出登录，清除当前cookie值

        """
        self.clear_cookie("nickname")
        self.clear_cookie("email")
        self.redirect("/")


