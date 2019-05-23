import os

list = ['D:\\PycharmProjects\\GetSpider\\down_upload_resource\\resource\\201904181826026267457515.jpg', 'D:\\PycharmProjects\\GetSpider\\down_upload_resource\\resource\\48000_201904271150019470491263.m4a', 'D:\\PycharmProjects\\GetSpider\\down_upload_resource\\resource\\201904241055417803615605.jpg', 'D:\\PycharmProjects\\GetSpider\\down_upload_resource\\resource\\201904261100406212431006.jpg']


for l in list:
    s = os.path.split(l)[1]
    print(s[:s.rfind('.')])

os.path.join('')