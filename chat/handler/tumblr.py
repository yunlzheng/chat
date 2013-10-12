#coding: utf-8
__author__ = 'zheng'
import re
import tornado.gen
from tornado.httpclient import AsyncHTTPClient
from BeautifulSoup import BeautifulSoup
from chat.handler import BaseHandler


class TumblrHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        http_client = AsyncHTTPClient()
        http_response = yield http_client.fetch("https://www.tumblr.com/")
        content = http_response.body
        soup = BeautifulSoup(content)
        img = soup.findAll('img')[0]
        pattern=re.compile(r"""<img\s.*?\s?src\s*=\s*['|"]?([^\s'"]+).*?>""",re.I)
        m = pattern.findall(str(img))
        self.write(m[0])