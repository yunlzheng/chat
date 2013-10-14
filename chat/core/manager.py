# coding: utf-8
import json
from tornado.log import app_log
from chat.model import Client
__author__ = 'zheng'


class ClientManager(object):

    _CLIENTS_MAP = {}

    @classmethod
    def get_clients(cls):
        """
        获取当前连接的clients

        @return:
        """
        return cls._CLIENTS_MAP

    @classmethod
    def get_client_by_email(cls, email):
        """
        根据websocket handler id获取当前连接client
        @param identity:
        @return:
        """
        app_log.info("current clients {0}".format(cls.get_clients()))
        try:
            client = cls._CLIENTS_MAP[email]
            return client
        except Exception as ex:
            return None

    @classmethod
    def add_client(cls, identity, nickname=None, email=None, handler=None):
        """
        添加新的client
        @param identity: websocket handler 编号
        @param nickname: 用户昵称
        @param email: 用户邮箱地址 唯一值
        @param handler : websocket handler实例对象
        @return:
        """
        client = Client(identity, nickname=nickname, email=email, handler=handler)
        cls._CLIENTS_MAP[email] = client
        return client

    @classmethod
    def remove_client(cls, email):
        """
        移除client
        @param email:
        """
        app_log.debug("remove client[{0}]".format(email))
        del cls._CLIENTS_MAP[email]

    @classmethod
    def send_to_all(cls, data):

        """
        向所有链接到当前服务器的客户端发送信息
        @param data:
        """
        clients = cls.get_clients()
        for key in clients.keys():
            try:
                clients[key].handler.write_message(json.dumps(data))
            except Exception as ex:
                app_log.exception(ex)

    @classmethod
    def send_to(cls, from_email, to_email, data):

        """
        向特定用户发送消息
        @param source_email: 发送者邮箱
        @param to_email: 接受者邮箱地址
        @param data:
        """
        from_client = cls.get_client_by_email(from_email)
        to_client = cls.get_client_by_email(to_email)
        try:
            # 当自己给自己发送消息时
            if from_email == to_email:
                to_client.handler.write_message(json.dumps(data))
            else:
                to_client.handler.write_message(json.dumps(data))
                from_client.handler.write_message(json.dumps(data))
        except Exception as ex:
            app_log.exception()

    @classmethod
    def publish(cls, redis=None, channel=None, message=None):
        redis.publish(channel, message)

    @classmethod
    def is_client_connected(cls, email):
        """
        检查当前连接的客户端是否已经打开了多个浏览器窗口
        @param email: 用户登录用的电子邮箱地址
        """
        try:
            client = cls.get_client_by_email(email)
            if client:
                return True
        except Exception as ex:
            return False



