from scrapy.spider import BaseSpider
from scrapy.http import Request
from reddit_scraper.items import RedditScraperItem
import simplejson as json
from datetime import datetime, timedelta

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
        non_expired_count = 0
        for story in raw_data['data']['children']:

            # check to see if the story was last posted outside our
            # time window for data collection
            created = datetime.utcfromtimestamp(story['data']['created_utc'])
            now = datetime.utcnow()
            d = timedelta(hours=-48)

            # if it's fresh enough, create an item and send it to the pipeline
            if now+d < created:
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
                
                non_expired_count += 1

                # yield the item, Scrapy sends it to the item pipeline
                yield item
        
        # if there were any "fresh" stories on this page, go ahead and
        # build a request for the next one
        if non_expired_count > 0:
            # JSON includes the id of the last post received, for forming
            # the next url like so:
            # http://reddit.com/r/doge/new.json?after=t3_1qluhk
            subreddit_name = raw_data['data']['children'][0]['data']['subreddit']
            after = raw_data['data']['after']
            url = "http://reddit.com/r/%s/new.json?after=%s" % (subreddit_name, 
                                                                after)
        
            # yield http request, Scrapy will fire off this script for that one.
            yield Request(url, callback=self.parse)
