import hashlib
data = '你的想象力，只有宇宙装得下'
print(type(hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()))
sum = 0
for s in data:
    print(ord(s))
    sum += ord(s)
print(sum)

for s in 'https://www.igetget.com/':
    if index % 2:
        source_id += ord(s)
    else:
        source_id += ord(s) * 3