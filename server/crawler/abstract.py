from lxml import html
import requests
import time

#Abstract class for webcrawling from MixesDb
class AbstractCrawler:
    def __init__(self):
        self.base_url = "http://www.mixesdb.com"
        self.start_time = time.time()
        return

    def get_tree(self, url):
        page = requests.get(url)
        return html.fromstring(page.content)

    def log_time(self):
        print("--- %s seconds to upsert values---" % (time.time() - self.start_time))
