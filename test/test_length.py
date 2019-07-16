
import os
import pickle

if os.path.exists('../token.txt'):
    with open('../token.txt', 'rb') as f:
        crawled_article = pickle.load(f)
print(len(crawled_article))