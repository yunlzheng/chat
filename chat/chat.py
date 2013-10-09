# coding: utf-8
import os
import tornado.web
from chat.handler import AuthHandler
from chat.handler import MainHandler
from chat.handler import WebSocketHandler

__author__ = 'zheng'
_CLIENTS_MAP = {}
_CHANNEL = "WEBSOCKET"
PROJECT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')


class Application(tornado.web.Application):

    def __init__(self):

        handlers = [
            (r"/", AuthHandler),
            (r"/chat", MainHandler),
            (r'/websocket', WebSocketHandler)
        ]

        settings = dict(
            template_path=TEMPLATE_DIR,
            static_path= STATIC_DIR,
            login_url="/",
            debug=True,
            redis=r,
            cookie_secret="123456"
        )

        tornado.web.Application.__init__(self, handlers, **settings)

