# coding: utf-8
from chat.handler import BaseHandler

class AuthHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        nickname = self.get_argument("nickname")
        email = self.get_argument("email")
        self.set_secure_cookie('email', email)
        self.set_secure_cookie('nickname', nickname)
        self.redirect("/chat")


