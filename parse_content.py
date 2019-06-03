# -*- coding: utf-8 -*-
import json

def get_content_list(param, ext_info):
    '''

    :param param:
    :param ext_info:
    :return:
    '''

    info_list = []

    for index, alist in enumerate(param['content']):
        temp_dict = {}
        temp_dict['type'] = alist['type']

        if temp_dict['type'] == 'audio':
            temp_dict['audio'] = {}
            temp_dict['aliasId'] = alist['audio']['aliasid']

            if ext_info['c']['article_info']['audio']['alias_id'] == temp_dict['aliasId']:
                # 音频链接，这里src需要从另一个链接得到
                temp_dict['audio']['mp3_play_url'] = ext_info['c']['article_info']['audio']['mp3_play_url']

            # 音频标题
            temp_dict['audio']['title'] = alist['audio']['title']
            temp_dict['audio']['rawSize'] = alist['audio']['rawSize']
            temp_dict['audio']['duration'] = alist['audio']['duration']
            temp_dict['audio']['size'] = alist['audio']['size']
            temp_dict['tips'] = alist['tips']
        elif temp_dict['type'] == 'image':
            # 去除版权页面,加强筛选，去除最后两个图片，最后两个图片一般是版权图片
            if len(alist['title']) > 0 or len(param['content']) - index > 3:
                temp_dict['src'] = alist['src']
                temp_dict['title'] = alist['title']

        elif temp_dict['type'] != 'center' and 'value' in alist:
            if temp_dict['type'] == 'comment':
                temp_dict['tag'] = alist['tag']

            temp_dict['value'] = alist['value']
            # 社会网络11里面的tip很大，异常的大
            if temp_dict['type'] == 'tip' and len(alist['value']) > 3500:
                temp_dict['value'] = ''
        # 增加过滤条件，版权归得到app所有，去除，其他的center可以添加
        elif temp_dict['type'] == 'center' and '\u7248\u6743\u5f52\u5f97\u5230App\u6240\u6709' not in alist['value']:
            temp_dict['value'] = alist['value']


        info_list.append(temp_dict)

    return info_list


def handle_dedao_dict(target_list):
    #先换value中的 "
    for item in target_list:
        temp = item.get('value')
        if temp and temp.count('"'):
            item['value'] = temp.replace('"','\'')

    temp = json.dumps(target_list).encode('gb2312').decode('unicode_escape')
    # 将神秘符号进行替换
    temp = temp.replace('	', ' ')
    temp = temp.replace('\n', '<br>')
    return temp





