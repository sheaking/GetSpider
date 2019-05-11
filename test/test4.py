import os
import pickle
from io import StringIO

with open('1.txt', 'w') as f:
    f.write('1')


with open('1.txt', 'w') as f:
    f.truncate()
print(os.path.getsize('1.txt'))
print(os.path.exists('1.txt'))
