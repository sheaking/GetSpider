#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import pickle
import os
import re
import sys
sys.path.append('../')
from handle_mysql import MySQL

def response(flow):
    # 该文章的评论
    # https://entree.igetget.com/bauhinia/v1/article/info
    if 'igetget.com/ledgers/notes/article_comment_list' in flow.request.url:

        content = json.loads(flow.response.text)

        # 如果有更多评论，就取出拼接再放入
        if content['c']['isMore']:
            if not os.path.exists('../temp_file/5.txt') or os.path.getsize('../temp_file/5.txt') == 0:
                with open('../temp_file/5.txt', 'wb') as f:
                    pickle.dump(content, f)
            else:
                print('之前大小：', os.path.getsize('../temp_file/5.txt'),)

                with open('../temp_file/5.txt', 'rb') as f:
                    temp = pickle.load(f)

                with open('../temp_file/5.txt', 'wb') as f:
                    f.truncate()

                print('中间大小：', os.path.getsize('../temp_file/5.txt'))
                temp['c']['list'] = temp['c']['list'] + content['c']['list']
                with open('../temp_file/5.txt', 'wb') as f:
                    pickle.dump(temp, f)
                print('之后大小：', os.path.getsize('../temp_file/5.txt'))

        # 如果就一条或者最后一条
        else:
            # 从文件取出，存入数据库，得到文章id，一起存入数据库
            # 如果这是最后一条
            request = flow.request
            print(request.content)
            bys = request.content
            s = '&' + bys.decode('utf-8') + '&'
            page_search = re.compile(r"&page=(.*?)&")
            page = re.search(page_search, s).groups(1)

            page_count_search = re.compile(r"&page_count=(.*?)&")
            page_count = re.search(page_count_search, s).groups(1)

            article_id_search = re.compile(r"&article_id=(.*?)&")
            article_id = re.search(article_id_search, s).groups(1)

            print(page[0],page_count[0],article_id[0])

            if os.path.getsize('../temp_file/5.txt'):
                print('最后一条')
                with open('../temp_file/5.txt', 'rb') as f:
                    temp = pickle.load(f)
                temp['c']['list'] = temp['c']['list'] + content['c']['list']
                print('一共  ',temp['c']['total'],'当前 ',len(temp['c']['list']))
                # 然后把temp解析拼装放入数据库
                with open('../temp_file/5.txt', 'wb') as f:
                    f.truncate()

            # 如果仅这一条
            else:
                # 直接存到数据库，就不用清空文件了
                print('只有一条')
                print('一共 ',content['c']['total'],'当前 ',len(content['c']['list']))
                temp = content



            ext_info = {}

            ext_info['article_id'] = int(article_id[0])

            ext_info['attribute_name'] = 'comment'

            comment = {}
            # 评论所属文章id
            comment['article_id'] = article_id[0]

            comment['per_page_count'] = page_count[0]

            # 评论列表
            comment['list'] = []

            # 评论总数量
            comment['comment_total'] = temp['c']['total']
            if 0 != int(comment['comment_total']):

                # 评论的额外信息，包括文章栏目信息，以备不时之需
                comment['extra'] = temp['c']['list'][0].get('extra')

                for a_comment in temp['c']['list']:
                    comment_dict = {}
                    comment_dict['note_id'] = a_comment.get('note_id')
                    # 评论内容
                    comment_dict['note'] = a_comment.get('note')
                    comment_dict['content'] = a_comment.get('content')
                    comment_dict['note_title'] = a_comment.get('note_title')
                    # 作者回复
                    comment_dict['note_line'] = a_comment.get('note_line')
                    # 评论时间
                    comment_dict['comment_reply_time'] = a_comment.get('comment_reply_time')
                    comment_dict['create_time'] = a_comment.get('create_time')
                    comment_dict['update_time'] = a_comment.get('update_time')

                    # 评论转发数
                    comment_dict['repost_count'] = a_comment['notes_count'].get('repost_count',0)
                    # 评论评论数
                    comment_dict['comment_count'] = a_comment['notes_count'].get('comment_count',0)
                    # 评论点赞数
                    comment_dict['like_count'] = a_comment['notes_count'].get('like_count',0)
                    comment_dict['notes_owner'] = a_comment.get('notes_owner')
                    comment['list'].append(comment_dict)
            # print(comment)
            else:
                comment['list'] = []

            # 如果大于20，就取前20个
            if len(comment['list']) > 18:
                comment['list'] = comment['list'][:18]

            ext_info['attribute_value'] = json.dumps(comment,ensure_ascii=False)

            # print(len(json.dumps(comment)))
            # print(json.dumps(comment).encode('gb2312').decode('unicode_escape'))
            # print(len(json.dumps(comment).encode('gb2312').decode('unicode_escape')))
            # print('哈哈')
            # 插入数据库
            try:
                mysql = MySQL()
                mysql.get_connection()
                # 目前判重机制是看这个article_id是否有额外属性comment，如果有就判重，但是没有比较内容是否重复，只是判断是否有这个属性
                mysql.insert('ext_attribute',ext_info)

            finally:
                mysql.close_connection()



# 去重，就搞个评论数量，当当前查出来的评论数量 - 数据库评论数量 > 10 就存储
# 评论只取最热门的10条，不足10条的去除
