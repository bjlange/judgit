import sys
from pymongo import MongoClient
from datetime import datetime, timedelta
from sklearn.cross_validation import KFold
sys.path.insert(0, '../learner')
from regressor import KNearest
from metrics import get_features, unweighted_distances

def weightedSum(weights, values):
	return sum(map(lambda x,y: x*y, weights, values))

def getDistances(post, training):
	allDistances = []
	for t in training:
		distances = unweighted_distances(post, t)
		distances.append(t['realScore'])
		allDistances.append(distances)
	return allDistances

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

	client = MongoClient('zoidberg.wksun.com', 27017)
	posts = client.reddit.posts

	postArray = []

	for post in posts.find():
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

	kf = KFold(len(postArray), n_folds=30, indices=True, random_state=42)

	trainingIndices = None
	testingIndices = None

	for train, test in kf:
		trainingIndices = train
		testingIndices = test
		break

	trainingData = [postArray[i] for i in trainingIndices]
	testingData = [postArray[i] for i in testingIndices]

	weights = generateWeights()

	sseArray = [0.0] * len(weights)
	print 'starting'
	count = 1
	for post in testingData:
		print count
		allDistances = getDistances(post, trainingData)
		for i in range(len(weights)):
			score = min(allDistances, key=lambda x: weightedSum(weights[i], x[0:6]))[6]
			sseArray[i] += (score - post['realScore']) ** 2
		count += 1
	with open('awesomeresults3.txt','w') as f:
		for i in range(len(weights)):
			f.write('%s\t%s\n' % (weights[i], sseArray[i] / len(testingData)))
