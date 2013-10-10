# coding: utf-8
__author__ = 'zheng'


class Singleton(object):

    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance


class ChatSigletonDefine(Singleton):

    _CLIENTS_MAP = {}
    _CHANNEL = "WEBSOCKET"

    @property
    def clients(self):
        return self._CLIENTS_MAP

    @property
    def channel(self):
        return self._CHANNEL

    @classmethod
    def get_singleton_instance(cls):
        return cls._instance
