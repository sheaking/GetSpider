#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import shutil
'清空资源目录'

def clear_dir(dir):
    file_list = os.listdir(dir)
    for f in file_list:
        file_path = os.path.join(dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(str(file_path) + " removed!")
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path, True)
            print("dir "+ str(file_path) + " removed!")
    print('文件夹清空成功')

if __name__ == '__main__':
    clear_dir(os.path.abspath('resource'))