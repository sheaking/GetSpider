import json
s = '''{"type": "elite", "value": "1. 在获取信息之前，需要提出假设，而不是盲目撒网；2. 寻找可以定性的信息，警惕不能反映事实的信息； 3. 寻找可以影响后续决策的信息。"}'''

temp = {

    'value':'asdfasdfa"sdfa" '
}
print(temp['value'])
temp['value'] = temp['value'].replace('"','\"')
print(temp['value'])
print(json.dumps(temp))

# print(s.count('\n'))
# print('\n' in s)
# print(s.find('\n'))
# s2 = s.replace('\n','\\n')
# print(json.loads(s2).get('value'))
#
# print(temp.count('"'))
