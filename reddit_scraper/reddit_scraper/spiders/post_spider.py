from scrapy.spider import BaseSpider
from scrapy.http import Request
from reddit_scraper.items import RedditScraperItem
import simplejson as json
import pprint
pp = pprint.PrettyPrinter()

#           /      \
#        \  \  ,,  /  /
#         '-.`\()/`.-'
#        .--_'(  )'_--.
#       / /` /`""`\ `\ \
#        |  |  ><  |  |
#        \  \      /  /
#            '.__.'
#   we climbin in ya internets
#   we snatchin your reddits up

class PostSpider(BaseSpider):
    name = "reddit_post"
    allowed_domains = ["reddit.com"]
    start_urls = [
        # TODO: pick some subreddits
        "http://reddit.com/r/doge/new.json",
    ]

    def parse(self, response):
        raw_data = json.loads(response.body)
        for story in raw_data['data']['children']:

            item = RedditScraperItem()
            item["title"] = story['data']['title']
            item["permalink"] = story['data']['permalink']
            item["post_id"] = story['data']['id']
            item["creation_time"] = story['data']['created_utc']
            item["domain"] = story['data']['domain']
            item["author"] = story['data']['author']
            item["subreddit"] = story['data']['subreddit']

            if story['data']['media'] == "null":
                item["media_embed"] = True
            else:
                item["media_embed"] = False
            
            # yield the item, Scrapy sends it to the item pipeline
            yield item
        
        # JSON includes the id of the last post received, for forming
        # the next url like so:
        # http://reddit.com/r/doge/new.json?after=t3_1qluhk
        subreddit_name = raw_data['data']['children'][0]['data']['subreddit']
        after = raw_data['data']['after']
        url = "http://reddit.com/r/%s/new.json?after=%s" % (subreddit_name, 
                                                            after)
        
        # yield http request, Scrapy will fire off this script for that one.
        yield Request(url, callback=self.parse)
