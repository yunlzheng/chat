# coding: utf-8
import os
import json
import threading
import redis
import tornado.web
import tornado.websocket
import tornado.ioloop

from chat.util import getAvatar

__author__ = 'zheng'

PROJECT_DIR = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(PROJECT_DIR, 'templates')
STATIC_DIR = os.path.join(PROJECT_DIR, 'static')

CLIENTS_MAP = {}
CHANNEL = "WEBSOCKET"

class Client():

    def __init__(self, id, nickname="匿名", email='', webSocketHandler=None):
        self.id = id
        self.webSocketHandler = webSocketHandler
        self.nickname = nickname
        self.email = email
        self.avatar = getAvatar(self.email)

class Listener(threading.Thread):

    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def work(self, item):
        print item
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

class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("email")


class AuthHandler(BaseHandler):

    def get(self):
        self.render("login.html")

    def post(self):
        nickname = self.get_argument("nickname")
        email = self.get_argument("email")
        self.set_secure_cookie('email',email)
        self.set_secure_cookie('nickname', nickname)
        self.redirect("/chat")

class MainHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        email = self.get_secure_cookie('email')
        self.render("index.html", clients = CLIENTS_MAP, email=email)

    @tornado.web.authenticated
    def post(self):
        message = self.get_argument("data")
        data = {
            "email":self.get_secure_cookie('email'),
            "nickname":self.get_secure_cookie('nickname'),
            "avatar":getAvatar(self.get_secure_cookie('email')),
            "message":message,
            "type":"normal"
        }
        r = self.settings['redis']
        r.publish(CHANNEL, json.dumps(data))

class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        _id = str(id(self))
        kwags = {
            "webSocketHandler": self,
            "email": self.get_secure_cookie('email'),
            "nickname": self.get_secure_cookie('nickname')
        }
        client = Client(_id, **kwags)
        CLIENTS_MAP[_id] = client
        #self.write_message("欢迎进入聊天室！")

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
        login_url="/",
        debug=True,
        redis=r,
        cookie_secret="123456"
    )
    application = tornado.web.Application([
        (r"/", AuthHandler),
        (r"/chat", MainHandler),
        (r'/websocket', WebSocketHandler)
    ], **settings)

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()