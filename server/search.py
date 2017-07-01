from crawler.search import SearchCrawler
import json
import psycopg2
from psycopg2.extras import RealDictCursor

'''TODO: Improve search handling to use PostgreSQL trigrams, making top search result the assumption
         and secondary search results suggestions.'''
class Search:
    def __init__(self, search_input):
        sc = SearchCrawler()
        self.search_input = search_input.title()
        self.search_term = sc.get_api_search_url(search_input)
        self.results = {'artist_tracks': {}, 'dj_tracks': [], 'djs_by_setlist': {}}
        db = json.load(open("db.json"))
        conn = psycopg2.connect(database=db['database'], user=db['username'], password=db['password'], host=db['host'])
        self.cur = conn.cursor(cursor_factory=RealDictCursor)
        self.get_dj_tracks()
        self.get_artist_tracks()
        return

    def get_dj_tracks(self):
        sql = """SELECT DISTINCT setspy_api_artist.name as artist, setspy_api_track.title FROM setspy_api_track
                 JOIN setspy_api_artist ON setspy_api_track.artist_id = setspy_api_artist.id
                 WHERE setspy_api_track.id IN (SELECT track_id FROM setspy_api_track_setlist_link
                 WHERE setlist_id IN (SELECT id from setspy_api_setlist WHERE dj_id =
                 (SELECT id FROM setspy_api_dj WHERE name = 'Helena Hauff')))
                 ORDER BY setspy_api_artist.name;"""
        self.cur.execute(sql, (self.search_term,))
        self.results['dj_tracks'] = self.cur.fetchall();
        return

    def get_artist_tracks(self):
        sql = """SELECT setspy_api_track.title as track, array_agg(DISTINCT setspy_api_setlist.title ORDER BY setspy_api_setlist.title) as setlist_urls FROM setspy_api_track
                JOIN setspy_api_artist ON setspy_api_track.artist_id = setspy_api_artist.id
                JOIN setspy_api_track_setlist_link on setspy_api_track_setlist_link.track_id = setspy_api_track.id
                JOIN setspy_api_setlist on setspy_api_setlist.id = setspy_api_track_setlist_link.setlist_id
                JOIN setspy_api_dj on setspy_api_dj.id = setspy_api_setlist.dj_id
                WHERE setspy_api_artist.name = %s GROUP BY track ORDER BY track;"""
        self.cur.execute(sql, (self.search_input,))
        self.results['artist_tracks'] = self.cur.fetchall()
        #.title should be .url was originally
        sql = """SELECT DISTINCT setspy_api_setlist.title, array_agg(DISTINCT setspy_api_dj.name ORDER BY setspy_api_dj.name) as djs FROM setspy_api_setlist
                JOIN setspy_api_dj on setspy_api_dj.id = setspy_api_setlist.dj_id
                JOIN setspy_api_track_setlist_link on setspy_api_track_setlist_link.setlist_id = setspy_api_setlist.id
                JOIN setspy_api_track on setspy_api_track.id = setspy_api_track_setlist_link.track_id
                JOIN setspy_api_artist ON setspy_api_track.artist_id = setspy_api_artist.id
                WHERE setspy_api_artist.name = %s GROUP BY setspy_api_setlist.title;"""
        self.cur.execute(sql, (self.search_input,))
        setlist_data = self.cur.fetchall()
        for setlist_data in setlist_data:
            url = setlist_data['title'] #should be url
            self.results['djs_by_setlist'][url] = ", ".join(setlist_data['djs']) + " (" + url[25:29] + ")"
        return
