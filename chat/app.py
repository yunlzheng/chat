# coding: utf-8
import os
from os.path import abspath, dirname

import tornado.web
import redis
from chat.router import handlers
from chat.core import Listener
from chat.define import ChatSigletonDefine

__author__ = 'zheng'
PROJECT_DIR = dirname(dirname(abspath(__file__)))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')


class Application(tornado.web.Application):

    _CLIENTS_MAP = {}

    def __init__(self):

        r = redis.Redis(host="localhost", db=2)
        channel = ChatSigletonDefine.get_singleton_instance().channel
        client = Listener(r, [channel])
        client.start()
        settings = dict(
            template_path=TEMPLATE_DIR,
            static_path=STATIC_DIR,
            login_url="/",
            debug=True,
            redis=r,
            cookie_secret="123456"
        )
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    application = Application()



