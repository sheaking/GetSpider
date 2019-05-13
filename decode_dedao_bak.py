import json
import pickle
import os
import re
from mitmproxy import ctx

def response(flow):

    #这里要防止把之前的清空
    if 'entree.igetget.com/purchased/v2/product/allList' in flow.request.url:
        #得到请求，看是否的第一次请求
        request = flow.request
        bys = request.content
        s = bys.decode('utf-8')
        page_search = re.compile(r"&page=(.*?)&")
        page = re.search(page_search,s).groups(1)

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



    if 'entree.igetget.com/bauhinia/v1/class/purchase/info' in flow.request.url:
        content = json.loads(flow.response.text)

        with open('temp_file/1.txt', 'rb') as f:
            _1_info = pickle.load(f)

        column_info = {}

        #拼装当前点击文章的栏目信息
        for alist in _1_info['c']['list']:
            #目前只爬取文章结构为40的文章
            #尽量多用content里的变量
            #column的id竟然不是唯一的，用类型进一步限制下，不然会把其他栏目的信息，放到错位的栏目上
            #用column_id和content_category先唯一限定column试试
            if alist['id'] == content['c']['class_info']['product_id'] and alist['category'] == 40 and alist['type'] == content['c']['class_info']['product_type']:
                column_info['column_id'] = alist['id']
                column_info['column_name'] = content['c']['class_info']['name']
                column_info['author_name'] = content['c']['class_info']['lecturer_name']
                column_info['author_avatar'] = content['c']['class_info']['lecturer_avatar']

                column_info['author_info'] = content['c']['items'][0]['content']
                column_info['intro'] = content['c']['class_info']['intro']
                column_info['highlight'] = content['c']['items'][1]['content']
                #课程总数
                column_info['course_num'] = content['c']['class_info']['phase_num']

                column_info['current_article_count'] = content['c']['class_info']['current_article_count']
                column_info['source'] = 'www.igetget.com'

                column_info['is_finished'] = 0 if content['c']['class_info']['phase_num'] - content['c']['class_info']['current_article_count'] else 1

                column_info['struct_category'] = alist['category']
                column_info['content_category'] = alist['type']
                column_info['create_time'] = alist['create_time']
                column_info['last_action_time'] = alist['last_action_time']

                column_info['column_learn_count'] = content['c']['class_info']['learn_user_count']
                column_info['class_id'] = content['c']['class_info']['id']
                break


        if column_info:
            #把category==40的栏目信息存储到数据库
            print(json.dumps(column_info))

        with open('temp_file/2.txt', 'wb') as f:
            pickle.dump(content,f)


    #https://entree.igetget.com/bauhinia/v1/article/info
    if 'entree.igetget.com/bauhinia/v1/article/info' in flow.request.url:
        content = json.loads(flow.response.text)

        with open('temp_file/4.txt', 'wb') as f:
            pickle.dump(content, f)


    # 当我们请求的url包含以下字符串的时候就做对应的操作，对正文进行解析
    #有该文章标题，封面，正文，
    #还需要添加文章属于哪个栏目，属于该栏目的哪章
    if 'entree.igetget.com/ddarticle/v1/article/get' in flow.request.url:
        content = json.loads(flow.response.text)


        article_info = {}
        with open('temp_file/4.txt', 'rb') as f:
            _4_info = pickle.load(f)

        if _4_info and _4_info['c']['dd_article_id'] == content['data']['article']['Id']:
            article_info['column_id'] = _4_info['c']['class_info']['product_id']
            article_info['column_name'] = _4_info['c']['class_info']['name']

            article_info['class_id'] = _4_info['c']['article_info']['class_id']
            article_info['article_id'] = _4_info['c']['article_info']['id']
            article_info['prev_article_id'] = _4_info['c']['prev_article_id']
            article_info['next_article_id'] = _4_info['c']['next_article_id']
            article_info['order_num'] = _4_info['c']['article_info']['order_num']

            article_info['cover_image'] = _4_info['c']['article_info']['logo']
            article_info['article_name'] = _4_info['c']['article_info']['title']
            article_info['chapter_id'] = _4_info['c']['article_info']['chapter_id']

            #得到文章 章节名
            with open('temp_file/2.txt', 'rb') as f:
                _2_info = pickle.load(f)
            if article_info['column_id'] == _2_info['c']['class_info']['product_id']  and article_info['class_id'] == _2_info['c']['class_info']['id'] and _2_info['c']['class_info']['has_chapter'] == 1:
                for adict in _2_info['c']['chapter_list']:
                    if article_info['chapter_id'] == adict['id']:
                        article_info['chapter_name'] = adict['name']
            article_info['article_learn_count'] = _4_info['c']['article_info']['cur_learn_count']
            article_info['audio_url'] = _4_info['c']['article_info']['audio']['mp3_play_url']
            article_info['create_time'] = content['data']['article']['CreateTime']
            article_info['update_time'] = content['data']['article']['UpdateTime']
            article_info['publish_time'] = content['data']['article']['PublishTime']



            #正文解析
            article_info['content'] = []
            sub_content = json.loads(content['data']['content'])
            for index,alist in enumerate(sub_content['content']):
                temp_dict = {}
                temp_dict['type'] = alist['type']

                if temp_dict['type'] == 'audio':
                    temp_dict['audio'] = {}
                    temp_dict['aliasId'] = alist['audio']['aliasid']

                    if _4_info['c']['article_info']['audio']['alias_id'] == temp_dict['aliasId']:
                        # 音频链接，这里src需要从另一个链接得到
                        temp_dict['audio']['mp3_play_url'] = _4_info['c']['article_info']['audio']['mp3_play_url']

                    # 音频标题
                    temp_dict['audio']['title'] = alist['audio']['title']
                    temp_dict['audio']['rawSize'] = alist['audio']['rawSize']
                    temp_dict['audio']['duration'] = alist['audio']['duration']
                    temp_dict['audio']['size'] = alist['audio']['size']
                    temp_dict['tips'] = alist['tips']
                elif temp_dict['type'] == 'image':
                    # 去除版权页面,加强筛选，去除最后两个图片，最后两个图片一般是版权图片
                    if len(alist['title']) > 0 or len(sub_content['content']) - index > 3:
                        temp_dict['src'] = alist['src']
                        temp_dict['title'] = alist['title']

                elif temp_dict['type'] != 'center' and 'value' in alist:
                    if temp_dict['type'] == 'comment':
                        temp_dict['tag'] = alist['tag']
                    temp_dict['value'] = alist['value']

                article_info['content'].append(temp_dict)

            print(json.dumps(article_info))
