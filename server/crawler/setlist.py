from pprint import pprint
import psycopg2
from abstract.crawler import AbstractCrawler
import db
from crawler.tracks import TracksParser
from models import Setlist, Track_Setlist_Link

#The purpose of this class is to scrape data from a MixesDB setlist url page in order to generate a data
#structure that can be used to seed or update the PostgresSQL database
class SetlistCrawler(AbstractCrawler):
    def __init__(self):
        AbstractCrawler.__init__(self)
        self.no_comments_selector = "not(contains(@class,'commenttextfield'))"
        return

    def crawl(self):
        conn, cursor = db.connect()
        cursor.execute("SELECT * FROM dj")
        dj_rows = cursor.fetchmany(100)
        while len(dj_rows):
            for row in dj_rows:
                self.current_dj_keyword = row[1].split("(")[0].strip()
                setlist_urls = self.get_setlist_urls(row[2])
                conn.commit()
            dj_rows = cursor.fetchmany(100)
        self.log_time()

    def get_tracks(setlist_url):
        setlist_page_tree = self.get_tree(setlist_url)
        headers_xpath = "//dl[parent::div[" + self.no_comments_selector + " and (child::ol or child::div)]]/dt/text()"
        headers_before_tracklist = setlist_page_tree.xpath(headers_xpath)
        for header in headers_before_tracklist:
            lowercase_header = header.lower()
            if self.current_dj_keyword.lower() in lowercase_header:
                return get_tracks_from_solo_dj_set()
            if "version" in lowercase_header:
                return self.get_tracks_from_solo_dj_set
        if len(headers_before_tracklist) > 1:
            return self.get_tracks_when_multiple_djs
        else:
            return self.

    def get_setlist_urls(self, dj_url):
        whie dj_url != False:
            dj_tree = self.get_tree(dj_url)
            scraped_setlist_urls = dj_tree.xpath('//ul[@id="catMixesList"]/li/a/@href')
            more_results_url = tree.xpath("//div[@class='listPagination'][1]/a[contains(text(), 'next')]/@href")
            dj_url = self.base_url + next_url[0] if len(more_results_url) else False
        scraped_setlist_urls = list(map(lambda url: self.base_url + url, scraped_setlist_urls))
        return scraped_setlist_urls

    def parse_tracks(self):
        tparser = TracksParser(self.track_texts)
        tparser.build_tracklist_data()
        if self.save:
            tparser.save_to_db()
        else:
            pprint(tparser.tracks_info)
        self.track_ids = tparser.setlist_trackids

    def get_tracks_when_multiple_djs(self, tracklist_headers):
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

    def get_tracks_when_one_dj(self):
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

    def get_page_mod_time(self):
        page_mod_time = self.tree.xpath("//li[@id='lastmod']/text()") #should be using PHP API to get the eexact
        if len(page_mod_time) > 1:
            page_mod_time = page_mod_time[1].strip()
        elif  len(page_mod_time) == 1:
            page_mod_time = page_mod_time[0]
        else:
            page_mod_time = "2010 Jan 1"
        return page_mod_time
