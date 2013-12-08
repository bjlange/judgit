import sys, os
from pymongo import MongoClient
from datetime import datetime, timedelta
sys.path.insert(0, '../learner')
from regressor import KNearest
from metrics import get_features
from heapq import nsmallest

def weightedSum(weights, values):
	return sum(map(lambda x,y: x*y, weights, values))

def generateWeights():
	weights = []
	for i in range(6):
		for val in [0.0, .25, .5, 2.0, 4.0]:
			basic = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
			basic[i] = val
			weights.append(basic)
	weights.append([1.0, 1.0, 1.0, 1.0, 1.0, 1.0])
	return weights

if __name__ == '__main__':
	path = os.path.join('data', 'fold1')
	files = [f for f in os.listdir(path) if os.path.isfile(os.path.join('data', 'fold1', f))]
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

	weights = generateWeights()

	sseArray = [0.0] * len(weights)
	for post in postArray:
		path = os.path.join('data', 'fold1', post['id'])
		with open(path, 'r') as f:
			allDistances = [[float(x) for x in line.split(',')] for line in f.read().split('\n') if len(line) > 0]
			for i in range(len(weights)):
				items = nsmallest(1, allDistances, key=lambda x: weightedSum(weights[i], x[0:6]))
				scores = map(lambda x: x[6], items)
				score = sum(scores) / len(items)
				sseArray[i] += (score - post['realScore']) ** 2
		print 'done1'

	with open('awesomeresults.txt','w') as f:
		for i in range(len(weights)):
			f.write('%s\t%s\n' % (weights[i], sseArray[i] / len(postArray)))

