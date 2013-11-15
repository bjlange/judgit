# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class RedditScraperItem(Item):
    title = Field()
    post_id = Field()
    creation_time = Field()
    domain = Field()
    author = Field()
    subreddit = Field()
    submission_type = Field()

