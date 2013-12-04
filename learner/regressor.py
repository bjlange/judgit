from metrics import post_distance
from heapq import nsmallest
class KNearest:
	def __init__(self, trainingData):
		self.data = trainingData
	def regress(self, item, k, weights):
		items = nsmallest(k, self.data, key=lambda x: post_distance(x, item, weights))
		scores = map(lambda x: x['realScore'], items)
		return sum(scores) / len(items)
