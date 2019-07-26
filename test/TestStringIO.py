# -*- coding: utf-8 -*-

import json
from io import StringIO

# dic = {
#     'key1':1,
#     'key2':[1,'2',4]
# }
#
# f = StringIO()
# js = json.dumps(dic)
# print(js)
# f.write(js)
#
#
# js = f.getvalue()
# print(js)
#
# js = json.loads(js)
# print(js)
#
# print('asdf'+'111')
#
# print('a' + str('asdf'))
#
#
# l = "font-family:'\@Songti SC';"
# l = l.replace('\\@','')
# print(l)


l = '''{"type": "quoted", "value": ["你好，欢迎来到《心理学基础30讲》，我是刘嘉。<br><br>这一讲，我继续带你回顾关于"现代人心理五宗罪"的直播内容，来跟你聊一聊拖延症的问题。<br><br>我相信你在工作中一定碰到过这样的问题：<br><br>为什么时间越紧迫，截止时间越接近，我反而越浪费时间？<br>为什么越是指责自己，就越是拖延？<br>为什么我的拖延症越来越严重？<br><br>通过今天这一讲，我想让你了解究竟是什么导致了拖延症，以及可以通过什么方法来治好它。<br>"]}'''

import re
print(re.findall(r': (.*?)', l))

import datetime
import time
print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


