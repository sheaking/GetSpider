import json
import pickle
# try:
#     from douyin.handle_mongo import save_task
# except:
#     from handle_mongo import save_task

def response(flow):

    if 'entree.igetget.com/purchased/v2/product/allList' in flow.request.url:
        content = json.loads(flow.response.text)

        #这里最好改成redis缓存的方式
        with open('1.txt', 'wb') as f:
            pickle.dump(content,f)

    if 'entree.igetget.com/bauhinia/v1/class/purchase/info' in flow.request.url:
        content = json.loads(flow.response.text)

        with open('2.txt', 'wb') as f:
            pickle.dump(content,f)


    #https://entree.igetget.com/bauhinia/v1/article/info
    #以下代码有些冗余
    if 'entree.igetget.com/bauhinia/v1/article/info' in flow.request.url:
        audio_info = {}
        content = json.loads(flow.response.text)

        audio_info['class_id'] = content['c']['class_id']
        # 属于哪本书
        audio_info['pid'] = content['c']['pid']
        # 当前id
        audio_info['article_id'] = content['c']['article_id']

        audio_info['dd_article_id'] = content['c']['dd_article_id']

        #形成一个双向链表，构成关系
        #之前文章的id，为0则是当前文章是第一章
        audio_info['prev_article_id'] = content['c']['prev_article_id']

        #之后文章的id，为0则当前文章是最后一章
        audio_info['next_article_id'] = content['c']['next_article_id']


        audio_info['aliasId'] = content['c']['article_info']['audio']['alias_id']
        audio_info['mp3_play_url'] = content['c']['article_info']['audio']['mp3_play_url']

        #属于本书的哪章，还需要顺序顺序
        #这个是前后顺序，没有章节
        audio_info['order_num'] = content['c']['article_info']['order_num']

        audio_info['cur_learn_count'] = content['c']['article_info']['cur_learn_count']

        #获取大标题如何用极其有限的信息去寻找真相？|《高爽·天文学通识30讲》
        # s = content['c']['article_info']['share_title']
        # s = s[s.find('|') + 1:].strip()
        # audio_info['big_title'] = s

        # audio_info['share_content'] = content['c']['article_info']['share_content']

        #属于章节的id
        audio_info['chapter_id'] = content['c']['article_info']['chapter_id']

        #获取chapter_name,这两个东西写到下面方法中最好



        #这里必需用这种方式，持久化到文件中，到那边到文件中取出来
        with open('dump.txt', 'wb') as f:
            pickle.dump(audio_info,f)

        print(json.dumps(audio_info))
        print(type(audio_info))


    # 当我们请求的url包含以下字符串的时候就做对应的操作，对正文进行解析
    #有该文章标题，封面，正文，
    #还需要添加文章属于哪个栏目，属于该栏目的哪章
    if 'entree.igetget.com/ddarticle/v1/article/get' in flow.request.url:
        # for user in json.loads(flow.response.text)['followers']:
        #     douyin_info = {}
        #     douyin_info['share_id'] = user['uid']
        #     douyin_info['douyin_id'] = user['short_id']
        #     save_task(douyin_info)
        # 这里必需这样写，不然会错
        dedao_info = {
            "extra_info":{},
            "article": {
                "author":{}
            },
            "content": []
        }
        content = json.loads(flow.response.text)
        with open('dump.txt', 'rb') as f:
            audio_info = pickle.load(f)

        if audio_info:
            dedao_info['extra_info']['pid'] = audio_info['pid']
            dedao_info['extra_info']['class_id'] = audio_info['class_id']
            dedao_info['extra_info']['article_id'] = audio_info['article_id']
            dedao_info['extra_info']['dd_article_id'] = audio_info['dd_article_id']
            dedao_info['extra_info']['prev_article_id'] = audio_info['prev_article_id']
            dedao_info['extra_info']['next_article_id'] = audio_info['next_article_id']
            dedao_info['extra_info']['order_num'] = audio_info['order_num']
            # dedao_info['extra_info']['big_title'] = audio_info['big_title']
            # dedao_info['extra_info']['share_content'] = audio_info['share_content']
            dedao_info['extra_info']['chapter_id'] = audio_info['chapter_id']

        with open('1.txt', 'rb') as f:
            book_info = pickle.load(f)

        if book_info:
            for alist in book_info['c']['list']:
                if alist['id'] == dedao_info['extra_info']['pid']:
                    dedao_info['extra_info']['category'] = alist['category']
                    dedao_info['extra_info']['big_title'] = alist['title']
                    break

        with open('2.txt', 'rb') as f:
            chapter_info = pickle.load(f)

        if chapter_info:
            if dedao_info['extra_info']['pid'] == chapter_info['c']['class_info']['product_id'] and dedao_info['extra_info']['class_id'] == chapter_info['c']['class_info']['id']:
                #判断本书是否更新完毕，更新完毕为1，否则为0
                dedao_info['extra_info']['finished'] = 0 if chapter_info['c']['class_info']['phase_num'] - chapter_info['c']['class_info']['current_article_count'] else 1
                #学习人数
                dedao_info['extra_info']['learn_user_count'] = chapter_info['c']['class_info']['learn_user_count']
                for chapter in chapter_info['c']['chapter_list']:
                    if dedao_info['extra_info']['chapter_id'] == chapter['id']:
                        dedao_info['extra_info']['chapter_name'] = chapter['name']
                        dedao_info['extra_info']['intro'] = chapter['intro']



        # 这里要得到文章id，根据这个id跟音频对应,
        dedao_info['article']['Id'] = content['data']['article']['Id']
        dedao_info['article']['AppId'] = content['data']['article']['AppId']
        dedao_info['article']['IdStr'] = content['data']['article']['IdStr']
        dedao_info['article']['AppIdStr'] = content['data']['article']['AppIdStr']




        print(type(content['data']['content']))  # 'data content类型：' +
        # 注意这里content['data']['content']类型是str的,不然出错
        sub_content = json.loads(content['data']['content'])

        # 文章标题
        dedao_info['article']['title'] = sub_content['title']
        # 文章封面
        dedao_info['article']['coverImage'] = sub_content['coverImage']
        # 作者名字头像
        dedao_info['article']['author']['name'] = sub_content['author']['name']
        dedao_info['article']['author']['avatar'] = sub_content['author']['avatar']


        # type有title，text，quotedOnlyGray（女性健康），titleCenter(本讲小结，女性健康)，center（女性健康）,elite(医学),tip(Dr魏)，quotedNew（）
        # audio，image，split，这些没有value值
        for alist in sub_content['content']:
            temp_dict = {}
            temp_dict['type'] = alist['type']

            if temp_dict['type'] == 'audio':
                temp_dict['audio'] = {}
                temp_dict['aliasId'] = alist['audio']['aliasid']

                if audio_info.get('aliasId') == temp_dict['aliasId']:
                    # 音频链接，这里src需要从另一个链接得到
                    temp_dict['audio']['mp3_play_url'] = audio_info['mp3_play_url']
                    print(audio_info.get('mp3_play_url'))
                    audio_info.clear()

                # 音频标题
                temp_dict['audio']['title'] = alist['audio']['title']
                temp_dict['audio']['rawSize'] = alist['audio']['rawSize']
                temp_dict['audio']['duration'] = alist['audio']['duration']
                temp_dict['audio']['size'] = alist['audio']['size']
                temp_dict['tips'] = alist['tips']
            elif temp_dict['type'] == 'image':
                # 去除版权页面
                if len(alist['title']) > 0:
                    temp_dict['src'] = alist['src']
                    temp_dict['title'] = alist['title']
            elif temp_dict['type'] != 'center' and 'value' in alist:
                if temp_dict['type'] == 'comment':
                    temp_dict['tag'] = alist['tag']
                temp_dict['value'] = alist['value']

            dedao_info['content'].append(temp_dict)

        print(json.dumps(dedao_info))



