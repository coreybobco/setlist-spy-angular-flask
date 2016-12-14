from pprint import pprint
from crawler.crawler import Crawler
from crawler.dj import DJCrawler

# The purpose of this class is to iterate through the MixesDB "Category: Artist" pages (i.e. the DJ pages)
# so the postgresql database can be seeded or updated
class DJsCrawler(Crawler):
    def __init__(self, save=False, initial_seed=True):
        Crawler.__init__(self)
        #No database values, just these attributes
        self.url = self.base_url + "/w/Category:Artist"
        self.save = save
        self.initial_seed = initial_seed
        #self.url = self.tree.xpath("//div[@class='listPagination'][1]/a[contains(text(), 'next')]/@href")[0]
        return

    def crawl_categories_pages(self):
        while self.url != False:
            self.crawl_categories_page()
            next_url = self.tree.xpath("//div[@class='listPagination'][1]/a[contains(text(), 'next')]/@href")
            if len(next_url):
                self.url = self.base_url + next_url[0]
            else:
                self.url = False
        return

    def crawl_categories_page(self):
        # Only run if db is initialized and empty
        # First begin iterating through list of "Category:Artist" pages, i.e. dj's
        self.tree = self.get_tree(self.url)
        dj_urls = self.tree.xpath("//ul[@id='catSubcatsList']//a/@href")
        dj_urls = list(map(lambda url: self.base_url + url, dj_urls))
        pprint(dj_urls)
        for dj_url in dj_urls:
            dj_crawler = DJCrawler(dj_url, self.save, self.initial_seed)
            dj_crawler.crawl()
        return