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
from Levenshtein import distance


def get_features(post):
    dt = datetime.fromtimestamp(post['creation_time'])
    return {
        'day_of_week': dt.weekday(),
        'hour_of_day': dt.hour + dt.minute/60.,
        'domain': post['domain'],
        'title': post['title'],
        'author': post['author'],
        'subreddit': post['subreddit'],
    }


def edit_distance(a, b):
    pass


