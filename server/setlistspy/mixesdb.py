from lxml import html
import requests
import re
import collections
from pprint import pprint

class MixesDBScraper:
    def __init__(self):
        self.base_url = "http://www.mixesdb.com"
        return

    def get_api_search_url(self, search_input):
        #Get the MixesDB search URL for the category of the DJ that was entered
        #This method should handle capitalization & substring queries. TODO: handle when multiple search results
        search_query = "+".join(search_input.split())
        url = self.base_url + "/db/index.php?title=Special%3ASearch&profile=cats&search=" + search_query + "&fulltext=Search"
        tree = self.get_tree(url)
        api_search_url = tree.xpath("//div[@class='searchresults']/ul[1]//div[@class='mw-search-result-heading']/span[@class='search-result-isCat bold']/a/@href")[0]
        api_search_url = self.base_url + api_search_url
        print(api_search_url)
        return api_search_url

    def get_set_urls(self, search_input):
        search_url = self.get_api_search_url(search_input)
        tree = self.get_tree(search_url)
        set_urls = tree.xpath('//ul[@id="catMixesList"]/li/a/@href')
        print(set_urls)
        return set_urls

    def get_tracklist(self, set_urls):
        tracklist = list()
        for set_url in set_urls:
            scraper_url = self.base_url + set_url
            tree = self.get_tree(scraper_url)
            tracks = tree.xpath('//div[@id="mw-content-text"]//ol/li/text()')
            tracks.extend(tree.xpath('//div[@class="list-track"]/text()'))
            tracklist.extend(tracks)
        tracks_by_artist = self.build_trackdata(tracklist)
        formatted_tracklist = self.build_formatted_tracklist(tracks_by_artist)
        formatted_tracklist = set(formatted_tracklist)
        formatted_tracklist = list(formatted_tracklist)
        formatted_tracklist.sort()
        return formatted_tracklist

    def get_tree(self, url):
        page = requests.get(url)
        return html.fromstring(page.content)

    def build_trackdata(self, tracks):
        #Filters for tracks and builds collection of them w/ data structure: 'artist' -> ('tracktitle','label')
        tracks_by_artist = collections.defaultdict(list)
        labels_by_track = collections.defaultdict()
        pattern = re.compile('^(?:\[[\d:\?]*\])?[\s]?(?!\?)([^\[]*) - ([^\[]*)(\[.*])?$')
        for track in tracks:
            match = pattern.match(track.strip())
            if match:
                artist = match.group(1)
                tracktitle = match.group(2).strip()
                if match.group(3):
                    #Strip extraneously release info like # and year if necessary
                    label =  match.group(3)
                    label = label.split("-")[0].strip("[ ]")
                    labels_by_track[tracktitle] = label
                tracks_by_artist[artist].append(tracktitle)
            else:
                print("BAD TRACK!!!! " + track)
        trackdata = dict()
        trackdata["tracks_by_artist"] = tracks_by_artist
        trackdata["labels_by_track"] = labels_by_track
        pprint(trackdata)
        return trackdata

    def build_formatted_tracklist(self, trackdata):
        #Convert track collection to alphabetized list of tracks with format "***REMOVED***artist***REMOVED*** - ***REMOVED***tracktitle***REMOVED*** [label]"
        formatted_tracklist = []
        tracks_by_artist = trackdata["tracks_by_artist"]
        labels_by_track = trackdata["labels_by_track"]
        for artist,tracklist in tracks_by_artist.items():
            for tracktitle in tracklist:
                formatted_track = artist + " - " + tracktitle
                if tracktitle in labels_by_track:
                    formatted_track += " [" + labels_by_track[tracktitle] + "]"
                formatted_tracklist.append(formatted_track)
        return formatted_tracklist
