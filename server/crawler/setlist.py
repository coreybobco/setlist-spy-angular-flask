from pprint import pprint
from crawler.crawler import Crawler
from crawler.tracks import TracksParser
from models import Setlist, Track_Setlist_Link

#The purpose of this class is to scrape data from a MixesDB setlist url page in order to generate a data
#structure that can be used to seed or update the PostgresSQL database
class SetlistCrawler(Crawler):
    def __init__(self, dj_id, dj_name, url, save=False, initial_seed=False):
        Crawler.__init__(self)
        #Database values
        self.row_id = False
        self.dj_id = dj_id
        self.url = url
        self.track_ids = list()
        self.multi_dj = False
        self.multi_version = True
        self.page_mod_time = False

        #Other attributes, including xpath components
        self.dj_name = dj_name
        self.searchable_dj_name = self.dj_name.split("(")[0].strip()
        self.no_comments_selector = "not(contains(@class,'commenttextfield'))"
        self.tree = self.get_tree(url)
        self.track_texts = list()
        self.save = save #If not saving, print for debugging and testing purposes
        self.initial_seed = initial_seed
        return

    def crawl(self):
        tracklist = list()
        page_mod_time = self.tree.xpath("//li[@id='lastmod']/text()")
        if len(page_mod_time) > 1:
            self.page_mod_time = page_mod_time[1].strip()
        elif  len(page_mod_time) == 1:
            self.page_mod_time = page_mod_time[0]
        else:
            self.page_mod_time = "2010 Jan 1"
        self.tracklist_headers = self.tree.xpath("//dl[parent::div[" + self.no_comments_selector + " and (child::ol or child::div)]]/dt/text()")
        if len(self.tracklist_headers) > 1:
            self.crawl_multi_header()
        else:
            self.crawl_single_dj()
        tparser = TracksParser(self.track_texts)
        tparser.build_tracklist_data()
        if self.save:
            tparser.save_to_db()
        else:
            pprint(tparser.tracks_info)
        self.track_ids = tparser.setlist_trackids
        if self.save:
            self.save_to_db()
        return

    def crawl_multi_header(self):
        '''When there are multiple headers in the tracklist section, determine if there are multiple
        artists in the tracklist and if there are multiple versions before handling'''
        for header in self.tracklist_headers:
            lowercase_header = header.lower()
            if self.searchable_dj_name.lower() in lowercase_header:
                self.multi_dj = True
            if "version" in lowercase_header:
                self.multi_version = True
        if self.multi_dj:
            self.crawl_multi_dj()
        else:
            self.crawl_single_dj()
        return

    def crawl_single_dj(self):
        self.track_texts = self.tree.xpath("//ol[parent::*[" + self.no_comments_selector + "]]/li//text()")
        self.track_texts.extend(self.tree.xpath("//div[parent::*[" + self.no_comments_selector + "] and @class='list']/div[contains(@class, 'list-track')]//text()"))
        # pprint(self.track_texts)
        return

    def crawl_multi_dj(self):
        #TODO: For now this only works when the preceding header is an artist, not 'Part 2', 'Version 1', etc
        #Also not working for DJ's with apostrophes/single quotes in name due to xpath
        belongs_to_dj_selector = "preceding-sibling::*[1]/dt[contains(text(), '" + self.searchable_dj_name + "')]"
        tracklist_condition = self.no_comments_selector + "] and " + belongs_to_dj_selector
        if not "'" in self.searchable_dj_name:
            self.track_texts = self.tree.xpath("//ol[parent::*[" + tracklist_condition + "]/li//text()")
            self.track_texts.extend(self.tree.xpath("//div[parent::*[" + tracklist_condition + " and @class='list']/div[contains(@class, 'list-track')]//text()"))
        # pprint(self.track_texts)
        return

    def save_to_db(self):
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





