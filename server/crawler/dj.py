from lxml import html
import requests
from pprint import pprint
from crawler.crawler import Crawler
from crawler.setlist import SetlistCrawler
from models import DJ

#The purpose of this class is to scrape data from a MixesDB setlist url page in order to generate a data
#structure that can be used to seed or update the PostgresSQL database
class DJCrawler(Crawler):
    def __init__(self, url, initial_seed):
        Crawler.__init__(self)
        #Database values
        self.row_id = False
        self.name = ''
        self.url = url

        #Other variables
        self.initial_seed = initial_seed
        return

    def crawl(self):
        tree = self.get_tree(self.url)
        self.name = tree.xpath("//h1[@id='firstHeading']/text()")[0][9::]
        self.save_to_db()
        set_urls = tree.xpath('//ul[@id="catMixesList"]/li/a/@href')
        set_urls = list(map(lambda url: self.base_url + url, set_urls))
        for set_url in set_urls:
            setlist_crawler = SetlistCrawler(self.row_id, self.name, set_url, self.initial_seed)
            setlist_crawler.crawl()

    def save_to_db(self):
        if self.initial_seed:
            data = DJ.create(name=self.name, url=self.url)
        else:
            data, created = DJ.get_or_create(name=name, url=url)
        self.row_id = data.id
        return



