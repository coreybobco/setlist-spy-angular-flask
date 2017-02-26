import csv
import os
import time
from abstract.crawler import AbstractCrawler
from seeder.dj import DJSeeder

'''Iterates through the MixesDB's "Category: Artist" pages (200 DJ's per page), scrapes DJ names and URLs, and writes data to a CSV as rows'''
class DJCrawler(AbstractCrawler):
    def __init__(self):
        AbstractCrawler.__init__(self)

    def crawl(self, starting_url=False):
        self.url = starting_url if starting_url else self.base_url + "/w/Category:Artist"
        self.reset_csv('dj_import.csv')
        os.chdir("csv")
        while self.url != False:
            print(self.url)
            self.tree = self.get_tree(self.url)
            dj_names = self.tree.xpath("//ul[@id='catSubcatsList']//a/text()")
            dj_urls = self.tree.xpath("//ul[@id='catSubcatsList']//a/@href")
            with open('dj_import.csv', 'a', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                for idx, dj_url in enumerate(dj_urls):
                    writer.writerow([dj_names[idx],  self.base_url + dj_url])
            f.close()
            self.seek_next_page()
            self.url = False #BAD LINE
        os.chdir("../")
        print("Crawled DJs")
        self.log_time()

    def seek_next_page(self):
        next_url = self.tree.xpath("//div[@class='listPagination'][1]/a[contains(text(), 'next')]/@href")
        if len(next_url) and next_url[0] != None:
            self.url = self.base_url + next_url[0]
        else:
            self.url = False
