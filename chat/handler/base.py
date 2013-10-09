# coding: utf-8
import tornado.web
__author__ = 'zheng'


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("email")
