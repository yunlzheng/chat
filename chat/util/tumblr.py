# coding: utf-8
import urllib2
import re
import argparse
from BeautifulSoup import BeautifulSoup

__author__ = 'zheng'


class Tumblr(object):

    def __init__(self):
        self.ns = 'NAMESERVER'

    def _getSoup(self, url):
        req = urllib2.Request(
            url = url,
            headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4'}
        )
        content = urllib2.urlopen(req).read()
        return BeautifulSoup(content)

    def _getItem(self, soup):
        imgList = soup.findAll('img', attrs={'src'})
        return imgList[0]

    def get_fullbackground(self):
        url = "https://www.tumblr.com/"
        self.soup = self._getSoup(url)
        return self._getItem(self.soup)


if __name__=="__main__":
    tumblr = Tumblr()
    print tumblr.get_fullbackground()
