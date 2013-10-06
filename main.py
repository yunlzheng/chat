# coding: utf-8
import os
import os.path
import threading
import redis
import tornado.web
import tornado.websocket
import tornado.ioloop

__author__ = 'zheng'

PROJECT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')

CLIENTS_MAP = {}
CHANNEL = "WEBSOCKET"

class Client():

    def __init__(self, id, nickname="匿名", webSocketHandler=None):
        self.id = id
        self.webSocketHandler = webSocketHandler
        self.nickname = nickname

class Listener(threading.Thread):

    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        print item
        print item['channel'], ":", item['data']
        for key in CLIENTS_MAP.keys():
            CLIENTS_MAP[key].webSocketHandler.write_message(item['data'])

    def run(self):
        for item in self.pubsub.listen():
            if item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print self, "unsubscribed and finished"
                break
            else:
                self.work(item)

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html", clients = CLIENTS_MAP)

    def post(self):
        data = self.get_argument("data")
        r = self.settings['redis']
        r.publish(CHANNEL, str(id(self))+":"+data)

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        _id = str(id(self))
        client = Client(_id, webSocketHandler=self)

        CLIENTS_MAP[_id] = client
        self.write_message("欢迎进入聊天室！")

    def send_to_all(self, message):
        r = self.settings['redis']
        r.publish(CHANNEL, message)

    def on_message(self, message):
        print message

    def on_close(self):
        del CLIENTS_MAP[str(id(self))]

if __name__ == '__main__':

    r = redis.Redis(host="192.168.1.111", db=2)
    client = Listener(r, [CHANNEL])
    client.start()
    settings = dict(
        template_path=TEMPLATE_DIR,
        static_path= STATIC_DIR,
        login_url="/sigin",
        debug=True,
        redis=r
    )
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r'/websocket', WebSocketHandler)
    ], **settings)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()