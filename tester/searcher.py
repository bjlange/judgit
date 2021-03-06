import sys
from pymongo import MongoClient
from datetime import datetime, timedelta
from sklearn.cross_validation import KFold
sys.path.insert(0, '../learner')
from regressor import KNearest
from metrics import get_features

if __name__ == '__main__':

	client = MongoClient()
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

	trainingData = [postArray[i] for i in trainingIndices]
	testingData = [postArray[i] for i in testingIndices]

	regressor = KNearest(trainingData)

	#import cProfile
	print 'starting'
	with open('results.txt', 'w') as f:
		for i in range(3):
			for val in [0.0, .25, .5, 2.0, 4.0]:
				weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
				sse = 0
				weights[i] = val
				for post in testingData:
					sse += (regressor.regress(post, 1, weights) - post['realScore']) ** 2
				mse =  sse / len(testingData)
				results = 'weights = %s\tk = %s\tmse = %s\n' % (weights, 1, mse)
				print results
				f.write(results)
