import json
from io import StringIO

dic = {
    'key1':1,
    'key2':[1,'2',4]
}

f = StringIO()
js = json.dumps(dic)
print(js)
f.write(js)


js = f.getvalue()
print(js)

js = json.loads(js)
print(js)

print('asdf'+'111')

print('a' + str('asdf'))