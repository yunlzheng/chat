# coding: utf-8
import os
from os.path import abspath, dirname

import redis
import tornado.httpserver
import tornado.web
from tornado.log import app_log
from tornado.options import define, options
from chat.router import handlers
from chat.core import Listener

__author__ = 'zheng'
PROJECT_DIR = dirname(dirname(abspath(__file__)))
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')
CONF_DIR = os.path.join(PROJECT_DIR, 'conf')
CONF_FILE = CONF_DIR+os.path.sep+"application.conf"

define('redis_host', default='localhost')
define('redis_db', default=2, type=int)
define('redis_channel', default='web_chat', help='message pubsub channel')
define("debug", default=False, type=bool)
define("port", default=8888, type=int)


class Application(tornado.web.Application):

    _CLIENTS_MAP = {}

    def __init__(self):

        r = redis.Redis(host=options.redis_host, db=options.redis_db)
        client = Listener(r, [options.redis_channel])

        client.start()
        settings = dict(
            template_path=TEMPLATE_DIR,
            static_path=STATIC_DIR,
            login_url="/",
            debug=options.debug,
            redis=r,
            cookie_secret="123456"
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def run():
    """
    start chat application

    """
    tornado.options.parse_command_line()
    tornado.options.parse_config_file(CONF_FILE)
    port = os.environ.get("PORT", options.port)
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(port)
    app_log.info("application run on {0}".format(port))
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    application = Application()



