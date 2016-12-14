from pprint import pprint
from crawler.crawler import Crawler
from crawler.setlist import SetlistCrawler
from models import DJ

#The purpose of this class is to scrape data from a MixesDB setlist url page in order to generate a data
#structure that can be used to seed or update the PostgresSQL database
class DJCrawler(Crawler):
    def __init__(self, url, save=False, initial_seed=False):
        Crawler.__init__(self)
        #Database values
        self.row_id = False
        self.name = ''
        self.url = url

        #Other variables
        self.save = save #If not saving, print for debugging and testing purposes
        self.initial_seed = initial_seed
        return

    def crawl(self):
        tree = self.get_tree(self.url)
        self.name = tree.xpath("//h1[@id='firstHeading']/text()")[0][9::]
        if self.save:
            self.save_to_db()
        else:
            pprint(self)
        while self.url != False:
            set_urls = tree.xpath('//ul[@id="catMixesList"]/li/a/@href')
            set_urls = list(map(lambda url: self.base_url + url, set_urls))
            for set_url in set_urls:
                setlist_crawler = SetlistCrawler(self.row_id, self.name, set_url, self.save, self.initial_seed)
                setlist_crawler.crawl()
            next_url = tree.xpath("//div[@class='listPagination'][1]/a[contains(text(), 'next')]/@href")
            if len(next_url):
                self.url = self.base_url + next_url[0]
                tree = self.get_tree(self.url)
            else:
                self.url = False
        return

    def save_to_db(self):
        if self.initial_seed:
            data = DJ.create(name=self.name, url=self.url)
        else:
            data, created = DJ.get_or_create(name=self.name, url=self.url)
        self.row_id = data.id
        return



