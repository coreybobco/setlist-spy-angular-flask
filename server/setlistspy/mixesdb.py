from lxml import html
import requests
import re
import collections
from pprint import pprint

class MixesDBScraper:
    def __init__(self):
        return

    def get_set_urls(self, DJ):
        DJ = "_".join(DJ.split())
        url = "http://www.mixesdb.com/w/Category:" + DJ
        tree = self.get_tree(url)
        set_urls = tree.xpath('//ul[@id="catMixesList"]/li/a/@href')
        return set_urls

    def get_tracklist(self, set_urls):
        tracklist = list()
        for set_url in set_urls:
            scraper_url = "http://www.mixesdb.com" + set_url
            tree = self.get_tree(scraper_url)
            tracks = tree.xpath('//div[@id="mw-content-text"]//ol/li/text()')
            tracklist.extend(tracks)
        trackdata_collection = self.build_trackdata_as_collection(tracklist)
        formatted_tracklist = self.build_formatted_tracklist(trackdata_collection)
        formatted_tracklist = set(formatted_tracklist)
        formatted_tracklist = list(formatted_tracklist)
        formatted_tracklist.sort()
        return formatted_tracklist

    def get_tree(self, url):
        page = requests.get(url)
        return html.fromstring(page.content)

    def build_trackdata_as_collection(self, tracks):
        #Filters for tracks and builds collection of them w/ data structure: 'artist' -> ('tracktitle','label')
        trackdata_collection = collections.defaultdict(list)
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
                    trackdata = tracktitle,label
                    trackdata_collection[artist].append(trackdata)
                else:
                    trackdata_collection[artist].append(tracktitle)
            else:
                print("BAD TRACK!!!! " + track)
        return trackdata_collection

    def build_formatted_tracklist(self, trackdata_collection):
        #Convert track collection to alphabetized list of tracks with format "***REMOVED***artist***REMOVED*** - ***REMOVED***tracktitle***REMOVED*** [label]"
        formatted_tracklist = []
        for artist,tracklist in trackdata_collection.items():
            for trackdata in tracklist:
                formatted_track = artist + " - "
                if type(trackdata) == tuple:
                    formatted_track = formatted_track + (" [").join(trackdata) + "]"
                else:
                    formatted_track = formatted_track + trackdata
                # formatted_track = formatted_track + (" [ ").join(trackdata) + "]" if type(trackdata) == "tuple" else formatted_track + trackdata
                # formatted_track = formatted_track + trackdata[1] if len(trackdata) == 2 else formatted_track
                formatted_tracklist.append(formatted_track)
        return formatted_tracklist