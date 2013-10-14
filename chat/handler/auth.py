# coding: utf-8
import tornado.web
from chat.handler import BaseHandler
from chat.core.manager import ClientManager


class AuthHandler(BaseHandler):

    def initialize(self):
        pass

    def get(self):
        if self.get_current_user():
            self.redirect("/chat");
        else:
            self.render("login.html", error=None)

    def post(self):
        nickname = self.get_argument("nickname")
        email = self.get_argument("email")
        if ClientManager.get_client_by_email(email):
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
        # TODO: 用户退出登录后需关闭websocket连接
        self.clear_cookie("nickname")
        self.clear_cookie("email")
        self.redirect("/")


