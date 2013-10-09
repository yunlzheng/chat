# coding: utf-8
import tornado.websocket
from tornado.log import app_log
from chat.model import Client
from chat.define import ChatSigletonDefine


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def initialize(self):
        self.channel = ChatSigletonDefine.get_singleton_instance().channel
        self.clients = ChatSigletonDefine.get_singleton_instance().clients
        print self.clients

    def open(self):

        _id = str(id(self))
        kwags = {
            "websocket_handler": self,
            "email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname')
        }
        client = Client(_id, **kwags)
        self.clients[_id] = client
        
    def send_to_all(self, message):
        r = self.settings['redis']
        r.publish(self.channel, message)

    def on_message(self, message):
        print message

    def on_close(self):
        try:
            print "current connection client: {0} ".format(self.clients)
            del self.clients[str(id(self))]
        except Exception as ex:
            print ex


