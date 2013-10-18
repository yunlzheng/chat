## What Is Tornado WebChat

[![Build Status](https://travis-ci.org/yunlzheng/chat.png?branch=master)](https://travis-ci.org/yunlzheng/chat)
基于tornado websocket的web聊天应用,底层使用了redis的发布/订阅机制

## Browser Support

* chrome
* safari
* firefox

## Dependences

### Runtime

   * Ubuntu 12.04
   * Python 2.7+

### Python Packages

   * BeautifulSoup==3.2.1
   * redis==2.8.0
   * tornado==3.1.1

## How To Install

1. install python dependences


    ```bash
    pip install -r requirements.txt
    ```

2. install redis server

    ```bash
    sudo apt-get install redis-server
    ```

3. configuration


    ```bash
    vim $PROJECT_HOME/conf/application.conf
    ```

    ```
    redis_host = "YOUR REDIS SERVER IP"
    ```

    ```
    redis_db = 'REDIS DB'
    ```

    ```
    redis_channel = "YOUR SUB/PUB CHANNEL"
    ```

4. run server

    ```bash
    python server.py
    ```

## Screenshot

1. 登录页面

![screenshot](https://raw.github.com/yunlzheng/chat/master/static/images/login.png)

2. 聊天页面

![screenshot](https://raw.github.com/yunlzheng/chat/master/static/images/chat.png)

## Changelog

* 群聊功能
* ctrl+enter 快捷键发送消息
* [emoji](http://www.emoji-cheat-sheet.com/) 表情支持（这个非常有趣）
* 添加私聊功能
* 使用脚本动态抓取[tumblr](https://www.tumblr.com/)登录页面的背景图片，应用到系统页面（借用）
* 使用github Identicons服务生成动态头像
* 添加了消息提示功能，主要包括[desktop notification](http://developer.chrome.com/extensions/notifications.html)桌面通知，Html audio播放提示音， 以及未读消息提示
* 解决同一用户打开多个浏览器窗口导致的问题

## TODOS

* 如果没有聊天记录，Who才知道你一天到晚说了些什么东西
* 如果没有用户管理，鬼才能知道那些是你说的～
* 某人说只能发文字，发表情都OUT了，还要能发图片
* 除了发图片以外，截图也是很牛叉的一个功能，当然还是必须要浏览器支持canvas才行









