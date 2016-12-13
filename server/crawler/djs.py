from lxml import html
import requests
from pprint import pprint
from crawler.crawler import Crawler
from crawler.dj import DJCrawler

# The purpose of this class is to iterate through the MixesDB "Category: Artist" pages (i.e. the DJ pages)
# so the postgresql database can be seeded or updated
class DJsCrawler(Crawler, initial_seed):
    def __init__(self, url):
        Crawler.__init__(self)
        self.url = self.base_url + "/w/Category:Artist"
        self.tree = self.get_tree(dj_categories_url)
        self.crawl_categories_page()
        #self.url = self.tree.xpath("//div[@class='listPagination'][1]/a[contains(text(), 'next')]/@href")[0]
        return

    def crawl_categories_pages(self):
        return

    def crawl_categories_page(self):
        # Only run if db is initialized and empty
        # First begin iterating through list of "Category:Artist" pages, i.e. dj's
        dj_urls = self.tree.xpath("//ul[@id='catSubcatsList']//a/@href")
        dj_urls = list(map(lambda url: self.base_url + url, dj_urls))
        for dj_url in dj_urls:
            dj_crawler = DJCrawler(url, self.initial_seed)
            dj_crawler.crawl()
        return