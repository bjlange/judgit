import sys
from pymongo import MongoClient
from datetime import datetime, timedelta
from sklearn.cross_validation import KFold
import numpy as np
sys.path.insert(0, '../learner')
from regressor import KNearest
from metrics import get_features

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

kf = KFold(len(postArray), n_folds=30, indices=True)

trainingIndices = None
testingIndices = None

for train, test in kf:
	trainingIndices = train
	testingIndices = test

trainingData = [postArray[i] for i in trainingIndices]
testingData = [postArray[i] for i in testingIndices]

regressor = KNearest(trainingData)

for post in testingData:
	print 'predicted: %s\treal:%s' % (regressor.regress(post, 1, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), post['realScore'])
