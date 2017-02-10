from pprint import pprint
import psycopg2
from crawler.abstract import AbstractCrawler
from crawler.tracks import TracksParser
from models import Setlist, Track_Setlist_Link

#The purpose of this class is to scrape data from a MixesDB setlist url page in order to generate a data
#structure that can be used to seed or update the PostgresSQL database
class SetlistCrawler(AbstractCrawler):
    def __init__(self):
        AbstractCrawler.__init__(self)
        #Database values
        # self.row_id = False
        # self.dj_id = dj_id
        # self.url = url
        # self.track_ids = list()
        # self.multi_dj = False
        # self.multi_version = False
        # self.page_mod_time = False

        #Other attributes, including xpath components
        # self.dj_name = dj_name
        # self.current_dj_keyword = self.dj_name.split("(")[0].strip()
        self.no_comments_selector = "not(contains(@class,'commenttextfield'))"
        # self.tree = self.get_tree(url)
        # self.track_texts = list()
        # self.initial_seed = initial_seed
        self.crawl()
        return

    def crawl(self):
        conn = psycopg2.connect(database=self.db['database'], user=self.db['username'], password=self.db['password'], host=self.db['host'])
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dj")
        dj_rows = cursor.fetchmany(100)
        while len(dj_rows):
            for row in dj_rows:
                self.current_dj_keyword = row[1].split("(")[0].strip()
                dj_page_tree = self.get_tree(row[2])
                setlist_urls = dj_page_tree.xpath('//ul[@id="catMixesList"]/li/a/@href')
                setlist_urls = list(map(lambda url: self.base_url + url, setlist_urls))
                for setlist_url in setlist_urls:
                    #TODO: Get the page mod time the right way.
                    self.setlist_page_tree = self.get_tree(setlist_url)
                    print(setlist_url)
                    tracklist_headers = self.setlist_page_tree.xpath("//dl[parent::div[" + self.no_comments_selector + " and (child::ol or child::div)]]/dt/text()")
                    if len(tracklist_headers) > 1:
                        track_texts = self.crawl_multi_header(tracklist_headers)
                    else:
                        track_texts = self.crawl_single_dj()
                    print(track_texts)
            dj_rows = cursor.fetchmany(100)
        self.log_time()

    def get_page_mod_time(self):
        page_mod_time = self.tree.xpath("//li[@id='lastmod']/text()") #should be using PHP API to get the eexact
        if len(page_mod_time) > 1:
            page_mod_time = page_mod_time[1].strip()
        elif  len(page_mod_time) == 1:
            page_mod_time = page_mod_time[0]
        else:
            page_mod_time = "2010 Jan 1"
        return page_mod_time

    def parse_tracks(self):
        tparser = TracksParser(self.track_texts)
        tparser.build_tracklist_data()
        if self.save:
            tparser.save_to_db()
        else:
            pprint(tparser.tracks_info)
        self.track_ids = tparser.setlist_trackids

    def crawl_multi_header(self, tracklist_headers):
        '''When there are multiple headers in the tracklist section, determine if there are multiple
        artists in the tracklist and if there are multiple versions before handling'''
        for header in tracklist_headers:
            lowercase_header = header.lower()
            if self.current_dj_keyword.lower() in lowercase_header:
                self.multi_dj = True
            if "version" in lowercase_header:
                self.multi_version = True
        if self.multi_dj:
            self.crawl_multi_dj()
        else:
            self.crawl_single_dj()

    def crawl_single_dj(self):
        track_texts = self.setlist_page_tree.xpath("//ol[parent::*[" + self.no_comments_selector + "]]/li//text()")
        track_texts.extend(self.setlist_page_tree.xpath("//div[parent::*[" + self.no_comments_selector + "] and @class='list']/div[contains(@class, 'list-track')]//text()"))
        return track_texts
        # pprint(self.track_texts)

    def crawl_multi_dj(self):
        '''TODO: not working for DJ's with apostrophes/single quotes in name due to xpath'''
        belongs_to_dj_selector = "preceding-sibling::*[1]/dt[contains(text(), '" + self.current_dj_keyword + "')]"
        tracklist_condition = self.no_comments_selector + "] and " + belongs_to_dj_selector
        if not "'" in self.current_dj_keyword:
            track_texts = self.setlist_page_tree.xpath("//ol[parent::*[" + tracklist_condition + "]/li//text()")
            track_texts.extend(self.setlist_page_tree.xpath("//div[parent::*[" + tracklist_condition + " and @class='list']/div[contains(@class, 'list-track')]//text()"))
        # pprint(self.track_texts)
        return track_texts

    def b(self):
        if self.initial_seed:
            setlist = Setlist.create(dj=self.dj_id, url=self.url, track_ids=self.track_ids, multi_dj=self.multi_dj,
                                  multi_version=self.multi_version, page_mod_time=self.page_mod_time)
            for track_id in self.track_ids:
                Track_Setlist_Link.get_or_create(track=track_id, setlist=setlist.id)
        else:
            setlist, created = Setlist.create_or_get(dj=self.dj_id, url=self.url, track_ids=self.track_ids, multi_dj=self.multi_dj,
                                     multi_version=self.multi_version, page_mod_time=self.page_mod_time)
            for track_id in self.track_ids:
                Track_Setlist_Link.get_or_create(track=track_id, setlist=setlist.id)
