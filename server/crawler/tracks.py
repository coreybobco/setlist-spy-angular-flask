#This class will parse a setlist for artists, titles, and labels and add those to the database if they
#do not already exist. The Setlist Parser class will also use the ID's of these it grabs so it can store
#the setlist by track id.
import re
from models import Artist, Label, Track, Artist

class TracksParser:
    def __init__(self, track_texts):
        self.track_texts = track_texts
        self.track_regex = re.compile('^(?:\[[\d:\?]*\])?[\s]?(?!\?)([^\[]*) - ([^\[]*)(\[.*])?$')
        self.tracks_info = list()
        self.setlist_trackids = list()

    def build_tracklist_data(self):
        #Filters for tracks and builds collection of them w/ data structure: 'artist' -> ('tracktitle','label')
        for track_text in self.track_texts:
            self.validate_and_extract_track_data(track_text)

    def validate_and_extract_track_data(self, track_text):
        match = self.track_regex.match(track_text.strip())
        if match:
            track_info['artist'] = match.group(1)
            track_info['title'] = match.group(2).strip()
            if match.group(3):
                #Strip extraneously release info like # and year if necessary
                label = match.group(3)
                track_info['label'] = label.split("-")[0].strip("[ ]")
            self.tracks_info.append(track_info)
        else:
            print("BAD TRACK!!!! " + track_text)

    def save_to_db():
        self.build_tracklist_data()
        for track_info in self.tracks_info:
            artist = Artist.get_or_create(name=track_info['artist'])
            label = Label.get_or_create(name=track_info['label'])
            track = Track.create_or_get(artist=artist.id, title=track_info['title'], label=label.id)
            self.setlist_trackids.append(track.id)
        return



