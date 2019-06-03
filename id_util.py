# -*- coding: utf-8 -*-
# 生成得到app的id规则
def generate_id(key):
    id = 0
    for index, s in enumerate(key):
        if index % 2:
            id += ord(s)
        else:
            id += ord(s) * 3
    return id