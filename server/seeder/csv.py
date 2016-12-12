from lxml import html
import requests
import re
import collections
from pprint import pprint
import csv

class CSV_Seeder:
    def __init__(self):
        self.base_url = "http://www.mixesdb.com"
        self.base_api_url = "http://www.mixesdb.com/db/api.php"
        self.djs = list()
        self.current_dj_row_id = 1;
        self.csv_headers = ***REMOVED***"dj.csv": "name,url",
                            "setlist.csv": "dj,url,order,page_mod_time"***REMOVED***
        # self.seed_csvs()
        self.no_comments_selector = "not(contains(@class,'commenttextfield'))"
        return

    def seed_csvs(self):
        self.reset_csvs()
        self.crawl_dj_categories()

    def crawl_dj_categories(self):
        # Only run if db is initialized and empty
        # First begin iterating through list of "Category:Artist" pages, i.e. dj's
        dj_categories_url = self.base_url +  "/w/Category:Artist"
        tree = self.get_tree(dj_categories_url)
        dj_urls = tree.xpath("//ul[@id='catSubcatsList']//a/@href")
        dj_urls = dj_urls[:8]
        dj_urls = list(map(lambda url: self.base_url + url, dj_urls))
        for dj_url in dj_urls:
            self.crawl_dj_page(dj_url)
            self.current_dj_row_id = self.current_dj_row_id + 1
            print(dj_url)
        print(self.djs)
        self.write_to_csv("djs.csv", djs)
        #pprint(dj_urls)
        #dj_categories_url = tree.xpath("//div[@class='listPagination'][1]/a[contains(text(), 'next')]/@href")[0]
        dj_categories_url = False
        print(dj_categories_url)
        return

    def crawl_dj_page(self, dj_url):
        tree = self.get_tree(dj_url)
        dj_name = tree.xpath("//h1[@id='firstHeading']/text()")[0][9::]
        self.djs.append([dj_name, dj_url])
        set_urls = tree.xpath('//ul[@id="catMixesList"]/li/a/@href')
        set_urls = list(map(lambda url: self.base_url + url, set_urls))
        for set_url in set_urls:
          self.crawl_setlist_page(dj_name, set_url)
        return

    def crawl_setlist_page(self, dj_name, set_url):
        tracklist = list()
        tree = self.get_tree(set_url)
        mod_time = tree.xpath("//li[@id='lastmod']/text()")[1].strip()
        xpath = "//dl[parent::div[" + self.no_comments_selector + " and (child::ol or child::div)]]"
        print(xpath)
        tracklist_headers = tree.xpath(xpath)
        print(tracklist_headers)
        # setlist = tree.xpath('//div[@id="mw-content-text"]//ol/li/text()')
        print(tree.xpath("//div[parent::div[" + self.no_comments_selector + "] and @class='list']/div[contains(@class, 'list-track')]/text()"))
        # setlist.extend(tree.xpath("//div[parent::div[" + self.no_comments_selector + " and @class='list']/div[contains(@class, 'list-track')]/text()"))
        # tracklist.extend(setlist)
        # self.build_tracklist_data(tracklist)
        # self.build_formatted_tracklist()
        # return self.formatted_tracklist'

        #Gets headers

        #XPATH FOR EXTRACTING JUST DJ IN QUESTION SET
        #$x("//ol[preceding-sibling::dl[1]/dt[contains(text()," + dj_name + ")]]")

    def reset_csvs(self):
        for filename,headers in self.csv_headers.items():
          print(filename)
          print(headers)
          f = open(filename, "w+")
          f.write(headers)
          f.close()

    def write_to_csv(filename, rows):
        print(self.djs)
        with open('filename', 'w', newline='') as csvfile:
          writer = csv.writer(csvfile, delimiter=',',
                                  quotechar='|', quoting=csv.QUOTE_MINIMAL)
          for row in rows:
            writer.writerow(row)
        return

    def get_tree(self, url):
        page = requests.get(url)
        return html.fromstring(page.content)
