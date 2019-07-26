# -*- coding: utf-8 -*-
from handle_mysql import MySQL
import json


'''
检测文章中是否有不合法的文章，并生成文章id
'''
mysql = MySQL()
try:
    mysql.get_connection()

    select_results = mysql.select('article', ['article_id', 'article_content'], 'uploaded = 0')

    problem_list = []

    # type:"audio , audio:"
    # type:"image , src:"
    for result in select_results:
        try:
            contents = json.loads(result[1])
        except:
            problem_list.append(result[0])


    if problem_list:

        print('出现问题的文章id：', problem_list)
    else:
        print('没有文章出现问题')
finally:
    mysql.close_connection()