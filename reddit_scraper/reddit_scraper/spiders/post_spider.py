from scrapy.spider import BaseSpider
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
        items = []
        for story in raw_data['data']['children']:

            item = RedditScraperItem()
            item["title"] = story['data']['title']
            item["permalink"] = story['data']['permalink']
            item["post_id"] = story['data']['id']
            item["creation_time"] = story['data']['created_utc']
            item["domain"] = story['data']['domain']
            item["author"] = story['data']['author']
            item["subreddit"] = story['data']['subreddit']

            # what should we use for submission type? media_embed?
            # item["submission_type"] = story['data']['']
            
            items.append(item)
        
        # id of the last post received, for forming the next url like so:
        # http://reddit.com/r/doge/new.json?after=t3_1qluhk
        print raw_data['data']['after']

        return items

        pass
