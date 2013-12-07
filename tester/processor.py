import sys, os
import json
from pymongo import MongoClient
from datetime import datetime, timedelta
from sklearn.cross_validation import KFold
sys.path.insert(0, '../learner')
from metrics import get_features, unweighted_distances

def getDistances(post, training):
	allDistances = []
	for t in training:
		distances = unweighted_distances(post, t)
		distances.append(t['realScore'])
		allDistances.append(distances)
	return allDistances

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

	print 'starting'
	currentFold = 1
	for train, test in kf:
		trainingIndices = train
		testingIndices = test
		trainingData = [postArray[i] for i in trainingIndices]
		testingData = [postArray[i] for i in testingIndices]

		for post in testingData:
			distances = getDistances(post, trainingData)
			path = os.path.join('data', 'fold%s' % (currentFold), post['id'])
			with open(path, 'w') as f:
				f.write(json.dumps(distances))

		currentFold += 1
