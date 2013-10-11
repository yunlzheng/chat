# coding: utf-8
import os
import tornado.options
import tornado.web
import tornado.ioloop
import tornado.httpserver
from chat import Application
from chat.app import CONF_FILE
from chat.define import ChatSigletonDefine

__author__ = 'zheng'

if __name__ == '__main__':

    ChatSigletonDefine()
    tornado.options.parse_command_line()
    tornado.options.parse_config_file(CONF_FILE)
    application = Application()
    port = os.environ.get("PORT", 8888)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()
