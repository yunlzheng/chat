# coding: utf-8
import os
from os.path import abspath, dirname

import tornado.web
import redis

from chat.handler import AuthHandler
from chat.handler import MainHandler
from chat.handler import WebSocketHandler
from chat.define import _CHANNEL
from chat.core import Listener

__author__ = 'zheng'
PROJECT_DIR = dirname(dirname(abspath(__file__)))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')


class Application(tornado.web.Application):

    def __init__(self):

        r = redis.Redis(host="localhost", db=2)
        client = Listener(r, [_CHANNEL])
        client.start()

        handlers = [
            (r"/", AuthHandler),
            (r"/chat", MainHandler),
            (r'/websocket', WebSocketHandler)
        ]

        settings = dict(
            template_path=TEMPLATE_DIR,
            static_path= STATIC_DIR,
            login_url= "/",
            debug= True,
            redis= r,
            cookie_secret="123456"
        )

        tornado.web.Application.__init__(self, handlers, **settings)


