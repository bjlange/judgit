from pymongo import MongoClient
from datetime import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class RedditScraperPipeline(object):
    def process_item(self, item, spider):
        client = MongoClient() #db connection defined here if it's not default
        db = client.reddit
        posts = db.posts
        # query database for post by ID
        db_post = posts.find_one(item['post_id'])
        
        if db_post:
            # if it's there, push a new datapoint on score
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
        
