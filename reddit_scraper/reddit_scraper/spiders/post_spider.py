from scrapy.spider import BaseSpider
import simplejson as json
import pprint
pp = pprint.PrettyPrinter()


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
            print story['data']['id'], story['data']['title']

        # id of the last post received, for forming the next url like so:
        # http://reddit.com/r/doge/new.json?after=t3_1qluhk
        print raw_data['data']['after']

        pass
