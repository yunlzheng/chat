# coding:utf-8
import threading
from chat.define import ChatSigletonDefine


class Listener(threading.Thread):

    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):

        clients = ChatSigletonDefine._instance.clients
        for key in clients.keys():
            try:
                clients[key].websocket_handler.write_message(item['data'])
            except Exception as ex:
                print "send message error happend {0}".format(ex)

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                break
            else:
                self.work(item)
