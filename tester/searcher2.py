import sys, os
from pymongo import MongoClient
from datetime import datetime, timedelta
sys.path.insert(0, '../learner')
from regressor import KNearest
from metrics import get_features
from heapq import nsmallest

def weightedSum(weights, values):
	return sum(map(lambda x,y: x*y, weights, values))

if __name__ == '__main__':
	path = os.path.join('data', 'fold1')
	files = [f for f in os.listdir(path) if os.path.isfile(f)]
	client = MongoClient()
	posts = client.reddit.posts

	postArray = []

	for f in files:
		post = posts.find_one({'_id': f})

		scoreToUse = 0
		submissionTime = datetime.fromtimestamp(post['creation_time'])
		delta = timedelta(days=1)
		for score in post['scores']:
			scoreToUse = score[1]
			if (submissionTime + delta) < score [0]:
				break
		post = get_features(post)
		post['realScore'] = scoreToUse
		postArray.append(post)

	print 'starting'

	weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

	sse = 0.0
	for post in postArray:
		path = os.path.join('data', 'fold1', post['id'])
		with open(path, 'r') as f:
			allDistances = [[float(x) for x in line.split(',')] for line in f.read().split('\n') if len(line) > 0]
			items = nsmallest(1, allDistances, key=lambda x: weightedSum(weights, x[0:6]))
			scores = map(lambda x: x[6], items)
			score = score / len(items)
			sse += (score - post['realScore']) ** 2
		print 'done1'

	print sse / len(posts)

