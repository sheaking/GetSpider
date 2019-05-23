
import re
from urllib.parse import urlparse
import os

s = '''
count=20&order=buy&category=all&h={"u":"1413042","thumb":"m","dt":"phone","ov":"7.1.2","net":"WIFI","os":"ANDROID","d":"344032cc40441123","dv":"ALP-AL00","t":"json","chil":"4","v":"2","av":"6.1.0","scr":"1.5","adv":"1","X-Dv":"ALP-AL00","ts":"1558428286","s":"d302ace41ad758cc","seid":"e13edfaec183ffdd6228be45b7988364"}&page=1&
'''
page_search = re.compile(r"&page=(.*?)&")
page = re.search(page_search,s).groups(1)
print(page == '1')


s2 = 'https://igetcdn.igetget.com/aac/201905/08/48000_201905081025399902169855.m4a'
print(urlparse(s2))

num = s2.rfind('/')
print(num)
print(s2[s2.rfind('/')+1:])

print(os.path.abspath('./'))
abs = os.path.abspath('./')
file = '2.txt'
with open(os.path.join(abs,file),'wb'):
    pass
