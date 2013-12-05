"""
The distance metrics for each of our features. scikit-learn's available
metrics in the DistanceMetric class are described here:

http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.DistanceMetric.html

Here are the metrics chosen for 

day of week:
time of day:
domain of content:
submission title:
submission author:
subreddit:
submission type:
"""

from sklearn.neighbors import DistanceMetric
from datetime import datetime
from Levenshtein import distance as ldist
from itertools import izip
import math
import re

splitter = re.compile(r'\W')
def get_features(post):
    dt = datetime.fromtimestamp(post['creation_time'])
    return {
        'day_of_week': dt.weekday(),
        'hour_of_day': dt.hour + dt.minute/60.,
        'domain': post['domain'],
        'title': set(splitter.split(post['title'].lower())),
        'author': post['author'],
        'subreddit': post['subreddit'],
    }

default_weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
def post_distance(a, b, weights=default_weights):
    distance = weights[0] * day_distance(a['day_of_week'], b['day_of_week']) +\
               weights[1] * hour_distance(a['hour_of_day'], b['hour_of_day']) +\
               weights[2] * domain_distance(a['domain'], b['domain']) +\
               weights[3] * title_distance(a['title'], b['title']) +\
               weights[4] * author_distance(a['author'], b['author']) +\
               weights[5] * subreddit_distance(a['subreddit'], b['subreddit'])
    return distance

def day_distance(a_day, b_day):
    dist = abs(a_day - b_day)
    return min(dist, 7 - a_day)

def hour_distance(a_hour, b_hour):
    dist = abs(a_hour - b_hour)
    return min(dist, 24 - dist)

def domain_distance(a_domain, b_domain):
    return ldist(a_domain, b_domain)

def title_distance(a_vect, b_vect):
    """
    Return the hamming distance between two word vectors
    """
    return len(a_vect | b_vect) - len(a_vect & b_vect)#sum(x != y for x, y in izip(a_vect, b_vect))

def author_distance(a_author, b_author):
    return ldist(a_author, b_author)

def subreddit_distance(a_subreddit, b_subreddit):
    return 0.0 if a_subreddit == b_subreddit else 1.0
