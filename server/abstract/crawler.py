from lxml import html
import requests
from abstract.parent import AbstractParent
from urllib.parse import urlparse, urlencode
from pprint import pprint

#Abstract class for webcrawling from MixesDb
class AbstractCrawler(AbstractParent):
    def __init__(self):
        AbstractParent.__init__(self)
        self.base_url = "http://www.mixesdb.com"
        return

    def get_tree(self, url):
        page = requests.get(url)
        return html.fromstring(page.content)

    def get_page_mod_time(self, url):
        page_title = urlparse(url).path[3:]
        query_params = { "action" : "query",
                         "format": "json",
                         "prop":    "revisions",
                         "titles":  page_title,
                         "rvprop":  "timestamp"
                       }
        api_endpoint = "http://mixesdb.com/db/api.php?action=query&" + urlencode(query_params)
        revision_json = requests.get(api_endpoint).json()
        mod_time = list(revision_json['query']['pages'].values())[0]['revisions'][0]['timestamp'][:-1].replace("T", " ")
        return mod_time
