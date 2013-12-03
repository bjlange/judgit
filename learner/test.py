from pymongo import MongoClient
from metrics import *


client = MongoClient()
db = client.reddit
posts = db.posts
example = posts.find({'subreddit': 'news'}).next()
example2 = posts.find({'subreddit': 'politics'}).next()

print get_features(example)
print post_distance(example, example2)
