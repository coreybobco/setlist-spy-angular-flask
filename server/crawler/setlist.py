from lxml import html
import requests

#Abstract class for webcrawling from MixesDb
#The purpose of this class is to scrape data from a MixesDB setlist url page in order to generate a data
#structure that can be used to seed or update the PostgresSQL database
class SetlistCrawler(Crawler):
    def __init__(self, dj_name, url):
        Crawler.__init__(self)
        self.dj_name = dj_name
        self.url = url
        self.multi_tracklist = False

    def crawl_setlist_page(self):
        tracklist = list()
        tree = self.get_tree(set_url)
        mod_time = tree.xpath("//li[@id='lastmod']/text()")[1].strip()
        self.tracklist_headers = tree.xpath("//dl[parent::div[" + self.no_comments_selector + " and (child::ol or child::div)]]/dt/text()")
        print(tracklist_headers)
        if len(tracklist_headers) > 1:
            self.crawl_multi_tracklist()
        # setlist = tree.xpath('//div[@id="mw-content-text"]//ol/li/text()')
        print(tree.xpath("//div[parent::div[" + self.no_comments_selector + "] and @class='list']/div[contains(@class, 'list-track')]/text()"))
        # setlist.extend(tree.xpath("//div[parent::div[" + self.no_comments_selector + " and @class='list']/div[contains(@class, 'list-track')]/text()"))
        # tracklist.extend(setlist)
        # self.build_tracklist_data(tracklist)
        # self.build_formatted_tracklist()
        # return self.formatted_tracklist'

    def crawl_multi_tracklist(self):
        #When there are multiple versions of a tracklist, this method should combine and sort them by order.
        #When the tracklists is for multiple DJ's, this 
        #Gets headers

        #XPATH FOR EXTRACTING JUST DJ IN QUESTION SET
        #$x("//ol[preceding-sibling::dl[1]/dt[contains(text()," + dj_name + ")]]")




