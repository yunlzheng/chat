# coding: utf-8
from chat.model import Client
from chat.define import ChatSigletonDefine
__author__ = 'zheng'


class ClientManager(object):

    @classmethod
    def get_clients(cls):
        return ChatSigletonDefine.get_singleton_instance().clients

    @classmethod
    def add_client(cls, identity, nickname=None, email=None, websocket_handler=None):
        client = Client(identity, nickname=nickname, email=email, websocket_handler=websocket_handler)
        ChatSigletonDefine.get_singleton_instance().clients[identity] = client
        return client

    @classmethod
    def remove_client(cls, identity):
        clients = ClientManager.get_clients()
        del clients[identity]

    @classmethod
    def send_to_all(self, redis=None, channel=None, message=None):
        redis.publish(channel, message)

    @classmethod
    def is_client_connected(cls, email):
        """
        检查当前连接的客户端是否已经打开了多个浏览器窗口
        @param email: 用户登录用的电子邮箱地址
        """
        clients = ChatSigletonDefine.get_singleton_instance().clients
        for key in clients.keys():
            client = clients[key]
            if client.email == email:
                return True

        return False

