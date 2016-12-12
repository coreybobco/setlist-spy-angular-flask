from lxml import html
import requests

#Abstract class for webcrawling from MixesDb
class Crawler:
    def get_tree(self, url):
        def __init__(self):
            self.base_url = "http://www.mixesdb.com"
            self.no_comments_selector = "not(contains(@class,'commenttextfield'))"

        def get_tree(self, url):
            page = requests.get(url)
            return html.fromstring(page.content)
