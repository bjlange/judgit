from metrics import post_distance
from heapq import nsmallest
import bottleneck
class KNearest:
	def __init__(self, trainingData):
		self.data = trainingData
	def regress(self, item, k, weights):
		#items = bottleneck.partsort([[post_distance(x, item, weights), x] for x in self.data], n=k, axis=0)
		#scores = map(lambda x: x[1]['realScore'], items)
		#return sum(scores) / len(items)
		items = nsmallest(k, self.data, key=lambda x: post_distance(x, item, weights))
		scores = map(lambda x: x['realScore'], items)
		return sum(scores) / len(items)
