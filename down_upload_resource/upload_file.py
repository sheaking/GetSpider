# !/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import base64
import os
import time
from handle_mysql import MySQL
from down_upload_resource.delete_dir import clear_dir
# 返回上传的地址，输入路径吧
# 方案，先下载到本地，然后上传，下载着上传着
# 上传一篇文章的所有信息，或者上传一个目录下的所有文件

'上传资源'

def upload_file(path,current_count = 1,max_retry_count = 3):
    '''
    :param path: 上传的文件路径
    :param current_count: 当前上传次数
    :param max_retry_count: 最大重试数
    :return: 返回上传成功后的访问路径
    '''
    if current_count <= max_retry_count:
        try:
            token_url = "http://qiniu.systoon.com/getToken.php"
            DOMAIN = "http://apr.qiniu.toon.mobi/"
            token = requests.get(token_url)
            l = os.path.getsize(path)
            file_name = os.path.split(path)[1]

            current_stamp = file_name[:file_name.rfind('.')]
            # en_utf8 = str(current_stamp).encode('utf-8')
            #
            # # key是根据当前时间生成的，不可能重复，但是也不可能通过计算得到
            # # 那我增量爬虫的时候怎么办？增量爬的时候把url进行过滤即可，那么也不会上传重复文件了
            # key = str(base64.urlsafe_b64encode(en_utf8)).replace('\'', '')[1:]
            key = current_stamp
            key2 = str(base64.urlsafe_b64encode(key.encode('utf-8'))).replace('\'', '')[1:]

            url = "http://upload.qiniup.com/putb64/" + str(l) + "/key/" + key2
            headers = {
                "Content-Type": "application/octet-stream",
                "Authorization": "UpToken " + token.text
            }
            with open(path, 'rb') as f:
                src = f.read()
                file64 = str(base64.b64encode(src)).replace('\'', '')[1:]
            r = requests.post(url, headers=headers, data=file64)
            # 如果上传返回的状态码不为200，就抛出异常
            if r.status_code != 200:
                raise Exception('上传状态码不为200，为 %s' % r.status_code)
            print('文件 %s 上传成功：%s' % (path,DOMAIN + key))
            return DOMAIN + key

        except Exception as e:
            print(e)
            print('文件 %s 再次上传，上传次数为 %s' % (path,current_count))
            return upload_file(path, current_count + 1, max_retry_count)

    else:
        print('文件 %s 上传次数超过 %s ,上传失败！' % (path, max_retry_count))
        # 上传3次都没有上传成功就抛出异常
        raise Exception('文件 %s 上传次数超过 %s ,上传失败！' % (path, max_retry_count))

if __name__ == '__main__':
    mysql = MySQL()
    mysql.get_connection()
    try:
        print(os.path.abspath('resource'))
        dir_list = os.listdir(os.path.abspath('resource'))
        # 每个dir就是一个文章的所有资源
        for dir in dir_list:
            try:
                dir_path = os.path.join(os.path.abspath('resource'), dir)
                file_list = os.listdir(dir_path)
                for file in file_list:
                    file_path = os.path.join(dir_path, file)
                    # 上传,如果上传失败就重复试3次
                    upload_file(file_path)
                    # time.sleep(1)
                # 该文章upload字段更新,更新为已上传成功
                mysql.update('article', 'avatar_uploaded = 1', 'article_id = %s' % dir)
            except Exception as e:
                print(e)
                # 这里写到日志里面
                print('文章 %s 上传失败！' % dir)
        # 清空文件夹
        # clear_dir(os.path.abspath('resource'))
    finally:
        mysql.close_connection()

    # upload_file()