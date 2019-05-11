import json
import pickle
import os

dedao_info = '''
{
            "article":{"id":1},
            "content":{
                "content":{
                    "audio":{
                        "title":"hehe"
                    }
                },
                "author":{}
            }
}
'''
# data = json.loads(dedao_info)
#
# a = {}
# b = data['content']['content']['audio']['title']
# a['content']['audio']['title'] = b
# print(a)
a = 1 if 5 - 5 else 0
print(a)

if {}:
    print('haha')
content = {}
with open('test.txt', 'wb') as f:
    print('hehe')

with open('test.txt', 'rb') as f:
    print(os.path.getsize('../temp_file/1.txt'))
    # content2 = pickle.load(f)
# print(content2)
# if content2:
#     print("hehhe")

list1 = [1,3,4]
list2 = ['234',34]
list3 = list2 +list1
print(list3)


