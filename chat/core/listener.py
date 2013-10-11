# coding:utf-8
import json
import threading
from chat.define import ChatSigletonDefine


class Listener(threading.Thread):

    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):

        data = item['data']
        try:
            data = json.loads(data)
            if data.get('to'):
                self.send_to(data.get('email'), data.get('to'), data)
            else:
                self.send_to_all(data)
        except Exception as ex:
            print ex

    def get_client_by_email(self, email=None):
        if not email:
            raise ValueError('email must be private')

        clients = ChatSigletonDefine._instance.clients
        for key in clients.keys():
            client = clients[key]
            if client.email == email:
                return client

    def get_client_by_id(self, id):
        return ChatSigletonDefine._instance.clients[id]

    def send_to(self, source, to, data):

        from_client = self.get_client_by_email(source)
        to_client = self.get_client_by_id(to)
        try:
            # 发送信息给发送者和接受者
            data['from'] = from_client.id
            # 当自己给自己发送消息时
            if from_client.id==to_client.id:
                to_client.websocket_handler.write_message(json.dumps(data))
            else:
                to_client.websocket_handler.write_message(json.dumps(data))
                from_client.websocket_handler.write_message(json.dumps(data))


        except Exception as ex:
            print ex

    def send_to_all(self,data):

        """
        向所有链接到当前服务器的客户端发送信息
        @param message:
        """
        clients = ChatSigletonDefine._instance.clients
        for key in clients.keys():
            try:
                clients[key].websocket_handler.write_message(json.dumps(data))
            except Exception as ex:
                print "send message error happend {0}".format(ex)

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                break
            else:
                self.work(item)
