# coding: utf-8
from chat.util.gavatar import Gavatar


class Client():

    def __init__(self, id, nickname="匿名", email='', websocket_handler=None):
        self.id = id
        self.websocket_handler = websocket_handler
        self.nickname = nickname
        self.email = email
        self.avatar =  Gavatar(email).get_default_avatar()

    def __str__(self):
        return self.id
