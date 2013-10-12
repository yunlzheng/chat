# coding: utf-8
import json
import tornado.websocket
from tornado.options import options
from tornado.log import app_log
from chat.model import Client
from chat.define import ChatSigletonDefine


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        clients = ChatSigletonDefine.get_singleton_instance().clients
        _id = str(id(self))
        kwargs = {
            "websocket_handler": self,
            "email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname')
        }
        client = Client(_id, **kwargs)
        clients[_id] = client
        data = {
            'type': 'add',
            'clients': []
        }
        for key in clients.keys():
            client = clients[key]
            data['clients'].append({
                "type": "add",
                "id": key,
                "nickname": client.nickname,
                "avatar": client.avatar,
                "email": client.email
            })
        self.send_to_all(json.dumps(data))

    def send_to_all(self, message):
        r = self.settings['redis']
        r.publish(options.redis_channel, message)

    def on_message(self, message):
        print message

    def on_close(self):
        clients = ChatSigletonDefine.get_singleton_instance().clients
        _id = str(id(self))
        del clients[_id]
        try:
            data = {
                "type": "out",
                "id": _id
            }
            self.send_to_all(json.dumps(data))
        except Exception as ex:
            app_log.exception(ex)




