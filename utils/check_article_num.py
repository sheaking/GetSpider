# -*- coding: utf-8 -*-
from handle_mysql import MySQL
import json

def check_num(column_id):
    '''
    检测指定column_id的文章是否缺失
    :param column_id:
    :return:
    '''
    mysql = MySQL()
    try:
        mysql.get_connection()
        ids = mysql.select('article_column', ['article_id'], 'column_id=%s' % column_id)
        print(ids)

        def f(x):
            return x[0]
        ids = list(map(f, ids))
        print(ids)

        # 找到第一篇的id
        for id in ids:
            r = mysql.select('ext_attribute', ['attribute_value'], "attribute_name = 'prev_article_id' and attribute_value = '0' and article_id = %s" % id)
            if r:
                first_id = id
                break

        token = True
        for i in range(400):
            # 查找当前id的下一篇id
            r = mysql.select('ext_attribute', ['attribute_value'], "attribute_name = 'next_article_id' and article_id = %s" % first_id)
            if not r:
                break
            if int(r[0][0]) == 0:
                token = False
                break
            # 检查下一篇id的文章是否存在
            r2 = mysql.select('article', ['article_id'], "article_id = %s" % r[0][0])
            # 如果不存在
            if not r2:
                break
            first_id = r[0][0]

        # 这个first_id的下一篇就没有
        if token:
            print('这篇id为：%s的下一篇文章不存在！' % first_id)
        else:
            print('没有不存在的文章！')


        problem_list = []

        # for result in select_results:
        #     try:
        #         contents = json.loads(result[1])
        #     except:
        #         problem_list.append(result[0])
        # if problem_list:
        #     print('出现问题的文章id：', problem_list)
        # else:
        #     print('没有文章出现问题')
    finally:
        mysql.close_connection()


if __name__ == '__main__':
    # 熊怡书院
    # check_num('222826')
    # 第一季
    # check_num('634923')
    # 第二季
    check_num('635063')