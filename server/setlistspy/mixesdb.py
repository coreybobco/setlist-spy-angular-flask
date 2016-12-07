from lxml import html
import requests
import re
import collections
from pprint import pprint

class MixesDBScraper:
    def __init__(self):
        self.base_url = "http://www.mixesdb.com"
        self.tracklist_data = dict()
        self.tracks_by_artist = collections.defaultdict(list)
        self.labels_by_track = collections.defaultdict()
        self.track_regex = re.compile('^(?:\[[\d:\?]*\])?[\s]?(?!\?)([^\[]*) - ([^\[]*)(\[.*])?$')
        self.formatted_tracklist = list()
        return

    def get_api_search_url(self, search_input):
        #Get the MixesDB search URL for the category of the DJ that was entered
        #This method should handle capitalization & substring queries. TODO: handle when multiple search results
        search_query = "+".join(search_input.split())
        url = self.base_url + "/db/index.php?title=Special%3ASearch&profile=cats&search=" + search_query + "&fulltext=Search"
        tree = self.get_tree(url)
        search_url_anchor = tree.xpath("//div[@class='searchresults']/ul[1]//div[@class='mw-search-result-heading']/span[@class='search-result-isCat bold']/a/@href")
        if len(search_url_anchor):
            return self.base_url + search_url_anchor[0]
        else:
            raise NameError("No search results")

    def get_set_urls(self, search_input):
        search_url = self.get_api_search_url(search_input)
        tree = self.get_tree(search_url)
        set_urls = tree.xpath('//ul[@id="catMixesList"]/li/a/@href')
        return set_urls

    def get_tracklist(self, set_urls):
        tracklist = list()
        for set_url in set_urls:
            scraper_url = self.base_url + set_url
            tree = self.get_tree(scraper_url)
            setlist = tree.xpath('//div[@id="mw-content-text"]//ol/li/text()')
            setlist.extend(tree.xpath("//div[parent::div[not(contains(@class, 'commenttextfield'))] and @class='list']/div[contains(@class, 'list-track')]/text()"))
            tracklist.extend(setlist)
        self.build_tracklist_data(tracklist)
        self.build_formatted_tracklist()
        return self.formatted_tracklist

    def get_tree(self, url):
        page = requests.get(url)
        return html.fromstring(page.content)

    def build_tracklist_data(self, track_texts):
        #Filters for tracks and builds collection of them w/ data structure: 'artist' -> ('tracktitle','label')
        for track_text in track_texts:
            self.validate_and_extract_track_data(track_text)

    def validate_and_extract_track_data(self, track_text):
        match = self.track_regex.match(track_text.strip())
        if match:
            artist = match.group(1)
            tracktitle = match.group(2).strip()
            if match.group(3):
                #Strip extraneously release info like # and year if necessary
                label =  match.group(3)
                label = label.split("-")[0].strip("[ ]")
                self.labels_by_track[tracktitle] = label
            self.tracks_by_artist[artist].append(tracktitle)
        else:
            print("BAD TRACK!!!! " + track_text)

    def build_formatted_tracklist(self):
        #Convert track collection to alphabetized list of tracks with format "***REMOVED***artist***REMOVED*** - ***REMOVED***tracktitle***REMOVED*** [label]"
        print(self.tracks_by_artist)
        for artist,tracklist in self.tracks_by_artist.items():
            for tracktitle in tracklist:
                formatted_track = artist + " - " + tracktitle
                if tracktitle in self.labels_by_track:
                    formatted_track += " [" + self.labels_by_track[tracktitle] + "]"
                self.formatted_tracklist.append(formatted_track)
        self.formatted_tracklist = set(self.formatted_tracklist)
        self.formatted_tracklist = list(self.formatted_tracklist)
        self.formatted_tracklist.sort()
