from pymongo import MongoClient
from datetime import datetime, timedelta
from scrapy.exceptions import DropItem
# from scrapy import log
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class RedditScraperPipeline(object):
    def __init__(self):
        self.ids_seen = set()
        
    def process_item(self, item, spider):
        if item['post_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['post_id'])
        
            client = MongoClient() #db connection defined here if it's not default
            db = client.reddit
            posts = db.posts
            # query database for post by ID
            db_post = posts.find_one(item['post_id'])
            
            if db_post:
                # if it's there, and the last measurement was more than 30
                # mins ago, push a new datapoint on score
                #log.msg("last post:" + str(db_post['scores'][-1]),level=log.DEBUG)
                
                last_check = db_post['scores'][-1][0]
                now = datetime.utcnow()
                d = timedelta(minutes=-30)
                if now+d > last_check:
                    posts.update(db_post,
                                 {'$push':{'scores':[datetime.utcnow(),
                                                     item["score"]]}})
            
            else:
                # if it's not there, create it
                # scores is a list of lists field- each element is [time,score]
                posts.insert({'_id':item['post_id'],
                              'title':item["title"],
                              'permalink':item["permalink"],
                              'creation_time':item["creation_time"],
                              'domain':item["domain"],
                              'author':item["author"],
                              'subreddit':item["subreddit"],
                              'media_embed':item["media_embed"],
                              'scores':[[datetime.utcnow(),
                                         item["score"]
                                     ]]
                          })
                
            return item
        
