from crawler.search import SearchCrawler
import json
import psycopg2
from psycopg2.extras import RealDictCursor

'''TODO: Improve search handling to use PostgreSQL trigrams, making top search result the assumption
         and secondary search results suggestions.'''
class Search:
    def __init__(self, search_input):
        sc = SearchCrawler()
        self.search_input = search_input
        self.search_term = sc.get_api_search_url(search_input)
        self.results = {'artist_tracks': {}, 'dj_tracks': [], 'djs_by_setlist': {}}
        db = json.load(open("db.json"))
        conn = psycopg2.connect(database=db['database'], user=db['username'], password=db['password'], host=db['host'])
        self.cur = conn.cursor(cursor_factory=RealDictCursor)
        self.get_dj_tracks()
        self.get_artist_tracks()
        return

    def get_dj_tracks(self):
        sql = """SELECT DISTINCT artist.name as artist, track.title, label.name as label FROM track
                 JOIN artist ON track.artist_id = artist.id
                 LEFT JOIN label ON track.label_id = label.id
                 WHERE track.id IN (SELECT track_id FROM track_setlist_link
                 WHERE setlist_id IN (SELECT id from setlist WHERE dj_id =
                 (SELECT id FROM dj WHERE name = %s)))
                 ORDER BY artist.name;"""
        self.cur.execute(sql, (self.search_term,))
        self.results['dj_tracks'] = self.cur.fetchall();
        return

    def get_artist_tracks(self):
        sql = """SELECT track.title as track, array_agg(DISTINCT setlist.url ORDER BY setlist.url) as setlist_urls FROM track
                JOIN artist ON track.artist_id = artist.id
                JOIN track_setlist_link on track_setlist_link.track_id = track.id
                JOIN setlist on setlist.id = track_setlist_link.setlist_id
                JOIN dj on dj.id = setlist.dj_id
                WHERE artist.name = %s GROUP BY track ORDER BY track;"""
        self.cur.execute(sql, (self.search_input,))
        self.results['artist_tracks'] = self.cur.fetchall()
        sql = """SELECT DISTINCT setlist.url, array_agg(DISTINCT dj.name ORDER BY dj.name) as djs FROM setlist
                JOIN dj on dj.id = setlist.dj_id
                JOIN track_setlist_link on track_setlist_link.setlist_id = setlist.id
                JOIN track on track.id = track_setlist_link.track_id
                JOIN artist ON track.artist_id = artist.id
                WHERE artist.name = %s GROUP BY setlist.url;"""
        self.cur.execute(sql, (self.search_input,))
        setlist_data = self.cur.fetchall()
        for setlist_data in setlist_data:
            url = setlist_data['url']
            self.results['djs_by_setlist'][url] = ", ".join(setlist_data['djs']) + " (" + url[25:29] + ")"
        return
