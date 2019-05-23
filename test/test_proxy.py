import requests
#设置代理，从西刺免费代理网站上找出一个可用的代理IP
proxies={
    'https':'https://221.6.32.206:50925'
} #此处也可以通过列表形式，设置多个代理IP，后面通过random.choice()随机选取一个进行使用

url = 'https://www.baidu.com'
#使用代理IP进行访问
res=requests.get(url,proxies=proxies)
print(res.text)