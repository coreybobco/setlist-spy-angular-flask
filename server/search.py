from crawler.search import SearchCrawler
import json
import psycopg2

'''TODO: Improve search handling to use PostgreSQL trigrams, making top search result the assumption
         and secondary search results suggestions.'''
class Search:
    def __init__(self, search_input):
        sc = SearchCrawler()
        self.search_term = sc.get_api_search_url(search_input)
        self.results = ***REMOVED***"dj_tracks":***REMOVED******REMOVED***, "artist_tracks":***REMOVED******REMOVED******REMOVED***
        db = json.load(open("db.json"))
        conn = psycopg2.connect(database=db['database'], user=db['username'], password=db['password'], host=db['host'])
        self.cur = conn.cursor()
        self.get_dj_tracks()
        self.get_artist_tracks()
        return

    def get_dj_tracks(self):
        sql = """SELECT DISTINCT artist.name, track.title, label.name FROM track
                 JOIN artist ON track.artist_id = artist.id
                 LEFT JOIN label ON track.label_id = label.id
                 WHERE track.id IN (SELECT track_id FROM track_setlist_link
                 WHERE setlist_id IN (SELECT id from setlist WHERE dj_id =
                 (SELECT id FROM dj WHERE name = %s)))
                 ORDER BY artist.name;"""
        self.cur.execute(sql, (self.search_term,))
        rows = self.cur.fetchall()
        for artist,track,label in rows:
            self.results['dj_tracks'].setdefault(artist,[]).append((track,label))
        return
        # dj_tracks = ***REMOVED***artist:(track,label) for artist,track,label in self.cur.fetchall()***REMOVED***
        # return dj_tracks
        # return self.cur.fetchall()

    def get_artist_tracks(self):
        sql = """SELECT track.title, label.name, dj.name, setlist.url FROM track
                LEFT JOIN label ON label.id = track.label_id
                JOIN artist ON track.artist_id = artist.id
                JOIN track_setlist_link on track_setlist_link.track_id = track.id
                JOIN setlist on setlist.id = track_setlist_link.setlist_id
                JOIN dj on dj.id = setlist.dj_id where artist.name = %s ORDER BY track.title;"""
        self.cur.execute(sql, (self.search_term,))
        rows = self.cur.fetchall()
        for track,label,dj,setlist_url in rows:
            self.results['artist_tracks'].setdefault(track + "[" + label + "]" if label else track,[]).append((dj,setlist_url))
        return