import json
s = '''{"type": "elite", "value": "1. 在获取信息之前，需要提出假设，而不是盲目撒网；2. 寻找可以定性的信息，警惕不能反映事实的信息； 3. 寻找可以影响后续决策的信息。"}'''

temp = {

    'value':'asdfasdfa"sdfa" '
}
print(temp['value'])
temp['value'] = temp['value'].replace('"','\"')
print(temp['value'])
print(json.dumps(temp))

s2 = '''{"type":"title","value":"1.	词汇量：学龄前1000个听力词汇的积累"}'''

print(s2.find('	'))

print(s2)
print(json.loads(s2.replace('	',' ')))


s3 = '''{"type": "elite", "value": "1）	组织行为学以组织目标为导向；<br>2）	组织行为学的研究方法是实证研究，这也导致它和管理学是两个学派，它们的根本区别在于是否认同真理的不变性；<br>3）	组织行为学的基本观点是权变。"}'''
print(s3.find('	'))
# print(s.count('\n'))
# print('\n' in s)
# print(s.find('\n'))
# s2 = s.replace('\n','\\n')
# print(json.loads(s2).get('value'))
#
# print(temp.count('"'))
