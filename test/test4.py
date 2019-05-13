import os
import pickle
from io import StringIO
import json

with open('1.txt', 'w') as f:
    f.write('1')


with open('1.txt', 'w') as f:
    f.truncate()
print(os.path.getsize('1.txt'))
print(os.path.exists('1.txt'))
a = json.dumps([
    {'haha':1},
    {'hehe':"asdgqasdg"}

])
print(type(a))

l = ['asdf','dfd','12sd']
if 'asdf' not in l:
    print('jaja')