# s = '如何用极其有限的信息去寻找真相？|    《高爽·天文学通识30讲》'
#
# print(s.find('|'))
# print(s[s.find('|') + 1:].strip())

m = [1, 2, 3]
n = [3, 4, 5]
for i in m:
    if i not in n:
        m.append(i)
    print(len(m))

print(m)