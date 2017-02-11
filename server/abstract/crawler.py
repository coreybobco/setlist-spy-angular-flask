from lxml import html
import requests
from abstract.parent import AbstractParent

#Abstract class for webcrawling from MixesDb
class AbstractCrawler(AbstractParent):
    def __init__(self):
        AbstractParent.__init__(self)
        self.base_url = "http://www.mixesdb.com"
        return

    def get_tree(self, url):
        page = requests.get(url)
        return html.fromstring(page.content)
