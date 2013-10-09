# coding: utf-8
import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
from chat import Application
from chat.define import ChatSigletonDefine

__author__ = 'zheng'

if __name__ == '__main__':

    ChatSigletonDefine()
    application = Application()
    port = os.environ.get("PORT", 8888)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
