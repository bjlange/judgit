import sys
from pymongo import MongoClient
from datetime import datetime, timedelta
from sklearn.cross_validation import KFold
sys.path.insert(0, '../learner')
from regressor import KNearest
from metrics import get_features, unweighted_distances
from heapq import nsmallest

def weightedSum(weights, values):
	return sum(map(lambda x,y: x*y, weights, values))

def getDistances(post, training):
	allDistances = []
	for t in training:
		distances = unweighted_distances(post, t)
		distances.append(t['realScore'])
		allDistances.append(distances)
	return allDistances


def testK(kArray, testingData, trainingData):
	sseArray = [0.0] * len(kArray)
	print 'starting'
	count = 1
	for post in testingData:
		print count
		allDistances = getDistances(post, trainingData)
		for i in range(len(kArray)):
			items = nsmallest(kArray[i], allDistances, key=lambda x: weightedSum([1.0, 1.0, 1.0, 1.0, 1.0, 1.0], x[0:6]))
			scores = map(lambda x: x[6], items)
			score = sum(scores) / len(items)
			sseArray[i] += (score - post['realScore']) ** 2
		count += 1
	return sseArray

def calcMSE(fold, testingData, trainingData):
	sse = 0.0
	count = 1
	for post in testingData:
		print '%s %s' % (fold, count)
		allDistances = getDistances(post, trainingData)
		items = nsmallest(5, allDistances, key=lambda x: weightedSum([1.0, 0.0, 4.0, 0.0, .25, 0.0], x[0:6]))
		scores = map(lambda x: x[6], items)
		score = sum(scores) / len(items)
		sse += (score - post['realScore']) ** 2
		count += 1
	return sse / len(testingData)

def calcPriorMSE(testingData, trainingData):
	sse = 0.0
	for post in testingData:
		sse += (38.0594 - post['realScore']) ** 2
	return sse / len(testingData)


if __name__ == '__main__':
	division = int(sys.argv[1])

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

	kf = KFold(len(postArray), n_folds=2, indices=True, random_state=42)

	trainingIndices = None
	testingIndices = None

	for train, test in kf:
		trainingIndices = train
		testingIndices = test
		break

	trainingData = [postArray[i] for i in trainingIndices]
	testingData = [postArray[i] for i in testingIndices]

	kf2 = KFold(len(testingData), n_folds=30, indices=True, random_state=42)
	toRegressIndices = None
	toUseIndices = None
	foldCount = 0
	mseArray = [0.0] * 30
	priorMSEArray = [0.0] * 30
	for train, test in kf2:
		if (division == 0 and foldCount <= 15) or (division == 1 and foldCount > 15):
			toRegressIndices = test
			toUseIndices = train
			toRegress = [testingData[i] for i in toRegressIndices]
			toUse = [testingData[i] for i in toUseIndices]

			print 'train:%s test:%s' % (len(toRegress), len(toUse))
			mseArray[foldCount] = calcMSE(foldCount, toRegress, toUse)
			priorMSEArray[foldCount] = calcPriorMSE(toRegress, toUse)
		foldCount += 1


	with open('validate%s.txt' % (division),'w') as f:
		for i in range(len(mseArray)):
			f.write('%s\t%s\n' % (i, mseArray[i]))
	with open('validatePrior%s.txt' % (division), 'w') as f:
		for i in range(len(priorMSEArray)):
			f.write('%s\t%s\n' % (i, priorMSEArray[i]))
