import requests
import time

url = 'https://entree.igetget.com/onepiece/v1/user/init?phone=17521359419'
url2 = 'https://httpbin.org/get'
url3 = 'http://www.baidu.com'
proxies = {
    "http": "http://175.8.109.48:8118",
    "https": "https://113.121.20.170:9999"
}

headers = {
    "X-App-Key": "android-6.0.1",
    "X-Uid": "0",
    "X-Thumb": "m",
    "X-Dt": "phone",
    "X-Ov": "4.4.2",
    "X-Net": "WIFI",
    "X-Os": "ANDROID",
    "X-D": "244032cc40441432",
    "X-Dv": "SM-G955F",
    "X-T": "json",
    "X-Chil": "175",
    "X-V": "2",
    "X-Av": "6.0.1",
    "X-Scr": "1.5",
    "X-Adv": "1",
    "X-Seid": "4ecb4596360141748382e7723ee1dab0",
    "X-Hitdot": "",
    "G-Auth-Sign": "OWNjNzk1MjhlNjg1M2FhM2Y2YmVhMjFlMjllZmQ5YTg=",
    "G-Auth-Nonce": "54bdf159d0d58b34ec36f0670b7efa90",
    "G-Auth-Ts": "1560498398",
    "G-Auth-Appid": "5a27d122ee4638163f594393",
    "Host": "entree.igetget.com",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip",
    "User-Agent": "okhttp/3.11.0",
}
r = requests.get(url=url2,headers=headers,proxies=proxies)
print(r.text)