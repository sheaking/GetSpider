#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import os
import re
from utils.id_util import generate_id
from utils.parse_content import *
from handle_mysql import MySQL
import time
import mitmproxy.http
from mitmproxy import ctx
from utils.handle_yaml import WriteUserCommand

class Counter():
    def __init__(self):
        self.num = 0
        self.wuc = WriteUserCommand()

    def response(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)
        self.wuc.write_data(self.num)
        #显示所有栏目列表发送的请求
        #这里要防止把之前的清空
        # if 'entree.igetget.com/purchased/v2/product/allList' in flow.request.url:
        if 'igetget.com/ddarticle/v1/article/get' in flow.request.url:
            pass



addons = [
    Counter()
]