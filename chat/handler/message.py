# coding: utf-8
import json
import tornado.websocket
from tornado.options import options
from tornado.log import app_log
from chat.core.manager import ClientManager


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        """
        1, 检查当前客户端时候已经打开浏览器窗口，是，发送错误提示信息
        """
        email = self.get_secure_cookie('email')
        nickname = self.get_secure_cookie('nickname')
        if ClientManager.is_client_connected(email):
            pass
        else:
            clients = ClientManager.get_clients()
            # 保存客户端信息
            ClientManager.add_client(str(id(self)), nickname=nickname, email=email, websocket_handler=self)
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

    def on_message(self, message):
        print message

    def on_close(self):

        _id = str(id(self))
        ClientManager.remove_client(_id)
        try:
            data = {
                "type": "out",
                "id": _id
            }
            self.send_to_all(json.dumps(data))
        except Exception as ex:
            app_log.exception(ex)

    def send_to_all(self, data):
        ClientManager.send_to_all(self.settings['redis'], options.redis_channel, data)





