import csv
import time
from crawler.abstract import AbstractCrawler
from seeder.dj import DJSeeder

'''Iterates through the MixesDB's "Category: Artist" pages (200 DJ's per page), scrapes DJ names and URLs, and writes data to a CSV as rows'''
class DJListCrawler(AbstractCrawler):
    def __init__(self, starting_url = False):
        AbstractCrawler.__init__(self)
        # self.reset_csv()
        self.url = starting_url if starting_url else self.base_url + "/w/Category:Artist"
        self.crawl()
        s = DJSeeder()
        s.upsert()

    def crawl(self):
        self.url = False
        while self.url != False:
            print(url)
            self.tree = self.get_tree(self.url)
            dj_names = self.tree.xpath("//ul[@id='catSubcatsList']//a/text()")
            dj_urls = self.tree.xpath("//ul[@id='catSubcatsList']//a/@href")
            with open('dj.csv', 'a', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                for idx, dj_url in enumerate(dj_urls):
                    writer.writerow([dj_names[idx],  self.base_url + dj_url])
            f.close()
            self.url = self.seek_next_page()
        self.log_time()

    def seek_next_page(self):
        next_url = self.tree.xpath("//div[@class='listPagination'][1]/a[contains(text(), 'next')]/@href")
        if len(next_url) and next_url[0] != None:
            return self.base_url + next_url[0]
        else:
            return False

    def reset_csv(self):
        with open('dj.csv', 'w', newline='') as f:
            f.close()
