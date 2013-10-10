# coding: utf-8
import json
import tornado.websocket
from tornado.options import options
from chat.model import Client
from chat.define import ChatSigletonDefine


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def initialize(self):
        self.channel = options.redis_channel
        self.clients = ChatSigletonDefine.get_singleton_instance().clients
        print self.clients

    def open(self):

        _id = str(id(self))
        print "1 on_open current add client {0}".format(_id)
        kwags = {
            "websocket_handler": self,
            "email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname')
        }
        client = Client(_id, **kwags)
        self.clients[_id] = client
        data = {
            "type": "add",
            "id": _id,
            "nickname": client.nickname,
            "avatar": client.avatar
        }
        self.send_to_all(json.dumps(data))
        print "2 on_open current add client {0}".format(_id)
        print "on_open current connection client: {0} ".format(self.clients)

    def send_to_all(self, message):
        r = self.settings['redis']
        r.publish(self.channel, message)

    def on_message(self, message):
        print message

    def on_close(self):

        _id = str(id(self))

        try:
            del self.clients[_id]
            data = {
                "type": "out",
                "id": _id
            }
            self.send_to_all(json.dumps(data))
            print "on_close: {0}".format()

        except Exception as ex:
            print ex


