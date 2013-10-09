# coding: utf-8
import os
import redis
import tornado.web
import tornado.websocket
import tornado.ioloop
from tornado.options import options, define
from chat import Application
from chat.chat import _CHANNEL
from chat.core.listener import Listener

__author__ = 'zheng'

if __name__ == '__main__':

    r = redis.Redis(host="localhost", db=2)
    client = Listener(r, [_CHANNEL])
    client.start()

    port = os.environ.get("PORT", options.port)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
