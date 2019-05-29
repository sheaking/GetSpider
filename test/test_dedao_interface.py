import requests
import time

headers = {
"X-App-Key":"android-6.0.2",
"X-Uid":"1413042",
"X-Thumb":"s",
"X-Dt":"phone",
"X-Ov":"7.1.2",
"X-Net":"WIFI",
"X-Os":"ANDROID",
"X-D":"144032cc40441224",
"X-Dv":"SM-G955N",
"X-T":"json",
"X-Chil":"154",
"X-V":"2",
"X-Av":"6.0.2",
"X-Scr":"1.0",
"X-Adv":"1",
"X-Seid":"f0d45b41b4c2d09e783a1d04ac1ce15a",
"X-Hitdot":"",
"G-Auth-Sign":"NDVjMmFlNDNlMjI5YTY1M2MxMmNmZWM1Mzc3NTc0ZTM=",
"G-Auth-Nonce":"a64a4113ce8891429cca3eb7843723ee",
"G-Auth-Ts":str(int(time.time())),
"G-Auth-Appid":"5a27d122ee4638163f594393",
"G-Auth-Token":"eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsdW9qaWxhYi5jb20iLCJleHAiOjE1NjI4MzEzNzcsImlhdCI6MTU1ODk0MzM3NywiaXNzIjoiRWFzZUdhdGV3YXkgSldUQXV0aCBQbHVnaW4iLCJuYmYiOjE1NTg5NDMzNzcsInN1YiI6IjE0MTMwNDIifQ.Kn4vbfn3fTIj8yzsiO6CPgUFycYPrkv2cRUaY_88D1Ihn5t8Vltdy6ebCVNnfsCDgRjhR4xMy-XSFi8vZeWnnQ",
"Content-Type":"application/json;charset=UTF-8",
"Content-Length":"330",
"Host":"entree.igetget.com",
"Connection":"Keep-Alive",
"Accept-Encoding":"gzip",
"User-Agent":"okhttp/3.11.0",
}
print(str(int(time.time())))

data = {
	"ptype": 22,
	"pid": 90,
	"reverse": False,
	"h": {
		"u": "1413042",
		"thumb": "s",
		"dt": "phone",
		"ov": "7.1.2",
		"net": "WIFI",
		"os": "ANDROID",
		"d": "144032cc40441224",
		"dv": "SM-G955N",
		"t": "json",
		"chil": "154",
		"v": "2",
		"av": "6.0.2",
		"scr": "1.0",
		"adv": "1",
		"X-Dv": "SM-G955N",
		"ts": str(int(time.time())),
		"s": "d302ace41ad758cc",
		"seid": "f0d45b41b4c2d09e783a1d04ac1ce15a"
	}
}

url = 'https://entree.igetget.com/bauhinia/v1/class/purchase/info'

r = requests.post(url=url, headers=headers, json=data)
print(r.json())
