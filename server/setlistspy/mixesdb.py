from lxml import html
import requests
import re
from pprint import pprint

class MixesDBScraper:
    def __init__(self, DJ):
        set_urls = self.get_set_urls(DJ)
        self.tracklist = self.get_tracklist(set_urls)
        pprint(self.tracklist)

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
            tracks = self.clean(tracks)
            tracklist.extend(tracks)
        tracklist = set(tracklist)
        return tracklist

    def get_tree(self, url):
        page = requests.get(url)
        return html.fromstring(page.content)

    def clean(self, tracks):
        cleaned_tracks = list()
        pattern = re.compile('^(?:\[[\d:\?]*\])?[\s]?(?!\?)([^\[]*) - ([^\[]*)(\[.*])?$')
        for track in tracks:
            match = pattern.match(track.strip())
            if match:
                formatted_track = match.group(1) + " - " + match.group(2).strip()
                if match.group(3):
                    #Strip extraneously release info like # and year if necessary
                    label =  match.group(3)
                    label = label.split("-")[0].strip(" ]") + "]"
                    formatted_track = formatted_track + " " + label
                cleaned_tracks.append(formatted_track)
            else:
                print("BAD TRACK!!!! " + track)
        return cleaned_tracks
