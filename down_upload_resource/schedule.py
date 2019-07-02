
import os
from down_upload_resource.download_file import down_dedao
from down_upload_resource.upload_file import upload_file
from down_upload_resource.delete_dir import clear_dir
from handle_mysql import MySQL
import time

# 目前一下子下载20条数据，到resource文件夹中
down_dedao(12)

# 进行上传
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
            mysql.update('article', 'uploaded = 1', 'article_id = %s' % dir)
        except Exception as e:
            print(e)
            # 这里写到日志里面
            print('文章 %s 上传失败！' % dir)
    # 清空文件夹
    # clear_dir(os.path.abspath('resource'))
finally:
    mysql.close_connection()


# 清空resource文件夹
# clear_dir(os.path.abspath('resource'))

