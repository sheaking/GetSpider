#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pickle
import os
import re
from utils.id_util import generate_id
from utils.parse_content import *
from handle_mysql2 import MySQL


def response(flow):

    #显示所有栏目列表发送的请求
    #这里要防止把之前的清空
    # if 'entree.igetget.com/purchased/v2/product/allList' in flow.request.url:
    if 'igetget.com/purchased/v2/product/allList' in flow.request.url:
        #得到请求，看是否的第一次请求
        request = flow.request
        bys = request.content
        s = '&' + bys.decode('utf-8') + '&'
        page_search = re.compile(r"&page=(.*?)&")
        page = re.search(page_search,s).groups(1)

        print('第几次：', page[0])
        #如果是第一次请求。刷新1.txt文件
        if page[0] == '1':
            print('------------------')
            if os.path.exists('temp_file/1.txt'):
                #移除旧的
                os.remove('temp_file/1.txt')
            #创建新的
            with open('temp_file/1.txt', 'wb') as f:
                pass

        content = json.loads(flow.response.text)

        _1_info_before = {}
        #这里要追加column，不然刷新后读不到数据了

        #得到请求参数，如果page = 1，就说明是第一次请求，清除1.txt（如果存在就清除），并创建新的1.txt
        #必须先创建1.txt
        with open('temp_file/1.txt', 'rb') as f:
            #如果不为空，就读
            if os.path.getsize('temp_file/1.txt'):
                print('no null')
                #读到数据，重新组装为json
                _1_info_before = pickle.load(f)

        if _1_info_before:
            _1_info_before['c']['list'] = _1_info_before['c']['list'] + content['c']['list']

        # 这里最好改成redis缓存的方式
        with open('temp_file/1.txt', 'wb') as f:
            # r如果里面有数据，就_1_info_before
            if os.path.getsize('temp_file/1.txt'):
                # 清除文件中所有数据
                # 必须要清空，不然gg
                f.truncate()
            else:
                pickle.dump(content, f)

        #如果不为
        if page[0] != '1':
            with open('temp_file/1.txt', 'wb') as f:
                if os.path.getsize('temp_file/1.txt') == 0:
                    pickle.dump(_1_info_before, f)


    #点击某个栏目后发送的请求1
    # if 'entree.igetget.com/bauhinia/v1/class/purchase/info' in flow.request.url:
    if 'igetget.com/bauhinia/v1/class/purchase/info' in flow.request.url:
        content = json.loads(flow.response.text)

        with open('temp_file/1.txt', 'rb') as f:
            _1_info = pickle.load(f)

        column_info = {}
        author_info = {}
        source_info = {}
        #拼装当前点击文章的栏目信息
        for alist in _1_info['c']['list']:
            #目前只爬取文章结构为40的文章
            #尽量多用content里的变量
            #column的id竟然不是唯一的，用类型进一步限制下，不然会把其他栏目的信息，放到错位的栏目上
            #用column_id和content_category先唯一限定column试试
            if alist['id'] == content['c']['class_info']['product_id'] and alist['category'] == 40 and alist['type'] == content['c']['class_info']['product_type'] and content['c']['class_info']['name'] == alist['title']:
                #栏目
                #根据栏目名称生成栏目id
                column_info['column_id'] = generate_id(content['c']['class_info']['name'])
                column_info['column_name'] = content['c']['class_info']['name']
                column_info['column_info'] = content['c']['items'][1]['content']
                column_info['column_learn_num'] = content['c']['class_info']['learn_user_count']
                # 课程总数
                column_info['article_num'] = content['c']['class_info']['phase_num']
                column_info['current_article_num'] = content['c']['class_info']['current_article_count']
                column_info['finished'] = 0 if content['c']['class_info']['phase_num'] - content['c']['class_info'][
                    'current_article_count'] > 0 else 1

                #作者
                author_info['author_id'] = generate_id(content['c']['class_info']['lecturer_name'])
                author_info['author_name'] = content['c']['class_info']['lecturer_name']
                author_info['author_avatar'] = content['c']['class_info']['lecturer_avatar']
                author_info['author_info'] = content['c']['items'][0]['content']

                #来源
                source_info['source_name'] = 'https://www.igetget.com/'
                source_info['source_info'] = ''
                source_info['source_id'] = generate_id(source_info['source_name'])

                break


        mysql = MySQL()
        mysql.get_connection()

        try:

            if column_info:
                print(json.dumps(column_info))
                # 把category==40的栏目信息存储到数据库
                mysql.insert('tb_column', column_info)

            if author_info:
                print(json.dumps(author_info))
                # 把作者信息存到数据库中
                mysql.insert('author', author_info)

        finally:
            mysql.close_connection()


        with open('temp_file/2.txt', 'wb') as f:
            pickle.dump(content, f)


    #点击栏目中的文章后发送的请求1
    #https://entree.igetget.com/bauhinia/v1/article/info
    if 'igetget.com/bauhinia/v1/article/info' in flow.request.url:
        content = json.loads(flow.response.text)

        with open('temp_file/4.txt', 'wb') as f:
            pickle.dump(content, f)


    # 当我们请求的url包含以下字符串的时候就做对应的操作，对正文进行解析
    #有该文章标题，封面，正文，
    #还需要添加文章属于哪个栏目，属于该栏目的哪章
    if 'igetget.com/ddarticle/v1/article/get' in flow.request.url:
        content = json.loads(flow.response.text)

        article_info = {}
        ext_info = {}
        article_author_info = {}
        article_column_info = {}
        article_source_info = {}
        article_category_info = {}

        with open('temp_file/4.txt', 'rb') as f:
            _4_info = pickle.load(f)

        mysql = MySQL()
        mysql.get_connection()
        try:
            if _4_info and _4_info['c']['dd_article_id'] == content['data']['article']['Id']:
                #栏目信息嵌入
                # article_info['column_id'] = generate_id(_4_info['c']['class_info']['name'])
                # article_info['column_name'] = _4_info['c']['class_info']['name']
                # article_info['class_id'] = _4_info['c']['article_info']['class_id']

                # 文章id
                article_info['article_id'] = _4_info['c']['article_info']['id']
                article_info['article_name'] = _4_info['c']['article_info']['title']
                # 正文是字符串，先进行loads
                sub_content = json.loads(content['data']['content'])
                # 正文解析,转换为字符串存储,并进行编码转换
                temp = handle_dedao_dict(get_content_list(sub_content, _4_info))
                article_info['article_content'] = temp

                # 显示文章信息
                print('article_info: ' + json.dumps(article_info))

                # return None
                # print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')


                #插入文章表
                mysql.insert('article', article_info)



                #关联文章和作者
                article_author_info['article_id'] = article_info['article_id']
                article_author_info['author_id'] = generate_id(_4_info['c']['class_info']['lecturer_name'])
                print('article_author_info: ' + json.dumps(article_author_info))
                mysql.insert('article_author',article_author_info)

                #关联文章和栏目
                article_column_info['article_id'] = article_info['article_id']
                article_column_info['column_id'] = generate_id(_4_info['c']['class_info']['name'])
                print('article_column_info: ' + json.dumps(article_column_info))
                mysql.insert('article_column', article_column_info)

                # 关联文章和来源
                article_source_info['article_id'] = article_info['article_id']
                article_source_info['source_id'] = generate_id('https://www.igetget.com/')
                print('article_source_info: ' + json.dumps(article_source_info))
                # mysql.insert('article_source', article_source_info)


                #额外信息
                ext_info['article_id'] = article_info['article_id']
                ext_info['attribute_name'] = 'prev_article_id'
                ext_info['attribute_value'] = _4_info['c']['prev_article_id']
                #插入额外属性表
                print('ext_info: ' + json.dumps(ext_info))
                # mysql.insert('ext_attribute',ext_info)

                ext_info['attribute_name'] = 'next_article_id'
                ext_info['attribute_value'] = _4_info['c']['next_article_id']
                #插入额外属性表
                print('ext_info: ' + json.dumps(ext_info))
                # mysql.insert('ext_attribute', ext_info)

                ext_info['attribute_name'] = 'cover_image'
                ext_info['attribute_value'] = _4_info['c']['article_info']['logo']
                # 插入额外属性表
                print('ext_info: ' + json.dumps(ext_info))
                # mysql.insert('ext_attribute', ext_info)

                ext_info['attribute_name'] = 'article_learn_count'
                ext_info['attribute_value'] = _4_info['c']['article_info']['cur_learn_count']
                # 插入额外属性表
                print('ext_info: ' + json.dumps(ext_info))
                # mysql.insert('ext_attribute', ext_info)

                ext_info['attribute_name'] = 'audio_url'
                ext_info['attribute_value'] = _4_info['c']['article_info']['audio']['mp3_play_url']
                # 插入额外属性表
                print('ext_info: ' + json.dumps(ext_info))
                # mysql.insert('ext_attribute', ext_info)

                # article_info['article_learn_count'] = _4_info['c']['article_info']['cur_learn_count']
                # article_info['audio_url'] = _4_info['c']['article_info']['audio']['mp3_play_url']

                #得到文章 章节名
                with open('temp_file/2.txt', 'rb') as f:
                    _2_info = pickle.load(f)

                if _4_info['c']['class_info']['name'] == _2_info['c']['class_info']['name']  and _4_info['c']['article_info']['class_id'] == _2_info['c']['class_info']['id'] and _2_info['c']['class_info']['has_chapter'] == 1:
                    for adict in _2_info['c']['chapter_list']:
                        if _4_info['c']['article_info']['chapter_id'] == adict['id']:

                            ext_info['attribute_name'] = 'chapter_name'
                            ext_info['attribute_value'] = adict['name']
                            #插入额外信息表
                            print('ext_info: ' + json.dumps(ext_info))
                            # mysql.insert('ext_attribute', ext_info)

                # article_info['create_time'] = content['data']['article']['CreateTime']
                # article_info['update_time'] = content['data']['article']['UpdateTime']
                # article_info['publish_time'] = content['data']['article']['PublishTime']



        except Exception as e:
            print('文章链接entree.igetget.com/ddarticle/v1/article/get 出现异常')
            print(e)
        finally:
            mysql.close_connection()

    # 该文章的评论
    # https://entree.igetget.com/bauhinia/v1/article/info
    if 'igetget.com/ledgers/notes/article_comment_list' in flow.request.url:

        content = json.loads(flow.response.text)

        # 如果有更多评论，就取出拼接再放入
        if content['c']['isMore']:
            if not os.path.exists('temp_file/5.txt') or os.path.getsize('temp_file/5.txt') == 0:
                with open('temp_file/5.txt', 'wb') as f:
                    pickle.dump(content, f)
            else:
                print('之前大小：', os.path.getsize('temp_file/5.txt'),)

                with open('temp_file/5.txt', 'rb') as f:
                    temp = pickle.load(f)

                with open('temp_file/5.txt', 'wb') as f:
                    f.truncate()

                print('中间大小：', os.path.getsize('temp_file/5.txt'))
                temp['c']['list'] = temp['c']['list'] + content['c']['list']
                with open('temp_file/5.txt', 'wb') as f:
                    pickle.dump(temp, f)
                print('之后大小：', os.path.getsize('temp_file/5.txt'))

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

            if os.path.getsize('temp_file/5.txt'):
                print('最后一条')
                with open('temp_file/5.txt', 'rb') as f:
                    temp = pickle.load(f)
                temp['c']['list'] = temp['c']['list'] + content['c']['list']
                print('一共  ',temp['c']['total'],'当前 ',len(temp['c']['list']))
                # 然后把temp解析拼装放入数据库
                with open('temp_file/5.txt', 'wb') as f:
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

            # 如果大于18，就取前18个
            if len(comment['list']) > 30:
                comment['list'] = comment['list'][:30]

            ext_info['attribute_value'] = json.dumps(comment,ensure_ascii=False)

            # print(len(json.dumps(comment)))
            # print(json.dumps(comment).encode('gb2312').decode('unicode_escape'))
            # print(len(json.dumps(comment).encode('gb2312').decode('unicode_escape')))
            # print('哈哈')
            # 插入数据库
            mysql = MySQL()
            try:
                mysql.get_connection()
                # 目前判重机制是看这个article_id是否有额外属性comment，如果有就判重，但是没有比较内容是否重复，只是判断是否有这个属性
                # mysql.insert('ext_attribute',ext_info)

            finally:
                mysql.close_connection()
