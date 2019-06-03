import requests
#设置代理，从西刺免费代理网站上找出一个可用的代理IP

# 要访问的目标页面
targetUrl  = 'https://www.httpbin.org/get'

# 代理服务器
proxyHost = "http-cla.abuyun.com"
proxyPort = "9030"

# 代理隧道验证信息
proxyUser = "H03929F8816459LC"
proxyPass = "4B500FA51D06F5FD"


proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
    "user" : proxyUser,
    "pass" : proxyPass,
}

proxies = {
    "http"  : proxyMeta,
    "https" : proxyMeta,
}


#使用代理IP进行访问
res=requests.get(targetUrl, proxies = proxies)
print(res.text)