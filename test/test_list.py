import time

# l = [1,2,3,4]
# for i in l:
#     l.append(4)
#     print(i)
#     print(len(l))
#     time.sleep(1)
import pickle
import json

a = [12,12]

with open('../token.txt', 'wb') as f:
    pickle.dump(a, f)
with open('../token.txt', 'rb') as f:
    b = pickle.load(f)
print(b)