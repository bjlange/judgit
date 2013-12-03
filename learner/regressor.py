from metrics import post_distance
from heapq import nsmallest
class KNearest:
	def __init__(self, trainingData, values):
		self.data = trainingData
	def regress(self, item, k):
		items = nsmallest(k, self.data, key=lambda x: post_distance(x, item))
		scores = map(lambda x: x.realScore, items)
		return sum(scores) / len(items)
