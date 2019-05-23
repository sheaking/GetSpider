# -*- coding: utf-8 -*-
def generate_id(key):
    id = 0
    for index, s in enumerate(key):
        if index % 2:
            id += ord(s)
        else:
            id += ord(s) * 3
    return id