# coding: utf-8
from chat.handler import AuthHandler
from chat.handler import LogoutHandler
from chat.handler import MainHandler
from chat.handler import WebSocketHandler
from chat.handler import TumblrHandler
__author__ = 'zheng'

handlers = [
    (r"/", AuthHandler),
    (r"/logout", LogoutHandler),
    (r"/chat", MainHandler),
    (r'/websocket', WebSocketHandler),
    (r'/background', TumblrHandler)
]
