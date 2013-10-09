# coding: utf-8
import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
from chat import Application


__author__ = 'zheng'

if __name__ == '__main__':

    port = os.environ.get("PORT", 8888)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
