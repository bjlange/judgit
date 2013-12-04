from pymongo import MongoClient
from metrics import *


client = MongoClient()
db = client.reddit
posts = db.posts
example = posts.find({'subreddit': 'news'}).next()
example2 = posts.find({'subreddit': 'politics'}).next()
example3 = posts.find({'subreddit': 'cats'}).next()

print get_features(example)
print post_distance(example, example2)
print post_distance(example, example3)

print 'The following distances should be the same'
print post_distance(example2, example3)
print post_distance(example3, example2)

print 'The following distance should be zero'
print post_distance(example3, example3)
