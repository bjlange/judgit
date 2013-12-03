from pymongo import MongoClient
from datetime import datetime, timedelta
from sklearn.cross_validation import KFold
client = MongoClient()
db = client.reddit
posts = db.posts

# first load everything into memory
postArray = []
scoreArray = []

for post in posts.find():
	# find latest score that's after the 24 hour mark
	scoreToUse = 0
	submissionTime = datetime.fromtimestamp(post['creation_time'])
	delta = timedelta(days=1)
	for score in post['scores']:
		scoreToUse = score[1]
		if (submissionTime + delta) < score[0]:
			break
	scoreArray.append(scoreToUse)
	postArray.append(post)

averageScore = float(sum(scoreArray)) / float(len(scoreArray))
averageScore = int(averageScore)
print averageScore

kf = KFold(len(scoreArray), n_folds=30, indices=True)

sseArray = []
for train, test in kf:
	sse = 0
	for testIndex in test:
		sse += (averageScore - scoreArray[testIndex]) ** 2
	sseArray.append(sse)
print sseArray
